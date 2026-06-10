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

## Current Setup / 현재 설정

| item | value |
| --- | --- |
| task / 태스크 | `Isaac-MT4-Coordinate-Plane-Direct-v0` |
| training script / 학습 스크립트 | `scripts/train_coordinate_stage1_three_camera_baseline_128_1500_video.sh` |
| body cameras / 몸체 카메라 | fixed left/right stereo projection |
| gripper camera / 그리퍼 카메라 | target `u/v/depth/visible` projection from gripper frame |
| policy observation / 정책 관측 | 54 values after target-tracking update |
| strict success / 엄격 성공 | same camera region and target center within `0.010 m` |
| region mastery gate / 영역 통과 기준 | 10 strict successes per region for new runs |
| video rule / 영상 규칙 | about 1 minute for training and demo videos |
| overshoot rule / 지나침 억제 | penalize moving past the target away from the robot |
| approach rule / 접근 방향 | prefer approach from the robot side or from above |

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

- Run record / 실행 기록: [20260610_111518_run_three_camera_coordinate_baseline_1500iter.md](20260610_111518_run_three_camera_coordinate_baseline_1500iter.md)
- Plot / 그래프: [region mastery graph](artifacts/20260610_111518_review_three_camera_region_mastery_counts.png), [camera graph](artifacts/20260610_111518_review_three_camera_visibility_and_alignment.png), [success graph](artifacts/20260610_111518_review_three_camera_success_curve.png)
- Video / 영상: [20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4](../videos/20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4)
- Demo video / 데모 영상: [20260610_114650_demo_three_camera_random_regions_1min.mp4](../videos/20260610_114650_demo_three_camera_random_regions_1min.mp4)
- Demo sequence / 데모 순서: [20260610_114650_demo_three_camera_random_regions_1min_sequence.csv](../videos/20260610_114650_demo_three_camera_random_regions_1min_sequence.csv)

## Next Step / 다음 단계

- KR: 1cm 기준, overshoot 벌점, 접근 방향 보상을 넣은 Stage 1을 다시 학습하고 1분 학습 영상과 랜덤 데모 영상을 확인한다.
- EN: Rerun Stage 1 with the 1 cm rule, overshoot penalty, and approach-direction reward, then review the 1-minute training and random demo videos.
