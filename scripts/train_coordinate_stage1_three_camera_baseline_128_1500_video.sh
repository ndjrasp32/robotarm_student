#!/usr/bin/env bash
set -euo pipefail

export MT4_MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-1500}"
export MT4_RECORD_VIDEO="${MT4_RECORD_VIDEO:-1}"
export MT4_VIDEO_LENGTH="${MT4_VIDEO_LENGTH:-3600}"
export MT4_VIDEO_INTERVAL="${MT4_VIDEO_INTERVAL:-12000}"

echo "[INFO] Stage 1 three-camera coordinate baseline"
echo "[INFO] body stereo cameras: left/right fixed virtual cameras"
echo "[INFO] gripper camera: target u/v/depth/visible projection in the policy observation"
echo "[INFO] region mastery requires 10 strict successes per region"
echo "[INFO] strict success distance is 0.010 m with target overshoot penalty"
echo "[INFO] training videos default to 3600 steps, about 60 seconds at 60 Hz"

"${HOME}/work/robotarm/robotarm_student/scripts/train_coordinate_stage1_plane_128_500.sh" \
  --run_name three_camera_coordinate_baseline_128env_1500iter \
  "$@"
