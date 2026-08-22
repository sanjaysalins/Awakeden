# Score style bank — dream trance / dream house

Locked 2026-08-22 on the Jacob's Ladder pilot. Every prompt below was
generated via ElevenLabs Music (`model_id: music_v1`, `force_instrumental:
true`) and judged by ear in a real bake-off — not picked from description
alone. Audio samples live in `references/score_bank/` (one per prompt, ~40s
or full-episode length as noted). Regenerate at a NEW episode's own length
with the pattern in `generate_full_variants.py` / `generate_score.py`
(both in `poc_living_water_ink_style_test/swirls_pilot_01_jacobs_ladder/`) —
same prompt text, `music_length_ms` set to that episode's own
narration-length + 3.0s landing hold + a ~2.5s margin, then trimmed with a
short fade in/out.

**Mixing note (important, cost real debugging time):** do NOT reuse
`pipeline/score_mix.py`'s shared `mix_tail()` / `SIDECHAIN` constant for
any of these — that duck (threshold=0.12, ratio=2.5) is tuned for this
repo's usual ambient orchestral pads and crushes a rhythmic groove to
near-inaudibility under continuous narration. Use the looser duck in
`mix_score.py` (`MUSIC_GAIN_DB = -4`, `DUCK_THRESHOLD = 0.35`,
`DUCK_RATIO = 1.6`) instead, and verify with a before/after `volumedetect`
sweep (narration-only vs scored, at several timestamps) BEFORE calling a
mix done — the first attempt at this looked fine by eye but was silent by
ear. See `feedback_ink_motif_animation_unsafe`-style memory discipline:
measure, don't assume.

## B — "1990s Dream Trance" — LOCKED for Jacob's Ladder

> 1990s dream trance, ethereal acoustic piano lead, melancholic but
> uplifting melody, driving 4/4 house beat, sweeping ambient synth pads,
> deep hypnotic bassline, soothing electronic, instrumental, nostalgic
> club comedown, atmospheric, 135 bpm

Sample: `references/score_bank/dream_trance_b_locked_sample.mp3` (full
62.04s, the actual locked Jacob's Ladder length). This is the user's own
revised prompt (an earlier draft of this candidate was accidentally an
image/video prompt — camera framing, a "Negative Prompt:" block — flagged
and replaced with this one before generating).

## C — "Dream House" — reference, not yet used on an episode

> Pioneering dream trance / dream house style: simple looping emotional
> piano melody in minor key, lush atmospheric synth pads and soft strings,
> steady but restrained four-on-the-floor kick, heavy reverb and delay
> creating a spacious dreamy soundscape, subtle acoustic guitar elements,
> mid-tempo around 138 BPM, instrumental, melancholic yet gently
> uplifting, nostalgic and hypnotic atmosphere, organic electronic fusion

Sample: `references/score_bank/dream_house_c_sample.mp3` (40s bake-off
sample). **Note:** the user's original prompt named "Robert Miles
'Children'" as a reference — ElevenLabs Music's ToS hard-blocks named
artist/song references, so that clause is stripped here; every other
descriptor is verbatim. User confirmed this is a good direction ("C is
also good").

## D — "90s Dream-House, Breakdown-Built" — reference, not yet used

> A mid-90s instrumental dream-house track at 137 BPM. A wistful minor-key
> piano melody carries the entire hook — no vocals, no acid line, nothing
> to replace it. Underneath, a soft four-on-the-floor kick and gentle
> offbeat hats, mixed back rather than forward. Wide ambient pads and
> string-like synth washes with long reverb tails fill the space. The
> arrangement is built around its breakdowns rather than its drops: it
> builds, then withdraws into near-silence with just piano and pad, then
> returns. Emotionally bittersweet and calming despite the tempo — a
> come-down record you can still dance to. No aggression, no hoover
> stabs, no rave riffs.

Sample: `references/score_bank/dream_house_d_breakdown_sample.mp3` (40s
bake-off sample). User confirmed this is a good direction ("D is also
good") — the "builds around its breakdowns" structural idea is worth
reusing on a future episode whose narration has a real hush-then-return
shape.

## Combo E — "Piano-Led Comedown" (B's drive + C's guitar + D's breakdown)

> A 1990s instrumental dream house / dream trance track, around 136 BPM.
> An ethereal acoustic piano lead carries a melancholic but uplifting
> melody throughout. A driving four-on-the-floor kick and deep hypnotic
> bassline underpin the groove, warm and steady rather than aggressive.
> Sweeping ambient synth pads and soft strings fill the space with long
> reverb tails, and subtle acoustic guitar textures thread through
> quietly underneath. The arrangement breathes: it builds, then withdraws
> into a near-silent breakdown of just piano and pad, before returning to
> the full groove. Instrumental, nostalgic, hypnotic, and calming — a
> genuine 90s club comedown record.

Sample: `references/score_bank/dream_combo_e_sample.mp3` (full 62.04s,
generated as an alternate for Jacob's Ladder; B was picked instead).

## Combo F — "Sparse Trance Hybrid" (leans into C/D's restraint)

> A restrained 1990s dream trance instrumental at 135 BPM. A simple,
> looping, wistful piano motif in a minor key is the emotional center. A
> soft four-on-the-floor kick and gentle offbeat hats stay mixed well
> back, felt more than heard. Warm synth bass moves slowly underneath.
> Ethereal pads and soft strings stretch out with heavy reverb and delay,
> spacious and dreamlike. The track favors quiet over intensity — no big
> drop, just a slow emotional swell and release. Melancholic, hypnotic,
> nostalgic, gently uplifting, instrumental, cinematic.

Sample: `references/score_bank/dream_combo_f_sample.mp3` (full 62.04s,
generated as an alternate for Jacob's Ladder; B was picked instead).

## Picking between them for a future episode

- Driving, present, club-comedown feel, episode has a clear single arc →
  **B** (locked default until proven wrong elsewhere).
- Episode leans quieter/more contemplative throughout → **C** or **Combo F**.
- Episode's narration has a real hush-then-return shape (a quiet middle
  beat, then a lift back up) → **D** or **Combo E** — both are built
  around a breakdown, not a drop.
