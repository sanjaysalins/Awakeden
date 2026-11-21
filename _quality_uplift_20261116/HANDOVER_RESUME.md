# HANDOVER - Quality uplift of the ready shorts (stopped 2026-11-16, night)

## First thing tomorrow (in order)
1. **Drive F: now has room (~141 GB free at stop).** Move the fixed films kept on C: to F:
   - from `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\` (ep13, ep08, jl, ep11, ep10, ep02 folders)
   - to each film's own `uplift\` (or `final\`) folder on F:, same file names. Check MD5 after copy, then decode check
     (`ffmpeg -v error -i <file> -f null -` prints nothing).
2. **Ask the owner** (one page, one pick each):
   - Lock the 5 ready films? (Can Any Good Thing fix1, The Cross That Wasn't His fix1, Where Are the Nine fix1,
     Woman Behold fix1, She Loved Much fix1 as-is)
   - Bier redo yes + cap raise $49 -> $56? (plan below)
   - Jacob's Ladder score: run the blind score panel ($0), then ~$1 ElevenLabs (cap $2)?
   - OpenArt top-up (49 credits left at stop; shared with other sessions).
3. Nothing is running. No agents, no paid jobs.

## How to lock a film (when owner says yes)
- Pin `FINAL_VIDEO.txt` to the fix1 file (keep old one as `FINAL_VIDEO.txt.prev_pre_fix1`).
- `.venv\Scripts\python.exe cli_publish.py <pack> --index` then `--copy-ok` (only the video changed).
  After `--index`, re-copy any `publish\captions_locked.srt` (index rebuilds captions).
- Write `UPLIFT_LOCKED.md` in the film's `uplift\` folder (date, file, MD5, $ spent).
- Rebuild tracker: `.venv\Scripts\python.exe build_upload_tracker.py`. Run `release_check.py` (want GREEN).
- Commit text only (never media).

## Where each film stands
| Film | Best file | State |
|---|---|---|
| ep08 Can Any Good Thing | `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\ep08\uplift\ep08_uplift_fix1.mp4` | v1 LOCKED; fix1 ready to swap (balloon + Nathanael fixed) |
| ep13 The Cross That Wasn't His | `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\ep13\uplift\ep13_uplift_fix1.mp4` | v1 LOCKED; fix1 ready to swap (hand/gate/dust fixed; bull still stands) |
| ep11 Where Are the Nine | `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\ep11\final\ep11_uplift_fix1.mp4` | ready (leper-touch Bible error + Samaritan face fixed) |
| ep10 She Loved Much | `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\ep10\final\ep10_uplift_fix1.mp4` | ready as-is; Simon F06B not fixed (new still ready, ~140 cr to animate) |
| Woman Behold (comic) | `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\woman_behold_john1926\visual\woman_behold_john1926_uplift_fix1.mp4` | ready ($0 fixes) |
| ep02 Ashes That Made Clean | `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\ep02\ep02_uplift_fix1_final.mp4` | free fixes only; man look + F02D walk-across need paid fix (cap $7, needs top-up) |
| Jacob's Ladder | `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\jl\uplift\jl_uplift_fix1.mp4` | picture fixed; owner: score too modern -> new cinematic score |
| ep07 The Bier He Touched | `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_07_the_bier_he_touched\uplift\ep07_uplift_fix1.mp4` | owner: "loads of AI slop" -> redo plan waits |

## Plans waiting on the owner
- **Bier redo:** `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_bier_redo\_BIER_REDO_DESIGN.html`.
  Keep 5 of 14 shots; 5 ref sheets + 8 stills + 9 clips; $4.47 first take / $6.71 with redos. My add: redo F04 too
  (Luke 7:14 "touched the bier", not the body). Needs cap $56.
- **JL score:** `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_jl_score\_OWNER.html` + `DESIGN.md`.
  Strings, harp, horn; split at 36.5 s; 2.5 s end fade; `generate_score_jl.py --go` (ElevenLabs gen_music, never
  composition_plan/music_v2), then `mix_score_jl.py`. House rule: blind score panel (Fable + AI panel) BEFORE spend.

## Money
- Spent ≈ $38.91 of the $49 owner cap (all in `data/spend_ledger.jsonl`). OpenArt balance 49 credits at stop.
- Rates: Kling 3 Omni pro sound-off 35 cr/s; Nano Banana Pro still 40 cr; $0.002/cr.

## Lessons from today
- Per-clip gates passed, but the owner still saw slop on the Bier: do a whole-film consistency pass
  (same faces, clothes, props on every page) before showing a film.
- "no bubble" in a Kling prompt CAUSED speech bubbles. Never name the thing you don't want.
- Check OpenArt balance before any paid launch (shared account).

## Review pages (all built, nothing auto-opened)
- `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\_FIX1_PART1.html`
- `C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\_FIX1_REVIEW.html` (ep10, ep11)
- `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\woman_behold_john1926\visual\uplift_v1\_FIX1_REVIEW.html`
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_02_ashes_that_made_clean\uplift\_FIX1_REVIEW.html`

## Other open items (older)
- 14 posted videos still say Awakeden in YouTube descriptions: owner fixes by hand
  (`F:\slk\PycharmProjects\JesusInTheBible\_FIX_YOUTUBE_DESCRIPTIONS.html`).
- ep12 Ye Are Not All Clean blocked (cuts-off bug). Women First Witnesses captions cover only 13 of 82 s.
- Global CLAUDE.md still says "honest AI disclosure once" — conflicts with the no-AI rule (owner to decide).
- Comic rollout to 8 more films ($0 plan) and insight-line narration changes not started (words gate first).
- pytest: 9 old failures in test_run_piece (KeyError 'stills'), not from this work.

## Update 2026-11-21
- All 5 films, Bier redo and JL score were already LOCKED (11-17/18). Release check GREEN.
- ep02 Ashes fix2 BUILT, waits for owner lock: `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_02_ashes_that_made_clean\uplift\fix2\ep02_uplift_fix2_final.mp4`
  (MD5 05b7ea948d14a29a1bf9f2e891756f84, audio MD5 = shipped). Review: `...\uplift\fix2\review\_FIX2_REVIEW.html`.
  4 stills redrawn to a new cream-tunic ref (`refs\unclean_man_ref_cream.png`), 5 clips + 1 F02C redo. Spent 1,455 cr = $2.91 (cap $7).
  To lock: pin FINAL_VIDEO.txt -> uplift/fix2/ep02_uplift_fix2_final.mp4, then the lock steps above.
- 2026-11-21 later: owner picked score "A. Felt piano" (existing score_epic.mp3, $0). LOCKED + pinned:
  `uplift/ep02_uplift_fix2_piano.mp4` (MD5 148960644f6c720563a113831ad8b8fb). Pack GREEN, release_check GREEN.
  Text committed (ep02 files only). data/spend_ledger.jsonl + _media_rules/paid_jobs_log.csv rows added but not committed (shared with other sessions).
