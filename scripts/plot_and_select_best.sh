#!/usr/bin/env bash
set -euo pipefail

cd ~/work/isaac/src/IsaacLab
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

TOOLS_DIR="${HOME}/work/robotarm/mt4_isaac_lab_task/tools"
BEST_FILE="${HOME}/work/robotarm/mt4_isaac_lab_task/logs/plots/best_checkpoint.txt"

echo "[INFO] Plotting MT4 training curves and checkpoint summaries..."
./isaaclab.sh -p "${TOOLS_DIR}/plot_mt4_training_and_checkpoints.py"

echo "[INFO] Selecting best MT4 checkpoint..."
./isaaclab.sh -p "${TOOLS_DIR}/select_best_mt4_checkpoint.py"

if [[ ! -s "${BEST_FILE}" ]]; then
  echo "[ERROR] best_checkpoint.txt was not created or is empty."
  echo "        Expected path: ${BEST_FILE}"
  echo "        Please check that training logs exist under logs/rsl_rl/mt4_simplified_reach_direct."
  exit 1
fi

echo "[OK] Best checkpoint:"
cat "${BEST_FILE}"
