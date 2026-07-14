"""cost_status.py — $0 deterministic spend watcher (statusline + PostToolUse hook).

STDLIB-ONLY on purpose (no `config` import): this runs with `python -S -E` on every
statusline refresh and after every Bash/PowerShell tool call, so startup must be
instant and must never touch .env / sitecustomize / WMI. The ledger rows already
carry est_usd + credits, so summing needs no rate tables.

Modes:
  --statusline   print one line for the Claude Code status bar (nothing if no ledger)
  --hook         PostToolUse: (1) log ad-hoc `hf generate create <model>` commands
                 typed in chat (pipeline renders call hf.exe INSIDE python subprocesses,
                 so they never match — no double count); (2) emit {"systemMessage": ...}
                 ONLY when today's total changed since the last report.
State: data/.cost_report_state.json  ·  Ledger: data/spend_ledger.jsonl
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "data" / "spend_ledger.jsonl"
STATE_DIR = ROOT / "data" / ".cost_state"  # one state file per Claude session
CREDITS_TO_USD = 0.15  # mirrors config.HF_CREDITS_TO_USD (nano_banana_2 2cr ~= $0.30)

# ad-hoc hf spend typed straight into chat. Anchored at a COMMAND position (start
# or after ;/&&/|/newline, optional path prefix) and matched only after quoted
# strings are stripped — a `git commit -m "..hf generate create.."` / echo / grep
# that merely MENTIONS the phrase must never write a phantom ledger row.
HF_ADHOC_RE = re.compile(
    r"(?:^|[;&|\n(])\s*(?:\S*[/\\])?hf(?:\.exe)?\s+generate\s+create\s+([\w.-]+)", re.I)
_QUOTED_RE = re.compile(r"\"[^\"]*\"|'[^']*'")
_DURATION_RE = re.compile(r"--duration\s+(\d+)")
# static USD per 5s/1-img generation for the models in use; unknown -> exact hf query
ADHOC_USD = {"nano_banana_2": 0.30, "kling3_0": 0.65, "veo3_1_lite": 0.33, "seedance1_5": 0.33}
_VIDEO_MODELS = {"kling3_0", "veo3_1_lite", "seedance1_5"}  # price scales with --duration

try:  # emoji-safe output on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def _usd(v) -> float:
    """Coerce est_usd to float (legacy rows carry strings like '20-35' / '~1')."""
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d+(?:\.\d+)?", str(v or ""))
    return float(m.group(0)) if m else 0.0


def today_by_provider() -> dict:
    today = datetime.now().astimezone().date()
    by_p: dict = {}
    if not LEDGER.exists():
        return by_p
    for ln in LEDGER.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        try:  # one torn/garbage line (unlocked concurrent appends) must never brick the hook
            r = json.loads(ln)
            if datetime.fromisoformat(r.get("ts") or "").astimezone().date() != today:
                continue
            # reconcile rows are actuals TRUE-UPS over ops already estimated above —
            # summing both would double-count the day
            if r.get("stage") == "reconcile":
                continue
            p = r.get("provider") or "other"
            d = by_p.setdefault(p, {"usd": 0.0, "credits": 0.0})
            d["usd"] += _usd(r.get("est_usd"))
            d["credits"] += r.get("actual_credits") or r.get("est_credits") or 0
        except Exception:
            continue
    return by_p


def _line(by_p: dict, sep: str = " · ") -> str:
    tot_u = sum(d["usd"] for d in by_p.values())
    tot_c = sum(d["credits"] for d in by_p.values())
    parts = [f"today ${tot_u:.2f} ({tot_c:.1f}cr)"]
    parts += [f"{p} ${d['usd']:.2f}"
              for p, d in sorted(by_p.items(), key=lambda x: -x[1]["usd"])]
    return "\U0001F4B0 " + sep.join(parts)


def adhoc_models(command: str) -> list[str]:
    """Models of genuinely ad-hoc `hf generate create` calls in `command` — quoted
    strings stripped first, one entry per chained call. [] for mere mentions."""
    bare = _QUOTED_RE.sub(" ", command)
    return [m.group(1) for m in HF_ADHOC_RE.finditer(bare)]


def _adhoc_usd(model: str, command: str = "") -> tuple[float, str]:
    """USD for one ad-hoc generation: static map (video price scales with the
    command's --duration, base 5s), else exact `hf generate cost` query."""
    if model in ADHOC_USD:
        usd = ADHOC_USD[model]
        if model in _VIDEO_MODELS:
            dm = _DURATION_RE.search(_QUOTED_RE.sub(" ", command))
            if dm:
                usd = round(usd * max(int(dm.group(1)), 1) / 5.0, 3)
        return usd, ""
    hf = Path(os.environ.get("USERPROFILE", "")) / "bin" / "hf.exe"
    try:
        r = subprocess.run([str(hf), "generate", "cost", model, "--prompt", "estimate", "--json"],
                           capture_output=True, text=True, timeout=15)
        d = json.loads(r.stdout)
        cr = float(d.get("credits_exact", d.get("credits", 0)))
        return round(cr * CREDITS_TO_USD, 3), ""
    except Exception:
        return 0.0, "UNKNOWN RATE — reconcile against hf transactions"


def _log_adhoc(model: str, command: str) -> str:
    """Append one ad-hoc ledger row; return a short description for the report line."""
    usd, warn = _adhoc_usd(model, command)
    row = dict(ts=datetime.now().astimezone().isoformat(), episode="(adhoc)", kind="adhoc",
               stage="chat", provider="hf", model=model, units=1,
               est_credits=round(usd / CREDITS_TO_USD, 2), actual_credits=None,
               est_usd=usd, mode="metered", est_only=True,
               note=(warn or command[:120]))
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return f"adhoc {model} ${usd:.2f}" + (" ⚠ UNKNOWN RATE" if warn else "")


def run_hook() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    command = str((payload.get("tool_input") or {}).get("command") or "")
    adhoc_notes = []
    if LEDGER.parent.exists():
        adhoc_notes = [_log_adhoc(m, command) for m in adhoc_models(command)]

    sid = re.sub(r"[^\w-]", "", str(payload.get("session_id") or "global"))[:40] or "global"
    state = STATE_DIR / f"{sid}.json"

    # fast path: no adhoc row and ledger untouched since this session's last report
    st = LEDGER.stat() if LEDGER.exists() else None
    prev = {}
    try:
        prev = json.loads(state.read_text(encoding="utf-8"))
    except Exception:
        pass
    sig = [st.st_mtime, st.st_size] if st else None
    if prev.get("sig") == sig and not adhoc_notes:
        return

    by_p = today_by_provider()
    tot = round(sum(d["usd"] for d in by_p.values()), 2)
    STATE_DIR.mkdir(exist_ok=True)
    state.write_text(json.dumps({"sig": sig, "total_usd": tot}), encoding="utf-8")
    # an adhoc row ALWAYS reports (even $0 UNKNOWN RATE — money moved, say so);
    # otherwise stay silent unless today's total actually changed
    if not adhoc_notes and tot == prev.get("total_usd"):
        return
    delta = tot - float(prev.get("total_usd") or 0.0)
    msg = _line(by_p)
    if 0 < delta < tot:
        msg += f"  (+${delta:.2f})"
    if adhoc_notes:
        msg += "  [" + ", ".join(adhoc_notes) + "]"
    print(json.dumps({"systemMessage": msg}, ensure_ascii=False))
    _prune_state()


def _prune_state() -> None:
    """Old sessions leave state files behind; keep the dir small without deleting
    a still-live session's state (age guard, not just count)."""
    try:
        import time
        files = sorted(STATE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
        week = time.time() - 7 * 86400
        for p in files[:-50]:
            if p.stat().st_mtime < week:
                p.unlink()
    except Exception:
        pass


def main() -> int:
    try:
        mode = sys.argv[1] if len(sys.argv) > 1 else "--statusline"
        if mode == "--hook":
            run_hook()
            return 0
        if not LEDGER.exists():
            return 0
        print(_line(today_by_provider(), sep=" | "))
    except Exception as e:
        # this runs after EVERY shell command / statusline tick — it must never
        # brick the session, whatever is on disk
        print(f"cost_status: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
