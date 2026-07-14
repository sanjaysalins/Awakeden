# Independent review — claude (OK, 310s)

All heavy claims verified against the repo before judging. What checked out (I ran it, not just read it):

- `pipeline/rollout_gate.py` + `pipeline/rollout_spend.py` exist; **22 gate tests pass live** (plan says 21 — off by one, in the plan's favor).
- Chokepoint is real: `run_piece.py:352-370` refuses on gate FAIL (exit 3) and stop-loss breach (exit 4); `run_piece.py:791-794` propagates the code to the shell (round-4 codex fix confirmed).
- Per-clip stop-loss re-check is inside the render loop (`run_piece.py:396-401`), not once per invocation.
- Re-roll mechanic real: `_clip_state` (`run_piece.py:326-329`) returns "missing" before any hash check, so a parked reject re-renders.
- Disk cross-check live run: **5 clips = 37.5cr, 447.5cr headroom** — dedup genuinely collapses the 3 promote-copies in `_fx_pilot/` against `clips/` and still charges the 2 rejected variants (sternface, bleedingwound). Ledger = disk, as claimed.
- Baseline dump checked in; `build_filmstrip` (`pipeline/clip_anim_qc.py:69`) and `_sfx_builder` (`cli_livingpage.py:47`) exist; all 13 pieces have `piece.json` + livingpage spec (no spec-less bypass); no silent fallback in `run_animate` (prints FAILED, substitutes nothing); the `father_forgive_them` cross-ref is real (`it_is_finished_john1930/piece.json:60`).

Findings that survive:

**1. The plan contradicts itself on current spend — in the meter section.** Machine-bar says "Current: 6 clips charged (disk) = 45cr, 440 headroom"; Budget v5 says 37.5cr / 447.5 remaining; answered-objections says "5 = 5". Live truth is 5 / 37.5 / 447.5. The 45cr line is stale residue from an earlier round. A spend-control document whose control section disagrees with its budget section by one clip is exactly the drift class this plan spent four rounds hunting.

**2. The 7.5cr/clip constant is silently pinned to 5-second clips and nothing enforces that.** `rollout_spend.py:19` charges `clips × 7.5` regardless of duration; every `piece.json` today says `"duration": 5`, so the math holds — but A(a) is a *full spec rewrite* ×3, and the project's own locked memory (`feedback-kling-lowmotion-fix`) prescribes single **10s** holds for low-motion clips, which living-light clips are. One authoring decision to bump a duration and HF bills ~2× while the fail-closed meter under-counts by half. Cheap fix: assert `animate.duration == 5` in the rollout gate, or scale credits by duration.

**3. The A(b) `--only` MUST is human discipline with no teeth.** The plan itself states a bare `--stage animate` "re-renders every hash-stale clip and burns the envelope" — after a gold-master-scale spec rewrite, stale clips will be plentiful, and the per-clip stop-loss only halts at the 485 global cap, so one accidental bare invocation can legally spend most of the remaining envelope on non-living-light re-renders. Three panel rounds converted exactly this class of control into code; this one stayed prose. Cheap guard in `run_animate`: when the gate is active, `--only` is empty, and >2 clips are non-fresh, refuse with an explicit override env.

Minor (no fix required, one-line caveats at most): a direct-Kling NSFW fallback render, if ever used, bills Kling credits the tally can't see — the disk count would charge it at the HF 7.5cr rate, wrong currency but conservative; and "21 gate tests" should read 22.

The structural machinery is real, tested, and matches the text — this is the first revision where every load-bearing claim I checked was true in code. What remains is one factual contradiction inside the artifact and two cheap hardening gaps in the fail-closed story that gates paid spend. A(a) ($0) is safe to proceed; the plan's own bar for A(b) is a clean verdict, and finding 2 is a real latent hole in the meter itself.

VERDICT: REVISE
TOP FIXES:
1. Reconcile the current-spend numbers to one truth (5 clips / 37.5cr / 447.5cr remaining) — delete the stale "6 clips = 45cr, 440 headroom" line in the machine-bar section.
2. Pin the billing assumption in code: assert `animate.duration == 5` in the rollout gate (or scale `KLING_CR_PER_CLIP` by duration) so a 10s anti-melt hold can't silently halve the meter.
3. Enforce the A(b) `--only` rule at the chokepoint: refuse a bare `--stage animate` when the rollout gate is active and more than ~2 clips are non-fresh, behind a loud explicit override.
