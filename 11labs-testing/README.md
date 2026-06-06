# 11labs-testing — audio enhancement test (Well / John 4)

Independent test: take the finished **viral_cut.mp4** (already narrated) and layer an
ElevenLabs **music score + event-timed SFX** *under* the narration, ducked so the voice
stays on top. Reuse-first: 3 of 5 layers come free from `../sound_library`.

Source clip:
`G:\My Drive\0 Personal\0Company\jobs\0salinss\saltandlightkingdom\0 Christianity\0 People Who Encountered Jesus\08 The Well That Never Runs Dry\viral_cut.mp4`

## Result — DONE (all 5 layers, music included)
- **Enhanced cut:**
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\11labs-testing\viral_cut_enhanced.mp4`
- Eleven Music score generated (`music_generation` scope enabled 2026-06-06). Final mix
  59.0s, mean −20.5 dB / max −3.8 dB (no clipping; music sidechain-ducked under the voice).
- `user_read` scope still off → exact credits not auto-reported; check the dashboard.

## Layer plan (under the narration)
| layer | source | when | cost |
|---|---|---|---|
| 🎵 music score | Eleven Music (instrumental, swells to grace) | 0–59s, ducked | metered — **BLOCKED** |
| 💧 well-water trickle | `river_well_water` (library) | full bed, -20dB | $0 reuse |
| 🏘️ faint noon "whispers" | `marketplace_chatter` (library) | 0–11s fade, -30dB | $0 reuse |
| 🏺 waterpot drop + run-off | new SFX (`waterpot_drop_run`) | 37.8s, -6dB | metered ✓ done |
| ✨ holy choir swell | `heavenly_choir_soft` (library) | 47–59s, -22dB | $0 reuse |

SFX anchored with WhisperX forced-alignment: "she dropped her **waterpot** and **ran**"
lands at **38.08–39.40s** (see `work/words.json`).

## Reusable library
The new SFX is registered into the shared pool for every other project:
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\sound_library\clips\waterpot_drop_run.mp3`
(slug `waterpot_drop_run`, `reuse_scope: neutral`). The library is now 29 clips —
generate once, tag, reuse; never re-pay ElevenLabs.

## To finish the music
The key generates TTS + sound-effects but NOT music. In the ElevenLabs dashboard →
**API Keys → edit this key → enable `Music Generation`** (and `User: Read` so spend can
be auto-reported). Eleven Music may also require a paid plan tier. Then:
```
.venv\Scripts\python.exe 11labs-testing\enhance.py --generate --yes   # music only (sfx cached)
.venv\Scripts\python.exe 11labs-testing\enhance.py --mix              # rebuild WITH music
```

## Files
- `enhance.py` — plan / generate (metered, --yes gated) / mix
- `_align.py` — WhisperX forced-align of the narration → `work/words.json`
- `layers/` — generated layers (waterpot.mp3; music.mp3 when unblocked)
- `work/` — extracted narration audio + word timings
