# Red-team triage — v3.1 -> v3.2

2026-11-15. Every BLOCKER and MAJOR from the four blind seats (`fable.md`, `spend.md`, `quality.md`, `codex.md` in this folder).
"Design" = `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\_swirls_short_design\SWIRLS_SHORT_PIPELINE_DESIGN_v3.md` (v3.2).

**Read this first:** "FIXED" here means **fixed in the design**. None of it is built. A row is only done when its test (T-number) passes; the design's section 6 tracks that.

| Count | |
|---|---|
| Items triaged | 68 (19 BLOCKER, 49 MAJOR) |
| Fixed in the design | 61 |
| Partly fixed (rest deferred or out of lane) | 7 |
| Rejected outright | 0 (one sub-point rejected: fable R5, see below) |

---

## fable.md (5 BLOCKER, 18 MAJOR)

| ID | Sev | Finding | Outcome | Where / test |
|---|---|---|---|---|
| M1 | B | Owner asked "about X", cap recorded up to 63% higher | FIXED: page says "about X, at most Y"; `approve --cap` must equal the quote's `at_most`; note must contain it | s3 rules, s5.4; T6 |
| D1 | B | KJV gate passes spliced quotes | FIXED: in-lane G1k wrapper (no ellipsis, whole-word continuous run, case-sensitive), never overridable | s3 step 1; T5. Shared fix = coordinator task 2 |
| M2 | B | Forced alignment echoes the transcript; stale audio passes | FIXED: `RUN voice` deletes `_turns\` on a text-hash change; G2w local whisper check of the audio against `units.json` | s3 step 2; T6b, T10b |
| F1 | B | One wrong letter in a caption is a WARN | FIXED: any wording difference = FAIL; cleared only by a recorded `read` bound to the file | s3 step 5; T7 |
| R1 | B | Word budget fails the pilot's own estimate | FIXED: pause counted only before a voiced quote; 5 quotes at most, 1 per page; one voiced answer on f02 | s1; brief s7; T4 |
| M3 | M | Still rendered outside the marker and copied in | FIXED: G14s — every still / ref needs a confirmed receipt | s3 step 5; T7 |
| M4 | M | Killed process leaves a live request | FIXED: heartbeat + `not_after` + start-up sweep; background by rule; `fetch` records the output hash | s5.1; T6 |
| M5 | M | Timeout during a render: void + retry pays twice | FIXED: claim-or-cancel; claimed = `LATE_PENDING`, never voidable; void needs a saved list dump | s5.1, s5.3; T6 |
| M6 | M | Two sessions service one request | FIXED: atomic rename claim; separate guarded folder | s5.1, s5.2; T6 |
| M7 | M | UNRESOLVED rows do not block their own step; no stated cost | FIXED: one open row per episode, any step; counted at 110% | s5.3; T6 |
| M8 | M | ElevenLabs can be run outside `paid` | FIXED in lane: fixed commands, score script refuses direct runs, `build()` refuses a marked folder. `per_turn_synth.py` by hand = out of lane | s5.5; T6b; coordinator task 4 |
| M9 | M | Approvals never expire; not bound to the quote | FIXED: grants carry the quote hash and die at the step's closing gate | s5.4; T6 |
| F2 | M | Hold gate passes a frozen clip, fails a live one | FIXED: absolute floor vs a frozen control, three 1 s windows, final file | s3 step 6 (G15h); T8 |
| F3 | M | Baked caption melting in the clip | FIXED: G13 re-reads planned strings on first / middle / last frame | s3 step 6; T7b |
| F4 | M | Animated motif has no flag | FIXED: `ink_changed` hard flag | s3 step 6; T7b |
| F5 | M | Strip tiles too small | FIXED: 540 px tiles, 6 per strip | s3 step 6; T7b |
| F6 | M | Blue motif on a blue river | FIXED: page rule 8; brief moves the stroke to dry ground / the scroll / gold-led | s4; brief s3 |
| D2 | M | "Three guesses, three noes" is not the text | FIXED in the brief: one question, an unprompted denial, then two guesses; no narrator "Are you the Christ?" | brief s2, s3, s7 |
| D3 | M | Isaiah's and John's KJV words differ | FIXED in the brief: "Isaiah wrote of a voice crying in the wilderness"; never "the same words" | brief s2, s5, s7 |
| D6 | M | Back cover figure reads as John | FIXED: page rule 7; brief back cover = Jesus larger, three-quarter, series-ref clothing | s4; brief s3 |
| R2 | M | One take at 0.65 ignores the owner rule | FIXED: character lines 0.3, two takes, cues; narrator 0.65 | s3 step 2 |
| R3 | M | 8 pages, 14+ answers | PARTLY: 4 money asks, 7 pages; title round folded into the writers' hand-back; plan check cut to 3 seats. Kept the page-3 and page-5 look stops (they are what makes one priced yes safe) | s3 table |
| R5 | M | Go / no-go comes late | PARTLY: first go / no-go moved to page 3 (the first paid picture, held for its slot on a phone). **Sub-point rejected:** buying that page before the guard is built — no money before the guard exists | s3 step 4; s7 |

## spend.md (5 BLOCKER, 11 MAJOR)

| ID | Sev | Finding | Outcome | Where / test |
|---|---|---|---|---|
| B1 | B | Double servicing | FIXED: claim by atomic rename | s5.2 rule 0; T6 |
| B2 | B | Cancel does not stop an in-flight render; late file used as free | FIXED: claim-or-cancel, `submitted.json` with `creation_id`, staging download, `LATE_PENDING` | s5.1-5.3; T6 |
| B3 | B | `SWIRLS_GEN_PROVIDER=hf` spends with no guard | FIXED: runner + the four render functions refuse non-OpenArt for a marked folder | s3 prerequisites, s9.1; T6 |
| B4 | B | Every `assemble` pays for alignment, unlogged | FIXED: assemble hook -> `build_from_cache`; `build()` refuses a marked folder | s3 step 9, s9.1; T10 |
| B5 | B | Request with no expiry after the client dies | FIXED: `not_after`, heartbeat, `finally:` cancel, start-up sweep | s5.1; T6 |
| M1 | M | "About X" vs cap | FIXED (same as fable M1) | s5.4; T6 |
| M2 | M | Caps too small for their own rerolls under the 110% rule | FIXED: `at_most = ceil((quote + rerolls) x 1.10)`; sums tested | s5.4, s8; T6 |
| M3 | M | Tariff fallback does not catch sound-on | FIXED: `sent_params` and credits read back from `openart_creation_show`, dump saved; else UNRESOLVED | s5.2 rule 5; T6; probe R1 |
| M4 | M | Same-step races; rows merge | FIXED: lock file, uuid rid, one open row | s5.3; T6 |
| M5 | M | Re-approval re-grants the whole step | FIXED: append-only grants; a unit grant adds renders for that unit only | s5.4; T6 |
| M6 | M | Old-protocol servicers answer guarded requests | FIXED: `gen_requests_guarded\` | s5.1; coordinator task 3 |
| M7 | M | Billed creation, failed download, pay again | FIXED: error replies carry `creation_id`; `RUN fetch` | s5.2 rule 6, s5.3; T6 |
| M8 | M | Marker guard fail-open on location | FIXED: runner refuses a trim episode with no marker; `out_path` must be under the episode; G14s | s3 step 0, s5.3; T6 |
| M9 | M | ElevenLabs price / command / receipt all typed | FIXED in lane: fixed commands, character-count price, auto-delete `_turns`. History receipt = probe R3 (unverified) | s5.5; T6b |
| M10 | M | `confirm --amount` clears a row with any number | FIXED: OpenArt rows need `creation_id` + record dump; over-price locks the step | s5.3; T6 |
| M11 | M | Direct MCP calls undetected | FIXED as far as possible: `RUN reconcile` (detective only; stated limit) | s5.6; T6 |

## quality.md (5 BLOCKER, 9 MAJOR)

| ID | Sev | Finding | Outcome | Where / test |
|---|---|---|---|---|
| B1 | B | Dash, quotes, short labels pass; WARN = pass | FIXED: judge on raw strings; open WARNs listed on every owner page | s3 step 5, s3 rules; T7 |
| B2 | B | `page_plan` schema vs code: three gates vacuous | FIXED: one schema, validated on load; `speaker` derived | s3 step 3; T4b |
| B3 | B | Fixed PNG ships the old MP4 (3 holes) | FIXED: fresh-mp4 rule, G14 over `MANIFEST.units[*].src`, receipts through SFX to `FINAL_VIDEO.txt` | s3 steps 6, 7, 9; T7, T12 |
| B4 | B | Frozen / settled hold passes | FIXED: G15h; back clip + 2 s in code | s1, s3 step 6; T3b, T8 |
| B5 | B | Cover border has no automatic check | FIXED: `edge_scan` wired, FAIL on covers | s3 step 5; T9 |
| M1 | M | Bubbles, lips, invented motion | PARTLY: verb list widened, speaker derived, 540 px frames, "still thing moves" hard flag, speaking clips played. **Deferred:** mouth-region pixel check | s3 steps 3, 6; s9.4 |
| M2 | M | No cross-page consistency check | PARTLY: contact sheet + one WARN read on page 4; refs must be sent (G7c). **Deferred:** as a FAIL | s3 step 5; s9.4 |
| M3 | M | Motif presence / dosage unchecked; ink animated | FIXED: `motif_marks` vs stage; `ink_changed` | s3 steps 5, 6; T7, T7b |
| M4 | M | Readability judged on stills; caption under the Shorts UI | FIXED: G13 re-read; 75% / right-15% rule; page 6 is the reading check | s2, s3 |
| M5 | M | Wrong word / page order | FIXED: G1s sequence, G8t order, G4 run checks | s3; T4, T4b, T5b |
| M6 | M | Score dead air passes | FIXED: G17 on the score and the mix. Under-voice ratio stays WARN (deferred as FAIL) | s3 step 8; T14 |
| M7 | M | Robotic character voices | FIXED (same as fable R2) | s3 step 2 |
| M8 | M | Overrides per gate name | FIXED: gate + unit + file hash + dated owner quote; five gates never overridable | s5.6; T7c |
| M9 | M | Can ship at 720p | FIXED: trim must declare 1080x1920; G15 checks the output | s1, s3 step 7; T1 |

## codex.md (4 BLOCKER, 11 MAJOR)

| # | Sev | Finding | Outcome | Where / test |
|---|---|---|---|---|
| 1 | B | The worker can manufacture the owner's priced yes | PARTLY: cap must equal the quote shown; note must carry the number and differ from any look note; stated plainly as a limit. **Out of lane:** an approval the session cannot type | s5 intro, s5.4; coordinator task 1 |
| 2 | B | ElevenLabs caps do not constrain purchases | PARTLY: fixed commands, price from the turns to be rendered, `align` once per audio hash. **Out of lane:** per-request reservation inside `per_turn_synth.py` | s5.5; T6b; coordinator task 4 |
| 3 | B | "$0" operations can spend (SRT, metered Vision) | FIXED: cache-only SRT; runner refuses metered Vision mode | s3 prerequisites, step 9; T6b, T10 |
| 4 | B | KJV verifier accepts a reversal | FIXED (same as fable D1) | T5 |
| 5 | M | Guard depends on where the output is saved | PARTLY: receipts required for every still / clip; runner refusals; `reconcile`. A direct MCP call is still rule-only | s5; T6, T7 |
| 6 | M | Cancellation / duplicate dispatch | FIXED (spend B1, B2) | T6 |
| 7 | M | Draft approval not bound to the draft | FIXED: `ok draft_cut` stores the `assembly_receipt` hash (inputs + output) | s3 step 7; T12 |
| 8 | M | Overrides can neutralise essential gates | FIXED (quality M8) | T7c |
| 9 | M | "I am" for "I am not" is a WARN | FIXED (fable F1) | T7 |
| 10 | M | Hold formula accepts 0 >= 0 | FIXED (G15h) | T8 |
| 11 | M | Writer packet attributes John's wording to Isaiah | FIXED in the brief | brief s7 |
| 12 | M | Strongest Christology missing from the writer packet | FIXED: three must-say truths in the packet and in the judge table | brief s7 |
| 13 | M | Refs declared but not used | FIXED: schema; G7c ref hashes in the payload | s3 steps 3, 4; T4b |
| 14 | M | Hand-fixed pilot hides episode-2 breaks in score / SFX copies | FIXED for the pilot: copies read inputs from `assembly_receipt.json`; T14 runs them. Shared tools still deferred | s3 steps 8, 9; T14; s9.4 |
| 15 | M | Film panel has no pass mark | FIXED: who / what / why right in every seat, no open Bible complaint, median curiosity 7+; else NOT PASSED | s3 step 10 |

---

## The 7 "partly" rows, in one place

| Item | What is left | Owner of what is left |
|---|---|---|
| fable R3 (owner burden) | 7 pages remain | design choice; revisit after the pilot |
| fable R5 (late go / no-go) | page 3 still needs phases A-C | by design (no money before the guard) |
| quality M1 (lips) | mouth-region pixel check | deferred, s9.4 |
| quality M2 (drift) | cross-page FAIL | deferred, s9.4 |
| codex 1 (manufactured yes) | owner-only approval | coordinator task 1 |
| codex 2 (ElevenLabs caps) | per-request reservation in the synth | coordinator task 4 |
| codex 5 (location) | direct MCP calls | rule + `reconcile`; no technical stop exists in lane |

## MINOR items taken anyway

fable: D4 (case-sensitive KJV; narrator says "God" once), D5 (no pointing on f04), D7 (John 1:29 no longer split over the last cut), D8 (brief cites the pinned corpus), F7 (undeclared crowd = FAIL), F12 (fps recorded), M10 (poster folder inside the episode).
spend: m1 (reroll count per kind + unit), m2 (price keyed on mode + aspect, else refuse), m3 (ref hashes in the request), m7 (`episode_id` in the marker).
quality: m1 (one-frame A/V tolerance), m4 (bare-skin hard flag), m6 (fps), m7 (WARN list on owner pages).
codex: 16 (cap sums fit).

MINOR items deferred: hard-prop shape check, silence check at cuts, SFX ear gate as its own stop (folded into page 7), log hash chain, hashes printed on owner pages, Windows cancel tombstone.
