# 2026-06-10 Three-Camera Coordinate Baseline Run / 3카메라 좌표 기준선 학습

## Summary / 요약

- KR: 몸체 좌/우 스테레오 카메라와 그리퍼 카메라 projection을 함께 쓰는 Stage 1 학습을 1500 iteration 실행했고, 9개 영역 모두 마스터했다.
- EN: Ran 1500 Stage 1 iterations using body left/right stereo plus a gripper-camera projection, and all 9 regions were mastered.

## Question / 질문

- KR: 세 번째 그리퍼 카메라를 추가해도 영역 마스터리가 유지되고, 타겟 가시성 지표가 개선되는가?
- EN: With the third gripper camera added, does region mastery hold and does target visibility improve?

## Decision / 결정

- KR: 이 run을 새 3카메라 좌표 기준선으로 기록한다. 단, 마지막 배치 strict 3cm 성공률은 낮으므로 정밀 중심 수렴은 다음 개선 대상으로 둔다.
- EN: Record this run as the new three-camera coordinate baseline. The final-batch strict 3 cm success rate remains low, so precise center convergence stays as the next improvement target.

- KR: 이 run은 당시 기준인 영역별 5회 성공으로 통과했다. 다음 run부터는 영역별 10회 성공으로 더 엄격하게 본다.
- EN: This run passed with the previous 5-success-per-region gate. From the next run, the gate is stricter at 10 successes per region.

## Implementation / 구현

- KR: 정책 관측을 47차원에서 51차원으로 확장했다.
- EN: Expanded the policy observation from 47 to 51 values.

- KR: 추가 관측은 그리퍼 카메라 기준 target `u`, `v`, `visible`, `depth` projection이다.
- EN: The added observation is target `u`, `v`, `visible`, and `depth` projection from the gripper camera.

- KR: `target_gripper_camera_visible_rate`, `target_three_camera_visible_rate`, `mean_gripper_camera_target_error`를 로그에 추가했다.
- EN: Added `target_gripper_camera_visible_rate`, `target_three_camera_visible_rate`, and `mean_gripper_camera_target_error` to logs.

## Result / 결과

| metric | value |
| --- | ---: |
| training time / 학습 시간 | 1097.05 s |
| final checkpoint / 최종 체크포인트 | `model_1499.pt` |
| mean_reward | 6194.7388 |
| mastered_region_count | 9 |
| active_region_number | 9 |
| camera_region_match_rate | 1.0000 |
| target_stereo_visible_rate | 1.0000 |
| target_gripper_camera_visible_rate | 0.9014 |
| target_three_camera_visible_rate | 0.9014 |
| gripper_stereo_visible_rate | 0.9575 |
| camera_region_entry_rate | 0.9397 |
| mean_distance | 0.0545 m |
| near_center_7cm_rate | 0.8811 |
| strict_region_center_success_rate | 0.0005 |

## Region Mastery / 영역 마스터리

| region | success count | mastered |
| --- | ---: | ---: |
| 1 | 11 | 1 |
| 2 | 33 | 1 |
| 3 | 9 | 1 |
| 4 | 9 | 1 |
| 5 | 15 | 1 |
| 6 | 11 | 1 |
| 7 | 13 | 1 |
| 8 | 37 | 1 |
| 9 | 1593 | 1 |

## Evidence / 근거 자료

- Record / 기록: [20260610_111518_three_camera_coordinate_baseline_128env_1500iter_three_camera_coordinate_baseline_1500.md](../../experiments/20260610_111518_three_camera_coordinate_baseline_128env_1500iter_three_camera_coordinate_baseline_1500.md)
- Metrics / 지표 CSV: [20260610_111518_index_three_camera_coordinate_final_metrics.csv](artifacts/20260610_111518_index_three_camera_coordinate_final_metrics.csv)
- Region mastery CSV / 영역 마스터리 CSV: [20260610_111518_index_three_camera_coordinate_region_mastery.csv](artifacts/20260610_111518_index_three_camera_coordinate_region_mastery.csv)
- Plot / 그래프: [region mastery graph](artifacts/20260610_111518_review_three_camera_region_mastery_counts.png), [camera graph](artifacts/20260610_111518_review_three_camera_visibility_and_alignment.png), [success graph](artifacts/20260610_111518_review_three_camera_success_curve.png)
- Plot archive / 그래프 archive: [20260610_111518_three_camera_coordinate_baseline_128env_1500iter_three_camera_coordinate_baseline_1500](../../logs/plots/20260610_111518_three_camera_coordinate_baseline_128env_1500iter_three_camera_coordinate_baseline_1500/)
- Video / 영상: [20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4](../videos/20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4)

## Interpretation / 해석

- KR: 세 번째 그리퍼 카메라의 target visible은 마지막 배치 기준 0.9014까지 올라갔다.
- EN: The third gripper camera reached a final-batch target visible rate of 0.9014.

- KR: 누적 영역 마스터리는 9/9로 성공했지만, 마지막 배치 strict 3cm 성공률은 0.0005라 “영역 선택”보다 “중심 정밀 수렴”이 다음 병목이다.
- EN: Cumulative region mastery succeeded at 9/9, but final-batch strict 3 cm success is 0.0005, so precise center convergence is the next bottleneck after region selection.

## Next Step / 다음 단계

- KR: 먼저 같은 세 카메라 구조에서 영역별 10회 성공 기준으로 다시 학습한다. 영상은 학습과 데모 모두 약 1분으로 남긴다.
- EN: First rerun the same three-camera setup with the 10-success-per-region gate. Keep both training and demo videos at about 1 minute.
