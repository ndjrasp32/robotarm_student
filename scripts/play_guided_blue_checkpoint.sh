#!/usr/bin/env bash
set -euo pipefail

cd ~/work/isaac/src/IsaacLab
unset CMEEL_PREFIX
export DISPLAY=:1
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Simplified-Reach-Direct-v0"
CHECKPOINT_FILE="${HOME}/work/robotarm/mt4_isaac_lab_task/logs/plots/guided_blue_checkpoint.txt"

if [[ ! -s "${CHECKPOINT_FILE}" ]]; then
  echo "[ERROR] guided_blue_checkpoint.txt was not found or is empty."
  echo "        Expected path: ${CHECKPOINT_FILE}"
  echo "        Run guided-blue training and record the guided-progress checkpoint first."
  exit 1
fi

CHECKPOINT="$(tr -d '\r\n' < "${CHECKPOINT_FILE}")"

if [[ ! -f "${CHECKPOINT}" ]]; then
  echo "[ERROR] The guided-blue checkpoint does not exist:"
  echo "        ${CHECKPOINT}"
  echo "        Refresh ${CHECKPOINT_FILE} with an existing checkpoint path."
  exit 1
fi

if command -v xdpyinfo >/dev/null 2>&1 && ! xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then
  echo "[WARN] DISPLAY=${DISPLAY} is not accessible from this shell."
  echo "       If you are using VNC, run this in the VNC terminal first:"
  echo "       xhost +SI:localuser:${USER}"
  echo "       Then run this script again from the same user/session."
fi

echo "[INFO] Playing guided-blue checkpoint for ${TASK_NAME}"
echo "[INFO] checkpoint=${CHECKPOINT}"

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py \
  --task "${TASK_NAME}" \
  --checkpoint "${CHECKPOINT}" \
  "$@"
