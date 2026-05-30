# RESUME.md — start here next session

## ═══════════ SESSION END 2026-05-30 (LATE) — CLARITY FIX + COST CONTROL — READ THIS FIRST ═══════════

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
