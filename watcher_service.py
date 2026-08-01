"""watcher_service.py — standalone $0 watcher for the agent_bridge stall problem.

Why: engine LLM calls (pipeline/agent_bridge.py) write a request file then BLOCK,
polling for a reply, up to AGENT_BRIDGE_TIMEOUT (default 3600s). If nobody is
actively servicing the requests dir, a run just sits there silently for up to an
hour, then dies. Confirmed real orphaned request: requests/0001_300107.request.md
sat 6 days with no reply.

What this does: runs forever as its own process (independent of any chat session),
polls .agent_bridge/requests/ every WATCHER_POLL_SEC, ages the oldest unanswered
request into ok -> pending -> stalled -> abandoned, and writes ONE small status
file (data/.watcher_status.json) for cost_status.py's statusline chip to read.
It does not (and cannot) fabricate a real reply -- v1 scope is detect + surface,
not auto-answer.

Also toggles Windows "stay awake" (SetThreadExecutionState) on only while a
request is actively pending/stalled -- not for the whole time this process runs,
so normal power-saving sleep still works when nothing is happening.

Start it: start_watcher.bat (pythonw, no console window). Stop it: End Task on
"pythonw.exe" in Task Manager, or delete data/.watcher.pid and it exits next poll...
no -- simplest is Task Manager; a pidfile only guards against double-start.

Knobs (env, mirrors AGENT_BRIDGE_* convention):
  WATCHER_POLL_SEC       10     seconds between scans
  WATCHER_PENDING_SEC    30     age at which a wait becomes worth a quiet chip
  WATCHER_STALLED_SEC    300    age at which it becomes a loud "needs you" chip
  WATCHER_ABANDONED_SEC  3600   mirrors AGENT_BRIDGE_TIMEOUT -- past this the
                                 engine has already given up and crashed
  WATCHER_KEEP_AWAKE     1      set 0 to disable the keep-awake behavior
  AGENT_BRIDGE_DIR       <repo>/.agent_bridge   (shared with pipeline/agent_bridge.py)
"""
from __future__ import annotations

import ctypes
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRIDGE_DIR = Path(os.environ.get("AGENT_BRIDGE_DIR") or (ROOT / ".agent_bridge"))
REQ_DIR = BRIDGE_DIR / "requests"
RESP_DIR = BRIDGE_DIR / "responses"
ARCHIVE_DIR = BRIDGE_DIR / "archive"

STATUS_PATH = ROOT / "data" / ".watcher_status.json"
PID_PATH = ROOT / "data" / ".watcher.pid"

POLL_SEC = float(os.environ.get("WATCHER_POLL_SEC", "10"))
PENDING_SEC = float(os.environ.get("WATCHER_PENDING_SEC", "30"))
STALLED_SEC = float(os.environ.get("WATCHER_STALLED_SEC", "300"))
ABANDONED_SEC = float(os.environ.get("WATCHER_ABANDONED_SEC", "3600"))
KEEP_AWAKE = os.environ.get("WATCHER_KEEP_AWAKE", "1") not in ("0", "false", "False")

NO_WIN = 0x08000000 if os.name == "nt" else 0
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

_HEADER_RE = re.compile(r"—\s*(.+?)\s*\(([^)]+)\)\s*$")

_awake = False


def _set_awake(on: bool) -> None:
    """Keep Windows from sleeping only while a request is actively pending/stalled
    (not the whole time this process runs -- that would defeat power saving)."""
    global _awake
    if os.name != "nt" or not KEEP_AWAKE or on == _awake:
        return
    flags = ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0)
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(flags)
        _awake = on
    except Exception:
        pass


def _label(req_path: Path) -> str:
    """Pull the human label off the request's own header line, e.g.
    '# AGENT-BRIDGE REQUEST 0001_300107 — text (thread-discovery)' -> 'text (thread-discovery)'.
    Bounded read (the header is always near the top) so this stays cheap even on
    the ~33KB requests seen in this repo."""
    try:
        with req_path.open(encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                if line.startswith("# AGENT-BRIDGE REQUEST"):
                    m = _HEADER_RE.search(line.strip())
                    return f"{m.group(1)} ({m.group(2)})" if m else line.strip().lstrip("# ")
    except OSError:
        pass
    return req_path.stem


def scan() -> dict:
    """Unanswered = a request file with no matching response AND not yet archived
    (archive/ holds fully-serviced pairs -- see pipeline/agent_bridge.py _archive)."""
    now = time.time()
    pending = []
    if REQ_DIR.exists():
        for rq in REQ_DIR.glob("*.request.md"):
            base = rq.name[: -len(".request.md")]
            if (RESP_DIR / f"{base}.txt").exists():
                continue
            if (ARCHIVE_DIR / rq.name).exists():
                continue
            try:
                age = now - rq.stat().st_mtime
            except OSError:
                continue
            pending.append((age, base, rq))

    if not pending:
        return {"updated_ts": now, "state": "ok", "count": 0}

    pending.sort(key=lambda t: -t[0])  # oldest (largest age) first
    age, base, rq = pending[0]
    if age < PENDING_SEC:
        state = "ok"
    elif age < STALLED_SEC:
        state = "pending"
    elif age < ABANDONED_SEC:
        state = "stalled"
    else:
        state = "abandoned"

    return {
        "updated_ts": now,
        "state": state,
        "count": len(pending),
        "oldest_id": base,
        "oldest_age_sec": round(age),
        "oldest_label": _label(rq),
    }


def _write_status(status: dict) -> None:
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATUS_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(status), encoding="utf-8")
    tmp.replace(STATUS_PATH)  # atomic swap so the statusline never reads a half-written file


def _pid_alive(pid: int) -> bool:
    if os.name != "nt":
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    try:
        out = subprocess.run(
            ["tasklist", "/fi", f"PID eq {pid}", "/fo", "csv"],
            capture_output=True, text=True, timeout=5, creationflags=NO_WIN,
        )
        return str(pid) in out.stdout
    except Exception:
        return True  # fail open: assume alive rather than risk two watchers fighting over keep-awake


def _claim_singleton() -> bool:
    PID_PATH.parent.mkdir(parents=True, exist_ok=True)
    if PID_PATH.exists():
        try:
            old_pid = int(PID_PATH.read_text().strip())
        except Exception:
            old_pid = None
        if old_pid and old_pid != os.getpid() and _pid_alive(old_pid):
            return False
    PID_PATH.write_text(str(os.getpid()), encoding="utf-8")
    return True


def _release_singleton() -> None:
    try:
        if PID_PATH.exists() and PID_PATH.read_text().strip() == str(os.getpid()):
            PID_PATH.unlink()
    except Exception:
        pass


def main() -> int:
    if not _claim_singleton():
        print("watcher_service: already running, exiting.", flush=True)
        return 0
    print(f"watcher_service: watching {REQ_DIR}", flush=True)
    try:
        while True:
            status = scan()
            _write_status(status)
            _set_awake(status["state"] in ("pending", "stalled"))
            time.sleep(POLL_SEC)
    except KeyboardInterrupt:
        pass
    finally:
        _set_awake(False)
        _release_singleton()
    return 0


if __name__ == "__main__":
    sys.exit(main())
