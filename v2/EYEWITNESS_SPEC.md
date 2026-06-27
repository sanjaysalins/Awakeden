# AWAKEDEN — Eyewitness Format SPEC (binding contract)

> The binding contract for Awakeden's eyewitness format (short + long). The `/witness*`
> skills are the procedures that enforce it; the verification (`cli_witness_lock` + the
> deterministic gates) is the fail-closed teeth; the 5-CLI panel is the outside review.
> When this spec and a skill disagree, **the spec wins** — update the spec, don't drift.
> Companion: `v2/EYEWITNESS_FOUNDATION.md` (the roadmap). Brand: **Awakeden**.

---

## 1. Scope & forms
A first-person biblical **witness** recounts a moment they lived, and the piece turns to
reveal it was a shadow of **Christ**, landing the CTA **on Jesus**. Two forms, one DNA:

| Form | Runtime | Spoken words | Cut |
|------|---------|--------------|-----|
| **SHORT** | ~75–110s | 220–320 | slideshow / boomerang stills |
| **LONG**  | ~9–11 min | 1300–1650 | slow-boomerang veo3 animation |

Only the **script length** and the **cut timing** differ; voice / stills / score / sfx /
caption / publish are shared, format-agnostic modules.

---

## 2. The eyewitness spine (7 beats — the skeleton)
Told *as the witness*. LONG hits all 7, in order. SHORT compresses to **B1 → B3 → B6 → B7**
(hook → the act → the reveal → the invitation) but may touch the others.

1. **"I was there"** — hook: the witness names themselves + the moment.
2. **The world** — who they were, the weight of it.
3. **The act** — the ritual / event in their own hands.
4. **The strange detail** — the thing they never understood (the freshness hook).
5. **The wrestling** — their honest doubt / question (the steel-man objection, *internalized*).
6. **The reveal** — Christ. The type→fulfillment named: *"and at last I understood…"*
7. **The invitation** — grace-anchored CTA, **on Jesus**: "Come."

---

## 2.1 The `narration.md` file format (what the gates parse)
```
# <Title> — Awakeden eyewitness (<short|long>)
**Witness:** <name>  ·  **Core text:** <ref>  ·  **Type→fulfillment:** <Christ link>
**Status:** <draft/lock notes>
---
## Beat 1 — I was there
<first-person witness prose…>   **"<verbatim KJV>"**   <…prose>
**[the LORD]** <a quoted spoken line from a named speaker — dialogue>
## Beat 2 — The world
…
## Beat 7 — The invitation
… come to **Jesus** …
```
- Everything after the first `---` is spoken. `## Beat N — <name>` headers mark the spine
  (gate EW-G2). `**"..."**` = a KJV quote (gate EW-G1, read by the `scripture` voice).
- `**[Speaker]**` at the start of a line = a dialogue line routed to that VOICE_MAP voice at
  the `/witness-voice` stage (the witness is the default voice for untagged prose). **A divine
  speaker (`[the LORD]`/`[God]`/`[Jesus]`) line MUST be a verbatim `**"..."**` KJV quote** —
  no invented divine speech (EW-G11).
- SHORT may use fewer beat headers (≥ hook/act/reveal/invitation); LONG uses all 7.
- The folder MUST contain a **`passage.txt`** (the episode's narrow KJV pericope + its named NT
  cross-refs) — EW-G1 verbatim-checks every quote against it (fail-closed if absent).
- Banned as spoken text: the templated reveal stinger **"at last I understood"** (vary the turn).

## 3. Invariants (EW-INV — never violate)

> **🔒 TWO NON-NEGOTIABLES (user, 2026-06-26) — above everything below:**
> **(A) Sound doctrine, proven BOTH ways.** Doctrine must be sound and grounded in
> the Bible, and verified BOTH independently (red-team/self-check) AND by the 5-CLI
> panel — never one alone; reject if EITHER flags a real doctrinal/grounding error.
> Strengthens EW-INV-4/7 and §10. **(B) The whole Bible, through Jesus.** Read the
> entire canon (OT + NT) with Christ as the lens; every piece traces its thread to
> and lands on Jesus (EW-INV-2/3). The spine, never optional.

- **EW-INV-1 First-person witness.** Narration is spoken in first person by a named biblical
  witness (or a justified, labelled composite), never the detached essay narrator.
- **EW-INV-2 CTA on Jesus.** The close names **Jesus/Christ** and invites to Him;
  grace-anchored (no fear / gain-loss / manufactured pressure); no banned bare "will you
  trust Him?" template; the response (faith / come / turn) is named.
- **EW-INV-3 The reveal is explicit.** The piece turns from the witness's experience to
  Christ and names the type→fulfillment; never left implicit.
- **EW-INV-4 KJV verbatim.** Every quoted verse is span-checked verbatim; attribute before
  quoting; a dedicated **scripture** voice reads all KJV quotes.
- **EW-INV-5 Spine present & ordered.** LONG = all 7 beats in order; SHORT = at least
  hook → act → reveal → invitation, in order.
- **EW-INV-6 Multi-voice cast.** witness (lead) + scripture + **≥1** other named voice
  whenever the story has speakers (the LORD / Jesus / a son / a messenger / the people).
- **EW-INV-7 Doctrine sound.** No supersession; name the **substitution** (penalty + what
  Christ bore); freshness = faithful depth (surprising about the *text*, never the *truth*).
- **EW-INV-8 Word budget per form.** SHORT 220–320; LONG 1300–1650 spoken words.
- **EW-INV-9 One witness, one spine.** Do not swap the witness or the thread mid-piece;
  reshape lines instead.
- **EW-INV-10 Reuse-first.** A world-manifest checks the reuse banks BEFORE rendering;
  log what is reused vs generated (the cost lever).
- **EW-INV-11 No fabricated Scripture or speech (DOCTRINE — the format's core hazard).**
  (a) **God / the LORD / Jesus get NO invented dialogue** — any divine-tagged line must be a
  verbatim KJV quote (EW-G11). (b) Invented human interiority is clearly *interpretive*, never
  asserted as historical fact, never contradicts Scripture, never claims revelation the text
  doesn't grant; the cross-time reveal (an OT witness "seeing" Christ) is a **signposted
  reflective device** — the witness sees by the Spirit's later light, never "in that moment I
  knew the crucifixion." (c) The reveal must name Christ explicitly and avoid the templated
  stinger "at last I understood" (EW-G12). Distilled from the red-team; the channel's whole
  brand is "reverent, Bible-driven."

---

## 4. Gate registry
Deterministic gates run in Python and are **fail-closed** (block the LOCK). Panel gates are
the outside 5-CLI review (advisory unless they converge on a real defect).

**Deterministic (block LOCK) — `pipeline/eyewitness_gates.py` + the cluster check in the lock:**
- **EW-G1 KJV-strict** — a per-episode **`passage.txt`** (the narrow pericope + named NT
  cross-refs) is **REQUIRED**; every `**"..."**` quote must be a **verbatim substring** of it.
  No quotes-without-passage, no whole-cache fallback (that let a wrong-book quote pass as
  "attributed"); a fabricated/altered/misattributed quote FAILs (not "ignored as paraphrase").
- **EW-G2 Spine coverage** — LONG: 7 beats present & ordered; SHORT: hook/act/reveal/invitation present.
- **EW-G3 Word budget** — within the form's range (§1 / EW-INV-8).
- **EW-G4 CTA-on-Jesus** — closing beat names "Jesus"/"Christ" **and** an invitation verb,
  **and** no banned bare-CTA template, **and** no fear / gain-loss / manufactured-pressure
  phrase (EW-INV-2).
- **EW-G5 First-person** — first-person markers above a raw floor **and** a **density** floor
  (markers per 100 spoken words) — catches the essay-narrator-in-costume (a few sprinkled "I").
- **EW-G6 Cast present** — ≥2 voice roles; the scripture voice carries every KJV quote.
- **EW-G11 Words-of-God (DOCTRINE)** — any divine-tagged `**[the LORD]**`/`**[God]**`/
  `**[Jesus]**` line must carry a verbatim KJV quote; invented divine speech FAILs.
- **EW-G12 Reveal sound (DOCTRINE)** — the reveal beat **body** names Christ explicitly; the
  templated stinger "at last I understood" (and variants) is banned as spoken text.
- **EW-CLUSTER (cross-episode, in the lock)** — blocks a slate of near-identical episodes by
  comparing content n-grams against sibling narrations (the skeleton headers are whitelisted).

**Panel (5-CLI outside review):**
- **EW-G7 Reveal earned** — the type→Christ turn is shown from the text, not merely asserted.
- **EW-G8 Wrestling real** — the witness's doubt is the genuine steel-man, internalized (not a strawman).
- **EW-G9 Doctrine** — sound; substitution named; no supersession; KJV attribution correct.
- **EW-G10 Voice/character** — the witness voice is consistent, characterful, first-person —
  not the essay narrator wearing a costume.

---

## 5. Voice cast conventions
- `witness` — the lead, a distinct characterful voice per witness (weathered/aged as fits).
- `scripture` — one dedicated KJV-reader voice for ALL quotes (every form, every episode).
- Named others — `the_LORD` / `jesus` / `son` / `messenger` / `people` etc. from the VOICE_MAP,
  one per quoted speaker in the story (maximize multi-voice, INV-7).
- The witness ≠ the_LORD voice (keep the divine voice distinct).

---

## 6. Word budgets & pacing
- SHORT 220–320 spoken words → ~75–110s at the natural multi-voice pace.
- LONG 1300–1650 spoken words → ~9–11 min (the eyewitness earns slightly more than the essay
  long's 950–1400; the cast + interior beats fill it).
- Natural pace; never time-stretch the voice. Boomerang fills long visual windows.

---

## 7. World-manifest & reuse (EW-INV-10)
Per episode, before any render:
1. List the scenes (the witness face + their moment + the type + the Christ-reveal + hero).
2. **Reuse check** — `clip_reuse.decide_for_scene` (clips) + `image_library` (stills) +
   sound/music libraries; honor aspect (9:16 short / 16:9 long) + the topical-fit Gaza rule.
3. **Generate only the gaps** — usually the witness's own face + their specific moment.
4. Write `world_manifest.json` logging reused vs generated (the cost ledger input).

---

## 8. Pipeline stages → skills
| Stage | Skill | Output |
|-------|-------|--------|
| 0+1 Study + Script | **`/witness`** `--form short\|long` | locked eyewitness `narration.md` |
| 1b Voice | **`/witness-voice`** | duration-locked multi-voice `narration.mp3` |
| 2 World + Stills | **`/witness-world`** | `world_manifest.json` + rendered/​reused stills |
| 3 Cut + Finish | **`/witness-cut`** `--form short\|long` | scored, sfx'd, captioned cut |
| 6 Publish | **`/publish`** (reused) | Awakeden social PUBLISH PACK |

Reused engine (subprocess, never reimplement): `per_turn_synth` (voice), the 16:9/9:16 stills
renderer + reuse banks, `_assemble_16x9` / the shorts assembler, `_add_score_lf` / music_library,
the sfx builders, `veed_io.caption`, `cli_publish`.

---

## 9. Verification (the fail-closed chokepoint)
`cli_witness_lock.py <folder> --form short|long` runs **EW-G1..G6 + G11 + G12 + the
cross-episode CLUSTER check**; on 0 blocking findings it writes `.locked` (a hash bound to the
spoken text **and the speaker tags**, so a voice-swap busts it too) and registers the artifact.
Exits non-zero on any blocking finding. **`require_lock(folder, form)`** is the enforcement
guard the `/witness-voice` and `/witness-cut` build steps MUST call at the top, so audio/video
can never render an unlocked or stale narration (a standalone CLI nobody runs is not
enforcement). Rules: `data/eyewitness_rules.json`; logic: `pipeline/eyewitness_gates.py` +
`cli_witness_lock.py`; regression tests + fixtures: `pipeline/test_eyewitness.py` (every
red-team bypass — invented divine speech, fabricated/misattributed KJV, fear-CTA, essay-density,
no-Christ reveal, templated stinger, near-identical cluster — has a fixture that MUST FAIL).
The standing verify before any LOCK or ship: **0 FAIL gates + tests green + the 5-CLI panel.**

---

## 10. Independent panel (outside review)
`independent_review.py --type eyewitness-short|eyewitness-long "<clean narration>"` — the
5-CLI panel (cursor + claude/gemini/codex/grok) reviews on the EW-G7..G10 lens (+ the standard
KJV / CTA / doctrine checks), on a CLEAN artifact (strip status/fix-notes; no `--context`
priming; run BEFORE the metered voice synth). Apply convergent fixes; a disputed REVISE goes
to the user. Mandatory for every LOCKED eyewitness narration (short and long).

---

## 11. Cost model (per episode, rough)
- SHORT: voice ~$0.30 · stills (reuse-heavy, ~2–4 gaps) ~$1–2 · score/sfx/caption $0 → **~$2**.
- LONG: voice ~$1–2 · stills (~6–12 gaps of ~24) ~$4–7 · veo3 animation ~$8–11 → **~$15–20**.
- Reuse (§7) is the lever; the banks grow as Awakeden ships, so each episode trends cheaper.
