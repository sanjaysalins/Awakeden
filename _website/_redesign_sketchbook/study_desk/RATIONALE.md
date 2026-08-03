# The Study Desk — design rationale

**The bet:** this site's job is reading, not immersion. So the mockups are built like a
modern study Bible that happens to be illustrated by the sketchbook hand — not like a
sketchbook that happens to contain text.

## Drawn directly from the real renders

Every token is sampled from the shipped stills, not imagined:

- **Paper cream / kraft / sepia ink** — the base palette of every Bronze Serpent plate.
- **Wash-blue, madder red, gold** — the style's own accent theology, kept with its meanings
  intact: blue = study apparatus (links, cross-refs, grid hairlines), red = only Christ's
  spoken words (the red-letter bar convention) plus EDEN in the wordmark, **gold = once per
  page, at the landing, never anywhere else** (gold is His glory only).
- **Kraft-tape corners on "plates"** — how artwork sits on the page, from the collage stills.
- **Torn-edge section dividers** (inline SVG) — the torn-page transition, used at two seams
  per page, not everywhere.
- **Caveat hand-notes with a wobbled leader line** — the tiny cursive field labels on the
  sl20 sketchbook spread ("profile study", "grip"), reborn as margin annotations.
- **The torn-page landing plate (s68)** — the film's own landing device becomes the site's
  structural rule: every page ends at a gold seam and lands on Jesus.
- Faint engineering-grid hairlines + one confined halftone patch — hero/opener bands only.

Type: **Literata** (built for long digital reading) for body, **Fraunces** for display,
**Caveat** strictly for hand-notes. The reading column is ~63ch at 1.14rem/1.85.

## Deliberately left out

- **No paper texture under running text.** Flat cream. Texture fights glyph edges and costs
  contrast; the real stills carry the "handmade" load instead.
- **No coffee rings, thumbprints, ink blots** in the chrome. One wobbled hand-note per
  section is the ceiling; more turns study into scrapbook.
- **No full-bleed artwork behind content, no parallax, no line-boil/animation.** One settle
  animation on the hero plate; reduced-motion kills it.
- **Grid + halftone confined to header bands.** Never behind a paragraph.
- **Insert-page style variants (cyanotype, scratchboard, gold-leaf plates) not used** —
  Style 1 is the spine; the site is chrome around Style 1, not a 16th variant.
- Media: 17 curated stills, downscaled to ≤1800px JPEG (~0.3–0.5MB each); the reading page
  itself is text-first and loads fast.

## The honest tradeoff

Restraint cuts both ways: on image-light screens this direction can read as "tasteful
editorial serif site" rather than unmistakably *the sketchbook world* — cream paper + serif
+ red accent is also a common generic look. The defence is structural, not decorative: the
annotated margin rail, the red/blue/gold ink discipline, taped plates, and the gold-seam
landing are load-bearing conventions from the films. If those conventions aren't kept up
ruthlessly in production (e.g. gold starts leaking into buttons), the distinctiveness
collapses into that generic look. Second risk: Caveat is a well-known Google handwriting
font — if it starts feeling stock, the production build should replace it with a lettered
woff subset of the films' own KUNSTLER-style hand.
