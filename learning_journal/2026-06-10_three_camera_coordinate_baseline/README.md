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

## Current Setup / 현재 설정

| item | value |
| --- | --- |
| task / 태스크 | `Isaac-MT4-Coordinate-Plane-Direct-v0` |
| training script / 학습 스크립트 | `scripts/train_coordinate_stage1_three_camera_baseline_128_1500_video.sh` |
| body cameras / 몸체 카메라 | fixed left/right stereo projection |
| gripper camera / 그리퍼 카메라 | target `u/v/depth/visible` projection from gripper frame |
| policy observation / 정책 관측 | 51 values |
| strict success / 엄격 성공 | same camera region and target center within `0.030 m` |
| region mastery gate / 영역 통과 기준 | 10 strict successes per region for new runs |
| video rule / 영상 규칙 | about 1 minute for training and demo videos |

## Evidence / 근거 자료

- Run record / 실행 기록: [20260610_111518_run_three_camera_coordinate_baseline_1500iter.md](20260610_111518_run_three_camera_coordinate_baseline_1500iter.md)
- Plot / 그래프: [region mastery graph](artifacts/20260610_111518_review_three_camera_region_mastery_counts.png), [camera graph](artifacts/20260610_111518_review_three_camera_visibility_and_alignment.png), [success graph](artifacts/20260610_111518_review_three_camera_success_curve.png)
- Video / 영상: [20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4](../videos/20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4)
- Demo video / 데모 영상: [20260610_114650_demo_three_camera_random_regions_1min.mp4](../videos/20260610_114650_demo_three_camera_random_regions_1min.mp4)
- Demo sequence / 데모 순서: [20260610_114650_demo_three_camera_random_regions_1min_sequence.csv](../videos/20260610_114650_demo_three_camera_random_regions_1min_sequence.csv)

## Next Step / 다음 단계

- KR: 먼저 10회 성공 기준과 1분 영상 규칙으로 Stage 1을 다시 확인한다. 그 다음 7cm 근접 이후 3cm 중심 수렴률을 높이는 fine-tuning을 설계한다.
- EN: First re-check Stage 1 with the 10-success gate and 1-minute video rule. Then design fine-tuning that improves convergence from 7 cm proximity to the 3 cm center target.
