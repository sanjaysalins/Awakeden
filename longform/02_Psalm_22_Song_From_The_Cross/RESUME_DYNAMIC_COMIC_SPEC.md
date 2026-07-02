# RESUME + SPEC — Psalm 22 dynamic graphic-comic (16:9 long) REBUILD

> Handoff for a fresh build (Fable). The current full cut is a **slideshow**, not a designed comic.
> This spec captures WHY and exactly WHAT to build so the long finally feels like the short — dynamic,
> fast-cut, designed, with captions that never cover the art. **The stills are DONE and LOCKED; the
> FINISHING LAYER (pacing + captions + composition + motion) is what to rebuild.**

---

## 0. TL;DR
- **Keep:** the 35 grounded/validated stills, their anchors, the narration+audio, and the tooling
  (`panel_fit`, `dynamic_cam`, `still_validate`, `render_grounded`, `comic_engine` 16:9).
- **Rebuild:** the finishing layer — **cut ~3× faster**, a **content-aware caption system** (sized +
  placed OFF the subject; kill the full-width bottom bar), **art-directed panel composition**, and
  **more genuine motion** (Kling on heroes + edit-punch).
- **Method:** build ONE movement as a slice → review → only then scale. Do NOT scale blind again.

---

## 1. Current state (what exists on disk)
Folder: `longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/`

| Asset | Path | Status |
|---|---|---|
| 35 inked 16:9 stills | `*.png` | ✅ DONE — grounded + validated + eye-audited. **Do not redo.** |
| Per-still anchors (subject keep-box + focus, normalised) | `*.anchor.json` | ✅ DONE — 34 stills. **Use these for caption placement + crops.** |
| Grounded prompt specs (verse + shot + pose + distinct_from) | `../still_specs.json` | ✅ source of truth for prompts |
| Prompt validation gate | `../still_validate.py` | ✅ catches lazy/dup/non-biblical BEFORE render |
| Grounded renderer | `../render_grounded.py` | ✅ renders from still_specs |
| Full-film beat spec (29 beats) | `mocomic_16x9_full.spec.json` | ⚠️ TOO SLOW — replace with a short-rate spec |
| Current full cut (the slideshow) | `mocomic_16x9_full.spec_preview.mp4` | ⚠️ reference for "what NOT to ship" |
| Narration (locked) + timeline | `../narration.mp3`, `../narration.spoken.txt`, `../narration.md` | ✅ 418.2s, verbatim KJV |
| 9 existing Kling clips + 7 hero pending | `clips/*.mp4` | 🟡 HF was down (HTTP 500) — re-render the 7 heroes when HF is back |

Tooling (reuse, do not rewrite):
- `panel_fit.py` — deterministic subject-safe crop solver (bias/zoom so a panel never chops the subject) + a fit-gate.
- `dynamic_cam.py` — $0 deterministic dimensional camera (PIL perspective per frame): `arc`, `swoop`. Zero morph. Good for supports + writing stills.
- `_polite.py` / venv `sitecustomize.py` — throttles ffmpeg to ~50% CPU (POLITE_CPU env) so renders don't hog the machine.
- `comic_engine.py` (`longform/_style_poc/ew04/_mocomic/`) — 16:9-capable multi-panel engine. **Its caption furniture is the thing to replace (§4).**

Spend so far: ~$2.30 (stills only). No score/SFX yet.

---

## 2. THE PROBLEM (user critique, 2026-07-02 — take literally)
1. **"Feels like a static slideshow, not a dynamic graphic comic animation."**
   - Root: cut rate is **~14s/beat** (29 beats / 418s). The short ran **~4s/beat**. 3× too slow.
   - Root: only **7 of 58 panels** are true generative motion; the other 51 are gentle $0 camera drifts. Camera-over-a-still ≠ animation.
2. **"Placement of stills and grids poorly thought through."** Stills dropped into fixed template rectangles with auto-crops. No page-level art direction (panel shape, negative space, reading flow).
3. **"Most of the time the bottom red box is hiding [the still]."** The caption/red-letter box is drawn **full-width at the bottom, fixed**, blind to where the subject is → it covers feet/hands/faces.
4. **"The red box is still big… we should not use the whole width, rather dynamically plan how much to use."** Caption furniture must be **sized to the text** and **placed in empty space**, not a full-width slab.
5. **"Very amateurish, lazy, not well thought-through production."** Correct diagnosis: it's a MECHANICAL assembly pipeline scaled up. Technically correct, artistically flat. Correct ≠ good.

---

## 3. DESIGN GOAL
A **dynamic inked graphic-novel motion comic** at 1920×1080, ~7 min, that feels like the LOCKED short
(`batches/cluster_01_cross/father_forgive_them/visual/_byteplus/..._mocomic_v2_scored.mp4`):
fast cuts, punch, a distinct image per beat, kinetic captions, red Scripture bars as sacred anchors —
just longer and 16:9. **Energy from CUT RATE + MOTION + DESIGN, not from long holds.**

---

## 4. SPEC — the four subsystems to build

### 4A. PACING — cut-driven (fixes "slideshow")
- **Target ~4–6s per beat → ~70–90 beats** for 418s (up from 29). Break the narration into clause-level beats.
- **Punch on active/hook beats** (the ninth-hour cry, nails, the mockers, "poured out", "it is finished"): edit-level **zoom-snap** (open tight → snap out), $0 ffmpeg. Reuse the short's `<slug>_punch` approach.
- **Sacred/red-letter beats** may hold slightly longer (5–7s) with ONE slow reverent move.
- **Rhythm = contrast:** fast montage clusters, then a held sacred beat. Never a flat even cadence.
- Derive beat boundaries from the narration timeline (word/clause timestamps) so cuts land on the words.

### 4B. CAPTION SYSTEM v2 — content-aware (fixes "box hides art / box too big")
Replace the full-width bottom bar entirely. New rules:
- **Width = fit the text**, wrapped to a MAX ~50–55% of frame width for short captions (never full-width unless the line truly needs it).
- **Placement = the largest empty rectangle that does NOT overlap the subject.** Algorithm (deterministic, $0, uses the anchors we already have):
  1. Load the panel's still `*.anchor.json` → `keep` box (subject) + `focus`.
  2. Candidate slots: bottom-left, bottom-right, top-left, top-right, lower-third-center (+ any large gutter in a multi-panel grid).
  3. Score each by: (a) **zero overlap** with the subject keep-box (hard requirement), (b) size ≥ text box, (c) rule-of-thirds / away from focus, (d) local contrast for readability.
  4. Place the caption in the best slot; if the subject fills the frame, use a subtle **gradient scrim** only under the text (not a full slab), in the darkest region.
- **Kinetic keyword captions** (narrator lines): same placement, smaller, words cascade in with the keyword in red. Reuse `kinetic_caption.py` logic but drive x/y from the slot solver (currently it's hardcoded bottom).
- **Red Scripture bars** (sacred KJV): keep the red-letter + `SPEAKER · ref` tag, but **sized to the text and tucked into an empty zone** — a designed plaque, not a full-width white slab. Still visually distinct (the sacred anchor) but never covering the face/subject.
- **Safe-zone data already exists:** every still has an anchor; the solver just needs the *complement* of the keep-box. No new measurement, no API.

### 4C. COMPOSITION — designed pages (fixes "poorly thought grids")
- **Panel shape follows the shot** (already tagged in `still_specs.json` per still): WIDE_ESTABLISH → full-bleed; CLOSE_PORTRAIT → tall panel; MACRO → inset/detail; multitude → wide; montage → grid.
- **Compose to the caption:** choose the crop (via `panel_fit`) so the subject sits on one side and the *other* side is negative space reserved for the caption. Subject + text share the frame, never overlap.
- **Rhythm of layouts:** mix single full-bleed hero beats with dense multi-panel montage beats — vary by beat function (hook / proof / sacred / turn / CTA). Not the same template mechanically.
- **Reading flow:** L→R, T→B; borders + gutters intentional (inked look). Keep the subject-safe crop guarantee from `panel_fit` (no chopped heads) — that part works.

### 4D. MOTION — genuine + punchy (fixes "barely animated")
- **Kling generative** on hero/emotional beats (the cry, pierced hands, the risen Christ, the CTA) — real life, camera-only INK prompt (`animate_full.py` pattern), 16:9, 5s. Retry the 7 pending when HF recovers.
- **$0 dynamic-cam** (`arc`/`swoop`) for supports — but BOLDER and matched to the beat, not a uniform gentle drift.
- **Edit-punch** (zoom-snap) on active beats — $0.
- **Writing stills** (scribe/scroll/manuscripts) → dynamic-cam ONLY (Kling garbles text).
- Balance is a cost lever: more Kling = more life = more $ (~$0.65/clip). Decide the Kling-vs-dyncam ratio up front.

### 4E. AUDIO (finishing)
- **Score:** dark→grace arc, chain `music_library` Suno tracks at $0 via `longform/_add_score_lf.py` (lonely/searching → sacred grace rise; grace lands on the CTA).
- **SFX:** forced-aligned ambient bed from `sound_library`, sidechain-ducked ($0).
- **Mix order:** narration (base) → music bed → SFX, each ducked under the one above.
- Captions are burned into the comic layer already (no separate caption pass).

---

## 5. BUILD ORDER (do NOT scale blind)
1. **Caption solver first** (§4B) — the safe-zone placement engine from anchors. Highest-visibility fix.
2. **Re-plan ONE movement** at short cut-rate (§4A) — e.g. M1 (0–45s) or M3 (the wounds). Per beat: template, still(s), caption {text, type, kw/ref}, motion, punch.
3. **Build that slice** → **review with the user** → iterate on pacing + caption placement until it feels like the short.
4. **Only then** scale the pacing + caption approach across all 7 movements.
5. Animate heroes (Kling) + punch, composite, then **score + SFX**.
6. Validate: 0-FAIL gates + doctrine (both self + 5-CLI panel) + the eye-audit on every rendered frame.

---

## 6. INVARIANTS / LOCKED DECISIONS (carry forward)
- **Stills are LOCKED** — 35 grounded, validated, eye-audited. Do not re-render without a new flag. `still_validate.py` must pass before ANY new still render (no lazy/terse prompts — memory `feedback-no-lazy-still-prompting`).
- **No chopped heads** — `panel_fit` subject-safe crops stay.
- **No static stills** — every beat moves (Kling or dynamic-cam).
- **KJV verbatim** in red bars; doctrine sound + Christ-lens; land on Christ.
- **Never Kling-animate writing** (garbles text).
- **Nail wording:** never "broad flat hammered head" (→ hammer) or "spike/blade/edge" (→ dagger); use "slender iron nail, small head" (memory + `render_lint` rule `nail-head-wording-renders-a-tool`).
- **CPU-polite renders** on (POLITE_CPU env).

## 7. OPEN DECISIONS (for the builder to set with the user)
- Exact cut-rate target (4s vs 6s) and total beat count.
- Caption style: tucked plaque vs gradient scrim vs pure kinetic — and one visual system for all three caption types.
- Kling-vs-dyncam ratio (cost vs generative life).
- Whether any stills need a light re-crop/reroll to *reserve negative space* for captions (some are full-bleed subjects with no room for text — may need a composition variant).

## 8. REFERENCE — the short that works (the bar to hit)
`batches/cluster_01_cross/father_forgive_them/` — `build_mocomic_v2.py` (comic engine + `--clips`),
`animate_v2.py` (Kling), `kinetic_caption.py` (cascade), `add_music_sfx.py` (score+SFX). Study its
cut rate, punch, and caption placement — that is the target energy at 16:9 + 7 min.
