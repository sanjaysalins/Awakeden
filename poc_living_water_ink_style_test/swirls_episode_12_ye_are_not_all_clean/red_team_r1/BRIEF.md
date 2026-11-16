# RED TEAM BRIEF: a finished vertical short film (YouTube Shorts / Reels), 78 seconds

You are ONE independent, hostile reviewer. You have not seen any other review. Assume the film has real flaws and find them. Do not flatter.

**What it is:** a narrated short for a channel that finds Jesus across the whole Bible, for a worldwide audience. Series look: each picture is a hand-drawn ink-and-watercolour "animation development storyboard page" (a title strip, a frame number, three small labelled sketch panels, one large scene illustration, handwritten notes). Some pictures are full-frame scenes instead. Each picture is a short AI-animated clip. Soft piano music, quiet room sounds. One narrator voice. Story: John 13 (Jesus washes the disciples' feet, including Judas; Judas leaves).

**Your focus:** the STILLS (the pictures themselves) and the ANIMATION (how they move), and how both serve the spoken words. Also say anything else that is clearly wrong.

## The evidence
- Contact sheets, a frame every 2 seconds, time printed above each frame: `sheet_1.jpg` (0-18 s), `sheet_2.jpg` (20-38 s), `sheet_3.jpg` (40-58 s), `sheet_4.jpg` (60-77.5 s). Single frames at full size: `frames/t_XXX.X.jpg`.
- Picture changes (cuts) happen at: 3.8 s, 13.4 s, 19.6 s, 34.5 s, 46.6 s, 50.5 s, 63.5 s. So there are 8 pictures in 78 s.
- Measured motion (mean pixel change between frames, per second; 0 = a still picture; a gently moving clip on this channel is usually 1.0-3.0):
  0-4 s: 1.8-3.9 · 5-12 s: 0.7-0.8 · 14-18 s: 0.3-0.5 · 20-33 s: 0.13-0.18 · 35-45 s: 0.06-0.19 · 47-49 s: 1.0-1.4 · 51-62 s: 0.03-0.12 · 64-77 s: 0.19-0.27. (Spikes at cuts removed.)
- A freeze detector (strict) also flagged near-still stretches at 31.3 s, 33.3 s, 44.5-46.6 s and 60.5-63.2 s.

## Spoken words, with the real time each sentence is said
  0.0-3.8   Judas walked out into the night on feet Jesus had washed.
  5.3-10.8  John says the devil had already "put into the heart of Judas Iscariot, Simon's son, to betray him."
 11.9-12.5  Jesus knew.
 13.3-15.0  He knew as He poured the water.
 15.5-17.9  He knew as He dried their feet with the towel.
 19.1-22.8  Then He told them, "ye are clean, but not all."
 23.6-26.6  And He quoted the old word for betrayal, from Scripture:
 27.4-31.9  "He that eateth bread with me hath lifted up his heel against me."
 33.0-36.7  He handed Judas the sop, a piece of dipped bread.
 37.6-39.6  "That thou doest, do quickly."
 41.0-43.3  Some at the table thought he had gone to buy food.
 44.1-47.1  Judas "went immediately out: and it was night."
 48.8-52.0  Jesus did not wash those feet because Judas earned it.
 52.8-56.0  He washed them knowing Judas would betray Him anyway.
 56.9-60.3  That is what His love does when it already knows the worst.
 61.6-65.9  He knows your heart, every corner of it, like that.
 67.1-71.4  He has not put the towel down. Bring Him your worst.
 (voice ends 71.4 s; the film runs to 78.0 s)

## KJV (John 13, the only authority for accuracy)
2 And supper being ended, the devil having now put into the heart of Judas Iscariot, Simon's son, to betray him;
4-5 He riseth from supper, and laid aside his garments; and took a towel, and girded himself. After that he poureth water into a bason, and began to wash the disciples' feet, and to wipe them with the towel wherewith he was girded.
10 ... and ye are clean, but not all. 11 For he knew who should betray him; therefore said he, Ye are not all clean.
18 ... He that eateth bread with me hath lifted up his heel against me.
26 Jesus answered, He it is, to whom I shall give a sop, when I have dipped it. And when he had dipped the sop, he gave it to Judas Iscariot, the son of Simon.
27 ... Then said Jesus unto him, That thou doest, do quickly.
29 For some of them thought, because Judas had the bag, that Jesus had said unto him, Buy those things that we have need of against the feast; or, that he should give something to the poor.
30 He then having received the sop went immediately out: and it was night.

## OUTPUT (Markdown, max ~700 words, these headings, cite a time in seconds every time)
## 1. STILLS: what is weak (list; time + what you see + why it hurts)
## 2. ANIMATION: what is weak (list; time + what you see/measure + why it hurts)
## 3. PICTURE vs WORDS: where the picture says something different from, or late for, the voice
## 4. ACCURACY: anything in a picture or a label that the KJV text does not support
## 5. VERDICT: SHIP / FIX / REBUILD, and a score 0-10
## 6. THE FIVE HIGHEST-VALUE FIXES (ranked; say which are free (re-edit) and which need new pictures or clips)
