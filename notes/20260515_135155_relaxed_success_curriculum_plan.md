# 20260515_135155 relaxed success curriculum plan

## 선생님 의견

- 최종 성공 기준이 너무 엄격하면 성공률이 거의 나오지 않는다.
- 먼저 성공률이 생기는 조건을 만들고, 그 다음 조건을 다시 엄격하게 줄여 가는 방향이 좋다.

## Codex 제안

- 현재 stage4의 최종 성공 반경은 기본 `0.035m`로 실험하고 있었다.
- 이전 best checkpoint의 `mean_distance`가 약 `0.052m`였기 때문에, `0.035m` 조건은 성공 신호가 너무 드물다.
- 먼저 `final_center_success_radius=0.055m`로 완화해 성공률을 만든다.
- 성공률이 생기면 다음 순서로 반경을 줄인다.
  - relaxed: `0.055m`
  - medium: `0.045m`
  - strict: `0.035m`
- 이 과정은 "처음부터 정답을 너무 어렵게 주지 않고, 가능한 성공을 만든 뒤 점점 정밀하게 만드는 curriculum"으로 학생들에게 설명할 수 있다.

## 적용

- `scripts/train_stage4_relaxed_success_128_300.sh` 추가
- 기존 task 이름 `Isaac-MT4-Simplified-Reach-Direct-v0` 유지
- 기존 strict/time-pressure 스크립트는 보존
- 새 스크립트는 `MT4_REACH_FINAL_CENTER_RADIUS=0.055`를 기본값으로 사용

## 실행

```bash
~/work/robotarm/robotarm_student/scripts/train_stage4_relaxed_success_128_300.sh --seed 42
MT4_PLOT_LABEL=20260515_135155_stage4_relaxed_success_128env_300iter \
  ~/work/robotarm/robotarm_student/scripts/plot_and_select_best.sh
```

## 평가 기준

- `success_rate`가 기존 `0.0005` 수준보다 의미 있게 증가하는지 본다.
- `stage4_center_ready_rate`도 함께 증가해야 한다.
- 단순히 완화 반경 안에 들어오는 것뿐 아니라 `mean_distance`, `mean_center_push_progress`, `mean_center_shortest_path_score`가 나빠지지 않는지 확인한다.
- 성공률이 생기면 다음 실험에서 `MT4_REACH_FINAL_CENTER_RADIUS=0.045`로 줄인다.

## 실행 결과

- run: `2026-05-15_13-49-56`
- best checkpoint: `model_1600.pt`
- success reason: `highest meaningful success_rate`
- `success_rate=0.028564453125`
- `stage4_center_ready_rate=0.041259765625`
- `stage3_touch_ready_rate=0.13330078125`
- `stage2_pregrasp_ready_rate=0.135009765625`
- `mean_distance=0.07203495502471924`
- `mean_center_push_progress=0.5714872479438782`
- `mean_center_shortest_path_score=0.6061863899230957`
- `mean_target_contact_penalty=0.0`

## 평가

- 성공 기준 완화는 즉시 효과가 있었다.
- 이전 실험의 성공률 `0.00048828125`보다 이번 best의 성공률 `0.028564453125`가 크게 높아졌다.
- 따라서 "먼저 성공 신호를 만들고 나서 조건을 엄격화한다"는 방향은 맞다.
- 단점도 확인되었다. best checkpoint는 성공률은 높지만 `stage2_pregrasp_ready_rate`와 `stage3_touch_ready_rate`가 낮다.
- 이는 성공 반경을 너무 넓히면 policy가 정교한 stage3 품질보다 완화된 성공 조건을 먼저 이용할 수 있음을 뜻한다.
- 다음 실험은 `0.055m`에서 계속 밀기보다 `0.045m`로 줄이고, stage3 품질이 유지되는 checkpoint를 고르는 방식이 좋다.

## 다음 제안

```bash
MT4_REACH_FINAL_CENTER_RADIUS=0.045 \
  ~/work/robotarm/robotarm_student/scripts/train_stage4_relaxed_success_128_300.sh --seed 42
```

이후 결과를 `0.055m` 실험과 비교한다.

- 성공률이 유지되면 다음은 `0.040m`
- 성공률이 사라지면 `0.050m`
- stage3가 무너지면 성공률보다 `stage3_touch_ready_rate`를 우선해서 checkpoint를 선택한다.
