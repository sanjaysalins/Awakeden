---
name: swirls-of-life
description: Make a 45-second "Swirls of Life" Bible short end to end — a woodcut front cover, six hand-drawn ink-and-watercolor storyboard pages (baked SEQ title, frame number, three labeled sketch panels, one hero scene, one big caption) and a woodcut back cover, with the blue-and-gold ink motif dosed to track the gospel turn. Twelve gated steps from words to publish pack, trim-only clips (no freeze, boomerang or zoom fill), a moving landing hold, and a fail-closed spend guard with an owner yes at every paid step. Use for any new Swirls short, or to render a single storyboard-page still in this style. NOT for /painted-comic (no baked text), NOT for the baroque/graphic_novel config styles, NOT a $0 clip effect (/line-boil, /print-grade).
---

# /swirls-of-life — the Swirls Short (45 s)

> **Do not install this file until build phases A-C of the design pass.** It names runner commands that do not exist yet. Matches design v3.2.

**Binding design:** `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\_swirls_short_design\SWIRLS_SHORT_PIPELINE_DESIGN_v3.md` (v3.2). The design wins over this file. Its section 6 says what is really built.

```
REPO   = F:\slk\PycharmProjects\JesusInTheBible
POC    = F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test
SKILL  = F:\slk\PycharmProjects\JesusInTheBible\.claude\skills\swirls-of-life
RUN    = .venv\Scripts\python.exe poc_living_water_ink_style_test\swirls_episode.py "<episode_dir>"
```

## When to use

- A new Swirls short (45 s only for now).
- Picking one up part-way: **start with `RUN status`** (done / not done, `NEXT:`, spend against each cap, open WARNs).
- Not for re-cutting an old episode.

## The format in one screen

| Unit | Spoken | On screen | Clip to order |
|---|---|---|---|
| front | hook, 4-5 words, voice from frame 0 | woodcut title cover, 2.0-3.0 s | 3-4 s |
| f01-f06 | 11-14 words each, 1 voiced quote at most | storyboard page, 5.0-7.0 s | `ceil(slot + 0.5)` |
| back | last line (10 words or fewer) + 3.0 s hold | woodcut back cover that **reads as Jesus**, moving to the last frame | `ceil(slot + 2.0)` |

- **80-88 words. 5 voiced character quotes at most.** Time check: `words / 2.2 + 0.4 x voiced quotes` = 38-42 s. Film = voice + 3.0 s, target 45 s.
- **Trim the tail only. 1.0x. Hard cuts. No freeze, boomerang, ping-pong, speed change, zoom or crop fill, ever.** Output is 1080x1920 at 30 fps, scaled and cropped, never stretched.
- Stills 40 cr (nano-banana-pro 2K 9:16). Clips 35 cr per second (Kling 3 Omni `pro`, **sound off**, 3-15 s). Re-check with `openart_model_cost` before any quote.

**Baked text on a page — only this:** `SEQ: <TITLE>` (the cover title, same on all six) · `F01`..`F06` · 3 labels (1-2 words, 6 in total, each spoken on that page) · ONE caption (2-5 words, a run of that page's spoken words, the biggest writing). No corner NOTE. 11 reading words at most. Nothing twice. No dash, quote mark, ellipsis or digit. Caption above 75% of the height, left of the right 15%.

**Motif stage:** 0, 0, 1, 1, 2, 2, 3, 3. Never on a thing of its own colour (no blue stroke on water).

## Rules that never bend

1. **Words before money.** A pick or praise never approves spend.
2. **Four money asks: voice, pictures, clips, music.** Each question shows two numbers from `RUN quote <step>`: **"about X, at most Y — yes?"** `RUN approve --cap` must equal Y, and the note must quote the owner with the number and the date.
3. **Look and price are two separate answers** on one page. If only the look is answered, ask the price again.
4. **Hard stops inside a paid step:** after the first picture (page 3) and after the 2 test clips (page 5), nothing more is bought until the owner's look is recorded.
5. **More than Y, a 4th render of one unit, or any spend after a step is closed = a new ask.**
6. **Every OpenArt request for a short goes through `openart_bridge.submit()`.** Never call the OpenArt generate tools directly for a marked episode. Never render a short's still into another folder and copy it in (it will be refused: no receipt).
7. **Servicing the bridge:** follow `POC\SWIRLS_SHORT_SERVICER.md` — claim by rename first; write the `creation_id` as soon as generation starts; download to staging; copy the receipt from `openart_creation_show`, never from a quote, a balance, or memory.
8. **Never clear an open spend row with a typed number.** Use `RUN fetch`, or `RUN confirm` with a saved record dump. If OpenArt's record cannot settle it, stop and tell the owner.
9. **ElevenLabs spends only through `RUN voice`, `RUN align`, `RUN score`.** Never run `per_turn_synth.py` or a score script by hand on a short.
10. **Start paid commands in the background** (a foreground command is killed at 10 minutes and leaves a live request).
11. **Every panel is blind and has a Fable seat.** Quorum Fable + 3 (text) or Fable + 2 (images). Gemini cannot read images; never count on Grok. 600 s, one retry at 900 s, one substitute, then stop.
12. **Scripture gates cannot be overridden.** KJV quotes are one unbroken whole-word run: no `...`, no dropped word, exact case.
13. **Overrides** are for one file, with the owner's dated words. A new render voids them.
14. **No hand fixes to a rendered still in the pilot.** Reroll.
15. **Owner pages:** plain HTML, short words, big pictures, click to zoom, the 4 questions, ONE pick, the open WARNs in plain words. Film pages say "watch on your phone". Never open anything; give the full `file:///` link.
16. No AI wording in public text. No media in git. Never commit unless asked. OpenArt only. Attended run; never the metered API.

## The 12 steps

### 0. Folder ($0)
`POC\swirls_episode_NN_slug\` + `HANDOVER_RESUME.md`, `words\`, `_DESIGN_BRIEF.md` (line 1: `John 1:19-29 (Isaiah 40:3 fulfilled)`), marker `.swirls_short`. `RUN status`.

### 1. Words and title ($0)
- Blind writers (Fable + 4; each also gives a 2-3 word title and a poster idea) -> judge table -> 2-3 candidates -> blind guardrail panel -> fix by convergence -> re-test once. Templates: `POC\_short_templates\`.
- Write `narration.md`, `narration-tagged.md` (an emotion cue on every character line), `voices.json`, `units.json`, `kjv_spans.json`, `_packaging\packaging.json`.
- `RUN words` (G1 shape, G1e time, G1s same words everywhere, G1k KJV, G1v speakers, `narration_gate.py`).
- `.venv\Scripts\python.exe independent_review.py "<episode>\narration.md" --type narration`
- **Page 1:** pick the words -> `RUN ok words --note "..."`. Then the voice price.

### 2. Voice + alignment (ASK 1)
- `RUN quote voice` -> ask -> `RUN approve voice --cap <Y> --unit usd --note "..."`
- `RUN voice` (clears stale `_turns\` itself; narrator at 0.65; character lines at 0.3, two takes).
- **Page 2:** take A or B by ear -> `RUN ok voice_ear --take A|B --note "..."`. Then the pictures price.
- `RUN align` (ElevenLabs timing, once per audio; plus the $0 check that the audio says the words). No whisper timing.
- G2: tempo 1.0, first word by 0.40 s, voice 39-45 s.

### 3. Timing, page plan, lints ($0)
- `RUN timing` -> `unit_timing.json`.
- Write `episode.py` (`mode="trim"`, `w=1080, h=1920`, `corner_note=""`, `clip_duration` from the timing file, each `Unit.src` = the canonical clip path) and `page_plan.json`:
  `{"north_star": "f04", "units": {"<tag>": {"full_figures", "crowd", "motion_carrier", "motif_stage", "subjects"}}}`.
- `RUN plan` (G3-G8). 3-seat blind check (Fable + 2, KJV attached).

### 4. North-star page + refs (inside ask 2)
- `RUN quote pictures` -> ask -> `RUN approve pictures --cap <Y> --unit cr --balance <live> --note "..."`
- `RUN still <north_star>` then `RUN hold <north_star>` (the page held for its slot under its voice line).
- **Page 3, on a phone — first go / no-go:** `RUN ok northstar_look --note "..."`.
- Crop refs into `refs\` + `refs\refs.json`; a missing subject: `RUN still ref:<name>` (3 at most).

### 5. Other stills + animatic (inside ask 2)
- `RUN still <id>` x 7 -> `RUN verify` (G9 strict audit, G10 edge scan, G14s receipts).
- Read every PNG; zoom 2x on every baked string. A text FAIL you believe is a misread: `RUN read <id> --string "<what is really there>" --note "..."`.
- `RUN animatic` -> the stills test film + `_qc\contact_sheet.jpg`.
- **Page 4, on a phone — go / no-go:** `RUN ok stills_animatic --note "..."`. Then the clips price.

### 6. Clips (ASK 3)
- `RUN quote clips` -> ask -> `RUN approve clips --cap <Y> --unit cr --balance <live> --note "..."`
- Test clips: **the north-star page, then the back cover.** `RUN animate <id>` -> `RUN clipqc <id>`.
- **Page 5:** both clips; play the back cover to its end -> `RUN ok clip_test_look --note "..."`.
- The other six, one at a time: `animate` -> `clipqc` -> read every strip image -> **play every clip where a character speaks.** A FAIL stops the batch.

### 7. Draft film ($0)
- `RUN assemble --draft` (G15, G15h, receipts).
- **Page 6, on a phone** (also the reading check for the lettering in motion) -> `RUN ok draft_cut --note "..."`. Then the music price.

### 8. Score (ASK 4)
- `RUN quote score` -> ask -> `RUN approve score --cap <Y> --unit usd --note "..."`
- The episode's own `generate_score_piano.py` (copy of ep16's, reading its inputs from `assembly_receipt.json` and `unit_timing.json`; felt piano; two parts split at the north-star page; never `composition_plan`).
- `RUN score` -> `RUN assemble --score piano` (G17 score gate).

### 9. SFX, SRT, final file ($0)
- The episode's own `build_sfx.py` (copy of ep13's, cue list rewritten, input from `assembly_receipt.json`); library sounds only.
- SRT from the alignment on disk only. No burned captions. `FINAL_VIDEO.txt` (G16 chain). `.venv\Scripts\python.exe check_landing_hold.py`

### 10. Film guardrail panel ($0)
- Blind, film only: 5 guardrail questions, who / what / why, curiosity 0-10. 2 rounds at most.
- **Pass:** every seat gets who / what / why; no open Bible complaint; median curiosity 7+. Else the page says NOT PASSED.
- **Page 7, on a phone:** the finished film + the result -> `RUN ok film_final --note "..."`. A pilot ends here.

### 11. Poster, packaging, publish — only when the owner asks to post
Movie-poster process through the guarded bridge into `<episode>\poster\`, own "about X, at most Y" ask. Then the packaging card, `/publish`, copy red team, strict GREEN, `release_check.py`.

## Gates

| Gate | What | Level |
|---|---|---|
| SWS-G0 | spend guard: grant = the cap the owner saw; look gates with file hashes; one open row; claim / cancel / staging; receipt from OpenArt's record | refuse |
| G1, G1e, G1v | words shape, time, speakers | FAIL |
| **G1s, G1k** | same words everywhere; KJV unbroken run | FAIL, no override |
| G2, G2w | voice timing; the audio says the words | FAIL |
| G3, G4, G5, G5a, G6, G7a-c, G8, G8t | timing, baked text, prose, dosage, refs declared / present / sent, motion carrier, order | FAIL |
| G9 | strict still audit (any wording, punctuation, digit or extra token difference; figures; bubble; motif; border) | FAIL; a text misread is cleared by `RUN read` |
| G10 | pixel edge scan | FAIL on covers, WARN on pages |
| G11 | clip decodes, long enough, big enough | FAIL |
| G13 | clip frames: bubble, new or changed text, figure change, ink changed, still thing moves, bare skin | FAIL with a bound override |
| **G14, G14s, G16** | every still, clip and final file matches its receipt | FAIL, no override |
| G15 | frame-exact cuts, 1080x1920 at 30 fps, picture = sound | FAIL |
| G15h | the last 3 s move in every 1 s window, above a frozen control | FAIL |
| G17 | score covers the whole film with no dead second | FAIL |

Settle an open row: `RUN fetch <rid>` · `RUN confirm <rid> --receipt <dump>` · `RUN confirm <rid> --void --list-dump <file>` (only a request no servicer ever claimed). `RUN reconcile` before each ask.

## Authoring (what still holds from the old skill)

- **Pages:** `SKILL\NORTH_STAR_PROMPT.md` (`woodcut_hybrid`) via `POC\test_the_cross\swirls_page.py`.
- **Covers:** `SKILL\NORTH_STAR_COVER_PROMPT.md` via `POC\swirls_cover.py`. Always nano-banana-pro.
- **Clips:** `SKILL\NORTH_STAR_ANIMATION_PROMPT.md`. The ink is never animated and never named.
- **Refs:** `SKILL\references\jesus_ref.png` is the series Jesus; everything else is cropped from the approved north-star page.
- **Score:** felt piano (ep8 / ep10 / ep13 / ep16); `SKILL\SCORE_DESIGN_EARLY.md`.

**Page rules:** three panels set up, the hero pays off · panels show things, not faces · one human action in the first half, then small living motion to the last frame · **the figure whose line is heard holds still, mouth closed; name the `motion_carrier`** · 3 full figures at most; a crowd is far, hatched and declared · back cover = Jesus, larger, facing, with motion written to run to the end.

## Superseded — do not follow

| Old | Now |
|---|---|
| Focal Tour gap-fill, freeze, boomerang, tail-loop, Ken Burns fill | Banned |
| `hf generate ...`, Higgsfield table, "~2 cr/still" | OpenArt through the guarded bridge |
| veo tiering; cover clips 4 / 6 / 8 s | Kling 3 Omni, 3-15 s |
| "thread / curl of blue ink", "Stage N" in prompts | "brushstroke"; stages live in `page_plan.json` |
| Corner note, 2-line captions | Dropped |
| Trance score bank as default | Felt piano |
| 62-106 s, 720p, silent covers | 45 s, 1080x1920, voice at frame 0 |
| One voice take at stability 0.65 for everyone | Characters 0.3 x 2 takes; narrator 0.65 |
| `credits_spent` from a quote or balance difference (`AGENT_BRIDGE.md` step 6) | `POC\SWIRLS_SHORT_SERVICER.md` |
| `build_srt.build()` after assemble | Cache-only SRT |

## Known defects and the fix that works

| Defect | Fix |
|---|---|
| Kling draws a speech bubble | Remove that figure's motion; do not re-word |
| Border on a cover | Wording does not fix it. Reroll |
| Face / costume / prop drift | A ref for every recurring subject, and check it was sent |
| Motif as cord, drip, flower, ring; or lost on a blue thing | Remove the noun; brushstroke + one direction; put it on dry ground or paper |
| Wrong, doubled or punctuated baked text | Reroll; short strings; zoom 2x |
| Lettering melts in the clip | Less motion near the text; reroll the clip |
| Clone or merged figure | Near/large + far/small; count full figures |
| Prop shape wrong after 2 rerolls | Change the camera angle |
| Negative clause makes Kling worse | Remove the described motion |
| Back clip settles, hold goes dead | Order slot + 2 s; write motion that runs to the end; test it second |
| Fixed PNG, old clip in the film | Re-animate; the old mp4 is superseded automatically |
| Timed-out request | `RUN fetch`. Never just re-run it |
| Score silent at the start | Two parts; G17 |
| Sound left on in a clip | 40 cr/s; the receipt shows it; send `generate_sound: false` |
| Stale voice after a word change | `RUN voice` clears `_turns\` itself |
