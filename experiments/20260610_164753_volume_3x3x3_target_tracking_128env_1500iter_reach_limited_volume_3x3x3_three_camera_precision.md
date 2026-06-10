# 2026-06-10_16-47-53_volume_3x3x3_target_tracking_128env_1500iter 좌표 영역 마스터리 확장 학습 / Coordinate Region Mastery Extended Run

## 목표 / Goal

Stage 1 학습을 새 1cm 엄격 성공 조건으로 다시 실행한다. / Rerun Stage 1 with the new strict 1 cm success rule:

- 목표와 같은 스테레오 카메라 영역에 진입 / same stereo camera region as the target
- 그리퍼 중심이 영역 중심 목표에서 `0.010 m` 이내 / gripper center within `0.010 m` of the region center target
- 목표를 지나친 뒤 돌아오는 움직임은 벌점으로 줄인다. / Penalize motion that passes beyond the target and comes back.
- 가능하면 로봇 쪽이나 위쪽에서 목표로 접근한다. / Prefer approaching the target from the robot side or from above.
- 목표와 그리퍼가 양쪽 가상 카메라에서 보임 / target and gripper visible from both virtual cameras

## 실행 / Run

- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_16-47-53_volume_3x3x3_target_tracking_128env_1500iter`
- Training command: `scripts/train_coordinate_stage1_volume_128_1500_video.sh`
- Training time: not recorded
- Final checkpoint: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_16-47-53_volume_3x3x3_target_tracking_128env_1500iter/model_1499.pt`
- Video: not copied yet
- Previous baseline: 2026-06-10 500-iteration Stage 1 result

## 최종 지표 / Final Metrics

| metric | value |
| --- | ---: |
| mean_reward | 36573.9023 |
| success_rate | 0.0000 |
| center_1cm_rate | 0.0000 |
| fine_center_4cm_rate | 0.9141 |
| near_center_7cm_rate | 0.9250 |
| strict_region_center_success_rate | 0.0000 |
| mean_distance | 0.0283 m (2.83 cm) |
| camera_region_entry_rate | 0.9287 |
| camera_region_match_rate | 1.0000 |
| target_estimate_error | 0.0000 m |
| target_overshoot | 0.0008 m |
| preferred_approach_error | 0.0252 m |
| gripper_camera_direction_error | 0.0442 |
| inside_workspace_rate | 0.9082 |
| target_stereo_visible_rate | 1.0000 |
| target_gripper_camera_visible_rate | 0.9470 |
| target_three_camera_visible_rate | 0.9470 |
| three_camera_ready_rate | 0.9470 |
| gripper_stereo_visible_rate | 0.9634 |
| active_region_number | 27 |
| mastered_region_count | 27 |

## 기준선 비교 / Baseline Comparison

| run | iterations | mastered regions | active region | mean distance | note |
| --- | ---: | ---: | ---: | ---: | --- |
| previous baseline | 500 | 2 | 3 | 0.0821 m | 3번 영역 마스터 전 정지 / stopped before region 3 mastery |
| previous extended baseline | 1500 | 7 | 8 | 0.0534 m | 8번 영역에서 정지 / stopped at region 8 |
| previous three-camera baseline | 1500 | 9 | 9 | 0.0545 m | 5회 성공 기준 / 5-success gate |
| this run | 1500 | 27 | 27 | 0.0283 m | 카메라 추정 목표 추적 보강 / camera-estimated target tracking update |

## 영역 마스터리 스냅샷 / Region Mastery Snapshot

| Region | Success Count | Best Episode Reward | Mastered | Active |
| --- | ---: | ---: | ---: | ---: |
| 1 | 13 | 25927.035156 | 1 | 0 |
| 2 | 53 | 9951.735352 | 1 | 0 |
| 3 | 19 | 2316.832031 | 1 | 0 |
| 4 | 21 | 25956.035156 | 1 | 0 |
| 5 | 49 | 19894.304688 | 1 | 0 |
| 6 | 34 | 27959.164062 | 1 | 0 |
| 7 | 13 | 3430.478271 | 1 | 0 |
| 8 | 39 | 20192.296875 | 1 | 0 |
| 9 | 18 | 27026.431641 | 1 | 0 |
| 10 | 19 | 28370.416016 | 1 | 0 |
| 11 | 38 | 31916.984375 | 1 | 0 |
| 12 | 38 | 24086.472656 | 1 | 0 |
| 13 | 24 | 29780.833984 | 1 | 0 |
| 14 | 40 | 30620.716797 | 1 | 0 |
| 15 | 49 | 24629.744141 | 1 | 0 |
| 16 | 21 | 32080.429688 | 1 | 0 |
| 17 | 24 | 33478.832031 | 1 | 0 |
| 18 | 28 | 34410.285156 | 1 | 0 |
| 19 | 28 | 29284.208984 | 1 | 0 |
| 20 | 28 | 28603.382812 | 1 | 0 |
| 21 | 15 | 29637.500000 | 1 | 0 |
| 22 | 28 | 31759.232422 | 1 | 0 |
| 23 | 28 | 32148.740234 | 1 | 0 |
| 24 | 25 | 34700.355469 | 1 | 0 |
| 25 | 20 | 33084.878906 | 1 | 0 |
| 26 | 22 | 35369.117188 | 1 | 0 |
| 27 | 1150 | 41094.941406 | 1 | 1 |

## 그래프 / Plots

### reward

![reward](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_reward.png)

### success

![success](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_success.png)

### region_progress

![region_progress](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_region_progress.png)

### distance

![distance](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_distance.png)

### camera

![camera](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_camera.png)

### visibility

![visibility](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_visibility.png)

### per_region

![per_region](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_per_region.png)

### region_mastery_counts

![region_mastery_counts](../logs/plots/20260610_164753_volume_3x3x3_target_tracking_128env_1500iter_reach_limited_volume_3x3x3_three_camera_precision/mt4_coordinate_region_mastery_counts.png)

## 학생 아이디어와 Codex 구현 / Student Idea vs. Codex Implementation

사용자 제안 / User proposal:

- 거리 기준은 `0.010 m`로 강화한다. / Tighten the distance criterion to `0.010 m`.
- 추적 보상은 실제 로봇팔 그리퍼와 목표 지점 사이의 거리에 집중한다. / Focus tracking reward on the actual gripper-to-target distance.
- 목표를 지나쳤다가 돌아오는 방식은 벌점으로 낮춘다. / Penalize overshooting the target and returning.
- 가능한 접근 방향은 로봇 쪽 또는 위쪽에서 목표로 들어오게 한다. / Prefer target approach from the robot side or from above.
- 성공을 하나의 전체 성공률이 아니라 번호가 붙은 영역 마스터리로 본다. / Treat success as numbered region mastery, not as one global success rate.
- 한 정책을 영역에서 영역으로 이어서 학습하고, 영역별 최고 행동 기록을 보존한다. / Continue one policy from region to region and preserve the best behavior record per region.
- 학생들이 실제 학습 장면과 결과를 볼 수 있도록 시각화한다. / Visualize the run so students can inspect what the agent actually learned.

Codex 구현 / Codex implementation:

- Stage 1 순차 좌표 영역 커리큘럼 학습을 실행했다. / Ran Stage 1 sequential coordinate-region curriculum training.
- 타겟 생성 좌표와 정책 입력 영역을 분리했다. / Separated target-generation coordinates from the policy-input region.
- 정책 입력의 영역 feature는 몸체 좌/우 스테레오 projection에서 추정한 영역으로 만들었다. / Built the policy-input region feature from the body left/right stereo projection.
- 몸체 좌/우 스테레오 projection으로 추정한 목표 상대좌표를 정책 입력에 추가했다. / Added the body-stereo-estimated target-relative position to the policy observation.
- 세 번째 그리퍼 카메라 projection을 관측과 보상 로그에 추가했다. / Added the third gripper-camera projection to observations and reward logs.
- 목표 중심으로 가도록 보상 신호를 더 직접적으로 넣었다. / Added a more direct reward signal for moving to the target center.
- 목표를 지나친 정도와 선호 접근 방향 오차를 로그로 남긴다. / Logged target overshoot and preferred approach error.
- 랜덤 데모에서 목표를 바꾼 뒤 정책 관측도 즉시 새로 읽도록 수정했다. / Fixed the random demo so observations refresh immediately after a target override.
- 엄격한 성공 조건을 3cm에서 1cm로 강화했다. / Tightened the strict success rule from 3 cm to 1 cm.
- Gym `RecordVideo`로 학습 영상을 기록했다. / Recorded training video through Gym `RecordVideo`.
- 좌표 전용 TensorBoard 그래프, 최종 지표 CSV, 체크포인트 CSV, 이 리포트를 생성했다. / Generated coordinate-specific TensorBoard plots, final metrics CSV, checkpoint CSV, and this report.

## 해석 / Interpretation

- 영역별 성공 횟수가 이 커리큘럼의 핵심 지표다. / Per-region success count is the key curriculum metric.
- 이번 학습의 핵심 확인점은 목표가 바뀔 때 그리퍼가 같은 위치만 반복하지 않고 새 목표 중심으로 움직이는지다. / The key check is whether the gripper follows the new target center instead of repeating one position.
- `camera_region_match_rate`는 생성된 정답 영역과 카메라 추정 영역의 일치 여부를 보여준다. / `camera_region_match_rate` shows whether the generated true region matches the camera-estimated region.
- `target_estimate_error`는 카메라로 추정한 목표 위치가 실제 목표와 얼마나 가까운지 보여준다. / `target_estimate_error` shows how close the camera-estimated target point is to the true target.
- 최종 `success_rate`는 마지막 로깅 배치 기준이라 영역별 누적 성공을 과소평가할 수 있다. / The final `success_rate` is batch-local and can understate cumulative per-region progress.
- 거리 기준은 완화하지 않았다. 마스터된 모든 영역은 같은 1cm 엄격 조건으로 집계된다. / The distance criterion was not relaxed. Every mastered region is counted with the same 1 cm strict success rule.
- 이번 수정의 목적은 실제 시연 접근 선택을 생성 좌표가 아니라 카메라 추정 영역에 의존하게 만드는 것이다. / This update makes demo approach selection depend on the camera-estimated region instead of generated coordinates.

Generated at `2026-06-10T17:16:26`.
