# Independent review — cursor (OK, 106s)

# Independent adversarial review — E2E Workflow (comic-strip-native)

This plan is more honest than its parent spec about gaps, runbook status, and cost ceilings. It still contains **blocking feasibility errors**, **false history**, and **inherited doctrine/tooling mistakes** that would waste spend if someone followed it literally today.

---

## 1. Stage 3 is architecturally broken as written (fatal)

**§7, lines 336–371** proposes word-timed `grid_choreography` over “live panels” on each page. That does not match what the tool actually consumes.

`panel_animator/grid_choreography.py::render()` takes **`clips: list[Path]`** — one **separate clip file per grid cell** — and composites them into a 2×2 (or other) layout. It does **not** accept one whole-page MP4 and rack focus across panels inside it.

But **§6e** animates **one 5s clip per whole page**. So Stage 3’s proposed reuse is a shape mismatch, not “exactly the move a comic-strip-native page needs.”

**Duration is also unresolved.** §6a maps Page 2 to **18–52s (~34s of narration)**, but §6e fixes animation at **5s per page**. Three pages ≈ **15s of motion** for a **~59s** short. §7 never states hold/loop/speed/extend strategy, panel-level re-clip strategy, or how SACRED STILLNESS spans 34 seconds. Calling this “$0 ffmpeg/PIL compositing, same as living-page” overstates reuse; living-page builds **many word-timed beats** from **`livingpage_short.spec.json`**, not three 5s blobs.

**§7, line 357** claims word alignment is “already produced at Stage 1b.” That is **false against the codebase**: `pipeline/handoff.py` does not write alignment; forced alignment is produced later via `pipeline/assembly_align.py` (e.g. `assembly_runner.py` Stage A1b). Stage 3 as proposed has **no step to generate `alignment.json`**.

**Hero bookend gap:** §7 mentions only “**hero close**” (lines 361–363). Locked AS-G6/AS-G7 require **open AND close** on the gospel-pivot. This plan never specifies the opening bookend.

---

## 2. §14 repeats a disproven claim and proposes a “next experiment” that already ran

**§14:** *“Comic-strip-native has never been tried against a locked EXTERNAL reference image — only page-to-page self-chaining within one piece.”*

That is **factually wrong**. `poc_thief_e2e/_comic_strip_native.py` (2026-07-24) explicitly runs `strip2_promise_ref` with `CHRIST_REF` chained via `--image` — the exact experiment §14 then labels “untested.” Results/outcome are not incorporated; the finding was silently dropped from the narrative.

This compounds the parent spec failure you flagged. It also **contradicts §6c** (“page 1 has no `--image`”) without stating which recipe is production-default vs experimental.

---

## 3. Inherited Christ body-gate problems (compounds COMIC_STRIP_NATIVE_SPEC failures)

**§6b / CSN-G3 (lines 236–237, 268)** inherit the parent spec’s anchor wording and gate text, which **conflict with `v2/AWAKEDEN_COMIC_DNA.md` §5a**:

| Issue | This plan | AWAKEDEN §5a |
|---|---|---|
| Beat split | CSN-G3 applies one passion rule “EVERY passion-beat panel” | **GLORY beats** (resurrection/gospel pivot) allow triumphant register; passion-only restrictions |
| Prompt phrasing | §6b says anchors carry Christ body gate “§2a” with repeated **negated** “NO blood / no wounds” language (via parent spec) | **Positive end-state only**; negated nouns can **draw** forbidden content; SP-G5 substring match has no negation awareness |
| Enforcement | “Human eye only” (CSN-G1–G5) | Passion Christ frames should be **Vision-checked** to FAIL idealized musculature + bright blood |

The plan acknowledges recurrence of body-gate violations (§6b, CSN-G3) but keeps the same prompt strategy AWAKEDEN already rejected.

**§6e** then **accepts animation invention as a named cost** on whole-page Kling clips. For passion/Christ panels, invented gestures are a **doctrine problem**, not just aesthetic noise. CSN-G5 is human eyeball only; there is **no equivalent** of `assembly_render.py`’s sacred Vision verify on finished gospel-pivot frames. Pre-still QC does not protect post-animation invention.

---

## 4. Missing NSFW / hybrid fallback — single point of failure for the primary genre

**§6e** standardizes on `hf generate create kling3_0` for whole crucifixion pages. The plan is **silent** on HF NSFW rejection for bare-torso/cross content — a known production blocker documented in `pipeline/video_render.py` / `HybridVideoProvider`, and already flagged in prior independent reviews of the parent spec.

Every POC script handles `NSFW-REJECTED` locally; this orchestration doc does not say what happens when animation fails on the exact subject matter (Penitent Thief, passion pages) the technique targets. That is a **hidden SPOF** not priced in §16’s “before reroll budget” table.

---

## 5. Conflicts with parallel locked visual identity work (AWAKEDEN)

**§7** anchors Stage 3 on **`build_livingpage_16x9.py` + `grid_choreography`**.

**`v2/AWAKEDEN_COMIC_DNA.md` §6** (user decision 2026-07-23) explicitly says retro/comic DNA does **NOT** extend the living-page Python/ffmpeg engine; **Remotion stays its own separate engine**, with word-timing rebuilt on the Remotion side.

**§19 item 21** flags AWAKEDEN vs comic-strip-native as unreconciled — but §7 still treats living-page as “the much closer existing analog” without resolving that **approved direction fork**. Risk: building Stage 3 on the wrong engine family.

---

## 6. Over-scoped E2E before the core idea is proven

The document honestly labels Stage 2 as hand-run and Stage 3 as unbuilt — good. But it still sequences **Stages 5–8 (thumbnail → upload → website → release sync)** as a coherent “topic → published website content” path while **Open Items §19** admits:

- Full end-to-end assembly **never built** (item 3)
- CLI wiring **does not exist** (item 12)
- Character/world-bible **not proven cross-piece** (item 15)

That is **premature end-to-end packaging**: publish/website/release mechanics are real, but attaching them to an unproven visual+assembly core implies a production lane that does not exist. A skeptic would stop after **one 60s cut exists and passes landing hold + sacred-frame check**, not after website cutouts.

---

## 7. Reuse claims that overstate or duplicate

- **§6e / §7 crop-and-recomposite:** correctly flagged “never tested,” but the plan recommends **whole-page Kling as default** while also naming crop-and-recomposite as the path that could **actually** feed `grid_choreography`. Those are **mutually exclusive product architectures**; the doc does not pick one.
- **§6b fact-card reuse:** sensible proposal, but **unbuilt**; meanwhile the old lane gets `verify_image()` Vision audit per PNG — comic-strip-native drops that for human-only CSN gates.
- **POC scripts vs production:** §18 admits hand-run `hf.exe`; no proposal to extend `visual_render.py` / `video_render.py` / `cost.check_budget` — guarantees drift from production behavior (estimator vs billed credits, NSFW handling, ledger paths).

---

## 8. Cost model: partially honest, still under-budgets real pieces

§16 improves on the parent spec’s internal typo (`~$1.20` vs `~$1.13–1.31` in COMIC_STRIP §8 line 454). Good.

Still missing from **§16 “≈ $10–12/piece”**:

- Still rerolls (body gate recurrence, §6b)
- Animation rerolls for doctrinal invention (§6e accepts this)
- NSFW fallback path cost
- §5.3 crop experiment (~$12) if whole-page animation fails acceptance
- **§6a panel-count ambiguity:** validated technique is **4-panel pages** (parent spec §4); Penitent Thief POC also used **3-panel** pages — page count ≠ panel count; 3 pages × 4 panels = 12 animated units if crop path is chosen

§16 correctly says `$25/short` is **advisory, not enforced** for this lane — but then compares to LP-BUDGET as if the comparison matters operationally.

---

## 9. Verification / gate gaps

| Gap | Where |
|---|---|
| **CSN-G6** referenced in §18 summary but **never defined** (only G1–G5 exist) | §18 table |
| Stage 3 has **no gates** despite SACRED STILLNESS / hero / landing hold dependencies | §7 lines 365–367 |
| **§12** calls `build_study_figures()` “honest infrastructure” but **`STUDY_FIGURES_ENABLED = False`** in `_website/build_catalog.py` — study illustrations are globally off, not merely “untested for comic pages” | §12 lines 551–553 vs code |
| No **`check_landing_hold.py`** in the Stage 3→3b handoff despite INV-26 dependency on build/score order | §8 mentions INV-26 only at 3b |
| No **`panel_variety_lint`** / multi-panel redundancy check for native 4-panel pages | entire doc |
| **`independent_review.py --type plan`** listed in Provenance as “not yet done” while this review is happening — fine, but visual stage has no external panel equivalent before spend | Provenance |

---

## 10. Smaller but concrete issues

- **§1 line 65:** “2d Animate each page (**Kling 3.0 direct**)” but command is **`hf generate create kling3_0`** — HF path, not `image_to_kling.py` direct-Kling. Terminology will cause wrong fallback behavior.
- **§6c backward reroll** “validated once” — high operational risk presented as protocol.
- **§9 caption default (WhisperX ivory lower-third)** is a defensible first ship, but the plan underweights legibility risk on dense ink linework; user interest in comic-aware captions is noted then deferred — OK, but Stage 4 is load-bearing for comprehension because §3 banned all baked text.
- **§13 SYNC-G8:** correctly notes `"unknown"` art style — good catch, low urgency.

---

## Summary

The plan’s strengths: explicit DRAFT status, runbook honesty, image-gate-before-Kling mirroring, open-items list, caption-policy reasoning, cost-ceiling honesty, cutout/study-page risks flagged.

The blockers: **Stage 3 cannot work as described**, **§14 falsifies experiment history**, **Christ gate + animation invention + NSFW path inherit or worsen parent-spec failures**, and **AWAKEDEN/living-page/Remotion fork is unresolved** while still proposing living-page tooling for assembly.

This is not shippable as an operational workflow until Stage 3 architecture, alignment generation, and cross-piece character locking are specified with a single chosen animation path (whole-page vs crop-and-recomposite).

---

VERDICT: REVISE
TOP FIXES:
1. Replace §7 with a concrete 60s timing spec: how 3×5s page clips (or 12 panel clips) cover ~59s narration, how `alignment.json` is generated, and whether build uses whole-page holds, per-panel crop+`grid_choreography`, or Remotion — pick one architecture; do not cite `grid_choreography` unless inputs match its API.
2. Correct §14: document that `poc_thief_e2e/_comic_strip_native.py` already tested external `CHRIST_REF` on page 1; report pass/fail; reconcile with §6c page-1 chaining; define the production default for cross-piece Christ locking.
3. Align CSN-G3 + anchor prompts with `AWAKEDEN_COMIC_DNA.md` §5a (glory/passion split, positive-only phrasing, Vision enforcement), add NSFW/hybrid animation fallback for passion pages, and add sacred-frame doctrine verification after animation — not just pre-still human eye checks.
