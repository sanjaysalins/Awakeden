# Independent review — cursor (OK, 130s)

## Findings

### 1. The A/B baseline is mischaracterized — improvement may be incremental, not “flat → deep”

The proposal says Scene 1 went from a **“flat centered postcard”** to a deep establishing panel. The **existing** EW01 scene-1 `subject_block` already specifies scale, crowd, and backdrop:

```41:41:longform/EW01_Two_Goats/v1/visual_16x9_inked/scene_plan.json
      "subject_block": "The high priest Aaron, small in golden vestments, stands alone before the towering curtained Tabernacle court at first light; behind and below him a vast hushed multitude of Israelites kept in shadow; immense pale sky; the sacred tent dominant and severe.",
```

Scene 7’s original block is already hand-forward (`"Aaron's weathered hands... holding two small marked lot-stones"`). The test scripts add **cinematic/DoF/macro vocabulary**, not depth where none existed. The evidence may show “more assertive camera language helps,” not “our stills are flat without this.” That weakens claimed advantage #1 and #4.

---

### 2. Rule 2 (“shallow depth of field”) directly fights the locked ink style stack

The plan says **`VISUAL_STYLE_BASE_GN` / `_TAIL_GN` stay identical** and only composition language changes. That is not true at the **assembled prompt** level: `assemble_final_prompt` concatenates subject + style into one string (`pipeline/visual_render.py`).

Both halves of the GN style block explicitly demand **2D ink, not lens physics**:

```460:469:config.py
VISUAL_STYLE_BASE_GN = (
    "Inked biblical graphic-novel / cinematic-manga illustration, bold clean "
    "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn "
    "2D artwork, dramatic ink shadows,"
)
VISUAL_STYLE_TAIL_GN = (
    "reverent and holy atmosphere, ancient Near-Eastern period-accurate, strong "
    "visible ink lines, no oil-painting brushstrokes, not photorealistic, not a "
    "glossy 3D render, not soft airbrushed anime, no text, no lettering, no "
```

Rule 2 asks the model to resolve a contradiction: **“flat cel-shaded” + “shallow depth of field.”** Models usually pick photoreal lens behavior and add a comic filter on top — exactly the drift the audit rubric is meant to FAIL (`STYLE_AUDIT_RUBRIC["graphic_novel"]` line 436–437: FAIL on **PHOTOREALISTIC or glossy 3D-RENDER look**). The plan names this risk but still bundles DoF as a mandatory rule instead of rejecting or replacing it with 2D-native depth (overlap, line weight, atmospheric fade).

---

### 3. Advantage #1 (`parallax_25d`) is a false linkage — and the tool is not on EW01’s critical path

Claim: **“deep stills… make our `parallax_25d` 2.5D tool actually work (a flat still has nothing to separate).”**

`parallax_25d.py` does **not** read prompt-stated depth layers. It runs **rembg once** on the nearest salient subject, composites that cutout over the full plate, and drifts the two layers:

```27:32:panel_animator/parallax_25d.py
def render(still: Path, out_mp4: Path, duration: float, fg_amp: float, bg_amp: float):
    base = Image.open(still).convert("RGB")
    ...
    fg = remove(base, session=session)          # RGBA cutout of the nearest subject
```

Bronze Serpent already uses `_render_parallax` in `dynamic_cam.py` on **existing** stills without this prompt discipline. `panel_animator/README.md` says parallax is **selective**, for calm panels — not a reason to rewrite every still. `RESUME.md` notes parallax was **only proven in the 60s prototype, never long-form**. EW01’s shipped path is Seedance/Kling panel clips (`_CLIPS_REVIEW.html`), not `parallax_25d`. Basing a global still standard on an unproven, non-default animator is premature.

---

### 4. Rule 3 (foreground crossing the lens) is the highest animation-regression risk — and the plan treats it as optional concern, not a blocker

The proposal asks whether foreground elements **“undo the frozen-tableau discipline.”** They do, structurally:

- Constitution **“Kling-friendly composition”** requires state-only tableaux and **macro-insertable cut anchors**, not near-lens figures primed to move (`data/constitution.md` §526–551).
- Locked comic-grid discipline: Seedance **invents motion** on hands/action panels; foreground-near-lens is the worst bait (CLAUDE.md comic-grid animator tiering).
- EW01 depth prompts literally push **“Extreme foreground, close to the lens”** hands and crowd silhouettes (`_test_depth_prompt.py` lines 27–28, 38–39).

The plan keeps rule 3 in the **universal four-rule bundle** while only *asking* about animation safety. That is backwards: rule 3 should be **beat-conditional** (establishing/action only), with explicit frozen-tableau reinforcement, or dropped until animated on Seedance/Kling and filmstrip-QC’d.

---

### 5. Rule 4 (“one committed camera angle… on every inked still”) collides with existing composition gates and pacing

Constitution **SP-G8** already enforces framing variety: `{wide, mid, close, overhead, low-angle}`, ≥3 distinct, none >50% (`data/constitution.md` §513–518). Forcing **low three-quarter / macro / crane on every still** is not variety — it swaps “flat centered monotony” for **“every beat is a blockbuster shot”** monotony. That directly threatens the plan’s own reverent-beat question: scene 25 is already **“HERO CLOSE… The landing”** — adding macro + foreground veil edge + low angle (`_redteam_depth.py` SCENE20/SCENE24) risks cheapening what is intentionally still and frontal.

---

### 6. Evidence is statistically unusable; red-team work exists but is not in the decision

The plan honestly flags **“n=2, scenes chosen for obvious depth potential”** and **50% period-slip (cross finial)** — then asks whether to adopt as **standard for all NEW inked still work**. That is not a proportionate decision threshold.

`_redteam_depth.py` was written to attack exactly this (reverent scene 20, multi-figure scene 24, variance rerolls) — **~$1.50, 5 stills** — but the proposal does not cite those results. `_depth_test/` outputs are not in the repo; the A/B images are unverifiable from the artifact alone. **Decision before red-team completion** is a verification gap.

---

### 7. “Zero marginal cost” / “$0 going forward” is false under your own defect model

The plan asks whether **“$0 going forward”** is honest given QC/defect rate — it is not:

- **50% period-slip in n=2** implies rerolls, not $0.
- More layers + foreground crowds + macro hands increase **T5 crowd mush**, **T3 eye errors** (guardrails prefer mid-shot over extreme face macro; `data/render_guardrails.md` §T3, §T5), and **T6 anachronism** surface area.
- Each failed still pays **HF seedream + Claude Vision audit retry** (`render_scene` retry loop in `visual_render.py`).

Rule 2–3 compositions are **more expensive in expectation**, even if the prompt text itself is free.

---

### 8. Retrofit cost is materially understated

**“retrofitting EW01's 25 existing stills (~$7.50 + re-animation)”** counts first-pass stills only (~$0.30 × 25). It omits:

- Audit rerolls at higher defect rate.
- **Re-animating ~25 panel clips** (Seedance/Kling — dominant spend; `_CLIPS_REVIEW.html` shows mixed tiers).
- Re-running assembly verify, filmstrip QC, `panel_variety_lint` retags, human eye review.
- Risk of **reuse_swap slug/filename gotcha** if subject_blocks change without matching pipeline idempotence (`RESUME.md` GOTCHA).

Real retrofit is **multiples of $7.50**, not $7.50 + marginal re-animation.

---

### 9. Missing enforcement / wiring plan (unlike your own guardrails precedent)

`data/render_guardrails.md` has an explicit **“Wiring plan”** (constitution → negative tail → banned tokens → gate). This proposal says **“prompt-system rule applied to every still”** but specifies **no** integration point:

- Not in `scene-plan-long` SKILL
- Not in SP-G8 / deterministic pre-checks
- Not in `verify_image` / audit rubric (which would need to FAIL photoreal bokeh if rule 2 stays)
- Not in `_build_inked_scene_plan.py` or constitution VISUAL ARC

Without wiring, “standard” is aspirational text, not enforceable pipeline behavior.

---

### 10. Unified / multi-vignette scenes are unaddressed

EW01 has unified tableau scenes (e.g. scenes 14, 15, 19, 20: **“soft-edged… single unified canvas”**). Mandatory **three physical depth layers + foreground lens-cross + committed angle** fights **SP-G6 vignette discipline** (soft memory panels, not diorama layers). The plan’s generalization question is real and has **no carve-out** for `scene_type: unified` or gospel-pivot hero frames.

---

### 11. Reuse: good on tools, bad on prior art

The plan correctly avoids duplicating renderers — it only touches `subject_block`. But it **does not reuse** existing composition infrastructure:

- SP-G8 framing variety
- Constitution macro_elements / cut-anchor discipline
- Render guardrails T1–T6
- Prior shorts “depth stills” work (`render_depth_stills.py`) used **scene-specific** depth language, not a blind four-rule injection

---

### 12. Over-engineering: global standard before bounded pilot

Jumping from n=2 cherry-picks to **“every still in every episode”** plus an EW01 retrofit decision is premature building. A proportionate plan would: pilot on **next new piece**, stratified by beat type (establishing / teaching / sacred / landing), measure **still pass rate + animation filmstrip fail rate**, then decide. The artifact jumps straight to org-wide adoption.

---

VERDICT: REVISE
TOP FIXES:
1. Drop or replace rule 2 (“shallow depth of field”) with 2D-native depth language (overlap, line-weight, atmospheric recession) so it cannot fight `VISUAL_STYLE_BASE_GN`’s “flat cel-shaded” and the photoreal FAIL rubric.
2. Do not adopt rules 3–4 globally — make foreground-lens-cross and extreme angles **beat-conditional** (establishing/action only), with explicit sacred/landing/hero exemptions; finish `_redteam_depth.py` and require animation filmstrip QC before any standard change.
3. Halt EW01 retrofit; if pursued later, budget still rerolls + full re-animation/assembly QA (not ~$7.50), and add a wiring plan (constitution / scene-plan skill / audit rubric) before calling it a pipeline standard.
