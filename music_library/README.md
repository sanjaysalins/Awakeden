# music_library — reusable instrumental music beds (Suno)

Sibling to `sound_library` (SFX/ambience) and `image_library` (stills). Music is the
most reusable asset of all — a mood bed isn't story-specific, so one good track serves
many clips across shorts AND long-form. Generated on the user's **flat-rate paid Suno
plan** (commercial rights), NOT metered ElevenLabs credits.

## Files
- `CATALOGUE.md` — the 20-track design spec (Suno v5.5 style prompts + filenames + my
  red-team) — **AI-panel reviewed**.
- `_specs.py` — machine-readable tags/metadata for the 20 beds (source of truth for ingest).
- `music_library.py` — the library API (`find(tags=…, mood=…)`, register, import).
- `ingest.py` — pull Suno downloads from `_inbox/` → measure → tag → register.
- `_inbox/` — drop raw Suno `.mp3` downloads here.
- `clips/` — ingested, registered tracks. `index.json` — manifest.

## Workflow
1. **You (Suno v5.5, Instrumental ON):** generate a catalogue prompt, download **both**
   takes, save as `<slug>_a.mp3` and `<slug>_b.mp3`. Start with the ⭐PILOT beds only.
2. Drop both in `_inbox/`.
3. **Me:** `python ingest.py` → measures LUFS + dBFS, tags from `_specs.py`, registers
   both takes as **`status=pending`** (NOT yet selectable).
3b. **Auto-QC:** `python qc.py` → reliably flags **vocal leaks** (reuses Whisper — words = sung
   vocals → reject) and shows swell + LUFS. Drums + wordless pads are ear-checked (no reliable
   offline detector without librosa/Demucs).
4. **Audition gate:** listen, then `python approve.py <slug> --url <suno_url>` to make a
   good take selectable, or `python approve.py <slug> --reject --notes "vocals/drums/mud"`.
   Only **approved** tracks can be picked by the engine.
5. **Selection per clip:** `find_for_beat(beat, tags)` returns a doctrine-safe approved
   track for that Gospel-Five-Beat beat; downstream we trim/align + sidechain-duck it.

## Source of truth & honest status
- `_specs.py` is the single source of truth → `python _gen_catalogue.py` rebuilds
  `CATALOGUE.md` (never hand-edit the catalogue).
- The **beat-aligned music placer** (trim + climax-align to the CTA + duck) is **not built
  yet** — that's the Phase-1 pilot. The Well `enhance.py` trims from t=0 only.

## Locked usage rules (red-team + panel)
- **One melodic bed per clip.** Two melodic beds clash ("two music"). Only `glory_*`
  pad/drones (melody-free, rhythm-free) may layer under a melodic bed.
- **Doctrine matrix is enforced in code** (`BEAT_ALLOWED` + `find_for_beat`):
  `tension_*` / `urgent_*` / `lonely_*` / `lament_*` are **narrative-only** — never on the
  Conviction or Landing (grace-anchored, no-fear rule).
- **music_library ≠ sound_library.** Don't stack a `glory_*` pad AND `sound_library`'s
  `heavenly_choir_soft` on one landing — pick one.
