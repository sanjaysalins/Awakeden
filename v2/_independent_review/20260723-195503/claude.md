# Independent review — claude (OK, 166s)

## Independent Review — AWAKEDEN COMIC DNA v0.3

I verified two of the plan's code claims directly against the repo before reviewing.

**Verified true:** §8's claim that `pipeline/visual_render.py`'s `render_scene()` never passes ref paths — confirmed at line 592 (`provider.generate(scene, audit_feedback=feedback)`, no `extra_ref_paths`), even though both `NBPProvider.generate` and `HFProvider.generate` already accept that parameter (lines 157, 242). So the "not production-wired" admission is accurate, not another overclaim.

### Findings

**1. §1 quietly overturns a LOCKED decision without flagging it as such.**
The recipe — "Christ + any recurring character → `nano_banana_pro`" + "neutral plates... → `seedream_v4_5`" — inverts the memory-locked 2026-06-08 provider split (`locked-stills-provider-split`: **NBP for Christ/face, HF `nano_banana_2` for neutral plates**). The doc even names the conflict in a footnote ("this is a different code path from the existing production `NBPProvider`... The two are not yet reconciled") but never states this plan is proposing to *supersede* a locked call. Per this project's own CLAUDE.md ("Locked decisions... do not relitigate without the user"), that needs to be said explicitly and put in front of the user for sign-off — not left as a parenthetical.

**2. The core visual mechanism (halftone dots) is unproven on the actual deliverable, but the pilot isn't gated on solving it first.**
§1 states the print-finish is "NOT yet proven on animation" and risks "crawl/moiré," and §6 repeats the same caveat. Since the output is video, not stills, this is the single largest technical risk to the whole identity — yet §8 lists it as one BUILD item among many rather than a hard blocker sequenced *before* any pilot clip renders. As written, the plan could spend the $45-75 pilot budget on clips whose signature texture visibly breaks.

**3. "MANDATORY" character-lock (§1) is proven on n=3 scenes, Christ only, via ad-hoc scripts — not the production path.**
The doc is honest about this in §8's table, but §1 still uses "MANDATORY" language for something that (a) isn't wired into `render_scene()` (verified above), and (b) has zero proof for any non-Christ character — the doc names Aaron as still lacking a ref. The §9 pilot cost estimate has no line item for the engineering work to wire this before a real (non-script) pilot render can happen.

**4. §9's cold-audience A/B — the actual decision gate for the whole direction — has no defined mechanism, sample size, or kill-criteria.**
"The same piece cut two ways... measured on thumbnail click-through, first-3-second retention, comment sentiment" doesn't say how you'd actually split cold YouTube Shorts traffic between two versions of one piece without two channels/accounts or sequential posts — both of which confound style as the variable (algorithm history, day/time, differing thumbnails). §10 admits this gap exists but defers it to "before the pilot" — yet this is the one checkpoint meant to stop a bad direction before 76 episodes; it deserves rigor before the pilot is authorized, not after.

**5. An unfootnoted claim sits right beside the claim that was just caught being fabricated.**
§1's `seedream_v4_5` pick ("chosen after a 14-model bake-off for its crowd/depth composition") and its runner-up comparisons cite no artifact path or ledger entry — unlike the neighboring Christ/`nano_banana_pro` claim, which now cites exact file+line+ledger timestamps *because the panel just caught it being wrong*. The same section just failed this exact evidentiary bar once; the second claim in it should be held to the same standard before being trusted.

**6. Minor — §5a's body-gate token list is ambiguous about being a prompt negative vs. a post-render Vision check.**
"ban `muscular / heroic / athletic...` tokens on any cross still" reads like it could be applied as prompt negatives. The doc itself cites `seedream-no-negative-channel` elsewhere in this same section (the "no blood" example) — naming a forbidden noun can draw it on this model family. Worth an explicit one-line clarification that this is a post-render Vision audit criterion only, not prompt language, so it doesn't repeat a failure mode the doc already knows about.

**7. Minor — the panel only reached 3/5 (DEGRADED), and a full re-run is "recommended," not required, before the next spend gate.**
Given this project's own "EXTERNAL independent review is ENFORCED... every SIGNIFICANT plan" rule, a visual-identity change gating 76 episodes seems like precisely the case that rule exists for. Softening it to "recommended" for this particular decision is inconsistent with the project's own standing policy.

---

VERDICT: REVISE
TOP FIXES:
1. Explicitly flag §1 as proposing to supersede the locked `NBP-Christ/HF-plates` provider split, and get the user's sign-off on that reversal before it's treated as the pilot recipe.
2. Make dot-crawl-on-animation a blocking spike (prove it on one real animated clip) before any pilot clip is rendered — it's the core visual signature and it's currently unproven on video.
3. Define the A/B mechanism concretely (how traffic is actually split cold on YouTube Shorts) plus sample size and kill-criteria before treating §9.2 as the gate that decides the whole direction.
