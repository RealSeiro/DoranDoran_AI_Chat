"""Claude Code를 켤 때(SessionStart 훅) AI에게 알려 줄 내용을 출력한다. 출력은 AI의 맥락에 들어간다.
- 이 컴퓨터에서 마지막으로 일한 사람 (.claude/.whoami, git에 안 올라감)
- 그 사람의 memory-bank/activeContext.md 칸
Codex에는 이 훅이 없으므로 AGENTS.md의 "0. 누구인지 먼저"를 따른다."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WHOAMI = ROOT / ".claude" / ".whoami"
ACTIVE = ROOT / "memory-bank" / "activeContext.md"
TEAM = ("박민경", "강현준", "곽민석", "김도현")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def section(name):
    try:
        text = ACTIVE.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(rf"^## {re.escape(name)}.*?(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(0).strip() if m else None


try:
    who = WHOAMI.read_text(encoding="utf-8").strip()
except OSError:
    who = ""

print("[PACCA 저장소] 작업 전에 AGENTS.md의 '0. 누구인지 먼저'를 따르세요.")
if who in TEAM:
    print(f"이 컴퓨터에서 마지막으로 일한 사람: {who}. "
          f"사용자가 이미 이름을 말하지 않았다면, 작업 전에 '{who} 님 맞으세요?'라고 확인하세요.")
    s = section(who)
    if s:
        print(f"\n{who} 님의 현재 상태 (memory-bank/activeContext.md):\n{s}")
else:
    print("이 컴퓨터에 저장된 작업자가 없습니다. 사용자가 이름을 말하지 않았다면, 작업 전에 "
          f"누구인지 물어보세요 ({' / '.join(TEAM)}).")
