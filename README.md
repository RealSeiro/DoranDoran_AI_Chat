# PACCA AI Service

**Personalized AI Conversation and Cognitive Activity Service for Older Adults**
고령자를 위한 개인화 AI 대화·인지 놀이 서비스 (AI P-실무프로젝트)

어르신이 AI 친구와 음성으로 대화하면, AI가 대화에서 관심사와 경험을 기억하고 그 기억으로 회상 놀이와 관심사 퀴즈를 이어 갑니다. 어르신이 동의한 범위에서만 보호자에게 일상 요약과 놀이 참여 현황을 보여 줍니다.

## 폴더 구성

| 폴더 | 담당 | 내용 |
|---|---|---|
| `android/` | 강현준 | Android 앱 (어르신 모드·보호자 모드, STT·TTS, 서버 API 연동) |
| `server/` | 김도현 | FastAPI 서버 + PostgreSQL (API, 인증·권한, 시스템 규칙, 스케줄러) |
| `server/ai/` | 곽민석 | AI 모듈. 서버와 주고받는 입출력 형식은 `server/ai/contract.py`에 정해져 있음 |
| `docs/` | 박민경 | 계획서, 기능명세서, 보고서, 발표자료 |

각자 자기 폴더에서 작업하면 서로의 작업과 충돌하지 않습니다. 앱과 서버는 API로, 서버와 AI 모듈은 `contract.py`의 형식으로만 연결됩니다.

## 서버 실행

`server/README.md`를 참고하세요. (`cd server` 후 실행)

## 함께 작업하는 방법

1. `main`에서 새 브랜치를 만든다: `git checkout -b 기능이름` (예: `android-chat-screen`, `ai-respond`)
2. 작업을 커밋하고 브랜치를 올린다: `git push -u origin 기능이름`
3. GitHub에서 Pull Request를 열고, 필요하면 팀원에게 확인을 부탁한 뒤 Merge한다.

- 비밀번호, API 키, `.env`, Firebase 키 파일은 절대 올리지 않습니다. (`.gitignore`에 등록돼 있음)
- 다른 사람 폴더를 고쳐야 하면 그 사람에게 먼저 말하고 PR로 올립니다.

## AI(Claude Code·Codex)와 함께 작업하기

방향은 각자 정하고, AI에게 하던 대로 일을 시키면 됩니다. AI는 `AGENTS.md`를 읽고 두 가지만 합니다.

1. **기억**: 시작할 때 `memory-bank/`를 읽어 앞사람이 한 일을 이어받고, 끝날 때 내 칸(`activeContext.md`)에 지금 상태를 **반드시** 남깁니다. 코드를 바꾸고 기억을 안 남기면 Claude Code가 끝나지 않습니다. 이것까지 같이 커밋해서 PR로 올려 주세요.
2. **검증**: 끝내기 전에 `python scripts/ai_verify.py`로 코드가 돌아가는지 확인합니다. Claude Code는 끝낼 때 자동으로 검사하고, 실패하면 끝나지 않고 고칩니다.
   - 서버 검사를 제대로 하려면 `server/.venv`에 패키지를 설치하고(`server/README.md`), DB를 켜 두세요(`docker compose up -d`). DB가 꺼져 있으면 `demo.py`는 건너뜁니다.
   - 훅은 `python` 명령으로 실행됩니다. Mac에서 `python`이 없으면 가상환경을 켠 뒤 Claude Code를 실행하세요.
   - Codex는 자동 검사가 없으니, 끝나기 전에 AI가 직접 돌리는지 봐 주세요.

| 파일 | 내용 |
|---|---|
| `memory-bank/projectbrief.md` | 무엇을, 왜 만드나 · 목표·정량 목표 · 담당 (계획서 3차본 기준) |
| `memory-bank/productContext.md` | 사용자 흐름(화면 1~15), 꼭 지킬 경험, 앱 예외 처리 |
| `memory-bank/systemPatterns.md` | 구조, 설계 원칙, 데이터 흐름·보관, 서버 예외 처리, **결정 기록** |
| `memory-bank/techContext.md` | 기술 스택, 설정값, 검증 도구 |
| `memory-bank/progress.md` | 되는 것, 남은 것, 알려진 문제 |
| `memory-bank/activeContext.md` | 사람별 지금 상태 |
