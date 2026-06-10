# Learning Journal / 학습 기록

`learning_journal/` is the student-facing folder for plans, decisions, results, and videos that came out of the Robotarm learning sessions. / `learning_journal/`는 Robotarm 학습 대화에서 나온 계획, 결정, 결과, 영상을 학생들이 바로 확인할 수 있게 모아 둔 폴더입니다.

## Start Here / 먼저 볼 순서

1. Read this file. / 이 파일을 먼저 봅니다.
2. Open the active learning thread folder. / 현재 진행 중인 학습 흐름 폴더를 엽니다.
3. Compare the plan, run result, plots, and video together. / 계획, 실행 결과, 그래프, 영상을 같이 비교합니다.

Current active thread / 현재 활성 흐름:

- [2026-06-10 Three-Camera Coordinate Baseline](2026-06-10_three_camera_coordinate_baseline/README.md)

## Folder Rule / 폴더 규칙

- `YYYY-MM-DD_short_topic/`: one learning thread from discussion to result. / 대화에서 결과까지 이어지는 하나의 학습 흐름입니다.
- `videos/`: stable video artifacts with regular filenames. / 규칙적인 파일명으로 보존하는 영상 자료입니다.
- `RECORD_FORMAT.md`: the rule for new records, videos, and commit-time checks. / 새 기록, 영상, 커밋 전 확인 규칙입니다.

Older `notes/`, `experiments/`, and `logs/plots/` remain as source archives. / 기존 `notes/`, `experiments/`, `logs/plots/`는 원자료 archive로 유지합니다.

## Naming Rule / 파일명 규칙

Use this format for new student-facing files. / 학생용으로 공유할 새 파일은 아래 형식을 사용합니다.

```text
YYYYMMDD_HHMMSS_kind_topic_detail.ext
```

Examples / 예시:

- `20260610_095546_run_camera_only_region_matching_1500iter.md`
- `20260610_114129_plan_success10_video1min_demo_check.md`
- `20260610_120000_demo_three_camera_random_regions_1min.mp4`
- `20260610_120000_demo_three_camera_random_regions_1min_sequence.csv`

`kind` should be one of `plan`, `run`, `demo`, `train`, `review`, or `index`. / `kind`는 `plan`, `run`, `demo`, `train`, `review`, `index` 중 하나를 기본으로 사용합니다.

## Video Index / 영상 인덱스

New videos should be about 1 minute. Older `2min` videos stay here only as archive evidence. / 새 영상은 약 1분으로 만듭니다. 예전 `2min` 영상은 근거 archive로만 유지합니다.

| file | purpose / 목적 | related record / 연결 기록 |
| --- | --- | --- |
| [20260512_153939_demo_folded_topdown_seed42_model999.mp4](videos/20260512_153939_demo_folded_topdown_seed42_model999.mp4) | early folded top-down baseline demo / 초기 folded top-down 기준 시연 | [folded_topdown_seed42_128env_1000iter.md](../experiments/folded_topdown_seed42_128env_1000iter.md) |
| [20260515_124112_train_stage4_center_low_exploration.mp4](videos/20260515_124112_train_stage4_center_low_exploration.mp4) | stage 4 center visual low-exploration check / Stage 4 center 저탐색 확인 | [mt4_reach_decision_log.md](../notes/mt4_reach_decision_log.md) |
| [20260515_142816_demo_best_checkpoint_random_targets_10episodes.mp4](videos/20260515_142816_demo_best_checkpoint_random_targets_10episodes.mp4) | best-checkpoint random target demo / best checkpoint 랜덤 타겟 시연 | [20260515_142816_best_checkpoint_demo_email.md](../notes/20260515_142816_best_checkpoint_demo_email.md) |
| [20260515_142816_demo_best_checkpoint_random_targets_10episodes_zoom.mp4](videos/20260515_142816_demo_best_checkpoint_random_targets_10episodes_zoom.mp4) | zoomed best-checkpoint demo / 확대 시연 | [20260515_142816_best_checkpoint_demo_email.md](../notes/20260515_142816_best_checkpoint_demo_email.md) |
| [20260610_032809_train_coordinate_region_mastery_stage1_1500iter.mp4](videos/20260610_032809_train_coordinate_region_mastery_stage1_1500iter.mp4) | 9-region Stage 1 training video / 9영역 Stage 1 학습 영상 | [20260610_031348_coordinate_region_mastery_1500_video.md](../experiments/20260610_031348_coordinate_region_mastery_1500_video.md) |
| [20260610_034439_train_coordinate_near_center_shaping_stage1_1500iter_step36000.mp4](videos/20260610_034439_train_coordinate_near_center_shaping_stage1_1500iter_step36000.mp4) | near-center shaping rerun video / 중심 접근 shaping 재학습 영상 | [20260610_034439_coordinate_near_center_shaping_1500.md](../experiments/20260610_034439_coordinate_near_center_shaping_1500.md) |
| [20260610_074432_train_coordinate_progress_2min.mp4](videos/20260610_074432_train_coordinate_progress_2min.mp4) | short coordinate training progress clip / 좌표 학습 진행 2분 클립 | [2026-06-10 thread](2026-06-10_camera_only_region_matching/README.md) |
| [20260610_074525_demo_9region_random_policy_2min_labeled.mp4](videos/20260610_074525_demo_9region_random_policy_2min_labeled.mp4) | labeled 9-region random policy demo / 라벨 포함 9영역 랜덤 정책 시연 | [2026-06-10 thread](2026-06-10_camera_only_region_matching/README.md) |
| [20260610_073944_demo_9region_random_policy_2min_sequence.csv](videos/20260610_073944_demo_9region_random_policy_2min_sequence.csv) | region order used in the random demo / 랜덤 시연의 영역 순서 | [2026-06-10 thread](2026-06-10_camera_only_region_matching/README.md) |
| [20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4](videos/20260610_113358_train_three_camera_coordinate_baseline_stage1_1500iter_step36000.mp4) | three-camera Stage 1 baseline training clip / 3카메라 Stage 1 기준선 학습 클립 | [2026-06-10 three-camera thread](2026-06-10_three_camera_coordinate_baseline/README.md) |
| [20260610_114650_demo_three_camera_random_regions_1min.mp4](videos/20260610_114650_demo_three_camera_random_regions_1min.mp4) | 1-minute random-region demo / 1분 랜덤 영역 데모 | [success10/video1min plan](2026-06-10_three_camera_coordinate_baseline/20260610_114129_plan_success10_video1min_demo_check.md) |
| [20260610_114650_demo_three_camera_random_regions_1min_sequence.csv](videos/20260610_114650_demo_three_camera_random_regions_1min_sequence.csv) | region order for the 1-minute demo / 1분 데모 영역 순서 | [success10/video1min plan](2026-06-10_three_camera_coordinate_baseline/20260610_114129_plan_success10_video1min_demo_check.md) |
| [20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4](videos/20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4) | 1cm target-tracking rerun training clip / 1cm 목표 추적 재학습 영상 | [1cm target-tracking run](2026-06-10_three_camera_coordinate_baseline/20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md) |
| [20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4](videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4) | 1cm target-tracking random demo / 1cm 목표 추적 랜덤 데모 | [1cm target-tracking run](2026-06-10_three_camera_coordinate_baseline/20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md) |
| [20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv](videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv) | region order for the 1cm target-tracking demo / 1cm 목표 추적 데모 영역 순서 | [1cm target-tracking run](2026-06-10_three_camera_coordinate_baseline/20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md) |

## What Students Should Check / 학생 확인 포인트

- Does the plan explain what changed and why? / 계획이 무엇을 왜 바꿨는지 설명하는가?
- Does the run record show the command, checkpoint, metrics, and interpretation? / 실행 기록에 명령, 체크포인트, 지표, 해석이 있는가?
- Does the video demonstrate the same behavior that the record claims? / 영상이 기록에서 말한 행동을 실제로 보여주는가?
- Are perception errors and control errors separated? / 인식 오차와 제어 오차가 분리되어 있는가?
- For new coordinate runs, did each region pass 10 strict successes? / 새 좌표 학습에서 각 영역이 엄격 성공 10회를 채웠는가?
- For random demos, does the `_sequence.csv` show changing region numbers? / 랜덤 데모에서 `_sequence.csv`의 영역 번호가 바뀌는가?
