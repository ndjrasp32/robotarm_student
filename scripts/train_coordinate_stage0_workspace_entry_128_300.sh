#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_student"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Coordinate-Workspace-Entry-Direct-v0"
MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-300}"

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 0: enter the camera-visible workspace cube from home"
echo "[INFO] repo=${PROJECT_DIR}"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/train_mt4_coordinate_curriculum.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  "$@"
