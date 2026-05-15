# 20260515_153741 blue funnel reward plan

## Teacher Idea

- 파란 구체를 딱 한 점으로 터치하게 하는 방식은 너무 빡빡하다.
- 빨간 구체처럼 파란 구체도 진입 유도 역할을 해야 한다.
- 로봇팔 방향으로 열린 부채꼴 영역을 만들고, 그 영역 안에서 파란 중심에 가까워질수록 보상을 크게 주면 더 안정적일 수 있다.
- 수치가 튀는 현상이 있더라도 완전히 이상한 방향이 아니면 더 오래 학습했을 때 결과가 나올 가능성이 있다.

## Codex Interpretation

파란 구체는 최종 목표라기보다 guide point다. 그래서 정확한 중심점 보상만 주면 학습 신호가 너무 희박하다. 이번 변경은 파란 구체 뒤쪽, 즉 로봇팔이 접근해 와야 하는 방향에 funnel reward를 추가한다.

- 파란 구체 바로 근처에서는 중심 정렬을 더 강하게 요구한다.
- 파란 구체에서 멀리 떨어진 로봇팔 쪽에서는 허용 반경을 넓혀 초기 진입 방향을 잡게 한다.
- 파란 구체를 지나쳐 빨간 구체 쪽으로 들어간 위치에는 이 funnel reward를 거의 주지 않는다.
- 기존 step gate는 유지한다. funnel reward는 gate를 대체하지 않고, gate에 도달하기 전까지 길을 안내한다.

## Added Parameters

- `MT4_REACH_MOVING_PREGRASP_FUNNEL_WEIGHT`
- `MT4_REACH_MOVING_PREGRASP_FUNNEL_DEPTH`
- `MT4_REACH_MOVING_PREGRASP_FUNNEL_MIN_RADIUS`
- `MT4_REACH_MOVING_PREGRASP_FUNNEL_MAX_RADIUS`

## Default Training Setup

기존 300-iteration script에는 완만한 funnel을 추가한다.

- `step_radius=0.035`
- `hold_steps=4`
- `moving_reward=16`
- `funnel_weight=10`
- `funnel_depth=0.090`
- `funnel_radius=0.020-0.080`

긴 학습용 script는 먼저 성공 사례를 많이 만들기 위해 더 넓은 funnel에서 시작한다.

- script: `scripts/train_stage4_blue_funnel_128_800.sh`
- `max_iterations=800`
- `step_radius=0.045`
- `hold_steps=2`
- `moving_reward=24`
- `funnel_weight=14`
- `funnel_depth=0.110`
- `funnel_radius=0.024-0.095`

## What To Watch

- `mean_moving_pregrasp_funnel_reward`: 파란 guide 영역을 따라 접근하는 보상
- `moving_pregrasp_step_ready_rate`: 현재 파란 guide 중심 근처에 들어온 비율
- `moving_pregrasp_final_rate`: 마지막 파란 guide까지 도달한 비율
- `stage4_center_ready_rate`: 빨간 중심 성공 반경에 들어온 비율
- `mean_target_contact_penalty`: 빨간 목표를 다른 링크가 건드리는지 여부

## Next Experiment

먼저 긴 학습을 다음 명령으로 진행한다.

```bash
~/work/robotarm/mt4_isaac_lab_task/scripts/train_stage4_blue_funnel_128_800.sh --seed 42
```

결과가 좋아지면 그 checkpoint에서 `step_radius=0.035`, `hold_steps=4`로 이어서 학습하고, 이후 `0.018`, `8 frames`로 엄격화한다.

## Training Result

- run: `2026-05-15_15-38-38`
- script: `scripts/train_stage4_blue_funnel_128_800.sh --seed 42`
- resume checkpoint: `2026-05-15_14-54-32/model_1899.pt`
- selected checkpoint: `model_2100.pt`
- plot snapshot: `logs/plots/20260515_153838_20260515_153741_blue_funnel_128env_800iter`
- experiment report: `experiments/20260515_153838_20260515_153741_blue_funnel_128env_800iter.md`

Selected checkpoint metrics:

- `success_rate=0.00048828125`
- `stage3_latched_rate=0.91259765625`
- `stage3_insertion_ready_rate=0.49169921875`
- `stage4_center_ready_rate=0.00048828125`
- `stage4_push_ready_rate=0.23388671875`
- `moving_pregrasp_final_rate=0.521728515625`
- `mean_moving_pregrasp_funnel_reward=0.16175898909568787`
- `mean_final_insertion_reward=0.014700287021696568`
- `mean_distance=0.05694566294550896`
- `mean_target_contact_penalty=0.0`

Training observation:

- 학습 초중반에는 `moving_pregrasp_final_rate`가 0.3-0.5대로 빠르게 올라갔다.
- 후반에는 파란 funnel guide를 따라가는 행동이 더 강해져 `moving_pregrasp_final_rate`가 0.8대까지 올라간 구간이 있었다.
- 동시에 `mean_distance`는 약 0.03m 수준까지 내려갔지만, `stage4_center_ready_rate`와 `mean_final_insertion_reward`는 거의 0에 머물렀다.
- 즉, 이번 실험은 파란 유도 영역을 따라가는 행동은 만들었지만, 빨간 구체 중심을 집게 사이에 넣는 최종 삽입 행동은 아직 별도 curriculum이 필요하다는 결과다.
- 후반에는 `mean_object_overlap`이 약 0.006-0.008 수준으로 생겼다. 물리 충돌은 아니지만 target 내부로 파고드는 geometry overlap 경향이 조금 보였으므로, 다음 단계에서는 final insertion 보상과 overlap penalty를 같이 조정해야 한다.

## Next Step

다음 실험은 두 갈래로 나누는 것이 좋다.

1. Guide 안정화:
   - 이번 후반 checkpoint를 사용해 `step_radius=0.035`, `hold_steps=4`로 조인다.
   - 목표는 `moving_pregrasp_final_rate`를 크게 잃지 않으면서 `stage3_touch_ready_rate`를 회복하는 것이다.
2. Final insertion 전용:
   - 파란 guide가 끝난 상태에서 시작하는 replay/curriculum을 따로 두고, 집게 중심과 빨간 구체 중심의 거리를 직접 줄인다.
   - 목표는 `stage4_center_ready_rate`와 `mean_final_insertion_reward`를 실제로 키우는 것이다.
