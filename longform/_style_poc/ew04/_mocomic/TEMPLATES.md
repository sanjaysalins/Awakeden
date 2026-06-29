# Motion-comic template catalogue ("back pocket")

Layout vocabulary for the animated-comic pipeline. Each template is a page layout
the engine knows how to fill from clips. Pick per beat; rotate for freshness; heroes
and gospel pivots stay `full`.

Every clip carries **anchors** so a crop never slices the main element:
`bias=[bx,by]` (0=left/top … 1=right/bottom offset) and, for fractured-hero,
`anchors=[[zoom,bx,by], …]` (one per sub-panel — e.g. full / eyes / hands / object).

`motion` tag drives the **fill guardrail**: `static`→boomerang (in/out ok);
`directional`/`talk`→hold last frame (one-way motion must never reverse).

| Template | Mode | Caption | Panels | Use it for |
|----------|------|---------|--------|-----------|
| `full` | single (full-bleed) | top overlay / red-letter bar | 1 | Heroes, gospel pivots, the landing. Speech = red-letter bar. |
| `two_v` | fill_each | **bottom** bar | 2 cols | Two distinct subjects/moments side by side (wide↔close pair). |
| `split_v` | split_page | **top** band | 2 cols | One still whose subjects already sit left/right (shot ↔ reverse). |
| `stack_h` | fill_each | bottom bar | 2 rows | Two establishing/landscape beats; before→after. |
| `big_inset` | fill_each | corner | 1 big + inset | A hero element + a reaction inset (object + face). |
| `triptych_v` | split_page | top band | 3 cols | A wide crowd/landscape read across three panels. |
| `strip_h3` | fill_each | bottom bar | 3 rows | A 3-step sequence (forge → lift → look). |
| `quad` | fill_each | corner | 2×2 | A montage / "the whole story in four beats". |
| `hero_frac3` | fracture | corner | 1 big + 2 small | **Fractured hero** — one clip: full + 2 anchor crops. |
| `hero_frac4` | fracture | corner | 2×2 | Fractured hero, four anchor crops. |
| `hero_band3` | fracture | bottom bar | 3 rows | Fractured hero strips — full → **eyes** → key object. Edgiest. |

## Modes
- **single** — one clip fills the whole page (bleed). Caption overlays.
- **fill_each** — each panel gets its own clip (cycled), anchor-fitted so the subject is centred, never sliced.
- **split_page** — one clip scaled to the page, cut into page-aligned panels — a continuous "broken page". Only use when subjects already sit where the panels fall.
- **fracture** — one hero clip shown across N panels, each a different zoomed anchor crop (full / eyes / hands / object). The clip's `anchors` list supplies them.

## Future back-pocket layouts (not built yet)
6-panel grid · T-layout / L-layout · diagonal-canted gutters · full-bleed splash with
a single inset · polyptych (one action across a whole row) · overlapping/breaking-the-
border panels. Add as the stories call for them.

## Add a template
Append to `TEMPLATES` in `comic_engine.py`: `name -> (mode, cap_slot, layout(content)->[rects])`.
Geometry is shared by the preview (`render_still_page`) and the video build
(`build_segment`), so a new layout shows up in both with no extra work.
