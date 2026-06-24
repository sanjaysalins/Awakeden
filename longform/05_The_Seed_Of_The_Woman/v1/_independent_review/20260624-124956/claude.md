# Independent review — claude (OK, 116s)

Verified against the repo. The narration is locked and the audio turns exist, so this plan is real and spend-bearing. Findings below cite the binding long-form spec (`v2/LONGFORM_SPEC.md`).

---

## Adversarial review — Seed of the Woman scene plan

### 1. Hard invariant violation: 26 scenes exceeds the cap of 25
`v2/LONGFORM_SPEC.md` is unambiguous — **LF-INV-4: "20–25 scenes… cap at 25"** and line 117 "Scene count: 20–25 scenes." This plan ships **26**. That's not a stylistic nit; it's a spec breach that the deterministic LF-SP gate should FAIL. It also pushes cost: 26 stills + 26 veo3 clips against the **$40/long ceiling** (LONGFORM_SPEC:242 — "If pre-flight shows > $40, trim scene count"). You must drop at least one scene, and the repetition below tells you which.

### 2. Severe repetition — the plan is visually monotonous
- **Serpent appears in ~12 of 26 scenes** (S3, S5, S7, S8, S9, S14, S17, S18, S19, S21, S23, S24), almost always the identical boilerplate "a single serpent low among the roots… coiled and STILL… NOT writhing NOT moving NOT the focus." This risks LF-SP-G8 ("none >40% of scenes"). The viewer sees the same shadowed snake a dozen times.
- **Three near-identical crucifixions:** S14, S20, S21 all render "the robed Christ CRUCIFIED — both arms outstretched and NAILED… head bowed." S20 and S21 are back-to-back (345–392s) showing essentially the same image. Collapse to one.
- **Three heel-over-serpent images:** S9, S18, S19 all show "a bare human HEEL above [the serpent's] head." S18 and S19 are adjacent and redundant.
- **Couple-in-dim-garden + still serpent:** S3, S5, S23, S24 are the same composition recycled. S5 and S24 especially.
- **Wide darkening-garden tableaus:** S2, S4, S6 blur together.

This is where you cut to get under 25. Merging the S18/S19 heel pair and the S20/S21 crucifixion pair alone fixes both the count and the worst repetition.

### 3. Premature cross spends the M6 payoff early
The narration's emotional reveal is M6 "That is the cross" (S20). But a **fully crucified Christ already appears at S14** (M4, 226s) and far/faint crosses at S13, S16, S17. By the time "That is the cross" lands, the audience has seen it four times. M4 is "naming the players / destroy the works of the devil" — a symbolic far cross (as S13 already does) is enough there; the explicit nailed crucifixion at S14 (252s) undercuts the M6 turn. Demote S14 to a distant/silhouette cross.

### 4. Copy-paste atmos bug — S17
S17's scene is "a small company of ordinary ancient people… serpent far back," but its `_atmos` reads **"the shaft of light strengthening over the heel and the still serpent."** There is no heel in S17. Leftover paste from a heel scene — the atmos cue contradicts the image. Fix the line.

### 5. veo writing-animation risk — S15 scroll
Memory/standing rule **"never animate writing"** (scroll/titulus/codex/sign) — veo morphs blank surfaces into hallucinated glyphs. S15 puts "an unrolled blank scroll across the knees." Even specified blank, a scroll under boomerang/push is exactly the failure case. Drop the scroll (a seated figure weighing a question needs no prop) or lock the camera dead-still.

### 6. Window lengths exceed the freeze-safe limit
Memory **"keep windows ≤~22s, split the longest"** (forward_slow freezes when the push runs out). Multiple windows blow past: **S24 26.5s, S14 26.1s, S11 24.9s, S23 24.9s, S20 24.3s, S13 24.1s.** forward_slow on a 26s window will reach end-of-motion and freeze for the last several seconds. These need continuation clips or splitting — and splitting fights the scene-count cap, which is another reason to merge the redundant scenes.

### 7. Minor — truncated/ambiguous prompt, S11
"the woman… with **one hand resting over her**" — over her *what*? Reads as a dropped word (womb?). Ambiguous prompts render unpredictably. Complete the phrase.

### What's right (so the user doesn't over-correct)
- Doctrine is sound: promise-before-sentence ordering (S7→S10), head/heel asymmetry (S18/S19), cross-as-the-strike (S20), resurrection close (S22, S26). Matches the locked narration's spine.
- Binding mix is satisfied: unified multi-element scenes, OT-echo garden, Jesus/NT-link, and the **hero Christ-close S26** (risen Christ, pierced hand) correctly closes on Christ per LF-AS-G6.
- veo guards are well thought-through: God-as-light-only, robed crosses for NSFW-safety, serpent always frozen.

The bones are good and doctrinally faithful — but it's over the hard scene cap, visually repetitive, and has two concrete bugs (S17 atmos, S15 scroll). That's a REVISE, not a pass.

VERDICT: REVISE
TOP FIXES:
1. Cut from 26 to ≤25 scenes (LF-INV-4 hard cap) by merging the redundant pairs — S18+S19 (heel), S20+S21 (crucifixion) — which also kills the worst repetition.
2. Fix the two concrete bugs: S17 atmos still references a non-existent "heel," and S15's scroll is a veo writing-morph hazard — remove it.
3. Pull the cross back from M4: demote S14's full crucifixion to a distant/silhouette cross so the M6 "That is the cross" (S20) keeps its payoff; and split or add continuation clips for the six windows >22s to avoid end-of-push freeze.
