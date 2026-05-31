# STATE.md — progress tracker

**Last updated:** 2026-05-31
**Status (2026-05-31):** REDO PROGRAM underway — re-doing all ~10 distinct narration topics through
an upgraded, panel-reviewed pipeline. Shipped this session: (1) a **PANEL GATE** in the runner
(`_regen_one.py` → text + `panel_request.md`, NO audio → user panels → `_finalize.py` renders audio);
(2) the tournament judge can now **graft ANY beat** + apply `synthesis_notes` (`engine._collect_grafts`);
(3) **RECURSIVE LEARNING — the calibration loop** (`data/learning/` + `pipeline/learning.py` +
`_calibrate.py` + `pipeline/kjv_check.py`): logs what the external panel catches that self-review
misses, PROPOSES fixes (propose-I-approve), 5 fixes applied + verified (deterministic KJV gate +
self-review strengthened on scene-scope/shaming/grace-trap/viewer-turn). kjv_check truncation bug fixed.
Redo done: 27 (Matt 16:15), 28 (Matt 8:26), 31 (John 8:12). Awaiting panel: 29 (John 5:6), 30 (Isaiah 53:5).
Remaining: I AM Door (John 10:9), Well (John 4:14), Prodigal (Luke 15), Psalm 22, Fire (John 21:17 threefold).
See RESUME.md top block. Memories: `recursive-learning-system`, `feedback-landing-not-tired`. Prior status below.

**Last updated:** 2026-05-30
**Status (2026-05-30):** 4 cuts finished + upload-kitted in the Drive tracker (QJA #02/#03/#04
+ prodigal). MOTION-OPEN / Christ-still-close is now the DEFAULT (ASSEMBLY_OPEN_MODE=hook; supersedes
the both-ends still) — all 4 cuts re-rendered 2026-05-30 + eyeballed: #02 storm→Christ,
#03 Bethesda man→Christ, #12 swine→cross (3 engine cuts via deterministic re-allocate, no LLM);
#16 rebuilt by hand (animated risen-Christ-at-fire open + frozen-Christ close — note #16 still
opens ON Christ, not a non-Christ hook; a true hook-open needs the queued threefold re-sequence).
Originals kept as .pre-motion-open / .still-both-ends.bak. Earlier still-bookend was baked in + applied to all
finished cuts. Production+posting TRACKER created on Google Drive (`…/0 Christianity/PRODUCTION
& POSTING TRACKER.md`) with per-clip upload kits + cross-series overlap map. RED-TEAM of the
whole plan done: FIXED the image audit to check anatomy (hands/fingers — the hero finger had
slipped); kit conventions captured (no clickbait, no shaming, per-platform hashtags). USER
DECISIONS for tomorrow: (1) switch bookend to MOTION-OPEN / STILL-CLOSE; (2) add a default
female voice to VOICE_MAP; (3) threefold assembler QUEUED (before Last Week). Focus (QJA 05-10
vs pilot I AM vs post-first) STILL OPEN. See RESUME.md "TOMORROW — START HERE". Prior status below.

**Status (2026-05-29 latest, superseded):**
**Status (2026-05-29 latest):** QJA #03 "Do You Want to Be Made Well" (John 5:6)
produced text+audio in AGENT-MODE, **zero metered API**. KEEPER folder
`narration/18 He Never Said Yes/v1` (first take #17 rerolled + deleted — user found
hook too soft + middle too sermonic; rerolled with a punchier director's-note brief).
Thread "He never said yes" (the man's non-answer, v7), 3-voice, 59.03s, atempo 1.1635.
Both reviews LOCKED. Audio stage is now bridged too (narration_pipeline verify/tag/
audit). At GATE 1 — visuals next. Prior agent-mode build status below.

**Status (2026-05-29 late):** AGENT-MODE shipped — `LLM_PROVIDER=agent|api`
(default `agent`). Every engine LLM call (text + both Vision audits) plus the
downstream `image_to_kling.py` cut-planner (Stage A + A.5) now route to the in-chat
agent via a file bridge (`pipeline/agent_bridge.py`, stdlib-only, shared across both
projects) instead of the metered API — zero API spend. The engine writes a request
file and blocks; the agent writes the reply; it continues. Validated end-to-end:
text (PONG) + a real `image_to_kling --plan-only` run (8-beat cut plan authored from
the Peter-fire PNG, audit passed, `.kling.json` written). Run CLIs with
run_in_background and service `.agent_bridge/requests/` → `responses/<id>.txt`; set
`LLM_PROVIDER=api` for unattended runs. See `AGENT_BRIDGE.md` + memory
`agent-mode-bridge`. Prior status below.

**Status (2026-05-29 end):** First real end-to-end episode SHIPPED — QJA #04 "Do You
Love Me" (`16 The Fire Jesus Built/v1`): tournament narration (3-voice, the user's 4
required elements) → cut-aware images (16, #14/#16 fixed) → 12 Kling clips → final
59.02s `assembly/viral_cut.mp4` that opens+closes on the risen Christ. The whole
assembly was done in AGENT-MODE (I hand-authored cut-plans + the jigsaw; Kling+ffmpeg
only; zero assembly API) — the user's cost direction (use the Max sub / in-chat, API
as fallback; formalizing as `LLM_PROVIDER=agent|api` is queued). API-cap note: both
projects share one Anthropic key (942c2bf7); it threw a usage cap then recovered same
session — check the console limit before big runs; engine now degrades gracefully.
See RESUME.md top block for the full pickup. Earlier this session also:
Assembly stage + orchestrator + red-team hardening + HF bake-off + **Part 2 cut-aware
planning** + the **draft tournament** (fix for "feels over-used") — all done. Visual planner is now
timeline-aware: nominates a gospel-pivot HERO (the cross) that bookends the cut +
dedicated ~2s INSERT shots for tiny beats + design-for-the-cut rules (in the
constitution). Validated on a temp re-plan (hero=cross #12, 2 inserts, LOCKED).
Video provider = direct-Kling (HF parked after bake-off: worse motion even with the
rich prompt, blocks the cross, not cheaper). Earlier history below.

**Status:** Visual stage built end-to-end (V1-V8). Prodigal v1 now has a
locked 16-scene plan, 16 rendered HF PNGs (all passed widened content audit),
and **all 16 Kling MP4s on disk** — the overnight job had stalled at 12/16;
the missing 4 (scenes 11-14, the unified multi-vignette block) were re-rendered
this session via `--skip-audit` and verified as real animations (first-vs-last
frame motion confirmed; scene 13 has a strong camera push-in). Text + audio
stage from earlier still all working — the 16-image visual pass sits on top of
run #12's 59.01s three-voice MP3.

---

## Quick status

### Text + audio
| Area | State |
|---|---|
| Text engine (generate / review / revise) | ✅ thread-aware, multi-voice nudge |
| KJV verbatim + wider pericope ±8 | ✅ `fetch_kjv_passage` |
| Thread discovery (4 levers) | ✅ working |
| Self-review (6 agents + 7 gates G1..G7) | ✅ with Jaded Scroller + G7 Freshness |
| Independent red-team audit | ✅ always on, authoritative |
| Multi-voice delivery | ✅ parables = Jesus tells the story; inner character voices nested |
| Audio auto-run (59s Shorts synth) | ✅ working |

### Visual
| Area | State |
|---|---|
| `pipeline/visual_models.py` (Scene + ScenePlan + audits) | ✅ |
| `pipeline/visual_engine.py` (discover_scenes + review + revise + paper_cohesion + enrich_unified_scenes) | ✅ |
| `pipeline/visual_render.py` (ImageProvider ABC + NBPProvider + HFProvider + verify_image + render_scene) | ✅ |
| `pipeline/visual_handoff.py` (paper artifacts + index.html + Kling subprocess) | ✅ |
| `pipeline/visual_runner.py` (orchestration + idempotence) | ✅ |
| `cli_visual.py` (Phase A/B/C flags) | ✅ |
| Constitution VISUAL ARC section | ✅ multi-vignette discipline + cliché blocklist + Kling-friendly section |
| 9 visual gates SP-G1..SP-G9 | ✅ (G2/G5/G6-vignettes/G8/G9 deterministic) |
| 6 panel agents | ✅ Scene Director / Theologian / Visual Skeptic / Character-Consistency Checker / Editor / Jaded Viewer |
| HF (Higgsfield) provider via CLI | ✅ default model `nano_banana_2` |
| NBP (Gemini) provider via google.genai | ✅ ref PNG anchor for Jesus variants |
| Per-image Claude Vision content audit | ✅ now checks subject_block + vignettes + visible_elements (widened in V5.8 after scene 11 silent miss) |
| Cut-hint sidecar (macro_elements + pacing + viral_role) | ✅ `<stem>.cut_hint.json` per PNG |
| Kling subprocess (image_to_kling.py + `--kling-skip-audit`) | ✅ wired |
| index.html review page (#NN refs + cards) | ✅ auto-written after every Phase B |
| Idempotence (skip on existing artifact + audit) | ✅ at PNG level and at scene-plan level |

## Completed work (visual stage, this session)

**V1-V3 — paper plan:**
- `Scene`, `ScenePlan`, `ScenePlanReview`, `ImageAudit`, `CohesionAudit`
  dataclasses with `from_json` parsers.
- `discover_scenes` proposes 18-25 candidates across the visual arc, picks
  14-20 final scenes (cap raised from 12 → 24 in V5.6).
- 6-agent panel (Scene Director, Theologian, Visual Skeptic,
  Character-Consistency Checker, Editor, Jaded Viewer). Theologian +
  Jaded Viewer paired so freshness stays exegetically honest.
- 9 gates SP-G1..SP-G9. Deterministic gates run in Python BEFORE the LLM
  panel and override the LLM verdict on those gates after merge:
  - SP-G2 Narration Alignment (beat_coverage covers every beat)
  - SP-G5 Prompt Conformance (banned-token regex on subject_block + mood_block)
  - SP-G6 Type Discipline (V5.7: unified scenes must have 3-5 named vignettes)
  - SP-G8 Composition Distribution (≥3 framings, no framing >50%)
  - SP-G9 Scene Mix & Gospel Frame (V5.5/V5.6: tiered by scene count)
- `paper_cohesion` runs before any image renders; blocking if FAIL.
- `visual_handoff.write_visual_paper_artifacts` produces `scene_plan.json` +
  `_source_prompts.md` + `scene_plan.review.md` + `scene_plan.independent-review.md`
  + `cohesion.paper.json`.

**V4 — Phase A sign-off (HOLD gate)** — user reviewed paper plan before
Phase B spend was authorized.

**V5 — NBP provider + content audit:**
- `NBPProvider` via `google.genai`; attaches `refs/ref_jesus_<variant>.png`
  from `nano_banana_pro_batch_output/jesus_harmony_v1` when scene declares a
  `jesus_variant`.
- `verify_image` Claude Vision audit, retry-with-feedback loop (default N=1).
- 6 short-priority scenes rendered as the first prodigal NBP batch; 5/6
  passed audit on first try (scene 06 audit caught a Rembrandt drift the
  Jaded Viewer had warned about — the audit retry couldn't fix the prior).

**V5.5 — scene mix + Jesus/NT-link enforcement:**
- SP-G9 deterministic gate: rich plans must have ≥1 unified + ≥1
  nt-gospel-link scene + ≥1 ot-echo scene (tiered by total count).
- Saved feedback memory `feedback-visual-mix-and-jesus-frame`.

**V5.6 — lift cap + Kling-friendly metadata:**
- `VISUAL_MAX_SCENES` raised from 12 → 24.
- `Scene` gained `macro_elements` (3-5 cut anchors), `pacing` (controlled /
  slower / faster), `viral_role` (hook-open / build / pivot / climax / close).
- `MAX_TOKENS` bumped to 32K (16K cap was truncating 14+ scene JSON outputs).
- `text_engine._call` switched to streaming for safety.
- Saved feedback memory `feedback-kling-friendly-scene-plans`.

**V5.7 — multi-vignette unified scenes:**
- `Scene.vignettes: list[str]` field (3-5 named noun phrases per unified scene).
- SP-G6 deterministic check folded into existing gate: counts vignettes.
- `enrich_unified_scenes` — one-Opus-call-per-unified-scene surgical rewrite
  preserving foreground subject while expanding to 3-5 named background
  vignettes. Used to backfill the prodigal's 6 unified scenes without
  regenerating the whole plan.

**V5.8 — audit widening + scene 11 crucifixion fix:**
- Per-image audit prompt previously checked only `visible_elements` (a sparse
  field). Silently passed a wrong scene 11 where Jesus stood beside the cross
  instead of crucified on it. **Widened audit:** now checks central-subject
  identity against full `subject_block` + each named vignette in `vignettes`.
- Re-rendered scene 11 with strengthened spec ("body suspended on the cross",
  "arms outstretched and nailed", "iron nails visibly through both hands and
  through the feet"). New audit verified Jesus actually crucified.

**V6 — HF (Higgsfield) provider:**
- `HFProvider` subprocesses `~/bin/hf.exe generate create nano_banana_2
  --prompt "..." --aspect_ratio 9:16 --wait`, scrapes the image URL from
  stdout, downloads via urllib. Default model is the user's rated winner for
  Baroque oil painting (HF-POC/RESUME.md).
- 16 prodigal scenes rendered, 16/16 passed (under both narrow audit and
  later widened audit after the V5.7 unified re-roll).
- HF credits used: ~50 of 463 available.

**V8 — Kling animation handoff:**
- `visual_handoff.run_kling_pipeline` subprocesses
  `PythonProject1/jesus/image_to_kling.py` with `KLING_SKILL_PATH` env
  pointed at `adhoc/SKILL_locked.md`. Forwards `--skip-audit` flag.
- Cut-hint sidecars (`<stem>.cut_hint.json`) write per render — V8 wiring of
  these into the image_to_kling director prompt is **deferred** (image_to_kling
  reads only the image right now; sidecars sit alongside for human inspection
  and future plumbing).
- First full Kling run failed gracefully on 11 of 16 scenes because Stage A.5
  audit went into nit-pick mode (documented hazard in HANDOVER.md). Re-ran
  with `--kling-skip-audit` — all 11 missing MP4s rendering successfully (in
  flight at session end).
- Saved feedback memory `feedback-kling-skip-audit`.

## Validated runs

**Text + audio:**
- `09-11` — prodigal iterations, ending with `11 The Confession He Never Finished`
  (2-voice narrator+jesus, 59.01s, atempo 1.2621×).
- `12 The Kiss That Cut Off the Bargain` — **3-voice** narrator → jesus →
  narrator → son (5 turns), 59.01s, atempo 1.419× (above 1.30 ceiling — see Open #8).

**Visual (on run #12 v1):**
- 16-scene plan, both reviews LOCKED, paper cohesion PASS.
- Hero singles (10): rehearsal / mid-syllable / father-at-window / among-swine
  / father-mid-sprint / kiss-tableau / kiss-macro / crumpled-rehearsal /
  famine-husks / open-doorway.
- Unified multi-vignette (6): Jesus-telling-divided-room (nt-link, ministry) /
  robe-ring-shoes (theological-centre) / elder-brother-threshold (nt-link) /
  cross-as-fathers-cost (nt-link, passion) / hosea-14-echo (ot-echo) /
  deut-30-echo (ot-echo).
- All 16 PNGs rendered via Higgsfield `nano_banana_2`. All 16 passed Claude
  Vision content audit (after the V5.8 audit widening; scene 11 specifically
  was re-rolled to fix a "standing beside cross" miss the narrow audit had
  ignored).
- 16 `.kling.json` cut plans written. **All 16 `.mp4`s now on disk** — the
  overnight job stalled at 12/16; scenes 11-14 re-rendered 2026-05-29 with
  `--skip-audit` (reused existing cut plans, exit 0 each). All 16 verified as
  genuine animations via first/last-frame extraction (scene 07 tear-roll,
  scene 13 camera push-in, others subtle motion). Scene 14 lamp reads as a
  multi-cup pedestal vs. single-flame spec — known audit nit, shipped as-is.

## Open items / issues

### Text + audio (carried from earlier in the day)

1. **Atempo overrun on long verses.** Run #12 hit 1.419× narrator atempo
   (>1.30 ceiling). Fix options: (a) constitution rule to quote only the
   essential clause of long verses, (b) lower `TARGET_WORDS_MAX` to ~145,
   (c) Editor-agent hard rule for multi-voice. DECISION PENDING.
2. **Female voice gap.** `VOICE_MAP` still has no female voice_id. Encounters
   series leans heavily on women (Samaritan, Martha, Mary) — biggest near-term
   text-lever, needs a voice_id from the user.
3. **Charter-shrinks-freshness meta-effect.** Worked examples in the
   constitution are being explicitly rejected by discovery as "predictable
   because cited". Watch over more runs; if persists, move examples to a
   generation-only prompt.
4. **Orphan folder `05 He Said It Under the Lamps`.** Incomplete (no MP3);
   safe to delete (out-of-repo guard prevents auto-delete).

### Visual (new)

5. **Cut-hint sidecar not yet consumed by image_to_kling.py.** Each PNG has
   a `<stem>.cut_hint.json` with macro_elements + pacing + viral_role, but
   `image_to_kling.py` doesn't read it — the Stage A director only sees the
   image. To wire this in, `image_to_kling.py` would need a small patch that
   injects the cut_hint contents into the SKILL_locked.md director's user
   prompt. Defer to a "V10 cut-hint plumbing" task.
6. **Audit nit-pick mode documented but unhandled at the engine layer.**
   `--kling-skip-audit` is the workaround. Worth a smarter solution
   eventually: e.g. if the audit fails 3× on the same positional/wording nit
   (no banned tokens, no missing subject), auto-promote to skip-audit for
   that single scene rather than the whole batch.
7. **Two soft vignettes in scene 11.** The robe-ring vignette upper-right and
   the youthful-face vignette lower-right are weaker than ideal. Acceptable
   as shipped; could re-roll once if the final cut wants them sharper.
8. **`rendered_cohesion` audit never built (V7 still pending).** A
   contact-sheet Claude Vision pass over all 16 PNGs against narration.md
   would catch set-level drift (Jesus face mismatches across scenes 8 and 11,
   palette drift, lighting direction). Cheap (~$0.10). Worth doing before
   the final assembly but not blocking.
9. **Final video assembly (out of current scope).** 16 × 10s Kling clips +
   59.01s MP3 + multi-voice timing → final 60s viral cut. Either via the
   `viral_cuts.py` / `viral_smart.py` tools in PythonProject1, or a new
   assembly step in this engine. Not started.

## NEXT TASK

In order of value:

1. ~~**Verify all 16 MP4s landed.**~~ ✅ DONE 2026-05-29 — re-rendered the 4
   missing (11-14), all 16 confirmed as real animations.
2. ~~**Build the index.html v2**~~ ✅ DONE 2026-05-29 — `write_review_index_html`
   in `pipeline/visual_handoff.py` now renders each scene as an inline
   `<video>` (auto-discovers `<stem>.mp4`, PNG as poster, looping/muted/controls)
   with a green "▶ clip" badge; falls back to `<img>` + "still only" badge when
   no MP4 exists. Regenerated for the prodigal; all 16 cards show clips.
3. ~~**Build a minimal final-assembly step**~~ ✅ DONE 2026-05-29 — built the
   full **Stage 4 assembly pipeline** (`cli_assemble.py` + `pipeline/assembly_*`).
   Intelligent clip↔word jigsaw (LLM) + deterministic slot allocator (speed-first,
   trim-past-cap, 2.2x cap) + 6-agent panel + AS-G1..G7 gates + independent audit
   + per-slot Vision verify + `upstream_notes.md` feedback loop. Produces a 59.01s
   `viral_cut.mp4` (hero kiss bookends start+end for a loop feel; 12 clips, avg
   1.92x) + a 160s `all_takes_reel.mp4`, in `<v1>/assembly/`. Validated end-to-end
   on the prodigal; both reviews LOCKED. See memory `assembly-stage-design`.
   Open follow-ups: (a) budget is soft (landed 12 vs 11); (b) Vision verify gave
   1 true flag (#03 lands on a hand/lamp macro mid-clip) + 1 false positive (#10
   fist misread); (c) consider crossfades vs hard cuts. — concat the 16 × 10s clips
   into a 160s "all takes" reel, AND a 60s viral cut using the
   `short_priority` ordering. This is the missing last leg between
   "everything rendered" and "a deliverable video." Likely a small
   `cli_assemble.py` using the already-present ffmpeg.
4. ~~**Seamless pipeline**~~ ✅ DONE 2026-05-29 (Part 1 of 3) — `cli_pipeline.py`
   + `pipeline/orchestrator.py`: one resumable topic→cut flow with 3 HUMAN gates
   (audio / images / clips). Exclusion is the curation lever (`--exclude` at the
   image gate skips Kling on bad images — cost saver; replans automatically).
   `VISION_AUDIT_MODEL`=Haiku for the coarse verify. Validated on the prodigal
   (gate detection + exclusion→replan→render). Cost model documented (~$23/ep).
   See memory `pipeline-orchestrator`.
   **Queued: Part 2** (cut-aware planning — feed timeline into discover_scenes,
   hero_candidate, ~2s inserts, design-for-cut constitution rules); **Part 3**
   (parallel 2-3 topics + tagged clip-reuse library).
5. ~~**Red-team hardening**~~ ✅ DONE 2026-05-29 — ran a 3-agent independent red
   team over everything built+planned; fixed the real findings: **hero = the
   gospel-pivot (cross), bookends open+close so the cut LANDS on Christ** (was
   ending on the emotional kiss — the biggest flaw); deterministic gospel-frame
   survival gate; **reverence speed cap 1.3x** on sacred clips; doctrinal verify
   now Opus-on-sacred + fail-closed + BLOCKING; de-hardcoded the prodigal-specific
   prompts; generalization fixes (budget enforced, key/index validation, negative
   windows, timeline pinned to narration.mp3, speaker-aware alignment). Validated:
   prodigal now opens+closes on the cross, all reviews LOCKED, sacred clips ≤1.3x.
6. ~~**HF Kling bake-off**~~ ✅ DONE 2026-05-29. Findings: (a) a SIMPLE motion-only
   prompt makes `kling3_0` produce a BLAND single zoom (user rejected it on sight) —
   the RICH 8-beat `.kling.json` cut plan is what gives the internal reframing
   (full→mid→close→return). Fair re-test: HF + the SAME rich prompt **matches
   direct-Kling's dynamism** (crop reframing, no morphing). So the cut-plan brain
   (image_to_kling Stage A) IS needed; feed its prompt to HF. Output 716×1284/24fps. (b) It
   takes an integer `duration` → variable-length generation is real (could kill the
   speed-up hack). (c) **Cost ≈ 6.25 credits / 5s std clip** → ~3 episodes/month on a
   300-credit plan; NOT cheaper than direct-Kling, just prepaid/consolidated. (d)
   **BLOCKER: HF's NSFW filter rejects the crucifixion** (bare torso) — and it's
   platform-wide (Seedance 2.0 rejects it too). So HF cannot animate the cross, which
   is now the mandatory hero/landing.
   ~~DECISION~~ ✅ RESOLVED: **HYBRID** (HF for clothed + direct-Kling fallback for
   NSFW-blocked sacred), and YES build it for the variable-duration win.
6b. ~~**Hybrid video provider**~~ ✅ BUILT 2026-05-29 — `pipeline/video_render.py`:
   VideoProvider ABC + HFVideoProvider (kling3_0, motion-only prompt, integer
   duration, NSFW detection→raise) + KlingDirectProvider (subprocess image_to_kling,
   the cross-capable fallback) + HybridVideoProvider (HF→fallback on NSFW/error).
   `VIDEO_PROVIDER=hybrid` is the default; wired into orchestrator SEG C
   (`animate_scenes`, idempotent; `VIDEO_PROVIDER=kling` reverts to legacy). Validated:
   HF success, NSFW→direct-Kling fallback on the cross, idempotent skip.
   **Provider feeds HF the RICH `.kling.json` cut-plan prompt** (`cut_plan_prompt`,
   reusing/generating image_to_kling Stage A) — NOT a minimal prompt: the bland-zoom
   lesson. Per-clip `duration` plumbed (defaults 10s); variable-duration PAYOFF needs
   Part 2 to pass per-slot targets. Bake-off spend: 300.72→267.97 ≈ 33 credits (5s std
   ≈6.25cr, 10s std ≈12.5cr); a ~13cr gap couldn't be tied to a specific op (delayed/
   moderation posting?) — WATCH credit accounting.
   Remaining red-team opens: decide the clip-DURATION policy in Part 2 (generate at target
   length to kill the speed-up hack) so HF-video is built last, not first; instrument
   real token/credit cost (the $23 model was optimistic; Opus Vision audits scale
   with the deep pool); keep human gates SERIAL per-episode (batch only generation);
   limit Part 3 clip reuse to thread-neutral plates (no Jesus/variant reuse).
7. **Polish the assembly POC**: try `--clips all` to see the strobe, A/B clip counts,
   maybe crossfades; refine verify to sample the establishing frame (not mid-reframe).
8. **Then queued text-stage opens:** female voice (#2), multi-voice
   word budget (#1).

## After each working session

Update this file: bump "Last updated", move completed items up, refresh
Quick status, log new issues, set "NEXT TASK". Then update `RESUME.md`'s
first action.
