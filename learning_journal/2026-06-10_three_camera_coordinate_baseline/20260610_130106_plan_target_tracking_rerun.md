# 2026-06-10 Target Tracking Rerun Plan / 목표 추적 재학습 계획

## Summary / 요약

- KR: 이전 3카메라 학습은 9개 영역을 빠르게 통과했지만, 데모에서 새 목표를 충분히 따라가지 못하고 비슷한 위치로 가는 모습이 남았다.
- EN: The previous three-camera run passed all 9 regions quickly, but the demo still looked like the arm often moved to a similar point instead of following each new target.

- KR: 이번 수정은 "영역을 맞추는 능력"에서 한 단계 더 나아가 "그 영역 안의 목표 중심까지 따라가는 능력"을 강화한다.
- EN: This update goes beyond matching the correct region and strengthens movement toward the target center inside that region.

## Question / 질문

- KR: 카메라가 세 대인데도 왜 새 목표를 충분히 못 따라갔을까?
- EN: Why did the policy struggle to follow new targets even with three cameras?

## Answer / 답

- KR: 카메라는 목표를 볼 수 있었지만, 정책 입력과 보상이 목표 중심으로 가는 행동을 충분히 강하게 요구하지 않았다.
- EN: The cameras could see the target, but the observation and reward did not ask strongly enough for motion to the target center.

- KR: 또한 랜덤 데모에서는 목표를 덮어쓴 뒤 정책 관측을 바로 새로 읽지 않아, 짧은 순간 이전 목표 정보로 행동할 수 있었다.
- EN: The random demo also refreshed the target before refreshing the policy observation, so the policy could briefly act from stale target information.

## Implementation / 구현

- KR: 정책 관측을 `51`개 값에서 `54`개 값으로 늘렸다.
- EN: Increased the policy observation from `51` values to `54` values.

- KR: 추가된 3개 값은 몸체 좌/우 스테레오 카메라로 추정한 목표 위치에서 현재 그리퍼 위치를 뺀 상대좌표다.
- EN: The 3 added values are the relative position from the current gripper to the body-stereo-estimated target point.

- KR: 목표 중심에 가까워질수록 보상이 커지도록 target-tracking 보상을 추가했다.
- EN: Added a target-tracking reward that becomes larger as the gripper gets closer to the target center.

- KR: 랜덤 데모는 목표를 바꾼 직후 항상 새 관측을 다시 읽도록 고쳤다.
- EN: Fixed the random demo to always reload observations immediately after changing the target.

- KR: 성공 기준은 완화하지 않았다. 여전히 같은 영역에 들어가고 목표 중심 `3 cm` 안에 들어와야 성공이다.
- EN: The success rule was not relaxed. Success still requires the same region and being within `3 cm` of the target center.

## New Run Rule / 새 실행 규칙

| item | value |
| --- | --- |
| script / 스크립트 | `scripts/train_coordinate_stage1_three_camera_target_tracking_128_1500_video.sh` |
| run name / 실행 이름 | `three_camera_target_tracking_128env_1500iter` |
| success gate / 영역 통과 기준 | 10 strict successes per region |
| training video / 학습 영상 | about 1 minute |
| demo video / 데모 영상 | about 1 minute, random region sequence CSV included |

## Check / 확인할 점

- KR: `region_mastery.csv`에서 각 영역이 10회 성공으로 넘어가는지 본다.
- EN: Check whether each region advances after 10 successes in `region_mastery.csv`.

- KR: 데모 CSV에서 목표 번호가 바뀌는지 확인한다.
- EN: Confirm that the target region number changes in the demo CSV.

- KR: 영상에서 목표 번호가 바뀔 때 그리퍼가 같은 지점만 반복하지 않고 새 위치로 움직이는지 본다.
- EN: In the video, check whether the gripper moves toward the new target instead of repeating one point.

## Evidence / 근거 자료

- Environment / 환경: [../../source/mt4_reach_direct/mt4_coordinate_curriculum_env.py](../../source/mt4_reach_direct/mt4_coordinate_curriculum_env.py)
- Demo recorder / 데모 도구: [../../tools/record_mt4_coordinate_region_demo.py](../../tools/record_mt4_coordinate_region_demo.py)
- Training script / 학습 스크립트: [../../scripts/train_coordinate_stage1_three_camera_target_tracking_128_1500_video.sh](../../scripts/train_coordinate_stage1_three_camera_target_tracking_128_1500_video.sh)
