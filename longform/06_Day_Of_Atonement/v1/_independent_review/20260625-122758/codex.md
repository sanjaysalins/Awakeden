# Independent review — codex (OK, 193s)

**Findings**

1. The plan overclaims timing precision. The header says **“scene t[] tile the turn timeline”** and **“every quote's visual matches its narration cue”**, but the artifact gives only broad 19-23s scene windows and no turn IDs, quote start/end times, or phrase-board mapping. The repo’s timing code explicitly expects real `_turns`-derived timing, not static metadata, so this is not reviewable from the plan alone.

2. The motion rules contradict themselves. The plan says **“atmos = the only thing veo animates (subjects are frozen)”**, but S22’s atmos says **“the far speck dwindling”** and S25 says **“the robe and hair stirring almost imperceptibly.”** Those are subject changes, not atmosphere. Either Veo moves the subject and risks morphing, or it obeys the freeze rule and the beat does not read.

3. S11/S22 rely on action the pipeline is trying to suppress. S11 says **“a single live goat led away… the small figure of the goat and the fit man dwindling”** and S22 says **“dwindling to a tiny speck”**, while the global rule says goats are **“ALWAYS still/calm”** and subjects are frozen. A frozen still plus slow push is a weak substitute for the central “carried away” action.

4. The plan hides a real moderation/retry risk behind false certainty. The header says **“all crosses robed -> veo NSFW-safe”**, but S12/S14/S19 still include crucifixion, nails, blood logic, and suspended body prompts. The actual animation driver has an NSFW fallback path, which means this is known risk, not “safe.”

5. S21 is historically wrong for the NT temple veil beat. It shows **“the Most Holy Place now OPEN… the golden ark of the covenant… mercy seat”** after S20’s torn temple veil. The Second Temple veil scene should not visually reveal the ark as if it were sitting behind the veil. This confuses tabernacle typology with first-century temple history.

6. The plan blurs tabernacle and temple too early. S1 is explicitly **“ancient Israelite tabernacle”**, but S3 shows the priest before **“the great heavy temple veil”** during the Leviticus 16 setup. S20 can be temple; S3 should be tabernacle language unless the narration has already moved to Matthew 27.

7. Several visuals are effectively repeats with small lighting changes. S2/S9/S21 all reuse the same **“golden ark… mercy seat… cherubim… incense… radiance”** construction. S5/S16/S18 repeat priest + altar + blood basin. S12/S14/S19 repeat the same long crucifixion anatomy block. For a 25-scene film, this is a high repetition load.

8. The cost/reuse plan is missing. The artifact proposes **25** NBP stills plus **25** Veo clips but gives no pre-flight spend estimate, approval gate, reroll cap, or reuse pass. The repo already has test gates and cost tooling; the plan should not proceed to paid generation without naming which scenes are test-gated and which existing library assets can be reused or rejected.

9. S15 is visually under-specified for its job. **“A single thoughtful bare-headed ancient man seated alone on a stone”** does not visualize the actual objection: **“primitive superstition”** / **“reading Christ back”**. It will read as generic contemplation, not the argument being answered.

10. S23/S24 risk literalizing access to God as walking into an earthly shrine. **“a single ordinary ancient figure… before the great TORN veil”** and **“stepping forward through the parted veil into… the opened Most Holy Place”** may visually imply ordinary physical entry into the temple Holy of Holies, with S21 compounding that by showing the ark. The theological point is access by Christ, not a literal post-crucifixion temple walk-in.

VERDICT: REVISE
TOP FIXES:
1. Add a real timing/review appendix: scene-to-turn/quote mappings from `_turns`, plus exact cue coverage for every quoted verse.
2. Fix the tabernacle/temple/ark confusion, especially S3 and S21-S24.
3. Add cost, test-gate, retry-cap, and reuse decisions before any paid NBP/Veo batch.
