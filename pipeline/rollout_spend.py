"""ROLLOUT STOP-LOSS (panel round-2 fix, 2026-07-14) — $0, deterministic.

The 485cr envelope was a false control: animate ledger rows carry est_credits=null (so
`cost summary` shows 0 credits) and account-level `reconcile` OVER-attributes when the
user spends on HF in parallel (observed: the 80cr women reconcile swallowed unrelated
Seedream rows). This counts what IS attributable: rollout-episode ledger rows since the
rollout started — Kling clips at the observed 7.5cr billing + BytePlus stills in USD.

Run at EVERY wave gate:
  .venv\\Scripts\\python.exe -m pipeline.rollout_spend          # exit 1 when cap breached
"""
import json
import sys
from pathlib import Path

LEDGER = Path(__file__).parent.parent / "data" / "spend_ledger.jsonl"
ROLLOUT_START = "2026-07-14"
CAP_CREDITS = 485.0           # user-approved envelope; PILOT SPEND COUNTS INSIDE IT
KLING_CR_PER_CLIP = 7.5       # observed HF billing (transactions 2026-07-13/14)

ROLLOUT_EPISODES = {
    "women_first_witnesses_luke245",           # gold master incl. pilot rolls
    "crucifixion_foretold_ps2218", "forsaken_cry_ps221", "i_thirst_john1928",
    "into_thy_hands_luke2346", "it_is_finished_john1930", "pierced_zech1210",
    "thirty_pieces_zech11", "today_paradise_luke2343", "watch_one_hour_matt2640",
    "woman_behold_john1926", "empty_tomb_john208", "sign_of_jonah_matt1240",
}


def tally():
    clips, stills_usd, per_ep = 0, 0.0, {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("ts", "") < ROLLOUT_START or r.get("episode") not in ROLLOUT_EPISODES:
            continue
        if r.get("stage") == "reconcile":
            continue      # over-attributes under parallel account use — excluded by design
        if r.get("kind") == "clip" and r.get("provider") == "hf":
            n = int(r.get("units") or 1)
            clips += n
            per_ep[r["episode"]] = per_ep.get(r["episode"], 0) + n
        elif r.get("kind") == "still":
            stills_usd += float(r.get("est_usd") or 0)
    return clips, clips * KLING_CR_PER_CLIP, stills_usd, per_ep


def main() -> int:
    clips, credits, stills_usd, per_ep = tally()
    print(f"ROLLOUT SPEND since {ROLLOUT_START} (attributable ledger rows):")
    for ep, n in sorted(per_ep.items()):
        print(f"  {ep:36} {n:3} clip(s)  {n * KLING_CR_PER_CLIP:7.1f}cr")
    print(f"  TOTAL: {clips} clips = {credits:.1f}cr of {CAP_CREDITS:.0f}cr cap"
          f"  (+ ${stills_usd:.2f} BytePlus stills, separate currency)")
    if credits >= CAP_CREDITS:
        print("STOP-LOSS BREACHED - no further paid renders; re-quote the user.")
        return 1
    print(f"  headroom: {CAP_CREDITS - credits:.1f}cr")
    return 0


if __name__ == "__main__":
    sys.exit(main())
