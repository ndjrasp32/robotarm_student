#!/usr/bin/env bash
set -euo pipefail

"${HOME}/work/robotarm/robotarm_student/scripts/play_best.sh" --num_envs 1 --real-time "$@"
