# Independent review — cursor (OK, 190s)

## Independent adversarial review — AWAKEDEN COMIC DNA v0.3

### 1. “Production-wired” ref-chaining is still ad-hoc (load-bearing)

§1/§8 mark ref-chaining as **“FIXED 2026-07-23”** and “proved end-to-end through the real function.” That overstates what was proven.

`render_scene()` now accepts `extra_ref_paths` — verified in `pipeline/visual_render.py` lines 551–600. But the **only production orchestrator** that calls it, `visual_runner.py` lines 323–326, still invokes:

```323:326:pipeline/visual_runner.py
        png_path, audit = visual_render.render_scene(
            scene, provider_obj, render_dir,
            max_retries=config.MAX_NBP_RETRIES, log=log,
        )
```

No `extra_ref_paths`. The proof path is `_smoke_render_scene.py`, which **monkeypatches** a throwaway `STYLE_REGISTRY["retro"]` entry and passes refs manually — explicitly *not* written to `config.py`.

There **is** an existing long-form renderer that reads `refs` from scene plans: `longform/_render_world.py` (lines 17–21, 131–157). §8’s incorporation map never mentions it. Instead the plan treats ref wiring as net-new BUILD while duplicating a parallel subprocess pattern (`_prove_it.py`, `_aaron_ref.py`, `_seedream_ref.py`).

**Single point of failure:** the pilot can “succeed” via one-off scripts while the path `cli_visual.py` / `visual_runner.py` users would actually run remains broken.

---

### 2. Cast reference bank is fragmented and inconsistent with EW01’s live scene plan

§8 lists **`christ_pc_ref.png` + `_retro_dna/aaron_retro_ref.png`** as the cast bank. EW01’s authoritative `scene_plan.json` points elsewhere:

```570:576:longform/EW01_Two_Goats/v1/visual_16x9_inked/scene_plan.json
    "cast": {
      "aaron": {
        "portrait": "Head-and-shoulders character portrait of Aaron..."
      },
      "christ": {
        "ref": "image_library/stills/christ_risen_face_scars.png"
      }
```

That Christ path **does not exist** in `image_library/stills/` (no `christ_risen_face_scars.png` in the repo). Prove-it/smoke tests use `v1/visual_16x9_inked/_painted_comic_test/christ_pc_ref.png`. Aaron’s DNA ref is a third path (`_retro_dna/aaron_retro_ref.png`), not wired into `world.cast`.

§1 still says **“Also open: only Christ has a locked ref — Aaron…”** while a few paragraphs later **“Aaron's locked reference — DONE.”** DONE means one PNG exists; it does **not** mean the production cast bank or `_render_world.py` will use it. Aaron is explicitly **not** chain-tested like Christ’s 3-scene `_prove_it/` run.

Top-of-doc ✅ **“Character drift FIXED — Christ + recurring cast”** is still ahead of evidence for Aaron.

---

### 3. `Scene` model ignores EW01’s `refs` field — cost split rests on dead metadata

§9’s **17 character / 8 plate** still split is derived from `scene_plan.json`’s `"refs"` arrays (17 non-empty, 8 empty — arithmetically correct). But `Scene.from_json()` in `visual_models.py` lines 94–125 **never loads `refs`**. Nothing in `pipeline/` maps `"refs": ["aaron"]` → `extra_ref_paths` except ad-hoc longform scripts.

Worse: the heuristic **refs ≠ character-model scenes**. Scene 13 is a crowd (`refs` empty → seedream) but `_animate_inked.py` puts it on **Kling** for motion-invention risk. Scene 14 has refs but is a ghosted multi-echo tableau — arguably plate-tier art with ref attach. The 17/8 table treats accounting labels as render policy without a defined rule.

EW01’s plan also has **no `jesus_variant`** anywhere (grep: zero matches). §5a’s passion/glory split and `assembly_engine.py` passion detection depend on that field. Passion Christ body tokens were added to `VISUAL_BANNED_TOKENS` (good), but SP-G5 only scans `subject_block` + `mood_block` — and this long-form plan has **no `mood_block` keys at all**.

---

### 4. §6 (Remotion) and §9 (pilot cost/animation) describe different products

§6 **ENGINE DECISION**: retro DNA does **not** extend `build_livingpage_16x9.py`; Remotion is a **separate engine** with **BUILD, not ported** word-exact slams, DoD gates, reuse/richness counters.

§9 then budgets **25 Seedance/Kling clips** copied from `_animate_inked.py` (8 Kling / 17 Seedance — matches `KLING_SCENES` in that script) and compares to a **~$29–34** total.

Missing from that envelope:

| Gap | Why it matters |
|-----|----------------|
| Full **Remotion long-form composition** (~584s, 25 beats) | POC is 4 beats (`_dnapoc_animate.py`) + splash hooks (`DnaSplashHook.tsx`), not EW01-scale |
| **Forced-alignment consumer** for word-timed slams (§6 admits TARGET, not built) | Without it, “cinematic inked comic” motion is hand-timed springs, not livingpage parity |
| **~25 Opus Vision still audits** via `render_scene()` | Every production render audits; not in §9 table |
| **Scene-plan / world-block rewrite** | `world.style` is still `"Baroque oil painting… Caravaggio and Rembrandt"` (scene_plan lines 555–560); per-scene `style_base` strings still say Baroque despite top-level `"style_base": null` |
| Print-finish on **animated** output | §1 OPEN: dot-crawl on screen-space finish; §6 says “print-finish over the top” anyway |

The plan grounds animation cost in ink migration tiering but assembly in a **different engine that doesn’t consume `_animate_inked.py` output paths by default** (`_paint_ew01_animate.py` lands clips in `_remotion/public/pc/` — different convention from `v1/visual_16x9_inked/clips/`).

---

### 5. Two-model recipe creates a third provider fork, not a clean override

§1 correctly notes HF `nano_banana_pro` ≠ direct Google `NBPProvider`. But `_render_world.py` — the closest thing to a production ref-chaining path — defaults to **`nano_banana_2`** (lines 54–64), not `nano_banana_pro`. `HFProvider.supports_character_anchor = False` (line 225) means SP-G7 character consistency is **advisory on HF runs** — unaddressed in the plan.

User decision to supersede `[[locked-stills-provider-split]]` is documented only in this draft doc (“NOT yet binding”, header). `config.py` `STYLE_REGISTRY` still has only `baroque` and `graphic_novel` — no `retro` / `awakeden_comic` key (§8 admits this). Pilot spend before SPEC/skill wire-in risks another silent memory-vs-code split like round 1’s Seedream false claim.

---

### 6. Border defect mitigation is manual and probabilistic, not pipeline-guaranteed

§1 claims `(a) VISUAL_BANNED_TOKENS` + retry loop catches bordered renders automatically. Tokens include `"border"` / `"frame"` (config.py ~525). But:

- The plan **same section** admits borders are **stochastic** (`_aaron_ref.py` bordered with no newsprint wording).
- Smoke test used **`max_retries=0`** — retry loop wasn’t part of the proof.
- Mitigation `(b)` is a **manual ~4.5% crop** on reference PNGs — not codified in `render_scene()` or `_render_world.py`.

Budgeting “most border fixes are a $0 crop” hides operator labor and doesn’t scale to 25 deliverable frames (only refs).

---

### 7. Print-finish: three scripts, contradictory animation strategy

§1 honestly flags `_print_finish.py` (still, luminance-masked) vs `panel_animator/print_grade.py` (clip, **unmasked** screen-space halftone) vs `_retro_grade_demo.py`, and says reconcile before lock. Good admission — but §6 still plans “print-finish over the top” on generative clips while `_dnapoc_animate.py` line 2–3 assumes **dots baked into plates** “move WITH the art = no dot-crawl.” Those are **mutually exclusive** strategies; the plan never picks one for the pilot.

`print_grade.py` applies a fixed screen-space dot texture over **moving video** — exactly the moiré/crawl risk §1 warns about.

---

### 8. A/B protocol doesn’t isolate the variable under test

§9.2’s corrected protocol (good catch on duplicate-content / Shorts thumbnail CTR) compares EW01 retro **between-subjects** against “last 2–3 comparable already-shipped inked/painted longs.”

Problems:

- **Confounds topic, hook, and audience fatigue** with style (Two Goats vs Bronze Serpent, etc.).
- **No pre-registered baseline metrics** (which 2–3 pieces? what AVd threshold = “meaningfully below”?).
- **Kitsch gate** (`_KITSCH_TEST.html`, “still unsent”) has no send protocol, audience definition, or kill criteria — it’s a HTML file, not a executed test.
- Publishing one retro long before validation still spends ~$30+ and weeks of Remotion build — the “free test first” ordering is stated but not enforced by a hard stop before any `_aaron_ref.py`-class spend (§10 admits R&D spend already moved).

---

### 9. Over-engineering before proof — Remotion fork vs reuse

§6 rejects extending livingpage (defensible for comic gutters / misregistration) but **does not price the rebuild** of livingpage’s mature capabilities listed in the same paragraph: ±0.05s word-snapped slams, DoD gates, §3b reuse/richness. Meanwhile **built and reused**: `PocKineticType`, `CaptionBox`, 2-up panels, SFX — all POC-scale.

§8’s **“~55% owned, ~45% to build”** still counts POC demos (`dna_splash_hook_v6.mp4`, 36s combo) as ownership of a **~10-minute** EW01 film. Missing for pilot: 6/9-tier grids, page-turns, balloons, word-timed slams, long-form Christ bookend gate (§5 admits “coverage gap”), thumbnail/website skins.

§10’s `/dna-check` is sketched before lock — and the plan itself admits it’s **“mostly provenance stamping, not look-verification”** while the substance checks are **paid Vision**. That duplicates `verify_image`, assembly verify, and `validate` without mapping which existing gates absorb DNA checks.

---

### 10. Cost table is a floor, not a pilot quote — and omits known spend classes

§9 **≈$29–34** is internally consistent with `_animate_inked.py` tier math (8×$1.13 + 17×$0.72 ≈ $21.25 animation). But:

- Opus planning listed as **“$0-5”** with “agent-mode $0” — production `cli_visual.py` Phase A is metered Opus (~$3–5 in CLAUDE.md) plus independent review.
- **No line for Vision audits** on 25 stills (+ retries at `MAX_NBP_RETRIES`).
- **No line for Aaron 3-scene chain proof** or border re-rolls beyond a flat 20% buffer.
- §10 correction that R&D already hit `spend_ledger.jsonl` contradicts any reader who still thinks pre-pilot spend is zero — but §9 table doesn’t include sunk POC costs in the decision budget.

Sanity-check against prior ink migration (~$35.80) is weak: that run used one still model family and existing livingpage/comic-grid assembly — not Remotion-from-scratch.

---

### What the plan gets right (not praise — just credit where honestly earned)

- Round-1 **Seedream identity false claim** correction is real and ledger-backed.
- **Pilot-one-piece-not-three** and **A/B duplicate-content fix** are genuine improvements.
- **§0 “system with range, not dial-to-11”** matches what restrained renders actually showed.
- **`/dna-check` not oversold as $0-deterministic** (§10) is rare good discipline.
- **Dot-crawl / print-finish-on-animation** flagged OPEN instead of hidden.

Those fixes improve the document; they do **not** make the pilot executable on the production path as sequenced.

---

VERDICT: REVISE
TOP FIXES:
1. **Wire ref-chaining on the path the pilot will actually use before any paid stills** — extend `longform/_render_world.py` (or `visual_runner.py`) to pass `extra_ref_paths` from `world.cast` + per-scene `refs`, pin `HF_MODEL_ID=nano_banana_pro`, and unify Christ/Aaron ref paths in `scene_plan.json`; demote §1 “FIXED” to “smoke-test only” until that lands.
2. **Pick one assembly + print strategy and re-budget** — either Remotion full EW01 film (with forced-alignment + finish policy: baked-in-plate dots OR post-grade, not both) OR a minimal slice (e.g. 3–5 minutes / 8–10 beats) as the real pilot; add Vision audit + scene-plan/world rewrite costs to §9.
3. **Run Aaron multi-scene chain proof + dot-crawl test on a Kling/Seedance clip before the $29 pilot** — free gates (`_KITSCH_TEST.html` with defined audience/kill criteria, Aaron `_prove_it`-style chain, one dynamic clip through the chosen print path) must pass with explicit go/no-go, not “lower-severity, deferred.”
