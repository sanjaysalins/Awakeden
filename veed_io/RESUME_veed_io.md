# RESUME — veed_io (VEED.io captions + offline caption replica)

> Kept separate from the repo-wide `RESUME.md` on purpose — that file is being
> edited by another concurrent session. Pick this up tomorrow from here.

Last worked: 2026-06-03. All paths absolute from
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\veed_io\`.

## What this is
Two independent things, both self-contained in `veed_io/` (no coupling to the
gospel-shorts engine):

1. **VEED subtitle integration** (fal.ai `veed/subtitles`) — `client.py`,
   `cli.py`, `models.py`, `presets.py`, `pricing.py`, `banner.py`, `env.py`.
   Spend-gated (loud red banner, fail-closed `--yes`). Needs `FAL_KEY`
   (auto-loaded from repo-root `.env`). Metered: $0.10/min basic, $0.20/min
   dynamic.

2. **OFFLINE caption replica** of the user's VEED look — `serif_captions.py`
   (ASS/ffmpeg renderer) + `caption.py` (one-command wrapper). **$0/video, no
   API.** This is the part we iterated on all session and LOCKED.

## DYNAMIC mode (NEW 2026-06-05 — now the default)
The enlarged key word + italic are driven by the **real vocal emphasis** measured
from the narration audio (`prosody.py`: per-word RMS loudness + duration → phrase-
local z-score + light text prior). The **big word follows the stress** (which word,
not where on screen), its **size breathes** with how hard the stress lands
(`BIG_FS_MIN..MAX`), and the **italic moves** to the runner-up word. Stopword guard
keeps a loud "the" small.

**STABLE FOCAL (updated 2026-06-05):** the big word's baseline is pinned to ONE
fixed Y every phrase (`Layout.big_anchor_y`, lower third) so the eye rests in a
single spot — no more inter-phrase drift. before/after lines stack above/below it.

**ASPECT-ADAPTIVE (2026-06-05):** `build_layout(w,h)` auto-detects the clip.
- **9:16 portrait** → keeps the YouTube-Shorts no-go zones.
- **16:9 landscape** (long-form deep-dives) → drops Shorts chrome, calm lower-third
  margins. Every font/margin scales by `h/REF_H`, so a word is the same FRACTION of
  frame height either way. Verified 1280x720 render.

- Default ON. `--static` restores the old LOCKED fixed look (big always mid, italic
  on all connectors, 2-slot drift).
- Knobs: weights in `serif_captions._dynamic_emphasis`; `BIG_FS_MIN/MAX`; portrait
  vs landscape geometry inside `serif_captions.build_layout`.
- Proven 2026-06-05 on "The Well That Never Runs Dry" (ep08):
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\veed_io\out\well\well_stable.mp4`
  contact sheet: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\veed_io\out\well\contact_stable.png`
  16:9 demo: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\veed_io\out\well\demo_16x9.mp4`

## EXACT timing — WhisperX forced alignment (NEW 2026-06-05)
Long-form had loose caption timing (faster_whisper drops words under the music
bed → the missing words were interpolated → drift). Fixed with **WhisperX**
(`aligner.py`): phoneme (wav2vec2) **forced alignment of the known script** —
every KJV word is snapped to the audio acoustically, nothing interpolated.
- `caption.py --aligner {auto,whisper,whisperx}`. **auto** = whisperx for 16:9 OR
  clips ≥120s (long-form), faster_whisper for shorts. Installed: torch 2.8 CPU,
  whisperx (numpy unchanged at 2.4.6).
- `aligner.forced_align_script` = the exact path (script known); `transcribe_align`
  = ASR+align (script unknown). A `_monotonic` pass clamps seam overlaps so two
  phrases never flash at once.
- **GOTCHA — feed a CLEAN spoken script.** A long-form `narration.md` has a trailing
  `## DEPTH & SOURCING` / `## VOICE PLAN` ledger that is NOT spoken. forced-align
  tries to place every script word in the audio, so those notes corrupt it. Use
  `veed_io/_extract_spoken.py <narration.md> <out.txt>` — keeps prose ONLY inside
  `## MOVEMENT` sections. (Roadmap: fold into `--script auto`.)
- First run downloads the wav2vec2 align model (~360MB); offline after. The
  `torchcodec ... could not load` warning is harmless (pyannote VAD falls back).
- Proven 2026-06-05 on the Isaiah 53 16:9 film (405s): forced-aligned **1177/1177**
  script words, 0 interpolated; 5/5 spot-checks word-exact (believed·wounded·All·
  Nazareth·Jesus). `...\veed_io\out\isaiah53\Isaiah53_16x9_whisperx.mp4`
  sync sheet: `...\veed_io\out\isaiah53\contact_whisperx_sync.png`

## LOCKED caption recipe (the STATIC fallback — `--static`)
Font **Inter** · colour **#F4F0D8** · one **big bold key word on its own line** ·
mid-phrase connector words **italic + slightly larger** · trailing word
**indent-tucked under the key word** (quote lockup) · **near-zero line gap**
(LINE_STEP_FACTOR ~0.70) · **whisper-subtle shadow (1)**, no border · **gentle
fade only, no zoom pop** · **two close left positions** (calm drift) · clamped
inside **YouTube Shorts no-go zones** (top150/bottom420/right190/left40).
All knobs are constants at the top of `serif_captions.py`.

## How to caption any clip (one command, offline)
```powershell
# RUN VIA POWERSHELL — the Bash-tool ffmpeg segfaults on fontconfig.
.venv\Scripts\python.exe -m veed_io.caption --video "CLIP.mp4"
# perfect words (force-align to exact script):
.venv\Scripts\python.exe -m veed_io.caption --video "CLIP.mp4" --script "narration.txt"
# QA the Shorts safe zones (red overlay):
.venv\Scripts\python.exe -m veed_io.caption --video "CLIP.mp4" --guides
# reuse/hand-fixed timings: --words clip.words.json   overrides: --color #RRGGBB --shadow 0 --no-indent --model small.en
```
Timings come from offline **faster_whisper** (`base.en`, installed). `--script`
transcribes for timing then difflib-aligns words to the script so mis-hears are
corrected (verified ASR "docked" -> scripted "stocked").

## Proven on
- "Who Do You Say I Am" (QJA 01): `out/who/who_LOCKED.mp4` (final locked look),
  `out/who/who_onecmd.mp4` (one-command), `out/who/who_guides.mp4` (safe-zone QA)
- Bread short: `out/bread_scriptfix.mp4` (force-align fix demo)
- VEED preset gallery (metered, already paid): `out/index.html` (28 presets)

## Outputs / media
`veed_io/out/` (~1.1 GB) is **gitignored** — media persists on disk but isn't
committed. Fonts in `veed_io/fonts/` (Inter upright+italic, OFL) ARE committed.

## Spend this session
**$1.79 total** — all on the early metered VEED preset tests (28 presets + the
glide/whisper/fusion trials on the Bread clip). Every caption-engine render was
**$0** (offline). fal.ai dashboard is authoritative.

## NEXT (pick up here tomorrow)
1. **Caption the rest of the QJA series** with the locked one-command tool. The
   source clips live under the Google-Drive "Questions Jesus Asked" folders; the
   "Why Are You Afraid" (QJA 02) export already has captions burned in, so it
   needs the caption-FREE master to re-style.
2. **Auto-find the script**: add `--script auto` to pull the exact narration text
   from the episode's engine folder / `timeline.json` automatically (today you
   pass the path by hand; Bread's came from assembly `timeline.json`).
3. Optional polish: try `--model small.en` for cleaner first-pass transcripts;
   consider a true forced-aligner (WhisperX) only if difflib timing ever drifts.
4. Decide whether the VEED metered path is still wanted now that the offline
   replica is locked (offline = $0 and matches the look).

## Memory written (persists across sessions)
`veed-io-offline-caption-replica`, `veed-io-fusion-findings`,
`feedback-veed-io-spend-control` (in the project memory dir).
