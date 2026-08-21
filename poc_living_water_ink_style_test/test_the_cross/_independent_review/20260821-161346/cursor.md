# Independent review — cursor (OK, 110s)

Independent adversarial review of **Swirls of Life v3** against the repo and the plan’s own claims.

---

## Feasibility vs. real codebase

**1. Pilot candidate contradicts the plan’s own multi-ref risk (line 67 vs. line 76).**

Build order recommends **Talitha Cumi** as a pilot with *“no multi-ref complications.”* The risk table names **#6 Talitha** (`Mark 5:21-24, 35-43`) as a multi-ref episode. Those cannot both be true. Talitha is also a **Mark sandwich** (Jairus interrupted by the woman with the issue of blood) — narratively and structurally heavier than “single-location, small cast” suggests.

**Better pilot per the plan’s own logic:** *The Ladder He Saw* (#3) — but that is **swirl-only**, which creates a different gap (below).

**2. Multi-ref risk is mis-scoped for swirls (line 76).**

The cited failure mode is `visual_runner._episode_from_creation()` rebuilding `refs` as `[primary_ref]` only:

```90:98:pipeline/visual_runner.py
def _episode_from_creation(d: dict) -> Episode:
    """The creation.json's `episode` block only stores title + primary_ref. We
    populate refs and theme with sensible empties — the scene planner gets
    the wider passage separately, so the episode block is mainly cosmetic."""
    return Episode(
        title=str(d.get("title", "")).strip() or "(untitled)",
        primary_ref=str(d.get("primary_ref", "")).strip(),
        refs=[str(d.get("primary_ref", "")).strip()] if d.get("primary_ref") else [],
```

Swirls explicitly **do not** go through `cli_visual.py` / `visual_runner`. The real swirls path still hits `handoff.py` (only persists `primary_ref`) and `runner.py` (fetches pericope window around **primary only**, not `episode.refs`). The risk is real for **narration/resume**, but citing `visual_runner` misdiagnoses it and invites the wrong fix.

**3. “Assembled through `northstar_shortform/`-style script” understates fork cost (line 67).**

`northstar_shortform/assemble.py` is a **Jacob’s Well POC fork** — hardcoded narration path, 8-shot beat map, shot stems, score reuse. `PRODUCTION_PIPELINE.md` lines 203–206 say assembly *“remains … hand-built assemble script, forked per episode.”* The plan treats “northstar-style” as a known path; in code it is still a **manual per-episode fork**, not a reusable runner. Pilot scope is larger than the prose implies.

**4. `swirls_page.py` path drift (line 77 vs. repo).**

Risk table references `swirls_page.py` as formalized. `PRODUCTION_PIPELINE.md` migration step 1 says `poc_living_water_ink_style_test/swirls_page.py`; the actual module is at `poc_living_water_ink_style_test/test_the_cross/swirls_page.py`. Minor, but it signals the plan and pipeline doc are not fully aligned on where the “single source of truth” lives.

**5. Long-form shape is asserted but not designed (lines 51–52, 79).**

`PRODUCTION_PIPELINE.md` long-form section: ~**20–26 spreads**, hero spreads ~**1/3**, rest **Focal Tour** (`focal-tour` skill). v3 says *“LONG, 7 movements, 16:9”* twice but never maps movements → spread count → hero vs. Focal Tour schedule → render budget. Risk table admits *“Neither #14 nor #15 has a swirls long-form precedent”* — accurate. There is **zero** swirls 16:9 long-form render path in `poc_*` (only `render_the_*_16x9.py` test pages for Hem/Thomas, not a 7-movement assembly).

---

## Hidden risks / false assumptions

**6. “Each independently verified clear” repeats v2’s failure mode without evidence (line 15).**

v3 correctly documents v2’s catalog miss (*“verse-literal search missed”* `the-empty-tomb`). Then it asserts the same confidence again: *“each independently verified clear”* — with **no inline collision matrix**, no search methodology, no manifest/narration-folder/`longform/`/`poc_*` crosswalk attached. I spot-checked refs in `_website/manifest.yaml`: no direct ref hits for most v3 picks — good — but **the plan does not prove that**, and v2 proved assertion ≠ audit.

Residual overlap not addressed:
- **#13 Simon of Cyrene** (`Mark 15:21`) — not a standalone shipped short, but **cluster_01_cross** fact sheets treat Simon as a checkable road-scene requirement; repeat-viewer overlap with cross content is likely.
- **#15 Emmaus** (`Luke 24:13-35`) — same chapter family as shipped **`women-first-witnesses`** (`Luke 24:5-6`, `studio_complete`). Not a duplicate story, but resurrection-cluster saturation the plan never discusses.

**7. Pilot gate does not prove what the season needs (lines 67–68, 78).**

Pilot candidates are **Talitha (Fray)** or **Ladder (swirl-only)**. Neither validates **Stain on new content** — the hardest validated family (Hem F04/F05 geometry, ceremonial-uncleanness sub-case). Step 2 says spread *“Stain/Fray/OT-NT variety”* after pilot, but exit criteria never require **one Stain + one Fray** on **new** pages in the pilot itself. Northstar/Jacob’s Well proved swirl-only assembly, not dead-ink grammar on this slate.

**8. #12 breaks validated ink grammar without a visual spec (line 42).**

*“The season's one Stain that does NOT clear”* is narratively strong but visually unplanned. `NORTH_STAR_PROMPT.md` / validated Hem work assumes stain **dispelled at hard cuts between pages** when grace lands. Judas’s unresolved stain needs page-level rules: Does stain persist **within** clips? Across pages while others clear? How does a viewer read “refused grace” vs. “grace not offered” **with narration muted** (the project’s own SP-G2-style test)? Martha was cut for inventing resolution; #12 risks inventing **visual** resolution rules without the same rigor.

**9. Long-form #14 introduces swirl behavior the “unchanged” system does not define (lines 11–13 vs. line 51).**

Dead-ink section: Stage 0→3 swirl + Stain/Fray only. #14 adds: swirl *“actively pushed toward the frame's edge by the crowd's own rising hostility”* while *“never dies, never dims.”* That is neither Stage 0–3 dosing nor dead ink — it is a **fourth, episode-specific swirl behavior**. Also tensions with animation discipline: motion is supposed to be camera/state-only; “crowd hostility pushes the swirl” sounds like **motif animation within a spread**, which prior swirls work explicitly avoids.

**10. #7 “Weep Not” as Fray is a taxonomy stretch (line 32).**

Fray is locked to *“fear/doubt only (James 1:6, Matthew 14:31).”* A widow weeping at her son’s bier is **grief**, not clearly fear/doubt. Jesus says *“Weep not”* — that is comfort before raising, not the Fray proof-text pattern used for Talitha (*“Be not afraid, only believe”* verbatim). Same class of mis-tag that caught v2 on Martha/shame — weaker, but real.

---

## Over-engineering / premature commitment

**11. Full 15-episode season architecture before one new-slate pixel (lines 15–54, 63–70).**

Cost discipline improved (*“No spend beyond one pilot short is authorized”*), but the document still locks **15 titles, motif assignments, long-form finale, and build sequencing** before any episode on this slate has rendered. That is planning debt if the pilot forces motif or page-count revisions — especially #12 and #14.

**12. Long-form spike suggested in risks but absent from build order (lines 69–70 vs. line 79).**

Risk table: *“Consider a shortened ‘one movement’ spike before committing either full long-form.”* Build order jumps from shorts → full #14 (7 movements) with no mandatory spike gate. The suggestion is orphaned.

**13. Diverges from `PRODUCTION_PIPELINE.md`’s stated next step without saying so.**

Migration path step 4: next real render is a **new Peace Be Still Fray page** through `swirls_page.py`, after open Thomas F02 issues settle — not a full new-slate pilot. v3’s pilot choice doesn’t reconcile with that sibling doc; two “what’s next” truths coexist.

---

## Missing steps / verification gaps

**14. Pilot lacks measurable exit criteria (line 67).**

*“Full page set”* — how many pages? Northstar used **8**; Hem validated **2**. No count, no required motif mix, no ref-chaining case, no caption-line-count stress (Kling **warns on 2-line captions** per `PRODUCTION_PIPELINE.md`), no `check_landing_hold.py` pass criterion, no caption step (prior reviews flagged captions as part of “whole pipeline”). “Ships clean” is not operational.

**15. No `series.json` draft, no thread/CTA patterns for new slate (implicit).**

v1 had a paste-ready `series.json` block with `hook_pattern`, `guardrails`, multi-ref `refs` arrays. v3 drops that entirely. For episodes like Talitha needing `refs: ["Mark 5:21-24", "Mark 5:35-43"]`, the plan never specifies `primary_ref` vs. supporting refs — the exact handoff failure it warns about.

**16. Governance acknowledged but not closed (line ~83 in artifact).**

*“Needs a fresh `independent_review.py` … before treating it as locked — not yet run.”* Correct — and this review is that pass. Plan should not be treated as locked until findings are addressed.

---

## Reuse

**17. Mostly good on distribution reuse; bad on underestimating assembly duplication.**

Distribution reuse claim matches `PRODUCTION_PIPELINE.md` (manifest, release_state, upload_tracker — style-agnostic). Good.

But the plan **does not reuse** any assembly orchestrator — each short forks `northstar_shortform/`. It also doesn’t reuse `cli.py`/`cli_pipeline.py` human gates for the visual track (deliberate, but means pilot reproduces manual POC discipline every time).

**18. Long-form should reuse Focal Tour — plan never schedules it (lines 51–52).**

`PRODUCTION_PIPELINE.md` says reuse `focal-tour` directly for non-hero spreads. v3 long-forms never mention Focal Tour, hero-spread ratio, or `$0` spread coverage — so long-form cost/feasibility is even thinner than the $50–95 band suggests.

---

## Cost / spend

**19. Per-episode bands conflict with project `/cost` ceilings (lines 60–61).**

`.claude/skills/cost/SKILL.md`: *“Stay under the per-episode ceiling (~$25 short, ~$40 long).”* v3: Short **$20–46** + **$5–6** narration (upper **~$52**); Long **$50–95** with *“zero ledger evidence.”* Upper bands exceed standing guardrails without reconciling why swirls earns an exception. Long-form band also ignores Focal Tour reducing paid hero spread count.

**20. Pilot cost not pre-flight quoted.**

Even with “one pilot authorized,” there is no page-count-based estimate tied to `hf generate cost` / `pipeline/cost.py` — the project’s INV-20 path. A “full page set” pilot at 6–8 pages × (still + animate) can silently exceed the short ceiling.

---

## What v3 genuinely fixed (not praise — accounting)

- Motif arithmetic (**5/5/3/1**) now matches the table.
- Martha cut, Syrophoenician fix, Emmaus finale replacing empty-tomb collision — real improvements.
- Pilot upgraded from “one still” to full short — correct direction.
- Season budget de-commitment — correct direction.
- NSFW Simon risk flagged — honest.

Those fixes don’t eliminate the gaps above.

---

VERDICT: REVISE
TOP FIXES:
1. Attach an explicit passage×manifest×narration×longform collision matrix (with search method) before repeating “each independently verified clear” — and drop Talitha as pilot unless multi-ref handling is specified and tested first.
2. Define pilot exit criteria: page count, at least one new Stain + one new Fray page, ref-chaining case, assembly fork checklist, landing-hold green, caption pass — and reconcile cost bands with `/cost`’s ~$25 short / ~$40 long ceilings.
3. Spec #12’s unresolved Stain and #14’s “hostile swirl” in the same visual grammar as `NORTH_STAR_*` (page-level rules, muted-watch test), add a mandatory long-form one-movement spike before #14/#15, and map long-form to hero spreads + Focal Tour per `PRODUCTION_PIPELINE.md`.
