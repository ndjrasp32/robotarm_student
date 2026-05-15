# 20260515_130324 stage4_strong_push_replay_128env_300iter

## Summary

- timestamp: 2026-05-15T13:05:54
- checkpoint: `model_1249.pt`
- checkpoint path: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_simplified_reach_direct/2026-05-15_13-03-24/model_1249.pt`
- plot snapshot: `/home/spark-robotics/work/robotarm/mt4_isaac_lab_task/logs/plots/20260515_130324_stage4_strong_push_replay_128env_300iter`
- reward profile: `stage4_strong_push`
- notes: Stronger Stage4 push curriculum: reward new best center-push progress and deeper push after progress 0.5. Improved push progress and produced sparse final center success, but final success remains low.

## Metrics

| metric | value |
|---|---:|
| success_rate | 0.000244140625 |
| stage1_alignment_ready_rate | 0.978271484375 |
| pregrasp_entry_success_rate | 0.903564453125 |
| pregrasp_entry_ready_rate | 0.066650390625 |
| pregrasp_entry_reached_rate | 0.744140625 |
| pregrasp_success_rate | 0.9755859375 |
| pregrasp_hold_ready_rate | 0.713623046875 |
| pregrasp_held_rate | 0.744140625 |
| stage2_pregrasp_ready_rate | 0.744140625 |
| stage2_alignment_ready_rate | 0.978271484375 |
| stage3_insertion_ready_rate | 0.744140625 |
| stage3_touch_ready_rate | 0.743896484375 |
| stage4_center_ready_rate | 0.000244140625 |
| stage4_push_ready_rate | 0.264892578125 |
| mean_pregrasp_entry_distance | 0.10580159723758698 |
| mean_pregrasp_distance | 0.07829289138317108 |
| mean_gripper_center_pregrasp_distance | 0.07829289138317108 |
| mean_touch_error | 0.026145214214920998 |
| mean_distance | 0.056145213544368744 |
| mean_insertion_alignment | 0.8916689157485962 |
| mean_target_contact_penalty | 0.0 |
| mean_pregrasp_center_progress | 0.9784697890281677 |
| mean_center_push_progress | 0.6130448579788208 |
| mean_best_center_push_progress | 0.6594560146331787 |
| mean_center_push_improvement | 0.0006966536166146398 |
| mean_best_target_center_distance | 0.2898886799812317 |
| mean_target_center_improvement | 6.049043804523535e-05 |
| mean_pregrasp_line_error | 1.3503495210898109e-08 |

## Interpretation

- 선생님 의견:
  - 마지막 중심 근처까지 왔으면 빨간 구체 쪽으로 더 확실히 밀어 넣어야 한다.
  - 1차 목표는 전체 task 완성보다 마지막 단계의 가능성을 여는 것이다.
- Codex 적용:
  - `center_push_improvement`를 추가해, episode 중 이전보다 더 안쪽으로 들어간 경우에만 추가 보상을 주었다.
  - `center_push_progress > 0.5` 이후 구간을 더 강하게 보상하는 depth reward를 추가했다.
  - replay reset 직후에는 현재 push progress를 기준점으로 저장해, 시작 상태 자체가 아니라 그보다 더 들어간 경우만 improvement로 보았다.
- 결과 평가:
  - 이전 center-push 실험의 `mean_center_push_progress=0.5227710008621216`보다 이번 `mean_center_push_progress=0.6130448579788208`가 높다.
  - `mean_best_center_push_progress=0.6594560146331787`로 episode 중 더 깊게 들어간 기록도 확인되었다.
  - `stage4_push_ready_rate=0.264892578125`는 이전보다 낮지만, 기준을 0.65로 높였기 때문에 더 엄격한 지표다.
  - `stage4_center_ready_rate=0.000244140625`, `success_rate=0.000244140625`로 최종 성공 샘플이 아주 드물게 발생했다.
  - `mean_target_contact_penalty=0.0`이므로 빨간 구체와의 위험한 몸체 충돌은 발생하지 않았다.
- 다음 제안:
  - push는 강화되었으므로 다음은 push 중 lateral error와 center distance를 동시에 유지하는 방향이 좋다.
  - center success 근처 replay state를 더 많이 모으거나, `final_center_success_radius`를 잠깐 완화했다가 다시 줄이는 curriculum을 적용한다.
