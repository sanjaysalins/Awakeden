"""pipeline/cost.py — spend ledger + exact cost estimation/reconciliation.

Built on the primitives the `hf` CLI actually exposes (red-team-verified), NOT a fragile
credit-balance delta:
  - hf generate cost <model> --json   -> EXACT credits BEFORE spending (pre-flight, no job)
  - hf account transactions --json     -> authoritative spend/refund rows (reconcile, concurrency-proof)
  - hf account status --json           -> current balance

We log CREDITS (the real unit on an Ultimate subscription); USD is a display estimate via
HF_CREDITS_TO_USD (anchored: nano_banana_2 = 2 credits ~= $0.30 => $0.15/credit). The LLM chokepoint
records token cost only when LLM_PROVIDER=api, else a '$0 (agent)' row — so the ledger never goes
blind on the mode flag.

Ledger: data/spend_ledger.jsonl, one row per metered op:
  {ts, episode, kind, stage, provider, model, units, est_credits, actual_credits, est_usd, mode, est_only, note}

CLI:
  python -m pipeline.cost balance
  python -m pipeline.cost estimate <model> [--prompt "..."] [--image path] [--units N]
  python -m pipeline.cost summary [--episode <id>]
  python -m pipeline.cost reconcile --episode <id> --since <ISO8601>
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

LEDGER = Path(__file__).resolve().parent.parent / "data" / "spend_ledger.jsonl"
CREDITS_TO_USD = float(getattr(config, "HF_CREDITS_TO_USD", 0.15))      # nano_banana_2 2cr ~= $0.30
ELEVEN_USD_PER_CHAR = float(getattr(config, "ELEVEN_USD_PER_CHAR", 0.0002))  # ~$0.20 / 1k chars
CEILING_USD = {"short": float(getattr(config, "CEILING_SHORT_USD", 25)),
               "long": float(getattr(config, "CEILING_LONG_USD", 40))}
# per-token USD for the api-mode LLM chokepoint (placeholder Opus-ish rates; only used if NOT agent)
LLM_USD_PER_TOKEN = {"input": 5 / 1_000_000, "output": 25 / 1_000_000}


# ---- hf CLI helpers ------------------------------------------------------------
def _hf(*args):
    r = subprocess.run([str(config.HF_CLI_PATH), *args], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        raise RuntimeError(f"hf {' '.join(args)} -> {(r.stderr or r.stdout)[:200]}")


def hf_balance() -> float:
    return float(_hf("account", "status", "--json")["credits"])


def hf_estimate(model: str, prompt: str = "estimate", image=None, params=None) -> float:
    """Exact credits for ONE generation of `model` (a query — creates no job, spends nothing).
    `params` = the SAME CLI params the real create call uses ({"mode": "pro", "sound": "off", ...});
    omit it and the query prices the model DEFAULTS (kling3_0: std + sound ON = 10cr, not
    the ~7.5 the sound-off pipeline actually pays). NOTE the estimator can overquote vs real
    billing: kling3_0 pro+sound-off quotes 8.75 but every observed transaction bills 7.5
    (43 rows, 2026-07-21) — `reconcile` against transactions remains the actuals source."""
    args = ["generate", "cost", model, "--prompt", prompt, "--json"]
    if image:
        args += ["--image", str(image)]
    for k, v in (params or {}).items():
        args += [f"--{k}", str(v)]
    d = _hf(*args)
    return float(d.get("credits_exact", d.get("credits", 0)))


def hf_transactions(size: int = 100):
    # HF API caps query.size at 100 (a larger value is a hard error, seen 2026-07-14)
    return _hf("account", "transactions", "--size", str(min(size, 100)), "--json")


# ---- ledger --------------------------------------------------------------------
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def record(episode, kind, stage, provider, model="", units=1, est_credits=None,
           actual_credits=None, est_usd=None, mode=None, est_only=False, note="") -> dict:
    row = dict(ts=_now(), episode=episode, kind=kind, stage=stage, provider=provider, model=model,
               units=units, est_credits=est_credits, actual_credits=actual_credits, est_usd=est_usd,
               mode=mode, est_only=est_only, note=note)
    LEDGER.parent.mkdir(exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def record_hf(episode, kind, stage, model, units=1, prompt="estimate", image=None, note="",
              params=None) -> dict:
    """Estimate (exact) + log an HF op (images/animation). Call this around each render.
    Pass `params` = the create call's own CLI params so the row prices the real config."""
    cr = hf_estimate(model, prompt, image, params) * units
    return record(episode, kind, stage, "hf", model, units, est_credits=round(cr, 2),
                  est_usd=round(cr * CREDITS_TO_USD, 3), mode="metered", note=note)


def record_eleven(episode, kind, stage, chars, note="") -> dict:
    """Log an ElevenLabs synth (estimate-only — no transactions API)."""
    return record(episode, kind, stage, "elevenlabs", "eleven_v3", chars,
                  est_usd=round(chars * ELEVEN_USD_PER_CHAR, 3), est_only=True, note=note)


NBP_USD_PER_IMG = float(getattr(config, "NBP_USD_PER_IMG", 0.50))      # Gemini Nano Banana Pro
KLING_USD_PER_CLIP = float(getattr(config, "KLING_USD_PER_CLIP", 0.65))  # direct-Kling clip


def record_nbp(episode, kind, stage, units=1, note="") -> dict:
    """Log NBP / Gemini stills (estimate-only — billed by Google, not HF credits)."""
    return record(episode, kind, stage, "nbp", "gemini-3-pro-image", units,
                  est_usd=round(units * NBP_USD_PER_IMG, 3), est_only=True, note=note)


def record_kling(episode, kind, stage, units=1, note="") -> dict:
    """Log a direct-Kling clip (estimate-only — Kling credits, not HF)."""
    return record(episode, kind, stage, "kling", "kling-direct", units,
                  est_usd=round(units * KLING_USD_PER_CLIP, 3), est_only=True, note=note)


def record_stage(episode, stage, note="") -> dict | None:
    """$0 wall-clock milestone marker (est_usd=0) in the SAME ledger as spend rows,
    not a parallel file -- summary()/today_summary() already coerce a missing
    est_usd to 0.0, so this doesn't disturb any existing total. Lets elapsed
    per-episode time be reconstructed from data/spend_ledger.jsonl instead of
    fragile file mtimes. Best-effort: a write failure must never block the
    caller (matches cost_status.py's fire-and-forget hook writes)."""
    try:
        return record(episode, "milestone", stage, "internal", est_usd=0.0, note=note)
    except Exception as e:
        print(f"   (stage-log skipped: {e})")
        return None


def record_llm(episode, stage, model, input_tokens=0, output_tokens=0, note="") -> dict:
    """The third chokepoint — never go blind on LLM_PROVIDER. agent => $0 row; api => token cost."""
    mode = getattr(config, "LLM_PROVIDER", "agent")
    if mode != "api":
        return record(episode, "", stage, "anthropic", model, mode="agent", est_usd=0.0,
                      note=(note + " ($0 agent-mode)").strip())
    usd = input_tokens * LLM_USD_PER_TOKEN["input"] + output_tokens * LLM_USD_PER_TOKEN["output"]
    return record(episode, "", stage, "anthropic", model, units=input_tokens + output_tokens,
                  est_usd=round(usd, 4), mode="api", note=note)


# ---- budget + rollup -----------------------------------------------------------
def load() -> list[dict]:
    """All ledger rows; a torn/garbage line (unlocked concurrent appends from two
    sessions) is skipped, never a crash — this feeds hooks that run constantly."""
    if not LEDGER.exists():
        return []
    rows = []
    for l in LEDGER.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            r = json.loads(l)
        except ValueError:
            continue
        if isinstance(r, dict):
            rows.append(r)
    return rows


def _usd(v) -> float:
    """Coerce a ledger est_usd to float. Old hand-written rows carry strings like
    '20-35' / '~1' / '<1' — take the leading number (range -> low bound), else 0."""
    if isinstance(v, (int, float)):
        return float(v)
    import re as _re
    m = _re.search(r"\d+(?:\.\d+)?", str(v or ""))
    return float(m.group(0)) if m else 0.0


def episode_total_usd(episode) -> float:
    return round(sum(_usd(r.get("est_usd")) for r in load() if r.get("episode") == episode), 2)


def estimate_batch(items) -> tuple[float, float]:
    """items = [(model, units, image_or_None), ...] -> (usd, credits) — exact pre-flight."""
    cr = sum(hf_estimate(m, image=img) * u for m, u, img in items)
    return round(cr * CREDITS_TO_USD, 2), round(cr, 2)


def check_budget(episode, kind, projected_usd, override=False) -> float:
    cap = CEILING_USD.get(kind, 1e9)
    projected_total = episode_total_usd(episode) + projected_usd
    if not override and projected_total > cap:
        raise SystemExit(
            f"\n*** BUDGET CEILING *** {episode} ({kind}) would reach ~${projected_total:.2f} "
            f"> cap ${cap:.2f}.\n   Re-run with override=True / --override to proceed.\n")
    return projected_total


def reconcile(episode, since_iso, note="reconcile") -> dict:
    """Net spend-minus-refund from hf transactions since `since_iso`; append an actuals row.
    spend rows carry negative credits, refunds positive => net cost = sum(-credits)."""
    net = sum(-float(t["credits"]) for t in hf_transactions(200)
              if t.get("created_at", "") >= since_iso)
    return record(episode, "", "reconcile", "hf", "", actual_credits=round(net, 2),
                  est_usd=round(net * CREDITS_TO_USD, 2), mode="metered",
                  note=f"{note} since {since_iso}")


def summary(episode=None) -> str:
    rows = load()
    if episode:
        rows = [r for r in rows if r.get("episode") == episode]
    by_ep: dict = {}
    for r in rows:
        ep = r.get("episode") or "(unattributed)"
        d = by_ep.setdefault(ep, {"usd": 0.0, "credits": 0.0, "n": 0})
        d["usd"] += _usd(r.get("est_usd"))
        d["credits"] += r.get("actual_credits") or r.get("est_credits") or 0
        d["n"] += 1
    out = ["episode                              ops   credits     ~USD"]
    tot_u = tot_c = 0.0
    for ep, d in sorted(by_ep.items(), key=lambda x: -x[1]["usd"]):
        out.append(f"{ep[:36]:36} {d['n']:4}  {d['credits']:8.1f}  ${d['usd']:7.2f}")
        tot_u += d["usd"]; tot_c += d["credits"]
    out.append(f"{'TOTAL':36} {len(rows):4}  {tot_c:8.1f}  ${tot_u:7.2f}")
    return "\n".join(out)


def today_rows() -> list[dict]:
    """Rows whose UTC ts falls on today's LOCAL date. Skips unparsable/garbage
    lines and `reconcile` true-up rows (their ops already have estimate rows —
    summing both would double-count the day)."""
    today = datetime.now().astimezone().date()
    out = []
    for r in load():
        try:
            if datetime.fromisoformat(r.get("ts") or "").astimezone().date() != today:
                continue
        except Exception:
            continue
        if r.get("stage") == "reconcile":
            continue
        out.append(r)
    return out


def today_summary(line: bool = False) -> str:
    """Today's repo-wide spend grouped by provider; line=True -> one compact string."""
    by_p: dict = {}
    rows = today_rows()
    for r in rows:
        p = r.get("provider") or "other"
        d = by_p.setdefault(p, {"usd": 0.0, "credits": 0.0, "n": 0})
        d["usd"] += _usd(r.get("est_usd"))
        d["credits"] += r.get("actual_credits") or r.get("est_credits") or 0
        d["n"] += 1
    tot_u = sum(d["usd"] for d in by_p.values())
    tot_c = sum(d["credits"] for d in by_p.values())
    ranked = sorted(by_p.items(), key=lambda x: -x[1]["usd"])
    if line:
        return " | ".join([f"TODAY ${tot_u:.2f} ({tot_c:.1f}cr)"]
                          + [f"{p} ${d['usd']:.2f}" for p, d in ranked])
    out = [f"today ({datetime.now().astimezone().date()})",
           "provider          ops   credits     ~USD"]
    for p, d in ranked:
        out.append(f"{p[:17]:17} {d['n']:4}  {d['credits']:8.1f}  ${d['usd']:7.2f}")
    out.append(f"{'TOTAL':17} {len(rows):4}  {tot_c:8.1f}  ${tot_u:7.2f}")
    return "\n".join(out)


# ---- CLI -----------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="spend ledger / cost tool")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    pe = sub.add_parser("estimate"); pe.add_argument("model"); pe.add_argument("--prompt", default="estimate")
    pe.add_argument("--image"); pe.add_argument("--units", type=int, default=1)
    ps = sub.add_parser("summary"); ps.add_argument("--episode")
    pt = sub.add_parser("today"); pt.add_argument("--line", action="store_true")
    pr = sub.add_parser("reconcile"); pr.add_argument("--episode", required=True); pr.add_argument("--since", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "balance":
        print(f"HF balance: {hf_balance():.1f} credits  (~${hf_balance()*CREDITS_TO_USD:.2f} @ ${CREDITS_TO_USD}/cr)")
    elif a.cmd == "estimate":
        cr = hf_estimate(a.model, a.prompt, a.image) * a.units
        print(f"{a.model} x{a.units}: {cr:.1f} credits  ~${cr*CREDITS_TO_USD:.2f}")
    elif a.cmd == "summary":
        print(summary(a.episode))
    elif a.cmd == "today":
        print(today_summary(line=a.line))
    elif a.cmd == "reconcile":
        r = reconcile(a.episode, a.since)
        print(f"reconciled {a.episode}: {r['actual_credits']} credits (~${r['est_usd']}) since {a.since}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
