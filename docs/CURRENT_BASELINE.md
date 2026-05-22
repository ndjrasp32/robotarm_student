# Current Baseline - robotarm_student

Date: 2026-05-22 KST

## Repository Role

`robotarm_student` is the student-facing WLKATA MT4 curriculum repository.

Use this repo for:

- repeatable IsaacLab MT4 curriculum runs
- staged reach, pregrasp, and insertion experiments
- Mars rover manipulation twin practice
- experiment notes that students can review without treating them as daily entry points

Use `robotarm_mt4` for hardware-facing Mirobot/MT4 asset checks and real-device transfer gates.

## Current Baseline

The active direction starts from the Mars rover MT4 manipulation plan:

- reference plan: `notes/20260521_mars_rover_mt4_rl_plan.md`
- active task package: `source/mt4_reach_direct`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger simplified asset generation: `scripts/create_two_finger_asset.sh`

Mission split:

- `pick`
- `place`
- `stack`
- `push`
- `pull`

The first practical validation target should be `push` or `pull`, because those can prove dynamic-object contact before relying on a fully validated grasp model.

## Today's Operating Rule

Use only this file and `README.md` as the daily starting point. Treat `notes/`, `experiments/`, and `logs/plots/` as archive unless this file links to a specific item.

## Reset Rationale

The project was reset to this baseline because the previous working state had too many daily notes, renamed repositories, and mixed student/hardware responsibilities. From 2026-05-22, this repo is treated as the student-facing MT4 curriculum baseline, and older `notes/` and `experiments/` entries remain archive instead of the daily source of truth.

The current start sequence is:

1. Open the Mars twin scene for `push` or `pull`.
2. Confirm object contact and reset behavior in simulation.
3. Record one concise experiment note only if a real training run or design decision changes.
4. Promote the result into this file only after it becomes the new baseline.

## Safety Gate

Do not treat a trained policy as hardware-ready until these are recorded:

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

Real robot motion must stay behind this gate.

## Documentation Policy

The existing `notes/` and `experiments/` folders are historical archive. They remain useful, but they are not the daily starting point.

Daily starting order:

1. Read this file.
2. Check `README.md`.
3. Use the latest dated note only if it is linked here or in README.
4. Add new findings as dated notes, then update this file only when the project baseline changes.

Do not create separate notes for routine command output or temporary plot artifacts. Keep those in logs and promote only stable conclusions.

## Next Work

1. Confirm the Mars twin scene opens for `push` and `pull`.
2. Confirm object contact and reset behavior in simulation.
3. Decide the conservative home pose and action limits.
4. Add or update one experiment note per training run.
5. Promote only stable, repeatable results back into this baseline.
