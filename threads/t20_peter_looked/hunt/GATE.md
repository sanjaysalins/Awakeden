# GATE - hunt

Judges read: 5 (claude, codex, fable, gemini, sonnet). Driver 2. Bars: FRESH 7, TRUE 8, CLEAR 7, JESUS 8, GROWTH 7, DEPTH 7, SOUND no flags, COMMON yes under 2 (partly is shown, not failed), 1 non-Claude judge, CONTEXT PASS x2, anchors valid.

| Card | FRESH | TRUE | CLEAR | JESUS | GROWTH | DEPTH | COMMON yes (partly) | Result |
|---|---|---|---|---|---|---|---|---|
| A | - | - | - | - | - | - | 0 (0) | FAIL: unparsed (claude); unparsed (codex); unparsed (fable); unparsed (gemini); unparsed (sonnet); no non-Claude judge (codex/gemini/grok) at the FRESH and DEPTH bars; CONTEXT gemini FAIL |
| B | 7 | 7 | 6 | 6 | 4 | 5 | 0 (3) | FAIL: TRUE 7<8; CLEAR 6<7; JESUS 6<8; GROWTH 4<7; DEPTH 5<7; SOUND flag from claude, codex, fable, gemini (no waiver: reword and re-judge); NOTE audit claude missing (run note_audit.py); NOTE audit codex missing (run note_audit.py); no non-Claude judge (codex/gemini/grok) at the FRESH and DEPTH bars |
| C | - | - | - | - | - | - | 0 (0) | FAIL: unparsed (claude); unparsed (codex); unparsed (fable); unparsed (gemini); unparsed (sonnet); no non-Claude judge (codex/gemini/grok) at the FRESH and DEPTH bars; CONTEXT gemini FAIL |

PASS cards: none

NO PASS - NO FILM: reword + re-judge, or pick another topic
