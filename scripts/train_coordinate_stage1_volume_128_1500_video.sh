#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_student"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Coordinate-Volume-Direct-v0"
MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-1500}"
VIDEO_ARGS=()
if [[ "${MT4_RECORD_VIDEO:-1}" != "0" ]]; then
  VIDEO_ARGS=(
    --video
    --video_length "${MT4_VIDEO_LENGTH:-3600}"
    --video_interval "${MT4_VIDEO_INTERVAL:-12000}"
  )
fi

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 1: sequential three-camera region entry over 3x3x3 workspace cells"
echo "[INFO] region mastery requires 10 strict 1cm successes per volume cell"
echo "[INFO] reward includes target tracking, overshoot penalty, and preferred robot-side/above approach"
echo "[INFO] repo=${PROJECT_DIR}"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"
if [[ ${#VIDEO_ARGS[@]} -gt 0 ]]; then
  echo "[INFO] training video enabled length=${MT4_VIDEO_LENGTH:-3600} interval=${MT4_VIDEO_INTERVAL:-12000}"
fi

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/train_mt4_coordinate_curriculum.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  "${VIDEO_ARGS[@]}" \
  --run_name volume_3x3x3_target_tracking_128env_1500iter \
  "$@"
