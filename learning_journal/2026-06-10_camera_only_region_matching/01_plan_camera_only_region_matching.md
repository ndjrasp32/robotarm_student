# 2026-06-10 Camera-Only Region Matching Plan / 카메라 전용 영역 매칭 계획

## Summary / 요약

- KR: 실제 로봇팔은 카메라로만 타겟을 인식해야 하므로, 학습에서도 타겟 생성 좌표를 정책 입력에서 제거한다.
- EN: Because the real robot arm must recognize the target only through cameras, training removes target-generation coordinates from policy input.

## Problem / 문제

- KR: 기존 랜덤 9영역 시연은 타겟 번호를 알고 있는 것처럼 보였지만, 실제 접근은 타겟 위치를 안정적으로 잡지 못했다.
- EN: The earlier random 9-region demo appeared to know the target number, but the actual approach did not reliably acquire the target position.

## Decision / 결정

- KR: 로봇 기준 좌표는 타겟 생성과 검증에만 사용한다.
- EN: Robot-frame coordinates are used only for target generation and validation.
- KR: 정책 관측과 시연 접근 선택은 두 카메라에서 계산한 `camera_estimated_region_id`만 사용한다.
- EN: Policy observations and demo approach selection use only `camera_estimated_region_id` computed from two cameras.
- KR: true region과 estimated region을 함께 기록해 인식 오차와 제어 오차를 분리한다.
- EN: Log both true and estimated regions so perception error and control error can be separated.

## Required Logs / 필요한 로그

| field | meaning / 의미 |
| --- | --- |
| `true_region_id` | generated target region / 생성된 타겟 영역 |
| `camera_estimated_region_id` | two-camera estimated region / 두 카메라 추정 영역 |
| `region_match` | true-estimated match / 정답-추정 일치 여부 |
| `target_visible_left/right` | target visibility / 타겟 가시성 |
| `gripper_visible_left/right` | gripper visibility / 그리퍼 가시성 |
| `perception_success_rate` | region-recognition success / 영역 인식 성공률 |
| `control_success_rate_by_estimated_region` | control result by estimated region / 추정 영역 기준 제어 결과 |
| `control_success_rate_by_true_region` | validation result by true region / 실제 영역 기준 검증 결과 |

## Demo Rule / 시연 규칙

- KR: 화면 overlay에는 true generated region과 camera-estimated region을 같이 표시한다.
- EN: The screen overlay shows both the true generated region and the camera-estimated region.
- KR: 접근 선택에는 true generated region을 쓰지 않고 camera-estimated region만 사용한다.
- EN: Approach selection uses only the camera-estimated region, not the true generated region.

## Next Step / 다음 단계

- KR: 기존 coordinate curriculum에서 생성 좌표와 정책 관측을 분리하고, Stage 1을 다시 학습한다.
- EN: Separate generated coordinates from policy observations in the coordinate curriculum, then rerun Stage 1 training.

