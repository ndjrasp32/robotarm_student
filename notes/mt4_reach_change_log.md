# MT4 Reach Task Change Log

## 2026-05-12 gripper_pitch axis and touch-aware reward

- Kept task name: `Isaac-MT4-Simplified-Reach-Direct-v0`.
- Added `assets/usd/mt4_simplified_v3.usd`, based on v2 plus:
  - new body: `gripper_link`
  - new revolute joint: `gripper_pitch`
  - joint limit: about `-68.75 deg` to `+68.75 deg`
- Updated the task to use 5 actions:
  - `base_yaw`
  - `shoulder`
  - `elbow`
  - `wrist_pitch`
  - `gripper_pitch`
- Updated observation size from `26` to `28`.
- The end-effector body is now `gripper_link` instead of `wrist_link`.
- Reward changes:
  - increased success bonus from `5.0` to `8.0`
  - reduced pure distance/pregrasp reward weights
  - increased alignment and touch-surface reward weights
  - added object-overlap penalty so the gripper tip should approach the target surface without passing through the target marker
- Target sampling changes:
  - target x range moved from `(0.16, 0.30)` to `(0.20, 0.32)`
  - target z range moved from `(0.06, 0.18)` to `(0.08, 0.18)`
  - targets too close to the robot base radius are resampled
- New logged metrics:
  - `mt4/mean_touch_error`
  - `mt4/mean_object_overlap`

Notes:
- The red target is still a visual marker, not a rigid object. This avoids the target being physically knocked away during reach training.
- Physical object dynamics should be added later in a separate grasp/lift task, after reach/touch behavior is stable.
