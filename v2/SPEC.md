# SPEC v2 — JesusInTheBible Content Engine (binding contract)

> **This is the single source of truth.** It supersedes the root `SPEC.md`
> (reverse-engineered v1 description) and absorbs the durable knowledge that
> used to live scattered across ~70 memory files and the "Locked decisions"
> block in `CLAUDE.md`. The per-stage **skills** in `.claude/skills/` are the
> repeatable procedures; this spec is what they enforce. Every non-negotiable
> here is backed by a **fail-closed validator** (no honor-system steps).
>
> Status/narrative live in `STATE.md` / `RESUME.md`. Behavioral + operational
> context lives in `CLAUDE.md`. Authored 2026-06-16 (Phase 0 of the v2 plan).

---

## 1. Purpose

Turn a Bible topic into finished, postable video:

- **Shorts** — 60-second, 9:16 YouTube Shorts. Viral hook → KJV proof →
  grace-anchored conviction → call-to-Jesus landing. **The first-class product.**
- **Long-form** — 6–8 minute, 16:9 deep-dive films that research a passage and
  feed the shorts (write the long first as the research foundation).

Both run the same discipline: panel review, independent red-team, and
fail-closed doctrinal/Scripture gates at every stage.

> **Long-form contract:** `v2/LONGFORM_SPEC.md` is the binding contract for the 16:9
> deep-dives — it defines LF-G1..G8 (text), LF-SP-G1..G9 (scene plan), LF-CLIP-*
> (veo3 animation), LF-AS-G1..G6 (assembly), and LF-INV-1..8 (long-form invariants).
> All INV-1..24 in this file also apply to long-form unless overridden there.
>
> **Motion-comic contract:** `v2/MOTIONCOMIC_SPEC.md` (v1.1) is the pattern for the
> **inked graphic-novel motion-comic** visual line — recipe MC-R1..R10, gates
> MC-G1..G10, the `format`-discriminated schema, the format deltas, and a
> derived (zero-reuse-for-the-first-long) cost model. It **refines INV-13** (inked
> art → Kling camera-only, not veo3, which morphs ink). **SHORT (9:16) rows are
> binding** (proven by the LOCKED Cluster 1 pilot); **all `[LONG]` (16:9) rows are
> PROVISIONAL** until one manual long pilot passes the doctrinal panel + 4-lens
> review + a gravitas A/B — the **Baroque-plate + veo3** long path stays the DEFAULT
> for reverent exegetical deep-dives. Revised after a 4-reviewer red-team (2026-07-01).
> Stage skills for long-form: `/narrate-long`, `/scene-plan-long`, `/animate-long`, `/assemble-long`.

---

## 2. The Pipeline — Stages 0–5

Each stage is independent, idempotent on LOCKED artifacts, resumable, and driven
by one **skill**. Three **human approval gates** remain (audio, images, clips).

```
TOPIC
  │  STAGE 0 — STUDY      /study      → pericope + locked thread (one spine)
  ▼  STAGE 1 — TEXT       /narrate    → locked narration + voices.json
  │     thread → draft tournament → self-review (G1..G8) → red-team → 5-CLI panel → LOCK
  ▼  ── audio (reused) ── /voice      → duration-locked narration.mp3 (~59s short)
  │     ═══════════════ HUMAN GATE 1: approve audio (by ear) ═══════════════
  ▼  STAGE 2 — VISUAL
  │     /scene-plan  → scene_plan.json (SP-G1..G9 + cohesion)
  │     /bible-check → scene_facts.json (Scripture-cited facts: BC-G1..G4) — facts DRIVE + CHECK the stills
  │     ═══════════ HUMAN GATE 2: approve images (reroll / exclude / hero) ═══
  │     /stills      → PNG per scene + Vision audit (IMG-*) + bible audit (BC-G4) + cut_hint sidecar
  │     ── bible-gate (fail-closed) ── no green Bible-Check = no animate spend ──
  │     /animate     → Kling clip per PNG (frozen tableau, camera-only)
  ▼  STAGE 3 — ASSEMBLY  /assemble   → viral_cut.mp4 (+ /sfx bed)
  │     timeline → jigsaw → AS-G1..G9 → render → per-slot verify
  │     ═══════════════ HUMAN GATE 3: approve clips (exclude) ═══════════════
  ▼  STAGE 4 — CAPTION   /caption    → viral_cut_sfx_captioned.mp4  (final clip)
  ▼  STAGE 5 — UPLOAD    /upload     → upload_kit (title/desc/tags/hashtags, UK-G1..G7)
OUTPUT
```

**Design for the cut:** Stage 2 reads the narration *timeline* and nominates the
gospel-pivot hero + short insert shots up front, so clips are built to be
assembled, not assembled after the fact.

### 2L. The LIVING-PAGE lane (motion-comic batch shorts — the lane that ships today)

The cluster shorts (batches/, Awakeden living-page standard) replace stages 2–3
with the manifest-driven lane below. **Entry points:** `cli_livingpage.py "<piece>"
[--continue]` (resumable position board; auto-runs $0 steps only) and
`run_piece.py "<piece>" --stage <stage>` (the per-stage runner). Per-piece data
lives in **`piece.json`** (still prompts/refs, animate moves, score params + dip
phrases, register metadata) — one tested runner, zero per-piece scripts.

```
narration.md + audio/ (Stage 0-1b, unchanged — incl. HUMAN GATE 1)
  ▼  beats spec      livingpage_short.spec.json  (word-timed choreography, /livingpage)
  ▼  manifest        piece.json                  (authored once; new pieces start here)
  ▼  run_piece --stage stills --render           [PAID seedream ~$0.05/still]
  │     lint (regex + structural) → guard_prompt autofix → reuse pre-flight
  │     → render → pending-FAIL audit sidecar (LP-ARM) → ledger row
  │  ══ HUMAN GATE 2: stills_gate.py --build → rubric + adversarial review → --approve ══
  │     + bib_validate (reads the spec; BC-G1/G2 $0)
  ▼  run_piece --stage animate                   [PAID HF kling3_0 pro 7.5cr ≈ $1.13/clip billed]
  │     PASS-sidecar gate → budget ceiling → render → .src.sha hash-bind → ledger
  │     (flow_check pre-filter: PASS skips vision NOMORPH; ESCALATE → vision QC)
  ▼  build_livingpage_16x9 --clips --no-ticks    ($0 ffmpeg; refuses on a red stills gate)
  ▼  run_piece --stage score                     ($0; warns when alignment newer → --stage retime)
  ▼  run_piece --stage register                  ($0 asset_index rows)
  ▼  website (_website/build_readpage.py) → /publish
```

The Baroque scene-plan lane above stays the contract for `cli_pipeline.py`
episodes (long-form + legacy shorts); the two lanes share Stage 0–1b and the
upload/caption tail.

---

## 3. Per-stage contract (the skill is the procedure; this is the contract)

| Stage | Skill | Reused engine (call, don't rewrite) | Output artifact | Gates |
|---|---|---|---|---|
| 0 Study | `/study` | `pipeline/scripture.py`, `engine.discover_thread` | thread + pericope, KJV cache | KJV-fetch, one-thread-spine (INV-5) |
| 1 Text | `/narrate` | `pipeline/engine.py`, `models.py`, `lock.py` | `narration.md`, `voices.json`, `creation.json` | G1–G8, KJV-strict, cluster, doctrine |
| 1b Audio | `/voice` | `PythonProject1/jesus/narration/per_turn_synth.py` (subprocess) | `narration.mp3` (~59s, multi-voice) | duration-lock, voices routing |
| 2a Scene | `/scene-plan` | `pipeline/visual_engine.py` | `visual/scene_plan.json` + cohesion | SP-G1–G9 |
| 2a+ Bible-Check | `/bible-check` | `pipeline/bible_kb.py`, `bib_validate.py`, `bible_gate.py`, `scripture.py` | `_bible_check/scene_facts.json` (sha-bound) + `fact_sheet.md` + `bible_check.status.json` + per-still `.bib_audit.json` | BC-G1–G4 + chokepoint (INV-25) |
| 2b Stills | `/stills` | `pipeline/visual_render.py` (+ `bible_kb.enrich_for_scene`) | PNG/scene + `cut_hint.json` + gallery | IMG-SUBJECT/ELEMENTS/ANATOMY/NOTEXT/PERIOD/TONE/COHERENT + BC-G4 |
| 2c Animate | `/animate` | `PythonProject1/jesus/.../image_to_kling.py` + `SKILL_locked.md` | `.kling.json` + `.mp4`/clip | CLIP-VIRAL, CLIP-IMAGE-GROUNDED, CLIP-FROZEN, CLIP-NOMORPH, NEVER-ANIMATE-WRITING |
| 2L Living-page | `/livingpage` | `run_piece.py` + `cli_livingpage.py` + `build_livingpage_16x9.py` + `stills_gate.py` + `render_lint/` + `pipeline/flow_check.py` | `piece.json` → stills+clips (+`.src.sha`) → `spec_preview.mp4` → `<piece>_scored.mp4` | LP-* registry (§4) |
| 3 Assembly | `/assemble` | `pipeline/assembly_engine.py` + `assembly_ffmpeg.py` | `viral_cut.mp4` + `index.html` | AS-G1–G9 |
| 3b SFX | `/sfx` | `sfx_pilots/sfxlib.py` | `viral_cut_sfx.mp4` | reuse-from-library, sidechain-duck (INV-18) |
| 4 Caption | `/caption` | `veed_io/caption.py` | `<clip>_captioned.mp4` | offline $0 ivory recipe (INV-16) |
| 5 Upload | `/upload` | `pipeline/upload_gates.py` | `upload/upload_kit.{json,md}` | UK-G1–G7 |
| 6 Publish/Release | `/publish` + `release_check.py` | `pipeline/publish_check.py` + `pipeline/release_state.py` | `publish/` pack + `data/release_ledger.json` | UK-G1–G7 + SYNC-G1–G8 |
| x Review | `/review` | `independent_review.py` | `_independent_review/<stamp>/` | 5-CLI panel before any LOCK (INV-9) |
| x Validate | `/validate` | `pipeline/validators.py` + `test_*.py` + `test_bible_kb*.py` | green suite | rules_integrity + 114 tests + 31 Bible-Check tests (adds coherence/dedup/still-review/clip-reuse + BC-G1/BC-G2/chokepoint hash-binding suites; CLIP-NOWRITING live; anchor-verse-unquoted + IMG-COHERENT fixtures still targets) |
| x Cost | `/cost` | `pipeline/cost.py` | `data/spend_ledger.jsonl` | pre-flight estimate + ask-before-spend (INV-20) |
| x Learn | `/learn` | `pipeline/learning.py` | `data/learning/` | defect ledger → propose-I-approve |

---

## 4. Gate registry (the teeth)

Every gate is **deterministic** (a Python validator, fail-closed) or **panel**
(a named LLM agent; LOCKED only when 0 gates FAIL). `D`=deterministic,
`P`=panel, `A`=advisory (never FAILs).

> Gates tagged **(Phase-1)** are v2 TARGETS not yet enforcing in code — building
> them is Phase 1 of the v2 plan. Everything untagged is live in v1 today.
> Gates tagged **(rollout-gated)** are wired in code but RUN report-only behind an env flag
> (default OFF); they raise once the flag is flipped after the shipped catalogue is backfilled.
> The header promise ("every non-negotiable has a fail-closed validator") holds for untagged
> gates; rollout-gated ones are honest about not blocking yet.

### TEXT — `pipeline/engine.py` (+ `kjv_strict.py`, `cluster_gate.py`, `doctrine_gate.py`)
| Gate | Type | Checks |
|---|---|---|
| G1 Biblical Accuracy | D+P | KJV verbatim (punctuation-strict override) + claim sound in context |
| G2 Relevance | P | hook names a real present ache |
| G3 Conviction | P | holy tension, grace-anchored (no gain/loss/fear/shame) |
| G4 CTA lands with Jesus | P | grace-gift not self-help; no grace-trap; does NEW work |
| G5 Structure | D | five beats in order, in budget, ~450–550 words, proof carries KJV |
| G6 Craft | P | standalone, plain prose, clean pacing |
| G7 Freshness | P | non-obvious TRUE detail; thread carried; exegetically honest |
| G8 The Five Questions (BINDING) | P | one idea / shown-not-explained / pierces + aimed at YOU / for a named audience / changes view of Christ / first-hearing test |
| KJV-strict | D | exact-verbatim span match (`test_kjv_strict.py`) |
| Cluster | D | no templated repetition across sibling artifacts (`test_cluster_gate.py`) |
| Doctrine | D | landmine scan: broken-bones, died-of-thirst, inability-concession, universalism, trinity-severed, works/fear/gain-loss (`test_doctrine_gate.py`) |
| Quote-count (Rule-8) | D | shorts carry ≤2 substantial KJV quotes (`lock.py::_rule8_findings`, live) |
| **Narrative-presence** | D | refuse the lock if a known-absent Bible character is asserted as an eyewitness (`validators.narrative_presence` + `data/narrative_facts.json`, fail-closed, zero false-positive; panel backstops unlisted cases). Defect class `invented-narrative-detail` (INV-4), promoted 2026-06-16 |
| **Anchor-verse-unquoted** (Phase-1) | D | currently an advisory stub (`lock.py::_anchor_findings` returns `[]`); to ENFORCE: a named proof-verse must be quoted verbatim |

### SCENE PLAN — `pipeline/visual_engine.py`
| Gate | Type | Checks |
|---|---|---|
| SP-G1 Biblical Accuracy | P | every literal scene defensible vs pericope |
| SP-G2 Narration Alignment | D | every beat has ≥1 supporting scene |
| SP-G3 Visual Variety | P | not repetitive; cliché blocklist |
| SP-G4 Theological Honesty | P | symbolic scenes smuggle no foreign doctrine |
| SP-G5 Prompt Conformance | D | no banned tokens in subject/mood blocks |
| SP-G6 Type Discipline | D | unified scenes carry 3–5 named vignettes, never panels/arches/windows |
| SP-G7 Character Consistency | P | Jesus/disciples identical; jesus_variant consistent |
| SP-G8 Composition Distribution | D | ≥3 framings; none >50% of scenes |
| SP-G9 Scene Mix & Gospel Frame | D | ≥1 unified + ≥1 Jesus/NT-link; ≥2 single; never 100% single |

### BIBLE-CHECK — `pipeline/bible_kb.py` (+ `bib_validate.py`, `bible_gate.py`, `scripture.py`)
Scripture-cited fact cards (location/time/place/customs/characters) that DRIVE the still
prompt (`enrich_for_scene`) and CHECK the image. Buckets: **specified** (Bible states it →
fail-closed) · **constrained** (must not contradict) · **free** (licence, not checked).
| Gate | Type | Checks |
|---|---|---|
| BC-G1 Citation integrity | D | every `specified` fact resolves to verbatim KJV (fetched, not generated); an unverifiable `specified` fact auto-downgrades — can't gate a pass on a guess |
| BC-G2 Over-reach | D ($0) | a `specified` claim naming a COLOUR/NUMBER/MATERIAL absent from its cited KJV is flagged (negation-aware) — catches the "white linen" class with no LLM. `test_bible_kb_regression.py` |
| BC-G3 Facts panel | P | 5-CLI adversarial review of the clean `fact_sheet.md` (`independent_review.py --type biblical-facts`); convergent flags verified vs KJV; verdict oscillates → binding bar = no doctrinal/citation error, not unanimous PASS |
| BC-G4 Image-vs-facts | P-Vision (fail-closed) | each still honours its specified (MUST match) + constrained (must not contradict) facts; image silent on a fact = NOT a violation. Writes a **hash-bound** `.bib_audit.json` (image sha + facts sha) — anti-stale/anti-tamper. Calibrated vs blind labels (`bible_calibrate.py`, INV-23) |
| Chokepoint | D | `bible_kb.gate(v1, stage)` — GREEN only if facts current (scene_plan sha unchanged) + every rendered still covered + passed, hash-current `.bib_audit.json` + 0 unverified `specified` + over_reach clean. Fail-closed before animate; going-forward (grandfather/`BIBLE_GATE` off/strict/warn). Writes `bible_check.status.json` |

### STILLS (Vision audit) — `pipeline/visual_render.py::verify_image`
| Rule | Type | Checks |
|---|---|---|
| IMG-SUBJECT | P-Vision | central subject identity matches spec |
| IMG-ELEMENTS | P-Vision | required visible elements present |
| IMG-ANATOMY | P-Vision | sound hands/faces/limbs |
| IMG-NOTEXT | P-Vision | no legible/garbled text, titulus, banned tokens |
| IMG-PERIOD | P-Vision | period-authentic Baroque, no modern look |
| IMG-TONE | P-Vision | reverent; no horror, no NSFW |
| IMG-COHERENT (rollout-gated) | P-Vision + D | blind default-PASS "fit for use" look — FAIL only on a CLEAR F1 modern/anachronism · F2 frame/border/split-screen · F3 broken face/grotesque expression · F4 impossible anatomy (floating head/limb, through-object, giant head) · F5 dominant garbled text. Fail-closed `*.coherence.json` sidecar (`audited∧passed∧hash`), k-vote hash-pooled `aggregate` for determinism. Validator: `coherence_gate.py` + `coherence.py`; chokepoint `lock.py::require_visual_coherence` (scoped to the selected cut), before `assembly_runner` loads clips, behind `JITB_REQUIRE_COHERENCE` (default OFF). Calibrated to precision 0.50 (INV-23). |
| STILL-REVIEW (rollout-gated) | Human | a human sign-off (`still_review.py`, `.stills_reviewed` token bound to the still-set hash) — authority on the SUBTLE defects the F1-F5 look misses by design; busts on any still add/change. Chokepoint `lock`-style in `assembly_runner`, behind `JITB_REQUIRE_STILL_REVIEW` (default OFF). The 4th human gate. |

> **Render guardrails T1–T6** (`data/render_guardrails.md`, baked into the constitution's VISUAL ARC):
> the subject_block rules that PREVENT the F1–F5 defects up front (no text-as-subject, one full-bleed
> scene, eyes level/downcast, iron-not-gem, ≤3 sharp crowd faces, strictly period). Prevention; the
> gate is the backstop.

### CLIP (animation) — `pipeline/validators.py` + clip QC
| Rule | Type | Checks |
|---|---|---|
| CLIP-VIRAL | D | ≥6 crop-cut beats with framing variety, not a 1–2 beat slow zoom |
| CLIP-IMAGE-GROUNDED | D | cut-plan has no rich-text injection + carries the anti-invention clause |
| CLIP-FROZEN | P-Vision | only the camera moves; nothing in the painting moves |
| CLIP-NOMORPH | P-Vision | faces/hands/forms stable frame-to-frame |
| **NEVER-ANIMATE-WRITING** | D | reject any animated scene whose subject is a scroll/titulus/codex/sign with intended legible text (`validators.never_animate_writing` + rule CLIP-NOWRITING, live) (INV-17) |

### ASSEMBLY — `pipeline/assembly_engine.py`
| Gate | Type | Checks |
|---|---|---|
| AS-G1 Timeline Coverage | D | slots tile [0, total] contiguously |
| AS-G2 No Reuse | D | each body clip once; hero close-only |
| AS-G3 Speed/Trim Health | D/A | avg ≤2.0×; advisory on spikes |
| AS-G4 Min Slot | D | each body slot ≥ 0.3s |
| AS-G5 Section Coverage | D | every spoken section has a clip |
| AS-G6 Hero Close | D | hero = gospel-pivot, bookends, single appearance |
| AS-G7 Gospel Frame | D | cut lands on Christ; reverence speed cap on sacred |
| AS-G8 Beat Continuity | P | thread carried open→climax→close, clips under right words |
| AS-G9 Beat Density | A | flags slow cuts; never FAILs |

### UPLOAD — `pipeline/upload_gates.py`
| Gate | Type | Checks |
|---|---|---|
| UK-G1 Length | D | every field within each platform's ceiling |
| UK-G2 KJV-strict | D | anchor verse verbatim if quoted |
| UK-G3 Doctrine | D | no clickbait/overclaim tokens |
| UK-G4 Brand | D | CTA-to-Jesus + footer present |
| UK-G5 Platform | D | hashtag counts + no malformed tags/links |
| UK-G6 No-Repeat | D | titles don't collide across platforms/siblings |
| UK-G7 Lint | D | plain-ASCII anti-slop + grace-anchored + anchor ref front-loaded |

The publish-pack GREEN gate (`pipeline/publish_check.py`, Stage 6) re-parses the
ON-DISK pack into an UploadKit and re-runs UK-G1..G7 (one rulebook) + placeholder
scan + captions.srt validity + CHAPTERS 0:00-ascending + ToS banlist + dash-slop
scan + `final_sha` freshness (a pack built from a superseded final is RED).

### RELEASE SYNC — `pipeline/release_state.py` + `release_check.py` (LIVE 2026-07-15, see v2/RELEASE_SYNC.md)
One registry (`_website/manifest.yaml` hard-joined via `source:`/`parent:`),
one finality rule (`pipeline/finality.py`, content-sha anchored, `.bak`-proof),
one write path for posted URLs (`upload_tracker.py --set <slug> <platform> <url>`
→ dated `data/release_ledger.json`), one $0 gate, one board (`production_board.py`).

| Gate | Type | Checks |
|---|---|---|
| SYNC-G1 Join | D | catalogue item ⇄ piece folder by explicit `source:` — fuzzy matching is dead; shipped item without a join = FAIL |
| SYNC-G2 Finality | D | `studio_complete`/`live` ⇒ a FINAL under the one rule |
| SYNC-G3 Pack fresh | D | `publish/_source.json.final_sha` == current final's sha |
| SYNC-G4 Thumbs fresh | D | `publish/thumbs/_meta.json.final_sha` == current final's sha (FAIL when live, WARN when studio_complete) |
| SYNC-G5 Site fresh | D | read page exists for promoted items; frame `_meta.source_sha` == scored video (WARN); `publish_meta.read_url` == the real `read/<slug>.html` (FAIL) |
| SYNC-G6 Posted truth | D | `youtube_id` ⇔ `public_status: live` ⇔ dated ledger entry; posted sha == current final |
| SYNC-G7 Long⇄short | D | a short in a cluster that has a long carries `parent:` = that long |
| SYNC-G8 Art style | D | `studio_complete`/`live` ⇒ not detected LEGACY Baroque oil-painting style (`pipeline/art_style.py`; hardened 2026-07-15, memory `graphic-novel-style-migration` — the oil-painting era never ships) |

### LIVING-PAGE lane — `run_piece.py` + `render_lint/` + `stills_gate.py` + `pipeline/flow_check.py` (all LIVE 2026-07-08)
`H` = human gate. Every LP-D gate is wired into the runner itself — a bespoke
script cannot skip them because there are no bespoke scripts left.

| Gate | Type | Checks |
|---|---|---|
| LP-LINT | D/A | rules.json regex + structural `lean-prompt-band` (18–50 words) + `scene-then-camera-closeup` (body-part close-up must name the whole scene); `guard_prompt` auto-positivizes poison tokens before EVERY paid call |
| LP-ARM | D | every rendered PNG gets a pending-FAIL audit sidecar at write time — a still with no verdict cannot go green (the 84-unaudited-stills fix, structural) |
| LP-EARNED | D | `narration_gate` blocks the LOCK on stock closers / unearned landings / template hooks (unmarked-verbatim-KJV counts as the piece's material) |
| LP-STILLS-GATE | H+P | `stills_gate.py` 5-axis rubric + independent adversarial reviewer + hash-bound human `--approve` BEFORE animate/build (HUMAN GATE 2) |
| LP-BC | D | `bib_validate` reads `livingpage_short.spec.json` (one scene per still slug; subject = the render prompt) — BC-G1 citation integrity + BC-G2 over-reach run $0 on batch pieces |
| LP-STILL-PASS | D | `hf_animate` refuses a production still without a PASS sidecar (`JITB_SKIP_STILL_GATE=1` override, discouraged) |
| LP-BUDGET | D | `cost.check_budget` ceiling ($25/short) pre-flights every Kling call; a ledger row per clip AND per still (reuse rows at $0) |
| LP-CLIP-HASH | D | `.src.sha` binds each clip to (still bytes + prompt + duration + aspect); stale → auto-retired to `_stale_from_bad_stills/` + re-rendered |
| LP-FLOWQC | D/A | `flow_check` homography + edge-residual pre-filter: PASS (bulletproof, incl. slow-dissolve anchors) skips the vision NOMORPH call; ESCALATE → vision QC (fail-open) |
| LP-ENGINE-PLAN | A | `choose_engine` value rule (legible-text→static · grid/inset→dyncam · hook/close/sacred/long-hold→kling) + projected-$ vs ceiling |
| LP-RETIME | D | score dip windows carry their spoken phrase + pads; `--stage retime` re-syncs after a re-voice; score warns when alignment is newer than the manifest |

---

## 5. Invariants (binding — do not relitigate without the user)

1. Viral-hook + CTA-to-Jesus 60s shorts — not the non-preachy "Attenborough" model.
2. Gospel Five-Beat structure, timed (Hook→Point→Proof→Conviction→Landing).
3. Grace-anchored conviction — no gain/loss / fear / manufactured pressure.
4. Freshness = faithful depth — surprising about the *text*, never the *truth*.
5. One thread spine hook→middle→CTA; reshape lines, never swap threads.
6. KJV verbatim in script; attribution frames stay narrator voice.
7. Multi-voice when the scene has speakers (parables: Jesus tells, characters speak).
8. Independent red-team is standard at every stage; LOCKED only on 0 FAIL gates.
9. External 5-CLI panel review is enforced before any LOCK (cursor + claude/gemini/codex/grok, no metered API).
10. Binding visual scene mix (SP-G9); never 100% single; unified scenes carry 3–5 vignettes (SP-G6).
11. Assembly hero = gospel-pivot; every cut closes on Christ (AS-G6/G7); reverence speed cap on sacred clips.
12. Kling-friendly state-only language — frozen tableau, camera-only motion.
13. Animation split: shorts = direct-Kling (HF Kling pro); long-form = veo3_1_lite/hybrid. Veo3 gates and prompt discipline defined in `v2/LONGFORM_SPEC.md` §4 (LF-CLIP-*).
14. Shorts are first-class — highest QC, native 9:16, never a cropped long still.
15. Reuse downstream pipelines (narration_pipeline, per_turn_synth, image_to_kling) — subprocess, never duplicate.
16. Caption is the final step on every finished clip (offline $0, ivory).
17. **Never animate writing** — scroll/titulus/codex/sign render garbled under generative animation; design text as illegible marks, hold as a still, or give it only a deterministic ffmpeg push-in/Ken-Burns (never Kling) (from `feedback-never-animate-writing`).
18. **Ambient/SFX bed by default** on every finished clip ($0 from `sound_library`, ear-gated) (from `feedback-ambient-sfx-default`).
19. **Library reuse is topical-fit-gated AND clean-gated** — only thread-neutral plates cross episodes; story-specific stills never do; AND a clip is reusable only if its still is coherence-verified (INV-23) and clip-qc'd. The reuse DECISION goes through `clip_reuse.py` (`decide`/`reuse_plan`), a gated layer over `clip_library.py` — call it, not `clip_library.find`, for reuse decisions (from `feedback-topical-fit-gate`, `feedback-gate-calibration-human-authority`).
20. **Ask before spending** — quote estimated metered spend and get explicit OK before any batch (from `ask-before-spending`).
21. **Period-authentic + reverent image audit** — FAIL modern faces/dress, horror, NSFW (from `feedback-period-reverent-image-audit`).
22. **Dyslexia UX** — review by ear, print full absolute paths, build an index/gallery for every batch (from `feedback-audio-first-review`, `feedback-show-full-paths`, `feedback-index-file-and-full-link`).
23. **Still coherence (IMG-COHERENT) + human authority on the subtle** *(rollout-gated — reports-only until `JITB_REQUIRE_COHERENCE=1`/`JITB_REQUIRE_STILL_REVIEW=1` after the catalogue is backfilled)* — a still is fit for use unless it has a CLEAR F1–F5 defect (blind default-PASS gate, fail-closed `*.coherence.json` sidecar = `audited∧passed∧hash`, k-vote hash-pooled so byte-identical stills can never disagree). The automated gate catches the OBVIOUS at scale; a human still-review sign-off is authority on the SUBTLE. Calibrate against blind human labels before trusting the fail-rate (from `feedback-gate-calibration-human-authority`).
24. **No fabricated verdicts** — no copy/reuse/servicer path may invent a passing audit/coherence/clip-qc verdict; it copies a REAL sidecar from the source or marks UNVERIFIED. (Closed in `clip_library.materialize`, `v2/pilot/_build_zech_reuse.py`, `v2/servicers/assembly_servicer.py`.)
25. **Biblically driven + checked stills (Bible-Check)** *(going-forward — `BIBLE_GATE` grandfathers pieces with no `_bible_check/`; flip `strict` to enforce the back-catalogue)* — every still is driven by Scripture-cited FACT CARDS (specified/constrained/free; KJV fetched verbatim, never generated) and CHECKED both ways: the FACTS by the 5-CLI panel (BC-G3, no doctrinal/citation error) and the IMAGE by a fail-closed Vision audit (BC-G4) bound by content hash to the PNG + facts. No still that contradicts a `specified`/`constrained` fact gets animated or shipped (`bible_kb.gate`, fail-closed before animate). The deterministic teeth (BC-G1 citation integrity, BC-G2 over-reach) are $0 and in `/validate`; the image gate is calibrated vs blind labels before its fail-rate is trusted (INV-23). Scripture is binding; historical notes are secondary and never override it (from `bible-kb-accuracy-pipeline`, `bible-kb-panel-calibration`; design in `v2/BIBLE_GATE_DESIGN.md`).
26. **Landing hold, ≥3.0s, on every finished cut — short or long-form** — after the last spoken word, video AND audio both keep running for a minimum 3.0s hold (last-frame clone + score/ambience ring-out) before the file ends; the audio track's duration must match the video track's (no silent early cutoff under a `-shortest` mux). Deterministic $0 gate: `check_landing_hold.py` (config check on `piece.json`'s `score.outro_hold`/`score.tpad` and the long-form `outro_s` recipes, plus an actual video/audio-duration-parity ffprobe check on any finished mp4) — WARNs, does not block, on already-shipped pieces below the standard (none retrofitted as of 2026-07-19; new pieces should ship at ≥3.0s). Found and fixed 2026-07-19: `run_piece.py`'s shared `score_cmd()` was missing the `apad` step the older per-piece `_score.py` scripts and both long-form score scripts already had, so its narration audio silently ended ~1.5s before the padded video — the piece PLAYED like it cut out early even though the intended hold was there in the video. (from `landing-hold-standard`.)
27. **AWAKEDEN watermark on every shipped final** (locked 2026-07-21) — every finished, postable video carries the site-exact wordmark (AWAK bone + EDEN red-bright, the retired split-E never returns; asset `_brand/awakeden_watermark_overlay.png`, regenerated by `pipeline/thumbnails.py` `brand_assets`). Positions are user-locked from side-by-side samples: 9:16 shorts **top-LEFT** (200px wide on a 1080 page at x=40, y=70 — top-right is where TikTok/Shorts draw their own UI icons; user picked left over center by eye), 16:9 long films **top-RIGHT** (260px wide on 1920 at 28px margins). Tool: `add_watermark.py` — idempotent (skips when `<stem>.prewm.bak.mp4` exists), fail-closed (new encode discarded on >0.05s duration drift), and the untouched original is always archived beside the final as `<stem>.prewm.bak.mp4` (`.bak.` names are invisible to the finality rule). Burn-in is the LAST finishing step, after score/sfx, before posting; downstream sha-keyed artifacts (thumbs, packs, read pages) re-key after it. All 22 shipped finals were brought to the standard 2026-07-21.

---

## 6. Reuse manifest (v2 calls these; it does NOT rewrite them)

| Subsystem | Entry point | Verdict |
|---|---|---|
| Audio | `PythonProject1/jesus/narration_pipeline.py` + `PythonProject1/jesus/narration/per_turn_synth.py` | REUSE-AS-IS |
| Scripture | `pipeline/scripture.py` (+ `data/kjv_cache.json`) | REUSE-AS-IS |
| Captions | `veed_io/{caption,aligner,serif_captions}.py` | REUSE-AS-IS |
| 5-CLI panel | `independent_review.py`, `panel_doctor.py` | REUSE-AS-IS |
| Media libraries | `_library/`, `image_library/`, `music_library/`, `sound_library/` + `cli_library.py` | REUSE-AS-IS |
| **Clip library** (NEW 2026-06-16) | `clip_library/` (`index.json` ~125 clips by reference, post-coherence prune) + `clip_library.py` (`find`/`materialize`, the index/materialize layer) + `ingest_clips.py` | the bank |
| **Reuse decision** (NEW 2026-06-17) | `clip_reuse.py` (`decide`/`decide_for_scene`/`reuse_plan`/`reuse_health`) over the library | the GATED reuse-first per INV-19 + INV-23 (coherence-verified ∧ clip-qc'd ∧ topical-fit ∧ no-repeat); `/scene-plan` step 0 auto-writes `visual/reuse_plan.json`. Reality: only ~34/125 indexed clips are clean-reusable post-gate |
| **Dedup / canonical** (NEW 2026-06-17) | `dedup.py` (perceptual dHash clusters) → `v2/coherence_audit/canonical_concepts.json` | one canonical coherence-verified still per repeated concept (rebuild once, reuse everywhere); never advertises a failed still |
| SFX beds | `sfx_pilots/sfxlib.py` (+ `build_ps22_0N.py` pattern) | REUSE-AS-IS |
| Spend ledger | `pipeline/cost.py` (+ `data/spend_ledger.jsonl`) | REUSE-AS-IS |
| Agent bridge | `pipeline/agent_bridge.py` (+ `.agent_bridge/`) | REUSE-AS-IS |
| CLI orchestration | `cli_pipeline.py`, `pipeline/orchestrator.py` | **WRAP** (v2 `cli_v2.py` shim + state machine reused) |

---

## 7. Cost model + ceilings

General metered estimate ~$23/episode (±30%): Kling ~$11 (48%) · images ~$5 (22%)
· Opus planning ~$5–6 · audio ~$0.50 · Vision audits small. **In agent-mode the
LLM lines drop to $0**, so a Psalm-22 short budgets to ~$17–18 (ceiling $25).

- **Provider split (locked):** NBP $0.50 (Christ/face), HF `nano_banana_2` $0.30
  (neutral plate), direct-Kling $0.65 (animation). Agent-mode LLM = $0.
- **Living-page lane (inked batch shorts):** BytePlus `seedream-4-5` ~$0.05/still ·
  HF `kling3_0 --mode pro --sound off` **7.5cr ≈ $1.13/clip BILLED** (verified against
  43 real transactions joined to job records, 2026-07-21; the `hf generate cost`
  estimator overquotes pro+sound-off as 8.75cr — transactions are the actuals source,
  the old ~$0.65 figure was the direct-Kling price) · everything else $0 ffmpeg/PIL.
  A finished piece runs ~$3–6. The $25/short ceiling is ENFORCED IN CODE at the Kling
  chokepoint (`cost.check_budget`, 2026-07-08), not advisory.
- **HF Kling pricing facts (verified 2026-07-21, style-independent):** the `sound`
  param defaults ON and is a real surcharge (pro quotes 12.5 ON → 8.75 OFF; std 10 →
  7.5) — every call site passes sound-off, keep it that way. `kling3_0_turbo` is NOT
  cheaper at equal output (1080p turbo quotes 10 > pro-off). `kling2_6` (5cr, boolean
  `--sound false`, no `--mode`) is REJECTED as shorts default: invents content on the
  gallery hard-cut (`_bakeoff_kling26/compare.html`, legacy-Baroque substrate) and the
  2026-07-17 inked style POC ranks it below kling3_0 ("inked line art fully survives"
  only on kling3_0). Ledger rows are flag-aware since 2026-07-21: pass `params={...}`
  (the create call's own flags) to `cost.record_hf`; never add a driver-side ledger row
  after `vp.animate()` — providers record internally.
- **Cost levers:** exclude bad images at GATE 2 (never animate them) · reuse
  pre-flight copies an identical sibling PASS still for $0 · `choose_engine`
  policy (static/dyncam/kling by value) · `flow_check` PASS skips a vision call ·
  Haiku for coarse assembly verify · cached constitution prefix · library reuse.
- **`/cost` runs `hf generate cost` pre-flight and blocks on INV-20** (ask first).

---

## 8. Agent bridge + deterministic servicer contract (toil reduction)

`LLM_PROVIDER=agent` routes all engine LLM/Vision calls through the in-chat agent
via `.agent_bridge/` files (zero metered API).

**v2 servicer (LIVE — Phase 2 built 2026-06-16):** `v2/servicers/assembly_servicer.py`
+ `v2/cli_v2.py` auto-answer every *mechanical* assembly verdict so the human stops
hand-writing them. Proven on a #08 dry-run: 14 requests auto-serviced, **1** left for
the agent (the jigsaw). Pure decision logic in `v2/servicers/bridge_lib.py` (9 unit
tests). Run: `.venv\Scripts\python.exe v2\cli_v2.py assemble "<v1>" <flags>`.

| Bridge request | Auto-answer rule | Status |
|---|---|---|
| `assembly-episode-fit` | `{"offtopic": []}` when clips are scene-native | LIVE |
| self-review / independent | LOCKED iff the request's deterministic pre-checks carry no FAIL (echoed; AS-G9 advisory; a FAIL is left for the human) | LIVE |
| slot-verify | auto-PASS **only after** a passing `clip_qc` sidecar exists for the clip | LIVE (guard enforced) |
| kling-audit | auto-PASS when the cut-plan passed `gate_cutplan` | LIVE (`_gen_servicer.py`) |
| `jigsaw` (plan_edit) | semantic — pin clips by meaning, hero NOT in `beat_assignment` | **agent-only** (never auto) |

**Genuine human gates stay human:** the jigsaw, audio ear-review, image pick/hero, clip QC.

---

## 9. A/B parity protocol (the acceptance test)

For a **fresh topic**, build episode **A on v1** (today's `cli_pipeline.py`) and
episode **B on v2** (the skills + this spec + consolidated guardrails). Then:

1. Run the **5-CLI panel** (`independent_review.py`) on both narrations + plans.
2. Compare: panel verdict, escaped-defect count (`learning.py`), metered cost
   (`spend_ledger.jsonl`), and human-touch count.
3. **v2 must tie-or-beat v1** on the panel, at **≤ cost** and **≤ touches**, with
   **0 FAIL gates** and the **full test suite green**. If v2 loses, fix the
   spec/skills and re-run before any cutover.

Continuous improvement: `/learn` feeds panel misses back into proposed gate
strengthening (propose-I-approve), closing the gap episode-over-episode.

---

## 10. Knowledge-migration index (memory → here)

Hard knowledge became invariants; soft knowledge became per-skill guardrails;
memory files become thin pointers. Representative map (full map in Phase 1):

| Memory | Lands as |
|---|---|
| `feedback-never-animate-writing` | INV-17 + `/animate` + NEVER-ANIMATE-WRITING validator |
| `feedback-ambient-sfx-default` | INV-18 + `/sfx` |
| `feedback-topical-fit-gate` | INV-19 + `/stills` `/library` guardrail |
| `ask-before-spending` | INV-20 + `/cost` |
| `feedback-period-reverent-image-audit` | INV-21 + IMG-PERIOD/IMG-TONE |
| `feedback-audio-first-review`, `feedback-show-full-paths`, `feedback-index-file-and-full-link` | INV-22 |
| `locked-stills-provider-split` | §7 cost table + `/stills` |
| `draft-tournament`, `clarity-over-cleverness`, `landing-not-tired` | `/narrate` + G7/G8 |
| `feedback-no-reuse-beat-match`, `feedback-still-bookend` | AS-G2/G6 + `/assemble` |
| `validation-engine`, `recursive-learning-system` | §4 + `/validate` + `/learn` |

---

## 11. Repo map (v2 additions)

```
v2/
  SPEC.md            this contract
  cli_v2.py          orchestration shim → drives reused engine via the bridge
  servicers/         deterministic per-stage bridge servicers (§8)
  parity/            A/B harness (§9)
.claude/skills/<stage>/SKILL.md   one markdown skill per stage (§3)

(reused, unchanged — see §6)
pipeline/  PythonProject1/jesus/  veed_io/  sfx_pilots/  *_library/  independent_review.py
data/  rules.json  learning/  spend_ledger.jsonl  kjv_*.json  constitution.md  render_guardrails.md (T1-T6)

(coherence/quality system, NEW 2026-06-17 — INV-23/24)
pipeline/  coherence.py  coherence_gate.py  dedup.py  clip_reuse.py  still_review.py  (+ test_*.py)
v2/coherence_audit/   provenance.py · build_reject_list.py · build_review_page.py ·
                      build_calibration_set.py · quarantine.py · *.json + *.html review pages
_rejected_coherence/  quarantined bad stills (reversible, gate fixtures)

(Bible-Check — biblical-accuracy of the stills, NEW 2026-06-29 — INV-25)
pipeline/bible_kb.py   engine: KB load · derive · KJV-hydrate · over_reach_scan · verify_biblical_accuracy ·
                       enrich_for_scene (facts DRIVE prompts) · check_status/gate/assert_green (chokepoint)
bib_validate.py        driver (derive → facts-panel → image-audit → report)   bible_gate.py   fail-closed CLI
bible_calibrate.py     image-audit calibration vs blind labels
bible_kb/   characters/ places/ objects/ customs/ eras/   (cited fact bank, grows from verified output)
            _calibration/labels.json   README.md
test_bible_kb.py  test_bible_kb_regression.py   (31 tests, in /validate)
v2/BIBLE_GATE_DESIGN.md   the 3-layer enforcement + regression design (panel-reviewed)
<v1>/_bible_check/   scene_facts.json (sha-bound) · fact_sheet.md · bible_check.status.json · index.html

(LIVING-PAGE lane engine, NEW 2026-07-08 — replaced the per-piece script quartets)
run_piece.py           manifest runner: stills/animate/score/register + hash-backfill ·
                       enrich-dips/retime · engine-plan · reuse pre-flight (byte-parity-proven vs the quartets)
cli_livingpage.py      resumable position board + --continue ($0 steps auto; paid/human printed)
pipeline/flow_check.py deterministic morph pre-filter (homography + edge residual + slow-dissolve anchors)
narration_gate.py      earned hook/landing — BLOCKING in pipeline/lock.py since 2026-07-08
stills_gate.py  ship_gate.py  render_lint/   (5-axis human gate · shared-still map · lint/autofix/verify sidecars)
<piece>/piece.json     the per-piece manifest (prompts/refs · moves · score+dip phrases · register rows)
<piece>/visual/clips/*.src.sha   clip↔(still+prompt) hash bindings
archive/quartets/      the retired _render_stills/_animate/_score/_register scripts + migration tools
pipeline/test_run_piece.py  test_cli_livingpage.py  test_flow_check.py  test_cost.py  test_render_guard.py
```
