# Independent review — grok (OK, 126s)

I'll verify this plan against the real codebase — POC engines, skills, governors, and sound assets — before judging it.The engines and skills already exist on disk — I'm checking how complete the promotion is versus what the plan still claims is unfinished.# Independent review — Fable Round 6: THE KEEPER (promotion plan)

**Stance:** This is a *revision* of a 5/5 REVISE plan, not a blank slate. Several prior panel fixes are real (authored energy, `torn_out_page` only, naming vs `tear_hole`, regression pairs, §5 gate order). That does **not** make the plan production-ready. Gaps that block a honest “promotion” remain, and at least one rule would fail the very POCs the user KEPT.

---

## What improved (brief, not praise)

- Energy is **authored**, not driven by `held_breath` (engine 1) — matches the approved panic/calm POCs and avoids calming the hand mid-scream.
- Transitions v1 is **`torn_out_page` only**; `slide_under` / `lift_away` are candidates, not ship items.
- Naming: `torn_out_page` vs landing `tear_hole`.
- Relationship to §6 / assembler `TRANSITIONS` is stated (extend, not fork).
- Regression rule (side-by-side vs approved clips) is the right honesty fix for “promote ≠ rewrite.”

Those do not clear the remaining blockers.

---

## Critical findings

### 1. Lane lint would FAIL the approved KEEP placement (self-contradiction)

**Plan claim (build order step 2):**  
`keeper_lint.py` “checks lanes against logo/UI zones.”

**House rule already in code / skill:** bottom UI band = `y > 0.82 * H` (`keeper_lint.BOTTOM_BAND_FRAC = 0.82`; living-sketchbook §5 letterer laws).

**Approved KEEP POCs:** journal origin at `H * 0.878`  
(`storm/_keeper_poc/_build_poc.py`, `storm/_bold_poc/_build_bold.py` — same coords the skill demo still uses).

`0.878H > 0.82H` ⇒ a faithful lint **FAILS the taste-gated look**. The plan never reconciles “journal lives in the margin / bottom of the page” (what the user approved) with “bottom 18% is forbidden UI band” (caption/watermark law).

Until this is resolved (different band for *overlay captions* vs *in-world Keeper margin*, or a margin-safe zone, or an explicit exception with eye-gate), step 2 is not a governor — it is a landmine that rejects the show’s own flagship placement.

---

### 2. Still no production integration step (prior panel fix ignored)

**Build order is:** engines + self-tests → lint → demos/skills → foley → §5 amendment → panel round 2.

**Missing entirely:** wire engines 1–5 into a real living-sketchbook assemble path (e.g. Storm `_s4_assemble.py` / successor), run governors on a real cut, human-gate **one** finished episode before skill “production lock.”

Round-1 reviews already demanded this. The revision still promotes five modules + five skills without a single mandatory “ship one cut with all of them” step. Without that, “promotion” is library code + docs, not a production engine.

Repo check: Storm assemble still does not import `keeper_hand` / `bleeding_word` / `margin_study` / `page_transitions` as a unified path; only partial candle usage appears elsewhere. Plan does not close that gap.

---

### 3. Foley names invent a parallel vocabulary; library gap is understated

**Engine cards claim:**  
`pencil_scratch`, `graphite_scratch`, single `drop`, dry-scratch + dip variants.

**Existing subsystem (`scriptorium_foley.DEVICE_SOUND_MAP`):**  
`keeper_scratch`, `ink_drop`, `paper_tear`, `nib_scratch` — and the standing skill states **zero stationery/paper-craft recordings**; every map is a weak substitute pending ear approval.

Plan step 4 says “map to EXISTING sound_library first” (good), but the build cards never name the real keys or require registration in `DEVICE_SOUND_MAP` / `storm_cue_list()`. `margin_study` still exports `graphite_scratch` without a mapped asset path in the plan. Risk: parallel cue tables and silent no-ops, or ElevenLabs one-shots pitched as optional while substitutes are already known-weak and **not ear-locked**.

---

### 4. `keeper_lint` as specified covers ~¼ of the governors the plan asserts

| Governor in plan | In step-2 lint? |
|---|---|
| ≤1 entry / spread, ≤4 + header / ep | Yes |
| Logo / bottom band | Yes (but broken — finding 1) |
| Doctrine keywords WARN | Yes |
| Verse-card time collision | Yes |
| ≤1 bleeding word / ep | **No** |
| ≤1 candle spread; never landing | **No** |
| ≤1 margin-study cluster | **No** |
| Never tear a page carrying the Word | **No** (caller only) |
| Never two hard transitions in 10s | **No** |
| Face-study fail-closed | Human only (ok) but not scheduled |

The plan *sells* deterministic teeth (“every content rule gets a fail-closed script”) while most load-bearing governors stay “episode-design / caller responsibility.” That is the same soft pattern the house already learned is insufficient for LOCK.

---

### 5. Engine 2 (`margin_study`) has no regression pair in the honesty rule

**Step 1 regression list:** `keeper_A/B`, `vault_1`, `vault_4`, `v2_05`, `bold_2`, `bold_3`.

**Absent:** the lamp / margin-study cluster (`keeper_C` / pencil studies) that is half of engine 2’s claim.

Regression dir even imports `margin_study` “for completeness; no regression pair needs it.” So the plan’s “re-render EXACT approved POC clips” rule does not apply to one of the five engines. That engine also claims LAW 2 contrast **1.9–2.3** in the plan text, while the promoted module defaults to **2.6** and explicitly rejects the old 1.9/2.3 as pre-scale-law — the plan document is already stale against its own promotion target.

---

### 6. §5 amendment timing contradicts itself

- Step 5: LAW 1 change written into living-sketchbook §5 **only after** panel passes this doc.  
- Same step: “Storm v6 applies it now … pending this gate.”

You cannot both (a) treat §5 rewrite as gated and (b) run a user-facing full-coverage demonstration on the new law. Living-sketchbook §5 **still** mandates universal letter-by-letter Scribed Ink reveal. Production that follows the skill as written will fight engines that assume Word-arrives-whole. Single point of failure for any episode lock that pretends LAW 1 is binding.

---

### 7. LAW 1 enforcement is mostly narrative, not machine

Plan: “every engine below enforces its side of it.”

Reality in the design:

- **Bleeding Word:** “caller must only ever point `locate_word()` at a KeeperEntry” — no type-level or lint-level ban on verse cards.  
- **Torn-out:** “this class has no idea what a frame contains.”  
- **Word Arrives Whole:** lives in “verse-compositing path” with a **pending** §5 change and `interrupt_at` only on the Keeper side.

Doctrine-critical asymmetry depends on caller discipline + a skill edit that is not locked. For a project that demands fail-closed + both-ways review, that is a structural hole, not a polish item.

---

### 8. Skill registration is premature relative to proof

Step 3: demos + user eye → register `/keeper-hand`, `/margin-study`, `/page-transitions`, `/bleeding-word`, `/candle-only`.

That is five production skills **before**:

- assembler integration (finding 2),  
- ear-approved foley (finding 3),  
- §5 panel pass (finding 6),  
- full governor lint (finding 4).

Over-registration before the chain works. Skills exist as procedure docs; the plan treats registration as if it equals production readiness.

---

### 9. Manifest pipeline is unspecified

Lint needs a hand-authored JSON “keeper-entry manifest” with spreads, origins, sizes, time windows, verse cards. Plan never says:

- who writes it,  
- that the assembler is the single source of truth that **emits** it,  
- or that lock fails if manifest ≠ what was composited.

A free-floating manifest is easy to pass while the real cut violates counts/lanes — classic rubber-stamp gate.

---

### 10. Doctrine-keyword WARN list will cry wolf

If the lint follows the house pattern already on disk (`saved`, `sin`, `repent`, `believe`, `faith`, `lord`, `christ`, `god`, `spirit`, …), almost any honest journal line in a gospel episode WARNs. Panel fatigue → ignores. Not fail-closed; not high-signal. Plan does not define a tighter list or “question form only” heuristic.

---

### 11. Cost claim is directionally right, slightly oversold

**True:** per-frame engines are $0 (PIL/numpy); no metered image/video for the devices themselves.

**Weak:** “the entire round … spent nothing” + foley “$0 unless quoted” papers over (a) weak substitute ear-debt already documented in scriptorium-foley, (b) any future ElevenLabs stationery bank the skill already says is needed, (c) human eye time on 6+ regression pairs + Storm integration — not free in schedule, only free in API dollars.

Not a spend scandal; do not claim the audio side is production-finished at $0.

---

### 12. Moving-clip / Two Hands governor is unverified

“Check the filmstrip, not frame 0” is correct and still **100% human**, with no build-order slot (no `margin_sentinel`-style step before keeper composite on motion clips). Single failure mode: origin safe on still, face walks into the lane mid-clip. Plan names it; plan does not schedule it.

---

## Feasibility vs codebase (summary)

| Claim | Reality check |
|---|---|
| Promote `_build_poc` / vault / bold / candle POCs | Paths exist; generalization is real work (plan now admits this) |
| `panel_animator/*` five engines | Modules exist; plan still reads as “to build” while also answering “mechanisms exist in code” — doc is half-spec / half-post-hoc |
| Extend assembler `TRANSITIONS` | Stated; **not** a build step with a deliverable cut |
| `keeper_lint` house pattern | Matches `margin_sentinel` spirit; **lane rule fights approved art** |
| Foley via existing library | Names mismatch; stationery gap known; substitutes weak |
| LAW 1 into §5 | Still letter-by-letter in living-sketchbook §5; pending |
| Regression pairs | Exists for most listed clips; **not** margin_study |

---

## Over-engineering vs under-proof

- **Over:** five skills + lint + laws + kill record theater before one integrated cut.  
- **Under:** integration, ear foley, §5 lock, margin regression, fail-closed LAW 1, manifest emission.

Promotion should be: **one Storm (or next episode) cut with engines + lint + foley + eye gate**, *then* skill lock. The plan inverts that.

---

## Verdict rationale

Not **PASS** — lane/lint contradiction, missing integration step, incomplete governors, §5 timing conflict, foley naming/gap, margin_study regression hole.

Not **FAIL** — creative selection and engine consolidation match the KEEP set; prior worst smuggling (`slide_under`/`lift_away` as v1, held-breath energy) is fixed; direction is shippable after targeted revision.

**REVISE.**
