# REDO NOTE — Psalm 22 inked long pilot (2026-07-01)

## 🔒 M1 APPROACH LOCKED (user, 2026-07-02) — scale to the full film
The M1 slice (0-44.9s) is the LOCKED recipe for the whole 16:9 inked long: SHORT's comic_engine
multi-panel grids + subject-safe crops (`panel_fit.py` + `<slug>.anchor.json` + fit-gate) + a mixed
camera palette (Kling generative for a few + $0 deterministic `dynamic_cam.py` arc/swoop for the rest;
NO static stills) + kinetic keyword captions + red Scripture bars. Build = `build_mocomic_16x9.py
--clips` off a `mocomic_16x9_*.spec.json`. Now scaling to all 24 pages (see `page_plan.json` map).


## Why a redo
The BytePlus stills hallucinated too much (gibberish Hebrew/Greek, Dome of the Rock,
medieval crown, blackletter "Septuagint", red-pill wound). **Root cause = my prompting,
not the model.** The prompts were long, dense, and full of hallucination hooks. Redo the
stills with the LEAN discipline below. This is now the standing rule for all BytePlus
(Seedream 4.5) rendering — short and long.

## The lean-prompting discipline (the fix)

BytePlus draws literally, fake-writes any text, guesses wrong on anything named, and
**draws any noun you mention — even one you say "NO" to** (no negative channel). So:

1. **ONE dominant subject.** Describe the subject + the mood in ~25–40 words. Then stop.
   Long prompts = more things to get wrong.
2. **No detail lists.** Name 1–2 objects max, never 5–6. Extra nouns = extra hallucinations.
3. **Never show legible text.** Scrolls/manuscripts: rolled shut, edge-on, tiny in the
   distance, or out of frame. **Never name a language or title** ("Hebrew", "Greek",
   "Septuagint") — it tries to write it and produces gibberish/anachronism.
4. **Never name a specific building/monument** ("Temple", "Second Temple", "Dome"). It
   guesses and gets it wrong/anachronistic. Say "an ancient stone city" or crop it out.
5. **Pure positive end-states only.** NEVER "no crown / not a worm / no dome". The forbidden
   noun gets drawn. Instead describe what IS there ("bare-headed, grey hair loose").
6. **Lean on the ref-lock for the face/character**, not on words. The ref carries identity;
   the prompt carries composition + mood.
7. **Design impossible things OUT of the shot.** If the model can't render readable text,
   correct architecture, coins/dice, etc. — frame it so that element isn't in the picture,
   don't try to describe it accurately.
8. **~25–40 words of subject. Fewer words = fewer hallucination hooks.**

Contrast: the CLEAN pilot stills (nail_through_hand, the risen hero, ends_of_earth,
crane_cross_soldiers) were the SIMPLE ones — one subject, few nouns, no text, no named
places. The DIRTY ones were the dense/text/place-heavy ones. That is the whole lesson.

## Current state (what exists)
- Page plan v2 (red-teamed, all fixes in): `v1/visual_16x9_inked/page_plan.json`
- 21 inked 16:9 stills rendered + eyeballed: `v1/visual_16x9_inked/*.png`
  (~$1 spent). Keepers are the simple ones; the text/place stills are the weakest even
  after reroll (`storm_over_jerusalem` temple still a bit off; scroll pages marginal).
- Renderer: `render_fresh_16x9.py` (has the current — too dense — prompts).
- Landscape assembly: NOT built yet. Kling animation: NOT run (no $ spent on motion).
- Reuse pool: 13 LOCKED 9:16 cross-short clips (10 mapped into the plan).
- Narration + audio: LOCKED, reused as-is ($0).

## What to redo (in order)
1. **Rewrite `render_fresh_16x9.py` prompts to the lean discipline above** — cut every
   detail list, kill every "NO x", remove every named language/building, keep 1 subject.
   Special care: the 3 text/scroll pages (david_psalmist, disputed_word_marks,
   greek_ot_scroll) and storm_over_jerusalem — design the text/temple OUT of frame or tiny.
2. **Re-render only the weak stills** (the dense/text/place ones); keep the clean keepers.
3. Then continue the pilot: build the $0 static landscape comic preview → approve layout →
   Kling animate the heroes (~$12) → reuse rails + kinetic captions + score → caption.

## DIRECTION CHANGE — the long must FEEL like the short (user, 2026-07-01)
"For the long format we got to make it feel like how we did short, so there will be a
need to do more stills." The short felt alive because every comic panel held a DISTINCT
still/clip + fast cuts + kinetic captions + punch. The current landscape plan is too
SPARSE (≤1 hero/page + reuse rails + ken-burns) — that reads slower/thinner than the short.

**Revise the page plan for DENSITY:**
- Most pages become MULTI-PANEL comic grids with a DISTINCT fresh still in each panel
  (like the short's mocomic), not one hero + a reuse rail.
- More cuts, more panels, punch on the active beats, kinetic captions throughout.
- This ~DOUBLES the fresh-still count (~18 -> ~35–40) and the cost (~$15 -> ~$25–30).
  Quality/feel wins over the flat-spend model (shorts-first, always-punchier).
- **This RELAXES MOTIONCOMIC_SPEC MC-R7** (the ≤1-paid-hero-per-page economics): for a
  long that must match short energy, spend for density. Reuse where it fits, but do NOT
  starve pages of distinct visuals to save money.

## Codify (so it never repeats)
- Add a `render_lint/rules.json` rule: `byteplus-lean-prompt` (advisory, stage:still).
- Fold rule into `v2/MOTIONCOMIC_SPEC.md` MC-R1 (stills) as the prompting sub-discipline.
- Memory: `byteplus-lean-prompting`.

## STATUS 2026-07-02 — long now built the SHORT's way (16:9)
The earlier `build_fastcut_16x9.py` was WRONG: flat full-frame ken-burns, no comic grids,
no Kling, oversized captions (user flagged all 3). Root cause = it bypassed the short's
locked chain. Fixed:
- `comic_engine.py` given an additive `set_page(w,h)` → 16:9-capable; default stays 9:16 so
  the short is byte-identical. (Locked shared engine — change is additive only.)
- `kinetic_caption.py` now scales furniture by HEIGHT (ph/1920), not width → captions
  proportionate on 16:9; 9:16 resolves to ×1.0 (unchanged).
- New `build_mocomic_16x9.py` + `mocomic_16x9_m1.spec.json` rebuild the SAME 0-44.9s slice as
  true multi-panel comic grids (big_inset/stack_h/quad, distinct still per panel; `full` only
  for the 2 red-letter singles). $0 static preview:
  `v1/visual_16x9_inked/mocomic_16x9_m1.spec_preview.mp4`
- Also fixed a runaway-ffmpeg bug in `build_fastcut_16x9.py` (`overlay_static` had no `-t` cap →
  multi-GB seg; that, not laptop instability, is what killed the earlier run).

## STATUS 2026-07-02 (later) — M1 slice ANIMATED in Kling (all 3 observations closed)
User approved Kling on the M1 slice. Rendered 9 inked 16:9 clips via HF Kling 3.0 **pro** (5s,
camera-only INK prompt, `animate_m1_16x9.py`). SPEND: ~$5.85 (9 × ~$0.65). Test-gated ONE clip
(cry_ninth_hour) + eyeballed frames first (ink held, no morph), then batched 8.
- SKIPPED `scribe_over_manuscripts` (legible writing → Kling garbles text); it stays ken-burns.
- Clips in `v1/visual_16x9_inked/clips/<slug>.mp4` (95MB). Spec carries directional motions so the
  engine slow-forwards (no boomerang yo-yo). Composited via `build_mocomic_16x9.py --clips`.
- ANIMATED preview: `v1/visual_16x9_inked/mocomic_16x9_m1.spec_preview.mp4` (45s, 23.7MB).
- Verified by eye: storm/architecture held, david push-in cropped the scroll out, quad = 4 live
  animated panels. All clean.
- OPEN POLISH (minor, not blocking): beat 3 (full sacred "My God my God", cry_ninth_hour pullback)
  overshoots a thin cream page-margin at top-left. Fix = give that beat's clip a slight zoom (~1.05)
  to crop the margin, or swap it to push-in. Cosmetic.

## STATUS 2026-07-02 (later 2) — scientific panel-crop system (no more chopped heads)
User: grid crops sometimes chop the head / hide the main element; wants a scientific repeatable
process. Root cause = the engine center-crops (bias 0.5) blind to the subject, AND some templates
have panels whose aspect is far from the 16:9 stills (stack_h rows = 4.19:1 → lose ~50% height →
head gone). Built a deterministic **MEASURE → SOLVE → VERIFY** system (all $0, key-independent —
no Anthropic API, which is dead):
- `panel_fit.py` — `solve_crop(panel, still, anchor, motion)` returns subject-safe (bias, zoom) that
  keeps the measured keep-box in frame (+ head-room for push-ins), or fit=False + reason when the
  panel aspect can't contain it. `fit_report()` = pre-flight gate.
- `<slug>.anchor.json` sidecars (10 written) — normalized keep-box + focus, measured by eye ONCE,
  cached + reused by every build. (For scale, new stills get an anchor at gallery-review.)
- `build_mocomic_16x9.py` now loads anchors, solves bias/zoom per panel, prints the fit-gate.
- Recomposed M1 ($0, reused the 9 clips): the two stack_h beats (2,4) that were chopping now keep
  the FULL face (bias snapped to the head) — letterbox rows read as intentional cinematic crops.
- Gate output: stack_h rows flagged 44-58% over-crop (advice: use quad/two_v ~1.78:1); quad/big
  panels 1-3% (silent). Recommendation surfaced: prefer templates whose panels ≈ still aspect.

APPLIED (user): swapped the 2 flagged stack_h beats (2,4) → two_v. Columns keep FULL height, so all
4 faces (Christ, David, scribe) are now fully framed; the wide nail-hand (pierced_hands_feet) takes
a 27% side-crop in the portrait column but reads great (nail+palm centered). Gate is now quiet
except that one cosmetic wide-subject note. LESSON: face-subjects want columns (two_v); wide subjects
(a hand, a landscape) want rows/wide panels — pair opposite-orientation subjects carefully, or split
them across beats. The gate surfaces this automatically.

## STATUS 2026-07-02 (later 3) — $0 dynamic camera (no static stills, orbit-feel, no morph)
User: animation felt samey (only Kling push/pull), wanted orbit/rotate/dynamic; and NO static stills.
Orbit on Kling repaints flat ink (unsafe). Built `dynamic_cam.py` — deterministic dimensional camera
(PIL perspective per frame): `arc` (yaw+push), `swoop` (yaw+pitch cranein). Pixels re-projected, never
repainted → faithful even on WRITING stills. Wired into `build_mocomic_16x9.py`: clip `"cam":"arc|swoop"`
uses the $0 move; any non-Kling slug falls back to `arc` (no more flat static holds). Proven on M1:
scribe (writing, un-Kling-able) now MOVES with pristine text; beat 6 sacred got a reverent swoop to the
face. Memory `zero-cost-dynamic-camera`. Bolder possible (raise deg) but keep tasteful.

NEXT: user reviews the swapped slice. THEN scale the dense spec to the full 24 pages
(`page_plan.json`) — 16 new stills + Kling batch — then score (dark→grace) + SFX + caption.
Reusable: `panel_fit.py` + the anchor-sidecar convention should graduate to the shared engine so
the shorts + all longs get subject-safe crops (propose at /learn).
