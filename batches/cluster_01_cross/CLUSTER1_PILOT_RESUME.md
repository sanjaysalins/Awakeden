# CLUSTER 1 (THE CROSS) — pilot resume · pick up here

**Date paused:** 2026-06-30 · **Pilot piece:** "Father, forgive them" (Luke 23:34), inked motion-comic 9:16 short.
**Spend so far:** ~$1.50 (audio synth ~$0.50 + 7 inked stills 7 cr ~$1). HF balance ~4800 cr.

## The bigger frame (why this piece)
We're producing the whole corpus by **shared visual world**, not series. Plan + manifest:
- `BATCH_PLAN.md` (root) — 7 visual-world clusters, build order Cross→Resurrection→Wilderness→Genesis→Ministry→Nativity/Throne.
- `batches/batch_manifest.json` — machine-readable: cluster → pieces → shared_elements → asset_status.
- Validators: `longform/_style_poc/ew04/_mocomic/LANDSCAPE_VALIDATION.md` + `landscape_validate.py` (6 DET gates, wired as a build pre-flight).
- This is the FIRST piece of Cluster 1, run as a PILOT to lock the inked look before batching the other ~8 cross shorts.

## DONE ✅
1. **Narration LOCKED** → `batches/cluster_01_cross/father_forgive_them/narration.md` (v4).
   - Authored in-chat (Anthropic key dead) → my red-team → **3 independent 5-CLI panel passes**.
   - Panel earned its keep: caught a REAL doctrinal error (labeled Christ's *intercession*, not His atoning
     *death*, as "the heart of the gospel" — a Rom 5:8 swap) my own red-team under-weighted. Fixed → 4/4 PASS.
   - v4 = duration trim to the 60s charter (~150 words), redundancy-only, all KJV verbatim preserved.
   - Panel transcripts: `father_forgive_them/_independent_review/`.
2. **Audio DONE + user-approved** → `father_forgive_them/audio/narration.mp3` (57.15s, natural pace).
   - 3 voices: narrator (Grounded Narrator) + jesus (red-letter) + **scripture = the gravitas "God-1" voice**
     (user-chosen as the dedicated KJV reader). Synth: `per_turn_synth.py --target 59 --natural --no-gate`.
   - The pipeline's verify/tag stages HANG (dead Anthropic key) — bypass them: hand-write `narration-tagged.md`
     (`<speaker name="x">...`) from the locked script + run per_turn_synth directly with `PYTHONIOENCODING=utf-8`.
3. **7 inked stills RENDERED + eyeballed** → `father_forgive_them/visual/nbp/01..07_*.png`; gallery `visual/gallery.html`.
   - Driver: `father_forgive_them/render_stills.py` (imports `longform/_base_elements_refs.py` render+STYLE; idempotent).
   - LOOK VALIDATED: inked graphic-novel style is excellent, Christ face CONSISTENT across panels, period-accurate, doctrine clean.
   - Beat sheet: `father_forgive_them/visual_beats.md` (7 panels mapped to narration + anchors + furniture + motion).

## NEXT (tomorrow) ▶▶
1. **Re-roll 2 stills** (~2 cr, ~$0.30) — both flagged on my eyeball:
   - `05_pierced_hand` — re-prompt TIGHT on the wounded hand only (no face); it currently reads face-dominant + near-dup of 07.
   - `07_risen_hero` — re-roll TEXT-FREE; seedream hallucinated a gibberish speech bubble because the locked STYLE
     literally names "NO speech bubbles" (seedream has NO negative channel → naming it DRAWS it). Pass a style
     string WITHOUT the text-negation clause for this re-roll.
2. **Animate** (the ~$13 spend, get the user's explicit go first) — 7 × Kling-pro 9:16 5s = **87.5 cr (~$13.13)**.
   - Driver: `_hf_animate_short.py <short_dir> --duration 5` (reads `visual/scene_plan.json` + `visual/nbp/NN_*.png`).
   - NEED FIRST: write `father_forgive_them/visual/scene_plan.json` (per-scene motion) — not built yet.
   - Shorts stay GENERATIVE (user rule) — no ffmpeg/kenburns cheapouts.
3. **Composite the motion-comic furniture** ($0) — write the 9:16 comic spec (the SHORTS engine, NOT landscape):
   - Engine: `longform/_style_poc/ew04/_mocomic/comic_engine.py` (1080×1920) + driver `build_episode.py` + a spec JSON.
   - Spec schema: `{episode, anim_dir, prefix, audio, beats:[{t:[t0,t1], tpl, clips:[{slug,motion,bias}], cap:{type:caption|redletter,...}}]}`.
   - Red-letter bar for the [jesus] prayer; Scripture bar for "And they parted his raiment, and cast lots."
   - audio = `father_forgive_them/audio/narration.mp3` (or a captioned/scored version).
4. **Assemble + caption**, then run the validators (`landscape_validate.py` siblings) + final watch.
5. **THEN batch the other ~8 cross shorts** off the locked look (manifest `clusters[0].net_new_to_build`).

## Exact unit costs (live `hf generate cost`, 2026-06-30)
- seedream_v4_5 inked still = **1 cr** ($0.15). · kling3_0 pro 9:16 5s = **12.5 cr** ($1.88).

## Gotchas locked in (memory)
- seedream **input_images ref-lock is BROKEN** (HF rejects `generate create ... --input_images [{id,type,url}]`, rc=3).
  Render NO-REF + carry a consistent character descriptor in every prompt for face consistency (worked well here).
- seedream **no-negative channel**: never NAME what to omit ("no text/speech bubbles/nails/glow") — it DRAWS it.
  Describe the positive end-state. The locked STYLE's "NO text..." clause leaks gibberish on speaking panels.
- HF **502s are transient** — render_stills.py is idempotent; just re-run to fill gaps.
