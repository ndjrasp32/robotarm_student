from __future__ import annotations

import argparse
import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tensorboard.backend.event_processing import event_accumulator


PROJECT_DIR = Path.home() / "work/robotarm/robotarm_student"
LOG_ROOT = Path.home() / "work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct"
PLOTS_DIR = PROJECT_DIR / "logs/plots"
EXPERIMENTS_DIR = PROJECT_DIR / "experiments"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create bilingual coordinate-curriculum plots and a student report.")
    parser.add_argument("--run-dir", type=Path, default=None, help="Isaac Lab run directory. Defaults to latest run.")
    parser.add_argument("--label", default="coordinate_region_mastery_extended", help="Report and plot snapshot label.")
    parser.add_argument("--training-command", default="", help="Command used for the run.")
    parser.add_argument("--training-time-seconds", type=float, default=None, help="Wall-clock training time.")
    parser.add_argument("--video-path", default="", help="Copied training or play video path.")
    parser.add_argument("--previous-report", default="", help="Previous report used as baseline comparison.")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip().lower()).strip("_")
    return slug or "coordinate_report"


def parse_checkpoint_iter(path: Path) -> int:
    match = re.search(r"model_(\d+)\.pt$", path.name)
    return int(match.group(1)) if match else -1


def latest_run_dir() -> Path:
    candidates = [path for path in LOG_ROOT.iterdir() if path.is_dir()]
    if not candidates:
        raise SystemExit(f"[ERROR] no coordinate curriculum runs under {LOG_ROOT}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def load_events(run_dir: Path) -> event_accumulator.EventAccumulator:
    event_files = sorted(run_dir.glob("events.out.tfevents.*"))
    if not event_files:
        raise SystemExit(f"[ERROR] no tensorboard event files in {run_dir}")
    ea = event_accumulator.EventAccumulator(str(run_dir))
    ea.Reload()
    return ea


def series(ea: event_accumulator.EventAccumulator, tag: str) -> tuple[list[int], list[float]]:
    events = ea.Scalars(tag)
    return [event.step for event in events], [event.value for event in events]


def find_tags(tags: list[str], needles: list[str]) -> list[str]:
    found: list[str] = []
    for tag in tags:
        low = tag.lower()
        if any(needle.lower() in low for needle in needles):
            found.append(tag)
    return found


def latest_value(ea: event_accumulator.EventAccumulator, tag: str | None) -> float | None:
    if tag is None:
        return None
    values = ea.Scalars(tag)
    if not values:
        return None
    return float(values[-1].value)


def find_one(tags: list[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        for tag in tags:
            if candidate.lower() == tag.lower():
                return tag
        for tag in tags:
            if candidate.lower() in tag.lower():
                return tag
    return None


def plot_group(
    ea: event_accumulator.EventAccumulator,
    tags: list[str],
    title: str,
    needles: list[str],
    out_path: Path,
) -> bool:
    matched = find_tags(tags, needles)
    if not matched:
        return False

    plt.figure(figsize=(11, 5.8))
    plotted = 0
    for tag in matched:
        xs, ys = series(ea, tag)
        if not xs:
            continue
        label = tag.replace("coordinate_curriculum/plane_localization_", "")
        plt.plot(xs, ys, label=label)
        plotted += 1

    if plotted == 0:
        plt.close()
        return False

    plt.title(title)
    plt.xlabel("training step")
    plt.ylabel("value")
    plt.grid(True, alpha=0.35)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return True


def read_region_mastery(run_dir: Path) -> list[dict[str, str]]:
    mastery_path = run_dir / "region_mastery.csv"
    if not mastery_path.exists():
        return []
    with mastery_path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def plot_region_mastery(rows: list[dict[str, str]], out_path: Path) -> bool:
    if not rows:
        return False
    regions = [int(row["region_number"]) for row in rows]
    counts = [int(row["success_count"]) for row in rows]
    mastered = [row["mastered"] == "1" for row in rows]
    colors = ["#2a9d8f" if value else "#8d99ae" for value in mastered]

    plt.figure(figsize=(9, 5))
    plt.bar(regions, counts, color=colors)
    plt.axhline(10, color="#d62828", linestyle="--", linewidth=1.2, label="mastery threshold")
    plt.title("Coordinate Region Mastery Counts")
    plt.xlabel("region number")
    plt.ylabel("strict 1 cm successes")
    plt.xticks(regions)
    plt.grid(True, axis="y", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return True


def markdown_path(path: Path) -> str:
    return str(path.relative_to(PROJECT_DIR))


def format_value(value: float | None, digits: int = 4) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "not recorded"
    minutes = int(seconds // 60)
    remainder = seconds - minutes * 60
    return f"{seconds:.2f} seconds ({minutes}m {remainder:.2f}s)"


def write_checkpoint_summary(run_dir: Path, out_path: Path) -> Path | None:
    checkpoints = sorted(run_dir.glob("model_*.pt"), key=parse_checkpoint_iter)
    if not checkpoints:
        return None
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["checkpoint", "iteration", "path"], lineterminator="\n")
        writer.writeheader()
        for checkpoint in checkpoints:
            writer.writerow(
                {
                    "checkpoint": checkpoint.name,
                    "iteration": parse_checkpoint_iter(checkpoint),
                    "path": str(checkpoint),
                }
            )
    return checkpoints[-1]


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir if args.run_dir is not None else latest_run_dir()
    run_dir = run_dir.expanduser().resolve()
    ea = load_events(run_dir)
    tags = ea.Tags().get("scalars", [])

    timestamp = run_dir.name.replace("-", "").replace("_", "_").replace(":", "")
    snapshot_name = f"{timestamp}_{slugify(args.label)}"
    snapshot_dir = PLOTS_DIR / snapshot_name
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    plots: dict[str, Path] = {}
    plot_specs = {
        "reward": ["Train/mean_reward", "mean_reward"],
        "success": [
            "success_rate",
            "center_success_radius_rate",
            "center_1cm_rate",
            "center_3cm_rate",
            "fine_center_radius_rate",
            "fine_center_4cm_rate",
            "near_center_radius_rate",
            "near_center_7cm_rate",
            "strict_region_center_success_rate",
        ],
        "region_progress": ["active_region_number", "mastered_region_count"],
        "distance": ["mean_distance", "mean_plane_error", "mean_workspace_entry_error", "mean_target_overshoot"],
        "camera": [
            "mean_camera_region_error",
            "camera_region_entry_rate",
            "mean_camera_alignment_error",
            "mean_gripper_camera_target_error",
            "mean_gripper_camera_direction_error",
            "mean_preferred_approach_error",
            "target_gripper_camera_visible_rate",
            "target_three_camera_visible_rate",
            "three_camera_ready_rate",
        ],
        "visibility": ["stereo_visible_rate", "inside_workspace_rate"],
        "per_region": ["region_", "success_count", "batch_success_rate"],
    }
    for name, needles in plot_specs.items():
        out_path = snapshot_dir / f"mt4_coordinate_{name}.png"
        if plot_group(ea, tags, f"MT4 Coordinate Curriculum: {name}", needles, out_path):
            plots[name] = out_path

    mastery_rows = read_region_mastery(run_dir)
    mastery_plot = snapshot_dir / "mt4_coordinate_region_mastery_counts.png"
    if plot_region_mastery(mastery_rows, mastery_plot):
        plots["region_mastery_counts"] = mastery_plot
        shutil.copy2(run_dir / "region_mastery.csv", snapshot_dir / "region_mastery.csv")

    latest_checkpoint = write_checkpoint_summary(run_dir, snapshot_dir / "mt4_coordinate_checkpoints.csv")

    metric_tags = {
        "mean_reward": find_one(tags, ["Train/mean_reward", "mean_reward"]),
        "success_rate": find_one(tags, ["coordinate_curriculum/plane_localization_success_rate"]),
        "center_success_radius_rate": find_one(
            tags,
            [
                "coordinate_curriculum/plane_localization_center_success_radius_rate",
                "coordinate_curriculum/plane_localization_center_1cm_rate",
            ],
        ),
        "center_1cm_rate": find_one(
            tags,
            [
                "coordinate_curriculum/plane_localization_center_1cm_rate",
                "coordinate_curriculum/plane_localization_center_3cm_rate",
            ],
        ),
        "fine_center_4cm_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_fine_center_4cm_rate"]
        ),
        "fine_center_radius_rate": find_one(
            tags,
            [
                "coordinate_curriculum/plane_localization_fine_center_radius_rate",
                "coordinate_curriculum/plane_localization_fine_center_4cm_rate",
            ],
        ),
        "near_center_7cm_rate": find_one(tags, ["coordinate_curriculum/plane_localization_near_center_7cm_rate"]),
        "near_center_radius_rate": find_one(
            tags,
            [
                "coordinate_curriculum/plane_localization_near_center_radius_rate",
                "coordinate_curriculum/plane_localization_near_center_7cm_rate",
            ],
        ),
        "strict_region_center_success_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_strict_region_center_success_rate"]
        ),
        "mean_distance_m": find_one(tags, ["coordinate_curriculum/plane_localization_mean_distance"]),
        "camera_region_entry_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_camera_region_entry_rate"]
        ),
        "camera_region_match_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_camera_region_match_rate"]
        ),
        "target_estimate_error_m": find_one(
            tags, ["coordinate_curriculum/plane_localization_mean_target_estimate_error"]
        ),
        "target_overshoot_m": find_one(tags, ["coordinate_curriculum/plane_localization_mean_target_overshoot"]),
        "preferred_approach_error_m": find_one(
            tags, ["coordinate_curriculum/plane_localization_mean_preferred_approach_error"]
        ),
        "gripper_camera_direction_error": find_one(
            tags, ["coordinate_curriculum/plane_localization_mean_gripper_camera_direction_error"]
        ),
        "inside_workspace_rate": find_one(tags, ["coordinate_curriculum/plane_localization_inside_workspace_rate"]),
        "target_stereo_visible_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_target_stereo_visible_rate"]
        ),
        "target_gripper_camera_visible_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_target_gripper_camera_visible_rate"]
        ),
        "target_three_camera_visible_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_target_three_camera_visible_rate"]
        ),
        "three_camera_ready_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_three_camera_ready_rate"]
        ),
        "gripper_stereo_visible_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_gripper_stereo_visible_rate"]
        ),
        "active_region_number": find_one(tags, ["coordinate_curriculum/plane_localization_active_region_number"]),
        "mastered_region_count": find_one(tags, ["coordinate_curriculum/plane_localization_mastered_region_count"]),
    }
    metrics = {name: latest_value(ea, tag) for name, tag in metric_tags.items()}

    metrics_csv = snapshot_dir / "mt4_coordinate_final_metrics.csv"
    with metrics_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "tag", "value"], lineterminator="\n")
        writer.writeheader()
        for name, value in metrics.items():
            writer.writerow({"metric": name, "tag": metric_tags[name] or "", "value": "" if value is None else value})

    report_path = EXPERIMENTS_DIR / f"{snapshot_name}.md"
    mastered_count = int(metrics["mastered_region_count"] or 0)
    active_region = int(metrics["active_region_number"] or 0)
    final_distance_cm = (metrics["mean_distance_m"] or 0.0) * 100.0
    video_line = f"- Video: `{args.video_path}`" if args.video_path else "- Video: not copied yet"

    report_lines = [
        f"# {run_dir.name} 좌표 영역 마스터리 확장 학습 / Coordinate Region Mastery Extended Run",
        "",
        "## 목표 / Goal",
        "",
        "Stage 1 학습을 새 1cm 엄격 성공 조건으로 다시 실행한다. / Rerun Stage 1 with the new strict 1 cm success rule:",
        "",
        "- 목표와 같은 스테레오 카메라 영역에 진입 / same stereo camera region as the target",
        "- 그리퍼 중심이 영역 중심 목표에서 `0.010 m` 이내 / gripper center within `0.010 m` of the region center target",
        "- 목표를 지나친 뒤 돌아오는 움직임은 벌점으로 줄인다. / Penalize motion that passes beyond the target and comes back.",
        "- 가능하면 로봇 쪽이나 위쪽에서 목표로 접근한다. / Prefer approaching the target from the robot side or from above.",
        "- 목표와 그리퍼가 양쪽 가상 카메라에서 보임 / target and gripper visible from both virtual cameras",
        "",
        "## 실행 / Run",
        "",
        f"- Run directory: `{run_dir}`",
        f"- Training command: `{args.training_command or '(not provided)'}`",
        f"- Training time: {format_duration(args.training_time_seconds)}",
        f"- Final checkpoint: `{latest_checkpoint}`" if latest_checkpoint else "- Final checkpoint: none found",
        video_line,
        f"- Previous baseline: `{args.previous_report}`" if args.previous_report else "- Previous baseline: 2026-06-10 500-iteration Stage 1 result",
        "",
        "## 최종 지표 / Final Metrics",
        "",
        "| metric | value |",
        "| --- | ---: |",
        f"| mean_reward | {format_value(metrics['mean_reward'])} |",
        f"| success_rate | {format_value(metrics['success_rate'])} |",
        f"| center_success_radius_rate | {format_value(metrics['center_success_radius_rate'])} |",
        f"| center_1cm_rate | {format_value(metrics['center_1cm_rate'])} |",
        f"| fine_center_radius_rate | {format_value(metrics['fine_center_radius_rate'])} |",
        f"| fine_center_4cm_rate | {format_value(metrics['fine_center_4cm_rate'])} |",
        f"| near_center_radius_rate | {format_value(metrics['near_center_radius_rate'])} |",
        f"| near_center_7cm_rate | {format_value(metrics['near_center_7cm_rate'])} |",
        f"| strict_region_center_success_rate | {format_value(metrics['strict_region_center_success_rate'])} |",
        f"| mean_distance | {format_value(metrics['mean_distance_m'])} m ({final_distance_cm:.2f} cm) |",
        f"| camera_region_entry_rate | {format_value(metrics['camera_region_entry_rate'])} |",
        f"| camera_region_match_rate | {format_value(metrics['camera_region_match_rate'])} |",
        f"| target_estimate_error | {format_value(metrics['target_estimate_error_m'])} m |",
        f"| target_overshoot | {format_value(metrics['target_overshoot_m'])} m |",
        f"| preferred_approach_error | {format_value(metrics['preferred_approach_error_m'])} m |",
        f"| gripper_camera_direction_error | {format_value(metrics['gripper_camera_direction_error'])} |",
        f"| inside_workspace_rate | {format_value(metrics['inside_workspace_rate'])} |",
        f"| target_stereo_visible_rate | {format_value(metrics['target_stereo_visible_rate'])} |",
        f"| target_gripper_camera_visible_rate | {format_value(metrics['target_gripper_camera_visible_rate'])} |",
        f"| target_three_camera_visible_rate | {format_value(metrics['target_three_camera_visible_rate'])} |",
        f"| three_camera_ready_rate | {format_value(metrics['three_camera_ready_rate'])} |",
        f"| gripper_stereo_visible_rate | {format_value(metrics['gripper_stereo_visible_rate'])} |",
        f"| active_region_number | {active_region} |",
        f"| mastered_region_count | {mastered_count} |",
        "",
        "## 기준선 비교 / Baseline Comparison",
        "",
        "| run | iterations | mastered regions | active region | mean distance | note |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        "| previous baseline | 500 | 2 | 3 | 0.0821 m | 3번 영역 마스터 전 정지 / stopped before region 3 mastery |",
        "| previous extended baseline | 1500 | 7 | 8 | 0.0534 m | 8번 영역에서 정지 / stopped at region 8 |",
        "| previous three-camera baseline | 1500 | 9 | 9 | 0.0545 m | 5회 성공 기준 / 5-success gate |",
        f"| this run | 1500 | {mastered_count} | {active_region} | {format_value(metrics['mean_distance_m'])} m | "
        "카메라 추정 목표 추적 보강 / camera-estimated target tracking update |",
        "",
    ]

    if mastery_rows:
        report_lines.extend(
            [
                "## 영역 마스터리 스냅샷 / Region Mastery Snapshot",
                "",
                "| Region | Success Count | Best Episode Reward | Mastered | Active |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in mastery_rows:
            report_lines.append(
                f"| {row['region_number']} | {row['success_count']} | {row['best_episode_reward']} | "
                f"{row['mastered']} | {row['active']} |"
            )
        report_lines.append("")

    report_lines.extend(["## 그래프 / Plots", ""])
    for name, path in plots.items():
        report_lines.extend([f"### {name}", "", f"![{name}](../{markdown_path(path)})", ""])

    report_lines.extend(
        [
            "## 학생 아이디어와 Codex 구현 / Student Idea vs. Codex Implementation",
            "",
            "사용자 제안 / User proposal:",
            "",
            "- 거리 기준은 `0.010 m`로 강화한다. / Tighten the distance criterion to `0.010 m`.",
            "- 추적 보상은 실제 로봇팔 그리퍼와 목표 지점 사이의 거리에 집중한다. / Focus tracking reward on the actual gripper-to-target distance.",
            "- 목표를 지나쳤다가 돌아오는 방식은 벌점으로 낮춘다. / Penalize overshooting the target and returning.",
            "- 가능한 접근 방향은 로봇 쪽 또는 위쪽에서 목표로 들어오게 한다. / Prefer target approach from the robot side or from above.",
            "- 성공을 하나의 전체 성공률이 아니라 번호가 붙은 영역 마스터리로 본다. / Treat success as numbered region mastery, not as one global success rate.",
            "- 한 정책을 영역에서 영역으로 이어서 학습하고, 영역별 최고 행동 기록을 보존한다. / Continue one policy from region to region and preserve the best behavior record per region.",
            "- 학생들이 실제 학습 장면과 결과를 볼 수 있도록 시각화한다. / Visualize the run so students can inspect what the agent actually learned.",
            "",
            "Codex 구현 / Codex implementation:",
            "",
            "- Stage 1 순차 좌표 영역 커리큘럼 학습을 실행했다. / Ran Stage 1 sequential coordinate-region curriculum training.",
            "- 타겟 생성 좌표와 정책 입력 영역을 분리했다. / Separated target-generation coordinates from the policy-input region.",
            "- 정책 입력의 영역 feature는 몸체 좌/우 스테레오 projection에서 추정한 영역으로 만들었다. / Built the policy-input region feature from the body left/right stereo projection.",
            "- 몸체 좌/우 스테레오 projection으로 추정한 목표 상대좌표를 정책 입력에 추가했다. / Added the body-stereo-estimated target-relative position to the policy observation.",
            "- 세 번째 그리퍼 카메라 projection을 관측과 보상 로그에 추가했다. / Added the third gripper-camera projection to observations and reward logs.",
            "- 목표 중심으로 가도록 보상 신호를 더 직접적으로 넣었다. / Added a more direct reward signal for moving to the target center.",
            "- 목표를 지나친 정도와 선호 접근 방향 오차를 로그로 남긴다. / Logged target overshoot and preferred approach error.",
            "- 랜덤 데모에서 목표를 바꾼 뒤 정책 관측도 즉시 새로 읽도록 수정했다. / Fixed the random demo so observations refresh immediately after a target override.",
            "- 엄격한 성공 조건을 3cm에서 1cm로 강화했다. / Tightened the strict success rule from 3 cm to 1 cm.",
            "- Gym `RecordVideo`로 학습 영상을 기록했다. / Recorded training video through Gym `RecordVideo`.",
            "- 좌표 전용 TensorBoard 그래프, 최종 지표 CSV, 체크포인트 CSV, 이 리포트를 생성했다. / Generated coordinate-specific TensorBoard plots, final metrics CSV, checkpoint CSV, and this report.",
            "",
            "## 해석 / Interpretation",
            "",
            "- 영역별 성공 횟수가 이 커리큘럼의 핵심 지표다. / Per-region success count is the key curriculum metric.",
            "- 이번 학습의 핵심 확인점은 목표가 바뀔 때 그리퍼가 같은 위치만 반복하지 않고 새 목표 중심으로 움직이는지다. / The key check is whether the gripper follows the new target center instead of repeating one position.",
            "- `camera_region_match_rate`는 생성된 정답 영역과 카메라 추정 영역의 일치 여부를 보여준다. / `camera_region_match_rate` shows whether the generated true region matches the camera-estimated region.",
            "- `target_estimate_error`는 카메라로 추정한 목표 위치가 실제 목표와 얼마나 가까운지 보여준다. / `target_estimate_error` shows how close the camera-estimated target point is to the true target.",
            "- 최종 `success_rate`는 마지막 로깅 배치 기준이라 영역별 누적 성공을 과소평가할 수 있다. / The final `success_rate` is batch-local and can understate cumulative per-region progress.",
            "- 거리 기준은 완화하지 않았다. 마스터된 모든 영역은 같은 1cm 엄격 조건으로 집계된다. / The distance criterion was not relaxed. Every mastered region is counted with the same 1 cm strict success rule.",
            "- 이번 수정의 목적은 실제 시연 접근 선택을 생성 좌표가 아니라 카메라 추정 영역에 의존하게 만드는 것이다. / This update makes demo approach selection depend on the camera-estimated region instead of generated coordinates.",
            "",
            f"Generated at `{datetime.now().isoformat(timespec='seconds')}`.",
            "",
        ]
    )
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    print("[OK] coordinate report generated")
    print(" run_dir       =", run_dir)
    print(" report        =", report_path)
    print(" snapshot_dir  =", snapshot_dir)
    print(" metrics_csv   =", metrics_csv)
    print(" latest_ckpt   =", latest_checkpoint)


if __name__ == "__main__":
    main()
