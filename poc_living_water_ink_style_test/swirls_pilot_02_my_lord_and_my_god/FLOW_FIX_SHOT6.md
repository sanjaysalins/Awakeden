# Fix directive — Shot 6 only ("My Lord and my God" close-up)

Paste this whole message into Google Flow. You can use the same project/session as before, or a
fresh one — either way, upload the two files named in step 0 first.

---

**Message to paste into Flow:**

You are fixing ONE still image and its ONE matching video clip from an episode you already made
most of. The earlier version of this exact still had a real defect: an extra line of text appeared
baked into the artwork below the caption, reading "Check that 'my God' is actually visible before
accepting this page." That line should never have been there — it was a note for a human reviewer,
not something to draw. It's now removed from the instructions below. Generate 2 things, in order,
checking each before moving to the next. Do not pause for approval between them. Turn off any
prompt-enhancement/auto-improve option first.

**Step 0 — Ingredients.** I've attached two images: one is the established Thomas character
reference, one is the established Jesus character reference, both already used across the rest of
this episode's other shots. Use them for likeness in the two generations below.

---

## Step A — the still image

- ACTION: generate_image | Aspect ratio: 9:16 vertical | Inputs: both attached reference images
  (Thomas + Jesus)

PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F05". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "he answered") a small sketch of Thomas's open hand, no longer raised in refusal, now simply open and relaxed at his side; panel 2 (handwrite: "and said unto him") a small sketch of the same gap of air from the previous page, now with the faintest single thread of blue reaching into it, still not touching; panel 3 (handwrite: "not faithless") a small sketch of morning light broadening across the floor. Below them, ONE large full-scene illustration filling the lower half of the page — framed tighter than the previous page — this is the close-up the confession earns: Thomas, now kneeling, risen upright on his knees, face lifted fully to Jesus, filling the lower-right of the frame; Jesus's presence at the frame's left edge, his open offered hand still visible at the frame's edge with its single faint nail-mark, not his whole figure — the camera has moved in close on Thomas's face and posture, not on Jesus. Thomas's one hand still half-lifted toward the edge of frame where Jesus's hand is, stopped just short of touching — a clear, deliberate, visible GAP remains, closer than ever but still not touching; this gap is a hard rule and holds even at this climax. Thomas's contour is now one single, unbroken, confidently struck line — fully resolved, no broken or tremored line remains anywhere on him — his face lifted in open, unguarded worship, eyes wide, jaw loose, nothing held back. A few soft threads of blue ink, with the faintest gold trace, curl in the narrow gap between his reaching hand and the edge of frame where Jesus's hand is, closer than any prior page, still not touching either. Small handwritten production notes: a caption beneath the main scene, handwritten on exactly two stacked lines, both lines fully present and fully legible — the first line reads "My Lord and", the second line directly beneath it reads "my God", and no other words, sentences, or instructions of any kind appear near this caption or anywhere else on the page. Below the caption, a corner note, handwrite: "NOTE: line steady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "CLOSE TWO-SHOT", "ONE:", "ONLY", or any other scene-description or editorial label as if it were part of the artwork — the framing description in this prompt is an instruction to you, not text to render), not extending, completing, or adding to any caption beyond the exact words quoted above, and not writing any sentence, note, or instruction of any kind anywhere on the page beyond the exact handwrite strings quoted. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS

**Check before moving on — must all pass:**
- The caption has exactly two lines, "My Lord and" then "my God" beneath it, both visible — and
  NOTHING else is written near it or anywhere else on the page. No extra sentence, no note, no
  instruction-like text anywhere. This is the exact defect being fixed — check it carefully.
- A clear gap of air between Thomas's hand and Jesus's hand — they do not touch.
- Thomas's outline is one single steady confident line — fully resolved, no break anywhere.
- Thomas kneeling, filling the lower-right; Jesus a partial presence at the left edge, not his whole
  figure.
- Jesus's visible palm shows one small faint dry mark only — no blood, no red.
- Top-left "SEQ: THOMAS", top-right "F05", corner note "NOTE: line steady", exactly 3 small panels
  labeled "he answered" / "and said unto him" / "not faithless" — nothing else.
- Thomas and Jesus both match the two attached reference images.

If any line fails, regenerate once more with the exact same prompt and the same two attached
images, nothing changed. If it still fails, keep whichever of the two attempts is closer and tell me
clearly which check(s) still don't pass — don't silently accept a bad result.

---

## Step B — the video clip

- ACTION: generate_video_with_first_frame | Starting frame: the image from Step A | Duration: 8
  seconds (or your nearest available length) | Aspect ratio: 9:16 vertical

PROMPT STARTS
One slow, visible breath loosens Thomas's shoulders fully across the length of the clip — a real, continuous, readable release of tension, shoulders and chest visibly settling from tight to open. His lifted face holds in open worship throughout, eyes wide and warm. The soft blue threads in the gap between his hand and Jesus's drift continuously and visibly, curling gently, never frozen into one shape. Camera: locked, close framing held throughout — no push, no zoom, the closeness is baked into the still. Thomas's lips stay closed and completely still — not speaking; the baked caption "My Lord and / my God" carries the words, not his mouth. His half-lifted hand stays exactly where drawn, in its own fixed gap, the whole clip — it never closes the gap, never touches. Jesus's visible hand at the frame's edge stays steady. Thomas's steady linework stays exactly as drawn, stroke for stroke.
Audio: a single soft settling breath, the faintest rustle as Thomas's weight shifts on his knees, otherwise near-silence. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS

**Check before moving on — must all pass:**
- Thomas's shoulders/chest visibly settle from the first frame to the last frame — real motion, not
  a static hold.
- The blue threads are still visibly moving in the last third of the clip, not frozen early.
- The hand-gap never closes and never touches, first frame to last.
- Both caption lines "My Lord and" / "my God" are unchanged and nothing extra has appeared on the
  page, first frame to last.
- Nobody's lips move. No speech, no music — ambient sound only.

Same retry rule as Step A: one retry if anything fails, then tell me clearly what's still wrong
rather than silently accepting it.

---

**When both are done**, tell me which is the still and which is the clip (your own filenames are
fine, just say which is which) so I can drop them into the finished episode in place of the old
Shot 6.

---

## For you (not part of the Flow message) — which files to upload as the two references

Upload these two, already-approved from the last successful batch:
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_02_my_lord_and_my_god\_flow_delivery_v7\Middle-aged_man_standing_portrait_202609081812.jpeg` — Thomas
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_02_my_lord_and_my_god\_flow_delivery_v7\Man_standing_in_watercolor_art_202609081812.jpeg` — Jesus

Using the real already-approved images (instead of generating fresh references again) keeps this
one shot looking identical to the rest of the already-assembled cut. Don't use the file named
`jesus_ref_upscaled3x.png_...jpeg` in that same folder — that one is not a real generated reference,
it's a stray/wrong file Flow returned both times this episode was run.
