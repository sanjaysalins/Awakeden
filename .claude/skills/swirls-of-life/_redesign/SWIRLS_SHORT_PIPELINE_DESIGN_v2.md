# Swirls of Life SHORT — repeatable pipeline + skill (DESIGN v2)

Written 2026-11-15 by the Fable design seat. Design only. No code, no paid call, no file edited.
Replaces v1 (`SWIRLS_SHORT_PIPELINE_DESIGN.md`). This file stands alone.

`POC   = F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test`
`SKILL = F:\slk\PycharmProjects\JesusInTheBible\.claude\skills\swirls-of-life`
`REPO  = F:\slk\PycharmProjects\JesusInTheBible`

**Panel status (honest):** v1 got REVISE from 4 seats (blind Fable, claude, cursor, gemini).
codex and grok timed out twice (`_independent_review\20261115-175421\` and `\20261115-180226\`).
That is a degraded panel. v2 must go back through `independent_review.py --type plan` with a
full quorum before anything is built.

---

## 0. What changed from v1

| # | Finding (who) | Checked in code? | Change in v2 |
|---|---|---|---|
| 1 | Landing hold is a frozen frame (Fable, orchestrator) | Yes. `swirls_assemble.py:339` `-shortest` + `pipeline\score_mix.py:46` `tpad=stop_mode=clone` | Trim mode drops `-shortest`; the back clip runs to the end; a freeze check on the last 3.5 s. `score_mix.py` not touched. Section 4.1 |
| 2 | Over-built before a pilot (all 4) | Yes. Runner has 5 commands today | Build = 1 new module + 4 small commands. No edits to `swirls_page.py` / `swirls_cover.py`. Rest deferred. Section 4 |
| 3 | SWS-G12 pixel heuristics (Fable, gemini, claude) | Yes. Panels are teal + gold by template (`swirls_page.py:84-89`) | Cut. Kept: first/last used frame + a freeze check, both warn-only |
| 4 | Exact text match will over-fail (gemini) | Agreed | Fuzzy match. FAIL only on missing / invented / doubled text. Near-miss = WARN + human 2x zoom |
| 5 | Spend guard must fail closed (Fable, cursor, claude) | Yes. `resp.get('credits_spent', '?')` (`swirls_page.py:392`) | Price counted BEFORE the request from known rates. Missing credit count = stop. Cap from worst case. Section 3 |
| 6 | $0 pace test first (Fable, claude) | ep10 + ep13 clips exist, 5-10 s, 1072x1928 | Step zero, fully specified. Section 1 |
| 7 | Voice step facts wrong (claude, Fable) | Yes. Real path `PythonProject1\jesus\narration\per_turn_synth.py`; `--target` required; one global `--stability`; all lines on `eleven_v3`; no alignment output | Step 2 rewritten. Alignment = `pipeline.assembly_align.align()`. Length estimate moved into step 1 |
| 8 | One test clip + a clip owner gate (cursor, Fable) | Agreed | Step 6a (one clip, owner yes) then 6b (batch). Draft film is the second look |
| 9a | 5 validators, not 3 | Yes (2 in `POC`, 3 in `POC\test_the_cross`) | All 5 named in section 4.4 |
| 9b | Kling pro = 1072x1928 | Yes (ffprobe, ep10 + ep13) | Plain scale to 1080x1920 (about 1% squeeze, no crop). SWS-G11: at least 1072 x 1900 |
| 9c | `CoverSpec.clip_duration` defaults to 4 | Yes (`swirls_cover.py:123`) | Every spec sets it; `plan` FAILS if spec and `unit_timing.json` differ |
| 9d | Corner note always written | Yes (`swirls_page.py:210-213`) | Corner note is REQUIRED in v1 (no code change). Dropped only if the pace test says so |
| 9e | Locked text says "speech bubble" + caps | Yes (`swirls_page.py:103-116`) | Stated openly: locked still text is exempt from the lint (9 episodes of evidence). Lint covers authored fields only |
| 9f | `units.json` vs alignment word count | ep13 used a hard `assert` | Three-way count check, fail closed. Step 3 |
| 9g | SWS-G7 runs before refs exist | Yes | Split: G7a (declared, at plan) and G7b (files exist, before stills) |
| 9h | Publish anchor read from `_DESIGN_BRIEF.md` line 1 | Yes (`pipeline\upload_engine.py:168-201`) | Episode keeps a one-line `_DESIGN_BRIEF.md` with the exact verse range |
| 9i | Thumbnail = front cover breaks the movie-poster rule | Yes (memory `feedback_movie_poster_thumbnails.md`) | Thumbnail goes through the blind key-art panel + 2-model bake-off. Own paid ask |
| 9j | `independent_review.py --type narration` missing | Yes (project CLAUDE.md) | Added to step 1, before the owner page |
| 9k | Bridge needs an attended session | Yes (`openart_bridge.py` blocks and polls) | Stated as prerequisite P1. This is an attended pipeline |
| + | Speaker-holds pages may look dead (claude, cursor, Fable) | — | Counted in the pace test and gated in the page plan (SWS-G8) |
| + | 30 s / 60 s sizes, felt piano "is the identity", 2-part score bend | — | 45 s only. Score docs not re-labelled. No bend needed |

### Rejected findings

| Finding | Why rejected |
|---|---|
| claude: `..._cast_vanished` clip "not found anywhere" | It exists: `swirls_episode_13_...\swirls_episode_13_the_cross_that_wasnt_his_f01_9x16.mp4.SUPERSEDED_cast_vanished`. The wider point (too few bad clips to tune thresholds) is accepted |
| claude: a 6% cover crop drops below 1,900 px | Stills are 1536x2752. A 6% crop leaves about 2,420 px. Not a problem. Auto-crop is dropped anyway (next row) |
| cursor: trim episodes still hit the SW-F1 freeze gate | `sw_f1_freeze_budget` skips any unit whose mode is not `freeze` (`swirls_verify.py:201`). The veo cover tier map is stale but harmless. Left alone |
| gemini: the bridge "compromises an unattended pipeline" | True, but OpenArt is MCP-only and the owner locked it. Accepted as a stated prerequisite, not redesigned |
| gemini: auto-crop distorts on uneven borders | Half accepted: no auto-crop. A border is a FAIL; the fix is one hand crop, same amount on all four sides, then the text read runs again |
| Fable: fix the corner-note and caption branches in `swirls_page.py` now | Deferred. v1 always gives one caption + one note, so those branches are never hit. Zero edits keeps all 5 validators green |
| cursor: drop the film red team until a pilot fails | The house rule needs the 5 guardrail questions on the finished film. Kept, but by hand with the existing template. No new command |
| Fable: defer `status` | Kept in the smallest form (a file checklist, about 40 lines). The owner asked for "what is next" |

---

## 1. Step zero — the $0 pace test (before any build or spend)

**Question:** can a viewer read one storyboard page in about 6 s on a phone?

- **Inputs (all on disk, nothing new rendered):**
  - ep13 `POC\swirls_episode_13_the_cross_that_wasnt_his\`: `front_cover.mp4`, pages f01 f02 f03 f05 f06 f09, `back_cover.mp4`, `narration.mp3`, `narration.alignment.json`, `unit_timing.json`.
  - ep10 `POC\swirls_episode_10_she_loved_much\`: `front_cover.mp4`, pages f01 f02 f04 f05 f08 f09, `back_cover.mp4`, `narration.mp3`, `narration.alignment.json`. (f03 is a Ken Burns clip; skip it.) Unit starts = walk `MANIFEST.units` word counts through the alignment words, as ep13's `_compute_unit_timing.py` does. If the counts do not match, build ep10 silent and say so.
- **Script:** `POC\_pace_test\pace_test.py <episode_dir> --pages f01,f02,...` (throwaway, about 80 lines, ffmpeg only).
  - Picture: front 2.5 s, each page 6.0 s, back 7.0 s. From frame 0, 1.0x, hard cuts, scaled to 1080x1920. About 45.5 s.
  - Sound: for each unit, that unit's own voice from its start to the last word that ends inside the slot, then silence to the slot end. (A real voice over the right page. Rough cuts are fine for a test.)
  - Also writes each page's first frame at 390 px wide (`phone_fNN.jpg`) and a table: baked words on the page, spoken words in the slot.
- **Out:** `POC\_pace_test\ep13_pace_6s.mp4`, `ep10_pace_6s.mp4`, `phone_*.jpg`, `pace_table.json`.
- **Blind seats ($0):** Fable + 2 CLI seats each get ONLY the 390 px frames. Task: "write every word you can read". Score = share of baked strings read, per string type (title, frame number, labels, caption, note).
- **Speaker-holds count:** for the 12 test pages, a table from `narration-tagged.md` + `episode.py`: is a character's line spoken on this page? Is there a second figure or prop that could carry the motion? Count pages where the answer is "speaker only".
- **Owner page:** `POC\_pace_test\_PACE_TEST.html` — the two films shown 390 px wide, the phone frames (click to zoom), the read scores, the speaker-holds count, one question.
- **Decision rule (set now, not after):**

| Result | Action |
|---|---|
| Owner says readable AND 2 of 3 seats read all three labels | Keep the page template. Build |
| Labels not read, rest fine | Labels become ONE word each; corner note dropped (one-line change in `_caption_prose`, all 5 validators re-run) |
| Owner says too fast | 5 pages at about 7 s instead of 6 at about 6 s. Same length, same cost |
| Still too dense at 7 s | Stop. The page layout needs a redesign pass. Nothing is built |

---

## 2. Format (45 s only in v1)

A **unit** = one picture + one clip: front cover, 6 pages, back cover. 8 units.

| Part | Rule |
|---|---|
| Film length | voice + 3.0 s hold. Must be 30.0-59.5 s. Target about 45 s |
| Words | about 85-95 (pace is 2.2 words per second, measured on ep13 and ep16) |
| Front slot | the hook line only, 7 words or fewer, 1.8-3.5 s. Voice starts at 0.0 s |
| Page slot | 4.0-8.0 s each (warn outside 4.5-7.5). One page may be short (4-5 s) at the turn |
| Back slot | last line (10 words or fewer) + 3.0 s hold, 9.0 s or less |
| Clip length | `clip_duration = max(3, ceil(slot + 0.5))`. Always longer than its slot. Trim the tail only |
| Animator | Kling 3 Omni on OpenArt, `pro`, sound off, 35 cr per second. Real output 1072x1928 |
| Stills | nano-banana-pro, 2K, 9:16, 40 cr |

**No fill, ever:** no freeze, no boomerang, no zoom, no crop into a panel, no panel inserts.
Each page plays as one locked-off full-page clip.

**Front cover:** woodcut cover, baked title 2-4 words (picked in the blind title round),
subtitle = the real Scripture range. A moving clip from frame 0, under the spoken hook.

**Back cover:** carries the last line, then the hold. ONE moving clip to the last frame.
Baked closing words = the film's own earned phrase, 2-5 words. Subtitle = the NT verse.

**Page design rules (authoring, checked at plan time):**
1. Three panels set up, the hero scene pays off. Each panel label is a word the narrator says on that page, in spoken order.
2. Panels show things, not faces (object, place, hands, silhouette).
3. Panel motion is light only (light warms, haze drifts). At most one panel has real motion.
4. The hero scene has one human action by one figure, done in the first half, then small living motion to the end. Never fully still.
5. A figure whose line is being spoken holds still, mouth closed in the still. **The motion goes to a second figure or a prop, chosen at page-plan time.** A page with a speaker and nothing else to move is a design fault (SWS-G8).
6. 3 or fewer full figures. Crowds are small, far, unfinished hatched shapes.
7. Phone safe zone: caption sits right under the hero scene, above 85% of frame height. Hero subject left of 85% width.

**Baked text per page:** `SEQ: TITLE` (2-4 words) · `F01`..`F06` · 3 labels (1-3 words, all different) ·
ONE caption line (2-5 words) · corner note `NOTE: ` + 1-3 words (required).
Allowed characters: letters, spaces, apostrophe, comma, full stop, `?`, `!`, the colon in `SEQ:` / `NOTE:`.
Digits only in the frame number, the panel numbers 1 2 3, and Scripture references on covers.
No dash, no ellipsis, no quote marks.

**Motif (blue and gold ink) by page:** F01 = 0, F02 = 1, F03 = 1, F04 = 2, F05 = 2, F06 = 3.
Front cover 0, back cover 3. Never goes down. The first stage-2 page is the gospel turn.
- In stills: written inside the scene sentence as "a brushstroke of blue ink" + one direction + flat properties (thin, matte, dry-edged). Never: thread, cord, ribbon, drip, drop, bloom, flower, petal, ring, loop, pool, puddle, glow, sparkle. Never a "Stage 2" label.
- `material_closer` (required field, dead ink is off): stage 0 = "the page carries no unusual ink anywhere." Stage 1-3 = "the one brushstroke of blue ink is the only unusual ink on the page, and every figure and the paper beneath them are free of any ink."
- **In clips the motif is never named.** Evidence is thin (one page). The test clip in step 6a is the real check.

**Clip prompt (no code change):** existing `assemble_animation_prompt` with `fence_kind="none"` and
`include_no_bubble_clause=False`. That gives: locked camera line, one motion clause per panel,
then the hero motion. 70-130 words in the authored fields.

---

## 3. The pipeline

**Prerequisites**
- **P1. Attended run.** A live Claude Code session with the OpenArt MCP must service `.agent_bridge\gen_requests\` for steps 4-6, and the LLM bridge for Vision audits (agent mode, never the metered API). This pipeline is repeatable, not unattended.
- **P2.** `SWIRLS_GEN_PROVIDER` stays `openart`. No automatic fallback.
- **P3.** Section 1's pace test has passed.

**Spend guard SWS-G0 (fail closed).** File: `<episode>\approvals.json`.
- `swirls_episode.py <dir> approve <step> --cap <credits> --balance <credits> --note "<owner's words, date>"`. `--balance` is the live number from `openart_account_get`, typed by the attending session. Refused if balance < cap.
- Before every paid request the runner works out the price itself (still 40 cr; clip 35 cr x seconds), writes a `requested` row to `<episode>\spend_log.jsonl`, and refuses if the step's rows + this price would pass the cap.
- After the reply: `credits_spent` must be a number. Missing, or more than 110% of the worked-out price: the row is marked `UNCONFIRMED` and **every later paid command refuses** until a person fixes the row.
- No approval file, no approval for that step, or a broken file = refuse.
- `_overrides.json` can excuse a gate FAIL. It can never excuse the spend guard.
- A words lock or praise never writes an approval. Each ask also gets its row in `REPO\data\spend_ledger.jsonl` (servicer, as today).

**Reroll rule:** at most 2 rerolls per item, one change each. After 2 fails stop, change the lever
(camera angle, remove the motion, shorten the clip) and show the owner. Never a third wording.

| # | Step | Paid? | Owner gate |
|---|---|---|---|
| 0 | Episode folder (by hand) | $0 | - |
| 1 | Words + title + packaging card | $0 | pick (locks words + title only) |
| 2 | Voice + alignment | about $0.35 | yes to price, then by ear |
| 3 | Timing + page plan + lints | $0 | - |
| 4 | North-star page + refs | inside the pictures cap | approve north star |
| 5 | Stills | about 400 cr | yes to price, then approve stills |
| 6a | ONE test clip | 245 cr | yes to price, then approve the clip |
| 6b | Remaining clips | about 1,610 cr | yes to price |
| 7 | Draft film (voice only) | $0 | approve the cut (this is the clip gate) |
| 8 | Score | about $1.00 | yes to price, then by ear |
| 9 | SFX + SRT + final file | $0 | - |
| 10 | Film guardrail panel | $0 | one page |
| 11 | Poster + packaging + publish pack | about $0.90 | yes to price; posting is the owner's call |

Every owner page is plain HTML in the episode folder, hand-copied from ep16's pages
(`_PICK_WORDS.html`, `_LISTEN_VOICE.html`, `_PICTURES.html`, `_FILM_V3.html`, `_LISTEN_SCORE.html`,
`_POSTER_PICK.html`, `_UPLOAD_READY.html`). Each carries the 4 questions (who for, take-away,
curiosity gap, global audience), ends in one recommended pick, and is never opened by the agent.

### Step 0 — Folder ($0)
Make `POC\swirls_episode_NN_slug\` by hand: `HANDOVER_RESUME.md`, `_DESIGN_BRIEF.md` (line 1 =
the exact verse range, e.g. `Psalm 41:9; John 13:18-27` — the publish engine reads it), `words\`.

### Step 1 — Words, title, packaging card ($0)
- Blind writers (Fable + Sonnet + Codex + Gemini + Grok, each from scratch, KJV attached) ->
  judge table -> 2-3 candidates -> blind guardrail panel (5 questions + global-audience test,
  words only) -> fix what 2+ seats raise or any Bible point -> re-test once.
  Templates: `F:\slk\PycharmProjects\MeekAndMighty\_pipeline\narration_clarity_template\`,
  `F:\slk\PycharmProjects\ArkAIology\episode-pipeline\guardrail_panel_template\`. Run by hand by the session.
- Shape given to writers: 8 lines, one per unit. Line 1 = hook, 7 words or fewer. Middle lines 9-16 words (one may be 6-9 at the turn). Last line 10 words or fewer, lands on Jesus on a word earned from the passage's own KJV. Character lines are KJV word for word.
- Same round: blind title + poster-idea pairs -> 2-3 for the owner.
- `REPO\independent_review.py "<episode>\narration.md" --type narration` on the recommended candidate, before the owner page. Findings fixed or answered on the page.
- **SWS-G1 (FAIL unless marked warn):**
  - 8 units; hook 7 words or fewer; last line 10 or fewer.
  - **Length estimate per unit, before any money:** `seconds = words / 2.2 + 0.4 x (character turns in the unit)`. Hook 3.5 s or less. Pages 4.0-8.0 s. Total estimate 40.0 s or less (2 s of margin under the 42 s voice target).
  - `REPO\narration_gate.py` passes. `PythonProject1\jesus\narration\narration_pipeline.py verify` passes (KJV verbatim).
  - Closing line is not the shape of the last 3 shipped endings (read from the shipped `narration.md` files; warn).
- Out: `narration.md`, `narration-tagged.md` (an emotion cue on every character line), `voices.json`, `units.json` (`{tag: exact text}`), `_packaging\packaging.json` (draft card).
- Owner: `_PICK_WORDS.html`. A pick locks words and title. It is not a spend order.

### Step 2 — Voice (paid, about $0.35)
- Delete `_turns\` first if any word changed (the cache is by file name only).
- `python F:\slk\PycharmProjects\PythonProject1\jesus\narration\per_turn_synth.py "<episode>" --target 42 --natural --pre-quote-pause 0.4 --stability 0.65`
  - `--target` is required; with `--natural` it is a ceiling only (no time-stretch). Never pass `--force` for a re-run.
  - One stability for every line; all lines go to `eleven_v3`. There are no per-line takes. A robotic line = delete that one file in `_turns\` and run again (a new take, pennies).
- Alignment: `pipeline.assembly_align.align(<episode>, force=True)` with `ASSEMBLY_ALIGN_BACKEND=elevenlabs` (the same call `POC\build_srt.py` makes; pennies, inside the voice cap) -> `narration.alignment.json`. $0 fallback: the whisperx script `POC\swirls_episode_16_let_the_little_children\_align.py`.
- **SWS-G2:** tempo factor in `narration.meta.json` = 1.0; first word starts by 0.40 s; voice 27-56.5 s (warn above 42).
- Owner: quote page, then `_LISTEN_VOICE.html`.

### Step 3 — Timing, page plan, lints ($0)
- `swirls_episode.py <dir> timing` -> `unit_timing.json` (ep13's schema + `clip_duration` per unit) and a printed quote for stills and clips.
  - Unit k runs from its first word's start to the next unit's first word's start. Front starts at 0.0. Back ends at `duration(narration.mp3) + 3.0`.
  - **Count check, fail closed:** spoken tokens (any token with a letter or digit) must be equal in `units.json`, `narration.md` and `narration.alignment.json`. Each `Unit.words` in `episode.py` must equal its `units.json` count.
- Sonnet writes `page_plan.json` (per unit: line, slot, speaker, figure count, who or what carries the motion, motif stage, recurring subjects, labels, caption, note) and `episode.py` (existing `PageSpec` / `CoverSpec` fields only; `mode="trim"`; `w=1080, h=1920`; every `clip_duration` set from `unit_timing.json`; `still_shot_type` in plain lower case).
- Blind check of `page_plan.json` (Fable + the AI panel, KJV attached): Bible facts, period details, animation risk.
- `swirls_episode.py <dir> plan` runs the old SW lints plus, for a trim episode:

| Gate | Checks | Level |
|---|---|---|
| SWS-G3 timing | slot ranges; total 30.0-59.5; each spec `clip_duration` = `unit_timing.json` value and is at least slot + 0.5 (covers too) | FAIL |
| SWS-G4 baked text | section 2 rules on every handwrite string; one caption line; note present | FAIL |
| SWS-G5 still prose | authored fields only: no ALL-CAPS word, no digits, no "check / confirm / ensure / verify / make sure", no "Stage N", no banned motif noun | FAIL |
| SWS-G5a clip prose | no motif, ink, blue, gold or stain word; no speech verb; 2 negatives at most; `fence_kind="none"`; bubble clause off | FAIL |
| SWS-G6 dosage | the map in section 2 | FAIL |
| SWS-G7a refs declared | each subject on 2+ units is named in `refs\refs.json` | FAIL |
| SWS-G8 motion carrier | a page whose speaker is the only thing that could move: FAIL on the turn page, FAIL if more than one such page, else warn | FAIL / warn |

The locked still text (`STYLE_OPEN_HYBRID`, `TEXT_LOCK_HYBRID`, palette constants) is exempt from G5. It contains capitals and the words "speech bubble". It has rendered clean for 9 episodes and is not edited.

### Step 4 — North-star page and refs (inside the pictures cap)
- Render the turn page first with the series `SKILL\references\jesus_ref.png` only. Owner approves it (`_NORTH_STAR.html`).
- Crop tight refs from it by hand (face + full figure per character, key props, the place) into `refs\`, listed in `refs\refs.json`. A recurring subject not on that page gets one single-subject ref render (40 cr). Crops only; never a whole scene as a ref.
- **SWS-G7b:** every declared ref file exists (the existing `sw_l4_refs_exist` hard stop).

### Step 5 — Stills (paid, about 400 cr)
- `swirls_episode.py <dir> still <id>` (existing path, plus SWS-G0).
- **SWS-G9 still audit** (one Vision call per still, bound to the PNG's sha256, new `audit_still_v2`): Vision returns `texts_seen`, `head_count`, and yes/no answers. Code compares text after lower-casing and stripping punctuation, with `difflib` ratio:
  - FAIL: an allowed string with no match of 0.6 or better (missing); a seen text of 4+ letters that matches nothing (invented); the same string matched twice (doubled); head count differs from the plan; a speech bubble; the motif drawn as a cord, drip, flower or ring.
  - WARN: a match between 0.6 and 1.0 (maybe misspelt, maybe misread). The person decides.
- **SWS-G10 cover edge scan** ($0 pixel scan of the four edges): a drawn rule or blank band = FAIL. Fix by hand: crop the same amount off all four sides (keeps 9:16), then re-run SWS-G9. No auto-crop.
- **Human check, always:** Read every PNG; zoom 2x on every baked string; hard props at full frame; count each named character.
- Owner: `_STILLS.html`.

### Step 6 — Clips
- **6a. One test clip (245 cr).** The turn page, 7 s. It tests the new prompt shape (no fence, no bubble clause, motif not named) on one clip, not eight. Owner sees `_CLIP_TEST.html` (the clip + a 5-frame strip). If a bubble or motif change shows: change ONE thing (turn the bubble clause back on), one reroll, look again.
- **6b. The rest (about 1,610 cr),** only after the owner's yes on 6a. `swirls_episode.py <dir> animate <id>` refuses unless the still's SWS-G9 passed and SWS-G3 is green.
- `swirls_episode.py <dir> clipqc [id]` writes `<clip>.clipqc.json` + `_qc\<id>_strip.jpg`:

| Gate | Checks | Level |
|---|---|---|
| SWS-G11 tech | length at least slot + 0.1 s; at least 1072 x 1900; decodes | FAIL |
| SWS-G14 fresh | the json stores the still's sha256; a changed still makes the clip stale and assembly refuses it | FAIL |
| SWS-G13 eyes | one Vision call on 5 frames of the used span: new text or bubble, head count, anyone enters / leaves / merges, modest | WARN |
| SWS-G12-lite | true first vs true last used frame side by side in the strip; ffmpeg `freezedetect` finds no still stretch of 1.0 s or more in the used span | WARN |

Warnings go on the owner's draft-film page. No pixel masks, no thresholds to tune.

### Step 7 — Draft film ($0) — the clip gate
- `swirls_episode.py <dir> assemble --draft` -> `<name>_draft.mp4` (picture + voice, 1080x1920, 30 fps, fast-start).
- **SWS-G15 (FAIL):** every unit is `trim`; each held piece = its slot within one frame; a clip shorter than its slot stops the build; total = voice + 3.0 s; picture and sound the same length (`check_landing_hold.py`); **`freezedetect` finds no freeze of 0.5 s or more in the last 3.5 s**; first word by 0.40 s.
- Owner: `_FILM_DRAFT.html` — the film, the unit strips, every clip warning. "Approve the cut?" Music is not asked for until this is a yes.

### Step 8 — Score (paid, about $1.00)
- Copy ep13's `generate_score_piano.py` into the episode. Keep the prompt wording; change only the timed turning points (from `unit_timing.json`) and the split point (the turn page). Two parts, as the locked standard says. Its own `check_no_dead_intro` runs on each part. Never `composition_plan`.
- `swirls_episode.py <dir> assemble --score piano`. SWS-G15 runs again on the scored file.
- Mix check by measurement, once, by hand (as ep16): music 10-16 dB under the voice in speech, up in the hold, no clipping. The duck is tuned for this track.
- Owner: quote, then `_LISTEN_SCORE.html`.

### Step 9 — SFX, SRT, final file ($0)
- Copy ep13's `build_sfx.py` (uses `REPO\sfx_pilots\sfxlib.py`), times from `unit_timing.json`. Library sounds only.
- `POC\build_srt.py` (already runs after a clean assemble). No burned captions. Write `FINAL_VIDEO.txt`. Re-run `check_landing_hold.py` and the freeze check on the final file.

### Step 10 — Film guardrail panel ($0)
The 5 guardrail questions + who / what / why + curiosity gap (0-10), blind, film only (per unit:
picture, baked words, spoken line, time), Fable seat + AI panel, built by hand from
`F:\slk\PycharmProjects\ArkAIology\episode-pipeline\guardrail_panel_template\`. Fix what 2+ seats
raise or any Bible point; fresh seats; stop after 2 rounds. Owner: `_FILM_REDTEAM.html` with
before/after scores and a "still weak" list. The page says simulated viewers are not real ones.

### Step 11 — Poster, packaging, publish pack (poster about $0.90)
- Thumbnail: the movie-poster process (blind key-art panel, 2-model bake-off, owner pick). Not the front cover by default.
- Finish the card -> `check_packaging.js` to `PACKAGING-READY` -> `cli_publish.py` -> blind copy red team -> `--index --strict` GREEN -> `release_check.py`.
- Gate: PACKAGING-READY; GREEN strict; NO-AI-WORDING; the verse range from `_DESIGN_BRIEF.md` on every platform.
- Owner: `_UPLOAD_READY.html`. Posting stays the owner's call.

---

## 4. Code plan (v1 build = the minimum slice)

### 4.1 `POC\swirls_assemble.py` — trim mode and the moving hold
- `Unit.mode` gains `"trim"`. A manifest is a **trim episode** when every unit is `trim`. A mix of `trim` with another mode is an error. A trim episode with no `unit_timing.json`, or one missing a tag, is an error (no word-count guess).
- New `make_trim(src, out, slot, cdur, manifest)`: raises `ShortClipError` if `cdur < slot + 0.05`; else `encode(["-i", src, "-t", slot], out, manifest)` (frame 0, 1.0x, existing plain scale).
- **The hold fix, trim episodes only:**
  1. The back unit's held length = `total - (measured sum of the other held files)`, so the picture track is `total` long within one frame.
  2. The voice mux drops `-shortest`. Picture stays `total` long; sound is the voice length.
  3. `score_mix.mix_tail` is called as today. Its `apad=whole_dur=total` pads the sound. Its `tpad` clone lands AFTER `total` and is cut off by the existing `-t total` in `output_args`. So the last 3.0 s are the back clip, moving. At most one cloned frame can remain from rounding.
  4. `score_mix.py` is not edited. Old episodes (`freeze` / `boomerang`) take the old path, byte for byte.
- `assemble(manifest, score_name=None)` on a trim episode = draft: stop after the mux, pad the sound to `total`, fast-start, write `<name>_draft.mp4`. `None` on an old episode is an error.

### 4.2 New: `POC\swirls_short.py` (one module)
`build_timing()` (step 3 walk + count check + clip durations + quote) · the lints SWS-G1, G3-G8 ·
`spend_guard()` + `approve()` (section 3) · `clipqc()` (ffprobe, sha256, 5-frame strip, `freezedetect`,
one Vision call through the existing `swirls_verify._vision_audit`) · `edge_scan()` ·
`freeze_check(mp4, last_seconds)` · `status()`.

### 4.3 `POC\swirls_verify.py` and `POC\swirls_episode.py`
- `swirls_verify.py`: add `audit_still_v2` (asks for `texts_seen`, `head_count`; code decides; same sha-bound sidecar). Old audits untouched.
- `swirls_episode.py`: new commands `timing`, `approve`, `clipqc`, `status`; flag `assemble --draft`. For a trim episode: `plan` adds the SWS lints; `still` / `animate` call the spend guard first; `animate` needs a passing SWS-G9; `assemble` needs fresh clip QC and adds SWS-G15. Old episodes see no change.
- **`status`** (the "what is next" for the owner and for a cold session): a plain file checklist, no state machine. Prints one line per step (done / not done, from files on disk + `approvals.json` + `spend_log.jsonl`), then `NEXT:` the first step not done and its command or owner question, then credits spent against each cap. `HANDOVER_RESUME.md` stays hand-kept for notes.

### 4.4 Tests
- New `POC\_validate_swirls_short.py` ($0): trim on synthetic ffmpeg clips; a too-short clip must fail; **the last 3 s of a trim build must not be frozen while a legacy build of the same clips is unchanged**; timing maths against ep13's alignment; count-check failure; lints against real past failures ("MEDIUM TWO-SHOT", a dash caption, doubled labels); spend guard refuses on a missing approval, a missing credit count and a passed cap.
- All five old validators stay green: `POC\_validate_swirls_assemble.py`, `POC\_validate_swirls_cover.py`, `POC\test_the_cross\_validate_swirls_page.py`, `..\_validate_swirls_page_hem.py`, `..\_validate_swirls_page_hybrid.py`.

### 4.5 Not touched
`swirls_page.py`, `swirls_cover.py` (stale veo comments stay; noted), `openart_bridge.py`,
`pipeline\*`, `per_turn_synth.py`, `build_srt.py`, `sfxlib.py`, `cli_publish.py`, all shipped
episode folders, the main 4-stage engine.

### 4.6 Build order
1. Pace test (section 1). Owner answer.
2. v2 through the plan panel with a full quorum.
3. Trim mode + hold fix + `_validate_swirls_short.py`. Six validators green.
4. `swirls_short.py`: timing, then lints, then spend guard, then clip QC, then status.
5. ONE pilot at 45 s.

### 4.7 Deferred until the pilot has shipped (and why)

| Deferred | Why it can wait |
|---|---|
| Scaffold script + template folder | Make the pilot folder by hand; turn the pilot's own folder into the template after |
| Owner-page builder | Copy ep16's pages for one pilot. Abstract after the second use |
| Shared score and SFX modules | ep13's two scripts copy cleanly once more |
| `redteam-pack` command | The templates already exist in the reference projects |
| Full state machine, `_STATUS.html`, handover rewriting | The file checklist covers "what is next" |
| 30 s and 60 s sizes | A table row once 45 s is proven |
| Bridge `job_id` / `_jobs.jsonl` | Keep job ids in the handover file, as ep16 did |
| Rewriting the 7 skill docs, new `PageSpec` fields, `anim_style` | Existing fields already express the short prompt |

---

## 5. Skill plan

Keep one skill: `swirls-of-life`. No second skill.
- **With the v1 build:** add a short block (15 lines or fewer) at the top of `SKILL\SKILL.md`: "SHORT pipeline (pilot): start with `swirls_episode.py <dir> status`; runbook = `SKILL\SWIRLS_SHORT_PIPELINE.md`" (this design, promoted). Nothing else in the skill folder changes.
- **After the pilot ships clean:** rewrite `SKILL.md` around the 12 steps; add dated SUPERSEDED banners to the stale parts of `PRODUCTION_PIPELINE.md`, `NORTH_STAR_PROMPT.md`, `NORTH_STAR_ANIMATION_PROMPT.md`, `NORTH_STAR_COVER_PROMPT.md` (HF calls, veo tiering, fill history, "Stage N dosage" wording). The score docs are not re-labelled; felt piano is used on precedent (ep10, ep13, ep16), not declared the identity here.
- **After a second episode repeats the result:** lock the skill.

---

## 6. Cost (45 s pilot)

OpenArt at $0.002 per credit. Re-derive from the real invoice.

| Ask | Clean run | Cap (worst case: 2 rerolls on 30% of items) |
|---|---|---|
| Voice + alignment | about $0.35 | $0.60 |
| Pictures: 8 units + 2 ref renders | 400 cr = $0.80 | 640 cr = $1.28 |
| Test clip (7 s) | 245 cr = $0.49 | 735 cr = $1.47 |
| Remaining clips (46 s) | 1,610 cr = $3.22 | 3,100 cr = $6.20 |
| Music | about $1.00 | $1.50 |
| Poster bake-off | about $0.90 | $1.20 |
| **Total** | **about $6.80** | **about $12.25** |

OpenArt worst case = 4,475 cr. The account holds about 8,000 cr and other sessions spend from it,
so each `approve` checks the live balance. Old episodes: $5-30 for 62-106 s at 720p.

---

## 7. Where the evidence is thin

- A 6 s page on a phone. Section 1 tests it for $0; real viewers are still the only proof.
- The cover design (title under a spoken hook) has no viewer data.
- The brushstroke motif wording worked on one page.
- The clip prompt drops the fence, the bubble clause and motif words together. One test clip checks it; one clip is still one clip.
- Vision misreads handwriting. The human 2x zoom stays.
- Image-content rounds (wrong shape, vanished or merged figures) are reduced by rules, not prevented. Expect 1-3 rounds.
- The cap percentages are guesses until the pilot.

---

## 8. Open questions for the owner (3)

1. **Default length.** My pick: **45 s, 6 pages** (about $7). 60 s only when a story needs it, after the pilot.
2. **Front cover.** My pick: **keep the woodcut title cover, 2-3 s, voice from the first frame.** For $0.29 more the pilot can also render a title-free cover so real seed viewers can compare the two.
3. **Pilot story.** My pick: **Psalm 41:9 -> John 13:18-27, the friend who ate His bread.** Two figures at a table, one prop, no crowd, no cross, and the motion (a hand taking the bread) belongs to the one who is not speaking. It fits the prophecy focus. Second choice: Isaiah 40:3 -> John 1:23.
