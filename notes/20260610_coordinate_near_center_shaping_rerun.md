# 2026-06-10 중심 접근 보상 반영 재학습 / Near-Center Shaping Rerun

## 반영 내용 / Applied Change

성공 기준은 그대로 둔다. / The success criterion stays unchanged.

- 엄격 성공 거리: `0.030 m` / strict success radius: `0.030 m`
- 보조 보상 거리: `0.070 m` 안쪽 / auxiliary shaping radius: inside `0.070 m`
- 보조 보상은 목표 카메라 영역에 들어온 뒤에만 적용 / auxiliary reward applies only after entering the target camera region

## 의도 / Intent

8번 영역 실패는 카메라 영역 진입 자체보다 중심점까지의 마지막 수렴이 약한 문제로 본다. / The region 8 failure is treated as weak final convergence to the center, not primarily as failure to enter the camera region.

그래서 7cm 안쪽 접근을 더 자주 만들도록 보상 신호를 촘촘하게 주되, 마스터 판정은 기존 3cm 조건으로만 집계한다. / Therefore the reward signal is made denser inside 7 cm, while mastery is still counted only by the existing 3 cm condition.

## 실행 계획 / Run Plan

- Command: `TERM=xterm-256color MT4_MAX_ITERATIONS=1500 MT4_RECORD_VIDEO=1 MT4_VIDEO_LENGTH=240 MT4_VIDEO_INTERVAL=12000 scripts/train_coordinate_stage1_plane_128_1500_video.sh`
- Report: `tools/report_mt4_coordinate_curriculum.py`
- Primary metrics: `mastered_region_count`, `active_region_number`, `region_XX_success_count`, `center_3cm_rate`, `near_center_7cm_rate`

## 학생용 해석 포인트 / Student Interpretation Points

- `near_center_7cm_rate`가 오르는데 `center_3cm_rate`가 낮으면, 정책은 근처까지는 오지만 정밀 수렴이 부족한 상태다. / If `near_center_7cm_rate` rises while `center_3cm_rate` stays low, the policy reaches nearby but lacks precise convergence.
- 영역 성공 횟수가 늘면 전체 `success_rate`보다 영역별 누적표를 우선 본다. / If region success counts rise, prioritize the cumulative per-region table over the final global `success_rate`.
- 모든 영역에서 거리 기준은 동일하므로, 특정 영역 실패는 기준 완화가 아니라 접근 방향, 가시성, 관절 한계, 중심 수렴 신호로 분석한다. / Since the distance criterion is identical for all regions, a region-specific failure should be analyzed through approach direction, visibility, joint limits, and center-convergence signal rather than by relaxing the criterion.
