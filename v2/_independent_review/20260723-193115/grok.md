# Independent review — grok (OK, 159s)

I'll verify the plan's claims against the real codebase—providers, print scripts, Remotion pieces, and existing gates—before writing the adversarial review.# Independent adversarial review — AWAKEDEN COMIC DNA v0.2 (plan)

Default: skeptical. The restraint, pilot-before-76, and ~40/60 honesty are real improvements. The plan is still not executable as written.

---

## Critical: internal contradictions

### 1. Character model: NBP vs Seedream (blocks implementation)

Two incompatible recipes live in the same doc:

| Claim | Where | What it says |
|---|---|---|
| Character lock | Red-team outcome (lines 15–17) | Christ + cast on **`nano_banana_pro` + chained `--image`**; `seedream_v4_5` = **neutral plates only** |
| Recipe | §1 (lines 52–65) | **Model = `seedream_v4_5` for EVERYTHING**; Seedream + ref “held the SAME man” |

What the disk actually shows:

- `longform/EW01_Two_Goats/_retro_dna/_prove_it.py` sets `MODEL = "nano_banana_pro"` and proves the 3-scene identity / marred cross on **NBP**, not Seedream.
- `_seedream_ref.py` is a **later, separate** Seedream+ref experiment (hero/welcome/teaching/cross).
- The doc cites `_prove_it/` as if it proved the §1 Seedream recipe. It did not. That is a false provenance claim.

**If someone builds from this plan, they do not know which pipeline to ship.** Fix: one authoritative provider rule (with which bake-off folder is evidence), delete or mark the other as superseded.

### 2. Misuse of `[[locked-stills-provider-split]]`

§1 cites that memory while saying “the model changed to seedream, the reference-chaining rule stands.”

`v2/SPEC.md` still locks **NBP for Christ/face, HF `nano_banana_2` for neutral**. Collapsing to Seedream-everywhere is a **SPEC amendment**, not a footnote. The plan never lists: which memory dies, which cost table updates, which `/stills` path changes. Hidden single point of failure: implementers will half-apply both rules.

### 3. “LOCKED” language while status is DRAFT

Header: “NOT yet binding.”  
§1 title: **“LOCKED 2026-07-23: Seedream 4.5…”**  
§3: Scripture treatment **“LOCKED for the pilot.”**

After a red-team that said “do not lock,” re-stamping LOCKED on the recipe re-creates the over-commitment problem the revision claims to fix. Either it is draft, or it is locked — not both.

---

## Feasibility / codebase truth failures

### 4. §8 inventory is stale and under-counts real code

Concrete false claims:

| Plan claim | Reality |
|---|---|
| `Kalam.ttf` **NOT in repo** — acquire | `_remotion/public/Kalam-Bold.ttf` and `Kalam-Regular.ttf` exist; `DnaPocFilm.tsx` / `DnaSplashHook.tsx` already load them |
| Narrator caption = **“CSS mockup only”** | Working `Caption` component in `DnaPocFilm.tsx` (comic-yellow `#ffe100`, top-left, Kalam italic caps) + shipped POC `dna_poc_v1.mp4` |
| SFX = pure **BUILD** | Working `Sfx` in `DnaPocFilm.tsx` (Bangers, angled) |
| “Only the kinetic-Scripture Remotion piece is proven” | Body POC + hook POC exist; caption + SFX + Scripture are all in the POC film |

Re-stating BUILD for things already proven as inline Remotion components will cause rebuild-from-zero instead of **extract reusable components from `DnaPocFilm.tsx`**. That is a reuse failure.

Missing from the map (real owners the pilot will hit):

- `/livingpage` skill and motion-comic gates  
- Existing comic-grid rules (every panel real generative clip; Seedance vs Kling tiering)  
- `pipeline/visual_render.py` / audit rubrics (still “graphic_novel / cinematic-manga”, not moderate retro)  
- Character-ref bank location beyond one EW01 `christ_pc_ref.png`

### 5. Wrong path assumptions

Plan paths like `_retro_dna/_prove_it/`, `_print_finish.py` read as repo-root. Actual home is:

`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\_retro_dna\`

Everything is **episode-local scratch**, not production DNA infrastructure. Plan treats ad-hoc scripts as if they were already productized.

### 6. No bridge into `STYLE_REGISTRY`

Plan: later “wire into `config.py` / `STYLE_REGISTRY`.”

Today `STYLE_REGISTRY` only has `baroque` | `graphic_novel`. Active GN prompt is **inked graphic-novel / cinematic-manga**, not “Silver Age + cream newsprint + Ben-Day.” There is:

- no `retro` / `awakeden_comic` style key  
- no audit rubric for moderate-retro  
- no decision: **replace** `graphic_novel` vs **third style**

§10’s `VISUAL_STYLE == the retro record` assumes a record that does not exist.

### 7. Format-split vs livingpage (unresolved conflict)

§9: Shorts = full-bleed, no tier grids; long-form = tiers + page-turns.

`/livingpage` is the standing finishing path for **both** long and short motion-comics. Comic-grid / panel-animator rules still bind multi-panel work. The DNA plan never says which skill wins when they disagree. Pilot will invent process on the fly.

### 8. Body gate not wired

§5a: Vision FAIL on idealized musculature + ban tokens. Existing `verify_image` / `STYLE_AUDIT_RUBRIC["graphic_novel"]` does **not** implement Isaiah-53 body checks. No step: extend which file, which gate id, fail-closed vs advisory, cost per still. “Proven in one PNG” ≠ production gate.

---

## Cost / spend

### 9. “Nothing costs render money until the pilot” is false and dangerous

Already spent: multi-model bake-offs, prove-it, seedream_ref, DNA POC animate (`_dnapoc_animate.py` notes ~$3.70 for 4 clips alone), hook iterations. Claiming zero until pilot rewrites history.

Worse: **cold A/B of the same piece two ways** (§9.2) is **≈2× stills + animate + assemble** for every pilot piece, then paid traffic / posting ops. No ceiling, no piece count (“handful” / “Cluster-1 scale” is vague), no `/cost` pre-flight. Contradicts the project’s standing cost skill.

### 10. Free kitsch-test vs paid A/B order is soft, metrics are weak

§10: free kitsch test → panel → pilot + A/B.  
`_KITSCH_TEST.html` exists and is unsent (per RESUME). Good.

But A/B metrics (CTR, first-3s retention, comment “cringe”) have:

- no sample size / platform / duration  
- no control for thumb vs body style (plan also requires non-halftone thumbs — confound)  
- no kill criteria (“pilot wins” undefined)  
- no what happens if A/B is mixed / noisy  

Strategy decision without decision rules.

### 11. Premature brand/site surface area

§8 lists website retro skin + thumbnail skin as BUILD items in the DNA. Those are post-lock productization. Building them before the free kitsch test + pilot is classic premature commitment.

---

## Over-engineering before the idea is proven

### 12. `/dna-check` designed before the look is locked

§10 designs a hybrid deterministic/Vision gate for a DNA still marked DRAFT, with VISUAL_STYLE record and provenance sidecars that don’t exist. Gate design is fine **after** pilot; writing the check architecture now risks codifying an unproven dial.

### 13. Print-finish reconciliation is open; animation story is inconsistent

§1 OPEN: three scripts conflict; still-only; crawl risk; rembg “real fix.”  
RESUME (same day) claims: “dot-crawl is solved-by-design (dots baked into the plate).”

Pick one. If dots are baked in-render, the canonical finish may be **thin or optional** — reconciling three scripts may be less critical than the plan claims. If finish is load-bearing, the DNA POC claim of “dots baked = no crawl” needs explicit scope (POC only vs all episodes).

`panel_animator/print_grade.py` is already the named production tool with README placement. Plan treats it as a peer of ad-hoc `_print_finish.py` / `_retro_grade_demo.py` instead of “extend the existing tool.”

---

## Hidden risks / missing steps

### 14. Multi-character cast is hand-waved

“Each recurring character gets a locked ref.” Only Christ ref is operationalized. EW01 needs Aaron (RESUME already notes bare muscular arm on Aaron/Christ). Pilot on Two Goats without a cast-ref bank will re-hit identity drift — the exact failure the DNA claims to have fixed.

### 15. Long-form hero-bookend gap acknowledged, not scheduled

§5: “long-form Remotion path needs its own bookend check — coverage gap to close.” No owner, no gate name, no pilot exit criterion. AS-G6/G7 do not automatically cover Remotion long-form.

### 16. Word-timed panel slams honesty is good; pilot still depends on it

§6 correctly demotes word-timing to a target. Pilot “Cluster-1 scale” with approximate 40% timing (`EW01Slices.tsx`) may look amateur next to livingpage pieces. Missing: pilot quality bar = acceptable without word-timing, or pilot blocked until ported.

### 17. “4-colour print system” vs 11-swatch table

§2 sells CMYK four-ink discipline, then lists process CMYK **plus** comic red, hero blue, storm, gold, desert, caption yellow. Fine as design range, dishonest as “4-colour.” Operators will not know max ink count for a still.

### 18. “The render prompt (both providers)”

§1. Recipe is single-model Seedream. “Both providers” is leftover from the NBP/HF split and will confuse implementers.

### 19. Sequencing for the 60% BUILD

§9 says build pilot then A/B. §8 says tier grids, balloons, canonical print, generalized lettering are unbuilt. **You cannot pilot the DNA without first building the path that produces a pilot cut.** Order should be:

1. Free kitsch test (kill/continue)  
2. Resolve model contradiction + minimal production path (one style record + ref-chain + Remotion extract)  
3. **One** pilot piece end-to-end (not a batch)  
4. A/B only if that piece is good enough to measure  

“Handful of pieces” before one green end-to-end is over-spend risk.

---

## What the plan gets right (brief, not praise for its own sake)

- Pilot before 76; audience can veto kitsch  
- Grandfather shipped non-retro  
- Honesty that much Remotion grammar is unbuilt (directionally right, inventory wrong)  
- Passion vs glory Christ split is doctrinally necessary  
- No-baked-text negatives + Remotion owns text  
- Format-aware thumbs (non-halftone) is real compression knowledge  
- dna-check honesty that look ≠ $0 provenance  

These do not cancel the model contradiction or the false inventory.

---

## Bottom line

Do **not** treat this as ready for the external panel as a binding plan until the provider story is one line, §8 matches the tree, and pilot cost/order is specified. Look direction may be fine; **this document is not yet a plan you can build from without guessing.**

VERDICT: REVISE  
TOP FIXES:  
1. **Resolve the NBP-vs-Seedream contradiction in one authoritative recipe** — state which bake-off folder is evidence; update or explicitly supersede `locked-stills-provider-split` / SPEC; delete the other claim.  
2. **Rewrite §8 against the real tree** — Kalam is vendored; extract caption/SFX/Scripture from `DnaPocFilm.tsx` (not “CSS mockup”); correct paths under `longform/EW01_Two_Goats/_retro_dna/`; map livingpage + stills audit + cast-ref bank.  
3. **Define a one-piece pilot with a hard cost ceiling and order** — free kitsch kill-gate → single production path → one end-to-end piece → only then dual-cut A/B with kill metrics; drop “nothing costs until pilot” and pre-pilot website/`/dna-check` build.
