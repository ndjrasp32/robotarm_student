# 2026-06-10 Coordinate Region Mastery Extended Run Plan

## Change

Increase the Stage 1 sequential 9-region training run from 500 iterations to 1500 iterations.

The success rule stays unchanged:

- same stereo camera cell as the target,
- gripper center within `0.030 m` of the region center,
- target and gripper visible in both virtual cameras.

## Why

The 500-iteration run mastered regions 1 and 2, then stopped at region 3. Its camera-region entry rate was already high, so this run tests whether the same reward and success criteria only needed more policy updates before changing the reward design.

## Output

- Training video is enabled by default in `scripts/train_coordinate_stage1_plane_128_500.sh`.
- `scripts/train_coordinate_stage1_plane_128_1500_video.sh` is the explicit long-run wrapper.
- `tools/report_mt4_coordinate_curriculum.py` generates coordinate-specific graphs and a student report from TensorBoard logs.
- `scripts/play_coordinate_stage1_best_video.sh` can record a checkpoint replay video after training.

## Decision Rule

Keep the result in simulation. Do not promote to real hardware unless all 9 regions are mastered or the report shows a stable region-by-region improvement path worth continuing.
