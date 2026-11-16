# Candidates round 2, ep 17 (fix of test r1). [cue] = voice emotion cue.

Round 1 votes: A = fable, codex. C = claude, cursor, gemini. No doctrine FAIL.
D = best fix of A. E = best fix of C. Both checked by script (word lint + KJV run check).

## D "Just a Voice" -- fix of A, whole 13-word speech on line 7
| # | Line | Words | Quote (ref, speaker) |
|---|---|---|---|
| 1 | Who is this desert man? | 5 | - |
| 2 | Priests from Jerusalem find John at the river: "Who art thou?" [questioner: sharp, official] | 11 | John 1:19, questioner |
| 3 | He says, "I am not the Christ", the one God promised. [john: firm, quick] | 11 | John 1:20, john |
| 4 | They guess two names. No. No. What does he call himself? | 11 | - (narrator reports) |
| 5 | John answers, "I am the voice of one crying in the wilderness." [john: quiet, sure] | 12 | John 1:23, john (stops at "wilderness") |
| 6 | Isaiah wrote of that voice: "Prepare ye the way of the LORD." [narrator reads, slow] | 12 | Isaiah 40:3, narrator |
| 7 | Jesus comes. "Behold the Lamb of God, which taketh away the sin of the world." [john: glad, full of wonder] | 15 | John 1:29 whole speech, john (2 narrator words before it) |
| 8 | The voice was John. The Lord is Jesus, God himself. | 10 | - |

- Total: 5+11+11+11+12+12+15+10 = **87 words**. Voiced character quotes: **4** (+1 narrator Isaiah read).
- Time: 87 / 2.2 = 39.5. With 4 pauses: 39.5 + 1.6 = **41.1 s**. If the Isaiah read also pauses: 39.5 + 2.0 = **41.5 s**. Both inside 38-42.
- Script lint: SWS-G1 CONDITIONAL (line 7 is the one allowed 15-word line), SWS-G1e PASS.
- Truths: (1) lines 3, 5, 8 ("The voice was John"). (2) lines 6 + 8 ("The Lord is Jesus, God himself"). (3) line 7, full KJV.
- Curiosity gap: who is the desert man? Paid on line 5 (a voice) and closed on line 8.
- Landing word from the passage: *voice*.
- Still weak: "Next day" is not spoken (only 2 narrator words fit before the whole speech; the page must show a new morning). No "Long ago" before Isaiah (no room). "taketh" has no plain echo. John's voice is not named on line 7 (third time we hear him, and the page shows him pointing).

## E "The Lord Is Coming" -- fix of C, 5-word run + plain words
| # | Line | Words | Quote (ref, speaker) |
|---|---|---|---|
| 1 | Who is this wild man? | 5 | - |
| 2 | Priests from Jerusalem reach the river and ask, "Who art thou?" [questioner: demanding] | 11 | John 1:19, questioner |
| 3 | He says, "I am not the Christ", the one God promised. [john: firm, quick] | 11 | John 1:20, john |
| 4 | They try two names. No. No. They must have an answer. | 11 | - (narrator reports) |
| 5 | John answers, "I am the voice of one crying in the wilderness." [john: steady, clear] | 12 | John 1:23, john (stops at "wilderness") |
| 6 | Long ago Isaiah wrote of that voice: "Prepare ye the way of the LORD." [narrator reads, slow] | 14 | Isaiah 40:3, narrator |
| 7 | Next day John sees Jesus coming and says, "Behold the Lamb of God." [john: glad, awed] | 13 | John 1:29 5-word run, john |
| 8 | That Lord is Jesus: God, taking away the world's sin. | 10 | - (narrator plain words; KJV sentence not split) |

- Total: 5+11+11+11+12+14+13+10 = **87 words**. Voiced character quotes: **4** (+1 narrator Isaiah read).
- Time: 87 / 2.2 = 39.5. With 4 pauses: **41.1 s**. With 5: **41.5 s**. Both inside 38-42.
- Script lint: SWS-G1 PASS, SWS-G1e PASS.
- Truths: (1) lines 3, 5, 7. (2) lines 6 + 8 ("That Lord is Jesus: God"). (3) lines 7 + 8.
- Curiosity gap: who is the wild man? Paid on line 5 (a voice), and line 8 says whose way he made ready.
- Landing words from the passage: *Lord*, *takes away the sin of the world* (plain).
- Still weak: "God himself" became "God" to fit 10 words. "Lamb" is not explained. The whole John 1:29 speech is not heard in John's voice.

## KJV check (script: swirls_short.kjv_run_found + kjv_strict.verify_span)
| Ref | Run | Result |
|---|---|---|
| John 1:19 | Who art thou? | True / OK |
| John 1:20 | I am not the Christ | True / OK |
| John 1:23 | I am the voice of one crying in the wilderness | True / OK |
| Isaiah 40:3 | Prepare ye the way of the LORD | True / OK |
| John 1:29 | Behold the Lamb of God, which taketh away the sin of the world. | True / OK (D) |
| John 1:29 | Behold the Lamb of God | True / OK (E) |

Note: on line 3 the comma sits OUTSIDE the quote marks on purpose. "I am not the Christ," with a comma inside fails the run check (the verse has a full stop there).

## Convergent points -> fix
| # | Point (seats) | D | E |
|---|---|---|---|
| 1 | Line 7: name Jesus, say who speaks, full speech wanted | Whole 13-word speech. 2 narrator words "Jesus comes." name Jesus. John named on 5 and 8; his voice + pointing page carry the speaker | "Next day John sees Jesus coming and says," names both. 5-word run; plain words finish it on line 8 |
| 2 | Line 6: Isaiah's own words read by narrator | "Prepare ye the way of the LORD." read by narrator | Same, with "Long ago" |
| 3 | "Not Elijah. Not the Prophet." overloads; gloss "Christ" | Names dropped: "They guess two names. No. No." Christ gloss: "the one God promised" | Names dropped: "They try two names. No. No." Same gloss |
| 4 | Hook: no "baptizing", no "Who is John really?" | "Who is this desert man?" (5, kept; best-rated hook) | "Who is this wild man?" (5) |
| 5 | Drop "Levites" | "Priests from Jerusalem" | "Priests from Jerusalem" |
| 6 | Landing: "God" plainly, Jesus = the Lord, takes away the world's sin, no "Behold him", keep "away" | "The Lord is Jesus, God himself." Sin taken away is in the full KJV on line 7 | "That Lord is Jesus: God, taking away the world's sin." |
| s1 | "saith", not "cries" (claude) | No verb needed | "and says" |
| s2 | "crying" may read as weeping (codex) | Not fixed in words (no room; KJV stays). Fix in the picture: John calling out, hand raised, not weeping | Same |
| s3 | "cannot go home with nothing" over-dramatic (codex, cursor, gemini note) | Line dropped; narrator asks "What does he call himself?" | Softened: "They must have an answer." |
| R | Modern-English dialogue (codex) | REJECTED. KJV verbatim is locked | REJECTED |

Accuracy notes kept: one question only (1:19); the Christ denial is unprompted; "They guess/try two names" = exactly the two guesses of 1:21 (never "three guesses", never "more"); no "same words"; no Elijah explained; no year count.
