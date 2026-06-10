from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

from isaaclab.app import AppLauncher


TASK_BY_STAGE = {
    "plane": "Isaac-MT4-Coordinate-Plane-Direct-v0",
    "sphere": "Isaac-MT4-Coordinate-Sphere-Direct-v0",
    "volume": "Isaac-MT4-Coordinate-Volume-Direct-v0",
}
FACE_NAMES = (
    "camera_plane",
    "x_max_front",
    "y_min_left",
    "y_max_right",
    "z_min_bottom",
    "z_max_top",
)

PROJECT_DIR = Path.home() / "work/robotarm/robotarm_student"
sys.path.append(str(PROJECT_DIR / "source"))

parser = argparse.ArgumentParser(description="Open the MT4 coordinate-plane curriculum scene in Isaac Lab.")
parser.add_argument("--stage", choices=sorted(TASK_BY_STAGE), default="plane")
parser.add_argument("--task", default=None, help="Override the Gym task id.")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--duration", type=float, default=120.0)
parser.add_argument("--target_interval", type=float, default=2.0)
parser.add_argument("--region_jitter", type=float, default=0.0)
parser.add_argument("--scripted_motion", action=argparse.BooleanOptionalAction, default=True)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import mt4_reach_direct  # noqa: F401, E402
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg  # noqa: E402


def scripted_action(t: float, num_envs: int, device: str) -> torch.Tensor:
    action = torch.zeros((num_envs, 5), device=device)
    action[:, 0] = 0.60 * math.sin(0.75 * t)
    action[:, 1] = 0.30 * math.sin(0.55 * t + 0.30)
    action[:, 2] = 0.35 * math.sin(0.70 * t + 1.10)
    action[:, 3] = 0.30 * math.sin(0.90 * t + 1.80)
    action[:, 4] = 0.25 * math.sin(0.65 * t + 0.60)
    return action


def print_region_state(env, elapsed: float):
    unwrapped = env.unwrapped
    region_number = int(unwrapped.region_ids[0].item()) + 1
    face_id = int(unwrapped.face_ids[0].item())
    target = unwrapped.target_pos[0].detach().cpu().tolist()
    target_visible = bool(unwrapped.target_stereo_visible[0].item())
    print(
        "[INFO] "
        f"t={elapsed:6.2f}s "
        f"region={region_number:02d}/{unwrapped.total_regions} "
        f"face={FACE_NAMES[face_id]} "
        f"target=({target[0]:.3f}, {target[1]:.3f}, {target[2]:.3f}) "
        f"target_stereo_visible={target_visible}",
        flush=True,
    )


def main() -> int:
    task = args.task if args.task is not None else TASK_BY_STAGE[args.stage]
    env_cfg = parse_env_cfg(
        task,
        device=args.device if args.device is not None else "cuda:0",
        num_envs=args.num_envs,
        use_fabric=False,
    )
    env_cfg.episode_length_s = max(args.duration, 1.0)
    if hasattr(env_cfg, "region_target_jitter_fraction"):
        env_cfg.region_target_jitter_fraction = args.region_jitter
    env = gym.make(task, cfg=env_cfg)
    env.reset()

    unwrapped = env.unwrapped
    unwrapped.sim.set_camera_view(eye=[0.56, -0.58, 0.42], target=[0.24, 0.0, 0.13])

    print(f"[INFO] Running {task}", flush=True)
    print("[INFO] Green marker is the sampled target. Blue marker appears on success.", flush=True)
    print(
        "[INFO] Policy observation includes body stereo projections plus a gripper-mounted camera projection.",
        flush=True,
    )
    if args.stage in ("plane", "volume") and args.target_interval > 0.0:
        print(
            f"[INFO] Viewer advances to the next numbered region every {args.target_interval:.1f}s.",
            flush=True,
        )
    unwrapped._compute_intermediate_values()
    print_region_state(env, 0.0)

    actions = torch.zeros((args.num_envs, unwrapped.cfg.action_space), device=unwrapped.device)
    start = time.time()
    next_target_time = args.target_interval
    while simulation_app.is_running() and time.time() - start < args.duration:
        elapsed = time.time() - start
        if args.scripted_motion:
            actions = scripted_action(elapsed, args.num_envs, unwrapped.device)
        env.step(actions)
        if args.stage in ("plane", "volume") and args.target_interval > 0.0 and elapsed >= next_target_time:
            env_ids = torch.arange(args.num_envs, device=unwrapped.device)
            unwrapped._sample_targets(env_ids)
            unwrapped._compute_intermediate_values()
            print_region_state(env, elapsed)
            next_target_time += args.target_interval

    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
