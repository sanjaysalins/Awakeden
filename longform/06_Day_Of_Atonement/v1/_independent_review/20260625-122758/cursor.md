# Independent review — cursor (OK, 104s)

## Independent adversarial review — *The Two Goats* scene plan (16:9 long-form)

Reviewed against `v2/LONGFORM_SPEC.md`, `/scene-plan-long`, `/animate-long`, `/assemble-long`, and the shipped `_build_scene_plan.py` / `_assemble_16x9.py` tooling. Skepticism first.

---

### Feasibility vs. real codebase

**The plan assumes tooling that exists, but skips mandatory pipeline steps.** Timeline tiling (`scene t[] tile the turn timeline`, 532.6s, contiguous windows) matches what `_build_scene_plan.py` already validates. `fill: boomerang` / `forward_slow` maps to real branches in `longform/_assemble_16x9.py`. veo3 via `_animate_16x9.py` is the correct long-form path (not shorts `animate_scenes()`).

**What's missing from the plan as a shippable stage-2a artifact:**
- `/scene-plan-long` step **0**: `clip_reuse.decide_for_scene()` — no reuse/bank decisions anywhere in episode 06.
- Steps **6–7**: 6-agent + LF-SP-G1..G9 panel, **independent scene-plan audit**, **`paper_cohesion`** (blocking). The markdown plan is a human review doc, not evidence those gates ran.
- `/cost` pre-flight and LF-INV-7 **test-gate** (2 stills + 2 veo clips before ~$22 batch) — not mentioned.
- Post-render **LF-CLIP-*** QC + `clipqc.json` / `coherence.json` chokepoint before assembly — not mentioned.

**Schema gap:** JSON has no `"hero": true` (Psalm 22 plan does). Hero is inferred only from “last scene is risen Christ.” `_assemble_16x9.py` never reads a hero flag; LF-AS-G5 is manual. That’s a verification hole.

**`directional: true` on all `forward_slow` scenes (S11/S22/S25):** Assembly correctly prefers `fill == "forward_slow"` over the directional chain, so no continuation clips are *required*. But `/animate-long` step 5 says directional windows >8s need `_cont` clips; an operator following the skill literally could waste money generating unused continuations. The plan’s own note (“no continuation-clip cost”) fights the `directional: true` flag.

---

### Hidden risks / false assumptions

**1. “Subjects are frozen” is contradicted in multiple subject_blocks.**

The header claims: *“every subject … is FROZEN; only ambient … moves”* and *“goats are ALWAYS still/calm.”* Several scenes invite veo locomotion anyway:

| Scene | Phrase | Risk |
|-------|--------|------|
| **S8** | *“a fit man **beginning to lead** the second goat … away”* | LF-CLIP-NOLOCOMOT — veo will walk the man/goat |
| **S11/S22** | *“led away”*, *“dwindling toward the far empty horizon”*, *“dwindling to a tiny speck”* | Subject motion implied; `forward_slow` only time-stretches one 8s clip — it does **not** execute a journey |
| **S13** | *“straying sheep **wandering** apart”* (twice) | Sheep locomotion + morph |
| **S24** | *“a single figure **stepping forward** through the parted veil”* | Direct NOLOCOMOT violation |
| **S25 (hero)** | *“**reaching** one open pierced hand gently forward”* + atmos *“robe and hair stirring”* | Face/hand morph on the one scene where the face is visible — highest-stakes LF-CLIP-NOMORPH failure |

The veo anti-morph prompt in `_animate_16x9.py` helps, but the **still design** is betting against veo’s default behavior. Goats are called out as a morph hazard in the header; sheep, walking figures, and reaching Christ are not guarded equally.

**2. Duplicate wilderness scapegoat (S11 + S22) is a strobe risk.**

S11 (*“The scapegoat bears it away — a land not inhabited”*) and S22 (*“As far as east from west — carried away (Psalm)”*) reuse essentially the same `SCAPEGOAT` + `WILDERNESS` plate (small goat, fit man, pale desert, heat-shimmer). Narration differs; **visual grammar does not**. In a 19–21s window each, the viewer gets ~40s of the same motif. LF-SP-G3 (“not repetitive”) is weak here.

**3. Hero / visual-peak split vs. written LF-AS-G5.**

- Spine: *“the film CLOSES on the living risen Christ (hero S25)”* — M7 resurrection close. That matches shipped pattern in episodes #04–#05 and LF-AS-G6 (*“M7 Invitation or hero”*).
- But LF-AS-G5 still says hero = **M6 substitution/cross**, visual peak, **within final 90s**.
- **S19** is labeled *“the Exchange centerpiece, EPIC monumental WIDE tableau”* at **385.8–409.4s** — **outside** the final 90s (442.6–532.6s). So the declared “centerpiece” and the spec’s “hero peak” are not the same shot, and neither is flagged in JSON.
- **Three crucifixions** (S12, S14, S19) vs. Seed-of-Woman build script cap of **exactly 2** — more spend, more cross fatigue, more NSFW-fallback surface.

**4. Period accuracy: “temple veil” in wilderness-tabernacle OT beats.**

`VEIL` constant and **S3** use *“the great heavy **temple** veil”* while M1 is explicitly tabernacle (goat-hair curtains, acacia, oil lamps). Lev 16 is pre-Solomonic. **S20** (Mt 27 fulfillment) can be temple; **S3** should not reuse temple language if the plan sells *“authentic ancient near-eastern sacred tent.”* Sloppy for a piece anchored on ritual detail.

**5. Mercy-seat / altar / veil repetition.**

- Mercy seat interior: **S2, S9, S21** (cloud + cherubim + radiance).
- Priest at bronze altar: **S5, S16, S18**.
- Veil architecture: **S3, S20, S23**.

Each beat is narratively defensible; stacked together the film risks **Baroque slideshow syndrome** — same sacred furniture, different caption.

**6. S15 skeptic is visually orphaned.**

*“a single thoughtful bare-headed ancient man seated alone on a stone … hands otherwise empty, no props”* — no goat, priest, veil, or cross. For M5’s steel-man it may pass narration, but on first viewing it reads as **stock “thinking man”** disconnected from the ritual spine the plan insists on elsewhere.

---

### Over-engineering / premature spend

**25 scenes × NBP × veo with zero reuse check is expensive before the idea is proven on goats.**

`scene_plan.json` sets `"image_provider": "nbp (Nano Banana Pro, Baroque oil)"` for **all** scenes. Cost model (`LONGFORM_SPEC.md` §7) assumes ~8 NBP + ~14 HF neutral plates (~$8.20 stills). This plan is ~**$12.50 stills alone** (+ ~$10 veo) with no `clip_reuse` pass. Priest/tabernacle/altar/wilderness plates are obvious HF candidates; cross/resurrection may reuse prior-episode banks (Seed/Bronze Serpent risen-close patterns).

**Three crucifixion stills + three veo clips** when the narration could carry M4→M6 with **two** varied crosses (Seed pattern) is spend without proven visual payoff.

**Boilerplate prompt bloat:** Every scene repeats ~120 words of identical Baroque/full-bleed guards before the unique beat. That’s not wrong, but it increases model sameness and audit fatigue — working against LF-SP-G3 variety.

---

### Missing verification gaps

The plan asks reviewers to check *“scene↔narration cohesion, doctrinal/period accuracy, binding mix, veo-morph hazards”* but provides **no evidence** of:

1. LF-SP-G6 **3–5 named vignettes** on unified scenes — only prose hints. **S4**: *“several small grouped vignettes”* (unnamed). **S17**: tabernacle + hill = **2** elements, not 3–5. `_build_scene_plan.py` only asserts `"unified" in subject_block` ≥2, **not** LF-SP-G6 properly.
2. LF-SP-G8 **≥3 framings; none >40%** — not checked in build script.
3. `paper_cohesion` over narration + plan.
4. Ear-check / LF-AS-G1..G6 after assembly.
5. Test-gate on **goat** + **risen-Christ-face** before full batch (the two highest morph risks).

---

### Reuse

**Plan duplicates generative work the repo already has tools to avoid.**

- No `clip_reuse` / `bank` fields (INV-19 / `/scene-plan-long` step 0).
- Risen-Christ hero close (S25) is structurally identical to #04/#05 hero closes — strong reuse candidate, not flagged.
- Wilderness scapegoat (S11/S22) duplicates **each other**, not library reuse.

---

### Cost / spend justification

Rough pre-flight vs. spec model:

| Line | Spec assumption | This plan |
|------|-----------------|-----------|
| NBP stills | ~8 × $0.50 | **25 × $0.50 = $12.50** |
| HF stills | ~14 × $0.30 | **0** |
| veo clips | ~22 × $0.40 | **25 × $0.40 = $10.00** |
| Continuation | ~4 × $0.40 | **0** (if forward_slow honored) |
| **Media subtotal** | ~$18 | **~$22.50+** |

Within the $40 ceiling, but **not optimized** and **not pre-flighted**. Paying for 3 crucifixions + 2 near-identical scapegoats before a $0.90–1.50 goat/hero test-gate is backwards per LF-INV-7.

---

### What the plan gets right (grudgingly)

- 25 scenes, all M1–M7 ≥2 scenes, contiguous `t[]` tiling — structurally sound.
- Goat-still discipline is explicitly acknowledged (*“veo morphs live animals”*).
- God-as-cloud-only, robed crosses, face reserved for hero — aligned with NSFW/hybrid fallback practice.
- OT-echo count (Isaiah S13, Psalm S22), Jesus/NT-link count, unified ≥2 — passes the **weak** automated checks.
- Boomerang on ~20s windows with 8s clips is mathematically viable (`factor ≈ 1.25`).

---

### Narration↔visual flags (plan’s own review lens)

- **S8** split-frame “one killed / one led away” is clever typology but the *“beginning to lead”* side fights animation discipline.
- **S11 vs narration “never to return”:** still shows figures mid-desert, not gone — OK if narration carries it; weak if the image must show “out of sight.”
- **S22** Psalm east-from-west needs **vast horizontal dawn**; subject is still “goat led away” — same as S11, not east-west geometry.

---

VERDICT: REVISE
TOP FIXES:
1. **Rewrite locomotion-bait scenes (S8, S13, S24, S25) to frozen tableaux** — or accept Ken-Burns/ffmpeg holds for those windows; do not send “lead / wander / step / reach” language to veo and claim LF-CLIP-NOLOCOMOT compliance.
2. **Run `clip_reuse` + split NBP/HF before batch spend** — reuse risen-hero/cross plates where eye-checked; merge or radically differentiate S11/S22 scapegoat visuals.
3. **Complete stage-2a verification the plan omits** — test-gate (goat calm + hero face), `paper_cohesion`, independent scene-plan audit, proper LF-SP-G6 named vignettes, `"hero": true` on S25, and fix OT “temple veil” → tabernacle curtain in S3.
