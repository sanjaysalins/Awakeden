# Jacob's Ladder: new CINEMATIC score (design only, nothing made, $0 spent)

Fable design seat, 2026-11-16. Owner said: "change the score, it feels too modern and needs to be cinamatic."

## Owner summary (short)

- **You are right.** The score now is a 1990s dance track: club kick drum, bass line, synth pads, 135 beats a minute. It never changes for 55 seconds.
- **New score:** warm strings, harp, one soft French horn. No drums. No synth. No piano. Slow.
- **One idea:** the harp plays 4 steps going UP (the ladder). It never reaches home. At "God came to him first" the 4 steps come DOWN and land home. The music says what the words say.
- **Quiet under the voice.** Now the music sits only 3 dB under the voice. New: 16 dB under. It rises only in the gaps and at the end.
- **End:** music lifts in the last hold, then a slow 2.5 s fade to the last frame (your Nazareth rule).
- **Voice, pictures, wind and bird sounds: not touched.**
- **Cost:** about **$1.00** first take. Cap **$2.00** with retakes. Billed to **ElevenLabs** (not OpenArt, not Higgsfield).

**Say yes to this score at about $1.00 (cap $2.00)?**

---

## 1. Why the current score reads "modern" (measured)

Source: `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_01_jacobs_ladder\score_final.mp3`, made 2026-08-22 by `generate_score_final.py` for the OLD words, then only trimmed to the new length by `assemble_jl_v3.py`. The audio in `jl_uplift_final.mp4`, `jl_uplift_fix1.mp4` and `jacobs_ladder_v3_sfx.mp4` is the same stream (same MD5 857cb24d...).

| What | Evidence |
|---|---|
| Genre | The prompt says it: "1990s dream trance, 135 bpm ... four-on-the-floor kick ... hypnotic bassline ... synth pads ... club comedown". |
| Beat | Measured tempo peak 135-137 bpm (onset autocorrelation 0.745). A film score has no fixed dance pulse. |
| Low end | 78 % of the energy is below 120 Hz (kick + bass). Only 0.1 % above 2 kHz: no bow, no air, no room. |
| No arc | Loudness per 5 s is flat: -14.6 to -15.0 dB from 5 s to 55 s. Same beat under "He ran", "I will not leave thee" and John 1:51. No hit points at all. |
| Mix | Gain -8 dB, duck ratio 1.3 = almost no duck. Music stays at about -23 dB all film. Voice is only 3.3 dB over it (median, per 0.25 s); at 10 % of spoken moments the music is louder than the voice. House standard (Nazareth) is 14-18 dB. |
| End | A 4 s fade starts at 52.5 s, UNDER the last line. The hold dies away (-28, -34, -45 dB). No lift. |

Honest limits: no separate music stem exists. I rebuilt the music stem from the script's own filter chain and measured that. Instruments come from the prompt + spectrum, not from ears. This is the same trance identity the owner rejected on ep8 ("I hate the score").

## 2. The design

**Sound:** warm string orchestra (deep cellos + basses), concert harp, one soft French horn. No drums, no percussion, no synth, no piano, no choir, no solo cello lead (cello solo was rejected on Naaman). The film's SFX bed already has a soft choir pad at 43.0-52.5 s, so a score choir would double it.

**Key + tune:** D minor (flight) turns to F major (dream). Ladder tune = 4 steps up, F G A C. It also comes back down, C A G F ("ascending and descending"). The UP form never lands home. The DOWN form lands home on F on the word "first".

**Film = 56.5 s. Last word ends 53.20 s. Word times from `audio\alignment.json`.**

| Film time | Words | Music |
|---|---|---|
| 0.0-6.2 | Jacob tricked... Esau wanted him dead. "He ran." @5.94 | Low cellos + basses, quiet restless short bowed pulse, D minor. Starts at once. |
| 6.2-9.4 | "What would God say to a man like that?" 7.22-9.34 | Pulse stops. One bare low note hangs. A question. |
| 9.8-12.5 | "He lay down... a stone for his pillow." | Very still. One soft high violin note over a low note. Night. |
| 13.5 | "In a dream" | Harp enters. Harmony warms to F major. |
| **15.0** | **"ladder" @14.96** | **HIT 1: harp, 4 steps UP (F G A C).** Strings open. |
| **18.2 / 18.9** | **"ascending" @18.15 / "descending" @18.89** | **HIT 2: steps UP, then the same notes DOWN.** |
| 21.0 | "The LORD stood above it" @20.95 | HIT 3: low strings + soft horn, one deep broad warm chord. |
| **23.4-24.4** | **"I will not leave thee."** | **HIT 4: stillness.** One held chord, no tune. Mix pulls it 8 dB lower (not zero). |
| 24.6-29.3 | "Before Jacob did anything... God promised to stay." stay @28.93 | Strings bloom, tender. Steps DOWN once at ~28, settling. |
| 30.0-35.5 | "Jacob woke afraid" / "Surely the LORD is in this place" | Hushed high shimmer. Awe, never scary. |
| 35.5-37.5 | (2.1 s silence, dawn) | Warm F major chord, first light. **Two-part split at 36.5 s**, 0.3 s crossfade. Music lifts +4 dB here. |
| 38.7 | "Jesus" @38.69 | Harp, 4 steps UP again, gentle. |
| **45.0** | **"heaven open" 44.98-45.38** | **HIT 5: full strings + horn open wide. The biggest moment.** |
| 47.2 / 47.9 | "ascending" / "descending" | Steps UP then DOWN inside the swell. |
| 50.5-51.9 | "Jacob never climbed that ladder." | Swell eases. Steps UP start and stop unfinished. |
| **52.2-53.2** | **"God came to him first." first @52.92** | **HIT 6: steps come DOWN and land home on F.** Full warm chord. |
| 53.2-54.0 | hold | Chord rings, +6 dB lift. |
| 54.0-56.5 | hold | **2.5 s fade, silent on the last frame.** Audio = video = 56.5 s. |

Honest odds: music_v1 follows "around X seconds in" cues to about +/-1.5 s and does not always obey note names. I expect 4 of 6 hits to land close on a first take (say 55 % +/-20 % for all the big three: stillness, sky-opens, home). The split can slide +/-0.8 s inside the dawn silence for $0 to line up part 2.

## 3. Generation + mix (exact)

**Tool the repo uses:** ElevenLabs Music, `POST https://api.elevenlabs.io/v1/music`, `model_id: "music_v1"`, free-text `prompt`, `music_length_ms`, `force_instrumental: true`. Via `gen_music()` in `F:\slk\PycharmProjects\JesusInTheBible\poc_folk_print_style\generate_score_v2.py` (has the dead-intro check). **Never** `composition_plan` / `music_v2`.

**Ready script (NOT run, needs `--go`):** `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_jl_score\generate_score_jl.py`. Both full prompts are in it (PART1 1,739 chars, PART2 1,219 chars).

| | Part 1 | Part 2 |
|---|---|---|
| Film span | 0.0 - 36.5 s | 36.5 - 56.5 s |
| Used | 36.65 s | 20.15 s |
| Ask for | 44 s (+7.3 spare) | 28 s (+7.8 spare) |
| Tempo / key | 66 bpm, D minor to F major | 60 bpm, F major |
| Cue clock | film time | film time minus 36.35 s |

Spare >= 7 s because music_v1 fades its own last ~5 s (Nazareth lesson). Join: `acrossfade=d=0.3` centred 36.5 s; end `afade=t=out:st=17.65:d=2.5` on part 2 (= film 54.0-56.5). Per-part gates before joining: dead-intro check, per-second RMS, no second under -45 dB inside the used span. Retake only the bad part. Output goes to `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\jl\score_cine\` (F: has ~119 MB free).

**Mix script ($0):** `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_jl_score\mix_score_jl.py`

1. Voice = `panel_jl\audio\narration.mp3`, padded to 56.5 s. No gain, no EQ, no limiter.
2. Music = score.mp3, base gain set BY MEASUREMENT (score duck is track-specific): the script measures voice-over-music per 0.25 s and sets the base so the median is 16 dB. Then sidechain duck keyed by the voice: threshold 0.12, ratio 2.5, attack 20, release 250 (Nazareth values; right for a non-rhythmic score).
3. Shape on top (dB, 0.3 s ramps): 23.2-24.6 **-8**; 31.8-35.6 **-4**; 35.5-37.5 **+4**; 44.0-49.7 **-3**; 50.4-53.2 **+2**; 53.2-end **+6**.
4. Picture = stream copy of `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\jl\uplift\jl_uplift_fix1.mp4`.
5. SFX = the same 5 layers and levels from `build_sfx_jl.py`, through `sfxlib.build` (same final limiter as the shipped film).
6. Out: `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\jl\uplift\jl_uplift_fix1_cine.mp4`. Then run `check_landing_hold.py`.

**Measured gates in the script (per 0.25 s RMS):** M1 voice 14-18 dB over music, p10 >= 10. M2 no dead air 0.5-54.0 s. M3 music under "I will not leave thee" >= 5 dB below the bar before, not zero. M4 hold lifts >= 4 dB. M5 last 2.5 s falls each step, last window < -45 dB. M6 voice unchanged by the chain (<= 0.3 dB). M7 peak <= -1 dBFS.

**"Not modern" proxy (re-run on the new score.mp3):** energy below 120 Hz < 35 % (now 78 %); no tempo peak > 0.5 at 120-140 bpm (now 0.745); per-5 s loudness range >= 6 dB (now 0.4 dB). These three numbers are my own guide lines, not a house gate. The owner's ear decides.

Dry test done at $0: the mix chain ran on the OLD score as a stand-in (audio only). M1, M3-M7 passed; M2 failed correctly (the old track is silent 0.5-1.75 s). Found and fixed: an `anullsink` on the voice leg cut the music tail; a limiter in this step moved voice windows up to 1 dB, so it is removed. NOT tested: the last step (picture copy + SFX build) and of course the real music.

## 4. Quote

ElevenLabs has no per-call cost API. Ledger rows (`data\spend_ledger.jsonl`) are estimates at **~$0.0135 per generated second**: 61 s = $0.88 (Nazareth), 65.5 s = $0.88 (Bethlehem), 69 s = $0.93 and 32 s = $0.43 (Immanuel), 86 s = $1.16 (Bartimaeus).

| | Seconds | Cost |
|---|---|---|
| First take (44 + 28) | 72 s | **~$1.00** (0.97, +/-10 %) |
| Retake part 1 only | 44 s | +$0.60 |
| Retake part 2 only | 28 s | +$0.40 |
| Full retake | 72 s | +$1.00 |
| **Cap** | | **$2.00** |

Retake odds from the last 4 scores: Bethlehem clean first try; Immanuel 1 part redone; Nazareth both parts redone; Bartimaeus clean. So about 50 % (+/-25 %) that one retake is needed. Likely total $1.00-$1.60.

**Bills:** the ElevenLabs account (`ELEVENLABS_API_KEY` in `PythonProject1\.env`). Not OpenArt. Not Higgsfield. Mix + SFX + checks = $0.

## 5. Before any spend

- House rule: score panels are blind and include the AI panel (claude / codex / grok). This file is the Fable seat only. The other seats should write their own score plan blind ($0) and be merged before `--go`.
- A yes to the design is not a spend order. The $1.00 needs its own yes.
- Log the spend to `data\spend_ledger.jsonl` after generation.
