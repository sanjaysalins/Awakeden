# Born in Bethlehem: cinematic score plan

## 1. Score idea

The score is a promise spoken in the dark and kept at dawn. A full orchestra holds back for most of the film. It opens up fully only once, at "He rose", and the tune finds its last note only after "He came to us."

- **Instruments:** full strings (low cellos and basses, wide violins), French horns, low trombones and tuba used gently, and timpani with deep orchestral bass drum. There is a soft celesta or harp shimmer for heaven. No choir, no synths, no rock kit.
- **The promise tune:** horns play four notes rising, then hang on a high note that does not resolve. It sounds like a question. At the end the strings play it again and add the missing step back down to the home note. The answer is "kept".

## 2. Why it fits

- **The comic look:** bold ink and slams want clear, graphic music. That means big blocks of sound with clean edges, not a wash. Strings give the slow pans their line. Drums mark the page turns, and the sound design's booms mark the panel slams. The two never collide.
- **The story:** the tune is left unfinished for about 700 years of story and 40 seconds of film. Viewers feel the gap without being told. When it finally ends on the home note, that is the promise kept.
- **Grace, not fear:** Herod gets weight from low brass, not horror. The biggest moment is reverent and warm, not a trailer hit.

## 3. Cue sheet

| Time (s) | What the music does | Why |
|---|---|---|
| 0–3.9 | Low sustained string chord. One soft timpani roll swells into "Did they go?" | Opens the question. The slams at 0.94 and 3.58 are booms in the sound design. |
| 3.9–9 | Strings drift down, with a slow pulse like a clock turning back | The time scroll rolls back 700 years |
| 9–14 | A solo horn plays the tune, unfinished, and hangs at 13.5 | Micah names Bethlehem: the promise is spoken |
| 15.8–17.4 | Almost nothing: a single held low note | The prophet's line |
| 17.8–27.8 | A walking pulse in low strings (pizzicato, then bowed). The tune returns on violins at ~23 and hangs again | The map journey; "God's promise came true" (still unfinished) |
| 27.8–33.4 | Low trombones and tuba, dark but not menacing. One timpani hit at ~28 | Herod |
| 33.8–36.3 | Thins to one held note | The scribe's line |
| 36.5–38.0 | A thin, high, uneasy violin line, cut cleanly at 38.0 | "Bethlehem was close by." |
| 38.0–39.0 | **True silence** | The hollow footprints, nobody went |
| 39.1–42 | Low strings come back quietly, building | "The Bible never says…" |
| 42.1–47 | Driving ostinato with deep drums and horns lifting | "The wise men went"; the gold footprints |
| 47–52.5 | Still: high strings, harp, no drums | Heaven, the cross, the tomb |
| 52.7–53.8 | **The one huge swell**: the full orchestra with horns on top, warm major key | "He rose from the dead" |
| 54.6–56.4 | Falls away to a soft high string pad | "He came to us." |
| 56.4–59.5 | Strings play the full tune and resolve to the home note, then a soft fade | The promise is completed, under the hero hold |

## 4. Split

**Split at 38.0 s.**

- Part 1 runs 0–38.0 s and ends in a clean cut-off.
- One second of digital silence is inserted, so the pause is true zero.
- Part 2 runs 39.0–59.5 s (20.5 s).

The join sits inside planned silence, so no seam can be heard. Each part is short, which lowers the risk of dead air.

## 5. Music prompts

**Part 1 (38 s):**
> Cinematic orchestral underscore, 38 seconds, reverent and serious, full string section, French horns, low trombones and tuba, timpani, no choir, no vocals, no synths, no rock drums, no Middle Eastern scales, no trailer hits. Starts with a low sustained string chord and a soft timpani roll swelling around 3 seconds in. Around 4 seconds in, strings drift downward with a slow clock-like pulse. Around 9 seconds in, a solo French horn plays a simple hopeful four-note rising melody that hangs unresolved on its high note around 13 seconds in. Around 15 seconds in, almost silence, one held low note. Around 18 seconds in, a gentle walking pulse in low strings begins, and around 23 seconds in the violins repeat the same rising melody, again left unresolved. Around 28 seconds in, one deep timpani hit and dark, dignified low brass. Around 33 seconds in, the music thins to a single quiet held note. Around 36 seconds in, a thin, high, uneasy violin line, then a clean stop at 38 seconds with no reverb tail.

**Part 2 (20.5 s):**
> Cinematic orchestral underscore, 20 seconds, full string section, French horns, harp, deep orchestral drums, no choir, no vocals, no synths, no rock drums, no trailer hits. Begins very quietly with low strings slowly building. Around 3 seconds in, a confident driving string ostinato with deep low drums and rising horns, hopeful and moving forward. Around 8 seconds in, the drums stop completely: still, sacred, high soft strings and gentle harp, peaceful and warm. Around 13.5 seconds in, one huge reverent swell of the full orchestra, horns soaring, warm major key, joyful but holy. Around 15.5 seconds in, it falls away to a soft high string pad, very quiet. Around 17.5 seconds in, the strings tenderly play a simple four-note rising melody and finally resolve it gently down to the home note, then a soft fade to silence by 20.5 seconds.

## 6. Mix notes

- **Under speech:** music sits about 14–18 dB below the voice, with sidechain ducking.
- **Under the two KJV lines** (16.0–17.4 s and 33.8–36.3 s): duck about 24 dB, nearly gone.
- **True silence** at 38.0–39.0 s: hard mute, plus the same mute on the sound-design track.
- **Lifts:** to about −8 dB under the voice at 42.1–45 s, and to about −4 dB at 52.7–53.8 s (the swell sits between words where it can).
- **"He came to us." (55.2–56.4 s):** about −24 dB.
- **The 3 s hold:** no voice, so the music rises to full level for the resolved tune. Fade the last 0.8 s.
- **Slams:** keep musical drum hits off the slam times by at least 0.15 s so they don't fight the booms.

## 7. Risks

1. **The tune never resolves, or resolves too early.** Check by ear at 13 s, 23 s and the final hold. If it's wrong, regenerate part 2 only, or lift the resolution from a second take.
2. **The duck crushes the score to silence** (the groove-duck lesson from earlier episodes). Measure the RMS of the music stem under speech in 1-second windows across the full timeline. It should stay audible, around −30 to −36 LUFS, never at the noise floor.
3. **The cues drift off the words.** The swell might land at 51 s, or drums might creep into heaven. Use a spectral or onset sweep to check: low-end energy above 60 Hz should be near zero across 47–52 s, and the swell should peak within ±0.4 s of 53.0 s. If a cue misses, nudge part 2's start offset before you regenerate.
