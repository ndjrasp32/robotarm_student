# 2026-06-10 Camera-Only Region Matching / 카메라 전용 영역 매칭

## Summary / 요약

- KR: 랜덤 9영역 시연이 타겟을 안정적으로 잡지 못했기 때문에, 타겟 생성 좌표와 정책 입력을 분리하고 두 대의 카메라 관측만으로 영역을 추정하도록 학습 구조를 바꿨다.
- EN: The random 9-region demo did not reliably acquire the target, so the learning setup was changed to separate target-generation coordinates from policy input and infer the target region only from two camera observations.

## Learning Question / 학습 질문

- KR: 실제 로봇팔은 타겟 좌표를 직접 받을 수 없는데, 시뮬레이션 학습에서도 카메라 두 대로 인식한 영역만 사용해 접근 방식을 선택할 수 있는가?
- EN: Since the real robot arm cannot receive target coordinates directly, can the simulation policy choose its approach using only the region inferred from two cameras?

## Decision / 결정

- KR: 타겟 영역 1-9는 로봇팔 기준 좌표로 생성하지만, 정책 입력과 시연 접근 선택에는 생성 좌표를 넣지 않는다. 학습과 시연은 `camera_estimated_region_id`를 기준으로 움직이고, 생성 좌표는 검증과 overlay용 라벨로만 사용한다.
- EN: Regions 1-9 are generated in the robot-frame workspace, but generated coordinates are not given to the policy or demo approach logic. Training and demos use `camera_estimated_region_id`; generated coordinates remain only as validation and overlay labels.

## Student Reading Order / 학생이 볼 순서

1. [01_plan_camera_only_region_matching.md](01_plan_camera_only_region_matching.md)
2. [02_run_20260610_095546_camera_only_region_matching_1500.md](02_run_20260610_095546_camera_only_region_matching_1500.md)
3. [20260610_074525_demo_9region_random_policy_2min_labeled.mp4](../videos/20260610_074525_demo_9region_random_policy_2min_labeled.mp4)
4. [20260610_073944_demo_9region_random_policy_2min_sequence.csv](../videos/20260610_073944_demo_9region_random_policy_2min_sequence.csv)

## Result Snapshot / 결과 요약

| item | value |
| --- | --- |
| policy input / 정책 입력 | two-camera estimated region / 두 카메라 추정 영역 |
| generated coordinate use / 생성 좌표 사용처 | target generation, validation, overlay only / 타겟 생성, 검증, overlay 전용 |
| mastered regions / 마스터 영역 | 9 / 9 |
| camera_region_match_rate | 1.0000 |
| near_center_7cm_rate | 0.8667 |
| strict 3cm success, final batch / 최종 batch 기준 3cm 성공률 | 0.0005 |

## Interpretation / 해석

- KR: 영역을 카메라 기반으로 추정하는 구조는 작동했고 9개 영역 마스터리 카운트도 채워졌다. 다만 최종 batch의 3cm 성공률은 낮아서, 시연용 접근은 카메라 영역 선택만으로 충분하지 않고 실제 타겟 중심으로 안정적으로 수렴하는 제어 개선이 더 필요하다.
- EN: Camera-based region estimation worked and all 9 region mastery counts were filled. However, the final-batch strict 3 cm success rate remained low, so demos still need stronger control convergence toward the true target center after the camera-based region choice.

## Source Archive / 원자료

- Plan archive / 계획 원본: [20260610_camera_only_region_matching_plan.md](../../notes/20260610_camera_only_region_matching_plan.md)
- Run archive / 실행 원본: [20260610_095546_camera_only_region_matching_1500.md](../../experiments/20260610_095546_camera_only_region_matching_1500.md)
- Plot archive / 그래프 원본: [20260610_095546_camera_only_region_matching_1500](../../logs/plots/20260610_095546_camera_only_region_matching_1500/)
