# RESUME + SPEC v2 — Psalm 22 dynamic graphic-comic (16:9 long) REBUILD

> Supersedes `RESUME_DYNAMIC_COMIC_SPEC.md` (v1). v1 was red-teamed and had 3 contradictions +
> missing acceptance criteria. v2 RESOLVES them with explicit decisions, adds a measurable
> Definition of Done, and a Kling/cost fallback. The honest headline correction to v1:
> **the stills are ~60% done, not 100% — the stills and the finishing layer are COUPLED.**

---

## 0. TL;DR
- **Goal:** the 7-min 16:9 long must feel like the LOCKED short — cut-driven, designed, captions that
  never cover the art. Current cut (`v1/visual_16x9_inked/mocomic_16x9_full.spec_preview.mp4`) is a
  slideshow = the "what NOT to ship" reference.
- **Reuse:** the 35 grounded stills, anchors, narration/audio, and tooling (`panel_fit`, `dynamic_cam`,
  `still_validate`, `render_grounded`, `comic_engine`). All still valid.
- **But also produce:** ~15–20 MORE grounded stills + re-render ~6–10 "caption-room" variants (see §R1/§R2).
- **Rebuild:** pacing, captions, composition, motion (§4).
- **Method:** build ONE movement as a slice, pass the Definition of Done (§5), review with user, THEN scale.

---

## R. THE THREE RESOLVED CONTRADICTIONS (this is the new value in v2)

### R1 — Captions vs full-frame stills: a 3-TIER caption system, decided per still
v1 said "place captions off the subject" but most heroes fill the frame. Resolution — a deterministic
tier picked from each still's `*.anchor.json` keep-box:
- **Tier 1 — placed caption** (the still leaves a caption-sized region with 0% keep-box overlap):
  put a compact caption there. Most wides, scenes, multi-panel members.
- **Tier 2 — designed lower-third scrim** (subject fills the frame but the bottom/edge region is
  *expendable* — shadow, sky, ground, robe): a SOFT translucent gradient band (not an opaque slab)
  with the text; this is intentional cinematic comic language, allowed. Height = wrapped text only.
- **Tier 3 — re-render a caption-room variant** (subject fills the frame AND every region carries a
  key element, e.g. a face cropped to all four edges): re-render that still with the subject shifted
  up / to one side to open negative space. This UN-LOCKS a NAMED subset only (expect ~6–10 stills).
  Must pass `still_validate.py`. List them explicitly in the new spec.
- **Decision rule (deterministic):** for each (still, caption) compute the largest caption-box that
  fits with 0% keep-box overlap. If it fits the text → Tier 1. If only a lower-third fits over an
  expendable region → Tier 2. Else → Tier 3 (flag for re-render).

### R2 — Cut rate vs still count: do the math, render the gap
v1 wanted ~90 beats but we have 35 stills → reuse → the repetition the user hated. Resolution:
- **Target ~5s/beat → ~70 beats** for 418s (short-like but not frantic).
- Grids give multiple images per beat: ~70 beats × avg ~1.5 panels ≈ **~105 panel-slots**.
- **Reuse rule:** a still may reappear only (a) ≥ 8 beats later AND (b) in a DIFFERENT crop/shot
  (macro↔wide) so it never reads identical. Enforce in the spec + a check.
- **Distinct-still budget under that rule ≈ 50–55.** We have 35 → **render ~15–20 more** (grounded via
  `still_specs.json` + `still_validate.py`; ~$1). So the still set is ~60–70% done, not done.
- If the user prefers ZERO new stills: fall back to ~55 beats @ ~7.5s with strict crop-varied reuse —
  less short-like, documented tradeoff. **Recommend the +15–20 stills path.**

### R3 — Long red-letter verses can't be tiny: two caption CLASSES, different rules
- **Kinetic keyword captions** (narrator lines): ALWAYS compact — ≤ 50% frame width, Tier-1/2
  placement off the subject, words cascade in, keyword in red. Small. "Never full-width" applies HERE.
- **Red-letter Scripture bars** (KJV, the sacred anchor — prominence matters): adaptive —
  - short verse (≤ ~8 words): a tucked plaque off the subject (Tier 1/2).
  - long verse: a **designed translucent parchment band** over the LOWER portion, height = wrapped
    text, soft top edge — full-width is allowed HERE because readability of Scripture wins, BUT it
    must be translucent (art shows through) and the beat's still must be chosen/cropped so the bottom
    is expendable. Never the current opaque white slab.

---

## 1. CURRENT STATE (files on disk)
Folder: `longform/02_Psalm_22_Song_From_The_Cross/` (stills under `v1/visual_16x9_inked/`)

| Asset | Path | Status |
|---|---|---|
| 35 inked stills | `v1/visual_16x9_inked/*.png` | ✅ grounded+validated+eye-audited · ⚠️ need ~15–20 more + ~6–10 Tier-3 re-renders |
| Anchors (keep-box+focus) | `*.anchor.json` | ✅ 34 — drives crops AND the caption tier decision (R1) |
| Grounded prompt specs | `still_specs.json` | ✅ source of truth for prompts |
| Validation gate | `still_validate.py` | ✅ MUST pass before any new/re-rendered still |
| Grounded renderer | `render_grounded.py` | ✅ renders from still_specs (BytePlus + ref-lock, ~$0.05/still) |
| Full-film beat spec (29 beats) | `v1/visual_16x9_inked/mocomic_16x9_full.spec.json` | ⚠️ TOO SLOW — replace |
| Slideshow cut (reference) | `mocomic_16x9_full.spec_preview.mp4` | ⚠️ what NOT to ship |
| Narration + timeline | `narration.mp3` / `narration.spoken.txt` | ✅ 418.2s, verbatim KJV |
| 9 Kling clips + 7 pending | `v1/visual_16x9_inked/clips/*.mp4` | 🟡 HF was HTTP-500; retry heroes when up |

Tooling (reuse, don't rewrite): `panel_fit.py` (subject-safe crops + fit-gate), `dynamic_cam.py`
($0 arc/swoop, zero morph), `comic_engine.py` (16:9-capable; **its caption furniture is what §4B
replaces**), `_polite.py` (CPU throttle), `render_lint/` (prompt rules incl. nail/feet lessons).

---

## 2. THE PROBLEM (user critique — take literally)
Slideshow feel (cut rate ~14s/beat vs the short's ~4s; only 7 of 58 panels truly animated) ·
grids/stills placed mechanically · the red/caption box covers the art · the box is full-width/too big ·
"amateurish, lazy, not well thought-through." Root cause: a MECHANICAL assembly pipeline scaled up.
Correct ≠ good.

---

## 3. DESIGN GOAL
A dynamic inked graphic-novel motion comic, 1920×1080, ~7 min, with the energy of the LOCKED short
(`batches/cluster_01_cross/father_forgive_them/visual/_byteplus/..._mocomic_v2_scored.mp4`):
fast cuts, punch, a distinct image per beat, kinetic captions, red Scripture bars as sacred anchors.
Energy from CUT RATE + MOTION + DESIGN, never from long holds.

---

## 4. SPEC — the four subsystems

### 4A. PACING (fixes slideshow) — see R2 for the count
- **~70 beats @ ~5s** median; break narration at clause level; cuts land on the words (use the timeline).
- **Punch on ACTIVE beats.** Definition: a beat whose narration carries a percussive verb/moment
  (pierced, poured, cast, mocked, cried, forsaken, finished) or a hook. Mechanic: an edit-level
  **zoom-snap on the cut-IN** (open ~12–15% tight, snap to full over 3–5 frames), $0 ffmpeg. Not
  throughout — only on the cut. Sacred/reflective beats do NOT punch.
- **Rhythm = contrast:** fast montage clusters, then ≤2 deliberately held sacred beats (max ~8s).

### 4B. CAPTIONS (fixes covering-the-art) — the 3-tier system, two classes (R1 + R3)
Replace `comic_engine`'s full-width bottom furniture. Build a `caption_layout.py` that, per
(panel-still, caption), reads the anchor and returns {box_xywh, style-tier, class}. Deterministic, $0,
no API. Kinetic = compact off-subject; red-letter = plaque (short) or translucent band (long). Reuse
`kinetic_caption.py` glyph rendering but drive x/y/width from the solver (currently hardcoded bottom).

### 4C. COMPOSITION (fixes mechanical grids)
- Panel shape follows the still's `shot` tag (already in `still_specs.json`): WIDE→full-bleed,
  CLOSE_PORTRAIT→tall, MACRO→inset, multitude→wide, montage→grid.
- Compose to the caption: pick the `panel_fit` crop so the subject sits one side, caption space the
  other. Keep the subject-safe crop guarantee (no chopped heads — that part works).
- Vary layouts by beat function (hook/proof/sacred/turn/CTA); mix single full-bleed heroes with dense
  montage beats. Intentional gutters/borders (inked look).

### 4D. MOTION (fixes barely-animated) — with the Kling/HF fallback (R5)
- **Kling generative** on hero/emotional/active beats (INK camera-only, 16:9, 5s, `animate_full.py`
  pattern). **Target ~15–20 Kling clips, HARD CAP ~$15.**
- **$0 dynamic-cam** (`arc`/`swoop`) for supports — bolder, matched to the beat, not uniform.
- **Edit-punch** on active beats ($0). **Writing stills → dynamic-cam ONLY** (Kling garbles text).
- **HF fallback:** if Higgsfield 500s, ship complete on dyncam; retry the Kling heroes when HF is up
  (idempotent) and re-composite ($0). Never block the film on the outage.

### 4E. AUDIO (finishing)
Score = dark→grace `music_library` Suno chain via `longform/_add_score_lf.py` ($0, grace lands on CTA).
SFX = forced-aligned `sound_library` bed, ducked ($0). Mix: narration → music → SFX. Captions are
burned in the comic layer (no separate pass).

---

## 5. DEFINITION OF DONE (measurable — the v1 gap)
The rebuild is only "done" when ALL pass:
1. **Cut rate:** median beat ≤ 6s; ≤ 2 held beats, none > ~8s.
2. **Captions:** every KINETIC caption 0% overlap with the subject keep-box; every red-letter band
   ≤ bottom 25% and only over an expendable region; no opaque full-width slab anywhere.
3. **Variety:** no still repeats within 8 beats; no identical crop reused; ≤ 55% Christ-centric
   (memory `scene-subject-variety-gate`); ≥1 OT-echo.
4. **Motion:** every beat moves; ≥ 40% of beats have Kling OR edit-punch (not just gentle drift).
5. **Doctrine (NON-NEGOTIABLE):** 0 doctrinal/citation errors, KJV verbatim, lands on Christ —
   verified BOTH self-red-team AND the 5-CLI panel (`independent_review.py`).
6. **Eye-audit:** every rendered frame checked — no morph, no NSFW, period-correct, no chopped heads,
   nail-not-dagger/hammer.
7. **The short test:** side-by-side with the locked short, the cut rate + energy read as the same family.

---

## 6. BUILD ORDER (do NOT scale blind)
1. `caption_layout.py` (§4B) — the tier solver. Highest-visibility fix; build + unit-test on 3 stills first.
2. Decide the still gap (R2): render ~15–20 new + re-render the Tier-3 list (all via `still_validate.py`).
3. Re-plan ONE movement at ~5s/beat (e.g. M3 the wounds, or M1). Per beat: template, still(s)+crop,
   caption {text, class}, motion, punch. Enforce the reuse rule.
4. Build that slice → run the Definition of Done → **review with the user** → iterate.
5. Only then scale to all 7 movements. Animate heroes (Kling, capped) + punch. Composite.
6. Score + SFX. Final Definition-of-Done pass incl. the 5-CLI doctrine panel.

---

## 7. LOCKED INVARIANTS (carry forward)
No lazy/terse prompts — `still_validate.py` must pass (memory `feedback-no-lazy-still-prompting`) ·
no chopped heads (`panel_fit`) · no static stills · KJV verbatim + sound doctrine + Christ-lens,
proven both ways · never Kling-animate writing · nail wording: "slender iron nail, small head" never
"broad flat hammered head" (→hammer) or "spike/blade/edge" (→dagger) (`render_lint` rule) ·
CPU-polite renders (`POLITE_CPU`).

## 8. OPEN DECISIONS FOR THE USER
- Cut-rate target: 5s (recommended) vs 4s (more frantic) vs 7.5s (no new stills).
- New-still budget: +15–20 (recommended) vs 0 (accept slower + reuse).
- Kling ratio / spend cap (default ~$15).
- Caption visual identity: exact scrim opacity, plaque style, font — one system for all three classes.

## 9. THE BAR TO HIT
`batches/cluster_01_cross/father_forgive_them/` — study `build_mocomic_v2.py` (comic engine + --clips),
`animate_v2.py` (Kling), `kinetic_caption.py` (cascade), `add_music_sfx.py` (score+SFX). Match its cut
rate, punch, and caption placement at 16:9 + 7 min.
