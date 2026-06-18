"""v2 orchestration shim — run a stage and auto-service its mechanical bridge requests.

Currently wraps the ASSEMBLY stage (the highest-toil one). It launches `cli_assemble.py`
and runs the deterministic servicer in-process, so the only bridge request a human still
answers is the semantic JIGSAW (pin clips by meaning). Everything else — episode-fit, the
two reviews, and the clip_qc-guarded slot-verifies — is auto-answered.

Usage (run in the background so the agent can service the jigsaw in chat):
  .venv\\Scripts\\python.exe v2\\cli_v2.py assemble "<v1 short folder>" \
      --provider nbp --hero 7 --exclude 2,4,6,8,11 --replan --rebuild --no-reel

The reused engine (cli_assemble.py, pipeline/*) is unchanged — this only removes toil.
"""
from __future__ import annotations
import os
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # .../JesusInTheBible
sys.path.insert(0, str(ROOT / "v2" / "servicers"))
import assembly_servicer as S                  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] != "assemble":
        print("usage: cli_v2.py assemble \"<v1 short folder>\" [cli_assemble flags...]",
              file=sys.stderr)
        return 2
    short = argv[1]
    passthrough = argv[2:]
    short_path = Path(short) if Path(short).is_absolute() else (ROOT / short)
    log_path = ROOT / "_v2_assemble.log"

    env = dict(os.environ)
    env.setdefault("LLM_PROVIDER", "agent")
    env["PYTHONUNBUFFERED"] = "1"

    cmd = [sys.executable, "cli_assemble.py", short, *passthrough]
    print(f"[cli_v2] launching: {' '.join(cmd)}", flush=True)
    print(f"[cli_v2] log -> {log_path}", flush=True)
    with open(log_path, "w", encoding="utf-8") as logf:
        proc = subprocess.Popen(cmd, cwd=str(ROOT), env=env, stdout=logf,
                                stderr=subprocess.STDOUT)
        # Service the mechanical bridge requests while the assemble runs.
        servicer = threading.Thread(
            target=S.serve, kwargs={"short_dir": short_path, "log_path": log_path},
            daemon=True)
        servicer.start()
        rc = proc.wait()
        servicer.join(timeout=10)

    print(f"[cli_v2] cli_assemble exited rc={rc}", flush=True)
    final = short_path / "assembly" / "viral_cut.mp4"
    if final.exists():
        print(f"[cli_v2] cut -> {final}", flush=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
