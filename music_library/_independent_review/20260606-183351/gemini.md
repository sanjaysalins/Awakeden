# Independent review — gemini (OK, 45s)

Here is your adversarial review.

### Critique

**1. The "Single-Bed" Contradiction Breaks the Pilot and Half the Catalogue**
*Claim:* "60s shorts = ONE primary melodic bed for the whole clip... Because it also covers the Landing it must be CTA-safe (picked via `find_for_beat('landing', …)`)"
*Claim:* "Pilot (4 beds): generate `sacred_grace_rise`, `lonely_searching`..."
*Claim:* "`lonely_searching` · beats: hook" AND "tension/urgent/lonely/lament are narrative-only."
*Flaw:* This is a fatal architectural contradiction. If a 60s short uses exactly *one* primary bed, and the code selects that bed by calling `find_for_beat('landing')` to ensure CTA safety, then beds tagged *only* for the `hook` beat will **never** be selected. `lonely_searching` is literally one of your 4 Pilot beds, yet under this rule, the engine can never use it for a short. If you bypass the landing check to allow `lonely_searching` to start the short, it will play all the way through the Conviction/Landing, directly violating your "NO fear/pressure/unresolved-ache on the Conviction or Landing" doctrine. You cannot have "one bed per short" while also having "narrative-only hook beds."

**2. The Physics of Ducking vs. Swelling (The Placer)**
*Claim:* "Music ducks to near-silent under the verbatim KJV quote (intelligibility)"
*Claim:* "trim-to-in-point + swell→CTA align"
*Flaw:* You are ignoring audio physics. In your narrative structure, the KJV quote (the Proof beat) immediately precedes the Conviction/CTA. If a bed's dynamic swell is aligned to hit exactly at the CTA, that swell is actively *building* during the Proof beat. If your placer aggressively ducks the bed to "near-silent" during the Proof to satisfy the >98% STT gate, you are muting the actual build-up of the swell. Worse, when the KJV quote ends, the sidechain compressor will release, instantly un-ducking a bed that is now at peak volume. This won't sound like a swell; it will sound like a jarring, amateurish volume snap.

**3. Unenforceable Metadata ("Arc Beds")**
*Claim:* "`approve.py` ... requires `--swell` for arc beds"
*Flaw:* How does `approve.py` know what an "arc bed" is? The schema and prompt lists provided show tags for beats and moods, but there is no `is_arc` or `requires_swell` boolean defined anywhere. If this relies on human memory, the CLI cannot enforce it. If it is hardcoded in `approve.py`, it violates your "edit `_specs.py` and regenerate" single-source-of-truth rule. 

**4. The Missing Fallback Trigger**
*Claim:* "Eleven Music is the bespoke-per-clip fallback... default to a reusable Suno bed... Use a bespoke Eleven Music score only when a clip needs a custom-timed climax"
*Flaw:* You are building an automated pipeline. How does the *engine* know "when a clip needs a custom-timed climax"? If the default is Suno, the pipeline will simply always pick a Suno bed. Without an explicit override flag defined in the script JSON/Markdown (e.g., `use_bespoke_score: true`), the Eleven Music fallback is unreachable dead code.

VERDICT: REVISE
TOP FIXES:
1. Resolve the Single-Bed Contradiction: Either allow mid-clip crossfading for shorts (so a `lonely` hook can transition to a `sacred` landing), or drop `hook`-only beds from the shorts pilot and acknowledge they are Phase 2 (long-form) only.
2. Fix the Placer Envelope: Design a specific audio-ducking curve that respects the `swell_s` timestamp, ensuring the compressor release is interpolated smoothly into the swell rather than snapping back to full volume post-scripture.
3. Add explicit `is_arc` (to `_specs.py`) and `force_bespoke_score` (to the script generation schema) boolean flags so the code can actually enforce your rules.
