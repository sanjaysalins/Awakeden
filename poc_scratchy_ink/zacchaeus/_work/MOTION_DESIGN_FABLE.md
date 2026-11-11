# Zacchaeus — motion layer design (Fable seat)

All times are FILM time (narration time +1.0 s after 39.15). Screen positions are estimates from the QC sheets — check each one on the real frame.

## 1. Verdict on the current cut

The clips are strong. The graphics layer is not in the same world as them.

- **Pills are app UI.** Rounded, see-through, soft. The art is hard black ink on flat yellow. Nothing else in the frame is see-through or round.
- **Captions fade in as blocks.** No link to the voice. A 0.12 s alpha fade is the most "video template" move there is.
- **KJV / narrator / Jesus look almost the same.** Only a tiny tab tells them apart. On a phone it is unreadable.
- **The hook has two text blocks at once** (title over his body + pill). The title sits on the figure. Neither one *shows* the idea.
- **The spine is only spoken.** "Who was looking for whom?" is never drawn. That is the big missing piece.
- **14 plain hard cuts.** No grammar. The 1 s pause at 39.15–40.15 is the best moment in the edit and nothing marks it.
- **Landing = one long pill over the trees for 9 s.** The 3 s hold has nothing to hold on.
- Caption 22 has a "1 COR 15:3-4" tab but the words are a paraphrase, styled like KJV. Fix: only word-for-word KJV gets the KJV look.

## 2. House look (5 lines)

1. **Type:** hand-lettered comic caps, slightly uneven baseline (±2 px, ±1° per word). Headline words in Permanent Marker (already in `_remotion/public`); body in a free hand-letter face. Never a clean sans.
2. **Ink behaviour:** everything is *drawn on* in stroke order, never faded. Edges roughened (feTurbulence + feDisplacementMap). All overlays "boil" on threes (new noise seed every 3 frames) so they move like the art.
3. **Colour:** three only. Ink black `#14110d`, paper cream `#f1e6c8`, mantle red (sample from Jesus's robe). Red is spent ONLY on Jesus's words and Jesus's line.
4. **Opacity:** 100% or 0%. No transparency, no blur, no soft shadow. Shadows are hatched.
5. **Rhythm:** things land ON the spoken word, 2–3 frames, with a pen scratch or ink tap. Then they sit still. Silence = nothing new on screen.

## 3. The moves, ranked

### Move 1 — THE SIGHT-LINE (signature device, the spine)
**Beats:** 1.42–5.70 (plant) · 18.68–20.9 (echo) · 71.04–76.90 (payoff) · 76.90–85.22 (lands, see Move 3).
**What you see:** Two hand-drawn lines. A thin, scratchy, *dashed black* line = Zacchaeus looking. A thick, sure, *solid red* brush line with an arrowhead = Jesus looking.
- Payoff shot (c13, empty tree at sunset — no people, zero face risk): on "came to look" (71.88) the black dashed line scratches UP the trunk to the empty branch and stops, unsure. On "Jesus" (72.84) the red line starts at the sun on the road and comes DOWN the road; on "find" (73.76) its arrowhead lands at the foot of the tree with an ink tap. On "He still looks for the lost" (75.40–76.6) the red line turns and runs off the BOTTOM of the frame — toward the viewer.
- Echo (c04, 18.68 "looked up"): a short red stroke rises in the open sky gap between crowd and branch. 1 s, then gone.
**Why:** it draws the reversal. A viewer with sound off and no English still gets it: small black line searching, big red line arriving.
**Build:** Remotion `<SightLine path color dashed start dur />`. SVG path, `strokeDasharray` draw-on, roughen filter, seed stepped every 3 frames. Points hand-placed per clip in a JSON.
**Risk:** line must sit on a still part of the frame; if a clip's camera drifts, the anchor slides (check each clip; add a 2-keyframe offset if needed). Red line is flat ink — no glow, ever.

### Move 2 — HOOK (0.00–5.70)
**Frame by frame:**
- 0.00–0.20: frame is black scribble hatch; it lifts off in 6 frames (pen-scratch sound) to show the climb. Motion in the first 6 frames.
- 0.12–1.9: black caption slab, bottom band, words stamp in as spoken: A MAN CLIMBED A TREE TO SEE JESUS.
- 1.42 ("see"): the black dashed sight-line scratches from the sky beside his head up and out the top-right. He is looking for someone off-page.
- 3.48 ("But"): the dashed line stops dead. One ink spat.
- 3.68–5.34: red line comes up the left margin from below and its arrowhead lands in the yellow sky behind his back (about x200, y600) on "him" (5.34). Caption swaps to BUT JESUS WAS LOOKING FOR **HIM.** — "HIM." underlined in red.
**Cut:** the floating "WHO WAS LOOKING FOR WHOM?" title. Two captions + two lines already ask it. Let the YouTube title carry the words.
**Why:** the hook becomes a picture of the question, not a sentence about it.
**Build:** same components as Moves 1 and 4.
**Risk:** his hands are on the trunk top-right and crowd faces are bottom — the lint in Move 4 must pass.

### Move 3 — LANDING (76.90–85.22)
**Frame by frame:**
- 76.90: splat cut. The red line from the last shot enters from the bottom, coming up the path.
- 77.24–79.6 ("To save them, He later died for our sins"): caption in the top-left sky. On "died" (78.62) the line runs INTO the black doorway and is gone. For ~0.8 s there is no red on screen.
- 80.38 ("rose"): the red line comes back OUT of the doorway, thicker.
- 81.42–82.2 ("on the third day"): three tally strokes scratch into the sky, one per word; the third is red.
- 82.2–85.22 (hold): the line runs down the path and off the bottom, arrowhead resting at the edge, pointing at the viewer. Nothing new appears. Only the boil moves. Caption stays.
**Why:** the same line that found Zacchaeus goes into death, comes out, and comes for *you*. The hold now holds on something.
**Build:** doorway = hand-traced polygon mask (`clipPath`) so the line passes "inside". Red on the black door needs a 3 px cream keyline.
**Risk:** highest taste risk. Must stay a plain ink line. If it reads cute, drop the tally and keep only in/out/toward-viewer.

### Move 4 — CAPTION SYSTEM (whole film)
Three looks, readable at a glance:
- **Narrator:** solid black brush-stroke slab, rough torn ends, cream caps. Like a comic caption box.
- **KJV (word-for-word only):** cream paper scrap, thick scratchy black border, hatched shadow, black lettering, hand-lettered ref tag (LUKE 19:8).
- **Jesus's KJV lines** (22.37, 55.12, 66.04): same paper scrap + a thick red brush bar down the left edge + a big red open-quote. Lettering stays black (red text is hard to read).
- Words stamp in 2 frames ahead of the voice, whole phrase max 2 lines, min 56 px, 100% opaque. One key word per line gets a scratch underline ("HALF", "FOUR TIMES", "LOST").
- **Safe-zone lint ($0 gate):** per clip, hand-mark face + hand boxes in `safe_boxes.json`; build fails if any caption or line overlaps one.
**Build:** Remotion `<InkCaption kind="narrator|kjv|jesus" words={alignment} />`; PNG brush-edge mask for the slab.
**Risk:** opaque captions hide more art than pills — keep them shorter and narrower (max 820 px wide).

### Move 5 — TRANSITION GRAMMAR (three cuts, no crossfades)
- **Splat cut (default, 11 cuts):** hard cut; on the cut frame a 2-frame ink spatter flicks in a corner. Almost free.
- **Hatch wipe (chapter turns only: 17.30, 44.50, 70.95):** cross-hatch strokes scribble over the frame in 5 frames, lift in 5. Stroke-order reveal via a noise-threshold mask (reuse `ink_transition.py`).
- **The held breath (40.09–41.15):** after "Jesus went anyway." nothing is drawn. Captions clear. Only time the layer is empty. Then the cut to the table.
**Risk:** hatch wipe eats ~0.3 s of each clip's ends; over-use turns it into a template.

### Move 6 — TALLY HITS (48.87–54.6)
"Half of all he had" (48.87): one horizontal scratch strikes through a drawn coin-stack mark, leaving half. "four times" (53.87–54.3): four tally strokes, one scratch sound each, in the top-left sky of c10 (hands with coins are lower-centre — keep clear).
**Why:** makes the cost of his change countable with sound off. Sets up the three-stroke tally in the landing.
**Risk:** decoration if it is too big. Small, margin only.

## 4. Build first — ~20 s preview

1. **Hook — 0.00–5.70** (Moves 2 + 4).
2. **The reversal — 70.95–76.90** (Move 1 payoff + hatch wipe in). Late, not mid, but it is the spine and it runs straight into the landing, so the red line can be judged across a real cut.
3. **Landing — 76.90–85.22** (Move 3).

Total 19.97 s. If the owner wants a true mid beat instead, swap item 2 for the call, 21.30–27.33 (Jesus-caption style test).
