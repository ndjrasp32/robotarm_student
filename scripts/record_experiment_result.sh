#!/usr/bin/env bash
set -euo pipefail

cd ~/work/isaac/src/IsaacLab
unset CMEEL_PREFIX
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

./isaaclab.sh -p "${HOME}/work/robotarm/robotarm_student/tools/record_mt4_experiment.py" "$@"
