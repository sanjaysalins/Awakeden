# Independent review — gemini (OK, 73s)

Here is the adversarial review of the AWAKEDEN COMIC DNA plan:

**1. Over-engineering / Massive Duplication (Section 6 & 8)**
*Claim:* "Remotion stays its own, separate engine... BUILD, not ported: word-exact slam timing... a DoD-equivalent gate set, the reuse/richness counters..."
*Finding:* This violates the core `CLAUDE.md` invariants "Reuse downstream pipelines, do not duplicate" and "Simplicity first". You are proposing building an entirely parallel assembly engine in a different tech stack (JS/React/Remotion) to replace what `cli_assemble.py`, `assembly_ffmpeg.py`, and `assembly_timing.py` already do in Python. Rebuilding the exact same timing logic, DoD gates, and reuse counters from scratch just for one visual style is the definition of over-engineering. 

**2. False Assumption on Deterministic Safety (Section 5a)**
*Claim:* "Passion-Christ body tokens (`muscular`/`heroic`/`athletic`...) added to `config.VISUAL_BANNED_TOKENS` — closes the 'Vision-only, no deterministic teeth' gap."
*Finding:* This is a false assumption. Banning a few specific text tokens from the *prompt* does not deterministically govern the *pixels* the AI generates. The model can still draw a muscular figure based on synonyms ("ripped", "brawny", "strong") or contextual inference, and the prompt filter cannot stop it. The Vision audit is still your only real "teeth"; claiming the gap is "closed" by a token blacklist is a false sense of security.

**3. Hidden Risk / Brittle Image Cropping (Section 1)**
*Claim:* "Cheaper than re-rolling: just crop it off... a flat ~4.5% inset crop on all four sides removes the cream margin... strictly better fix than fighting the prompt"
*Finding:* A blind, automated 4.5% geometric crop is a major risk. It assumes the AI-generated border is perfectly symmetrical and exactly 4.5% thick every time. Applying this silently risks chopping off heads, edge details, or altering the composition/aspect ratio destructively. If an image is bad, rely on your existing `render_scene()` retry-on-audit-fail loop rather than introducing destructive automated cropping.

**4. Flawed A/B Testing Methodology (Section 9.2)**
*Claim:* "compare it between-subjects, not within — its real performance... against the last 2-3 comparable already-shipped inked/painted longs"
*Finding:* This pilot testing methodology is scientifically invalid. If you change *both* the narrative story (subject) and the visual style simultaneously, you cannot isolate which variable caused a drop or spike in retention. If EW01 performs worse than a previous episode, you won't know if the audience rejected the retro style, or if they just didn't find the "Two Goats" story as engaging. 

VERDICT: REVISE
TOP FIXES:
1. Scrap the parallel Remotion engine build; integrate the retro tier-grids, slams, and text overlays into the existing Python/ffmpeg `cli_assemble.py` pipeline.
2. Fix the A/B test protocol to actually isolate the visual style variable (e.g., test the retro style on an already-proven script/audio track, or run a true controlled test).
3. Remove the automated 4.5% blind crop mitigation and rely on the established Vision-audit rejection loop for bordered images.
