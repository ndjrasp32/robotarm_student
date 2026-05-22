# 20260515_143522 stage latch progressive plan

## Branch

`experiment/stage-latch-progressive-weighting`

## Teacher Idea

- 앞 스테이지를 완수한 시점에서 다음 스테이지에 진입한다.
- 후반 스테이지 성공에 가까워질수록 이미 확보한 스테이지 점수에 더 강한 가중치를 준다.
- 이렇게 하면 뒤 스테이지 보상이 앞 스테이지를 흐트러뜨리는 문제를 줄일 수 있을 것 같다.

## Codex Proposal

이번 branch에서는 stage를 "항상 다시 계산되는 순간 조건"과 "한 번 확보되면 episode 동안 유지되는 latch 조건"으로 분리한다.

- `stage1_latched`: 집게 진입 방향 정렬을 한 번 확보했는가
- `stage2_latched`: 파란 구체 근처 접촉/대기 조건을 한 번 확보했는가
- `stage3_latched`: 파란 구체 이후 빨간 구체 방향 진입 조건을 한 번 확보했는가

그리고 다음 reward를 작게 추가한다.

- `stage_latch_reward`: 확보한 stage를 현재도 잘 유지하면 받는 점수
- `progressive_stage_weight`: stage4 방향으로 더 들어갈수록 `stage_latch_reward`를 조금 키우는 multiplier

## Why This Is Different From Adding More Reward Terms

이전 방식은 여러 reward가 동시에 켜져 서로 당기는 힘이 생길 수 있었다.

이번 방식은 "앞 단계를 통과해야 다음 신호가 의미를 갖는다"는 구조를 더 분명하게 만든다. 그래서 학생들에게도 다음처럼 설명할 수 있다.

> 로봇팔은 먼저 방향을 맞추고, 그 다음 파란 위치를 확보하고, 그 다음 빨간 목표 중심으로 들어간다. 이전 단계를 확보하지 못하면 뒤 단계 보상은 큰 의미를 갖지 않는다.

## Initial Parameters

- `MT4_REACH_STAGE_LATCH_WEIGHT=1.5`
- `MT4_REACH_PROGRESSIVE_STAGE_WEIGHT=0.8`
- `MT4_REACH_STAGE3_TIME_PRESERVE_WEIGHT=0.9`
- `MT4_REACH_NEAR_TERMINAL_WEIGHT=4.0`
- `MT4_REACH_FINAL_CENTER_RADIUS=0.045`
- `MT4_ENTROPY_COEF=0.0030`

## Test Command

```bash
~/work/robotarm/robotarm_student/scripts/train_stage4_latched_progressive_128_300.sh --seed 42
```

## Metrics To Watch

- `stage1_latched_rate`
- `stage2_latched_rate`
- `stage3_latched_rate`
- `mean_stage_latch_reward`
- `mean_progressive_stage_weight`
- `stage3_touch_ready_rate`
- `stage4_center_ready_rate`
- `success_rate`
- `mean_target_contact_penalty`

## Expected Result

좋은 방향이라면 stage3가 높아지더라도 stage4 center가 완전히 사라지지 않아야 한다. `stage_latch_reward`가 높아지는데 `success_rate`가 떨어지면, latch 유지 보상이 너무 커서 로봇팔이 마지막 진입을 피하는 것이다.

## Result

- run: `2026-05-15_14-36-12`
- best checkpoint: `model_1600.pt`
- `success_rate=0.013671875`
- `stage1_latched_rate=0.941162109375`
- `stage2_latched_rate=0.37158203125`
- `stage3_latched_rate=0.37158203125`
- `stage3_touch_ready_rate=0.3564453125`
- `stage4_center_ready_rate=0.013671875`
- `stage4_push_ready_rate=0.044189453125`
- `mean_stage_latch_reward=0.330735445022583`
- `mean_progressive_stage_weight=1.0618454217910767`
- `mean_target_contact_penalty=0.0`

## Interpretation

- latch metric 자체는 정상 작동했다.
- stage1은 매우 안정적이고, stage2/stage3도 episode 중 확보된 상태를 기록할 수 있게 되었다.
- 하지만 best checkpoint는 run 시작점인 `model_1600.pt`로 선택되었고, 추가 학습 후반에는 stage3 유지가 강해지는 대신 최종 center 성공률이 거의 사라졌다.
- 따라서 이 실험은 "앞 단계 보존"에는 효과가 있었지만, "보존된 상태에서 빨간 구체 중심으로 더 밀어 넣는 행동"은 충분히 만들지 못했다.

## Next Candidate

다음 실험은 latch 보상을 더 키우기보다, `stage3_latched` 이후에만 켜지는 final insertion 전용 신호를 분리하는 쪽이 좋다.

- `stage_latch_weight`는 낮추거나 유지한다.
- `progressive_stage_weight`는 유지하되 final center progress를 직접 키운다.
- final center 근처에서는 시간 벌점을 유지하고, 성공 조건에 들어오면 episode 종료 보상을 크게 준다.
- 학생 설명에서는 "앞 단계는 잠금 해제 조건이고, 마지막 단계는 별도 미션"으로 나누어 말한다.
