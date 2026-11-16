# Independent review (Fable seat) — SWIRLS_SHORT_PIPELINE_DESIGN.md

Reviewed 2026-11-15, cold, read-only. Nothing paid, nothing edited, no browser.
Design under review:
`F:\slk\PycharmProjects\JesusInTheBible\.claude\skills\swirls-of-life\_redesign\SWIRLS_SHORT_PIPELINE_DESIGN.md`

Code read in full: `swirls_assemble.py`, `swirls_episode.py`, `swirls_verify.py`, `swirls_cover.py`,
`test_the_cross\swirls_page.py`, `test_the_cross\openart_bridge.py`, `pipeline\score_mix.py` (mix tail),
ep13 `unit_timing.json` + `episode.py`, the analysis file, and the memory files it cites.
All under `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\` unless a full path is given.

Short answer: the format maths and the "trim only, clips from real word times" core are sound and
checked. The design is roughly twice as big as it needs to be for a first pilot, it misses one real
code bug that breaks its own "hold is never a frozen frame" rule, and its biggest viewer risk
(a dense page in about 6 seconds on a phone) is sent to a paid pilot when it can be tested for $0 first.

---

## 1. Will it make a good 30-60 s film with fewer fix rounds?

**Partly yes.** These parts should really cut fix rounds, and they are cheap:
- Slots from real word times + every clip longer than its slot + trim only. This removes the whole
  fill family (defect 8), which was the owner's loudest complaint.
- Short baked strings, code compares what Vision reads to an allowed list (G9), no dashes or digits.
- Clip bound to the still's hash (G14). Small, and it fixes a real ep7 failure.
- Refs made before the stills, not cropped from whatever rendered first.
- Shorter clips (7-8 s, not 10+). Less time for Kling to invent things.

**What it will not fix.** The costly rounds on ep13 and ep16 were image-content rounds: cross shape,
vanished or merged figures, clones. Look at ep13's own folder: f01 has 7 superseded stills, f03 has 8
superseded stills and 3 superseded clips. The design's answer for those is a prompt lint, a Vision
call and the "2 rerolls then change the lever" rule. That is a sensible rule, but it is discipline,
not prevention. Expect 1-3 rounds, not zero. The 25-30% buffer looks thin against that history.

**Most likely to break first (in order):**
1. **The untested clip prompt (`short_v2`).** It drops the fence, the bubble clause and every motif
   word all at once, on a model path where each of those was added to stop a real defect. The logic
   ("remove, do not negate") is backed by memory, but three removals in one go on a paid pilot means
   that if a clip fails you will not know which removal did it. Also note PixVerse failed 4 of 4 on
   grid pages by reading a per-panel list as a shot list; `short_v2` still has "one clause per panel".
   Kling has coped with that so far, at 720p and 10 s. Not proven at this prompt shape.
2. **SWS-G12 (pixel gates).** No thresholds exist, the text-box positions it needs come from nowhere
   in the design, and the "blue-ink mask" will be confused by the page's own art (see 2.6). I expect
   this gate to eat build time and then either false-fail or be overridden.
3. **The landing hold.** As the code stands today the hold is a frozen frame (see 2.1). The design
   does not list the change that fixes it.
4. **Page density.** A page with 7 text strings and 4 pictures in about 5.9 s, with a voice over it.
   See section 4.

---

## 2. Wrong facts and wrong assumptions about the code

**2.1 (HIGH) The hold is a freeze today, and the design does not change the code that makes it one.**
- `swirls_assemble.py:337-339` muxes picture and voice with `-shortest`. With a `unit_timing.json`
  whose last unit ends at voice end + 3.0 s (ep13's file does: back ends 106.431, voice is 103.431),
  the picture is cut back to the voice length.
- `pipeline\score_mix.py:46` then adds the hold as `tpad=stop_mode=clone:stop_duration={outro}`.
  That is a cloned last frame. A dead freeze, for 3.0 s, on the landing.
- The design says (1.3) "The hold is never a frozen frame" and (4.4) `pipeline\*` incl. `score_mix.py`
  is untouched. Section 4.1 only adds a draft path with `apad`. Nothing removes `-shortest` or the
  clone pad for the scored path (`assemble --score piano`, step 8), which is the path that ships.
- Fix: in `trim_only`, drop `-shortest`, pad the voice to `total`, and do not clone-pad the picture
  (or rely on `-t total` cutting the clone off, and say so). Add an SWS-G15 check that the last 3.0 s
  of the final file still moves. This is the one gate the "no freeze" owner rule most needs, and it
  is missing.

**2.2 "The three existing `_validate_swirls_*.py` scripts" (section 4).** There are five:
`_validate_swirls_assemble.py`, `_validate_swirls_cover.py` in the POC root, and
`test_the_cross\_validate_swirls_page.py`, `_validate_swirls_page_hem.py`,
`_validate_swirls_page_hybrid.py`. All five must stay green, since `swirls_page.py` and
`swirls_cover.py` are both being edited.

**2.3 "The locked still constants are NOT edited" clashes with the design's own rules.**
- Corner note is not optional in code. `swirls_page.py:210-213` always writes
  `and a corner note, handwrite: "{corner_note}"`. With the design's "optional" corner note left
  empty the prompt asks the model to hand-write an empty string. That invites invented text.
- Zero or two caption lines both fall into the "two stacked lines" branch (`swirls_page.py:204-209`).
- The frozen text names the thing the design says never to name: `TEXT_LOCK_HYBRID` says
  "speech bubble" (`swirls_page.py:112`). It also holds all-caps words ("ONE large", "NOT the panels'",
  "MAIN SCENE ONLY", `swirls_page.py:103-116`) and "is the point of this test" (`:125`).
  SWS-G5 lints only authored prose, so the lint will pass a prompt that still breaks its own rule.
  Either accept that openly (9 episodes of evidence say the frozen text is safe) or stop claiming
  the no-caps / no-bubble-word rule is enforced.
- `still_shot_type` is documented as "exact capitalization" e.g. "MEDIUM WIDE shot"
  (`swirls_page.py:153`) and is spliced in as "a {still_shot_type}: " (`:262`). That is the source of
  the drawn "MEDIUM TWO-SHOT". Lower-casing it is right; the field comment needs fixing too.
- `material_closer` is a required field whose job is to describe "this page's own dead ink"
  (`swirls_page.py:157`). Dead-ink motifs are OFF in v1. The design never says what goes there.

**2.4 Cover clip settings the design did not list.**
- `swirls_episode.py:48-52` hardcodes covers as `veo3_1_lite` for the freeze gate. Harmless in trim
  mode (SW-F1 skips non-freeze units, `swirls_verify.py:201`) but it is stale and should be in the list.
- `CoverSpec.clip_duration` defaults to 4 (`swirls_cover.py:123`). A back cover needs 8. If the
  template or `timing` does not write this value into `episode.py`, the back clip renders 4 s and
  the build fails after money is spent. The design says clip length comes "from `unit_timing.json`"
  (step 6) but `cmd_animate` reads it from the spec (`swirls_page.py:433`, `swirls_cover.py:260`).
  Pick one source and gate it before spend (compare spec value to `unit_timing.json`).

**2.5 The spend cap rests on a number nobody guarantees.** SWS-G0 "adds up credits from bridge
responses". The response is free-form JSON written by whichever Claude session services the bridge;
the code reads `resp.get('credits_spent', '?')` (`swirls_page.py:392, 451`). There is no schema check
in `test_the_cross\openart_bridge.py:45-85`. A missing field means the cap never trips. Simpler and
safer: count the cap from the known price (stills 40 cr, clips 35 cr x seconds) at request time.

**2.6 The "blue-ink mask" (G12) and "motif matches its stage" (G9) will fight the page style.**
The hybrid template tells the model to draw the three panels in "deep teal shadows, golden-hour
glow" (`swirls_page.py:84-89, 122-126`). Covers must name a warm and a cool token, usually gold and
teal/blue (SW-L1, `swirls_verify.py:39-54`, `swirls_cover.py:79-86`). So a stage-0 page and the
stage-0 front cover already contain blue and gold. A colour mask cannot tell motif ink from panel
art, and the panels are exactly where "light warms, haze drifts" motion is allowed.

**2.7 Paths.** `per_turn_synth.py` is at
`F:\slk\PycharmProjects\PythonProject1\jesus\narration\per_turn_synth.py`, not `PythonProject1\jesus\`
(the project CLAUDE.md has the same slip). `--natural` does exist (line 172). `sfxlib` is one file at
`F:\slk\PycharmProjects\JesusInTheBible\sfx_pilots\sfxlib.py`, at the repo root, not under the POC.

**2.8 Output size.** Real Kling pro clips are 1072x1928 (ep13 f01, ep16 `v3\clips\p01.mp4`), not
1080x1920. The first ep16 clips (`clips\c01.mp4`) are 716x1284. `encode()` scales without cropping
(`swirls_assemble.py:93`), so a 1080x1920 manifest squeezes height by about 1%. Not visible. G11's
"height >= 1,900" is fine. Just state the real number.

**2.9 Calibration set is thinner than it sounds.** The labelled bad clips are almost all figure
defects (vanished, walked off, merged). Only one is a text defect
(`back_cover.mp4.SUPERSEDED_title_lettering_vanished`). There is no labelled motif-growth clip and no
labelled panel-border-shift clip. So G12's text, motif and border thresholds would be tuned on one
example or none. Other folders also name files differently
(`...SUPERSEDED_chest_hole_defect.mp4` in ep11), so a glob on `*.mp4.SUPERSEDED_*` misses them.

**Checked and correct:** file names (`front_cover.png`, `<name>_fNN_9x16.png`); manifest default
720x1280 (`swirls_assemble.py:67-68`); `unit_timing.json` is already read (`:251-267`) and ep13 has
the stated schema; sidecar audits are sha-bound (`swirls_verify.py:323-339`); the stale veo comment
(`swirls_cover.py:123`); ep13's `generate_score_piano.py` has `check_no_dead_intro`; all cost sums
(1,190 / 1,855 / 2,345 cr; $3.02 / $4.51 / $5.73); pace 2.2 words per second (ep13: 227 words in
103.4 s). "Three 45 s episodes" from 8,000 cr is tight with buffer (2,840 x 3 = 8,520) and other
sessions spend from the same account.

---

## 3. Is it over-built? Yes. What to cut for v1

The design adds 20 gates, 9 new files and 10 new commands before one pilot has proved the format.
The project rule is "minimum that solves the problem, no abstractions for single-use code". The
design's own section 7 says a pilot may break its core bets. Building the full machine first is the
wrong order.

**Keep for v1 (this is what stops the known defects):**
- Trim mode + the hold fix (2.1) + `_validate_swirls_short.py`.
- `swirls_timing.py` (small, and it gives the quote).
- Text lints G4 / G5 / G5a and the dosage check G6. Plain string checks.
- G9's "code compares the text list" audit and the cover edge scan G10.
- G14 hash binding. A 5-frame strip + one Vision call (G13). First-frame vs last-used-frame diff.
- The two-line approval record for spend (a JSON entry, checked before `still` / `animate`).

**Cut or defer until the pilot has shipped:**
| Item | Why it can wait |
|---|---|
| `swirls_state.py`, `status`, rewriting `HANDOVER_RESUME.md`, `_STATUS.html` | A hand-kept handover file has worked on every episode. Step detection from disk is a small state machine with its own bugs. |
| `swirls_pages.py` (one builder for all owner pages) | Abstraction before the second use. Hand-write the 6 pages for the pilot, copy ep16's. |
| `swirls_score.py`, `swirls_sfx.py` shared modules | Copy ep13's two scripts once more. Lift them into shared code after two episodes agree. |
| `swirls_new_episode.py` + `_episode_template\` | Copy a folder by hand for the pilot. Template it once the shape is proven. |
| `redteam-pack` command | The blind pack scripts already exist in the reference projects. Reuse, do not rebuild. |
| SWS-G12 except the first/last frame diff | No thresholds, no box source, colour mask is confounded (2.6, 2.9). |
| G0 running credit totals from the bridge | Use known prices instead (2.5). |
| G8, G17, G18 as coded gates | G8 is all warnings. G17: measure once by hand, as ep16 did. G18: the 1.0 s merge in `build_srt.py` is enough. |
| `AGENT_BRIDGE.md` `job_id` / `_jobs.jsonl` change | ep16 kept job ids in a text file. Fine for one pilot. |
| The 30 s and 60 s sizes | Build and prove 45 s only. The other two are a table row later. |
| Rewriting all seven skill docs | Already deferred by the design. Good. Keep it that way. |

That is roughly 4 new files and about 8 gates instead of 9 files and 20 gates, with the same
defect cover.

---

## 4. What a real viewer would notice (missing or under-weighted)

1. **Page density on a phone. This is the format's biggest open risk and it can be tested for $0.**
   One page shows a title, a frame number, three labelled panels, a hero scene, a caption and maybe
   a corner note, in about 5.9 s, while a voice speaks 13 words. The stills are 1536x2752; at phone
   size each panel is roughly a third of the width, and a panel label is a few millimetres tall.
   Old pages had 7-13 s (ep13) and still used one short caption. The design admits "nobody has
   measured it" and then sends it to a paid pilot. Instead: trim existing ep10 / ep13 page clips to
   6 s each, hard cut, play on a phone, and run the blind newcomer seat on that. $0. If the panels
   cannot be read, the fix (2 panels, or panels without labels, or bigger labels) changes the still
   template, so it must be known before step 5, not after step 6.
2. **The same header on every page.** `SEQ: TITLE` and `F0N` are repeated on all 4-8 pages. At
   6 s a page that is a real share of the reading time, spent on text that carries no story.
   Consider it at the density test.
3. **Three text layers at once.** Baked caption, the platform's own captions from the SRT, and the
   voice. "No burned captions" is kept, but uploaded SRT captions sit in the lower third, right over
   the baked caption line. The 85% rule covers the app's buttons, not the caption track.
4. **Right-edge buttons.** Shorts / TikTok / Reels put a button column down the right side of the
   lower half. That is on top of the hero scene. The design guards only the bottom 15%. Keep the
   hero subject left of about 85% width. The top-edge title and frame number also sit under the
   app's top bar on some platforms.
5. **The hook is a title card.** The elevate panel found the first 2 seconds were the gap. The new
   open still shows a woodcut cover with a baked title and a Scripture reference, now with a voice.
   It is better than a silent 4-10 s card. It is not yet a picture-first hook, and the Scripture
   reference in frame 1 tells a newcomer "sermon" before the curiosity gap opens. Cheap test: in
   the same pilot, render the title-free arm too (one extra still + 3 s clip, about 145 cr) and put
   both in front of real seed viewers. The design lists this as an open question; I would make it
   part of the pilot.
6. **Sameness of rhythm.** Every page is 5-6 s, same layout, locked camera, no inserts. Six equal
   beats in a row. The no-insert rule is right for the owner, but nothing in the design varies the
   pace. One cheap lever inside the rules: allow one short page (4 s) at the turn and let the brief
   ask for it. The slot range already permits it; the words brief (9-18 words per line) does not
   invite it.
7. **Speaker stillness at the peak.** Rule 5 (the speaking figure holds, mouth closed) means the
   pages where Jesus speaks are the stillest pages. Those are usually the gospel turn. The design
   flags this for one-figure pages only. It applies to every quote page. Put the turn's motion in a
   second figure by design, at page-plan time, not as a footnote.
8. **Loop.** The back cover "may" echo the front. For a Short the loop point matters; a 3 s hold on
   closing words then a cut to a title card is a clear stop sign. Fine for a landing on Jesus, but
   say it was chosen.

---

## 5. Owner-rule conflicts

1. **Frozen hold vs "no freeze" and INV-26.** See 2.1. As designed the shipped file ends on a
   3 s cloned frame. Highest-priority conflict because the design claims the opposite.
2. **Thumbnail = `front_cover.png` (step 12) vs the movie-poster rule.** Memory
   `feedback_movie_poster_thumbnails.md` (2026-11-13, used again on ep16 on 2026-11-14): skip the
   safe still-plus-type poster; run a blind key-art panel and a 2-model bake-off. A woodcut cover
   with carved type is the "safe" round the owner called "not really your creative best". Either
   the cover goes through the key-art panel before it is drawn (and the cost of the bake-off, about
   $0.90, joins the quote), or the owner is asked to waive it for Swirls. Not silent.
3. **Locked narration needs the 5-CLI panel (`independent_review.py --type narration`).** Project
   CLAUDE.md makes it mandatory and makes sound doctrine "proven both ways" non-negotiable. Step 1
   runs blind writers and a guardrail panel but never names this gate. Add it, or state that the
   guardrail panel with a KJV Bible seat replaces it and get the owner's yes.
4. **Step 3 page-plan panel is "Fable + 2 CLI seats".** The house rule panel is Fable plus the AI
   panel (Claude, Codex, Grok CLIs and subagents). Two CLI seats is a cut-down panel. Small, but say
   it is a deliberate bend.
5. **Felt piano "is the identity now".** Memory says it is a loved candidate, "not yet formally
   adopted". Marking `SCORE_STYLE_BANK.md` superseded is an owner decision. Add it to the open
   questions or leave the banner out.
6. **Two-part score bend at 30 s.** Disclosed in section 8. The memory says two-part is the
   default, "not a fallback". Fine as an ask; it must be asked, and it goes away if v1 is 45 s only.
7. **Cover crop (G10).** Disclosed. I agree it is not a fill. But an auto-crop that rescales also
   moves the title toward the edge; gate it with a re-run of the text read after the crop.
8. **Four questions on every pick page.** They are on `_PICK_WORDS.html` only. The memory rule says
   every pick page (stills, film, upload).
9. **Open questions.** Three, each with a pick. Good. But the bends in section 8 and the two above
   (thumbnail, felt piano) are also owner decisions, so the true count is six. Fold them into one
   short page with picks, not a second list.
10. **Simplicity first** (project CLAUDE.md rule 2). See section 3. This is the rule the design
    breaks most.

No conflict found on: OpenArt default and never auto-falling back; words before money; a pick
never authorising spend; never auto-opening files; no AI wording; no media to git; hold length 3.0 s;
covers on nano-banana-pro; posting held for the owner.

---

## Ranked top-8 fix list

1. **Fix the frozen hold.** In `trim_only`, remove `-shortest` (`swirls_assemble.py:339`) and the
   clone pad effect (`pipeline\score_mix.py:46`) for the scored path, and add a gate that the last
   3.0 s of the final file moves. List the change in section 4.1.
2. **Run a $0 phone-density test before any build or spend.** Trim existing ep10 / ep13 page clips
   to 6 s, hard cuts, blind newcomer seat + the owner's phone. Decide panel count / label size /
   header from that.
3. **Halve v1.** Build only: trim mode, timing, text lints, G9 text compare, G10, G13 strip, G14
   hash, simple approval record. Defer state/status, the page builder, shared score and SFX modules,
   scaffold, redteam-pack, 30 s and 60 s sizes.
4. **Drop or shrink SWS-G12.** Keep only first-frame vs last-used-frame diff. The colour mask is
   confounded by teal/gold panels and covers, text boxes have no source, and there is one labelled
   text-defect clip to calibrate on.
5. **Resolve the "constants not edited" contradiction.** Fix the always-on corner note and the
   zero-caption branch (`swirls_page.py:204-213`) under `short_v2`, say what `material_closer`
   holds with dead ink off, and be honest that frozen text still says "speech bubble" and uses caps.
6. **Make clip length single-sourced and gated before spend.** `CoverSpec.clip_duration` defaults
   to 4 (`swirls_cover.py:123`); check every spec's `clip_duration` equals `unit_timing.json` in
   `plan`. Compute the spend cap from known prices, not from the free-form bridge reply.
7. **Close the owner-rule gaps.** Movie-poster thumbnail process for the cover (or an explicit
   waiver), `independent_review.py --type narration` on the locked words, felt-piano adoption asked
   not assumed.
8. **De-risk the clip prompt.** Before the pilot's full clip spend, render ONE page clip with
   `short_v2` (about 245 cr) and check bubbles, motif, panel cuts. Three clauses are being removed
   at once; find out on one clip, not eight. Add the title-free cover arm to the same pilot.

VERDICT: REVISE
