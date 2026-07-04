# MOTION-COMIC SPEC v1.1 — the inked graphic-novel build pattern (binding for SHORT; PROVISIONAL for LONG)

> **Relationship to the contract.** Binding pattern for the **inked graphic-novel
> motion-comic** visual line. Extends `v2/SPEC.md` (master) + `v2/LONGFORM_SPEC.md`
> (long-form). All invariants INV-1..25 apply unless overridden here; where this and
> those conflict **for motion-comic work**, this wins. Skills in `.claude/skills/`
> are the procedures; this is what they enforce.
>
> **Status (v1.1, revised 2026-07-01 after a 4-reviewer red-team — 3 adversarial
> agents + the 5-CLI panel, all REVISE/FAIL, now addressed):**
> - **SHORT (9:16) rows are BINDING** — proven by the LOCKED Cluster 1 pilot
>   ("Father, forgive them", `batches/cluster_01_cross/father_forgive_them/`).
> - **All `[LONG]` (16:9) rows are PROVISIONAL** — validated by ONE manual long pilot
>   (Psalm 22, in progress) passing the doctrinal 5-CLI panel + the 4-lens review +
>   the reverence budget (MC-R10/MC-G7/MC-G10). **The gravitas A/B vs Baroque is
>   RETIRED** (user decision 2026-07-01: the inked motion-comic is a deliberate new
>   direction, chosen on the still comparison — not something to bake-off against oil
>   painting). The Baroque path remains available for other episodes but is no longer
>   the yardstick the inked long must beat. The inked long is now THE direction; the
>   pilot proves it out *mechanically*, not against Baroque.
>
> **Reuse-first economics (the whole point of cross-short-first):** the long reuses
> the already-built 9:16 short clips NATIVE in rails wherever topically-fitting
> (MC-R7), and renders FRESH 16:9 inked stills only for hero cells. Psalm 22 shares
> the cross world with the LOCKED short, so its garments/lots (Ps 22:18), mockers,
> pierced hands (Ps 22:16), David's scroll, darkness and risen close reuse the
> pilot's clips directly.

---

## 1. Purpose, scope & the long-look selection rule

One visual language — **flat inked art, held by camera-only motion, in comic grids
with kinetic captions** — at two sizes: **Short** (9:16, ~60s, first-class product,
INV-14) and **Long** (16:9, 6–8 min deep-dive, research foundation, LF-INV-1).

**Two long-form looks now coexist; the choice is gated, not arbitrary
(`scene_plan.header.style`):**
- `baroque` → **DEFAULT** for reverent Types-&-Shadows exegesis (validated: Isaiah 53
  et al.). Painterly plates + veo3.
- `graphic_novel` → shorts (binding) and **narrative/eyewitness or explicitly-opted
  longs (provisional)**. Inked stills + Kling camera-only.
A long may use `graphic_novel` only with an explicit header flag AND a passing
gravitas gate (§9); the scene-plan header validator enforces this.

The Baroque path is NOT retired by this spec.

---

## 2. The pipeline (both formats)

Same stage spine as `v2/SPEC.md §2`; `[SHORT]`/`[LONG]` mark differences.

```
0 STUDY /study · 1 TEXT /narrate|-long (+1b /voice) · GATE1 audio(ear)
2a /scene-plan|-long → 2a+ /bible-check → GATE2 images →
2b /stills (BytePlus ref-lock, MC-R1) → 2c /animate (Kling camera-only, MC-R2) →
2d /comic (one comic engine + kinetic captions, MC-R3/R4) →
3 AUDIO /sfx + score (MC-R5) · GATE3 clips → 3b /review (4-lens, MC-G7) →
4 /caption (built-in at 2d; burn-in fallback only) · 5 /upload
```
`[SHORT]` animates every scene. `[LONG]` animates ≤1 hero cell per page (MC-R7); the
rest are style-matched reuse clips or ken-burns stills.

**Build order is PILOT-FIRST (§8): the long recipe is locked by a MANUAL pilot
before any orchestrator is built.**

---

## 3. The recipe — motion-comic rules (MC-R*)

- **MC-R1 — Stills: BytePlus Seedream 4.5 + ref-lock.** Model `seedream-4-5-251128`.
  Passion beats → bare-torso ref; risen beats → risen-face ref; **context / ot_echo /
  human_us / symbolic → NO Christ ref** (face-bleed fix). **Risen wounds remain
  VISIBLE as the healed print of the nails / spear-mark** (John 20:25–27; Rev 5:6):
  a closed, dark, identifiable pierced mark — not raw/bleeding, not a raised red
  bead/pill, **never erased to blank skin** (a render fix must not overwrite the
  theology). BytePlus has **no negative channel** — name only positive end-states.
  Size is the only format knob (`1440x2560` / `2560x1440`). [pilot; wound corrected
  by doctrine red-team 2026-07-01; `seedream-no-negative-channel`]

- **MC-R2 — Animation: Kling camera-only, invent nothing (INK_BASE).** HF Kling 3.0
  pro, `--aspect_ratio` per format, 5s. INK_BASE keeps flat ink (camera-only, no
  morph/subject-motion/new-lines). Test ONE clip before a batch. **Overrides INV-13
  for the inked line: inked → Kling camera-only (veo3 morphs ink); Baroque → veo3.**
  **CLIP-VIRAL exception:** the shorts `CLIP-VIRAL` gate (≥6 crop-cuts, gallery tour)
  does NOT apply to the ink line — a slow push-in is the intended discipline; the
  motion-comic uses `CLIP-INK` instead (camera-only, no invented motion, ink held).
  [pilot; refines INV-13; resolves the CLIP-VIRAL conflict the panel flagged]

- **MC-R3 — Comic assembly: distinct clip per panel, template variety.** ONE comic
  engine (parameterized by canvas, §6). Every panel a **distinct** still/clip — never
  one still sliced. `full` reserved for hero singles. Include ≥1 **cinematic epic
  wide** (dwarfing scale) to break close-up monotony. [pilot Tier-1]

- **MC-R4 — Kinetic captions + static red Scripture bars.** Plain captions cascade
  word-by-word, payload keyword in RED, box snaps in. **Scripture / red-letter bars
  stay STATIC** (KJV verbatim + speaker + ref). Text de-slopped. [pilot Tier-2]

- **MC-R5 — Audio: $0 SCORE+SFX + four dynamics moves (narration synth is separate &
  metered).** Score = chained music_library Suno excerpts, **loudness-matched**,
  dark→grace arc landing on the CTA; SFX placed at true beat times ($0 sound_library,
  INV-18); no choir pad. Four moves: (a) **clear a hole** before the pivotal line;
  (b) **gated reverb** on the sacred/Scripture line only; (c) a **soft low bell** on
  the key word; (d) **thin the CTA** — ease DOWN to intimacy, never swell (INV-3).
  NB: the **narration MP3 (ElevenLabs, stage 1b) is METERED** and is the largest
  synth in a long — it is NOT part of this $0 claim (see §7). [pilot Tier-1/2]

- **MC-R6 — Motion punch on active beats only.** Edit-level ffmpeg zoom-snap on
  ACTIVE beats; sacred/reflective beats keep the slow push. $0, no morph. [pilot Tier-2]

- **MC-R7 `[LONG]` — ≤1 paid hero per page + STYLE-MATCHED reuse.** Each landscape
  page: one Kling-animated inked hero cell + cells that are **style-matched
  (inked, topically-fitting, aspect-native) reuse clips** or ken-burns stills ($0).
  ⚠ **Flat spend is ASYMPTOTIC, not immediate** — the inked reuse bank does not exist
  for the FIRST inked long, so cost it at **zero reuse / full freight** (§7). A cell
  may be credited $0 only if MC-G9 verifies it is inked-style ∧ topically-fitting ∧
  aspect-native. [`landscape` design; `library-lacks-living-christ`]

- **MC-R8 — Every artifact registered.** Still/clip → `asset_index.json` `fft_<slug>`
  rich metadata; redo'd assets deleted + de-indexed. [🔒 `global-asset-index`]

- **MC-R9 — Never animate legible writing (INV-17), Hebrew default = indistinct.**
  Scrolls/codices default to **indistinct strokes**. Period script may be used ONLY
  if (a) the era's script form is pinned in the Bible-Check fact card (BC-G*), (b) it
  is out of focus at frame-in, and (c) the **first animated frame** is Vision-audited
  (Kling can morph strokes mid-push). Prefer pushing to a non-text focal subject. [INV-17]

- **MC-R10 `[LONG]` — Reverence budget.** Over a 6–8 min long, **≤40% of beats may be
  "active" (punch/fast/kinetic-heavy)**; every 7-movement section contains ≥1
  still-or-slow-push reverent beat; keyword-in-red density capped per movement.
  Kineticism is a seasoning, not the grammar of a meditation. [doctrine red-team]

---

## 4. Gate registry (MC-G*)

Types: **D** deterministic/fail-closed · **P** panel/LLM · **A** advisory. A
fail-closed **D** gate ships with `data/rules.json` + a validator in
`pipeline/validators.py` + a **fixture/test** (no validator+fixture ⇒ it is advisory,
period). Advisory prompt-lessons live in `render_lint/rules.json`.

| Gate | Checks | Type | Home (file · verdict · fixture) | Status |
|---|---|---|---|---|
| MC-G1 Subject variety | Christ ≤60%, ≥1 ot_echo, ≥40% depth, ≤2 consecutive Christ, ≥1 epic wide | D | `render_lint/verify.py::check_scene_subjects` (exists; **needs fixture** to be fail-closed) | wire /scene-plan |
| MC-G2 Template variety | ≥5 templates, `full` ≤40%, no adjacent repeat, distinct-clip-per-panel | D | `render_lint/verify.py::check_comic_spec` (exists; **needs fixture**) | wire /comic |
| MC-G3 Wound/period/anatomy | risen wound PRESENT & readable as nail/spear print; period; anatomy | P-Vision | extend `verify_image` (IMG-*) + `check_wound_present` (**to build + fixture**) | extend IMG audit |
| MC-G4 No gibberish script | **pixel/OCR** check of animated text regions (NOT slug/prompt) | P-Vision + D | new `check_script_legibility` (**to build**); defers to existing fail-closed `validators.never_animate_writing` | build; resolve overlap |
| MC-G5 Captions well-formed | every plain cap kinetic+kw; every Scripture quote a static red bar w/ verbatim+ref | D | new `check_captions` over mocomic spec (**to build + fixture**) | wire /comic |
| MC-G6 Audio dynamics | loudness-matched sections; a clearing on the pivotal line; thinned (not swelling) CTA; narration peak on top; no choir pad | D | new `check_audio_mix` loudness-window verifier (**to build + fixture**) — today only piece-local `add_music_sfx.py` | build then wire /sfx |
| MC-G7 4-lens review (**doctrine-first**) | **DOCTRINE** (5-CLI panel, blocking) + retention + art + sound/soul; a retention/art PASS NEVER satisfies LOCK | P | `/review` — doctrinal panel = `independent_review.py` (restated, not "inherited") + Agent-tool lenses with a written rubric + recorded verdict artifact | manual, gates LOCK |
| MC-G8 Epic-wide present | ≥1 dwarfing-scale wide | D | folded into MC-G1 | wire /scene-plan |
| MC-G9 `[LONG]` Hero budget + reuse validity | ≤1 paid hero/page; each $0-credited reuse cell is coherence+clipqc'd ∧ inked-style ∧ topical ∧ aspect-native | D | `clip_reuse.py` + landscape validate (**to build + fixture**) | wire /comic-long |
| MC-G10 `[LONG]` Christ-landing | final beat `subject_type ∈ {christ_hero,christ_risen}` AND caption = CTA-to-Jesus (mirrors AS-G6/G7 for landscape) | D | new `check_christ_landing` (**to build + fixture**) | wire /assemble-long |

Existing gates apply unchanged EXCEPT `CLIP-VIRAL` (replaced by `CLIP-INK` for the
ink line, MC-R2). TEXT, SP-G*, BC-G*, IMG-*, other CLIP-*, AS-*/LF-AS-*, UK-* all hold.
"To build" gates are advisory until their validator+fixture ship — no silent no-ops.

---

## 5. Schema — one file, explicit `format` discriminant

Not "format-agnostic": a **tagged union** with documented required/forbidden fields
per branch, so validators assert on the branch. Join key = **`slug`**.

`scene_plan.json`:
- `header{ format:"9:16"|"16:9" (discriminant), style:"graphic_novel"|"baroque",
  provider, animation{model,aspect,duration}, audio_seconds, page_seconds [LONG] }`
- `scenes[]{ index, slug, beat, t_start, t_end, subject_type, christ_ref, concept,
  bible_ref, prompt_seed, macro_elements[], motion, why, reuse }`

`mocomic.spec.json`:
- `{ format, episode, audio, beats[]{ t, tpl, clips[]{ slug, motion,
  fidelity(hero|col|kb) — REQUIRED if 16:9, FORBIDDEN if 9:16 }, cap{...} } }`

Branch rules the validators enforce: `fidelity` required⇔`[LONG]`; `tpl` must be in
the format's template set (disjoint vocabularies); `[SHORT]` = every clip animated,
`[LONG]` = ≤1 `hero` per page.

---

## 6. Format deltas (9:16 ↔ 16:9) — ONE geometry engine, no fork

| Axis | Short 9:16 | Long 16:9 |
|---|---|---|
| Canvas | 1080×1920 | 1920×1080 (render 2560×1440 → down) |
| Image size | `1440x2560` | `2560x1440` |
| Kling aspect | `9:16` | `16:9` |
| Templates | vertical stacks | wide rails/bands + native-9:16 reuse rails |
| Caption geom | bottom third, 1080 wrap | lower band, wider wrap, scaled font |
| Anim scope | every scene | ≤1 hero/page (MC-R7) |
| Narration | ~60s, 5-beat | 6–8 min, 7-movement |

**Code parameterization (backward-compatible, default 9:16):**
- ✅ **DONE** — `_hf_animate_short.hf_animate(..., aspect_ratio="9:16")`;
  `kinetic_caption.render_states(..., page=(W,H))` width-scaled; `byteplus` size is
  already a function arg.
- **TODO — the one real refactor:** unify geometry into **ONE** engine. `comic_engine.py`
  (`PAGE_W/H` in ~20 sites) and `landscape_engine.py` (a hand-copied fork of the same
  template algebra) are TWO implementations of one thing — they will drift. Extract
  the shared geometry into `pipeline/motioncomic/geometry.py` parameterized by
  `(page_w, page_h, template_set)`; **retire `landscape_engine.py`**; make
  `kinetic_caption` import the same `PAGE` config (kill its 3rd copy). Do NOT "promote"
  the fork.

---

## 7. Cost model — derived, zero-reuse for the first long

**Pages/clips are DERIVED, never asserted:** `pages = ceil(audio_seconds ÷
page_seconds)`; `animated_beats = pages × moments_per_page`. Pick `page_seconds` +
`moments_per_page` in the header and price off them. A watchable motion-comic turns
every ~5–8s, so a 6–8 min long is **~45–80 animated beats**, not 10–14.

- **Short:** ~13 stills (~$0.5) + ~13 Kling (~$8.5) + audio $0 + LLM $0 ≈ **~$9–10**.
- **First inked LONG (zero reuse — the bank doesn't exist yet):** cost at full freight.
  Charitable ~30s-page / 12-page build ≈ **~$18–24** (12 hero Kling + NSFW→direct-Kling
  fallbacks on passion heroes + ~20% 502 re-spend + hero/filler stills + **ElevenLabs
  6–8 min multi-voice synth ~$2–5, +1 re-synth**). Watchable-paced (4–6 moments/page)
  ≈ **~$30–50**. Flat-spend is **asymptotic** — only after many inked topics seed the
  16:9 reuse bank.
- **ASK-before-spend is a CHOKEPOINT, not a reference:** every render script consumes a
  `/cost` token per attempt-BATCH (incl. retries + NSFW fallbacks); auto-retries are
  capped, then re-ASK. Idempotence keys on "paid attempt made," not just "output exists."
  Pre-classify NSFW beats straight to direct-Kling (skip the wasted HF attempt). (INV-20)

---

## 8. Build order — PILOT-FIRST, then automate

The red-team's #1 flaw was automating an unproven format. So:

**Phase A — de-risk the format (manual, like the short pilot):**
0. **Pre-step (hygiene):** name the CANONICAL pilot script per stage (the surviving
   `_v2` set), quarantine the `redo_*`/`refix_*`/`reroll_*`/`probe_*` graveyard, and
   **move `comic_engine.py` out of `longform/_style_poc/ew04/_mocomic/` into
   `pipeline/motioncomic/`** (kills the importlib path hack).
1. Unify geometry into one parameterized engine (§6 TODO) + landscape template set.
2. **MANUALLY pilot ONE cross-cluster inked long** end-to-end by hand: narration
   (`/narrate-long`) → 16:9 stills → Kling-16:9 heroes → comic pages → audio → caption.
3. LOCK the long recipe: doctrinal 5-CLI panel + 4-lens (MC-G7) + **gravitas A/B vs a
   Baroque cut of the same passage** (§9). Only on pass do `[LONG]` rows become binding.

**Phase B — automate (only after A locks):**
4. Generalize the canonical scripts into `pipeline/motioncomic/` stage modules.
5. Build `cli_motioncomic.py <topic|v1> --format short|long` — chains the modules, 3
   human gates, resumable. State model: **per-scene status** (rendered/animated/qc'd)
   + **per-clip NSFW-fallback flag** in `pipeline.state.json`; position detection is
   schema-generic (NOT reused from the ScenePlan-coupled `orchestrator.py`), keyed on
   on-disk artifact+sidecar per stage.
6. Ship MC-G1..G10 each with validator + fixture/test; wire the D gates into their
   stages; surface MC-G3/G7 for human sign-off.

---

## 9. A/B, gravitas gate & learning

The manual long pilot (Phase A) is judged by: doctrinal 5-CLI panel + the 4-lens
review + a **gravitas A/B** — the same passage cut both inked and Baroque, panel +
user judging which sustains reverence over 8 min. Log escaped defects (`learning.py`)
+ metered cost (`spend_ledger.jsonl`) + human touches. `/learn` promotes escaped
defects into `render_lint/rules.json` (prompt lesson) or `data/rules.json` + validator
+ fixture (hard block), reflected here as a new MC-R/MC-G row. Propose-I-approve.
Inked-long binds ONLY on a clean gravitas pass; otherwise Baroque remains the long default.
