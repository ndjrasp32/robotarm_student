# 2026-06-10 좌표 영역 마스터리 확장 학습 계획 / Coordinate Region Mastery Extended Run Plan

## 변경 / Change

Stage 1 순차 9영역 학습을 1500 iteration 이상으로 다시 실행한다. / Rerun the Stage 1 sequential 9-region training at 1500 iterations or more.

성공 조건은 그대로 유지한다. / The success rule stays unchanged:

- 목표와 같은 스테레오 카메라 셀에 진입 / same stereo camera cell as the target
- 그리퍼 중심이 영역 중심 목표에서 `0.030 m` 이내 / gripper center within `0.030 m` of the region center
- 목표와 그리퍼가 양쪽 가상 카메라에서 보임 / target and gripper visible in both virtual cameras

## 이유 / Why

500회 학습은 1, 2번 영역을 마스터한 뒤 3번에서 멈췄다. 1500회 학습은 7번 영역까지 마스터하고 8번 영역에서 멈췄다. / The 500-iteration run mastered regions 1 and 2 and stopped at region 3. The 1500-iteration run mastered through region 7 and stopped at region 8.

두 결과 모두 카메라 영역 진입률은 높았지만, 중심 3cm까지 안정적으로 수렴하는 능력이 부족했다. / In both results, camera-region entry was high, but stable convergence to the 3 cm center criterion was still weak.

따라서 이번 반영은 성공 기준을 완화하지 않고, 7cm 이내 중심 접근 구간에서만 조밀 보상을 추가한다. / Therefore this update does not relax the success rule; it adds dense shaping only inside the 7 cm near-center band.

## 사용자 제안과 Codex 제안 / User Proposal and Codex Proposal

사용자 제안 / User proposal:

- 거리 기준은 모든 영역에서 동일하게 3cm로 둔다. / Keep the distance criterion identical across all regions at 3 cm.
- 영역별 성공 횟수를 기준으로 다음 영역으로 넘어간다. / Advance by per-region success counts.
- 하나의 정책을 이어서 학습하고, 영역별 최고 보상 기록을 남긴다. / Continue one policy and preserve the best reward record per region.
- 학습 시간, 성공률, 그래프, 영상까지 학생용 결과물로 남긴다. / Save training time, success rates, graphs, and video as student-facing results.

Codex 제안 / Codex proposal:

- `near_center_7cm_rate`를 추가해 3cm 직전 수렴 상태를 관찰한다. / Add `near_center_7cm_rate` to observe convergence before the strict 3 cm success.
- `near_center_weight`를 추가하되 성공 판정에는 넣지 않는다. / Add `near_center_weight` but keep it out of the success condition.
- 리포트와 노트는 한국어/영어 병기로 작성한다. / Write reports and notes in Korean/English bilingual form.

## 출력 / Output

- 학습 영상은 `scripts/train_coordinate_stage1_plane_128_1500_video.sh`에서 기본 활성화된다. / Training video is enabled by default in `scripts/train_coordinate_stage1_plane_128_1500_video.sh`.
- `tools/report_mt4_coordinate_curriculum.py`는 좌표 전용 그래프와 학생용 병기 리포트를 생성한다. / `tools/report_mt4_coordinate_curriculum.py` generates coordinate-specific graphs and a bilingual student report.
- `scripts/play_coordinate_stage1_best_video.sh`는 학습 후 체크포인트 재생 영상을 기록할 수 있다. / `scripts/play_coordinate_stage1_best_video.sh` can record a checkpoint replay video after training.

## 판단 규칙 / Decision Rule

결과는 시뮬레이션 안에서만 판단한다. 9개 영역을 모두 마스터하거나, 다음 학습으로 이어갈 만큼 안정적인 영역별 개선 경로가 보일 때까지 실제 하드웨어로 승격하지 않는다. / Keep the result in simulation. Do not promote to real hardware unless all 9 regions are mastered or the report shows a stable region-by-region improvement path worth continuing.
