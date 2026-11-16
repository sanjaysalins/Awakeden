# HANDOVER / RESUME — Swirls Short pipeline + pilot #17 "Only a Voice"

Stopped 2026-11-15 late (owner: "bring it to a logical point, continue tomorrow"). **$0 spent on all of this. Nothing committed.**

## Where we are (one line)
Pipeline designed (Fable v3.2), red-teamed, BUILT and tested ($0). Pilot words are at version G, waiting on the last narration panel, then ONE owner page to lock the words.

## 1. Pipeline (DONE, $0)
- Design (binding, v3.2): `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\_swirls_short_design\SWIRLS_SHORT_PIPELINE_DESIGN_v3.md`
- New skill text (NOT installed — `.claude\` is coordinator-only): `...\_swirls_short_design\SKILL_v3.md`
- Red team (4 blind seats) + triage: `...\_swirls_short_design\_redteam\` (TRIAGE.md: 68 holes, 61 fixed, 7 part)
- Build report: `...\_swirls_short_design\BUILD_REPORT.md`
- Code (all in lane): `swirls_guard.py`, `swirls_short_run.py`, `swirls_short.py`, `SWIRLS_SHORT_SERVICER.md`, edits to `swirls_episode.py`, `swirls_verify.py`, `swirls_assemble.py`, `build_srt.py`, `test_the_cross\openart_bridge.py`, `swirls_page.py`, `swirls_cover.py`; `_short_templates\`, `fixtures\golden_8unit\`.
- Tests (re-run by me): `_validate_swirls_short.py` 414 checks ALL PASS; `_validate_swirls_assemble.py` ALL PASS; page + hem validators PASS. `_validate_swirls_cover.py` and `_validate_swirls_page_hybrid.py` were ALREADY red at baseline (not caused by this work).
- Owner pages: `...\_swirls_short_design\_DESIGN_READY.html`, `_REDTEAM_RESULT.html`, `_BUILD_DONE.html`
- Last plan panel on v3.2 (`_swirls_short_design\_independent_review\20261115-231254\`): 3 REVISE + gemini FAIL. Convergent: **no money until probes R1-R3 run and `approve` needs the owner's own click**; make the doc match the code. Gemini: servicer steps as real code; fix kjv_strict at the root.

## 2. Pilot #17 words (IN PROGRESS, $0)
Folder: `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_17_voice_in_the_wilderness\` (marker `.swirls_short` made; `status` says NEXT = step 1 words).
Story: Isaiah 40:3 -> John 1:19-29. Brief: `...\_swirls_short_design\PILOT_BRIEF_isaiah40.md`.

History (all in `_words\`):
1. 5 blind writers (fable, claude, codex, cursor, gemini): `blind\seat_*.md` (pack `blind\PACK.md`).
2. Judge table + A/B/C: `JUDGE_TABLE.md`, `CANDIDATES.md`.
3. Blind test r1 (5 seats): `test_r1\` -> C 3 votes, A 2. Fixes -> D/E (`CANDIDATES_R2.md`).
4. Blind test r2 (5 fresh seats): `test_r2\` -> E 4-1. Scores flat ~7/8/7 -> stop testing.
5. F (`FINAL_WORDS_F.md`): Fable seat PASS; 5-CLI panel all REVISE (landing was a bare statement, hook generic, Elijah/Prophet confusing).
6. **G (`FINAL_WORDS_G.md`) = current.** Fable fresh seat (`_review_fable_seat_G.md`): REVISE, small, pick G1:
   - line 7 "Jesus comes." -> "John sees Jesus come:" (newcomer may think Jesus says "Behold")
   - line 8 "Behold him." -> "Look to him."
   - pay words: line 4 "Two more guesses. No, twice. They need an answer."; line 3 drop "first"; line 6 "its cry" -> "the cry"
   - time risk: slow cues on 6-7 may push speech to 43-45 s.
7. **5-CLI narration panel on G finished: all 5 REVISE** (`_words\_independent_review\20261115-234719\`). No doctrine error. Convergent fixes for H:
   - **Landing (5/5):** "Behold him" = old load-bearing word; "Look to him" is a stock closer (gemini). Build an invitation from John's own act of pointing + voice + Lamb/takes away sin, in plain words a stranger knows; must not fit any other short.
   - **Hook (5/5):** must work with zero Bible knowledge (who John is / what "promised one" means). Claude: put the spoken irony "only a voice" in the audio.
   - **Line 4 (4/5):** "two great names. No, twice." is a riddle — say plainly what happened.
   - **Line 6 (3/5):** "God comes" must not sound like part of Isaiah's quote; "its cry" can mean weeping.
   - **Line 7 timeline (cursor, grok + Fable seat):** say "the next day" / name John as speaker so Jesus doesn't seem to enter the priest scene.
   - **Time (claude, Fable seat):** slow cues push 88 words over 42 s — likely cut to ~82.
   - Grok: link "the Christ" = "the promised one" by ear.

## 3. Resume tomorrow — do this in order
1. Read the G panel: newest folder in `_words\_independent_review\`. Fold fixes where 2+ seats agree (plus Fable's 5 above) -> `FINAL_WORDS_H.md`. Recount words, KJV-check each quote: `swirls_short.kjv_run_found(ref, text)`. Check time; line 7 rule was "<=2 narrator words before the whole 13-word speech" — Fable's fix makes it 4; decide (owner) or use the 5-word run + plain words.
2. One owner HTML page: before/after scores, the final 8 lines, still-weak list, ONE pick. **A pick locks WORDS + TITLE only.** Recommend real seed viewers on lines 7-8.
3. Before ANY money (voice is the next paid step):
   - run $0 probes R1 (OpenArt creation record fields), R2 (ElevenLabs alignment permission), R3 (ElevenLabs history);
   - owner OK for the settings `ask` rule so `approve` needs the owner's own click (coordinator task);
   - real ElevenLabs rates (placeholders are UNVERIFIED);
   - then ask the voice price as "about X, at most Y — yes?".

## 4. Coordinator tasks (out of lane — not ours to edit)
1. Settings `ask` rule so `swirls_episode.py ... approve` needs the owner's click.
2. Fix `pipeline\kjv_strict.verify_span`: `verify_span('John 1:20','I am ... the Christ')` returns OK (ellipsis splice reverses the verse) — affects the whole project. Verified 2026-11-15.
3. `AGENT_BRIDGE.md`: point guarded requests at `SWIRLS_SHORT_SERVICER.md`; no quote/balance-diff receipts; claim step.
4. `per_turn_synth.py`: per-speaker stability, marker check, cache by text hash.
5. Install `SKILL_v3.md` into `.claude\skills\swirls-of-life\` after review.
6. Check `release_check.py` on a POC episode before first post.
7. Later: move the OpenArt bridge out of `test_the_cross\`.

## 5. Also still open from earlier
- Website deploy + `release_check.py` after the 2026-11-15 upload batch (could-ye-not-watch-one-hour, why-did-she-leave-her-jar) — owner never answered.
