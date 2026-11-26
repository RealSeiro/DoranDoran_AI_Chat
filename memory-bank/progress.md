# progress — 되는 것, 남은 것, 알려진 문제 (요약만)

## 되는 것
- **서버**: 기능명세서의 서버 쪽 기능 구현 (자유 대화, 대화 기록·보관기간, 하루 1번 알림, 기억 저장·조회·삭제,
  퀴즈 문제은행·판정, 놀이 세션·기록, 계정 연결, 일상 요약, 공유 동의, 탈퇴). 기능 ↔ 코드 표는 `server/README.md`.
- **검증**: `check_ai.py` 5개, `demo.py` 43개 확인 통과 (2026-11-26 확인)
- **AI**: 규칙 기반 가짜 AI(`server/ai/fake.py`)로 서버 전체가 끝까지 돈다.

## 남은 것
- `android/`: 저장소에 아직 없음 (강현준)
- 진짜 AI: `server/ai/llm.py`에 `respond`, `summarize_day` 구현 → `check_ai.py ai.llm` 통과 → `ai/__init__.py` import 교체 (곽민석)
- `docs/`: 저장소에 아직 없음 (박민경)
- 퀴즈 30문제 팀 검수 → `verified = true` → `QUIZ_ONLY_VERIFIED=1`
- `TURN_RETENTION_DAYS`(대화 원문 보관 기간) 팀 확정
- 실제 푸시: Firebase 서비스 계정 키 설정 (키 파일은 커밋 금지)

## 알려진 문제
- (아직 없음)
