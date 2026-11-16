## VERDICT (PASS / REVISE / FAIL) and score 0-10
**REVISE — 5/10.** Good instincts (voice at 0s, one panel at a time, KJV byte-gate). But the plan contradicts itself in six places, its own storyboard fails its own gates, and the "alive" claim rests on CSS previews with motion switched off. Nothing here has been seen moving.

## BIGGEST RISK (quote the line)
"At rest a panel is a real Kling/Seedance clip." That is the same camera-only footage that scored 4.75 for alive. Ink Wake, Gutter Cut and Card Slam are 0.5s entrances; the other ~85% of screen time is unchanged. You are repainting the doorways and calling the room new. And the signature sits in a band you admit is narrow: under 0.5s a pencil→ink→colour pass reads as a wipe on a phone; slower and it "becomes a tic". No real render proves the band exists.

## WHAT TO CUT OR SIMPLIFY
- Page Turn and Break-Out: both "medium", both once per episode, Break-Out depends on a cutout with a known clipped arm. Drop from v1; ship 5 moves.
- Two proof paths. Design: "rebuild the first 20s of Piece 1". Recipe: "build the machine WHILE making Piece 2". Pick one.
- Eight sound cues in 28s (scratch, thud, crackle, paper, knock, breath, tone, bell) against "Max 2 per episode" and "No SFX on sacred". `warm_tone.wav` fires at 12.8 on `p2b`, `"sacred": true`. Your gate fails your example.
- Ink Wake frequency: "how most panels enter" vs "not on every cut" vs "max once per page" vs "no move 3 times in a row". Four rules, no number.

## WHAT IS MISSING
- **Who Jesus is.** 4 of 5 seats lost here last time. The new 28s never says it; "Jesus answers it before you can ask" assumes the viewer already knows Him. Same failure, repeated, $0 to fix.
- **Decode of "giveth" and "cometh".** Flagged 5/5; only "in no wise" gets a card. The decode gate has no word list, so it can never fail.
- **The example balloon breaks the 8-word rule.** "All that the Father giveth me shall come to me;" is 10 words. The min-time rule (1.2s + 0.25s/word) is broken by the hook card (6 words, needs 2.7s, gets 1.8s), the HIS OWN WORDS card (1.0s) and the thought (1.5s).
- **Picture fights words.** KNOCK lands on "That fear keeps you at the door". Knocking is coming; fear is a hand that does not knock. Your Recipe rule, broken in your storyboard.
- **Invented line eats its own reason.** "What if He says no?" is justified by "narration already says 'rehearsing'" — the line the thought replaces.
- **Order bug.** Recipe step 5 (animatic) needs voice; step 6 records it. `word_t0` drives every panel; voice before panel map.
- **Static gate is blind.** Line-boil and the ink front change pixels constantly, so "almost no pixel change over 4s" never trips. It measures jitter, not life.
- **No face gate.** The stated top risk (Jesus off-model) is left to eyeballs; no embedding-distance check.

## THREE SMALLEST FIXES (exact wording or rule)
1. Narration, before 12.8s: "Jesus — God's own Son, sent for you —". One plain line, through words-lock.
2. Rule: "Ink Wake on at most 1 panel in 3; always the first panel; always the Jesus panel." The gate counts.
3. Rule: "Balloon ≤ 8 words AND on screen ≥ 1.2s + 0.25s × words, or FAIL and print the text." Then split: "All that the Father giveth me / shall come to me;".

**The ONE change that helps most:** before building eight tools, cut a 10-second real-clip proof (3 panels, Ink Wake at 0.5/0.8s, one gold balloon, the who-Jesus-is line) and blind-test it on a phone. If viewers cannot say both "it was drawn in front of me" and "who Jesus is", this is a wipe over 4.75 footage.

## ODDS this makes episodes more watched than a plain Ken Burns comic (range with error bars)
**60% (45–75%).** Most of the lift comes from voice-at-0s, one text layer and the 4-second rule — all of which a Ken Burns comic could adopt tomorrow. The ink language on its own: 50% ± 20, a coin flip until one real clip exists. These are simulated seats, not viewers; ten real phones beat another panel.
