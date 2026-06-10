# 2026-06-10 Reach-Limited 3x3x3 Region 19 Failure / 가동범위 제한 3x3x3 19번 영역 실패

## Summary / 요약

- KR: 첫 보수 27영역은 이전 wide 실패보다 훨씬 좋아져 18개 영역을 통과했지만, 높은 층의 가까운 코너인 19번 영역에서 멈췄다.
- EN: The first conservative 27-cell workspace improved greatly over the wide failure and mastered 18 cells, but stopped at region 19, the near high corner.

## Run / 실행

| item | value |
| --- | --- |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_16-33-17_volume_3x3x3_target_tracking_128env_1500iter` |
| command | `scripts/train_coordinate_stage1_volume_128_1500_video.sh` |
| stopped at | iteration `631/1500` |
| reason | no precision progress at active region 19 |

## Result / 결과

| metric | value |
| --- | ---: |
| `active_region_number` | 19 |
| `mastered_region_count` | 18 |
| `region_19_success_count` | 0 |
| `success_rate` | 0.0000 |
| `center_1cm_rate` | 0.0000 |
| `fine_center_4cm_rate` | 0.0000 |
| `near_center_7cm_rate` | 0.0000 |
| `mean_distance` | 0.0891 m |
| `inside_workspace_rate` | 0.8994 |
| `target_three_camera_visible_rate` | 0.9060 |
| `mean_gripper_camera_direction_error` | 0.1139 |

## Interpretation / 해석

- KR: 실패 원인은 카메라 인식이 아니라 작업공간 경계다. 19번 중심은 `(0.260, -0.053, 0.250)`이고, 로그에서 `x_min`과 `z_max` 경계 샘플이 계속 잡혔다.
- EN: This was not a perception failure. Region 19 centered at `(0.260, -0.053, 0.250)`, and the logs repeatedly hit the `x_min` and `z_max` workspace boundaries.

- KR: 목표는 세 카메라에 대체로 보였고 gripper-camera 방향 오차도 작아졌지만, 평균 거리가 8-9 cm 근처에 머물러 7 cm 근접권이나 4 cm 정밀권으로 들어가지 못했다.
- EN: The target was mostly visible to all three cameras and gripper-camera direction improved, but mean distance stayed around 8-9 cm and never entered the 7 cm near band or 4 cm fine band.

- KR: 따라서 27개라는 개수보다, 가까운 쪽 높은 코너가 현재 MT4 모델의 안정 학습 영역 밖에 있다고 보는 것이 맞다.
- EN: The issue is less the count of 27 cells and more that the near high corner is outside the stable learnable region for the current MT4 model.

## Decision / 결정

- KR: 이 실패는 좋은 실패 기록으로 보존한다. 다음 27영역은 같은 3카메라/1cm 성공 조건을 유지하되, 박스를 `center=(0.305, 0.00, 0.205)`, `size=(0.09, 0.14, 0.09)`로 줄인다.
- EN: Keep this as a useful failure record. The next 27-cell run keeps the same three-camera and 1 cm success criteria, but shrinks the box to `center=(0.305, 0.00, 0.205)`, `size=(0.09, 0.14, 0.09)`.

- KR: 새 19번 중심은 약 `(0.275, -0.047, 0.235)`가 되어, 실패 지점보다 로봇에서 약간 멀고 낮은 곳으로 이동한다.
- EN: The new region 19 center is about `(0.275, -0.047, 0.235)`, slightly farther from the robot and lower than the failed point.

## Next Step / 다음 단계

- KR: 보수 박스로 다시 학습하고, `mastered_region_count`, `fine_center_4cm_rate`, `target_three_camera_visible_rate`, `mean_gripper_camera_direction_error`를 계속 추적한다.
- EN: Rerun training with the smaller box and keep tracking `mastered_region_count`, `fine_center_4cm_rate`, `target_three_camera_visible_rate`, and `mean_gripper_camera_direction_error`.
