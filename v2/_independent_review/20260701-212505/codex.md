# Independent review — codex (OK, 253s)

**Findings**

- **Blocking: “Every non-negotiable is backed by a gate” is false.** MC-G5 names `new check_captions`, MC-G6 names `new check_audio_mix`, and MC-G3 names `new check_wound_continuity`; these do not exist. MC-G1/G2 exist only partially in [render_lint/verify.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/render_lint/verify.py:111), and the spec itself says “wire into,” not wired.

- **The INV-13 override is under-specified and conflicts with live long-form rules.** The phrase “this spec wins” does not reconcile `LONGFORM_SPEC.md` LF-INV-3, which still says “veo3_1_lite is the long-form animation model,” or LF-CLIP-DURATION, which expects ≥7.5s clips. The artifact also says “Existing gates… CLIP-* … still apply unchanged,” but `CLIP-VIRAL` currently requires ≥6 crop-cuts, while MC-R2 requires “only the camera moves” 5s Kling pushes.

- **BytePlus is not a production `/stills` provider.** MC-R1 says “BytePlus Seedream 4.5 + ref-lock,” but the reusable providers in [pipeline/visual_render.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/visual_render.py:98) are `nbp` and `hf`. BytePlus lives in batch-local scripts under `batches/cluster_01_cross/...`, so the plan is promoting a pilot driver without defining the provider interface, retries, audit sidecars, or cost ledger integration.

- **“Promote `landscape_engine.py` to production” is premature.** The referenced long-form engine is inside `longform/_style_poc/ew04/_mocomic/`, still uses “veo” naming, hardcoded EW04 paths/assets, and `landscape_validate.py` imports `build_ew04_sequence.py` in `main()`. That is not a production, episode-agnostic long-form path.

- **The cost model is materially wrong for animation.** The artifact claims “~13 Kling clips (~$0.65 ea ≈ $8.5),” but Cluster 1 records HF `kling3_0 pro 9:16 5s = 12.5 cr ($1.88)` and 12 clips at about `$22`. A 13-clip short is closer to `$24–25` before stills/audio, not `$9–10`.

- **The long-form economy is unproven.** MC-R7 says “≤1 paid hero per page + native-9:16 reuse” and “10–14 pages” for 6–8 minutes. That implies very long pages held by reused portrait rails/Ken Burns, but no retention, pacing, or doctrinal coherence gate proves that this can carry a long-form deep-dive.

- **Reuse systems are split.** MC-R8 mandates root `asset_index.json`, while production reuse decisions currently flow through `clip_library/index.json` plus `pipeline/clip_reuse.py`. The spec does not define which index is authoritative or how root `asset_index` feeds the existing clean/topical/coherence gates.

- **MC-G4 is mislabeled deterministic.** “No legible pseudo-alphabet” is listed as D, but current checks are prompt/slug based, not pixel/OCR based. A visual gibberish-text failure can still pass if the slug/prompt does not advertise writing.

- **Audio gates are aspirational.** MC-R5/MC-G6 require loudness matching, cleared room, gated reverb, bell, thinned CTA, and no choir pad, but the real implementation is a piece-local `add_music_sfx.py`. There is no generic `check_audio_mix`, no fixture, and no fail-closed verifier.

- **Brand/reverence risk is not gated.** The plan introduces “kinetic captions,” “payload keyword in RED,” and “zoom-snap” motion punches around sacred material, but only MC-G7’s manual “sound/soul” pass catches over-sensationalization. That is too weak for a binding Christian brand/doctrine spec.

VERDICT: FAIL
TOP FIXES:
1. Reconcile INV-13/LF-INV-3/CLIP-* with an explicit motion-comic override matrix and remove incompatible “unchanged” gates.
2. Convert BytePlus, motion-comic assembly, landscape engine, caption, audio, and validation from batch/POC scripts into episode-agnostic modules with real tests.
3. Replace the cost model with measured HF/BytePlus ledger integration and block spend on true per-model estimates.
