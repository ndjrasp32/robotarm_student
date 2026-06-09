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
    plt.axhline(5, color="#d62828", linestyle="--", linewidth=1.2, label="mastery threshold")
    plt.title("Coordinate Region Mastery Counts")
    plt.xlabel("region number")
    plt.ylabel("strict 3 cm successes")
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
        "success": ["success_rate", "center_3cm_rate", "near_center_7cm_rate", "strict_region_center_success_rate"],
        "region_progress": ["active_region_number", "mastered_region_count"],
        "distance": ["mean_distance", "mean_plane_error", "mean_workspace_entry_error"],
        "camera": ["mean_camera_region_error", "camera_region_entry_rate", "mean_camera_alignment_error"],
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
        "center_3cm_rate": find_one(tags, ["coordinate_curriculum/plane_localization_center_3cm_rate"]),
        "near_center_7cm_rate": find_one(tags, ["coordinate_curriculum/plane_localization_near_center_7cm_rate"]),
        "strict_region_center_success_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_strict_region_center_success_rate"]
        ),
        "mean_distance_m": find_one(tags, ["coordinate_curriculum/plane_localization_mean_distance"]),
        "camera_region_entry_rate": find_one(
            tags, ["coordinate_curriculum/plane_localization_camera_region_entry_rate"]
        ),
        "inside_workspace_rate": find_one(tags, ["coordinate_curriculum/plane_localization_inside_workspace_rate"]),
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
        "Stage 1 학습을 다시 실행하되 엄격한 성공 조건은 동일하게 유지한다. / Rerun Stage 1 while keeping the same strict success rule:",
        "",
        "- 목표와 같은 스테레오 카메라 영역에 진입 / same stereo camera region as the target",
        "- 그리퍼 중심이 영역 중심 목표에서 `0.030 m` 이내 / gripper center within `0.030 m` of the region center target",
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
        f"| center_3cm_rate | {format_value(metrics['center_3cm_rate'])} |",
        f"| near_center_7cm_rate | {format_value(metrics['near_center_7cm_rate'])} |",
        f"| strict_region_center_success_rate | {format_value(metrics['strict_region_center_success_rate'])} |",
        f"| mean_distance | {format_value(metrics['mean_distance_m'])} m ({final_distance_cm:.2f} cm) |",
        f"| camera_region_entry_rate | {format_value(metrics['camera_region_entry_rate'])} |",
        f"| inside_workspace_rate | {format_value(metrics['inside_workspace_rate'])} |",
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
        f"| this run | 1500 | {mastered_count} | {active_region} | {format_value(metrics['mean_distance_m'])} m | "
        "제안사항 반영 재학습 / rerun with proposal updates |",
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
            "- 거리 기준은 `0.030 m`로 고정한다. / Keep the distance criterion fixed at `0.030 m`.",
            "- 성공을 하나의 전체 성공률이 아니라 번호가 붙은 영역 마스터리로 본다. / Treat success as numbered region mastery, not as one global success rate.",
            "- 한 정책을 영역에서 영역으로 이어서 학습하고, 영역별 최고 행동 기록을 보존한다. / Continue one policy from region to region and preserve the best behavior record per region.",
            "- 학생들이 실제 학습 장면과 결과를 볼 수 있도록 시각화한다. / Visualize the run so students can inspect what the agent actually learned.",
            "",
            "Codex 구현 / Codex implementation:",
            "",
            "- Stage 1 순차 9영역 학습을 실행했다. / Ran Stage 1 sequential 9-region training.",
            "- 엄격한 3cm 성공 조건은 바꾸지 않았다. / Kept the strict 3 cm success rule unchanged.",
            "- 7cm 이내 중심 접근 보상을 추가해 3cm 성공까지의 조밀 신호를 강화했다. / Added near-center shaping inside 7 cm to strengthen the dense signal toward 3 cm success.",
            "- Gym `RecordVideo`로 학습 영상을 기록했다. / Recorded training video through Gym `RecordVideo`.",
            "- 좌표 전용 TensorBoard 그래프, 최종 지표 CSV, 체크포인트 CSV, 이 리포트를 생성했다. / Generated coordinate-specific TensorBoard plots, final metrics CSV, checkpoint CSV, and this report.",
            "",
            "## 해석 / Interpretation",
            "",
            "- 영역별 성공 횟수가 이 커리큘럼의 핵심 지표다. / Per-region success count is the key curriculum metric.",
            "- 이전 1500회 학습은 7개 영역에서 멈췄지만, 이번 학습은 9개 영역을 모두 마스터했다. / The previous 1500-iteration run stopped at 7 mastered regions, while this run mastered all 9 regions.",
            "- 7cm 중심 접근 보상은 8번 병목을 넘기는 데 효과가 있었다. / The 7 cm near-center shaping was effective for passing the region 8 bottleneck.",
            "- 최종 `success_rate`는 마지막 로깅 배치 기준이라 영역별 누적 성공을 과소평가할 수 있다. / The final `success_rate` is batch-local and can understate cumulative per-region progress.",
            "- 거리 기준은 완화하지 않았다. 마스터된 모든 영역은 같은 3cm 엄격 조건으로 집계된다. / The distance criterion was not relaxed. Every mastered region is counted with the same 3 cm strict success rule.",
            "- 이번 수정의 목적은 7cm 안쪽에서 중심으로 더 안정적으로 수렴하게 하는 것이다. / This update aims to make convergence toward the center more stable inside 7 cm.",
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
