# 20260515_141527 near-terminal reward plan

## Goal

Stage 4에서 집게 중심이 빨간 구체 중심 가까이까지 왔지만 마지막 성공 반경 안으로 들어가지 못하는 병목을 줄인다.

## Teacher Idea

- 앞 단계가 유지된 상태에서 마지막 단계만 더 잘 밀어 넣고 싶다.
- 최종 성공 직전까지는 시간 벌점을 유지한다.
- 성공 위치에 도착하면 시간 벌점과 추가 shaping을 멈추고 성공으로 episode를 종료한다.
- 뒷 단계 보상이 앞 단계 행동을 흐트러뜨리지 않도록, stage 3 유지와 stage 4 진입 보상의 균형을 잡고 싶다.
- 탐색은 너무 낮추지 말고 약간만 유지해 더 나은 체크포인트를 찾게 한다.

## Codex Proposal

- 기존 성공 조건은 그대로 둔다: `final_center_success_radius=0.045m`.
- 성공 반경 바로 바깥쪽 `near_terminal_radius=0.050m`에 작은 bridge reward를 추가한다.
- 이 보상은 다음 조건을 모두 만족할 때만 적용한다.
  - stage 3 ready 상태
  - 아직 success는 아님
  - 집게 중심과 빨간 구체 중심 거리가 `0.050m`보다 작음
  - body-target clearance penalty가 없음
- 보상값은 단순 거리만 보지 않고 다음 항목을 함께 곱한다.
  - 빨간 구체 중심으로 최단거리 방향에 가까운가
  - 파란 구체에서 빨간 구체 방향으로 실제 push progress가 있는가
- stage 3 유지 보상은 `1.6 -> 1.2`로 살짝 낮춘다. 마지막 진입을 더 허용하기 위해서다.
- entropy는 `0.0025 -> 0.0030`으로 아주 조금 올린다. 탐색을 완전히 줄이지 않기 위해서다.

## Why Not Add Many More Terms?

로봇팔 조작 task에서 reward 항목이 여러 개인 것은 드문 일이 아니다. 특히 접근, 정렬, 접촉, 삽입, 충돌 회피처럼 순서가 있는 문제는 하나의 최종 성공 보상만으로는 학습 신호가 너무 희박해진다.

다만 항목이 많아질수록 위험도 커진다.

- 서로 반대 방향의 보상이 동시에 걸리면 정책이 흔들릴 수 있다.
- 중간 보상이 너무 크면 최종 성공을 회피하고 중간 상태에서 머무를 수 있다.
- 학생들이 원인을 해석하기 어려워진다.

그래서 이번 변경은 새 항목을 하나만 추가한다. 역할은 "최종 성공 직전 5mm 구간을 연결하는 안내 신호"로 제한한다. 성공 조건을 바꾸거나 충돌 벌점을 약화하지 않는다.

## Script

```bash
~/work/robotarm/robotarm_student/scripts/train_stage4_near_terminal_128_300.sh --seed 42
```

기본값:

- `MT4_REACH_FINAL_CENTER_RADIUS=0.045`
- `MT4_REACH_NEAR_TERMINAL_RADIUS=0.050`
- `MT4_REACH_NEAR_TERMINAL_WEIGHT=5.0`
- `MT4_REACH_STAGE3_TIME_PRESERVE_WEIGHT=1.2`
- `MT4_ENTROPY_COEF=0.0030`

## Metrics To Watch

- `success_rate`
- `stage3_touch_ready_rate`
- `stage4_center_ready_rate`
- `stage4_push_ready_rate`
- `mean_near_terminal_reward`
- `mean_stage3_time_preserve`
- `mean_stage4_time_pressure`
- `mean_target_contact_penalty`

## Expected Interpretation

- `mean_near_terminal_reward`가 올라가는데 `success_rate`가 오르지 않으면, 성공 반경이나 집게 중심 정의가 아직 너무 엄격할 수 있다.
- `stage3_touch_ready_rate`가 크게 떨어지면, 마지막 보상이 앞 단계 안정성을 방해한 것이다.
- `mean_target_contact_penalty`가 커지면, 빨간 구체를 밀어 치는 방식으로 보상을 얻는 문제가 생긴 것이다.

## Result

- Run: `2026-05-15_14-18-24`
- Best checkpoint: `model_1600.pt`
- Selection reason: `highest meaningful success_rate`
- `success_rate=0.01416015625`
- `stage3_touch_ready_rate=0.370849609375`
- `stage4_center_ready_rate=0.01416015625`
- `stage4_push_ready_rate=0.037841796875`
- `mean_near_terminal_reward=0.034814152866601944`
- `mean_stage3_time_preserve=0.07492419332265854`
- `mean_stage4_time_pressure=0.13307860493659973`
- `mean_target_contact_penalty=0.0`

## Evaluation

- 새 `near_terminal_reward` 지표는 정상적으로 기록되었다.
- 충돌 벌점은 0으로 유지되어, 빨간 구체를 치는 방향으로 성공을 얻는 문제는 보이지 않았다.
- best checkpoint가 `model_1600.pt`로 선택되었다. 이번 run의 시작 checkpoint 근처가 가장 좋았다는 뜻이다.
- 학습 중반에는 stage3 지표가 0.7-0.8까지 올라갔지만 final success는 낮아졌다. 즉 stage3를 안정적으로 유지하는 정책은 강화되었으나, 마지막 중심 진입은 아직 별도 구조가 필요하다.

## Next Idea: Stage Latch + Progressive Stage Weighting

선생님 제안처럼 앞 스테이지를 완수한 시점에서 다음 스테이지로 진입하고, 후반 스테이지 성공에 가까워질수록 이미 확보한 스테이지 점수의 가중치를 강하게 주는 방법이 타당하다.

이 방식은 단순히 보상 항목을 더 늘리는 것보다 구조적으로 낫다. 이유는 보상이 항상 켜져 있는 것이 아니라, stage gate를 통과한 뒤에만 의미를 갖기 때문이다.

다만 다음을 조심해야 한다.

- stage 확보 점수가 너무 크면 로봇팔이 앞 단계에서 머무를 수 있다.
- 뒤 stage 성공률이 낮을 때는 progressive weight가 너무 늦게 켜져 학습 신호가 약할 수 있다.
- 그래서 처음에는 stage별 latch 지표를 로그로 분리하고, reward weight는 작게 시작해야 한다.

다음 실험 후보:

- `stage1_latched`: 진입 방향 정렬 확보
- `stage2_latched`: 파란 구체 접촉/대기 확보
- `stage3_latched`: 파란 구체 중심 정렬 및 빨간 구체 방향 진입 확보
- `stage4_progress_weight`: stage4 progress가 올라갈수록 stage3 latch 유지 보상의 가중치를 서서히 올림
- success 시에는 기존처럼 terminal reward만 남기고 episode 종료
