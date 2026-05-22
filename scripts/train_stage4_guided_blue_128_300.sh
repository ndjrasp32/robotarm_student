#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_student"
BEST_FILE="${PROJECT_DIR}/logs/plots/best_checkpoint.txt"
STATE_FILE="${MT4_REACH_STAGE4_STATE_FILE:-${PROJECT_DIR}/data/stage4_center_states/latest.pt}"

cd ~/work/isaac/src/IsaacLab
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

TASK_NAME="Isaac-MT4-Simplified-Reach-Direct-v0"

if [[ ! -s "${BEST_FILE}" ]]; then
  echo "[ERROR] Guided-blue Stage-4 training needs a starting checkpoint."
  echo "        best_checkpoint.txt was not found or is empty:"
  echo "        ${BEST_FILE}"
  echo "        Run ${PROJECT_DIR}/scripts/plot_and_select_best.sh first."
  exit 1
fi

if [[ ! -f "${STATE_FILE}" ]]; then
  echo "[ERROR] Stage-4 replay state file does not exist:"
  echo "        ${STATE_FILE}"
  echo "        Run ${PROJECT_DIR}/scripts/collect_stage4_center_states.sh first."
  exit 1
fi

CHECKPOINT_PATH="$(tr -d '\r\n' < "${BEST_FILE}")"
if [[ ! -f "${CHECKPOINT_PATH}" ]]; then
  echo "[ERROR] The checkpoint recorded in best_checkpoint.txt does not exist:"
  echo "        ${CHECKPOINT_PATH}"
  echo "        Re-run ${PROJECT_DIR}/scripts/plot_and_select_best.sh after training logs are available."
  exit 1
fi

LOAD_RUN="$(basename "$(dirname "${CHECKPOINT_PATH}")")"
LOAD_CHECKPOINT="$(basename "${CHECKPOINT_PATH}")"

export MT4_REACH_TRAINING_MODE=stage4_center
export MT4_REACH_RESET_MODE=pregrasp_replay
export MT4_REACH_PREGRASP_STATE_FILE="${STATE_FILE}"
export MT4_REACH_REPLAY_PROB="${MT4_REACH_REPLAY_PROB:-0.96}"
export MT4_REACH_REPLAY_JOINT_NOISE="${MT4_REACH_REPLAY_JOINT_NOISE:-0.002}"
export MT4_REACH_REPLAY_TARGET_NOISE="${MT4_REACH_REPLAY_TARGET_NOISE:-0.0005}"
export MT4_REACH_REPLAY_JOINT_VELOCITY_SCALE="${MT4_REACH_REPLAY_JOINT_VELOCITY_SCALE:-0.04}"
export MT4_REACH_MOVING_PREGRASP="${MT4_REACH_MOVING_PREGRASP:-1}"
export MT4_REACH_MOVING_PREGRASP_STEPS="${MT4_REACH_MOVING_PREGRASP_STEPS:-3}"
export MT4_REACH_MOVING_PREGRASP_FINAL_FRACTION="${MT4_REACH_MOVING_PREGRASP_FINAL_FRACTION:-0.70}"
export MT4_REACH_MOVING_PREGRASP_STEP_RADIUS="${MT4_REACH_MOVING_PREGRASP_STEP_RADIUS:-0.055}"
export MT4_REACH_MOVING_PREGRASP_REWARD_WEIGHT="${MT4_REACH_MOVING_PREGRASP_REWARD_WEIGHT:-10.0}"
export MT4_REACH_FINAL_INSERTION_WEIGHT="${MT4_REACH_FINAL_INSERTION_WEIGHT:-48.0}"
export MT4_REACH_FINAL_CENTER_RADIUS="${MT4_REACH_FINAL_CENTER_RADIUS:-0.045}"
export MT4_REACH_NEAR_TERMINAL_RADIUS="${MT4_REACH_NEAR_TERMINAL_RADIUS:-0.050}"
export MT4_REACH_NEAR_TERMINAL_WEIGHT="${MT4_REACH_NEAR_TERMINAL_WEIGHT:-4.0}"
export MT4_REACH_STAGE_LATCH_WEIGHT="${MT4_REACH_STAGE_LATCH_WEIGHT:-0.9}"
export MT4_REACH_PROGRESSIVE_STAGE_WEIGHT="${MT4_REACH_PROGRESSIVE_STAGE_WEIGHT:-0.5}"
export MT4_REACH_ACTION_SCALE="${MT4_REACH_ACTION_SCALE:-0.026}"
export MT4_REACH_ACTION_PENALTY="${MT4_REACH_ACTION_PENALTY:-0.020}"
export MT4_REACH_STAGE4_PUSH_WEIGHT="${MT4_REACH_STAGE4_PUSH_WEIGHT:-72.0}"
export MT4_REACH_STAGE4_PUSH_IMPROVEMENT_WEIGHT="${MT4_REACH_STAGE4_PUSH_IMPROVEMENT_WEIGHT:-120.0}"
export MT4_REACH_STAGE4_PUSH_DEPTH_WEIGHT="${MT4_REACH_STAGE4_PUSH_DEPTH_WEIGHT:-48.0}"
export MT4_REACH_STAGE4_SHORTEST_PATH_WEIGHT="${MT4_REACH_STAGE4_SHORTEST_PATH_WEIGHT:-44.0}"
export MT4_REACH_STAGE4_DISTANCE_SHELL_WEIGHT="${MT4_REACH_STAGE4_DISTANCE_SHELL_WEIGHT:-36.0}"
export MT4_REACH_STAGE4_TIME_PENALTY="${MT4_REACH_STAGE4_TIME_PENALTY:-0.075}"
export MT4_REACH_STAGE3_TIME_PRESERVE_WEIGHT="${MT4_REACH_STAGE3_TIME_PRESERVE_WEIGHT:-0.8}"
export MT4_REACH_TERMINAL_SUCCESS_QUALITY_WEIGHT="${MT4_REACH_TERMINAL_SUCCESS_QUALITY_WEIGHT:-18.0}"
export MT4_REACH_SUCCESS_BONUS="${MT4_REACH_SUCCESS_BONUS:-64.0}"
export MT4_REACH_CENTER_PUSH_IMPROVEMENT_SCALE="${MT4_REACH_CENTER_PUSH_IMPROVEMENT_SCALE:-0.010}"
export MT4_REACH_CENTER_DISTANCE_SHELL_SIZE="${MT4_REACH_CENTER_DISTANCE_SHELL_SIZE:-0.005}"
export MT4_REACH_STAGE4_PUSH_READY_PROGRESS="${MT4_REACH_STAGE4_PUSH_READY_PROGRESS:-0.65}"

MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-300}"

echo "[INFO] Guided-blue Stage-4 training for ${TASK_NAME}"
echo "[INFO] mode=${MT4_REACH_TRAINING_MODE} reset=${MT4_REACH_RESET_MODE}"
echo "[INFO] replay_state_file=${MT4_REACH_PREGRASP_STATE_FILE}"
echo "[INFO] moving_pregrasp=${MT4_REACH_MOVING_PREGRASP} steps=${MT4_REACH_MOVING_PREGRASP_STEPS} final_fraction=${MT4_REACH_MOVING_PREGRASP_FINAL_FRACTION}"
echo "[INFO] moving_step_radius=${MT4_REACH_MOVING_PREGRASP_STEP_RADIUS} moving_reward=${MT4_REACH_MOVING_PREGRASP_REWARD_WEIGHT}"
echo "[INFO] final_insertion_weight=${MT4_REACH_FINAL_INSERTION_WEIGHT}"
echo "[INFO] final_center_radius=${MT4_REACH_FINAL_CENTER_RADIUS}"
echo "[INFO] stage_latch_weight=${MT4_REACH_STAGE_LATCH_WEIGHT} progressive_stage_weight=${MT4_REACH_PROGRESSIVE_STAGE_WEIGHT}"
echo "[INFO] resume_run=${LOAD_RUN} checkpoint=${LOAD_CHECKPOINT}"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --resume \
  --load_run "${LOAD_RUN}" \
  --checkpoint "${LOAD_CHECKPOINT}" \
  --seed "${MT4_SEED:-42}" \
  agent.policy.init_noise_std="${MT4_INIT_NOISE_STD:-0.40}" \
  agent.algorithm.entropy_coef="${MT4_ENTROPY_COEF:-0.0030}" \
  "$@"
