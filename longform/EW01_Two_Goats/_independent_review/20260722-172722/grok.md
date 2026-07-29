# Independent review — grok (OK, 144s)

I'll pressure-test this plan against the real stills pipeline, style blocks, and animation constraints—not the proposal's own framing.## Independent review — depth-composition discipline plan

**Default: do not adopt as a standard.** The plan asks for a pipeline-wide rule change on n=2 cherry-picked wins, while its own sample already shows a serious period defect. Several claims conflict with locked style, existing gates, and how `parallax_25d` actually works.

---

### 1. Evidence is too weak to set a standard (critical)

**Phrase:** *"A/B on 2 scenes"* / *"**BUT n=2**, scenes chosen for obvious depth potential"*

- Sample size 2, both “easy depth” scenes (court establishing + macro lots). That is not a generalization base for “**every** inked still.”
- Selection bias is admitted in the artifact and never resolved.
- A harder red-team script already exists (`longform/EW01_Two_Goats/_redteam_depth.py`: reverent #20, multi-figure #24, variance re-renders of #1/#7). The plan still asks “adopt as the standard?” without requiring those results as a **pass condition**.
- **Missing step:** stratified pass criteria before any “standard” language (e.g. ≥6 scenes: 2 action, 2 multi-figure, 2 sacred/hero; period FAIL rate ≤ baseline; style still reads as ink, not photo-blur; i2v invent-motion not worse).

---

### 2. The A/B is confounded — not “only depth language” (critical)

**Phrase:** *"same style block, same model, **only the depth language added**"*

False against the actual test prompts in `_test_depth_prompt.py`.

Original scene 1 `subject_block` already has scale/depth:

> *“Aaron, **small**… towering… multitude… in shadow… tent **dominant**”*

The “depth” rewrite is a full restage: extreme foreground silhouettes, low three-quarter, soft crowd, “strong shallow DoF,” colossal tent. That is **composition redesign**, not a small additive rule. You cannot credit the four-rule formula alone; better art direction alone can explain the win.

---

### 3. Period-slip evidence already falsifies “$0 / low risk” (critical)

**Phrase:** *"one of the two grew an **anachronistic cross finial** (a **50% period-slip** in this tiny sample)"*  
**Phrase:** *“Comic level at **zero marginal cost**”* / *“**$0 going forward**”* (via risks section)

- 1/2 period failure is not a footnote; it is a cost and doctrine signal (INV-21 / IMG-PERIOD / T6).
- Prompt-only changes are not free if re-roll rate rises. At HF still prices used in long-form tables (~$0.30/plate) or seedream (~$0.05 in living-page notes), every re-roll is real spend + human audit time.
- The “$0” claim is **not honest** given the proposal’s own defect sample. At minimum cost model must be: *baseline re-roll rate → expected re-roll rate with depth rules → delta $ per episode*.

---

### 4. “Shallow DoF” fights the locked ink style (critical)

**Rule 2:** *"Shallow depth of field — one plane sharp, others soft."*

Conflicts with production style:

- `VISUAL_STYLE_BASE_GN`: **“flat cel-shaded comic colour”**
- `VISUAL_STYLE_TAIL_GN`: **“not photorealistic, not a glossy 3D render”**
- Comics build depth with **overlap, scale, line weight, solid blacks** — not lens bokeh.

Risk the plan names (“DoF → photoreal drift”) is correct and under-weighted. Making DoF **mandatory on every still** is the most dangerous of the four rules: it is camera language that pulls seedream toward photo/cinematic blur and away from inked graphic-novel purity.

**Better comic-native substitute (not in plan as the default):** “near figures overlap far figures; far forms smaller/simpler ink; no soft-lens bokeh.”

---

### 5. Universal rules vs sacred / hero / landing beats (high)

**Rule 3–4:** foreground-near-lens + committed low/macro/crane on **every** scene  
**Risks:** *“does assertive foreground-macro/low-angle CHEAPEN the holy…”*

Existing locks already push the opposite for sacred landings:

- Hero / gospel-pivot is to be **iconic, near-still, loop-friendly** (constitution design-for-the-cut).
- EW01 hero (#25) is deliberately face/hand open-door close — not a silhouette-cluttered deep stack.
- LF-CLIP rules: **no locomotion / no invent**; calm sacred holds are first-class.

A hard universal “foreground element crossing the lens” will:
- cheapen Christ-enthroned / veil / landing frames, and/or  
- create a **new monotony** (every shot = soft shoulders at the bottom) — undermining “anti-slideshow variety.”

**Missing bound:** tier the rule (establishing/action = depth OK; hero/sacred/landing = calm frontal or simple mid, **exempt** from near-lens + DoF).

---

### 6. Animation-safety risk is real and under-specified (high)

**Phrase:** *"frozen-tableau content **stay identical**"*  
**Risk:** *“foreground figure near the lens is prime for the model to animate”*

Content does **not** stay identical if you add more near-camera figures and sharp/soft planes.

Repo evidence:
- Seedance invents motion on multi-figure/action panels (locked 2026-07-17 bake-off).
- Long-form uses veo / hybrid atmospheric i2v; LF-CLIP-NOINVENT / NOLOCOMOT exist **because** extra ambiguous near-field content gets completed into motion/hands/figures.
- Veo3-aware still design already wants **atmosphere** (dust, light), not more animate-able people at the lens.

**Missing verification:** no before/after clip QC plan (same still → same animator → invent-motion rate). Adopting still rules without measuring Stage 2c is incomplete for this engine.

---

### 7. `parallax_25d` advantage is oversold (medium–high)

**Phrase:** *"make our `parallax_25d` 2.5D tool actually work (a flat still has nothing to separate)"*

`panel_animator/parallax_25d.py` + skill:
- extracts **one** rembg salient cutout, not fg/mid/bg layers;
- amps kept small to hide ghosting;
- skill already says multi-layer is **future** work (“extend if 3-layer needed”);
- multi-element deep stills can make rembg **worse** (wrong salient pick: hand vs body vs crowd).

Depth-layered stills do **not** automatically unlock better 2.5D. Treating parallax as a primary justification is a false dependency. Parallax is selective ($0 calm panels), not the main long-form path (real generative clips).

---

### 8. Duplicates / ignores existing composition machinery (medium)

Repo already has anti-flat tools the plan barely engages:

| Existing control | What it already does |
|---|---|
| **SP-G8** framing mix | wide/mid/close/overhead/low-angle; no one framing >50% |
| **Cliché blocklist** | bans “centred-mid-shot symmetry across every scene” |
| **T5** | ≤3 sharp faces; rest soft-focus/shadow |
| **macro_elements** | near-camera cut anchors without full restage |
| **vignettes / unified scenes** | mid-depth supporting memory layers |

Adopting four **new mandatory** rules without mapping “reuse vs replace” risks stacking prompt weight, conflicting guidance, and no deterministic gate (no SP-G# for “must name two depth planes”).

**Missing:** where this lives (constitution? `visual_engine` discover prompt? SP deterministic pre-check?) and how FAIL is defined.

---

### 9. Retrofit EW01 cost is undercounted and poorly timed (high)

**Phrase:** *"retrofitting EW01's 25 existing stills (**~$7.50 + re-animation**)"*

EW01 inked already has:
- 25 PNGs under `visual_16x9_inked/`
- 25 clips under `clips/`
- assembled `EW01_Two_Goats_16x9.mp4`

Real cost stack if retrofit:
1. 25 stills + **re-rolls** (period/anatomy/extra figure)  
2. **25 re-anims** (veo/hybrid — often larger than still cost)  
3. clip QC + re-assemble + score/sfx/caption as needed  
4. human still-review / bible-check re-touch  

~$7.50 is **stills-only at ~$0.30 with zero re-rolls** — fantasy given the 50% period-slip sample. Retrofit is **not** justified until (a) the rule is proven on new work, (b) a short list of *actually flat* scenes is named, not a blanket 25.

Also: scene_plan still carries legacy Baroque `style_base` strings while ink render uses `STYLE_REGISTRY` — composition rewrite on all 25 is a larger plan rewrite than “add four rules to subject_block.”

---

### 10. Over-engineering / premature standardization (critical)

**Decision asked:** *"Adopt this as the **standard for all NEW inked still work**?"*

That is premature. Correct process for this repo (test-gate before batch, LF-INV-7, cost skill):

1. Finish red-team sample; human eye on full-res.  
2. Keep **only** rules that survive (likely: explicit scale/overlap layers; **drop** mandatory shallow DoF).  
3. Pilot on **one new episode’s** establishing beats only.  
4. Measure re-roll + clip invent rates.  
5. **Then** write a bound constitution clause — not a global SHOT formula import from ArkAIology.

Importing an external four-rule “discipline” as default is process theater relative to n=2.

---

### 11. Implementation gaps

- No comic-native wording as the **preferred** depth language.  
- No sacred/hero exemption.  
- No interaction with T5 / SP-G8 / banned tokens / style tail.  
- No gate, no schema field, no “when NOT to apply.”  
- No decision matrix: Reject / Bound pilot / Full standard — only a yes/no framed as standard-or-not.  
- No spend pre-flight for retrofit beyond a single optimistic line.

---

### Bottom line

Depth **can** help flat establishing panels. The two cherry-picked stills may look better. That does **not** justify:

- mandatory shallow DoF on every still,  
- mandatory near-lens clutter on sacred/hero frames,  
- “$0 going forward,”  
- full EW01 retrofit, or  
- pipeline standard status.

**Bound or reject; do not adopt as written.**

---

VERDICT: REVISE  
TOP FIXES:  
1. Drop “adopt as standard” and full EW01 retrofit until a stratified red-team (≥ reverent + multi-figure + variance) passes with period/style/i2v metrics — n=2 + 50% period-slip is a hard block.  
2. Split the four rules: keep optional **scale/overlap depth layers + committed angle** for establishing/action only; **forbid mandatory shallow DoF** (conflicts with flat cel-shaded ink + photoreal drift); **exempt hero/sacred/landing** from near-lens foreground.  
3. Replace “$0 / only subject_block changes / parallax needs this” with an honest cost+reuse model (re-roll delta, re-anim cost, map to SP-G8/T5/macro_elements) and measure invent-motion before any global prompt rule.
