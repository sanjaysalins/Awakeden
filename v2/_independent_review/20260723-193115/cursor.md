# Independent review — cursor (OK, 178s)

## Independent adversarial review — `AWAKEDEN COMIC DNA` v0.2

### 1. Internal contradiction on the single most important claim (character lock)

The doc simultaneously says two incompatible things about the drift fix:

- **Red-team outcome:** “Character drift FIXED — render Christ + recurring cast on **`nano_banana_pro` + a chained `--image` reference** … `seedream_v4_5` = **neutral plates only**.”
- **§1 (LOCKED):** “**Model = `seedream_v4_5` for EVERYTHING**” and “proven: Seedream 4.5 + `christ_pc_ref` held the SAME man.”

The actual prove-it script uses **`nano_banana_pro`**, not Seedream:

```19:19:longform/EW01_Two_Goats/_retro_dna/_prove_it.py
MODEL = "nano_banana_pro"
```

Seedream+ref is a *separate* ad-hoc test (`_seedream_ref.py`), and its output folder is not present in the repo snapshot — so “proven on Seedream 4.5” is an assertion, not a reproducible artifact here. **You cannot lock Seedream-for-everything while citing NBP as the proven drift fix.**

---

### 2. “LOCKED 2026-07-23” vs “DRAFT, NOT yet binding” — commitment language still broken

Header: **“Status: DRAFT … NOT yet binding”** and §9: **“Only after the pilot wins do we wire into `config.py` …”**

But §1 opens with: **“The look — the recipe (LOCKED 2026-07-23: Seedream 4.5, moderate retro)”** and §3: **“LOCKED for the pilot: the `PocKineticType` gold treatment.”**

That is the exact over-commitment the red-team said to fix. “Pilot decides kitsch” and “recipe LOCKED” cannot both be true in the same revision.

---

### 3. Conflicts with binding `v2/SPEC.md` and live `config.py`

**§1** locks **`seedream_v4_5` for EVERYTHING** and cites **`[[locked-stills-provider-split]]`**.

Binding spec says the opposite split:

```338:339:v2/SPEC.md
- **Provider split (locked):** NBP $0.50 (Christ/face), HF `nano_banana_2` $0.30
  (neutral plate), direct-Kling $0.65 (animation).
```

Live registry already has `graphic_novel` → `seedream_v4_5`, but its prompts are **inked cinematic-manga**, not Silver Age Ben-Day retro:

```460:469:config.py
VISUAL_STYLE_BASE_GN = (
    "Inked biblical graphic-novel / cinematic-manga illustration, bold clean "
    "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn "
    "2D artwork, dramatic ink shadows,"
)
```

The DNA retro recipe (“1960s Silver Age … coarse Ben-Day dots … CMYK misregistration”) is a **new style identity**, not an “extend `STYLE_REGISTRY`” tweak. The incorporation map understates that.

Also: **`RESUME.md` still documents painted-comic (`nano_banana_pro` + chained refs) as the chosen go-forward**, with explicit note that **HFProvider ref-chaining is not production-wired**. This plan pivots again without reconciling that fork.

---

### 4. Character ref chaining is not production-ready (despite “MANDATORY”)

§1: **“chain the character's `--image` reference into *every* frame they appear in”**

`HFProvider` exposes `extra_ref_paths`, but **`render_scene()` never passes them**:

```592:592:pipeline/visual_render.py
        png_bytes = provider.generate(scene, audit_feedback=feedback)
```

Class doc still says **“No reference-image attachment by default”** and `supports_character_anchor = False`. Ad-hoc `_prove_it.py` / `_seedream_ref.py` bypass the pipeline via raw `hf` subprocess — exactly what `RESUME.md` warned about. **Mandatory rule ≠ enforceable until scene_plan + runner wire refs per recurring character.**

---

### 5. §8 incorporation map is stale vs the author’s own POC work

| Claim in §8 | Reality in repo |
|---|---|
| “Narrator caption box … **BUILD — CSS mockup only**” | Built in `DnaPocFilm.tsx` (`Caption` component, comic-yellow `#ffe100`) |
| “**Kalam.ttf NOT in repo**” | `DnaPocFilm.tsx` loads `Kalam-Bold.ttf`; `RESUME.md` says it’s vendored in `_remotion/public/` |
| “Kinetic Scripture type … **BUILT** (the one proven Remotion piece)” | True — but §8 ignores caption/SFX also exist in the same POC file |

If the external reviewer reads §8 alone, they will **under-estimate progress and over-estimate “BUILD” scope** — bad for pilot scoping.

---

### 6. Print-finish: honest OPEN flag, then contradicted downstream

§1 is good: **“OPEN: this finish is a still-image pass; it is NOT yet proven on animation”** and warns of **dot crawl/moiré**.

But §6 says: **“print-finish over the top”** on living plates. `DnaPocFilm.tsx` comment claims **“dots baked into the plate = no crawl”** with no print-finish pass on video. The existing **`/print-grade` skill** already documents clip-duration pitfalls and multiply-blend discipline — the plan proposes reconciling three scripts instead of naming **`panel_animator/print_grade.py`** as the canonical clip path and proving *that* on animated panels.

Three-way reconciliation (`_print_finish.py` / `print_grade.py` / `_retro_grade_demo.py`) before lock is right — but **no step says “run print-grade on dnapoc clips and eyeball 6s loops for crawl.”** Verification gap.

---

### 7. Format-split (§9.3) fights locked production grammar

§9.3: **“full-bleed single-focal-point for 9:16 Shorts (no tier grids / page-turns on a phone)”**

Project locked rule: comic multi-panel grids with real animated clips per cell (Bronze Serpent, panel animator tiering). Shorts today are **9:16 Kling gallery-tour hard cuts**, not Remotion tier pages. The plan introduces a **third assembly paradigm** (Remotion retro tiers for long-form, full-bleed for shorts, existing comic-grid lane for shipped pieces) without a migration or “which lane owns shorts going forward” decision.

---

### 8. A/B protocol (§9.2) is underspecified and expensive

**“Cold-audience A/B on real traffic … retro-comic vs plain cinematic-inked”** on thumbnail CTR, 3s retention, comment sentiment:

- No **sample size**, **duration**, or **statistical bar** — YouTube noise will not resolve “kitschy tract” in a handful of pieces.
- Each arm needs **full still set + animation + assembly** (or a parallel Remotion rebuild) — not “$0 until pilot.”
- **“Same piece cut two ways”** ignores that retro DNA also changes **lettering, SFX, tier grammar** — not a single-variable A/B unless you control for motion/edit differences.
- Comment-sentiment scraping is manual, biased, and slow — not a gate.

The free **`_KITSCH_TEST.html`** (§10) is the right cheap test; §9.2 jumps to paid traffic before proving the cheaper instrument has been sent and read.

---

### 9. Cost / spend claims are not honest

- §1: **“cheap ($0.15)”** for Seedream vs `v2/SPEC.md` living-page lane **~$0.05/still** — pricing inconsistent inside the same project.
- §10: **“Nothing costs render money until the pilot”** — false against `STATE.md` / `RESUME.md`: 14-model bake-off, `_prove_it.py`, `_dnapoc_animate.py` (~$3.70), hook renders, etc. already spent metered HF.
- §9 pilot: **“~Cluster-1 scale, a handful of pieces”** — undefined unit; no spend ceiling quoted despite `/cost` + INV-20 being binding project discipline.

---

### 10. Doctrine body gate (§5) is Vision-only; banned tokens not in deterministic layer

§5 **Body gate:** Vision FAIL on idealized musculature + ban tokens **`muscular / heroic / athletic / six-pack / V-taper`**.

Those tokens are **not** in `config.VISUAL_BANNED_TOKENS` (grep: no matches). Passion prompts can still ship without a deterministic pre-render FAIL. Vision audits on sacred frames are necessary but **known-unreliable** for subtle body-shape failures — the plan admits Vision is needed for `/dna-check` substance but doesn’t add SP-G5-style deterministic substring checks for passion beats.

Also: `_prove_it.py` notes **NSFW rejection on bare-torso cross** — a provider SPOF not in §5. Robed framing may be mandatory for HF, not “a per-piece call.”

---

### 11. Reuse failures — rebuilds what already exists

- **SFX overlays:** §8 says **BUILD Remotion component**; `panel_animator/` already has **`/impact-burst`**, Bangers styling, spread-thin discipline — plan doesn’t say reuse vs replace.
- **Captions:** **`/typography-panel`** skill’s locked default is **parchment caption band**; §3 locks **comic-yellow `#FFE100` box** — conflicts with existing panel-animator standard (“parchment band is STANDARD default” in project rules).
- **`/dna-check`:** proposed new gate overlaps **`validate` skill**, `check_landing_hold.py`, `add_watermark.py`, render lint — no mapping of which existing gates absorb DNA checks vs net-new Vision spend.

---

### 12. Motion / word-timing gap blocks tier grammar

§6 honestly flags: **“Word-timed panel slams are a TARGET, not yet built”** — good.

But §5 tier grammar (6/9 grids, cliffhanger panel, beat map) **depends on word-synced reveals** for the “comic” feel. `EW01Slices.tsx` uses **approximate 40%-into-window timing** and is **full-bleed, NO grid** (§8 admits this). §6 promises **“tier reveals, page-turn transitions”** without a dependency chain: forced alignment port from `build_livingpage_16x9.py` → Remotion tier composer → pilot.

---

### 13. Long-form hero bookend gap acknowledged but not gated

§5: **“long-form Remotion path needs its own bookend check — coverage gap to close”**

No step in §10 lock process adds **LF-AS-G6/G7 equivalent** before pilot. Shorts have AS-G6/G7; long-form DNA POC (`DnaPocFilm`) is 4 beats with no open/close Christ bookend enforcement.

---

### 14. Animation model mismatch

DNA POC animates via ad-hoc **`kling3_0` + `seedance1_5`** (`_dnapoc_animate.py`). `STYLE_REGISTRY["graphic_novel"]["anim_model"]` is **`cinematic_studio_video_v2`**. Locking DNA in config without reconciling **which animator owns retro plates** will produce wrong defaults on `run_piece --stage animate`.

---

### What the revision got right (minimal credit)

- §0 “system with range, not dial-to-11” is a real fix to kitsch risk.
- §1 print-finish caveat (luminance mask naivety, animation crawl) is honest.
- §9 “pilot before 76” and §10 migration/grandfathering policy are sensible.
- §10 `/dna-check` scope honesty (“mostly provenance stamping, not look-verification”) is correct — rare good instinct.

---

VERDICT: REVISE
TOP FIXES:
1. **Pick one character-lock recipe and align all proof to it** — either revert to NBP+ref for Christ/recurring cast (per `_prove_it.py` and `v2/SPEC.md` split) or publish reproducible Seedream+ref artifacts and a side-by-side drift test; delete the contradictory “nbp fixed / seedream everything” pairing in §red-team + §1.
2. **Strip all “LOCKED” labels until after pilot** — replace §1/§3 locks with “pilot candidate”; wire incorporation map to what `DnaPocFilm.tsx` already proves (caption, Scripture, SFX, Kalam) vs what is genuinely unbuilt (tier grid, balloons, production ref wiring).
3. **Add a verification spine before any paid pilot:** (a) print-grade on animated dnapoc clips — eyeball crawl; (b) wire `--image` refs through `render_scene` + scene_plan fields; (c) deterministic passion-beat token bans in config; (d) define A/B as kitsch HTML first, then a scoped 1-piece dual-render with a quoted spend cap and one primary metric.
