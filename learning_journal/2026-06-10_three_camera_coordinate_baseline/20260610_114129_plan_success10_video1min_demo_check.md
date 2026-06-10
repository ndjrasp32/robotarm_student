# 2026-06-10 Success 10 and 1-Minute Video Plan / 성공 10회와 1분 영상 계획

## Summary / 요약

- KR: 다음 학습부터는 한 영역을 5번이 아니라 10번 성공해야 다음 영역으로 넘어간다.
- EN: From the next training run, one region must succeed 10 times, not 5 times, before moving to the next region.

- KR: 학습 영상과 데모 영상은 기본 길이를 약 1분으로 맞춘다.
- EN: Training and demo videos now default to about 1 minute.

## Question / 질문

- KR: 세 카메라 덕분에 너무 빨리 성공 처리되는 경우가 있으니, 더 좋은 결과를 고르려면 성공 횟수를 늘리는 것이 맞는가?
- EN: Since three cameras can make a region pass quickly, should we require more successes to select a better result?

## Decision / 결정

- KR: 맞다. 10회 기준은 학습을 조금 더 오래 붙잡지만, 운 좋게 한두 번 성공한 결과를 기준선으로 고르는 위험을 줄인다.
- EN: Yes. The 10-success rule may hold a region longer, but it reduces the chance of accepting a lucky result as the baseline.

- KR: 1분 영상은 너무 길지 않으면서도 타겟이 바뀌는지, 로봇팔이 같은 곳만 가는지 확인하기에 충분하다.
- EN: A 1-minute video is short enough to review often and long enough to check whether targets change or the arm repeats one spot.

## Implementation / 구현

- KR: `region_mastery_successes`를 `10`으로 바꿨다.
- EN: Changed `region_mastery_successes` to `10`.

- KR: 학습 영상 기본 길이를 `3600` step으로 바꿨다. 이 태스크에서는 대략 60초다.
- EN: Changed the default training video length to `3600` steps, which is about 60 seconds in this task.

- KR: 데모 영상 기본 길이도 `3600` step으로 바꾸고, 5초마다 다른 영역 목표를 보여주도록 했다.
- EN: Changed the default demo length to `3600` steps and set the demo to show a different region target every 5 seconds.

## Demo Check / 데모 확인

- KR: 랜덤 데모를 만들 때 영상 파일과 `_sequence.csv` 파일을 함께 남긴다.
- EN: Random demos keep both the video file and a matching `_sequence.csv` file.

- KR: CSV의 `region_number`가 여러 번호로 바뀌면 목표 위치가 실제로 바뀐 것이다.
- EN: If `region_number` changes across the CSV, the target position really changed.

- KR: CSV는 바뀌는데 영상에서 로봇팔이 같은 곳만 간다면, 다음 병목은 목표 생성이 아니라 정책이 목표를 따라가는 능력이다.
- EN: If the CSV changes but the arm still moves to one spot, the bottleneck is policy tracking, not target generation.

## Result / 결과

| item | value |
| --- | --- |
| checkpoint / 체크포인트 | `model_1499.pt` |
| video length / 영상 길이 | `3600` steps, about 60 seconds |
| target interval / 목표 변경 간격 | `300` steps, about 5 seconds |
| region sequence / 영역 순서 | `4, 7, 8, 5, 9, 3, 6, 1, 2, 8, 3, 6` |

- KR: CSV 기준으로 1분 동안 목표 영역은 계속 바뀌었다. 따라서 “계속 같은 곳만 찍는 느낌”이 다시 보이면, 우선 목표 생성 문제가 아니라 정책이 새 목표를 따라가지 못하는 문제로 본다.
- EN: The CSV confirms that the target region changed during the 1-minute demo. If the video still looks like the arm repeats one spot, treat it first as a policy-tracking issue, not a target-generation issue.

## Evidence / 근거 자료

- Record rule / 기록 규칙: [../RECORD_FORMAT.md](../RECORD_FORMAT.md)
- Training script / 학습 스크립트: [../../scripts/train_coordinate_stage1_three_camera_baseline_128_1500_video.sh](../../scripts/train_coordinate_stage1_three_camera_baseline_128_1500_video.sh)
- Demo recorder / 데모 기록 도구: [../../tools/record_mt4_coordinate_region_demo.py](../../tools/record_mt4_coordinate_region_demo.py)
- Demo video / 데모 영상: [20260610_114650_demo_three_camera_random_regions_1min.mp4](../videos/20260610_114650_demo_three_camera_random_regions_1min.mp4)
- Demo sequence / 데모 순서: [20260610_114650_demo_three_camera_random_regions_1min_sequence.csv](../videos/20260610_114650_demo_three_camera_random_regions_1min_sequence.csv)

## Next Step / 다음 단계

- KR: 이 설정으로 다음 Stage 1 학습을 다시 돌리고, 1분 학습 영상과 랜덤 데모 영상을 같이 확인한다.
- EN: Rerun Stage 1 with this setup, then review the 1-minute training video and random demo video together.
