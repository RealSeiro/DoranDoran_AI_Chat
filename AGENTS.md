# AGENTS.md — AI(Claude Code·Codex)가 이 저장소에서 일하는 방법

이 파일은 Codex가 자동으로 읽고, Claude Code는 `CLAUDE.md`를 통해 읽는다.
팀원 누구의 AI든 같은 방식으로 일해서, 다음 사람이 끊김 없이 이어받게 하는 것이 목표다.

## 이 프로젝트

PACCA: 어르신이 AI 친구와 음성으로 대화하면, AI가 대화에서 기억을 남기고 그 기억으로 회상 놀이·퀴즈를 하는 서비스.
어르신이 동의한 범위에서만 보호자에게 일상 요약과 놀이 참여 현황을 보여 준다.
자세한 내용은 `memory-bank/`에 있다.

## 작업 순서

### 1. 시작할 때
1. `git pull`로 최신 상태를 받는다. (`main`이 아니면 `main`을 반영했는지 확인)
2. `memory-bank/`의 파일을 이 순서로 읽는다:
   `projectbrief.md` → `productContext.md` → `systemPatterns.md` → `techContext.md` → `progress.md` → `activeContext.md`
3. 사용자가 시킨 일이 기억과 어긋나면 (이미 결정된 것을 뒤집음, 다른 사람 담당 부분을 건드림) 시작 전에 사용자에게 먼저 말한다.
4. 기준 계획은 과제 계획서 3차본이고, 그 내용이 memory-bank에 들어 있다. 시킨 일이 계획서와 어긋나면
   (예: 보호자에게 원문 보여 주기, 공유 기본값을 '공유'로, 알림 반복, 의학적 판단) 시작 전에 사용자에게 먼저 말한다.

### 2. 작업할 때
- **담당 폴더를 지킨다.** `android/` 강현준, `server/` 김도현, `server/ai/` 곽민석, `docs/` 박민경.
  다른 사람 폴더를 고쳐야 하면 사용자에게 먼저 알리고, 그 내용을 PR 설명에 적는다.
- **연결 약속은 함부로 바꾸지 않는다.** 앱↔서버는 API(`server/app/schemas.py`), 서버↔AI는 `server/ai/contract.py`.
  바꿔야 하면 사용자에게 먼저 말하고, 바꾼 뒤 `memory-bank/systemPatterns.md`의 결정 기록에 남긴다.
- 서버 규칙(LLM에 맡기지 않고 코드로 정하는 것)은 `server/app/rules.py`에 둔다. 규칙을 AI 프롬프트로 옮기지 않는다.
- 새 기능에는 확인을 같이 만든다:
  서버 흐름이면 `server/scripts/demo.py`에 `check(...)`를 추가하고, AI 모듈 약속이면 `server/scripts/check_ai.py`에 추가한다.
- 비밀값(`.env`, API 키, Firebase 키 파일, 비밀번호)은 절대 커밋하지 않고, 코드·문서에 적지도 않는다.

### 3. 끝내기 전에: 스스로 검증
1. `python scripts/ai_verify.py`를 실행한다. 바뀐 폴더에 맞는 검사를 돌린다:
   - `server/`: 파이썬 문법 → `check_ai.py` (DB 불필요) → `demo.py` (DB가 켜져 있으면, 43개 이상 확인)
   - `android/`: `gradlew assembleDebug` (`android/gradlew`가 있으면)
2. 실패하면 **코드를 고친다.** 검사를 지우거나 느슨하게 바꿔서 통과시키지 않는다.
   검사 자체가 틀렸다고 판단되면 고치지 말고 사용자에게 이유를 설명한다.
3. 건너뛴 검사가 있으면 (예: DB가 꺼져서 `demo.py`를 못 돌림) 사용자에게 그렇다고 말한다. "다 통과"라고 하지 않는다.
4. Claude Code에서는 이 검증이 끝낼 때 자동으로 한 번 더 돈다 (`.claude/settings.json`의 Stop 훅).
   실패하면 끝나지 않고 실패 내용이 다시 전달된다. 3번 연속 실패하면 멈추고 사람에게 넘긴다.
   Codex에는 자동 훅이 없으니 위 1~3을 반드시 직접 한다.

### 4. 마지막으로: 기억 업데이트
- `memory-bank/activeContext.md`: **이 작업을 한 사람의 칸만** 고친다 (지금 하는 일, 다음 할 일, 막힌 것). 다른 사람 칸은 건드리지 않는다.
- `memory-bank/progress.md`: 기능이 새로 되거나, 남은 일·알려진 문제가 생기거나 없어졌을 때만 고친다.
- `memory-bank/systemPatterns.md`: 구조나 약속에 관한 결정을 했으면 "결정 기록" **맨 아래에 한 줄 추가**한다 (날짜 · 누가 · 무엇을 · 왜). 예전 줄은 고치지 않는다.
- 그대로인 내용은 다시 쓰지 않는다. 기억 파일은 짧게 유지한다 (누적 일지가 아니라 지금 상태).
- 커밋은 `main`이 아닌 브랜치에 하고, PR로 올린다 (README의 "함께 작업하는 방법").
