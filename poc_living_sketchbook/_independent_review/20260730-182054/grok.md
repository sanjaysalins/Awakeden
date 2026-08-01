# Independent review — grok (OK, 123s)

I'll verify the plan against the real repo — existing engines, skills, POCs, and lettering rules — before writing an adversarial review.## Independent review — Round 6 promotion plan

Authority check first: the 9 KEEP / 13 KILL roster matches `C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\storm\ROUND6_VERDICTS.txt`. The creative read (hand / lamp / Word, not book-lore) is consistent with that sheet. The problems are in **promotion mechanics**, not in the taste verdict itself.

---

### Critical: false energy assumption (engine 1)

**Claim:** *"Production energy source: the held-breath envelope sampled over the entry's window — the narration's own fear drives the hand."*

**Reality:** `panel_animator/held_breath.py` returns **1.0 during speech** and dips toward a floor during **silences**. It is a silence damper, not a fear/panic meter. The skill says the same: it multiplies other devices during gaps.

The proven POC does the opposite of what the plan claims: it hard-codes story energy (`energy=0.85` panic on s01, `energy=0.08` calm on s10) in `_keeper_poc/_build_poc.py`. Wiring `energy_envelope` into `KeeperEntry` would make the hand **calm while the narrator is talking panic**, and **dip mid-sentence only at pauses** — the wrong dramatic map.

**Fix needed:** keep author/beat-tagged energy (or a separate beat-energy table). Use held-breath only as a secondary amplitude multiply on already-set energy, if at all — and say so.

---

### Critical: “promote, don’t rewrite” invents an API that doesn’t exist

**Claim:** promote `_keeper_poc/_build_poc.py` with API  
`KeeperEntry(lines, origin, size=64, energy, seed) → compose(frame, t)` plus `starve=…`, `interrupt_at=t`, `field_header(text)`.

**Reality:** the POC is free functions (`keeper_line`, `entry_events`, `compose_at`, `pencil_study`). Starve and interrupt live as one-off logic in `_vault_poc/_build_vault.py` (e.g. filter events `t < T_WORD`, `STARVE_N = 5`), not as a shared API.

That is a **new module design**, not a straight promote. Fine if honest; dangerous if people expect seed-stable byte clones of approved POCs after a class refactor.

---

### Critical: no production wiring step

Build order:

1. engines + self-tests  
2. demos + eye gate  
3. five new skills  
4. foley bank  
5. amend living-sketchbook §5  
6. panel this doc  

Missing: **one real episode path** that imports the engines into an assembler (Storm’s `_s4_assemble.py` or a shared assemble stage), mixes foley, and ships a cut.

Living-sketchbook already admits: *“None of the 10 ADOPTs are wired into a real assembler yet.”* This plan risks five more orphaned tools + five skills before any integrated proof.

Promotion without an end-to-end assemble step is not production; it is a second POC shelf.

---

### High: unproven transition siblings shipped as v1

**Claim:** v1 ships `torn_out` **plus** `slide_under` and `lift_away`, “designed to the same desk test.”

User verdict only kept **Torn-Out Page** and noted *“we can have more such transition effects.”* That opens a **lane**, not two designs.

Only `bold_2_torn_page` is proven. Shipping two unbuilt, un-eyed siblings in the same promote pass is premature and conflicts with the plan’s own “nothing ships without a new gate.”

Also: living-sketchbook §6 already has `paperRip` / `inkSwipe` / halftone; Storm already uses `TRANSITIONS = {23.55: "paperRip"}`. The plan never says whether `page_transitions.py` **replaces**, **extends**, or **duplicates** that path.

---

### High: “torn page” name collision

SKILL §1 landing device: **torn hole in the paper** with gold light (composition).  
Round-6 keep: **Torn-Out Page** = journal page ripped out as a transition.

Engine 5 also says *“never the landing spread (the torn page owns landing light)”* — which “torn page”? If both keep the same name, assemblers and authors will mix them. Needs distinct names (e.g. `landing_tear_hole` vs `torn_out_page`).

---

### High: LAW 1 vs §5 has no detection / enforcement path

**Claim:** Word Arrives Whole is LAW 1 + `interrupt_at`; enforcement lives in the “verse-compositing path”; this “DELIBERATELY revises §5’s universal letter-by-letter reveal.”

Gaps:

- §5 today: Scribed Ink is letter-by-letter for verse reveals.  
- No code path that decides “His speech” vs “narration-voice verse.”  
- Only one POC (`vault_1_word_whole`) demos the interrupt pattern.  
- The plan says “pending panel” but still treats the §5 change as part of the promote package.

Without a fail-closed rule (e.g. only when voice is Jesus/God **and** verbatim KJV **and** spoken speech), this becomes a soft style choice and will be applied inconsistently.

---

### High: foley path ignores existing infrastructure

**Claim:** each engine “exports” `pencil_scratch` / `drop` / etc.; bank one-shots; ask before ElevenLabs.

Already exists:

- `panel_animator/scriptorium_foley.py` + skill: `DEVICE_SOUND_MAP`, `Cue`, `build_foley_bus`, held-breath multiply, sidechain duck.  
- Explicit open gap: no real stationery bank; substitutes only; ElevenLabs only with user OK.  
- `frottage.foley_cues` already names `graphite_scratch`.  
- `paper_tear` already mapped for `paperRip` (`bread_tearing` substitute).

Parallel “export a cue” APIs that do not extend `DEVICE_SOUND_MAP` will duplicate foley wiring. Plan step 4 should be: **extend scriptorium-foley’s map + one shared cue schema**, not a fifth ad-hoc cue system.

---

### Medium: governors are prose, not gates

Limits like ≤1 keeper entry per spread, ≤4 + 1 header per episode, ≤1 bleed, ≤1 candle, never Word-page tear, never two hard transitions inside 10s are good taste rules.

This repo’s standing pattern is **$0 fail-closed lints** (`check_landing_hold`, panel variety, etc.). The plan only puts governors in SKILL text. Process governors fail under deadline; written rules without a check are not promotion-grade.

Voice governor (*“never doctrine claims… reviewed with the narration by the panel”*) is especially weak: Keeper text is free-form and can invent theology. Needs at least a checklist + panel on the **entry text list** before composite, preferably a deterministic “no verse-claim / no CTA verb” lint on keeper lines.

---

### Medium: self-tests uneven; engines 2–5 thin

Engine 1 lists real tests (jitter monotonicity, byte-stable after last event, starve alpha, interrupt).

Engines 2–5 get “with self-tests” in the build order only. No concrete asserts for:

- margin studies only from approved crop  
- never tear a verse-bearing page  
- bleed only on keeper ink bbox  
- candle anchor must hit a lit region  

POC scripts also hardcode Storm paths and lamp boxes (e.g. s04 lamp crop) — production needs a declared subject/region contract, not more hardcoded Storm coords.

---

### Medium: Two Hands “filmstrip governor” is manual SOP, not an engine

*“lanes planned against the CLIP’s motion… check the filmstrip, not just frame 0”* is correct and hard. It is **not** “an assembler pattern over engine 1” until the assembler has a lane-vs-motion checklist (or a margin-sentinel-style tool). As written, it is hope.

---

### Medium: cost claims are mostly right, slightly oversold

- Engines $0 per use: true (PIL/ffmpeg pattern, like other `panel_animator` tools).  
- One-time foley on quota with ask-first: matches standing rule and scriptorium-foley’s open gap.  
- *“The entire round… spent nothing”*: true for the **device POC batch**, not for Storm stills/clips that the demos sit on. Do not let that line become “living-sketchbook is free.”

Spending risk that is underplayed: **demo re-renders + user eye gate on every Storm spread at new scale**, then full reassemble if you actually prove integration. Still cheap vs Kling, but not “register five skills and done.”

---

### Low / documentation

- `_IDEA_VAULT.md` header still says Blind Emboss / Two Hands etc. are awaiting eye; ROUND6 already closed that. Citing the vault as kill authority without refreshing it will mislead the next session.  
- Five new slash-skills (`/keeper-hand` …) before one integrated episode over-weights docs relative to wiring. Prefer one skill section under living-sketchbook until the stack ships once.

---

### What is solid (for balance, not praise)

- Kill list matches the final sheet; “never re-pitch book-lore lane” is clear.  
- LAW 1 (Word asymmetry) and LAW 2 (scale) match the user’s notes and the bold re-render direction already in code (`BOLD = 1`).  
- Consolidating five hand behaviours into one instrument is the right shape **if** the energy source and promote API are fixed.  
- Acknowledging Word-Whole as law + interrupt, not a sixth engine, is correct.  
- Requiring external panel before lock matches the repo’s significant-plan rule.

---

### Bottom line

This is a strong **selection memo** dressed as a **production promote plan**. Selection is done. Promotion is not feasible as written: wrong energy source, invented promote API, unproven transition siblings in v1, foley that ignores `scriptorium_foley`, LAW 1 with no detector, governors without teeth, and no end-to-end assemble step.

Do not lock this plan until those are fixed.

VERDICT: REVISE  
TOP FIXES:  
1. Replace “held-breath = fear energy” with an explicit beat/author energy map (held-breath only as optional silence damp); rewrite engine-1 production energy language and tests.  
2. Add a mandatory build step: wire engines 1–5 into one real Storm (or next episode) assemble path and ship one cut before registering five skills; drop or demote `slide_under`/`lift_away` to post-torn_out gated POCs.  
3. Specify LAW 1 enforcement (when Word arrives whole vs letter-reveal), extend `scriptorium_foley.DEVICE_SOUND_MAP` instead of parallel cues, and add deterministic governor lints (counts, no tear on verse pages, keeper-text doctrine check).
