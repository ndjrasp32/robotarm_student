from __future__ import annotations

import argparse
import csv
import math
import os
import random
import shutil
import sys
from datetime import datetime
from pathlib import Path

from isaaclab.app import AppLauncher


PROJECT_DIR = Path.home() / "work/robotarm/robotarm_student"
ISAACLAB_DIR = Path.home() / "work/isaac/src/IsaacLab"
RSL_RL_SCRIPT_DIR = ISAACLAB_DIR / "scripts/reinforcement_learning/rsl_rl"
sys.path.append(str(RSL_RL_SCRIPT_DIR))
sys.path.append(str(PROJECT_DIR / "source"))

import cli_args  # isort: skip  # noqa: E402


parser = argparse.ArgumentParser(description="Record a 9-region random target demo with a trained MT4 policy.")
parser.add_argument("--task", default="Isaac-MT4-Coordinate-Plane-Direct-v0")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--video_length", type=int, default=7200, help="Video length in simulation steps.")
parser.add_argument("--target_interval_steps", type=int, default=360, help="Steps per displayed region target.")
parser.add_argument("--sequence_seed", type=int, default=42)
parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment.")
parser.add_argument("--output_dir", type=Path, default=PROJECT_DIR / "logs/videos")
parser.add_argument("--prefix", default=None)
parser.add_argument(
    "--agent", type=str, default="rsl_rl_cfg_entry_point", help="Name of the RL agent configuration entry point."
)
cli_args.add_rsl_rl_args(parser)
AppLauncher.add_app_launcher_args(parser)
args_cli, hydra_args = parser.parse_known_args()
args_cli.enable_cameras = True

sys.argv = [sys.argv[0]] + hydra_args

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import gymnasium as gym  # noqa: E402
import torch  # noqa: E402
from rsl_rl.runners import DistillationRunner, OnPolicyRunner  # noqa: E402

from isaaclab.envs import DirectMARLEnv, DirectRLEnvCfg, ManagerBasedRLEnvCfg, multi_agent_to_single_agent  # noqa: E402
from isaaclab.utils.assets import retrieve_file_path  # noqa: E402
from isaaclab.utils.dict import print_dict  # noqa: E402
from isaaclab_rl.rsl_rl import RslRlBaseRunnerCfg, RslRlVecEnvWrapper, handle_deprecated_rsl_rl_cfg  # noqa: E402

import importlib.metadata as metadata  # noqa: E402
import isaaclab_tasks  # noqa: F401, E402
import mt4_reach_direct  # noqa: F401, E402
from isaaclab_tasks.utils import get_checkpoint_path  # noqa: E402
from isaaclab_tasks.utils.hydra import hydra_task_config  # noqa: E402


INSTALLED_RSL_RL_VERSION = metadata.version("rsl-rl-lib")


def build_region_sequence(total_steps: int, interval_steps: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    segment_count = max(1, math.ceil(total_steps / max(interval_steps, 1)))
    sequence: list[int] = []
    while len(sequence) < segment_count:
        cycle = list(range(9))
        rng.shuffle(cycle)
        sequence.extend(cycle)
    return sequence[:segment_count]


def set_region_target(base_env, region_id: int) -> None:
    env_ids = torch.arange(base_env.num_envs, device=base_env.device)
    region_ids = torch.full((base_env.num_envs,), region_id, dtype=torch.long, device=base_env.device)
    target = base_env._front_face_region_centers(region_ids)
    face_ids = torch.zeros((base_env.num_envs,), dtype=torch.long, device=base_env.device)

    base_env.target_pos[env_ids] = target
    base_env.face_ids[env_ids] = face_ids
    base_env.region_ids[env_ids] = region_ids
    base_env.face_one_hot[env_ids] = torch.nn.functional.one_hot(face_ids, num_classes=6).float()
    base_env.region_features[env_ids] = base_env._region_features(region_ids)
    base_env._compute_intermediate_values()
    base_env._update_markers()


def write_sequence_csv(path: Path, sequence: list[int], interval_steps: int, step_dt: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["segment", "start_s", "end_s", "region_number"])
        for i, region_id in enumerate(sequence):
            start_s = i * interval_steps * step_dt
            end_s = (i + 1) * interval_steps * step_dt
            writer.writerow([i + 1, f"{start_s:.3f}", f"{end_s:.3f}", region_id + 1])


def copy_recorded_video(video_folder: Path, output_path: Path) -> Path:
    candidates = sorted(video_folder.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise RuntimeError(f"No mp4 was recorded under {video_folder}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidates[-1], output_path)
    return output_path


@hydra_task_config(args_cli.task, args_cli.agent)
def main(env_cfg: ManagerBasedRLEnvCfg | DirectRLEnvCfg, agent_cfg: RslRlBaseRunnerCfg) -> None:
    agent_cfg = cli_args.update_rsl_rl_cfg(agent_cfg, args_cli)
    agent_cfg = handle_deprecated_rsl_rl_cfg(agent_cfg, INSTALLED_RSL_RL_VERSION)
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    env_cfg.region_target_jitter_fraction = 0.0
    env_cfg.master_regions_sequentially = False
    env_cfg.sequential_region_targets = False
    env_cfg.episode_length_s = max(
        float(args_cli.target_interval_steps) * float(env_cfg.sim.dt) * float(env_cfg.decimation),
        1.0,
    )

    log_root_path = os.path.abspath(os.path.join("logs", "rsl_rl", agent_cfg.experiment_name))
    if args_cli.checkpoint:
        resume_path = retrieve_file_path(args_cli.checkpoint)
    else:
        resume_path = get_checkpoint_path(log_root_path, agent_cfg.load_run, agent_cfg.load_checkpoint)
    env_cfg.log_dir = os.path.dirname(resume_path)

    stamp = args_cli.prefix or datetime.now().strftime("%Y%m%d_%H%M%S_coordinate_random_region_demo")
    raw_video_dir = args_cli.output_dir / f"{stamp}_raw"
    output_video = args_cli.output_dir / f"{stamp}.mp4"
    sequence_csv = args_cli.output_dir / f"{stamp}_sequence.csv"

    env = gym.make(args_cli.task, cfg=env_cfg, render_mode="rgb_array")
    if isinstance(env.unwrapped, DirectMARLEnv):
        env = multi_agent_to_single_agent(env)
    base_env = env.unwrapped
    base_env.sim.set_camera_view(eye=[0.56, -0.58, 0.42], target=[0.24, 0.0, 0.13])

    video_kwargs = {
        "video_folder": str(raw_video_dir),
        "step_trigger": lambda step: step == 0,
        "video_length": args_cli.video_length,
        "disable_logger": True,
    }
    print("[INFO] Recording random-region policy demo.")
    print_dict(video_kwargs, nesting=4)
    env = gym.wrappers.RecordVideo(env, **video_kwargs)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    if agent_cfg.class_name == "OnPolicyRunner":
        runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    elif agent_cfg.class_name == "DistillationRunner":
        runner = DistillationRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    else:
        raise ValueError(f"Unsupported runner class: {agent_cfg.class_name}")

    print(f"[INFO] Loading model checkpoint from: {resume_path}")
    runner.load(resume_path)
    policy = runner.get_inference_policy(device=base_env.device)

    sequence = build_region_sequence(args_cli.video_length, args_cli.target_interval_steps, args_cli.sequence_seed)
    write_sequence_csv(sequence_csv, sequence, args_cli.target_interval_steps, base_env.step_dt)
    print("[INFO] Region sequence:", " ".join(str(region_id + 1) for region_id in sequence))

    set_region_target(base_env, sequence[0])
    obs = env.get_observations()
    current_segment = 0
    for timestep in range(args_cli.video_length):
        if not simulation_app.is_running():
            break
        segment = min(timestep // args_cli.target_interval_steps, len(sequence) - 1)
        if segment != current_segment:
            current_segment = segment
            set_region_target(base_env, sequence[current_segment])
            obs = env.get_observations()

        with torch.inference_mode():
            actions = policy(obs)
            obs, _, dones, _ = env.step(actions)
            set_region_target(base_env, sequence[current_segment])
            if hasattr(policy, "reset"):
                policy.reset(dones)
            elif hasattr(runner.alg, "policy") and hasattr(runner.alg.policy, "reset"):
                runner.alg.policy.reset(dones)
            elif hasattr(runner.alg, "actor_critic") and hasattr(runner.alg.actor_critic, "reset"):
                runner.alg.actor_critic.reset(dones)
            if torch.any(dones):
                obs = env.get_observations()

    env.close()
    copied = copy_recorded_video(raw_video_dir, output_video)
    print(f"[OK] demo_video={copied}")
    print(f"[OK] sequence_csv={sequence_csv}")


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
