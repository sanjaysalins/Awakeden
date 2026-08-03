# The Archive of Insert Pages — rationale

**The idea:** the films' own signature move — one plain hand, with occasional insert pages
told slightly differently — becomes the site's information architecture. Page TYPES map to
registers the way film beats do. Chrome, navigation, wordmark and body text stay in ONE
Style-1 voice on every page, so the registers read as filed pages in one binder, not themes.

## The page-type → register map

| Page type | Register | Why this pairing |
|---|---|---|
| Homepage, reading pages | **Style One** (the spine) | The default IS the identity. Ivory paper, ink/wash, kraft tape, faint blue grid, one thin gold edge — lifted directly from `bs_s01_camp_wide` / `baseline`. |
| Catalogue | **Scholar's Margin** (insert) | A catalogue *is* an index, so it's filed in the indexing hand: full-page graph grid, a ruled red ledger margin with plate numbers, drawn thread-arrows — all taken from the real `s43_insert_scholars_margin2` plate. |
| Featured film + every study's landing block | **Gilded Proclamation** (insert) | Gold is His glory only, so gold never marks "featured product" — it marks the Christ-landing (`s67`, `s68`). One gold moment per page, maximum. |
| Announced-but-unmade episodes | **Blueprint / Cyanotype** (insert) | Cold print-process blue = planned, not yet inked (`sv05`). Coming-soon cards are empty dashed plates — honest, and cheap to maintain. |
| Cross-reference blocks inside studies | **Scholar's Margin** (inline insert) | The shadow→body typology table with the drawn arrow, labelled as an insert page. |

## Signature device: the scarlet thread

Every episode carries a hand-drawn red arrow from OT shadow to NT landing (`NUM 21:8 ⟶ JOHN 3:14`)
— the site-wide encoding of "every piece lands on Jesus." It turns gold only inside a gilded
block. Drawn straight from the Jericho landing plate (`j13`), where Rahab's scarlet cord
literally crosses the torn page to the cross.

## Type doctrine (LAW 1, translated to web)

Scripture is **set** in Libre Caslon — the 18th-century English Bible face; the Word arrives
whole, never in a casual hand. The Keeper's margin notes are **handwritten** (Caveat, tilted).
Filing labels are **typed** (Courier Prime — the archive's index-card voice). Body is Spectral.
Red-letter keeps the red bar + red text convention.

## What I drew from the real images

Torn-plate collage, tape strips, halftone/grid patches, the single gold-leaf edge and the
coffee-ring-and-thumbprint "working desk" tone all come from the 10 stills I opened and studied,
not from the word "sketchbook." Captions use plate numbers because the shipped film really has 68.

## The honest tradeoff

A multi-register system is the most expensive of the three directions to keep coherent. Every
new page type forces a decision ("which hand is this?"), a new contributor can misuse a register
(gold on a promo is a doctrine bug, not a style bug), and the CSS surface is ~3 registers × every
component. The mitigations are built in — registers are *labelled on the page* ("Insert page ·
Scholar's Margin"), the map above is closed (new page types default to Style One), and chrome
never changes register — but this direction only stays elegant under editorial discipline. If
that discipline isn't wanted, a single-register site is the safer buy.
