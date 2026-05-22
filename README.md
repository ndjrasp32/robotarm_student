# robotarm_student

학생/실습용 WLKATA MT4 IsaacLab 강화학습 repo입니다.

이 저장소는 MT4 기반 reach, pregrasp, insertion curriculum과 학습 결과 기록을 수업/반복 실습 기준으로 관리합니다.
실제 기기 제어와 하드웨어 전이 판단은 별도 안전 게이트를 통과한 뒤 `robotarm_mt4` 기준과 맞춰 진행합니다.

## 오늘부터 보는 기준

- 시작 문서: `docs/CURRENT_BASELINE.md`
- 현재 목표: 학생이 따라갈 수 있는 MT4 staged curriculum과 Mars twin 기준선 정리
- 현재 우선순위: 하드웨어 안전 검증보다 강화학습을 앞세우지 않는다.
- 과거 `notes/`와 `experiments/`는 참고 archive로 둔다. 새 기준 판단은 README와 `docs/CURRENT_BASELINE.md`를 우선한다.

매일 시작할 때는 이 순서만 봅니다.

1. `docs/CURRENT_BASELINE.md`
2. `README.md`
3. `notes/`와 `experiments/`는 기준 문서에 링크된 항목만 필요할 때 확인

새 문서는 늘리지 않는 것을 기본값으로 둡니다. 실험 결과는 `experiments/`에 한 건으로 남기고, 기준이 바뀐 경우에만 `docs/CURRENT_BASELINE.md`로 승격합니다.

## 역할

- 실제 MT4 asset 기반 시뮬레이션 및 정책 학습
- joint/action mapping과 hardware transfer 전 단계의 실습 기록 관리
- staged reach/pregrasp/insertion curriculum 실험 기록 관리

## 주요 위치

- IsaacLab task: `source/mt4_reach_direct`
- 실행 스크립트: `scripts/`
- 실험 기록: `experiments/`
- 작업 노트: `notes/`
- 실제 기기 관련 자료: `hardware/`

## 문서 운영 규칙

- 새로 시작할 때는 먼저 `docs/CURRENT_BASELINE.md`를 갱신한다.
- 일회성 판단/실험 로그는 `notes/YYYYMMDD_*.md` 또는 `experiments/YYYYMMDD_*.md`에 남긴다.
- 오래된 실험 문서는 삭제하지 않고 archive로 유지한다.
- README에는 현재 기준과 진입점만 둔다.
- 오늘의 작업 기준은 README와 `docs/CURRENT_BASELINE.md` 두 파일만으로 판단한다.
