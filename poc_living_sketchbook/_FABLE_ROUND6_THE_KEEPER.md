# Fable — round 6: THE KEEPER (the promotion round) — 🔒 LOCKED 2026-07-30

> **LOCK RECORD.** User order: "lock it" (evening, after approving the engine
> regression pairs). Panel round 1: 5/5 REVISE → revised (all findings applied).
> Panel round 2 (`_independent_review/20260730-214250/`): cursor/claude/gemini
> REVISE, codex timeout, grok no-verdict — findings triaged below; NONE dispute
> the nine devices, the five engines, or the two laws. Locked with a tracked
> punch list, per the user's authority over disputes.
>
> **Round-2 dispositions:**
> - **TRACKED (the Round 6.1 punch list, before episode two ships):**
>   (1) assembler-integration: episode assemblers import `panel_animator` engines,
>   not `_build_*` POCs, and emit the Keeper-Entry Manifest JSON that
>   `keeper_lint.py` reads — the lint is inert until an emitter exists (claude #2,
>   cursor #1); (2) margin_sentinel runs on animated clips BEFORE keeper
>   compositing (cursor); (3) regression extended to keeper_C + two-hands
>   (cursor #3); (4) episode-level budget scheduling for bleed/candle/transition/
>   study folded into the lint.
> - **DECISION FOR THE USER:** foley one-shots — claude-reviewer is right that
>   clean pencil-scratch and dip/drop assets do NOT exist in the library (Storm
>   v6 shipped on substitutes). Quote: 3–4 ElevenLabs SFX one-shots on quota,
>   banked forever; ear A/B against the substitutes before adoption.
> - **ANSWERED (already the design; wording now explicit):** candle anchors are
>   HUMAN-pinned coordinates at the still-QC gate (never auto-detected) — gemini
>   #1; the interrupt/verse frame authority is the alignment word-onset quantized
>   to frame, consumed by BOTH keeper_hand.interrupt_at and the verse compositor —
>   gemini #2; the moving-clip filmstrip check belongs to the human assembly eye
>   gate, not the $0 lint — gemini #3; the lint's doctrine keyword list is a
>   FLOOR that only WARNs — the panel's semantic review at episode lock remains
>   the authority that CLOSES each WARN (gemini's brittleness point + claude #3),
>   per the standing both-ways doctrine rule.
> - Storm v6/v6.1's LAW 1 usage is now panel-processed rather than merely
>   flagged (cursor #2) — this lock record is that closure.

**Date:** 2026-07-30 · **Source:** the user's COMPLETE taste-gate verdicts
(`storm/ROUND6_VERDICTS.txt`, final sheet 18:16) over 22 POC devices built and judged the
same day — 9 KEEP, 13 KILL, 0 undecided. · **What this round is:** not exploration —
promotion. The nine survivors become production engines, governors, foley cues, and skills.
Nothing else from rounds 1–5's POC lanes ships without a new gate.

**Read first:** `ROUND6_VERDICTS.txt` (the authority), `_IDEA_VAULT.md` (kill record),
memories `round6-keeper-selection` + `feedback-device-must-live-in-the-book`,
`.claude/skills/living-sketchbook/SKILL.md` §5 (the lettering laws these extend).

---

## What the selections reveal (the creative take)

Look at the nine together: the Performing Handwriting, the Margin Studies, the Field
Header, the Torn-Out Page, the Bleeding Word, the Word Arrives Whole, the Inkwell Runs
Dry, the Candle-Only Spread, Two Hands at Once.

Every keep is one of three things: **the Keeper's hand acting** (writing, failing,
studying, tearing), **the desk's light** (the candle), or **the Word's authority**
(arriving whole). Every kill is one of two things: a **material trick** (aging,
erasing, breathing, weather, wax) or **book-lore across episodes** (flyleaf, emboss,
pricks, the second hand — the entire "long game" lane, killed to the last device).

The show's identity, as chosen by its owner: **one person, one page, one lamp, one
Word — tonight.** Not the book as an artifact with a history; the page as a live
performance. And the standing note on nearly every keep — bigger, bolder — says the
same thing: this is a SHOW, not an archive. Legible at arm's length, felt at phone
scale.

Nine devices consolidate into **five engines and two laws** — fewer modules than
devices because the hand is ONE instrument with many behaviours.

---

## The two laws (before any engine)

**LAW 1 — the asymmetry of the Word.** The Keeper's ink shakes, heaves, gets struck
through, skids, starves, bleeds, and can be torn out with its page. The WORD does
none of these — ever. It never writes letter-by-letter (human speed), never shakes,
never bleeds, never runs dry, never ages, and no page carrying it is ever torn,
erased, or transitioned violently. It does exactly one thing the Keeper's hand
cannot: **it arrives whole** — complete between one frame and the next. This law is
the entire doctrine of the lettering system, and every engine below enforces its
side of it. (KJV verbatim + formal register rules from §5 stand unchanged.)

**LAW 2 — the scale law (user, 2026-07-30).** Keeper-hand text is BIG and BOLD:
≥54px at 1080-width (56–64 standard), always with the extra stroke weight
(`BOLD = 1` in the engine — already applied and re-rendered across every kept POC).
Margin-study graphite runs at 1.9–2.3 contrast, never the ghostly 1.0 of the first
POC. If a mark is worth making, it is worth SEEING.

---

## The five engines (build cards)

### 1. `panel_animator/keeper_hand.py` — the flagship instrument
The Performing Handwriting + Field Header + Inkwell + the human half of Word-Whole +
Two Hands, one module. Promote the proven POC engine (`_keeper_poc/_build_poc.py`)
with its energy mapping intact — ONE number (0 calm … 1 panic) drives jitter, heave,
lean, pressure, burst-timing.
- **API:** `KeeperEntry(lines, origin, size=64, energy, seed)` → per-frame
  `compose(frame, t)`; `~~word~~` strikes; `skid=True`; `starve=(n_glyphs, blot_xy)`
  (the Inkwell behaviour); `interrupt_at=t` (the Word-Whole behaviour — glyph events
  after t never fire); preset `field_header(text)` (energy 0.15, size 60, top lane).
- **Production energy source (CORRECTED by panel, 2026-07-30):** energy is AUTHORED
  per entry in the episode's beat table — exactly as the taste-gated POCs did
  (0.85 panic / 0.08 calm were hand-set, and that is what the user approved).
  held-breath is a SILENCE damper (1.0 during speech, dips in gaps) and must NOT
  drive the hand — wiring it here would calm the hand mid-scream. It remains an
  audio-side amplitude multiplier only. A derived "fear envelope" is a possible
  future device with its own POC and gate, not part of this promotion.
- **Moving clips (Two Hands):** `compose` is already per-frame — the assembler runs
  it over clip frames. Governor: lanes planned against the CLIP's motion (a face may
  MOVE into a lane — check the filmstrip, not just frame 0).
- **Voice governor:** the Keeper's words are a human voice — questions and
  observations only, reviewed with the narration by the panel, never doctrine
  claims, never competing with a verse card on the same spread. ≤1 entry per spread,
  ≤4 entries + 1 header per episode: it is a journal, not subtitles.
- **Foley:** each entry exports a `pencil_scratch` cue for its write window
  (one-shot to bank once; dry-scratch + dip variants for starve).
- **Self-tests:** jitter(0.85) > jitter(0.1) on measured glyph offsets; byte-stable
  after last event; starve alpha strictly decreasing; interrupt leaves trailing
  glyphs unrendered forever.

### 2. `panel_animator/margin_study.py` — the doodle with a reason
Promote `pencil_study` + sweep reveal + leader line + keeper caption (LAW 2 contrast
locked in). Studies derive ONLY from the spread's own approved art — they can never
contradict the drawing. Governors: ≤1 cluster (2–3 studies) per episode; subject =
what the Keeper would fixate on (the narration names it); a study of the Face is
fail-closed to the user's eye. Foley: soft `graphite_scratch` under each reveal.

### 3. `panel_animator/page_transitions.py` — the family the user asked for
(REVISED by panel.) v1 ships **torn_out_page ONLY** — the one device the user's
verdict actually approved (grab → lift+shadow → rip away, deckle flash, rip cue at
release). The note "we can have more such transition effects" opens a LANE, not two
designs: **slide_under** and **lift_away** are named CANDIDATES that get their own
$0 POC round and the user's taste gate before any production code — the same gate
that killed 13 of 22 this week applies to my ideas too. Naming fix (grok): this
device is `torn_out_page`; the landing's torn-hole device is the `tear_hole` —
never the same words again. Relationship to §6 (cursor): this EXTENDS the existing
transition stack (paperRip/inkSwipe/halftone stay; torn_out_page wires through the
same assembler TRANSITIONS mechanism, not a parallel path). Every future candidate
must be a two-hand paper action; wipes, dissolves, CG curls die at the pitch.
Governors: NEVER a page carrying the Word; hard physical transitions at act turns
only; never two inside 10s.

### 4. `panel_animator/bleeding_word.py` — one drop, one word, once
Promote the bloom (radial wet darkening + edge dissolve + 2–3 descending trails).
Governors: Keeper's words only — the Word never bleeds (LAW 1); the bled word is THE
word the episode is about; ≤1 per episode; the drop lands on the word's own ink,
never on art. Foley: a single `drop` one-shot at impact.

### 5. `panel_animator/candle_only.py` — the light budget
Promote the radial grade (warm inside / cold-dark outside, soft 260px falloff,
flicker jitter on R). Anchor MUST be a drawn light source in the approved art (the
lamp, a fire, a torch) — the desk's lamp answering the page's lamp. R(t) is
energy-driven inverse (fear closes the light down; the turn opens it). Governors:
≤1 spread per episode; never the landing spread (the torn page owns landing light);
the source must survive the still's own QC first.

**Not engines:** The Word Arrives Whole is LAW 1 + `interrupt_at` — its enforcement
lives in the verse-compositing path (no write-on choreography for His speech;
Scribed Ink's letter-reveal remains for narration-voice verses only — this
DELIBERATELY revises §5's universal letter-by-letter reveal, pending panel).
Two Hands at Once is an assembler pattern over engine 1.

---

## The kill record (13 — never re-pitch, even rebranded)

Erasure · The Dive · Negative-Space Light · Entries Across Days · Permanence Split ·
Dog-Ear · Page Breathes · Rain-Shadow · Wax Seal · Blind Emboss · Flyleaf Census ·
Pricked Margin · Second Hand.

What the kills teach, so future rounds pitch better: (a) the whole
book-across-episodes lane is dead — seriality lives in the cast, the style, and the
CTA, not in book-lore props; (b) subtle died everywhere it appeared (breathes,
emboss, rain-shadow) — the taste gate wants VISIBLE and HUMAN; (c) even a
theologically gorgeous device (the Erasure) dies when the user's eye says no — the
gate is the gate.

---

## Build order (REORDERED per panel — governance before lock)

0. ✅ Panel round 1 ran (2026-07-30, 5/5 REVISE, `_independent_review/20260730-182054/`);
   this doc is the revision. ALL findings and verdicts go to the user, disputes marked
   (codex's correction to my earlier wording — accepted).
1. Engines 1–5 with self-tests. HONESTY FIX (claude/grok): "promote, don't rewrite"
   understated the work — starve falloffs, interrupt_at, candle R(t), and torn-page
   timing are hand-keyframed closures in the POCs; generalizing them into APIs is
   real design. Therefore the **regression rule**: each generalized engine must
   re-render the EXACT approved POC clips (keeper_A/B, vault_1, vault_4, v2_05,
   bold_2, bold_3) side-by-side against the originals, and the user eye-checks the
   PAIRS — "looks similar on fresh demos" does not count as "matches what was
   approved."
2. `keeper_lint.py` — new deterministic $0 governor (claude's catch, house pattern:
   every content rule gets a fail-closed script): counts entries per spread (≤1) and
   per episode (≤4 + header), checks lanes against logo/UI zones, flags any keeper
   text containing doctrine-adjacent phrasing (keyword list) for the panel, and
   flags keeper-mark collisions with verse cards. Runs before any episode lock.
3. Demos + user eye gate → SKILL.md registrations (`/keeper-hand`, `/margin-study`,
   `/page-transitions`, `/bleeding-word`, `/candle-only`).
4. Foley: map every cue to EXISTING sound_library assets first ($0); only if a cue
   has no usable asset, quote the ElevenLabs one-shots and ask before generating.
5. **§5 amendment gate:** the LAW 1 red-letter change to living-sketchbook §5 is
   written into the SKILL only AFTER the panel passes this revised doc. Retroactivity
   (claude): FORWARD-ONLY — shipped pieces are grandfathered (the landing-hold
   precedent); Storm v6 applies it now as the user-directed full-coverage
   demonstration, explicitly flagged as pending this gate.
6. Panel round 2 on the revised doc + the updated skill before production lock.

**Answered inline (gemini asked for mechanisms — they exist in code):** candle
anchors are authored per-spread coordinates from the still-QC pass (the POC's
`LAMP = (0.295W, 0.495H)` pattern), never auto-detected; the graphite conversion is
the proven invert–blur–dodge in `_build_poc.pencil_study()`; lane safety on moving
clips is the filmstrip check named in engine 1's governor.

**Cost:** $0 per episode-use across all five engines; foley stays $0 unless a
missing one-shot is quoted and approved. The entire round — 22 POCs, three review
pages, the selection system, this promotion, and its panel round — spent nothing.
