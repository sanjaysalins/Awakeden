# LANDSCAPE_VALIDATION.md — gate spec for the 16:9 long-form motion-comic build

**Date:** 2026-06-30 · **Status:** spec drafted, validators NOT built yet · sibling of `LANDSCAPE_RESUME.md`.

> Every long-form motion-comic page must clear this registry before the episode is called done.
> Each gate is tagged by **HOW** it's checked:
> - **DET** = deterministic code check (cheap, runs on every build, fail-closed)
> - **VISION** = Claude-Vision audit of the rendered page/frame (look at it myself, per standing rule)
> - **PANEL** = the 5-CLI independent doctrinal panel on the narration (run once per episode)
> - **EYE** = human gallery review (authority on the subtle)
>
> Reject = **DET ∪ VISION ∪ EYE flags** (any one fails the page). PANEL is authoritative on doctrine.

---

## A. The user's 4 rules (2026-06-30)

| ID | rule | HOW | FAIL when |
|----|------|-----|-----------|
| **LV-G1** | **≥1 animated cell per page** — the whole grid or at least one sub-cell must move (veo hero OR a 9:16 reuse clip OR a Ken-Burns still). No fully-frozen page. | DET | a page's cell list has 0 cells of kind `v` and 0 `kb` with motion (all static PNG) |
| **LV-G2** | **Crop framing is intentional** — each still/clip shows the meaningful part of the frame; no cut-off heads, no feet/fabric/floor/empty as the subject. Anchor to face / eyes / hands / key object. | VISION + EYE | a face is clipped at the frame edge, or the cell centers on a non-expressive region |
| **LV-G3** | **No clip used twice** — every cell sources a distinct asset. Reuse from the catalogue first; if none fits, create new. Near-identical Christ-face clips also count as a repeat. | DET (+ VISION for near-dupes) | the same `src` path appears in 2 cells across the episode, OR vision flags two cells as near-identical |
| **LV-G4** | **Visuals match the narration beat** — every cell depicts what its beat actually says; nothing invented, nothing off-topic. | VISION + PANEL | a cell shows an element not in (or contradicting) its beat text |

## B. The gaps I flagged (must-add)

| ID | rule | HOW | FAIL when |
|----|------|-----|-----------|
| **LV-G5** | **Captions sourced from the LOCKED narration** — caption text is pulled verbatim from the locked narration (KJV-verbatim for any red-letter quote), NOT hand-paraphrased. Then **force-aligned to THIS audio** (page windows from `alignment.json`, not the shorts spec) so captions never desync and `-shortest` never truncates a beat. | DET | a caption string is not a substring of the locked narration, OR page windows don't sum within tolerance of the audio duration |
| **LV-G6** | **Doctrine, per page + per episode** — God / THE_LORD never shown with face or body (light / glory / caption only); period-correct (ancient biblical — no modern / medieval / European dress, no Buddha-style idols); the episode lands on Christ. The standing **5-CLI doctrinal panel** runs on the narration before lock. | VISION (per page) + PANEL (per episode) | any page depicts the Father, a modern/anachronistic element, a wrong-culture idol; or the episode never lands on Christ; or the panel flags a real doctrinal error |
| **LV-G7** | **Reading order = story order** — cells are laid out so the eye follows the narration L→R then T→B. The beat sequence must match the cell raster order. | DET (+ EYE) | a cell's beat index is out of raster order on the page |

## C. Carried from existing memories (apply here too)

| ID | rule | HOW | source |
|----|------|-----|--------|
| **LV-G8** | **No backwards / boomerang motion** on directional content — poured blood must not un-pour, a torn veil must not un-tear, a walker must not moonwalk. Set `fill` mode per still (boomerang only for atmosphere-dominant locked-camera stills). | DET (`physics_motion_check.py`) + EYE | a one-way-motion clip is set to boomerang/reverse fill |
| **LV-G9** | **World consistency across the whole episode** — each recurring character keeps ONE locked face (Moses, the witness, Christ); palette / period / lighting stay coherent page-to-page, not just within a page. Author a per-episode World Bible before render. | VISION + EYE | a character's face drifts between pages, or palette/period breaks |
| **LV-G10** | **9:16 reuse clips stay NATIVE** — a portrait reuse clip is contain-fit in its cell (true proportions, no crop / zoom / upscale). Only the 16:9 veo hero cover-fills its 16:9 cell. | DET | a 9:16 source is rendered cover-cropped (output AR ≠ source AR) |
| **LV-G11** | **Never animate writing** — no generative motion on a scroll / titulus / codex / sign; Kling/veo morph letters into garbled text. Hold as a still or deterministic push-in. | DET (flag scenes tagged text) + EYE | a text-bearing cell is set to a generative animate |

## D. Budget / economy (advisory, not pass/fail)

| ID | rule | HOW |
|----|------|-----|
| **LV-B1** | ≤1 veo per page (the one paid hero); prefer Ken-Burns + native reuse for the rest. | DET (warn) |
| **LV-B2** | Reuse-first, **aspect-matched** — 9:16 reuse fills a `col` rail; a wide cell needs a fresh 16:9 veo, never an upscaled portrait. | DET (warn) |

---

## Build order (how a real long-form page run should go)

1. **Lock the narration** → run **LV-G6 panel** (5-CLI doctrinal) → fix or answer every flag.
2. **Force-align** the narration to its audio → page windows from `alignment.json` (**LV-G5**).
3. **Pick template per beat** → assign cells; enforce **LV-G1** (≥1 animated), **LV-G7** (reading order), **LV-B1/B2** (budget).
4. **Source assets** → catalogue-first, **LV-G3** (no dup), **LV-G10** (native 9:16), **LV-G2** anchor crops.
5. **Set motion** per cell → **LV-G8** (physics fill), **LV-G11** (no animated text).
6. **Render page** → **VISION** pass for LV-G2/G4/G6/G9 → **EYE** gallery review.
7. **Mux** score + ambient bed → final.

## Status of validators

- **Built today:** none — this is the spec only.
- **Reuse existing:** `physics_motion_check.py` (LV-G8), the 5-CLI panel via `independent_review.py` (LV-G6), the still period/identity Vision audit (LV-G2/G6/G9), `clip_anim_qc` filmstrip (LV-G2 anchors).
- **To build (DET):** LV-G1, LV-G3 (dup-slug set), LV-G5 (caption ⊆ narration + window-sum), LV-G7 (raster order), LV-G10 (AR match), LV-G11 (text-tag flag).
- These only matter **if landscape is adopted for a real long-form build** — for the EW04 template they're the carry-forward checklist.
