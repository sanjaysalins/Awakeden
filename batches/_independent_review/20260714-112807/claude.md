# Independent review — claude (OK, 194s)

I verified the plan's factual claims against the repo before judging. Most check out exactly: `pipeline/rollout_gate.py` exists and does what's listed, the gold master PASSes, `it_is_finished` FAILs with exactly 6 reasons, `empty_tomb` really is 9 stills / 20 beats with `risen_christ_wounds` used 5×, and the 13-piece wave list matches the actual cluster folders. The plan is honest. But three things don't survive scrutiny.

## Findings

**1. The re-roll margin contradicts the plan's own pilot data (Budget section).**
The plan budgets "+~50% QC-lottery re-roll margin" on a claimed "~1 in 3 first rolls fails." But the plan itself reports "~52.5cr / 7 Kling rolls" for the pilot, and the gold master's `piece.json` shows only **3 kept living-light clips** (`women_bowed`, `risen_christ_seeking`, `women_tiny_dawn`). The ledger confirms `risen_christ_seeking` alone was rolled 3 times. That's **7 rolls → 3 keepers ≈ 2.3 rolls per keeper = +133%**, not +50%. Even granting that the v1/v2 template failures are now codified as locks and the go-forward rate should improve, +50% is exactly the *mean* of a 1-in-3 reject rate with zero headroom — one unlucky piece eats the margin. At the observed pilot rate, living-light alone is ~525cr and the total lands near ~700cr, ~45% over the approved 485.

**2. "rollout_gate PASS" is sold as the bar, but the gate doesn't check several of the stated gold-master properties (Goal section vs `pipeline/rollout_gate.py`).**
The per-piece flow is "spec upgrade → rollout_gate PASS → paid renders." Unchecked by the gate:
- **Cold→warm arc direction** — the gate only checks fx *presence* ≥50% (line 60). A spec with a flat 7900K on every beat passes; nothing verifies temp actually descends toward the landing.
- **Double-lighting** — listed as a known risk with a manual mitigation, yet trivially gate-checkable: the gate already iterates living-light slugs per beat (lines 79–85); adding "beat plays a living_light clip AND has `fx.rays` → FAIL" is ~3 lines. Leaving a known, deterministic failure mode to memory across 13 pieces is the exact gap gates exist for.
- **Scale variety, shatter-only-multi-figure, sound accents / no hype drop, motion-hook open** — all in the Goal bullets, none gated, not named as human-checklist items either.
- Cosmetic but ironic: `SLOP_TOKENS` (line 22) misses the Unicode ellipsis `…`, and the gate's own FAIL messages print as mojibake (`�`) on the Windows console.

**3. Budget structure has no aggregate stop-loss and a soft clip count.**
"~30 clips" assumes ~2.3/piece, but the Goal commits to "2–3 per piece" → up to 39 base clips (292cr before margin). "Per-episode ceilings enforced" at the chokepoint doesn't protect the 485cr *total* — 13 episodes can each stay under their ceiling and still blow the aggregate. The wave human gates are the natural checkpoint, but the plan never says a wave gate includes "cumulative spend vs 485 + re-forecast."

**Smaller items:**
- `father_forgive_them` migration (Wave C) is the only piece with no `livingpage_short.spec.json` at all (gate confirms). The "≈35cr extras" figure has no shown basis, and the mocomic→livingpage migration is novel work with no de-risk step.
- Phase 0 is called "shipped" but `rollout_gate.py`, `test_rollout_gate.py`, and the plan itself are **untracked in git**. Commit before Wave A so 13 pieces run against a pinned gate.
- Wave D's new de-dup stills: the plan routes them through bible-check/vision-audit (good) but doesn't mention registering them in the root `asset_index.json` per the standing global-asset-index rule.

What's right: Wave A as a small proving batch, backups before rebuild, image-gate-style QC-by-eye per clip, the verbatim-prompt escape, and the fail-closed glitter ban are all real and sensible. The plan's honesty (open questions, admitted pilot fails) is a strength — the pilot data just needs to actually drive the budget.

VERDICT: REVISE
TOP FIXES:
1. Fix the re-roll math: pilot ran 7 rolls for 3 keepers (+133%), not +50% — either budget to the observed rate (~700cr) or make Wave A an explicit rate-measurement gate that re-quotes the user before Wave B, plus a hard cumulative 485cr stop-loss checked at every wave gate.
2. Close the cheap gate gaps in `pipeline/rollout_gate.py`: temp-arc direction (early beats colder than landing), double-lighting (living_light beat must not also carry `fx.rays`), Unicode ellipsis in SLOP_TOKENS; list the un-gateable Goal bullets (scale variety, sound accents, hook-open bookend) as named human-checklist items per piece.
3. Pin the clip count (default 2 living-light clips/piece, 3 only by exception) so the 30-clip base holds, and commit the Phase 0 files to git before Wave A starts.
