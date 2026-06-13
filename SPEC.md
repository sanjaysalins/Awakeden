# SPEC — JesusInTheBible Content Engine

> **Reverse-engineered specification** of the system as built (2026-06-13).
> Describes *what the system does and how it is structured*, derived from the
> code and produced artifacts. For current production status read `STATE.md` /
> `RESUME.md`; for operational context read `CLAUDE.md`. This is the contract,
> not the narrative.

---

## 1. Purpose

A faith-content production engine that turns a Bible topic into finished video:

- **Shorts** — 60-second, 9:16 YouTube Shorts. Viral hook → KJV proof →
  grace-anchored conviction → call-to-Jesus landing. *The first-class product.*
- **Long-form** — 6–8 minute, 16:9 deep-dive "full meal" films that research a
  passage and feed the shorts.

Both run through the same discipline: panel review, independent red-team, and
fail-closed doctrinal/Scripture gates at every stage.

---

## 2. The Four Stages

Each stage is independent, idempotent on LOCKED artifacts, and resumable. They
chain through `cli_pipeline.py` with three **human approval gates**.

```
TOPIC
  │
  ▼  STAGE 1 — TEXT            cli.py            → locked narration + voices
  │       thread discovery → draft tournament → self-review (gates+panel)
  │       → red-team audit → write narration folder
  │
  ▼  ── audio (reused) ──      narration_pipeline.py + per_turn_synth.py
  │       verify→tag→audit → duration-locked narration.mp3 (~59s short / 6-7m long)
  │       ════════════════════ HUMAN GATE 1: approve audio ════════════════════
  │
  ▼  STAGE 2 — VISUAL          cli_visual.py     → scene plan → images → clips
  │   Phase A  discover scenes → review (SP-G1..G9) → red-team → cohesion
  │   ════════════════════ HUMAN GATE 2: approve images (reroll / exclude) ════
  │   Phase B  render PNG per scene (NBP or HF) + per-image Vision audit
  │   Phase C  animate each PNG → Kling clip (image_to_kling.py)
  │
  ▼  STAGE 3 — ASSEMBLY        cli_assemble.py   → viral_cut.mp4 + reel.mp4
  │       build timeline → jigsaw clip↔word plan → review → render → verify
  │       ════════════════════ HUMAN GATE 3: approve clips (exclude) ══════════
  │
  ▼  STAGE 4 — CAPTION         veed_io.caption   → <clip>_captioned.mp4  (final)
OUTPUT
```

**Key principle — design for the cut:** Stage 2 reads the narration *timeline*
and nominates a gospel-pivot hero plus short insert shots up front, so the
clips are built to be assembled, not assembled after the fact.

---

## 3. Stage 1 — TEXT

**Entry:** `cli.py` (interactive) · **Orchestrator:** `pipeline/runner.py` ·
**LLM:** `pipeline/engine.py`

| Step | What happens | Module |
|------|--------------|--------|
| Scripture | Fetch exact KJV verse + pericope (±8 verses), cached | `scripture.py`, `data/kjv_cache.json` |
| Thread (Stage 0) | Propose 3-4 fresh exegetical angles across 4 levers; pin each to a verse; pick the freshest-honest | `engine.py` |
| Draft tournament | 4 **divergent** candidates (distinct thread/hook/conviction/CTA) → judge the hook→CTA arc → synthesize winner + graft best hook/CTA | `engine.py` |
| Self-review | 6-agent panel + 8 gates (G1..G8; G8 = "The Five Questions"); revise while any gate FAILs (≤ `MAX_REVISIONS`) | `engine.py`, `models.py` |
| Red-team | Independent hostile auditor — authoritative, always on | `engine.py` |
| Lock gate | Fail-closed: KJV-strict + cross-artifact cluster check | `lock.py`, `cli_lock.py`, `kjv_strict.py`, `cluster_gate.py` |
| Handoff | Write narration folder; auto-run audio pipeline | `handoff.py` |

**Output folder** (`PythonProject1/jesus/narration/<NN_Title>/v1/`, underscores
no spaces): `narration.md` · `voices.json` · `narration.creation.json` ·
`narration.creation-review.md` · `narration.mp3`.

**Structure — Gospel Five-Beat** (`data/structures.json`, 60 s total):
Hook (0-8s) → Point (8-18s) → Proof (18-40s, KJV at normal pace) → Conviction
(40-52s, grace-anchored) → Landing (52-60s, restate + invite).

**Audio** is **reused, not reimplemented**: `narration_pipeline.py` +
`per_turn_synth.py` (ElevenLabs, multi-voice when the scene has speakers,
duration-locked ~59 s). `VOICE_MAP` holds 40+ speaker→voice_id mappings.

---

## 4. Stage 2 — VISUAL

**Entry:** `cli_visual.py "<v1 folder>"` · **Orchestrator:** `visual_runner.py`

**Flags:** `--provider {nbp,hf}` · `--plan-only`/`--no-render` · `--no-animate`
· `--short-only`/`--no-short-only` · `--max-retries N` · `--kling-skip-audit` ·
`--replan`

### Phase A — Scene plan (paper, ~$3 Opus)
`discover_scenes` (Stage V0) generates a candidate pool across visual-arc beats
(prompt target ~18-25) and selects 14-20 final scenes (cap 24). **Binding mix** (SP-G9 deterministic): hero singles +
≥4 unified multi-vignette scenes + Jesus/NT-link + OT-echo. Self-review = 6
agents + 9 gates (SP-G1..G9, with deterministic pre-checks before LLM judges) →
independent audit → `paper_cohesion` (blocking if FAIL).
Writes `visual/scene_plan.json` + `_source_prompts.md` + review files +
`cohesion.paper.json`.

### Phase B — Render (~$0.30 HF / ~$0.50 NBP per image)
One PNG per scene from `style_base + subject_block + mood_block + style_tail`
(fixed Flemish-Baroque oil style). Two providers:
- **HFProvider** — Higgsfield CLI `nano_banana_2`, neutral plates, no ref.
- **NBPProvider** — Gemini `gemini-3-pro-image-preview`, attaches
  `ref_jesus_<variant>.png` for Christ/face consistency.

Each PNG gets a **Claude Vision content audit** (checks `subject_block` +
vignettes + visible_elements + banned tokens) and a `<stem>.cut_hint.json`
sidecar (macro_elements + pacing + viral_role). PNG + passed-audit sidecar =
skip on re-run. Writes per-provider `index.html` gallery.

### Phase C — Animate (~$0.65/clip Kling)
Subprocess `image_to_kling.py` with `KLING_SKILL_PATH=adhoc/SKILL_locked.md`:
Stage A Vision cut-plan (`.kling.json`) → Stage A.5 audit (skip with
`--kling-skip-audit` on Baroque) → Stage B **Kling 3.0** image-to-video render
(`.mp4`). The cut-plan is an 8-beat viral edit (full→mid→close→macro→return)
*inside a single clip* — camera-only reframing on a frozen tableau, no subject
motion.

**Animation is split by format (locked):**
- **Shorts → direct-Kling** (`VIDEO_PROVIDER=kling`). Only Kling executes the
  crop-cut viral plan; HF's NSFW filter also blocks the cross.
- **Long-form → `veo3_1_lite` via HF** (`VIDEO_PROVIDER=hybrid`,
  `VIDEO_DURATION=8`), hybrid falls back to direct-Kling for the NSFW-blocked
  cross. Veo is a generative animator, *not* a crop-cut editor.

---

## 5. Stage 3 — ASSEMBLY

**Entry:** `cli_assemble.py "<v1 folder>"` · **Orchestrator:** `assembly_runner.py`

**Flags:** `--provider {nbp,hf}` · `--clips {N|all}` · `--plan-only` ·
`--no-reel` · `--no-verify` · `--hero N` · `--exclude N,N` · `--speed-cap F` ·
`--rebuild` · `--replan`

| Step | What | Module |
|------|------|--------|
| Timeline | Build from per-turn `__atempo` audio (not scrambled meta) | `assembly_timing.py` |
| Align | Forced per-word phrase board | `assembly_align.py` |
| Load clips | From `scene_plan.json` + ffprobe durations | `assembly_timing.py` |
| Jigsaw plan | LLM matches each clip to its narration phrase | `assembly_engine.py` |
| Allocate | Deterministic speed-first / trim-past-cap | `assembly_engine.py` |
| Gates | AS-G1..G9: G1-G7 deterministic (incl. AS-G6 hero=gospel-pivot, AS-G7 "Gospel Frame"/Christ-close), AS-G8 panel beat-continuity, AS-G9 advisory beat-density | `assembly_engine.py` |
| Render | trim+setpts+scale/pad → 1080×1920 30fps CFR; concat; mux narration | `assembly_ffmpeg.py`, `assembly_render.py` |
| Verify | Per-slot Vision audit (Opus on sacred frames, fail-closed) | `assembly_render.py` |

**Output:** `viral_cut.mp4` (60 s) + `all_takes_reel.mp4` + `index.html`.

**Assembly rules (locked):**
- **Hero = gospel-pivot, never the emotional climax** (AS-G6). Hero must be
  cross / Christ / NT-gospel-link.
- **Open on the animated hook clip, close on the hero still** (`ASSEMBLY_OPEN_MODE=hook`).
- **Every cut closes on Christ** (AS-G7 "Gospel Frame").
- **Never reuse a clip in one video.** Pool size is the lever; more clips sped
  up = more moments. Each clip matches its narration phrase.
- **Speed caps:** 2.2× general, **1.3× reverence cap** on sacred clips.

---

## 6. Stage 4 — CAPTION (final step on every clip)

`.venv\Scripts\python.exe -m veed_io.caption --video "<clip>" [--script <scripture>]`
— offline ($0) ffmpeg/libass + faster-whisper timing, ivory default look.
Output `<clip>_captioned.mp4`. WhisperX phoneme forced-align for long-form
(feed a clean spoken script). This is the standing last step on every finished
clip.

---

## 7. Seamless Pipeline + Human Gates

**Entry:** `cli_pipeline.py` · **Orchestrator:** `pipeline/orchestrator.py`

One topic→cut flow. State persisted in `pipeline.state.json` (provider / hero /
excluded / notes). Artifact-driven position detection makes it resumable.

- **GATE 1 (audio):** approve the narration MP3.
- **GATE 2 (images):** approve stills. `--reroll N,N` re-render weak ones;
  `--exclude N,N` drop bad images *before paying Kling to animate them*
  (the chief cost lever); `--hero N` set the bookend.
- **GATE 3 (clips):** approve clips; `--exclude N,N` drop glitchy clips
  (auto-replans).

```
cli_pipeline.py                              # NEW topic (interactive)
cli_pipeline.py "<v1>" --continue            # cross one gate
cli_pipeline.py "<v1>" --reroll 6,11         # GATE 2: re-render
cli_pipeline.py "<v1>" --hero 7 --continue   # GATE 2: set hero
cli_pipeline.py "<v1>" --exclude 3,10 --continue  # GATE 2/3: drop + continue
```

---

## 8. Cross-Cutting Systems

### 8.1 LLM routing — agent bridge
`LLM_PROVIDER=agent` (default) routes **all** engine LLM calls (text, Vision,
Kling cut-planner) through the in-chat Claude Code agent via a file bridge
(`pipeline/agent_bridge.py`, `.agent_bridge/`) — **zero metered API spend**.
`LLM_PROVIDER=api` uses the metered Anthropic API.
Models: text = `claude-opus-4-7`; review/judge = `claude-sonnet-4-6`; coarse
Vision audit = `claude-haiku-4-5-20251001`.

### 8.2 Quality gates (fail-closed)
| Gate | Enforces | Module |
|------|----------|--------|
| KJV-strict | Exact-verbatim Scripture | `kjv_strict.py`, `data/kjv_corpus.json` |
| Cluster | No templated repetition across sibling artifacts | `cluster_gate.py` |
| Doctrine | Doctrinal landmine scan | `doctrine_gate.py` |
| Lock | Fail-closed chokepoint before audio | `lock.py` / `cli_lock.py` |
Unit-tested: `test_kjv_strict.py`, `test_cluster_gate.py`, `test_doctrine_gate.py`, `test_lock.py`.

### 8.3 Enforced independent review
`independent_review.py` — after every LOCKED narration and every SIGNIFICANT
plan, an outside multi-CLI panel (**cursor primary** + claude/gemini/codex/grok
via local CLI subscriptions, **no metered API**) reviews adversarially in
parallel. Each writes a raw review + `VERDICT: PASS|REVISE|FAIL`. The
convergent flags are verified by hand before declaring done.
`--type {narration,plan}`, `--providers`, `--context`, `--red-team`.

### 8.4 Recursive learning
`pipeline/learning.py` + `data/learning/` — a calibration loop that captures
what the external panel catches that self-review misses, builds a defect ledger
+ taxonomy, and proposes (user-approves) strengthening the deterministic gates.

### 8.5 Cost tracking
`pipeline/cost.py` + `data/spend_ledger.jsonl` — per-episode cost ledger;
`hf generate cost` for exact pre-flight, `hf account transactions` to
reconcile; per-episode ceilings (~$25 short, ~$40 long). Budget doc:
`PSALM22_SHORTS_BUDGET.md`.

### 8.6 Reusable asset libraries
| Library | Holds | Manager |
|---------|-------|---------|
| `_library/` | 9:16 hero stills (reuse-classified) | `cli_library.py`, `pipeline/hero_library.py` |
| `image_library/` | 16:9 Baroque plates | `index.json` |
| `music_library/` | Suno instrumental beds (doctrine-gated, approval-gated) | `_specs.py` |
| `sound_library/` | SFX / ambience | `index.json` |
| `veed_io/` | Offline caption tooling (code module, no asset index) | `caption.py` |
**Topical-fit rule:** only thread-neutral plates may be reused across episodes;
story-specific stills never cross into unrelated episodes.

---

## 9. Cost Model (general ~$23/episode, ±30%)

This is the documented general estimate (metered API). Kling clips ~$11 (48%) ·
images ~$5 (22%) · Opus planning across 3 stages ~$5-6 · audio ~$0.50 · Vision
audits small. In agent-mode the LLM lines drop to $0, so an actual Psalm 22
short budgets to **~$17-18** (10 NBP + 6 HF stills + QC + 14 Kling clips;
ceiling $25), per `PSALM22_SHORTS_BUDGET.md`.
**Levers:** exclude bad images at GATE 2 (never animate them); Haiku for coarse
assembly verify; cached constitution prompt prefix.
**Provider split (locked):** NBP $0.50 (Christ/face), HF nano_banana_2 $0.30
(neutral plate), direct-Kling $0.65 (animation). Agent-mode LLM = $0.

---

## 10. Repository Map

```
config.py                  env, models, paths, voice map, ALL knobs (55+ env vars)
cli.py / cli_visual.py / cli_assemble.py / cli_pipeline.py / cli_library.py / cli_lock.py
independent_review.py      multi-CLI external review

pipeline/
  engine.py runner.py handoff.py            TEXT
  scripture.py series.py structures.py      inputs
  kjv_strict.py cluster_gate.py doctrine_gate.py lock.py   GATES (+ tests)
  agent_bridge.py                           zero-cost LLM routing
  visual_engine.py visual_runner.py visual_render.py visual_handoff.py   VISUAL
  assembly_*.py (engine/runner/timing/align/ffmpeg/render/handoff)       ASSEMBLY
  video_render.py                           video provider ABC
  orchestrator.py                           seamless pipeline + 3 gates
  learning.py cost.py hero_library.py panel.py review_voice.py
  models.py visual_models.py assembly_models.py   DATA MODELS

data/
  constitution.md          60s charter + VISUAL ARC second charter
  series.json              ~10 series, ~76 episodes (hook/cta/guardrails)
  structures.json          Gospel Five-Beat (timed beats)
  kjv_cache.json kjv_corpus.json           Scripture
  learning/                defect ledger + taxonomy

longform/                  produced episodes (Isaiah 53 long, Psalm 22 long + 8 shorts, ...)
_library/ image_library/ music_library/ sound_library/ veed_io/   reusable assets
STATE.md RESUME.md README.md *_PLAN.md *_BUDGET.md    status + strategy docs
```

---

## 11. Data Models (selected)

- **TEXT** (`models.py`): `Beat`, `Draft`, `ThreadCandidate`/`Thread`,
  `GateResult` (PASS/CONDITIONAL/FAIL), `AgentVerdict` (STRONG/CAUTION/REVISION NEEDED),
  `Review` (LOCKED/REVISE/REWORK).
- **VISUAL** (`visual_models.py`): `SceneCandidate`, `Scene` (subject_block,
  mood_block, macro_elements, vignettes, viral_role, shot_kind, jesus_variant…),
  `ScenePlan`, `ScenePlanReview`, `CohesionAudit`, `ImageAudit`.
- **ASSEMBLY** (`assembly_models.py`): `NarrationSegment`, `Phrase`,
  `ClipAsset`, `EditSlot` (role, speed_factor, op), `EditPlan`,
  `EditPlanReview`, `AssemblyAudit`.

---

## 12. Locked Invariants (do not relitigate without the user)

1. **Viral-hook + CTA-to-Jesus 60 s shorts** — not the non-preachy "Attenborough" model.
2. **Gospel Five-Beat** structure, timed.
3. **Grace-anchored conviction** — no gain/loss / fear / manufactured pressure.
4. **Freshness = faithful depth** — surprising about the *text*, never the *truth*.
5. **One thread spine** through hook → middle → CTA; reshape lines, never swap threads.
6. **KJV verbatim** in script; attribution frames stay narrator voice.
7. **Multi-voice when the scene has speakers** (parables: Jesus tells, characters speak).
8. **Independent red-team is standard** at every stage; LOCKED on 0 FAIL gates.
9. **External multi-CLI review is enforced** before "done."
10. **Binding visual scene mix** (SP-G9); never 100% single illustration.
11. **Assembly hero = gospel-pivot; every cut closes on Christ** (AS-G6/G7).
12. **Kling-friendly state-only language** — frozen tableau, camera-only motion.
13. **Animation split:** shorts = direct-Kling, long-form = veo3_1_lite/hybrid.
14. **Shorts are first-class** — highest QC, native 9:16, never a cropped long still.
15. **Reuse downstream pipelines** (`narration_pipeline.py`, `per_turn_synth.py`,
    `image_to_kling.py`) — subprocess, never duplicate.
16. **Caption is the final step** on every finished clip.
```
