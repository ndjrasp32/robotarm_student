# Record Format / 기록 양식

Use this format when adding or promoting student-facing records. / 학생용 기록을 추가하거나 승격할 때 이 양식을 사용합니다.

## File Naming / 파일명

```text
YYYYMMDD_HHMMSS_kind_topic_detail.ext
```

Recommended `kind` values / 권장 `kind` 값:

- `plan`: design decision or next training plan / 설계 결정 또는 다음 학습 계획
- `run`: training or evaluation result / 학습 또는 평가 결과
- `train`: training video / 학습 영상
- `demo`: playback or demonstration video / 재생 또는 시연 영상
- `review`: interpretation, issue review, or lesson summary / 해석, 문제 검토, 수업 요약
- `index`: mapping table or artifact index / 연결표 또는 산출물 인덱스

## Document Template / 문서 템플릿

```markdown
# YYYY-MM-DD Title / 제목

## Summary / 요약

- KR:
- EN:

## Question / 질문

- KR:
- EN:

## Decision / 결정

- KR:
- EN:

## Implementation / 구현

- KR:
- EN:

## Result / 결과

| metric | value |
| --- | ---: |

## Evidence / 근거 자료

- Record / 기록:
- Plot / 그래프:
- Video / 영상:

## Next Step / 다음 단계

- KR:
- EN:
```

## Commit-Time Checklist / 커밋 전 확인

- Student-facing records are linked from `learning_journal/README.md`. / 학생용 기록은 `learning_journal/README.md`에서 연결됩니다.
- Videos are stored under `learning_journal/videos/`. / 영상은 `learning_journal/videos/` 아래에 둡니다.
- Video filenames follow `YYYYMMDD_HHMMSS_kind_topic_detail.ext`. / 영상 파일명은 `YYYYMMDD_HHMMSS_kind_topic_detail.ext`를 따릅니다.
- Korean and English appear together for plan/result summaries. / 계획과 결과 요약에는 한글과 영어를 병기합니다.
- Source archive links still resolve. / 원자료 archive 링크가 깨지지 않습니다.

