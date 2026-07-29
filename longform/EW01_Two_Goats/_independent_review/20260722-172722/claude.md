# Independent review — claude (OK, 144s)

I verified the plan's claims against the actual codebase and the project's own defect record. Findings below, most severe first.

## Feasibility failures against the real model

**F1 — Rule 2 ("shallow depth of field") directly fights the locked ink style AND the documented seedream behavior. This is the biggest problem and the plan waves at it without resolving it.**
- The style tail you're keeping (`config.py:465`, `VISUAL_STYLE_TAIL_GN`) literally reads *"no oil-painting brushstrokes, **not photorealistic, not a glossy 3D render, not soft airbrushed anime**."* "Shallow depth of field / one plane sharp, others soft" is a lens/photo token pulling in the exact opposite direction. You'd be adding a photoreal instruction to a prompt whose own tail forbids photoreal.
- Worse, the project's own record (`memory/byteplus-lean-prompting.md`, `seedream-no-negative-channel.md`) says seedream draws **literally** and hallucinates on every extra noun, and the standing rule is **LEAN: one subject, 25–40 words, then STOP.** This proposal bolts *four extra clauses* onto every prompt — the opposite of the lean discipline that was adopted specifically to stop hallucination. The soft-background DoF may also trip the graphic_novel Vision audit as "airbrushed/photoreal" and force re-roll loops.

**F2 — Rule 3 ("a foreground element crossing close to the lens — silhouettes, hands") violates a LOCKED invariant, not just an "open question."**
- CLAUDE.md locked decision: *"Kling-friendly state-only language — image is a frozen tableau; only the camera moves."* Memory `living-light-no-fresh-blood` / `longform-motion-fill`: *any surviving mid-motion or prominent near-lens element WILL be animated.* A big foreground hand/silhouette by the lens is the single most likely thing the i2v model invents motion on. The plan lists this under "risks I want attacked" as if undecided — but the codebase already decided it. This isn't advisory; it's a locked contradiction.

## Cost dishonesty

**F3 — "zero marginal cost" / "$0 going forward" is contradicted by your own A/B and defect log.**
- Your evidence (proposal lines 22–23): n=2, cherry-picked "obvious depth potential" scenes, and **1 of 2 grew an anachronistic cross finial — a 50% period-slip in the sample.** That's not zero-cost; that's a re-roll.
- This is not a fluke: `memory/ink-render-failure-modes.md` #3 already logs *"church steeple + rooftop cross in a pre-crucifixion Jerusalem skyline"* as a KNOWN seedream defect. Adding "towering tent / crane / architectural depth" language is exactly the prompting that summons it. Depth language plausibly **raises** the defect/re-roll rate on every still — real recurring spend, applied fleet-wide.

**F4 — "~$7.50" to retrofit EW01 is only the still re-roll and hides the real bill.** Re-animation of 25 stills under the tiered animator (`comic-grid-cost-tiered-animation`: Seedance/Kling) is unquantified and is the larger cost, plus re-running the stills gate + panel. And EW01 is **mid-flight** (`memory/ew01-ink-migration-status.md`) — retrofitting an unproven composition change onto in-progress, already-QC'd work risks destabilizing it for no proven gain.

## Over-reach / premature standardization

**F5 — "standard for EVERY still in EVERY episode" from n=2 is building before the idea is proven.** Violates the CLAUDE.md engineering rule (*"Simplicity first… think before acting; if uncertain, ask"*). The plan's own "Generalization" line admits it's untested on multi-figure and reverent scenes — i.e. the hard cases — yet proposes to standardize anyway. That's the tail wagging the dog.

**F6 — No enforcement mechanism and no test protocol.** The plan is a policy with no *how*: where do rules 1–4 live (the `discover_scenes` prompt in `pipeline/visual_engine.py`? a new SP-gate?), how is compliance checked, how are sacred scenes deterministically exempted? With no gate, it drifts. And v2/SPEC.md mandates an A/B protocol — the plan jumps straight from n=2 to "adopt + retrofit," skipping the very protocol the contract requires.

## The one weak "advantage"

**F7 — The `parallax_25d` justification is shaky and possibly backwards.** I confirmed `panel_animator/parallax_25d.py` exists, but it uses **rembg (`u2net`) to extract the single nearest salient subject** — it is not aware of your prompt's "named layers." A "foreground element crossing close to the lens" (rule 3) is exactly what could make rembg grab the *wrong* cutout (the foreground silhouette instead of the intended subject), degrading the parallax, not enabling it. The claim "depth language makes the tool work" is unverified and plausibly false.

## What's actually fine
Rules 1 (name depth layers) and 4 (one committed camera angle) are cheap, ink-compatible, and build depth the way comics actually do (overlap/linework) — worth keeping. The change correctly reuses the existing style architecture instead of duplicating tools. The danger is concentrated in rules 2 and 3.

---

VERDICT: REVISE
TOP FIXES:
1. Drop rule 2 ("shallow depth of field") entirely — replace with ink-native depth (overlap, scale contrast, atmospheric line-weight) so you don't inject a photoreal token that fights `VISUAL_STYLE_TAIL_GN` and the lean-prompt discipline; keep rules 1 and 4.
2. Gate rule 3 against the locked frozen-tableau/animation-safety invariant — forbid prominent near-lens live subjects (hands/figures) on any still that will be animated, and exempt sacred/reverent beats with a calm variant; make it a deterministic SP-gate, not prose.
3. Do NOT standardize or retrofit EW01 yet — run the SPEC-mandated A/B on the HARD cases (multi-figure + reverent), measure the true re-roll rate (your sample already shows 50% period-slip), price re-animation honestly, and bring numbers back before adopting fleet-wide.
