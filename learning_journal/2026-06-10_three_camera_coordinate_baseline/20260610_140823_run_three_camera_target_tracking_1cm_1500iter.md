# 2026-06-10 1cm Target-Tracking Rerun / 1cm 목표 추적 재학습

## Summary / 요약

- KR: 세 대 카메라 입력에 카메라 추정 목표 좌표를 더하고, 1cm 성공 기준으로 Stage 1을 다시 학습했다.
- EN: Stage 1 was rerun with three-camera observations, camera-estimated target coordinates, and the stricter 1 cm success rule.

## Question / 질문

- KR: 목표가 바뀔 때 로봇팔이 같은 위치만 반복하지 않고 새 목표 중심을 따라갈 수 있는가?
- EN: When the target changes, can the arm follow the new target center instead of repeating one similar point?

## Decision / 결정

- KR: 영역 통과 기준을 영역별 엄격 성공 10회로 두고, 성공 거리는 `0.010 m`로 유지한다.
- EN: Keep the region gate at 10 strict successes per region, and keep the success distance at `0.010 m`.

- KR: 카메라가 목표를 잘 찾는지와 로봇팔이 마지막 1cm까지 잘 맞추는지는 나누어 본다.
- EN: Separate camera target recognition from final 1 cm arm-control precision.

## Implementation / 구현

- KR: 정책 입력을 51개 값에서 54개 값으로 늘렸다. 새 값은 몸체 스테레오 카메라가 추정한 목표 상대좌표다.
- EN: The policy observation increased from 51 to 54 values. The new values are the target-relative coordinates estimated from the body stereo cameras.

- KR: 목표를 지나쳐 반대편으로 넘어가는 움직임에는 `target_overshoot` 벌점을 넣었다.
- EN: Motion that passes beyond the target receives a `target_overshoot` penalty.

- KR: 로봇 쪽이나 위쪽에서 목표로 들어오는 접근을 선호하도록 `preferred_approach_error`를 기록하고 보상에 반영했다.
- EN: `preferred_approach_error` is logged and rewarded so the arm prefers entering from the robot side or from above.

- KR: 랜덤 데모에서는 목표를 바꾼 직후 정책 관측도 즉시 다시 읽도록 수정했다.
- EN: The random demo now refreshes policy observations immediately after every target change.

## Run / 실행

| item | value |
| --- | --- |
| task | `Isaac-MT4-Coordinate-Plane-Direct-v0` |
| command | `./scripts/train_coordinate_stage1_three_camera_target_tracking_128_1500_video.sh` |
| run directory | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter` |
| final checkpoint | `model_1499.pt` |
| training time | 2251.43 seconds, about 37m 31s |
| training video | [20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4](../videos/20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4) |
| demo video | [20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4](../videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4) |
| demo sequence | [20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv](../videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv) |
| full report | [20260610_132926_three_camera_target_tracking_128env_1500iter_three_camera_target_tracking_1cm_stage1_1500iter.md](../../experiments/20260610_132926_three_camera_target_tracking_128env_1500iter_three_camera_target_tracking_1cm_stage1_1500iter.md) |

## Result / 결과

| metric | value |
| --- | ---: |
| mastered_region_count | 9 / 9 |
| region success gate | 10 strict successes |
| mean_distance | 0.0345 m, 3.45 cm |
| near_center_7cm_rate | 0.8943 |
| center_1cm_rate | 0.0000 in the final logging batch |
| camera_region_match_rate | 1.0000 |
| target_three_camera_visible_rate | 0.9197 |
| target_overshoot | 0.0128 m |
| preferred_approach_error | 0.0264 m |

## Interpretation / 해석

- KR: 영역별 누적 기록으로는 9개 영역이 모두 1cm 엄격 조건을 10회 이상 통과했다.
- EN: In cumulative per-region records, all 9 regions passed the 1 cm strict condition at least 10 times.

- KR: 마지막 배치의 `center_1cm_rate`는 0이었다. 이것은 마지막 순간에 1cm 안에 자주 머물지는 못했다는 뜻이다.
- EN: The final batch `center_1cm_rate` was 0. This means the policy did not often stay inside 1 cm at the final moment.

- KR: 그래서 이번 결과는 "카메라가 목표 영역을 못 찾는다"보다 "마지막 몇 cm를 더 정확히 제어해야 한다"에 가깝다.
- EN: So the current bottleneck is closer to final-centimeter control than to camera target recognition.

- KR: 데모 순서는 `4, 7, 8, 5, 9, 3, 6, 1, 2, 8, 3, 6`으로 바뀐다. 같은 목표만 반복하는 데모 설정 문제는 수정됐다.
- EN: The demo sequence changes through `4, 7, 8, 5, 9, 3, 6, 1, 2, 8, 3, 6`. The demo setup no longer keeps one stale target observation.

## Evidence / 근거 자료

- Report / 리포트: [experiment report](../../experiments/20260610_132926_three_camera_target_tracking_128env_1500iter_three_camera_target_tracking_1cm_stage1_1500iter.md)
- Plot / 그래프: [region mastery counts](../../logs/plots/20260610_132926_three_camera_target_tracking_128env_1500iter_three_camera_target_tracking_1cm_stage1_1500iter/mt4_coordinate_region_mastery_counts.png)
- Training video / 학습 영상: [1 minute clip](../videos/20260610_140823_train_three_camera_target_tracking_1cm_stage1_1500iter_2026-06-10_13-29-26_three_camera_target_tracking_128env_1500iter.mp4)
- Demo video / 데모 영상: [1 minute random-region demo](../videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min.mp4)
- Demo sequence / 데모 순서: [sequence CSV](../videos/20260610_141000_demo_three_camera_target_tracking_1cm_random_regions_1min_sequence.csv)

## Next Step / 다음 단계

- KR: 다음 병목은 카메라가 아니라 마지막 1cm 정밀 제어다. 다음 학습은 속도를 낮추는 마지막 접근 단계 또는 목표 근처에서 멈추는 보상을 분리해서 확인한다.
- EN: The next bottleneck is final 1 cm precision, not camera recognition. The next run should test either a slower final-approach phase or a separate stop-near-target reward.
