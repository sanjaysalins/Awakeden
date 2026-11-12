# Motion design brief v2: Mary and Martha — REDESIGN THE DOODLES

## What the owner said about v1 (verbatim)
"I feel the doodle can be much better, it feels very forced at the moment and is not complementing the episode"
(Earlier ask: "better transitions effects ... great motion graphics and doodles". v1 = F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\MARY_MARTHA_MOTION_v1.mp4,
spec F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v1\MOTION_DESIGN.md, frames motion_v1\QC_sheet.jpg.)

## My diagnosis (check it yourself, disagree if wrong)
v1's doodles are a diagram language laid ON TOP of the art: an abstract scribble "knot" for worry, a lasso round the kitchen pots,
cream text cards. They explain; they do not belong to the pictures. The owner's 3 style references
(F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v2\OWNER_REFS.jpg — LOOK AT IT) already have their own doodle
language, part of the picture itself: faint unfinished pencil line-sketches of era objects on the cream paper (jars, clay oil lamps
with a flame, shelves, a woven blind), pale golden leafy vines/botanical swirls in the margins, soft steam curls from clay cups.
Several of our own shots have the same sketch layer (look at F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v1\f01.png ... f15.png:
shelf/jar/lamp sketches in f02, f04, f05, f06, f09, f12; golden leaf vines behind the family in f13).

## The job
Write a NEW doodle + text layer that COMPLEMENTS the pictures: doodles that look like the illustrator kept drawing on the page in the
same pencil and gold, growing out of the art's own sketch layer and its cream margins — gentle, warm, sparse, tender. Fewer and
better beats. Keep v1's CUT and its 6 TRANSITIONS exactly (they worked; table in motion_v1\MOTION_DESIGN.md section 4).
Rethink the on-screen words too: keep only what truly helps a newcomer with English as a second language
("careful" = full of worry is the one hard word); text must sit on the art the same gentle way, not as UI cards.
- One quiet visual thread is still welcome IF it comes from the refs' own vocabulary (e.g. a lamp, a vine, steam), never an abstract symbol.
- Doodles must never cover faces or touching hands; respect Shorts safe zones (text x 60-950, y 160-1490).
- No knot, no lasso, no arrows, no hearts, halos, sparkle, glow, emoji, UI shapes, pills, drop shadows.
- Martha is not the villain; grace, not pressure. KJV on screen word-for-word only.
- Animate like a hand drawing: line draw-on, slow growth, gentle settle. Doodles may be slightly animated after drawing (steam drifts, a vine leaf sways) but subtle.
- Remotion SVG/CSS only, $0. No new AI images.

## Read
- Words + per-word times: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\voice_v2\narration.md and narration.alignment.json
- 15 gridded frames: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v1\f01.png ... f15.png (grid = 108x192 px cells of 1080x1920)
- Look: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\STYLE.md
- v1 spec (cut, transitions, format to copy): F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v1\MOTION_DESIGN.md
- v1 build (components available: Swatch, Write, Line, smooth, pencil filters): F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\MaryMarthaV1.tsx

## Output
ONE file: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v2\MOTION_DESIGN.md — same precision as v1
(idea in 3 lines; beat table with frames, word hit, what appears, motion + easing, exact SVG path data or shape recipe in 1080x1920 px,
colours hex, why it complements THIS picture; do-not list; risks). Mark 3 KEY FRAMES (frame numbers) that best show the new look,
so the owner can judge from stills before a full render. No code.
