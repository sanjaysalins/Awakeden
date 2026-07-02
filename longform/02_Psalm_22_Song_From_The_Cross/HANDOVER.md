# HANDOVER — build the Psalm 22 dynamic graphic-comic (16:9 long)

Paste this to the builder (Fable). It is self-contained: read the spec, then build.

---

## The task
Rebuild the finishing layer of the Psalm 22 16:9 long-form so it feels like our LOCKED short —
**dynamic, fast-cut, designed comic** — not a slideshow.

**READ FIRST (source of truth):**
`longform/02_Psalm_22_Song_From_The_Cross/RESUME_DYNAMIC_COMIC_SPEC_v2.md`
(v2 — resolves the caption/still-count/verse-width contradictions and has a measurable Definition of Done.)

**Reference the failure, don't repeat it:** the current slideshow cut is
`longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/mocomic_16x9_full.spec_preview.mp4`.
**The bar to hit** is the locked short in `batches/cluster_01_cross/father_forgive_them/`.

## Environment / how to run (Windows, PowerShell + Git-Bash)
- Repo root: `C:\Users\sanjay\PycharmProjects\JesusInTheBible`
- Python: `.venv\Scripts\python.exe` (all scripts). The venv auto-throttles ffmpeg to ~50% CPU
  (`POLITE_CPU` env; set `POLITE_CPU=0` to disable, `33` for a third).
- Key entry points (in the pilot folder unless noted):
  - `still_validate.py` — MUST pass before rendering any still. `render_grounded.py --only <slug> --render`
    renders from `still_specs.json` (BytePlus Seedream, ~$0.05/still, ref-lock).
  - `dynamic_cam.py <slug> --move arc|swoop` — $0 deterministic camera.
  - `animate_full.py --only <slug>` — Kling (HF) hero animation (16:9, ~$0.65/clip).
  - `build_mocomic_16x9.py --spec <spec>.json --clips` — composite.
  - `panel_fit.py` — subject-safe crop solver (import).
  - Doctrine panel: `.venv\Scripts\python.exe independent_review.py "<artifact.md>" --type plan`
- **Higgsfield (Kling) may be down (HTTP 500).** If so: ship complete on `dynamic_cam`, retry the Kling
  heroes later (idempotent), re-composite. Never block the film on the outage.
- Give the user CLICKABLE `file:///C:/...` links to review outputs (they review by eye/ear).

## The 5 things v2 decides (do not re-litigate — build them)
1. **Captions = 3-tier system** (spec §R1/§4B): Tier-1 placed off-subject / Tier-2 designed translucent
   lower-third / Tier-3 re-render a caption-room variant. Build `caption_layout.py` (deterministic,
   uses the anchors). Kill the full-width opaque bottom bar.
2. **Two caption classes** (§R3): kinetic keyword captions = compact ≤50% width; red-letter Scripture =
   plaque (short verse) or translucent band (long verse). Readability of Scripture wins for red-letter.
3. **Pacing = ~70 beats @ ~5s** (§R2), cuts on the words, edit-punch on ACTIVE beats only.
4. **Still set is ~60–70% done** — render **~15–20 more** + re-render the **Tier-3 caption-room list**
   (all via `still_validate.py`). The stills and finishing are COUPLED; don't assume "stills = done".
5. **Motion:** ~15–20 Kling clips, **hard cap ~$15**; dyncam for supports; punch on hooks; writing
   stills = dyncam only.

## Method (critical — do NOT scale blind)
Build `caption_layout.py` → decide the still gap → re-plan and build **ONE movement** as a slice →
**pass the Definition of Done (spec §5)** → **show the user a clickable link + get sign-off** → only
THEN scale to all 7 movements → animate heroes + punch → composite → score + SFX → final DoD pass.

## Definition of Done (spec §5 — must all pass)
Median beat ≤6s · kinetic captions 0% subject-overlap, red-letter band ≤bottom-25% over expendable
region, no opaque full-width slab · no still repeats within 8 beats · every beat moves, ≥40% Kling/punch
· **0 doctrinal/citation errors, KJV verbatim, lands on Christ — verified BOTH self-red-team AND the
5-CLI panel** · every frame eye-audited (no morph/NSFW/chopped-head/dagger-hammer nail) · passes the
side-by-side "short test".

## Do NOT touch
The narration/audio · the tooling (`panel_fit`, `dynamic_cam`, `still_validate`, `render_grounded`,
`comic_engine`) · the LOCKED invariants (spec §7). Only re-render stills the Tier-3 rule names, and
only through `still_validate.py`.

## Budget
Stills+re-renders ≈ $1–2 · Kling ≤ $15 · score/SFX/caption $0. Pre-flight any metered batch and get
the user's OK before spending (the `/cost` discipline).
