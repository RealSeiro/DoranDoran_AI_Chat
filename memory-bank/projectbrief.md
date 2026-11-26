# projectbrief — 무엇을, 왜 만드나 (거의 안 바뀜)

**PACCA AI Service**: Personalized AI Conversation and Cognitive Activity Service for Older Adults
고령자를 위한 개인화 AI 대화·인지 놀이 서비스 (AI P-실무프로젝트)

## 목표
- 어르신이 AI 친구와 **음성으로 자유 대화**한다.
- AI가 대화에서 관심사·경험을 **기억**하고, 그 기억으로 **회상 놀이(RECALL)**와 **관심사 퀴즈(QUIZ)**를 이어 간다.
- 어르신이 **동의한 범위에서만** 보호자에게 일상 요약과 놀이 참여 현황을 보여 준다.

## 범위를 정하는 원칙
- 기억은 어르신이 **실제로 한 말에 근거**해야만 저장한다 (허위 기억 방지).
- 규칙(퀴즈 정답 판정, 일상 질문 하루 1번, 공유 동의 등)은 LLM이 아니라 **서버 코드**가 정한다.
- 보호자는 연결(관문 1)과 동의(관문 2)를 모두 지나야 볼 수 있다.

## 팀과 담당
| 폴더 | 담당 | 내용 |
|---|---|---|
| `android/` | 강현준 | Android 앱 (어르신 모드·보호자 모드, STT·TTS, 서버 API 연동) |
| `server/` | 김도현 | FastAPI 서버 + PostgreSQL (API, 인증·권한, 시스템 규칙, 스케줄러) |
| `server/ai/` | 곽민석 | AI 모듈 (서버와의 약속: `server/ai/contract.py`) |
| `docs/` | 박민경 | 계획서, 기능명세서, 보고서, 발표자료 |
