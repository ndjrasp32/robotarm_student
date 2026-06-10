# 2026-06-10 Three-Camera Coordinate Baseline / 3카메라 좌표 기준선

## Summary / 요약

- KR: 몸체 좌/우 스테레오 카메라에 그리퍼 장착 카메라 projection을 추가한 새 Stage 1 좌표 학습 기준선입니다.
- EN: This is the new Stage 1 coordinate-learning baseline with a gripper-mounted camera projection added to the body left/right stereo cameras.

## Question / 질문

- KR: 세 대의 카메라를 함께 쓰면 타겟 영역 추정 이후 실제 타겟 중심으로 더 안정적으로 수렴하는가?
- EN: Does using three linked cameras improve convergence from target-region recognition to the true target center?

## Thread Index / 기록 순서

1. [20260610_111308_plan_three_camera_coordinate_baseline.md](20260610_111308_plan_three_camera_coordinate_baseline.md)
2. [20260610_111518_run_three_camera_coordinate_baseline_1500iter.md](20260610_111518_run_three_camera_coordinate_baseline_1500iter.md)
3. [20260610_114129_plan_success10_video1min_demo_check.md](20260610_114129_plan_success10_video1min_demo_check.md)
4. [20260610_130106_plan_target_tracking_rerun.md](20260610_130106_plan_target_tracking_rerun.md)
5. [20260610_131608_plan_1cm_overshoot_approach_reward.md](20260610_131608_plan_1cm_overshoot_approach_reward.md)
6. [20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md](20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md)
7. [20260610_143523_plan_volume_3x3x3_region_training.md](20260610_143523_plan_volume_3x3x3_region_training.md)
8. [20260610_143719_run_volume_3x3x3_failure_reach_audit.md](20260610_143719_run_volume_3x3x3_failure_reach_audit.md)
9. [20260610_163317_run_reach_limited_volume_region19_failure.md](20260610_163317_run_reach_limited_volume_region19_failure.md)
10. [20260610_171626_reach_limited_27_success_analysis_and_precision_plan.md](20260610_171626_reach_limited_27_success_analysis_and_precision_plan.md)
11. [20260610_175400_run_volume_precision_5mm_800iter.md](20260610_175400_run_volume_precision_5mm_800iter.md)

## Current Setup / 현재 설정

| item | value |
| --- | --- |
| task / 태스크 | `Isaac-MT4-Coordinate-Plane-Direct-v0` |
| training script / 학습 스크립트 | `scripts/train_coordinate_stage1_three_camera_target_tracking_128_1500_video.sh` |
| body cameras / 몸체 카메라 | fixed left/right stereo projection |
| gripper camera / 그리퍼 카메라 | target `u/v/depth/visible` projection from gripper frame |
| policy observation / 정책 관측 | 54 values after target-tracking update |
| strict success / 엄격 성공 | same camera region and target center within `0.010 m` |
| region mastery gate / 영역 통과 기준 | 10 strict successes per region for new runs |
| video rule / 영상 규칙 | about 1 minute for training and demo videos |
| overshoot rule / 지나침 억제 | penalize moving past the target away from the robot |
| approach rule / 접근 방향 | prefer approach from the robot side or from above |

## Next Volume Run / 다음 27영역 실행

| item | value |
| --- | --- |
| task / 태스크 | `Isaac-MT4-Coordinate-Volume-Direct-v0` |
| training script / 학습 스크립트 | `scripts/train_coordinate_stage1_volume_128_1500_video.sh` |
| region split / 영역 분할 | `3x3x3`, 27 workspace cells |
| reach-limited workspace / 가동범위 기반 박스 | center `(0.305, 0.00, 0.205)`, size `(0.09, 0.14, 0.09)` |
| region mastery gate / 영역 통과 기준 | 10 strict 1 cm successes per volume cell |
| expected metric / 기대 지표 | `mastered_region_count` should progress toward 27 |

## Current Fix / 현재 보정

- KR: 이전 정책은 영역 통과는 빨랐지만, 데모에서 새 목표 중심을 충분히 따라가지 못했다.
- EN: The previous policy passed regions quickly, but the demo did not follow new target centers well enough.

- KR: 새 보정은 카메라로 추정한 목표 상대좌표 3개를 정책 입력에 추가하고, 목표 중심으로 가까워지는 보상을 강화한다.
- EN: The new update adds 3 camera-estimated target-relative values to the policy input and strengthens the reward for moving to the target center.

- KR: 랜덤 데모는 목표를 바꾼 직후 정책 관측도 바로 새로 읽도록 수정했다.
- EN: The random demo now refreshes policy observations immediately after target changes.

- KR: 이번 추가 보정은 성공 거리 기준을 1cm로 강화하고, 목표를 지나쳤다가 돌아오는 움직임을 줄이며, 로봇 쪽이나 위쪽에서 목표로 접근하도록 보상한다.
- EN: The latest update tightens strict success to 1 cm, reduces overshoot-and-return behavior, and rewards approach from the robot side or from above.

## Evidence / 근거 자료

- Latest run / 최신 실행: [20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md](20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md)
- Latest report / 최신 리포트: [20260610_132926_three_camera_target_tracking_128env_1500iter_three_camera_target_tracking_1cm_stage1_1500iter.md](../../experiments/20260610_132926_three_camera_target_tracking_128env_1500iter_three_camera_target_tracking_1cm_stage1_1500iter.md)
- Latest training video / 최신 학습 영상: [20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4](../videos/20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4)
- Latest demo video / 최신 데모 영상: [20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4](../videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4)
- Latest demo sequence / 최신 데모 순서: [20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv](../videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv)
- Run record / 실행 기록: [20260610_111518_run_three_camera_coordinate_baseline_1500iter.md](20260610_111518_run_three_camera_coordinate_baseline_1500iter.md)
- Plot / 그래프: [region mastery graph](artifacts/20260610_111518_review_three_camera_region_mastery_counts.png), [camera graph](artifacts/20260610_111518_review_three_camera_visibility_and_alignment.png), [success graph](artifacts/20260610_111518_review_three_camera_success_curve.png)
- Video / 영상: [20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4](../videos/20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4)
- Demo video / 데모 영상: [20260610_114650_demo_three_camera_random_regions_1min.mp4](../videos/20260610_114650_demo_three_camera_random_regions_1min.mp4)
- Demo sequence / 데모 순서: [20260610_114650_demo_three_camera_random_regions_1min_sequence.csv](../videos/20260610_114650_demo_three_camera_random_regions_1min_sequence.csv)

## Next Step / 다음 단계

- KR: 다음 실행은 3x3x3 27영역 인식 학습이다. 9영역에서 확인한 카메라 추정과 1cm 추적 보상을 유지하되, 깊이 방향까지 영역 마스터리를 확장한다.
- EN: The next run is 3x3x3 27-cell region-recognition training. Keep the camera estimate and 1 cm tracking reward from the 9-cell run, but extend region mastery through depth.
