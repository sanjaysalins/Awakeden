# Independent review — codex (OK, 179s)

The gates do **not** enforce the advertised contract. These are MUST-FIX findings from the code; runtime verification was blocked because Python could not launch.

1. **Any doctrinal objection can be waived without changing anything.** Step 5’s `WORDING-FIX: C` suppresses **every** SOUND flag for C, regardless of its reason; no revised text or re-review is required ([gate.py:70](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/gate.py:70)).  
   **Fix:** Remove the waiver; require fresh SOUND PASS judgments on the corrected card.

2. **Invented Scripture can satisfy “real KJV quotes.”** In [gate.py:51](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/gate.py:51), `"..."` produces no checkable fragments, so `all(...)` returns true. Thus `Bogus 999:999 "..."` and `Nonsense 999:999 "..."` count as two valid books. Separately, `Psalm` and `Psalms` count separately despite resolving to the same canonical book.  
   **Fix:** Require nonempty quotation text, validate every reference, and count canonical book identifiers.

3. **A familiar angle with decorative citations still passes.** `books_ok()` counts quotes anywhere, including disclaimers and WHY-VERSE; it never establishes that two passages support the central insight. Gospel parallels qualify, although [loom.py:32](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/loom.py:32) explicitly discounts them. `COMMON=yes` is merely displayed ([gate.py:74](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/gate.py:74)). WHY-VERSE and LABEL are not gate requirements.  
   **Fix:** Require identified anchors, their substantive contribution, and a justified WHY-VERSE or explicit ECHO limitation; block known-common central claims.

4. **“Median of 6 judges” can mean one judge—or incomplete votes.** Scores are pooled without requiring six successful, distinct judges or one complete vote per card ([gate.py:16](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/gate.py:16)). Duplicate rows count; stale files remain eligible after cards change.  
   **Fix:** Validate the agreed panel, complete votes, score ranges and current input fingerprints; fail explicitly on missing or stale judgments.

5. **“No loom, no hunt” checks filenames, not completed work.** Any nonempty placeholder satisfies [run_seats.py:8](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/run_seats.py:8); BRIEF and KJV_PACK can silently be absent. Calling judges and gate directly bypasses these checks entirely.  
   **Fix:** Require passage-matched, successful prerequisites at every downstream entry point.

6. **Two supposedly blind seats never receive the kill list.** The README gives Fable/Sonnet **“ONLY `BRIEF.md` + `KJV_PACK.md`”** ([README.md:33](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/README.md:33)); the list is appended only inside `run_seats.py`, not saved into BRIEF.  
   **Fix:** Build one shared hunt prompt containing the kill list and supply it to all six seats.

7. **The owner card can present a failed card as a contender.** [owner_card.py:10](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/owner_card.py:10) never checks PASS status; it displays numeric medians without SOUND objections. Scores precede the familiarity question, encouraging anchoring. YES/NO are inert spans, and the generated score table is HTML-escaped into literal markup.  
   **Fix:** Require a current PASS, show the insight and question before scores, record the owner’s decision, and render the table correctly.

8. **“Seed viewers decide” has no enforced consequence or reliable measurement.** Step 11 records a percentage; nothing consumes it. The form’s pass calculation ignores whether viewers understood the insight, despite collecting that answer ([SEED_VIEWER_FORM.md:20](F:/slk/PycharmProjects/JesusInTheBible/_roadmap/hunt_kit/SEED_VIEWER_FORM.md:20)). DEPTH’s “low/high” descriptions likewise provide no defensible boundary at 7.  
   **Fix:** Define anchored scoring examples and require documented viewer comprehension, ≥60% novelty, and owner approval before narration.

VERDICT: FAIL
TOP FIXES:
1. Remove WORDING-FIX immunity and require re-review of corrected doctrine.
2. Validate actual KJV anchors and substantive cross-book insight, not citation counts.
3. Fail closed on incomplete or stale reviews and missing viewer or owner approval.
