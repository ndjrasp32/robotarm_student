# 2026-06-09 Coordinate Camera Region Stage 1 Result

## Goal

Train the student repository only on sequential workspace coordinate recognition before porting anything to the mt4 repository or real hardware.

The stage-1 target was changed from six surface faces to 27 numbered workspace cube cells. Each success resets the arm to the home posture, then samples the next numbered target. Observations keep the stereo camera projection features so the policy learns the camera-frame coordinate basis first.

## Changes Tested

- `MT4CoordinateCurriculumEnv` now samples 27 sequential volume-cell targets.
- Region features include normalized `(region id, x cell, y cell, z cell)`.
- Stage-1 success uses stereo camera projection proximity: `camera_alignment_error < 0.95` with target and gripper visible.
- Same-camera-cell entry is still logged as `camera_region_entry_rate`.

## Training Run

- Command: `scripts/train_coordinate_stage1_plane_128_500.sh`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_01-33-56`
- Envs: 128
- Iterations: 500
- Seed: 42
- Final checkpoint: `model_499.pt`
- Training time: 269.45 seconds

## Final Console Metrics

- `success_rate`: 0.0007
- `camera_region_entry_rate`: 0.2200
- `mean_camera_region_error`: 1.2091
- `mean_distance`: 0.2476
- `inside_workspace_rate`: 0.0000
- `target_stereo_visible_rate`: 1.0000
- `gripper_stereo_visible_rate`: 0.9531
- Region numbers covered: 1 to 27

## Analysis

This run is not good enough to promote to the mt4 repository or real hardware.

The useful part is that the target sequence and stereo visibility path are working: all 27 region IDs are sampled, target visibility is stable, and gripper visibility reaches about 95%. The policy also learns some coarse camera cell overlap, with `camera_region_entry_rate` around 22%.

The failure is that the final success rate remains near zero and the arm does not stay inside the intended workspace cube. The policy appears to learn a camera-visible posture that partially overlaps the target image cells, but it does not learn reliable workspace-cell entry from the current reward/action setup.

## Next Step

Do not move this to mt4 yet. The next training revision should split the task into two easier stages:

1. Home-to-visible-workspace stage: reward and success only for entering the camera-visible workspace cube.
2. Camera-region stage: once inside the cube, train numbered region selection with the 27-cell target features.

The current single-stage setup asks the policy to solve visibility, workspace entry, and numbered region matching at the same time, which is too sparse for this arm model.

## Follow-up Revision

The student repository was updated again to match the "enter the region, then reset home and move to the next number" training idea.

Code changes:

- Added `Isaac-MT4-Coordinate-Workspace-Entry-Direct-v0` as a stage-0 warm-up task.
- Added `scripts/train_coordinate_stage0_workspace_entry_128_300.sh`.
- Changed stage-1 success from exact center alignment to camera-region entry:
  - success when the gripper enters the same stereo camera cell, or
  - when stereo projection error is within `camera_region_success_radius = 0.80`.
- Kept strict `camera_region_entry_rate` logging so loose success and exact cell entry can be compared.
- Added workspace boundary distance logging as `mean_workspace_entry_error`.

## Follow-up Training Runs

### Stage 0 Workspace Entry

- Command: `MT4_MAX_ITERATIONS=300 scripts/train_coordinate_stage0_workspace_entry_128_300.sh`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_01-43-58`
- Final checkpoint: `model_299.pt`
- Training time: 153.31 seconds

Final metrics:

- `success_rate`: 0.0000 before the later relaxed success-radius fix
- `inside_workspace_rate`: 0.0000
- `mean_workspace_entry_error`: 0.0596
- `gripper_stereo_visible_rate`: 0.9531
- `camera_region_entry_rate`: 0.0967

Analysis:

The policy learned to move the gripper into a camera-visible pose and close to the workspace boundary, but strict "inside the cube" success was too hard for this arm/workspace placement. A relaxed workspace-entry success radius of `0.065m` was added after this run.

### Stage 1 Strict Cell Entry

- Command: `MT4_MAX_ITERATIONS=500 scripts/train_coordinate_stage1_plane_128_500.sh`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_01-47-06`
- Final checkpoint: `model_499.pt`
- Training time: 267.29 seconds

Final metrics:

- `success_rate`: 0.0002
- `camera_region_entry_rate`: 0.0032
- `mean_camera_region_error`: 0.7201
- `inside_workspace_rate`: 0.8640
- `mean_workspace_entry_error`: 0.0125
- `gripper_stereo_visible_rate`: 0.9617

Analysis:

This run is useful but not sufficient. It strongly improved physical workspace entry, from 0% to about 86%, but exact 3x3 stereo-cell entry remained too sparse as a terminal success condition.

### Stage 1 Relaxed Reward Resume

- Command: `MT4_MAX_ITERATIONS=150 scripts/train_coordinate_stage1_plane_128_500.sh --resume --load_run 2026-06-09_01-47-06 --checkpoint model_499.pt`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_01-52-32`
- Final checkpoint: `model_648.pt`
- Training time: 75.54 seconds

Final metrics:

- `success_rate`: 0.0027
- `camera_region_entry_rate`: 0.1255
- `mean_camera_region_error`: 1.0342
- `inside_workspace_rate`: 0.2749
- `mean_workspace_entry_error`: 0.0538
- `gripper_stereo_visible_rate`: 0.8655

Analysis:

The relaxed reward increased strict stereo-cell entry to about 12.5%, which is the best camera-region recognition signal so far. However, it degraded workspace stability.

### Stage 1 OR Success Check

- Command: `MT4_MAX_ITERATIONS=100 scripts/train_coordinate_stage1_plane_128_500.sh --resume --load_run 2026-06-09_01-52-32 --checkpoint model_648.pt`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_01-54-24`
- Final checkpoint: `model_747.pt`
- Training time: 49.63 seconds

Final metrics:

- `success_rate`: 0.0015
- `camera_region_entry_rate`: 0.0374
- `mean_camera_region_error`: 0.9765
- `inside_workspace_rate`: 0.2026
- `mean_workspace_entry_error`: 0.0524
- `gripper_stereo_visible_rate`: 0.8965

Analysis:

The OR success check confirmed that the current resumed policy is unstable under the revised objective. It should not be promoted.

## Current Decision

Do not move this to the mt4 repository yet.

The best current result is not a single final policy; it is a diagnosis:

- The arm can learn workspace entry under the camera-coordinate observation.
- The arm can produce some stereo camera-cell entry signal when the reward is relaxed.
- The current 27-cell sequential task is still too hard because workspace stability and region discrimination fight each other.

The next revision should keep the camera-frame target basis, but reduce the first numbered curriculum from 27 cells to a smaller set:

1. Train 9 front-facing cells first with workspace stability locked in.
2. Add depth as a second phase after the 9 cells are stable.
3. Keep success as `same camera cell OR relaxed stereo projection radius`, but report strict same-cell entry separately.

## Current 9-Cell Plan

This is the plan to commit before the next training run:

1. Keep the coordinate basis in the camera frame, because the next object approach stage needs the robot to understand the camera-defined workspace first.
2. Train only 9 front camera-plane cells first, not the full 27-cell volume.
3. Treat entering the target camera region as a first-stage success. The environment ends the episode on success, resets the arm to the home posture, then samples the next numbered region.
4. Keep strict same-camera-cell entry as a separate metric, so relaxed success does not hide whether true region recognition is improving.
5. Run Stage 1 again from this simpler 9-cell setup, then decide whether to add depth as Stage 1b or move to sphere reach.

## 9-Cell Follow-up

The student repository was revised to reduce stage 1 from 27 volume cells to 9 camera-plane cells:

- Stage 1 now samples only 9 sequential y/z cells.
- The target depth is fixed at the workspace center x position, not the near x-min face.
- Stage 1 has a dedicated reward branch that penalizes distance, plane error, camera alignment error, and workspace-entry error instead of accumulating positive visibility reward for long episodes.
- Relaxed success was widened to `camera_region_success_radius = 1.35` for this first 9-cell pass.
- Strict same-camera-cell entry remains logged separately as `camera_region_entry_rate`.

### Interrupted Diagnostic Runs

Several short runs were intentionally stopped early because the reward was clearly going in the wrong direction:

- `2026-06-09_02-04-03`: 9 x-min/front-face cells, stopped near iteration 210. Success stayed near zero.
- `2026-06-09_02-06-57`: stronger dense reward, stopped near iteration 89. Dense reward encouraged long episodes without real cell entry.
- `2026-06-09_02-08-20`: negative-cost reward with x-min targets, stopped near iteration 387. The policy stayed camera-visible but could not enter the x-min plane.
- `2026-06-09_02-09-43`: workspace-center camera-plane targets with `success_radius = 1.05`, stopped near iteration 378. Initial success improved but remained too sparse.

### 9-Cell Relaxed Success Run

- Command: `MT4_MAX_ITERATIONS=150 scripts/train_coordinate_stage1_plane_128_500.sh --resume --load_run 2026-06-09_01-43-58 --checkpoint model_299.pt`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_02-10-45`
- Final checkpoint: `model_448.pt`
- Training time: 74.21 seconds

Final metrics:

- `success_rate`: 0.0051
- `camera_region_entry_rate`: 0.0000
- `mean_camera_region_error`: 1.6058
- `mean_distance`: 0.2897
- `mean_plane_error`: 0.0945
- `mean_workspace_entry_error`: 0.1427
- `inside_workspace_rate`: 0.0000
- `gripper_stereo_visible_rate`: 0.3696
- Region numbers covered: 1 to 9

Analysis:

The 9-cell structure works mechanically: targets are limited to region numbers 1 through 9, and relaxed success causes early resets at the start of the run. However, the learned policy still does not produce strict camera-cell entry. The final policy degraded gripper stereo visibility and workspace entry, so it should not be promoted.

Current decision:

Do not move this policy to the mt4 repository or real hardware.

The next useful revision is not another reward-only tweak. The task needs a better reset or waypoint scaffold before numbered camera cells:

1. Reset stage 1 from a known camera-visible pregrasp/workspace-entry state instead of always from home.
2. Train the 9 camera-plane cells from that stable state.
3. Only after strict `camera_region_entry_rate` becomes nonzero and stable, add the home-to-cell transition back in.

### Full 9-Cell Stage 1 Run After Commit

- Command: `MT4_MAX_ITERATIONS=500 scripts/train_coordinate_stage1_plane_128_500.sh`
- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-09_07-40-41`
- Envs: 128
- Iterations: 500
- Seed: 42
- Final checkpoint: `model_499.pt`
- Training time: 249.24 seconds

Final metrics:

- `success_rate`: 0.0657
- `camera_region_entry_rate`: 0.0000
- `mean_camera_region_error`: 2.1750
- `mean_distance`: 0.3319
- `inside_workspace_rate`: 0.0000
- `mean_workspace_entry_error`: 0.2361
- `target_stereo_visible_rate`: 1.0000
- `gripper_stereo_visible_rate`: 0.1514
- Region numbers covered: 1 to 9

Analysis:

This run confirms that the 9-cell reduction alone does not solve the coordinate-recognition stage. The relaxed success signal reached about 6.6%, but the strict same-camera-cell metric stayed at 0%, and the arm never entered the configured workspace volume. The policy is exploiting the loose projection-radius success and sparse gripper visibility instead of learning physical region entry.

Do not promote this checkpoint to `robotarm_mt4`.

Next revision:

1. Gate Stage 1 success with workspace entry, not stereo visibility alone.
2. Make the Stage 0 workspace-entry checkpoint useful before Stage 1, either by resuming from it or by starting Stage 1 from reset states closer to the workspace.
3. Tighten the relaxed camera success radius after workspace entry is nonzero; current `1.35` is too loose and allows non-regional success.
