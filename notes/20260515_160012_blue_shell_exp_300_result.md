# 20260515_160012 blue shell exponential 300-iteration result

## Run

- script: `scripts/train_stage4_blue_center_128_300.sh --seed 42`
- run: `2026-05-15_15-57-15`
- resume checkpoint: `2026-05-15_14-54-32/model_1899.pt`
- selected checkpoint: `model_2100.pt`
- plot snapshot: `logs/plots/20260515_155715_20260515_155715_blue_shell_exp_128env_300iter`
- report: `experiments/20260515_155715_20260515_155715_blue_shell_exp_128env_300iter.md`

## Teacher Idea Tested

- 파란 guide에 같은 거리권 반복 보상이 생기지 않도록 one-shot shell reward를 준다.
- 가까워질수록 지수적으로 보상이 커지도록 한다.
- 마지막 파란 guide가 빨간 중심에 있을 때, 집게 중심이 그 지점에 들어오면 성공으로 본다.

## Main Metrics

- `success_rate=0.00146484375`
- `stage3_latched_rate=0.9013671875`
- `stage3_insertion_ready_rate=0.798583984375`
- `stage4_center_ready_rate=0.000732421875`
- `moving_pregrasp_final_rate=0.000732421875`
- `moving_pregrasp_step_ready_rate=0.019287109375`
- `mean_moving_pregrasp_exp_reward=0.07414236664772034`
- `mean_moving_pregrasp_shell_improvement=0.014892578125`
- `mean_best_moving_pregrasp_distance=0.15152236819267273`
- `mean_distance=0.06119658797979355`
- `mean_target_contact_penalty=0.0`

## Interpretation

새 보상은 정상적으로 작동했다. `mean_moving_pregrasp_exp_reward`와 `mean_moving_pregrasp_shell_improvement`가 0이 아니며, `blue_final_center_ready_rate`도 학습 중 아주 낮게나마 발생했다.

하지만 300 iteration 조건에서는 마지막 파란 guide까지 거의 도달하지 못했다. selected checkpoint 기준 `moving_pregrasp_final_rate=0.000732421875`이고, `moving_pregrasp_step_ready_rate=0.019287109375`라서 현재 병목은 최종 삽입 보상보다 moving guide gate 자체다.

특히 `stage3_insertion_ready_rate`는 약 0.80, `stage3_latched_rate`는 약 0.90으로 높다. 즉 기본 정렬/진입 준비는 잘 된다. 그런데 `0.035m` 반경 안에서 `4 frames` 유지해야 파란 guide가 다음 단계로 넘어가는 조건이 너무 엄격해, guide가 끝까지 진행되지 않는다.

## Recommendation

다음 실험은 reward를 더 복잡하게 늘리기보다 gate를 약간 완화하는 쪽이 좋다.

- `MT4_REACH_MOVING_PREGRASP_STEP_RADIUS=0.045`
- `MT4_REACH_MOVING_PREGRASP_HOLD_STEPS=2`
- `MT4_REACH_MOVING_PREGRASP_REWARD_WEIGHT=20-24`
- 현재 shell/exponential reward는 유지
- 300 iteration으로 다시 짧게 비교

이 조건에서 `moving_pregrasp_final_rate`가 먼저 0.1 이상 올라가면, 그 다음 `0.035m/4 frames`로 다시 조이는 방식이 적절하다.
