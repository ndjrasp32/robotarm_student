# 2026-06-10_03-44-39 좌표 영역 마스터리 확장 학습 / Coordinate Region Mastery Extended Run

## 목표 / Goal

Stage 1 학습을 다시 실행하되 엄격한 성공 조건은 동일하게 유지한다. / Rerun Stage 1 while keeping the same strict success rule:

- 목표와 같은 스테레오 카메라 영역에 진입 / same stereo camera region as the target
- 그리퍼 중심이 영역 중심 목표에서 `0.030 m` 이내 / gripper center within `0.030 m` of the region center target
- 목표와 그리퍼가 양쪽 가상 카메라에서 보임 / target and gripper visible from both virtual cameras

## 실행 / Run

- Run directory: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_03-44-39`
- Training command: `TERM=xterm-256color MT4_MAX_ITERATIONS=1500 MT4_RECORD_VIDEO=1 MT4_VIDEO_LENGTH=240 MT4_VIDEO_INTERVAL=12000 scripts/train_coordinate_stage1_plane_128_1500_video.sh`
- Training time: 861.01 seconds (14m 21.01s)
- Final checkpoint: `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_03-44-39/model_1499.pt`
- Video: `learning_journal/videos/20260610_034439_train_coordinate_near_center_shaping_stage1_1500iter_step36000.mp4`
- Previous baseline: `experiments/20260610_031348_coordinate_region_mastery_1500_video.md`

## 최종 지표 / Final Metrics

| metric | value |
| --- | ---: |
| mean_reward | 6028.4316 |
| success_rate | 0.0005 |
| center_3cm_rate | 0.0005 |
| near_center_7cm_rate | 0.8667 |
| strict_region_center_success_rate | 0.0005 |
| mean_distance | 0.0555 m (5.55 cm) |
| camera_region_entry_rate | 0.9446 |
| inside_workspace_rate | 0.8840 |
| gripper_stereo_visible_rate | 0.9651 |
| active_region_number | 9 |
| mastered_region_count | 9 |

## 기준선 비교 / Baseline Comparison

| run | iterations | mastered regions | active region | mean distance | note |
| --- | ---: | ---: | ---: | ---: | --- |
| previous baseline | 500 | 2 | 3 | 0.0821 m | 3번 영역 마스터 전 정지 / stopped before region 3 mastery |
| previous extended baseline | 1500 | 7 | 8 | 0.0534 m | 8번 영역에서 정지 / stopped at region 8 |
| this run | 1500 | 9 | 9 | 0.0555 m | 제안사항 반영 재학습 / rerun with proposal updates |

## 영역 마스터리 스냅샷 / Region Mastery Snapshot

| Region | Success Count | Best Episode Reward | Mastered | Active |
| --- | ---: | ---: | ---: | ---: |
| 1 | 18 | 3148.148438 | 1 | 0 |
| 2 | 40 | 3383.852539 | 1 | 0 |
| 3 | 8 | 3391.473877 | 1 | 0 |
| 4 | 6 | 3186.023926 | 1 | 0 |
| 5 | 33 | 3468.383545 | 1 | 0 |
| 6 | 40 | 1715.004761 | 1 | 0 |
| 7 | 6 | 4906.007324 | 1 | 0 |
| 8 | 10 | 4809.619141 | 1 | 0 |
| 9 | 830 | 6729.692383 | 1 | 1 |

## 그래프 / Plots

### reward

![reward](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_reward.png)

### success

![success](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_success.png)

### region_progress

![region_progress](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_region_progress.png)

### distance

![distance](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_distance.png)

### camera

![camera](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_camera.png)

### visibility

![visibility](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_visibility.png)

### per_region

![per_region](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_per_region.png)

### region_mastery_counts

![region_mastery_counts](../logs/plots/20260610_034439_coordinate_near_center_shaping_1500/mt4_coordinate_region_mastery_counts.png)

## 학생 아이디어와 Codex 구현 / Student Idea vs. Codex Implementation

사용자 제안 / User proposal:

- 거리 기준은 `0.030 m`로 고정한다. / Keep the distance criterion fixed at `0.030 m`.
- 성공을 하나의 전체 성공률이 아니라 번호가 붙은 영역 마스터리로 본다. / Treat success as numbered region mastery, not as one global success rate.
- 한 정책을 영역에서 영역으로 이어서 학습하고, 영역별 최고 행동 기록을 보존한다. / Continue one policy from region to region and preserve the best behavior record per region.
- 학생들이 실제 학습 장면과 결과를 볼 수 있도록 시각화한다. / Visualize the run so students can inspect what the agent actually learned.

Codex 구현 / Codex implementation:

- Stage 1 순차 9영역 학습을 실행했다. / Ran Stage 1 sequential 9-region training.
- 엄격한 3cm 성공 조건은 바꾸지 않았다. / Kept the strict 3 cm success rule unchanged.
- 7cm 이내 중심 접근 보상을 추가해 3cm 성공까지의 조밀 신호를 강화했다. / Added near-center shaping inside 7 cm to strengthen the dense signal toward 3 cm success.
- Gym `RecordVideo`로 학습 영상을 기록했다. / Recorded training video through Gym `RecordVideo`.
- 좌표 전용 TensorBoard 그래프, 최종 지표 CSV, 체크포인트 CSV, 이 리포트를 생성했다. / Generated coordinate-specific TensorBoard plots, final metrics CSV, checkpoint CSV, and this report.

## 해석 / Interpretation

- 영역별 성공 횟수가 이 커리큘럼의 핵심 지표다. / Per-region success count is the key curriculum metric.
- 이전 1500회 학습은 7개 영역에서 멈췄지만, 이번 학습은 9개 영역을 모두 마스터했다. / The previous 1500-iteration run stopped at 7 mastered regions, while this run mastered all 9 regions.
- 7cm 중심 접근 보상은 8번 병목을 넘기는 데 효과가 있었다. / The 7 cm near-center shaping was effective for passing the region 8 bottleneck.
- 최종 `success_rate`는 마지막 로깅 배치 기준이라 영역별 누적 성공을 과소평가할 수 있다. / The final `success_rate` is batch-local and can understate cumulative per-region progress.
- 거리 기준은 완화하지 않았다. 마스터된 모든 영역은 같은 3cm 엄격 조건으로 집계된다. / The distance criterion was not relaxed. Every mastered region is counted with the same 3 cm strict success rule.
- 이번 수정의 목적은 7cm 안쪽에서 중심으로 더 안정적으로 수렴하게 하는 것이다. / This update aims to make convergence toward the center more stable inside 7 cm.

Generated at `2026-06-10T03:59:55`.
