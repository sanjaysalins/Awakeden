# Score Plan: "Blind Bartimaeus" (Composer Seat)

## 1. SCORE IDEA
The crowd walks, the music walks with it, and when Jesus stands still the music stops too.

- **Instruments:**
  - A soft frame drum and a muted plucked oud play a slow walking beat. This is the crowd's feet.
  - A low bowed drone sits underneath, like the heat on the road.
  - A breathy ney flute carries the motif.
  - In part 2 only, a warm, quiet string pad enters for the sight and the bookend.
- **Motif, "the cry":** three notes that go up and then fall back (D, F, A, then down to E). It never comes to rest, like "have mercy." When he can see, the same three notes finally land home on D major (D, F#, A, D). We hear the cry answered.

## 2. WHY IT FITS
- **The look:** gouache picture-books feel hand-made. Plucked strings, a skin drum and a reed flute are hand-made sounds. There are no big synths and no trailer hits. The sound is dusty and warm, not "epic."
- **The story's one idea is a STOP.** The drum is the moving crowd, so cutting it at "And Jesus stood still" makes the listener feel the stop. It isn't just shown.
- **The motif carries the arc:** first a cry with no answer, then the same notes answered when he sees. When he follows Jesus up the road the beat comes back, but now it walks *with* Jesus.

## 3. SCORE CUE SHEET
| Time (s) | Music | Why |
|---|---|---|
| 0–3 | Ney plays the cry motif once, very soft, high above a thin drone | It echoes his shout and doesn't fight it |
| 3–13 | Drone plus a light oud pluck. The walking drum starts at about 5 s, quiet | We meet the beggar, and the crowd is moving |
| 13–21 | The drone drops lower and a minor shade comes in. The drum keeps walking | "Road to Jerusalem… killed there." Will He stop? |
| 21–25.6 | A slow build. The drum gets a little stronger and the ney plays a higher, unresolved cry | "Shouted even louder" |
| **25.6–26.6** | **Everything cuts. Near silence: only the tail of a reverb** | The planned pause, a held breath |
| **26.6–33.7** | **No drum. One low sustained note, almost nothing** | "And Jesus stood still." The crowd's feet are gone |
| 33.7–38.4 | A small lift: one warm oud figure, then the drone opens slightly | The cloak is flung off and he moves |
| 38.4–48.9 | Very sparse: only the drone, and short soft plucks in the gaps between lines | Dialogue. Leave room for Jesus's low voice |
| **48.9–56** | **The lift. The motif resolves in D major on ney with the warm string pad** | His eyes open and he sees |
| 56–61.3 | The walking drum returns, gentle and steady, a little slower | He follows Jesus up the road |
| 61.3–66 | The drum stops. A low drone with one falling cry figure, solemn | The cross at dusk |
| 66–68.4 | A rising swell with strings | "He rose to life," the open tomb |
| 68.4–69.4 | The swell holds. It does not cut | The pause should breathe, not go dead |
| 69.4–76.2 | Warm and settled, with the full motif in major played once, slowly | "Jesus stood still for one man" |
| **76.2–79.17** | **The 3 s hold: one sustained D-major chord, ney on the last note, fading in the final 1 s** | The sunset bookend comes to rest |

## 4. SPLIT
- **Split at 48.9 s**, the point where the story resolves: the last word of "thy faith hath made thee whole," right before he sees.
- Part 1 is the unanswered cry (D minor, a walking beat that stops). Part 2 is the answer (D major). A change of key at that point sounds planned, not like a seam.
- Make part 1 50 s long and part 2 32 s long. Crossfade over 0.4 s at 48.9 s and trim the end to 79.17 s.

## 5. MUSIC PROMPTS

**Part 1 (50 s):**
> Quiet, warm, hand-played Middle-Eastern folk underscore for a children's storybook film, D minor, 70 BPM. Instruments: breathy ney flute, soft muted oud, gentle frame drum, low bowed drone. No vocals, no synths, no cinematic hits. Starts with the ney alone playing a three-note rising-then-falling phrase over a thin drone. Around 5 seconds in, a soft walking frame-drum pulse begins with light oud plucks. Around 13 seconds in, the drone drops lower and darker. Around 21 seconds in, a slow, gentle build, with the ney repeating its phrase higher. Around 25 seconds in, ALL instruments stop completely: near silence. Around 26 seconds in, only one low sustained drone note, no drum at all, very still, for about 7 seconds. Around 34 seconds in, a small warm oud figure. Around 38 seconds in to the end, very sparse and very quiet: drone with occasional single oud plucks, leaving space for speech.

**Part 2 (32 s):**
> Quiet, warm, hand-played Middle-Eastern folk underscore for a children's storybook film, D major, 70 BPM. Breathy ney flute, soft oud, gentle frame drum, low drone, warm soft string pad. No vocals, no synths, no cinematic hits. Opens with a hopeful swell: the ney plays a three-note rising phrase that resolves home, with strings. Around 7 seconds in, a gentle, steady frame-drum walking pulse returns. Around 12 seconds in, the drum stops; low solemn drone with one falling ney phrase. Around 17 seconds in, a rising warm string swell that holds steady. Around 21 seconds in, settled and peaceful, with the ney playing the three-note phrase slowly. Around 27 seconds in, one sustained warm D-major chord, ney holding the final note, slowly fading to silence by 32 seconds.

## 6. MIX NOTES
- **Level:** keep the music about 18–20 dB under the voice during speech and about 12 dB under in the gaps. Use a gentle sidechain duck (slow attack, about 400 ms release) so the beat doesn't pump.
- **Lifts** (duck eased off, about 8 dB under): 48.9–56, 66–68.4, and 76.2–79.17.
- **Near-out:** gate the music to −40 dB or lower from 25.6 to 26.6. From 26.6 to 33.7 keep it about 24 dB under: barely felt.
- **Shouts:** Bartimaeus's cries at 0–3 and 23–25.6 get a deeper duck so his raw voice sits on top.
- **The 3 s hold:** music only, and audio length must equal video length (79.17 s). Fade out over the last 1.0 s, not earlier.

## 7. RISKS
1. **The drum doesn't stop at "stood still."** The model may keep the beat going. *Check:* measure the beat onsets and loudness from 25.6 to 33.7 s. There should be no drum hits at all. If they leak, regenerate part 1 or hand-mute that window and cross-fill with the drone.
2. **Dead air, or the music swamps the voice.** *Check:* take a loudness reading every 0.5 s across the whole film, not only the average or the peak. Flag any music gap over 1 s outside 25.6–26.6. Confirm the voice-to-music gap stays at 15 dB or more during dialogue (38–49 s, Jesus's low voice).
3. **The seam at 48.9 s sounds stitched** (a jump in tempo, tone or loudness). *Check:* listen to 46–52 s on headphones three times. Measure that the loudness step across the join is under 2 dB. If needed, nudge the split to land exactly on "whole," where the voice covers it.
