# Independent review — claude (OK, 100s)

Verified against the codebase. The artifact is presented as a "design (for panel review)" — a forward plan — but every component already exists and is wired in (`pipeline/bible_kb.py`, `bible_gate.py`, `bible_calibrate.py`, `test_bible_kb_regression.py`, and `bible_kb.gate(...)` is live in both `_animate_16x9.py:48` and `_animate_directional.py:66`). Reviewing it as a plan is therefore partly moot. I judged it as both.

## Findings

**1. Mis-framed: this is a built system, not a plan.** It's labeled "design (for panel review)" but it's already shipped and enforcing (it currently *blocks* EW01). A panel can't shape a design that's a fait accompli. This collides with the project's own "prove the idea before building" / "independent review BEFORE it's called done" discipline — the review here is a rubber-stamp, not a gate.

**2. The deterministic "teeth" don't bite the dog that actually bites.** The goal says check "location/time/place/customs/characters." But `over_reach_scan` (Layer 1, the *binding* bar) only flags colour/number/material descriptors from a hardcoded `_HIGH_RISK` set that are absent from the *cited* KJV. None of this project's logged recurring errors are colour/number/material: they're "witness over-claims an act Scripture assigns to another" (EW01 Lev 10 "I carried them out myself"), Joseph ten-brothers, Noah cubits, wrong actor/location. The one layer billed as fail-closed teeth catches *zero* of the actual defect class the 2026-06-29 re-audit found. That's the core substantive gap, not a nuance.

**3. "25 tests" is wrong — it's 18.** `test_bible_kb_regression.py` has 18 tests (all green, 0 parametrize). A trivially-checkable number is inflated ~40%. Undermines trust in the other round numbers.

**4. Layer-2 calibration "P=1.00 R=1.00 (n=8)" is theater.** Eight hand-seeded examples, detector tuned against them, same model auditing — circular and statistically meaningless (the CI at n=8 is enormous). The artifact half-admits this ("sanity signal," "independence is weak") yet still reports a perfect matrix, which reads as false confidence. Either drop the numbers or label them non-evidential.

**5. Staleness rests on filesystem mtime — fragile single point of failure.** `scene_plan mtime > facts mtime + 1` (`bible_kb.py:696`). git checkout/clone/worktree/copy rewrite mtimes arbitrarily — your current `git status` already shows dozens of churned files. A `git stash`/`checkout` can make stale facts look current *or* current facts look stale. The `+1`-second fudge is a magic number. A content hash of `scene_plan.json` stored in `scene_facts.json` would be robust; mtime is not.

**6. Going-forward-only + grandfathering = protects ~nothing today.** Every existing piece with no `_bible_check/` dir is skipped (`bible_kb.py:784`). The entire 32-narration corpus — the one that *just had 4 errors found* — is exempt. EW01, the sole adopter, has 6/25 scenes covered and so the gate blocks it (can't ship). Net current protection: future EW pieces only, and only once someone authors complete fact sheets.

**7. No cost/labor line for the thing the whole system depends on.** GREEN is unreachable without a complete, cited, hydrated SceneFacts sheet *per scene*. Authoring + citing those is the real (human/LLM) cost — and it's unestimated. "$0, every commit" hides that the binding input is expensive. EW01 blocking is the proof.

**8. Chokepoint ≠ ship-time.** Acknowledged in "known limits," but worth weighting: it's one stage (before-animate). A still swapped after animate, or a reuse-bank clip pulled at assembly, bypasses the check. Calling it "no still that contradicts Scripture gets... shipped" (the goal) overstates what a single before-animate hook delivers.

**Credit where due:** it genuinely *reuses* `bib_validate` / SceneFacts / the existing `.bib_audit.json` sidecars rather than duplicating them; the policy escape-hatch design (off/exempt/grandfather/warn/strict) is sensible; the fail-closed `assert_green` raises rather than warns by default. The architecture is fine. The problems are the over-claims and the coverage/teeth mismatch.

VERDICT: REVISE
TOP FIXES:
1. Make Layer-1 deterministic teeth cover the project's actual recurring error class (wrong actor / wrong location / wrong attributed act), not just colour/number/material — or stop calling colour/number/material the "binding bar" and be explicit that the real check is the per-scene image audit + human panel.
2. Correct the false numbers: "25 tests" → 18; drop or de-weight the "P=1.00 R=1.00 (n=8)" calibration claim as non-evidential; and re-label the doc as "built + wired" rather than "design for review."
3. Replace mtime staleness with a stored content hash of `scene_plan.json`, and add a coverage/cost plan for the grandfathered corpus (the pieces that actually had errors are currently all skipped) plus a ship-time (assembly/publish) gate, not just before-animate.
