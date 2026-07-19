# LONGFORM SPEC v1 — Long-form Content Engine (binding contract)

> **Relationship to SPEC.md:** This is the parallel contract for 16:9, 6–8 min deep-dives.
> All invariants (INV-1..24) in `v2/SPEC.md` apply unless explicitly overridden here.
> Where this spec and `v2/SPEC.md` conflict, this spec wins for long-form work.
> The per-stage long-form skills in `.claude/skills/*-long/` enforce this contract.
>
> Status/narrative: `STATE.md` / `RESUME.md`. Operational context: `CLAUDE.md`.
> The existing pilot is `longform/01_Isaiah_53_Suffering_Servant/v1`.

---

## 1. Format & purpose

**Long-form:** 16:9, 6–8 min, reverent documentary pace.
**Function:** Research foundation — the long is written first; shorts are distilled cuts from it (longs-first funnel, LF-INV-1). Never produce a Types & Shadows short without the long already locked.
**Series:** Types & Shadows (Awakened Catalogue). Topic order: Passover Lamb → Bronze Serpent → Seed of the Woman → Day of Atonement / Scapegoat → Melchizedek.
**Audience:** A curious viewer who wants depth, not just the hook.

Same discipline as shorts: panel review, independent red-team, fail-closed doctrinal/Scripture gates at every stage.

---

## 2. The Pipeline — Stages 0–5

```
TOPIC
  │  STAGE 0 — STUDY        /study          → pericope + locked thread (7-movement spine)
  ▼  STAGE 1 — TEXT         /narrate-long   → locked narration.md + voices.json
  │     thread → 7-movement draft → self-review (LF-G1..G8) → red-team → 5-CLI panel → LOCK
  ▼  STAGE 1b — AUDIO       /voice          → narration.mp3 (multi-voice, ~400–480s)
  │     (same voice pipeline as shorts; longer word budget, same multi-voice rules)
  │     ══════════════════ HUMAN GATE 1: approve audio (by ear) ═══════════════
  ▼  STAGE 2a — VISUAL PLAN /scene-plan-long → 20–25 scenes, LF-SP-G1..G9 + cohesion
  │     ══════════ HUMAN GATE 2a: test-gate (1–2 paid stills, user approves) ══
  ▼  STAGE 2b — STILLS      /stills         → PNG per scene + same IMG-* Vision audit
  │     (same providers: NBP $0.50 for Christ/face, HF $0.30 for neutral plates)
  │     ═══════════════ HUMAN GATE 2b: approve images (reroll / exclude) ══════
  ▼  STAGE 2c — ANIMATE     /animate-long   → veo3_1_lite clip per PNG (LF-CLIP-*)
  │     (atmospheric motion, no locomotion/morphing/invention; boomerang fill)
  │     ══════════════════ HUMAN GATE 3: approve clips (exclude bad) ══════════
  ▼  STAGE 3 — ASSEMBLY     /assemble-long  → <title>_16x9.mp4 (~6–8 min)
  │     scene-window fill → LF-AS-G1..G6 → render 1920×1080 30fps
  ▼  STAGE 3b — SFX/SCORE   /sfx + score   → immersive audio bed + Cinematic-Orchestral
  ▼  STAGE 4 — CAPTION      /caption        → _captioned.mp4 (WhisperX long-form timing)
  ▼  STAGE 5 — DISTIL       /distil         → 3–4 shorts per long (see §LF-INV-8)
OUTPUT
```

**Test-gate before batch (LF-INV-7):** render 1–2 paid stills + animate them before paying for the full 20–25 scene batch. User approves look + veo3 motion before batching.

---

## 3. The 7-movement spine (binding structural contract)

All long-form narrations follow this spine in order (LF-G5 enforces deterministically):

| # | Movement | Role | Approx duration |
|---|---|---|---|
| M1 | **The Picture** | Set the OT scene plainly, as a first-time listener meets it | ~40–60s |
| M2 | **The Problem** | Why this ritual/sign existed; the human need underneath | ~40–60s |
| M3 | **The Strange Detail** | The freshness hook — the oddly specific feature that begs explanation | ~40–60s |
| M4 | **The Match** | Walk the OT text verbatim against the Gospel record; centuries-early | ~60–90s |
| M5 | **The Honest Objection** | Steel-man the "coincidence / over-reading" pushback; then answer it | ~40–60s |
| M6 | **The Exchange** | The substitution heart: what it cost, who it was for (grace-anchored) | ~40–60s |
| M7 | **The Invitation** | Land on Christ; Spirit convicts, script invites; no fear/gain-loss | ~30–50s |

Total: ~330–500s (~6–8 min). Trim words before compressing the voice.

---

## 4. Gate registry (long-form)

> `D` = deterministic (Python validator, fail-closed). `P` = panel agent.
> `A` = advisory. Gates inherited unchanged from `v2/SPEC.md` are noted with (→SPEC).

### TEXT — Stage 1 (`/narrate-long`)

| Gate | Type | Checks |
|---|---|---|
| LF-G1 Biblical Accuracy | D+P | KJV verbatim (same as G1 → SPEC §4) + every claim exegetically defensible in its passage context |
| LF-G2 Passage Depth | P | Does each movement add something a casual reading misses? At least M3 (Strange Detail) must be genuinely non-obvious |
| LF-G3 Conviction | P | Grace-anchored throughout (no gain/loss/fear/shame); M6 Exchange is substitution-clear (Christ bore the penalty, did not merely set an example) |
| LF-G4 Invitation | P | M7 lands on Christ specifically; grace-gift not self-help; does NEW work — not a recycled "will you trust Him?" |
| **LF-G5 7-Movement Structure** | **D** | All 7 movements present, in order; each movement > 100 words; total 950–1400 words for 6–8 min. **Validator: `validators.lf_movements`, enforced in `cli_lock.py --form long` since 2026-07-19** (before that this row claimed D with no code behind it). Word-budget enforcement is corpus-calibrated: within 10% of the band → WARN (Day of Atonement locked at 1426), beyond 10% → BLOCK. Applies only to '## Movement N' format; witness/legacy long formats get a WARN, not a block |
| LF-G6 Craft | P | Standalone, plain prose, clean pacing; no paragraph starts the same way twice |
| LF-G7 Thread Integrity | P | One thread spine carried through all 7 movements; M3 Strange Detail resolves in M4 Match; M5 Objection strengthens M6; closing mirrors the opening image |
| **LF-G8 Honest Objection Quality** | **P** | M5 must steel-man the real pushback (not "some people wonder if…" strawman); the answer must address the specific concern raised, not pivot away from it |
| KJV-strict | D | Exact verbatim span match (→SPEC §4; same `test_kjv_strict.py`) |
| Doctrine | D | Landmine scan: universalism / trinity-severed / works / fear-gain-loss; PLUS long-form extras: LF-DOCTRINE-SUPERSESSION (types don't cancel Israel's story), LF-DOCTRINE-PENAL-CLEAR (M6 Exchange must not reduce to "Jesus suffered so we don't have to" without naming the *penalty* he bore) |
| Narrative-presence | D | Same as SPEC §4 INV-4 — refuse lock if an absent character is asserted as eyewitness |

> **Word budget:** 950–1400 spoken words. At 150 wpm natural pace = 380–560s. Aim for the middle (1100–1250 words ≈ 440–500s). Trim the longest movement first.

### SCENE PLAN — Stage 2a (`/scene-plan-long`)

> **Schema note:** The long-form pipeline uses a DIFFERENT `scene_plan.json` format
> from the shorts engine (`pipeline/visual_engine.py`). Long-form format (proven on Isaiah 53):
> `{scenes: [{id, mvt, t:[start, end], title, camera, atmos, sfx, directional, ...}]}`.
> Lives at `visual_16x9/scene_plan.json`. It is hand-authored or produced by a dedicated
> long-form scene plan script — NOT output by `pipeline/visual_engine.py` (which writes
> the shorts `ScenePlan` format with `slug/subject_block/shot_kind`). The two formats are
> incompatible; do not mix them.

| Gate | Type | Checks |
|---|---|---|
| LF-SP-G1 Biblical Accuracy | P | Every literal scene defensible vs pericope |
| **LF-SP-G2 Movement Coverage** | **D** | Every movement (M1–M7) has ≥2 scenes; no movement is visually skipped. Requires `mvt` field on each scene. **Validator: `validators.lf_movement_coverage()` (real since 2026-07-19), part of `validators.lf_scene_plan()` which also enforces deterministically: Christ-close final scene, ≥1 Jesus scene, ≤60% Christ-centric, non-empty `atmos` veo3 hint per scene, and LF-SP-G5 banned tokens (negation-aware; 'frame' excluded — calibration over all 134 approved scenes showed its every post-negation hit was doorframe/off-frame/16:9-frame idiom). Scene-count vs LF-INV-4 is WARN-only (approved dense rebuilds run 27–32). All 5 locked plans sweep clean.** |
| LF-SP-G3 Visual Variety | P | Not repetitive; long-form cliché blocklist (see §clichés) |
| LF-SP-G4 Theological Honesty | P | Symbolic scenes carry no foreign doctrine |
| LF-SP-G5 Prompt Conformance | D | No banned tokens in subject/mood blocks (same T1–T6 → SPEC §4) |
| LF-SP-G6 Type Discipline | D | Unified scenes carry 3–5 named vignettes, never panels/arches/windows (→SPEC §4) |
| LF-SP-G7 Character Consistency | P | Jesus/disciples identical across scenes; jesus_variant consistent |
| LF-SP-G8 Composition Distribution | D | ≥3 framings; none >40% of scenes (tighter than shorts 50% cap — at 22 scenes, variety matters more) |
| **LF-SP-G9 Scene Mix & Gospel Frame** | **D** | ≥2 unified multi-vignette + ≥1 Jesus/NT-link + ≥1 OT-echo + ≥1 hero Christ-close; never 100% single-subject |

**Scene count:** 20–25 scenes. Calibration: ~1 scene per 18–24s of narration. At 7 min (420s) → 18–23 scenes.

**Long-form cliché blocklist** (in addition to the shorts blocklist in `data/constitution.md`):
- "Moses raising the staff dramatically" (show the crowd looking, not Moses acting)
- "A glowing golden cross" (Baroque wood, not fluorescent)
- "Jesus teaching on a hillside with a crowd" as the M6 Exchange scene (M6 is specifically about substitution, not teaching)
- Curtain/veil shot as the ONLY M6 image (needs the human cost alongside)

### STILLS — Stage 2b (`/stills`)

**Same gates as shorts** (IMG-SUBJECT / IMG-ELEMENTS / IMG-ANATOMY / IMG-NOTEXT / IMG-PERIOD / IMG-TONE / IMG-COHERENT).

**Same providers:** NBP ($0.50) for Christ/face scenes; HF `nano_banana_2` ($0.30) for neutral plates. Same T1–T6 guardrails.

**Veo3-aware still design** (additional requirement):
- Every still's `subject_block` prose must include 1–2 **atmospheric motion hints** — subtle features veo3 can animate without inventing new content (e.g. "a torch casts flickering light on the stone walls", "desert fabric stirs in a dry wind", "dust motes drift in a shaft of light through the opening"). These hints are written INTO the existing `subject_block` field; there is no separate schema key.
- Avoid stills where the ONLY interesting feature is human movement (running, pointing, dramatic gesture) — veo3 will animate it, violating LF-CLIP-NOLOCOMOT.
- When authoring the veo3 prompt in `/animate-long`, extract the atmospheric hint from the `subject_block` prose — it is not stored as a separate field.

### CLIP (veo3 animation) — Stage 2c (`/animate-long`)

| Gate | Type | Checks |
|---|---|---|
| **LF-CLIP-ATMOSPHERE** | P-Vision | Clip has visible atmospheric motion (flame, fabric, light — veo3 must not produce a static JPEG lookalike) |
| **LF-CLIP-NOLOCOMOT** | P-Vision | No subject locomotion: no walking, running, dramatic reach/point/grab sequences; human figures may breathe, hold posture, or turn slightly |
| LF-CLIP-NOMORPH | P-Vision | Faces, hands, and forms stable frame-to-frame — no melting, halo-bloom, or morphing (→SPEC CLIP-NOMORPH) |
| **LF-CLIP-NOINVENT** | P-Vision | No elements not in the still: no extra figures, no hands entering frame, no invented objects; veo3 may interpret ambiguous areas but not materialize new subjects |
| LF-CLIP-NOWRITING | D | Writing scenes (scroll / titulus / codex / sign) are NOT animated with veo3 — hold as a still or give a deterministic ffmpeg push-in (→SPEC INV-17 NEVER-ANIMATE-WRITING) |
| **LF-CLIP-DURATION** | D | Clip is ≥7.5s (veo3 at 8s, accounting for boomerang transitions); short clips flag for a continuation or boomerang |

**Verdict discipline (since 2026-07-19):** LF-CLIP-* verdicts are recorded as
fail-closed `.clipqc.json` sidecars via `pipeline/clip_qc.py` (`record_verdict`
after a REAL look at the extracted frames; `LF_CRITERIA` states the rules;
`python -m pipeline.clip_qc "<clips dir>" --dir --frames` for the worklist).
`_assemble_16x9.py` checks every scene's clip and refuses assembly when
`JITB_REQUIRE_CLIPQC=1` (report-only by default until an episode's clips are
backfilled — same rollout pattern as INV-23). No sidecar = UNVERIFIED, never
assumed passing (INV-24).

**Veo3 prompt discipline (the animate-long recipe):**
```
Baroque oil painting in motion. [Subject description from subject_block].
Atmospheric motion only: [atmospheric_element from still — e.g. torch flame flickers, fabric stirs in wind, dust motes drift].
Camera makes one slow [pan left / drift in / pull back] across 8 seconds.
No human movement. No new elements. The people hold their pose as if frozen in paint.
Painterly atmospheric life only.
```
- Keep prompts under 80 words.
- Do NOT give veo3 a multi-beat cut-plan (it will ignore it and animate the subject instead — confirmed 2026-05-30).
- Hybrid fallback: `VIDEO_PROVIDER=hybrid` (veo3_1_lite → direct-Kling for NSFW-blocked scenes).

**Fill strategy for time windows:**
- **Camera-only / static scenes** → seamless boomerang (forward + reverse, looped) via `_assemble_16x9.py`.
- **Directional scenes** (processional, crowd movement) → forward-chain continuation clips (`<stem>_cont1.mp4`, etc.), generated in advance.
- **Writing scenes** → deterministic ffmpeg Ken-Burns push-in (never veo3).

### ASSEMBLY — Stage 3 (`/assemble-long`)

| Gate | Type | Checks |
|---|---|---|
| LF-AS-G1 Timeline Coverage | D | Scene windows tile [0, audio_dur] contiguously; no gap > 0.5s. **Validator: `validators.lf_assembly()` (real since 2026-07-19) — also carries G4 movement-coverage (incl. clip-on-disk per movement), G6 gospel frame, and G5 hero-window when a `hero` flag exists. WINDOW-LANE ONLY (`_assemble_16x9.py`): do not run it on a livingpage-lane scene_plan, whose `t` values are still-source metadata and whose contiguity the beat-spec builder asserts itself. All 4 window-lane plans sweep clean.** |
| LF-AS-G2 No Reuse | D | Each clip (or boomerang of a clip) appears for exactly one scene window; no clip reused across scene slots |
| **LF-AS-G3 Pacing Health** | D/A | Avg playback rate ≤1.3× (voice sets the pace, clips fill it); never speed a clip > 2.0×; flag freeze-holds > 15s as advisory |
| **LF-AS-G4 Movement Coverage** | D | Every M1–M7 movement has ≥1 clip in the final cut; no movement is silent-black. Requires `mvt` on each scene. **Enforced by `validators.lf_assembly(plan, audio_dur, clips_dir)` since 2026-07-19 (checks a real `NN_*.mp4` exists on disk for at least one scene of every movement).** |
| **LF-AS-G5 Hero = Christ-at-centre** | D | Hero scene = the substitution/exchange/cross scene (from M6); it is the visual peak; it must appear within the final 90s of the cut |
| LF-AS-G6 Gospel Frame | D | Opening clip = The Picture (M1, an OT scene); closing clip = The Invitation (M7 or hero); cut ends on Christ — never on a crowd, symbol, or landscape alone |

**Assembly tool:** `longform/_assemble_16x9.py` (boomerang + directional chain, $0 ffmpeg).
**Output:** `visual_16x9/<film_name>_16x9.mp4`, 1920×1080 30fps.

> **Critical:** Do NOT use `pipeline/assembly_engine.py` or `cli_assemble.py` for long-form. Those are the shorts assemblers (9:16, 60s, AS-G1..G9). The long-form assembler is `longform/_assemble_16x9.py` exclusively.

### SFX / SCORE — Stage 3b

Same Cinematic-Orchestral standard as shorts (INV-18, `feedback-cinematic-score-standard`):
- Full orchestral (strings + horns + organ), sweeping crescendo, wide reverb.
- NEVER the sparse/minimalist variant.
- Immersive long-form soundstage: narrator voice + character voices + SFX bed (sound_library) + score, each ducked under the next.
- SFX bed: reuse-first from `sound_library/`; generate with ElevenLabs only if no match.
- No dual scores (INV: feedback-no-choir-pad-under-score): SFX beds carry ambience/accents ONLY; the orchestral score is the single musical bed.

### CAPTION — Stage 4

Same `/caption` skill as shorts. For long-form, **WhisperX phoneme forced-align is mandatory** (not offline faster_whisper alone):
- Run `_extract_spoken.py` on `narration.md` to produce a clean spoken script (strip `[narrator]` / `[voice]` / depth notes — only the words spoken).
- Feed the clean script to WhisperX with `--aligner auto` for 1:1 word-level timing.
- Confirmed on Isaiah 53 16:9: 1177/1177 words, 0 interpolated (→`veed-io-whisperx-longform-timing` memory).

---

## 5. Long-form invariants (LF-INV, in addition to INV-1..24 in SPEC.md)

| # | Invariant |
|---|---|
| LF-INV-1 | **Longs-first funnel** — for new Types & Shadows topics, the long is the research foundation; shorts on this topic are distilled from it. Never write a new Types & Shadows short before its long is LOCKED. (Does not apply retroactively to pre-spec content such as Psalm 22 shorts or Isaiah 53 which predated this rule.) |
| LF-INV-2 | **7-movement spine is the structural contract** (not Gospel-Five-Beat). All 7 movements must be present, in order, gated by LF-G5. |
| LF-INV-3 | **veo3_1_lite is the long-form animation model** (INV-13 override for long-form). Do not feed it a crop-cut plan. Hybrid fallback (→direct-Kling) for NSFW-blocked scenes. |
| LF-INV-4 | **20–25 scenes for 6–8 min.** Calibrate: `ceil(audio_dur / 20)` scenes as the floor; cap at 25. |
| LF-INV-5 | **No speed-to-fit** — clips fill their window via boomerang/directional-chain, not atempo or speed > 1.3×. The voice sets the pace. |
| LF-INV-6 | **The Honest Objection (M5) must be a genuine steel-man.** A throwaway "some wonder if…" + immediate dismissal FAILs LF-G8. |
| LF-INV-7 | **Test-gate before batch.** Render 1–2 paid stills + animate with veo3 BEFORE the full batch. User approves look + motion quality. |
| LF-INV-8 | **Shorts distilled from the long must inherit its thread spine.** A short cannot contradict the long's exegesis or introduce a different entry thread. |
| LF-INV-9 | **Landing hold applies to longs** — the ≥3.0s hold + audio/video duration parity rule (canonical: `v2/SPEC.md` INV-26, added 2026-07-19) binds long-form finals exactly as shorts. Gate: `check_landing_hold.py` (also run automatically in the whole-repo scan). New long score recipes author `outro_s: 3.0`; legacy 2.5s pieces are WARN-only, not retrofitted. |
| LF-INV-10 | **Bible-gate is wired into the long animate path** — `bible_kb.gate` (INV-25 chokepoint) is enforced in code by `longform/_animate_16x9.py` + `_animate_directional.py` before any veo3 spend; a still contradicting a `specified`/`constrained` fact card never animates. (Documented 2026-07-19 — the enforcement predates this entry; the spec/skills simply never stated it.) |

---

## 6. Reuse manifest (long-form additions)

All reused subsystems from SPEC.md §6 apply. Long-form additions:

| Subsystem | Entry point | Notes |
|---|---|---|
| veo3 animation | `pipeline/video_render.py::HFVideoProvider` (`VIDEO_PROVIDER=hybrid`, `VIDEO_HF_MODEL=veo3_1_lite`, `VIDEO_DURATION=8`) | REUSE-AS-IS; do not rewrite |
| Long-form assembly | `longform/_assemble_16x9.py` (episode-generic via `_episode.py`) | REUSE-AS-IS; pass episode slug/dir |
| WhisperX align | `veed_io/aligner.py` + `_extract_spoken.py` | REUSE-AS-IS; mandatory for long-form captions |
| Cinematic score | `eleven_music/` + `sfx_pilots/add_music.py` (`regen=False` reuses cached score) | REUSE-AS-IS |
| Immersive soundstage | `longform/_soundstage_cinematic.py` (SFX bed layer) | REUSE-AS-IS |

---

## 7. Cost model (long-form)

Per-episode estimate ~$20–35 (±30%). Set-of-5 ≈ $100–130 media spend.

| Line | Unit cost | Qty | Est. |
|---|---|---|---|
| NBP stills (Christ/face) | $0.50 | ~8 | $4 |
| HF stills (neutral plates) | $0.30 | ~14 | $4.20 |
| veo3_1_lite clips (8s) | ~$0.40 | ~22 | $8.80 |
| Continuation clips (directional) | ~$0.40 | ~4 | $1.60 |
| Audio synth (multi-voice, ~7 min) | ~$1.50 | 1 | $1.50 |
| Cinematic-Orchestral score | ~$2 | 1 | $2 |
| Opus (agent-mode) | $0 | — | $0 |
| **Total** | | | **~$22–35** |

**Ceiling:** $40/long (from `LONGFORM_TYPES_SHADOWS_SLATE.md`). If pre-flight shows > $40, trim scene count or shift stills to reuse.

**Test-gate spend:** $0.90–1.50 for 2 stills + 2 veo3 clips — always pay this before the batch.

**`/cost` pre-flight:** quote exact spend before each metered step and block on INV-20 (ask-before-spending).

---

## 8. A/B parity protocol (long-form)

For the first long-form after Isaiah 53 (pilot):
1. Run the **5-CLI panel** on the narration + scene plan before any metered spend.
2. Compare to Isaiah 53 on: panel verdict (≥4/5 PASS), escaped-defect count, gate FAIL count (must be 0).
3. Human still-review + clip QC before assembly locks.
4. The assembled long must pass LF-AS-G1..G6 with 0 FAIL gates.

---

## 9. Integration with v2/SPEC.md

| SPEC.md reference | Long-form adaptation |
|---|---|
| Stage 1b `/voice` | Same pipeline; word budget 950–1400 (not ~145 shorts budget) |
| Stage 2a `/scene-plan` | Replaced by `/scene-plan-long` for long-form (20–25 scenes, LF-SP-G1..G9) |
| Stage 2c `/animate` | Replaced by `/animate-long` for long-form (veo3 not Kling; no crop-cut plan) |
| Stage 3 `/assemble` | Replaced by `/assemble-long` (boomerang/directional fill, LF-AS-G1..G6) |
| INV-13 | veo3_1_lite confirmed for long-form (this spec adds the gate contract that INV-13 lacked) |
| INV-14 (shorts first-class) | Long-form is the research foundation; shorts from it are still first-class product — the long is not cut corners |
| AS-G3 avg ≤2.0× | Replaced by LF-AS-G3 avg ≤1.3× for long-form |
| CLIP-VIRAL (≥6 crop-cuts) | Not applicable to veo3 long-form; replaced by LF-CLIP-ATMOSPHERE + LF-CLIP-NOLOCOMOT |
