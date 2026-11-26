# AGENTS.md — AI(Claude Code·Codex)가 이 저장소에서 일하는 방법

방향은 각 팀원이 정한다. AI는 그 사람이 시키는 대로 일하고, 두 가지만 한다:
**① 일한 내용을 기억으로 남겨서 다음 사람이 이어받게 하고, ② 끝내기 전에 코드가 돌아가는지 검증한다.**

## 시작할 때
`memory-bank/`를 읽고 프로젝트와 지금까지의 맥락을 파악한다.
`projectbrief.md`(무엇을, 왜) · `productContext.md`(사용자 흐름) · `systemPatterns.md`(구조, 결정 기록) ·
`techContext.md`(기술, 실행 방법) · `progress.md`(되는 것, 남은 것) · `activeContext.md`(사람별 지금 상태)

## 끝내기 전에: 검증 (반드시)
1. `python scripts/ai_verify.py`를 실행한다. 바뀐 폴더에 맞는 검사가 돈다:
   - `server/`: 파이썬 문법 → `check_ai.py` (AI 모듈 약속) → `demo.py` (DB가 켜져 있으면, 전체 흐름 43개 확인)
   - `android/`: `gradlew assembleDebug` (`android/gradlew`가 있으면)
2. 실패하면 코드를 고친다. 검사를 지우거나 느슨하게 바꿔서 통과시키지 않는다.
   검사 자체가 틀렸다고 판단되면 고치지 말고 사용자에게 이유를 설명한다.
3. 건너뛴 검사가 있으면 (예: DB가 꺼져서 `demo.py`를 못 돌림) 사용자에게 그렇다고 말한다.
4. 새 기능을 만들었으면 그 기능을 확인하는 검사도 같이 만든다
   (서버 흐름은 `server/scripts/demo.py`, AI 모듈은 `server/scripts/check_ai.py`).

Claude Code에서는 끝낼 때 이 검증이 자동으로 돌고, 실패하면 끝나지 않는다 (`.claude/settings.json`의 Stop 훅,
3번 연속 실패하면 멈추고 사람에게 넘김). 코드·문서를 바꿨는데 `activeContext.md`를 안 고쳤어도 같은 방식으로 막힌다.
Codex에는 자동 훅이 없으니 검증과 기억 남기기를 직접 한다 (`ai_verify.py`가 기억이 빠졌는지도 알려 줌).

## 마지막으로: 기억 남기기 (반드시)
- `activeContext.md`: 일한 사람의 칸에 지금 하는 일, 다음에 하려는 일, 막힌 것을 적는다. 누구인지 모르면 사용자에게 묻는다.
  그 사람이 정한 방향을 적는다. AI가 다음 할 일을 정해서 적지 않는다.
- `systemPatterns.md`: 구조나 약속(API, `server/ai/contract.py`)을 바꿨으면 "결정 기록" 맨 아래에 한 줄 추가한다 (날짜 · 누가 · 무엇을 · 왜).
- `progress.md`: 새로 된 것, 새로 생긴 남은 일·문제가 있으면 고친다.
- 지금 상태만 짧게 적는다. 그대로인 내용은 다시 쓰지 않는다.

## 하나 더
비밀값(`.env`, API 키, Firebase 키 파일, 비밀번호)은 커밋하지 않고, 코드·문서·기억에도 적지 않는다.
