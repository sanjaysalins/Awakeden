# Swirls of Life — production pipeline design

2026-08-21. Answers: how do we stop writing one `render_the_X.py` per episode
without over-building before the format has proven itself. Decided with the
user: **formalize the scripts into one parameterized module now; do NOT
build full deterministic gates (SP-G/AS-G-style) yet** — the art+animation
recipe is still moving (see `NORTH_STAR_ANIMATION_PROMPT.md`'s OPEN ledger),
and gating a moving target is wasted engineering. Revisit gate-building once
4-5 full episodes have shipped clean. See `SWIRLS_OF_LIFE_SERIES_PLAN.md`
section 1 for the audience/takeaway/goal framing this pipeline serves.

## The real problem being solved

Six scripts exist today (`render_the_hem.py`, `render_the_thomas.py`,
`render_the_thomas_f01_v2.py`, `render_the_storm_f06.py`,
`render_the_storm_veo.py`, `render_f07_v2.py`), each ~150-350 lines, each
re-typing the same ~120 words of boilerplate (the "one single storyboard
page..." opening, the "No other text..." lock, the palette/style-negative
block, the page-global stillness fence, the no-bubble clause) with only the
per-page content actually varying. Every new episode currently means
copy-pasting one of these and hand-editing ~40% of it — real duplication
risk (a boilerplate fix, like the door-lock or anti-bubble wording found
2026-08-21, has to be hand-propagated to every file that needs it) and no
single source of truth for "what does a valid swirls page prompt look like."

**Not building:** a `Scene`/`ScenePlan`-compatible pipeline. A swirls page
(baked title + 3-panel row + one big illustration) is not a `cli_visual.py`
scene — one image, one clip. Forcing it into that model would be a worse fit
than the current one-off scripts. This pipeline copies `cli_visual.py`'s
*pattern* (plan → render → animate, deterministic boilerplate + LLM-authored
content), not its code or its classes.

## The Page spec — corrected scope, 2026-08-21

**First draft of this section (same day) over-claimed.** It proposed a
`MotifDose(kind, level, sub_case)` / `SwirlSpec(stage, source, behavior)`
pair that would *auto-generate* the stain/fray/swirl prose from a few
parameters. Checked against the real validated prompts (Hem F04/F05,
Thomas F01v2/F02) before writing the module, and that doesn't hold up: F04's
stain clause alone is ~120 words of scene-specific geometry — "lying around
and beneath the kneeling woman in the lower-right of the page, its soft
feathered edge reaching across the drawn frame border into the page's own
bottom-right margin, where it ends in a fine dried tide-line" — none of
which is derivable from `level="D2"`. A generator that only takes a dosage
level either produces something this specific (impossible without
re-inventing a scene-layout language as complex as prose) or produces
something generic enough to lose the exact grounding that makes these
prompts actually pass QC. Templating content that resists templating is
worse than not templating it — so the spec below only mechanizes what's
**genuinely identical across pages**, and leaves scene-specific description
as authored prose fields, same as today, just assembled through one shared
function instead of copy-pasted into a new file each time.

```python
@dataclass
class Panel:
    label: str                    # circled-number caption
    content: str                  # authored prose — what's drawn
    motion: Literal["light_only", "content_safe"]
    motion_detail: str = ""       # authored prose, required if content_safe

@dataclass
class PageSpec:
    seq_title: str
    frame_label: str              # "F01"
    panels: tuple[Panel, Panel, Panel]
    main_scene_still: str         # authored prose — shot type, setting,
        # characters, motif clause, swirl clause: everything the validated
        # scripts currently put in one long paragraph. NOT decomposed
        # further per the finding above.
    main_scene_animation: str     # authored prose — the "Large bottom
        # panel:" paragraph's content (character motion, NO_MOUTH, the
        # page-global fence's motif-specific callout)
    caption_lines: list[str]      # 1 or 2 stacked KJV-fragment lines
    corner_note: str
    refs: list[Ref]               # Ref(subject, path) per RECURRING subject —
        # character, object, artifact, AND location — each cropped from its
        # first approved render and chained into every later page it is on.
        # assemble_still_prompt appends a manifest ("image 1 is Jacob...;
        # image 3 is the field stone...") so the model knows which ref is
        # what; render_still hard-stops before spending if a path is missing.
        # Locked 2026-08-22 after the Jacob's Ladder pilot: with only a
        # full-figure Jacob ref, the beard, dress, stone, staff, ladder and
        # terrain ALL drifted across 8 approved stills. A face close-up ref
        # is needed in addition to a full-figure one for any character who
        # gets a close panel.
    model_tier: Literal["kling3_0", "veo3_1_lite"]
        # per the locked tiering rule: kling for any page needing a
        # completing gesture (a nod, a blink, a bow); veo for pure holds/
        # atmospheric pages. Chosen by the author, not inferred — the rule
        # needs judgment (NORTH_STAR_ANIMATION_PROMPT.md), not a heuristic.
    aspect_ratio: Literal["9:16", "16:9"] = "9:16"
```

`assemble_still_prompt(spec)` and `assemble_animation_prompt(spec)` stitch
the boilerplate constants below around the author's prose blocks in the
validated fixed order — replacing every hand-written `*_STILL_PROMPT` /
`*_ANIMATION_PROMPT` string constant with one shared assembly function, so a
boilerplate fix (the 2026-08-21 door-lock and anti-bubble wording, for
example) is made in exactly one place instead of hand-propagated across
files. Character BUILD strings (`_THOMAS_BUILD`, the Hem woman's build)
still move into one `CHARACTER_REGISTRY: dict[str, str]`, since those genuinely
are identical reusable text, just currently copy-pasted.

## Shared boilerplate library

Extracted verbatim from the validated scripts — these are genuinely
identical text today, just copy-pasted. One module-level constant/helper
each — none of these generate scene content, they only wrap the author's
prose blocks in the exact validated fixed structure:

- `STYLE_OPEN.format(seq_title, frame_label)` — "One single storyboard page
  of hand-drawn animation development art..." through the frame-number
  line, verbatim across all six existing scripts.
- `TEXT_LOCK` — "No other text, letters, numbers, or words appear
  anywhere on the page beyond the exact handwrite strings given above..."
  verbatim.
- `PALETTE_BLOCK` — the "Palette: black ink, ochre..." + "Not
  photorealistic, not anime..." style-negative paragraph, verbatim.
- `panel_prose(panels)` — assembles the "Across the top, a row of exactly
  three small storyboard panels..." sentence from the 3 authored
  `Panel(label, content)` values; the wrapping phrasing is fixed, only the
  3 panel descriptions vary.
- `page_global_fence(motif_callout: str)` — "every ink line and mark on the
  page is long set and stays exactly as drawn — including
  [motif_callout]..." — takes ONE authored phrase naming what the motif
  callout is (e.g. `"the broken, tremored linework of Thomas's figure"` or
  `"the grey stain beneath the woman"`), not a dosage level — the two-
  population lesson (a motif-local fence leaves the rest of the page
  unfenced) is baked into the wrapping structure, the specific callout stays
  authored.
- `NO_MOUTH_CLAUSE` / `LIPS_CLOSED_CLAUSE` — the two fixed phrasings for
  "this character's line IS the caption, no mouth movement" vs. "this
  character isn't speaking, compact lips-closed" — genuinely fixed wording,
  applied per-character by the author.
- `NO_BUBBLE_CLAUSE` — **flag, don't silently trust**: proven unreliable on
  Kling for two-line stacked captions as of 2026-08-21 (failed 3 consecutive
  attempts on Thomas F02 despite a strengthened version of this exact
  clause, holding clean the same day on a 1-line caption's earlier Hem
  pages). The module emits a runtime WARNING when `model_tier == "kling3_0"`
  and `len(caption_lines) > 1`, recommending veo3_1_lite instead — this is
  exactly the kind of institutional knowledge a hand-written script silently
  has and a new author would have to relearn the expensive way.
- `loaded_object_clause(object_desc: str)` — generalizes the 2026-08-21 door
  fix: any "loaded prior" panel object (a door, a nail) needs an explicit
  "the object itself never moves/opens/changes, only light across it
  shifts" clause, not just "light shifts across X" — takes the object's
  name, wraps it in the validated fixed phrasing.

**Deliberately NOT mechanized** (stays authored prose, per the correction
above): the stain/fray/swirl clauses themselves, character poses, scene
setting/blocking. These are where the actual creative and QC-passing work
lives; templating them would either fail to reproduce validated quality or
require a parameter language as complex as writing the prose directly.

## Long-form adaptation

Long-form doesn't use pages — per `SWIRLS_OF_LIFE_SERIES_PLAN.md` section 4,
it uses ~20-26 *spreads* paced per 7-movement envelope, with real clips only
on hero spreads (~1/3) and Focal Tour (`$0`, already `.claude/skills/
focal-tour/`) covering the rest. This means the long-form pipeline is NOT
"the same PageSpec at higher volume" — it's `PageSpec` (unchanged) for hero
spreads, plus a much simpler `FocalTourSpec` (already exists as
`focal-tour`'s own interface — reuse it directly, don't reinvent) for
everything else. No new data model needed for long-form; it's a scheduling
problem (which spreads are hero vs. Focal-Tour-only), not a rendering one.
That scheduling decision belongs in each long-form episode's own build step,
not in this module.

## Distribution — reuse wholesale, build nothing new

`_website/manifest.yaml`, `pipeline/release_state.py`,
`upload_tracker.py`, `production_board.py` are all style-agnostic — they key
off the narration folder + finished video file, not the art pipeline that
produced it. Once a swirls episode has a `narration/<title>/v1/` folder and
a finished cut in the same shape every other episode uses, it's already
visible to this machinery for free. **No swirls-specific distribution code
should ever be written** — if something doesn't fit, the fix belongs in the
shared release tooling, not a swirls-only fork of it.

## Migration path (validates the module at $0)

1. ✅ **Done 2026-08-21.** Built `poc_living_water_ink_style_test/
   swirls_page.py` with the spec + boilerplate above.
2. ✅ **Done.** Re-expressed Thomas F01 v2 (Fray fence, 1-line caption,
   no-bubble clause present) and Hem F04 (Stain fence, 2-line caption,
   no-bubble clause absent — the pre-fix page) as `PageSpec` objects, content
   sliced directly from the original validated constants (not retyped, to
   keep the check honest — it validates assembly logic, not transcription).
3. ✅ **Done, both PASS.** `_validate_swirls_page.py` (Thomas) and
   `_validate_swirls_page_hem.py` (Hem) diff the generated prompts against
   the exact hardcoded originals: **byte-identical on both**, across both
   fence families (fray/stain), both caption-line counts, and both
   bubble-clause states. Zero render spend. Keep these two scripts as
   permanent regression tests — re-run them after any boilerplate edit.
4. **Not yet done — the next real step.** Retire the one-off scripts only
   after one genuinely NEW page (not a re-expression of an old one) has
   rendered clean through the module — e.g. build 3's Peace Be Still
   Fray-on-disciples page. This costs real render spend; hold until the
   currently-open items (the live unexplained-spend flag, Thomas F02's
   still-unresolved animation) are settled, not bundled into this pass.

## What this explicitly does not do

- No deterministic SP-G/AS-G-style gate suite. That's real future work,
  correctly deferred (see the top of this doc) until the format stops
  changing every session.
- No independent-review wiring for individual pages (the SERIES PLAN still
  gets the 5-CLI panel; individual pages don't, same as today).
- No change to how episodes get animated/assembled into a final cut — that
  remains `northstar_shortform/`'s hand-built assemble script, forked per
  episode, until enough episodes exist to justify its own formalization
  pass (a separate, later decision, not bundled into this one).
