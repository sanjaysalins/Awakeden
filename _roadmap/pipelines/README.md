# FOUR PIPELINES — run in parallel, worked on every day

Owner, 2026-11-19: "build pipelines that can run in parallel" + "a 4th one for miscellaneous, POC kind of testing work."
No output targets, no posting schedule. This file is HOW the four lanes run side by side without blocking each other.
History: design + red team in `_roadmap\three_streams\` (SYNTHESIS, REDTEAM_RESULT, PIPELINES.md v2, reviews).

## 1. The four lanes

| Lane | What | Folder (one per item) | Front end | Then |
|---|---|---|---|---|
| **P1 THE THREAD** | OT prophecy fulfilled in Jesus | `threads\tNN_name\` | `hunt_kit` Driver 1 (`gate.py --driver 1`) | shared film line |
| **P2 THE ENCOUNTER** | What Jesus did, through OT + NT | `encounters\eNN_name\` | `hunt_kit` Driver 2 (GROWTH judge) | shared film line |
| **P3 THE DAY** | Life today (and later current events) with a Bible view | `today\dNN_name\` | `today\P3_GATE.md` first, then `hunt_kit` with a P3 brief | shared film line |
| **P4 THE LAB** | POCs, style tests, bake-offs, tool builds, fixes | `poc_<name>\` (existing pattern) | `lab\` rules below | owner decides: graduate, park, or drop |

**Sorting rule (P1-P3):** P1 only when the New Testament itself quotes the OT text or says "fulfilled". P2 starts from something Jesus did; OT links labelled out loud (ECHO / NT-STATED). P3 starts from the viewer's life. Tie -> the lane whose test it passes most strictly (P1 > P2 > P3).

**Spoken = seen (owner, 2026-11-19).** The owner uploads a timed `.srt`; YouTube translates and dubs from it. So **every word or point on screen must also be spoken**: no on-screen-only labels, verse refs, cards or landings. Cards may only repeat what is said. Captions stay a sidecar `.srt`, never burned in. Checked at WORDS (the script lists every on-screen text and the line that speaks it) and at FILM CHECK.

**Every P1-P3 film ends on Jesus + one personal take-away earned from its own verses.** All existing gates stay (KJV checker, fresh-insight rounds, global-audience test, guardrail panel, words-before-money, media rule, packaging rule).

## 2. Shared film line (P1-P3; T13 is the worked example)

```
WORDS -> VOICE -> PICTURES -> CLIPS -> EDIT -> SOUND -> FILM CHECK -> PACKAGING -> RELEASE PACK
```
| Stage | Existing tool / pattern | Paid? |
|---|---|---|
| WORDS | blind writers (Fable + AI panel; each gets the hunt's `WORDS_MUST_FIX.md` if any) -> judge table -> global test -> guardrail panel -> `WORDS_LOCK_<date>.md`, `narration_gate.py` | $0 |
| VOICE | ElevenLabs takes (`threads\t13_job_sea\audio\rebuild.py` pattern) | quote |
| PICTURES | look lock + cast refs, OpenArt NBP, era + clone check | quote |
| CLIPS | Grok Imagine (T13) — **blocked: Grok out of credit** — or the locked HF Kling pro | $0 / quote |
| EDIT | Remotion `comic_kit` (copy per episode; never edit the kit in a lane) | $0 |
| SOUND | score (2-part, 2.5 s end fade) + SFX library + 3 s landing hold | quote (score) |
| FILM CHECK | blind guardrail film panel; captions as sidecar `.srt` | $0 |
| PACKAGING | title round + AGY poster + packaging card -> `MeekAndMighty\_pipeline\check_packaging.js` | $0 |
| RELEASE PACK | `/publish` GREEN + copy red team | $0 |

## 3. How the lanes run in parallel

**One Claude session per lane** (P1, P2, P3, P4), plus **one HUB session**. Five sessions, each with its own job.

**Lanes write ONLY inside their own item folders.** Nothing shared.

**The HUB owns every shared thing** (single agent per shared resource):
- files: `_roadmap\INSIGHT_BANK.md`, `_roadmap\TWO_DRIVERS_ROADMAP.md`, `data\release_ledger.json`, `data\kjv_cache.json`,
  `data\spend_ledger.jsonl`, `F:\slk\PycharmProjects\_media_rules\paid_jobs_log.csv`, `_remotion\src\Root.tsx` + `comic_kit\`,
  `_UPLOAD_TRACKER.html`, the lane board.
- queue: **paid / media jobs** (OpenArt, ElevenLabs, paid clips) — one job at a time, first come first served.
- **CLI panels** (any script that calls the claude/codex/gemini/grok/cursor CLIs: `sunday_school.py`, `run_seats.py`, `run_judges.py`, `context_check.py`, `independent_review.py`) are run BY the lane, but always wrapped:
  `.venv\Scripts\python.exe _roadmap\pipelines\panel_lock.py run P1 -- .venv\Scripts\python.exe <script> ...` — one panel at a time across all lanes.
- **Fable / Sonnet blind seats** are spawned by the HUB (a lane has seen its own angle, so it cannot write a blind seat). The lane asks in `TO_HUB.md` with the path of the prompt file.
- A lane asks the hub by writing `TO_HUB.md` in its own folder (one line per ask: what, why, cost if paid). The hub does it and writes the answer back in that line.

**Every item folder has `STATE.md`** (template: `_roadmap\pipelines\STATE_TEMPLATE.md`). A session resumes from it, never from memory.

**Each lane's daily loop:**
1. Read your `STATE.md` files.
2. Not waiting -> do the next stage, update `STATE.md`.
3. Waiting (owner, hub queue, panel) -> do $0 work: hunt the next idea, prepare the next page, run a $0 check.

**Limits, so lanes don't jam:**
- Per lane: at most **1 item past WORDS** + **1 item in HUNT** at a time. P4: at most 2 open tests.
- Each of P1-P3 keeps **1 proved idea waiting** (a PASS card in the bank), so a failed hunt (~30-40%) never stalls it.
- A panel run without Grok is marked "Grok seat missing" in its file.

**Board:** `.venv\Scripts\python.exe _roadmap\pipelines\status.py` -> reads every `STATE.md` + `_roadmap\pipelines\LANE_QUEUE.md` (hub-owned "up next" list), writes `_roadmap\pipelines\_BOARD.html`: "needs you" first, each lane as a 6-step track, then "how we work". $0.

## 4. P4 THE LAB — rules

- Anything goes: style tests, model bake-offs, tool prototypes, a new device, a pipeline fix.
- Lives in its own `poc_<name>\` folder with a `STATE.md` (`lane: P4`) and a one-line **question** it answers ("Does X beat Y for Z?").
- **Never touches a locked pipeline, a locked film, or a shared file.** Needs one? Ask the hub.
- $0 by default. Paid = quote + owner yes + log, like everything else. Bake-offs follow the media rule.
- Ends with ONE owner page: the answer + a pick: **graduate** (hub folds it into a lane or the film line), **park**, or **drop**.
  A graduated change to a locked model or rule still needs the full bake-off + owner pick.

## 5. Open before the lanes can finish a film
- **Clips:** Grok is out of credit (T13's clips were made through the Grok tool). Top up Grok, or use the locked HF Kling pro (quoted per film). Owner choice.
- **P3 gate:** draft at `today\P3_GATE.md`. Must pass its own panel (Fable + AI panel) before the first P3 hunt. P3 starts with life issues; real events after the gate is proved.
- **Dubbing:** no test needed (owner, 2026-11-19): timed `.srt` + YouTube auto-dub. The "spoken = seen" rule above covers it.
