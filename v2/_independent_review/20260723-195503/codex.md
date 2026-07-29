# Independent review — codex (OK, 274s)

**Findings**

1. The pilot cannot prove the production path as sequenced. The plan says “Character lock (MANDATORY, but NOT YET production-wired)” in §1, then says “Only after the pilot wins do we wire into `config.py` + skills + gates” in §9. That means the pilot would validate ad-hoc scripts, not the real renderer. The code confirms it: `HFProvider.generate()` accepts `extra_ref_paths`, but `render_scene()` calls `provider.generate(scene, audit_feedback=feedback)` with no refs.

2. “Two models, split by role” is not supported by the current runner. `config.py` has one `still_model` per style; `graphic_novel` is `seedream_v4_5`, and there is no `retro` / `awakeden_comic` style key. There is also no per-scene routing for “recurring character → nano_banana_pro” vs “neutral plate → seedream_v4_5`.

3. The “Body gate” is not actually deterministic. §5 says to “ban `muscular / heroic / athletic / six-pack / V-taper` tokens,” but `config.VISUAL_BANNED_TOKENS` does not include those. The plan even admits this is “not yet addressed” in §10, then downgrades it as lower-severity. For a doctrine gate, that is backwards.

4. The palette claim is still false. §2 says the table is “the single source of truth” and “the reference card must match it exactly,” but `_DNA_REFERENCE.html` uses `#C0392B` for red while the doc declares comic red as `#ED1C24`; it also omits several declared palette chips.

5. The print finish is a single unresolved failure point. §1 admits dots mostly come from the render, the finish is unproven on animation, and three print scripts conflict. §6 still plans “print-finish over the top.” That is not a locked recipe; it is three competing implementations plus a known crawl/moiré risk.

6. The SFX carve-out is policy text, not enforcement. §5 bans SFX on crucifixion / veil-tear / resurrection, but `DnaSplashHook.tsx` renders `ImpactBurst` from a global burst list without beat-type gating. The same mistake can recur.

7. The A/B plan is underspecified. §9 says “the same piece cut two ways,” but retro-comic changes model, lettering, SFX, grid grammar, motion, and thumbnails. §10 admits no sample size or kill criteria. That will not isolate whether the audience prefers the visual identity.

8. The pilot cost range is too optimistic to anchor decisions. §9 estimates `$15-25/piece`, but excludes paid Vision checks, retries, failed renders, A/B duplication, and the `$0.50/still` direct NBP path if that provider wins reconciliation.

VERDICT: REVISE
TOP FIXES:
1. Wire the production path first: style key, per-scene model routing, ref-chain plumbing, cast refs, and provenance.
2. Turn doctrine/style rules into deterministic gates where possible before pilot: body tokens, no-baked-text, SFX carve-outs, palette/version checks.
3. Define the pilot/A-B protocol and exact cost preflight before spending: variables held constant, sample size, kill criteria, retry budget, and model mix.
