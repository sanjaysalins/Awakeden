# Music Placer — Phase-1 technical design (`placer.py`)

The piece the panel kept flagging: how a chosen library bed actually lands under a clip.
This is a **design spec**, built to satisfy the round-2 reviewers BEFORE any Suno spend.
It is implemented + proven during the pilot (4 beds on the John 4 short), not before.

## Reuse, do NOT duplicate (CLAUDE.md locked rule)
The hard parts already work and are proven on the Well clip — `placer.py` **generalizes**
them, it does not reinvent:
| need | reuse from | status |
|---|---|---|
| word-level timing of the narration | `11labs-testing/_align.py` → `veed_io.aligner.forced_align_script` | proven |
| sidechain-duck a bed under the voice | `11labs-testing/enhance.py` `mix()` `sidechaincompress=threshold=0.05:ratio=6...` | proven |
| place audio at a word timestamp | `enhance.py` (waterpot anchored to a word @ 37.8s) | proven |
| fades / adelay / alimiter / mux | `enhance.py` `mix()` filtergraph | proven |
| narration-safe gain target | `ingest.py` LUFS (`input_i`) | proven |

**New, bed-specific logic (the only ~30% to build):** trim-to-in-point + align-swell-to-CTA
+ duck-under-the-KJV-quote.

## Architecture decision (resolves "one bed vs five beats" AND "hook-only beds")
- **60s shorts = ONE primary melodic bed for the whole clip** (NOT per-beat swaps — too
  choppy at 60s). Because that one bed also covers the Landing, it **must be CTA-safe**
  (`find_for_beat("landing", …)` — so tension/urgent/lonely/lament are structurally
  impossible as the shorts **primary**). Optionally one `glory_*` pad layered under the landing.
- **Hook-only moods** (`lonely`/`lament`/`tension`/`urgent`) are NEVER the shorts primary.
  They serve as an **optional opening bed** that plays the first ~12s and **crossfades into**
  the CTA-safe primary (`placer.py --hook <slug>`). This is how `lonely_searching` is used in
  the pilot — as the hook open, not the spine. So the catalogue's hook beds and the one-bed
  rule are consistent: open (hook) → resolve (CTA-safe primary), a single melodic line that
  hands off once, plus the optional glory pad. No mid-clip melodic stacking.
- **Long-form (6–8 min) = one bed PER MOVEMENT** (7-movement spine), crossfaded at movement
  boundaries, pads looped/extended, music dipped under scripture. **Scoped to Phase 2** —
  out of the shorts pilot.

## Inputs
- `video` / `narration` (existing clip), `words.json` (from `_align.py`)
- `bed` = `MusicLibrary.find_for_beat("landing", tags=…)` (primary, approved, CTA-safe)
- `bed.swell_s` = the bed's climax time, logged at approval (`approve.py --swell`)
- optional `pad` = `MusicLibrary.find_layer(tags=["holy"])`
- `kjv_span` = (q0, q1): the verbatim KJV quote window, from `words.json`

## Algorithm
1. **CTA anchor** `t_cta` = start time of the Landing beat's first word (from `words.json`).
2. **In-point** so the bed's swell lands on the CTA:
   `bed_start = t_cta - bed.swell_s`; trim window `[bed_start, bed_start + clip_len]`.
   If `bed_start < 0`, shift to 0 and accept the swell a little early, or pick a section
   with an earlier swell (logged per take). Pads (no swell) just trim from 0.
3. **Gain** to a narration-safe target from `bed.lufs_i` (e.g. normalize so the bed sits
   ~−20 LUFS under the voice), then sidechain-duck (reuse `enhance.py` graph).
4. **KJV-quote intelligibility duck:** over `[q0, q1]` apply an extra −10 dB volume envelope
   on the bed so the verbatim Scripture stays clear (the engine's word alignment is known to
   drop words under music — `veed_io/aligner.py`).
5. **Optional glory layer:** `pad` at ~−26 dB under the landing only; no second melodic bed.
6. **Fades + mux:** afade in 0.5s / out 1.5s, `alimiter`, mux onto the video (reuse `mix()`).

## Pilot acceptance gates (must pass before batching the other 16)
- **Intelligibility:** run `veed_io.aligner.transcribe_align` on the final muxed audio →
  ≥ 98% of script words recovered (proves music doesn't bury the narration / KJV quote).
- **No clipping:** final `max_volume` < −1 dBFS; narration peak unchanged vs. original.
- **Doctrine:** the chosen primary bed came from `find_for_beat` (CTA-safe by construction).
- **Listen gate:** human approves the mix (no "two music", swell lands on the CTA).

## Suno reality / QC budget (gemini, cursor)
- "no drums" is unreliable in Suno; expect a rejection rate. Generate extra takes as needed
  (`_c`, `_d`, … — `ingest.py` accepts any suffix); `approve.py` requires one primary per base.
- Percussion is **intentional only** on `tension_*`/`urgent_*`/`triumphant_*` (narrative);
  any stray beat on a "no-drums" bed = reject at the audition gate.
