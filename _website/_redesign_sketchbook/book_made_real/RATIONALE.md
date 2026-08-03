# THE BOOK MADE REAL — rationale

## The structural decision
The earlier three mockups dressed a normal website in sketchbook skin: hero banner,
feature cards, margin-note sidebar. This one deletes the website. What loads is a
**closed book on a desk** — the only object, the only navigation. Every surface you
ever see is a face of a physical leaf in a real 3D leaf-turn engine (9 leaves, 18
faces, front/back, spine-hinged). There is no scroll, no page-as-rectangle, no grid.

- **Progress bar** = the fore-edge stacks. Pages you've read pile on the left,
  pages remaining on the right. They are also the turn buttons.
- **Table of contents** = an INDEX page bound into the book (leader dots, folio
  numbers). Clicking an entry doesn't teleport — it **riffles**, fast-turning the
  intermediate leaves. Unfinished chapters are listed as **"pages uncut"** — the
  honest book word for "coming soon".
- **A two-page spread carries art and text at once**: the chapter plate bleeds
  across the gutter (each leaf face carries its half), reading text runs beneath;
  plates elsewhere are tipped in with tape corners, inside the text flow.
- **The tear is the argument**: the Nehushtan page (the sign become a shrine) is
  torn out BY THE READER — you perform Hezekiah's act — and John 3:16 is already
  waiting on the page beneath. A deckled scar stays at the spine forever. The torn
  leaf's verso (seen only if you turn past instead) tells you to go back and tear.
  Per LAW 1 the torn page carries no Scripture.

## Device ports (mechanics, not screenshots)
| panel_animator source | web interaction |
|---|---|
| `page_transitions.py` TornOutPage | live tear on leaf 6: grab → smootherstep lift (−2.2°, +8,−6, growing shadow) → deckle flash at rip−0.35s → rip-away on the same `p^1.8` acceleration, same rotate-center (60px, 60% h). Below-page already waiting; wobbled deckle scar remains. |
| `ink_transition.py` `make_reveal_field` | the actual Python function generated `_media/ink_field.png`; JS thresholds it per-frame in canvas (`(t−(f−edge))/2·edge`, edge 0.09) — the chapter plate arrives as an ink blot, not a fade. |
| `annotators_circle.py` | seeded sum-of-sines wobbled ellipse (same term counts/amps), drawn as a growing point-prefix in two passes (60/40 split, second pass lighter + offset) around "looketh" — rubric red. |
| `raking_light.py` | gaussian sweep band crosses the closed cover every 8s; gold flare = gaussian overlap of band centre with EDEN and the gold strip. |
| `ribbon_marker.py` | landing CTA: ribbon drops 0.6s after the last spread settles — smootherstep 0.4s drop + fixed 6px decaying micro-bounce — then absolute stillness. Rubric red, frayed clip-path tip. |
| `grid_choreography.py` | the reader's pointer IS the page camera: the study under your eye brightens (never zooms), the rest dim; idle 2.6s hands attention back to a slow auto-rack. Hand-inked borders + paper gutters per the 2026-07-24 finding. |

Also: Scribed-Ink letter-reveal only on the narration-voice verse; Num 21:8 and the
red-letter John 3:14–15 **arrive whole** (LAW 1). Gold is used only on His glory:
the thread, the John 3:16 drop cap, EDEN, the swash under "Look to Him, and live."

## The honest tradeoff
A book model fights the web's native strengths. **Touch/mobile is the real cost**:
a 1360×910 spread scaled onto a phone is legible only in landscape, swipe conflicts
with text selection, and the tear needs a deliberate tap. I shipped swipe + tap +
arrow keys + edge buttons + `prefers-reduced-motion` (instant turns, devices render
complete), but a production build needs a true single-page portrait mode (one leaf
per view) and larger type — that is a second engine, not a media query. Deep-linking
and SEO also suffer (one URL, state in the book): production would mirror each
spread at a crawlable URL and riffle to it on load.
