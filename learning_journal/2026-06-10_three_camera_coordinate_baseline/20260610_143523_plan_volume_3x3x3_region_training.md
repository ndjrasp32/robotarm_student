# 2026-06-10 3x3x3 Volume Region Training Plan / 3x3x3 영역 인식 학습 계획

## Question / 질문

- KR: 3x3 평면 9영역 대신 깊이까지 포함한 3x3x3 27영역을 카메라 기반으로 인식하고 추적하면, 새 목표를 더 잘 따라갈 수 있는가?
- EN: If the target space is split into 3x3x3 volume cells instead of a 3x3 plane, can the camera-conditioned policy follow new targets more reliably?

## Decision / 결정

- KR: 기존 9영역 태스크는 보존하고, 27영역 전용 `Isaac-MT4-Coordinate-Volume-Direct-v0` 태스크를 추가한다.
- EN: Keep the existing 9-region task and add a dedicated 27-cell task, `Isaac-MT4-Coordinate-Volume-Direct-v0`.

- KR: 첫 실패 이후, 27영역은 현재 모델의 샘플링된 gripper 가동범위 안쪽으로 보수적으로 좁힌다. 새 박스는 center `(0.30, 0.00, 0.21)`, size `(0.12, 0.16, 0.12)`이다.
- EN: After the first failure, constrain the 27-cell workspace to a conservative subset of the sampled gripper reach. The revised box is center `(0.30, 0.00, 0.21)`, size `(0.12, 0.16, 0.12)`.

- KR: 영역 마스터리는 1번부터 27번까지 순차 진행하며, 각 영역은 1cm 엄격 성공 10회가 필요하다.
- EN: Region mastery proceeds sequentially from region 1 to 27, requiring 10 strict 1 cm successes per region.

- KR: 보상은 그리퍼 중심과 실제 목표 사이 거리, 목표 지나침 벌점, 로봇 쪽 또는 위쪽 접근 선호를 유지한다.
- EN: Rewards keep the gripper-to-target distance term, target overshoot penalty, and robot-side or above approach preference.

## Changes / 수정 내용

- KR: `MT4CoordinateVolumeEnvCfg`를 추가해 `volume_region_shape=(3,3,3)`와 `front_face_region_targets=False`를 사용한다.
- EN: Added `MT4CoordinateVolumeEnvCfg` using `volume_region_shape=(3,3,3)` and `front_face_region_targets=False`.

- KR: `MT4CoordinateVolumeEnvCfg`의 workspace를 reach-limited box로 조정하고, body stereo camera의 `camera_look_at`도 같은 중심으로 맞춘다.
- EN: Adjusted the `MT4CoordinateVolumeEnvCfg` workspace to the reach-limited box and aligned the body stereo camera `camera_look_at` to the same center.

- KR: 27영역에서도 순차 마스터리 로직이 작동하도록 `_uses_region_mastery()` 조건을 완화했다.
- EN: Relaxed `_uses_region_mastery()` so sequential mastery also works for 27 volume cells.

- KR: 볼륨 Stage 1 보상에 1cm 중심 보상, near-center 보상, overshoot 벌점, 접근 방향 선호를 적용했다.
- EN: Applied 1 cm center reward, near-center reward, overshoot penalty, and preferred approach reward to volume Stage 1.

- KR: 새 실행 스크립트 `scripts/train_coordinate_stage1_volume_128_1500_video.sh`를 추가했다.
- EN: Added the new run script `scripts/train_coordinate_stage1_volume_128_1500_video.sh`.

## Run / 실행

```bash
./scripts/train_coordinate_stage1_volume_128_1500_video.sh
```

## Expected Checks / 확인 기준

- KR: `mastered_region_count`가 27까지 증가하는지 확인한다.
- EN: Check whether `mastered_region_count` reaches 27.

- KR: `camera_region_match_rate`, `center_1cm_rate`, `mean_distance`, `mean_target_overshoot`를 함께 본다.
- EN: Review `camera_region_match_rate`, `center_1cm_rate`, `mean_distance`, and `mean_target_overshoot` together.
