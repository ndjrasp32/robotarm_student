# robotarm_student

## 한국어

`robotarm_student`는 학생/실습용 WLKATA MT4 IsaacLab 강화학습 저장소입니다.

이 저장소는 MT4 기반 staged reach, pregrasp, insertion curriculum과 실험 기록을 수업과 반복 실습 기준으로 관리합니다. 실제 MT4 asset 검증, 하드웨어 매핑, 실제 기기 이식 판단은 `robotarm_mt4`에서 관리하고, 이 저장소에서는 학생이 따라갈 수 있는 강화학습 흐름과 실험 archive를 유지합니다.

### 오늘부터 보는 기준

매일 시작할 때는 이 순서만 봅니다.

1. `docs/CURRENT_BASELINE.md`
2. `learning_journal/README.md`
3. `README.md`
4. `notes/`와 `experiments/`는 기준 문서에 링크된 항목만 필요할 때 확인

현재 기준은 Mars rover MT4 manipulation plan에서 다시 시작합니다. 첫 실용 검증 대상은 `push` 또는 `pull`입니다. 이 두 미션은 완전한 grasp 모델에 의존하기 전에 동적 물체 접촉과 reset 동작을 먼저 확인할 수 있기 때문입니다.

### 리셋 이유

2026-05-22 기준으로 작업 기준을 리셋했습니다. 이전 상태에서는 날짜별 노트와 실험 기록이 너무 많아졌고, GitHub 저장소 이름도 `robotarm_student`와 `robotarm_mt4`로 정리되었으며, 학생용 curriculum과 실제 하드웨어 전이 책임이 한 흐름 안에 섞여 있었습니다. 이제 이 저장소는 학생용 MT4 curriculum baseline으로만 봅니다. 오래된 `notes/`, `experiments/`, `logs/`는 삭제하지 않고 archive로 유지합니다.

### 주요 위치

- IsaacLab task: `source/mt4_reach_direct`
- coordinate workspace-entry warm-up: `scripts/train_coordinate_stage0_workspace_entry_128_300.sh`
- coordinate-plane curriculum viewer: `scripts/view_coordinate_curriculum.sh`
- coordinate-plane stage 1 training: `scripts/train_coordinate_stage1_plane_128_500.sh`
- student learning journal: `learning_journal/README.md`
- active three-camera coordinate thread: `learning_journal/2026-06-10_three_camera_coordinate_baseline/README.md`
- camera-only region archive: `learning_journal/2026-06-10_camera_only_region_matching/README.md`
- coordinate region mastery note: `notes/20260610_coordinate_region_mastery_plan.md`
- camera-only region matching plan: `notes/20260610_camera_only_region_matching_plan.md`
- coordinate-sphere stage 2 training: `scripts/train_coordinate_stage2_sphere_128_800.sh`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger asset 생성: `scripts/create_two_finger_asset.sh`
- 실행 스크립트: `scripts/`
- 실험 기록: `experiments/`
- 작업 노트 archive: `notes/`
- 학생용 계획/결과/영상 기록: `learning_journal/`
- 실제 기기 관련 보조 자료: `hardware/`

### 문서 운영 규칙

- 새 문서는 늘리지 않는 것을 기본값으로 둡니다.
- routine command output이나 임시 plot은 새 노트로 만들지 않습니다.
- 실제 학습 run 또는 설계 결정이 바뀐 경우에만 dated note나 experiment record를 하나 남깁니다.
- 기준이 바뀐 경우에만 `docs/CURRENT_BASELINE.md`로 승격합니다.
- 실제 로봇 motion은 `robotarm_mt4`의 safety gate를 통과하기 전까지 이 저장소의 기본 작업으로 보지 않습니다.

## English

`robotarm_student` is the student-facing WLKATA MT4 IsaacLab reinforcement-learning repository.

This repository manages MT4 staged reach, pregrasp, insertion curriculum work and experiment records for classroom use and repeatable practice. Real MT4 asset validation, hardware mapping, and hardware-transfer decisions belong in `robotarm_mt4`. This repository keeps the student learning path and experiment archive.

### Daily Starting Point

Start each day in this order:

1. `docs/CURRENT_BASELINE.md`
2. `learning_journal/README.md`
3. `README.md`
4. Open `notes/` and `experiments/` only when the baseline links to a specific entry

The active baseline restarts from the Mars rover MT4 manipulation plan. The first practical validation target should be `push` or `pull`, because those missions can validate dynamic-object contact and reset behavior before relying on a complete grasp model.

The coordinate-plane curriculum is a student-side simulation path for learning the camera-frame front workspace before object approach:

0. `Isaac-MT4-Coordinate-Workspace-Entry-Direct-v0`: learn to move from home into the camera-visible workspace.
1. `Isaac-MT4-Coordinate-Plane-Direct-v0`: split the front camera plane into 3x3 regions, number them 1-9, require same-region entry plus center approach within 1 cm, reset home, then advance after 10 strict successes in that region.
2. `Isaac-MT4-Coordinate-Sphere-Direct-v0`: reuse the same three-camera coordinate observation and train the existing target-sphere reach behavior after the 9-region coordinate stage is stable.

The current region-matching baseline keeps robot-frame coordinates only for target generation and validation. Training infers the target region from the body left/right stereo observations and also receives a gripper-mounted camera projection for target tracking. New target-tracking runs use a stricter 1 cm success distance, add an overshoot penalty, and prefer approach from the robot side or from above.

Coordinate curriculum training uses `tools/train_mt4_coordinate_curriculum.py` so the task is registered from `robotarm_student/source` instead of the hardware-transfer repo or stale IsaacLab copies.

Use `scripts/view_coordinate_curriculum.sh --stage plane` to verify that the Stage 1 target marker advances through regions 1-9 in order. Keep this validation in `robotarm_student`; only transfer the approach to `robotarm_mt4` after the student simulation result is repeatable.

### Reset Rationale

The working baseline was reset on 2026-05-22. The previous state had too many daily notes and experiment records, the GitHub repositories had been renamed into `robotarm_student` and `robotarm_mt4`, and student curriculum work was mixed with hardware-transfer responsibilities. From now on, this repository is the student-facing MT4 curriculum baseline. Older `notes/`, `experiments/`, and `logs/` remain as archive.

### Important Paths

- IsaacLab task: `source/mt4_reach_direct`
- coordinate workspace-entry warm-up: `scripts/train_coordinate_stage0_workspace_entry_128_300.sh`
- coordinate-plane curriculum viewer: `scripts/view_coordinate_curriculum.sh`
- coordinate-plane stage 1 training: `scripts/train_coordinate_stage1_plane_128_500.sh`
- student learning journal: `learning_journal/README.md`
- active three-camera coordinate thread: `learning_journal/2026-06-10_three_camera_coordinate_baseline/README.md`
- camera-only region archive: `learning_journal/2026-06-10_camera_only_region_matching/README.md`
- coordinate region mastery note: `notes/20260610_coordinate_region_mastery_plan.md`
- camera-only region matching plan: `notes/20260610_camera_only_region_matching_plan.md`
- coordinate-sphere stage 2 training: `scripts/train_coordinate_stage2_sphere_128_800.sh`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger asset generation: `scripts/create_two_finger_asset.sh`
- runnable scripts: `scripts/`
- experiment records: `experiments/`
- work-note archive: `notes/`
- student-facing plan/result/video records: `learning_journal/`
- real-device support material: `hardware/`

### Documentation Policy

- Do not create new documents by default.
- Do not turn routine command output or temporary plots into new notes.
- Add one dated note or experiment record only when a real training run or design decision changes.
- Promote only baseline-changing conclusions into `docs/CURRENT_BASELINE.md`.
- Real robot motion is not part of the default workflow here until the safety gate in `robotarm_mt4` is satisfied.
