# Independent review — claude (OK, 290s)

All of this plan's load-bearing feasibility claims check out against the real codebase — I verified each one rather than trusting the artifact. Findings below, then the verdict.

## Verified TRUE (checked, not trusted)

- **`pipeline/rollout_gate.py` exists and enforces exactly what the plan claims** — every machine-gated bullet (≤60% full-bleed at `rollout_gate.py:16`, ≥3 templates, still≤2 uses, adjacent-two-shot rule, fx≥50%, arc DIRECTION with the 7000K cool pole and ≤5500K warmest landing at lines 66–75, `…` in the slop tokens at line 25, ≥2 living_light, played-not-dyncam'd at lines 96–104, double-lighting at lines 91–95, landing lit at lines 105–108) is real code, not aspiration.
- **The gate IS wired into the runner:** `run_piece.py:343-353` refuses paid animate (exit 3) when any living_light piece fails `check_piece`. The plan's "no longer CLI-only" claim is true.
- **All 12 target pieces + the gold master have `livingpage_short.spec.json` on disk** (13 specs found; `father_forgive_them` correctly absent — it genuinely is a different format, so Wave E's separation is right).
- **Gate tests pass now:** 18/18 in `pipeline\test_rollout_gate.py`; full suite collects 312 tests, consistent with the "305+ passed / 1 skipped" claim.
- **The gemini rebuttal is correct:** `run_piece.py:34` really is the BytePlus ARK endpoint with `SEEDREAM_USD_PER_IMG`; gemini's "unsupported" flag was wrong.
- **The credits stop-loss is mechanically checkable:** I initially suspected a units mismatch (ledger in USD vs stop-loss in credits) — wrong; `pipeline/cost.py` logs `est_credits`/`actual_credits`, the summary totals credits per episode, and `reconcile` pulls the real HF transaction deltas. `summary --episode` exists (`cost.py:200`).
- **Phase 0 is committed** (bbe943f, per git log).

## Real problems

1. **The 485cr envelope has an ambiguous zero point.** "HARD STOP-LOSS: 485cr cumulative" sits next to "Spent so far: ~52.5cr pilot + promotion." Does cumulative include the 52.5? If yes, forward headroom is ~432cr and the hoped case (380cr) lands within ~50cr of the wall — a different picture than "inside it." A hard stop-loss with an undefined starting balance isn't hard. State the exact ledger filter (which episodes/kinds count) and whether pilot spend is inside or outside the 485.
2. **The Wave D "≈110cr" is the only underived number in the budget** — no breakdown of how many new stills × cost, or extra clips for empty_tomb/sign_of_jonah. It's also exactly the number that pushes worst case over the envelope, so it deserves one line of arithmetic, not a hand-wave.
3. **Gate trigger has a partial-migration window:** the runner gate fires only `if pj["animate"].get("living_light")` (`run_piece.py:346`). A piece whose spec is mid-upgrade but whose `piece.json` doesn't yet carry living_light entries can still take paid animate re-renders (e.g. hash-stale regular clips) completely ungated. The plan's per-piece ordering covers this only by discipline — the exact single point of failure the panel fix was meant to remove.
4. **Wave A's re-roll measurement is n≈6 clips.** The plan gates on a re-quote (good) but doesn't say how it will use a noisy measurement. Commit to forecasting B–D at max(measured, pilot 2.3×) unless Wave A shows a clearly better rate; a lucky 6-clip run shouldn't lower the worst-case number. (The wound/CU proof biasing Wave A hard is actually conservative — good.)
5. **Checklist #3 (doubled audio) is claimed un-gateable but probably isn't:** spec beat `sfx` keys vs the `_sfx.py` bed manifest is a $0 set-intersection check. Not a blocker, but "un-gateable" is asserted, not demonstrated.
6. **The plan proceeds under a DEGRADED panel** (grok/codex dead, 3/3 of surviving voices). It says the panel is re-running on this revision — fine, but Wave A start should be explicitly conditioned on that re-run's verdict, per the repo's own enforced-review rule.

Everything else — wave structure, human gates, backup-before-rebuild, Wave D's reuse-first ordering, Wave E separation — is sound and appropriately un-clever. This is a plan that survived its first panel round and actually incorporated the fixes; the remaining defects are budget-hygiene and one narrow gate window, all fixable on paper before a single credit is spent, and the re-quote gate after Wave A absorbs the budget uncertainty before it can bite.

VERDICT: PASS
TOP FIXES:
1. Define the 485cr stop-loss unambiguously: state whether the ~52.5cr already spent counts inside it, and name the exact ledger query (episode set + kinds) that the wave-gate check runs.
2. Derive the Wave D ≈110cr figure (N new stills × cr + N extra clips × 7.5cr) instead of asserting it — it's the number that breaches the envelope.
3. Close the partial-migration gate window: make `run_piece --stage animate` run `rollout_gate.check_piece` for ANY piece whose folder has a `livingpage_short.spec.json`, not only those already carrying living_light entries in piece.json.
