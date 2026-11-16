# Independent review — codex (OK, 204s)

Three remaining MUST-FIX bypasses, reproduced with in-memory fixtures:

1. **A later SOUND flag disappears.** [ `_rules.py:201`](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/_rules.py:201) keeps “the one with the most parsed values.” Input: a complete passing `ANGLE A` row, followed by `ANGLE A | SOUND FLAG (doctrinal overclaim)`. Result: **PASS**, with no failure reasons. Two judges appending `ANGLE A | COMMON? yes` likewise leave the card passing. This violates challenge gates 5–6. Aggregate objections across every occurrence; conflicting or ambiguous rows must fail closed.

2. **Changing the kill list does not invalidate judgments.** [gate.py:32](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/gate.py:32) checks staleness only against `CARDS.md`. Input: finish judging, then correct `SUNDAY_SCHOOL.md` to explicitly include the candidate’s angle. Result: **PASS** using judgments that never saw that kill item. `owner_card.py` also accepts this unchanged review state. Bind judgments to the complete prompt inputs and invalidate them when those inputs change.

3. **The owner-answer command clears nonexistent or failed cards for words.** [owner_answer.py:6](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/owner_answer.py:6) checks only whether the answer is YES/NO. Input: `owner_answer.py <existing-empty-topic> Z NO "unseen"` with no cards, gate, or owner card. Result: it records NO and prints **“words may start.”** Existing answers also lack any binding to the reviewed card version. Require current gate clearance and bind the answer to the exact card shown.

VERDICT: FAIL
TOP FIXES:
1. Preserve every SOUND FLAG and COMMON objection across duplicate judge rows.
2. Invalidate judgments whenever their prompt inputs change.
3. Require current card clearance and version binding before owner-answer clearance.
