# 2026-06-10 좌표 영역 마스터리 계획 / Coordinate Region Mastery Plan

## 목적 / Purpose

이 노트는 다음 좌표 평면 학습 전에 학생용 설계 아이디어를 구분해서 정리한다. / This note separates the student-facing design ideas before the next coordinate-plane training run.

커리큘럼은 스테레오 카메라 기준 좌표계를 유지한다. 목표는 물체 조작으로 바로 넘어가는 것이 아니라, 먼저 로봇팔이 카메라가 정의한 전방 작업공간의 번호 영역을 배우게 하는 것이다. / The curriculum keeps the stereo camera-frame coordinate basis. The goal is not to jump directly to object manipulation, but to first make the arm learn the numbered front workspace regions defined by the cameras.

## 사용자 제안 / User Proposal

- 이후 접근 단계에 안정적인 카메라 좌표 기준이 필요하므로, 좌표 영역은 카메라 프레임으로 유지한다. / Keep coordinate regions in the camera frame because the later approach stage needs a stable camera-coordinate basis.
- 전체 27개 부피 셀보다 먼저 9개 전방 평면 영역을 학습한다. / Use 9 front-plane regions first instead of a full 27-cell volume.
- 성공률 하나로 평가하지 않고, “1번 영역 성공”처럼 번호별 성공으로 평가한다. / Evaluate success as “region N success” rather than one undifferentiated success rate.
- 목표 영역에 들어가고, 영역 중심점에서 약 3cm 이내까지 접근해야 성공으로 센다. / Count success only when the gripper enters the target region and approaches within about 3 cm of the region center.
- 각 영역을 독립 모델로 따로 학습하지 않는다. / Do not train each region as a separate independent model.
- 하나의 정책을 이어서 학습한다. 1번 영역이 충분히 성공하면 그 단계의 가장 좋은 행동 기록을 남기고, 보상 압력을 다음 영역으로 넘겨 2번 영역을 학습한다. / Continue training one policy. When region 1 succeeds enough times, preserve the best behavior record from that phase and shift reward pressure to region 2.
- 영역별 학습 값과 진도를 기록해 학생들이 커리큘럼 진행을 확인하게 한다. / Record learned values and progress per region so students can inspect how the curriculum advanced.

## Codex 제안 / Codex Proposal

- 첫 버전은 같은 RSL-RL 환경 안에서 순차 영역 마스터리로 구현한다. / Implement the first version as sequential region mastery inside the same RSL-RL environment.
- Stage 1에서는 모든 병렬 환경이 현재 활성 영역만 샘플링한다. / During Stage 1, all envs sample only the current active region.
- 성공 후에는 기존 home reset을 유지하고, 마스터 조건에 도달할 때까지 같은 영역을 다시 샘플링한다. / Keep the existing home reset after success and resample the same region until it reaches the mastery threshold.
- 활성 영역이 설정된 성공 횟수에 도달한 뒤에만 다음 영역으로 이동한다. / Advance to the next region only after the active region reaches the configured success count.
- 엄격한 Stage 1 성공 조건은 같은 카메라 셀, 중심 거리 `0.030 m` 미만, 목표와 그리퍼의 양안 가시성이다. / Strict Stage 1 success requires the same stereo camera cell, gripper-to-target distance below `0.030 m`, and visibility of both target and gripper in both cameras.
- 영역별 엄격 성공, 누적 성공 횟수, 최고 성공 에피소드 보상, 마스터 여부, 활성 영역 번호, 3cm 중심 접근률을 로그에 남긴다. / Log strict per-region success, cumulative success counts, best successful episode reward, mastered flag, active region number, and 3 cm center approach rate.
- 영역 성공이 기록될 때마다 학습 run 디렉터리에 `region_mastery.csv`를 쓴다. / Write `region_mastery.csv` into the training run directory whenever a region success is recorded.

## 구현 선택 / Implementation Choice

RSL-RL 학습 중간에 외부 오케스트레이션 없이 “최고 모델 하나만 남기고” 체크포인트를 실제로 가지치기하기는 어렵다. / The environment cannot literally prune and keep only one model checkpoint mid-run without adding an external orchestration loop around RSL-RL.

이번 구현에서는 이를 두 가지 실용적인 방식으로 표현한다. / In this pass, that idea is represented in two practical ways:

- 활성 영역이 넘어갈 때 같은 정책 가중치를 계속 이어서 학습한다. / RSL-RL continues from the same policy weights as the active region advances.
- 영역별 최고 성공 에피소드 보상을 기록해, 나중에 가장 깔끔한 전환 시점 주변 체크포인트를 고르거나 재개할 수 있게 한다. / The environment records the best successful episode reward per region so later runs can select or resume from checkpoints around the cleanest transitions.

이 방식은 학생 실습을 하나의 학습 명령으로 단순하게 유지하면서도, 번호 영역 마스터리로 커리큘럼이 진행된다는 핵심 아이디어를 보존한다. / This keeps the student workflow simple enough for one training command while preserving the key educational idea: the curriculum advances by numbered region mastery, not by random target mixing.

## 현재 파라미터 / Current Parameters

- Task: `Isaac-MT4-Coordinate-Plane-Direct-v0`
- Regions: 카메라 전방 평면 3x3 셀, 1-9번 / 3x3 front camera-plane cells, numbered 1-9
- Mastery threshold: 영역당 엄격 성공 5회 / 5 strict successes per region
- Center success radius: `0.030 m`
- Training command: `scripts/train_coordinate_stage1_plane_128_500.sh`

## 관찰할 지표 / What To Watch

- `coordinate_curriculum/plane_localization_active_region_number`
- `coordinate_curriculum/plane_localization_mastered_region_count`
- `coordinate_curriculum/plane_localization_center_3cm_rate`
- `coordinate_curriculum/plane_localization_near_center_7cm_rate`
- `coordinate_curriculum/plane_localization_strict_region_center_success_rate`
- `coordinate_curriculum/plane_localization_region_01_success_count` through region 09
- `region_mastery.csv` in the run directory

## 승격 규칙 / Promotion Rule

9개 영역 시뮬레이션을 반복적으로 모두 마스터하거나, 영역별로 안정적인 개선이 확인되기 전에는 `robotarm_mt4`나 실제 하드웨어로 옮기지 않는다. / Do not move this to `robotarm_mt4` or real hardware unless the 9-region simulation can repeatedly master all regions or produce a clearly improving region-by-region sequence with stable workspace entry and stereo visibility.
