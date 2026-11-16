# Blind review — SWIRLS_SHORT_PIPELINE_DESIGN_v3.md (Fable seat)

Date 2026-11-15. Read-only, $0. I read the design plus: `swirls_assemble.py`, `swirls_short.py` (timing + lint part),
`swirls_episode.py` (command list, `_bridge_credits`), `test_the_cross\openart_bridge.py`, `pipeline\score_mix.py`,
`pipeline\assembly_align.py`, `pipeline\upload_engine.py` (anchor), `per_turn_synth.py` (argparse, natural mode),
`AGENT_BRIDGE.md` (gen response contract). I did not read any other design file or any review folder.
I did not run the validators; "139 checks pass" and "3 of 5 old validators pass" are the design's claims, unchecked by me.

## Short answer

The timing and trim design is sound. The build order is testable. The spend guard has one real hole
(the "receipt" is not a receipt) and one bypass (the flag is opt-in). Clip quality and the moving hold are
still judged by eye, not by a gate. It is over-built in places for a $7 pilot. REVISE, not FAIL.

## What I checked and found right

- **Trim math.** `clip_duration = min(15, max(3, ceil(slot + 0.5)))` gives 3-4 s (front), 6-8 s (pages), 7-10 s (back)
  for the slot table. Matches the table. About 53-54 clip-seconds x 35 cr = about 1,855-1,890 cr. Matches section 8.
- **Cumulative frame boundaries + `-frames:v`.** Correct fix. The code on disk today still uses `-t slot` per unit and
  "back = total minus the others" (`swirls_assemble.py` `make_trim` + the trim loop), so the design's REDO note is accurate.
- **Moving hold, structurally.** `mix_tail` does `tpad clone` + `output_args(total=...)` adds `-t total`. If the picture
  is already `total` long, the cloned frames are cut. The trim mux on disk already drops `-shortest`. Claim holds.
- **A/V match.** `apad=whole_dur=total` in both the draft path and `mix_tail`. Good.
- **Alignment.** `align()` default backend is whisper and `build_srt.build()` forces a re-align. Both true. The design's
  fixes (force elevenlabs, meta hash, `force` argument) are right.
- **Anchor parser, `--natural`, tagged file.** All as the design says.
- **Slot rule.** `build_timing` on disk already implements "first word of k to first word of k+1; back = mp3 + 3.0".

## Findings (worst first)

### F1. The OpenArt "receipt" is not a billed number — the 110% check cannot catch sound-on (spend guard, HIGH)
`AGENT_BRIDGE.md` step 6 tells the servicer to fill `credits_spent` from "a cost estimate via `openart_model_cost` for
the same config (or diff `openart_account_get` before/after)". So:
- The usual value is a **quote for the payload's config**, typed by the servicing session. It will equal the guard's own
  price every time, even if the real MCP call went out with sound on, a different duration, or `4k`.
- The balance-diff option is wrong whenever another session spends at the same time (the design itself says other
  sessions spend from this balance).
So section 5's line "Sound left ON bills 40 cr/s = 114% -> caught" is not true as designed. The guard prices the
request file, not the call the servicer actually makes.
**Fix:** the response must echo the parameters actually sent (`model, duration, resolution, generate_sound`) and the
creation / history id, and `credits_spent` must come from that creation's own record. `after()` compares the echoed
parameters to the payload; a mismatch or a missing echo = `UNRESOLVED`. Update the servicing steps in `AGENT_BRIDGE.md`
and add both cases to T6.

### F2. `REQUIRE_GUARD` is opt-in by the caller, so it is not "inside the door" (spend guard, HIGH)
The flag is a module global the runner sets after it loads a trim episode. Any other script that imports
`swirls_page` / `swirls_cover` / `openart_bridge` (this repo's habit: one-off `render_*.py` files) sends an unguarded
request for the same episode. The session can also call the OpenArt MCP tools directly with no request file at all.
**Fix:** decide at the boundary, from the payload: if `out_path` sits inside a folder that has `approvals.json`
(or a `.swirls_short` marker written at step 0), `submit()` raises unless a guard is set. Put the guard's `rid` in the
request file and tell the servicer to refuse a request for such a folder with no `rid`. State plainly that a direct MCP
call is outside every guard and is banned by rule only.

### F3. Clip defects and the moving hold are WARN-only — the two things the owner cares about most are not gated (HIGH)
- SWS-G13 (new text, speech bubble, head count change, figure enters / leaves) is WARN. SWS-G12 is WARN.
  "A real defect seen in the strip stops the batch" is the session's judgment, not code. Defect 1 (Kling bubbles) and
  defect 8 (clones) in section 10 therefore rest on a WARN.
- SWS-G15f (landing motion) is WARN until T8, and may stay WARN. SWS-G15 only proves there are no *cloned* frames.
  A Kling back clip that settles after 4 s gives a dead hold and passes every FAIL gate.
**Fix:** make the hard flags in G13 (bubble, new text, head count differs) a FAIL that needs an `_overrides.json`
entry with a note — that is the fail-closed shape the design already uses elsewhere. For the hold, do not wait on
`freezedetect` tuning: measure mean frame difference over the last 3.0 s of the back unit against the same clip's
first 3.0 s (the project's own pixel-diff rule). FAIL below a small fraction; T8 only sets the fraction.

### F4. Token *count* equality is not text equality (timing, MEDIUM)
`timing` checks that `units.json`, `narration.md` and the alignment have the same number of tokens. The audio and the
alignment transcript come from `narration-tagged.md` (`assembly_align.transcript`), which the check never reads.
A word moved between two units, or a tagged file that drifted from `narration.md` with the same count, passes — and
then every cut is on the wrong word. **Fix:** compare the normalized token *sequence* (lower-case, punctuation
stripped) across `units.json` (joined in order), `narration.md`, the tagged transcript, and the alignment words. Still $0.

### F5. Slot gates fire after voice money; hook and KJV-line budgets are tight for this pilot (timing, MEDIUM)
- Front: 6 words at 2.2 w/s = 2.7 s, plus the first-word offset (up to 0.4 s), plus the gap to F01's first word. That
  lands at 3.2-3.5 s: WARN or FAIL, found only at step 3. Make the hook 4-5 words, or estimate each unit's slot
  (words / 2.2 + lead-in + 0.4 if the next unit opens a new voice) in SWS-G1 and FAIL there, before the voice.
- John 1:23's speech is 22 words. SWS-G1k needs a continuous KJV run; SWS-G1 caps a page at 15 (warn 16). It must be
  split across two pages or cut to a 16-word run. Say so in the pilot brief so writers do not all fail the same gate.
- Estimate window is 38-42 s but 93 words (5 + 6 x 13 + 10) with 4 character turns is 43.9 s. The word budget and the
  estimate gate disagree at the top end. State the real ceiling (about 88 words with turns).

### F6. Head count vs "small, far, unfinished hatched crowds" will misfire (still audit, MEDIUM)
SWS-G9 FAILs when Vision's `head_count` differs from the plan. Page rule 6 asks for hatched far crowds. Vision will not
count those the same way twice. That produces false FAILs and trains everyone to override. **Fix:** plan and count
`full_figures` (near, named) only; report the crowd as present / absent. Also "text invented (4+ letters)" will trip on
storyboard scribble marks — make that a WARN unless the string is a real word.

### F7. Too many stops and too much kit for a first pilot (LOW, but it costs days)
About 16 owner interactions for a $7 film (7 price asks + 9 `ok` gates + panel page + poster pick + upload). Build
before the pilot: 20-plus gates, 13 tests. What I would cut or push to after the pilot:
- **SWS-G10 edge scan + T9** — the same border is already a FAIL in the G9 read. Defer.
- **T13** ("same ffmpeg argument lists as ep13/ep16's own scripts") — brittle, and phase D can be the per-episode
  scripts once more for the pilot.
- **Poster bake-off, `adopt`, `page_plan_view`, SWS-G1c, cr/usd dual units, 12-hour expiry** — nice, not needed to
  learn whether a 45 s film works.
- **Owner stops:** put each `ok` page and the *next* price on the same page as two separate answers (pick, then
  "spend X? yes/no"). Still one explicit yes per spend; half the round trips.
Keep: frame-exact trim, the guard (with F1/F2 fixed), G14 provenance, the animatic, the single test clip.

### Smaller points
- `RUN align` is a paid ElevenLabs call that does not go through `paid`; "inside the voice cap" with no row. Log it.
- The reroll limit (2 per item) is a rule in prose. The spend log already has unit ids — count rows and refuse the third.
- `approve` / `ok` notes are typed by the session. Nothing proves the owner said it. Fine, but say it: the guard stops
  accidents, not a wrong record. Require a non-empty note with a date.
- SWS-G15 "picture frames = round(total x 30)" on the *scored* file: `-t total` after `tpad` can land one frame either
  side. Give it a one-frame tolerance or T2 will flap.
- G11 says clip >= slot + 0.1; `make_trim` on disk says + 0.05; G3 says + 0.5. Pick one number for the delivered clip.
- T12 uses a fake bridge and fake Vision. It proves the plumbing and the ordering, nothing about film quality. Say so.
- Poster step's gate "(film final)" has no `ok` name. Name it or the guard cannot check it.
- T2's "byte-for-byte unchanged in behaviour" is not a test. Say what is compared (ffmpeg argument list for a legacy
  manifest before / after).

## Will it make good 45 s films, repeatably?

Not proven, and the design says so honestly (section 11). The plumbing will be repeatable. The film quality rests on
four untested things: 6 s page reading, a 2-3 s cover, a clip prompt that drops three safety clauses at once, and a back
clip that keeps moving for 7-9 s. The animatic and the single test clip are the right cheap probes. I would add one
more cheap probe: render the **back cover** as the second test clip (not last), because it is the longest, the costliest
(about 315 cr) and the one the landing depends on.

VERDICT: REVISE

TOP FIXES
1. Make the OpenArt receipt real: response echoes the parameters actually sent + the creation id; `credits_spent` from that creation's record, never a quote or a balance diff; `after()` checks the echo; add to T6 and `AGENT_BRIDGE.md`.
2. Enforce the guard from the payload, not a caller flag: `submit()` refuses any request whose `out_path` is inside a guarded episode folder unless a guard is set; request carries the `rid`; servicer refuses without it.
3. Promote SWS-G13's hard flags (bubble, new text, head count change) to FAIL-with-override, and enforce the 2-reroll limit from the spend log.
4. Gate the moving hold now with a frame-difference ratio on the last 3.0 s (FAIL), instead of a `freezedetect` WARN that may never be promoted; render the back cover as the second test clip.
5. Replace token-count equality with normalized token-sequence equality across `units.json`, `narration.md`, the tagged transcript and the alignment.
6. Move per-unit slot estimates into SWS-G1 (before voice money): hook 4-5 words, real word ceiling stated, and tell the pilot writers John 1:23 (22 words) must be split or cut to a 16-word run.
7. Cut for the pilot: SWS-G10 + T9, T13 and the shared score/SFX tools, poster bake-off, `adopt`, `page_plan_view`; count full figures only in G9; pair each `ok` page with the next price ask to halve owner stops.
