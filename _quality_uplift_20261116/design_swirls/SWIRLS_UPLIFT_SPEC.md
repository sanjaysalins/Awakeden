# Swirls of Life - uplift before upload: BUILD SPEC

Date 2026-11-16. Design lead: Fable. Read-only pass: nothing generated, nothing spent, no repo file changed outside this folder.
Scope: the 8 Swirls films in `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\EPISODES.txt`.
Owner page (short): `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\_SWIRLS_UPLIFT_OWNER.html`

---

## PLAIN SUMMARY (read this, skip the rest if you like)

- **The big problem is real and bigger than first reported.** I measured every clip. 7 of 8 films fill time with freeze, backwards play or slow zoom. Only Little Girl, Get Up is clean.
- **6 key moments are not real clips** (the first report said 3). 4 are a zoom on a still: The Bier - the touch, "Arise", and the end card; She Loved Much - the feet. 2 are a fully frozen picture: Where Are the Nine - "Go shew yourselves"; The Cross - the opening cover.
- **Where Are the Nine has 5 bad clips**, not 1: the healed man changes face (F10), one clip is a frozen picture (F03), and 3 clips zoom into the page, move the blue swirl or invent things (F05 red-roof farmhouses, F06 smoke, F07 glow + cut-off words).
- **Can Any Good Thing is out of sync.** Pages arrive about 5 seconds after the words they belong to. Free to fix.
- **The fix:** keep every good clip we have. Buy only the missing seconds, as short new shots. Hard cuts. No fill at all. Then add a light layer of **pencil marks** on the page margins, tied to spoken words. The blue swirl is never touched.
- **$0 part:** the pencil kit, the re-timing, all doodles, one borrowed page each way between Can Any Good Thing and Jacob's Ladder.
- **Paid part:** 38 new pictures + 286 seconds of new clips for 7 films. **About $21 if every shot works first time. About $32 with the usual redo rate. Cap $35.** Extras worth having: about $3 more.
- **Pilot: Can Any Good Thing (ep 08).** Words are settled, it is short, and it shows every part of the fix. Pilot cost: **$2.50 to $3.70, cap $4.50.**
- No narration changes anywhere in this plan.

**My pick: say yes to the $0 kit build + the ep 08 pilot at a $4.50 cap. Judge the rest after you see it.**

---

## 0. What I checked, and what changed versus the earlier report

Evidence is saved next to this file:
- Slots vs clip lengths + every mp4 on disk: `...\design_swirls\audit\units_slots_and_all_clips.txt` (made by `...\design_swirls\tools\plan_all_units.py`, calls the repo's own `swirls_assemble.plan_units`).
- First-vs-last-frame motion audit of every unit clip: `...\design_swirls\audit\clip_motion_audit.txt` (made by `...\design_swirls\tools\clip_motion_audit.py`; ECC affine alignment. `zoom=1.058 aligned~3.7` = a pure camera move on a still; `raw=0.0x` = frozen).
- Contact sheets I looked at: `...\design_swirls\audit\sheet_*.jpg`. Proof frame for ep07 F04: `...\design_swirls\audit\ep07_f04_first_vs_last_frame.jpg`.
- Real word times for 7 films: `...\design_swirls\word_timings\*.txt` (from each film's own alignment json; voice starts at 0.00).

Corrections to `swirls_report.md` / `_SUMMARY.html`:

| Earlier claim | What the files show |
|---|---|
| 3 hero moments are stills | **6.** Ken Burns (zoom 1.058, no motion inside): ep07 F03, **ep07 F04 "Arise"**, ep07 back cover, ep10 F03. Fully frozen: **ep11 F03**, **ep13 front cover** (frame-to-frame diff 0.0005). |
| ep11: one face defect + F07 crop | F10 wrong man. Also F05, F06, F07, F10 are PixVerse clips (1072x1920) that zoom inside the clip (zoom 1.065 / 1.064 / 0.966), animate the motif (F10 ribbons + bubbles), invent content (F05 top panels turn into red-roofed farmhouses, F06 vapour, F07 glow). All four need a Kling re-animation. |
| "6-7 films use fill" | 7 of 8. Fill seconds per film on the shipped cut: ep02 ~33 s of 62, ep08 ~22 of 64, ep07 ~16 of 72, ep10 ~21 of 106, ep11 ~18 of 84, ep13 ~27 of 106, JL ~25 of 56.5 (plus 2 repeated pages). |
| not mentioned | **ep08 picture/voice sync is off by ~5 s** (slots were guessed from word counts; the hook lines are short). ep02/07/10 use the same guess but land close. ep11/ep13 already use real timing. |
| not mentioned | The freeze code adds a **slow zoom** to every freeze tail (`make_freeze` zoompan to 1.06). So "freeze" units also break the no-zoom rule. ep10's back cover ends with the title cropped ("...HIS PEAC"). |
| JL "needs a Jesus page" | True. Also: the hook holds a 4 s cover for 10 s; pages F03 and F04 play twice; no back cover. **An unused, good page exists: JL F01** ("the threat / tents behind / the long road", 4.0 s) - it fits "Esau wanted him dead. He ran." at $0. JL F07/F08 and the old back cover stay unused (their baked words "You are not" / "He is that ladder" were dropped by the 2026-11-02 words lock). |
| unused longer clips could fix the fill | **No.** There is no spare longer take anywhere. Unused files are either defective (named so), older takes of the same still at the same length, or ep11's bake-off takes (same still, same length - cutting two takes of one page back to back is a jump). Only two $0 re-uses are real: JL F01 (above) and the two cross-film borrows in section 4. |

Earlier owner rule (2026-11-08): "do not fix current episodes". Today's ask overrides it for these 8, but the spirit stays: **shipped files are never overwritten.** Every uplift is a new file in an `uplift\` subfolder; `FINAL_VIDEO.txt` moves only after the owner says yes to the new cut.

---

## 1. The shared "Swirls uplift kit"

A thin pencil layer on top of finished clips. It behaves like a second hand - an editor's pencil - on the storyboard page. Mock (self-contained, nothing loads from the web):
`file:///F:/slk/PycharmProjects/JesusInTheBible/_quality_uplift_20261116/design_swirls/kit_mock.html`

### 1.1 Look (tokens)
| Token | Value |
|---|---|
| Canvas | 1080x1920, 30 fps, Remotion on top of the cut. Clip pixels are never altered. |
| Graphite | `#4A4640`, opacity 0.82, `mix-blend-mode: multiply` |
| Red pencil | `#A8432F`, opacity 0.85, multiply. **One red mark per film**, on the film's key word. |
| Stroke | 5 px (rings/circles 6 px, dashes 4 px, dash 20/16), round caps and joins |
| Hand | every path through `wobblePts(seed, amp 1.6, step 22)`; second pass at 35 % opacity, 1.5 px off, for circles/rings |
| Boil | held marks only: 2 seeds swapped every 4 frames (`boilSeed(f, seed, 4, 2)`). Never the page. |
| Lettering (S6 only) | Kalam Regular 34 px, graphite. Already in `_remotion\public\Kalam-Regular.ttf`. |
| Banned colours | blue and gold (they belong to the motif), white, any glow or shadow |

### 1.2 Devices
| Id | Device | What it does | Draw time | Max / film | Status |
|---|---|---|---|---|---|
| S1 | **Look-up ring** | pencil ring round ONE of the 3 small top panels when the voice says what that panel shows | 10 f + 6 f second pass | 3 | BUILD (Remotion). The python `focal-tour` skill is NOT used: it dims the page, which changes the art. |
| S2 | **Caption underline** | wobbly line under a baked caption word as it is spoken | 8-10 f | 3 | BUILD |
| S3 | **Caption circle** | two-pass ellipse round 1-2 baked words (Remotion twin of `/annotators-circle`) | 12 f | 1, and it is the red one | BUILD |
| S4 | **Margin arrow** | curved arrow from blank margin to a detail; head drawn last | 12 f + 3 f head | 2 | BUILD |
| S5 | **Idea doodle** | one tiny wordless diagram that shows the line's logic. Built only from: line, dash, arrow, tick, tally stroke, cross-out, footprint, eye. Designed per film (section 4). | 10-30 f | 2 | BUILD (primitives) + per-film data |
| S6 | **Verse tag** | a reference ("John 1:48") writes itself left to right in a blank margin, only on a spoken KJV quote. Decoration only; meaning stays spoken. | 12 f wipe | 2, default OFF | BUILD |
| S7 | **Page turn** | 8 f: the outgoing page slides left 104 % with a 3-degree tilt and a soft shadow; the next page is already under it. No dissolve. Only between two different pages, never onto the back cover. | 8 f | 3 | BUILD (simple transform; `comic_kit\transitions.tsx` has the easing) |
| S8 | **Tick burst** | 3 short ticks at one physical hit, on the SFX frame (small cousin of `/impact-burst`) | 4 f | 1 | EXISTS: `comic_kit\doodles.tsx` `motion_ticks`, retoned to graphite |

### 1.3 Rules (the gate checks these)
1. **Word-tied.** Every mark names a spoken word and its time from the film's alignment file. It starts drawing 2 frames before that word and is finished as the word lands.
2. **One at a time.** Never two marks drawing at once. At least 3.0 s between mark starts. **At most 8 marks per 60 s.**
3. **Quiet zones.** No mark in the first 1.0 s, on either cover, or in the last 3.0 s hold.
4. **Keep-outs.** No stroke inside (a) the blue-gold motif box + 24 px, (b) any baked text (S2/S3 sit under/around it, never over it), (c) Jesus' face or hands, (d) any face. A dashed line that must cross a motif thread lifts (48 px gap).
5. **Leaves before the cut.** Marks fade 5 f and are gone 5 f before the shot ends (S2/S3 may ride to 5 f before the cut).
6. **Dub-safe.** Marks are wordless except S6. Nothing the viewer needs is carried by a mark.
7. **Not allowed, ever:** animating or masking the motif, glow, light sweeps, whole-page boil/`line-boil`, `parallax-panel`, zoom or camera move added to a clip, pills/captions, particles, `raking-light`/`damp-cockle` (they move the paper under baked text).

### 1.4 Where it gets built
- New folder `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\swirls_kit\`:
  - `marks.tsx` - S1..S6, S8 as data-driven components. Import `InkStroke, wobblePts, boilSeed, prog, pathD, mulberry` from `..\comic_kit\core`.
  - `SwirlsUplift.tsx` - `<OffthreadVideo src=base.mp4>` + S7 page turns + one full-frame SVG mark layer. Props = the episode's `uplift.json`.
  - register `SwirlsUplift` in `_remotion\src\Root.tsx` (one `<Composition>` with `calculateMetadata` reading `total_frames`).
- Per film: `<episode>\uplift\uplift.json` (schema = `...\design_swirls\pilot_ep08_uplift.json`), copied with `base.mp4` to `_remotion\public\swirls_uplift\<ep>\`.
- `$0 gate` `<repo>\poc_living_water_ink_style_test\check_swirls_uplift.py` (new): fails on any rule in 1.3 (spacing, count, quiet zones, keep-out overlap, word time within +-3 f of the alignment file), on any shot whose clip is shorter than its slot + 0.05 s, and on total frames != audio length.
- S7 needs both pages on screen for 8 f: so a shot that ends in a page turn must have 4 spare frames after its slot (true for every page turn planned here).

---

## 2. How every film is re-cut (same recipe, all 7 page films)

1. **Picture only.** Voice, score and SFX are untouched: the audio stream is copied from the shipped `*_final*_sfx.mp4`. Film length does not change by a frame.
2. **New script per film**, never the old assembler: `<episode>\uplift\cut_uplift.py`, reading `uplift.json` `shots`. For each shot: `fps=30, scale=1080:1920:force_original_aspect_ratio=increase, crop=1080:1920`, `-frames:v (f1-f0)` from the clip's frame 0, 1.0x. **Fail closed** if the clip is shorter than the slot + 0.05 s. No tpad, no reverse, no setpts, no zoompan. (`swirls_assemble.make_trim` already does exactly this; reuse the function, do not edit the episode's `episode.py`.)
3. Cut points come from the **real word times** (section 4 tables), not word counts. Convention: a page arrives about 0.25 s before its first word.
4. **Shot length:** no page stays longer than 10 s; a new shot is bought at the first whole second n where the slot <= n - 0.01 s (Kling takes whole seconds 3-15 and delivers n.04 s; the hard floor is clip >= slot + 0.05 s).
5. **New shots are ordinary storyboard pages** (same `PageSpec`: 3 top panels + big picture + one caption that is a verbatim spoken fragment; no NOTE line, per the v3.2 short design). No template change. Labels continue the film's numbering with a letter (F03B). New specs live in `<episode>\uplift\uplift_pages.py`, importing the character builds and `refs\` from the episode's own `episode.py` (read-only import).
6. **Model:** stills `nano-banana-pro` (40 cr). Clips `kling-3-omni` pro, sound off (31.6 cr/s measured: 158 cr / 5 s, 284 cr / 9 s). **Not PixVerse for storyboard pages** - every PixVerse page clip in ep11 zooms into the page. OpenArt only; Higgsfield only if the owner says so.
7. **Every new clip passes 4 checks before it enters a cut** (all $0): `clip_motion_audit.py` zoom within 1.000 +-0.010; not frozen (mean frame diff > 0.15); baked text identical first vs last frame at 2x zoom (caption-fade defect is ~1 in 3); motif box pixel-diff ~0. Plus the standing eye checks: cloned people, era props, hands.
8. **Animation prompt rule for longer clips:** two small beats, not one - a completing gesture in the first half, a second small living motion (breath, cloth, leaves, dust) in the second half - and the standing clause "the ink stays exactly as drawn, in place, for the whole clip".
9. Output: `<episode>\uplift\<ep>_uplift_base.mp4` (cut + original audio) -> Remotion `SwirlsUplift` -> `<ep>_uplift_final.mp4` (video from Remotion, audio stream-copied again from the shipped final, `+faststart`). Then `check_landing_hold.py`.

---

## 3. Money model (re-quote with `openart_model_cost` before any yes)

| Item | Rate | Source |
|---|---|---|
| OpenArt credit | $0.002 | CLAUDE.md, owner's real billing |
| Kling 3 Omni pro clip | 31.6 cr/s = **$0.063 per second** | ledger: 158 cr / 5 s, 284 cr / 9 s |
| Nano Banana Pro still | 40 cr = **$0.08** | ledger |
| Redo allowance | x1.5 on everything | this series' own history (many `DEFECTIVE_` / `SUPERSEDED_` files) |

Three numbers per film below: first-take cost, with-redos cost, and what it buys.

---

## 4. Per episode

Legend: **EX** = existing clip, $0. **RE n** = new n-second Kling clip of an existing approved still. **NEW n** = new still + new n-second clip. Times are seconds on the film; frames = seconds x 30.

### 4.1 ep08 Can Any Good Thing - PILOT (64.03 s) - full detail in section 5
New: 4 stills, 34 s. First take **$2.47**, with redos **$3.70**.

### 4.2 Jacob's Ladder (56.52 s) - build second, pairs with ep08
Shipped cut: `F:\slk\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_rewrite_v4\panel_jl\video\jacobs_ladder_v3_sfx.mp4`. Clips live in `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_01_jacobs_ladder\`. Uplift folder: `...\panel_jl\uplift\`.
Note: `assemble_jl_v3.py` lists a last unit `f02b` (Jacob asleep) from 50.45 s, but the shipped film shows F04 there (frames at 52 s and 55 s). Trust the film, not the script.

| # | Time | Words | Shot | Source |
|---|---|---|---|---|
| 1 | 0.00-3.45 | Jacob tricked his blind father and took his brother's blessing. | front cover (woodcut) | EX 4.0 `_style_test_durer_woodcut\front_cover_woodcut.mp4` |
| 2 | 3.45-7.40 | Now Esau wanted him dead. He ran. | **F01** (never used in v3) | EX 4.0 `the_ladder_f01_9x16.mp4` |
| 3 | 7.40-12.35 | What would God say to a man like that? He lay down... stone for his pillow. | F02 | EX 5.04 |
| 4 | 12.35-20.60 | In a dream he saw "a ladder set up on the earth"... "ascending and descending on it." | F03 | RE 9 |
| 5 | 20.60-29.65 | The LORD stood above it and promised: "I will not leave thee." Before Jacob did anything to make things right, God promised to stay. | F04 | RE 10 |
| 6 | 29.65-32.30 | Jacob woke afraid: "Surely the LORD... | F05 | EX 5.04 |
| 7 | 32.30-37.25 | ...is in this place; and I knew it not." (+1.5 s silence) | F06 | EX 5.04 |
| 8 | 37.25-43.70 | Centuries later, Jesus used that same picture about himself, calling himself the Son of man: | **new F07 - the Jesus page.** Jesus speaking to Nathanael by a fig tree; top panels: the same stone / the same ladder rail (same shape as F03) / "the Son of man". Caption: `that same picture`. Refs: series `jesus_ref.png`, ep08 `nathanael_ref.png`. | NEW 7 |
| 9 | 43.70-50.20 | "ye shall see heaven open, and the angels of God ascending and descending upon the Son of man." | **$0 choice: borrow ep08 F06** (Jesus under open heaven, caption "ascending and descending", 9.04 s; its header reads "SEQ: CAN ANY GOOD THING" - use S7 page turn in, so it reads as a leaf from the sister film). **Paid choice:** new JL F08 with the F03 ladder shape above Jesus. | EX 9.04 (or NEW 7) |
| 10 | 50.20-56.52 | Jacob never climbed that ladder. God came to him first. + 3 s hold | **new back cover** (woodcut, to match the front): dawn, the pillow stone set upright as a pillar, the open sky (Genesis 28:18). Baked title = spoken words: `GOD CAME TO HIM FIRST` / `GENESIS 28`. No ladder, no figure of Jesus needed here - the words land it. | NEW 7 |

Removes: 6 s cover freeze, both repeated pages, all boomerang. Adds Jesus on screen for 13 s.
Marks: S5 **footprints** (5 pencil prints walk up the left margin of F01) at "ran."@5.94; S1 ring on F03 panel 2 "first rung" at "ladder"@14.96; S3 **red circle** on the baked caption `"I am with thee"` at "leave"@23.93 - caption and spoken quote differ by design, so use S2 underline in graphite instead and give the red circle to F06's baked `"I knew it not"` at "knew"@34.69; S1 ring on F04 panels 1-2-3 ("this land" / "as the dust" / "whither thou goest") is NOT used - those words are not spoken in v3; S5 **two arrows up/down** beside the borrowed page at "ascending"@47.18 / "descending"@47.92; S6 tag `John 1:51` at "ye"@44.13 (optional).
Paid: 2 stills (F07, back) + 33 s = **$2.25 first take, $3.37 with redos**. With the paid F08: 3 stills + 40 s = **$2.77 / $4.15**.
Flag: F01's baked caption "the sun was set" is KJV (Genesis 28:11) but is not spoken in the v3 words. Harmless; owner call.

### 4.3 ep07 The Bier He Touched (72.03 s)
Sync is already close. Three of its eight pictures are zooms on a still (F03, F04, back cover).

| # | Time | Words | Shot | Source |
|---|---|---|---|---|
| 1 | 0.00-7.70 | A widow was walking behind her only son's body... He was all she had left. | front cover (a real 8.04 s clip, and the picture IS the scene) | EX |
| 2 | 7.70-13.00 | The law was simple: touch a dead man, and you were unclean. | F01 | EX 6.04 |
| 3 | 13.00-17.00 | Everyone kept their distance. That was survival, not cruelty. | new F01B: the crowd pressed back along the wall, a bare strip of road between them and the bier. Caption `kept their distance`. | NEW 5 |
| 4 | 17.00-19.70 | Jesus walked toward her instead of away. | new F02A: sandalled feet walking toward us through the gap (F02's own top panel 2, made the big picture). Caption `toward her`. | NEW 3 |
| 5 | 19.70-25.50 | And when the Lord saw her... "Weep not." | F02 | EX 7.04 |
| 6 | 25.50-30.00 | Then he touched what no one else would touch: and he came and touched the bier, | **HERO 1** new F03A, tight: only His hand coming down on the wooden pole/rail, bearers' feet behind. Hand lands in the first 2 s, then holds. The shroud is out of frame (cloth is what broke the old clip). Caption `touched the bier`. | NEW 5 |
| 7 | 30.00-34.00 | and they that bare him stood still. | F03 wide, as a real clip: bearers' heads turn, hands lower; shroud and Jesus' hand do not move. | RE 5 |
| 8 | 34.00-40.20 | Under that same law, the touch should have made him unclean. It didn't work that way with him. | new F03B: His hand resting on the wood, clean; the stain on the boards dry and pale nearest the hand (the episode's own "stain dies of the touch" geometry). Caption `it didn't work that way`. | NEW 7 |
| 9 | 40.20-44.60 | And he said, "Young man, I say unto thee, Arise." | **HERO 2** F04 as a real clip: He speaks, the widow's clasped hands tighten, a bearer looks up. Nothing on the bier moves. | RE 5 |
| 10 | 44.60-50.55 | And he that was dead sat up, and began to speak. And he delivered him to his mother. | F05 | EX 6.04 |
| 11 | 50.55-56.50 | Death didn't spread from the boy to Jesus. Life spread from Jesus... | F06 | EX 6.04 |
| 12 | 56.50-61.30 | ...to the boy. That is still the only direction he touches anything dead in you. | new F06B: His open hand reaching toward us, the road behind. Caption `the only direction`. | NEW 5 |
| 13 | 61.30-66.00 | Not to catch what's wrong with you - to give you what's his instead. | new F06C: mother and son walk in through the gate, his hand in hers, the bier left against the wall. Caption `what's his instead`. | NEW 5 |
| 14 | 66.00-72.03 | He touched a funeral, and it became a homecoming. + hold | **HERO 3** back cover as a real clip: door light warms, dust motes drift. Cloths and the blue hook stay exactly as drawn. | RE 7 |

Marks: S5 **dashed gap line** between crowd and bier on F01B at "distance."@13.90; S4 arrow along the feet's direction on F02A at "toward"@18.06; S8 tick burst at the bearers' feet on shot 7 at "still."@32.44 (on the SFX hit); S3 **red circle** on F04's baked `Arise` at "Arise."@43.90; S5 **the reversed arrow** on F06 (blank right margin): a grey arrow boy -> Jesus draws at "Death"@51.60, gets one cross-out stroke at "Jesus."(~53.3), then a firm arrow Jesus -> boy at "Life"@54.30; S2 underline on the baked `Life spread from Jesus` is skipped (too close in time).
Paid: 6 stills + 47 s = **$3.45 first take, $5.18 with redos**. Optional +1 still +3 s ($0.27): a close shot of the widow for "He was all she had left" at 5.2-7.7.
Not a picture fix, owner call: back cover says NUMBERS 19:11 (a planned link to ep02). A new viewer may not get it.

### 4.4 ep11 Where Are the Nine (83.61 s)
Best-paced film, most broken clips. `unit_timing.json` already holds real times.

| # | Time | Words | Shot | Source |
|---|---|---|---|---|
| 1 | 0.00-3.14 | Jesus told ten men with leprosy to go... | front cover | EX 4.04 |
| 2 | 3.14-9.10 | ...before a single one of them was healed. They were cleansed on the road. Only one of them came back. | F01 | EX 6.04 |
| 3 | 9.10-12.60 | They'd stood at a distance, as their disease required, | new F01B: the measured stretch of empty road between the ten and Jesus, seen from the side. Caption `at a distance`. | NEW 4 |
| 4 | 12.60-18.55 | and cried out, "Jesus, Master, have mercy on us." | F02 | EX 6.04 |
| 5 | 18.55-24.50 | He told them, "Go shew yourselves unto the priests." They obeyed before they could see any difference. | **F03 - today a frozen picture.** Real clip: His raised hand lowers, the men look at each other, one starts to turn. | RE 6 |
| 6 | 24.50-26.60 | "And it came to pass, that, as they went, | F04 | EX 4.04 |
| 7 | 26.60-29.70 | they were cleansed." | new F04B - **the miracle, never really shown**: one walking man's forearm, the pale patches gone; he has stopped and stares at it. Caption `they were cleansed`. | NEW 4 |
| 8 | 29.70-35.65 | Nine kept going. One turned back, "and with a loud voice glorified God, | F05 (shipped clip morphs its top panels into red-roofed farmhouses) | RE 6 |
| 9 | 35.65-41.70 | and fell down on his face at his feet, giving him thanks: and he was a Samaritan." | F06 (shipped clip zooms and adds vapour) | RE 7 |
| 10 | 41.70-47.20 | Jesus asked it out loud, naming exactly what nine men had skipped: "Were there not ten cleansed? | F07 (shipped clip zooms until the caption is cut, adds a glow) | RE 6 |
| 11 | 47.20-50.60 | but where are the nine? | new F07B: the empty road over the hill (F07's own top panel 2 made big). Caption `where are the nine?`. | NEW 4 |
| 12 | 50.60-55.20 | There are not found that returned to give glory to God, save this stranger." | F08 | EX 5.04 |
| 13 | 55.20-62.10 | To the one still on his face, he said, "Arise, go thy way: thy faith hath made thee whole." | F09 | EX 7.04 |
| 14 | 62.10-66.60 | Nine had exactly what they'd asked for, and kept walking. | new F09B: nine small figures, backs to us, going over the rise. Caption `kept walking`. | NEW 5 |
| 15 | 66.60-74.50 | One turned back to him. Luke calls it thanks. Jesus calls it faith. | **F10 redrawn - the face fix.** Same Samaritan as F06-F09 (balding, grey, short beard): chain a face crop from F09 as a ref + the "no other figure looks like this" clause. Same caption. Camera locked, motif still. | NEW 8 |
| 16 | 74.50-77.70 | That question didn't end with the nine. | new F10B: the empty road from the viewer's eye, one pair of footprints turned round. Caption `didn't end with the nine`. | NEW 4 |
| 17 | 77.70-83.61 | Go back and find him - at his feet, not on the road. + hold | back cover | EX 6.04 |

Marks: S5 **dashed distance line** with two end ticks on F01B at "distance,"@11.62; S5 **nine footprints up the margin, one pair turned back** on F05 at "Nine"@29.94 then "One"@31.52; S5 **nine empty pencil outlines** sketch in along the road on F07B at "nine?"@49.50; S3 **red circle** on F08's baked `stranger` at "stranger."@54.70; S2 underline on F10's baked `faith` at "faith."@72.34.
Paid: 6 stills + 54 s = **$3.89 first take, $5.84 with redos**. The face fix alone (shot 15): 1 still + 8 s = **$0.59 / $0.88**.
Era note: after RE of F05 check the still's own village panel at 2x for roof shape before paying for the clip.

### 4.5 ep02 The Ashes That Made Clean (61.93 s)
Only 4 pages for 62 s. More than half the film is fill today. Jesus is never on screen.

| # | Time | Words | Shot | Source |
|---|---|---|---|---|
| 1 | 0.00-3.95 | A man touches a dead body - not sin, just proximity to a grave - | front cover | EX 4.0 |
| 2 | 3.95-7.90 | and by nightfall, the law calls him unclean. | F02 (its baked caption is exactly these words) | EX 4.0 |
| 3 | 7.90-10.30 | He cannot cleanse himself. | new F02B: he scrubs his own palm with dust; the mark stays. Caption `cannot cleanse himself`. | NEW 3 |
| 4 | 10.30-17.40 | Someone else must burn a heifer to ash, mix it with water - and becomes unclean too, just for making it. | F01 | RE 8 |
| 5 | 17.40-23.20 | Scripture says: "He that toucheth the dead body of any man shall be unclean seven days... | new F02C: the man alone outside the camp line, seven stones set in a row beside him. Caption `unclean seven days`. | NEW 7 |
| 6 | 23.20-29.20 | he shall purify himself with it on the third day, and on the seventh day he shall be clean." | new F02D: a clean man brings the water and a hyssop sprig to him across the gap. Caption `on the third day`. | NEW 7 |
| 7 | 29.20-32.30 | You don't have to have sinned to feel unclean. | new F03A: his face, close, looking at his hand. Caption `to feel unclean`. | NEW 4 |
| 8 | 32.30-39.30 | Living close to death - a grave you can't stop visiting - can leave a stain water alone can't reach. | F03 (he lays one more stone, the hand stays, shoulders drop) | RE 8 |
| 9 | 39.30-46.20 | Hebrews says the ashes could only point forward: "How much more shall the blood of Christ... | F04 | EX 7.04 |
| 10 | 46.20-49.60 | purge your conscience from dead works to serve the living God?" | new F04B: outside a city wall, far off, a single cross on a hill, a hyssop stalk in the near corner (John 19:29). The only place the film shows where the ashes pointed. Caption `the blood of Christ`. Needs `/bible-check`. | NEW 4 |
| 11 | 49.60-58.10 | He touched what makes us unclean, and did not become unclean - so we could finally be. | new F05: the front cover's fallen man again, and a clean hand (the back cover's sleeve) reaching down to him - the cover's reach, answered. Caption `He touched what makes us unclean`. | NEW 9 |
| 12 | 58.10-61.93 | Ready to let Him make you clean? + hold | back cover | EX 4.0 |

Marks: S5 **seven tally strokes** beside F02C at "seven"@22.22, then on F02D stroke 3 gets a ring at "third"@25.06 and stroke 7 at "seventh"@26.42 (the tally is redrawn on F02D, same place); S1 ring on F01 panel 3 "the burning" at "ash,"@12.08; S3 **red circle** on F03's baked `stain` at "stain"@36.70; S6 tag `Hebrews 9:14` on F04 at "blood"@44.14 (optional).
Paid: 6 stills + 50 s = **$3.64 first take, $5.46 with redos**.

### 4.6 ep10 She Loved Much (106.29 s)
Free wins first: the hook says "No water. No kiss. No oil." while the cover is on screen; F01's three panels show exactly those three things. And the title-free cover clip from the 2026-11-08 test exists.

| # | Time | Words | Shot | Source |
|---|---|---|---|---|
| 1 | 0.00-2.00 | No water for his feet. | front cover | EX 4.04 |
| 2 | 2.00-9.95 | No kiss. No oil. That's what Simon the Pharisee never gave Jesus at his own table. | F01 (panels "no water / no kiss / no oil", caption "at his own table") | EX 8.04 |
| 3 | 9.95-13.90 | A woman he hadn't invited walked in anyway, and gave him all three. | the **title-free cover clip** (she stands at the lit door): `...\_bakeoff_format_v2\B1\ep10_cover_notitle_try1.mp4` | EX 4.04 (known small flaw: soft patch on the wall where the title was) |
| 4 | 13.90-21.85 | "A woman in the city, which was a sinner... brought an alabaster box of ointment, and stood at his feet behind him weeping, | F02 | EX 8.04 |
| 5 | 21.85-25.00 | and began to wash his feet | **HERO** new F03A, from above: one tear lands on a dusty foot. No face, no mouth. Caption `with tears`. | NEW 4 |
| 6 | 25.00-28.60 | with tears... and kissed his feet, | new F03B, from behind her shoulder: her loosed hair wipes the foot; her face is hidden by the hair. Caption `her hair`. | NEW 4 |
| 7 | 28.60-32.50 | and anointed them with the ointment." | new F03C: her hands tip the alabaster jar; oil runs over the foot. Caption `the ointment`. | NEW 4 |
| 8 | 32.50-40.45 | Simon thought it, not out loud: "This man, if he were a prophet, would have known... for she is a sinner." | F04 | EX 8.04 |
| 9 | 40.45-43.40 | Jesus answered anyway. | new F04B: Jesus' head turns from her to Simon. Caption `answered anyway`. | NEW 3 |
| 10 | 43.40-53.30 | A creditor had two debtors... "he frankly forgave them both" | F05 | EX 10.04 |
| 11 | 53.30-58.30 | - frankly, that's freely. "Which of them will love him most?" Simon hedged: | F06 | EX 7.04 |
| 12 | 58.30-61.90 | "I suppose that he, to whom he forgave most." | new F06B: Simon close, eyes drop, a small shrug. **Same Simon as F04/F08** (bearded, head-cloth) - shipped F06 draws him bald. Caption `I suppose`. | NEW 4 |
| 13 | 61.90-68.85 | Jesus turned to her, and asked Simon: "Seest thou this woman?" Simon had seen the sin. Never the woman. | F07 | EX 7.04 |
| 14 | 68.85-78.00 | "Her sins, which are many, are forgiven; for she loved much: but to whom little is forgiven, the same loveth little." | F08 | EX 10.04 |
| 15 | 78.00-83.90 | Forgiven first - love was the receipt, not the price. | new F08B: her empty open hands, the empty jar on the floor beside her. Caption `the receipt, not the price`. | NEW 6 |
| 16 | 83.90-91.85 | "Thy faith hath saved thee; go in peace." Not thy tears. Not thy ointment. | F09 | EX 8.04 |
| 17 | 91.85-98.40 | Thy faith. That answer holds for whoever still carries what Simon called her - a sinner. | new F09B: she walks out through the door into the street light, face up, the jar left behind. Caption `Thy faith`. | NEW 7 |
| 18 | 98.40-106.29 | She came in carrying an alabaster box. She left carrying his peace. + hold | back cover (the empty room, the jar) | EX 8.04 |

Marks: S1 rings on F01 panels 2 then 3 at "kiss."@2.50 and "oil."@4.34 (panel 1's word is over the cover; leave it); S5 **two tally stacks** in F05's blank margin: a tall one at "five"@46.46, a short one at "fifty."@48.42, one stroke through both at "both"@52.20; S3 **red circle** on F08's baked `forgiven` at "forgiven;"@71.08; S2 underline on F09's baked `Thy faith` at "Thy faith."@91.58 (cut is at 91.85, so draw it 8 f early); S5 on F08B: a small pencil "receipt" tick-mark beside the empty hands at "receipt,"@80.20.
Paid: 7 stills + 32 s = **$2.58 first take, $3.87 with redos**.
Continuity that stays (not in the quote): Jesus sits upright in F04/F05 and reclines in F01-F03; her head-cover comes and goes. Optional: redraw F06 with the right Simon (+1 still + 7 s, $0.52) - shot 12 already hides the worst of it.
Still 106 s long. Not a picture problem; noted only.

### 4.7 ep13 The Cross That Wasn't His (106.43 s)
Words are the freshest of the eight. Walking gives real motion. Real timing already in use. Problem: sameness, and a frozen opening.

| # | Time | Words | Shot | Source |
|---|---|---|---|---|
| 1 | 0.00-5.00 | The man who would carry the cross of Jesus was walking the other way. | **front cover - today a frozen still.** Real clip: Simon walks on the spot toward us, dust at his feet; the group in the gate barely shifts. (Two earlier tries failed: he walked out of frame / merged with the group. State "he stays in the same place in the frame".) | RE 5 |
| 2 | 5.00-12.95 | Mark says the soldiers "led him out to crucify him. And they compel one Simon a Cyrenian, who passed by, | F01 | EX 8.04 |
| 3 | 12.95-15.10 | coming out of the country." | new F01B: Simon's face, close, eyes on the road, not on them. Caption `passed by`. | NEW 3 |
| 4 | 15.10-23.05 | Jesus, out of the city. Simon, in from the country. Same road. They put the cross on Simon's... | F02 | EX 8.04 |
| 5 | 23.05-26.10 | ...back. Nobody asked him. | new F02B: a soldier's hand shut on Simon's arm (F09's "forced out" panel, made big). Caption `Nobody asked him`. | NEW 4 |
| 6 | 26.10-34.05 | Luke says, "on him they laid the cross, that he might bear it after Jesus." Simon turns, and walks out too. | F03 | EX 8.04 |
| 7 | 34.05-37.40 | Now he is through the gate. | new F03B: his sandal crossing the worn threshold stone, the beam's foot dragging behind. Caption `through the gate`. | NEW 4 |
| 8 | 37.40-42.35 | In the King James Bible, outside is "without." | F04 | EX 5.04 |
| 9 | 42.35-50.20 | The sin offering, an animal killed for the people's sin, had its blood carried into the sanctuary, God's holy tent. | F05 | EX 10.04 |
| 10 | 50.20-54.30 | Its body went out, burned "without the camp." | new F05B - **the Old Testament made the big picture**: two men carry the body on a pole past the last tent toward a fire on open ground. Older, browner paper. Caption `without the camp`. | NEW 5 |
| 11 | 54.30-64.25 | Then it says of Jesus: "Wherefore Jesus also, that he might sanctify the people with his own blood, suffered without the gate." | F06 | EX 10.04 |
| 12 | 64.25-67.00 | Out there, where Simon is walking. | new F06B: the road outside the wall from high up, Simon small on it. Caption `out there`. | NEW 3 |
| 13 | 67.00-72.95 | Hebrews turns to you: "Let us go forth therefore unto him without the camp, | F07 | EX 6.04 |
| 14 | 72.95-77.20 | bearing his reproach." Reproach is shame. | new F07B: Simon's face under the beam; bystanders at the roadside stare and point. Caption `Reproach is shame`. | NEW 5 |
| 15 | 77.20-82.15 | Bearing it is carrying it, as Simon carried the wood. | F08 | EX 5.04 |
| 16 | 82.15-90.10 | Simon was forced out. You are asked. Turn on your own road, and carry his shame after him, | F09 | EX 8.04 |
| 17 | 90.10-96.50 | freely this time. Only the shame. | new F09B: an open, offered hand (F09's "asked" panel, made big), the road behind it. Caption `Only the shame`. | NEW 7 |
| 18 | 96.50-106.43 | He went out through that gate first, and the atoning, the dying, the finishing, that was his, with his own blood. + hold | back cover (its baked title is the spoken line) | EX 10.04 |

Marks: S5 **two arrows on the road** on F01, one out of the gate, one in, meeting, at "out"@7.36 and "country."(~14.0 - so draw arrow 2 on F01B's margin instead, pointing the other way); S5 **in/out plan** in F05's blank margin: a small square (camp) with a box (tent), an arrow in at "blood"@46.48; on F05B the same square redrawn, an arrow out at "out,"@51.28; S3 **red circle** on F04's baked `without` at "without."@40.92; S1 rings on F09 panels 1 then 2 at "forced"@82.80 and "asked."@85.30; S2 underline on F07's baked `Let us go forth` at "forth"@69.86.
Paid: 7 stills + 36 s = **$2.83 first take, $4.25 with redos**.
Optional lifts: (a) F05A, the priest carrying the bowl in through the tent curtain for 42.35-50.20, replacing F05 (+1 still + 8 s, $0.59) - fixes the film's weakest 10 s; (b) a far hill with three crosses for "the dying, the finishing, that was his" at 99.5-103.5 is NOT recommended: it would split the back cover while its own title is being spoken.
Not reopened: the cross sometimes reads as an X (F04, F08).

### 4.8 ep06 Talitha Cumi (53.9 s) - nothing required
Vector style, real clips, hard cuts, Remotion pills. Shipped words = `...\swirls_episode_06_talitha_cumi\short_g5\narration.md`; word times = `...\short_g5\narration.alignment.json`. The pencil kit does not apply (no paper page).
- $0, optional, in `_remotion\src\TalithaCumi.tsx`: make the second strike through "Too late." (Jesus overrules it) a clearly different hand - one firm stroke, 4 f, against the first slow shaky one.
- Paid, optional: three 3 s close shots inside 20-34 s (His hand closes round hers / His face before "Talitha cumi" / her eyes open). 3 stills + 9 s = about $0.81 first take, $1.22 with redos, on whatever model made the vector clips (re-quote).
- **It can post now.**

---

## 5. PILOT: ep08 Can Any Good Thing - full change list

Why this one: (1) its words are settled - no insight is waiting on it, so nothing bought is thrown away later; (2) it shows every part of the recipe: backwards play on 6 of 8 units today, a 5 s sync error, a long hold on the back cover; (3) it has the kit's best single doodle ("I saw thee"); (4) it is short (64 s) and cheap; (5) it hands a page to Jacob's Ladder and takes one back, so film 2 is half-built by film 1. It does not test a hero re-animation - that risk is kept out of the pilot on purpose and comes third (ep07).

Machine-readable copy: `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\pilot_ep08_uplift.json`
Episode: `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_08_can_any_good_thing\`
Shipped film (never touched): `...\swirls_episode_08_can_any_good_thing\CAN_ANY_GOOD_THING_final_sfx.mp4` (64.033 s, 720x1280)
New output: `...\swirls_episode_08_can_any_good_thing\uplift\ep08_uplift_final.mp4` (1921 frames, 1080x1920)

### 5.1 Shot list (30 fps; shot = frames f0..f1, clip plays from its own frame 0 at 1.0x)
| Shot | Frames | Seconds | Page | Words under it | Clip | Was |
|---|---|---|---|---|---|---|
| S01 | 0-108 | 0.00-3.60 | front cover | A man insulted Jesus behind His back. Jesus complimented him to his face. | EX `front_cover.mp4` 4.00 | held 7.4 s, played backwards |
| S02 | 108-216 | 3.60-7.20 | F01 | Philip told Nathanael the news: the Messiah - Jesus, of Nazareth. | EX f01 5.04 | arrived at 7.4 s, 4 s late |
| S03 | 216-365 | 7.20-12.17 | F02 | Nathanael's answer: "Can there any good thing come out of Nazareth?" Philip did not argue - he invited. | EX f02 5.04 | arrived at 14.5 s, 7 s late |
| S04 | 365-579 | 12.17-19.30 | F03 | Jesus spoke first: "Behold an Israelite indeed, in whom is no guile!" Nathanael asked: | **RE 8** | 4 s on screen, during the wrong line |
| S05 | 579-636 | 19.30-21.20 | **F03B** | "Whence knowest thou me?" | **NEW 3** | - |
| S06 | 636-909 | 21.20-30.30 | F04 | Jesus answered: "Before that Philip called thee, when thou wast under the fig tree, I saw thee." A moment only heaven had seen - named. | **RE 10** | 5 s clip + 4.3 s backwards |
| S07 | 909-981 | 30.30-32.70 | **F05A** | The doubt did not fade. It fell. | **NEW 3** | - |
| S08 | 981-1191 | 32.70-39.70 | F05 | Nathanael said: "Rabbi, thou art the Son of God; thou art the King of Israel." | EX f05 9.04 | 9 s clip + 3.2 s tail loop |
| S09 | 1191-1340 | 39.70-44.67 | **F05B** | And Jesus went further: "Thou shalt see greater things than these... | **NEW 5** | - |
| S10 | 1340-1560 | 44.67-52.00 | F06 | Hereafter ye shall see heaven open, and the angels of God ascending and descending upon the Son of man." | EX f06 9.04 | ok |
| S11 | 1560-1680 | 52.00-56.00 | Jacob's Ladder F03 | That is Jacob's ladder - the one Jesus said He is, standing open, permanently. | EX `..\swirls_pilot_01_jacobs_ladder\the_ladder_f03_9x16.mp4` 5.04 | - |
| S12 | 1680-1806 | 56.00-60.20 | **F07** | He is not offended by honest questions. He already sees you, under your fig tree. | **NEW 5** | back cover, backwards |
| S13 | 1806-1921 | 60.20-64.03 | back cover | Come and see. + 3.1 s hold | EX `back_cover.mp4` 4.00 | held 10.4 s |

Hard cuts everywhere except one S7 page turn into S11 (frames 1556-1564). Every existing clip used is shorter on screen than its own length (checked: 3.60/4.00, 3.60/5.04, 4.97/5.04, 7.00/9.04, 7.33/9.04, 4.00/5.04, 3.83/4.00).
If the owner dislikes the borrowed page (S11): drop it and buy F06 as RE 12 instead (+$0.76).

### 5.2 New pictures (4 stills). Same `PageSpec` template, `panel_style="woodcut_hybrid"`, refs from `...\swirls_episode_08_can_any_good_thing\refs\` (`jesus_ref.png`, `nathanael_ref.png`, `philip_ref.png`), builds imported from the episode's `episode.py`. No NOTE line.
| Page | Big picture | 3 top panels (label) | Caption (spoken words) | Motif | Clip motion (two beats) |
|---|---|---|---|---|---|
| F03B | Nathanael, medium close, a step back, brow knotted, one hand half raised - caught. Jesus' shoulder at the frame edge only. | his narrowed eyes (`caught`) / an empty road (`never met`) / a fig leaf (`the tree`) | `"Whence knowest thou me?"` | none | he draws back half a step; then his hand lowers |
| F05A | Low angle: Nathanael's knees meeting the dust, hem and sandals, Jesus' feet standing still in front of him. No faces. Leave blank paper left of the knees for the tick burst. | a cracked clay cup (`the doubt`) / dust rising (`it fell`) / two pairs of feet (`before him`) | `It fell.` | none | knees land in the first second, dust settles; then the hem stills |
| F05B | Jesus, medium, face lifted, one open hand raised toward the sky; Nathanael small and low, looking up the same way. Wide blank sky top third. | Jesus' eyes lifted (`further`) / a seam of light in cloud (`greater things`) / Nathanael's upturned face (`than these`) | `greater things than these` | one small Stage-2 thread at the raised hand, static | His hand rises a little and holds; then cloud drifts, robe hem moves |
| F07 | From above, like F04: the same fig tree, the same worn ground - and nobody there. A woven mat and a pair of sandals left under it. Blank right margin for the arrow. | the mat (`your place`) / leaf shade on the ground (`already seen`) / an open road (`come and see`) | `under your fig tree` | the same blue contour ring as F04, static | leaves stir, dappled light slides; then one leaf drops onto the mat |
Each still: check cloned people, hands, era (no modern buildings, no European roofs, mat = woven reed), and all baked words at 2x zoom before any clip is bought.

### 5.3 Re-animated pages (2 clips from approved stills)
- **F03, 8 s:** beat 1 (0-3 s) Nathanael's stride slows to a stop; beat 2 (3-8 s) Jesus' raised hand lowers a little, robe hems and grass move. The three figures behind stay as drawn. Blue thread and flower: exactly as drawn, whole clip. (Old defect on this page: "stuck legs".)
- **F04, 10 s:** beat 1 (0-4 s) leaves stir, dappled light slides across the ground; beat 2 (4-10 s) the man under the tree lifts his head once, slowly, and holds. Camera locked top-down. Cloud and contour ring: exactly as drawn.

### 5.4 Pencil marks (8 marks + 1 page turn; spacing and count pass rule 1.3)
| Id | Frame | Word (time) | Shot | Device | What is drawn |
|---|---|---|---|---|---|
| M1 | 276 | good @9.28 | S03 F02 | S2 underline | under the baked `"any good thing"`, bottom left |
| M2 | 534 | no @17.88 | S04 F03 | S3 circle, **red** | round `no guile` in the baked caption. The film's one red mark. |
| M3 | 669 | Before @22.38 | S06 F04 | S1 ring | round top panel 1 `unseen prayer` |
| M4 | 805 | I @26.90, saw @27.14, thee @27.40 | S06 F04 | S5 idea doodle | a pencil eye in the right margin (10 f), then a dashed line down to the man under the tree (14 f from frame 815). The dash lifts over the blue ring. Holds through "A moment only heaven had seen - named", fades by 899. |
| M5 | 962 | fell. @32.12 | S07 F05A | S8 tick burst | 3 ticks beside the knees, on the SFX thud if there is one |
| M6 | 1067 | Son @35.64 | S08 F05 | S2 underline | under the baked `the Son of God` |
| M7 | 1468 / 1497 | ascending @49.00 / descending @49.96 | S10 F06 | S5 idea doodle | an up arrow, then a down arrow, in the blank left margin beside the picture |
| M8 | 1773 | your @59.16 | S12 F07 | S4 margin arrow | from the right margin to the empty mat |
| T1 | 1556-1564 | - | S10 -> S11 | S7 page turn | F06 slides away, the Jacob's Ladder page is under it |
No mark on the covers, none in the last 3.8 s.

### 5.5 Build steps (each with its check)
| Step | Do | Cost | Pass when |
|---|---|---|---|
| A1 | Build `swirls_kit` + `check_swirls_uplift.py` (section 1.4) | $0 | renders a test comp; gate fails on a planted overlap |
| A2 | `uplift\cut_uplift.py`; run it with the 6 missing shots as **grey slugs labelled NEW SHOT** | $0 | 1921 frames; audio stream identical to shipped; every EX shot under its clip length |
| A3 | Overlay M1, M2(on slug), M3-M4(on slug), M6, M7, T1; owner looks at this **animatic** | $0 | owner says the pencil layer is right (or names what to change) |
| B1 | Quote from `openart_model_cost`, owner's yes | - | written price, cap $4.50 |
| B2 | 4 stills (F03B, F05A, F05B, F07) through the OpenArt bridge; eye + 2x text check | ~$0.32 | all 4 pass section 5.2 checks |
| B3 | 6 clips (8, 3, 10, 3, 5, 5 s); 4 checks of section 2.7 on each | ~$2.15 | zoom 1.000 +-0.010, not frozen, text and motif unchanged |
| B4 | Re-measure mark positions on the real frames; final cut; Remotion; mux | $0 | gate green; `check_landing_hold.py` green |
| B5 | One owner page: old vs new, side by side. Shipped file and `FINAL_VIDEO.txt` untouched until yes. | $0 | - |
| B6 | Log actual credits to `data\spend_ledger.jsonl` | $0 | - |
Independent review: this spec is a spend-bearing plan, so it needs `independent_review.py --type plan` (plus the Fable seat) before B1.

---

## 6. Build order and quote

| # | Film | Why here | New stills | New clip s | First take | With redos (x1.5) |
|---|---|---|---|---|---|---|
| 0 | Kit + gate + ep08 animatic | everything else stands on it | 0 | 0 | $0 | $0 |
| 1 | ep08 Can Any Good Thing (pilot) | settled words, shows the whole recipe | 4 | 34 | $2.47 | $3.70 |
| 2 | Jacob's Ladder | shares pages with ep08; gets its Jesus page | 2 | 33 | $2.25 | $3.37 |
| 3 | ep07 The Bier He Touched | 3 of the 6 fake clips | 6 | 47 | $3.45 | $5.18 |
| 4 | ep11 Where Are the Nine | face fix + 4 bad clips | 6 | 54 | $3.89 | $5.84 |
| 5 | ep13 The Cross That Wasn't His | freshest words; frozen opening | 7 | 36 | $2.83 | $4.25 |
| 6 | ep10 She Loved Much | the feet; longest film | 7 | 32 | $2.58 | $3.87 |
| 7 | ep02 The Ashes | needs the most new picture | 6 | 50 | $3.64 | $5.46 |
| - | ep06 Talitha Cumi | nothing needed; can post now | 0 | 0 | $0 | $0 |
| | **Total** | | **38** | **286** | **$21.11** | **$31.67** |

(With the paid JL F08 page instead of the borrowed one: 39 stills, 293 s, $21.64 / $32.46.)

Asked-for line items, inside the totals above:
| Item | What | First take | With redos |
|---|---|---|---|
| Stretched clips, all 7 films | 286 s of new clip + 38 stills | $21.11 | $31.67 |
| Jacob's Ladder Jesus page | 1 still + 7 s (F07); second page borrowed at $0 | $0.52 | $0.78 |
| Still-for-clip hero moments (6, not 3) | ep07 touch (still + 5 s + 5 s), ep07 Arise (5 s), ep07 back (7 s), ep10 feet (3 stills + 12 s), ep11 F03 (6 s), ep13 cover (5 s) | $3.16 | $4.74 |
| ep11 face fix | F10 redraw + 8 s | $0.59 | $0.88 |

Optional extras (not in the totals): JL F08 $0.52 - ep13 priest page $0.59 - ep10 F06 redraw $0.52 - ep07 widow close $0.27 - Talitha 3 closes $0.81. All five: about $2.70 first take, $4.05 with redos.
**Quote to approve: $21 to $32 for the seven films, hard cap $35. Extras: up to $4 more.** About 10,600 to 16,000 OpenArt credits (17,500 at the cap). A yes to this covers pictures only.

$0 list (no approval needed beyond "go"): the kit, the gate, 7 re-timed cuts, about 45 pencil marks, 6 page turns, JL F01 put back in, ep10's hook moved onto F01, ep10's title-free cover clip re-used, the two borrowed pages, ep06's second strike.

---

## 7. Later - needs the words gate first (NOT in this pass)

These would change narration, so they wait for blind drafting, the 5-CLI panel + Fable, and a separate voice quote. If the owner means to do them, do them **before** buying shots for that film - new voice moves every cut.
- ep07: Elijah's line (1 Kings 17:21-23 -> Luke 7:15). Panel: USE. -> hold ep07's paid shots until decided.
- ep11: Naaman echo (Luke 4:27 -> Luke 17:18). Panel: USE, careful words ("echo"). -> hold ep11's paid shots until decided.
- ep06: Peter in the room (Mark 5:37 -> Acts 9:40). Careful words.
- ep08 / JL: "no guile" = Jacob (Genesis 27:35 -> John 1:47); "ye shall see" is plural. Not picked. If ever picked, the pilot's shots S04-S05 would move.
- ep02: "Ready to let Him make you clean?" is the tired closer shape. ep02's third-day line (Numbers 19:12) is medium risk.
- ep07 back cover verse (Numbers 19:11) and JL F01's unspoken caption: owner calls, not word changes.
If ep07 and ep11 are held for words, the picture order becomes: ep08, JL, ep13, ep10, ep02, then ep07 and ep11.

## 8. Honest limits
- I judged motion from frames plus measured first/last-frame alignment, not from watching playback with sound. The 6 "not a real clip" findings are measured; "feels dull" calls are not.
- Mark positions come from a 10x10 grid over small frames. They must be re-measured on the real 1080x1920 frame (gate G-KEEP) - especially motif boxes.
- Costs use this account's past billed rates. OpenArt's Kling limits (whole seconds 3-15) were confirmed on Higgsfield, not re-checked on OpenArt today: check `openart_model_form_get` ($0) first.
- New pages must match pages drawn in August-September. Style drift is the main quality risk; the refs folders exist for every film, and the redo allowance is there for it.
- The pencil layer is a design guess until real people see it. The mock is not a test. Recommend the owner's seed viewers see old vs new ep08 before films 2-7 are bought.
- This spec has not been through the outside panel yet (house rule for a spend-bearing plan).
