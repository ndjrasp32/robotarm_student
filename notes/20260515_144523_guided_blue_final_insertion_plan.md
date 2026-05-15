# 20260515_144523 guided blue final insertion plan

## Teacher Idea

- 터미널이 잘 보이지 않으니, 지표만 보며 마지막 성공 단계를 맞추기가 어렵다.
- 파란 구체에 정렬된 상태로 집게가 도착하면, 그 다음에는 파란 구체를 빨간 구체 방향으로 조금씩 옮긴다.
- 이 과정을 두세 번 반복하면 로봇팔은 이미 정렬된 상태로 빨간 구체 가까이에 있게 된다.
- 그러면 마지막 최종 스테이지의 성공률이 올라갈 수 있다.

## Codex Proposal

이 아이디어는 기존 task를 버리는 것이 아니라, 기존 blue pregrasp marker를 curriculum guide로 확장하는 방식이다.

- 빨간 구체는 계속 최종 목표로 유지한다.
- 파란 구체는 처음에는 기존 pregrasp 위치에 둔다.
- 집게 중심이 현재 파란 구체에 가까워지고, 삽입 방향 정렬이 유지되면 파란 구체를 빨간 구체 방향으로 한 단계 이동한다.
- 기본값은 3단계 이동이다.
- 마지막 파란 구체는 빨간 구체 중심까지 들어가지 않고, 기존 touch target 방향의 약 70%까지만 이동한다.
- 이 상태가 되면 `final_insertion_reward`를 켜서 빨간 구체 중심으로 짧고 직접적인 진입을 유도한다.

## Why This May Work

기존 방식은 마지막에 한 번에 빨간 구체 중심으로 들어가는 보상을 줬다. 그러면 정책이 stage3에서 안정적으로 대기하더라도, 마지막으로 어디까지 얼마나 밀어 넣어야 하는지 충분히 배우기 어렵다.

이번 방식은 "움직이는 파란 구체를 따라가라"는 더 직관적인 중간 목표를 제공한다. 학생들에게는 다음처럼 설명할 수 있다.

> 파란 구체는 선생님이 손가락으로 안내하는 중간 지점이다. 로봇팔이 한 지점에 잘 도착하면, 선생님 손가락이 목표물 쪽으로 한 칸 움직인다.

## Implementation

- `MT4_REACH_MOVING_PREGRASP=1`
- `MT4_REACH_MOVING_PREGRASP_STEPS=3`
- `MT4_REACH_MOVING_PREGRASP_FINAL_FRACTION=0.70`
- `MT4_REACH_MOVING_PREGRASP_STEP_RADIUS=0.055`
- `MT4_REACH_MOVING_PREGRASP_REWARD_WEIGHT=10.0`
- `MT4_REACH_FINAL_INSERTION_WEIGHT=48.0`

## Metrics To Watch

- `mean_moving_pregrasp_fraction`
- `moving_pregrasp_final_rate`
- `mean_moving_pregrasp_reward`
- `mean_final_insertion_reward`
- `stage3_latched_rate`
- `stage4_center_ready_rate`
- `success_rate`
- `mean_target_contact_penalty`

## Test Command

```bash
~/work/robotarm/mt4_isaac_lab_task/scripts/train_stage4_guided_blue_128_300.sh --seed 42
```

## Expected Interpretation

- `moving_pregrasp_final_rate`가 올라가면 파란 구체 단계 이동 curriculum은 작동한다.
- `mean_final_insertion_reward`가 생기는데 `stage4_center_ready_rate`가 그대로라면, 마지막 보상은 감지되지만 성공 조건까지는 부족한 것이다.
- `mean_target_contact_penalty`가 올라가면 파란 구체가 너무 빨간 구체에 가깝거나, final insertion reward가 충돌을 허용하는 방향으로 강한 것이다.

## Result

- run: `2026-05-15_14-54-32`
- strict success based best checkpoint: `model_1600.pt`
- guided-progress final checkpoint: `model_1899.pt`

`model_1600.pt`는 strict `success_rate=0.018798828125` 때문에 best로 선택되었다. 하지만 이 값은 moving-blue curriculum이 학습되기 전 시작점에 가까운 값이다.

`model_1899.pt` 기준 변화:

- `stage3_latched_rate=0.75146484375`
- `stage3_touch_ready_rate=0.682373046875`
- `stage4_push_ready_rate=0.451416015625`
- `mean_center_push_progress=0.6830252408981323`
- `mean_best_center_push_progress=0.7647878527641296`
- `mean_moving_pregrasp_fraction=0.38554686307907104`
- `moving_pregrasp_final_rate=0.548583984375`
- `mean_final_insertion_reward=0.04587549716234207`
- `mean_target_contact_penalty=0.0`
- `success_rate=0.0009765625`

## Interpretation

- 선생님이 제안한 "파란 구체를 빨간 구체 방향으로 단계적으로 옮기는 방식"은 작동했다.
- 파란 guide를 끝까지 따라가는 비율이 절반 이상으로 올라갔고, stage4 push 지표도 크게 좋아졌다.
- 충돌 벌점은 계속 0이라, 빨간 구체를 치고 들어가는 식의 나쁜 해법은 아직 보이지 않는다.
- 다만 strict final center success는 오히려 낮다. 즉, 정책은 가까이 밀고 들어가는 흐름을 배웠지만, 현재 성공 반경과 중심 판정은 아직 너무 좁거나 보상 선택 기준과 맞지 않는다.

## Next Candidate

다음 실험은 두 갈래 중 하나가 좋다.

1. 학습용 성공 반경을 `0.045m -> 0.050m` 정도로 아주 조금 완화해서 성공 신호를 만든다.
2. checkpoint selector를 strict success 단독이 아니라 `moving_pregrasp_final_rate`, `stage4_push_ready_rate`, `mean_final_insertion_reward`를 함께 보는 guided-stage 기준으로 분리한다.

시각화는 `model_1600.pt`뿐 아니라 `model_1899.pt`도 따로 play해야 한다. 이번 실험의 학습된 변화는 `model_1899.pt` 쪽에 있기 때문이다.
