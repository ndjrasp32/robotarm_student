# 20260515_130240 stage4 strong push plan

## 선생님 의견

- 마지막 중심 근처까지 왔으면 빨간 구체 쪽으로 더 확실하게 밀어 넣어야 한다.
- 지금 과제는 전체 동작보다 마지막 단계 성공률을 먼저 잡는 것이다.
- 최종적으로 빨간 구체 중심이 집게 가운데에 들어와 있어야 다음 grasp 단계로 넘어갈 수 있다.

## Codex 제안

- 기존 `center_push_progress`는 현재 위치가 삽입 경로에서 얼마나 전진했는지 알려준다.
- 하지만 같은 위치에서 머무르거나 약간 뒤로 빠졌다가 다시 오는 행동을 충분히 막지는 못한다.
- 그래서 episode 중 이전보다 더 안쪽으로 들어갔을 때만 보상하는 `center_push_improvement`를 추가한다.
- 또한 `center_push_progress > 0.5` 이후를 더 강하게 보상하는 depth reward를 추가한다.
- replay reset 상태에서는 이미 진행된 위치에서 시작할 수 있으므로, reset 직후의 progress를 기준점으로 잡고 그보다 더 들어갔을 때만 improvement 보상을 준다.

## 적용

- `mean_best_center_push_progress` 지표 추가
- `mean_center_push_improvement` 지표 추가
- `stage4_center_push_improvement_weight` 추가
- `stage4_center_push_depth_weight` 추가
- `center_push_improvement_scale` 추가
- `stage4_push_ready_progress`를 환경변수로 조절 가능하게 변경
- 강한 마지막 push 학습 스크립트 추가:

```bash
~/work/robotarm/mt4_isaac_lab_task/scripts/train_stage4_push_strong_replay_128_300.sh --seed 42
```

## 기대

- `mean_best_center_push_progress`가 기존보다 올라가야 한다.
- `mean_center_push_improvement`가 완전히 0에 머물지 않아야 한다.
- `stage4_push_ready_rate`는 기준을 0.65로 올렸기 때문에 처음에는 낮아질 수 있다.
- 최종 판단은 `stage4_center_ready_rate`, `success_rate`, `mean_target_contact_penalty`를 함께 본다.

## 실행 결과

- run: `2026-05-15_13-03-24`
- best checkpoint: `model_1249.pt`
- `success_rate=0.000244140625`
- `stage4_center_ready_rate=0.000244140625`
- `stage4_push_ready_rate=0.264892578125`
- `mean_center_push_progress=0.6130448579788208`
- `mean_best_center_push_progress=0.6594560146331787`
- `mean_center_push_improvement=0.0006966536166146398`
- `mean_target_contact_penalty=0.0`
- plot snapshot: `logs/plots/20260515_130324_stage4_strong_push_replay_128env_300iter`

## 평가

- 이전 center-push 실험의 best checkpoint는 `mean_center_push_progress=0.5227710008621216`이었다.
- 이번 strong-push 실험은 `mean_center_push_progress=0.6130448579788208`, `mean_best_center_push_progress=0.6594560146331787`로 더 깊게 들어갔다.
- `stage4_push_ready_rate`는 0.65 기준으로 높였기 때문에 이전보다 낮아졌지만, 더 엄격한 기준에서도 0.26 수준이 나왔다.
- `stage4_center_ready_rate`와 `success_rate`가 0이 아닌 값으로 다시 나타났다.
- 다만 성공률은 아직 매우 낮다. 다음 병목은 "더 깊게 밀어 넣는 것"이 아니라, 깊게 들어가면서도 lateral error와 중심 거리 정밀도를 유지하는 것이다.

## 다음 제안

- 다음 실험은 push weight를 더 키우기보다, center success 근처 상태를 더 많이 replay state로 수집하는 편이 좋다.
- 또는 final center radius를 수업용으로 잠깐 `0.040~0.045`로 완화해 성공 샘플을 늘린 뒤 다시 줄이는 curriculum이 좋다.
