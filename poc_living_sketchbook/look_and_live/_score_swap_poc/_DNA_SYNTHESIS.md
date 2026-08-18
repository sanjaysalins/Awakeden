# Musical-DNA research pass — Robert Miles "Children" pre-drop build

**Status: research done, nothing generated/spent yet.** Follow-up to the first (mood-word)
panel pass in `poc_living_sketchbook/son_of_man_lifted_up/_score_swap_poc/_PANEL_PROMPTS.md`,
which produced the prompt already used for `LOOKANDLIVE_MILESPOC_cc_scored_sfx.mp4`. This round
asked for literal musical structure — BPM, key, chords, arpeggio mechanics, layering order,
instrumentation, dynamics arc — not mood words.

## Voices dispatched

- **Fable** (Anthropic model, via Agent tool) — OK, cited real sources (SongBPM, a published
  production case-study, Wikipedia, Chordify/ChordU, Tunebat).
- **claude, grok, codex** (local CLI panel via `independent_review.py`'s `run_one`/`PROVIDERS`,
  dispatched 2-at-a-time to stay gentle on CPU/RAM) — all OK.
- **cursor, gemini** — FAILED: both died in ~5s on a "Workspace Trust Required" interactive
  dialog (`cursor-agent` blocks headless execution in an untrusted-workspace state) — an
  environment issue, not a content failure. Same underlying CLI (cursor-agent) serves both the
  `cursor` and `gemini` voices in this project's panel config, so one root cause killed both.
  Worth fixing (`cursor-agent` workspace-trust flag/config) before the next panel round, but not
  blocking here — 4/5 voices answered, quorum for a research pass.
- Raw outputs: `dna_claude.txt`, `dna_grok.txt`, `dna_codex.txt`, this file. Fable's raw answer
  is quoted in the "Fable" bullet under Tempo/Key/etc. below via the session transcript, not a
  separate file (Agent tool result, not a local CLI file write).

## Convergent findings (3-4 way agreement — treat as reliable)

- **Tempo: 137 BPM**, straight 4/4. (Fable, grok, codex all landed here independently; claude's
  lone ~95-96 BPM guess is very likely a mix-up with the genre's *feel* — the Dream Version's
  own published/DJ-database tempo is 137, and 3 of 4 sourced voices agree.)
- **Key: F minor / natural minor (Aeolian)**, no modulation anywhere in the build (Fable, codex
  say F minor directly; grok says F# minor — a semitone off but same mode family/shape; all
  agree it's a single unmoving minor tonal center).
- **Chord loop: i – VI – III – VII** (tonic minor, then three major "color" chords borrowed from
  the relative-major family), one chord per bar, looped without variation through the whole
  build — no secondary dominants, no key change. (Fable: Fm-Db-Ab-Eb; grok: F#m-D-A-E, same
  shape. Codex reads a related VI-iv-i loop with added 9th/sus colors — a plausible alternate
  transcription of the same harmonic family, not a contradiction.)
- **The piano is NOT a single arpeggio line** — it's a two-hand architecture: a broken-chord
  ostinato (left hand, wide root-5th-octave-9th spread) under a simple, repeating melodic figure
  (right hand). The pattern itself barely varies bar to bar; only the chord root moves. What
  *reads* as a dense 16th-note arpeggio is partly the notes themselves and partly a **tempo-
  synced stereo/ping-pong delay** (eighth or dotted-eighth) filling the gaps between played
  notes — Fable and codex both independently flagged this delay-does-the-work detail.
  Load-bearing production trick, worth keeping in the brief.
- **Layering order across a patient ~24-bar / ~40-42s intro** (Fable and codex converge tightly
  here, both citing the same production case-study source):
  1. Bars 1-8 (~0-14s): piano ostinato alone, already in reverb/delay, plus a very low
     sustained sub-drone (felt more than heard) and a soft percussive organ-type stab marking
     the pulse.
  2. Bars 9-16 (~14-28s): ONE new secondary color joins — a clean/muted plucked layer
     (guitar-like) — piano continues unchanged underneath.
  3. Bars 17-24 (~28-42s): a deliberate thinning (the organ stab drops out) then a crescendo via
     rising piano intensity plus a snare-roll build in the final 4 bars, foreshadowing an
     arrival without yet delivering any low end.
  4. (Outside this POC's scope: the drop — full kick/bass/pads landing all at once. Our piece
     stays in stages 1-3 forever, never reaching this.)
- **Dynamics arc**: near-flat, quiet opening; growth is ADDITIVE (new layers stacking), not a
  volume fader ride; low end is essentially absent the entire build; stereo image starts
  narrow/centred on the piano and widens as the pad spreads; a deliberate thin-then-swell shape
  late in the build (mirrors the layering order above).
- **Space**: one big shared cathedral/hall reverb so phrase-ends bloom into the room (piano
  stays present/close, the bed feels spacious); NO sidechain pumping anywhere in this section
  (nothing to duck against — that's a post-drop technique).
- **Instrumentation, convergent core**: bright, reverbed/delayed sampled piano (glassy attack,
  moderate decay — not a dark Rhodes); warm slow-attack pad/string bed; a felt-not-heard
  sustained sub-drone; a soft percussive organ-type stab; one plucked secondary texture late.
  Fable and codex both independently named the **Kurzweil K2000** as the actual hardware — a
  striking specific convergence, though not something to put in a text-to-music prompt verbatim
  (irrelevant to a generator; the resulting *timbre character* is what matters).

## Divergent / lower-confidence points (noted, not used as load-bearing)

- claude's ~95-96 BPM and its i-VII-VI-v progression reading diverge from the 3-way consensus —
  self-flagged low confidence on exact numbers; treated as an outlier here.
- grok's layering description (generic pad-first / filter-sweep-riser build) is vaguer and less
  sourced than Fable/codex's matching 24-bar breakdown — kept the more specific, convergent
  version.
- The exact drop mechanism (hard additive slam per Fable/codex vs. filter-sweep reveal per grok)
  doesn't matter for this POC since our piece never reaches the drop.

## Translating the DNA into a SAFE, un-named ElevenLabs prompt

ElevenLabs Music hard-blocks named artist/song references (confirmed live yesterday — a 400
"bad_prompt" on directly naming "Robert Miles' Children"). Every candidate below describes the
structure in pure musical language only, and keeps the sacred/reverent register (cello + pipe
organ standing in for the original's guitar pluck + house organ stab — safer, more devotional,
already validated in yesterday's accepted prompt) rather than the original's secular "dream
house" instrumentation.

### Candidate A — full technical brief (closest to the real DNA)

> Sacred instrumental for a reverent short film, 137 BPM, in a minor key, one continuous rising
> build that never resolves. A reverbed piano plays a repeating two-hand figure: a steady
> broken-chord ostinato under a simple, hypnotic melodic line, looping a slow four-chord minor
> progression — tonic minor, then two warm major color-chords, then a fourth minor-adjacent
> chord — the same chord shape returning again and again without ever resolving to a final
> cadence. A tempo-synced stereo echo trails every piano note, thickening the texture. The piece
> opens with piano alone in a vast cathedral reverb; a warm sustained string pad and a low
> felt-more-than-heard drone join first; then a solo cello and a distant pipe-organ swell
> arrive. In the final third the texture briefly thins, then swells again, gaining harmonic
> density and stereo width, as if gathering for an arrival it never reaches. No drums, no
> bassline, no drop, no vocals, no choir: pure continuous ascent, reverent and awe-filled,
> ending still mid-rise, suspended and unresolved.

### Candidate B — concise, closer to yesterday's accepted wording, DNA-enriched

> Sacred ambient dream-trance instrumental, 137 BPM, reverent and awe-filled, never clubby: a
> bright reverbed piano plays a repeating broken-chord ostinato under a simple hypnotic melody,
> looping a slow four-chord minor progression that never resolves. A tempo-synced echo doubles
> every note. Piano begins alone; a warm string pad and a low sustained drone join first, then a
> solo cello and a distant pipe-organ swell. The arrangement continuously intensifies in
> harmonic density, loudness, and stereo width for the full length — like the opening build of a
> classic 1990s dream-trance anthem, but sacred, not euphoric. No drums, no beat, no drop, no
> vocals: one unbroken ascent that never resolves into a pulse.

### Candidate C — leans harder into the layering-order stages (most literal structure match)

> A 137 BPM sacred instrumental in a minor key that only ever builds, never resolves, in three
> patient stages. Stage one: a reverbed piano alone, playing a repeating broken-chord ostinato
> under a simple melodic figure, looping a four-chord minor progression, tempo-synced echo
> trailing every note, a very low sustained drone barely audible beneath it. Stage two: a warm
> string pad and a solo cello join, widening the space around the still-unchanged piano figure.
> Stage three: the texture briefly thins, then swells with a distant pipe-organ and rising
> harmonic density and stereo width, gathering toward an arrival that never comes. No drums, no
> bassline, no drop, no vocals, no choir: continuous devotional ascent, ending suspended,
> mid-rise, unresolved.

## Next step (not done yet)

Present A/B/C to the user, get a pick (or edits/a merge), confirm which — and how many — to
actually generate (METERED, ~$1/generation per the spend ledger), generate at ~61-62s to match
Look and Live's real runtime with ring-out margin, mix into a new candidate file (same pattern
as `_generate_and_mix.py`), then ear-check before calling any of it done.
