"""One CLI panel at a time across lanes. Usage (wrap any panel run):
  .venv\\Scripts\\python.exe _roadmap\\pipelines\\panel_lock.py run P1 -- <command ...>
Waits (polling every 30 s, up to 3 h) until no other lane holds the lock, runs the command, always releases.
`status` shows the holder. The lock is a folder (mkdir is atomic). A lock older than 3 h is treated as stale."""
import subprocess, sys, time
from pathlib import Path

LOCK = Path(__file__).with_name(".panel_lock")
STALE = 3 * 3600


def holder():
    f = LOCK / "holder.txt"
    return f.read_text(encoding="utf-8").strip() if f.exists() else "?"


def acquire(lane):
    start = time.time()
    while True:
        try:
            LOCK.mkdir()
            (LOCK / "holder.txt").write_text(f"{lane} {time.strftime('%Y-%m-%d %H:%M:%S')}", encoding="utf-8")
            return
        except FileExistsError:
            if time.time() - LOCK.stat().st_mtime > STALE:
                print(f"[panel_lock] stale lock ({holder()}) removed", flush=True)
                release()
                continue
            if time.time() - start > STALE:
                sys.exit(f"[panel_lock] gave up after 3 h; held by {holder()}")
            print(f"[panel_lock] {lane} waiting; held by {holder()}", flush=True)
            time.sleep(30)


def release():
    for f in LOCK.glob("*"):
        f.unlink()
    LOCK.rmdir()


if __name__ == "__main__":
    if sys.argv[1:2] == ["status"]:
        print(holder() if LOCK.exists() else "free")
    elif sys.argv[1:2] == ["run"] and "--" in sys.argv:
        lane, cmd = sys.argv[2], sys.argv[sys.argv.index("--") + 1:]
        if Path(cmd[0]).exists():
            cmd[0] = str(Path(cmd[0]).resolve())  # Windows CreateProcess needs a full path for a relative exe
        acquire(lane)
        try:
            sys.exit(subprocess.call(cmd))
        finally:
            release()
    else:
        sys.exit(__doc__)
