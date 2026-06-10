#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_student"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
BASE_RUN="${MT4_PRECISION_LOAD_RUN:-2026-06-10_16-47-53_volume_3x3x3_target_tracking_128env_1500iter}"
BASE_CHECKPOINT="${MT4_PRECISION_LOAD_CHECKPOINT:-model_1499.pt}"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Coordinate-Volume-Precision-Direct-v0"
MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-800}"
VIDEO_ARGS=()
if [[ "${MT4_RECORD_VIDEO:-1}" != "0" ]]; then
  VIDEO_ARGS=(
    --video
    --video_length "${MT4_VIDEO_LENGTH:-3600}"
    --video_interval "${MT4_VIDEO_INTERVAL:-12000}"
  )
fi

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 2: warm-started 5mm precision control inside the reach-limited 3x3x3 workspace"
echo "[INFO] warm start load_run=${BASE_RUN} checkpoint=${BASE_CHECKPOINT}"
echo "[INFO] success requires same 3D cell, body stereo visibility, gripper camera visibility, and 5mm center distance"
echo "[INFO] action_scale=0.015, center_success_radius=0.005, fine_center_radius=0.020"
echo "[INFO] repo=${PROJECT_DIR}"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/train_mt4_coordinate_curriculum.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  --resume \
  --load_run "${BASE_RUN}" \
  --checkpoint "${BASE_CHECKPOINT}" \
  "${VIDEO_ARGS[@]}" \
  --run_name volume_precision_5mm_128env_800iter \
  "$@"
