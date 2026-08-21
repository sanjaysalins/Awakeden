# Independent review — claude (OK, 260s)

## Independent review — Swirls of Life v3 series plan

I checked the plan's own citations against the live repo rather than taking them on faith.

### 1. The pilot-episode pick contradicts the plan's own risk table (Feasibility / internal consistency)

**Build order** says: *"Candidate: **Talitha Cumi** or **The Ladder He Saw** — both single-location, small cast, no multi-ref complications."*

But the **Open risks** table two sections earlier says: *"Multi-ref episodes will silently lose supporting passages... Affects **#6 (Talitha, two Mark chunks)**, #14..., #2..."*

Talitha Cumi *is* #6. The document picks it as the pilot specifically *because* it claims no multi-ref complications, while its own risk table names it as an example of exactly that bug. I verified the underlying technical claim is real: `pipeline/handoff.py:121` writes only `episode.primary_ref` (a single string), and `pipeline/visual_runner.py:97` reconstructs `refs=[primary_ref] if primary_ref else []` — genuinely single-ref only. Mark 5:21-24 (Jairus asks) and 5:35-43 (the raising) are separated by the intercalated bleeding-woman pericope (5:25-34) and sit outside the documented ±8-verse `PASSAGE_WINDOW` from a single verse anchor — so the risk-table's own concern is plausible, and the build-order section's claim it doesn't apply to Talitha is simply wrong. If this ships as written, the pilot — the one gate the whole slate depends on — is picked on a false premise.

### 2. The motif-balance tally is wrong, the same failure class v3 claims to have fixed

*"Motif balance: 5 Stain (one deliberately unresolved) · 5 Fray (including Emmaus) · 3 swirl-only · 1 motif-free. Counts checked against the table this time, not just asserted."*

5+5+3+1 = **14**, not 15. I re-tallied against the actual table rows: swirl-only = #1, #3, #9 (3); Stain = #2, #4, #10, #11, #12 (5); Fray = #5, #6, #7, #8, #15 (5); motif-free = #13 (1). **#14 ("This Day Is This Scripture Fulfilled") never gets a dead-ink category at all** — the Long-form table has no "Dead ink" column, and its prose description ("the swirl is actively pushed toward the frame's edge... it never dies, never dims") describes the *living* swirl under pressure, not a Stain/Fray assignment, and isn't swirl-only either since something is clearly happening to it. It's simply missing from both the table and the count. This is precisely the "plan cannot count itself" failure that gemini and codex both flagged as fatal on v2 — reintroduced in a new spot, directly under a sentence claiming the counting was fixed. That claim is false as written.

### 3. A FAIL verdict is dismissed by unverifiable assertion, not resolved per the project's own governance rule

Open risks: *"One reviewer (gemini) flagged this as a FAIL on principle — that tradeoff was made deliberately with the user earlier the same session, not an oversight."*

I confirmed gemini's actual verdict was FAIL (not REVISE) on exactly this point, and codex independently also returned FAIL, both calling the `swirls_page.py`-bypasses-`cli_visual.py`-gates decision fatal. CLAUDE.md's own rule is: *"A REVISE I disagree with goes to the user, not silently ignored"* — this document self-adjudicates a harder FAIL verdict with a claim of user sign-off that has no citation, timestamp, or artifact anywhere in `_independent_review/20260821-141811/` or elsewhere I could find. That may well be true, but as written it's not verifiable from the document — it reads as a first-person assertion overriding two independent FAILs.

### 4. Unresolved-Stain design (#12) isn't checked against the project's own NON-NEGOTIABLE grace framing

CLAUDE.md locks: *"Grace-anchored conviction — NO gain/loss / self-interest framing, NO manufactured pressure."* #12's stated purpose is explicit contrast-by-design: *"Retroactively, every OTHER resolved stain in the season means more."* A motif built so one character's ink is permanently unwashed specifically to make the others' cleansing feel more valuable is gain/loss framing at the visual-motif layer, even if narration-level G-gates catch bad CTA copy. It isn't in the Open Risks table at all, despite that table existing to surface exactly this kind of thing.

### 5. Minor: the "Fable creative pass" citation isn't traceable

*"A Fable creative pass and a 4/5 independent-review panel... Full detail: `_independent_review/20260821-141811/` and the Fable critique referenced there."* I globbed the whole `poc_living_water_ink_style_test/test_the_cross/` tree for anything Fable-related — nothing exists except the word "Fable" appearing inside `cursor.md`/`codex.md` (the CLI-panel transcripts, which reference the project's own locked Fable-pass convention, not a standalone Fable review output). There's no retrievable Fable-pass artifact backing the specific findings attributed to it (the "shame at being served" mistag, the Martha resolution gap).

### What's solid
The collision-audit fix for the empty-tomb/Melchizedek/Walking-on-water overlaps checks out — I confirmed `the-empty-tomb.html` is John 20:8/Mary at the tomb (a real match to the v2 finale collision), and none of v3's 15 refs collide with `data/series.json`. The Syrophoenician-woman doctrine fix (swirl-only instead of "Stain — Gentile outsider status") is a real, correct fix. The no-season-spend / pilot-first framing is appropriately cautious.

VERDICT: REVISE
TOP FIXES:
1. Fix the build-order/risk-table contradiction: either drop Talitha Cumi as pilot candidate or drop the multi-ref risk claim against it — they cannot both stand, and the pilot gate is load-bearing for the whole slate.
2. Recount the motif balance against the actual table (including assigning #14 an explicit dead-ink category) and correct the "counts checked" claim, which is currently false.
3. Replace the unverifiable "made deliberately with the user" claim with an actual citation/decision record before treating gemini's and codex's FAIL verdicts as resolved, and add #12's contrast-by-design framing to the Open Risks table against the project's grace-anchored NON-NEGOTIABLE.
