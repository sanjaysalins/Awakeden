# Hunt kit - find the fresh angle first ($0)

Rule: **hunt the link first. No strong link, no film.** Contract: `_roadmap\TWO_DRIVERS_ROADMAP.md` (sections 2-3).
One folder per hunt = the **topic dir** (e.g. `encounters\e09_go_home\hunt\`). Run from the repo root.
`PY` = `.venv\Scripts\python.exe`, `KIT` = `_roadmap\hunt_kit`.

> **CHALLENGE GATES (owner, 2026-11-16, hardened after red team) - plain words**
> 1. No loom, no hunt. `loom.md` must have the loom.py header and 1+ match. The loom is ours only.
> 2. No Sunday-school list, no hunt: `SUNDAY_SCHOOL.md` needs 5+ bullets (it includes the most-cited cross-references). Hand edits are logged at its bottom. Checked in run_seats, run_judges, gate, owner_card.
> 3. ONE hunt prompt: `HUNT_PROMPT.md` = brief + kill list + KJV text. Fable/Sonnet seats get ONLY that file. Judges get ONLY `JUDGE_PROMPT.md` (has the kill list).
> 4. ANCHOR gate: each card has `ANCHOR-1` (inside the passage), `ANCHOR-2` (another book, not a Gospel parallel), `WHY-VERSE`, `LABEL`. Quotes: 4+ real words, a real verse, exact KJV. PROPHECY/NT-STATED need a New Testament WHY-VERSE. ECHO needs a shared 3-word phrase or a loom match. DETAIL alone fails.
> 5. No waiver. Any SOUND flag fails the card. Fix = reword the card and RE-JUDGE (new judge files).
> 6. 5+ distinct judge files, every card fully scored in each (else "unparsed"), all newer than CARDS.md (else "stale"). One non-Claude judge (codex/gemini/grok) must clear FRESH and DEPTH. COMMON yes/partly from 2+ judges fails. DEPTH = strength of the link, not number of books.
> 7. CONTEXT seat: `context_check.py` -> codex and gemini must both PASS the card in context (+-10 verses around both anchors).
> 8. Owner card only for a card that is PASS in a current GATE.md. The owner sees the question first. Words start only when `OWNER_ANSWER.md` says NO for the chosen card (`owner_answer.py`).
> 9. Seed viewers (5-10) are needed before PUBLISH, not before words. Record the % in `INSIGHT_BANK.md`.

| Step | What | Command / file |
|---|---|---|
| 1 | Loom: word matches for the passage | `PY KIT\loom.py <topic> "Luke 8:22-39"` -> `<topic>\loom.md` (ours only, never sent) |
| 2 | Sunday-school list = KILL LIST | `PY KIT\sunday_school.py <topic> "Luke 8:22-39"` (2 CLI seats) -> `<topic>\SUNDAY_SCHOOL.md`; read it. Any hand edit: log it at the bottom ("EDIT date: what and why") |
| 3 | Brief + real verse text | copy `BRIEF_TEMPLATE.md` -> `<topic>\BRIEF.md` (no hand-written kill items), then `PY KIT\kjv_pack.py <topic> "Luke 8:22-39"` |
| 4 | 6 blind seats | `PY KITun_seats.py <topic>` (builds `HUNT_PROMPT.md`; `--check-only` tests prerequisites) + Fable and Sonnet (see below) |
| 5 | Quote check + FACTS check | `PY KIT\check_quotes.py <topic>\hunt_claude.md ...`, then `FACTS_TEMPLATE.md` -> `<topic>\FACTS.md` by hand |
| 6 | Neutral cards | by hand -> `<topic>\CARDS.md` (no authors, random order, only checked quotes). Each card: `ANCHOR-1:`, `ANCHOR-2:`, `WHY-VERSE:` (each `Book C:V "exact KJV"`), `LABEL:`, `DOES NOT PROVE:`, optional `INSIGHT:`. Re-run `kjv_pack.py` with every card verse |
| 7 | CONTEXT seat | `PY KIT\context_check.py <topic> A B C ...` (ALL candidate cards in one run) -> `context_codex.md`, `context_gemini.md`. `--prompt-only` writes `CONTEXT_PROMPT.md` only |
| 8 | 5+ fresh blind judges | copy `JUDGE_TEMPLATE.md` -> `<topic>\JUDGE_BRIEF.md`, then `PY KITun_judges.py <topic>` (builds `JUDGE_PROMPT.md`) + Fable and Sonnet judges |
| 9 | Gate | `PY KIT\gate.py <topic>` (Driver 1: add `--driver 1`) -> `<topic>\GATE.md`; exit 1 + "NO PASS - NO FILM" if nothing passes. A flagged card: reword, redo steps 7-9 |
| 10 | Owner card | `PY KIT\owner_card.py <topic> C` -> `<topic>\_OWNER_CARD.html` (refuses a non-PASS card); give the owner the file:/// link, do not open it |
| 11 | Owner answer | `PY KIT\owner_answer.py <topic> C NO "note"` -> `<topic>\OWNER_ANSWER.md` |
| 12 | Bank winner AND losers | rows in `_roadmap\INSIGHT_BANK.md` (medians) |
| 13 | Words | only when `OWNER_ANSWER.md` says NO for the chosen card |
| 14 | Seed viewers (5-10 real people) | `SEED_VIEWER_FORM.md`; needed before PUBLISH, not before words. Put "not seen" % and "said it back" % in `INSIGHT_BANK.md` |

## Fable + Sonnet seats
The scripts cannot call them. The live Claude session runs them as **blind subagents**: a fresh agent each,
given ONLY `HUNT_PROMPT.md` (judges: ONLY `JUDGE_PROMPT.md`), no repo context, no other seat's work.
Save as `hunt_fable.md` / `hunt_sonnet.md` (judges: `judge_fable.md` / `judge_sonnet.md`).
A session that has seen our own candidate angle is not blind - it must not write a seat itself.

## Bars (median of 5+ judges)
FRESH 7.0+ (6.0-6.9 = "classic", max 1 in 4 films) - TRUE 8.0+ - SOUND all PASS - CLEAR 7.0+ - JESUS 8.0+ - GROWTH 7.0+ (Driver 2) - DEPTH 7.0+ - valid ANCHORs in 2 books - CONTEXT PASS x2 - one non-Claude judge at FRESH+DEPTH bars. `gate.py` enforces all of these; nothing is waived.
Seed viewers decide (before publish): 60%+ "had not seen this".

## Notes
- Seats run in a temp folder outside the repo, so no CLAUDE.md or drafts leak in.
- `run_seats.py <topic> grok` re-runs one seat. Grok often times out: note it, do not block.
- `kjv_pack.py` rewrites `KJV_PACK.md` each run: give it the full list of refs every time.
- CLI calls go through `_cli.py`, which uses this repo's `independent_review.py` (plan logins, no metered keys).
  Timeouts are doubled (`REVIEW_TIMEOUT_MULT=2`); set the env var to change.
- `check_quotes.py` only sees `Book C:V "quote"` on one line. Text in `<!-- -->` in a brief is not sent.
- KJV logic lives once, in `prophecy\01_bethlehem\fresh_hunt\kjv_check.py` (loaded by `_kjv.py`).
- $0: CLI plan usage only. No paid API, no pictures, no voice.
