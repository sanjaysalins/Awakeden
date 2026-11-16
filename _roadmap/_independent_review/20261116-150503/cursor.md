# Independent review — cursor (OK, 230s)

## Independent adversarial review — `TWO_DRIVERS_ROADMAP.md`

### Feasibility vs the real codebase

**§2b “copy of `prophecy/01_bethlehem/fresh_hunt/`” is not a portable engine.** `run_seats.py` and `run_judges.py` hard-code that folder’s `BRIEF.md` / `CARDS.md` / `JUDGE_BRIEF.md` and import `independent_review` from `F:\slk\PycharmProjects\ArkAIology`, not this repo’s `independent_review.py`. A “1 hunt a day” rhythm still means **manual per-topic folder setup** every time, not a parameterized hunt CLI.

**§2b step 3 vs automation:** “6 seats (Fable + Sonnet + claude / codex / gemini / grok CLIs)” — the scripts default to **four CLIs only** (`ThreadPoolExecutor(4)`). Fable/Sonnet are ad hoc in Bethlehem (`hunt_fable.md`), not part of `run_seats.py`. The plan treats six seats as routine; the repo only automates half.

**§2b step 7 — `INSIGHT_BANK.md`:** marked “(new, simple table)” but **no such file exists** in `_roadmap/`. Banking is specified before the single artifact that makes the bank operable.

**§2b step 1 `/concordance-loom`:** The skill and `pipeline/concordance.py` are real and $0, but there is **no wired step** from loom output → `BRIEF.md` → `run_seats.py`. Step 1 is a skill invocation, not a repeatable script path in the prophecy lane.

**§8 `kjv_check_roadmap.py`:** Exists and matches the claimed 86/0 run, but **only substring/word-order checks**. Section 8 admits it does not verify narrative claims (e.g. T7 “Jesus leaves out ‘in whom I trusted’”, T9 “the judge tears his robe”). That conflicts with **§5** “All quotes below are exact KJV and machine-checked (section 8)” as if section 8 validated the **angles**, not just quoted fragments.

**§4 Tue “blind writers → judge table → 2-3 candidates → global-audience test → guardrail panel” for both episodes:** Bethlehem/Nazareth handovers show **multi-day** word rounds (`words/v3`, `v4`, guardrail film, re-voice). Cramming two full WORDS lanes into one Tuesday is not evidenced by prior builds.

**§2c score dimensions vs implementation:** Bethlehem’s `JUDGE_BRIEF.md` adds **FIT** (upgrade-an-existing-film). The plan’s universal gates (Q4, §2c) omit FIT and never say how hunt briefs are templated per driver or greenfield vs upgrade.

**GROWTH (§3) is not in §2c’s judge table.** Driver 2’s “bar: 7.0” has no hook in the blind-judge machinery unless every hunt copies a new brief — not specified.

### Hidden risks and false assumptions

**Hunt-first does not imply FRESH ≥ 7 on the finished film.** Bethlehem already ran §2b-style hunt ($0) and still got blind film **“new-to-you” 5.8** and overall **6.3** (`prophecy/01_bethlehem/HANDOVER_RESUME.md`). The plan’s leap from “hunt before lock” to **Q4 “FRESH 7.0 or more (median)”** is **unvalidated** on shipped prophecy shorts.

**§4 vs §4 (contradiction):** “Owner gives about **15-30 minutes a day**” vs per-episode “**60-90 minutes**, spread over 4-5 small decisions” × **2 films/week** ⇒ **~2–3 h/week minimum**, before ear-checks, clip pages, and pack approval. The daily cap is aspirational, not budgeted.

**§183 bank rule vs §267 order:** “The bank should hold **6+ passed insights** before we worry about speed” but **Week 1** immediately commits to ★ **T7** and ★ **E2** without a bank or passed hunts. You’re back to **topic-first production** for the flagship triple.

**§251 overlap audit admitted failure:** “I could not confirm from file names alone that **E4, E8 and T5** have no overlap” — yet **24 candidates** are published with KJV-checked quotes, inviting sunk-cost attachment before dedup against eyewitness/Swirls/living-sketchbook corpus (e.g. storm “pass by” / E7 is already concordance-loom folklore in STATE).

**★ T7 as “lowest risk of a doctrine stretch” (§249)** is inconsistent with the angle: David–Ahithophel–Kidron–Olivet–hanging mapped onto Jesus–Judas, plus **“first friend to betray a king”** (§198) — not stated in the cited KJV pack; Psalm 41 does not name the friend. Section 8 flags psalm honesty but not the **David typology** or **Ahithophel→Judas** imputation. This is exactly where **ECHO sounds like prophecy** (§6 risk row).

**★ E2 “needs no outside claim” (§249)** vs the row: **Leviticus + Hebrews 13:12** — outside Mark 1 and typology many sermons already preach (“swap places”). Week-1 “deepest / lowest risk” pairing is **marketing**, not measured FRESH.

**§125 E8 “He said ‘when’, not ‘if’”** — Luke 22:32 KJV does not contain “if”; the insight is **editorial**, not machine-checkable. Plan punts exegesis to judges while claiming machine spine (Q3).

**Six AI judges for FRESH (§2b.6)** correlates with the same models that **proposed** the angles (§2b.3). §2d “Ask real people” is optional-adjacent; **60%+ seed “No”** is a measure (§6) but not a **hard gate** like Q4. AI FRESH can pass while humans say “Sunday school.”

**§6 “AI judges … likely off by 1-2 points”** undermines Q4’s precision while Q4 blocks spend — calibration risk is acknowledged but **not designed into the gate** (no anchor cards, no human tie-break rule).

### Over-engineering / premature scale

**§5 “24 episodes”** with working titles, labels, and “fresh angles” before the hunt engine is generalized is **reverse order** of §0 (“hunt the link first, only make the film if the link is strong”). You’ve pre-built a curriculum that will fight the **30–40% hunt fail** rate (§6) psychologically and in scheduling.

**Five named scores + four Driver-2 “so what” tests + seven Q-tests + spoken labels + seed viewers + YouTube retention (§6)** — heavy governance for a lane that still lacks `INSIGHT_BANK.md` and a topic-agnostic `run_hunt.py`.

**§4 three lanes at full speed** (hunt daily + 2 words/week + 2 films/week) before **one** greenfield episode completes the full hunt→words→film→publish loop under the *new* Q1–Q7 contract is scaling process ahead of proof.

### Missing steps, edge cases, verification gaps

**No deterministic SOUND gate** despite “All PASS” bar (§2c); only LLM judges. Main engine has `narration_gate.py`, `bible-check` skill, eyewitness gates — **not referenced** for Salt prophecy lane. Q3 covers quotes only.

**Q2 “the film says the label out loud”** — no visual/word-count or guardrail-film question template in the plan (Bethlehem guardrails never asked “what kind of link was this?” as §6 claims for ECHO risk).

**Q1 “Driver 1 needs one OT + one NT”** — several rows lean on **DETAIL/ECHO** with 3–5 refs (T3, T7, E11). Unclear whether extra books must be quoted or only the two anchors.

**“Blind film check on both” Saturday (§4)** while still hunting topics 3–5 same week — no failure mode when film check FAILs and hunts are already queued.

**Immanuel “about $2.47 through clips” (§165)** vs handover **~$4.09 and incomplete** (score/SFX/panel pending) — **understates** cost basis for the $8–14 band.

**Doctrine “both ways” (§66)** — plan does not require **`independent_review.py --type narration`** on each locked script, only hunt judges; conflicts with enforced EXTERNAL panel in `CLAUDE.md`.

**§2a DETAIL (kind E)** in Driver 1 table vs Driver 2 — Driver 1 episodes that are mostly ECHO (T5 Genesis 49) need explicit **headline label rule** when PROPHECY and ECHO coexist (rule in §2a exists but T5 title is prophecy-framed).

### Reuse

**Good:** `kjv_check.py` reuse, `narration_gate.py` ban row, concordance-loom, Bethlehem hunt as pattern, ledger quote discipline.

**Bad:** `run_seats.py` pulls **`ArkAIology`** while this repo has **`JesusInTheBible/independent_review.py`** — duplicate, wrong default path, fragile on any machine that isn’t yours.

**Missing reuse:** `pipeline/kjv_check.py`, `bible-check` skill, prophecy’s existing **guardrail_film_*** folders as the required “blind film check” spec — plan names it but doesn’t point to the established builder pattern.

### Cost / spend

**$8–14 per short** is plausible for Bethlehem **after** many $0 iterations (handover ~$7–8), but **not inclusive** of rejected hunts, re-voice, re-score, reroll images, or owner time. **§165 Immanuel** shows cliff-line quoting (“through clips”) can mislead go/no-go.

**“1 hunt a day | $0 (uses CLI plan usage)”** — six hunts + six judge runs + words + guardrails × 2/week will **compete** with film work for the same CLI quotas; plan has no throttle when usage limits hit (single point of failure).

**Month $65–110** assumes stable $8–14; T7/E2-style multi-verse comics may exceed Well/Bethlehem if clip count rises — not sensitivity-tested.

---

**Strong parts (not letting you off the hook, but fair):** §0 bar (“old in the text, new to the viewer”), label taxonomy §2a, ban table §1, fail-cheap hunts, quote-before-yes, and honest §6 retention unknown are aligned with repo values. The weakness is **operational closure and evidence**, not the thesis.

VERDICT: REVISE  
TOP FIXES:  
1. Generalize hunt infra (per-topic template + use repo `independent_review.py`, create `INSIGHT_BANK.md`, define hunt PASS = all §2c bars + human seed rule) and **run one pilot (not ★ T7)** end-to-end before Week-1 schedule or 24-episode table.  
2. Reconcile evidence: Bethlehem hunt + film FRESH **&lt; 7** — either lower the bar, add **hard** human FRESH gate, or separate **angle FRESH** from **film FRESH** with explicit rework loop when Saturday blind film check fails.  
3. Demote or rewrite ★ **T7** and **E2** until overlap audit and SOUND review (David–Judas chain, “first friend”, leper swap); extend `kjv_check` or a **FACT manifest** for non-quoted claims (omitted psalm phrase, when/if, typology steps); fix §5 vs §8 honesty so “machine-checked” cannot mean “angle verified.”
