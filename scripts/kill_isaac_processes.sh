#!/usr/bin/env bash
set -euo pipefail

cd ~/work/isaac/src/IsaacLab
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

echo "[INFO] Stopping Isaac Lab / Isaac Sim processes owned by ${USER}..."

patterns=(
  "isaaclab.sh"
  "scripts/reinforcement_learning/rsl_rl/train.py"
  "scripts/reinforcement_learning/rsl_rl/play.py"
  "kit/kit"
  "omni.kit"
  "isaac-sim"
  "Isaac Sim"
)

found=0
for pattern in "${patterns[@]}"; do
  if pgrep -u "${USER}" -f "${pattern}" >/dev/null 2>&1; then
    found=1
    echo "[INFO] pkill -f ${pattern}"
    pkill -u "${USER}" -f "${pattern}" || true
  fi
done

if [[ "${found}" -eq 0 ]]; then
  echo "[OK] No matching Isaac processes were running."
else
  sleep 2
  echo "[OK] Kill signal sent. Remaining matching processes, if any:"
  ps -u "${USER}" -o pid=,comm=,args= | grep -E "isaaclab.sh|rsl_rl/(train|play)\\.py|kit/kit|omni\\.kit|isaac-sim|Isaac Sim" | grep -v grep || true
fi
