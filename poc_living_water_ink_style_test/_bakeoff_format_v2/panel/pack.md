# EVIDENCE PACK: a bake-off to decide how to make NEW "Swirls of Life" episodes significantly better

## Context
Swirls of Life = 60-second-ish YouTube Shorts / Reels. A Bible scene told as a hand-drawn ink-and-watercolor storyboard page (baked title, frame number, 3 small sketch panels, one big illustration, handwritten KJV caption fragments); AI stills, AI animation per page, ElevenLabs narration, felt-piano score, SFX. Lands on Jesus. Global audience incl. non-native English. Solo creator (the owner), dyslexic, wants simple answers. 12 films finished, ZERO posted, so no viewer data exists. Owner said: do NOT fix current episodes; work on new ones and design a great bake-off.

## Measured facts (audit of 12 finished films, $0)
- Runtime: only 4 of 12 near 60 s (56.5, 61.9, 64.0, 64.4). Others 68-72 s (x4), 78, 84, 106, 106.
- Cover (title card) shown ~3-6 s at start in eps 11, 12, 13 and Jacob's Ladder; narrator speaks from ~0.1 s in all.
- 11 of 12 are 720x1280; one 1080x1920.
- No file is broken; A/V lengths match; no decode errors.
- A blind 5-seat panel earlier said: the biggest gap is the viewer (first 2 s, pacing, phone legibility, muted autoplay, loop ending); post early; shape refs for hard props (cross drew as an X on >=6 of 9 pages in ep13; ep13 had 70 rejected renders, older eps may not have kept rejects); drop cheap draft pass; do not build many generic defect gates.

## The proposed new-episode rules (to be tested)
First 2 s: open on picture with hook already spoken; title card <=1.5 s or moved to the end. Length: target 45-60 s. Pages: 5-6 not 9. Rhythm: the 3 small panels become quick cuts (change every ~3 s). Phone test: big picture carries beat alone with chrome covered. Muted test: story understood with sound off. Landing: last frame rhymes with first (loop), new ending shape, mechanical check vs shipped endings. Quality: 1080x1920, fast-start wrap, motion fallback = re-render not push-in on hook/landing. Fewer rejects: hard-prop check at design time, one approved shape ref tested on 1 page, reject log with reason codes.

## The proposed bake-off design
Rules: one story same words (narration, voice, score, art constant; only FORMAT changes); scoring + win rule written before looking; 3 layers (numbers + blind panel + real viewers), a win needs 2 of 3; paired comparison on the same story only; error bars, "likely" not "proved"; owner's build hours count.

Bake-off 1 (FORMAT, ~$0): story = Ep 8 "Can Any Good Thing" (64 s, 0 rejects, no open bug), re-cut from its EXISTING stills/clips, no new generation, copies in a new folder. Arms: A control = as shipped. B hook-first = title <=1.5 s, hook spoken at once, 6 pages. C rhythm = B + the 3 small panels used as cuts. D big-picture = no page chrome on interior beats, big illustration full screen, chrome only on cover and ending, loop ending. Known limit: panel crops are low-res; D crops from clips made as whole pages.
Judging: Layer 1 numbers ($0): time to first picture change, cover hold, seconds per cut, runtime, resolution, ending-shape match, owner build hours. Layer 2 blind panel (Fable seat + Claude, Codex, Grok, Sonnet; film-only; shuffled labels): who/what/why yes/no, "would I swipe at 3 s", hook 0-10, muted-understood yes/no, does the end pay off. Layer 3 real viewers: 20-30 people on phones, each sees 2 arms in random order, muted once and with sound once, pick one, note where they would swipe; optionally (owner's call) post winner and control on different days, same hour, read 48 h numbers (swipe-away 0-3 s, % viewed, replays).
Win rule: an arm wins if it beats Control in 2 of 3 layers and no seat loses who/what/why; ties go to the cheaper/faster-to-build arm; if Control wins stop changing the format; report seat splits, never average them away.

Bake-off 2 (stop rejects; needs price + owner yes): does a shape ref stop the X-cross? Arms: control (current prompt, 5 cross stills), shape ref (1 approved side-on ref chained, 5 stills), angle-first (camera angle chosen before first render, 5 stills). Count X rate by eye and pixel check. ~15 stills, roughly $1.20 at ~40 credits each (quote first).
Order: blind panel on this design; bake-off 1; bake-off 2 only with quote + yes; then write winning rules into the Swirls skill.
