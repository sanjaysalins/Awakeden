# Music Library Catalogue — instrumental beds (Suno v5.5)

> AUTO-GENERATED from `_specs.py` (`python _gen_catalogue.py`). Do not hand-edit — edit `_specs.py` and regenerate, so prompts/tags never drift.

Reusable **instrumental** music beds for the gospel engine (60s shorts + 6–8 min long-form). Generated on the user's flat-rate paid Suno plan (commercial rights), NOT metered ElevenLabs credits. Sibling to `sound_library` (SFX) / `image_library` (stills).

**Suno settings (every track):** v5.5 · **Instrumental = ON** · save **both** takes as `<slug>_a.mp3` + `<slug>_b.mp3` → drop in `_inbox/` → `python ingest.py`.
**Count:** 20 prompts × 2 takes = **40 raw files** → audition → approve **one primary take per base slug** (`_a`/`_b`/… are candidates; extra takes OK if both have ghost drums/vocals). Not a guaranteed 20.

## Status (honest)
- ✅ Built: library API, specs, ingest (LUFS + dBFS), audition/approve gate (`approve.py`: blocks a 2nd take per base unless `--force`; requires `--swell` on arc beds), doctrine-aware PRIMARY selection (`find_for_beat`; energy-fit is a ranking bonus, not a hard filter — a wrong-energy bed only loses if a better-fit one is approved), layer selection (`find_layer`, glory pads only).
- ✅ **`placer.py` is BUILT + PROVEN** on John 4 (4 pilot beds, 2026-06-06): lonely hook → sacred swell auto-aligned to the landing @ 47.8s → glory pad under the close, all ducked. **STT word-recovery 99.4%** (gate ≥98%), 59.0s, no clipping. Swell auto-detected via numpy RMS envelope. Generalizes the proven `enhance.py mix()`. See `PLACER.md`.
- 🔁 Eleven Music is the bespoke-per-clip fallback (key scope enabled 2026-06-06, so it works — but it's **metered**, so a reused Suno bed is preferred).

## Shorts vs long-form architecture (resolves one-bed-vs-five-beats)
- **60s shorts = ONE primary melodic bed for the whole clip** (not per-beat swaps). Because it also covers the Landing it must be **CTA-safe** (picked via `find_for_beat('landing', …)`), + an optional `glory_*` pad layered under the landing.
- Music **ducks to near-silent under the verbatim KJV quote** (intelligibility — the aligner drops words under a music bed). Pilot gate = STT word-recovery ≥ 98%.
- **Long-form = one bed per movement**, crossfaded; pads looped; music off under scripture. **Phase 2** — out of the shorts pilot.

## Staged plan (test-gate discipline — don't batch all 20 first)
0. **Lock design (done):** `PLACER.md` + metadata/gates in code.
1. **Pilot (4 beds):** generate `sacred_grace_rise, lonely_searching, neutral_teaching_warm, glory_holy_stillness` (ingest is pilot-gated — `--all` to override). `placer.py` is built; **prove** it on John 4 against the acceptance gates in `PLACER.md` (`lonely_searching` = the hook open that crossfades into the CTA-safe `sacred_grace_rise` primary, + `glory` pad layer).
2. **Batch the rest** only after the loop passes and the look is locked.
3. Every track stays `status=pending` (unselectable) until a human audition approves it; arc beds require a `--swell` timestamp at approval.

## Beat → mood doctrine matrix (enforced in code by `find_for_beat`)
LOCKED: grace-anchored conviction — NO fear/pressure/unresolved-ache on the Conviction or Landing. `tension`/`urgent`/`lonely`/`lament` are narrative-only.

| beat | allowed PRIMARY moods |
|---|---|
| hook | awe, lament, lonely, neutral, tension, urgent |
| point | awe, neutral, pastoral, sacred, tender |
| proof | awe, neutral, sacred, tender, triumphant |
| conviction | neutral, pastoral, sacred, tender |
| landing | neutral, pastoral, sacred, tender, triumphant |

**Layer (not primary):** `glory_*` beds are melody-free / rhythm-free — `find_for_beat` NEVER returns them; `find_layer()` does. They're the only safe second musical element under a primary bed. One primary melodic bed per clip.

## Boundaries
- **music_library vs sound_library:** music = melodic/score/atmosphere *beds*; sound_library = ambient SFX + one-shots (incl. the existing `heavenly_choir_soft` swell). Don't stack a `glory_*` pad AND the choir SFX on one landing — pick one.
- **Suno bed vs Eleven Music:** default to a reusable Suno bed ($0, flat plan). Use a bespoke Eleven Music score only when a clip needs a custom-timed climax and the spend is OK.
- **License:** Suno paid plan grants commercial USE but not copyright protection. `ingest.py` records `source/license/created`; add the Suno export URL via `approve.py --url`.

## The Suno v5.5 style prompts (instrumental)
> Paste each into Suno's **Style** box, Instrumental ON. Tempo is given as musical terms (Suno ignores numeric BPM).

### SACRED — devotional grace, melodic — the flagship beds
**`sacred_grace_rise`**  ⭐PILOT → `sacred_grace_rise_a.mp3`, `sacred_grace_rise_b.mp3`  ·  beats: point, proof, conviction, landing
`Cinematic neoclassical film score, sacred and tender; solo piano, warm strings, subtle duduk; starts intimate and sparse, one steady build to a warm redemptive climax near the end, then gentle resolve; clean film-score mix, instrumental only, no vocals, no choir, no drums`

**`sacred_intimate_piano`** → `sacred_intimate_piano_a.mp3`, `sacred_intimate_piano_b.mp3`  ·  beats: point, proof, conviction, landing
`intimate sacred solo piano with delicate string pad underneath, prayerful, hushed, tender devotional, lots of space and air, chamber, no percussion, slow adagio`

### LONELY — sparse, hollow, unresolved (hooks, outcasts) — narrative-only on the CTA
**`lonely_searching`**  ⭐PILOT → `lonely_searching_a.mp3`, `lonely_searching_b.mp3`  ·  beats: hook
`Sparse neoclassical cinematic, hollow and searching; lone cello and distant duduk over faint ambient strings; very slow, lots of space, unresolved; instrumental only, no vocals, no choir, no drums`

**`lonely_windswept`** → `lonely_windswept_a.mp3`, `lonely_windswept_b.mp3`  ·  beats: hook
`desolate ambient cinematic, low drone with a thin lonely ney flute, windswept wilderness, bleak and barren, sustained dark strings, sense of isolation, no rhythm, no drums`

### TENDER — warm human compassion, mercy, hope
**`tender_compassion`** → `tender_compassion_a.mp3`, `tender_compassion_b.mp3`  ·  beats: point, proof, conviction, landing
`tender cinematic, warm strings and soft harp, gentle and compassionate, comforting, mercy and kindness, hopeful glow, chamber orchestra, no drums, gentle andante`

### NEUTRAL — unobtrusive exposition bed (the Point beat + long-form teaching stretches)
**`neutral_teaching_warm`**  ⭐PILOT → `neutral_teaching_warm_a.mp3`, `neutral_teaching_warm_b.mp3`  ·  beats: hook, point, proof, conviction, landing
`Understated cinematic underscore, calm and neutral; soft warm strings and gentle piano, low-key; steady and unobtrusive with room for a narrator, no big melody; instrumental only, no vocals, no choir, no drums`

**`neutral_teaching_low`** → `neutral_teaching_low_a.mp3`, `neutral_teaching_low_b.mp3`  ·  beats: hook, point, proof, conviction, landing
`minimal ambient underscore, soft low strings and a subtle warm pad, very understated background bed, neutral and calm, leaves space for a speaking voice, no melody hooks, no drums, larghetto`

### AWE — mounting crescendo, revelation, wonder
**`awe_revelation_build`** → `awe_revelation_build_a.mp3`, `awe_revelation_build_b.mp3`  ·  beats: hook, point, proof
`cinematic crescendo, building orchestral strings layered with a soft wordless choir pad, mounting wonder and revelation, steadily rising to an awe-struck peak, epic but reverent, no drum beat, moderate moderato`

**`awe_holy_mystery`** → `awe_holy_mystery_a.mp3`, `awe_holy_mystery_b.mp3`  ·  beats: hook, point, proof
`mysterious sacred ambient, shimmering high strings over deep low cello, glassy bells, sense of the divine drawing near, holy and otherworldly, slow swelling, no percussion`

### TRIUMPHANT — victory, resurrection, the King
**`triumphant_resurrection`** → `triumphant_resurrection_a.mp3`, `triumphant_resurrection_b.mp3`  ·  beats: proof, landing
`triumphant cinematic orchestral, bright full strings and soaring brass, radiant and victorious, redemptive resurrection swell, glorious and uplifting, majestic and kingly, epic finale, light timpani swells, lively allegretto`

### LAMENT — grief, suffering, the cross — narrative-only on the CTA
**`lament_suffering_cello`** → `lament_suffering_cello_a.mp3`, `lament_suffering_cello_b.mp3`  ·  beats: hook
`mournful cinematic, grieving solo cello over low sustained strings, sorrowful and heavy, the weight of suffering, aching lament, dark chamber, no drums, very slow grave`

**`lament_forsaken`** → `lament_forsaken_a.mp3`, `lament_forsaken_b.mp3`  ·  beats: hook
`desolate sacred lament, near-silent sparse strings and a distant lone violin, abandonment and anguish, hollow grief, almost ambient, trembling, no percussion, extremely slow`

### TENSION — dread, threat, chaos — NARRATIVE villainy ONLY, never conviction/landing
**`tension_dread_pulse`** → `tension_dread_pulse_a.mp3`, `tension_dread_pulse_b.mp3`  ·  beats: hook
`dark cinematic tension, low pulsing string ostinato, no melody, mounting dread and unease, ominous undertow, creeping threat, sparse low percussion pulse, driving moderate`

**`tension_storm_unrest`** → `tension_storm_unrest_a.mp3`, `tension_storm_unrest_b.mp3`  ·  beats: hook
`agitated cinematic storm, frantic tremolo strings and swelling low brass, chaos and turmoil, rising percussion swells, danger and unrest, dramatic, intense`

### GLORY — holy stillness, PAD/DRONE (no melody → the only safe layer partner)
**`glory_holy_stillness`**  ⭐PILOT → `glory_holy_stillness_a.mp3`, `glory_holy_stillness_b.mp3`  ·  beats: (narrative-only)
`Sacred ambient drone, weightless and holy; sustained ethereal pad with soft low strings; timeless, no melody, no rhythm, slow evolving texture; instrumental only, no vocals, no choir, no drums`

**`glory_light_descending`** → `glory_light_descending_a.mp3`, `glory_light_descending_b.mp3`  ·  beats: (narrative-only)
`radiant sacred ambient, slowly swelling warm pad with gentle glassy bells and soft high strings, the divine breaking in, light descending, glowing and holy, no beat, no drums`

### PASTORAL — peace, rest, the shepherd
**`pastoral_still_waters`** → `pastoral_still_waters_a.mp3`, `pastoral_still_waters_b.mp3`  ·  beats: point, conviction, landing
`peaceful pastoral cinematic, gentle flowing strings and soft harp with light woodwind, restful and serene, still waters, green pastures, calm reassuring, no drums, gentle andante`

**`pastoral_shepherd_calm`** → `pastoral_shepherd_calm_a.mp3`, `pastoral_shepherd_calm_b.mp3`  ·  beats: point, conviction, landing
`warm folk-orchestral, simple gentle acoustic strings and soft flute, comforting and homely, the good shepherd, pastoral calm, intimate, no drums, moderate andante`

### URGENT — forward motion, the call — narrative-only on the CTA
**`urgent_journey_drive`** → `urgent_journey_drive_a.mp3`, `urgent_journey_drive_b.mp3`  ·  beats: hook
`driving cinematic strings, light rhythmic staccato ostinato, forward momentum and travel, a determined journey, propulsive but orchestral, taut frame-drum pulse, driving allegro`

**`urgent_call_rising`** → `urgent_call_rising_a.mp3`, `urgent_call_rising_b.mp3`  ·  beats: hook
`rising cinematic urgency, accelerating layered strings building insistently, a summons, a moment of decision, mounting resolve to a decisive hit, orchestral, urgent allegro`
