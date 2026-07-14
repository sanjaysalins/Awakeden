# Independent review — codex (OK, 277s)

**Findings**

1. The “HARD envelope” is not actually fail-closed. The plan admits “failed-but-BILLED rolls … leave neither row nor mp4” and says “HF balance eyeball at each wave gate covers them.” That is post-hoc manual detection, not a chokepoint. `pipeline.rollout_spend` only counts ledger rows and mp4s, so billed failures can overspend before the next wave gate.

2. Budget zero-point is contradictory. It says “pilot spend COUNTS INSIDE it,” but later says July 12-13 Women spend was “approved and reconciled separately” and sets “5 clips = 37.5cr.” The code uses `ROLLOUT_START = "2026-07-14"`, excluding earlier Women pilot rows. Pick one accounting rule and update the plan/code/comments consistently.

3. `--only <ll_slugs>` is not enforced. The plan says “A(b) invocations MUST use `--only <ll_slugs>`,” but `run_piece.py` merely skips slugs not listed and does not fail unknown or non-living-light targets. A mistyped `--only` can exit successfully without rendering; a wrong valid slug can spend on the wrong clip.

4. The “Per-slug roll cap: 3 attempts” is just prose. I found no attempt counter or enforcement in the reroll path. Parking rejects makes the clip “missing,” so repeated paid attempts remain possible unless the human remembers the cap.

5. “One render path, no silent fallback” is not enforced. `_hf_animate_short.py` still contains the ffmpeg fallback path; the plan relies on “never use” discipline rather than making bypass CLIs refuse rollout dirs or call the rollout gate/spend checks.

6. A(a) tooling is still vapor from a verification standpoint. The plan names “backup helper + before/after page builder + `wave_checklist.json` writer,” but the repo only clearly has the lower-level `build_filmstrip()` helper. If A(b) is blocked on this, the plan needs concrete filenames, commands, tests, and pass criteria.

7. “RE-QUOTE FIRST,” “near-ceiling episode = ASK THE USER,” and B-D forecast rules are not deterministic gates. Existing budget code blocks only hard USD cap breaches; it does not define near-ceiling or enforce re-quote forecasts.

VERDICT: REVISE
TOP FIXES:
1. Make spend control truly fail-closed: reservation/lock before each paid call plus reconciliation for billed failures.
2. Resolve the rollout zero-point contradiction and recompute remaining credits from that single rule.
3. Enforce `--only` and per-slug attempt caps in code, not SOP prose.
