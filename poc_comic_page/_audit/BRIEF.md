# Brief for every fix agent ($0, local only)
Goal: give each assigned finished Short the same $0 hook + plain-words fixes we proved on Piece 1, WITHOUT touching originals.
Read first (short): F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_assemble_piece1_v4.py (the drawtext recipe: Impact font, white + gold 0xF2C14E, black@0.62-0.66 box) and F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_panel_design\_DESIGN_PANEL_REPORT.html (rules).
Data: F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_audit\videos.json (id -> video path) and audit.json (measurements) and frames\<id>_0.3.png / _1.2.png (first frames; LOOK at them).
Per piece:
1. Find the narration text (the piece's own narration.md / script / srt next to the video, or its publish pack). Do not invent facts.
2. HOOK CARD: if the first 2s show no question/hook text, burn a 2.0s card (<=7 words, plain, asks the viewer's own fear/question that the narration itself answers; no claim beyond the verse). If a hook already shows, skip and say so.
3. DECODE CARDS: for 0-2 archaic quoted KJV words that carry the key line (e.g. 'in no wise', 'cometh'), show 'OLD = PLAIN' for >= 1.2s + 0.25s/word, only where the narrator speaks them (use srt/alignment timings). Plain meaning must not change doctrine; if unsure, skip and list it.
4. Rules: ONE text layer at a time; never overlap burned-in captions or other cards (check frames at the card times); card font >= 84px for hook, >= 100px for decode; keep audio stream copied untouched; output duration must equal source within 0.05s; do not re-time anything.
5. Write NEW file next to the source: <source stem>_v5hook.mp4 (never overwrite or delete anything). Use ffmpeg local only. Run at normal priority; use -threads 4.
6. Verify by extracting frames at each card time and at 1s after, and LOOK at them (Read tool). Fix and rerun if text is cut, overlapping, or unreadable.
7. Write F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_audit\fixes\<id>.json: {id, source, output, hook_text|null, hook_skipped_reason, decode_cards:[{old,plain,t0,t1}], skipped_decodes:[...], title_question_proposal, verified:true|false, notes}. Proposal only; do NOT edit publish packs, titles, FINAL_VIDEO pins, the tracker, or any ledger.
Hard limits: $0 only (no HF/Kling/OpenArt/ElevenLabs/Gemini/API calls); do not open any browser or file; do not touch other agents' pieces; do not use the Workflow tool; if a piece's files are missing or the rules cannot be met cleanly, record verified:false with the reason instead of forcing it.
Final reply: one short line per piece: id, hook text or skipped, decode cards, verified.
