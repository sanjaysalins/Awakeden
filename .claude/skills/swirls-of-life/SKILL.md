---
name: swirls-of-life
description: Generate a hand-drawn ink-and-watercolor "animation development art" storyboard-page still for a Bible scene — one found-looking production page with a baked title, frame number, three labeled sketch panels, one large full-scene illustration, and short handwritten notes, plus the blue-and-gold "Swirls of Life" ink motif dosed across the episode to track its gospel turn. Character/object/location consistency comes from chained reference images (series-wide Jesus ref + fresh per-episode refs). Use when rendering any Bible scene as a storyboard-page still in this style (prototyped and validated on John 4, Jesus and the Samaritan woman). NOT for the clean no-baked-text /painted-comic style, NOT for the config baroque/graphic_novel styles, and NOT a $0 clip effect (see /line-boil, /print-grade for those).
---

# /swirls-of-life — ink-and-watercolor storyboard-page Bible stills

**Goal:** render a Bible scene as ONE page of hand-drawn animation development
art — delicate ink linework + watercolor on paper, laid out like a real found
storyboard page: a title top-left, a frame number top-right, a top row of three
small labeled sketch panels, one large full-scene illustration filling the
lower half, and short handwritten production notes tucked in naturally. The
page is (1) Scripture-accurate, (2) consistent shot-to-shot via chained
reference images, and (3) carries the **Swirls of Life** motif — blue (and
muted gold) ink that behaves like literal wet ink on paper and whose *dosage*
across the episode tracks how far the story has moved into the gospel truth.
Prototyped and validated on John 4 (Jesus and the Samaritan woman at Jacob's
well) at both 9:16 and 16:9, on Higgsfield's `nano_banana_pro`.

## Locked lessons (do not relitigate)

- **This style bakes text into the image ON PURPOSE — the OPPOSITE of
  `/painted-comic`.** Do not import painted-comic's "the art paints NO text,
  ever" rule here. The baked title, frame number, panel labels, and
  handwritten notes ARE the design — the page is meant to read as a real
  found piece of production art, not a clean overlay-ready plate. Validated:
  `nano_banana_pro` rendered every title, frame number, panel label, and
  handwritten note LEGIBLY across every John 4 test — **as long as each
  requested string is short** (a title phrase, "F04", a 2-4 word note).
  Never ask it to bake a sentence or a paragraph; long text is where legibility
  dies. Request each note explicitly as `handwrite: "..."`.
- **Reference images are mandatory for any multi-shot production — text
  description alone drifts.** A 4-page John 4 storyline generated with only a
  repeated text description of Jesus held *close enough* by luck; an earlier
  test with the same no-ref approach drifted Jesus into a completely
  different, older man on one panel. The fix is validated: crop a clean
  headshot of each recurring subject from an already-approved page and chain
  the crops into every subsequent generation with repeated `--image` flags
  (`nano_banana_pro` accepts up to 14; local paths auto-upload — see
  `hf model get nano_banana_pro`, param `image_references`). Test evidence:
  Jesus + woman headshot crops chained into a brand-new scene (different pose,
  sunset lighting, standing looking at a distant town instead of seated at the
  well) — both faces matched the crops closely. Same finding as
  `/painted-comic`'s Noah/ark lesson, independently re-proven in this style.
- **Every recurring subject gets a ref — characters, objects, artifacts,
  AND locations — not just the lead.** Locked 2026-08-22 after the Jacob's
  Ladder pilot shipped 8 approved stills with only one ref (Jacob, full
  figure): the stone went brown→grey, the staff grew a crook, the ladder
  changed wood, F07 became a green meadow, Jacob's tunic/robe inverted, his
  mantle became a cape, and his beard thickened on every close panel (a
  full-figure crop is too small to pin a face — add a FACE close-up ref for
  any character who gets a close panel). Mechanism: `swirls_page.Ref(subject,
  path)` per subject in `PageSpec.refs`, cropped from the subject's first
  approved render into the episode's `refs/`; the prompt gets an auto
  manifest ("image 3 is the field stone — ...") and `render_still` refuses
  to spend if a ref file is missing.
- **Score direction is a SERIES-WIDE reference bank, not a per-episode
  invention.** `SCORE_STYLE_BANK.md` (this folder) holds validated
  ElevenLabs Music prompts + audio samples (`references/score_bank/`) from
  the Jacob's Ladder pilot's 2026-08-22 bake-off — a "modern groove" /
  90s dream-trance-and-house direction, picked over this project's usual
  ambient-orchestral scores at the user's explicit request. Check it before
  generating a fresh score prompt for a new episode; regenerate the picked
  prompt at the new episode's own length rather than reusing the sample
  file verbatim (it's fitted to Jacob's Ladder's 62.04s). Its own mixing
  note is important: do NOT reuse `pipeline/score_mix.py`'s shared duck for
  a rhythmic groove — see that file for why and for the looser duck values
  that actually work.
- **Jesus's reference is a SERIES-WIDE constant; everything else is
  per-episode.** `references/jesus_ref.png` is established once, in THIS ink
  style, and reused across every future episode. Do NOT chain the main
  pipeline's Baroque-oil `ref_jesus_<variant>.png` — a photoreal-oil reference
  fights the ink generation. Every other character, key object, and key
  location gets a fresh episode-scoped ref (see Steps).
- **The Swirls of Life motif carries meaning through DOSAGE, not decoration.**
  Delicate blue ink lines / watercolor blooms / curls, sometimes with muted
  gold — always behaving like literal wet ink on paper, NEVER a magic-particle
  VFX glow. It is the story's own visual signal for the living water / the
  Spirit / the gospel truth entering the scene. Withhold it until the story
  earns it; its *presence*, never its literal size or brightness, signals
  progress. The validated 4-stage progression (see Steps) maps onto whatever
  narrative structure the episode already uses — it is a reusable device, not
  a John 4 schedule.
- **One page per prompt, not a sequence.** The validated pattern asks for a
  single storyboard page. Multi-page stories are built as independent calls,
  one per beat, with the refs chained into each.
- **Both aspect ratios are validated.** 9:16 and 16:9 both held the full page
  layout (title / F## / 3 panels / big scene / notes). Pick per destination.

## Steps

0. **Design the whole shot list as ONE pass, still + animation together, before
   rendering anything** (the "Fable design machine" — added 2026-08-20 per the
   user's own review of the first POC: "keep it simple, get very good at
   designing what's in the stills and what parts should be animated"). Dispatch
   a Fable-model design agent over the locked narration + `NORTH_STAR_PROMPT.md`
   + `NORTH_STAR_ANIMATION_PROMPT.md` and have it produce one table, one row
   per shot: the still prompt, the real animation prompt (every shot on a
   short gets real motion by default — see `NORTH_STAR_ANIMATION_PROMPT.md`'s
   "THE DEFAULT"), and the Focal Tour gap-fill plan for whatever time is left
   after that clip's natural length. Long-form (or an occasional short, to
   save credits) may instead choose to skip real motion entirely on a given
   shot — that's a genuine design-time exception, not the shorts default. This
   replaces discovering a shot's timing/motion needs AFTER the raw clip comes
   back wrong — it's all decided on paper, at $0, reviewed by eye, before any
   still or clip is generated. See `NORTH_STAR_ANIMATION_PROMPT.md` for the
   full template, the locked rule (the ink/swirl motif is NEVER an AI motion
   request), and the retroactive check against the 2026-08-19
   John 4 shots.
1. **Map the episode's own turning points to the four Swirls stages** before
   writing any prompt. Identify, from the locked narration itself: the
   setup/hook (Stage 0 — ABSENT: little to no blue), the inciting moment — the
   ask, the opening question (Stage 1 — FIRST TRACE: exactly one restrained
   thread/curl of blue, nothing more), the personal/complicating turn
   (Stage 2 — PRESENT: blue visibly there, still quiet, not spectacular), and
   the resolution (Stage 3 — DIFFUSED: blue woven through the whole scene, no
   longer tied to one figure, often paired with a crowd/community image).
   Write the stage next to each beat; every beat's prompt states its own dose.
2. **Establish new canon refs for a new episode.** `references/jesus_ref.png`
   already exists (series constant — if it doesn't yet, create it first the
   same way). For each OTHER recurring character, key object, and key
   location: generate a clean single-subject portrait/object/location shot in
   this ink style, eyeball-approve it at 1:1, crop it clean, and save it under
   an episode-scoped name — e.g. `references/john4_woman_ref.png`,
   `references/john4_well_ref.png`. Approved storyboard pages are a fine crop
   source (that is exactly how the John 4 refs were made).
3. **Write the page prompt from the validated template**, filling in per-beat:

   ```
   One single storyboard page of hand-drawn animation development art, ink and
   watercolor on paper. Top-left title, handwrite: "SEQ: <SEQUENCE NAME>".
   Top-right frame number, handwrite: "F<NN>". Across the top, a row of exactly
   three small labeled storyboard panels numbered 1, 2, 3: panel 1 <small
   sketch relevant to the beat>, panel 2 <...>, panel 3 <...>. Below them, ONE
   large full-scene illustration filling the lower half of the page: <the
   beat's main scene — subjects, action, setting, lighting, mood>. <SWIRLS
   DOSAGE LINE for this beat's stage — e.g. Stage 1: "a single restrained
   thread of blue ink curls from <element>, nothing more, like wet ink
   spreading on the paper">. Small handwritten production notes integrated
   naturally on the page, e.g. a corner note, handwrite: "<SHORT NOTE>".
   ```

   Keep every `handwrite:` string SHORT. State the Swirls dose explicitly on
   every beat — including Stage 0, where the prompt should say the page
   carries no blue ink motif, so a stray decorative swirl doesn't leak in
   before the story earns it.
4. **Generate with the refs chained** (Jesus ref on every shot he's in, plus
   the episode refs for whoever/whatever else recurs in the shot):

   ```
   hf generate create nano_banana_pro \
     --prompt "<full page prompt>" \
     --image .claude/skills/swirls-of-life/references/jesus_ref.png \
     --image .claude/skills/swirls-of-life/references/john4_woman_ref.png \
     --aspect_ratio 9:16 --resolution 2k --wait
   ```

   (`hf` = the Higgsfield CLI at `HF_CLI_PATH`, default `~/bin/hf.exe`.)
5. **Eyeball at 1:1 (Read the PNG), do not trust a thumbnail.** Check, in
   order: every baked string is legible and spelled right (title, F##, panel
   numbers, each note); faces match the chained refs; the layout held (3
   panels top, one big scene below, notes present); the Swirls dose matches
   the beat's stage — no blue before Stage 1, only ONE thread at Stage 1, not
   spectacular at Stage 2, genuinely woven-through at Stage 3, and always
   wet-ink-on-paper, never a glow/particle effect. Regenerate on any fail.

## CLI reference

| flag | value | note |
|---|---|---|
| model | `nano_banana_pro` | still model, ~2 credits/still (ledger is truth) |
| `--image` (repeat) | `references/jesus_ref.png` + episode refs | up to 14; auto-uploaded from local path (`image_references` param) |
| `--aspect_ratio` | `9:16` or `16:9` | BOTH validated for the full page layout |
| `--resolution` | `2k` | |

## Guardrails

- **Cost** — ~2 cr/still; budget for regens (baked-text misspellings and
  dosage leaks are the likely systematic failures). The ledger (`/cost`,
  `/spend`) is the only truth.
- **References required** — a shot with a recurring subject generated without
  its chained ref silently loses consistency; treat a missing ref as a hard
  stop, exactly as `/painted-comic` does.
- **Eyeball-QC is mandatory** — Read every PNG at full resolution; a thumbnail
  will pass an illegible note or a drifted face that 1:1 catches. This
  project's standing rule (`always-independent-red-team`,
  `feedback-verify-by-looking-not-running`) applies with extra force here
  because the baked text is load-bearing.
- **Known transient failure: Higgsfield 503.** The one real failure mode seen
  in validation was an occasional transient 503 from Higgsfield — it
  auto-refunds and a plain retry succeeds. It is NOT a prompt problem; do not
  rewrite the prompt in response to one.
- **Short strings only** — the legible-baked-text capability is validated for
  short phrases, frame numbers, and 2-4 word notes. Do not escalate to
  sentences/paragraphs on the strength of this skill; that is outside what was
  tested.
- **Before this ships at series scale**, run the same kind of independent
  red-team eyeball pass `/painted-comic` flags — every red-team round on that
  style found errors eye-QC had passed, and this style adds spellable baked
  text as a whole new error surface. One validated episode (John 4) is a
  prototype, not production proof.
