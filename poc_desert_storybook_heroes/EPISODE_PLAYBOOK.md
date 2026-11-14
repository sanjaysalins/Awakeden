# Desert-Storybook Short — Episode Playbook (copy this for the next one)

Built from **Blind Bartimaeus** (Mark 10:46-52), 2026-11-13/14. 79 s, 9:16, 17 shots.
Reference folder (copy scripts from here): `F:\slk\PycharmProjects\JesusInTheBible\poc_desert_storybook_heroes\bartimaeus\`
Total real spend ~ $16.6. Every paid step had its own quoted yes from the owner.

## The rules that run the whole way
- **Each paid step needs its own quoted yes from the owner** (price and cap). Praise or a "lock" is never permission to spend.
- Every gate uses a **blind panel**: Fable + the AI panel (Claude, Codex, Grok and Gemini CLIs, plus a Sonnet seat). Each seat writes or judges from scratch. The pack is built by a script and leak-checked.
- Never open files. Give `file:///` links. Pages are short and visual.
- Log every spend in `F:\slk\PycharmProjects\JesusInTheBible\data\spend_ledger.jsonl`.
- Keep `HANDOVER_RESUME.md` in the episode folder up to date after every step.
- No media goes to GitHub.

---

## Step 1 — Words ($0) → owner locks
Folder `words\`.
1. Write a `BRIEF.md` (the problem list) and fetch the KJV text into `KJV.txt`.
2. **Blind writers:** 4-5 seats each write the narration from scratch. They are Fable, Sonnet, Codex, Gemini and Grok.
3. Make a judge table, then combine the best parts into 2-3 candidates.
4. Run the **5-guardrail blind panel** (`guardrail_r1\`, `guardrail_r2\`). It asks:
   - Who is this for?
   - What is the take-away?
   - Does it work for a global audience?
   - Is it accurate to the Bible?
   - Is this the best version?
5. Fix anything that 2 or more seats raise, plus any accuracy point. Run the panel again, at most 2 rounds.
6. The owner picks on a page (`_BARTIMAEUS_WORDS.html`), which gives `LOCKED_WORDS.md`.
- House style:
  - Character lines are KJV, word for word.
  - The narrator explains every old word in plain English.
  - The ending lands on Jesus: the cross and the rising, from 1 Cor 15:3-4.
- The hook is the cry itself, at 0 s.

## Step 2 — Voice (~$0.50, ask first)
Folder `audio\`.
- Run `per_turn_synth --natural` (no time-stretch).
- Character lines use eleven_v3 with emotion cues, stability 0.3, and **2 takes each**. The owner picks the takes.
- Voices:
  - narrator `LSi9zNCeliLuhIGGS0By`
  - Jesus `tlETan7Okc4pzjD0z62P`
  - Bartimaeus `puDRtQWF8NtQiPMJygTb` (pick a fresh one for a new character)
- `rebuild_narration.py` rebuilds the mix and writes `timeline.json`, which holds the real line timings.
- If words change later, delete `_turns/` for those lines first (stale-cache gotcha).

## Step 3 — Shot plan ($0)
- Write `SHOT_PLAN.md`: one shot per beat, timed from `timeline.json`.
- Each clip must be **longer than its slot**. Trim only. No freeze, boomerang or zoom fill.
- Choose the heroes: the stop, the healing and the ending. They get real motion.
- No stone at the tomb, because Kling rolls it. The cross is empty.

## Step 4 — Pictures (~$2, ask first)
Folder `stills\` and `refs\`.
- Use GPT Image 2 i2i through OpenArt: 9:16, 2k, medium (47 credits each).
- Give it one look ref, plus a ref for each recurring character, one for **each costume state** (e.g. with cloak and without).
- `stills\build_requests.py` writes the requests. `history_ids.txt` keeps the job ids.
- QC every still:
  - There is one of each character, with no clones.
  - Hands are right.
  - Story facts hold (eyes shut until healed; the cloak is gone after he throws it off).
  - Buildings fit the period (Herod's temple, not Greek).
- Note: OpenArt may drop the 3rd ref on two-person shots.

## Step 5 — Clips (~$6, ask first)
Folder `clips\`.
- Use Kling 3 Omni i2v pro, sound off, 35 credits/s, through OpenArt.
- `build_clip_requests.py` makes the requests.
- `qc_strip.py` checks the first and last frames and runs a pixel diff, to catch motion Kling invented.
- Redo only what is broken. Keep old versions as `*_pre_xxx.mp4`.

## Step 6 — Draft film ($0)
- `film\assemble_v2.py` cuts the clips at 1.0x with hard cuts, trimmed to the voice timings.
- Add a **3 s landing hold** at the end.
- Picture and sound must be the same length.

## Step 7 — Look check (owner watches)
- The owner caught Bartimaeus's face and clothes drifting between shots.
- Fix: make a new character ref, redraw the drifting stills, and remake their clips (~$4).
- **Next time: lock a ref for every costume state before Step 4**, which saves this cost.

## Step 8 — Music (~$1.20 per try, ask first)
Folder `score_panel\` and `score\`.
1. Build a blind score panel (Fable, Claude, Codex, Grok). Each seat designs the score from the timed lines in `_timed_lines.txt`.
2. Merge what they agree on.
3. Generate the score in **2 parts, split at the turn** (the standing rule).
4. The owner liked **v2: felt piano and cello with a hummable tune**. It is in D minor, turning to D major at the healing, and the music stops under "Jesus stood still".
5. Mix with `score\mix_score_v2.py`:
   - music about 14 dB under the voice, with a sidechain duck;
   - small raises at the healing and the ending hold.
- Check loudness by measuring it, not by eye.

## Step 9 — Sound effects (~$0.40, ask first)
Folder `sfx\`.
- `gen_sfx.py` makes new ElevenLabs sounds, 2 takes each: hush, cloak, birds.
- `add_sfx.py` lays library sounds from `sound_library\clips\`: wind, crowd and footsteps.
- Dip the effects at the stop.
- The output is `film\..._final_v1.mp4`.

## Step 10 — Motion graphics + lettering in Remotion ($0)
1. **Fable designs the motion layer** (`motion_v1\MOTION_DESIGN.md`). Its devices:
   - dust strokes that march with the crowd;
   - cry rings;
   - a dark edge that stands for blindness;
   - everything freezing at the stop;
   - a gold bloom at sight;
   - dust and page wipes between shots.
2. Align the words for $0 with `motion_v1\align_words.py` (faster-whisper), which writes `words.json`.
3. **Fable designs the lettering separately** (`motion_v2_type\TYPE_DESIGN.md`, "Three Hands"). The owner rejected the first, sticker-like text.
   - **SHOUT:** his cry, in Protest Revolution, red earth `#B23A22`, growing word by word.
   - **TELLER:** the narrator, in Caveat Brush, as ink multiplied onto the painting, written on as each word is spoken.
   - **WORD:** Scripture and gospel facts, in IM Fell English, pressed on and never moving. Jesus's words are on a bare-paper patch in sage `#2F5347`.
   - **Arc:** no gold before sight. "sight." is a hollow outline; "see." is big and gold.
   - First Fable makes a static preview (`_TYPE_PREVIEW.html`), and the owner says yes.
4. Build it in `_remotion\src\BartimaeusV2.tsx`, registered in `Root.tsx`.
   - Copy this file. Change `CUT`, `SHOT`, `GUARD` (the face boxes), `ROADCFG` and `LINES`.
   - Base video: `_remotion\public\bart\base.mp4`, the final film with no audio.
   - Fonts go in `_remotion\public\`.
5. Render with `npx remotion render src/index.ts BartimaeusV2 out.mp4 --muted`, then copy the audio in from the final film.
6. QC:
   - Pull a frame from every shot.
   - **No text or effect may cover a face.** Measure the guard boxes on the moving clip, not on the still.
   - Picture and sound must be the same length.
- Gotchas:
  - `mix-blend-mode` dies under a parent with a transform, so each blended layer must be a sibling box.
  - Guard masks cut square notches into soft edges.
  - A thin ring of light reads as a computer UI circle, so use a soft bloom instead.

## Step 11 — Finished-film guardrail panel ($0)
Folder `guardrail_r3_film\`.
1. `build_pack.py` builds a **film-only** pack: per shot, the picture, the words on screen and the spoken lines, numbered. It runs a leak check.
2. Seat prompts reuse the r2 seat text.
3. CLI seats: `run_seats.py bible:claude,hook:codex,global:gemini,global:grok`.
4. Agent seats: Fable (judge) and Sonnet (newcomer). Each reads only its own prompt file.
5. Tabulate the answers. Fix what 2 or more seats raise, plus any accuracy point. Make one owner page.

## Step 12 — Packaging (title, poster, publish pack)
Folder `packaging\` and `_packaging\NN_name\`.
1. **Search data ($0):** pull YouTube autocomplete for 10-15 phrases into `_packaging\NN_name\autocomplete_<date>.txt`, using `suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=...` with a generic user agent.
2. **Title round ($0):** files go in `packaging\title_r1\`.
   - Write `BRIEF.md` (the film's words, the pictures that exist, the real searches, the rules).
   - Run `run_cli.py` (codex, grok, gemini, claude) plus a Fable agent. Each writes 6 title and thumbnail pairs.
   - Take the converged pairs into `JUDGE_BRIEF.md`.
   - Run `run_judges.py` plus a Fable judge.
3. **Poster ($0.40, ask first):** files go in `packaging\poster_r1\`.
   - Run a blind key-art prompt (`PROMPT_keyart.md`) through 3 CLIs plus Fable. Each pitches movie titles and 2 posters with image prompts.
   - Render the best 4 with GPT Image 2 i2i (look ref, plus Bartimaeus and Jesus refs).
   - `compose.py` adds real type in the film's fonts.
   - Blind poster judges (Fable, Sonnet, Opus) look at `judge\Q1..Q6.jpg` and `PHONE_SIZE.jpg`. Apply the fixes they agree on.
   - **The owner picks.** Here the owner overrode the judges.
4. **Piece folder:** create `batches\cluster_04_encounters\<name>_short\`. Copy the format from `woman_at_well_short`.
   - Files: `FINAL_VIDEO.txt`, `LOCKED.json` (with the sha256), `piece.json`, `publish_meta.json` and `narration.md`.
   - `audio\` holds `narration.mp3`, `narration-tagged.md`, `voices.json` and `narration.alignment.json`.
   - `visual\` holds `<name>_final.mp4` and `<name>_final.words.json`.
   - `packaging\` holds the lock note and the thumbnail.
   - Make the words json with `pipeline.assembly_align._whisper_align` on the narration (CPU is fine). The film's audio must start at 0.
5. **Packaging card + gate:**
   - Write `_packaging\NN_name\packaging.json` (copy the woman-at-well card).
   - Run `PACKAGING_ROOT=_packaging node F:\slk\PycharmProjects\MeekAndMighty\_pipeline\check_packaging.js _packaging\NN_name\packaging.json` until it prints `[GATE] PACKAGING-READY`.
   - R03 ("Bible" in the title) was overridden with a written reason.
   - **No AI wording in any public text.**
6. **Publish pack:**
   - Run `.venv\Scripts\python.exe cli_publish.py "batches\cluster_04_encounters\<name>_short"`.
   - Reconcile the 5-CLI panel findings (`upload\_independent_review\<stamp>\`) into the `publish\*.md` files.
   - Run `cli_publish.py ... --index`, then `--strict`, until it is GREEN.
   - Then run `release_check.py`.
   - The paste page is `publish\PUBLISH_INDEX.html`. Posting is held for the 30-episode target.

## Step 13 — Owner red team of the publish pack ($0)
Folder `batches\...\<name>_short\publish\_redteam_owner_r1\`. Copy it from Bartimaeus.
1. **Build one blind prompt** (`PROMPT.md`) with these parts:
   - The job, and 8 checks: Bible accuracy, honesty, consistency, global words, platform fit, owner rules, captions, anything else.
   - The KJV text of every passage the video uses, **including the ending passage** (e.g. 1 Corinthians 15:3-4).
   - A one-line description of the thumbnail and the pinned comment.
   - All 4 platform `.md` files and `captions.srt`, pasted in.
2. **Seats:** run `run.py` (claude, codex, gemini, grok) plus a **Fable agent** that reads only `PROMPT.md`. Each writes `seat_<name>.md`: a VERDICT, the issues with exact replacement text, and what is good.
3. **Tabulate:** fix anything 2 or more seats raise, plus any Bible-accuracy point from any one seat. Keep the video's own locked words. Do not re-voice for packaging.
4. **Fixes Bartimaeus needed (check these every time):**
   - **Scripture range:** cite every passage the video tells, including the cross and the rising, on **every** platform.
   - **The pinned comment drifts from the pack.** It lives in `_packaging\NN\packaging.json`. Fix it there, and say "many", not "a whole crowd".
   - **Don't ask a question the title or thumbnail already answers.** Bartimaeus: "Would He stop?" became "What would He do for one blind beggar?"
   - **Captions:** cut by phrase, with no cue under about 1 s, and quote KJV lines the same way every time. Hand-fix them and keep a copy as `captions_redteam_fixed.srt`.
   - **Archaic words in plain text**, such as "hold his peace", become "be quiet".
   - **Tags:** no vague ones like "jericho"; use real searched phrases. The first hashtag is the card's `person_tag`.
5. **Gates again:**
   - `check_packaging.js` must print PACKAGING-READY.
   - `cli_publish.py ... --index --strict` must be GREEN.
   - Then **re-copy `captions_redteam_fixed.srt` over `captions.srt`**, because `--index` rebuilds the captions.
   - Check again with `python -c "from pipeline import publish_check; publish_check.report(r'<piece>', strict=True)"`.
   - Run `release_check.py` last.
6. **Use only `publish\`.** `upload\upload_kit.*` is the engine's first draft, not the paste source.

## NO AI WORDING — ever (owner rule)
- No public text may say anything about AI: not "made with AI tools", "AI-generated" or "AI art/voice". This covers titles, descriptions, captions, tags, the pinned comment and paste pages.
- The **platform AI switches** (YouTube altered content, Meta AI label, TikTok AI-generated) stay ON at upload. That is a setting, not words.
- **Enforced in code (2026-11-14):**
  - `data/upload_brand.json` no longer has an `ai_note`.
  - `pipeline/upload_engine.py` no longer writes one.
  - `pipeline/publish_check.py` FAILs any `publish\*.md` line with AI wording (`NO-AI-WORDING`).
- **Sweep for old packs:** `.venv\Scripts\python.exe tools_strip_ai_wording.py` is a dry run; add `--apply` to fix. It cleared 447 lines in 187 files.
- **Already-posted videos** keep their old text online. Edit them in YouTube Studio or the app by hand.

---

## Cost table (Bartimaeus actuals)
| Step | ~USD |
|---|---|
| Voice (+ v4 lines) | 0.65 |
| Pictures (+ redos) | 2.40 |
| Clips | 6.80 |
| Look fix (stills + clips) | 4.32 |
| Music v1 + v2 | 2.32 |
| SFX | 0.40 |
| Motion, lettering, panels | 0 |
| **Total** | **~16.6** |

## Biggest lessons
1. Lock **every costume state** as a ref before you make any pictures. Skipping this cost ~$4.
2. Design the text with Fable **as its own pass**, preview it on real frames, and only then build it.
3. The music works best when it **stops at the turn** and the melody resolves at the healing.
4. Measure everything (face guards on the moving clip, loudness, lengths). Never judge one still by eye.
