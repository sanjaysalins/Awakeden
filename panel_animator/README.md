# panel_animator — comic-grid panel toolkit

All $0, deterministic (Playwright/PIL/ffmpeg — no Higgsfield spend, no login).
Every tool has its own skill (`.claude/skills/<name>/SKILL.md`) with full
usage, locked lessons, and a CLI reference. This file is the roster and the
decision framework for WHEN to reach for each one — read this first.

## The standard default: the parchment caption band

`typography_panel.py` and `infographic_panel.py` share one caption treatment
— a torn hand-inked parchment band (`assets/caption_band.png`), never a
rounded card or drop-shadow box. This is the **default, frequently-used**
text/diagram treatment for this style. Keep using it wherever a beat needs
in-world text or a two-still comparison.

Locked: never let a counter/stat show a fabricated number (verify against the
real KJV text first, land honestly on the dash if there isn't one); never add
a typography panel just because a beat "could" have one — pull the exact verse
or narration phrase that beat is actually about.

## The other six: selective, not default

`grid_choreography.py`, `impact_burst.py`, `ink_transition.py`,
`line_boil.py`, `parallax_25d.py`, `print_grade.py` are real tools, not a
checklist to run on every panel. **Spread them thin across an episode** —
picking one for a beat is a creative decision, not a mechanical pass. Before
reaching for one, ask what the STILL shows, what the NARRATION beat is doing,
and what's actually missing:

| Tool | Reach for it when… | Not when… |
|---|---|---|
| `grid_choreography` | a beat needs a genuine multi-panel montage (a crisis unfolding across several moments) and you want the reader's eye pulled deliberately, not four clips looping independently forever | there's only one clip's worth of content for the beat |
| `impact_burst` | there's a real point of contact — a bite, a strike, a pole driven into the ground, a slam — at an exact timestamp | the beat is calm/contemplative, or you'd have to invent a "hit" that isn't really there |
| `ink_transition` | the CUT ITSELF carries meaning — type dissolving into fulfillment, danger giving way to the remedy, one movement ending and another beginning | a plain hard cut already reads fine; not every beat change needs a transition treatment |
| `line_boil` | a panel HOLDS for a while and perfect digital stillness starts reading as static/dead | the clip already has real camera motion (redundant) or is very short |
| `parallax_25d` | a CALM panel (a reaction, a quiet reveal) needs to feel alive without inventing action — a cheaper, often more honest alternative to a generated push-in | the panel needs actual story motion (a strike, a turn, a walk) |
| `print_grade` | as the LAST pass over a finished sequence, to unify everything into one printed-comic texture | mid-build — always last, never per-panel |

## Every grid still needs real animation

Per `CLAUDE.md`'s comic-grid tiering rule: a grid built entirely of static
typography/infographic panels is not acceptable. At least one cell in any
multi-panel grid must be a real generative animated clip (Seedance/Kling,
never Ken Burns). A grid mixing one text/diagram panel alongside real animated
clips is exactly the intended pattern — see the 60s Bronze Serpent prototype
(`longform/04_The_Bronze_Serpent/_prototype_60s/`) for a worked example: a
2x2 grid with three real animated clips and one typography panel, choreographed
together with `grid_choreography`.

## Known gotchas (see individual SKILL.md files for the full list)

- `ImageDraw` on an RGBA image does not alpha-blend — draw on a separate layer
  and `Image.alpha_composite()`, or low-alpha ink textures render as pale
  holes instead of stains.
- Never ask an image model to paint a diagram or lettering into a still — it
  reliably invents garbled fake text even when told not to. Diagrams are
  always two real stills + `infographic_panel`'s deterministic overlay.
- `-loop 1` image inputs in an ffmpeg filter graph need an explicit `-t
  <duration>` — `-shortest` on the output is not reliably enough to stop the
  encode once a filter (e.g. `blend`) is fed an infinite-looped stream.
