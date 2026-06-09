# 2026-06-10 Coordinate Region Mastery Stage 1 Result

## Goal

Test the 9-region camera-frame curriculum with sequential region mastery.

The run uses one continuous policy. Stage 1 samples only the active front camera-plane region. A region is mastered after 5 strict successes, then the environment advances to the next numbered region.

Strict success means:

- gripper enters the same stereo camera region as the target,
- gripper is within `0.030 m` of the region center target,
- target and gripper are visible in both cameras.

## Code Baseline

- Commit: `461b07c` (`Add coordinate region mastery curriculum`)
- Plan note: `notes/20260610_coordinate_region_mastery_plan.md`
- Task: `Isaac-MT4-Coordinate-Plane-Direct-v0`
- Training command: `TERM=xterm-256color MT4_MAX_ITERATIONS=500 scripts/train_coordinate_stage1_plane_128_500.sh`

## Run

- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_02-59-41`
- Envs: 128
- Iterations: 500
- Seed: 42
- Final checkpoint: `model_499.pt`
- Training time: 259.83 seconds
- Region mastery file: `region_mastery.csv`

## Final Metrics

- `mean_reward`: 3527.9282
- `success_rate`: 0.0000
- `mean_distance`: 0.0821 m
- `mean_plane_error`: 0.0316 m
- `mean_camera_region_error`: 0.4114
- `camera_region_entry_rate`: 0.9456
- `inside_workspace_rate`: 0.8896
- `mean_workspace_entry_error`: 0.0142 m
- `gripper_stereo_visible_rate`: 0.9646
- `center_3cm_rate`: 0.0000
- `strict_region_center_success_rate`: 0.0000
- `active_region_number`: 3
- `mastered_region_count`: 2

## Region Mastery Snapshot

| Region | Success Count | Best Episode Reward | Mastered | Active |
| --- | ---: | ---: | ---: | ---: |
| 1 | 5 | 2086.4673 | 1 | 0 |
| 2 | 5 | 323.8190 | 1 | 0 |
| 3 | 0 | | 0 | 1 |
| 4 | 0 | | 0 | 0 |
| 5 | 0 | | 0 | 0 |
| 6 | 0 | | 0 | 0 |
| 7 | 0 | | 0 | 0 |
| 8 | 0 | | 0 | 0 |
| 9 | 0 | | 0 | 0 |

## Analysis

The new curriculum mechanism works: the policy mastered region 1, continued training, mastered region 2, and advanced to region 3 without starting a separate model.

The remaining failure is not camera-region recognition. By the end of training, the policy enters the requested camera cell about 94.6% of the time, stays inside the workspace about 89.0% of the time, and keeps the gripper stereo-visible about 96.5% of the time.

The bottleneck is physical center approach. Region 3 never reaches the 3 cm center radius during the final phase, and final mean distance remains about 8.2 cm. This suggests the 3 cm target is too sparse as the only advancement signal once the policy has learned same-cell entry.

## Decision

Do not promote this policy to `robotarm_mt4` or real hardware.

Keep the current region mastery structure, but revise the next run so region advancement has an intermediate center-distance ladder:

1. Keep same-camera-cell entry as a required gate.
2. Add center thresholds such as 10 cm, 7 cm, 5 cm, then 3 cm.
3. Allow region mastery to advance only at 3 cm, but give stronger dense shaping below 10 cm so the policy does not settle at same-cell entry.
4. Consider resuming from `model_150.pt` or `model_200.pt` if region 3 degradation appears after the first two regions are mastered.
