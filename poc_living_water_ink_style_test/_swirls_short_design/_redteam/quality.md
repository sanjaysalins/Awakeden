# Red team — quality escapes (Swirls SHORT design v3.1 + code on disk)

Scope: a bad 45 s film that passes every gate. Read-only, $0. Did not read any _review*, _independent_review*, _redteam* file.
Ran `_validate_swirls_short.py` (ALL PASS) and one $0 probe of `swirls_verify.judge_still_texts` (results quoted below).
"Design" = `SWIRLS_SHORT_PIPELINE_DESIGN_v3.md`. "Disk" = the code as it is today.

Probe results (`judge_still_texts`, expected caption `I am the voice`, frame `F04`):

| What Vision reads | Verdict |
|---|---|
| `I am — the voice` (em-dash) | **PASS** |
| `"I am the voice"` (added quote marks) | **PASS** |
| extra shot labels `MCU`, `POV` | **PASS** |
| `F05` where `F04` was asked | WARN only |
| `wildernes`, `I am the vioce` | WARN only |
| caption drawn twice, read as one string | WARN only |
| cover `JOHN 1:28` where `JOHN 1:23` was asked | WARN only |

---

## BLOCKER

**B1. Dash, quote marks and short shot labels pass the still audit outright (baked-text errors).**
How: `_norm_text` (swirls_verify.py:414-416) strips every non-alphanumeric character before matching, so a dash or quote mark is invisible. The "invented" rule needs 4+ letters (line 438), so `MCU`, `POV`, `INT`, `CU` pass. Near misses from 0.6 to 0.97 are only WARN (lines 463-466). So a wrong frame number, a wrong verse on the cover or a misspelt caption is only WARN, and `_report` (swirls_episode.py:130-139) treats WARN as passing. A caption drawn twice and read as one string is also only WARN. Design SWS-G9 (section 3 step 5) keeps the same fuzzy WARN band. The only safety is the session's 2x zoom.
Fix: judge punctuation on the raw string. Any of `— – - " “ ” …` in a seen text = FAIL. Any digit that differs from the expected one = FAIL (F0n, chapter:verse). Any extra token (even 1-3 letters) that is not in the plan = FAIL. A seen string that holds the same expected string twice = DOUBLED FAIL. Near-miss stays WARN only for a letter-level misspelling of 5+ letter words. Add these 7 cases to T4/T7.

**B2. The page_plan schema in the design does not match the code. Three gates silently go green.**
How: the design's `page_plan.json` has `full_figures`, `subjects` and a top-level `north_star` (section 3 step 3). The code reads `heads` (swirls_episode.py:106), `recurring` (swirls_short.py:412) and a per-unit `turn` (swirls_short.py:434). Result: the head / full-figure check gets `None` and is skipped (verify.py:454). SWS-G7a sees 0 recurring subjects and PASSES. The SWS-G8 "turn page" FAIL can never fire. Clones, vanishing figures and costume drift lose their only automatic check, and there is no error.
Fix: one schema, validated on load. Missing `full_figures` / `subjects` / `speaker` / `motion_carrier` on any unit, or no `north_star` = FAIL. `turn` is derived from `north_star`. Add a test: the design's own example plan must make the G7a and G8 FAIL cases fire.

**B3. A fixed PNG still ships the old MP4 (known defect #12). Three holes on disk.**
How: (a) `_animate_trim` returns True with "[skip] already exists" when the mp4 is there (swirls_episode.py:221-224). Fixing the PNG never re-renders the clip. (b) `clipqc` writes the CURRENT still's hash into `.clipqc.json` (swirls_short.py:723-724), so re-running clipqc ties the old clip to the new still, and G14 PASSES. (c) G14 at assemble checks `_unit_clip()`, a path built from the PNG name (swirls_episode.py:299-309). `assemble` actually uses `Unit.src` from `episode.py` (swirls_assemble.py:350). A `src` that points at an older or a different file is never checked. The design's receipt-based G14 fixes (b) only. It does not mention (a), (c), or the step 9 SFX script, which reads a hard-coded `CUT` file name (ep13 `build_sfx.py:50`) and is pinned by hand in `FINAL_VIDEO.txt`.
Fix: `animate` refuses when the mp4 exists and its receipt's `input_sha256` is not the current PNG. G14 runs over `MANIFEST.units[*].src`, comparing against the receipt `output_sha256`. `assemble` writes `assembly_receipt.json` (output sha + the 8 src shas). `FINAL_VIDEO.txt` and the SFX input must equal that output sha, and step 9 checks it.

**B4. A frozen or settled landing hold passes (known defect #10).**
How: on disk the only hold check is `freeze_check`. It is WARN only (swirls_short.py:666-692) and runs at the final assemble too (swirls_episode.py:311). The back clip is ordered with only +0.5 s (swirls_short.py:122), not the design's +2.0. So the used span runs into Kling's settled tail, where motion usually stops. The design's G15h (section 3 step 6) is not built (section 6 says DESIGNED). As designed, it can also be fooled three ways: (1) the bar is relative to the clip's own first 3 s, so a calm clip sets a near-zero bar that H.264 grain clears; (2) it takes the mean over 3 s, so motion that stops 1.5 s into the hold still passes; (3) a whole-frame mean counts a slow camera drift as "living motion".
Fix: an absolute floor first. Re-encode the clip's last used frame as a 3 s still through the same chain; the hold must be at least k x that noise floor (set k in T8). Measure in 3 x 1 s windows and fail if ANY window falls below the floor. Measure on the FINAL file (after score and SFX), not only on the clip. Until G15h passes T8, the back cover gets a played-through owner check that is recorded with `ok`.

**B5. Cover border has no automatic check at all (known defect #2).**
How: today's `STILL_V2_ROLE` has no border field (verify.py:398-408). The design adds a Vision `drawn_border` flag and DEFERS the pixel scan G10 (section 9.4). The defect history says this border "resists wording; verify by pixel scan" (EPISODE_ANALYSIS item 2) — a Vision read is just an eye again. `edge_scan` already exists, is tested and costs $0 (swirls_short.py:744-763), but nothing calls it. The 11 px scale-crop (section 1) does not remove an inset border.
Fix: wire `edge_scan` into `still` / `verify` for the covers now, as FAIL on covers and WARN on pages. Tune it on the shipped ep2/5/7/8 covers. Keep `drawn_border` as a second check.

## MAJOR

**M1. Speech bubbles, lips moving and invented motion in clips: no automatic check on disk; partial in the design.** The disk `clipqc` makes 5 frames at 216 px for a person to look at (swirls_short.py:719-722). The design's G13 has hard flags for bubble / new text / figure count, but nothing for **mouth movement**. A 2 fps strip cannot show lips moving, and the session plays only the back cover and clips with a WARN (step 6b). G5a's speech-verb list (swirls_short.py:309-311) has no `answers, replies, preaches, proclaims, lips, voice, announce, exclaim, pray, murmur`, so "John answers" in the pilot's f02 clip prose passes. Also: SWS-G8 trusts a hand-typed `speaker` field and never derives it from `narration-tagged.md`. Fix: derive `speaker` per unit from the tagged voices. Widen the verb list. In G13, add a mouth-region pixel-difference check on the speaking figure (box from the plan or the Vision read). Read the strip frames one by one at 540 px or more, not as a 216 px tile. Make "invented motion / prop moves" a hard flag on pages where the plan says that prop is still.

**M2. Characters and costumes drift between pages; no check compares pages with each other (known defect #3).** G9 reads each still on its own. G13 drift is soft WARN. G7a goes vacuous (B2). Fix: one cross-page Vision read of the north-star crop next to each page for every recurring subject (same costume, beard, cloth colour; Jesus matches the series ref), FAIL on a mismatch. At least, put the 8 stills on one contact sheet on owner page 4.

**M3. Motif presence and dosage are never checked on the render (and the motif can be animated in the clip).** G6 checks only the planned `motif_stage`. G9 has only `motif_bad_shape` and no "motif present / how many strokes". So f02-f06 with no motif ("the swirls was missing in the middle pages", ep2) or a motif on f01 / front passes. G13 has no motif field, so ink that glows or blobs in a clip (defect history item 4) is not flagged. Fix: add `motif_marks` (count + colour) to the G9 read and judge it against stage 0/1/2/3. Add `ink_changed` to G13 as a hard flag.

**M4. Phone readability is judged on the wrong thing and the caption may sit under the Shorts UI.** The go / no-go animatic holds the crisp STILLS (step 5). The film shows Kling clips, which soften and warp handwriting ("caption fades in clip", ep7). G13 flags only NEW text, not the planned caption going blurry. Section 4 rule 6 puts the caption "above 85% of frame height". That band is inside the bottom area the Shorts title, channel and buttons cover (roughly the bottom fifth). Nothing measures caption size or position in pixels. Fix: G13 must re-find every planned string on the clip's first, middle and last used frames (missing or below the match ratio = FAIL). Move the caption rule to above about 75% height and clear of the right-hand button column, and check it from a Vision bounding box. The phone review uses the draft film (page 6) as the readability decision, not only the animatic.

**M5. Cut on the wrong word / wrong page order.** On disk G1s compares token COUNTS only (swirls_short.py:97-101; design marks the sequence check DESIGNED). Nothing checks that `MANIFEST.units` order equals the `units.json` / `unit_timing.json` order. `assemble` walks the manifest order and looks up slots by tag, so two swapped units put each picture under the other's words. G4 never checks that the caption and labels are words spoken on THAT page (`lint_baked_text` takes no units text). Fix: an order-equality check (manifest, units.json, unit_timing, page_plan) at `plan` and `assemble`. In G4, caption = a contiguous token run of `units[tag]`, and each label must be in `units[tag]`.

**M6. Score dead air or a crushed score passes (known defect #11).** The copied ep16 checks run on the raw score parts, not on the mix. `check_no_dead_intro` returns on the FIRST audible 4 s window in the first 10 s, so a 4-8 s dead start passes — on a 45 s film that is the whole cover and part of f01 (generate_score_piano.py:86-99). The sweep uses 5 s mean windows at -55 dB, so a 2-3 s dead gap passes, and so does a dead hold at the end. Nothing checks that the score is at least `total` long, or that the two parts join without a gap. "Mix measured once, music 10-16 dB under the voice, up in the hold" (step 8) is not a gate, and the DuckProfile is copied from another score (memory: a duck does not carry over between scores). Fix: a `score_mix_gate` on the final mixed file. Music-only stem (or mix minus voice) 1 s windows: none below the floor anywhere from 0 to `total`. Under voice: music 10-16 dB below it. Hold: music at least X dB above its under-voice level. Score length at least `total`. FAIL, not WARN.

**M7. Character voices will sound robotic.** Step 2 runs `per_turn_synth.py ... --stability 0.65`. The owner rule (memory "Dialogue needs emotion cues") is stability 0.3 with 2 takes for character lines; 0.65 is the setting that was called robotic. Only the owner's ear catches this. Fix: character turns at 0.3, two takes each, the pick recorded in the `voice_ear` gate; the narrator keeps its own setting.

**M8. Overrides are per gate name, not per unit, and are not tied to the image.** `apply_overrides` keys on `g.gate` (verify.py:600-616). The G9 names have no unit id (`SWS-G9[bubble]`), so one override clears bubbles on every page and every later reroll. Nothing checks for the owner's words (the design promises that for G15h). Fix: key on `gate + unit + sha256 of the PNG/mp4`; an override for a changed file is void. G15h / G13 hard-flag overrides need a dated owner quote, the same check as `--note`.

**M9. Output can ship at 720p.** `EpisodeManifest` defaults to `w=720, h=1280` (swirls_assemble.py:68-69). `encode` stretches to that size (line 115). No gate checks the final resolution. 720p was named as a viewer gap (EPISODE_ANALYSIS, Elevate panel). Fix: G15 FAILs unless the output is 1080x1920 at 30 fps; trim episodes refuse the default size.

## MINOR

- **m1. A/V tolerance is loose.** SW-A1 / SW-A3 allow 0.3 s (check_landing_hold.py:31; verify.py:562). The design wants one frame. The math itself is sound: trim video runs to `total`, `apad=whole_dur` on both the draft and the scored path, and the `mix_tail` clone falls after `-t total`. step 9's `sfxlib.build` re-muxes with `-shortest` (sfx_pilots/sfxlib.py:88); safe only while its audio is at least as long as the video. Tighten to 1 frame on trim episodes and re-check after SFX.
- **m2. Cuts drift a little on disk.** Each piece is cut with its own `-t slot` (swirls_assemble.py:232). Frame rounding adds up over 7 cuts (up to about 0.1 s by f06), and the back unit absorbs it. The design's cumulative `B(k)` fixes this; it is DESIGNED, not built. Cuts land exactly on the word's aligned start, so any alignment error shows the old page for the first syllable. Consider a 2-frame lead.
- **m3. Clips are stretched 1.2% today** (scale to a fixed size, no crop). Designed fix, not built.
- **m4. Modesty / NSFW reading in clips is only a soft WARN** (G13). The pilot has a camel-hair garment, and the cheap-model bake-off found bare chests across models. Add `modesty` as a hard flag for any figure in a garment that leaves skin bare.
- **m5. Cross drawn as X or log: no gate**, only the session's full-frame eye. Not in this pilot. Add a prop-shape item to the G9 read before any cross episode.
- **m6. Kling frame rate.** If the native clips are 24 fps, `-r 30` repeats frames. That is fine for G15h at 0.5 s spacing, but it can judder on slow pans. Probe the native fps in G11.
- **m7. WARN never stops anything.** `_report` passes CONDITIONAL. Every near-miss and freeze WARN depends on the session reading the console. List the open WARNs on every owner page.

## Hold / trim math — what I found by reading the code

- **No cloned frames: true on disk.** The trim draft and the scored path keep the picture whole (no `-shortest`, swirls_assemble.py:381-390). The back unit's slot is `total - sum(previous held)` (line 356), and `make_trim` refuses a clip shorter than slot + 0.05. So the last 3 s are the back clip's own frames. At most about 1 frame of the `mix_tail` clone survives before `-t total`.
- **Moving: NOT guaranteed.** The clip is ordered with only +0.5 s (swirls_short.py:122, not the design's +2.0 and no cap at 15). Nothing FAILs a settled tail (B4).
- **A/V: matched** within the 0.3 s gate, on both the draft path (`apad=whole_dur`) and the scored path (`mix_tail` `apad=whole_dur=total` plus `-t total`).
