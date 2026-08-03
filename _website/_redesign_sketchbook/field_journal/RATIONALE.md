# THE FIELD JOURNAL — design rationale

**The premise:** the website *is* the sketchbook the films are drawn in. Not a themed
site — one continuous physical object: a book on a dark desk, page-stack edges under it,
a torn corner to turn the page, ribbon-red reading progress, index tabs for navigation.

## Drawn from the real generated images (not imagined)

- **The paper system is sampled straight from the shipped stills** (`bronze_serpent_long/stills/`):
  warm cream ground, kraft torn-paper collage pieces, masking-tape strips, faint blue
  engineering-grid hairlines, halftone dot patches, coffee rings. Every one of those exists
  in the renders (s01, s16, s27…), so the UI vocabulary — tape, deckled mats, grid patches
  in margins — is the *art's own* vocabulary, and taped-in plates sit on the page without a seam.
- **Style 1 stays the spine.** Page chrome is plain cream/kraft everywhere. Bake-off variants
  appear only as *content* ("insert leaves": charcoal, wet-bleed, scratchboard — all
  production-approved in `style_manifest.json`), presented in the margins exactly as the
  locked doctrine uses them: occasional, deliberate.
- **Gold is Christ-only, enforced in CSS.** The gold thread (OT chip → red-letter card), the
  gold underline on "whosoever believeth in him", and the torn-page landing (s68) are the only
  gold on all three pages. Buttons are rubric red; tabs are kraft. The colophon states the rule.
- **s68 (torn hole, gold light) became the landing device sitewide** — the film's own landing
  grammar reused as the site's "every page lands on Jesus" moment.
- **sl20 (the user-loved sketchbook spread)** anchors the catalogue's cast pages.

## Long-text readability inside the immersion

The rule: **texture never sits behind the reading measure.** The study page is a two-column
grid — a clean ~66ch serif column (Source Serif 4, 1.15rem/1.8, ~12:1 contrast) beside a
250px *working margin* that absorbs all the handmade noise: Caveat field notes, leader lines,
grid patches, insert-leaf thumbnails. Script faces (Pinyon = Scribed Ink, Caveat = keeper's
hand) are display/annotation only, never body. Rotation is only applied to taped media,
never to text blocks. On mobile the margin notes fold inline as taped slips. Verse registers
are typographically distinct: elder-leaf foxed card for OT, red-letter block with rubric bar
for Christ's words — keeping the red-letter convention in manuscript form.

## Honest tradeoff / risk

The immersion machinery (desk frame, tabs, tape, torn corners) spends real screen area and
novelty budget; on small phones it compresses to near-invisibility, and if the register of
whimsy drifts even slightly it could read as "scrapbook craft kit" rather than a working
field journal — undermining the reverence the content demands. The guardrails are the two
CSS-enforced reservations (gold = glory, red = His words + rubric accents) and the flat,
quiet reading column; any production build should treat those as gates, not suggestions.
A second real cost: catalogue thumbnails currently all come from one episode's art, so the
grid undersells the eventual variety.

*Mockup only — no live-site files touched. Images transcoded from the real PNGs into
`_media/` (16 curated stills, ~4.7 MB total).*
