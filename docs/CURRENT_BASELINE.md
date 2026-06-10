# Current Baseline - robotarm_student

Date: 2026-06-10 KST

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
- coordinate workspace-entry warm-up: `Isaac-MT4-Coordinate-Workspace-Entry-Direct-v0`
- coordinate-plane curriculum viewer: `scripts/view_coordinate_curriculum.sh`
- coordinate-plane stage 1: `Isaac-MT4-Coordinate-Plane-Direct-v0`
- student learning journal: `learning_journal/README.md`
- active three-camera coordinate thread: `learning_journal/2026-06-10_three_camera_coordinate_baseline/README.md`
- camera-only region archive: `learning_journal/2026-06-10_camera_only_region_matching/README.md`
- coordinate region mastery plan: `notes/20260610_coordinate_region_mastery_plan.md`
- camera-only region matching plan: `notes/20260610_camera_only_region_matching_plan.md`
- coordinate-sphere stage 2: `Isaac-MT4-Coordinate-Sphere-Direct-v0`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger simplified asset 생성: `scripts/create_two_finger_asset.sh`

미션은 다음처럼 분리합니다.

- `pick`
- `place`
- `stack`
- `push`
- `pull`

첫 실용 검증 대상은 `push` 또는 `pull`입니다. 두 미션은 완전한 grasp 모델에 의존하기 전에 동적 물체 접촉과 reset 동작을 먼저 증명할 수 있습니다.

추가 curriculum은 로봇팔 전면 작업공간을 몸체 좌/우 고정 가상 카메라와 그리퍼 장착 카메라 projection으로 학습합니다. 타겟 생성에는 로봇 기준 좌표를 쓰지만, 정책 관측과 시연 접근 선택에는 생성 좌표를 넣지 않고 카메라 기반 추정 영역, 카메라 추정 목표 상대좌표, 그리퍼 카메라 target projection을 사용합니다.

0. Stage 0: 홈 자세에서 카메라 가시 작업공간 안으로 진입하는 warm-up을 학습한다.
1. Stage 1: 전면 카메라 평면을 3x3 영역으로 나눠 1-9번을 부여하고, 같은 카메라 영역에 들어가면서 영역 중심 1cm 이내로 접근하면 성공으로 본다. 새 학습부터는 한 영역이 strict success를 10회 달성해야 같은 policy로 다음 번호를 이어서 학습한다.
2. Stage 2: 같은 three-camera coordinate 관측으로 기존 target sphere reach를 학습한다.

2026-06-10 새 기준선은 1500 iteration Stage 1 학습에서 9/9 영역을 모두 마스터했습니다. 마지막 배치 지표는 `target_three_camera_visible_rate=0.9014`, `camera_region_match_rate=1.0000`, `mean_distance=0.0545 m`, `strict_region_center_success_rate=0.0005`입니다. 이 결과는 기존 5회 성공 기준으로 만든 기준선입니다. 다음 학습부터는 영역별 10회 성공 기준을 사용해, 운 좋게 빨리 통과한 결과보다 더 안정적인 결과를 고릅니다.

현재 보정은 목표가 바뀌어도 비슷한 위치만 반복하는 문제를 줄이기 위한 target-tracking 재학습입니다. 정책 입력은 `51`개 값에서 `54`개 값으로 늘었고, 추가된 값은 몸체 스테레오 카메라로 추정한 목표 상대좌표입니다. 랜덤 데모 도구도 목표를 바꾼 직후 정책 관측을 즉시 새로 읽도록 수정했습니다.

2026-06-10 추가 보정은 성공 거리 기준을 `0.010 m`로 강화하고, 추적 보상을 그리퍼와 목표 지점 사이의 실제 거리 중심으로 더 강하게 둡니다. 목표를 지나쳐 반대편으로 넘어갔다가 돌아오는 움직임은 `target_overshoot` 벌점으로 낮추고, 가능하면 로봇 쪽 또는 위쪽에서 목표로 접근하도록 `preferred_approach_error`를 기록하고 보상에 반영합니다.

2026-06-10 1cm target-tracking 재학습은 1500 iteration에서 9/9 영역을 모두 마스터했습니다. 영역별 누적 성공 횟수는 모두 10회를 넘겼고, 마지막 배치 지표는 `mean_distance=0.0345 m`, `near_center_7cm_rate=0.8943`, `camera_region_match_rate=1.0000`, `target_three_camera_visible_rate=0.9197`, `target_overshoot=0.0128 m`입니다. 다만 마지막 배치의 `center_1cm_rate=0.0000`이므로, 다음 병목은 카메라 인식보다 목표 근처 마지막 1cm 정밀 제어입니다. 실행 기록은 `learning_journal/2026-06-10_three_camera_coordinate_baseline/20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md`입니다.

2026-06-10 첫 3x3x3 27영역 학습은 좋은 실패 기록으로 보존합니다. 1500 iteration 동안 `mastered_region_count=0`, `inside_workspace_rate=0.0000`, `center_1cm_rate=0.0000`이었고, 원인은 영역 수 자체보다 가동범위 기반 작업 박스를 먼저 확정하지 않은 데 있었습니다. 다음 27영역 학습은 gripper 가동 샘플을 기준으로 center `(0.30, 0.00, 0.21)`, size `(0.12, 0.16, 0.12)`인 보수 박스에서 실행합니다. 상세 기록은 `learning_journal/2026-06-10_three_camera_coordinate_baseline/20260610_143719_run_volume_3x3x3_failure_reach_audit.md`입니다.

Stage 1 검증은 `scripts/view_coordinate_curriculum.sh --stage plane`로 먼저 수행합니다. marker와 콘솔 로그가 1번부터 9번까지 순차적으로 넘어가는지 확인하고, 학습 run에서는 `region_mastery.csv`와 region별 success count를 같이 확인합니다. 이 결과가 반복 가능해진 뒤에만 `robotarm_mt4` 실제 기기 이식 후보로 올립니다.

### 오늘의 운영 규칙

오늘부터 매일 기준은 이 파일, `learning_journal/README.md`, `README.md`입니다. `notes/`, `experiments/`, `logs/plots/`는 이 파일이나 learning journal이 특정 항목을 링크하지 않는 한 archive로 취급합니다.

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
- `learning_journal/`는 학생에게 공유할 계획, 결과, 영상의 정리본입니다.
- routine command output이나 임시 plot artifact는 별도 노트로 만들지 않습니다.
- 새 finding은 dated note로 남기되, project baseline이 바뀔 때만 이 파일을 갱신합니다.
- 오늘 기준 판단은 이 파일, `learning_journal/README.md`, `README.md`만으로 끝나야 합니다.

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
- coordinate workspace-entry warm-up: `Isaac-MT4-Coordinate-Workspace-Entry-Direct-v0`
- coordinate-plane curriculum viewer: `scripts/view_coordinate_curriculum.sh`
- coordinate-plane stage 1: `Isaac-MT4-Coordinate-Plane-Direct-v0`
- student learning journal: `learning_journal/README.md`
- active three-camera coordinate thread: `learning_journal/2026-06-10_three_camera_coordinate_baseline/README.md`
- camera-only region archive: `learning_journal/2026-06-10_camera_only_region_matching/README.md`
- coordinate region mastery plan: `notes/20260610_coordinate_region_mastery_plan.md`
- camera-only region matching plan: `notes/20260610_camera_only_region_matching_plan.md`
- coordinate-sphere stage 2: `Isaac-MT4-Coordinate-Sphere-Direct-v0`
- Mars twin viewer: `scripts/view_mars_twin.sh`
- two-finger simplified asset generation: `scripts/create_two_finger_asset.sh`

The missions are split into:

- `pick`
- `place`
- `stack`
- `push`
- `pull`

The first practical validation target should be `push` or `pull`, because those missions can prove dynamic-object contact and reset behavior before relying on a complete grasp model.

The additional curriculum learns the front robot workspace through body left/right fixed virtual cameras plus a gripper-mounted camera projection. Target generation may use robot-frame coordinates, but policy observations and demo approach selection must not receive those generation coordinates; they use the camera-estimated region, the camera-estimated target-relative position, and the gripper-camera target projection.

0. Stage 0 learns home-to-camera-visible-workspace entry as a warm-up.
1. Stage 1 splits the front camera plane into 3x3 regions, numbers them 1-9, and treats a region as successful only when the gripper is in the same camera region and within 1 cm of the region center. New runs require 10 strict successes in one region before the same policy continues into the next number.
2. Stage 2 reuses the same three-camera coordinate observation for target-sphere reach.

The 2026-06-10 baseline mastered all 9 Stage 1 regions in a 1500-iteration run. Final-batch metrics were `target_three_camera_visible_rate=0.9014`, `camera_region_match_rate=1.0000`, `mean_distance=0.0545 m`, and `strict_region_center_success_rate=0.0005`. That baseline was produced with the previous 5-success mastery gate. New runs use a 10-success gate so region advancement prefers more repeatable behavior.

The current correction is a target-tracking rerun meant to reduce the demo pattern where the arm keeps moving to a similar point after targets change. The policy input increased from `51` values to `54` values; the added values are the body-stereo-estimated target-relative position. The random demo recorder now refreshes policy observations immediately after every target override.

The 2026-06-10 follow-up tightens the success distance to `0.010 m`, strengthens tracking around the actual gripper-to-target distance, penalizes moving past the target with `target_overshoot`, and logs/rewards `preferred_approach_error` so the arm prefers entering from the robot side or from above.

The 2026-06-10 1 cm target-tracking rerun mastered all 9 regions within 1500 iterations. Every region exceeded the 10-success cumulative gate. Final-batch metrics were `mean_distance=0.0345 m`, `near_center_7cm_rate=0.8943`, `camera_region_match_rate=1.0000`, `target_three_camera_visible_rate=0.9197`, and `target_overshoot=0.0128 m`. However, final-batch `center_1cm_rate=0.0000`, so the next bottleneck is final 1 cm control precision more than camera recognition. The run record is `learning_journal/2026-06-10_three_camera_coordinate_baseline/20260610_140823_run_three_camera_target_tracking_1cm_1500iter.md`.

Keep the first 2026-06-10 3x3x3 27-cell run as a useful failure record. Over 1500 iterations it stayed at `mastered_region_count=0`, `inside_workspace_rate=0.0000`, and `center_1cm_rate=0.0000`; the cause was not only the number of cells, but the missing reach-based workspace definition before volume training. The next 27-cell run uses a conservative gripper-reach box with center `(0.30, 0.00, 0.21)` and size `(0.12, 0.16, 0.12)`. Details are in `learning_journal/2026-06-10_three_camera_coordinate_baseline/20260610_143719_run_volume_3x3x3_failure_reach_audit.md`.

Validate Stage 1 first with `scripts/view_coordinate_curriculum.sh --stage plane`; the marker and console log should advance from region 1 through 9 in order. During training, also inspect `region_mastery.csv` and the per-region success counts. Keep this validation in `robotarm_student` and consider `robotarm_mt4` transfer only after the student simulation result is repeatable.

### Today's Operating Rule

From today, use this file, `learning_journal/README.md`, and `README.md` as the daily baseline. Treat `notes/`, `experiments/`, and `logs/plots/` as archive unless this file or the learning journal links to a specific entry.

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
- `learning_journal/` is the student-facing summary of plans, results, and videos.
- Do not create separate notes for routine command output or temporary plot artifacts.
- Record new findings as dated notes, then update this file only when the project baseline changes.
- Daily baseline decisions should be possible from this file, `learning_journal/README.md`, and `README.md`.

### Next Work

1. Confirm the Mars twin scene opens for `push` and `pull`.
2. Confirm object contact and reset behavior in simulation.
3. Decide the conservative home pose and action limits.
4. Add one meaningful experiment note per training run.
5. Promote only stable, repeatable results into this baseline.
