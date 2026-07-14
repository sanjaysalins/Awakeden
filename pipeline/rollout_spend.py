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


def disk_clip_count(root: Path | None = None) -> int:
    """Cross-check (panel rounds 3-4): the ledger writer is best-effort — hf_animate
    proceeds unmetered if pipeline.cost errors — so ledger rows can UNDER-count. Count
    rendered mp4s on disk (rollout episodes, newer than the rollout start):
    - RECURSIVE under clips/ so QC rejects parked in _rejected/ and stale clips in
      _stale_from_bad_stills/ stay charged (at 2.3x/keeper most paid rolls are rejects)
    - DE-DUPED by (size, mtime): promote copies a pilot mp4 into clips/ via copy2, which
      preserves both — one HF bill must not count twice."""
    import datetime as dt
    root = root or LEDGER.parent.parent / "batches"
    cutoff = dt.datetime.fromisoformat(ROLLOUT_START).timestamp()
    seen = set()
    for ep_dir in root.glob("cluster_0*/*"):
        if ep_dir.name not in ROLLOUT_EPISODES:
            continue
        for pattern in ("clips/**/*.mp4", "_fx_pilot/**/*.mp4"):
            for m in (ep_dir / "visual").glob(pattern):
                st = m.stat()
                if st.st_mtime >= cutoff:
                    seen.add((ep_dir.name, st.st_size, round(st.st_mtime, 2)))
    return len(seen)


def check(verbose: bool = True) -> int:
    """0 = inside the cap; 1 = BREACHED. Called at the animate chokepoint AND wave gates."""
    clips, credits, stills_usd, per_ep = tally()
    disk = disk_clip_count()
    if disk > clips:
        if verbose:
            print(f"[stop-loss] WARNING: {disk} rollout clips on disk vs {clips} ledger rows "
                  f"- ledger under-counted; charging the cap at the DISK number")
        credits = disk * KLING_CR_PER_CLIP
    if verbose:
        print(f"ROLLOUT SPEND since {ROLLOUT_START} (attributable; disk cross-checked):")
        for ep, n in sorted(per_ep.items()):
            print(f"  {ep:36} {n:3} clip(s)  {n * KLING_CR_PER_CLIP:7.1f}cr")
        print(f"  TOTAL: {max(clips, disk)} clips = {credits:.1f}cr of {CAP_CREDITS:.0f}cr cap"
              f"  (+ ${stills_usd:.2f} BytePlus stills, separate currency)")
    if credits >= CAP_CREDITS:
        print("STOP-LOSS BREACHED - no further paid renders; re-quote the user.")
        return 1
    if verbose:
        print(f"  headroom: {CAP_CREDITS - credits:.1f}cr")
    return 0


def main() -> int:
    return check(verbose=True)


if __name__ == "__main__":
    sys.exit(main())
