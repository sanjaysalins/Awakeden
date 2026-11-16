# RED TEAM — Swirls Short pipeline v3.1 + SKILL_v3 + pilot brief (Fable seat, blind)

2026-11-15. $0, read-only. Read: the three target files, `test_the_cross\openart_bridge.py`,
`pipeline\score_mix.py`, `pipeline\kjv_strict.py`, `pipeline\assembly_align.py` (grep),
`swirls_short.py` / `swirls_episode.py` / `swirls_assemble.py` (grep), `AGENT_BRIDGE.md` (grep),
ep16 `generate_score_piano.py` (grep). Not read: any `_review*`, `_independent_review*`, other `_redteam*`, `OWNER_SUMMARY`.

Two things were RUN ($0): `kjv_strict.verify_span` on the pilot's quote runs, and `verse_texts` on the 8 verses.
Everything else is from reading. Section 6 of the design says most of the guard is DESIGNED, not built, so
"does the gate stop it" below means "would it, if built exactly as written".

Format per attack: **Setup -> What happens -> Gate that should stop it -> Does it really.**

---

## 1. Money without the owner's own priced yes

### M1. The owner says yes to one price; the agent records a bigger one  (BLOCKER)
- Setup: owner page 4 asks "2 test clips, about 595 cr — yes?" (design s3 table). Owner: yes.
- What happens: the agent types `approve clip_test --cap 945`. Same on every step: 160 asked / 240 cap,
  280 / 520, 1,330 / 2,170, $0.35 / $0.60, $1.00 / $1.50 (s8). Pilot: owner hears $6.08, guard allows $9.85 (+62%).
  The extra is rerolls bought with no new ask.
- Gate: SWS-G0 cap.
- Really? No. The guard enforces the cap, and nothing ties the cap to the number on the owner page (s5.4:
  the note is free text). The house rule is "own explicit ask with a quoted price". The owner never saw 945.

### M2. Forced alignment cannot see stale audio -> wrong words bought and cut to  (BLOCKER, also a bad-film path)
- Setup: one word changes after a first synth. `_turns\` is not deleted (it is a prose rule, s3 step 2; known
  trap in memory `feedback_per_turn_synth_stale_cache`).
- What happens: `per_turn_synth` reuses the old-text turn. `align` is FORCED alignment: it is fed the
  transcript of `narration-tagged.md` (`assembly_align.py:49`) and returns exactly those words with times.
  So the "fourth list" in SWS-G1s (s3 step 3) is the transcript echoed back. It always matches.
- Gate: SWS-G1s, alignment meta gate.
- Really? No. The meta gate binds alignment to the mp3 hash, not the mp3 to the words. The only catch is the
  owner's ear on an 85-word read. Then clips are bought against that timing.

### M3. Stills rendered outside the guard walk straight in  (MAJOR)
- Setup: a one-off script calls `submit()` with `out_path` in the scratchpad or `REPO\openart\` (both legal
  lanes, no marker), then copies the PNG into the episode.
- What happens: unguarded 40 cr each, no row, no cap. `verify` (G9) audits it and writes a sidecar.
  `animate` only needs "G9 passed on the current PNG" (s3 step 6).
- Gate: SWS-G14 provenance.
- Really? Only for clips. G14 reads "clip sha = its row's output; row's input = current still". No gate says
  the still itself has a confirmed row. Step 5's "a hand-edited PNG no longer matches its receipt hash and is
  refused" has no gate behind it in the table.

### M4. Hard kill, not a timeout: request stays live, gets paid, then paid again  (MAJOR)
- Setup: `RUN animate f02` blocks up to 3600 s (`openart_bridge.py:33`). The attending session is also the
  servicer. Run in the foreground it cannot service itself; the Bash tool kills it at 600 s. Or the terminal
  closes, or the PC sleeps.
- What happens: no `except` runs on a process kill, so the request never moves to `cancelled\` (s5.1 covers
  "timeout or any error" only). The row is `requested`. The session then sees a valid request with a `rid`,
  services it, pays 245 cr, writes a reply nobody reads. `confirm --amount` closes the row, but nothing sets
  `output_sha256` on that path, so G14 fails the paid clip -> a second render of the same unit.
- Gate: cancelled-first rule; open-row block.
- Really? No for the kill path. Yes, it blocks other steps; no, it does not stop the paid orphan.

### M5. Timeout while Kling is already rendering -> void + retry = paid twice  (MAJOR)
- Setup: the servicer has already called generate (a 10 s clip takes minutes). Client times out.
- What happens: the file moves to `cancelled\`; the generation still completes and bills; the late reply is
  "ignored and logged". The servicer may still download to `out_path`. `confirm --void` needs a note that
  "names the check made in OpenArt's history" (s5.3) — typed by the same agent, verified by nothing.
  Void -> retry -> second charge. A late download can also overwrite the retry's file after its hash was taken.
- Gate: void rule.
- Really? Half. It is a prose promise. No code reads OpenArt history.

### M6. Two sessions service the same request  (MAJOR)
- Setup: a second Claude Code session in this repo is watching `gen_requests\` (the owner has run 5 parallel
  sessions; memory `feedback_single_agent_per_shared_resource`).
- What happens: `AGENT_BRIDGE.md` has no claim / lock step for gen requests (grep: none). Both read the file,
  both call generate. One reply wins. Two charges, one receipt. A session following `AGENT_BRIDGE.md`
  (not edited by this build, s12 item 1) sends no `creation_id` -> row UNRESOLVED after the money is gone.
- Gate: servicer rule 1-5.
- Really? No. Fix is an atomic rename of the request into `claimed\<session>` before any MCP call.

### M7. UNRESOLVED rows do not block their own step and have no stated cost  (MAJOR)
- Setup: a clip reply comes back with a mismatch -> UNRESOLVED.
- What happens: s5.3 says an open row "blocks every paid command of every OTHER step". Inside step 6b the next
  `animate` goes on. `spent + 1.10 x price` — what an UNRESOLVED row counts as is not written. If 0, the cap leaks.
- Really? Unspecified = not stopped.

### M8. ElevenLabs has no boundary at all  (MAJOR)
- Setup: anyone runs `per_turn_synth.py "<episode>"` or `"<episode>\generate_score_piano.py"` directly.
- What happens: paid. No marker check lives in either script. SKILL rule 4 bans direct calls for OpenArt only.
  `build_srt.build()` is "unchanged" (s9.1) and still reaches `align()`.
- Gate: `RUN paid`.
- Really? No. `RUN paid` is a wrapper you can skip. Cheapest fix: a 6-line `.swirls_short` check at the top of
  the episode's own copied score script, and a rule line in the SKILL naming voice + score.

### M9. Approvals never expire and are not bound to a quote  (MAJOR for episode 2+)
- Setup: step cap has headroom (e.g. 840 cr in `clips`). Days later, or after context compaction, a session
  rerolls "inside the cap".
- What happens: allowed. Expiry was removed (changelog 17). `approve` stores no hash of `unit_timing.json`
  or the quote. Only the per-unit reroll count (3) limits it: 8 units x 2 rerolls is a lot of silent spend.
- Really? No.

### M10. The poster  (MINOR in the pilot, MAJOR when posting)
- The 2-model bake-off writes where its script says. If that is `REPO\openart\...`, no marker, no guard.
  Rule only (s3 step 11).

---

## 2. A bad film that passes every gate

### F1. One wrong letter in the caption is a WARN  (BLOCKER)
- Setup: f06 renders `Behold the Lamp`. Or f02 `I am now`.
- What happens: G9 FAILs "expected text missing", but a fuzzy match 0.6-0.97 is WARN (s3 step 5).
  "Lamp" vs "Lamb" scores about 0.93. So does "the vice" for "the voice".
- Really? Passes. Backstop is the same agent's 2x zoom among a pile of WARNs. On a film whose landing word is
  "Lamb", that is not good enough. Short strings need exact match after normalising, else FAIL.

### F2. Dead clip passes the moving-hold gate; live clip fails it  (MAJOR)
- Setup A: the back clip is frozen from frame 0 (Kling does this on woodcuts). Grain and codec noise give a
  small, equal frame difference all the way. Ratio last 3 s / first 3 s = 1.0 >= R 0.25. PASS (s3 step 6, G15h).
- Setup B: Jesus walks in the first 3 s (big difference), then only reeds and water. Ratio 0.1. FAIL — on a
  hold that is alive. Fix needs "the owner's words" or a 350 cr reroll.
- Really? The gate measures decline, not motion. It needs an absolute floor set on a known-frozen control,
  measured on a masked region (paper excluded).

### F3. Baked text melts in the clip  (MAJOR)
- Setup: Kling softens or re-letters the caption over 7 s (the /animate skill excludes writing scenes for this).
- What happens: G13 hard flags are bubble, NEW legible text, full-figure change. A caption that turns to mush
  is none of those.
- Really? Passes. Re-read the caption on the true last used frame with the G9 text judge.

### F4. The ink motif animates  (MAJOR)
- Setup: Kling makes the blue stroke glow, streak or flow (memory `feedback_ink_motif_animation_unsafe`).
- What happens: prevention is "never named in clips" (G5a). G13 has no motif flag, hard or soft.
- Really? Passes.

### F5. The strip is too small to see what G13 hunts  (MAJOR)
- 2 fps x 8 s = 16+ frames in one image. Tile size is not specified. At a normal contact-sheet size each
  frame is under 300 px wide; a small bubble or a 6-letter invented word is not readable.
- Really? Unspecified = not stopped. State a minimum tile width (>= 540 px) and split strips.

### F6. Pilot-specific: the motif is blue ink in a blue river  (MAJOR)
- f02-f03 put "one thin brushstroke of blue ink along the waterline"; f06/back "blue and gold in the water"
  (brief s3). Vision cannot tell the motif from the watercolor river, so `motif_bad_shape` and the stage-0
  "no unusual ink" pages are unauditable. G6 checks plan numbers, never the render. The series' signature
  device will not read on a phone either.

### F7. Clone hidden as "crowd"  (MINOR)
- A sketchy second John is read as a hatched far figure -> `crowd` differs -> WARN only.

### F8. Hard props have no gate  (MINOR for the pilot, MAJOR for an episode with a cross)
- "Cross drawn as X" is caught only by the human full-frame look (s11 row 8). The pilot has no cross; ep 2 may.

### F9. Dead pages f01-f03  (MINOR)
- Speaker held still, carrier is "the river". If Kling freezes it, only G12 `freezedetect` WARNs. G15h is back-only.

### F10. Cut lands in the silence, not on the word  (MINOR)
- Forced alignment places a word that follows a 0.4 s pause early. G15 checks cut = `B(k)`, i.e. the cut
  against the alignment, not the alignment against the sound. Owner eye only.

### F11. SFX has no ear gate before `film_final`; mix is "measured once" before SFX  (MINOR)

### F12. Frame rate  (MINOR)
- G11 checks size and length, not fps. A 24 fps Kling clip forced to 30 fps duplicates frames. T1 is synthetic.

### Checked and holds
- Cloned hold frames: `swirls_assemble.py:382-390` keeps the picture at `total` and cuts the `mix_tail`
  clone (`score_mix.py:46`) with `-t total`. Sound vs picture length: G15 + `check_landing_hold.py`.

---

## 3. Doctrine / KJV

### D1. The KJV gate passes spliced quotes  (BLOCKER) — RUN, not guessed
`pipeline.kjv_strict.verify_span` splits on `...` and matches fragments in order (`_ordered_in`, kjv_strict.py:171-184):

```
("John 1:20", "I am ... the Christ")   -> OK      (KJV: "I am not the Christ")
("John 1:21", "I am ... that prophet") -> OK
("John 1:20", "am not the Chr")        -> OK      (matches inside words)
("John 1:21", "I am")                  -> OK
```

SWS-G1k = `verify_span` + "appears word for word in the narration". G1s strips punctuation, so the ellipsis
vanishes and John says "I am the Christ" in his own voice with every gate green. The brief's rule 1
("an unbroken run") is enforced by nobody. Fix: G1k must refuse any span containing `...` / `…`, and match on
whole-word token runs.

### D2. "Three guesses, three noes" is not what the text says  (MAJOR)
- Brief s2 Point + f02 + writers' line 3. John 1:19-20: they ask "Who art thou?" and he says "I am not the
  Christ" unprompted ("he confessed, and denied not"). They guess twice: Elias, that prophet (1:21).
- A narrator line "Are you the Christ?" puts a question in their mouths that the KJV does not record here.
- Fix: "One question. Three times he says who he is not." Tell the writers.

### D3. The fulfilment link is not audible  (MAJOR — clarity for a newcomer)
- John (KJV): "the voice of one crying in the wilderness". Isaiah 40:3 (KJV): "The voice of him that crieth
  in the wilderness". Different words. On f05 the narrator reads the OTHER half ("Prepare ye the way of the LORD").
- So the viewer never hears the same line twice, yet is told Isaiah "wrote that line". A writer will be tempted
  to say "Isaiah wrote those exact words" = an over-reach in KJV.
- Fix: brief must say "Isaiah wrote OF a voice crying in the wilderness" (never "the same words"), and f05
  should show/echo "voice ... wilderness", or use Matthew 3:3's wording via the narrator.

### D4. "LORD" vs "Lord"  (MINOR)
- The conviction beat rests on the divine name. By ear they are the same word. `verify_span` is case-blind
  (`("Isaiah 40:3", "Prepare ye the way of the Lord")` -> OK), so a baked caption can carry either casing.
- The claim itself is sound (Isaiah 40:3 also says "a highway for our God"). Let the narrator say "God" plainly
  once; do not hang the turn on capitals.

### D5. f04 invents a pointing gesture a day early  (MINOR)
- John points "away past himself" and the questioners look. Nothing in 1:23. It also spends the f06 payoff.
  Have him open his hands / look down the road instead.

### D6. The film may end on a figure nobody can identify  (MAJOR)
- Front cover: ONE small lone figure from behind (John). Back cover: the same wilderness, ONE small figure
  "walking on" (Jesus). No halo, no glow, woodcut, small. A newcomer reads it as the same man.
- This is the 3 s hold and the landing. Locked rule: every cut closes on Christ, clearly.
- Fix: Jesus larger, facing or three-quarter, in the series-ref clothing; John small and still at the edge,
  pointing. Then "Lamb" has a referent.

### D7. Splitting John 1:29 across f06 -> back  (MINOR)
- Brief s7 allows "which taketh away the sin of the world" in John's voice as the opening of line 8.
  That is a hard cut mid-sentence, an 8-word KJV run plus at most 2 narrator words, and the comma is required
  by the gate (`"Behold the Lamb of God which taketh away..."` -> MISQUOTE, run today). Remove that option.

### D8. Sound and correct (no action)
- All 8 verses in brief s1 match the pinned corpus (run today). All 9 listed runs verify OK.
- "They were of the Pharisees" = 1:24. Bethabara = 1:28. No baptism, no dove, no priests on "the next day":
  all correct. Jesus in the place of the LORD: historic and sound. Landing has no gain / loss pressure.
- But brief s1 says it was "checked against bible-api.com and `data\kjv_cache.json`" — the design's own s0 says
  that cache has a known error. Change the line to "checked against the pinned corpus".

---

## 4. Repeatability and owner burden

### R1. The word budget cannot be met by this pilot  (BLOCKER for step 1)
- Estimate = words / 2.2 + 0.4 x changes of voice, must be 38-42 (s1). The design assumed "about 4 changes".
- The pilot's own shape: f01 2, f02 up to 6 (three John answers), f03 2, f04 2, f06 2 = 10-14 changes = 4.0-5.6 s.
- 88 words -> 44.0-45.6 s FAIL. 80 words -> 40.4-42.0 s, just passes. Real window: about 80-82 words.
  Five blind writers told "80-88 is a hard budget" will mostly fail G1e.
- f02 alone: 12 words + 6 changes = 7.85 s > 7.5 FAIL.
- And the 0.4 is not what the synth does: `--pre-quote-pause 0.4` pads before quotes only; post-quote is 0
  (`per_turn_synth.py:162-165`). The estimator double counts.
- Fix: count only narrator->character changes; give the writers the true window; cap f02 at one voiced answer.

### R2. Voice settings ignore a locked lesson  (MAJOR)
- Memory `feedback_dialogue_needs_emotion_cues`: default lines sounded robotic; fix was stability 0.3 and
  2 takes. The design buys ONE take at `--stability 0.65` (s3 step 2). Likely result: owner rejects at page 2,
  words stay, second buy breaks the $0.60 cap -> another ask.

### R3. Owner stops  (MAJOR)
- 8 owner pages. 6 money asks, each "two separate answers" = 14 answers minimum for a $6 film.
- Plus: G15h override needs the owner's words; a 4th reroll needs a new yes; any still reroll after page 4
  voids `stills_animatic` (hash-bound) and the page is asked again; same for `draft_cut` if one clip changes.
- Plus about 7 panel runs (writers, guardrail x2, title/poster, 5-CLI, plan check, film x2) at up to 10 min a seat.
- For a dyslexic owner on calls this is the real cost, and it repeats every episode.

### R4. Episode 2 breakers
- The installed skill is still the old one (Higgsfield, freeze fill) until the coordinator installs v3 (s12).
- `AGENT_BRIDGE.md` still tells the servicer a quote is fine (s12 item 1). Two rule files that disagree.
- Score and SFX are hand-edited copies of ep16 / ep13 scripts written for 62-106 s films.
- `R` for G15h is tuned on ep10/13/16 back covers: old format, different clip lengths.
- Panel packs and owner pages are built by hand (`page_plan_view`, page builder deferred).
- A less talky story changes the voice-change count and the whole budget moves (R1).
- A story with a cross or a crowd meets F8 and the "no model is clean on crowds" finding with no gate.

### R5. The go / no-go comes late  (MAJOR)
- "Does a 6 s page read on a phone" is the one question that can kill the format. It is asked at page 4,
  after build phases A + B + C (guard, bridge hooks, fake-servicer T6, T12) and four owner pages.
- It can be answered much earlier and cheaper: locked words -> voice ($0.35) -> ONE north-star page (40 cr)
  held for its slot on the phone. Or $0 with scratch stills.

---

## 5. Over-build — what to cut so the pilot ships

Keep: trim-only + frame-exact cuts; scale-and-crop; G1 / G1k (fixed per D1) / G4; one still audit; marker +
cap check; clip receipts by hash; the animatic; the owner's eye.

Cut or defer for the pilot:
1. **4 money asks, not 6.** Voice · pictures (north star first, hard stop, then the rest, one cap) ·
   clips (2 tests first, hard stop, then the rest, one cap) · music. The house rule needs a priced yes for
   recording and for animation; it does not need two asks for stills.
2. **Probe R1 + `credits_source` machinery.** Use "creation id + sent params + tariff" now. Reconcile once
   against the OpenArt history at the end.
3. **T6 fake-servicer thread and the full T12 walk.** Keep a 10-line refusal test per rule. T12 proves
   plumbing only (the design says so).
4. **G15h ratio + T8 calibration.** One absolute floor + the owner's eye on test clip 2.
5. **Hash-bound `ok` gates on the $0 look steps.** Keep hashes only where money follows a file (stills -> clips).
6. **Step 3 blind plan panel**, the title + poster-idea round, SRT, `still ref:` command, G1e per-unit
   estimates (keep the whole-film one), `paid` wrapper for a $1 score (use the marker check from M8).
7. **Step 9 SFX** can ship in the pilot as-is from ep13 or be skipped; it is not what is being tested.

Do first, before any build: fix the word budget (R1), the KJV splice hole (D1), the caption exact-match (F1),
and show the CAP on the owner page (M1). Those four are cheap and each one can sink the pilot.

---

## SEVERITY-RANKED LIST

### BLOCKER
1. **M1 — Owner is asked the clean price, the guard is given a cap up to 63% higher.** Fix: the owner page states the cap ("up to 945 cr"), and `approve --cap` must equal the number on the page (store the page's sha).
2. **D1 — KJV gate passes spliced quotes ("I am ... the Christ" = OK against John 1:20; run today).** Fix: G1k rejects any span with `...`/`…` and matches whole-word token runs only.
3. **M2 — Forced alignment echoes the transcript, so stale audio with old words passes G1s.** Fix: `paid voice` deletes `_turns\` whenever the `narration-tagged.md` hash changed, plus a $0 local whisper word check of the mp3 against `units.json`.
4. **F1 — A one-letter-wrong caption ("Lamp" for "Lamb") is only a WARN (fuzzy 0.6-0.97).** Fix: caption, labels and SEQ need an exact normalised match or FAIL.
5. **R1 — Word budget 80-88 fails the pilot's own estimate gate (10-14 voice changes, not 4); f02 fails alone.** Fix: count only narrator->quote pauses (what the synth really adds), publish the true window, one voiced answer on f02.

### MAJOR
6. **M3 — A still rendered outside the marker and copied in is never checked for a receipt.** Fix: `verify` and `animate` require the PNG sha to equal `output_sha256` of a confirmed row.
7. **M4 — A killed process (Bash 600 s limit, closed terminal) leaves a live request that is paid later, then fails G14 and is bought again.** Fix: run paid commands in the background by rule; servicer refuses a request whose client pid/heartbeat file is dead; `confirm --amount` records the output hash.
8. **M5 — Timeout during a running render: void needs only a typed note, retry pays twice.** Fix: no `--void` without a creation-list dump saved to the row; block retry for that unit until then.
9. **M6 — No claim step: two sessions can service one request.** Fix: atomic rename into `claimed\` before any MCP call; reply refused without the claim.
10. **M7 — UNRESOLVED rows do not block their own step and have no stated cost.** Fix: any open row blocks all paid commands; count it at 1.10 x price.
11. **M8 — ElevenLabs voice / score / old `build_srt.build()` can be run directly, outside `RUN paid`.** Fix: marker check inside the episode's score script; SKILL rule 4 names voice + score; `build()` refuses a marked folder.
12. **M9 — Approvals never expire and are not bound to the quote; cap headroom is a standing blank cheque.** Fix: store the `unit_timing.json` / quote hash in the approval; headroom dies when the step's `ok` gate is recorded.
13. **F2 — Moving-hold ratio passes a clip frozen from frame 0 and fails a live hold after a big early action.** Fix: absolute motion floor on a masked region, set against a frozen control.
14. **F3 — Baked caption melting in the clip trips no flag.** Fix: re-read baked text on the last used frame with the G9 judge; FAIL on mismatch.
15. **F4 — Animated / glowing motif in a clip has no G13 flag.** Fix: add `motif_changed` as a hard flag (first vs last frame).
16. **F5 — 2 fps strip tile size unspecified; defects unreadable.** Fix: tiles >= 540 px wide, split into several strips.
17. **F6 — Pilot puts a blue ink motif on a blue river; cannot be audited or seen.** Fix: move the stroke to dry ground / sky / the scroll, or make it gold-led on river pages.
18. **D2 — "Three guesses, three noes": the text has one unprompted denial and two guesses.** Fix: reword the brief; ban a narrator "Are you the Christ?" question.
19. **D3 — Isaiah's KJV words differ from John's; the film never lets the viewer hear the link.** Fix: say Isaiah wrote "of a voice crying in the wilderness", never "the same words"; echo "voice / wilderness" on f05.
20. **D6 — Back cover = a small lone back-view figure, same as the front cover's John.** Fix: Jesus larger and facing, John small at the edge pointing.
21. **R2 — One take at stability 0.65 ignores the locked "emotion cues, 0.3, two takes" lesson.** Fix: quote and buy two takes for character lines inside the voice cap.
22. **R3 — 8 owner pages, 14+ answers, ~7 panel runs for a $6 film.** Fix: 4 money asks, 5 pages; drop the step-3 plan panel and the title/poster round from the pilot.
23. **R5 — The format's go / no-go waits for phases A-C and four pages.** Fix: one north-star page held for its slot on the phone, right after the voice, before the guard build.

### MINOR
24. M10 poster bake-off can write outside a marker — fix: poster folder must sit inside the episode.
25. F7 clone read as crowd is WARN — fix: FAIL when `crowd` appears and the plan says false.
26. F8 no hard-prop gate (cross as X) — fix: optional `hard_props` list in `page_plan.json`, one Vision yes/no each.
27. F9 dead f01-f03 pages only WARN — fix: same absolute floor as F2 on every clip, WARN -> FAIL on the turn page.
28. F10 cut vs real sound not checked — fix: silence-detect each cut point +-0.15 s, WARN.
29. F11 SFX has no ear gate — fix: fold into page 8 with one line "sounds ok?".
30. F12 clip fps unchecked — fix: G11 records fps; resample with `fps=30` stated.
31. D4 LORD / Lord casing — fix: narrator says "God" once; caption casing checked case-sensitively.
32. D5 f04 pointing a day early — fix: open hands, no point until f06.
33. D7 John 1:29 split over the last cut — fix: remove that option from brief s7.
34. D8 brief cites the bible-api cache as its check — fix: cite the pinned corpus.
35. R4 old skill / `AGENT_BRIDGE.md` still live for episode 2 — fix: coordinator items 1 and 3 before ep 2, not "later".
