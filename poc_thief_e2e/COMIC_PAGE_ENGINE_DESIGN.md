# COMIC PAGE ENGINE — system design (DRAFT, 2026-07-25)

> Status: **proposal + one $0 POC, not wired, not locked.** Builds directly on
> `.claude/skills/comic-strip-native/COMIC_STRIP_NATIVE_SPEC.md` (the binding
> draft spec for the technique) — this document adds the ONE missing layer the
> user asked for (comic text boxes) and assembles the already-validated pieces
> into a single end-to-end system for BOTH formats (9:16 shorts, 16:9 long).
> Where this doc and the spec disagree, the spec wins.

## What the user asked for

Comic-book style pieces (long 16:9 + short 9:16) where **every panel is
animated** and the page carries **real comic-book text boxes** (speech
bubbles + caption boxes). NBP for stills, Kling for animation.

## The system in one picture

```
narration (locked, KJV)                          [existing /narrate + /voice]
   │
   ▼
A. PAGE SCRIPT      beats → pages → panels; per panel: composition, speaker,
   (paper, $0-3)    bubble/caption text (KJV verbatim from kjv_cache), layout
   │                choice per page (1-4 panels, grid_choreography LAYOUTS)
   ▼
B. PANEL STILLS     nano_banana_pro, ONE CALL PER PANEL at full res
   (~$0.30/panel)   (spec §0.5 pivot — NOT whole-page draws), chained
   │                panel-to-panel with verbatim Character Anchors;
   │                NO baked text ever (spec §3)
   ▼
C. HUMAN GATE       full-res eye-check: CSN-G1..G4 + body gate on every
   ($0)             passion panel, every time (stochastic, spec §1.4)
   ▼
D. PANEL ANIMATION  cost-tiered per panel (single-panel input fixes the
   (~$0.90-1.31/     whole-page collapse): calm → Minimax Hailuo ~$0.90
   panel)            (zero-invention validated §0.5b) or Seedance;
   │                 action/crowd → Kling 3.0 pro ~$1.13-1.31;
   │                 passion/Christ panels: crop-path discipline (§5.3
   │                 validated) — animate the panel ALONE, never the page
   ▼
E. PAGE COMPOSITE   grid_choreography.py — paper gutters, wobbled ink
   ($0)             borders, virtual page camera (spotlight sweep);
   │                layout per page, not one fixed skeleton
   ▼
F. COMIC TEXT LAYER code-drawn bubbles + parchment captions, overlaid
   ($0)             AFTER animation — POC VALIDATED TODAY (see below)
   ▼
G. ASSEMBLY         narration.mp3 + score + SFX + WhisperX captions for
   (existing)       spoken narration + landing hold + watermark
```

Stages A-E are the comic-strip-native spec's validated architecture, reused
as-is. Stage F is new, built and eye-checked today at $0.

## F. The comic text layer — what was validated today

`poc_thief_e2e/_comic_text_layer.py` → outputs + review:
`poc_thief_e2e/clips/_text_layer/` (`page2_with_text.mp4`, `_REVIEW.html`).

**Why text is code-drawn on top, never baked into the art (locked, spec §3):**
baked text garbles under animation ("FLESH UNT THE BUCKS OF HE AIR"), a typo
costs a re-render + re-animate instead of a free code fix, and baked text can
never be timed. This layer is the project's "AI draws, code writes" rule
applied to comic lettering.

**Element types (both demonstrated):**
- **Speech bubble** — ivory fill, hand-wobbled double ink outline, drop
  shadow, tail aimed at the speaker's MOUTH; Comic Sans Bold all-caps.
  Optional **red-letter** text for Christ's own words (printed-KJV
  convention — user to confirm this design choice).
- **Caption box** — parchment fill + wobbled ink border, Georgia italic;
  carries the narrator/attribution frames ("And Jesus said unto him,").

**Hard rules learned/enforced in the POC (candidate gate CSN-G7):**
1. **Text verbatim from `data/kjv_cache.json`, never from memory** — the
   cache caught "Dost **not thou** fear God" where memory said "Dost thou
   not."
2. **Speaker attribution is a doctrine check, not a style nit** — the POC's
   first render pointed the thief's rebuke at the Christ-figure; fixed with
   an off-panel tail. Every bubble's tail must trace to its true speaker
   (off-panel tails are legitimate comic grammar).
3. **Never cover the speaker's mouth/face with their own bubble** — Jesus'
   bubble moved below his face with a short upward tail.
4. Bubbles may cross panel borders/gutters (authentic comic grammar);
   captions anchor near the TOP of their cell.

**Known POC limitation (the one real engineering item left in F):** overlays
are static in page space while grid_choreography's camera pushes panels, so
placement had to be chosen safe-across-all-states. Production fix: draw the
text cell-relative INSIDE the choreography pass (text rides its panel), which
also gives per-word/per-bubble timing from WhisperX narration alignment for
free. Small, deterministic, $0.

## Formats

- **9:16 shorts** — validated end-to-end at the visual layer (Penitent Thief,
  3 pages). 12s/page at 4 panels; a ~60s short ≈ 3-5 pages or fewer pages
  held longer under narration.
- **16:9 long-form** — every piece of the chain is aspect-agnostic
  (nano_banana_pro takes `--aspect_ratio 16:9`, grid_choreography takes
  `--w/--h` + horizontal layouts like `3-big-left`, the text layer is
  geometry-only) — **but 16:9 is UNTESTED for native panel generation
  (spec §10.5). Needs one paid test page before planning long-form on it.**
- **Cross-aspect reuse** stays live: 9:16 panels fit 16:9 vertical grid
  cells per the locked `vertical-panels-cross-aspect-reuse` rule.

## Cost model (per 4-panel page, honest range)

| Item | Cost |
|---|---|
| 4 panel stills (NBP separate-stills path) | ~$1.20 |
| 4 panel animations, tiered (2 Hailuo + 2 Kling mix) | ~$4.10-4.40 |
| Composite + text layer + captions | $0 |
| **Per page, zero-reroll floor** | **~$5.50** |
| With the spec's honest 1-in-3 reroll rate | **~$7-9/page** |

A 3-page short ≈ **$17-27** visual layer (vs ~$23 full-episode budget of the
current pipeline — comparable). Long-form 16:9 scales linearly per page;
reuse-first discipline (existing banks) cuts real cost per episode.

## Gates

CSN-G1..G6 from the spec apply unchanged (no baked text; anchor fidelity;
Christ body gate on EVERY passion panel EVERY generation; canonical wording
only; multi-timestamp clip QC; layout compliance). Proposed addition:

| Gate | Checks |
|---|---|
| **CSN-G7 text layer** | every bubble/caption string byte-equal to its `kjv_cache.json` source; every tail traces to the true speaker (off-panel allowed); no bubble covers its own speaker's mouth; red-letter only on Christ's words |

G7 items 1 is trivially automatable ($0, string compare); 2-3 are eye-checks
until a Vision check exists.

## What a PAID POC should prove next (needs user OK — ~$6-9)

Today's $0 POC reused the crop-test page (panels cropped from a native page,
so resolution is the compromised path). One new page built the RIGHT way:

1. Pick the next beat (Penitent Thief page 3 equivalent, or a new story).
2. 4 separate full-res NBP panel stills, chained anchors (~$1.20).
3. Eye-gate, then tiered animation: calm panels Hailuo, action Kling
   (~$4.10-4.40 + rerolls).
4. grid_choreography composite + text layer + a narration-timed pass.
5. Multi-timestamp QC + this doc's G7 checks.

Open after that (from spec §10, unchanged): 16:9 test page, panel-layout
variety, full end-to-end assembly with audio, Seedream 5.0 Pro consistency
follow-up, Vision-check for the body gate, NSFW fallback path.

## Provenance

- Spec + all animation/still bake-offs: `COMIC_STRIP_NATIVE_SPEC.md`
  (2026-07-25, red-teamed same day).
- Text-layer POC (this doc's stage F): `_comic_text_layer.py`, outputs in
  `clips/_text_layer/`, $0 spend, eye-checked at 5 timestamps across 3
  render iterations (attribution fix, camera-drift fix, mouth-cover fix).
