#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_student"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
LOG_ROOT="${HOME}/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

CHECKPOINT="${1:-}"
if [[ -z "${CHECKPOINT}" ]]; then
  CHECKPOINT="$(find "${LOG_ROOT}" -name 'model_*.pt' -type f -printf '%T@ %p\n' | sort -nr | awk 'NR==1 {print $2}')"
fi

if [[ -z "${CHECKPOINT}" || ! -f "${CHECKPOINT}" ]]; then
  echo "[ERROR] checkpoint not found: ${CHECKPOINT:-latest model_*.pt}"
  exit 1
fi

echo "[INFO] Recording coordinate policy video"
echo "[INFO] checkpoint=${CHECKPOINT}"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${ISAACLAB_DIR}/scripts/reinforcement_learning/rsl_rl/play.py" \
  --task Isaac-MT4-Coordinate-Plane-Direct-v0 \
  --num_envs "${MT4_PLAY_NUM_ENVS:-1}" \
  --checkpoint "${CHECKPOINT}" \
  --video \
  --video_length "${MT4_PLAY_VIDEO_LENGTH:-3600}" \
  --headless \
  --seed "${MT4_SEED:-42}"
