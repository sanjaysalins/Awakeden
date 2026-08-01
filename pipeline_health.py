"""pipeline_health.py -- $0 rolling health report for the pipeline-slowdown
POC (see PIPELINE_SLOWDOWN_POC_PLAN.md, 2026-08-01). Re-run every couple of
episodes to see whether the fixes are actually helping, not just installed.

Reads ONLY data that already exists -- no new logging beyond record_stage()/
record_hf() already wired into the animate scripts:
  - data/spend_ledger.jsonl   -> milestone rows (animate_start/animate_end,
    nsfw_fallback_recovered/nsfw_fallback_failed) per episode
  - .agent_bridge/archive/    -> request->response latency, recomputed live
    (not a frozen snapshot -- always reflects current archive contents)
  - data/.watcher_status.json -> current bridge stall state

CLI:
  .venv\\Scripts\\python.exe pipeline_health.py            # text report
  .venv\\Scripts\\python.exe pipeline_health.py --html      # also writes _PIPELINE_HEALTH.html
"""
from __future__ import annotations
import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "data" / "spend_ledger.jsonl"
BRIDGE_ARCHIVE = ROOT / ".agent_bridge" / "archive"
WATCHER_STATUS = ROOT / "data" / ".watcher_status.json"

MILESTONE_STAGES = {"animate_start", "animate_end",
                     "nsfw_fallback_recovered", "nsfw_fallback_failed"}


def _load_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    return rows


def animate_elapsed_by_episode(rows: list[dict]) -> dict[str, float]:
    """{episode: seconds between its animate_start and animate_end}, only for
    episodes that have BOTH markers (older/unrun episodes just won't appear)."""
    starts, ends = {}, {}
    for r in rows:
        if r.get("kind") != "milestone":
            continue
        ep = r.get("episode")
        ts = r.get("ts")
        if not ep or not ts:
            continue
        try:
            t = datetime.fromisoformat(ts).timestamp()
        except ValueError:
            continue
        if r.get("stage") == "animate_start":
            starts.setdefault(ep, t)
        elif r.get("stage") == "animate_end":
            ends[ep] = t  # last one wins if a script re-ran
    return {ep: ends[ep] - starts[ep] for ep in starts if ep in ends and ends[ep] >= starts[ep]}


def nsfw_fallback_events(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r.get("kind") == "milestone"
            and r.get("stage") in ("nsfw_fallback_recovered", "nsfw_fallback_failed")]


def bridge_latency_stats(max_plausible_sec: float = 6 * 3600) -> dict:
    """Recomputed live from archive/ mtimes every run -- not a frozen number.
    Pairs older than max_plausible_sec are dropped (almost certainly an
    unrelated file touch, not real service time)."""
    if not BRIDGE_ARCHIVE.exists():
        return {"n": 0}
    lat = []
    for req in BRIDGE_ARCHIVE.glob("*.request.md"):
        resp = BRIDGE_ARCHIVE / f"{req.name[:-len('.request.md')]}.txt"
        if not resp.exists():
            continue
        try:
            dt = resp.stat().st_mtime - req.stat().st_mtime
        except OSError:
            continue
        if 0 <= dt < max_plausible_sec:
            lat.append(dt)
    if not lat:
        return {"n": 0}
    lat.sort()
    n = len(lat)
    return {
        "n": n,
        "median": statistics.median(lat),
        "p90": lat[int(n * 0.9)],
        "p99": lat[min(int(n * 0.99), n - 1)],
        "max": lat[-1],
    }


def watcher_snapshot() -> dict | None:
    try:
        status = json.loads(WATCHER_STATUS.read_text(encoding="utf-8"))
    except Exception:
        return None
    age_sec = datetime.now(timezone.utc).timestamp() - float(status.get("updated_ts", 0))
    status["_status_file_age_sec"] = round(age_sec)
    return status


def _fmt_sec(s: float) -> str:
    if s < 60:
        return f"{s:.0f}s"
    if s < 3600:
        return f"{s / 60:.1f}m"
    return f"{s / 3600:.1f}h"


def build_report() -> dict:
    rows = _load_ledger()
    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "animate_elapsed": animate_elapsed_by_episode(rows),
        "fallback_events": nsfw_fallback_events(rows),
        "bridge_latency": bridge_latency_stats(),
        "watcher": watcher_snapshot(),
    }


def render_text(report: dict) -> str:
    out = [f"pipeline health -- generated {report['generated']}", "=" * 60]

    out.append("\n1. NSFW auto-fallback (poc_comic_page/_animate_piece1_v2.py)")
    events = report["fallback_events"]
    if not events:
        out.append("   no fallback events logged yet -- fix hasn't been exercised")
    else:
        recovered = [e for e in events if e["stage"] == "nsfw_fallback_recovered"]
        failed = [e for e in events if e["stage"] == "nsfw_fallback_failed"]
        out.append(f"   {len(recovered)} recovered automatically, {len(failed)} failed both providers")
        for e in events[-10:]:
            out.append(f"     [{e['stage']}] {e.get('episode')}: {e.get('note')}")

    out.append("\n2. Animate stage wall-clock (per episode, start->end)")
    elapsed = report["animate_elapsed"]
    if not elapsed:
        out.append("   no episode has both animate_start and animate_end yet")
    else:
        for ep, sec in sorted(elapsed.items(), key=lambda x: -x[1]):
            out.append(f"   {ep:<24} {_fmt_sec(sec)}")
        out.append("   (baseline for comparison: Storm 6 rebuild versions / 38h total,")
        out.append("    Bronze Serpent 5+ reroll cycles / 14h24m -- see PIPELINE_SLOWDOWN_POC_PLAN.md.")
        out.append("    A single episode looking faster is NOT proof by itself -- format-")
        out.append("    learning-curve confounds this; treat as directional only.)")

    out.append("\n3. Agent-bridge service latency (live, from .agent_bridge/archive/)")
    bl = report["bridge_latency"]
    if bl["n"] == 0:
        out.append("   no archived request/response pairs found")
    else:
        out.append(f"   n={bl['n']}  median={_fmt_sec(bl['median'])}  "
                    f"p90={_fmt_sec(bl['p90'])}  p99={_fmt_sec(bl['p99'])}  max={_fmt_sec(bl['max'])}")
        out.append("   (2026-08-01 baseline: median 27.5s, p90 85s -- watch for this drifting up)")

    out.append("\n4. Watcher (stall detection)")
    w = report["watcher"]
    if w is None:
        out.append("   data/.watcher_status.json not found -- is watcher_service.py running?")
    else:
        stale = w["_status_file_age_sec"] > 60
        out.append(f"   state={w.get('state')}  pending_count={w.get('count', 0)}"
                    f"{'  [STATUS FILE STALE -- watcher may not be running]' if stale else ''}")
        if w.get("oldest_id"):
            out.append(f"   oldest unanswered: {w['oldest_id']} "
                        f"({_fmt_sec(w.get('oldest_age_sec', 0))} old) -- {w.get('oldest_label', '')}")

    return "\n".join(out)


def render_html(report: dict) -> str:
    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    events = report["fallback_events"]
    recovered = [e for e in events if e["stage"] == "nsfw_fallback_recovered"]
    failed = [e for e in events if e["stage"] == "nsfw_fallback_failed"]
    elapsed = sorted(report["animate_elapsed"].items(), key=lambda x: -x[1])
    bl = report["bridge_latency"]
    w = report["watcher"] or {}

    rows_events = "".join(
        f"<tr><td>{esc(e.get('episode'))}</td><td>{'recovered' if e['stage'].endswith('recovered') else 'FAILED'}</td>"
        f"<td>{esc(e.get('note'))}</td><td>{esc(e.get('ts'))}</td></tr>" for e in events[-20:]
    ) or "<tr><td colspan=4>no fallback events logged yet</td></tr>"

    rows_elapsed = "".join(
        f"<tr><td>{esc(ep)}</td><td>{_fmt_sec(sec)}</td></tr>" for ep, sec in elapsed
    ) or "<tr><td colspan=2>no complete animate_start/animate_end pair yet</td></tr>"

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Pipeline Health</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem;
        background: #fafafa; color: #222; }}
h1 {{ font-size: 1.4rem; }} h2 {{ font-size: 1.1rem; margin-top: 2rem; border-bottom: 2px solid #ddd; padding-bottom: .3rem; }}
table {{ border-collapse: collapse; width: 100%; margin-top: .5rem; }}
td, th {{ text-align: left; padding: .4rem .6rem; border-bottom: 1px solid #eee; font-size: .9rem; }}
.stat {{ font-size: 1.3rem; font-weight: 600; }}
.note {{ color: #666; font-size: .85rem; }}
.bad {{ color: #b3261e; font-weight: 600; }}
.ok {{ color: #1e7b34; font-weight: 600; }}
</style></head><body>
<h1>Pipeline health -- generated {esc(report['generated'])}</h1>
<p class="note">Re-run every couple of episodes: <code>.venv\\Scripts\\python.exe pipeline_health.py --html</code>.
See <code>PIPELINE_SLOWDOWN_POC_PLAN.md</code> for the diagnosis this tracks against.</p>

<h2>1. NSFW auto-fallback</h2>
<p><span class="stat">{len(recovered)}</span> recovered automatically &middot;
<span class="stat {'bad' if failed else ''}">{len(failed)}</span> failed both providers</p>
<table><tr><th>episode</th><th>result</th><th>note</th><th>when</th></tr>{rows_events}</table>

<h2>2. Animate stage wall-clock</h2>
<table><tr><th>episode</th><th>elapsed</th></tr>{rows_elapsed}</table>
<p class="note">Baseline: Storm 6 rebuild versions / 38h total, Bronze Serpent 5+ reroll cycles / 14h24m.
A single faster episode is directional only, not proof (format-learning-curve confound).</p>

<h2>3. Agent-bridge service latency (live)</h2>
{f'<p><span class="stat">n={bl["n"]}</span> &middot; median {_fmt_sec(bl["median"])} &middot; p90 {_fmt_sec(bl["p90"])} &middot; p99 {_fmt_sec(bl["p99"])} &middot; max {_fmt_sec(bl["max"])}</p>' if bl["n"] else "<p>no archived pairs found</p>"}
<p class="note">2026-08-01 baseline: median 27.5s, p90 85s. Watch for this drifting up over time.</p>

<h2>4. Watcher (stall detection)</h2>
<p class="stat {'bad' if w.get('state') not in (None, 'ok') else 'ok'}">state={esc(w.get('state', 'unknown'))}</p>
{f"<p>oldest unanswered: {esc(w.get('oldest_id'))} ({_fmt_sec(w.get('oldest_age_sec', 0))} old)</p>" if w.get('oldest_id') else ""}
</body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", action="store_true", help="also write _PIPELINE_HEALTH.html")
    a = ap.parse_args()
    report = build_report()
    print(render_text(report))
    if a.html:
        out = ROOT / "_PIPELINE_HEALTH.html"
        out.write_text(render_html(report), encoding="utf-8")
        print(f"\n[html] -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
