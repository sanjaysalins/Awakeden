# Fix panel synthesis (2026-11-21)

Blind seats: fable (subagent), sonnet (subagent), claude (CLI), codex (CLI), gemini (AGY, Gemini 4 Carbon).
grok = 402 (balance exhausted), no output. Pack = PROMPT.md (spoken words only, no lead verdicts; leak-checked).
Avg = mean of the 4 scores (0-10) across 5 seats. Lines picked by convergence (2+ seats), credited.

| # | Short | Avg | Stay 3 s | Verdict |
|---|---|---|---|---|
| S2 | Simeon / Mary at the cross | 6.8 | 4Y 1M | FIX LAST + TITLE |
| S6 | Father, into Thy hands | 6.5 | 3Y 2M | FIX FIRST + TITLE · HUMAN CHECK the "evening prayer" claim |
| S10 | Storm | 6.0 | 5Y | HOLD: middle adds feelings not in the text (raging/furious, knees, His reason for sleeping) - 4 seats. First/last fix is not enough |
| S4 | Nazareth | 5.6 | 2Y 3M | FIX FIRST + TITLE |
| S5 | Ten healed | 5.1 | 1Y 4M | FIX FIRST + LAST + TITLE |
| S8 | Empty tomb | 5.0 | 1Y 3M 1N | FIX LAST + TITLE · HUMAN CHECK "Believed what? That his Lord was risen" (claude, single-source; John 20:9) |
| S1 | Rahab | 5.0 | 5M | FIX FIRST + LAST + TITLE |
| S7 | Snake on a pole | 4.9 | 5M | FIX FIRST + TITLE (middle scolds: 4 seats; ok but weak) |
| S9 | Simon of Cyrene | 4.0 | 1Y 3M 1N | HOLD: locked middle = Hebrews word study + "carry his shame" ask (all 5) |
| S3 | Bethlehem | 4.0 | 2M 3N | DROP x3 (fable, claude, gemini), last x5. Owner call: it is dated 1 Dec |

## Picked lines (convergent)
- S1 FIRST: "When Jericho fell, the only family that walked out alive was a prostitute's." (fable; claude + gemini same move: shame first)
- S1 LAST [DIRECT]: "Whatever they call you, her name is in His family. There is room for yours." (fable; gemini same idea) - replaces the "bring everyone you love inside" command (all 5 flagged)
- S1 TITLE: "Her Name Was Shameful. Her Family Was the One Saved." (claude; fable/sonnet/gemini shame-first)
- S2 LAST [QUIET PICTURE]: "He was dying, and He made sure His mother did not go home alone." (fable; gemini + sonnet same picture)
- S2 TITLE: "Dying, He Still Saw His Mother's Pain" (fable/claude/codex/sonnet)
- S4 FIRST: "Afraid God is angry with you? Watch where Jesus stopped reading." (fable/claude/gemini)
- S4 TITLE: "Afraid God Is Angry? See Where Jesus Stopped Reading" (fable/claude/gemini)
- S5 FIRST: "Ten sick men begged Jesus for mercy. He sent them off, still sick." (fable/claude/sonnet)
- S5 LAST [QUIET PICTURE]: "Nine went on clean. One, face down at His feet, went on whole." (claude/sonnet/fable)
- S5 TITLE: "Nine Were Healed and Kept Walking. One Turned Back." (sonnet; claude/fable similar)
- S6 FIRST: "If you are afraid to die, listen to the last thing Jesus said." (fable/gemini/claude)
- S6 TITLE: "Afraid to Die? Jesus' Last Words Were a Night Prayer" (fable/claude/sonnet/gemini)
- S7 FIRST: "People were dying of snake bites. God's cure was a snake on a pole." (fable/claude/codex/gemini)
- S7 TITLE: "Bitten and Dying, They Were Told Only to Look" (fable/claude/sonnet)
- S8 LAST [DIRECT]: "You were not there. He spoke about you anyway, and called you blessed." (sonnet; claude/fable/gemini same)
- S8 TITLE: "Never Seen Jesus? He Already Called You Blessed" (claude; gemini/fable similar)
- S11 TITLE: "He Said No Three Times. Jesus Made Him Breakfast." (fable; claude/sonnet/gemini same)
- S3 TITLE (if kept): "They Knew Where the King Was. Did They Go?" (fable/claude/sonnet)

## Needs human check (not in the films until checked)
- S6: "Jewish tradition made these words an evening prayer ... a child could learn" - outside the Bible text (claude, sonnet, fable). Web-check before posting.
- S8: "Believed what? That his Lord was risen." - John 20:8-9 does not say what John believed (claude only).
- S2: "turns to bind it" reads more than John 19:26 says (claude only).
- S10: added feelings + motive in the locked middle (fable, claude, sonnet, codex).

Lines to re-record: S1 x2, S2 x1, S4 x1, S5 x2, S6 x1, S7 x1, S8 x1 = 9 lines.
