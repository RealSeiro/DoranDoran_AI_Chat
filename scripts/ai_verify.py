"""AI(Claude Code·Codex)가 작업을 끝내기 전에 스스로 돌리는 검증.

사람이 직접 돌릴 때:   python scripts/ai_verify.py          (바뀐 폴더만 검사)
                       python scripts/ai_verify.py --all    (전부 검사)
Claude Code가 부를 때: python scripts/ai_verify.py --hook   (.claude/settings.json의 Stop 훅)

검사 내용 (바뀐 폴더에 따라):
  server/   ① 파이썬 문법  ② AI 약속 검사 scripts/check_ai.py (DB 불필요)
            ③ 처음부터 끝까지 시연 scripts/demo.py (DB가 켜져 있을 때만)
  android/  gradlew assembleDebug (android/gradlew가 있을 때만)
  docs/ 등  검사 없음

--hook 모드: 실패하면 exit 2 → Claude Code가 끝내지 못하고 실패 내용을 보고 고친다.
             같은 세션에서 3번 연속 실패하면 멈추고 사람에게 넘긴다 (무한 반복 방지).
표준 라이브러리만 쓴다 (가상환경이 꺼져 있어도 이 파일은 돈다).
"""
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "server"
ANDROID = ROOT / "android"
STATE = ROOT / ".claude" / ".verify-state.json"
MAX_TRIES = 3
TAIL = 60  # 실패했을 때 보여 줄 마지막 줄 수

if hasattr(sys.stdout, "reconfigure"):          # Windows 콘솔에서 한글·기호 깨짐 방지
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def sh(cmd, cwd, timeout=600):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, f"{timeout}초 안에 안 끝남"
    except FileNotFoundError as e:
        return 127, str(e)
    out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
    return p.returncode, out


def git_changed():
    """커밋 안 한 변경 + 아직 push 안 한 커밋에 들어 있는 파일들"""
    files = set()
    code, out = sh(["git", "status", "--porcelain"], ROOT, 30)
    if code == 0:
        files |= {line[3:].strip().strip('"').split(" -> ")[-1] for line in out.splitlines() if line.strip()}
    code, out = sh(["git", "diff", "--name-only", "@{u}...HEAD"], ROOT, 30)
    if code == 0:
        files |= {line.strip() for line in out.splitlines() if line.strip()}
    return files


def server_python():
    """server/.venv가 있으면 그 파이썬, 없으면 지금 파이썬"""
    for p in (SERVER / ".venv" / "Scripts" / "python.exe", SERVER / ".venv" / "bin" / "python"):
        if p.exists():
            return str(p)
    return sys.executable


def db_is_up():
    try:
        with socket.create_connection(("localhost", 5432), timeout=1):
            return True
    except OSError:
        return False


def check_server(results, notes):
    py = server_python()
    code, out = sh([py, "-c", "import fastapi, pydantic, sqlalchemy"], SERVER, 60)
    if code != 0:
        notes.append("server 검사 못 함: 가상환경에 패키지가 없음 (server/README.md의 '처음 실행' 참고)")
        return
    results.append(("server 파이썬 문법", *sh([py, "-m", "compileall", "-q", "app", "ai", "scripts"], SERVER)))
    results.append(("server AI 약속 (check_ai.py)", *sh([py, "scripts/check_ai.py"], SERVER)))
    if db_is_up():
        results.append(("server 전체 시연 (demo.py)", *sh([py, "scripts/demo.py"], SERVER)))
    else:
        notes.append("DB가 꺼져 있어 demo.py는 건너뜀 (server에서 docker compose up -d 하면 같이 검사됨)")


def check_android(results, notes):
    win = os.name == "nt"
    gradlew = ANDROID / ("gradlew.bat" if win else "gradlew")
    if not gradlew.exists():
        notes.append("android/gradlew가 없어 앱 빌드 검사는 건너뜀")
        return
    results.append(("android 빌드 (assembleDebug)", *sh([str(gradlew), "assembleDebug", "-q"], ANDROID, 900)))


def run(all_areas):
    changed = None if all_areas else git_changed()
    touched = lambda area: changed is None or any(f.startswith(area + "/") for f in changed)  # noqa: E731
    results, notes = [], []
    if changed is not None and not changed:
        return results, notes, False
    if touched("server"):
        check_server(results, notes)
    if touched("android"):
        check_android(results, notes)
    if changed is not None and any(f.startswith("server/schema.sql") for f in changed):
        notes.append("schema.sql이 바뀜: 내 DB에 반영하려면 server에서 docker compose down -v 후 up -d (데이터 지워짐)")
    return results, notes, True


def report(results, notes):
    lines = []
    for name, code, _ in results:
        lines.append(f"  {'통과' if code == 0 else '실패'}  {name}")
    for n in notes:
        lines.append(f"  참고  {n}")
    return "\n".join(lines)


def failures_text(results):
    parts = []
    for name, code, out in results:
        if code != 0:
            tail = "\n".join(out.strip().splitlines()[-TAIL:])
            parts.append(f"■ 실패: {name}\n{tail}")
    return "\n\n".join(parts)


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(state):
    try:
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass


def hook_mode():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    sid = data.get("session_id", "unknown")
    results, notes, ran = run(all_areas=False)
    state = load_state()
    failed = [r for r in results if r[1] != 0]

    if not failed:
        state.pop(sid, None)
        save_state(state)
        if ran and (results or notes):
            print(json.dumps({"systemMessage": "자동 검증\n" + report(results, notes)}, ensure_ascii=False))
        sys.exit(0)

    tries = state.get(sid, 0) + 1
    state[sid] = tries
    save_state(state)
    if tries > MAX_TRIES:
        state.pop(sid, None)
        save_state(state)
        print(json.dumps({"systemMessage": f"자동 검증이 {MAX_TRIES}번 연속 실패해서 멈춤. 사람이 확인해 주세요.\n"
                          + report(results, notes)}, ensure_ascii=False))
        sys.exit(0)

    print(f"자동 검증 실패 ({tries}/{MAX_TRIES}). 아직 작업을 끝내지 말고 원인을 고친 뒤 다시 끝내세요.\n"
          "- 검사(테스트·demo.py·check_ai.py)를 고쳐서 통과시키지 말고, 코드를 고치세요.\n"
          "- 검사 자체가 틀렸다고 판단되면 고치지 말고 사용자에게 이유를 설명하세요.\n\n"
          + report(results, notes) + "\n\n" + failures_text(results), file=sys.stderr)
    sys.exit(2)


def main():
    if "--hook" in sys.argv:
        hook_mode()
    results, notes, ran = run(all_areas="--all" in sys.argv)
    if not ran:
        print("바뀐 파일이 없어 검사할 것이 없음 (전부 검사: --all)")
        sys.exit(0)
    print(report(results, notes) or "  검사할 것이 없음 (docs 등 검사 없는 폴더만 바뀜)")
    failed = failures_text(results)
    if failed:
        print("\n" + failed)
    print("\n모두 통과" if not failed else "\n실패한 검사가 있음")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
