# Independent review — cursor (OK, 94s)

## Adversarial review — Fable Round 6: THE KEEPER

### Feasibility vs. real codebase

**1. “Promote `_keeper_poc/_build_poc.py`” is only ~40% of engine 1.**  
The plan says engine 1 comes from one POC file (“Promote the proven POC engine (`_keeper_poc/_build_poc.py`)”), but the kept behaviors live in four separate scripts:
- Handwriting / field header / margin studies → `_keeper_poc/_build_poc.py`
- Word-Whole + Inkwell + scribed verse → `_vault_poc/_build_vault.py`
- Bleeding + torn page → `_bold_poc/_build_bold.py`
- Candle + Two Hands → `_vault2_poc/_build_vault2.py`

`starve=(n_glyphs, blot_xy)` and `interrupt_at=t` are **not** in `_build_poc.py`; Inkwell starve is post-processed glyph alpha in `vault_4`, and Word-Whole is event filtering + `scribed_verse_layer()` in `vault_1`. “Promote, don’t rewrite” understates a real merge/refactor.

**2. Production energy source misidentifies an existing tool.**  
> “Production energy source: the held-breath envelope sampled over the entry's window — the narration's own fear drives the hand.”

`held_breath.energy_envelope()` is a **silence-damping** function: 1.0 during speech, dips toward `floor=0.25` in alignment gaps ≥0.35s. It is not a fear curve. Storm’s actual fear arc is hand-authored (`storm_tide_curve()` in `_s4_assemble.py`, comment: “rises with the fear, freezes under Scripture…”). POC panic uses explicit `energy=0.85`, not held-breath. Wiring keeper jitter to held-breath would make the hand **calmer in narrational silences**, not more afraid at “waves breaking over the rail.”

**3. “Word-Whole enforcement lives in the verse-compositing path” — which path?**  
There are already **three** scribed-ink implementations:
- `_s4_assemble.py` → `scribed_ink_card()` (production assembler)
- `_vault_poc/_build_vault.py` → `scribed_verse_layer()` (POC, instant pop-in)
- `_lettering_compare/_render_candidates.py` → `render_scribed_ink()` (referenced by §5)

The plan does not name the integration point, how instant-arrival mode is selected vs. letter-by-letter, or how word timing from alignment is preserved when reveal choreography is removed.

**4. Two unproven transitions ship in v1.**  
> “v1 ships **torn_out** (proven…) plus two siblings… **slide_under**… **lift_away**”

Only `bold_2_torn_page` exists as a POC. `slide_under` and `lift_away` have **zero** reference implementations. The user note was “we can have more such transition effects” — that opens a lane, it does not approve two specific unbuilt siblings for v1. This violates the plan’s own “promotion, not exploration” framing in the opening paragraph.

**5. Hardcoded Windows font paths propagate silently.**  
POCs use `C:/Windows/Fonts/Inkfree.ttf`, `KUNSTLER.TTF`, etc. The plan never mentions font discovery/portability. Every existing `panel_animator/` module that ships will hit this on Linux/CI unless addressed in promotion.

**6. Candle “anchor MUST be a drawn light source” has no detection step.**  
The candle POC hardcodes `LAMP = (W * 0.295, H * 0.495)` on `s04_asleep.png`. There is no algorithm, QC checklist item, or fail-closed gate for “find lamp in approved art” — only a governor sentence. Production will devolve into per-still hand coordinates (same fragility as `FAITH_BBOX` / `STILL_WATER_HORIZON` in `_s4_assemble.py`).

---

### Hidden risks & single points of failure

**7. LAW 1 vs. existing landing grammar is unresolved.**  
LAW 1: “no page carrying [the Word] is ever torn… transitioned violently.”  
`living-sketchbook/SKILL.md` §1: landing = “**The torn page** — a doorway/tomb/veil rendered as a TORN HOLE…”  
§3: “LANDING spread: the torn-page device + sacred stillness.”  
If the landing carries Christ/verse imagery, governors collide. The plan assigns landing light to torn page (“never the landing spread” for candle) but never reconciles torn landing with “Word pages never torn.”

**8. Two Hands on moving clips + no margin_sentinel in the chain.**  
The plan says compose runs per-frame over clip frames and governors must “check the filmstrip, not just frame 0.”  
The repo already has `margin_sentinel.py` + skill: run on **raw** animated clips before paper-layer compositing, because Kling invents margin marks (s09_rebuke defect). Keeper overlays write **into** those margins. The plan never requires sentinel before keeper compositing, so you can get keeper ink composited on top of (or competing with) animator hallucinations — the exact defect class that shipped four review rounds.

**9. Voice governor has no build step.**  
POC docstring: keeper words are “**PLACEHOLDER VOICE** for taste only — **panel review** before anything ships.”  
Build order (steps 1–6) has demos, skills, foley, §5 update, external panel — but **no** keeper copy authoring, narration panel review, or doctrine gate for keeper journal text before production use. “Voice governor” is policy without procedure.

**10. §5 amendment can land before the panel that must approve it.**  
> “DELIBERATELY revises §5's universal letter-by-letter reveal, **pending panel**”  
Build order: step 5 updates `living-sketchbook/SKILL.md`; step 6 is external panel review. If executed literally, the binding lettering law changes **before** the mandated SIGNIFICANT-plan review.

---

### Over-engineering / premature build

**11. Five new modules + three skill registrations before assembler proof.**  
`living-sketchbook/SKILL.md` §5b still says: “**None of the 10 ADOPTs are wired into a real assembler yet**.”  
This plan adds five engines and skill registrations but **no step to wire into `_s4_assemble.py`** (or a shared assembler). Demos on Storm spreads at new scale (step 2) do not prove episode-level timing, overlay exit margins (§5 letterer law: overlay bleeding 0.6s into next spread’s face), or governor caps across 10–14 spreads.

**12. `page_transitions.py` duplicates an existing transition stack.**  
`_s4_assemble.py` already has `TRANSITIONS = {23.55: "paperRip"}`; Jericho/Two Goats use `paperRip` / `inkSwipe`. `scriptorium_foley.py` already cues `paper_tear` for paperRip. A parallel “two-hand paper action” family with no migration/coexistence rule risks two transition systems, double-tear foley, or assembler ambiguity at act turns.

**13. Parent skill is still DRAFT.**  
`living-sketchbook/SKILL.md` header: “**Status: DRAFT** (not yet panel-locked).” Promoting five production engines + amending §5 while the parent skill is explicitly not locked inverts the repo’s gate order (engines before the container skill is authoritative).

---

### Missing steps, edge cases, verification gaps

**14. No episode-level scheduler for governors.**  
Caps are scattered: “≤1 entry per spread, ≤4 entries + 1 header per episode”, “≤1 cluster (2–3 studies) per episode”, “≤1 per episode” (bleed, candle), “never two [transitions] inside 10s”. Nothing plans **how** an episode author picks which spread gets the single bleed, the single candle, the header, and up to four entries without collision. Self-tests on individual engines don’t enforce cross-device budgets.

**15. Bleeding word targeting is brittle in the only POC.**  
`bold_3_bleed` locates “fear.” by manually summing `textlength()` offsets. Engine API doesn’t specify word-index or glyph-range targeting — only “the bled word is THE word the episode is about.” Production will repeat the FAITH_BBOX class of hand-maintained coordinates.

**16. Foley step contradicts existing foley architecture and cost claim.**  
Step 4: bank `pencil_scratch`, `drop`, `rip` — “**ElevenLabs quota, ask-before-generating**.”  
`scriptorium_foley.py` explicitly: “**No ElevenLabs, no new generation**” and documents that **no textural scratch asset exists** (nib_scratch uses high-pass gravel as a hack). Step 4 is spend-bearing and bypasses the existing `$0` cue-list + `build_foley_bus()` integration path.  
Cost footer: “**$0 per episode-use**… entire round… **spent nothing**” — false once step 4 runs, and it ignores that Storm stills/clips under the POCs were not free to produce.

**17. Missing verification for LAW 1 and letterer laws.**  
Self-tests listed (jitter ordering, byte-stable, starve alpha, interrupt) don’t test: Word never bleeds, Word never torn, type never covers a face, watermark zone, hard exit before next spread. Those are the failures §5 documents as already shipped twice.

**18. Margin study on **moving** clips is unspecified.**  
POC crops a **still** lamp region (`lamp_box = base.crop(...)`). On Two Hands spreads, the “detail the Keeper fixates on” moves. `pencil_study(src, …)` needs a stable crop strategy (first frame? tracked bbox? still-only governor?) — not stated.

---

### Reuse failures

**19. Does not extend `scriptorium_foley.py`.**  
Existing pattern: devices export schedules → `storm_cue_list()` → `build_foley_bus()` with held-breath ducking. Plan says each entry “exports a `pencil_scratch` cue” but never says to register devices in scriptorium’s cue map — parallel one-off foley instead of reuse.

**20. Duplicates scribed-ink / transition work instead of extending it.**  
Word-Whole should be a mode flag on the existing scribed path (assembler + §5 grammar), not orphaned in `keeper_hand.py` (“Not engines: … lives in verse-compositing path”). `ink_transition.py` and assembler `paperRip` already exist; `page_transitions.py` doesn’t say build on or replace them.

**21. `margin_sentinel` and `held-breath` exist but aren’t in the promotion chain.**  
Held-breath is misassigned as fear source; margin-sentinel is omitted entirely despite being the exact tool for “writing on margins of animated clips.”

---

### Cost / spend justification

**22. “One-time foley one-shots on quota” is underspecified and opt-in spend without ROI proof.**  
Scratch/rip may be hackable from `sound_library` (veil_tearing for rip is already mapped for paperRip). Plan jumps to ElevenLabs generation without a `$0` library-first attempt — inconsistent with scriptorium-foley’s standing approach and the project’s ask-before-spending rule.

**23. Scale re-render cost is hidden.**  
User verdict: “TEXT BIGGER AND BOLDER — sizes up ~1.35x” (`ROUND6_VERDICTS.txt`). Step 2 “Demos on the real Storm spreads at the new scale → user eye gate” implies re-compositing/re-encoding all keeper demos. That’s time-cost, and any still-dependent coordinate (candle anchor, bleed target, lane positions) must be re-authored — not accounted for.

---

### What the plan gets right (for balance)

- Grounded in real verdicts (`ROUND6_VERDICTS.txt`: 9 KEEP / 13 KILL).
- LAW 1 (Word vs. Keeper asymmetry) matches the strongest POC insight (`vault_1_word_whole`).
- Consolidating nine devices toward fewer engines is directionally sane.
- Governors on bleed/candle/torn+Word are copied from POC review HTML, not invented.
- External panel review is named (even if sequenced wrong).

---

VERDICT: REVISE  
TOP FIXES:  
1. Replace “held-breath = fear” with an explicit episode energy source (reuse the `storm_tide_curve` pattern or a named fear envelope from alignment/beats); document how it maps to `energy` 0…1 — do not wire keeper jitter to silence damping.  
2. Reorder build: external panel review of this plan + §5 amendment **before** skill lock or unproven builds; v1 = promote **proven** POCs only (`torn_out`, not `slide_under`/`lift_away`); add a concrete assembler integration step (`_s4_assemble.py` or successor) with governor enforcement and margin_sentinel before keeper compositing.  
3. Publish a POC→module consolidation map (four `_build_*.py` sources → five engines + scribed-ink mode flag); extend `scriptorium_foley.py` for cues; attempt `$0` sound_library mapping before any ElevenLabs one-shots; reconcile `page_transitions.py` with existing `paperRip`/§6 transition stack.
