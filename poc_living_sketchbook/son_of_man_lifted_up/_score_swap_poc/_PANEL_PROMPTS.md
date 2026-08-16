# Score-swap POC — Eleven Music "Robert Miles Children build-up" score for Son of Man Lifted Up

**Status: PAUSED at a clean checkpoint. Nothing spent yet.** Started 2026-08-16 while
waiting on the Look and Live rebuild; the user asked to wrap the session before spending,
so this is ready to pick up in a fresh session, not abandoned mid-thought.

## The ask

User: take the SHORTEST finished episode we have, and instead of the current (Suno-sourced)
score, generate ONE continuous ElevenLabs Music score styled after Robert Miles' "Children"
**at its build-up stage** (the slow arpeggiated-piano-over-pads section before the beat
drops) — the whole episode gets that single rising-build register for its entire length,
never resolving into a beat/drop. Use the local AI CLI panel to help craft the prompt.

## Target episode

`poc_living_sketchbook/son_of_man_lifted_up/` — **58.0s**, confirmed the shortest real
finished living-sketchbook episode (checked every episode's actual rendered duration via
ffprobe; the only shorter files in the whole tree are tiny bake-off test clips, not real
episodes). John 3:14-15, Nicodemus's night conversation with Jesus, landing on the cross.

Its current score (`_s5_score_sfx.py`) chains TWO Suno `music_library/` beds:
`lonely_searching_a` (0-40s, the rooftop dialogue) crossfading into `sacred_grace_rise_a`
(35.75s on, the cross reveal). This POC replaces BOTH with ONE Eleven Music generation —
the ambient SFX layers (wind/thunder/crowd) and the narration sidechain-ducking stay
exactly as they are, only the music bed source changes.

## What's already done

**Ran the local CLI panel** (reused `independent_review.py`'s own `run_one`/`PROVIDERS`
dispatch — local subscriptions, NOT metered API — via a one-off script, not a permanent
pipeline file) with a production-brief-style creative brief. All 5 providers replied
(raw outputs also saved alongside this file: `claude.txt`, `codex.txt`, `cursor.txt`,
`gemini.txt`, `grok.txt`). Strong independent convergence — every single one landed on
"arpeggiated piano + warm pads + no drums/drop/vocals + continuously intensify + never
resolve", which is a good signal per this project's own draft-tournament philosophy
(convergent phrasing across independent reviewers = a real signal, not chance).

### The 5 raw candidates

**claude:** A slow-building dream-trance instrumental for a reverent short film: a single
arpeggiated piano figure cycling and slowly layering over warm, sustained atmospheric pads,
joined by a soft rising string swell and distant airy choir textures that thicken gradually
across the full 58 seconds. No drums, no bassline, no drop, no vocals — the arpeggio and
pads simply keep ascending in intensity and density, like Robert Miles' "Children" frozen
in its opening build, but sacred and hushed rather than euphoric, evoking hushed awe and
quiet reverence rather than club energy. The piece should feel like it is perpetually
rising toward a holy revelation it never quite resolves, ending still mid-ascent, unresolved
and suspended.

**codex:** 58-second instrumental sacred dream-trance build-up, referencing only the opening
section of Robert Miles' "Children": arpeggiated piano over warm synth pads, with solo cello
and faint pipe organ entering gradually. Begin as a hushed night conversation with Nicodemus,
then let the piano pattern widen and the pads swell continuously toward the image of the Son
of Man lifted up on the cross. Keep it reverent and awe-filled, with no vocals, no drums, no
beat/drop, and no club energy.

**grok:** Dream-trance cinematic score, sacred and awe-filled, never clubby. Slow arpeggiated
piano, warm analog pads, a low cello drone, and a distant pipe-organ swell begin in hushed
stillness and intensify without pause, gaining harmonic weight and lift for the full duration.
No drums, no kick, no drop, no vocals: one unbroken reverent ascent that stays in the
opening-build register and never resolves.

**cursor:** Dream-trance ambient score in the spirit of Robert Miles "Children" opening only:
slow arpeggiated piano over warm analog pads and soft string swells, reverent and awe-filled,
sacred not euphoric. No drums, no beat, no drop, no vocals, no club energy. Arc: begin sparse
and hushed, then continuously intensify through layered piano figures and widening pad
harmony for the full 58 seconds, rising toward a luminous peak that never resolves into a
pulse.

**gemini:** Sacred ambient dream-trance intro featuring a slow, arpeggiated acoustic piano
layered over warm atmospheric synthesizer pads and subtle cello swells. The arrangement is a
continuously intensifying, sustained build-up that rises steadily in reverence and awe. The
entire piece maintains this dreamy, rising tension without ever resolving into a beat, drop,
or percussion.

### Synthesized final prompt (my pick, ready to use as-is)

Merged the converging elements — deliberately dropped "choir" (this project's own locked
Suno-prompting rule says the standard closer is "instrumental only, no vocals, no choir, no
drums"; "choir" as a NAMED texture is safer left out entirely rather than risk any
vocal-like rendering) and dropped the narrative specifics ("Nicodemus", "the cross") since
the Eleven Music model responds to musical language, not story references:

> Sacred ambient dream-trance instrumental, reverent and awe-filled, never clubby: a slow
> arpeggiated piano cycling over warm analog pads, joined by a soft cello drone and a
> distant pipe-organ swell. The arrangement begins hushed and continuously intensifies in
> harmonic density and lift for the full length, rising steadily like the opening build of
> Robert Miles' "Children" — but sacred, not euphoric. No drums, no beat, no drop, no
> vocals: one unbroken ascent that never resolves into a pulse.

## What's NOT done yet — the next session's job

1. **Confirm the prompt** (use the synthesized one above, or pick/tweak from the 5 raw
   candidates) — quick judgment call, not a blocker.
2. **Generate the score.** Reuse the real, proven Eleven Music call shape from
   `sfx_pilots/add_music.py` (`MUSIC_URL = "https://api.elevenlabs.io/v1/music"`, POST
   `{"prompt": ..., "music_length_ms": N, "force_instrumental": true, "model_id": "music_v1"}`,
   header `xi-api-key` from `PythonProject1/.env`'s `ELEVENLABS_API_KEY` via
   `pipeline.assembly_align._resolve_key()`). Generate at ~61-62s (58s target + a couple
   seconds of ring-out margin, matching `add_music.py`'s own `outro` convention) so the
   piece never runs dry before the video ends. **METERED — historical Eleven Music
   generations in this project's spend ledger run ~$1 each; ask the user for explicit OK
   before the API call, per the standing ask-before-spending rule.**
   - **Do NOT apply `add_music.py`'s `reshape_music()` as-is** — it reshapes the arc to
     CREST at ~70% through and ease DOWN to a floor by the end (built for a piece that
     needs to settle under the landing CTA). This POC wants the OPPOSITE: a piece that
     stays in rising build-up register the WHOLE way, never easing down. Skip the
     reshape, or write a version that only stretches/trims (fixes Eleven's known
     "dies ~10s early" issue) without the ease-down volume curve.
3. **Mix it into `son_of_man_lifted_up`.** Don't reuse `add_music.py`'s `_mix_and_caption`
   verbatim (it targets the OLD `cli_assemble.py` folder layout, `<v1>/assembly/
   viral_cut_sfx.mp4`) — instead edit `son_of_man_lifted_up/_s5_score_sfx.py` directly:
   replace its `musA`/`musB` two-bed crossfade filter-graph inputs (currently
   `music_library/clips/lonely_searching_a.mp3` + `sacred_grace_rise_a.mp3`) with the ONE
   new Eleven-generated mp3 as a single continuous bed spanning 0-58s, keep the exact same
   `AFMT`/`SIDECHAIN` sidechain-ducking against the narration (from `pipeline/score_mix.py`)
   and the exact same 3 ambient SFX layers (wind/thunder/crowd) untouched.
4. **Landing-hold check** (`check_landing_hold.py`) + **eye/ear-check** the result before
   calling it done — listen to the whole thing, confirm the build never resolves
   awkwardly right at the landing line, confirm the narration is still clearly on top of
   the mix (per this project's own audio-layer-stack rule: narration -> MUSIC -> SFX,
   ducked, voice always audible).
5. This is a **POC** — if it works, it's a genuinely new score option for future shorts;
   if it doesn't (e.g. Eleven's music model can't actually sustain a build without ever
   resolving over 58s), that's a real, useful finding too. Report back either way, don't
   just silently keep it if it's mediocre.

## Files here

- `_PANEL_PROMPTS.md` — this file.
- `claude.txt`, `codex.txt`, `cursor.txt`, `gemini.txt`, `grok.txt` — raw panel outputs.
