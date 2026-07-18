# CLAUDE.md — JesusInTheBible narration-creation engine (operational context)

Loaded at the start of every session. Reference material, not narrative.
For current progress read `STATE.md`. For "what to do first tomorrow" read `RESUME.md`.

> **THE CONTRACT:** `v2/SPEC.md` is the single binding source of truth — stages,
> invariants (INV-1..INV-22), the full gate registry, the reuse manifest, the
> cost model, and the A/B protocol. The per-stage skills in `.claude/skills/`
> are the repeatable procedures that enforce it. When this file and `v2/SPEC.md`
> disagree, the spec wins; update the spec, don't drift. (v1's reverse-engineered
> `SPEC.md` is superseded.)

## Engineering behavior (applies to every code AND pipeline change)

Bias toward caution over speed. For trivial tasks, use judgment.

**1. Think before acting.** State assumptions explicitly; if uncertain, ask. If
multiple interpretations exist, present them — don't pick silently. If a simpler
approach exists, say so. If something is unclear, stop and name it.

**2. Simplicity first.** Minimum that solves the problem, nothing speculative. No
features beyond what was asked, no abstractions for single-use code, no
"flexibility" that wasn't requested, no error handling for impossible scenarios.
If 200 lines could be 50, rewrite it.

**3. Surgical changes.** Touch only what you must. Don't "improve" adjacent code,
don't refactor what isn't broken, match existing style. Remove only the
imports/vars YOUR change orphaned; mention pre-existing dead code, don't delete
it. Every changed line should trace to the request.

**4. Goal-driven execution.** Turn the task into a verifiable goal and loop until
it passes (e.g. "add validation" → "write tests for invalid inputs, then make
them pass"). For multi-step work, state a brief plan with a verify-check per step.
For this engine the standing verify is: 0 FAIL gates + the full test suite green +
(for any LOCK) the 5-CLI panel.

## What this project is

A **gospel-short content engine** for 60-second YouTube Shorts. Takes a Bible
topic and produces (1) an engaging, viral-hook, **CTA-to-Jesus** narration
(KJV) with multi-voice audio, then (2) a **scene-planned, image-rendered,
Kling-animated visual track** ready for final cutting.

Four stages, each independent and each with the same gates / panel / red-team
discipline:

1. **Text** (this project, `cli.py`): topic → locked script.
2. **Audio** (REUSE `PythonProject1/jesus/narration_pipeline.py` + `per_turn_synth.py`):
   script → duration-locked MP3.
3. **Visual** (this project, `cli_visual.py`): script → scene plan → images
   (Higgsfield CLI `nano_banana_2` or Gemini "Nano Banana Pro") → Kling
   animations.
4. **Assembly** (this project, `cli_assemble.py`): clips + narration MP3 →
   intelligent clip↔word jigsaw → deterministic speed/trim allocation → 60s
   `viral_cut.mp4` (hero bookend) + `all_takes_reel.mp4`. POC — iterating.

All four chain via **`cli_pipeline.py`** — one seamless, resumable flow with three
HUMAN quality gates (you approve the audio, the images, and the clips). Deep pool
kept for curation; excluding a clip is the curation lever (and excluding a bad
*image* at the image gate skips paying Kling to animate it). Cut-aware planning
(hero designed up front + inserts) and parallel/clip-reuse are the queued Part 2/3.

## How the text+audio pipeline works

```
pick series+episode (or custom topic)
  → fetch exact KJV verse + wider pericope (bible-api.com, cached, ±8 verses)
  → discover_thread (Stage 0, Opus 4.7) — propose 3-4 candidates across the
       4 levers (overlooked detail / original-language / NT-confirmed OT echo
       / cultural-historical), pin each to a verse, pick the freshest-honest
  → generate draft — DRAFT TOURNAMENT (default): 4 DIVERGENT candidates (distinct
       thread/hook/conviction/CTA, parallel) → judge the hook→CTA arc → synthesize
       winner + graft best hook/CTA. De-templated CTA. (ENGINE_TOURNAMENT=0 → single draft.)
  → self-review (6 panel agents + 7 gates G1..G7; revise while any gate FAILs)
  → INDEPENDENT red-team audit (fresh hostile auditor; authoritative; ALWAYS ON)
  → write <NN_Title>/v1/ into PythonProject1/jesus/narration/  (NEW folders use
       underscores, no spaces — click-to-open paths; legacy space-named folders kept as-is)
       narration.md · voices.json · narration.creation.json · narration.creation-review.md
  → audio auto-run: narration_pipeline.py verify→tag→audit, then
       per_turn_synth.py --target 59 --pre-quote-pause 0.4 --stability 0.65
       → duration-locked narration.mp3 (~59s, multi-voice when scene has speakers)
```

## How the visual pipeline works

```
cli_visual.py <path-to-v1-folder> [--provider hf|nbp] [--plan-only] [--no-render]
              [--no-animate] [--short-only|--no-short-only] [--kling-skip-audit]

Phase A (paper, ~$3 Opus):
  → discover_scenes (Stage V0, Opus 4.7) — propose 18-25 candidates across
      visual arc beats; pick 14-20 final scenes (configurable, cap 24)
      Mandatory mix (SP-G9 deterministic): hero singles + 4+ unified
      multi-vignette scenes + Jesus/NT-link + OT-echo scenes
  → self-review (6 panel agents + 9 gates SP-G1..SP-G9; deterministic
      pre-check on SP-G2/G5/G6 vignettes/G8/G9 BEFORE LLM judges)
  → INDEPENDENT scene-plan audit
  → paper_cohesion (Opus over narration + plan; blocking if FAIL)
  → write <v1>/visual/ artifacts: scene_plan.json + _source_prompts.md
      + scene_plan.review.md + scene_plan.independent-review.md
      + cohesion.paper.json

Phase B (render, ~$0.30/image HF or ~$0.50/image NBP):
  → Provider produces PNG per scene (style_base + subject_block + mood_block + style_tail)
      - HFProvider: subprocess ~/bin/hf.exe (Higgsfield), default nano_banana_2
        for Baroque oil painting (HF-POC rated winner). No reference attachment.
      - NBPProvider: google.genai gemini-3-pro-image-preview, attaches
        ref_jesus_<variant>.png from nano_banana_pro_batch_output for char consistency
  → Per-PNG Claude Vision content audit (now checks subject_block + vignettes,
      not just visible_elements — earlier narrow audit silently passed wrong scenes)
  → Idempotent: PNG + passed-audit sidecar = skip on re-run
  → Each PNG gets a <stem>.cut_hint.json sidecar (macro_elements + pacing + viral_role
      for the downstream Kling stage)
  → write <v1>/visual/<provider>/index.html for browser review (cards w/ #NN ref badges)

Phase C (animate, ~$0.65/clip Kling):
  → Subprocess PythonProject1/jesus/image_to_kling.py with KLING_SKILL_PATH env
      = adhoc/SKILL_locked.md (locked-discipline cut-plan SKILL)
  → image_to_kling.py Stage A (Claude Vision cut plan, .kling.json)
      → Stage A.5 audit (often nit-picks on Baroque — use --kling-skip-audit)
      → Stage B Kling 3.0 image-to-video render (.mp4 per PNG)
```

## File map (this project)

```
config.py                     env, model, paths, voice map, all knobs
cli.py                        interactive text/audio entry point
cli_visual.py                 visual-stage entry point (--provider, --plan-only, etc.)
data/constitution.md          the 60s charter + VISUAL ARC section
data/series.json              10 greenlit series (76 episodes)
data/structures.json          narration structures; default = gospel-five-beat
data/kjv_cache.json           cached exact-KJV lookups (also passage:<ref> wider)

pipeline/series.py            load/query series
pipeline/structures.py        load/render structures
pipeline/scripture.py         exact KJV + context + wider passage fetch
pipeline/models.py            Draft (beats), Thread, Review, Beat, GateResult, AgentVerdict
pipeline/engine.py            text Opus calls: discover_thread / generate / review /
                                independent_review / revise
pipeline/handoff.py           write narration folder + auto-run audio pipeline
pipeline/runner.py            orchestrates a text/audio run

pipeline/visual_models.py     Scene (incl. macro_elements/vignettes/pacing/viral_role/
                                jesus_variant), ScenePlan, ScenePlanReview,
                                ImageAudit, CohesionAudit, GateResult
pipeline/visual_engine.py     visual Opus calls (CUT-AWARE: take the narration `timeline` →
                                nominate gospel-pivot hero_candidate + ~2s shot_kind=insert for
                                tiny beats; design-for-the-cut rules): discover_scenes / review_scene_plan /
                                independent_review_scene_plan / revise_scene_plan /
                                paper_cohesion / enrich_unified_scenes; deterministic
                                gate pre-checks (SP-G2/G5/G6-vignettes/G8/G9)
pipeline/visual_render.py     ImageProvider ABC + NBPProvider + HFProvider; assemble_final_prompt;
                                verify_image (Claude Vision content audit, checks subject_block
                                + vignettes + visible_elements + banned tokens); render_scene
                                with retry-on-audit loop; cut_hint sidecar writer
pipeline/visual_handoff.py    write paper artifacts + run_kling_pipeline subprocess wrapper;
                                index.html generator (per-scene cards w/ #NN refs + inline <video> clips)
pipeline/visual_runner.py     orchestrates Phase A + Phase B + Phase C with idempotence

cli_assemble.py               assembly-stage entry (--clips, --plan-only, --hero, etc.)
pipeline/assembly_models.py   NarrationSegment, ClipAsset, EditSlot, EditPlan,
                                EditPlanReview, AssemblyAudit
pipeline/assembly_timing.py   build_timeline (from _turns __atempo audio, NOT the
                                scrambled meta) + load_clips (scene_plan + ffprobe)
pipeline/assembly_ffmpeg.py   ffprobe_duration + render_segment (trim+setpts+scale/pad,
                                1080x1920 30fps CFR) + concat_copy + mux_narration
pipeline/assembly_engine.py   plan_edit (LLM jigsaw) + allocate (speed-first/trim-past-cap)
                                + AS-G1..G7 gates + review/independent/revise
pipeline/assembly_render.py   render_cut + render_reel + verify_cut (per-slot Vision)
pipeline/assembly_handoff.py  edit_plan.json + reviews + timeline + upstream_notes +
                                index.html (timeline jigsaw + embedded cut/reel)
pipeline/assembly_runner.py   orchestrate plan→review→render→verify; idempotent on LOCKED
                                (--exclude drops clips; replans automatically when set changes)

cli_pipeline.py               ONE seamless topic→cut entry; 3 human gates (--continue/--reroll/--exclude/--hero)
pipeline/orchestrator.py      composes the 4 stage runners; artifact-driven position detection;
                                pipeline.state.json (provider/hero/excluded); image-gate-before-Kling cost saver
pipeline/video_render.py      VideoProvider ABC + HFVideoProvider (hf kling3_0, motion-only prompt,
                                integer duration, NSFW→raise) + KlingDirectProvider (image_to_kling fallback)
                                + HybridVideoProvider (HF→fallback on NSFW). animate_scenes(); VIDEO_PROVIDER=hybrid

narration_gate.py             $0 EARNED hook+landing gate (run BEFORE spend on every new
                                narration): FAILs stock closers ("come to Jesus" family)
                                unless the piece's own KJV uses the verb, unearned landings,
                                template hooks; WARNs corpus-stale closer verbs
pipeline/finality.py          the ONE "what is the final video" rule + content sha (v2/RELEASE_SYNC.md)
pipeline/release_state.py     per-piece release state (manifest join x finality x pack x thumbs x site x ledger)
release_check.py              $0 fail-closed SYNC gate (SYNC-G1..G7) — run before any _website deploy / after posting
upload_tracker.py             THE one write path for posted URLs: --set <slug> <platform> <url>
                                -> dated data/release_ledger.json (+ manifest youtube_id for YT)
production_board.py           the human board — same release_state, rendered (_PRODUCTION_BOARD.html);
                                EPISODES roll-up (long+shorts as one unit of work) above the flat table
pipeline/episode_state.py     Episode = a long + its parent-linked shorts, DETECTED not declared
build_upload_tracker.py       _UPLOAD_TRACKER.html — paste-URL posting runbook; episodes render as
                                one release-campaign block (long + shorts together), not flat cards
README.md                     user-facing docs
```

## Run

```
.venv\Scripts\python.exe cli.py                            # interactive text + audio
.venv\Scripts\python.exe cli.py --no-audio                 # text only

.venv\Scripts\python.exe cli_visual.py "<v1 folder>"                          # full visual pipeline (Phase A+B+C)
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --plan-only              # just the scene plan
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --no-animate             # plan + images, no Kling
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --provider hf            # Higgsfield (default)
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --provider nbp           # Nano Banana Pro
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --no-short-only          # render all scenes, not just short_priority
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --kling-skip-audit       # bypass nit-picky Stage A.5 audit

.venv\Scripts\python.exe cli_assemble.py "<v1 folder>"                        # full assembly (cut + reel + verify)
.venv\Scripts\python.exe cli_assemble.py "<v1 folder>" --plan-only            # edit plan + reviews, no render
.venv\Scripts\python.exe cli_assemble.py "<v1 folder>" --clips all            # force all 16 clips (may strobe)
.venv\Scripts\python.exe cli_assemble.py "<v1 folder>" --no-reel --no-verify  # cut only
.venv\Scripts\python.exe cli_assemble.py "<v1 folder>" --hero 7 --speed-cap 2.2  # force hero + cap
.venv\Scripts\python.exe cli_assemble.py "<v1 folder>" --exclude 3,10         # drop glitchy clips (replans)
.venv\Scripts\python.exe cli_assemble.py "<v1 folder>" --rebuild --replan     # ignore idempotence

# Seamless end-to-end pipeline with 3 human gates (audio / images / clips):
.venv\Scripts\python.exe cli_pipeline.py                                      # NEW topic (interactive)
.venv\Scripts\python.exe cli_pipeline.py "<v1 folder>" --continue             # cross one gate
.venv\Scripts\python.exe cli_pipeline.py "<v1 folder>" --reroll 6,11          # GATE 2: re-render weak images
.venv\Scripts\python.exe cli_pipeline.py "<v1 folder>" --hero 7 --continue    # GATE 2: set hero + continue
.venv\Scripts\python.exe cli_pipeline.py "<v1 folder>" --exclude 3,10 --continue  # GATE 2/3: drop clips + continue
```

## Cost model (~$23/episode, ±30%)

Kling clips ~$11 (48%) · images ~$5 (22%) · Opus planning across 3 stages ~$5-6 ·
audio ~$0.50 · Vision audits small. **Levers:** exclude bad images at GATE 2 so
they're never animated; `VISION_AUDIT_MODEL`=Haiku for the coarse assembly verify
(subtle per-image audit stays Opus); constitution prefix is prompt-cached.

## Required env

- `JesusInTheBible/.env`: `ANTHROPIC_API_KEY`. Optional: `CLAUDE_MODEL` (default
  `claude-opus-4-7`), `CLAUDE_MAX_TOKENS` (default 32000), `MAX_REVISIONS`,
  `INDEPENDENT_REVIEW`, `REVIEW_MODEL`, `NARRATION_STRUCTURE`, `SHORTS_MODE`,
  `SHORTS_TARGET_SECONDS`, `TARGET_WORDS_*`, `THREAD_DISCOVERY`,
  `PASSAGE_WINDOW`, visual knobs (`VISUAL_*`, `HF_MODEL_ID`, `HF_CLI_PATH`,
  `GEMINI_API_KEY`, `KLING_SKILL_PATH`, `NBP_REFS_DIR`).
- `PythonProject1/.env`: `ELEVENLABS_API_KEY` (audio), `GEMINI_API_KEY` (NBP),
  Kling credentials (already in place from prior HF-POC work).

## Locked decisions (do not relitigate without the user)

- **🔒 NON-NEGOTIABLE — sound doctrine, proven BOTH ways** (user, 2026-06-26):
  every piece's doctrine must be SOUND and GROUNDED IN THE BIBLE, and verified
  BOTH independently (my own red-team/self-check) AND by the 5-CLI panel — never
  one alone. A clean self-check is not enough; a panel PASS is not enough on its
  own. Reject if EITHER flags a real doctrinal/grounding error.
- **🔒 NON-NEGOTIABLE — the whole Bible, through Jesus** (user, 2026-06-26): the
  series reads the ENTIRE canon (OT + NT) with Christ as the lens; every piece
  traces its thread to and LANDS ON Jesus. This is the spine, never optional.
- **Model: viral-hook + CTA-to-Jesus 60s shorts** — NOT the non-preachy/no-CTA
  "Attenborough" model.
- **Structure: Gospel Five-Beat** (Hook→Point→Proof→Conviction→Landing, timed).
- **Grace-anchored conviction** — NO gain/loss / self-interest framing, NO
  manufactured pressure. The Spirit convicts; the script invites.
- **Independent red-team audit is standard practice** — always on,
  authoritative, at every stage (text, scene plan, image, eventually animation).
  LOCKED on 0 FAIL gates; CONDITIONAL/CAUTION advisory.
- **EXTERNAL independent review is ENFORCED** (see the section below) — every LOCKED
  narration AND every SIGNIFICANT plan is reviewed by an outside multi-CLI panel
  (cursor primary + claude/gemini/codex/grok) via `independent_review.py` BEFORE it is
  called done. I address (or explicitly answer) the findings; the user decides on any
  REVISE I dispute. This is in addition to the in-engine red-team, not a replacement.
- **Freshness = faithful depth** — surprising about the *text*, never about
  the *truth*. Novelty in entry point; orthodoxy in claim and landing.
- **One thread spine through hook → middle → CTA**, mirrored hook → climax →
  closing in the visual arc. Never swap threads to placate freshness feedback;
  reshape the lines instead.
- **KJV verbatim** in the script; attribution frames stay in narrator voice.
- **Multi-voice when scene has speakers** — parables = Jesus tells the story,
  inner character lines get their own voice (narrator → jesus → narrator → son
  for the prodigal).
- **Visual scene mix is binding** (SP-G9 deterministic): hero singles +
  multi-vignette unified + Jesus/NT-link + OT-echo. Target 14-20 scenes for
  rich passages; never 100% single.
- **Assembly hero = the gospel-pivot, never the emotional climax** (AS-G6
  deterministic). The hero bookends the cut open AND close, so it carries the
  landing — it must be the cross / Christ / NT-gospel-link image. Every cut must
  close on Christ (AS-G7 gospel-frame survival + reverence speed cap on sacred
  clips). The doctrinal Vision verify runs on Opus for sacred frames, fail-closed.
- **Multi-element unified scenes carry 3-5 named vignettes** (SP-G6 deterministic),
  each as a soft-edged background memory, never in panels/arches/windows.
- **Kling-friendly state-only language** — image is a frozen tableau; only the
  camera moves (per `adhoc/SKILL_locked.md`).
- **Comic-grid panel animator tiering** (cost control, locked 2026-07-17, TIGHTENED
  2026-07-17 same day): **every panel on every screen must be a real generative
  animated clip — Ken Burns / `dynamic_cam` is NOT an acceptable substitute anywhere,
  full stop.** (Earlier same-day framing allowed ≥1 real panel per grid with the rest
  on $0 Ken Burns — the user explicitly overrode that a few hours later: "every screen
  should use animated clips.") Default clip animator is **Seedance 1.5 Pro** (~4.8cr
  vs Kling's ~10cr). The 2026-07-17 bake-off (`longform/04_The_Bronze_Serpent/v1/
  visual_16x9_inked/_bakeoff_i2v/index.html`) showed Seedance matches Kling on a calm
  single-figure panel but INVENTS motion on multi-figure/action panels (a coiled
  serpent uncoiled and slithered, a raised hand moved to a different pose, a frozen
  hammer-strike continued its swing) — so **Kling is reserved for panels with
  action/crowd/complexity**; calm single-figure panels stay on Seedance. Comic-style
  multi-panel grid stays the default layout; **hero stills / important images get a
  single full-bleed panel**, not chopped into a multi-panel grid — that single panel
  still needs a real clip. **Reuse-first for 9:16 grid panels:** before generating a
  new panel clip for a 9:16-shaped slot, check the shorts' own rendered clips (native
  9:16, HF Kling pro gallery-tour) for a topically-matched one and drop it in
  near-natively (per `vertical-panels-cross-aspect-reuse`) — $0 beats Seedance beats
  Kling, in that order, whenever a matching shorts clip already exists. This is a real
  cost increase over the original same-day framing — confirm the spend estimate with
  the user before converting a piece's remaining Ken-Burns panels.
- **Reuse downstream pipelines, do not duplicate** — `narration_pipeline.py`,
  `per_turn_synth.py`, `image_to_kling.py` are subprocess'd, not re-implemented.
- **Panel-variety gate for comic grids** (locked 2026-07-17): a full-film eye
  survey of Bronze Serpent found 9 of 20 multi-panel grids showing visually
  redundant content — two panels of the same crucifixion face close-up, two
  panels of the same "light shaft through clouds," etc. `panel_variety_lint.py`
  (per-episode, e.g. `longform/04_The_Bronze_Serpent/panel_variety_lint.py`) is
  the deterministic $0 guard: every still used in a multi-panel grid needs a
  short category tag in `visual_tags.json` (subject+pose+framing, e.g.
  `christ-face-closeup`, `wounded-hand-macro`, `light-shaft-clouds`); the lint
  FAILS any grid where 2+ panels share a tag, and WARNs if one camera-motion
  direction dominates >60% of panels. **This deterministic tag-check is a
  floor, not the ceiling** — it caught 6 of 9 real collisions automatically;
  the other 3 needed a human eye-check because the redundancy was about
  composition/mood once cropped into the panel shape, not raw subject tag (see
  `always-independent-red-team` / `feedback-verify-by-looking-not-running`).
  Run the lint AND look at every multi-panel grid's actual composited frame
  before calling a comic-grid piece done — an untagged or newly-added still
  must get a tag before it enters a grid.

## Independent review gate (ENFORCED — cursor + panel)

Replicates the user's `ai-panel` independent-review pattern, self-contained in this repo
as `independent_review.py`. **Standing rule: I do my work, THEN an outside panel reviews it
before I call it done.** Mandatory for (a) every LOCKED narration and (b) every SIGNIFICANT
plan (architecture, a new pipeline/stage, a spend-bearing batch design — not trivial edits).

```
.venv\Scripts\python.exe independent_review.py "<artifact.md>" --type narration   # or --type plan
.venv\Scripts\python.exe independent_review.py "<artifact.md>" --type plan --providers cursor,claude
```

- Reviewers (adversarial, read-only, parallel): **cursor primary** + claude + gemini + codex +
  grok — all via the user's LOCAL CLI subscriptions (**no metered API**; they consume CLI usage).
- Each writes a raw review + a `VERDICT: PASS|REVISE|FAIL` + top fixes to
  `<artifact_dir>/_independent_review/<stamp>/`; I read them, **verify the convergent flags
  myself** (don't trust a verdict blindly — see `always-independent-red-team`), synthesize the
  merged verdict, and fix or explicitly answer each before declaring done.
- A REVISE I disagree with goes to the user, not silently ignored.
- Validated 2026-06-04 on the Isaiah 53 long-form: 4/5 reviewers caught a real Acts 8:35
  KJV-verbatim elision the in-engine pass had missed. Memory: `enforced-independent-review`.

## What NOT to do

- Do NOT invent doctrine or use contrarian/clickbait readings to chase freshness.
- Do NOT add gain/loss or fear framing to the conviction/CTA.
- Do NOT duplicate any of the downstream pipelines (narration / per_turn_synth /
  image_to_kling).
- Do NOT hand-edit files inside the PythonProject1 narration tree casually —
  the engine owns that output; writing *new* files there is fine, in-place
  edits are guarded. Exception: surgical scene-plan tweaks (e.g. renaming a
  vignette in scene_plan.json) are OK when the change is too small to justify
  a full revise call.
- Do NOT switch model IDs without the user. Default models: text = claude-opus-4-7;
  image = `nano_banana_2` (HF for shorts / NBP "Nano Banana Pro" for long-form).
  **Animation is SPLIT by format:**
  - **Shorts → HF Kling pro** (`_hf_animate_short.py`, `hf.exe generate create kling3_0
    --mode pro --duration 5 --aspect_ratio 9:16`), executing the hard-cut gallery-tour
    cut-plan (full→element→element→return) *inside a single clip*. **direct-Kling
    (`image_to_kling.py`) is the FALLBACK ONLY for NSFW/bare-torso-cross stills HF
    refuses.** Bake-off history: 2026-05-29 direct-Kling beat plain HF Kling 3.0 on the
    OLD prompt; **2026-06-18 re-bake-off (same still + byte-identical gallery-tour prompt +
    5s, `_bakeoff/compare.html`) flipped it — HF Kling pro rendered 1076×1924 and stayed
    faithful, direct-Kling rendered 716×1284 and hallucinated a garbled "BINTX" titulus
    not in the still.** So shorts default to HF-pro for quality/faithfulness; direct-Kling
    keeps the NSFW cross. (Was "Shorts → direct-Kling"; the 2026-06-15 session had already
    moved to HF-pro, now confirmed by the re-bake-off + the user.)
  - **Long-form (16:9 deep-dives) → veo3_1_lite** via HF (`VIDEO_PROVIDER=hybrid`,
    `VIDEO_HF_MODEL=veo3_1_lite`, `VIDEO_DURATION=8`). Bake-off verdict (2026-05-30):
    veo3_1_lite keeps the Baroque oil look without softening it to photoreal, across
    every scene type, at ~half Kling's credits; hybrid falls back to direct-Kling for
    the NSFW-blocked cross. `seedance1_5` is the fallback (more dynamic but photoreal-
    softens). HFVideoProvider is now model-aware (per-model media flag / no Kling-only
    `--mode`·`--sound` / duration snapped to the model's legal set).
  - **Settled (2026-05-30):** veo CANNOT execute the shorts' viral cut-plan. Fed the
    exact 8-beat `image_to_kling` cut-plan, Kling did crisp crop-cuts (frozen tableau);
    veo ignored the "cut to / no invented movement" discipline — it animated the subject
    (the father actually ran), used dissolve/morph transitions, and invented elements
    (a hand reaching in to grab the ring). Veo is a generative *animator*, not a crop-cut
    editor. Kling is the permanent shorts animation model; veo is long-form only.

## Working with the user

Honest pushback over validation. Short sentences. No preamble/recap.
**Look at images yourself with the Read tool** when the user flags a problem —
don't trust the SDK audit's pass/fail signal blindly (see memory:
`feedback-kling-skip-audit`, `always-independent-red-team`).
