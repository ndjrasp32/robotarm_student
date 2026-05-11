#!/usr/bin/env bash
set -euo pipefail

cd ~/work/isaac/src/IsaacLab
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Simplified-Reach-Direct-v0"

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] num_envs=128 max_iterations=1000 headless=true"

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations 1000 \
  --headless \
  "$@"
