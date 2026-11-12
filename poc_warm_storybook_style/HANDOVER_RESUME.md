# HANDOVER / RESUME: Warm Storybook POC, "Mary and Martha" (Luke 10:38-42 + John 11:5)

Stopped 2026-11-11 night at a clean point. Nothing running. Owner said: "close for the night, pick up tomorrow".

## 2026-11-12 UPDATE
- Redraws DONE ($0.24, ledgered): stills/s03_v2.png, s14_v2.png, s15_v2.png (old kept). Curtain instead of door
  (no metal); s14 Jesus face now matches s06. My QC: OK. Page: _REDRAWS.html. Job ids in stills/_jobs.txt.
- Owner OK'd pictures + clips (yes). 15 Kling v3 pro clips DONE (~$6.86 ledgered): clips/s01-s15.mp4,
  ids in clips/_jobs.txt, QC sheets _qc/clips/. Page _CLIPS.html.
- s13 BAD: cartoon breath-cloud puff ~0.5-4.5 s (slot is 4.8 s, can't trim around it). Redo ~$0.42 needs a yes;
  new prompt must NOT say "breath out" (remove the noun/verb, per kling-negative-clauses memory).
- s12 minor: Mary teary in background. Usable.
- s13 REDONE (owner yes, $0.42 ledgered, no breath wording): clean. Old kept as clips/s13_old_puff.mp4.
- Preview film BUILT ($0): MARY_MARTHA_PREVIEW_v1.mp4, 85.2 s, voice only, 15 hard cuts at 1.0x, 3 s hold,
  audio/video match (0.1 s). Script: build.py (gentle: run via PowerShell Start-Process BelowNormal).
- NEXT: owner watches -> music quote (~$2.50, 2-part felt piano like ep16) -> needs a yes.

## FIRST THING TOMORROW (old, 2026-11-11)
Owner has NOT yet answered: **redraw 3 pictures for ~$0.25?** (s03 door, s14 Jesus face, s15 door).
Ask again in one line. Do not spend until a fresh explicit yes.
Owner review page: file:///F:/slk/PycharmProjects/JesusInTheBible/poc_warm_storybook_style/_PICTURES.html

## Owner rules for this POC
- "Replicate this exact style" = the owner's 3 refs in `refs/` (from Downloads). Style written in `STYLE.md`.
- "Maintain consistency of character and era and setting" -> `CONSISTENCY.md` (3 people + Lazarus, one house,
  1st-century Judea, NEVER-draw list: no modern door handles/locks, switches, mugs with handles, ghost people).
- Every paid step = its own quoted price + explicit yes (praise/lock is not a spend order).
- Gentle mode ON (state file = 3): one bg job, one agent at a time, BelowNormal, ffmpeg -threads 3.

## Done (spent ~$1.61, all in data/spend_ledger.jsonl, episode "poc_warm_storybook_mary_martha")
1. Style test: 3 stills `test/t1-t3` ($0.24). t2 (Mary at His feet) = NORTH STAR.
2. Words LOCKED (owner "yes"): `narration.md` = candidate D (179 words). Process in `words_blind/`:
   5 blind writers (Fable, Opus, Claude, Codex, Grok) -> 3 converged on "dost thou not care" -> "Martha, Martha"
   -> John 11:5 -> candidates A/B -> blind test r1 (B won 4/4) -> C -> fresh blind test r2 (7.5-8/10, small
   fixes) -> D. Table + history: `words_blind/candidates.md`. Pick page `_PICK_WORDS.html`.
3. Voice LOCKED (owner "lock it"): `narration.mp3` 82.13 s natural 1.0x ($0.25). `voices.json`: narrator
   LSi9zNCeliLuhIGGS0By, jesus UzI1NsMEV3ni5JRkRSls (both = ep16), martha NbkKnEAZ7Bqw4EAkVEaz (= Jesus Wept Martha).
   `narration-tagged.md` drives per_turn_synth. Alignment `narration.alignment.json` (whisperx, `_align.py`).
   Listen page `_LISTEN_VOICE.html`. Last 0.3 s: add tail fade at build (ep12 click lesson).
4. Picture plan `PICTURE_PLAN.md`: 15 shots, slots from word timings, film = 82.13 + 3.0 s hold = ~85.1 s.
5. Stills ($1.12): `stills/s01-s15.png` (s04 = test t2 reused). Job + OpenArt resource ids in `stills/_jobs.txt`.
   QC sheets in `_qc/`. 12 OK. 3 FIX:
   - s03: modern metal lever handle + lock plate on the door -> redraw as doorway with a woven cloth curtain
     (or plain plank door with a wooden peg, NO metal).
   - s15: metal D-handle on door (left) -> same curtain fix; keep everything else (it's the landing shot).
   - s14: Jesus' face drifted to owner ref2's lighter auburn Jesus -> redraw with refs s06 (Jesus close,
     resource:ixxp16CGWz4C9sYfgTNa) + t2 (resource:smEdRfAQQa3jB4SrJ9b5) + ref2 for composition only.
   Small, not blocking: Mary/Martha wear sandals in s11 (sheet says barefoot).
   Refs used for all stills: resource:smEdRfAQQa3jB4SrJ9b5 (t2), resource:yZa6WeuKrp60gTTI7cI4 (t1),
   upload:aWt8yGmQieEsMsOkbYlM (ref1). NOTE: OpenArt only used the first 2 refs listed each time.

## Next steps (each paid step needs its own quote + yes)
1. Redraw s03/s14/s15 (~$0.25). QC: zoom every door/prop (modern metal sneaks in), count people, check faces.
2. Owner OKs all 15 pictures.
3. Clips: 15 Kling v3 image2video PRO, sound off (~35cr/s = $0.07/s). Each clip LONGER than its slot
   (no freeze/boomerang/zoom fill, 1.0x hard cuts). ~100 s total -> quote ~$7. OpenArt parallel limit 8
   videos (other sessions share the account) -> submit in 2 waves. QC by frame strips + first/last-frame diff,
   check hand/arm pass-through in s12/s14/s15 (hug/hand-hold clips).
4. Build film (copy ep16 `build_v3.py` pattern): hard cuts on slots, voice, 3.0 s landing hold, tail fade.
5. Music: 2-part felt-piano (ep16 `generate_score_piano.py`, split at the resolution, ~"So, did He care?"
   64.4 s), ~$2.50 quote. Mix like ep16 (duck, -15 dB then lift for the ending, alimiter).
6. Text layer (optional, Remotion like ep16) + global-audience/guardrail blind panel on the FILM.
7. Title + thumbnail as one curiosity unit, packaging gate, publish pack. Posting held (30-episode hold).
   Commit text/code only when asked; never media.

Total so far ~$1.61. Est. remaining ~$10 (redraw 0.25, clips ~7, music ~2.5).

## 2026-11-12 MUSIC
- Owner yes ~$2.50 then yes ~$1.55 more. Spent ~$2.45 (ledgered: score_piano_part1_try1 $0.90, score_piano_retry $1.55).
- Try 1 part 1: E major, silent 0-16.2 s. Try 2 part 1: F major (clashes), silent after 42.9 s. Both in _score_rejected/.
- $0 rescue: _splice_part1.py = try 1's 16.2-31.0 s phrase + try 1 16.2-67.2 s (keys match part 2, E minor).
- generate_score_piano.py -> score_piano.mp3 (85.23 s, sweep clean). mix_score.py -> MARY_MARTHA_SCORED_v1.mp4
  (-11 dB, lift to -6 dB at 64.4-69.3, to 0 dB at 74-78 for the decaying last chord; duck 0.12/2.5/20/250; alimiter).
  Video 85.23 / audio 85.15. Page _LISTEN_SCORE.html. NEXT: owner listens.

## 2026-11-12 TIGHTER WORDS (owner: "ending can be more insightful for a global audience" + "tighter version")
- words_blind_v2/: 5 blind writers (fable, opus, claude depth, codex, claude plain [grok timed out]). tests/: films.json A-F.
- Round 1 (fable/codex): A 7/7, B 8/7, C 7.5/7, D(now) 8/7. Convergent fixes -> E (146 w).
- Round 2 (fresh fable/codex/claude): E 7/7/7, ending 6/6/6: "He gave her what she needed" = slogan. Stop rule (2 rounds).
- F = E + converged ending ("He looked past all her work, and saw her worry"), UNTESTED. Page _PICK_WORDS_V2.html.
- NEXT: owner picks (F / D / one more blind check of F). Voice re-record ~$0.25 needs its own yes.
- Round 3 (owner yes, fresh fable/codex/claude) on F: 7/7/7, ending 7/7/6.5. Convergent: fix "her", cut "Look again", join worry+love.
  -> G (147 w, ~70 s) in tests/films.json, on _PICK_WORDS_V2.html. NEXT: owner picks G -> voice ~$0.25 needs its own yes.
- G LOCKED (owner "go"). voice_v2/: narration.md, narration-tagged.md, narration.mp3 (68.61 s natural 1.0x, ~$0.20 ledgered), alignment.
- build_v2.py -> MARY_MARTHA_PREVIEW_v2.mp4 (71.6 s, all 15 clips, s12/s13 swapped order). fit_score_v2.py ($0, no repeat phrase)
  -> score_piano_v2.mp3. mix_score_v2.py (-11 -> -8 at 50.4-55.4, -> 0 at 62-66, 6 dB dip at 60.1 "Lazarus" chord) -> MARY_MARTHA_SCORED_v2.mp4.
  Page _LISTEN_V2.html. Project total ~$11.78. NEXT: owner watches -> guardrail/global-audience panel on FILM, title+thumb, pack.

## 2026-11-12 MOTION v1 (owner: "better transitions ... great motion graphics and doodles")
- Fable spec motion_v1/MOTION_DESIGN.md (brief motion_v1/BRIEF.md). Built _remotion/src/MaryMarthaV1.tsx (comp MaryMarthaV1,
  clips copied to _remotion/public/mm/, 15 layers, 6 transitions). Swatch opacity .8 (ep16 owner liked see-through), lasso 8 px.
- _remotion/out/mm_motion_v1.mp4 + audio of MARY_MARTHA_SCORED_v2 -> MARY_MARTHA_MOTION_v1.mp4 (71.6 s). QC sheets motion_v1/. Page _MOTION_V1.html. $0.
- NEXT: owner watches -> guardrail/global-audience panel on FILM -> title + thumbnail -> packaging + pack.
- Owner: v1 doodles "very forced ... not complementing". Fable redesign motion_v2/MOTION_DESIGN.md (refs' own vocabulary: pencil lamp,
  gold flame coloured into the art's unlit lamps, gold olive sprig). Built _remotion/src/MaryMarthaV2.tsx (D1 dropped; D4/D5 flames
  tracked to the clip push, measured). -> MARY_MARTHA_MOTION_v2.mp4 (71.6 s). Page _MOTION_V2.html. Risk: may be too subtle on a phone.
- Owner: "Doodles much bigger" (keep v2). MaryMarthaV2.tsx edited: steam curls shots 1-2, kitchen lamp x1.5 darker 4.5 px,
  flames x1.25, family sprig x1.3 top-left deeper gold, ending sprig dropped. -> MARY_MARTHA_MOTION_v3.mp4. Page _MOTION_V2.html (top).
- Owner: "go stronger ... flowers or motifs ... even cutier". Added flowersFor() in MaryMarthaV2.tsx: Vine + Blossom (5 petals,
  blush/honey/cream, terracotta centre, back-ease pop, sway), x1.5 size, 8 shots. -> MARY_MARTHA_MOTION_v4.mp4. Page _MOTION_V4.html. $0.
  NEXT: owner OK -> guardrail/global-audience blind panel on the FILM -> title + thumbnail -> packaging -> pack.
- Owner: "cutier and more fuller" + "do that in all scenes": Vine2 (buds, pollen dots), Butterfly, vines in all 15 shots -> MARY_MARTHA_MOTION_v5.mp4. Page _MOTION_V5.html. $0.
- 2026-11-12 LOCKED (owner "lock it"): MARY_MARTHA_MOTION_v5.mp4. See FILM_LOCK.md.
- Guardrail panel r1 on locked film (guardrail_r1/): Fable 7, Claude-bible 7, Claude-global 7 (grok timeout), Codex 6, newcomer 6. All 5 same take-home. Weak: line 5 (5/5), Lazarus intro (3), 'never' (3). Page _GUARDRAIL_R1.html. Fix needs voice ~$0.25 + retime $0: owner to decide.

## 2026-11-12 WORDS H (owner "yes" to the 3 guardrail_r1 fixes, ~$0.25 quoted)
- voice_v3/: words H = G with line 5 "Mary had chosen the one thing needed: to listen to Him. And He would not send her away.",
  line 6 "...the Bible says this about Martha, Mary and their brother: ...", line 7 "He did not call Martha's work wrong."
  Only turn 04 re-rendered (turns 00-03 copied from voice_v2) -> 70.85 s, ~$0.09 ledgered voice_v3_words_H. Alignment done.
- build_v3.py -> MARY_MARTHA_PREVIEW_v3.mp4 (73.85 s). New cuts 43.10/50.67/56.03 (s14 now enters on "Martha, Mary" - s14 is only 8.04 s)/64.03/66.63.
- fit_score_v3.py: part 2 starts 52.83 s so its warm chord lands on "Now Jesus loved" (57.83); ~2 s hush after "So, did He care?"; sweep clean.
  mix_score_v3.py (lift 52.83-57.83, 0 dB 64.2-68.2, dip 62.5 on "Lazarus") -> MARY_MARTHA_SCORED_v3.mp4.
- _remotion/src/MaryMarthaV3.tsx (copy of V2 = v5 look, retimed; comp MaryMarthaV3, 2216 frames) -> MARY_MARTHA_MOTION_v6.mp4. v5 untouched.
- NEXT: owner watches v6 -> (optional fresh blind re-test) -> title + thumbnail -> packaging gate -> pack. Posting held (30-ep hold).

## 2026-11-12 v6 LOCKED + PUBLISH-READY (owner "Lock v6 and finish the publish step")
- FILM_LOCK.md updated. Piece batches/cluster_04_encounters/mary_martha_short (slug mary-and-martha-did-he-care, manifest entry added): LOCKED.json sha 51c56477...
- Packaging: 3 blind cards (Fable/Opus/Sonnet) -> packaging/PACKAGING_CARD_MERGED.md. YT title "Martha Asked Jesus. He Said Her Name Twice."; FB "Mary and Martha: Did Jesus Care? (Luke 10)"; thumb "DOES ANYONE / EVEN CARE?" on still s05.
- Pack GREEN --strict; red team Fable 7.5 / Opus 7.5 / Sonnet 8, convergent fixes applied (thumb bands, full KJV quote, hook first). release_check GREEN, tracker rebuilt.
- NEXT: owner eyeballs PUBLISH_INDEX.html. Posting held (30-episode hold). Commit text only when asked.

## 2026-11-12 UPLOAD RED TEAM r2 + v7 (owner "please red team the upload details", then "yes" ~$0.10)
- red_team_r2/ (piece folder): Fable 8, Claude 7.5, Codex 7, Grok 6 (all REVISE, no KJV error). Convergent copy fixes applied; page _RED_TEAM_R2.html.
- Film line fix (Codex + Claude): voice_v4 words H2 "And He said it would not be taken away from her." (~$0.09 ledgered voice_v4_words_H2).
- build_v4.py / fit_score_v4.py / mix_score_v4.py / _remotion/src/MaryMarthaV4.tsx -> MARY_MARTHA_MOTION_v7.mp4 (72.97 s). LOCKED (FILM_LOCK.md); piece final swapped, captions rebuilt, pack GREEN --strict, release_check GREEN.
- NEXT: owner eyeballs; commit text only when asked; posting held (30-episode hold).
