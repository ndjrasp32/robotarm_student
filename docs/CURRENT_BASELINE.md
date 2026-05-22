# Current Baseline - robotarm_student

Date: 2026-05-22 KST

## 한국어

### 저장소 역할

`robotarm_student`는 학생용 WLKATA MT4 curriculum 저장소입니다.

이 저장소에서 관리하는 범위:

- 반복 가능한 IsaacLab MT4 curriculum 실행
- staged reach, pregrasp, insertion 실험
- Mars rover manipulation twin 실습
- 학생이 참고할 수 있는 실험 기록 archive

하드웨어에 가까운 Mirobot/MT4 asset 검증, joint/action mapping, 실제 기기 transfer gate는 `robotarm_mt4`에서 관리합니다.

### 현재 기준

현재 방향은 Mars rover MT4 manipulation plan에서 다시 시작합니다.

- 참고 계획: `notes/20260521_mars_rover_mt4_rl_plan.md`
- active task package: `source/mt4_reach_direct`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger simplified asset 생성: `scripts/create_two_finger_asset.sh`

미션은 다음처럼 분리합니다.

- `pick`
- `place`
- `stack`
- `push`
- `pull`

첫 실용 검증 대상은 `push` 또는 `pull`입니다. 두 미션은 완전한 grasp 모델에 의존하기 전에 동적 물체 접촉과 reset 동작을 먼저 증명할 수 있습니다.

### 오늘의 운영 규칙

오늘부터 매일 기준은 이 파일과 `README.md`입니다. `notes/`, `experiments/`, `logs/plots/`는 이 파일이 특정 항목을 링크하지 않는 한 archive로 취급합니다.

시작 순서:

1. Mars twin scene을 `push` 또는 `pull`로 연다.
2. simulation에서 object contact와 reset 동작을 확인한다.
3. 실제 training run이나 설계 결정이 바뀐 경우에만 concise experiment note를 하나 남긴다.
4. 반복 가능한 새 기준이 되었을 때만 이 파일로 승격한다.

### 리셋 이유

2026-05-22 기준으로 baseline을 리셋했습니다. 이전 작업 상태는 날짜별 노트가 너무 많고, 저장소 이름이 바뀌었으며, 학생용 curriculum과 하드웨어 전이 책임이 섞여 있었습니다. 이제 이 저장소는 학생용 MT4 curriculum baseline입니다. 이전 `notes/`와 `experiments/` 항목은 daily source of truth가 아니라 archive입니다.

### Safety Gate

학습된 정책은 아래 항목이 기록되기 전까지 hardware-ready로 보지 않습니다.

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

실제 로봇 motion은 이 gate 뒤에 둡니다.

### 문서 운영 규칙

- 기존 `notes/`와 `experiments/`는 historical archive입니다.
- routine command output이나 임시 plot artifact는 별도 노트로 만들지 않습니다.
- 새 finding은 dated note로 남기되, project baseline이 바뀔 때만 이 파일을 갱신합니다.
- 오늘 기준 판단은 `README.md`와 이 파일만으로 끝나야 합니다.

### 다음 작업

1. `push`와 `pull` Mars twin scene이 열리는지 확인한다.
2. object contact와 reset 동작을 simulation에서 확인한다.
3. conservative home pose와 action limits를 정한다.
4. training run마다 의미 있는 experiment note를 하나만 남긴다.
5. 안정적으로 반복되는 결과만 이 baseline으로 승격한다.

## English

### Repository Role

`robotarm_student` is the student-facing WLKATA MT4 curriculum repository.

Use this repository for:

- repeatable IsaacLab MT4 curriculum runs
- staged reach, pregrasp, and insertion experiments
- Mars rover manipulation twin practice
- experiment archives that students can review

Use `robotarm_mt4` for hardware-facing Mirobot/MT4 asset checks, joint/action mapping, and real-device transfer gates.

### Current Baseline

The active direction restarts from the Mars rover MT4 manipulation plan.

- reference plan: `notes/20260521_mars_rover_mt4_rl_plan.md`
- active task package: `source/mt4_reach_direct`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger simplified asset generation: `scripts/create_two_finger_asset.sh`

The missions are split into:

- `pick`
- `place`
- `stack`
- `push`
- `pull`

The first practical validation target should be `push` or `pull`, because those missions can prove dynamic-object contact and reset behavior before relying on a complete grasp model.

### Today's Operating Rule

From today, use only this file and `README.md` as the daily baseline. Treat `notes/`, `experiments/`, and `logs/plots/` as archive unless this file links to a specific entry.

Start sequence:

1. Open the Mars twin scene for `push` or `pull`.
2. Confirm object contact and reset behavior in simulation.
3. Record one concise experiment note only if a real training run or design decision changes.
4. Promote the result into this file only after it becomes the new repeatable baseline.

### Reset Rationale

The baseline was reset on 2026-05-22 because the previous working state had too many dated notes, the repositories had been renamed, and student curriculum responsibilities were mixed with hardware-transfer responsibilities. From now on, this repository is the student-facing MT4 curriculum baseline. Older `notes/` and `experiments/` entries remain archive rather than the daily source of truth.

### Safety Gate

Do not treat a trained policy as hardware-ready until these items are recorded:

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

Real robot motion must stay behind this gate.

### Documentation Policy

- Existing `notes/` and `experiments/` are historical archive.
- Do not create separate notes for routine command output or temporary plot artifacts.
- Record new findings as dated notes, then update this file only when the project baseline changes.
- Daily baseline decisions should be possible from `README.md` and this file alone.

### Next Work

1. Confirm the Mars twin scene opens for `push` and `pull`.
2. Confirm object contact and reset behavior in simulation.
3. Decide the conservative home pose and action limits.
4. Add one meaningful experiment note per training run.
5. Promote only stable, repeatable results into this baseline.
