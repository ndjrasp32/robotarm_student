# 20260610_131608 1cm 거리 기준과 지나침 억제 보정

## 질문 / Question

- KR: 목표 위치를 더 정확히 따라가게 하려면 성공 거리 기준을 1cm로 강화하고, 목표를 지나쳤다가 돌아오는 행동을 줄여야 하는가?
- EN: Should the success distance be tightened to 1 cm and should overshoot-and-return behavior be discouraged?

## 판단 / Decision

- KR: 반영한다. 이전 3cm 기준은 영역 학습에는 도움이 되었지만, 데모에서 목표 중심을 정확히 찍는 기준으로는 느슨했다.
- EN: Apply the change. The earlier 3 cm rule helped region learning, but it was loose for demo-level target-center tracking.

- KR: 추적 보상은 실제 그리퍼 중심과 목표 지점 사이의 거리 중심으로 둔다.
- EN: Keep tracking reward focused on the actual gripper-center to target distance.

- KR: 목표를 지나쳐 로봇 반대편으로 넘어갔다가 되돌아오는 움직임은 `target_overshoot` 벌점으로 줄인다.
- EN: Reduce motion that passes beyond the target and returns by adding a `target_overshoot` penalty.

- KR: 가능하면 로봇 쪽이나 위쪽에서 목표로 접근하도록 `preferred_approach_error`를 보상과 로그에 넣는다.
- EN: Add `preferred_approach_error` to rewards and logs so the arm prefers approaching from the robot side or from above.

- KR: 접근 방향 선호는 성공 반경 1cm와 별개로, 로봇 쪽 또는 위쪽에서 약 3cm 여유를 두고 들어오는 상태를 더 좋게 본다.
- EN: The approach preference is separate from the 1 cm success radius and prefers entering with about 3 cm clearance from the robot side or from above.

## 수정 내용 / Changes

- KR: `center_success_radius`를 `0.030 m`에서 `0.010 m`로 강화했다.
- EN: Changed `center_success_radius` from `0.030 m` to `0.010 m`.

- KR: 목표 중심 보상을 더 정밀하게 만들기 위해 `precision_center_exp_scale`을 추가했다.
- EN: Added `precision_center_exp_scale` for a sharper target-center reward.

- KR: Stage 1 보상에 `target_overshoot_penalty_weight`와 `preferred_approach_weight`를 추가했다.
- EN: Added `target_overshoot_penalty_weight` and `preferred_approach_weight` to Stage 1 rewards.

- KR: `preferred_approach_margin`은 `0.030 m`로 두었다.
- EN: Set `preferred_approach_margin` to `0.030 m`.

- KR: 학습 로그에 `mean_target_overshoot`, `mean_preferred_approach_error`, `center_1cm_rate`를 추가했다.
- EN: Added `mean_target_overshoot`, `mean_preferred_approach_error`, and `center_1cm_rate` to training logs.

- KR: 리포트 도구와 기준 문서도 1cm 기준으로 바꿨다.
- EN: Updated the report tool and baseline documents to use the 1 cm rule.

## 다음 확인 / Next Check

- KR: Stage 1을 다시 학습한 뒤 `center_1cm_rate`, `mean_target_overshoot`, 랜덤 데모 영상을 함께 본다.
- EN: After rerunning Stage 1, review `center_1cm_rate`, `mean_target_overshoot`, and the random demo video together.
