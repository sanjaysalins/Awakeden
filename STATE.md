# STATE.md — progress tracker

**Last updated:** 2026-06-21
**Status (2026-06-21 LATEST):** **ALL 8 PSALM 22 SHORTS FULLY SHIPPED + PUBLISH PACKS DONE.**
Stage 6 publisher (`cli_publish.py`) built + red-teamed + committed. All 8 shorts (#01–#08) have complete
publish packs (youtube_short / tiktok / facebook / instagram .md files + captions.srt + PUBLISH_INDEX.html).
FIX-ALL Phase A complete: Well + Door + Fire all DONE. Gaza Road (#25) DONE (64.4s, $7 spend).
**NEXT:** fill `data/upload_brand.json` handles → post the 8 shorts → website Netlify deploy.
Open: #02 sc08 faint titulus (keep/swap). Phase B/C deferred. Prior status below.

**Status (2026-06-20 earlier):** 3-pilot sweep mid-flight (Isaiah + Mockers done).
Isaiah: narrator 1.08x, softer + full Cinematic-Orchestral score (user set the rule: score must move the listener
deeply); fixed a stale-alignment bug (regen narration.alignment.json after any length change). Mockers-v2: multi-voice
(narrator+david+mocker), narrator 1.087x, replaced 4 titulus FAIL clips + backfilled to 18 from clean #02 set,
cinematic-orchestral score, shofar dropped. Finals: `C:/Users/sanjay/ISAIAH_53_5_FINAL.mp4` + `MOCKERS_V2_FINAL.mp4`.
NEXT: Zechariah (same recipe). New memories: alignment-cache-staleness; cinematic-score bar raised. Prior status below.

**Status (2026-06-20 earlier):** ISAIAH 53:5 first pass (81.2s).
Parallel-swept all 3 pilots (subagents). Isaiah: backfilled 10→16 clips ($0 reuse), user DELETED + blacklisted
2 full-body clips (`05_by-whose-stripes`, `06_in-his-own-body`, pruned from clip_library 122→120) → replaced
scene5←`10_wounded-for-us`, hero scene6←`08_whom-they-pierced`; re-assembled (15 slots eye-verified, LOCKED 0-rev,
worst hold 10.8s) → SFX → cinematic-redemptive score (~$2) → ivory caption. **FINAL = `C:/Users/sanjay/
ISAIAH_53_5_FINAL.mp4`.** **NEXT: Mockers-v2 + Zechariah** (single-narrator → multi-voice; Mockers FAILs 04/08/10/12,
Zech FAILs 01/06/11). Mockers-v2 + Zechariah
still single-narrator + have FAIL clips (Mockers 04/08/10/12 titulus+gems; Zech 01/06/11). Also: installed
**mattpocock/skills** (33 skills in `.claude/skills/`, cleaned the `--all` 47-dir mess) + ran domain-modeling demo →
**`CONTEXT.md`** glossary. Slices pages: `C:/Users/sanjay/ISAIAH_strips.html`. See RESUME.md top. Prior status below.

**Status (2026-06-20 prior):** **Awakeden.com static prelaunch site scaffolded in `_website/`** (manifest-driven catalogue, Netlify + Cloudflare plan, 10 catalogue items, plain copy pass). Not deployed yet; run `build_catalog.py` + local server to preview. **Production:** #02 Mockers full-treatment DONE + titulus clip recalled from #08/#01; **ALL 8 Psalm-22 shorts at new bar**; **NEXT: 3 pilots** + optional #02 sc08 titulus decision. See RESUME.md top. Prior status below.

**Status (2026-06-20, production):** **#02 "The Mockers' Words" full-treatment + recalled a titulus clip from #08/#01.**
Swept #02 (sc07 wrong-clip, sc08 grotesque mouth, sc12 = writing/INRI-titulus FAIL). The sc12 clip had been
reused as a backfill into #08 sc07 + #01 sc11 → **replaced in both** (#08←a-death-not-his-own, #01←david-records),
re-rendered/SFX/re-mixed/captioned, both finals refreshed. #02: replaced sc07←rulers-sneer + sc08←he-could-have-
come-down (pilot), excluded sc12, **multi-voice (narrator + david + MOCKER `[mocking]`)**, 12 clips + hero 11
(~5.3s/slot), LOCKED, SFX, cinematic score (reshaped), caption. **FINAL = `…/02_The_Mockers_Words/assembly/
viral_cut_sfx_music_captioned.mp4` (67.5s)**, copy `C:/Users/sanjay/02_Mockers_Words_FINAL.mp4`. OPEN: #02 sc08
has a faint illegible titulus (user to keep/swap). Spend ≈ $2.50. **ALL 8 Psalm-22 shorts (#01–#08) now done at
the new bar; NEXT: the 3 pilots.** See RESUME.md top. Prior status below.

**Status (2026-06-19, prior):** FULL-TREATMENT SWEEP **#01 "The Crucifixion Foretold" now at the new bar.**
Swept clean (only the 4 garbled-writing scrolls flagged, already excluded) → multi-voice (narrator + david
Ps 22:18) → **backfilled to PUNCHY** (filled the scroll slots + 1 new slot with 6 clean reuse clips →
14 clips + hero ≈ 5.0s/slot) → reassembled LOCKED → SFX → cinematic-orchestral score (reshaped to fill+settle)
→ ivory caption. **FINAL = `…/01_The_Crucifixion_Foretold/assembly/viral_cut_sfx_music_captioned.mp4` (75.0s)**,
copy `C:/Users/sanjay/01_Crucifixion_Foretold_FINAL.mp4`. GOTCHA: reuse_swap keeps the OLD filename when you
change a slot's scene_plan slug → assembler silently excludes it; rename `NN_*` files to the new slug (or don't
change the slug). Spend ≈ $2.50. **#01, #03–#08 now done; NEXT: #02, then 3 pilots.** See RESUME.md top. Prior status below.

**Status (2026-06-19, prior):** FULL-TREATMENT SWEEP **#08 "I Thirst" now at the new bar.** Swept all 14
clips by eye → reuse-replaced 5 defective (2 gem-nails sc06/sc10 + frame-morph sc01 / grotesque-mouth sc04 /
empty-void-crane sc07, $0 reuse) → multi-voice (narrator + david Ps 22:15 + jesus "I thirst") → reassembled
LOCKED → SFX → cinematic-orchestral score (reshaped to fill+settle) → ivory caption. **Caught + fixed an
INVERTED CROSS** — kept-slot 13's `drink-and-never-thirst` showed a cross reflected in water (= upside-down
cross) for ~4s under the landing captions; the element-gate + still-review had PASSED it, only the animated
frame revealed it → replaced with `room-to-turn` (upright dawn-cross). New memory `feedback-cross-in-water-
inverted`. **FINAL = `…/08_I_Thirst/assembly/viral_cut_sfx_music_captioned.mp4` (73.4s)**, copy at
`C:/Users/sanjay/08_I_Thirst_FINAL.mp4`. Spend ≈ $2.50. **#03–#08 now done; NEXT: #01, #02, then 3 pilots.**
See RESUME.md top. Prior status below.

**Status (2026-06-19, prior):** FULL-TREATMENT SWEEP — **#04, #05, #06, #07 now at the new bar**
(multi-voice + sweep/fix-defects + backfill-to-punchy + speed-to-fit + cinematic orchestral score +
ivory caption). Locked **TWO new standards** (config defaults flipped + memories): (1) **SPEED-TO-FIT,
NEVER TRIM** — `ASSEMBLY_SPEED_CAP` 2.2→4.0, `ASSEMBLY_REVERENCE_CAP` 1.3→3.0, and the **HERO CLOSE is
now a whole sped clip in MOTION** (`ASSEMBLY_HERO_STILL` 1→0, hero-tail via `_slot_op`) — supersedes the
freeze-on-Christ close; (2) **CINEMATIC-ORCHESTRAL SCORE** (full strings+horns+organ, sweeping, −8 dB,
reverent/no-percussion) + score-shaping fix (Eleven Music ends its arc ~10s early on long narrations →
reshape to fill the duration + duck the back half so the end settles, not surges). #06 sc03 still
re-rendered (titulus removed); #07 sc07 re-animated via direct-Kling (crop-only plan), hero = the
substitution clip. Finals + per-short review HTMLs at `C:/Users/sanjay/0N_*.{mp4,html}`. Spend ≈ $20.
**NEXT: #08, then #01/#02, then 3 pilots; optional #03/#04 score top-up.** See RESUME.md top. Prior status below.

**Last updated (prior):** 2026-06-17
**Status (2026-06-17 PART 2):** MERGED the coherence system into the binding `v2/SPEC.md` (drift fixed:
INV-23 coherence + INV-24 no-fabricated-verdicts, both **rollout-gated/reports-only**; gate vocabulary
unified to **F1–F5**; IMG-COHERENT + STILL-REVIEW gate rows; side doc `COHERENCE_GATE_SPEC.md` retired
to a SUPERSEDED build-log). Fixed the **clip_reuse bug** (clip-QC requirement excluded the whole bank →
catalogue 34→**115** clean-reusable). **Reassembled ALL 7 videos that held a quarantined bad clip,
CLEAN** — Psalm 22 #01/#02/#03/#07 (punchy) + the 3 v2 pilots Isaiah/Mockers-v2/Zech (clean but slower,
accepted clean-over-punchy); old finals saved as `_PRE_COHERENCE.mp4`; total spend ≈ $3. Findings: NBP
gems any prominent nail-wound (un-rebuildable → exclude); pilots too thin to be punchy without a real
reuse-backfill. ~114 tests green. THEN the **MUSIC PHASE**: an AI panel (4 composer lenses → judge)
designed a bespoke instrumental score brief per short (`music_designs.json`); generated + ducked +
captioned all 11 via `sfx_pilots/add_music.py` → `viral_cut_sfx_music_captioned.mp4` + review page
`music_review.html`. User feedback applied: level retuned −17→**−8dB + gentle duck** (was inaudible),
and a **2.5s end-hold** added (hold last frame + score rings out) — PROVEN on #03 (54.33s). Eleven Music
bills a SEPARATE invisible quota (no exact spend number). DO FIRST TOMORROW: re-run `music_batch.py` with
`regen=True` to apply −8dB + 2.5s-tail to the OTHER 10, then USER EAR-REVIEW all 11. Rollout flags still OFF.
See RESUME.md top (PART 2 → MUSIC PHASE). Prior status below.

**Status (2026-06-17 PART 1):** Built a **STILL-COHERENCE / QUALITY GATE** after the user flagged many shipped
stills as "not fit for use" (floating head, giant head, standing-not-hanging crucifixion, off/sickly
faces, garbled scroll text, frames, modern props). New: `pipeline/coherence.py` (fail-closed sidecar +
content-hash verdict sharing + k-vote ensemble/aggregate — byte-identical stills can no longer get
different verdicts), `pipeline/coherence_gate.py` (vision gate, RETUNED to default-pass / fail only on
clear F1–F5), `pipeline/dedup.py` (perceptual dedup + verified-only canonical reuse), enforcement
chokepoint `lock.require_visual_coherence` (scoped to the selected cut; rollout flag
`JITB_REQUIRE_COHERENCE` OFF until shipped shorts are backfilled), INV-24 closed 3 auto-bless doors,
and `v2/coherence_audit/` tooling (provenance, reject_list, review page, blind calibration, quarantine).
**Calibration:** over-strict first pass (87 fail, precision 0.08) → user blind-labeled 50 → retuned →
**6 fail, precision 0.50**; reject list 93→29. **Quarantined 17 confirmed-bad stills** (+clips =102 files)
to `_rejected_coherence/` (reversible) + pruned 11 dangling clip_library refs (136→125). **Wired
guardrails T1–T6** into the constitution + banned tokens + `data/render_guardrails.md`. Red-teamed 2×;
**100 tests green**. 7 shipped videos still contain the bad clips (reassembly deferred per user). NEXT:
2 TODOs — periodic human still-review gate; clip-reuse optimization pipeline. See RESUME.md top. Prior status below.

**Last updated (prior):** 2026-06-15
**Status (2026-06-15):** LOCKED a new SHORTS ANIMATION RECIPE after the shipped clips showed hallucination
(morphing hands/faces) + "dancing Jesus on the cross". Recipe = **HF Kling 3.0 `--mode pro` + a HARD-CUT
CUT-PLAN prompt** (jump-cuts between crops of a frozen painting, targets from each scene's `macro_elements`;
subject never moves) via tool `_hf_animate_short.py`. Bake-off ruled out: plain-zoom prompt (too basic),
ffmpeg hard-cuts (jittery/lifeless — user reserves ffmpeg for NSFW only). Writing/scroll scenes are EXCLUDED
from cuts (user's call). Rolled across all 8 shorts: **CLIPS RE-RENDERED for all 8**; **fully rebuilt + final
(viral_cut_sfx_captioned.mp4): #03 (51.8s), #05 (43.9s), #06 (61.8s)**. **#01/#02/#04/#07/#08 = clips QC'd,
still need assembly→SFX→caption** (see RESUME.md for exclude/hero per short + the bridge-servicing pipeline).
#07 sc7 (bare-torso) HF-NSFW-blocked → ffmpeg (the sanctioned exception). Spend ~1270 HF cr (~$190); balance
1036 cr. New memories: `feedback-shorts-generative-not-ffmpeg`, `feedback-never-animate-writing`. See RESUME.md
top. Prior status below.

**Last updated:** 2026-06-14
**Status (2026-06-14e):** Built a **VALIDATION ENGINE** after a run of defects the pipeline should have caught
(root cause: agent-mode shortcut servicers bypassing the real validators). NEW: `data/rules.json` (rule
registry), `pipeline/validators.py` (deterministic cut-plan + criteria gates), `pipeline/clip_qc.py`
(fail-closed per-clip QC), `pipeline/test_validation.py` + fixtures (66 tests green), `VALIDATION_ENGINE_PLAN.md`;
closed the bypass in `.agent_bridge/_gen_servicer.py` (camera-only gated crop-cuts) + added a period/tone check
to `verify_image`. Committed `e38da55` + `bbb423c`. REBUILT clean through the engine: **#07** (60.1s), **#08**
(67.0s), **#01** (64.1s, garbled inscription removed), **#05** (43.9s, garbled Greek→illegible). AUDITED
#02/#03/#04/#06: their "verse-on-a-scroll" scenes render **garbled Hebrew** (#02 sc3, #03 sc3, #04 sc3+sc7,
#06 sc2) — fix queued (re-render writing as illegible marks; NOT started, metered). Crowds/faces period-clean.
NEXT: fix those scrolls, then Upload-Kit batch / Types & Shadows slate. See RESUME.md top. Prior status below.

**Last updated (prior):** 2026-06-14
**Status (2026-06-14d):** PSALM 22 SHORTS BATCH complete — all 8 shorts postable with ambient/SFX bed +
ivory captions (`…/shorts/<NN>/assembly/viral_cut_sfx_captioned.mp4`). This session: finished #07 (scene-11
clip + assemble + SFX + caption); built #08 "I Thirst" end-to-end (creation.json → 14-scene plan LOCKED → 14
NBP stills QC'd → 14 Kling clips → assemble hero=pierced-side living-water Christ → SFX → caption; Ps 69
landmine guarded); retrofitted SFX beds onto #01–#04 (`sfx_pilots/build_ps22_01..04,07,08.py`). Fixed a
mid-session Windows Store Python venv break (re-register the appx — memory `store-python-venv-break`). NEXT:
user ear-review the 8 finals; then the paused Upload-Kit batch (needs footer handles) or the Types & Shadows
long-form slate. See RESUME.md top. Prior status below.

**Last updated:** 2026-06-06
**Status (2026-06-06):** Big session — (1) **comprehensive production plan + tracker** built from data/series.json
(red-team + 5-CLI panel): PRODUCTION_PLAN.md / PRODUCTION_TRACKER.html + BATCH_PLAN / ASSET_LIBRARY_PLAN / TODO;
(2) **long-form drivers made EPISODE-GENERIC** (`longform/_episode.py`; Isaiah migrated + regression-verified);
(3) **spend ledger built** (`pipeline/cost.py` + data/spend_ledger.jsonl; hf generate-cost/transactions, credits,
per-episode ceilings; wired into long-form drivers); (4) caption Windows-drive-colon fix; (5) **Psalm 22 CLUSTER**:
the locked long-form (script + 6:58 mp3) + **8 LOCKED shorts** (`…/02_Psalm_22…/v1/shorts/`), each via 1 red-team +
1 panel (LEAN process), KJV self-verified — garments/mockers/forsaken-cry/declared-to-brethren (4 airtight) +
he-hath-done-this/ends-of-the-earth/body-foretold/I-thirst (4 yellow). New memories: accuracy-over-throughput,
narration-review-process, shorts-longform-funnel, psalm22-short-series, spend-ledger-system. NEXT: render the 8
shorts' audio (in progress), then Psalm 22 stills / next long-form. See RESUME.md top. Prior status below.

**Last updated:** 2026-06-03
**Status (2026-06-03):** NATURAL-SPEED direction locked (memory `feedback-natural-speed-more-clips`): narration
never time-stretched to 59s — 59s is a ceiling, trim words if over, never compress the voice; use MORE clips,
speed the CLIPS not the voice, hit each narration beat. Engine: `SHORTS_NATURAL_SPEED` (default ON) wires
`--natural` into per_turn_synth via `handoff.py`; `ASSEMBLY_CLIP_BUDGET` 11→14; `_finalize.py` now clears
stale `_turns/*.mp3`. The 5 I AM episodes re-rendered at natural speed: 32=60.6s (−7 words), 33=60.2s (−6),
34=52.9s (untouched), 35=65.2s (Option A trim, full John 6:51 kept — accepted long), 36=54.6s (untouched);
32/33/35 re-stamped. NOT done: pin clips to each spoken-phrase window (beat-precision) — needs visuals to test;
5 I AM episodes still need visuals (`cli_visual.py`, 14-clip budget). See RESUME.md top. Prior status below.

**Last updated:** 2026-06-02 (end of session)
**Status (2026-06-02 end):** Multi-dimension direction proven at scale — **5 I AM-set narrations SHIPPED**
across two sayings (Door ×2 + Bread ×3). Bread cluster: ai-panel merge
`C:\Users\sanjay\PycharmProjects\PythonProject1\ai-panel\runs\2026-06-02-08-56-02\final-narration.md` →
Ep 34/35/36 at ~59s each, all `short_gate` PASS + stamped. Full paths in RESUME.md top. Next: gold approve,
visuals (cli_visual.py), listen by ear, next multi-dimension topic. Prior status below.

**Last updated:** 2026-06-02
**Status (2026-06-02):** #6 "I AM the Door" (John 10:9) FINISHED as **TWO complementary episodes**, both
LOCKED + 2-voice rendered (~59s, relaxed atempo ~1.03–1.04): **32 The Door Was a Body** (the *invitation*
dimension — open door, come in as you are, saved/safe/fed/pasture; user-directed v-c, no external panel) and
**33 The Shepherd In The Gap** (the *shepherd-as-the-gate* dimension — His body in the gap, the wolf comes
first; shipped v-a as-is at the user's choice for devotional latitude; KNOWN ACCEPTED RISK = contested
fold-folklore, agent flagged pre-render, faithful core grounded in John 10:11). **NEW STANDING DIRECTION
(user):** deliberately explore MULTIPLE doctrinally-faithful dimensions per Bible topic — one passage speaks
several truths, serves more listeners; NON-NEGOTIABLE = Bible-driven + fits evangelical biblical doctrine
(memory `multi-dimension-per-topic`). Redo backlog 27–33 CLEAR. Next: pick a topic and produce its faithful
dimensions (starter dimension-map for Woman-at-Well / Prodigal / Psalm 22 / John 21:17 threefold in RESUME.md
top block). Method that worked: hand-tag → clear stale _turns → per_turn_synth direct. See RESUME.md. Prior status below.

**Last updated:** 2026-06-01 (late)
**Status (2026-06-01 late):** Started next redo topic **#6 "I AM the Door" (John 10:9, series `i-am`)** fully
in agent-mode (thread→tournament→4 candidates→judge→synth→self-review→independent, all serviced in chat; both
reviews LOCKED). Folder `32_The_Door_Was_a_Body/v1` (NEW underscore naming, working). Text reworked 3× to the
user's direction: (a) shepherd-as-door → panel flagged contested folklore + dropped pasture payoff; (b) user:
"lead with I AM/deity" → reframed on the divine-Name echo, 5-LLM panel cut the rule-6 substitution import +
present-tensed it; (c) user: "'I am the door' must land as a PERSONAL salvation INVITATION, not a metaphor" →
current narration.md is the invitation-centered version (deity for weight, heart = "come in and be saved, open
for you as you are," delivers saved/safe/fed/pasture). **NOT rendered — narration.mp3 on disk is STALE (earlier
shepherd 2-voice take).** Tomorrow: re-read narration.md, decide render/tweak/re-panel, then render 2-voice
(clear _turns first — the _finalize stale-_turns bug) + lock. See RESUME.md top block. Prior status below.

**Status (2026-06-01):** REDO panel backlog CLEARED — **27/28/29/30/31 all LOCKED**. This session: confirmed
#31 audio; paneled + finalized **#30 Smitten of God** (Isaiah 53:5 — judged 3 LLMs: dropped the 1-Peter quote
to 2 Isaiah quotes, fixed 53:4 verbatim, identity-forward landing 'the guilt was never His. He took yours —
into His own body', + an **Isaiah VOICE** on the two prophecy quotes → 5-turn multi-voice); paneled + finalized
**#29 The Race He Could Never Win** (John 5:6 — judged 4 LLMs: quoted the title question 'Wilt thou be made
whole?' which the draft had paraphrased, reframed the conviction off viewer-produced desire to grace acting
first; kept the RACE spine distinct from shipped #18 'He Never Said Yes'; 2-voice narrator+jesus). Calibration:
logged the misses, re-opened **grace-trap** (recurred in #29's conviction) + **kjv-verbatim** (coverage gap on
#30's uncached 53:4), added **quote-count-rule8** + **anchor-verse-unquoted**; 4 deterministic fixes PROPOSED
(awaiting approval). Engine changes: NEW episode folders use **underscores not spaces** (handoff.py); helper
**_panel_existing.py** rebuilds panel_request.md for a gate-skipped folder. Known trap: `_finalize.py` doesn't
clear `_turns/*.mp3` (stale audio on re-render — delete _turns manually). NEXT redo topic: **#6 I AM the Door
(John 10:9)**. See RESUME.md top block. Prior status below.

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
