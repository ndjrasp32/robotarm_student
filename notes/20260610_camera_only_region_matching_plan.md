# 2026-06-10 카메라 전용 영역 매칭 계획 / Camera-Only Region Matching Plan

## 목적 / Purpose

실제 로봇팔은 타겟을 좌표 truth로 직접 알 수 없고, 카메라로만 인식해야 한다. / The real robot arm cannot directly know target ground-truth coordinates; it must recognize the target through cameras only.

따라서 다음 학습과 시연은 타겟 생성 좌표와 정책 입력 좌표를 분리한다. 타겟 영역 1-9번은 로봇팔 기기 기준 좌표로 생성하되, 학습과 시연에서 정책이 사용하는 영역 판단은 두 대의 카메라 관측으로만 만든다. / Therefore the next training and demo separate target-generation coordinates from policy-input coordinates. Regions 1-9 are generated in the robot-device coordinate frame, but the region decision used by training and demo is produced only from two-camera observations.

## 핵심 원칙 / Core Principle

- 타겟 생성에는 로봇 기준 좌표를 사용한다. / Use robot-frame coordinates for target generation.
- 생성 좌표는 정답 라벨과 검증용으로만 남긴다. / Keep generation coordinates only as labels and validation data.
- 정책 관측에는 생성 좌표를 넣지 않는다. / Do not feed generation coordinates into the policy observation.
- 정책은 두 카메라에서 보이는 타겟 위치로 1-9번 영역을 추정한다. / The policy estimates regions 1-9 from the target position visible in the two cameras.
- 시연에서는 생성 좌표를 접근 로직에 쓰지 않고, 카메라 기반 추정 영역으로 접근 방식을 선택한다. / During demo, do not use generation coordinates for approach logic; choose the approach mode from the camera-estimated region.

## 현재 문제 / Current Problem

랜덤 9영역 시연은 타겟 번호를 알고 있는 것처럼 보이지만, 실제 접근은 타겟 위치를 안정적으로 잡지 못했다. / The random 9-region demo appears to know the target number, but the actual approach did not reliably acquire the target position.

이 문제는 정책이 "어느 영역에 있는 타겟인지 먼저 확인한 뒤 그 영역 접근 방식을 선택"하는 구조가 부족하다는 뜻이다. / This means the policy lacks a structure that first confirms which region the target is in and then selects the matching approach behavior.

## 제안 구조 / Proposed Structure

1. 타겟 생성 / Target generation
   - 시뮬레이션은 로봇팔 기준 workspace를 3x3 영역으로 나누고, 매 episode마다 1-9번 중 하나를 랜덤 선택한다. / Simulation splits the robot-frame workspace into 3x3 regions and randomly selects one of regions 1-9 each episode.
   - 선택된 영역 안에서 타겟 좌표를 생성한다. / Generate the target coordinate inside the selected region.
   - 이 좌표와 true region id는 환경 내부 평가와 report용으로만 저장한다. / Store the coordinate and true region id only for internal evaluation and reports.

2. 카메라 관측 / Camera observation
   - 두 대의 고정 카메라에서 타겟 pixel 또는 normalized image coordinate를 얻는다. / Obtain target pixels or normalized image coordinates from two fixed cameras.
   - 두 카메라 모두에서 타겟이 보일 때만 valid observation으로 본다. / Treat the observation as valid only when both cameras see the target.
   - 카메라 관측값을 stereo matching 또는 calibrated projection으로 camera-region estimate에 매핑한다. / Map the camera observations to a camera-region estimate through stereo matching or calibrated projection.

3. 영역 매칭 / Region matching
   - camera-estimated target position을 3x3 영역 id로 변환한다. / Convert the camera-estimated target position into a 3x3 region id.
   - 학습 중에는 true region id와 camera-estimated region id를 비교해 perception mismatch를 따로 기록한다. / During training, compare true region id and camera-estimated region id and log perception mismatch separately.
   - 접근 보상은 camera-estimated region을 기준으로 준다. / Give approach reward using the camera-estimated region.

4. 접근 정책 / Approach policy
   - 정책 입력에는 gripper camera projection, target camera projection, estimated region id, visibility flag를 넣는다. / Policy observation includes gripper camera projection, target camera projection, estimated region id, and visibility flags.
   - 영역별 접근 모드는 별도 hard-coded branch가 아니라, estimated region id를 조건으로 받는 하나의 정책에서 학습한다. / Region approach is learned by one policy conditioned on the estimated region id, not by separate hard-coded branches.
   - 시연 단계도 같은 입력만 사용한다. / Demo uses the same inputs.

## 학습 기준 / Training Rule

성공 판정은 두 층으로 나눈다. / Split success into two layers.

- Perception success: camera-estimated region id가 true generated region id와 일치한다. / Perception success means the camera-estimated region id matches the true generated region id.
- Control success: camera-estimated region 기준으로 접근한 뒤, 검증용 true target center와 gripper 거리가 `0.030 m` 이내다. / Control success means the gripper approaches according to the camera-estimated region and ends within `0.030 m` of the validation-only true target center.

거리 기준은 1-9번 모든 영역에서 동일하게 유지한다. / Keep the distance criterion identical for all regions 1-9.

## 필요한 로그 / Required Logs

- `true_region_id`: 생성된 실제 영역 번호 / generated true region number
- `camera_estimated_region_id`: 두 카메라로 추정한 영역 번호 / region number estimated from two cameras
- `region_match`: true와 estimated의 일치 여부 / whether true and estimated match
- `target_visible_left`, `target_visible_right`: 양쪽 카메라 타겟 가시성 / target visibility in both cameras
- `gripper_visible_left`, `gripper_visible_right`: 양쪽 카메라 그리퍼 가시성 / gripper visibility in both cameras
- `perception_success_rate`: 영역 인식 성공률 / region perception success rate
- `control_success_rate_by_estimated_region`: 추정 영역 기준 접근 성공률 / approach success rate by estimated region
- `control_success_rate_by_true_region`: 실제 생성 영역 기준 검증 성공률 / validation success rate by true generated region

## 시연 기준 / Demo Rule

시연 영상에서는 화면에 true generated region과 camera-estimated region을 같이 표시한다. / In demo videos, display both the true generated region and the camera-estimated region.

하지만 접근 선택에는 camera-estimated region만 사용한다. true generated region은 학생이 인식 오차와 제어 오차를 구분해서 보기 위한 overlay로만 사용한다. / However, use only the camera-estimated region for approach selection. The true generated region is only an overlay so students can separate perception error from control error.

## 다음 구현 순서 / Next Implementation Order

1. 현재 coordinate curriculum 환경에서 true target generation과 policy observation을 분리한다. / Separate true target generation from policy observation in the current coordinate curriculum environment.
2. 두 카메라 target projection에서 3x3 estimated region을 계산하는 helper를 추가한다. / Add a helper that computes the 3x3 estimated region from two-camera target projections.
3. perception metrics와 mismatch logging을 추가한다. / Add perception metrics and mismatch logging.
4. 학습은 estimated region 기반 보상으로 다시 실행한다. / Rerun training with reward based on estimated region.
5. 시연 영상은 true/generated region과 camera-estimated region overlay를 모두 넣되, policy 접근은 camera estimate만 사용한다. / Generate demo video with both true/generated and camera-estimated overlays, while the policy uses only the camera estimate.

## 승격 규칙 / Promotion Rule

이 계획은 실제 로봇 motion을 바로 수행하지 않는다. / This plan does not run real robot motion directly.

`robotarm_student`에서는 카메라 기반 인식과 제어가 시뮬레이션에서 반복 가능해야 한다. 그 뒤에만 `robotarm_mt4`에서 no-motion camera calibration, low-speed dry-run, safety gate 순서로 실제 기기 이식을 검토한다. / In `robotarm_student`, camera-based perception and control must be repeatable in simulation first. Only after that should `robotarm_mt4` evaluate real-device transfer through no-motion camera calibration, low-speed dry-run, and the safety gate.
