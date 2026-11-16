# Film v2 request (give this + BUILD_BRIEF.md to a fresh Sonnet build agent if v2 is not done)

Build film v2 (keep v1 untouched). $0, same rules as `BUILD_BRIEF.md` (gentle mode: Remotion --concurrency=2, ffmpeg -threads 2; never open files; never commit; no paid tools).

1. NEW AUDIO (owner-locked): `audio\narration.mp3` is now 59.18 s (one closing line added). Words: `words\FINAL_WORDS_v5.md`; word times in `audio\narration.words.json` (timing unchanged up to "This day" ~49.9-50.5 s). New last line: narrator "His welcome is still open, for you, today." at ~52.34-55.6 s, then silent hold to the end. Add a narrator pill for it (no tab). Landing stays S14 full-bleed, still, nothing drawn: S14 is 10.04 s, so start the S14 landing no earlier than ~49.1 s (gate G12: no panel longer than its clip). Update the `NazarethComic` Composition frame count to the new audio length; re-run every gate incl. G1/G2 against the new narration.mp3.

2. $0 FIXES from the v1 review (`build\contact_v1.jpg`):
 a. Fewer repeats: no clip on more than 2 pages; S05 (widow) and S06 (shackle) only on their own beat ("good news for the poor" / "freedom for prisoners") plus at most one echo. The "That local boy was saying..." and "He stopped reading at God's welcome" pages lean on Jesus panels (S01, early S03, S09 crop) and S13/S12, not widow/shackle. Fewer, bigger panels are fine; G10 must stay >= 60%.
 b. S13: drop the grey/sepia memory tint; at most a light warm vignette so it matches the warm golden look.
 c. S04: crop on the hands + scroll (the handing over), not the attendant's face (it looks like the townsman S12).

Deliver: `film\NAZARETH_COMIC_v2.mp4`, `build\contact_v2.jpg` (look at it yourself), `build\gates_out_v2.txt`, review page `_FILM_v2.html` (v1 and v2 side by side). Report: page plan, repeat count per clip, gates, doubts.
