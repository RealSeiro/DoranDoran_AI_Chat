# systemPatterns — 구조와 결정

## 전체 구조
```
[Android 앱]  ──HTTP API (Bearer 토큰)──▶  [FastAPI 서버]  ──함수 호출──▶  [AI 모듈 server/ai/]
 어르신 모드                                  │  app/service.py 대화 엔진        respond()
 보호자 모드                                  │  app/rules.py   서버 규칙        summarize_day()
                                              ▼
                                        [PostgreSQL]  테이블 16개 (server/schema.sql)
```
- 앱은 서버하고만 통신한다. 응답 모양은 `server/app/schemas.py`.
- 서버와 AI는 `server/ai/contract.py`의 입출력 모양으로만 연결된다. AI를 바꿀 때는 `server/ai/__init__.py`의 import 한 줄만 바꾼다.

## 대화 한 번이 처리되는 순서 (`app/service.py`)
어르신 말 저장 → (퀴즈 중이면) 서버가 정답 판정 → 맥락(기억·일상·놀이) 모으기 → AI 호출 → AI가 낸 후보 검사 후 저장

## 역할 나누기 (LLM vs 서버 규칙)
- **AI**: 말 만들기, 기억 후보·일상 정보 후보 찾기 (항상 근거 `evidence` 첨부), 놀이 제안·시작·끝 판단, 요약 문장 쓰기
- **서버**: 후보 저장 여부 결정 (`rules.evidence_ok`), 일상 질문 하루 1번 제한, 퀴즈 문제 고르기·정답 판정 (`rules.judge_quiz`), 놀이 기록, 공유 동의, 알림
- AI가 규칙을 어기면: 다시 요청(`rule_reminder`) → 그래도 어기면 서버가 문장을 바꿈. AI 호출이 실패하면 서버가 직접 진행.

## 보호자 화면 권한
모든 보호자 조회는 관문 1(계정 연결, `links`) → 관문 2(항목별 동의, `consents`)를 지난다 (`app/auth.py`).

## 결정 기록 (맨 아래에 추가만. 날짜 · 누가 · 무엇을 · 왜)
- 2026-11-26 · 김도현 · AI 협업용 기억(`memory-bank/`)과 자동 검증(`scripts/ai_verify.py`, Claude Code Stop 훅)을 추가 · 팀원 AI가 이어서 작업해도 맥락이 안 끊기고, 망가뜨린 코드가 그대로 올라가지 않게
