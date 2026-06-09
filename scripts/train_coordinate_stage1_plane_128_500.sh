#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_student"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Coordinate-Plane-Direct-v0"
MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-1500}"
VIDEO_ARGS=()
if [[ "${MT4_RECORD_VIDEO:-1}" != "0" ]]; then
  VIDEO_ARGS=(
    --video
    --video_length "${MT4_VIDEO_LENGTH:-240}"
    --video_interval "${MT4_VIDEO_INTERVAL:-12000}"
  )
fi

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 1: sequential stereo camera-region entry over 9 camera-plane workspace cells"
echo "[INFO] repo=${PROJECT_DIR}"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"
if [[ ${#VIDEO_ARGS[@]} -gt 0 ]]; then
  echo "[INFO] training video enabled length=${MT4_VIDEO_LENGTH:-240} interval=${MT4_VIDEO_INTERVAL:-12000}"
fi

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/train_mt4_coordinate_curriculum.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  "${VIDEO_ARGS[@]}" \
  "$@"
