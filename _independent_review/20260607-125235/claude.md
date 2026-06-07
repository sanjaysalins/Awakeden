# Independent review — claude (OK, 181s)

I verified the plan's load-bearing claims against the actual codebase. Here's what I found.

## Claims verified TRUE (the plan is honest about the code)
- **`_extract_spoken.py` fail-open** — confirmed: lines 20-23 only keep text inside `## MOVEMENT`; the real short #1 uses `**[narrator]**` with no `## MOVEMENT`, so it returns empty. The motivating defect is real.
- **Ps 22:7 cache corruption** — confirmed: cache holds `"…shake the head saying,"` (no comma). The v2 correction is also right: **Acts 8:35 is clean in the cache** (`"Then Philip opened his mouth…"`).
- **Engine already gates conviction** — confirmed: `engine.py` G3 "creates holy tension and pierces" and G8(3) "the conviction beat actually PIERCES." Deferring Fix 5 (Phase D) is the correct call; v1's premise was genuinely wrong.
- **Rule-8 is short-specific** — confirmed: `quote-count-rule8` in `defect_classes.json` literally says "KJV renders at fixed pace… >2 quotes rushes the narrator / blows 60[s]." Short-only scoping is right.
- **kjv_check ignores NT cross-refs** — confirmed: lines 13/19/88 skip low-overlap/cross-ref quotes as "ignored." B4's NT-vs-its-own-verse fix targets a real gap.
- **G5 would false-FAIL hand-authored content** — confirmed: G5 requires beat_ids in order + proof beat carries the quote + word budget. C1's "no five-beat coercion" is justified.

**All 10 v1 convergent findings are genuinely resolved in the design.** Not cosmetically — each maps to a real code fact I could check.

## NEW problems v2 introduces or leaves open

**1. The "witnessed full-Bible canon" (B2/B3) over-engineers against the plan's own Phase-A-first logic.** B3 asserts "a ref missing from a *full-Bible* canon means the canon build is broken." But the locked content quotes ~30 verses. Cross-source punctuation-diffing a full KJV (~31,000 verses) will surface *hundreds* of legitimate edition divergences, each routed to "human adjudication" — unbounded manual cost, unquantified. The cheap, consistent move is a **scoped canon: witness only the quoted + planned-cluster refs first**, identical fail-closed behavior, a fraction of the work. B1 (audit-what's-actually-corrupt) is the right off-ramp — but B2 ignores it and builds the full canon anyway.

**2. The new defect classes are inert by the plan's own admission.** I confirmed `panel_misses` is **read** (`learning.py:56`) but has **no writer anywhere**. So adding `cluster-repetition` / `catalogue-phrase-reuse` to `defect_classes.json` (C2) is bookkeeping that the calibration loop can never observe. The plan flags this ("if absent… tracking is inert") but still lists the additions as if they feed learning. State plainly: **the cluster gate (A2) is the only real guarantee; the defect-class entries are dead vocabulary until a writer lands.**

**3. "Reuse `independent_review.py`" (A2) undersells real CLI surgery.** I checked: it's hardcoded single-artifact — `art = Path(args.artifact)`, one `{artifact}` format slot, `--type` `choices=["narration","plan"]`. Cluster review needs N artifacts concatenated + a new lens + a new type + the choices list edited. Feasible, but the plan doesn't say *how* N artifacts reach the CLI (concat to a temp file? new `--artifacts`?). Specify it.

**4. Whitelist vs the acceptance test is a latent contradiction.** A2 whitelists "Come to Him" as load-bearing gospel vocab — but A3 *demands* the gate flag 8× "Come to Him." This only holds if exact-match operates on the **full CTA sentence/clause** (which the plan does say) and the whitelist applies **only** to the near-dup/semantic layer. Make that explicit, or the two requirements collide.

## Minor
- The headline cache bug (Ps 22:7 comma) is **interior** punctuation — but no shipped short actually quotes 22:7 (short #1 quotes 22:18). The real integrity check is B1 over the *actually-quoted* spans (22:18, John 19:24, etc.). Fine — B1 covers it — but the marquee example isn't in any locked short.
- `_finalize.py` is at repo root, not `pipeline/` as the prose implies. Trivial.

## Judgment
The substantive v1 findings are all resolved, the design is fail-closed, there's no auto-rewrite (human approves every rewrite), and the off-ramps (B1 before B2, A3 gates the whole effort) are real. The remaining issues are **scoping and honesty refinements**, not safety or doctrine flaws. Safe to implement once the canon is scoped down and the inert-defect-class claim is corrected in the text.

VERDICT: PASS
TOP FIXES:
1. Scope B2/B3 to a **witnessed canon of only the quoted + planned-cluster refs** first (drive it off the B1 audit); defer any full-Bible canon until that's proven — building the full witnessed Bible now contradicts the plan's own "prove the cheap catch first" discipline and creates unbounded manual adjudication cost.
2. Correct C2's wording: with **no `panel_misses` writer** (confirmed — `learning.py:56` only reads), the new defect classes are dead vocabulary; state that A2 is the real guarantee and either add a writer or mark the classes bookkeeping-only.
3. Specify the multi-artifact mechanism for A2's `independent_review.py` (it's hardcoded single-artifact, `--type` choices fixed) and make explicit that the cluster whitelist never suppresses exact full-CTA-sentence matches, so it can't defeat the A3 acceptance test.
