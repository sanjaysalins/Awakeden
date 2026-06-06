# RESUME.md — start here next session

## ═══════════ SESSION 2026-06-06 (LATEST) — PLANS + SPEND LEDGER + PSALM 22 CLUSTER (LONG + 8 SHORTS) ═══════════

**Big session. Everything committed (clean tree). Two phases:**

### A) Strategy + tooling (all committed)
- **Production plan + tracker** (`PRODUCTION_TRACKER.html` / `PRODUCTION_PLAN.md`, gen by `_production_tracker.py`)
  — built from `data/series.json` (10 series / 76 eps), red-teamed + 5-CLI-paneled. Funnel + tiering, proof-first
  priority, gated pipeline, honest cost range, distribution, cross-series collisions, backlog buckets.
- **`BATCH_PLAN.md`** · **`ASSET_LIBRARY_PLAN.md`** (plan→spend→reuse→verify, red-team-revised) · **`TODO.md`**
  (master backlog) · **`PRODUCER_ORCHESTRATOR_PLAN.md`** (red-teamed → DON'T build the orchestrator; do
  long-form-generic first — DONE).
- **Long-form drivers now EPISODE-GENERIC** (`longform/_episode.py` + `_render/_animate/_assemble/_make_index`
  read per-episode `scene_plan.json`; Isaiah migrated + regression-verified). `_test_gate.py` (--approved gate).
- **Spend ledger BUILT** — `pipeline/cost.py` + `data/spend_ledger.jsonl`: `hf generate cost` (exact pre-flight) +
  `hf account transactions` (reconcile, credits not USD) + LLM `mode` chokepoint + per-episode ceilings; wired into
  the long-form drivers. CLI: `python -m pipeline.cost {balance|estimate|summary|reconcile}`. Memory `spend-ledger-system`.
- **Caption fix** committed (`veed_io/serif_captions.py` Windows drive-colon → run from .ass dir). **Isaiah 53 captioned:**
  `…/01_Isaiah_53…/v1/visual_16x9/Isaiah53_16x9_captioned.mp4`.

### B) Psalm 22 cluster — LONG-FORM STUDY + 8 SHORTS, ALL LOCKED (narration; $0 except the long's mp3)
`longform/02_Psalm_22_Song_From_The_Cross/v1/`
- **Long-form** `narration.md` LOCKED (3 passes) + **`narration.mp3` 6:58** (narrator 1.2x). Scene plan NOT yet authored.
- **8 SHORTS** in `…/v1/shorts/`, each through ONE red-team + ONE 5-CLI panel (LEAN process, memory
  `narration-review-process`), KJV self-verified, committed: 01 Crucifixion-Foretold(garments 22:18→Jn19:24) ·
  02 Mockers(22:7-8→Mt27:43) · 03 Forsaken-Cry(22:1→Mt27:46) · 04 Declared-to-Brethren(22:22→Heb2:12, resurrection) ·
  05 He-Hath-Done-This(22:31~Jn19:30) · 06 Ends-of-the-Earth(22:27) · 07 Body-Foretold(22:14,17) · 08 I-Thirst(22:15~Jn19:28).
  (🔴 worm v6 left to the long-form — contested tola typology.)
- **LOCKED process & direction (memories):** `accuracy-over-throughput` · `narration-review-process` (1 red-team +
  1 panel → lock) · `psalm22-short-series` · `shorts-longform-funnel` (long FIRST, shorts distilled). KJV self-verify
  caught the cache DROPPING a comma in Ps 22:7 — audit the cache (TODO).

### C) 8 shorts' AUDIO — RENDERED (narrator LSi9zNCeliLuhIGGS0By, --natural, ElevenLabs ≈ $3). mp3s on disk:
`…/02_Psalm_22…/v1/shorts/<NN>/narration.mp3` — durations at NATURAL pace:
01 Crucifixion-Foretold 65.4s · 02 Mockers 67.7s · 03 Forsaken-Cry 60.5s · 04 Declared-to-Brethren 64.3s ·
05 He-Hath-Done-This 55.2s · 06 Ends-of-the-Earth 65.3s · 07 Body-Foretold 68.1s · 08 I-Thirst 71.1s.

▶▶ **DO FIRST NEXT SESSION:** **LISTEN to the 8 short mp3s** (paths above). **DECISION NEEDED:** 6 of 8 run >60s at
natural pace (the classic Shorts target is ~60s; I-Thirst is 71s). Pick ONE: (a) trim a few narrator words per short
(accuracy-locked KJV quotes stay; just tighten prose — re-run the prep + per_turn_synth), or (b) a MILD narrator
speed-up (~1.05–1.15x; note the shorts natural-speed rule prefers trimming over stretching). 05 (55s) + 03 (60.5s)
are already fine. THEN: Psalm 22 stills (long first, reuse audit) OR next long-form (Passover / Bronze Serpent / 7 Words).

## ═══════════ SESSION 2026-06-05 — ISAIAH 53 FILM DONE + CALM SCENES LIVENED ═══════════

**⏸ SESSION PAUSED — everything committed (git `07ec813`, working tree clean). Awaiting user watch/approval.**

**The 16:9 film is finished and rebuilt with livelier motion.** Final cut + gallery (FULL paths):
- FILM: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9\Isaiah53_16x9.mp4` — 1920×1080, **6:45 (405.3s)**, closes on risen Christ.
- GALLERY: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9\index.html`

**What I did this session (picking up the paused animation):**
1. **S6 cross was THE blocker.** veo NSFW-refuses the image itself (nail-wound + blood); the direct-Kling
   fallback is **hardcoded 9:16** (`image_to_kling.py`) = wrong aspect for a 16:9 film, AND it hangs on the
   agent bridge. So I used the sanctioned fallback (c): a gentle **ffmpeg 16:9 slow push-in** from the still
   ($0), which the assembler boomerangs like any static scene. No freeze. (S16, the other robed cross, animated
   fine on veo — only S6's graphic nail-wound trips the filter.)
2. **S13 (chariot) + S14 (Philip)** were missing their forward-chain continuation clips (redone Gaza stills;
   old conts had been backed up). Regenerated via `_animate_directional.py` (veo). All 6 directional chains
   now complete (8,9,11,13,14,20). Re-assembled → 405.3s.
3. **User flagged the calm scenes felt like ken-burns.** ROOT CAUSE (verified by frame-diff): the anti-morph
   veo prompt (`_animate_16x9.py`) forces a FROZEN painting — only camera + atmosphere move — so calm scenes
   read as a slow camera drift. FIX = **NEW `longform/_reanimate_one.py`**: a per-scene `LIVELY` prompt dict
   that animates REAL motion in living elements only (flame, smoke, dust, wind, cloud, light, cloth edges)
   while still guarding faces/hands. Test-first on S2 (flame flickers, smoke rises, dust drifts, hand intact)
   → user approved → rolled out. **10 calm scenes re-animated:** 1,2,3,4,5,7,10,12,16,17. Old clips saved as
   `<stem>.prev.bak.mp4`. (HF had a transient **HTTP 502 outage** mid-run on 12/16/17 — the script now
   RESTORES the backup on failure so a scene is never left blank; retried, all rendered.)
4. **Landing scenes S18/S19/S20/S21 livened too (user asked), then DIALED BACK.** First pass used
   "luminous motes drift upward" → veo bloomed heavy GOLDEN GLITTER/bokeh (user: too much, "2" = dial back).
   LESSON (now memory `feedback-veo-no-glitter-glow`): particle words ("motes/sparkles/dust/shimmer") make veo
   add AI-glitter, and text negatives ("NO glitter") do NOT reliably suppress it on bright glowing backgrounds.
   Fix = strict "keep the painted light EXACTLY as is, steady, only cloth edges stir" + for the worst offenders
   use a **clean ffmpeg push-in** (zero added anything). FINAL landing state:
   - **S18** = clean ffmpeg push-in (veo kept sparkling its warm bg no matter what).
   - **S20** = clean ffmpeg push-in, **19.5s single clip** so the directional branch needs NO conts (its veo
     cont-chain kept re-introducing sparkle + a light-burst over the pierced hand).
   - **S19, S21** = clean veo (strict steady-light prompt held; gentle breathing motion). S21 halo is the
     gentlest motion — if user wants it bone-clean too, swap to ffmpeg push-in.
   - **S6** (cross) still ffmpeg (veo NSFW-refuses it).

**Spend this session ≈ $9** (3 directional conts + 10 calm re-animations + landing iterations, veo3_1_lite via
HF; the ffmpeg push-ins S6/S18/S20 were $0).

**NEW tool:** `longform/_reanimate_one.py` (re-animate ONE scene with a livelier `LIVELY[id]` prompt; backs
up to `.prev.bak.mp4`; restores-on-failure). **NEW memory:** `feedback-index-file-and-full-link` (always give
the user a reviewable index file + the whole absolute path).

▶▶ **DO THIS FIRST ON RETURN:**
1. **Watch the full cut** — S1/S2/S3 opening should feel alive (flame/smoke/wind), and the S18→S21 landing
   should be clean (no glitter). Confirm no scene morphs in motion. Path above.
2. If anything still reads off: re-animate ONE scene via `longform/_reanimate_one.py <id>` (livelier) — but
   for any bright glowing/glory scene PREFER a clean ffmpeg push-in (see S6/S18/S20 commands in git or just
   copy the S18 zoompan one) to avoid veo glitter. After any change re-run
   `.venv\Scripts\python.exe longform\_assemble_16x9.py` then `..\_make_index.py`.
3. If the film is approved → it's DONE (audio already locked, `narration.immersive.mp3` 405.3s). Then: posting
   kit for the long-form, or pick the next long-form topic / next multi-dimension short.

## ═══════════ SESSION 2026-06-05 (LATER) — ISAIAH 53 STILLS RE-DO (hero-still bar) ═══════════

**User raised the bar:** every still must be a HERO still; the OPENING must grip instantly; fix
modern/anachronistic dress + any picture-frames. Locked the user's production LOOP:
NARRATION → MOTION → FIRST FRAME → ELEMENTS (must already be in the still) → animate ONLY
pre-placed elements → QC the WHOLE clip (≥6 frames), not just the last.

**Process: red-team (mine, RT1-10) → external ai-panel (`independent_review.py`, claude/gemini/codex
PASS=none, FAIL/REVISE) → fixed → executed with INDEPENDENT image review every batch.** The panel +
full-res re-audit proved my FIRST audit (contact-sheet based) was the weak link — it missed S7 (gilt
picture-frame triptych), S12 (Christian cross headstones), and that S6/S16 never showed the cross.
**Memory `feedback-audit-stills-fullres`: always QC images full-res, never from a thumbnail.**

**12 stills RE-RENDERED + independently verified** (NBP gemini-3-pro-image, 16:9, ~$11):
S1 epic prophet-on-cliff open · S2 non-legible script · S3 NON-figurative glory (no Christ pre-reveal) ·
S6 intimate robed cross (clean pierced hand) · S7 substitution (weight/freed, not "praying friends") ·
S10 1st-c trial (no Dutch hats) · S11 1st-c column (flat, no banners/canvas-on-wall) · S12 BURIAL act
(not empty/open tomb) · S13/S14/S15 Gaza trio unified · S16 cosmic robed cross. Kept: S4,S5,S8,S9,S17-21.
Originals in `visual_16x9/_redo_backup/`.

**Key learnings baked in (for the remaining episodes + future films):**
- Encode the BEAT not just objects (S3/S7 first passed the frame check but failed the meaning).
- Negative prompts alone fail ("NO triptych" still produced one; "NO canvas" produced a canvas-on-wall)
  → use POSITIVE full-bleed/flat framing.
- Gaza continuity = SINGLE-image reference (render S13, attach its PNG as ref for S14/S15) — NOT text-only,
  NOT multi-role refs. Wired via NEW `NBPProvider.generate(extra_ref_paths=...)` + `_redo_stills.py --ref`.
- Cross stills render fine on NBP; the NSFW block is only on the VIDEO stage (veo) → Kling fallback.

**NEW tools this session:** `longform/_redo_stills.py` (re-render specific scenes, backs up stale
PNG/MP4/cont to `_redo_backup/`, no auto-bank, `--ref` continuity), `longform/_make_index.py`
(self-contained `visual_16x9/index.html` gallery — grid + #NN + redone/kept badges + click-to-zoom
lightbox), `pipeline/visual_render.py` NBP `extra_ref_paths`. Plans: `STILLS_REDO_PLAN.md` +
`STILLS_REDO_PLAN_v2.md` + `_independent_review/` in visual_16x9/.

▶▶ PAUSED MID-ANIMATION (user stepped out 2026-06-05). The animation job was still running in the
background — let it finish; clips persist on disk. **DO THIS FIRST NEXT SESSION:**

1. **Check what animated.** Read the animation log (task `bwznxragf`) /
   re-run `.venv\Scripts\python.exe longform\_animate_16x9.py` (idempotent — it SKIPS scenes that
   already have an .mp4, so it only retries the FAILED ones). Then list `visual_16x9\*.mp4` and find
   any redone scene MISSING a clip.
   Known at pause: S1,S2,S3,S7 animated OK; S4,S5,S8,S9 skipped (kept); **S6 robed cross FAILED** both
   veo (HF NSFW refusal) AND the direct-Kling fallback ("produced no mp4, exit 0"). S10-S16 were still
   running (S16 is the other robed cross — expect the SAME failure).

2. **FIX THE ROBED-CROSS ANIMATION (the blocker)** — S6 + S16. veo NSFW-blocks the cross (known, memory
   `feedback-hf-video-blocks-cross`) AND the Kling fallback in `pipeline/video_render.KlingDirectProvider`
   silently produced no mp4 (exit 0) — DEBUG why (it ran `image_to_kling.py`; check its output/skill path/
   NSFW audit). Options if Kling won't cooperate: (a) animate via `image_to_kling.py` directly with
   `--kling-skip-audit`; (b) since the stills are ROBED (not bare-torso) re-try veo with an even more
   explicitly-clothed/cropped prompt; (c) LAST RESORT — boomerang/ken-burns the still itself (the
   assembler already boomerangs static scenes, so a still with no veo clip could be handled by giving
   it a gentle camera move). **The cross is the gospel pivot — both beats MUST have a clip before assembly.**

3. **Directional chains** S11/S13/S14 — Phase 2 (`_animate_directional.py`) regenerates their `_cont*`
   clips from the NEW base last frames (idempotent; only the redone ones, since S8/S9/S20 conts still exist).
   Confirm it ran after Phase 1.

4. **Re-assemble:** `.venv\Scripts\python.exe longform\_assemble_16x9.py`. NOTE: it `SystemExit`s
   "missing clip" if ANY scene lacks a base .mp4 — so S6/S16 must have a clip first (step 2). Audio is
   LOCKED (`narration.immersive.mp3`, 405.3s); boomerang for static + forward-chain for directional.

5. **QC + show:** spot-check the redone scenes in motion (sample frames across each window), regenerate
   the gallery (`.venv\Scripts\python.exe longform\_make_index.py`), then show the user the final film:
   `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9\Isaiah53_16x9.mp4`

STILLS ARE DONE + independently verified (12 redone, ~$11). Animation spend in progress (~$11 budgeted).
Backups: `visual_16x9\_redo_backup\` (all originals), `Isaiah53_16x9.frozen.bak.mp4` (pre-redo film).
Minor cosmetic: faint faux-signature squiggle in a corner of S12 (invisible in motion; ignore).

## ═══════════ SESSION 2026-06-05 — ISAIAH 53 FILM: FREEZE REMOVED + NARRATOR 1.20x + DIRECTIONAL CHAINS ═══════════

**User feedback acted on (final state):**
1. **"I don't like the freeze."** → no more frozen ken-burns. TWO fill modes in
   `longform/_assemble_16x9.py` (old frozen version = `_assemble_16x9.frozen.bak.py`):
   - **camera-only / static scenes (15)** → seamless **BOOMERANG** (forward + reverse, looped).
   - **DIRECTIONAL scenes (6: S08 sheep, S09 lamb, S11 marching column, S13 chariot, S14 Philip,
     S20 reaching hand)** → boomerang looked COMICAL (walking/riding backward), so **FORWARD-only**:
     the original clip + **chained continuation veo clips** (each clip's last frame seeds the next →
     the chariot keeps rolling forward). Driver `longform/_animate_directional.py` (NEW).
     10 continuation clips generated (veo3_1_lite, HF) ≈ **$6**. Test-first validated on S13 (seam
     invisible, style held, motion forward). `DIRECTIONAL = {8,9,11,13,14,20}` set in the assembler.
2. **"Narrator faster, up to 1.20."** → re-synthed at **narrator atempo 1.2001x**; **the_LORD + eunuch
   left natural 1.0**. $0 — reused existing `_turns/*` base renders, only re-applied atempo + re-concat.

**Rebuild chain (re-derived from the 1.0x baseline so cues still land on their words):**
- narration.mp3: 482.9s → **405.3s** (`per_turn_synth --target 405`). God/eunuch unchanged.
- Re-aligned (free whisper, `_pilot_cue_times.py`) → new cue times. `longform/_retime.py` (NEW) holds the
  canonical 1.0x cue times + BEDS/SHOTS + scene windows and warps them to the current target (piecewise-
  linear). To re-time again: change narrator `--target`, re-run `_pilot_cue_times.py`, paste the new column
  into `_retime.py` CTRL, run it (rewrites scene_plan.json + prints BEDS/SHOTS), patch `_soundstage_cinematic.py`.
- Soundstage rebuilt on new anchors → all library sounds reused, $0 → `narration.immersive.mp3` = **405.3s**.
- Re-assembled. **GOTCHA (handled):** concat frame-rounding leaves video ~2s short of audio → mux `tpad`
  clones the last frame (hero settle/hold on Christ) up to audio length, then `-shortest`.

**FINAL FILM:** `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9\Isaiah53_16x9.mp4`
— 1920×1080, **6:45 (405.3s)**, narrator 1.20x, boomerang + forward-chain motion (no freeze, no comical reverse),
immersive soundstage, closes on risen Christ. Backups: `Isaiah53_16x9.frozen.bak.mp4` (1.0x frozen film),
`narration.natural1x.bak.mp3` / `narration.immersive.natural1x.bak.mp3` (1.0x audio).

▶ NEXT: user watches the 1.20x / no-freeze cut. Speed still dialable (change `--target`, re-time, re-assemble).
If any boomerang scene still reads as directional, add its id to `DIRECTIONAL` and chain it (~$0.65/extra clip).

## ═══════════ SESSION END 2026-06-04 (LATEST) — ISAIAH 53 16:9 LONG-FORM FILM FINISHED ═══════════

**✅ The first 16:9 long-form FILM is done, end to end.**
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9\Isaiah53_16x9.mp4`
— 1920×1080, **8:03 (482.9s)**, 21 Baroque scenes, veo3_1_lite motion + slow ken-burns hold per scene,
balanced immersive soundstage muxed in. Closes on the risen Christ through "Have you believed the report?".

**How it was built (NEW 16:9 long-form path — pipeline was shorts-only):**
- Scene plan (free, hand-authored): `visual_16x9/scene_plan.json` — 21 scenes mapped to the 7
  movements + narration word-times + the soundstage cues (visuals match the sounds).
- Images: **NBP / Gemini 3 Pro Image** (`gemini-3-pro-image-preview`), 16:9 Baroque, via the existing
  NBPProvider with `ASPECT_RATIO="16:9"`. Driver `longform/_render_images_16x9.py`. ~$10.
  Image gate: looked at all 21 myself; rerolled only S4 (had come out an elderly beggar → fixed to the
  marred Servant, anchored jesus_variant=passion).
- Animation: **Higgsfield → veo3_1_lite** (16:9, 8s), via HFVideoProvider (`VIDEO_HF_ASPECT=16:9`).
  Driver `longform/_animate_16x9.py`. Anti-morph prompt (keep the painting frozen). 21/21 ok, the robed
  cross scenes (6,16) passed veo — NO Kling fallback needed. ~$8-11 Higgsfield credits.
- Assembly: `longform/_assemble_16x9.py` — each veo clip plays then a slow ken-burns push on its frozen
  last frame to fill its narration window; concat 1920×1080 30fps; mux narration.immersive.mp3. ffmpeg-only.
  GOTCHA FIXED: 21 segments lost ~2s to frame-rounding → don't `-shortest` against the short video; tpad
  the video's last frame to the audio length so the close isn't clipped.
- Test-first de-risk worked: rendered 1 scene (img+clip) before the batch; confirmed veo holds the Baroque oil.

**NEW: image_library/** (memory `image-library`) — 16:9 reusable Baroque stills bank, sibling to
sound_library + the 9:16 hero `_library`. 21 Isaiah-53 stills banked (neutral plates + gospel-Christ
reusable; story-specific = this-thread). Topical-fit discipline enforced.

▶ NEXT: user listens/watches the film; tweak any scene (reroll image / re-animate / adjust hold). The
soundstage cues already match the visuals. Prophet-voice re-cast still parked (panel-gated).

## ═══════════ SESSION END 2026-06-04 (LATE) — IMMERSIVE SOUNDSTAGE + SOUND LIBRARY + ENFORCED CURSOR-PANEL + ISAIAH 53 v3 RE-LOCK ═══════════

**Four things shipped this session (all in JesusInTheBible repo):**

1. **Immersive long-form audio (Isaiah 53 pilot).** Hand-crafted cinematic soundstage:
   13 layered environmental sounds across the 7 movements, placed on whisper word-times,
   mixed with ffmpeg (looped beds → one sidechain duck under the voice → one-shots → limiter).
   Two renders in the v1 folder: `narration.immersive_cinematic_full.mp3` (lean-in) +
   `narration.immersive_cinematic.mp3` (balanced). Scripts: `longform/_soundstage_cinematic.py`,
   `longform/_pilot_cue_times.py`. Rules locked: **FOREGROUND-DUCK** — voices AND animal calls
   get -7dB + deeper duck (atmospherics stay full); "Behold my servant" plays CLEAN.
   ⏳ AWAITING USER LISTEN: pick FULL vs balanced; flag any cue. Memory `longform-soundstage-pipeline`.

2. **Sound library** (`sound_library/`): generate once, reuse across long+short form. 28 neutral
   clips + living catalogue `SOUND_IDEAS.md` (both biblical-times lists merged). `sound_library.py`
   (find/register/import). Spend this session ~$11-14 ElevenLabs (durable asset). Memory `sound-library`.

3. **ENFORCED independent review** (`independent_review.py`): after a narration/significant plan, an
   outside panel (cursor primary + claude/gemini/codex/grok, local CLIs, NO metered API) adversarially
   reviews before it's called done. **Hard rule now in CLAUDE.md.** Memory `enforced-independent-review`.

4. **Isaiah 53 narration v3 RE-LOCK.** The new panel CAUGHT a real Acts 8:35 KJV elision the engine
   missed (+ 53:10-11 splice, 49:3/53:3 punctuation, "pierced"). All fixed + verified vs cache + ASR.
   Then applied 4 user-approved EDITORIAL fixes (M1 "rich man in his death"; M6 hint-only resurrection;
   M7 "taken away" not "paid in full"; M7 "bore them in your place"). Audio re-rendered → **482.89s**,
   immersive mix rebuilt on the new timeline. narration.md status = v3 LOCKED.
   ▶ Optional next: one final confirmation panel pass on the v3 narration (KJV already clean).

---

## ═══════════ SESSION END 2026-06-04 — ISAIAH 53 PANEL MERGED + LONG-FORM AUDIO RENDERED — READ FIRST ═══════════

**Isaiah 53 long-form pilot is now SCRIPT-LOCKED (v2) + has multi-voice AUDIO.** Folder:
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\`

### ✅ External AI panel JUDGED + merged into narration.md (now v2, lock-ready)
Panel output: `C:\Users\sanjay\PycharmProjects\PythonProject1\ai-panel\runs\2026-06-03-22-26-11\final-narration.md`
(judge=claude; gemini=polish; codex=nothing substantive). Folded in the winning fixes:
- **M2 KJV verbatim fix** — dropped the altered `"We hid as it were our faces from him."` (KJV 53:3 is
  "and we hid…"; the draft capitalised + clipped it). Every remaining quote mark is now exact KJV.
- **M4 objection steel-manned** — now CONCEDES Isaiah 49:3 ("Thou art my servant, O Israel" — God really
  does call the nation "servant"), then answers SINLESSNESS FIRST (53:9, kills nation + remnant), then
  53:8 "for my people." Verified 49:3 verbatim via bible-api. Biggest quality lift.
- **M6 resurrection over-read softened** — "hiding in plain sight" → "a shape that only resurrection
  fills… the NT brings to full light" (NT-confirmed, not proven from bare Isaiah).
- **M3 pacing trim.** Sourcing ledger + status line updated.
- OPEN (cosmetic): terminal punctuation inside clipped quotes (KJV colon vs script period) left as-is.

### ✅ Long-form AUDIO built BY HAND (no pipeline existed) — natural pace, multi-voice
- **`narration.mp3` = 476.56s (7 min 57s)**, atempo locked **1.0 (zero time-stretch)** per the natural-speed rule.
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\narration.mp3`
- NEW artifacts: `narration-tagged.md` + `voices.json` (narrator LSi9zNCeliLuhIGGS0By · the_LORD/god
  UzI1NsMEV3ni5JRkRSls on Isa 52:13 · eunuch/disciples puDRtQWF8NtQiPMJygTb on Acts 8:34).
- **HOW (reuse this for long-form):** wrap EVERY KJV quote as a `<speaker>` span (the_LORD/eunuch for the
  two voiced ones, `narrator` for the rest) so per_turn_synth splits the read into 35 small eleven_v3-safe
  turns (longest 794 chars). Then run with **`--natural`** + a high `--target` ceiling so it never compresses:
  ```
  export $(grep ELEVENLABS_API_KEY <PythonProject1/.env | xargs)
  <JITB .venv>/python.exe <PythonProject1>/jesus/narration/per_turn_synth.py "<v1>" \
      --target 600 --natural --no-gate --pre-quote-pause 0.4 --post-quote-pause 0.35 --stability 0.65
  ```
  (per_turn_synth calls NO LLM — only ElevenLabs — so no agent-bridge needed. ~6.5k chars ≈ $1–2.)
- ⚠️ UNVERIFIED BY EAR: the `[slow]/[reflective]/[deliberate]` delivery tags on narrator paragraphs —
  eleven_v3 usually treats them as cues but can occasionally voice one. User to listen; if a stray tag is
  spoken, strip tags on that turn + re-render the single `_turns/NN_*.mp3` with --force.

### ▶ FIRST THINGS NEXT SESSION (Isaiah 53 long-form)
1. **User listens to `narration.mp3`.** If a delivery tag is verbalised or a voice is off → fix that turn.
2. If audio approved → decide the VIDEO path (the user chose "audio first"; video not yet greenlit).
   16:9 long-form visuals are NOT built (cli_visual is 9:16/shorts-shaped). Options + spend below; ASK first.
3. Production-path decision still open: extend the engine for long-form (structures.json entry + 16:9
   visual mode + veo3_1_lite) vs keep hand-crafting. The audio half is now a proven hand-craft recipe (above).

### Decisions made this session (user)
- **Length: KEEP ~8 min** (the verbatim Servant Song is the "full meal"; trimming <7 min cuts depth not Scripture).
- **Scope: AUDIO FIRST** (done). Full 16:9 video NOT yet authorised — quote spend before building it.

## ═══════════ SESSION END 2026-06-03 (LATE) — LONG-FORM PILOT STARTED (Isaiah 53) — READ FIRST ═══════════

**NEW DIRECTION (user):** build a **long-form** companion to the shorts — 16:9, **~6–8 min**, same
narration style + animation, but **deep, substantial, "a full meal"** (the short is "a quick snack").
Must be heavily researched, well-structured, make sense to a first-time listener, rooted in the Bible,
and bring out depth the shorts can't. Picked **one pilot topic from the catalogue: Isaiah 53 — The
Suffering Servant** (~5–7 min target chosen; landed ~7.5–8 min). Memory: `longform-deep-dive-format`.

### ✅ ep08 Woman at the Well (John 4) — FINISHED earlier this session
- `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\08 The Well That Never Runs Dry\v1\assembly\viral_cut.mp4` (59.0s)
- 11 clips, none reused, every beat matched (verified frame-by-frame), opens on the woman, closes on Christ at the well. Both reviews LOCKED. Library now 88 stills.

### ▶▶ LONG-FORM PILOT — WHERE IT STANDS (do this first next session)
Working folder (NEW — long-form lives in THIS repo, not PythonProject1):
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\01_Isaiah_53_Suffering_Servant\v1\`
- **`narration.md`** — the LOCKED-candidate script. **7-movement long-form spine** (the new structure):
  Report → Behold My Servant (scandal) → The Exchange (substitution heart) → Silent Lamb + honest
  objection → "Of whom speaketh the prophet this?" (Acts 8 fulfilment) → It Pleased the LORD →
  The Arm of the LORD (conviction+landing). Passage walked verbatim = Isaiah 52:13–53:12 + Acts 8:32-35.
  Tightened after internal red-team (1348 → ~1180 spoken words; ~28% is unavoidable KJV quote).
- **`panel_request.md`** — the document the USER asked for, to feed his **external AI panel**.
  Adapted from `pipeline/panel.py` for long-form: engine/red-team self-assessment (attack length /
  M3-M5 drag / resurrection over-read / objection / landing) + full 7-movement script (KJV bolded
  + referenced) + a copy-paste PROMPT block with 8 binding rules for 2–4 external LLMs.
- **Internal independent red-team already done** (general-purpose agent): verdict REVISE → only real
  defect was LENGTH; doctrine SOUND, every KJV quote verbatim, objection steel-manned, landing
  grace-anchored. Its cut list was applied.

### ▶ FIRST THINGS NEXT SESSION (long-form)
1. **User is running `panel_request.md` through his external AI panel tonight** — he'll bring the
   replies back. JUDGE them, fold winners into `narration.md`, lock the script.
2. Open decision he was asked (UNANSWERED — he pivoted to "panel it" + "save for tomorrow"):
   (a) keep ~8 min as-is vs trim narration to <7 min; (b) how far to take the pilot — full
   audio+16:9 video / audio-only first / script-only. **ASK before any metered spend.**
3. When script locks → build the long-form PRODUCTION path. NOT YET BUILT (this was a hand-crafted
   pilot, no pipeline): need (a) multi-voice audio at long-form length (narrator + `the_LORD` for
   Isa 52:13 + `eunuch` for Acts 8:34 — voices.json TBD), (b) **16:9** scene plan (cli_visual is
   9:16/shorts-shaped — long-form needs 16:9 + more scenes), (c) **veo3_1_lite** animation (the
   LOCKED long-form video model, `VIDEO_PROVIDER=hybrid`, `VIDEO_HF_MODEL=veo3_1_lite`,
   `VIDEO_DURATION=8` — veo keeps the Baroque look at ~half Kling credits; falls back to direct-Kling
   for the NSFW-blocked cross), (d) a 16:9 assembly. Decide: extend the engine (structures.json
   long-form entry + 16:9 visual mode) vs keep hand-crafting the pilot. Quote spend first.

### NOTE on length math
Walking the full Servant Song verbatim is naturally ~7.5–8 min — the verbatim chapter+Acts is ~330
spoken words (~28%) and won't be cut. Forcing <7 min means trimming narration depth, not Scripture.

## ═══════════ SESSION END 2026-06-03 — NATURAL SPEED + MORE CLIPS — READ FIRST ═══════════

**User direction (LOCKED, memory `feedback-natural-speed-more-clips`):** narration plays at NATURAL,
CONSTANT speed — never time-stretch to hit 59s. 59s is a CEILING: under is fine; over → TRIM WORDS
(never compress the voice). And use MORE video clips, speeding up the CLIPS (not the voice) so each
lands on its narration beat.

### Engine changes shipped (agent-mode/free, all in this repo)
- `config.SHORTS_NATURAL_SPEED` (NEW, default ON) → `handoff.py` passes `--natural` to per_turn_synth.
  per_turn_synth `--natural` was already built (atempo locked 1.0, --target = ceiling, flags words to
  trim if over). Set `SHORTS_NATURAL_SPEED=0` to revert to atempo-to-target.
- `config.ASSEMBLY_CLIP_BUDGET` 11 → **14** (more clips; allocator already speeds clips, sacred ≤1.3×).
- `_finalize.py` now ALSO clears `_turns/*.mp3` + `narration.meta.json` (fixes the stale-_turns trap).
- `runner.py` "run later" hint shows `--natural`.
- ⏳ NOT YET DONE (the user's beat-precision ask): the assembler still places clips per SECTION
  (`assembly_engine._video_windows`), not pinned to each spoken phrase's time window. Tightening this so
  each clip sits exactly under the line it depicts is the next code task — but it can't be tested until
  the 5 I AM episodes have VISUALS (none rendered yet).

### The 5 I AM episodes RE-RENDERED at natural speed (ElevenLabs ~$0.60 this session)
| Ep | Folder (…/PythonProject1/jesus/narration/) | Natural length | Note |
| --- | --- | --- | --- |
| 32 | `32_The_Door_Was_a_Body/v1/narration.mp3` | **60.6s** | trimmed −7 narrator words; accepted ~60s |
| 33 | `33_The_Shepherd_In_The_Gap/v1/narration.mp3` | **60.2s** | trimmed −6 words; accepted ~60s |
| 34 | `34_The_Hunger_Bread_Cant_Fill/v1/narration.mp3` | **52.9s** | already natural; untouched |
| 35 | `35_Manna_Fulfilled/v1/narration.mp3` | **65.2s** | Option A narrator trim (full John 6:51 kept); user accepts 65s — it's the long one |
| 36 | `36_In_No_Wise_Cast_Out/v1/narration.mp3` | **54.6s** | already natural; untouched |

All edited episodes (32/33/35) re-stamped via `short_gate.py … --stamp --register` — 32 PASS, 33 CONDITIONAL
(its usual scene-first open), 35 PASS (verse verified verbatim). 34/36 untouched. **All 5 are LOCKED audio.**

### Re-render gotchas hit this session (so you don't repeat them)
- `rm` in the Bash tool needs **forward-slash** paths — backslash paths silently no-op (-f), leaving stale
  `_turns/*.mp3` that per_turn_synth then `[skip]`s. Use `C:/Users/.../v1/_turns/*.mp3` or `--force`.
- Editing narration.md invalidates the short_gate stamp → per_turn_synth GATE-BLOCKs. Re-run
  `short_gate.py "<v1>" --stamp --register` (deterministic, no LLM) before re-synth.
- ElevenLabs re-rolls voice timing each render (±1–2s) → chasing strict ≤59 is a moving target; that's
  why 32/33 were accepted at ~60s.

### ▶ FIRST THINGS NEXT SESSION
1. (Optional) tighten the assembler to pin clips to each spoken phrase's window (the beat-precision ask).
2. The 5 I AM episodes still need VISUALS — run `cli_visual.py "<v1 folder>"` (with the new 14-clip budget).
3. Or pick the next multi-dimension topic (Woman at Well / Prodigal / Psalm 22 / John 21:17).

## ═══════════ SESSION END 2026-06-02 (LATE) — DOOR (×2) + BREAD (×3) SHIPPED ═══════════

**Where we are:** 5 I AM-set narrations LOCKED + rendered across TWO sayings. **Full paths** (for other-service handoff).

### I AM the Bread of Life (×3) — SHIPPED (Cursor session + ai-panel merge)

| Ep | Folder | Audio |
| --- | --- | --- |
| 34 | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\34_The_Hunger_Bread_Cant_Fill\v1\` | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\34_The_Hunger_Bread_Cant_Fill\v1\narration.mp3` (59.02s) |
| 35 | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\35_Manna_Fulfilled\v1\` | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\35_Manna_Fulfilled\v1\narration.mp3` (59.03s) |
| 36 | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\36_In_No_Wise_Cast_Out\v1\` | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\36_In_No_Wise_Cast_Out\v1\narration.mp3` (59.02s) |

**Panel request (engine):** `C:\Users\sanjay\PycharmProjects\JesusInTheBible\data\bread_of_life_panel_request.md`

**ai-panel merge (4/4 drafts):** `C:\Users\sanjay\PycharmProjects\PythonProject1\ai-panel\runs\2026-06-02-08-56-02\final-narration.md`

**Brief:** `C:\Users\sanjay\PycharmProjects\PythonProject1\ai-panel\examples\bread-of-life-panel-brief.txt`

**Ship order:** 36 → 34 → 35

**Gates:** `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\short_gate.py` — all three PASS + stamped.

**Unattended synth:** `$env:LLM_PROVIDER="api"` before `narration_pipeline.py` (agent-bridge blocks).

**Narration pickup doc:** `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\RESUME.md`

### I AM the Door (×2) — SHIPPED earlier today

| Ep | Folder | Audio |
| --- | --- | --- |
| 32 | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\32_The_Door_Was_a_Body\v1\` | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\32_The_Door_Was_a_Body\v1\narration.mp3` |
| 33 | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\33_The_Shepherd_In_The_Gap\v1\` | `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\33_The_Shepherd_In_The_Gap\v1\narration.mp3` |

**Method (reuse):** multi-dimension drafts → one combined panel request → external LLMs → judge/synthesize → gate stamp → render.

**Multi-dimension direction:** `multi-dimension-per-topic` (memory). See FIRST THINGS below.

---
**Earlier today — #6 I AM the Door (John 10:9) FINISHED as TWO complementary episodes**, both LOCKED + rendered (2-voice narrator+jesus, ~59s, relaxed atempo ~1.03–1.04, no rush):
- ✅ **32 The Door Was a Body** — the *invitation* dimension: deity ("I AM", too holy to speak) gives
  weight; heart = "come in and be saved — the door is open for you AS YOU ARE, before you fix a thing";
  delivers the verse's saved/safe/fed/pasture payoff. ~151 words. LOCKED-as-is (user-directed v-c, no
  external panel; `panel_request.md` on disk reflects the superseded v-b deity version).
  `PythonProject1/jesus/narration/32_The_Door_Was_a_Body/v1/narration.mp3`
- ✅ **33 The Shepherd In The Gap** — the *shepherd-as-the-gate* dimension: the sheepfold gap, His body
  in it, the wolf comes first (substitution/protection). Shipped v-a as-is at the user's choice (devotional
  latitude). ⚠️ KNOWN ACCEPTED RISK: rests on the CONTESTED fold-folklore ("no gate, shepherd's body = the
  door", "no figure of speech") — John 10:1-3 itself names a doorkeeper+door. Agent flagged it pre-render;
  user accepted (SLK = devotional, not Awakeden apologetics). Faithful core is sound (only-access + body-takes-
  the-wolf grounded in John 10:11 "the good shepherd giveth his life for the sheep").
  `PythonProject1/jesus/narration/33_The_Shepherd_In_The_Gap/v1/narration.mp3`

### ▶▶ NEW STANDING DIRECTION (user, 2026-06-02) — EXPLORE MULTIPLE DIMENSIONS PER TOPIC
One Bible passage can speak **several distinct truths** and serve more listeners — so deliberately produce
**multiple doctrinally-faithful narrations per topic** (as we just did with John 10:9 → invitation + shepherd-gate),
not one per passage. **NON-NEGOTIABLE: every dimension must be Bible-driven and fit evangelical biblical
doctrine.** Freshness in the entry-point only; orthodoxy in the claim and landing (the locked rule still holds).
Memory: `multi-dimension-per-topic`. When considering ANY topic, think across all the Bible-based narratives /
angles it can faithfully carry, pin each to a verse, and offer them. A starter dimension-map is in the FIRST
THINGS block below.

### ▶ FIRST THINGS NEXT SESSION
The redo backlog (27/28/29/30/31/32/33) is CLEAR. Next: pick a topic and explore its faithful dimensions
(user's new direction). Remaining distinct redo topics — each now a CANDIDATE for multiple dimensions:
- **Woman at the Well** (John 4:14) — dims e.g. (a) living water / never-thirst-again; (b) He told her all she
  ever did = seen-and-still-wanted; (c) "I that speak unto thee am he" = the Messiah self-revealed to an outsider.
- **Prodigal** (Luke 15) — dims e.g. (a) the running father / kiss that cut off the bargain (shipped #12);
  (b) the elder brother / grace that offends the dutiful; (c) "this my son was dead, and is alive again" = resurrection language.
- **Psalm 22** — dims e.g. (a) "My God, my God, why hast thou forsaken me"; (b) "they pierced my hands and my
  feet"; (c) "they part my garments" — predictive precision; (d) the turn to praise in v22-31.
- **Fire / threefold** (John 21:17) — needs the pacing-vs-repetition design call; dims e.g. (a) threefold
  restoration mirrors threefold denial; (b) charcoal-fire (anthrakia) callback; (c) "feed my sheep" = restored calling.
Confirm series id before `_regen_one.py`, OR (faster, proven this session) hand-author each dimension's text +
2-voice render direct when the user has a clear angle. ASK est. spend before any metered batch (audio ~$0.20/ep).

### How #6 was finished (method that worked — reuse it)
Hand-tag `narration-tagged.md` (jesus speaker on the verse) → **delete `_turns/*.mp3` + narration.mp3 + meta**
(the `_finalize` stale-_turns trap) → run `per_turn_synth.py "<v1>" --target 59 --pre-quote-pause 0.5
--stability 0.65 --force` directly. New sibling episodes = new underscore folder (e.g. `33_...`) with
narration.md + narration-tagged.md + voices.json (narrator LSi9zNCeliLuhIGGS0By + jesus tlETan7Okc4pzjD0z62P).

(Prior history — panel gate / recursive learning / 4 proposed calibration fixes — still applies; see below.)

## ═══════════ SESSION END 2026-06-01 (LATE) — #6 I AM THE DOOR IN PROGRESS — READ FIRST ═══════════

**Where we are:** panel backlog cleared earlier today (#29 + #30 LOCKED; 27/28/29/30/31 all done). Then
started the next redo topic **#6 "I AM the Door" (John 10:9, series `i-am`)** end-to-end in agent-mode
(thread→tournament→judge→synth→self-review→independent, all serviced in chat). Folder (NEW underscore naming):
`PythonProject1/jesus/narration/32_The_Door_Was_a_Body/v1`.

### ▶▶ #6 IS MID-ITERATION — DO THIS FIRST TOMORROW
The TEXT has been reworked 3 times based on the user's direction; `narration.md` currently holds the
**invitation-centered** version (the keeper-in-progress). **`narration.mp3` on disk is STALE** (an earlier
shepherd-spine 2-voice render) — it does NOT match the current narration.md. Nothing is locked.
1. Re-read the current `narration.md` (the invitation version). Decide with the user: render as-is, tweak the
   invitation wording, or run one more panel.
2. To render: it's **2-voice (narrator + jesus** on the "I am the door" verse); voices.json already = narrator+jesus.
   Hand-tag narration-tagged.md (jesus speaker on the verse), then **delete `_turns/*.mp3` + narration.mp3 +
   narration.meta.json** (the _finalize stale-_turns bug) and run per_turn_synth.py directly (target 59,
   pre-quote-pause 0.5, stability 0.65). ~$0.20 ElevenLabs.
3. Then LOCK + update calibration.jsonl/RESUME/STATE.

### #6 iteration history (so you don't relitigate)
- v-a: shepherd-as-door (body sleeps across the gap) — panel flagged it rests on CONTESTED field-fold folklore
  (10:1-3 has a porter+door) and drops the verse's "go in and out, find pasture" payoff.
- v-b: user said "lead with the I AM / deity" → reframed on the divine Name (Ex 3:14 "I AM THAT I AM" echo);
  panel (5 LLMs) said CUT "a door takes the blow meant for the sheep" (rule-6 substitution import from 10:11),
  present-tense the claim (not "became"), withhold "the door" from the Point. Applied.
- v-c (CURRENT): user said "'I am the door' must land as a PERSONAL salvation INVITATION, not a metaphor/riddle."
  Reweighted: deity gives weight, but the heart is "come in and be saved — open for you, as you are" + delivers
  saved/safe/fed/pasture. This is what's in narration.md now. `panel_request.md` still reflects v-b (regenerate
  via the script in chat history / `_panel_existing.py`-style if re-paneling v-c).

### CURRENT #6 narration.md (invitation version, ~151 words, 1 KJV quote John 10:9):
Hook: God's own name is "I AM" — too holy to speak. And that God looked at people who could never climb up to
Him, and opened a door. | Point: He doesn't hand you a ladder to climb, or a list to finish. He is the way in —
and the way is a Person. | Proof: Hear Him: "I am the door: by me if any man enter in, he shall be saved, and
shall go in and out, and find pasture." Any man. That's the invitation: don't earn your way up — come in through
Him, and you're saved, safe, and fed. | Conviction: You keep waiting until you've cleaned yourself up enough to
be let in. But the door is already open — open for you, as you are, before you fix a thing. | Landing: So come
in. The great I AM is the door, and He's holding it open for you. Step through — the pasture was waiting all along.

(Panel backlog + locked-episode details + the 4 proposed calibration fixes are in the REDO PROGRESS / FIRST
THINGS blocks below. The 2026-05-31 context — workflow / panel gate / recursive learning — still applies.)

## ═══════════ SESSION END 2026-05-31 — REDO PROGRAM + PANEL GATE + RECURSIVE LEARNING — READ FIRST ═══════════

**Big picture:** we are RE-DOING all ~10 distinct narration topics through an upgraded,
panel-reviewed pipeline (user: "redo them all for the best outcome"). Decisions locked:
**narrations-only this pass** (visuals later, per-episode), **panel every landing/script**,
**keep the 4 shipped cuts live** (redo into NEW folders), **one topic at a time**, **agent-mode only**.

### NEW WORKFLOW (this is how every episode runs now)
1. `python _regen_one.py "<series_id>" "<Book c:v>"` → runs text tournament + both reviews in
   agent-mode, then **STOPS at the PANEL GATE**: writes `<v1>/panel_request.md` (engine
   self-assessment + a ready-to-paste external-LLM prompt) and renders **NO audio**.
2. User pastes `panel_request.md` into 2-4 other LLMs, brings the replies back.
3. Agent JUDGES the panel feedback, finalizes the beats by editing `<v1>/narration.md`.
4. `python _finalize.py "<v1>"` → renders the audio (ElevenLabs, ~$0.20; service the bridge
   tag/verify/audit calls in chat). Clears stale artifacts first.
The panel gate is now a real runner property (`runner.create_narration(panel_gate=True)`), not
a step to remember. **ALWAYS check the bridge request's 'YOUR TASK' line** before answering —
a deterministic-gate FAIL flips self-review to a REVISE (expects a revised DRAFT, not a review).

### REDO PROGRESS (folders in PythonProject1/jesus/narration/)
- ✅ **27 A List of Dead Men** (Matt 16:15) — FINALIZED.
- ✅ **28 What Manner of Man** (Matt 8:26 storm) — FINALIZED (paneled).
- ✅ **30 Smitten of God** (Isaiah 53:5) — LOCKED 2026-06-01 (paneled by 3 LLMs; judged → dropped the
  1-Peter quote so Proof is 2 Isaiah quotes, fixed 53:4 to verbatim '...smitten of God, and afflicted.').
  Landing reworked to identity-forward ('The punishment was real, but the guilt was never His. He took
  yours — into His own body.'). **Isaiah VOICE added** for the two prophecy quotes (weighty voice
  UzI1NsMEV3ni5JRkRSls) → 5-turn multi-voice, 59.02s, narrator atempo 1.2285. ⚠️ _finalize.py does NOT
  clear _turns/*.mp3 → edits silently reuse stale per-turn audio; delete _turns manually + run
  per_turn_synth directly (or fix _finalize to clear _turns).
- ✅ **29 The Race He Could Never Win** (John 5:6 Bethesda) — LOCKED 2026-06-01. Paneled by 4 LLMs
  (panel_request.md rebuilt via new helper `_panel_existing.py`). Strong convergence: (1) Rule-1 quote-
  SELECTION fix — the draft paraphrased the title question 'Wilt thou be made whole?' and spent both quote
  slots on secondary verses; now quotes John 5:6 + 5:8; (2) Rule-4/5 conviction fix — 'he asks if you still
  want it' (viewer-produced desire = grace-trap RECURRENCE) reframed to grace exposing 'you must close the
  distance to God before He acts'. KEPT the RACE spine (did NOT fold panel-4's 'he never said yes' insight —
  that's the shipped #18's thread, same passage; kept #29 distinct). 2-voice (narrator + jesus on both
  quotes), 59.04s, narrator atempo 1.1593, 158 words. (Series = questions-jesus-asked.)
- ✅ **31 The Light You Can Stand In** (John 8:12) — FINALIZED (paneled 6 LLMs; honest
  woman-scene-with-pillar-of-fire spine). Audio confirmed 2026-06-01: 59.02s.
- 🔶 **32 The Door Was a Body / I AM the Door** (John 10:9, series `i-am`) — TEXT MID-ITERATION (invitation
  version in narration.md), NOT rendered (mp3 is stale). See the "#6 IS MID-ITERATION" block at top. Do first.
- REMAINING distinct topics to redo (after #32): Woman at the Well (John 4:14) · Prodigal (Luke 15) ·
  Psalm 22 · Fire/"Do You Love Me" (John 21:17 — THREEFOLD, needs a pacing-vs-repetition design call first).

### ▶ FIRST THINGS NEXT SESSION
**Panel backlog is now CLEARED — 27/28/29/30/31 all LOCKED.** Next redo topic: **#6 I AM the Door
(John 10:9)** — run `_regen_one.py "questions-jesus-asked-or-correct-series" "John 10:9"` (confirm series id
first) → panel gate → user panels → judge → `_finalize.py` (or hand-render the 2-voice path if multi-voice).
Remaining distinct topics after that: Woman at the Well (John 4:14) · Prodigal (Luke 15) · Psalm 22 ·
Fire/threefold (John 21:17 — needs the pacing-vs-repetition design call first).

**Calibration fixes PROPOSED (awaiting approval), now 4 across #30+#29 panels:**
   (a) deterministic **Rule-8 quote-count gate** (>2 double-quoted spans FAILs a pacing gate; #30);
   (b) **widen kjv_check coverage** — feed the cached wider pericope (passage:<ref>) to verbatim_mismatches
   so flanking-verse quotes are checked, not just the single anchor verse (#30 Isa 53:4 slipped);
   (c) deterministic **anchor-verse-unquoted check** — the episode's primary_ref verse must appear as a
   quoted span (esp. the QUESTION for Questions-Jesus-Asked); #29 paraphrased 'Wilt thou be made whole?';
   (d) extend the **grace-trap gate to the CONVICTION beat** (not just the landing) — #29's 'he asks if you
   still want it' recurred there. See data/learning/defect_classes.json (3 classes re-opened/added 2026-06-01).

**Two known engine traps to fix when convenient (free, agent-mode):**
   - `_finalize.py` does NOT clear `_turns/*.mp3` → editing narration.md + re-finalizing silently REUSES
     stale per-turn audio. Workaround used this session: delete `_turns/*.mp3` + narration.mp3 + meta, run
     per_turn_synth.py directly. FIX: have _finalize clear `_turns/` too.
   - New episode folders now use **underscores not spaces** (handoff.py `_safe_title` + `_LEADING_NUM`),
     so paths are click-to-open; legacy folders kept as-is. User strongly prefers QUOTED full paths or
     underscore paths in chat (memory `feedback-show-full-paths`).

### ENGINE CHANGES SHIPPED THIS SESSION (all committed-worthy, agent-mode/free)
- **Landing-not-tired + grace-tuned-question + scene-scope** rules locked into constitution +
  generate prompt + judge (memory `feedback-landing-not-tired`).
- **Panel gate** (`pipeline/panel.py`, `_regen_one.py` panel_gate, `_finalize.py`).
- **Tournament judge can graft ANY beat** (not just hook/CTA) + apply `synthesis_notes`
  (`engine._collect_grafts`; legacy graft_hook_from/cta_from still work).
- **RECURSIVE LEARNING — the calibration loop** (memory `recursive-learning-system`):
  `data/learning/{defect_classes.json, calibration.jsonl}` + `pipeline/learning.py` + `_calibrate.py`.
  Logs what the external panel caught that self-review missed; PROPOSES fixes; user approves.
  **5 fixes applied + verified** (deterministic KJV gate `pipeline/kjv_check.py` wired into both
  reviews; self-review strengthened on scene-scope / shaming / grace-trap / viewer-turn). Run
  `python _calibrate.py` to see blind spots. Autonomy = **propose-I-approve**.
- **kjv_check bug fixed**: it false-positived on truncated quotes; now only flags a real
  sentence-ender mismatch (the Matt 8:27 '!'-vs-'?' case). Verified.
- Open red-team findings (NOT yet fixed): cli.py/cli_pipeline.py bypass the panel gate;
  atempo>1.30 ships with a warning not a block; no KJV check for cross-ref (NT) quotes.

### Calibration loop — how to feed it each episode
After a panel + finalize, append a record to `data/learning/calibration.jsonl`:
`{episode, ref, self_review, independent, panel_misses:[{defect_class,beat,detail,caught_by,deterministic}], user_verdict}`.
If a "fixed" defect class recurs in panel_misses, re-open it. Phase 2 (designed, not built):
regression set + auto-promotion. Phase 3: audience retention → reweight tournament priors.

## ════════════════════════════════════════════════════════════════

## ═══════════ SESSION END 2026-05-30 (LATE) — CLARITY FIX + COST CONTROL ═══════════

**Nothing is mid-flight. Bridge queue empty. Safe to stop. Picking up = listen to 3 mp3s.**

### What happened this session
1. **Audio quality fixes** (committed) — god voice → HF-POC's shipped
   `UzI1NsMEV3ni5JRkRSls`; dialogue gaps (pre 0.5s + post 0.45s) around every quote;
   fixed a duplicate-line bug pinning word count to 165 (made narrator rush). Word
   target now 115–140. `config.py` + `pipeline/handoff.py`.
2. **First-hearing clarity test** locked into the engine (committed) — this was the fix
   for the user's "clever but doesn't make complete sense" rejection. In 5 places:
   generate prompt, new gate **G8.6**, tournament judge weighting, **G1 now FAILs
   exegetically false asides**, and a "CLARITY BEATS CLEVERNESS" section in
   `data/constitution.md` (cached prefix → every call sees it). Rule: spine must be a
   FELT TRUTH, never a writerly conceit (geography/grammar/wordplay only season a line);
   zero-Bible-knowledge assumed; no logic-tricks; no self-contradiction.
3. **Three rejected narrations regenerated from scratch**, all LOCKED (self +
   independent), audio rendered ~60s with the new pacing:
   - `24 The Answer Was a Gift` (Matt 16:15) — was "Cliff of Rival Gods"
   - `25 The Question on the Gaza Road` (Isa 53:5) — was "Pronouns That Preached"
   - `26 Jesus Walked Past the Pool` (John 5:6) — was "He Never Answered Jesus"
   (in `PythonProject1/jesus/narration/`; old 19/21/22 LEFT UNTOUCHED for A/B)
4. **COST CONTROL** (committed) — `REVIEW_MODEL=claude-sonnet-4-6`: Opus only for
   WRITING (draft tournament / synthesize / revise), Sonnet for the ~6-8 review/judge
   calls per episode. Big cost drop, quality barely moves. Override:
   `REVIEW_MODEL=claude-opus-4-7`.
5. **STANDING RULE (memory `feedback-ask-before-spending`)**: ALWAYS quote estimated
   spend and wait for explicit OK before any metered batch run. The user was surprised
   by ~$15-18 of Opus on the 3-episode regen. Each text episode = ~11-19 LLM calls.
   Free alternative = agent-bridge (`LLM_PROVIDER=agent`, the default).

### ▶ FIRST THING NEXT SESSION — listen + judge #24/#25/#26
```
start "" "C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\24 The Answer Was a Gift\v1\narration.mp3"
start "" "C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\25 The Question on the Gaza Road\v1\narration.mp3"
start "" "C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\26 Jesus Walked Past the Pool\v1\narration.mp3"
```
If they read clear → proceed to the **5-narration batch** the user wanted: these 3 +
**2 more strong OT picks** (to choose, from `jesus-in-ot`: Sign of Jonah / Pierced
Zech 12:10 / Bethlehem Micah 5:2 / Crucifixion Foretold Ps 22:16). Then **batch
hero/still image design** reusing the 12-plate `_library` + Jesus Soul ref.
**REMEMBER: quote the est. spend and get an OK before running the batch.**

### Still open / not done
- `23 The Prepared Belly` (Jonah) text LOCKED but NO audio (never cleared tag stage;
  can run now — API cap is lifted).
- Default female voice in `config.VOICE_MAP` (carried from prior session).
- Folder-naming cleanup of the narration tree.
- Wire `_library` plates into the engine image stage (reuse before generating).
- Automatic daily Drive backup of `_library`.

### Run one episode (text+audio, stops at Gate 1)
```
.venv\Scripts\python.exe _make_ep.py <series_id> <episode_index>   # questions-jesus-asked | jesus-in-ot
```
`_regen3.py` regenerates the specific 3 rejected topics. Both force `LLM_PROVIDER=api`
(remove that line for the free bridge). Known gotcha: `per_turn_synth` round-trip audit
false-positives when the tagger strips quote-marks around a `<speaker>` line (blocked
#26); bypass by running `per_turn_synth.py <v1> --target 60 --pre-quote-pause 0.5
--post-quote-pause 0.45 --stability 0.65 --force` directly. (memory
`feedback-audio-pacing-and-god-voice`.)

## ════════════════════════════════════════════════════════════════

## ═══════════ SESSION END 2026-05-30 — READ THIS FIRST (handoff) ═══════════

**Where we are:** the engine is a proven topic→final-cut pipeline running in **agent-mode**
(LLM_PROVIDER=agent, zero metered API — every LLM call serviced in-chat via the file bridge).
A full episode (QJA #03) was produced end-to-end this way. The **still bookend** (identical
first & last frame, hero held ~2s each, narration continuous) is baked in and applied to all
finished cuts. A **production + posting tracker** now lives on the user's Google Drive.

**✅ 4 cuts finished + upload-kitted** (in the Drive tracker's READY TO POST queue):
- QJA #02 "Why Are You Afraid" (Matt 8:26) — `…/02 Why are you afraid/v3/assembly/viral_cut.mp4`
- QJA #03 "He Never Said Yes" (John 5:6) — `…/18 He Never Said Yes/v1/assembly/viral_cut.mp4`
- QJA #04 "The Fire Jesus Built" (John 21:17) — `…/16 The Fire Jesus Built/v1/assembly/viral_cut.mp4`
- Prodigal "The Kiss That Cut Off the Bargain" (Luke 15:20) — `…/12 The Kiss…/v1/assembly/viral_cut.mp4`
(prefix `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration`)

**TRACKER (Drive, user-owned, living):**
`G:\My Drive\0 Personal\0Company\jobs\0salinss\saltandlightkingdom\0 Christianity\PRODUCTION & POSTING TRACKER.md`
— dashboard, cross-series OVERLAP map, READY-TO-POST queue with per-clip upload kits
(title/desc/hashtags/pinned comment), full roadmap (8 greenlit series + QJA). Memory:
`slk-posting-tracker` (holds the kit + red-team copy conventions).

**Done this session:** full agent-mode QJA #03 (text reroll for punch → audio → 16-image
plan+render → 16 Kling clips → assembly), hero #09 image rerolled (bad finger) + re-animated
+ cut rebuilt, still bookend baked into the pipeline + applied to #18/#12 (engine) and #16
(overlay, since its John-21 threefold can't pass the standard assembler), the Drive tracker +
upload kits, and a RED-TEAM of the whole plan with fixes applied (below).

**RED-TEAM fixes APPLIED today:**
1. `pipeline/visual_render.py` — image audit now explicitly checks **anatomy** (hands/fingers/
   faces/limbs; hard-fail on a malformed foreground hand). The hero finger had slipped the
   old audit. Verify it triggers on the next render.
2. Tracker — added the cross-series **overlap map**, pinned-comments on all kits, fixed the
   prodigal mislabel (parable, not Encounters).
3. Kit copy conventions captured in memory `slk-posting-tracker`: **no clickbait** (charter
   bans withhold-the-answer curiosity gaps), **no shaming the person in the text** (don't call
   the Bethesda man's reply "excuses"), **per-platform hashtags** (#fyp=TikTok-only; #Shorts=YT;
   #Reels=IG/FB — give a YT/IG/FB set + a tight ~6-tag TikTok line), handle **@SaltandLightKingdom**.

## ▶ TOMORROW — START HERE (decided; implement first)
1. ✅ **DONE (2026-05-30) — Motion open / Christ-still close.** The assembler now OPENS on the
   animated hook clip (grabs the scroll) and only the CLOSE is the held hero still. Today's
   Implemented via `config.ASSEMBLY_OPEN_MODE=hook` (DEFAULT; `hero`=legacy both-ends still):
   allocate() sets hero_head=0 so the body plays from t=0 and the first body clip (a hook-open)
   leads; only the hero-tail (Christ) close remains, frozen via ASSEMBLY_HERO_STILL. AS-G6 +
   matcher/planner prompts + visual_engine hero text updated. ALL 4 cuts re-rendered + eyeballed
   2026-05-30 (3 engine cuts via deterministic re-allocate, no LLM; #16 rebuilt by hand). NOTE:
   #16 still opens ON the animated risen Christ at the fire (its hand-assembly opens on Christ);
   a true non-Christ hook-open for #16 needs the queued threefold/window-aware re-sequence.
   Originals kept as .pre-motion-open.bak / .still-both-ends.bak.
2. **Default female voice** (user decision: "pick a default for now"). Add a sensible ElevenLabs
   female `voice_id` to `config.VOICE_MAP` (woman/mary/martha/etc.) so women in Encounters etc.
   don't collapse to narrator. User may swap it later.
3. **Focus — STILL OPEN** (user wants to clarify): finish QJA 05–10 vs pilot I AM vs post the 4
   done first. Ask/confirm before producing the next topic.

## Improvements to consider tomorrow
- **Threefold/repeated-pattern assembler** (QUEUED per user) — build a window-aware allocation
  mode BEFORE the Last Week series (19 micro-beat eps) / any repeated-pattern episode; #16
  already had to be hand-assembled + overlay-bookended.
- **Per-slot verify samples mid-reframe** — the assembly Vision verify grabs a MID-slot frame,
  which often lands on a macro/insert (the mat, the pool, the crowd) instead of the establishing
  subject. Sample the establishing (early) frame per slot for stricter, truer reads.
- **Awakeden brand signature** — Types & Shadows + Resurrection on Trial are Awakeden, not SLK;
  their kits should sign off Awakeden + apologetic tone. (QJA/I AM/Encounters = SLK.)
- **Cross-series overlap** — decide a dedup/stagger strategy (tracker has the map): same passage
  in multiple series = near-duplicate videos; pick one angle or space them months apart.
- **Agent-mode servicing is heavy** (~90+ bridge calls/episode). Consider a small batch-serve
  helper / tighter loop so a full episode is faster to service in chat.
- **Codify kit generation** — eventually have the engine auto-draft the upload kit (title/desc/
  hashtags) per episode using the captured conventions, instead of hand-writing each.
- **Post the 4 done + gather retention data** before committing to 100+ more — real numbers
  should steer the still-bookend question and the hook style.

## ════════════════════════════════════════════════════════════════

## ═══════════ SESSION END 2026-05-29 (latest) — QJA #03 IN AGENT-MODE ═══════════

**✅ QJA #03 "Do You Want to Be Made Well" (John 5:6) — text + audio DONE, ZERO
metered API. KEEPER = `PythonProject1\jesus\narration\18 He Never Said Yes\v1`.**
(The first take, #17, was rerolled + DELETED — see below.)
- Full **agent-mode** runs: text tournament + both reviews + audio verify/tag/audit all
  serviced in-chat via the bridge. The 4-parallel-candidate tournament moment serviced fine.
- Tournament thread = **"He never said yes"** — the man's reply in v7 is not a yes
  (he answers Jesus' question with his excuse about the pool); grace heals him anyway.
- 3-voice (narrator / jesus / man), **59.03s, atempo 1.1635**. Both text reviews LOCKED.
- **Audio stage is now bridged too** — `narration_pipeline.py` verify/tag/audit route
  through the same file bridge (duck-typed `_BridgeResponse`). So a whole episode runs
  zero-API. (Memory `agent-mode-bridge` updated.)
- **REROLL LEARNING:** the user found the first draft soft — hook too literary, middle
  too sermonic. Fix that worked: re-run the tournament with a binding DIRECTOR'S NOTE in
  `notes` (grip in 3s / concrete-visceral / kill abstract commentary / show-don't-preach).
  For this user, default the QJA brief that way; the stock tournament leans literary.
  See memory `qja-series-production-status`.

**✅ STILL BOOKEND baked into the pipeline (2026-05-29/30, user feedback) AND applied to
ALL existing cuts.** The cut now opens AND closes on the SAME frozen still of the hero
(identical first & last frame — "two slices of bread"), ~2s each, animation as the meat
between, narration continuous. Applied: #18 (engine), #12 (engine rebuild — byte-identical
bookends), #16 (OVERLAY — see note). All 3 verified first==last frame by eye.

**#16 threefold limitation (known gap):** #16 "The Fire Jesus Built" (John 21) has the
threefold ("Lovest thou me?" x3 / "Feed my sheep" x3) = ~28 tiny spoken windows. The
standard 11-clip jigsaw can't fill that many windows without repeating clips (AS-G2 FAIL)
+ sub-0.8s flashes (AS-G4 FAIL) — the engine correctly REFUSED. So #16 stays hand-assembled
(original preserved as `viral_cut.pre-bookend.bak.mp4`); I gave it the still bookend by
ffmpeg-overlaying the frozen hero #05 onto the first/last 2s (audio untouched). FUTURE FIX:
a repeat-aware / window-aware allocation mode for threefold-structured episodes.
Code: `config.ASSEMBLY_HERO_STILL` (default ON) + `ASSEMBLY_HERO_HEAD/TAIL`=2.0 +
`assembly_ffmpeg.render_still()`/`extract_frame()` + `assembly_render.render_cut()` renders
hero-head/hero-tail as one reused still. Also re-rolled the hero #09 IMAGE earlier (a
finger was malformed) → re-animated + rebuilt. QJA #03 final cut now has the still
bookend (verified first/last frame are the same hero painting). Memory: `feedback-still-bookend`.

**✅ COMPLETE END-TO-END — first full episode produced ENTIRELY in agent-mode (zero
metered API across ALL four stages): text → audio → visuals → clips → assembly.**
Final deliverable: `…\18 He Never Said Yes\v1\assembly\viral_cut.mp4` (59.03s) +
all_takes_reel.mp4 + index.html. Edit plan LOCKED, per-slot Vision verify PASS on all
11 slots (sacred frames clean — the pierced hand #14 and the hero raising-hand #09
both verified correct by my eye). Hero #09 bookends open+close so it lands on Christ.
The user approved all 16 clips at GATE 3 (no exclusions). Assembly: 11 clips, avg
1.54x, sacred capped ≤1.3x. The whole pipeline's LLM work (≈90+ bridge calls across
the session) was serviced in-chat.

Known craft note (assembly POC, carry-over): several per-slot mid-reframe frames land
on a macro/insert (the mat, the pool, the crowd) rather than the establishing subject —
verify still PASS (related, not contradictory) but the cut could sample the establishing
frame per slot for stronger reads. Optional ~9-clip recut for more air (AS-G3 was brisk).

NEXT: produce another QJA episode (05-10) — the full agent-mode pipeline is now proven
on a real end-to-end run. Or polish #03 (recut at --clips 9). Folder `…\18 He Never Said Yes\v1`.

--- earlier (now superseded) ---
**At GATE 2 (images done, clips not yet run).** Visual scene plan LOCKED (16 scenes,
both reviews + cohesion; 1 revise for an SP-G5 banned-token 'frame' I'd left in 3
subject_blocks). All 16 HF images rendered + agent-mode Vision-audited (I looked at
each by eye). Hero #09 "Rise — The Hand of Mercy" (open raising hand). Mix: 12 single
· 4 unified (#3/#4/#12/#13) · 2 NT-link (#9/#14 cross) · 2 OT-echo (#12 Jer 2:13 /
#13 Isa 35:6). **#13 and #15 were rerolled at the user's request** (#13 was a vivid
style outlier → now somber Baroque; #15 read Christ-like → now a clear everyman) via
surgical scene_plan.json subject_block edits + delete-png-and-re-render. The cross
(#14) came back robed (sidesteps Kling NSFW, pierced hand still shown).
NEXT: GATE 2 decision → animate all 16 with direct-Kling (~$10) → GATE 3 (drop glitchy
clips) → assemble. Folder `…\18 He Never Said Yes\v1\visual\hf\` + index.html.

## ════════════════════════════════════════════════════════════════

## ═══════════ SESSION END 2026-05-29 (late) — AGENT-MODE SHIPPED ═══════════

**✅ Agent-mode (`LLM_PROVIDER=agent|api`) is BUILT, wired, and validated.** This
formalizes the user's cost direction: run the engine on the Max subscription
(in-chat) instead of the metered API. Default is now **`agent`**.

How it works: every engine LLM call writes a request file and BLOCKS, polling for
a reply; the in-chat agent reads the request (and, for Vision, Reads the image),
writes the raw reply, the engine continues. **Zero API spend.** See `AGENT_BRIDGE.md`
for the full operating loop.

Coverage (all three confirmed):
- **Text** — `engine._call` (thread/tournament/judge/synthesize/review/independent/
  revise + scene planning + assembly planning). Smoke-tested (PONG).
- **Vision** — `visual_render._vision_call` + `assembly_render._verify_slot_vision`.
- **Kling cut-planner** — `PythonProject1/jesus/image_to_kling.py` Stage A director
  + Stage A.5 audit, via the SAME bridge (imported by `JITB_BRIDGE_PATH`; subprocess
  env stamped by `config.inject_agent_env`). **End-to-end validated**: ran
  `image_to_kling.py --plan-only --force` on the Peter-at-the-fire PNG; I authored
  the 8-beat cut plan from the image, audit passed, `.kling.json` written — no API.

Files: NEW `pipeline/agent_bridge.py` (stdlib-only, shared by both projects) +
`AGENT_BRIDGE.md`. EDITS: `config.py` (LLM_PROVIDER, agent_mode(), inject_agent_env(),
require_api_key() no-ops in agent mode), `pipeline/engine.py`, `pipeline/visual_render.py`,
`pipeline/assembly_render.py`, `pipeline/video_render.py`, `pipeline/visual_handoff.py`,
the 4 CLIs (startup banner), and `PythonProject1/jesus/image_to_kling.py`.

**TO RUN IN AGENT-MODE:** launch the CLI with `run_in_background=true`, watch
`.agent_bridge/requests/`, Write each reply to `.agent_bridge/responses/<id>.txt`.
**For unattended/cron:** set `LLM_PROVIDER=api`. Memory: `agent-mode-bridge`.

**NEXT:** produce a NEW QJA episode (03, 05-10) fully in agent-mode as the first
real full run — measure how the in-chat servicing feels at tournament scale (4
parallel candidate requests at once), then iterate ergonomics (e.g. a batch-serve
helper) if needed.

## ════════════════════════════════════════════════════════════════

## ═══════════ SESSION END 2026-05-29 — READ THIS FIRST ═══════════

**Big picture:** the engine is now a full topic→final-cut pipeline (text tournament →
cut-aware visuals → assembly), with gospel-integrity gates, and it was just run on a
real new episode end-to-end. Everything below ("Where we are" + dated sections) is
prior history; this block is the current truth.

**✅ QJA #04 "Do You Love Me" is FINISHED end-to-end (agent-mode).**
Folder: `PythonProject1\jesus\narration\16 The Fire Jesus Built\v1`
- Narration: tournament-generated (charcoal-fire / `anthrakia` thread), 3-voice
  (narrator/Jesus/Peter — Peter now voiced), carries the 4 elements the user
  required (threefold enacted, restored calling, viewer inner-voice, series signature).
  59.0s MP3. Both text reviews LOCKED.
- Visuals: cut-aware scene plan LOCKED (16 scenes); 16 HF images. #14 (crucifixion)
  and #16 (empty place) were re-rolled with fixed specs + verified by eye.
- Clips: 12 Kling clips (the cut's hero + 11 body) rendered from cut-plans I
  hand-authored from the scene metadata (no fresh planning call).
- **Final cut: `…\16 The Fire Jesus Built\v1\assembly\viral_cut.mp4` (59.02s)** +
  `all_takes_reel.mp4` (120s) + `index.html`. Opens AND closes on the risen Christ
  at the fire; threefold via inserts; cross at "calling you have not earned." Verified
  by eye. Built via my jigsaw + ffmpeg — **zero assembly API**.

**⚠️ API-cap situation:** `JesusInTheBible\.env` and `PythonProject1\.env` use the
SAME Anthropic key (fingerprint 942c2bf7). Earlier today that key threw a usage-cap
error ("regain 2026-06-01"), but it was RESPONDING AGAIN later the same session (cap
likely raised by the user, or transient/rate-limit). **Check the Anthropic console
usage limit before a big run.** The engine now degrades gracefully on a cap
(`visual_render.verify_image` logs+skips+flags instead of crashing).

**💡 Agent-mode (the user's cost direction — IN-CHAT/Max-sub instead of metered API):**
proven manually this session — I (the agent) did the cut-plan authoring + the assembly
jigsaw, engine did Kling+ffmpeg+deterministic. The user wants this as the DEFAULT with
the API as fallback. NOT yet formalized in code (queued: a `LLM_PROVIDER=agent|api` mode).

**FIRST ACTIONS NEXT SESSION:**
1. Watch `…\16 The Fire Jesus Built\v1\assembly\viral_cut.mp4` (+ index.html). It's done.
2. Decide direction: (a) formalize **agent-mode** (`LLM_PROVIDER=agent|api`) so future
   runs use the Max sub by default; (b) produce more QJA episodes (03, 05-10 are
   unstarted; 01+02 already done by the user); (c) polish #04 (e.g. tighten any clip).
3. To re-open the cut or re-cut #04: agent-mode assembly = build EditPlan slots +
   `assembly_render.render_cut` (ffmpeg, no API). Normal mode = `cli_assemble.py "<v1>"`
   (needs API). Clips/images already rendered, so re-cuts are cheap (ffmpeg only).

Tournament + cut-aware planning + gospel gates all validated on a real episode this
session. Memories updated: `feedback-draft-tournament`, `qja-series-production-status`,
`pipeline-orchestrator`, `assembly-stage-design`.

## ════════════════════════════════════════════════════════════════

## Where we are

Visual stage built end-to-end **and tested on the prodigal** during this
session (V1–V8). The text+audio stage from earlier in the day still runs
fine; tonight's work sat on top of `12 The Kiss That Cut Off the Bargain`'s
59.01s three-voice MP3.

Prodigal v1 now has:
- **16-scene locked plan** at `<v1>/visual/scene_plan.json`. Both reviews
  LOCKED, paper cohesion PASS. Mix: 10 hero singles + 6 multi-vignette
  unified (3 Jesus / NT-gospel-link, 2 OT-echo). Each unified scene carries
  4 named vignettes (e.g. scene 11: running father / paternal embrace /
  robe-ring carried out / swallowed bargain).
- **16 Higgsfield PNGs** (`nano_banana_2`) at `<v1>/visual/hf/`, all 16
  passed the widened Claude Vision content audit. Scene 11 had a silent
  miss caught by user review (Jesus standing beside cross, not crucified);
  audit was widened (V5.8) to check `subject_block` + `vignettes`, scene 11
  re-rolled, now correct.
- **Kling MP4s landing in flight** at session end (9/16 confirmed; rest
  rendering via `--kling-skip-audit` background job). Should be all 16 by
  tomorrow morning.

Full detail in `STATE.md`; operating rules in `CLAUDE.md`. New feedback
memories: `feedback-visual-mix-and-jesus-frame`,
`feedback-kling-friendly-scene-plans`, `feedback-kling-skip-audit`.

## First action tomorrow

**DONE (2026-05-29):** All 16 MP4s verified. The overnight job had stalled at
12/16; the 4 missing unified-block scenes (11 cross / 12 hosea-14 / 13 deut-30
/ 14 crumpled-rehearsal) were re-rendered with `--skip-audit` (reused the
existing `.kling.json` cut plans, exit 0 each). First/last-frame extraction
confirms all 16 are genuine animations — scene 11 shows Jesus correctly
crucified, scene 13 has a strong camera push-in. The prodigal visual track is
fully rendered.

**Also DONE (2026-05-29):** index.html v2 with inline `<video>` clips, AND the
full **Stage 4 assembly pipeline** — `cli_assemble.py` builds a 59.01s
`viral_cut.mp4` (kiss bookends start+end for a loop feel) + a 160s
`all_takes_reel.mp4` in `<v1>/assembly/`, with an intelligent clip↔word jigsaw,
deterministic speed/trim allocation, panel + gates + independent audit + Vision
verify + an `upstream_notes.md` feedback file. Validated end-to-end on the
prodigal (both reviews LOCKED). See memory `assembly-stage-design`.

Run it: `.venv\Scripts\python.exe cli_assemble.py "<v1 folder>"`
(add `--plan-only`, `--clips all`, `--no-reel`, `--no-verify`, `--hero NN`,
`--speed-cap X`, `--rebuild`, `--replan`). Review page: `<v1>/assembly/index.html`.

**Also DONE (2026-05-29):** the **seamless pipeline (Part 1 of 3)** —
`cli_pipeline.py` chains topic→narration→images→clips→cut with THREE human quality
gates (you approve audio, images, clips). Excluding a clip is the curation lever
(`--exclude` at the image gate also skips paying Kling for bad images). Cost
model: ~$23/episode (Kling ~48%, images ~22%, Opus ~25%). See memory
`pipeline-orchestrator`.

Run a new episode end-to-end:
```
.venv\Scripts\python.exe cli_pipeline.py                          # pick topic; runs text+audio; stops at GATE 1
.venv\Scripts\python.exe cli_pipeline.py "<v1>" --continue        # → images; stops at GATE 2 (review, confirm hero)
.venv\Scripts\python.exe cli_pipeline.py "<v1>" --continue        # → clips; stops at GATE 3
.venv\Scripts\python.exe cli_pipeline.py "<v1>" --exclude 3,10 --continue   # → final cut, minus bad clips
```

**Also DONE (2026-05-29): red-team hardening.** Ran a 3-agent independent red team
over everything; fixed the real findings. Biggest: the cut used to CLOSE on the
emotional kiss — now the **hero is the gospel-pivot (the cross), bookending open +
close, so it lands on Christ** (verified: prodigal opens+closes on the crucifixion).
Plus: deterministic gospel-frame-survival gate, **reverence speed cap (1.3x) on
sacred clips**, doctrinal verify now Opus-on-sacred + fail-closed + BLOCKING,
de-hardcoded prompts, and generalization fixes (budget enforced, key/index
validation, negative-window clamp, timeline pinned to narration.mp3). See memory
`assembly-stage-design` (red-team section) + `pipeline-orchestrator`.

**Also DONE (2026-05-29): HF Kling bake-off + hybrid video provider.**
- Bake-off: HF `kling3_0` makes good frozen-tableau motion from a SIMPLE motion-only
  prompt (the 8-beat .kling.json is NOT needed); integer `duration` (variable length
  is real); ~6.25 credits / 5s std clip (NOT cheaper than direct-Kling); **HF NSFW
  filter blocks the crucifixion platform-wide** (Kling + Seedance).
- Decision: **HYBRID** — HF for clothed clips, auto-fallback to direct-Kling for the
  NSFW-blocked cross. Built `pipeline/video_render.py` (VIDEO_PROVIDER=hybrid default),
  wired into orchestrator SEG C; validated (HF path, NSFW fallback on the cross,
  idempotent skip). See memory `assembly-stage-design` / `pipeline-orchestrator`.

**Also DONE (2026-05-29): video decision + Part 2 cut-aware planning.**
- Video: after a fair bake-off (HF even with the rich cut-plan prompt looked worse
  than direct-Kling, isn't cheaper, blocks the cross), **direct-Kling is the default**
  (`VIDEO_PROVIDER=kling`); HF/hybrid code parked but available.
- **Part 2 shipped**: the visual planner is now timeline-aware — `discover_scenes`
  (+ review/revise) takes the narration timeline, nominates a gospel-pivot
  `hero_candidate` (the cross) that bookends the cut, and creates ~2s `shot_kind:insert`
  shots for sub-2.6s beats; "design for the cut" rules folded into the constitution;
  `cli_visual --replan` added; assembler reads `hero_candidate` as the hero. Validated
  on a temp re-plan (hero=cross, 2 inserts, both reviews LOCKED, mix intact).

**Also DONE (2026-05-29): draft tournament + named-disciple voices.** User found
single-draft output "over-used / CTA formulaic" → built a DRAFT TOURNAMENT (now the
default): 4 divergent candidates → judge the hook→CTA arc → synthesize winner + graft
best hook/CTA; de-templated CTA. Validated on QJA Ep04 (fresh charcoal-fire arc, CTA
"will you follow Him again?" grafted from another candidate). Named NT speakers
(peter/john/…) now map to the dialogue voice. See memory `feedback-draft-tournament`.
The seeded #04 ("14 The Charcoal Fire") is the OLD single-draft version — regenerate
it via the tournament to get the fresher script + Peter voiced.

**⛔ PARKED — Anthropic API usage cap hit 2026-05-29 (regains 2026-06-01 00:00 UTC,
or raise it in the Anthropic console).** QJA #04 ("16 The Fire Jesus Built") is at
GATE 2 with a COMPLETE 16-image pool: cut-aware plan LOCKED; hero #05 = risen Christ
at the fire; threefold via inserts #06-#11; calling via #12 Ezekiel-34 / #13 Isaiah-40
/ #15 follow-me; #14 (crucifixion) + #16 (empty place by the fire) were re-rolled with
fixed specs and VERIFIED BY EYE (their engine Vision-audits were skipped under the cap
— flagged in their sidecars). The cap blocks the next steps (Kling clips' cut-planner
= Vision; assembly = Opus). RESUME when unblocked:
`cli_pipeline.py "…\16 The Fire Jesus Built\v1" --continue` → clips (GATE 3) → assemble.
(Engine now degrades gracefully on a usage cap instead of crashing — `verify_image`
logs + skips + flags for review.)

**Next (when API is back):**
1. **Finish QJA #04** (clips + assembly) via the --continue above, then
   **run a NEW episode end-to-end through `cli_pipeline.py`** (the first real full
   run) — text→audio→gate→cut-aware plan→images→gate→direct-Kling clips→gate→assemble.
   Measure real cost (instrument token/credit usage — the ~$23 estimate was optimistic;
   Opus Vision audits scale with the deep pool).
2. **Part 3** — parallel batch (3-5 theme-clustered, gates SERIAL per-episode) +
   clip-reuse library (thread-neutral plates only; no Jesus/variant reuse).
3. Optional: re-plan the prodigal with `cli_visual --replan` to give it hero_candidate +
   inserts (note: regenerates the plan; would need image re-render for new/changed scenes).

To re-verify the MP4 count any time:
```
ls "C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\12 The Kiss That Cut Off the Bargain\v1\visual\hf\*.mp4"   # expect 16
```
To re-render any single missing/bad scene (idempotent — skips ones with both
.kling.json + .mp4; set KLING_SKILL_PATH first):
```
$env:KLING_SKILL_PATH="C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\adhoc\SKILL_locked.md"
C:\Users\sanjay\PycharmProjects\PythonProject1\.venv\Scripts\python.exe `
  C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\image_to_kling.py `
  "<path-to-NN_scene.png>" --skip-audit
```

## Then (queued)

1. ~~**Build index.html v2 with `<video>` tags**~~ ✅ DONE 2026-05-29.
   `write_review_index_html` (in `pipeline/visual_handoff.py`) now embeds each
   `<stem>.mp4` as an inline looping/muted `<video>` (PNG poster, controls,
   "▶ clip" badge), falling back to `<img>`+"still only" when no MP4. Re-runs
   of Phase B regenerate it automatically; to rebuild by hand call
   `write_review_index_html(v1_folder, 'hf')`. The prodigal page shows all 16
   clips inline.
2. **Minimal final assembly step.** 16 × 10s clips + the 59.01s MP3 needs
   to become a delivered video. Either (a) concat all 16 into a 160s "all
   takes" reel for review, or (b) build a 60s viral cut using `short_priority`
   ordering aligned with the narration timestamps. Likely path: small new
   `cli_assemble.py` that uses ffmpeg.
3. **`rendered_cohesion` audit (V7 was never built).** Cheap one-Vision-call
   pass over a 4×3 contact sheet of all 16 PNGs against `narration.md`.
   Catches set-level drift (Jesus face inconsistency between scenes 8 and
   11, palette drift, lighting). Advisory; produces a re-roll list.

## Text-stage opens carried over (lower priority right now)

- **Multi-voice word budget** (STATE.md #1) — run #12 hit narrator atempo
  1.419× because the script was 180 words with 2 character quotes. Probably
  lower `TARGET_WORDS_MAX` to 145–150 globally, or add an Editor-agent hard
  cap of 140 narrator words on multi-voice shorts.
- **Female voice** (STATE.md #2) — `VOICE_MAP` still has no female voice_id.
  Needs a voice_id from the user; biggest near-term lever for the Encounters
  series.

## How to run

```
cd C:\Users\sanjay\PycharmProjects\JesusInTheBible

# text + audio
.venv\Scripts\python.exe cli.py
.venv\Scripts\python.exe cli.py --no-audio

# visual
.venv\Scripts\python.exe cli_visual.py "<v1 folder>"                            # full pipeline
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --plan-only                # paper plan only
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --no-animate               # plan + render, no Kling
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --provider hf              # Higgsfield (default)
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --provider nbp             # Nano Banana Pro
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --no-short-only            # render all scenes
.venv\Scripts\python.exe cli_visual.py "<v1 folder>" --kling-skip-audit         # bypass nit-picky Stage A.5
```

## Quick review

Listen to the prodigal audio:
```
start "" "C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\12 The Kiss That Cut Off the Bargain\v1\narration.mp3"
```

Browse the visual review page:
```
start "" "C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\12 The Kiss That Cut Off the Bargain\v1\visual\hf\index.html"
```

## Don't forget

- **Independent red-team review of every outcome** is standard practice at
  every stage (text plan, scene plan, image, eventually animation).
- **Look at images / clips yourself with the `Read` tool** when reviewing —
  don't trust the SDK audit's pass/fail signal blindly. The narrow audit
  silently passed a wrong scene 11 in this session; widening it required
  user catching it visually.
- **Grace-anchored only** — no gain/loss, no fear, no manufactured pressure.
- **KJV verbatim**; freshness = faithful depth, never new doctrine.
- **One thread runs through hook → middle → CTA in script AND opening →
  climax → closing in visuals.** Never swap threads to placate freshness
  feedback — reshape the lines / scenes instead.
- **`--kling-skip-audit`** is the documented escape hatch when Stage A.5
  goes nit-pick mode on Baroque content. Use it; the Kling renders are fine.
- **Reuse downstream pipelines, never duplicate** — `narration_pipeline.py`,
  `per_turn_synth.py`, `image_to_kling.py` are subprocess'd.
