# Folk Print POC — "The Second Fire" (John 21:1-17) — HANDOVER

## 2026-11-12 NIGHT STOP — RESUME HERE
- **State:** words LOCKED, voice LOCKED (B, 84.89 s), 17 fuller stills DONE, 17 clips DONE, preview v1 BUILT
  (`SECOND_FIRE_PREVIEW_v1.mp4`, 87.9 s, 1080x1920 = 9:16, voice only, no music/SFX). Owner: "this is great".
- **2026-11-13: clip 16 FIXED** (owner yes, $0.42 ledgered, job XpuImcn2AnW79VFkKbSl, no smoke wording). Old clip kept as `clips/s16_v1_smoke.mp4`. Preview v2 `SECOND_FIRE_PREVIEW_v2.mp4` (87.9 s, A/V match). Page `_WATCH_v2.html`.
- **2026-11-13: music DONE** (owner yes; ~$1.33 ledgered): `generate_score_piano.py` (split 53.2 s) -> `score_piano.mp3`, sweep clean; `mix_score.py` (-9 dB part 1, -14 dB part 2, lift 75.2-80.3, hold lift) -> `SECOND_FIRE_SCORED_v1.mp4` (-19.3 LUFS, A/V match). Key match at the join NOT checked by tool (no librosa) - owner ear-check. Page `_LISTEN_SCORE.html`.
- **RESUME FIRST:** ask the owner "Keep this music? Next: film panel ($0)."
- **Then (each its own quote + yes):** music ~$2.50 (2-part felt piano like ep16 `generate_score_piano.py`,
  split at the turn ~"After the meal" 53.2 s; measure duck by numbers) -> film blind panel ($0: global-audience +
  5 guardrail questions, Fable + AI panel, film-only pack) -> title + thumbnail pair -> packaging card + publish pack.
- **Spent on this film:** ~$11.01, all in `data/spend_ledger.jsonl` (episode `poc_folk_print_second_fire`):
  voice $0.26, pictures $3.68, clips $7.07.
- **Gotchas learned:** OpenArt only lists 2 refs per call but results followed all refs; nano-banana-pro kept adding a
  woman/child to group shots - "only these two people" (remove the crowd) fixed it; sun/sunburst behind a head reads as
  a halo - say "sun far off to the side"; OpenArt video parallel limit 8 is shared with other sessions.
- Gentle mode ON (`C:\Users\sanjay\.claude\.gentle-state` = 3). Nothing committed (commit text only, when asked; no media).

Started 2026-11-12. Owner gave style ref `refs/ref_01_teaching_by_sea.jpg` (flat folk-art, orange/teal, grain). Style + era watch-list: `STYLE.md`.
Owner picked the story "Breakfast after failure" (John 21) for an uplifting piece.

## Words (state: LOCKED by owner 2026-11-12 -> narration.md)
- 5 blind writers `words_blind/panel_r1/` (fable_failed, opus_judge, claude_depth, codex_hook, grok_plain) - all 5 built on "a fire of coals".
- Combined A/B `words_blind/candidates.md` -> blind test r1 (`test_r1/`): split 2-2 (A Fable/Claude, B Codex/Grok).
- Merged C/D `words_blind/candidates_r2.md` -> fresh blind test r2 (`test_r2/`): C won 4/4 (7.5/8/7/8).
- Fixed final: `words_blind/FINAL_C2.md` (~194 words, ~75 s). Pick page `_PICK_WORDS.html`.
- Fact verified: exact "fire of coals" occurs only John 18:18 + John 21:9 in the whole KJV (`data/kjv_full` search).
- $0 spent.

## Next (each paid step = its own quote + yes)
1. Owner locks words -> guardrail 5-question panel ($0) -> voice (ElevenLabs, quote ~$0.15; narrator / Jesus / Peter).
2. Character + location refs in the folk style (Jesus, Peter, boat, shore fire) -> shot plan from line timings -> stills -> clips.

## Voice v1 (owner yes, ~$0.26 ledgered, episode "poc_folk_print_second_fire")
- `narration-tagged.md` + `voices.json` (narrator LSi9.., jesus UzI1.. = Mary&Martha voices; peter puDR.. = "Who Do You Say I Am").
- `narration.mp3` 93.95 s natural 1.0x (synth says ~19 s over a 75 s target). `narration_tight_0.45.mp3` 84.9 s = long pauses cut to 0.45 s ($0, ffmpeg silenceremove).
- Listen page `_LISTEN_VOICE.html`. Owner to pick A/B, or trim ~25 words + re-record changed turns (~$0.15, needs its own yes). Mary&Martha precedent: owner ended near 70 s.

## Voice LOCKED = B (owner "B"): `narration.mp3` = tight-pause version 84.89 s (raw 93.95 s kept as `narration_raw_93s.mp3`). Alignment `narration.alignment.json` (194 words, `_align.py`).
## Picture plan: `PICTURE_PLAN.md` (17 stills, slots from alignment, +3 s hold).
## Refs + 3 test stills (owner yes, $0.64 ledgered): `refs/R1-R5*.png` (OpenArt ids in `refs/_ids.txt`), `test/t1-t3` (ids `test/_jobs.txt`). All checked by eye, good.
- t1 = s03 ("I am not"), t2 = s13 (face to face), t3 = s17 (HERO, bread into Peter's hands).
- Review page `_TEST_PICTURES.html`. NEXT: owner yes -> other 14 stills (~$1.12) -> QC (count people, hands, era) -> clips quote (~$7).

## Fuller pictures (owner asked "much fuller" -> picked "busier pictures")
- 2-pic test ($0.16) then all 17 redrawn fuller ($1.36), all ledgered. Files `stills_full/s01-s17.png` (ids `stills_full/_jobs.txt`). Old plain set kept in `stills/`.
- QC: 12 young disciple looks like a child; 13 a woman sorting fish (not in John 21); 14 sun disc behind Peter's head = halo look. 9 = watch (mid-leap, may read as walking on water).
- Page `_PICTURES_FULL.html`. NEXT: owner yes -> redraw 12/13/14 (~$0.24) -> clips quote (~$7).
- Redraws done (ledgered): 12/13/14 ($0.24), then 12/13 again ($0.16): 12 = exactly 7 disciples, 13 = only Jesus+Peter (a woman kept sneaking in), 14 = sun off his head. Old versions kept as s12_v1/v2, s13_v1/v2, s14_v1.
- ALL 17 FULLER STILLS DONE ($3.68 pictures total). Small leftovers: 12 has one distant round-top doorway; 9 mid-leap may read as walking on water.
- NEXT: clips quote ~$7 (17 Kling pro, ~100 s, each longer than slot) -> needs owner yes.

## Clips + preview (2026-11-12 late)
- 17 Kling v3 pro clips, sound off, 101 s (~$7.07 ledgered): `clips/s01-s17.mp4`, ids `clips/_jobs.txt`, QC strips `clips/_qc/`.
- QC: all clean except s16 (big cartoon smoke plume grows into the sky). s09 now clearly dives INTO the water.
- Preview `SECOND_FIRE_PREVIEW_v1.mp4` (87.9 s, A/V match, faststart) via `build.py` ($0). Page `_WATCH_v1.html`.
- NEXT: owner watches -> s16 fix (~$0.42, no smoke wording) -> music quote (~$2.50, felt piano 2-part like ep16) -> film panel -> packaging.

## 2026-11-13 Score v1 judged weak by owner ("we can do a much better score") + "plan for great sfx"
- Blind panel ($0): `score_sfx_panel/` (pack.md, prompts/, panel_r1/ fable/claude/codex/grok/sonnet).
- Convergence: 5/5 three-note motif falling at night -> rising at sunrise; 5/5 split at sunrise ~23.6 s, D minor -> D major;
  4/5 oud + wooden flute/ney + low cello (frame drum after sunrise); 5/5 SAME fire sound at 3 s, 37 s, end; 4/5 rooster ~15 s;
  3/5 splash ~34 s; 4/5 bread tear at the end.
- Page `_SCORE_SFX_PLAN.html`. Ask: make it all (~$1.80: music ~$1.40 + 3 new SFX ~$0.40)? No spend yet.
- 2026-11-13 BUILT (owner yes, ~$1.71 ledgered): `generate_score_v2.py` -> `score_v2/score_v2.mp3` (sweep clean) + `sfx_new/` (rooster/splash/sizzle x2; picked t1 each by envelope).
  `mix_v2.py` -> `SECOND_FIRE_SCORED_v2.mp4` (-13.9 LUFS, peak -1.4, A/V 87.9/87.9). Voice-vs-bed measured 7-25 dB everywhere
  (fixed: bread tear + music lift moved into the hold after 84.7 s; 5 dB music dip 71-76 s; sheep lower). Page `_LISTEN_V2.html`.
- RESUME: ask owner "Keep v2? Next: film panel ($0)."

## 2026-11-13 MOTION v1 (owner: "better transition effect between scenes ... motion graphics ... bolder fuller doodles")
- Brief `motion_v1/BRIEF.md` (+ STILLS_SHEET.jpg). Fable spec `motion_v1/MOTION_DESIGN.md`: art's own shapes only (sparks,
  stars, ray stitches, wave scallops, folk flowers, gulls, fish, steam, woven hem band); 3 count coals (3 go out on the no's,
  light on "Three times, yes"); transitions: ember iris x3 (on the 3 fire sounds), sun-ray pinwheel wipe x3, wave wipe x2, hard x8.
- Build (Sonnet, $0): `_remotion/src/SecondFireV1.tsx` (comp SecondFireV1, DENSITY prop), clips in `_remotion/public/sf/`.
  Outputs: `motion_v1/TEST_d100.mp4` + `TEST_d060.mp4` (20 s, s07-s11), full `SECOND_FIRE_MOTION_v1.mp4`, QC `motion_v1/qc/`.
- 2026-11-13 MOTION v1 BUILT ($0): `SECOND_FIRE_MOTION_v1.mp4` (87.9/87.9 s, -13.9 LUFS). Builder changes vs spec: camera-follow
  (SIFT track) for all doodles, coals 1.4x, many positions moved off faces/boat/sheep (full list in builder report; spec file unchanged).
  Known: ray wipe sweeps over Jesus ~0.5 s; 5->6 wave band passes over boat men's heads a few frames; tests rendered before
  fish 1.45x tweak. Page `_MOTION_V1.html`. RESUME: owner watches; keep full strength or lighter?
- 2026-11-13 MOTION v2 ($0): ray wipe only at sunrise (4->5, 11->12 hard), tongue rings 7 mixed flames. `SECOND_FIRE_MOTION_v2.mp4`
  (87.9 s, -13.9 LUFS). Blind film panel `film_panel_r1/` (fable judge, claude bible, codex hook, grok global, sonnet newcomer):
  scores 7/6.5/7.5/6/7; doctrine sound; 4/5 flag "whole Bible, exact words ... only twice" (KJV-only fact; KJV re-verified: John 18:18 + 21:9 only).
  3/5 want the two-fires mystery in line 1 (not doing: score at ~7 stop point). Page `_FILM_PANEL_R1.html`.
  RESUME: ask "re-record 1 sentence -> 'In the King James Bible, these words appear only twice.' (~$0.10)?"
- 2026-11-13 FACT FIX (owner yes, ~$0.06 ledgered): 1 narrator sentence re-recorded ("In the King James Bible, these words appear
  only twice."), take 2 spliced at 40.30-44.38 s, same length (old voice kept as `narration_v2_wholeBible.mp3`, takes in `voice_fix/`).
  build.py -> PREVIEW_v3, mix_v2.py -> SCORED_v3, + motion video `_remotion/out/sf_motion_v2.mp4` -> `SECOND_FIRE_MOTION_v3.mp4`
  (87.9/87.9 s, -13.9 LUFS). Page `_WATCH_v3.html`. RESUME: ask "lock v3? next title + thumbnail".
  NOTE: narration.alignment.json still has the OLD words for 40.46-44.08 (timings fine); re-run _align.py before captions/srt.

## 2026-11-13 POSTER + MOVIE TITLE bake-off (owner: "thumbnail that looks like a movie poster, several bake offs, movie title")
- R1 blind panel ($0) `poster_r1/` (fable/claude/codex/grok/sonnet): 5/5 top title "The Second Fire"; posters converge on
  A split two fires (s11), B bread in hands (s17) + new-art C two-sided face, D same man twice, E bread to viewer, F three cold coals.
- `poster_r1/poster.py` ($0, Bebas Neue + Oswald, 9:16 + 16:9 side-panel) -> `poster_r1/out/`. Page `_POSTERS_R1.html`.
- RESUME: ask "make C/D/E/F new art, 8 pictures ~$0.65?" then R2 blind judge at phone size.
- 2026-11-13 R1 new art made (~$0.64 ledgered): `poster_r1/art/` C1/C2 D1/D2 E1/E2 F1/F2 (E both = halo look; F2 = 4-5 coals, fail).
  R2 blind phone-size judge `poster_r1/judge_r2/` (fable/opus/sonnet/haiku, shuffled P1-P6, key in `_KEY_do_not_give_to_seats.txt`):
  4/4 #1 = P5 = C_face (two-sided face, C2). Taglines enlarged in poster.py. 3/4: the two fires look the same -> redraw
  left fire = dying fire with 3 dark coals, right = bright coal fire with bread; also chin swirl. Page `_POSTERS_R2.html`.
  RESUME: ask "redraw C, 2 takes ~$0.16?"
- 2026-11-13 POSTER R3 (owner: "not really your creative best ... spend more"; cap ~$4-5 yes): blind key-art panel `poster_r3/panel_r1/`
  (fable/claude/codex/grok, 16 ideas) -> bake-off A 6 ideas x nano-banana-pro vs gpt-image-2 x2 (~$2.09) -> blind judge
  `poster_r3/judge/` (4 seats, shuffled Q01-12): winners burn-through + double exposure (flame-faces out: reads as kiss) ->
  bake-off B refined x3 x2 models (~$1.04). Finalists `poster_r3/final/` (9:16 + 16:9). Page `_POSTERS_FINAL.html`.
  Poster spend total ~$3.77; film total ~$18.30. RESUME: owner picks A/B/C/D (my pick A = burnB_nbp2).
- 2026-11-13 THUMBS PICKED (owner: "B and D both are great" -> yes to B for Shorts, D for wide): `thumbs/SECOND_FIRE_thumb_shorts_9x16.jpg`
  (= burnB_gpt2, "He fed him first.") + `thumbs/SECOND_FIRE_thumb_wide_16x9.jpg` (= doubleB_gpt1, "He carried that night."); alts kept.
  Title: THE SECOND FIRE. RESUME: lock film v3 (`SECOND_FIRE_MOTION_v3.mp4`)? then packaging card + gate + publish pack ($0).
- 2026-11-13 FILM v3 LOCKED (owner yes): FILM_LOCK.md (sha f6568e7d...). narration.md/-tagged.md updated to the KJV line (old kept *.v2_wholeBible.*);
  alignment redone (old kept narration.alignment.v2_wholeBible.json). Piece `batches/cluster_04_encounters/second_fire_short/`
  (slug second-fire-he-fed-him-first): 3 blind packaging cards (fable/opus/sonnet) -> Sonnet builder doing merge + packaging gate +
  publish pack + release_check. RESUME: check builder report, eye-check PUBLISH_INDEX.html, then upload red team (optional, $0).
- 2026-11-13 PACK BUILT ($0): piece second_fire_short, PACKAGING-READY (2 WARN: R03 no "Bible" in title - overridden; R04 hook 49>45),
  cli_publish --strict GREEN, release_check GREEN, hold 3.2 s by ffprobe. YT title A "The Second Fire: Why a Fire Was Waiting for Peter"
  (B "...After Peter Said No Three Times"). Registered in _website/manifest.yaml. CAVEAT: packaging.json discoverability flag set true
  but the hostile discoverability/red-team panel has NOT run (noted in card) -> run it before upload ($0).
  Page: batches/cluster_04_encounters/second_fire_short/publish/PUBLISH_INDEX.html. Nothing committed/uploaded.
- 2026-11-13 UPLOAD RED TEAM r1 (piece red_team_upload/, 5 seats, 5/5 REVISE): applied ($0) title -> "The Second Fire" (5/5 8/10),
  "said no to Jesus" fact fix, tagline "HE SAID NO AT THE FIRST ONE." on both thumbs (v1 kept thumbs/v1/), wide art bigger,
  KJV glosses, spoiler out of description. Pre-fix copies publish/_pre_redteam/. Gate READY (PACKAGING_ROOT=scratchpad/pk),
  pack GREEN --strict --no-panel, release_check GREEN. My pack bug: TikTok/IG captions not shown to seats.
  Page `_UPLOAD_RED_TEAM.html`. RESUME: ask "fresh blind re-test ($0)?"
- 2026-11-13 UPLOAD RED TEAM r2 (red_team_upload_r2/, fresh 5 seats, full files): title 9/8/7/9/6; applied tagline
  "AT THE FIRST FIRE, PETER SAID NO.", wide reframed (both fires + Jesus), "not one of Jesus' followers", TikTok/IG open on Peter
  (John 18:17-27), glosses, FB send-line out. Gate READY, pack GREEN, release GREEN. 2 rounds = stop. Page `_READY_TO_POST.html`.
  RESUME: owner posts (30-episode hold may apply - ask), then upload_tracker.py --set second-fire-he-fed-him-first <platform> <url>.
  Not committed (text only when asked; no media).
