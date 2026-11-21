SLUG: it-is-finished
STATUS: READY
VERDICT: FIX
FILLS: Old July engine; spec_report has no speed table. 3.4-7.0 s seventh_day_light = dyncam (camera push on a still = Ken Burns) - low/med | rest kling. Frame-diff freeze test clean.
SLOP: 37-38 and 15-17 - nail-through-hand close-ups show a wrist band/cuff (anachronism) - low | otherwise consistent
TEXT: 0-3 s - hook card "WHAT WAS FINISHED?" not spoken (voice says "The first time the Bible says finished...") - low/med | ~39 s - gloss "GAVE UP THE GHOST = DIED": "= DIED" not spoken - med
END: hold=0.15 (last word 58.94, film 59.10) silent_end=NO (tail RMS 1674, audio is loud to the final frame) - abrupt end
FIX_IDEA: Add >=3.0 s landing hold: video last frame + audio pad/fade (score tail), $0 (ffmpeg tpad + apad/afade, ~2.5 s fade per owner rule). Drop the "= DIED" gloss, $0 re-cut
