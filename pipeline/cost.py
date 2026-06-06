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


def hf_estimate(model: str, prompt: str = "estimate", image=None) -> float:
    """Exact credits for ONE generation of `model` (a query — creates no job, spends nothing)."""
    args = ["generate", "cost", model, "--prompt", prompt, "--json"]
    if image:
        args += ["--image", str(image)]
    d = _hf(*args)
    return float(d.get("credits_exact", d.get("credits", 0)))


def hf_transactions(size: int = 200):
    return _hf("account", "transactions", "--size", str(size), "--json")


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


def record_hf(episode, kind, stage, model, units=1, prompt="estimate", image=None, note="") -> dict:
    """Estimate (exact) + log an HF op (images/animation). Call this around each render."""
    cr = hf_estimate(model, prompt, image) * units
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
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()]


def episode_total_usd(episode) -> float:
    return round(sum((r.get("est_usd") or 0) for r in load() if r.get("episode") == episode), 2)


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
        d["usd"] += r.get("est_usd") or 0
        d["credits"] += r.get("actual_credits") or r.get("est_credits") or 0
        d["n"] += 1
    out = ["episode                              ops   credits     ~USD"]
    tot_u = tot_c = 0.0
    for ep, d in sorted(by_ep.items(), key=lambda x: -x[1]["usd"]):
        out.append(f"{ep[:36]:36} {d['n']:4}  {d['credits']:8.1f}  ${d['usd']:7.2f}")
        tot_u += d["usd"]; tot_c += d["credits"]
    out.append(f"{'TOTAL':36} {len(rows):4}  {tot_c:8.1f}  ${tot_u:7.2f}")
    return "\n".join(out)


# ---- CLI -----------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="spend ledger / cost tool")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    pe = sub.add_parser("estimate"); pe.add_argument("model"); pe.add_argument("--prompt", default="estimate")
    pe.add_argument("--image"); pe.add_argument("--units", type=int, default=1)
    ps = sub.add_parser("summary"); ps.add_argument("--episode")
    pr = sub.add_parser("reconcile"); pr.add_argument("--episode", required=True); pr.add_argument("--since", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "balance":
        print(f"HF balance: {hf_balance():.1f} credits  (~${hf_balance()*CREDITS_TO_USD:.2f} @ ${CREDITS_TO_USD}/cr)")
    elif a.cmd == "estimate":
        cr = hf_estimate(a.model, a.prompt, a.image) * a.units
        print(f"{a.model} x{a.units}: {cr:.1f} credits  ~${cr*CREDITS_TO_USD:.2f}")
    elif a.cmd == "summary":
        print(summary(a.episode))
    elif a.cmd == "reconcile":
        r = reconcile(a.episode, a.since)
        print(f"reconciled {a.episode}: {r['actual_credits']} credits (~${r['est_usd']}) since {a.since}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
