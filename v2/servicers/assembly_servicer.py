"""v2 deterministic assembly servicer (the toil killer).

Auto-answers the *mechanical* agent-bridge requests of an assembly run so the human
stops hand-writing them (this session I wrote ~5 per short by hand):

  - assembly-episode-fit      -> {"offtopic": []}              (auto)
  - self-review / independent -> LOCKED echoed from the deterministic pre-checks (auto,
                                 ONLY when no gate FAILs — a FAIL is left for the human)
  - slot-verify               -> PASS, but ONLY when the source clip has a passing
                                 clip_qc sidecar (fail-closed; closes the v1 bypass)
  - jigsaw (plan_edit)        -> LEFT for the agent (semantic: pin clips by meaning)

Run standalone:
  SHORT_DIR=<v1 short folder> ASM_LOG=<abs path to the assemble log> \
    .venv\\Scripts\\python.exe v2\\servicers\\assembly_servicer.py
or import serve() from cli_v2.
"""
from __future__ import annotations
import glob
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]                      # .../JesusInTheBible
sys.path.insert(0, str(HERE.parent))        # for bridge_lib
sys.path.insert(0, str(ROOT))               # for pipeline
import bridge_lib as B                       # noqa: E402
from pipeline import clip_qc                 # noqa: E402
from pipeline import coherence               # noqa: E402

REQ = ROOT / ".agent_bridge" / "requests"
RESP = ROOT / ".agent_bridge" / "responses"


def _clips_all_qcd(short_dir: Path) -> tuple[bool, list[str]]:
    """Fail-closed slot-verify guard: every scene clip in visual/nbp/ must carry a passing
    clip_qc sidecar (a real look) AND its still must be coherence-verified (INV-23/24 — the
    servicer must not auto-pass a slot whose still never cleared the body-plausibility gate).
    Coherence enforcement honours the JITB_REQUIRE_COHERENCE rollout flag (off = report only).
    Returns (ok, [names needing QC])."""
    nbp = short_dir / "visual" / "nbp"
    clips = [Path(p) for p in glob.glob(str(nbp / "*.mp4"))]
    if not clips:
        return False, ["<no clips found in visual/nbp>"]
    missing = [c.name for c in clips if not clip_qc.is_verified(c)]
    if os.getenv("JITB_REQUIRE_COHERENCE", "0") not in ("0", "false", "no"):
        for c in clips:
            png = c.with_suffix(".png")
            if not coherence.is_verified(png):
                missing.append(f"{png.name} (coherence: {coherence.verdict_reason(png)})")
    return (not missing), missing


def _write(base: str, obj) -> None:
    (RESP / f"{base}.txt").write_text(json.dumps(obj), encoding="utf-8")


def serve(short_dir: Path, log_path: Path | None = None,
          idle_limit: int = 60, poll: float = 3.0) -> None:
    """Service assembly bridge requests until the log reports DONE or idle times out."""
    short_dir = Path(short_dir)
    print(f"[v2-servicer] watching {REQ}  short={short_dir.name}", flush=True)
    slot_gate_warned = False
    idle = 0
    while True:
        if log_path and Path(log_path).exists():
            try:
                tail = Path(log_path).read_text(encoding="utf-8", errors="ignore")[-2000:]
                if "DONE — edit plan" in tail:
                    print("[v2-servicer] assembly DONE -> exit", flush=True)
                    return
            except OSError:
                pass
        worked = False
        for rq in sorted(glob.glob(str(REQ / "*.request.md"))):
            base = os.path.basename(rq)[:-len(".request.md")]
            if (RESP / f"{base}.txt").exists():
                continue
            try:
                text = Path(rq).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            kind = B.classify(text)

            if kind == "slot-verify":
                ok, missing = _clips_all_qcd(short_dir)
                if ok:
                    _write(base, {"passed": True,
                                  "note": "clip carries a passing clip_qc sidecar (real look)"})
                    print(f"[v2-servicer] slot-pass {base}", flush=True)
                    worked = True
                elif not slot_gate_warned:
                    print(f"[v2-servicer] slot-verify BLOCKED — clips need clip_qc: {missing}",
                          flush=True)
                    slot_gate_warned = True
                continue

            action, payload = B.response_for(kind, text)
            if action == "write":
                _write(base, payload)
                print(f"[v2-servicer] auto {kind} {base} -> "
                      f"{payload.get('overall', 'offtopic:[]')}", flush=True)
                worked = True
            elif kind == "jigsaw":
                print(f"[v2-servicer] >>> JIGSAW {base} needs the agent (pin clips by meaning)",
                      flush=True)
        idle = 0 if worked else idle + 1
        if idle > idle_limit:
            print("[v2-servicer] idle timeout -> exit", flush=True)
            return
        time.sleep(poll)


if __name__ == "__main__":
    sd = os.environ.get("SHORT_DIR")
    if not sd:
        print("set SHORT_DIR=<v1 short folder>", file=sys.stderr)
        raise SystemExit(2)
    short = Path(sd)
    if not short.is_absolute():
        short = ROOT / sd
    log = os.environ.get("ASM_LOG")
    log_path = (ROOT / log) if (log and not Path(log).is_absolute()) else (Path(log) if log else None)
    serve(short, log_path)
