# Swirls Short #17 "Only a Voice" — narration candidate G (F + the 5-CLI panel fixes)

45-second vertical Bible short. 8 lines, one storyboard page each. KJV verbatim for every character line. 3 s silent hold after line 8.

| # | Line | Words | Speaker / cue | Ref |
|---|---|---|---|---|
| 1 | Is John the promised one? | 5 | narrator (hushed, the crowd's own wonder) | Luke 3:15 (grounding only, not quoted) |
| 2 | Priests from Jerusalem find him at the river: "Who art thou?" | 11 | narrator; quote = questioner (sharp, official) | John 1:19 |
| 3 | Not the promised one, he says first: "I am not the Christ." | 12 | gloss = narrator, BEFORE the quote; quote = john (firm, quick) | John 1:20 |
| 4 | They guess two great names. No, twice. They need an answer. | 11 | narrator (reports John 1:21-22, no names) | John 1:21-22 |
| 5 | Finally: "I am the voice of one crying in the wilderness." | 11 | quote = john (quiet, sure; "crying" read as calling out loud, never weeping) | John 1:23 |
| 6 | Isaiah wrote its cry: God comes. "Prepare ye the way of the LORD." | 13 | narrator; short stop after "God comes", then reads Isaiah (slow, ringing) | Isaiah 40:3 |
| 7 | Jesus comes. "Behold the Lamb of God, which taketh away the sin of the world." | 15 | 2 narrator words; quote = john (glad, full of wonder, slow on "sin of the world") | John 1:29 |
| 8 | **G1 (pick):** The voice is John. The Lord is Jesus. Behold him. | 10 | narrator (warm, open, unhurried) | John 1:23, Isaiah 40:3, John 1:29 |
| 8 | **G2 (alt):** Hear the voice. Behold the Lamb: Jesus, the Lord. | 9 | narrator (warm, open) | same |

**Counts (recounted by script).** G1 = 5+11+12+11+11+13+15+10 = **88 words**. G2 = 87 words.
Line 7 is the one off-range line (15). Landing 10 (G1) / 9 (G2). Hook 5.
**Voiced character quotes: 4** (lines 2, 3, 5, 7), 1 per line. Plus 1 narrator Isaiah read (line 6).
**Time check:** G1 88 / 2.2 + 0.4 x 4 = **41.6 s**. G2 87 / 2.2 + 1.6 = 41.1 s. Then 3.0 s hold.
(If the Isaiah read is also counted as a pause: G1 42.0 s, G2 41.5 s. Still inside 38-42, but G1 has no spare room.)

**KJV check** — `swirls_short.kjv_run_found(ref, text)`, all `(True, 'ok')`:

| Line | Run | Ref | Result |
|---|---|---|---|
| 2 | Who art thou? | John 1:19 | ok |
| 3 | I am not the Christ. | John 1:20 | ok |
| 5 | I am the voice of one crying in the wilderness | John 1:23 | ok |
| 6 | Prepare ye the way of the LORD | Isaiah 40:3 | ok |
| 7 | Behold the Lamb of God, which taketh away the sin of the world. | John 1:29 | ok (whole speech) |

Control: a changed run ("who takes away") returns False, so the check has teeth. All 5 runs are in PACK.md's table.

**Must-say truths.** John points away from himself to Jesus (3, 5, 7, 8). Jesus is the Lord whose way is made ready, God himself coming (6 "God comes" + "the LORD", 7 "Jesus comes", 8 "The Lord is Jesus"). Jesus is the Lamb who takes away the sin of the world (7, KJV whole).

**Curiosity gap.** Is this man the promised one? He says no — only a voice (5) — and the gap pays off when the one the voice is for walks in (7) and is named (8).

## Panel point -> fix

| # | Panel point | Seats | Fix in G |
|---|---|---|---|
| 1 | Landing was a bare doctrine line, no invitation, could end any short | 5/5 | Line 8 is built only from this piece's words: **voice** (5), **Lord** (6), **Behold** (7). "Behold him" is John's own KJV verb, handed to the viewer. An invitation, no pressure, no gain/loss. None of the banned endings. |
| 2 | Hook generic; "desert man" clashes with "at the river" | claude, codex, gemini | Hook is now the real irony: people wondered if John was the promised one (Luke 3:15); he says no, only a voice. "Desert" is gone. It is the narrator's question, not the priests' — they still ask only "Who art thou?". |
| 3 | Line 4: Elijah / the Prophet lose a newcomer; "The Prophet? No." teaches John is not a prophet; "must have an answer" unclear | claude, codex, grok, testers | Names cut. "They guess two great names. No, twice." Nothing says John is not a prophet. No invented question. "They need an answer" is plain. |
| 4 | Lamb had no meaning; "sin of the world" was cut | cursor, grok, round-2 testers | Line 7 carries the whole 13-word KJV speech with 2 narrator words before it. Gemini's "taketh" worry: the word sits inside a clear phrase and John's slow read; judged a smaller risk than a Lamb with no meaning. |
| 5 | Line 3: quote ran into the gloss by ear | cursor | Gloss moved in front of the quote and split from it by "he says first:". The line now ends on John's own words. "First" keeps the denial unprompted. |
| 6 | "God himself" was claimed with no heard words behind it; LORD (6) -> Lamb (7) -> Jesus (8) had no bridge | codex, cursor, grok, Fable | Line 6 says "God comes" right before "the way of the LORD". Line 7 opens "Jesus comes". The ear hears: God comes -> Jesus comes -> "The Lord is Jesus". "God" said plainly once. |
| 7 | Line 6 framed the cry as the label for the voice | grok | "Isaiah wrote its cry" — the quote is now named as the cry. Never "the same words". |
| 8 | Title idea dropped at the end | gemini, cursor, grok | Landing starts on "The voice is John". |
| 9 | "crying" may be heard as weeping | Fable, grok | KJV stays. Voice cue on line 5 + picture note: John calling out, mouth open, hand raised. Line 6 "its cry" helps. |

## Still weak

- **"Behold"** is an old word doing the landing's work. It is heard seconds earlier with John pointing, so it should carry. If a seed viewer trips, swap line 8 to "The voice is John. The Lord is Jesus. Look to him." (11 words — would need "first" cut from line 3).
- **G1 is at the top of the budget** (88 words, 41.6 s). No room to add a word.
- **"Next day" is gone** from line 7 to fit the whole KJV speech. Page 7 must show it: new day, Jesus walking in, no priests.
- **"Isaiah"** is not introduced ("long ago" was cut). Page 6 art: an old scroll.
- **Line 5 has one narrator word** ("Finally:"). The voice change must make clear it is John.
- **Line 4 "two great names"** is vague on purpose. A Bible reader may miss Elijah; page 4 art can letter the two names small.
- **"taketh"** stays (gemini's worry). Plain alternative breaks the whole-speech rule or costs words.
- **Hook leans on Luke 3:15**, which is outside the pack's verse table. True to the text, but the Bible seat should confirm.
- Not yet re-tested by blind seats. G needs the panel and a global-audience pass before the words lock. A lock never authorizes spend.
