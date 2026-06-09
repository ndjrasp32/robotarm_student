# 2026-06-10 Coordinate Region Mastery Plan

## Purpose

This note separates the student-facing design ideas before the next coordinate-plane training run.

The curriculum still keeps the camera-frame coordinate basis. The goal is not to jump directly to object manipulation, but to first make the arm learn the numbered front workspace regions that the stereo cameras define.

## User Proposal

- Keep the coordinate regions in the camera frame, because the later approach stage needs a stable camera-coordinate basis.
- Use 9 regions first instead of a full 27-cell volume.
- Evaluate success as "region N success" rather than a single undifferentiated success rate.
- Count a success only when the gripper enters the target region and approaches the region center closely enough, about 3 cm from the center point.
- Do not train each region as a separate independent model.
- Continue training one policy: when region 1 succeeds enough times, keep the best-performing behavior from that phase, clear the phase reward pressure, and continue into region 2.
- Record the learned value/progress for each region so students can inspect how the curriculum advanced.

## Codex Proposal

- Implement the first version as sequential region mastery inside the same RSL-RL environment.
- During Stage 1, sample only the current active region for all envs.
- Keep the existing home reset after success, then sample the current region again until it reaches the mastery threshold.
- Advance from region 1 to region 2 only after the active region reaches the configured success count.
- Use strict Stage 1 success:
  - same stereo camera cell, and
  - gripper-to-target distance less than `0.030 m`, and
  - target and gripper visible in both cameras.
- Log strict per-region success, cumulative per-region success counts, best successful episode reward, mastered flag, active region number, and 3 cm center approach rate.
- Write `region_mastery.csv` into the training run directory whenever a region success is recorded.

## Implementation Choice

The environment cannot literally prune and keep only one model checkpoint mid-run without adding an external orchestration loop around RSL-RL. For this pass, "best model only" is represented in two practical ways:

- RSL-RL continues from the same policy weights as the active region advances.
- The environment records the best successful episode reward per region, so the training run can later select or resume from checkpoints around the cleanest region transitions.

This keeps the student workflow simple enough for one training command while preserving the important educational idea: the curriculum advances by numbered region mastery, not by random target mixing.

## Current Parameters

- Task: `Isaac-MT4-Coordinate-Plane-Direct-v0`
- Regions: 3x3 front camera-plane cells, numbered 1-9.
- Mastery threshold: 5 strict successes per region.
- Center success radius: `0.030 m`.
- Training command: `scripts/train_coordinate_stage1_plane_128_500.sh`

## What To Watch

- `coordinate_curriculum/plane_localization_active_region_number`
- `coordinate_curriculum/plane_localization_mastered_region_count`
- `coordinate_curriculum/plane_localization_center_3cm_rate`
- `coordinate_curriculum/plane_localization_strict_region_center_success_rate`
- `coordinate_curriculum/plane_localization_region_01_success_count` through region 09
- `region_mastery.csv` in the run directory

## Promotion Rule

Do not move this to `robotarm_mt4` or real hardware unless the 9-region simulation can repeatedly master all regions or produce a clearly improving region-by-region sequence with stable workspace entry and stereo visibility.
