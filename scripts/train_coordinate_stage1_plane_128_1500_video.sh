#!/usr/bin/env bash
set -euo pipefail

export MT4_MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-1500}"
export MT4_RECORD_VIDEO="${MT4_RECORD_VIDEO:-1}"
export MT4_VIDEO_LENGTH="${MT4_VIDEO_LENGTH:-3600}"
export MT4_VIDEO_INTERVAL="${MT4_VIDEO_INTERVAL:-12000}"

"${HOME}/work/robotarm/robotarm_student/scripts/train_coordinate_stage1_plane_128_500.sh" "$@"
