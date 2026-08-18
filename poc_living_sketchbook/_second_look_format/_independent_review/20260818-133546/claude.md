# Independent review — claude (OK, 104s)

## Independent Review — "The Second Look" Plant Spec

### 1. Word-alignment sequencing bug (feasibility, high severity)
§3 says the Plant 2 snap fires "using the caption stage's existing word-alignment JSON — deterministic ffmpeg cut." But per this project's own documented pipeline order (`CLAUDE.md`'s stage list: assemble → sfx → caption), forced word-alignment is produced by the **caption** stage, which runs *after* assembly (Stage 3) and sfx (Stage 3b). This spec needs frame-accurate word-timing *during* the Turn's assembly cut, at a point in the pipeline where that JSON doesn't exist yet. Either the plan means to run captioning early (a real pipeline-order change, not mentioned anywhere) or it's citing a data source that isn't available at the point it's needed. This needs to be resolved concretely — e.g. by pulling timing from the audio synth stage's own turn-level timestamps (`per_turn_synth.py` output) instead of the caption JSON — before this is locked.

### 2. Internal contradiction: "Noon Frieze" + "low sun" (false assumption)
Plant 3's composition note claims "low sun (already established in the Noon Frieze default palette — this plant needs no new lighting setup)" to produce a long, legible crossbar shadow. But the style's own name — Noon Frieze — implies overhead/midday light, which produces *short* shadows pooled near the subject's feet, not the long raking shadow this plant requires. This is exactly the kind of thing that should be checked against the actual 32 validated test renders before the composition note is written as settled fact — right now it reads as an assumption, not a verified property of the style.

### 3. No fallback/kill criterion for the load-bearing plant
Plant 2 is explicitly flagged as "the highest-risk plant" and it's also the ONE that carries "the highest-impact" word-locked snap in §3, and the ONE requiring an entirely new rendered asset "built to match the first's silhouette exactly." The plan has no defined outcome if Plant 2 fails the §4 blind test (or if the match-cut asset doesn't actually align with the coil silhouette once rendered). Does the whole format die, does the Turn re-anchor on a different plant, does the piece ship with only 3 working plants? For a document that gates spend on a pilot, this decision point needs to exist before rendering starts, not be discovered after.

### 4. No tie-in to the existing assembly gates (reuse gap)
The project has a locked, deterministic hero-bookend/landing system already built (`AS-G6` hero-must-be-gospel-pivot, `AS-G7` gospel-frame + reverence speed cap, `INV-26`/`check_landing_hold.py` ≥3.0s hold). This spec's "final frame matches the opening frame exactly" loop mechanic is functionally a new kind of bookend, and the doc never says whether it's built through `cli_assemble.py`'s existing engine (and therefore inherits those gates) or as a bespoke standalone script that bypasses them. Given the file map's explicit "reuse downstream pipelines, do not duplicate" rule, this should be stated one way or the other. It also isn't clear there even IS a landing/CTA beat after 0:52 — the doc describes the piece ending at the Turn with no explicit conviction/CTA text, which is a gap against the locked CTA-to-Jesus landing rule beyond just the "hold Jesus's name for 45s" tension already raised in open question #1.

### 5. Blind test in §4 is underspecified and may not be genuinely blind
"Show them cold, no context, to fresh reviewers" — no sample size, no criteria for who counts as "fresh" (this looks like a largely solo project; are there actual naive outside viewers lined up, or is "fresh" aspirational?), and no quantified pass bar beyond "anyone... unprompted" (one person reacting is not evidence either way). Before spending on the pilot render, this section needs: how many reviewers, who they are, and what fraction constitutes pass/fail.

### 6. No cost estimate anywhere in a spend-gating document
This is explicitly "step 1 of the 6-step production plan," and later steps include a from-scratch second rendered asset for Plant 2 plus animation — yet no dollar figure appears anywhere, and the doc doesn't reference the project's own `/cost` pre-flight discipline ("pre-flight the spend of any metered batch, get explicit user OK, then log it"). Even a rough estimate for the stills-only next step would be reasonable to include here.

VERDICT: REVISE
TOP FIXES:
1. Fix the word-alignment sequencing bug in §3 — identify a timing source that actually exists at assembly time (or explicitly reorder the pipeline), not the caption stage's JSON.
2. Add an explicit kill/fallback criterion for Plant 2 (the load-bearing, highest-risk plant) and verify the "low sun" claim against actual Noon Frieze reference renders before locking Plant 3's composition note.
3. State explicitly whether the Turn/loop mechanic reuses `cli_assemble.py`'s existing AS-G6/AS-G7/landing-hold gates or runs outside them, and confirm what (if anything) happens after 0:52 to satisfy the CTA-to-Jesus landing rule.
