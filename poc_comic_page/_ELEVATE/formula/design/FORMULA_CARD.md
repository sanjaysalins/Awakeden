# Formula card: the 38-second Jesus short

Model film: "Jesus Promised Paradise to a Criminal" (Luke 23:39-43).
Rule of the card: **fix the skeleton, rotate the skin.** Every film finds its own fresh true detail.

## 1. Fixed skeleton (same every film)

| Part | Rule | Model film |
|---|---|---|
| Length | 30-60 s total, the shorter the better (owner, 2026-11-15) | 38.0 s |
| Words | about 60-130 spoken words (shorter preferred) | 74 words |
| Voices | 3-4: narrator + 1-2 people in the story + Jesus | narrator, mocker, thief, Jesus |
| Scripture | KJV verbatim, 2-3 short quotes, verse tag for each. Partial verses cut at a clause and said so. | Luke 23:39b, 42b, 43b |
| Hook | Said in the first 2.5 s. First picture is the hook's subject. | 0.0-3.7 s |
| Set-up | One plain line: who and where | 3.8-6.5 s |
| Jesus speaks | Once, late, 55-70 percent in. 0.4 s pause before each quote. | 22.4 s (59 percent) |
| Landing | Short echo of His own words. Lands on Jesus. One plain invite. No gain/loss, no pressure. | 26.5-34.7 s |
| Hold | 3.0 s of picture and sound after the last word | 35.0-38.0 s |
| Look | COMIC PAGES (owner-approved 2026-11-15): 2-4 live panels per page, panels slam in on words, camera reads panel by panel; at least 60 percent of runtime on 2+ panel pages; full-bleed only for the hook payoff, Jesus' line (still) and the landing. No duplicate clip on a page; crop on faces, never the back of a head. | model film v3: 9 pages, 62 percent |
| Last picture | Jesus, or the place He promised. Never the emotional peak. | garden, Jesus on the hill |

Gates stay as they are: narration gate, doctrine both ways (own red-team + 5-CLI panel), guardrail questions, landing-hold check. Words lock before any spend.

## 2. Rotating skin (new every film)

**Never the same hook shape or landing shape 2 films in a row.** Log the shape used in each film.

Hook shapes (pick 1):
1. **The odd gift.** Someone gets what they should not. ("Jesus promised paradise to a criminal. Why?") Used in the model film.
2. **The small detail.** The text records one exact thing. Why?
3. **The wrong person.** The last person you expect does the right thing.
4. **The one word.** One word in the verse changes the scene.
5. **The question in the story.** Open on a question a person in the text really asks.

Landing shapes (pick 1):
1. **The trade-up echo.** "Not X. Y." built from His words. Used in the model film.
2. **His line again.** Repeat 2-4 of His own words, then stop.
3. **The earned word.** End on one plain word taken from the film's own quote.
4. **The quiet question.** One honest question to the viewer, no answer given.
5. **Picture lands it.** One plain sentence, then the last picture does the rest.

Also new each film: the fresh true detail, the story's own contrast, the comic moves.
Not part of the formula: "someday vs today" and "X for a Y?". Those belong to the model film.

## 3. Comic move rule (replaces the doodle rule, 2026-11-15)

This is a graphic comic book. Use comic motion, not storybook doodles.

- FULL comic motion (owner, 2026-11-15): page turns, panel slams, dives and doodles throughout, each tied to a spoken word. Model film: `../MODEL_FILM_LOCK.json` (v3, gates G1-G11).
- Pick from: panel slam on a page + camera dive, spiky balloon edge + shout marks, ink gutter split, halftone hush, ink-bleed cut, sun-line burst.
- **When Jesus speaks: nothing.** No border, no lines, no dots. Loud ink for others, stillness for Him.
- No-draw zone: Jesus' face, any crucifixion close-up. A panel border round a picture is fine. A mark on the picture is not.
- Nothing to read. No sound-effect words, glyphs, arrows. Nothing that only works left-to-right.
- Keep clear of the pill (y 974-1250) and the platform zones (top 200 px, bottom from 1500 px, right rail).
- Ink `#14100C`, bone `#F3E9D2`, page paper `#FAF0D6`. 8-9 px outlines, wobbled edge. No glow, no stock vector look.
- Move frame = `ceil(word_start * 30)` from the words.json. Never early.
- Anything stuck to the picture must track the clip's own motion, then apply the push-in per frame.
- No move in the 3 s hold. The landing stays still.
- Model design: `comic\COMIC_MOTION_DESIGN.md` in this folder.

## 4. Language rules

- **ONE upload per film (owner decision, 2026-11-15).** The English pills stay on the picture. Each other language = a translated SRT that is then used to make a DUBBED audio track (same voices, same slots), added to the same YouTube video. Dubbing is paid: quote the price and get a separate yes first.
- A word-free copy (`build_s32.py clean`) exists as a spare master only; it is not uploaded.
- **A human writes each SRT.** A fluent speaker checks it. No raw machine output.
- **Scripture lines come from a public-domain Bible in that language. Never machine-translate Scripture.** Check the edition is public domain in the target country before use. Starting points to verify: Reina-Valera 1909 (Spanish), Louis Segond 1910 (French), Luther 1912 (German), Almeida older edition (Portuguese), Synodal (Russian), Chinese Union Version 1919, Van Dyck (Arabic).
- **The echo must match.** The landing repeats His words, so the narrator lines must reuse the exact words that Bible uses.
- **Verse tags use the local book name:** Lucas 23:43, 路加福音 23:43, لوقا 23:43.
- **Cue timing:** each cue at least 1.2 s, at most about 6 s, 2 lines max.
- **No one-word orphans.** Join a short word to its neighbour. In the model film: "Someday." (0.4 s) joins "He asked to be remembered." and "Today." joins "Not someday."
- **Line length:** about 32 characters per line for Latin scripts, about 14-16 for Chinese, Japanese, Korean.
- **CJK:** no spaces between words, break lines at a phrase, use full-width punctuation.
- **RTL (Arabic, Hebrew, Urdu, Persian):** plain text only, verse tag on its own line, check that numbers and punctuation sit on the correct side on a real phone.
- Title, description and tags are written per language too, by a human.

## 5. Does this story fit? (need 5 of 6)

1. Does Jesus say one short line (12 words or fewer) that turns the scene?
2. Does someone else in the story also speak?
3. Is there a fresh true detail in the text that most people miss?
4. Can a person who has never read the Bible follow it in 2 plain sentences?
5. Does it land on Jesus without adding anything the text does not say?
6. Is there a wide, face-free picture for the hold?

If 1 or 5 is "no", it is not this formula. Use another format.
