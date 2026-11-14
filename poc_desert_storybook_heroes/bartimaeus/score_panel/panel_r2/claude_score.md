# Blind Bartimaeus: score plan (composer seat)

## 1. SCORE IDEA
One four-bar tune follows the man's journey. It starts as a cry that never finishes, goes almost silent when Jesus stops, and is sung whole once he can see and follows Jesus.

- **Instruments:** felt piano (the main voice), warm string section, a solo cello that sings the tune from the healing onward, and a little oud and ney for the Jericho road. No drums, no drones, no trailer hits.
- **Key and tempo:** D minor, about 66 bpm. It turns to D major at the tomb.
- **The tune (motif):**
  - First half rises: D – F – G – A.
  - Second half falls back: A – G – F – E.
  - It stops on **E**, one step short of home. That is the question: "would He stop?"
  - Sung whole, it adds the last note, **…F – E – D**, and comes home.

## 2. WHY IT FITS
- **The look:** felt piano and gouache are both soft and hand-made, like a picture book. Warm strings match the ochre dusk light. A few oud notes put us on a dusty road, not in a church hall.
- **The story:** the tune that won't finish is the blind man's unanswered cry. Jesus stopping is heard as near-silence. Sight is the tune finally landing on its home note.
- **The voices:** a slow, plain tune with long notes leaves room for three voices and old KJV wording.

## 3. SCORE CUE SHEET

| Time (s) | What the music does | Why |
|---|---|---|
| 0–3.0 | One low piano D, a soft ney breath | Leaves the raw cry bare |
| 3.0–12.7 | Piano plays the tune once, unfinished on E. Light oud plucks | Who he is; the question is planted |
| 12.7–20.8 | Low strings come in under the piano. The tune climbs a step. Slow pulse | The long road to Jerusalem; the stakes |
| 20.8–25.6 | Strings swell a little. Piano repeats the tune, unfinished on E, a little higher | He shouts louder |
| **25.6–27.5** | **Almost silence: one held high violin E, ppp** | The pause, then "And Jesus stood still" |
| 27.5–33.7 | Single soft piano notes, very sparse | He stops for one man |
| 33.7–38.4 | Short rising piano run, oud flourish | Cloak flung off, he comes |
| 38.4–48.9 | Thin bed: piano chords only, no tune | Clear room for the questions and answers |
| **48.9–56** | **Lift: cello sings the whole tune, ending on D. Strings bloom** | Eyes open; the hero shot |
| 56–61.3 | Tune carries on, walking pulse in the piano | He follows Jesus up the road |
| 61.3–66 | Drop to cello alone, low and slow | The cross at dusk |
| 66–69.4 | Turn to D major, strings rise | "He rose to life," the open tomb |
| 69.4–76.2 | Piano and cello play the whole tune once more, gently | "Jesus stood still for one man" |
| **76.2–79.17** | **Last D chord on piano and strings, one oud note, let ring to silence** | The 3 s hold on the sunset bookend |

## 4. SPLIT
**Split at 26.1 s.** The join hides inside the planned silence. Part 1 fades out on the unfinished E. Part 2 starts from near-silence on that same E. A 1.5 s crossfade is enough.

Part 1 gets ~28 s and Part 2 ~55 s, about 83 s in total, within the ~90 s budget.

## 5. MUSIC PROMPTS

**PART 1 (generate 28 s):**
> Gentle cinematic score for a warm storybook film, D minor, 66 bpm, no drums, no vocals. Lead instrument is a soft felt piano playing a simple, singable, folk-like melody: four rising notes D F G A, then falling A G F E, ending unresolved on E. Light Middle-Eastern colour from a few soft oud plucks and a breathy ney. Opens with one low piano note and a soft ney breath. Around 3 seconds in, the piano plays the melody once, ending unresolved. Around 13 seconds in, warm low strings enter under the piano with a slow pulse, and the melody climbs a step higher. Around 21 seconds in, the strings swell gently and the piano repeats the melody a little higher, again ending unresolved on E. Around 25 seconds in, everything falls away except one held quiet high violin note. Intimate, hopeful, quiet, leaving room for a spoken voice. Not ambient, not a drone, not epic.

**PART 2 (generate 55 s):**
> Gentle cinematic score for a warm storybook film, D minor turning to D major, 66 bpm, no drums, no vocals, continuous sound throughout with no gaps. Same simple melody: D F G A, A G F E, resolving finally to D. Opens on one held, very quiet high violin E. Around 2 seconds in, sparse single felt-piano notes. Around 8 seconds in, a short rising piano phrase and a small oud flourish. Around 12 seconds in, soft held piano chords only, very quiet. Around 23 seconds in, a warm solo cello sings the full melody, resolving to D, and the strings bloom: tender and joyful. Around 29 seconds in, a gentle walking piano pulse continues the melody. Around 35 seconds in, the music thins to a low, slow solo cello, sorrowful. Around 40 seconds in, it turns to D major and the strings rise with quiet hope. Around 43 seconds in, piano and cello play the full melody once more, gently. Around 50 seconds in, a final soft D major chord on piano and strings with one oud note, ringing out slowly to silence. Felt piano, warm strings, solo cello, light oud and ney. Not ambient, not epic.

## 6. MIX NOTES
- **Level:** music sits about 18–20 dB under the voice, with an extra 6–8 dB duck while anyone speaks. Use a looser duck, so the tune survives between phrases.
- **Lifts:**
  - 48.9 s, eyes open: duck eases to about 4 dB.
  - 54.8–59.8 s: the walking tune is audible.
  - 66 s: major turn.
  - 69.4 s: the last full tune.
- **Near-silence:**
  - 25.6–27.5 s: only the violin E, under −40 dB.
  - 38.4–48.9 s: chords only, so the three voices stay clear.
- **The 3 s hold (76.17–79.17):** no duck. Bring the music up to about −20 LUFS-short so the chord is clearly heard. Natural decay, a 0.8 s fade at the very end. Audio and video must be the same length (pad the audio to 79.17 s with `apad=whole_dur`).

## 7. RISKS
1. **Dead air inside Part 2** (a long generation goes quiet).
   - *Check by measurement:* RMS in 0.5 s windows across the whole timeline. Flag anything under −45 dB outside 25.6–27.5 s and after 79 s.
   - *Fix:* re-roll, or split Part 2 again at 48.9 s.
2. **No real tune, just wash** (the model drifts to ambient).
   - *Check by ear:* after one listen, can you hum it? Is the tune audible at 48.9 s and 69.4 s?
   - *Check by measurement:* a pitch tracker on the music stem should show the four-note rise.
   - *Fix:* re-roll with "clear melody, solo instrument in front."
3. **The seam doesn't match or the duck buries the tune** (key or tempo drift at 26.1 s, music crushed under speech).
   - *Check:* listen to 24–29 s on loop for key and tempo match.
   - *Check by measurement:* the music stem under speech should stay above −38 dB short-term.
   - *Check by ear:* listen for oud creeping over the narrator.
