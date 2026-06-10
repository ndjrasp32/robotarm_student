# 2026-06-10 3x3x3 Volume Failure and Reach Audit / 3x3x3 실패 기록과 가동범위 확인

## Run / 실행

- KR: 27영역 첫 실행은 정상 종료됐지만 영역 마스터리는 전혀 진행되지 않았다.
- EN: The first 27-cell run finished normally, but region mastery did not progress.

| item | value |
| --- | --- |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_14-37-19_volume_3x3x3_target_tracking_128env_1500iter` |
| command | `scripts/train_coordinate_stage1_volume_128_1500_video.sh` |
| iterations | 1500 |
| final checkpoint | `model_1499.pt` |

## Final Metrics / 마지막 수치

| metric | value |
| --- | ---: |
| `Train/mean_reward` | 1603.8280 |
| `success_rate` | 0.0000 |
| `mean_distance` | 0.2881 m |
| `camera_region_entry_rate` | 0.0000 |
| `camera_region_match_rate` | 1.0000 |
| `inside_workspace_rate` | 0.0000 |
| `target_stereo_visible_rate` | 1.0000 |
| `target_three_camera_visible_rate` | 0.0000 |
| `gripper_stereo_visible_rate` | 0.0000 |
| `center_1cm_rate` | 0.0000 |
| `near_center_7cm_rate` | 0.0000 |
| `strict_region_center_success_rate` | 0.0000 |
| `active_region_number` | 1 |
| `mastered_region_count` | 0 |

## Interpretation / 해석

- KR: 실패 원인은 단순히 27개 영역이 많아서라기보다, 첫 3D 셀부터 gripper가 작업 박스 안으로 들어오지 못한 것이다.
- EN: The failure is not only that 27 cells are more numerous; the gripper never entered the workspace from the first 3D cell.

- KR: 목표 자체는 좌/우 고정 카메라에 보였다. 하지만 gripper가 양안 카메라에 잡히지 않았고, 작업공간 안에 들어온 비율도 0이었다.
- EN: The target stayed visible to the fixed stereo cameras, but the gripper was not stereo-visible and never entered the workspace.

- KR: home 자세의 gripper 중심은 `(0.1876, 0.0000, 0.5192)`였고, 기존 첫 영역 목표는 약 `(0.2076, -0.0783, 0.0875)`였다. 시작 거리 약 `0.439 m`로, 낮은 코너 목표부터 시작한 것이 1cm strict gate에는 너무 공격적이었다.
- EN: The home gripper center was `(0.1876, 0.0000, 0.5192)`, while the previous first target was about `(0.2076, -0.0783, 0.0875)`. The start distance was about `0.439 m`, too aggressive for a strict 1 cm gate from a low corner.

## Reach Audit / 가동범위 확인

- KR: 현재 MT4 모델의 조인트 제한에서 gripper 중심을 랜덤 샘플링했다. 전체 샘플의 대략적인 범위는 `x=-0.309..0.531`, `y=-0.528..0.534`, `z=-0.192..0.624`였지만, 학습에 쓸 박스는 이 전체 외피가 아니라 안정적으로 접근 가능한 전방 부분만 써야 한다.
- EN: Random gripper-center samples under the current MT4 joint limits covered roughly `x=-0.309..0.531`, `y=-0.528..0.534`, `z=-0.192..0.624`. The training workspace should use a stable front subset, not the full envelope.

- KR: 새 27영역 박스는 center `(0.30, 0.00, 0.21)`, size `(0.12, 0.16, 0.12)`로 잡는다. 범위는 `x=0.24..0.36`, `y=-0.08..0.08`, `z=0.15..0.27`이다.
- EN: The revised 27-cell box uses center `(0.30, 0.00, 0.21)` and size `(0.12, 0.16, 0.12)`, i.e. `x=0.24..0.36`, `y=-0.08..0.08`, `z=0.15..0.27`.

- KR: 이 후보 박스의 27개 중심은 조인트 샘플 분포에서 최근접 거리 `0.005..0.041 m` 안에 들어왔다. 기존 박스의 최대 최근접 거리는 약 `0.075 m`였으므로, 새 박스가 1cm 정밀 학습 전에 더 보수적이다.
- EN: The 27 centers in this candidate box had nearest sampled gripper distances of `0.005..0.041 m`. The previous box reached about `0.075 m`, so the revised box is more conservative before strict 1 cm training.

## Decision / 결정

- KR: 이 실패는 그대로 보존한다. 실제 Mirobot으로 옮길 때도 먼저 조인트 제한과 안정 작업영역을 계산한 뒤, 그 안에서 영역 학습을 시작해야 한다는 좋은 교육 사례다.
- EN: Keep this failure record. For a later real Mirobot transfer, this is a useful teaching case: compute joint limits and a stable workspace before region training.

- KR: 다음 학습은 reach-limited 27영역 박스로 다시 실행한다.
- EN: The next run uses the reach-limited 27-cell workspace.
