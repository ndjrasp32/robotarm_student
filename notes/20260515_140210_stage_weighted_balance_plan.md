# 20260515_140210 stage weighted balance plan

## 선생님 의견

- 뒤쪽 결과가 앞쪽 결과에 영향을 미치면 전체 틀이 흐트러질 수 있다.
- 앞쪽 결과는 유지하고, 시간이 흐르면 앞쪽 결과 유지에 조금 더 가중치를 주는 방법을 고려한다.
- 단, 너무 크게 주면 최종 성공을 피하고 시간을 끄는 경향이 생길 수 있다.
- 최종 성공 보상은 조금 크게 잡되, 최단거리 루트 찾기에 과하게 영향을 주지 않는 선이 좋다.
- 최종 성공을 했을 때만 마지막 stage 품질 가중치를 주는 방식도 고려할 수 있다.

## Codex 제안

- stage3 유지 보상은 작게 둔다.
  - `stage3_time_preserve`는 stage3가 준비된 상태에서 시간이 지날수록 조금 생긴다.
  - 정렬, lateral line, touch 품질이 유지될 때만 보상을 받는다.
- 시간을 끄는 행동을 막기 위해 stage4 시간 벌점은 같이 조금 올린다.
- 최종 성공 step에서는 여전히 shaped reward를 끊고, 성공 보상만 준다.
- 대신 성공했을 때만 `terminal_success_quality`를 추가한다.
  - 최단거리 정렬
  - 빨간 구체 방향 진입 진행률
  - 성공 반경 안에서 중심에 더 가까운 정도
- 이렇게 하면 마지막 stage 보상이 실패 step에서 앞 단계 전체를 과하게 끌어당기는 일을 줄이고, 성공한 경우에만 좋은 성공을 더 선호하게 된다.

## 적용

- `stage3_time_preserve_weight` 추가
- `terminal_success_quality_weight` 추가
- `MT4_REACH_SUCCESS_BONUS` 환경변수 추가
- `mean_stage3_time_preserve` 지표 추가
- `mean_terminal_success_quality` 지표 추가
- `scripts/train_stage4_weighted_balance_128_300.sh` 추가

## 실험 설정

- `final_center_radius=0.045`
- `stage3_time_preserve_weight=1.6`
- `terminal_success_quality_weight=18.0`
- `success_bonus=64.0`
- `stage4_time_penalty=0.075`

## 실행

```bash
~/work/robotarm/mt4_isaac_lab_task/scripts/train_stage4_weighted_balance_128_300.sh --seed 42
MT4_PLOT_LABEL=20260515_140210_stage4_weighted_balance_128env_300iter \
  ~/work/robotarm/mt4_isaac_lab_task/scripts/plot_and_select_best.sh
```

## 평가 기준

- `stage3_touch_ready_rate`가 `0.045m` 이전 실험의 `0.3669`보다 유지 또는 개선되는지 본다.
- `success_rate`가 완전히 사라지지 않는지 본다.
- `stage4_time_pressure`가 커지는데도 성공률이 살아 있다면, 마지막 진입을 더 빨리 해결하는 방향으로 해석한다.
- `terminal_success_quality`가 기록되면 성공 step의 질을 따로 비교할 수 있다.

## 실행 결과

- run: `2026-05-15_14-08-19`
- best checkpoint: `model_1600.pt`
- success reason: `highest meaningful success_rate`
- `success_rate=0.01318359375`
- `stage4_center_ready_rate=0.01318359375`
- `stage4_push_ready_rate=0.05078125`
- `stage3_touch_ready_rate=0.37158203125`
- `stage2_pregrasp_ready_rate=0.38134765625`
- `mean_center_push_progress=0.5685770511627197`
- `mean_center_shortest_path_score=0.6180036067962646`
- `mean_stage4_time_pressure=0.13207276165485382`
- `mean_stage3_time_preserve=0.07407005876302719`
- `mean_terminal_success_quality=0.0`
- `mean_target_contact_penalty=0.0`

## 평가

- 이전 `0.045m` 실험과 비교해 성공률은 `0.0144 -> 0.0132`로 거의 유지되었다.
- `stage3_touch_ready_rate`는 `0.3669 -> 0.3716`으로 소폭 개선되었다.
- 학습 후반에는 `stage3_touch_ready_rate`가 0.7 이상까지 올라가므로, stage3 유지 보상은 의도한 방향으로 작동했다.
- 하지만 최종 성공률은 후반에 다시 낮아졌다.
- 즉, 이번 가중치는 앞 단계 보존에는 도움이 되었지만, 마지막 중심 진입을 충분히 강화하지는 못했다.
- `mean_terminal_success_quality=0.0`은 평균 성공이 매우 드물어 quality 신호가 충분히 학습되지 않았다는 뜻이다.

## 다음 제안

- stage3 유지 보상을 더 키우기보다, stage4 마지막 transition을 더 직접적으로 강화한다.
- 예를 들어 `stage4_push_ready_progress`를 약간 낮추거나, `center_push_progress`가 일정 값 이상일 때 terminal 근처 보상을 더 세분화한다.
- terminal quality는 성공했을 때만 적용되므로 안정적이지만, 성공이 너무 드물면 학습 신호가 약하다.
- 따라서 다음에는 "성공 직전 0.050m band" 같은 near-terminal 보상을 작게 추가하는 편이 좋다.
