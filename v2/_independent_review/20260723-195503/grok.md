# Independent review — grok (OK, 142s)

I'll verify the plan's key claims against the real codebase and tools, then deliver an adversarial review with concrete findings.# Independent adversarial review — AWAKEDEN COMIC DNA v0.3 (plan)

Skeptical default. Prior model-contradiction fix is real; several execute-blockers and false framings remain.

---

## Feasibility / codebase reality

**1. `[[locked-stills-provider-split]]` is mis-cited (load-bearing).**  
Red-team outcome: “Character drift FIXED — … `nano_banana_pro` + chained `--image` … ([[locked-stills-provider-split]])”.  
Real lock in `v2/SPEC.md` and `/stills`: **NBP (Google `genai` / `gemini-3-pro-image-preview`, $0.50) for Christ/face + HF `nano_banana_2` for neutrals** — not HF-billed `nano_banana_pro`.  
§1 invents a **third** fork (HF `nano_banana_pro` via ad-hoc `hf generate create`) and tags it with the locked memory. That is not “reverting to the split”; it is a new recipe wearing an old label.

**2. “Character drift FIXED” / “Isaiah-53 cross FIXED” still overclaim.**  
Checkmarks at top vs §1: “MANDATORY, but NOT YET production-wired” and “Proven on Christ only (3 scenes)”.  
Verified: `render_scene()` calls `provider.generate(scene, audit_feedback=feedback)` with **no** `extra_ref_paths`; `HFProvider.supports_character_anchor = False`.  
Fixed in a one-off script (`_prove_it.py`), not in the production path the pilot must use. Top of doc still sells “FIXED”.

**3. Pilot sequencing collides with its own BUILD list.**  
Status / §9: pilot → A/B → wire into `config.py` / skills / gates.  
§8: ref-chaining, cast bank, canonical print pass are **BUILD**.  
Without pre-pilot wiring, the pilot re-runs ad-hoc scripts (`_prove_it.py` class) — the failure mode the panel already named. A pilot that cannot use `visual_render.render_scene` does not prove the production DNA.

**4. Dual `nano_banana_pro` paths left open as if the pilot can wait.**  
§1: HF-billed `nano_banana_pro` ≠ production `NBPProvider`; “treat them as separate until one is chosen.”  
You cannot budget, audit, or ship a pilot with two character engines. Pick **before** any pilot still spend, or the A/B measures noise from provider drift.

**5. Dot-crawl is execute-blocking for an animated pilot, not a pre-lock footnote.**  
§1 OPEN: finish is still-only; fixed screen-space dots will crawl on motion.  
§6 still: “print-finish over the top” + “prove no dot-crawl.”  
§9 budgets **$12–18 animation/piece**. Spending that before “bake into plate OR per-frame finish” is proven is burning money on a known moiré risk.

**6. Format-split vs locked `/livingpage` is unresolved and pilot-blocking.**  
§9.3: 9:16 = full-bleed only (no tier grids / page-turns); tiers for 16:9.  
`/livingpage` (binding `v2/LIVINGPAGE_STANDARD.md`): **every** motion-comic finish, long or short — word-timed slams, grids, DoD gates.  
§10 admits “format-split vs `/livingpage` standard” not addressed. A pilot that ignores livingpage is off-standard; one that follows livingpage contradicts §9.3.

---

## Hidden risks / single points of failure

**7. NSFW / provider refusal omitted from the doctrine split.**  
`_prove_it.py` lines 49–50: NSFW reject path for bare-torso cross (“may need a clothed framing”).  
§5a: “robed or loincloth — a per-piece call.”  
If HF rejects loincloth passion frames, that is not a creative choice — it is a **provider SPOF**. Plan must force robed (or direct-Kling / NBP fallback) for passion Christ, not leave it aesthetic.

**8. Body gate is Vision-only prose; no deterministic teeth.**  
§5a bans `muscular / heroic / athletic / six-pack / V-taper`.  
§10: “doctrine body-gate tokens not in a deterministic config list” — deferred.  
`VISUAL_BANNED_TOKENS` exists in `config.py` and is already SP-G5 material. Pilot passion frames without those tokens in the ban list will re-ship bodybuilder Christ under “Vision will catch it.”

**9. Cast bank is Christ-only; Two Goats pilot needs Aaron.**  
§1 / §8 admit Aaron has no locked ref; RESUME already flags bare muscular arm.  
“Pilot on Two Goats” without `aaron_*_ref` means the second named face is free to drift while the doc claims character-lock is the solved blocker.

**10. Seedream+ref is a half-artifact, not a closed neutral lane.**  
`_seedream_ref/` has only `sr_hero.png` / `sr_welcome.png` — not teaching/cross jobs defined in the script. Neutral-only is fine only if named characters **never** land on seedream plates. SP-G9 multi-vignette scenes often mix cast + setting; the plan never defines the handoff rule when both appear.

---

## Over-engineering / premature commitment

**11. “~55% owned, ~45% to build” is inflated.**  
§8 credits Remotion POC pieces (`DnaSplashHook`, `DnaPocFilm`, kinetic type, caption, SFX) as owned DNA.  
Still open for a real system: production ref-chain, cast bank beyond Christ, balloons, 6/9 tier + page-turns, one print path proven on **animation**, retro `STYLE_REGISTRY` key, thumbnail/website skins, livingpage word-timing port.  
That is **POC demos + a recipe**, not ~55% of a shippable series identity. Closer to “demo shelf + open BUILD map.”

**12. `/dna-check` sketched before the look is production-wired.**  
§10 designs provenance + paid Vision DNA checks while `STYLE_REGISTRY` has no `retro`/`awakeden_comic` key and print provenance does not exist. Gate design ahead of a single production still path is premature.

**13. Three-way print “reconciliation” treats ad-hoc as peer of production.**  
§1/§8: reconcile `_print_finish.py` / `panel_animator/print_grade.py` / `_retro_grade_demo.py`.  
Prior panel was right: **`print_grade.py` is already the named clip tool** (skill + README). Plan should extend that, not re-peer three scripts. Remotion `Grain`+`Misregister` is a **fourth** path if used on film.

---

## Missing steps / verification gaps

**14. A/B is not a protocol.**  
§9.2: “cold-audience A/B… thumbnail CTR, first-3s retention, comment sentiment… Lock only what the scroller rewards.”  
§10: sample-size / kill-criteria still “not yet addressed.”  
Missing: platform, traffic source, n, win rule, stop rule, whether both arms share the **same** stills/clips (cost 1× vs 2×), and who decides on a draw. Without that, “pilot A/B decides kitsch” is rhetoric.

**15. No named pilot slate.**  
§9: “~Cluster-1 scale, a handful of pieces.”  
No episode IDs, short vs long, still counts, which cast refs are required, or whether EW01 is in or out. Cost and scope are un-auditable.

**16. Cost band understates real pilot spend.**  
§9: stills $3–5 + animation $12–18 ≈ **$15–25/piece**, 3-piece ≈ **$45–75**, “before Opus.”  
Also missing: Vision body/DNA audits, NSFW re-rolls, dual A/B arm if cuts differ at still/clip stage, long-form veo rates if pilot is 16:9, and already-spent R&D (doc admits ledger is not zero). “Get a real `/cost` pre-flight” is correct but should be a **hard gate with a line-item table**, not a soft note under a lowball band.

**17. Word-timing honesty is good; pilot success criteria still over-promise “intentional DNA.”**  
§6: word-timed slams are TARGET; `EW01Slices.tsx` uses ~40% window timing.  
A pilot that ships approximate timing is not testing the livingpage-grade product. Say so in success criteria or port timing first on **one** piece.

**18. Full-quorum re-run is “recommended,” not required before spend.**  
Status line sequences full-quorum → pilot; §10 softens to recommended after a 3/5 degraded run that already missed a false model claim once. For a series-identity plan, **degraded panel + remaining execute-blockers** should block pilot credits, not just “lock.”

---

## Reuse

**19. Ad-hoc render culture continues.**  
Recipe lives in `_retro_dna/_prove_it.py` while production is `pipeline/visual_render.py` + `STYLE_REGISTRY`.  
Plan’s “wire after pilot wins” guarantees more one-off scripts. Reuse-first would be: pick provider → wire `extra_ref_paths` + scene-plan character refs → one STYLE_REGISTRY key → then 1–3 stills smoke, then pilot.

**20. Neutral model choice reuses bake-off well; character path does not reuse `/stills`.**  
`seedream_v4_5` for neutrals matches current `graphic_novel` still model. Character path abandons production NBPProvider without a bake-off of **HF nano_banana_pro vs NBPProvider** on the same ref + same three poses.

---

## Cost / spend justification

Pilot-before-wire + dual character engines + unproven print-on-motion + A/B without kill rules is **not** justified at $45–75+ (real number higher).  
R&D already spent; further spend needs: (1) one character path chosen and production-wired, (2) print path proven on a short animated loop, (3) A/B protocol written, (4) livingpage vs format-split decision, (5) full-quorum panel on the **corrected** doc. Until then, only $0 paper + free kitsch fixtures.

---

## What improved (for calibration, not praise)

§1 model correction is real and ledger-backed. Pilot-not-76, no-text negatives, seedream negative-channel warning, owned-vs-build honesty, and dna-check not oversold as pure $0 are real fixes. They do **not** make the plan executable.

---

VERDICT: REVISE  
TOP FIXES:  
1. Resolve the character still path to ONE production recipe (pick HF `nano_banana_pro` **or** Google `NBPProvider`; stop citing `locked-stills-provider-split` for the wrong path), wire `render_scene`/`extra_ref_paths` + Aaron ref **before** any pilot still spend, and demote top-of-doc “FIXED” to “proven ad-hoc only.”  
2. Make print-on-animation a hard pre-pilot gate: bake dots into the plate **or** prove `panel_animator/print_grade.py` (single canonical path, not three-script peer reconcile) on a 5–6s loop with zero crawl — no animation budget until that passes.  
3. Write an executable pilot protocol before credits: named slate + short/long, livingpage vs §9.3 format-split decision, A/B sample size/kill criteria/cost multiplier, deterministic passion body-token ban list, NSFW/robed fallback, and full-quorum panel as a hard gate before spend.
