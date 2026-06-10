# 2026-06-10 Three-Camera Coordinate Baseline Plan / 3카메라 좌표 기준선 계획

## Summary / 요약

- KR: 기존 몸체 좌/우 스테레오 projection은 유지하고, 그리퍼 기준 카메라 projection을 정책 관측에 추가한다.
- EN: Keep the existing body left/right stereo projection and add a gripper-frame camera projection to the policy observation.

## Question / 질문

- KR: 카메라가 몸체 스테레오 2대와 그리퍼 1대로 연동되면 타겟 위치 추적과 좌표 학습이 더 잘 되는가?
- EN: With two body stereo cameras and one gripper camera linked together, does target tracking and coordinate learning improve?

## Decision / 결정

- KR: 새 baseline은 실제 로봇 motion이 아니라 IsaacLab simulation 학습으로만 만든다.
- EN: The new baseline is created only through IsaacLab simulation training, not real robot motion.

- KR: 타겟 생성 좌표는 검증/라벨용으로만 유지하고, 정책에는 카메라 projection에서 나온 특징을 넣는다.
- EN: Target-generation coordinates remain only for validation and labels; the policy receives camera-projection features.

- KR: 성공 조건은 기존과 같이 같은 카메라 영역 진입과 타겟 중심 `0.030 m` 이내 접근으로 유지한다.
- EN: The success rule remains same-region entry plus reaching within `0.030 m` of the target center.

## Implementation / 구현

- KR: `observation_space`를 47에서 51로 늘려 그리퍼 카메라 `u`, `v`, `visible`, `depth` 특징을 추가한다.
- EN: Increase `observation_space` from 47 to 51 and add gripper-camera `u`, `v`, `visible`, and `depth` features.

- KR: 로그에 `target_gripper_camera_visible_rate`, `target_three_camera_visible_rate`, `mean_gripper_camera_target_error`를 추가한다.
- EN: Add `target_gripper_camera_visible_rate`, `target_three_camera_visible_rate`, and `mean_gripper_camera_target_error` to logs.

- KR: 전용 학습 스크립트 `scripts/train_coordinate_stage1_three_camera_baseline_128_1500_video.sh`를 사용한다.
- EN: Use the dedicated script `scripts/train_coordinate_stage1_three_camera_baseline_128_1500_video.sh`.

## Result / 결과

| metric | value |
| --- | ---: |
| smoke test | passed |
| training iterations | 1500 completed |
| mastered_region_count | 9 |
| target_three_camera_visible_rate | 0.9014 |

## Evidence / 근거 자료

- Record / 기록: [20260610_111518_run_three_camera_coordinate_baseline_1500iter.md](20260610_111518_run_three_camera_coordinate_baseline_1500iter.md)
- Plot / 그래프: [region mastery graph](artifacts/20260610_111518_review_three_camera_region_mastery_counts.png), [camera graph](artifacts/20260610_111518_review_three_camera_visibility_and_alignment.png), [success graph](artifacts/20260610_111518_review_three_camera_success_curve.png)
- Video / 영상: [20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4](../videos/20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4)

## Next Step / 다음 단계

- KR: 다음 학습은 7cm 근접 이후 3cm 중심 정밀 수렴을 강화한다.
- EN: The next training step should improve precise 3 cm center convergence after 7 cm proximity.
