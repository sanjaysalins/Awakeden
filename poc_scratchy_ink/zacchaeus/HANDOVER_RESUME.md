# Zacchaeus (Luke 19:1-10) - HANDOVER / RESUME (2026-11-10 night)

Folder: `F:\slk\PycharmProjects\JesusInTheBible\poc_scratchy_ink\zacchaeus\`
Style: the owner's Google Flow pictures (scratchy ink, red mantle over olive tunic Jesus).
Refs in `style_refs\` (copied from `poc_scratchy_ink\lazarus_come_forth\style_refs\`, with STYLE_NOTES.md).

## UPDATE 2026-11-11
Owner said yes: words v2 LOCKED (salvation glossed, 19:6 joy told, 195 words ~70 s). t3 redrawn (+2 credits ~$0.10, logged), good. Old = stills/t3_v1.png.
Guardrail panel DONE (r1+r2, guardrail_r1/ guardrail_r2/). New words = words/FINAL_WORDS_v3.md (v3.1, 214 words ~75 s), awaiting owner re-lock. Page _ZACCHAEUS_GUARDRAIL.html.
v3.1 LOCKED by owner 2026-11-11.
Voice RECORDED 2026-11-11 (owner yes <=$0.50, logged ~$0.40): audio/narration.mp3 = 81.2 s natural (long!). Crowd line is narrator; (pause) not in audio, add in edit.
81 s kept (owner ok). 12 stills made (24 cr). Owner: no freeze/boomerang/zoom -> CLIP_PLAN.md (14 scenes, native-length clips, trim only).
CLIP_PLAN done: 4 redraws + 14 clips (209.25 cr), all logged. FILM BUILT 2026-11-11: ZACCHAEUS_POC.mp4 85.2 s, trim-only, 1 s pause, 3.06 s hold, -15.1 LUFS. build_film.py, qc_clips.py.
Owner: film "good", asked to push motion. Fable design _work/MOTION_DESIGN_FABLE.md; Remotion _remotion/src/ZaccPreview.tsx (20 s preview: hook + reversal + landing) -> _ZACCHAEUS_MOTION.html (before/after). $0.
Owner: motion look "sloppy" -> dropped. Picked A + consistency fix (owner yes ~$2.20, logged $2.31): one fig tree (s01c, s14d), one room (s09b), clips c01 c09 c13 redone, two-pass loudness. FILM REBUILT: 85.2 s, -14.3 LUFS, peak -1.4.
PUBLISH-READY 2026-11-11: owner "lock it". Piece batches/cluster_04_encounters/zacchaeus_short (slug zacchaeus-who-was-looking): LOCKED.json sha 6997b049..., packaging (3 blind cards merged), pack GREEN, thumbs from clean stills (publish/make_thumbs.py), red team 6/7/7.5 REVISE -> fixes applied, release_check GREEN, tracker rebuilt. Spend total $15.10 (ledger).
NEXT = owner uploads + sends links: upload_tracker.py --set zacchaeus-who-was-looking <platform> <url>. Commit TEXT ONLY when asked.

## Where we stopped (old)
The owner was shown the 4 test stills and asked: "Lock the words + redraw t3 (~$0.10)?"
**No answer yet.** Ask again first thing.

## Done
1. Ideas round (blind seats Fable/Opus/Sonnet/Codex) -> owner picked **A "Who was looking for whom?"**.
   Files: `ideas\`, page `_ZACCHAEUS_IDEAS.html`.
2. Words: 5 blind writers -> test (X won 2/3) -> fixes -> re-test (Fable 7.5, Codex 7, Gemini 9.5) -> fixes.
   Final: `words\FINAL_WORDS.md` (~179 words, ~65 s). Page `_ZACCHAEUS_WORDS.html`.
   **NOT LOCKED.** Still weak: "salvation" not glossed; 19:6 "joyfully" and "fourfold" left out.
3. 4 test stills (owner yes, 8 credits ~$0.40, in `data\spend_ledger.jsonl`).
   Script `make_stills.py` (nano_banana_2, 9:16, 2k, refs = owner's Flow pictures).
   - t1 Jesus sheet: good.
   - t2 Zacchaeus in the tree: good.
   - t3 Jesus calls his name: WEAK (near copy of t2, Jesus small, back turned). Redraw = close low view up the tree, Jesus's face looking up, Zacchaeus looking down surprised. ~2 credits ~$0.10. NEEDS A YES.
   - t4 crowd grumbles: good.
   Page: file:///F:/slk/PycharmProjects/JesusInTheBible/poc_scratchy_ink/zacchaeus/_ZACCHAEUS_VISUALS.html

## Next (in order, each paid step = quoted price + its own yes)
1. Owner: lock words? redraw t3?
2. Guardrail panel (5 questions, blind, Fable seat) on the locked words. $0.
3. Quote voice (ElevenLabs, ~$0.16 like Jesus Wept). Use
   `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\per_turn_synth.py --natural`.
   Voices: narrator, jesus, crowd, zacchaeus. Delete `_turns\` if text changes (stale cache).
4. Quote remaining stills + animation (Jesus Wept was 13 stills+clips ~174 credits ~$8.70).
   Count each named person in every still (cloned-people rule).
5. Build film (copy the Jesus Wept build), loudness to ~-14 LUFS, landing hold >= 3 s.
6. Packaging card + blind panel, thumbs, `cli_publish.py <folder> --index --copy-ok --no-panel`, red team, manifest + tracker.
7. Commit TEXT ONLY when the owner asks (nothing for Zacchaeus/Lazarus/Jonah committed yet).

## Other open items (not Zacchaeus)
- Owner to upload Jesus Wept + Barabbas, send links -> `.venv\Scripts\python.exe upload_tracker.py --set <slug> <platform> <url>`
  (slugs `jesus-wept-the-sentence`, `barabbas-son-of-the-father`). Turn on each platform's AI label.
- Jesus Wept thumb mouth reads a bit smiling (redraw ~$0.70, owner said leave it).
- Jonah style tests `poc_style_scratchy\jonah_sulk\v1.png`, `v2.png` (~$0.20) - no decision.
- Lazarus idea dropped by the owner ("no another story").

## Rules
Gentle mode ON (`C:\Users\sanjay\.claude\.gentle-state` = 3). Never auto-open files. No media to GitHub.
Blind panels always have a Fable seat. Short plain words, end with one pick.
