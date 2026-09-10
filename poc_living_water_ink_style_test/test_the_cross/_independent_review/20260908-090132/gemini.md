# Independent review — gemini (OK, 33s)

Here is the adversarial review of the plan.

### Findings

**1. Feasibility Risk: Generative AI cannot easily render "wax resist"**
> "Proposed fix... hardness reads as the paper not taking the swirl where that person stands — a dry patch on a page otherwise at Stage 3, like wax resist."
Generative image and video models (Nano Banana Pro, Kling, Seedance) are notoriously bad at executing complex negative spatial constraints (e.g., "draw swirling ink everywhere *except* this specific human outline"). Relying on an "absence of a mark" as a load-bearing grammatical rule for episode #14 is a massive risk. You are assuming the models can reliably render a clean "dry patch" amidst dynamic Stage 3 swirls without leaking ink or hallucinating. This is premature rule-building before the visual proof-of-concept exists.

**2. Missing Verification: "Turning back pages" assumes unbuilt tooling**
> "Intention: use the format's own native device — the sketchbook turns back to pages 4 and 5."
This assumes the existence of a 3D page-turning pipeline or compositing script capable of bringing previously rendered clips (episodes 4 and 5) into a new episode's physical "sketchbook" space. The current codebase supports comic grids, `dynamic_cam3d`, and specific devices (like `blue-line` or `keeper-hand`), but there is no proven mechanism for a literal backwards page-turn of shipped episodes. This is a technical single point of failure. 

**3. Hidden Risk: Merging a locked script violates pipeline invariants**
> "note: this passage is ALSO already a locked backlog script, `44_Grace_Spoken_First`... merge these into one build"
The pipeline rules treat "locked" scripts as strictly gated. You cannot casually merge a locked script with a new conceptual frame ("Where Art Thou? (Fable's frame)") without fundamentally rewriting it, which breaks its locked status and requires a full re-run of the narration gates and red-team audits. The plan treats this as a simple administrative merge, ignoring the friction of unlocking and rewriting a finished asset.

**4. Over-engineering / Cost: Unjustified scope creep**
> "Proposed season shape after this pass: 18 episodes (not 15)"
The plan casually expands the season by 20% (from 15 to 18 episodes). At the stated ~$23/episode cost model, this is an unacknowledged budget increase. The stated goal was to reassess the *remaining 5 items* of the 15-episode season, but it bloated into adding new episodes to fix "season-level gaps" instead of just replacing the weak planned episodes with the new candidates. 

**5. Doctrine / Visual Risk: Fray on Jesus**
> "Hebrews 5:7... earns Fray ON CHRIST HIMSELF — a first."
The dead-ink system is a visual metaphor. If "Fray" is visually consistent with previous uses of dead ink, the audience will instinctively read it as a defect or Stain (sin) on Jesus, regardless of the narration saying it is fear/agony. Visual metaphors don't come with footnotes. This is a massive doctrinal risk that the visual format itself may not be able to safely support.

VERDICT: REVISE
TOP FIXES:
1. Prove the "wax resist" negative-prompting effect in a single visual POC before adopting it as a load-bearing season grammar rule.
2. Cut the scope creep; replace #6 and #9 entirely with new candidates to maintain the 15-episode season budget instead of expanding to 18.
3. Validate exactly how the "sketchbook turns back" effect will be composited using existing CLI tools before committing to it for Episode 14.
