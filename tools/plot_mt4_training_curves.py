from pathlib import Path
from tensorboard.backend.event_processing import event_accumulator
import matplotlib.pyplot as plt

log_root = Path.home() / "work/isaac/src/IsaacLab/logs/rsl_rl/mt4_simplified_reach_direct"
out_dir = Path.home() / "work/robotarm/mt4_isaac_lab_task/logs/plots"
out_dir.mkdir(parents=True, exist_ok=True)

event_files = sorted(log_root.rglob("events.out.tfevents.*"))

if not event_files:
    raise SystemExit(f"[ERROR] no tensorboard event files found under {log_root}")

print("[INFO] event files:")
for f in event_files[-5:]:
    print(" -", f)

# Use latest run by modified event file path
latest_event = event_files[-1]
run_dir = latest_event.parent
print("[INFO] using run:", run_dir)

ea = event_accumulator.EventAccumulator(str(run_dir))
ea.Reload()

tags = ea.Tags().get("scalars", [])
print("[INFO] scalar tags:")
for t in tags:
    print(" -", t)

def find_tags(keywords):
    found = []
    for t in tags:
        low = t.lower()
        if any(k.lower() in low for k in keywords):
            found.append(t)
    return found

groups = {
    "reward": find_tags(["reward", "mean_reward"]),
    "success": find_tags(["success"]),
    "distance": find_tags(["distance"]),
    "episode_length": find_tags(["episode_length", "length"]),
}

for group_name, group_tags in groups.items():
    if not group_tags:
        print(f"[WARN] no tags for {group_name}")
        continue

    plt.figure(figsize=(10, 5))

    plotted = 0
    for tag in group_tags:
        events = ea.Scalars(tag)
        if not events:
            continue

        xs = [e.step for e in events]
        ys = [e.value for e in events]

        plt.plot(xs, ys, label=tag)
        plotted += 1

    if plotted == 0:
        plt.close()
        continue

    plt.title(f"MT4 training curve: {group_name}")
    plt.xlabel("training step / iteration")
    plt.ylabel(group_name)
    plt.legend()
    plt.grid(True)

    out_path = out_dir / f"mt4_{group_name}_curve.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()

    print("[OK] wrote", out_path)
