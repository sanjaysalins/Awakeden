# Independent review — cursor (OK, 160s)

## Adversarial review — Swirls of Life season direction v5

### 1. `#12` is not “ready to build” — the plan overclaims against its own history and codebase

**Lines:** *"GREENLIT, build next"*, *"unchanged design, ready to build now — no plan overhead"*, *"already slate-approved"*

Problems:

- **No build artifact exists.** There is no `swirls_episode_12_*` folder; every other shipped short has one. “Slate-approved” ≠ design-brief-ready.
- **Not unchanged.** v4’s resolved high-tide design was **Stage 2 + D2** (“grace fully offered, not yet fully declared”). v5 silently switches to **“dose 1 while the room runs Stage 3”** — same math (`1+3=4`), different visual/theological page. Calling this *unchanged* is false.
- **QUAD lock still unresolved.** `NORTH_STAR_PROMPT.md` rule 2: stain and swirl **“never touch.”** Foot-washing is literal contact. Fable’s v3 review flagged this explicitly for #12; v5 never answers it.
- **v4 open risks dropped, not fixed.** v4 named **`pipeline/handoff.py` only writing `primary_ref`** as blocking #12 (John 13:1–30 span). v5 greenlights build without mentioning multi-ref handoff at all.
- **Prior panel required a visual spec first.** The 2026-08-21 independent review demanded page-level rules for an **unresolved Stain** (muted-watch test, within-clip persistence) before spend. v5 skips that and jumps to “build next.”

This is the plan’s biggest feasibility hole: it treats the hardest untested motif in the season as zero-overhead.

---

### 2. Process self-contradiction: panel gate for others, immediate spend for #12

**Lines:** *"has NOT yet been through `independent_review.py --type plan`"*, vs. *"Build #12 … next"*, *"In parallel, not instead: this v5 document goes to independent_review"*

The document requires panel review before **Part 2 NEW candidates** are scheduled, but recommends **immediate build of #12** — the episode with the **most untested motif behavior** and unresolved QUAD/high-tide questions. That inverts the caution the plan claims to introduce.

Also: the new standing gate (*"apply to every episode … at candidate-selection time"*) is never applied to #12 in v5; it inherits v4 selection and gets a bypass via GREENLIT.

---

### 3. Internal scheduling contradictions (the plan contradicts itself)

**A. Daniel 3 — double-listed with opposite instructions**

- *"Ready to plan now"* table includes **But If Not**
- *"Needs a build decision … do not schedule until panel-checked"* also lists **But If Not (Daniel 3)**

Same episode, opposite gates. The build sequence (*"Daniel 3 and Genesis 32 follow"*) treats it as scheduled while the flagged table says don’t.

**B. Isaiah 6 — season 1 vs season 2**

- Season-2 pool: *"A Man of Unclean Lips | Isaiah 6"*
- 18-episode table row: *"then | A Man of Unclean Lips | Isaiah 6"*
- Footer: *"first parable and first Acts episode deferred to season 2"* — but Isaiah 6 is **not** deferred in the table.

**C. “18 episodes” scope creep without cost authorization**

v4 explicitly: *"Per-episode planning bands only; no season-total spend authorized."* v5 adds 3 OT builds (Daniel 3, Genesis 32, Isaiah 6) with no cost bands, no OpenArt attended-bridge note, no per-episode fork estimate. That’s planning debt, not strategy.

---

### 4. `#14` “sketchbook turns back” overclaims what the format has proven

**Lines:** *"use the format's own native device — the sketchbook turns back to pages 4 and 5"*, *"No other format can do this"*

What actually shipped in ep 8 (`swirls_episode_08_can_any_good_thing/episode.py`): **“Episode 1's own ladder redrawn small as a pinned-up storyboard thumbnail”** — a **redrawn echo**, not compositing shipped clips from eps 4/5 into a literal backward page-turn.

There is no swirls pipeline for re-inserting prior episode MP4s/PNGs into a sketchbook turn. v4’s own risk table still applies: long-form is *"7 movements, 16:9"* with **no mapping to ~20–26 spreads, Focal Tour, or hero ratio** per `PRODUCTION_PIPELINE.md`. #14 is labeled **KEYSTONE** on unbuilt tooling.

Same problem for Genesis 32: *"sketchbook turns back to ep 3 (the Ladder)"* — ep 3 lives in `swirls_pilot_01_jacobs_ladder/`, nonstandard naming/path, making reuse even less mechanical.

---

### 5. KJV / text accuracy error on re-aimed #9

**Line:** *"He calls that 'great faith' (Matt 15:28)"* for **Mark 7:24–30**

Mark’s parallel account does **not** contain “great faith” — that’s Matthew 15:28. For a series bound to KJV verbatim and sound doctrine, anchoring a redesign on a cross-reference from the **wrong pericope** is a real defect, not a stylistic choice.

---

### 6. “No CTA” landing fix conflicts with binding project charter (unresolved)

**Lines:** *"Landing on 'and it was night' (13:30) — no CTA"*, *"fixes the landing-fatigue problem in one stroke"*

`data/constitution.md` defines shorts as **“CTA-to-Jesus”** with G8 requiring a takeaway that *“land[s] on a response to Jesus by grace.”* A deliberate no-CTA close may be artistically right for Swirls — but the plan treats it as settled without:

- a formal Swirls-vs-constitution exception,
- panel sign-off on format divergence,
- or verification that `narration_gate.py` / landing-hold checks accept it.

Landing fatigue is real; constitution conflict is unaddressed.

---

### 7. “Wax resist” — proposed grammar before visual proof

**Lines:** *"dry patch on a page otherwise at Stage 3, like wax resist"*, *"Needed before #14 builds"*

Good that it’s flagged for panel — but v5 still slots #14 as **KEYSTONE** in the 18-episode table while the grammar is explicitly undecided. Generative stills/animation are bad at **negative spatial constraints** (“swirl everywhere except this outline”). Prior review also noted v4’s #14 “crowd pushes swirl” behavior is neither Stage 0–3 dosing nor dead ink — a **fourth swirl behavior**. v5 tables it as `swirl S3 + resist(?)` without resolving the v4 animation-discipline tension (“camera moves only” vs crowd acting on ink).

Building season architecture on unproven negative-space rendering is premature.

---

### 8. Backlog cross-check claim is sloppy

**Line:** *"Cross-checked against the project's own 44-item narration backlog (`PythonProject1/jesus/narration/`)"*

That path currently has **~59 folders**, not 44. “Cross-checked … verified refs below, not guessed” overstates diligence.

**`He Never Said Yes *(confirmed backlog, John 5:6)*`** — the actual folder is **`18 He Never Said Yes`**, not #44. Minor numbering error, but it undercuts trust in the audit.

---

### 9. Genesis 3 “merge” ignores locked-pipeline friction

**Line:** *"merge these into one build, don't run both"* for `44_Grace_Spoken_First`

`44_Grace_Spoken_First/v1/` is **LOCKED** (`.locked`), with full **Baroque HF visual pipeline** — different format, different style, different spend profile than Swirls. “Merge” is not administrative; it implies **unlock → rewrite → re-gate narration → throw away or port visuals**. The plan treats it like deduplicating a backlog row.

Also: `poc_living_sketchbook/first_gospel_in_the_curse/` already consumes that narration for a **different** format — triple collision risk (Swirls + locked shorts + sketchbook POC).

---

### 10. New standing gate mostly duplicates existing machinery without enforcement

**Lines:** questions 1–2 restate constitution G8 Q4–Q5 almost verbatim; question 3 (intention) is the only genuinely new element.

No template, no gate script, no `$0` linter — just prose. Meanwhile the plan exempts #12 from re-application. Restating G8 at backlog time is fine; calling it a **“new standing gate”** oversells it unless operationalized.

---

### 11. Reuse claim for `papermakers-mark` is wrong pipeline

**Line (season-2 table):** *"`papermakers-mark` device already built for exactly this 'hidden presence' beat"*

`panel_animator/papermakers_mark.py` serves **Living Sketchbook / panel_animator**, not `swirls_page.py`. Assuming cross-format drop-in for a Swirls Mark 4 episode skips integration cost and style-match verification.

---

### 12. Missing verification steps v4 had and v5 dropped

v4 **Open Risks** table included items v5 omits entirely:

- No production pipeline integration (`PRODUCTION_PIPELINE.md` — per-episode fork, not `cli_visual.py`)
- Long-form shape underspecified (no one-movement spike requirement before #14/#15)
- Zero swirls 16:9 long-form precedent
- NSFW/cross render risk (still relevant if season expands)

Dropping known blockers while expanding scope is a regression, not polish.

---

### What the plan gets right (briefly)

- Talitha Jairus-POV redesign and outsider-fatigue diagnosis are strategically sound.
- Moral-vs-ceremonial Stain rebalance is correctly identified from shipped evidence.
- Flagging Daniel 3 / Gethsemane for doctrine-before-narration is appropriate.
- Open items 1–5 are honestly named (even if the build table ignores their implications).

---

VERDICT: REVISE
TOP FIXES:
1. **Withdraw “build #12 now” until QUAD-lock foot-washing, unresolved-Stain page rules, and v4 multi-ref handoff are specified** — prior Fable/panel findings still block spend; v5’s Stage 3/dose-1 change needs explicit re-design, not “unchanged.”
2. **Resolve internal contradictions before any schedule is trusted:** Daniel 3 (ready vs do-not-schedule), Isaiah 6 (season 1 table vs season-2 pool), and prove #14’s “page turn” as redraw/composite spec (ep 8 pattern) — not “native device” — before KEYSTONE commitment.
3. **Fix #9’s Matthew 15:28 citation in a Mark 7 frame; reconcile no-CTA landing with constitution CTA requirement;** restore v4 open-risks + cost bands for the 18-episode expansion.
