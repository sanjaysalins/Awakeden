# Episode 12 — "Ye Are Not All Clean" (John 13:1-30, Judas) — status 2026-09-09

## Where this stands

**Narration LOCKED 2026-09-09.** `narration.md` in this folder is final — 15 rounds of the 5-CLI
independent-review panel across two full passes (a Sonnet hand-edit lineage, then a genuine Fable
creative rewrite per the user's request to find more conviction). Doctrine, KJV verbatim, and
no-fear-framing confirmed clean by every reviewer in every round of the final (Fable) lineage.
User approved lock on the one remaining open item (the CTA's exact closing shape — a genuine
producer-level call, not a defect) 2026-09-09. Full history:
memory `project_ye_are_not_all_clean_episode_12`, `_NARRATION_PANEL_STATUS.html` in this folder,
and `_independent_review/` (15 timestamped rounds).

**Locked text:**

> Judas walked out into the night on feet Jesus had washed.
>
> John says the devil had already "put into the heart of Judas Iscariot, Simon's son, to betray
> him." Jesus knew. He knew as He poured the water. He knew as He dried their feet with the towel.
>
> Then He told them, "ye are clean, but not all." And He quoted the old word for betrayal, from
> Scripture: "He that eateth bread with me hath lifted up his heel against me."
>
> He handed Judas the sop — a piece of dipped bread. "That thou doest, do quickly." Some at the
> table thought he had gone to buy food. Judas "went immediately out: and it was night."
>
> Jesus did not wash those feet because Judas earned it. He washed them knowing Judas would
> betray Him anyway. That is what His love does when it already knows the worst.
>
> He knows your heart, every corner of it, like that. He has not put the towel down — bring Him
> your worst.

169 words. $0 gate: PASS (`narration_gate.py`).

## Plan-only verification pass — DONE, both real risks cleared (2026-09-08)

1. **Zone-separation storyboard (QUAD-lock "never touch" vs. John 13's literal foot-washing
   contact): holds.** John 13:1-11 dramatizes only ONE individual exchange (Peter's protest,
   v6-9) — nothing in the text forces a panel singling out Judas's own feet at the basin. Judas's
   distinct beat naturally lands later, at the sop (13:21-30) — bread, not feet, no basin, no
   swirl-motif staging there. So the page design v4 of the series plan already proposed — "Jesus's
   swirl centers on the basin where he washes the OTHER disciples; Judas's stain stays local to his
   own feet, a clean-paper band between them" — is achievable, not just asserted. Full writeup:
   memory `project_swirls_backlog_v6`.
2. **`pipeline/handoff.py` truncating the wide John 13:1-30 ref span: does not apply.** Confirmed by
   direct code check — grepped the whole `poc_living_water_ink_style_test/` tree for any use of
   `pipeline.handoff` or `write_narration_folder`. Zero matches, anywhere. The Swirls pipeline never
   routes narration through that main-engine code — narration is hand/Fable-written straight into
   each episode's own `narration.md`. This "risk" had been copy-pasted across v4→v5→v6 of the series
   plan (and re-flagged again by the independent panel) without anyone ever checking whether the
   code path it names is even in the Swirls build's execution path. It isn't.

## The landing decision — RESOLVED 2026-09-09

User chose to keep the binding G8 CTA-to-Jesus requirement over a format exemption. First closing
beat (Sonnet-written, small addition) went through 9 panel rounds; then, per the user's explicit
request for "another perspective from Fable and the panel" to find more conviction, a fresh Fable
creative pass replaced it with the "washed anyway / knew he'd betray anyway" turn above — 6 more
panel rounds, now LOCKED. See memory `project_ye_are_not_all_clean_episode_12` for the full
round-by-round history, including the note on which specific fixes worked and which introduced new
problems (useful precedent for future episodes on this same "washed ≠ saved" territory).

## Voice synthesis — DONE 2026-09-09

Ran the real pipeline: `PythonProject1/jesus/narration_pipeline.py --stage verify` → `--stage tag`
→ `--stage audit` (agent-bridge serviced live, 3 requests: verify, tag, audit — all passed, tag
validation/speaker validation/round-trip prose all clean), then
`PythonProject1/jesus/narration/per_turn_synth.py --target 65 --pre-quote-pause 0.4 --stability 0.65
--natural` (real ElevenLabs spend, user-approved). One tonal tag fix applied from the audit's own
finding (dropped `[deliberate]` off paragraph 4 — it fought the text's own "do quickly"/
"immediately" urgency).

**Result:** `narration.mp3`, 74.55s, natural pace (no time-stretch — `narrator_atempo_factor: 1.0`
in `narration.meta.json`), voice `LSi9zNCeliLuhIGGS0By` (series-standard narrator). Ran 9.56s over
the 65s target ceiling; per this project's standing rule (never compress to hit a target, trim
words instead if it matters — see `feedback_narration_process_gold_standard`), this was accepted
as-is rather than compressed. **HUMAN GATE 1 — APPROVED 2026-09-09** (user: "lock it").

## Visual design brief — LOCKED 2026-09-09

`_DESIGN_BRIEF.md` (862 lines) written — as SONNET, not Fable, per the global "Fable for major
pivots only" rule (this is routine per-episode design within an already-established house style).
Followed the `_DESIGN_BRIEF.md` + `episode.py` pattern from ep11/ep13 (the SKILL.md's own
"one storyboard page" template is a superseded prototype format, not what's actually shipped).

**Shape:** 6 interior pages (F01-F06) + front/back covers, `panel_style="woodcut_hybrid"`. Two hard
doctrinal calls, both reasoned explicitly: **no Stain/mark on Judas** (would visually assert what
nine narration rounds fought to avoid claiming — that his exclusion was a visible defect, not a
heart Jesus already knew), and the **Swirls-of-Life ink motif anchored to the water in the basin**,
never to a person (a first for the series — every prior episode anchored to a hand/threshold — but
the only way to guarantee the motif never touches Judas). The episode's own landing beat ("He knows
your heart... bring Him your worst") maps to the BACK COVER, not an interior page — the direct-
address turn to the viewer, past Judas's own unresolved exit.

10 open questions flagged, none silently resolved — **all approved on the recommended option**
2026-09-09 (user: "lock it"). Full list + resolutions in `_DESIGN_BRIEF.md` §8 and
`_DESIGN_BRIEF_QUESTIONS.html` in this folder.

## Generation route DECIDED: Google Flow

User: "I need the google flow brief" (2026-09-09) — decides item 2 below. `ASSEMBLY_PLAN.md` built
first from REAL forced-alignment on the locked `narration.mp3` (not word-count estimates) — real
per-beat timing, plus a genuine finding: 0.00s gap between F04 and F05 in the actual audio, so that
page-cut must be a deliberate hard cut, not one riding a breath. `FLOW_RUN_SHEET.md` (1125 lines)
built from the validated pilot's structural template + this episode's own `_DESIGN_BRIEF.md`
content. 20 generations (4 refs + 8 stills + 8 clips).

## Red-team pass — DONE 2026-09-09, real bugs found and fixed

Caught one myself before running the panel: F03's still prompt described Jesus "speaking" with no
mouth-state guard, while its own clip correctly said "lips closed" — fixed (the still is the source
frame the clip animates from, so the gap mattered). Then ran the full 5-CLI panel
(`independent_review.py --type plan`, `_independent_review/20260909-230105/`) — **3 FAIL, 2 REVISE**,
strong real convergence, not nitpicks:
- **Confirmed, fixed:** Section 0/3's ZONE rule flatly claimed "Judas + motif never happens by
  design" while Steps S3/S4 (F02/F03) correctly have both in the same wide frame at a safe distance
  — rewritten to state the real two-part rule (proximity-ban on F02/F03, zero-tolerance on F04/F05).
  4 of 5 reviewers caught this independently.
- **Confirmed, fixed:** retry-budget math said "up to 45 attempts" but every one of the 20 steps
  carries a CRITICAL line — worst case is 60, not 45 (verified by direct count). 3 of 5 reviewers
  caught this independently.
- **Confirmed, fixed:** S8's attach-table row said "none" while the step itself attaches
  REF_BASIN_TOWEL; also added STILL_01 as an actual Ingredient for the Back Cover's "match the Front
  Cover style" check (was text-only — the pilot's own worst real defect was exactly a text-only style
  match failing).
- **Confirmed, fixed:** "no gold near Judas" could read as contradicting the baseline palette's own
  "soft gold wash" language used on every page — added an explicit motif-vs-palette distinction.
- **Confirmed, fixed:** `check_landing_hold.py` doesn't actually check what the doc claimed for this
  episode (its no-arg scan never reaches `poc_living_water_ink_style_test/`, and per-file mode only
  checks audio/video parity, not the ≥3.0s hold itself) — added explicit manual verification steps.
- **Confirmed, fixed:** "three marked LONG" undercounted — four clips (F03/F04/F06/back cover) need
  extension beyond Flow's native ceiling.
- **Added, from real project memory the sheet was missing:** a baked-text 2x-zoom check and a
  measured frame-diff motion check in the post-download human review section (`feedback_
  baked_text_needs_full_zoom_check`, `feedback_animation_motion_check_by_pixel_diff`).
- Also fixed the matching inconsistency in `_DESIGN_BRIEF.md` itself (§0's summary line and §3's
  ref-table both still said Jesus is absent from F04, contradicting §6's actual scene).

**Considered, kept as-is:** several reviewers (gemini, cursor, codex) wanted a mandatory human
stills-review gate between Phase 2 and Phase 3. Raised to the user 2026-09-09 — **decided: keep it
unattended**, matching the pilot's own deliberate, already-validated structure (single run, one
full review after the zip returns).

## Flow delivery received and reviewed — 2026-09-09

User ran `FLOW_RUN_SHEET.md` through Google Flow; delivered zip (`Sept 09 - 23_22.zip`, 40MB, 21
files — 20 real generations + 1 echoed upload of the Jesus ref) extracted to `_flow_delivery_v1/`.
No FINAL REPORT/label log came back as a file — matched every asset by content, by eye, exactly as
the pilot's own process anticipated (Flow's filenames are content-descriptive, not the REF_/STILL_/
CLIP_ labels). Full review: `_flow_delivery_v1/_GATE2_REVIEW.html`.

**Real result: 6 of 8 stills clean, 6 of 8 clips clean, 2 real problems found by direct pixel
inspection (not self-reported pass/fail) — awaiting the user's call on both, not yet regenerated:**

1. **STILL_04/CLIP_04 (F03) — leaked internal prompt text baked as visible captions.** Under each of
   the 3 top panel handwrite captions, Flow also printed my own panel-description text as small
   extra type (e.g. under "clean," also "single washed foot, dry, resting no floor, close-up, no
   face"). Confirmed real, needs a regen with a stronger no-extra-text guard.
2. **STILL_04/CLIP_04 (F03) — possible real zone violation, needs the user's eye.** The man kneeling
   beside the basin, reaching toward Jesus, shares the same coloring/robe/sash as the confirmed
   Judas figure on F04 — if that IS Judas, he's within arm's reach of the basin, not "at least an
   arm's length away" as required. Could not be resolved with full confidence from the image alone;
   flagged rather than guessed.
3. **CLIP_03 (F02) — the clip's own animation invented a stray blue-ink thread rising from near the
   wall/lamp shelf, not from the basin's water surface as required** (confirmed via first-vs-last
   frame diff, not eyeballed playback). The approved still itself is clean; only this one clip needs
   a redo.

**Clean, checked directly (not just trusted):** Front Cover, F01, F04, F05, F06 (hero), Back Cover —
stills and their clips both. Correct captions verbatim, correct motif dose per page (present +
basin-anchored on F02*/F06, absent on F04/F05, diffused/floating free on Back Cover — *F02's still is
clean, only its clip drifted), no other leaked text, no era-breaking objects except one minor note
below. Motion checked via real first/last-frame extraction on every clip, not a played-back glance.

**Minor, not blocking:** REF_DOORWAY has a European-style hinged door with a round handle — a small
era-accuracy slip (this project's own prompt never explicitly banned modern door hardware, a gap in
the original brief, not something Flow got wrong per the letter of the prompt). Background-only on
F05 and the Front Cover.

**Clip lengths came back as predicted in `ASSEMBLY_PLAN.md`:** all 8 at Flow's normal 8-10s ceiling,
not the requested "longest available" — F03/F06/Back Cover will need freeze-hold extension at
assembly; Front Cover/F02/F05 came back longer than their real target and will get trimmed.

## Assembled — 2026-09-10

User: "I think its all go, just assemble it and shot it o me" — accepted the delivered Flow content
as-is, including the two flagged F03/F02-clip issues (not regenerated). Built via a bespoke ffmpeg
script (`_assembly_v1/`, no `episode.py`/`swirls_assemble.py` — those are OpenArt/HF-specific, this
is a one-off Flow-delivery assembly matching the pilot's own approach), from `ASSEMBLY_PLAN.md`'s
real timing, corrected to also absorb each beat's own preceding pause (so the video timeline stays
exactly in sync with the narration, not just each clip's own speech-only span):

| Unit | On-screen duration | Source clip | Trim/extend |
|---|---|---|---|
| Front | 3.74s | Man_walking_away_from_viewer (8.0s) | trim from start |
| F01 | 9.62s | Jesus_blinks_in_lamp_light (8.0s) | +1.62s freeze-pad |
| F02 | 6.16s | Jesus_washing_disciples_feet_basin (8.0s) | trim from start |
| F03 | 14.86s | Jesus_speaking_at_seated_table (10.005s) | +4.86s freeze-pad |
| F04 | 12.08s | Bread_passing_between_two_men (10.005s) | +2.08s freeze-pad |
| F05 | 3.88s | Man_walking_through_doorway (8.0s) | trim from END (max darkness) |
| F06 | 13.00s | Figure_resting_hands_at_basin (10.005s) | +3.00s freeze-pad |
| Back | 14.47s | Blue_ink_threads_drift_slowly (10.005s) | +4.475s freeze-pad |

All clips normalized to 1080x1920 30fps CFR, concatenated, muxed with the locked `narration.mp3`.

**Caught and fixed a real bug in my own first assembly attempt before showing it:** the initial mux
used `apad` + `-shortest`, which would have truncated the video back down to the narration's raw
74.55s length and silently deleted the entire landing hold — exactly the documented ffmpeg pad/parity
bug class this project's own memory warns about (`feedback_ffmpeg_duplicate_vf_and_duck_transfer`).
Fixed to measure the real video duration and use `apad=whole_dur=<that exact number>` with no
`-shortest`.

**Landing hold verified by hand, not just the automated gate:** first pass landed the hold at 2.98s
— 0.02s under the ≥3.0s INV-26 minimum (a real, if marginal, shortfall against the real last-word
timestamp from forced-alignment, 74.32s — the automated `check_landing_hold.py` gate only checks
audio/video parity for this project's folder, not the actual hold length, so this needed a manual
check). Added more back-cover padding; final hold is **3.48s**, comfortably over.

**Final: `_assembly_v1/viral_cut.mp4`, 77.80s, video/audio parity exact (77.80s/77.80s), landing hold
3.48s.** The F04→F05 hard cut was checked directly (extracted frames either side) — reads as a
genuine, deliberate contrast (lit room → total darkness), not an accidental jump cut. Not yet given
score or SFX (the standard next polish pass on every other finished episode) — this is the narration
+ visuals cut only.

## SFX + score added — 2026-09-10

**SFX: already present, no separate pass needed.** User caught that the clips' own baked ambient
audio (Flow's per-shot "Audio:" prompt lines) was real, non-silent sound — my first assembly had
wrongly stripped it with `-an` while normalizing every segment (the exact same class of "did the
delivered asset already carry something" miss the pilot's own memory documents). Rebuilt every
segment preserving its own audio track (trim/extend logic applied to audio in sync with video this
time), measured real levels first (-30 to -63dB mean across the 8 clips — genuine ambient, not
digital silence), then mixed as a quiet bed (-8dB) under the narration.

**Score: `generate_score_piano.py` written for this episode** (two-part felt-piano identity, same
six-episode-validated "Fig Tree" series sound, split at F06's real start — 50.34s — per the LOCKED
two-part-generation standard). **The newly-added full-timeline sweep check (not just the first-10s
check episode 13's own script had) caught a real dead-air defect on the first generation attempt**:
a 10-second near-silent span at 40-50s in Part 1, traced to my own prompt wording ("thins to almost
nothing... the most withheld and empty") — language that invited literal silence, the same failure
class as episode 13's original incident. Fixed the wording (kept the emotional intent, dropped the
near-silence description), regenerated ONLY Part 1 (Part 2 was already clean, verified by hand
before reusing it — no wasted re-spend). Final `score_piano.mp3`, 77.87s, clean sweep confirmed.

**Final mix: narration (full) + clip ambient bed (-8dB) + score (-13dB), 3-way `amix` with
`normalize=0`** (so none of the three tracks gets auto-attenuated against my own intended balance).
`_assembly_v1/viral_cut_final.mp4` — 77.83s video / 77.87s audio (gap -0.03s, within one frame),
mean level -23dB / peak -6.7dB (no clipping), landing hold **3.51s** (still comfortably over the
3.0s INV-26 minimum). Not personally verified by ear — that's the user's own listen, same as every
other episode's audio approval.

## Freeze-frame → Ken Burns + audio-artifact fix — 2026-09-10

User feedback on the first `viral_cut_final.mp4`: "there is some spoken word at 0:14, then there
are lots of freeze frame... I hate freeze frame, we should look at doing some ken burn motion."
Two separate real problems, both fixed:

**Spoken-word artifact at 0:14.** That timestamp falls right at the F01→F02 clip boundary, during a
genuine silence in the narration track itself (real forced-alignment: narrator's next word doesn't
start until 14.58s) — so any audible speech there had to be coming from one of the two clips' own
baked ambient audio, not the narration. Diagnostic `astats` on F02's own source clip
(`Jesus_washing_disciples_feet_basin_...mp4`) first 1.5s found real, focused energy in the vocal
frequency band (300-3400Hz, peak -19.3dB) — consistent with the user's report, and a known Flow/Veo
risk (video-generation models can produce unintended vocalization despite "no dialogue" prompt
instructions) already documented in this project's own pilot memory. I cannot literally hear the
clip myself to confirm the word, so I trusted the user's ear: **muted F01's and F02's own ambient
audio tracks specifically** (both segments now `-an`), left all 6 other clips' ambient beds
untouched. Re-measured mix at 0:12-0:16 in the vocal band after the fix: mean -43.9dB (down from
whatever was driving the original report) — consistent with genuine silence there now.

**Freeze-frame → Ken Burns.** Replaced every `tpad=stop_mode=clone` static freeze extension (the 5
padded segments: F01 +1.62s, F03 +4.855s, F04 +2.075s, F06 +2.87s-ish, Back +4.475s — exact pad
recomputed per clip's real delivered length) with a real slow zoom-in (Ken Burns push, zoom
1.00→1.06) built from each clip's own true last frame via ffmpeg's `zoompan`, at the base clip's
native 1080x1920 30fps. Verified genuinely moving, not frozen, by pixel-diff (project convention,
`feedback_animation_motion_check_by_pixel_diff`): F03's tail (the longest, 4.855s) measured mean
absolute pixel difference of 44/255 between its first and last frame — real, substantial motion.

Rebuilt the full concat + 3-way audio mix (ambient bed + narration + score) from scratch on top of
the Ken-Burns segments. **New final: `_assembly_v1/viral_cut_final.mp4`, 77.97s video / 77.97s audio
(exact parity), mean -22.7dB / peak -6.8dB (no clipping), landing hold 3.65s** (last word ends
74.32s per forced-alignment, video ends 77.97s — comfortably over the 3.0s INV-26 minimum). Old
version preserved as `viral_cut_final.mp4.SUPERSEDED_freezeframe_and_spokenword_artifact` per this
project's superseded-file convention. Not personally verified by ear — the muting fix is based on
trusting the user's report, not something I can confirm by listening myself; needs the user's own
re-listen to confirm the artifact is actually gone and the Ken Burns motion reads well.

## Ken Burns → reverse-boomerang + narration hard-stop fix — 2026-09-10

User, after watching the Ken Burns version: "instead of ken burn most of them can do the reverse
boomerang effect, instead of ken burn effect" + "and you cut the narration abruptly in the end."
Two more real problems, both fixed:

**Narration's own hard stop — confirmed as a genuine defect, not a mix artifact.** Measured
`narration.mp3`'s own last 50ms windows directly: the file sits at -10 to -14dB max volume all the
way to its literal last sample (74.554535s) — no natural decay at all, it simply stops while still
near full level. That is exactly what the user heard. Fixed with a 120ms `afade=t=out` applied to
the narration track only, right at its own tail, before mixing (does not touch or regenerate the
underlying TTS file). Verified in isolation: the faded tail now decays -12dB → -28dB smoothly
instead of stopping flat.

**Ken Burns → reverse-boomerang.** Replaced the zoom-in tails on all 5 padded segments (F01, F03,
F04, F06, back cover) with a ping-pong of each clip's own settled last 1.0s: reverse(tail) →
forward(tail) → reverse(tail) → ... until the pad duration is filled, trimmed to the exact length.
Continuity at every seam is exact by construction (each segment starts exactly where the previous
one ended). Checked the one real risk flagged by this project's own memory
(`project_swirls_boomerang_continuous_motion_unsafe` — a clip with no completing gesture can visibly
reverse when boomeranged) directly on the back cover's "ink threads drift slowly" footage before
trusting it: sampled 5 frames across its last 1.5s and measured pixel-diff — the first→last diff
(3.2/255) was NOT larger than each individual step (2.6-5.0/255), meaning the drift is bounded/
settled, not a runaway one-directional flow. Safe to boomerang; did not need to fall back to Ken
Burns for that one. Confirmed real (non-frozen) tail motion on both F03 (calm, 1.7-1.8/255
first→mid→last) and the back cover (3.6/255) after building, and confirmed the base→tail seam has
no visible jump (2.0/255, within re-encode noise).

**Audio on the boomerang tails: looped forward, never reversed** (reversed ambient sound reads as an
obvious backwards-audio artifact even when quiet) — took each clip's own last 1.0s of ambient audio
and looped it forward to fill the pad, instead of the Ken Burns version's mistaken `anullsrc` silence
(a bug in that version: the code comment claimed "carry the ambient bed through" but the
implementation actually inserted real digital silence at every tail — never shipped, caught before
approval).

Rebuilt the full concat + 3-way mix again. **New final: `_assembly_v1/viral_cut_final.mp4`, 78.03s
video / 78.03s audio (exact parity), mean -22.7dB / peak -6.7dB (no clipping), landing hold 3.71s**
(last word ends 74.32s, video ends 78.03s). Old Ken Burns version preserved as
`viral_cut_final.mp4.SUPERSEDED_kenburns_and_narration_hardstop`; the original freeze-frame version
remains at `viral_cut_final.mp4.SUPERSEDED_freezeframe_and_spokenword_artifact`.

## Narration ending, round 2 — 2026-09-10

User, after the boomerang+120ms-fade build: "it cut again before completing." Investigated properly
this time instead of assuming the first fix was enough:

- Confirmed via an ISOLATED test (narration alone, no mix) that the 120ms fade genuinely did work as
  coded — but it only had 120ms of a 234ms-long true trailing tail to work with (narration.mp3's
  real content ends at 74.32s, the file itself ends at 74.554535s), so the taper was real but too
  short to read as natural. Extended it to use the FULL available 234ms tail.
- **Caught my own mistake before shipping it**: a first attempt at a longer, more noticeable fix
  (500ms fade + a light room-echo for extra natural decay) actually started the fade at 74.054535s —
  which is DURING the word "worst." itself (that word spans 73.94-74.32s per forced-alignment), not
  after it. That would have faded real spoken content, not just trailing silence — caught by
  isolated testing before it reached the user. The echo attempt was also dropped: `aecho` applies
  across the ENTIRE narration track (a faint 70ms-delayed doubling of every word), not just the tail
  it was meant for — confirmed by a whole-file level shift (-6.7dB peak → -10.5dB peak) that had no
  business changing from a tail-only effect.
- **Shipped fix:** fade only from 74.32s (the real last word's own end timestamp, confirmed never
  touched) to 74.554535s (file's true end) — the full natural tail, linear curve. Verified in
  isolation: content up to 74.32s is bit-for-bit unchanged, then decays smoothly -20dB → -45dB by
  the file's end. No aecho, no earlier fade-start.

**Current final: `_assembly_v1/viral_cut_final.mp4`, 78.03s video / 78.03s audio (exact parity), mean
-22.7dB / peak -6.7dB (matches the unfaded baseline — confirms the fade doesn't touch overall
levels), landing hold 3.71s.** Superseded chain, oldest to newest:
`viral_cut_final.mp4.SUPERSEDED_freezeframe_and_spokenword_artifact` →
`...SUPERSEDED_kenburns_and_narration_hardstop` → `...SUPERSEDED_boomerang_v1_short_fade` → current.

**Honest caveat:** 234ms is the maximum real trailing audio this TTS render actually contains — this
fix uses all of it, but if the user still hears it as an abrupt stop, a fade alone cannot manufacture
audio that was never recorded. The real fix at that point would be either regenerating the last
narration turn via `per_turn_synth.py` with more natural trailing room, or a properly-scoped tail
extension (split narration at 74.32s, apply reverb/echo only to the split-off tail chunk, then
re-concatenate) rather than a filter applied to the whole track. Not attempted tonight — flagging as
the next step if needed, not silently declaring this fully solved.

## Next steps

1. **User re-watches/listens to the new `_assembly_v1/viral_cut_final.mp4`** — confirm the narration
   ending now reads as a natural taper (not a cut), and that the reverse-boomerang motion reads well.
   This is the last real gate before this episode joins the other finished-but-unposted ones.
2. If the narration ending still reads as cut short, the fade has hit its ceiling (only 234ms of real
   trailing audio exists) — next move is a properly-scoped tail-extension (split + reverb the tail
   chunk only, re-concatenate) or a `per_turn_synth.py` re-render of the last turn, not another fade
   tweak.
3. Decide whether to revisit the two accepted-as-is Flow issues (F03's leaked text/possible zone
   proximity, F02 clip's stray ink thread) before calling this episode fully finished, or ship
   as-is (episode 12 is still under the standing 30-episode posting hold either way).
