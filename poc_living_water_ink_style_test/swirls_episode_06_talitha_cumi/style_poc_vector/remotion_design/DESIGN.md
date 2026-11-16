# Talitha Cumi — Remotion "elevate" pass — DESIGN

Base layer: `../TALITHA_PREVIEW_G5_v2_score.mp4` (1080x1920, 30 fps, 53.8 s = 1614 frames). Audio untouched.
Mock of the key frames: `mock.html` (same folder).

## The idea in one line

The film is a fight between two voices. The news says **"Too late."** Jesus says **"Be not afraid, only believe."**
The graphics only ever do one job: show which voice wins.

## Signature device — "The Overruled Word"

- The words **Too late.** land as a dark pill, like a verdict. (12.4 s)
- When Jesus does not turn back, ONE orange brush stroke runs through the words — and **does not stop at the end of the word**. It keeps going, off the right edge of the screen. The stroke *is* "He kept going". (15.0 s)
- It comes back once, at the close, small, and is struck again; Jesus's words take its place. (44.3 s -> 45.4 s)
- Used 3 times total: land, strike, close. Nowhere else. Never on the miracle itself.

## Colours (sampled from the stills)

| Name | Hex | Where it came from | Used for |
|---|---|---|---|
| Cream | `#F6E9CA` | stone wall, p1 | all pill text, pill border |
| Deep teal | `#0E434D` | room wall, p4c | normal pill fill (at 66% alpha) |
| Navy | `#15253C` | Jesus's mantle, p1 | "Too late." pill fill (at 80% alpha) |
| Turquoise | `#2DAFB1` | sky, p1 | Jesus speaker tab |
| Orange | `#EE8D44` | sunset, p3 | the strike stroke only |
| Burnt orange | `#BE6829` | orange wall, p1 | other speaker tabs |
| Flame | `#F8D898` | lamp flame, p4c | gold chip text highlight |
| Gold (derived) | `#F2B63C` | between flame and sunset — not a direct sample | verse chip fill |
| Ink | `#101418` | outline black | chip text, text shadow |

## Shared parts (build once)

**Font:** Kalam (Google Fonts), weights 400 + 700. One font only.

**Pill** — `<Pill>`
- Fill `rgba(14,67,77,0.66)`, border `4px solid rgba(246,233,202,0.9)`, radius 44 px, padding 26 px 44 px.
- Text Kalam 700, cream `#F6E9CA`, `text-shadow: 0 3px 0 rgba(16,20,24,.55)`. Line height 1.15.
- Sizes: normal 84-96 px. Big (Talitha cumi, final line) 112 px. Max 2 lines, max 4 words a line. Line breaks are fixed by hand (as written with " / " below) — never let text auto-wrap.
- Max width 920 px, centred (x = 80..1000). No `backdrop-filter` (slow to render, and blurs the art).
- In: fade 0->1 and rise 18 px over 8 frames (`interpolate`, ease-out). No bounce — keep it calm.
- Out: fade over 8 frames. Jesus's pills fade over 12.

**Speaker tab** — small rounded label sitting on the pill's top-left edge (overlaps border by half its height).
- Kalam 700, 40 px, ink text. Radius 20 px, padding 4 px 22 px.
- "Jesus" tab: turquoise `#2DAFB1`. Other tabs: burnt orange `#BE6829` with cream text.

**Verse chip** — small label on the pill's bottom-right edge.
- Gold `#F2B63C`, ink text, Kalam 700, 38 px, radius 999 px, padding 2 px 24 px.
- Only on words that are KJV word-for-word.

**Two text bands** (nothing ever covers a face or the joined hands; both bands sit inside Shorts-safe space)
- TOP band: y 190-520. Used on p1, p3, p4c, p5 (sky / ceiling there).
- LOW band: y 1010-1520 (p7 only goes above 1240). Used on p2 and p7 (faces are high in those pictures).

**Strike stroke** — `<Strike>`: one SVG path, slightly wobbly, `stroke #EE8D44`, width 26, round caps, drawn with `stroke-dashoffset`. A second thin dry-brush line (width 6, 60% alpha, offset 14 px below) gives a brush feel. No glow, no particles.

## Beat sheet (frames at 30 fps)

Rule for timing: text comes in ON the spoken word (or just before it), and stays at least 1.5 s.

| # | Frames | Time | Picture | What appears | Why |
|---|---|---|---|---|---|
| 1 | 0-159 | 0-5.3 | p1 plea | **HOOK.** TOP band, y 180. ONE pill, already on screen at frame 0 (no fade — only a 6-frame scale 1.06->1.0 settle). Speaker tab, larger than usual (48 px): "A father begs Jesus". Pill text, 96 px, two lines: "My little girl / is dying." Out f151-159. | A stranger gets who + the stake in the very first frame, in 9 words. The text leads the voice by about 2 s on purpose. |
| 2 | 237-357 | 7.9-11.9 | p2 news | LOW band, y 1240. Pill, 96 px, two lines: "Thy daughter / is dead". Tab "The messenger". Chip "Mark 5:35". In f237-245, out f349-357. The "why troublest thou..." line is heard, NOT shown. | The blow. KJV, 4 short words. The hard old line would be too much to read. |
| 3 | 372-449 | 12.4-15.0 | p2 -> p3 | **DEVICE lands.** "Too late." in the navy pill (`rgba(21,37,60,0.80)`), 150 px, centred, y 1300. In: drops 40 px and stops hard over 5 frames (ease-out cubic, no bounce). No tab, no chip. **It stays on screen through the picture cut at f408.** | The verdict. Holding it over the cut makes the walk happen *under* the words. |
| 4 | 450-510 | 15.0-17.0 | p3 walk | **DEVICE strikes**, on "and did not turn back". Stroke starts at x 150, crosses the words by f462, then runs on to x 1100 (off screen) by f474. From f462 the pill fades to 45% and shrinks to 0.9. Pill out f498-510. Stroke fades with it. | The whole film in one move. The line that keeps going = He kept going. |
| 5 | 528-600 | 17.6-20.0 | p3 walk | TOP band, y 210. Pill, 96 px, two lines: "Be not afraid," at f528, "only believe." at ~f564. Tab "Jesus" (turquoise). Chip "Mark 5:36". Out f588-600. | First time we hear the answer. Same pill returns at the end, so the viewer already knows it. |
| — | 606-758 | 20.2-25.3 | p4 hand | **Nothing.** | A breath before the climax. The room is quiet; the screen is too. |
| 6 | 759-963 | 25.3-32.1 | p4c arise | TOP band, y 210. BIG pill, 112 px: "Talitha" f759, "cumi." f777 (each word fades + rises 12 px over 10 frames — slow, gentle). Tab "Jesus". Chip "Mark 5:41". At f906 (30.2 s) a second, smaller pill fades in under it (y 450, 76 px, no tab): "Little girl, get up." Both out f951-963. | The title words, in His voice, held the whole beat. Then the plain meaning for people who do not know the words. "Damsel, I say unto thee, arise" is heard only — three text lines would be too many. |
| 7 | 969-1050 | 32.3-35.0 | p5 rise | TOP band, y 210. One pill, 84 px, two lines: "She got up" at f969, "and walked." (line 2) at f999. No tab, no chip. Out f1042-1050. | Plain proof, in 5 words. Nothing shown on "The news had said it was over" — the picture answers it. |
| — | 1128-1292 | 37.6-43.1 | p6 family | **Nothing.** | The hug is the payoff. Words would get in the way. |
| 8 | 1330-1530 | 44.3-51.0 | p7 believe | **DEVICE closes.** LOW band. "Too late." navy pill, smaller (96 px), y 1260, in at f1330 on the spoken words. At f1362 ("hear Him instead") the same stroke crosses it and runs off the right edge (f1362-1386). Pill dims to 45%, slides up 250 px to y 1010 and shrinks to 0.7 (f1386-1404) — it makes room. Fades out f1515-1530. | Closes the thread. The lie is now small and pushed aside, not erased by magic. |
| 9 | 1446-1614 | 48.2-53.8 | p7 believe | **ENDING.** LOW band, y 1150. BIG pill, 112 px, two lines: "Be not afraid," f1446, "only believe." f1497. Tab "Jesus". Chip "Mark 5:36" in at f1512. Holds to the last frame. Last 8 frames: the whole frame (video + pill) fades to deep teal `#0E434D`, not black. No end card. No logo. No "subscribe". | Last thing on screen = His words, alone, for 3 quiet seconds. Long enough to read twice. |

Total: 9 moments, 2 fully clean pictures.

## Things NOT to do

- No glow, sparkle, light rays or particles — anywhere.
- No text on p4 and p6.
- No word-by-word karaoke captions. Only the lines above.
- Do not strike anything except "Too late."
- No pill may cover a face, or the joined hands on p4c, or the hand on the shoulder on p7 (about x 300-520, y 640-780).
- Do not move, zoom or re-grade the base video.

## Build notes for Remotion

- `<OffthreadVideo>` base + one `<AbsoluteFill>` overlay. Each row above = one `<Sequence from durationInFrames>`.
- Fonts: `@remotion/google-fonts/Kalam` (`loadFont()`, weights 400/700).
- Strike: measure the path with `getLength()` (or `@remotion/paths` `evolvePath`) and animate with `interpolate(frame, [0,24], [0,1], {extrapolateRight:'clamp', easing: Easing.out(Easing.cubic)})`.
- Beat 3 crosses a picture cut: it must be its own Sequence (f372-510 together with beat 4), not tied to a per-picture component.

## Open questions (check before building)

1. Exact frame of "only believe." in the 17.6-20.2 line was not given — f564 is a guess. Take it from the word alignment.
2. The art moves. The band positions were set from the stills. Check each pill against the real clip's first AND last frame.
3. p4c still shows the girl lying down with open eyes, not sitting up. If the clip has her rise, check the TOP band stays clear of Jesus's head (about y 700-890 in the still).
4. p4/p4c stills have a thin orange outline around Jesus and the girl. It is in the art, not from this design. Owner rule is "no glow on Jesus" — worth one look.
5. The hook text is on screen about 2 s before the voice says "my little girl is dying". Done on purpose for the 2-second hook. If it feels odd, split it: tab at f0, pill text at f48.
6. Not viewed in a browser (house rule: never auto-open). Font widths were estimated, so check pill widths on first render.
