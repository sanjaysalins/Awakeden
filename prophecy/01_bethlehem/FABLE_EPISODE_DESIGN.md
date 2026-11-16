# Born in Bethlehem - EPISODE DESIGN (score, sound, lifts, series recipe)

Fable design answer, 2026-11-15. Design only. $0 spent. Nothing built.
Based on: `film\BETHLEHEM_FILM_v4b.mp4` (60 frames, 1 per second, plus 8 close frames), `words\FINAL_WORDS_v2.md` (locked, not touched), word times in `_remotion\public\bethlehem\film_v3_data.json`.

**Limits of this review.** I looked at still frames. I did not watch playback and I did not hear the voice. Word END times below are my estimate from word START times (about +0.4 s). A builder must read the real ends from `audio_v2\narration_v2.words.json` before cutting music to them.

**House rule note.** This is ONE seat (the Fable seat). The playbook asks for a blind score panel (Fable + Claude + Codex + Grok) before money is spent. Use this file as the Fable seat, not as the final score brief.

---

## 1. SCORE

### The one idea: "the unfinished tune"

A promise is a sentence that is not finished yet. So the music is a tune that is not finished yet.

- **The promise tune** = 4 slow notes going up, on felt piano. It stops one note short of home. It hangs.
- Micah plays it. Then 700 years pass. It still hangs.
- At the birth it comes back, warmer, and still hangs. (A baby is not the end of the story.)
- On the last line it finally gets its **5th note: home**. Promise kept.

A newcomer does not need to know music to feel this. An unfinished tune makes you wait. A finished one lets you breathe out.

### The second idea: "walking pulse"

The film is about who WENT. So the beat is footsteps.

- A soft plucked cello pulse at **72 beats a minute** (a slow walk) plays when people are walking.
- It **stops** when the experts do not go. The viewer hears the not-going.
- It comes back, brighter, on "The wise men went".

### Palette (3 colours only)

| Instrument | Job |
|---|---|
| Felt piano (soft, close, a little hammer noise) | The promise tune. Always the tune. |
| Solo cello | Warm long notes under the tune. Plucked = the walking pulse. |
| One soft frame drum (hand, not stick) | Only under the two journeys. Very quiet. |

No choir. No big drums. No risers. No Middle-East cliché scales. Key: D minor, turning to D major at 43.5 s (same family as the Bartimaeus score the owner liked). Tempo 72.

### Music map (seconds are film time)

| Time | Line | Music |
|---|---|---|
| 0.0-3.9 | "The Bible experts knew... Did they go?" | Almost nothing. One low held cello note. The question lands dry. |
| 3.9-5.9 | time scroll | No tune. Sound design only (see section 2). Cello note slides DOWN a step: going back. |
| 5.9-11.3 | "a prophet called Micah..." | Cello long notes, D minor. Calm, old. |
| **11.3** | **"Bethlehem."** | **Promise tune, first time. 4 notes. Hangs.** |
| 12.6-15.6 | "Out of it, he said, a ruler would come," | Cello holds the hanging note. |
| 15.8-17.6 | KJV: "that is to be ruler in Israel." | Music dips very low (about 22 dB under the voice). Scripture is heard clean. |
| 17.8-22.7 | Map A: "lived far away... tax order sent them" | Walking pulse starts. Frame drum, very soft. |
| **22.7-25.1** | **"There, Jesus was born."** | **Pulse stops. Promise tune again, warmer (cello joins). Still hangs.** No swell. Sacred. |
| 25.2-29.2 | "Wise men from the east..." | Pulse back, a little lighter and quicker in feel (same tempo). |
| 29.3-34.3 | "King Herod asked..." / "In Bethlehem of Judaea." | Pulse keeps going. One low dark cello note under Herod. Dip under the scribe's KJV line (32.2-34.0). |
| 34.8-36.3 | "Bethlehem was close by." | Pulse thins to single plucks, slowing. |
| **~36.3-37.4** | **(the 1 s pause)** | **Music fully OUT. True quiet.** The first hollow print blinks in silence. |
| 37.4-39.5 | "The Bible never says the experts went." | One low held cello note only. No pulse. No tune. |
| ~39.5-40.5 | (silence) | Out again. |
| **40.5** | **"The wise men went,"** | **Pulse returns, full and bright.** |
| 41.9-43.4 | "and found the child." | Pulse stops gently. Warm cello chord. |
| **43.5** | **"But Jesus had come much farther."** | **THE TURN. Part 2 starts. D major. Wide, open cello line.** |
| 46.0-48.0 | "He came down from heaven." | High piano notes step DOWN (matches the gold ribbon coming down). |
| 48.1-50.4 | "He died for our sins." | Drop to solo cello, one long note. Nothing else. |
| 50.5-52.4 | "He rose again the third day." | The one real swell of the film. Peak at **51.7** (the dawn cut). |
| 52.5-54.6 | "Before anyone went to Him," | Pull back to piano alone. |
| **~54.6-56.2** | **(pause) "He came to us."** | **Music drops out. The line is said almost dry.** This is the Bartimaeus device the owner liked. |
| **~56.3-59.3** | (3 s hold) | **Promise tune, complete: 4 notes + the home note at about 57.5.** Ring out. End together with the picture. |

### Bespoke or library?

**My pick: bespoke, 2 parts, split at 43.5 s. About $1.20 per try. Needs its own yes.**

Why: the whole idea is a tune that comes back three times and stops twice. A library bed cannot do that. The 4 approved beds in `music_library` are pads and moods with no tune.

**$0 fallback** (if the owner says no to the spend): `lonely_searching_a` under 0-43 s, cross-fade to `sacred_grace_rise_a` with its swell (at 130.4 s in the file) lined up to 51.7 s, through `music_library\placer.py`. Then cut the two silences and the "He came to us" drop by hand in the mix. It will be pleasant. It will not carry the promise idea.

### Notes for the prompt writer

- Part 1 (0-43.3 s, ask for ~45 s): "Solo felt piano and solo cello, D minor, 72 bpm, sparse and intimate. A simple four-note rising phrase on piano that never resolves, repeated a few times with long gaps. Plucked cello walking pulse with a very soft hand frame drum. Ends unresolved on a held note. No choir, no strings section, no cinematic drums."
- Part 2 (43.5-59.3 s, ask for ~17 s): "Same felt piano and solo cello, D major, 72 bpm. Opens wide and warm, one gentle swell, then piano alone plays a five-note rising phrase that resolves home and rings out. No choir, no drums."
- **Honest risk:** the generator will not place notes on exact seconds, and it may not play the same 4 notes in Part 2. So: (a) do the two silences, the KJV dips and the "He came to us" drop **in the mix**, not in the prompt; (b) slide Part 1 so a statement of the tune lands on 11.3; (c) if the tunes do not match, cut the 4-note phrase out of Part 1 and reuse it at 22.7 and 56.3 with the home note from Part 2. Expect 2 tries.
- Do not use ElevenLabs composition_plan (proven dead end, per memory).
- Mix: music about 14 dB under the voice, sidechain duck, measured not guessed. Rhythmic pulse needs a looser duck or it vanishes (memory: groove score).

---

## 2. SOUND DESIGN

8 moments. Ambience level. Nothing louder than the voice. All dip to zero in the two silences (36.3-37.4, 39.5-40.5).

| # | Time | What we see | Sound | Source |
|---|---|---|---|---|
| 1 | 0.0-3.9 | Experts round the scroll, torches | Low torch crackle, stone room | `fire_crackling` ($0) |
| 2 | 3.9-5.9 | Time scroll rolls in and out | Parchment unroll in, roll away out. Wind pulled backwards under it | **paper: gap (see below)** + `wind_desert_bleak` reversed ($0) |
| 3 | 11.3 and 12.6 | Gold ring, then crown, drawn on Bethlehem | Short nib scratch, twice | **gap** |
| 4 | 17.5-22.1 | Map A unfolds; walkers go south | Paper fold open (17.5). Two people walking on dirt, slow (19.0-22.0). Coins clink once on "tax order" (20.7) | fold: **gap**. `footsteps_dirt_approach`, `coins_clinking` ($0) |
| 5 | 22.7-25.1 | Manger | Only night air and one far sheep. Very low. No effects on the birth word | `flock_sheep_field` at about -30 dB ($0) |
| 6 | 25.2-27.8 | Camels, star crossing | Soft padded steps on sand, slow | `footsteps_dirt_approach` pitched down ~20 %, low-passed ($0, a stand-in. Do NOT use `horse_hooves_walk`: hooves clip-clop, camels do not) |
| 7 | 34.3-37.4 | Map B, hollow prints pop one by one | One soft dry tap per print (7 taps). Then silence. **No footsteps.** The empty road must sound empty | `waterpot_drop_run` first 0.35 s only ($0, as in scriptorium-foley) |
| 8 | 40.5-42.0 | Map C: prints turn gold down to Bethlehem | Real footsteps now, one per print as it turns gold. Same road, now walked | `footsteps_dirt_approach` cut into single steps ($0) |
| 9 | 51.7-59.3 | Dawn, risen Jesus | Morning birds fade in slowly, very soft | `dawn_morning_warm` ($0) |

**The pair 7 and 8 is the important one.** Same road. First taps with no steps. Then steps. The ear gets the point without a word.

**Left out on purpose:** thunder on the crosses (the sacred window stays clean), tomb stone roll (the tomb is already open), choir, donkey (not in the text), any whoosh.

**The gap.** `sound_library` has no paper or pen sounds at all. The scroll, the map folds and the nib are the signature of this series, and every episode will need them.
- $0 option: stand-ins from the library (`bread_tearing` onset for paper, high-passed footsteps for nib). The scriptorium-foley skill already says these are weak.
- **My pick: buy a small paper bank once. About $0.40** (ElevenLabs SFX, 2 takes each: parchment unroll, parchment roll-up, paper map unfold, nib scratch short, soft camel steps on sand). Save it into `sound_library` so the whole series reuses it for $0. Needs its own yes.

---

## 3. WHAT ELSE WOULD LIFT THIS CUT (ranked) + honest weak spots

### 1. Clear Herod's face and the hook question ($0, Remotion)
- At 29.3-34.7 the read-along pill and then the scribe's speech balloon sit **right across Herod's eyes** in the bottom panel. His glare is the best acting in that page and it is covered. Move both down to about y 1500 (his beard / the wall) or into the gutter above that panel.
- "DID THEY GO?" is the hook. "GO?" is on screen for well under a second before the time scroll wipes it. Let the lettering stay on top of the scroll's entry for about 0.4 s more. The voice does not move.

### 2. Make "promised, then kept" land in the picture ($0, Remotion)
- The series is about a promise kept. But the film's own spine is "went / came". The only place the promise idea is shown is the end mark, and it is **tiny** (small grey text, low right, last 2 seconds). On a phone it will not be read.
- Fix: make the end mark a real, readable stamp (about 3x bigger, centred under the pill, on from ~56.5 s), landing with the home note of the tune. Nothing on His face or body.
- With the tune from section 1 this may be enough. Do not add a "kept" stamp on the manger. That window stays clean.

### 3. The last picture ($0 to soften, or about $0.35 to redo)
- The risen Jesus has a **fire-orange and electric-blue outline**. It is the loudest, most "AI" picture in the film and it is held the longest (7.6 s). It does not match the ink-and-parchment look that the owner liked.
- $0: a gentle warm grade over that shot to calm the blue, plus a slow push. About $0.35: one new still + one clip in the dawn look without the flame outline. Owner's call; it is a taste point, not an error.

### Other honest weak spots (no fix asked)
- Map A at ~20 s: the pill sits on top of the "Bethlehem" label for a moment ("Bet" shows). Small. Nudge the pill down or the label up.
- The crosses and the tomb share one screen as small panels (43.5-51.7). "He died for our sins" gets a small picture. It is calm and reverent, but it is the weakest picture of the gospel lines.
- The map is not to scale. Still true. No numbers are shown, so it is honest, but say so if asked.
- Three places put text over art: "Micah" tag, "A SCRIBE", "MATTHEW 2:5". The last two are very small. A newcomer will not read them. Fine to keep; do not rely on them.
- Camel walk, crown wobble and map folds were never checked in playback by me. The owner has now watched it and liked it, so this risk is lower, not zero.

---

## 4. RECIPE for the next prophecy episodes

Grammar: **promise -> time gap -> kept -> farther (the gospel) -> one-line landing.**

**Repeat every episode (the series signature):**
1. **The unfinished tune.** Same 4 notes on felt piano when the prophet speaks. Left hanging. The 5th note comes only on the last line. Same tune in every episode, so viewers learn it.
2. **The time scroll.** Same parchment roller, same "ABOUT ___ YEARS EARLIER" card with the number counting, same paper sound. Only the number changes.
3. **The prophet's own words on a scroll**, in the old serif type, with the verse tag. Music dips under it. Every time.
4. **Hollow, then gold.** One hand-drawn thing is shown hollow (not yet / not done) and turns gold when it is kept. In this film it was footprints.
5. **Silence at the turn.** Music fully out for about 1 s just before the fulfilment or the sting. Then out again under the last line.
6. **Sacred windows stay clean.** Birth, cross, tomb, risen Jesus: soft pill only, no doodles, no effects, no sound hits.
7. **Same end mark, big enough to read:** "PROMISED, THEN KEPT", landing on the home note. Same 3 s hold.
8. **Same sound world:** felt piano + cello + paper and pen sounds. Hook said dry.

**Change every episode:**
9. **The one drawn device, picked from the prophecy itself.** Bethlehem was about a PLACE, so it got a map. A prophecy about a price gets coins counted (30 pieces). About a donkey and a road, a road. About a person, a family line. Ask: "what is this promise made of: a place, a number, a person, an object?" and draw that. Do not reuse the map unless the prophecy is about a place.
10. **The hook question and the landing line** come from that story's own twist (here: who went). Also the key colour of the pulse (walking here; could be a heartbeat, a hammer, a count). Never the same landing shape twice.

**Order of work (unchanged house rules):** words locked first, then voice, then pictures, then score design from real word times. Each paid step gets its own quote and its own yes.
