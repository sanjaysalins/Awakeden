# LANDSCAPE_RESUME.md — 16:9 long-form motion-comic TEMPLATE (pick up here)

**Date:** 2026-06-30 · **Status:** template POC built + verified · **Spend this thread: ~9 cr** (1 still + 1 veo).

> **Scope (user, 2026-06-30):** this is a **TEMPLATE / proof-of-concept** of HOW a long-form
> narration page is assembled — NOT a new product, NOT a pivot. We keep posting BOTH shorts
> and longs. Memory: [[ew04-landscape-template-scope]]. Secondary to the base-elements-library
> directive at the top of root `RESUME.md`.

---

## What it is

A 16:9 landscape motion-comic page = a grid of typed cells, each filled at one of 3 fidelities:
- **hero** (16:9) = the ONE paid veo animation per page  `[VEO]`
- **col** (9:16) = an existing shorts clip dropped in **NATIVE** (no crop/zoom)  `[REUSE]`
- **kb** = a still + Ken Burns ($0 cheat)  `[KEN BURNS]`

Budget rule: **≤1 veo per page**; several templates are veo=0, so a long-form alternates paid
pages with free pages and the per-episode veo budget stays flat (~30-35 veo on a ~50-page ep).

## Files (all in `longform/_style_poc/ew04/_mocomic/`)

| file | what |
|------|------|
| `landscape_looktest.py` | 4 static wide pages; reusable helpers (`fill_bias`, `sanitize`, `_box`, colors, FONT, PAGE_W/H) |
| `landscape_engine.py` | the **10-template library** (Core 6 + Extended 4); renders $0 static preview + `_templates/_TEMPLATE_SHEET.png`; 11/12 catalogued not built |
| `landscape_motion_page.py` | single mixed-fidelity page compositor (the first proof) |
| `build_ew04_sequence.py` | **the real 10-page sequence** end-to-end; concats pages + muxes narration |
| `_hero_still.py` / `_hero_veo.py` | render the ONE wide 16:9 hero (HF seedream still → veo3_1_lite 8s) |

**Outputs** (in `_mocomic/_landscape/`):
- ▶ **`EW04_landscape_sequence.mp4`** — 2560×1440, 69.3s, narration+score muxed (the deliverable)
- `hero_serpent_wide.png` (still) + `hero_serpent_wide.mp4` (the veo, idempotent)
- `_seq_f3/f21/f65.png` — canonical review frames
- `EW04_landscape_motion_page.mp4` — the earlier single-page proof

**Run:** `.venv\Scripts\python.exe longform/_style_poc/ew04/_mocomic/build_ew04_sequence.py`  (pure ffmpeg, $0)

## The 10-beat → template map (in build_ew04_sequence.py PAGES)

| # | beat | template | paid |
|---|------|----------|------|
| 0 | dying of snakebite | rail_duo | free |
| 1 | venom = judgment | triptych_cols | free |
| 2 | I begged Him | full_bleed | free |
| 3 | **forge it, lift it high** | **big_inset** | **★ veo** |
| 4 | look, and live | full_bleed | free |
| 5 | the Teacher answered | grid_2x3 | free |
| 6 | John 3:14 (red-letter) | full_bleed | free |
| 7 | lifted Jesus on a pole | full_bleed | free |
| 8 | you who are bitten | rail_duo | free |
| 9 | look, and live (Christ) | full_bleed | free |

---

## RED-TEAM REVIEW (self, 2026-06-30) — verdict: PASS as a template, with carry-forward fixes

**Doctrine — SOUND:**
- Bronze serpent on pole = Num 21:8-9 ✓. God never depicted (caption/glory only) ✓. Lands on risen Christ ✓.
- John 3:14 red-letter is **KJV-verbatim** ✓ ("...even so must the Son of man be lifted up").
- Caption "I begged Him. He would not." = dramatized eyewitness framing of Num 21:7-8 (people asked
  Moses to pray the serpents away; God did NOT remove them — gave the look-and-live remedy instead).
  The remedy-not-removal reading is faithful and IS the thread. OK in eyewitness voice.

**⚠ Carry-forward fixes (must do before any REAL long-form build, not just template):**
1. **Captions are hand-written paraphrases** in `build_ew04_sequence.py`, NOT sourced from the locked
   EW04 narration text. A real build must pull caption text from the locked narration (verbatim for
   KJV quotes). + run the standing **doctrinal 5-CLI panel** on the actual narration (this template
   skipped it because the narration was already locked upstream).
2. **Beat windows are hand-aligned to `ew04.spec.json`** (the shorts spec), not force-aligned to THIS
   audio. `-shortest` truncates on drift → caption desync risk. Real build: align page windows to the
   narration `alignment.json` (see [[alignment-cache-staleness]]).
3. **Hardcoded EW04 asset slugs** (`V("01b_moses_close")` etc.) — fine for POC, needs parameterizing
   to be a general long-form template.

**Honest visual limits (already told user):**
- **5/10 pages fall back to full-bleed Ken-Burns** because ALL reuse art is PORTRAIT (9:16). The rich
  wide templates (`splash_strip`, `band_of_three`, `big_left_L`, `polyptych`) are UNUSED — they need
  fresh **16:9 veo heroes** to shine. That's the upgrade lever.
- **Grid clip cells show cream gaps**: a 9:16 clip can't fill a landscape grid cell without cropping,
  so after the native-fix it sits as a portrait panel with cream beside it (reads as an intentional
  mixed-panel comic; it's sharp). Optional fix = reshape grid 'col' cells to true 9:16 slots.

**The 9:16-NATIVE fix (this session) — VERIFIED:**
- User rule: a 9:16 reuse clip must stay NATIVE in its cell — never cover-cropped/zoomed (it trashes
  resolution). Implemented `fit_box()` + `vid_cell(contain=True)` in `build_ew04_sequence.py`; border
  hugs the actual clip box. Stills still Ken-Burns; the 16:9 veo hero fills its 16:9 cell (contain=False).
- Probe-confirmed: clips render **746×1328** in columns, **364×648** (true 9:16) in grid cells. Zero crop.

---

## NEXT SESSION — decisions waiting on the user

1. **Grid cream gap:** reshape the grid's 2 clip cells into true 9:16 slots (zero gap, $0)? or ship as-is?
2. **Upgrade lever:** spend ~8 cr each on 3-4 fresh **16:9 veo heroes** (camp vista / cross-lifted wide /
   risen-Christ wide) to unlock the rich multi-cell templates on pages 1/5/7/9? (quote + get OK first).
3. **Productionize** (only if we adopt this for real long-form): fix the 3 carry-forward items above —
   captions from locked narration + force-align to audio + parameterize slugs.

**Remember:** this is the SECONDARY thread. Primary tomorrow-directive = the **base-elements library**
(index every character/object/location across all narrations → locked ref per element), top of root `RESUME.md`.
