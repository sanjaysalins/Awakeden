# Independent review — cursor (OK, 60s)

## Independent adversarial review — eyewitness SHORT visual strategy

This is a reasonable *question*, but the plan is **partly stale**, **assumes unvalidated transfers**, and **recommends spend before the cheapest proofs**. Findings below cite the artifact’s exact phrases.

---

### 1. Stale against the repo — you may be debating a decision you already made on audio/structure

**Lines 3–4, 14** — `~75–110s` and “viral/snackable entry” — no longer match shipped reality. `STATE.md` (2026-06-26) records a **punchy short redesign**: ~**150–200w → gates retuned to 120–210**, target **~60–75s**, structure **Hook → strange thing → turn → punch**, with `atempo=1.12` approved on Aaron. EW01 short audio is **~74.7s** (`narration.meta.json`), and the script is explicitly `(short, PUNCHY)` with 4 beats — not the calm B1→B3→B6→B7 frame implied here.

**Lines 35–38, 45** — “deliberately **intimate and calmer**” and “eyewitness short was intentionally made calm/intimate, which **fights punchy**” — that tension was **already resolved in text/audio**. Calm versions were kept as `narration.calm.md`; production shorts are punchy. The plan still frames “calm vs punchy” as open while **metered visual production is the stated next step** (`STATE.md`: “NEXT… metered VISUAL production”).

**Binding spec drift:** `v2/EYEWITNESS_SPEC.md` §1 still says SHORT = `220–320` words / `~75–110s` / slideshow boomerang, but `data/eyewitness_rules.json` now has `word_min: 120, word_max: 210`. The plan inherits the **old spec numbers**, not the enforced gates.

**Impact:** Option **C** (“**Boomerang/hold the calm middle beats**”) directly **fights** the approved punchy middle that is supposed to **race** (`STATE.md` line 45). A calm visual middle + punchy audio is a **retention mismatch** the plan never names.

---

### 2. Feasibility — long-form validation does **not** transfer to 9:16 shorts without a POC

**Lines 18–29** — “What we just validated on the LONG form” and the **vetted GREEN/RED camera palette** — validated **only at 16:9**. `longform/_test_camera_palette.py` hard-sets `config.VIDEO_HF_ASPECT = "16:9"` and prints `veo3_1_lite 16:9 8s`. Vertical face-forward hooks are **higher morph risk** (more frame height on faces, tighter crop grammar). The plan treats palette transfer as settled; the codebase has **zero 9:16 veo palette tests**.

**Lines 57–60 (Option B)** — “**paced faster** (quicker moves, **tighter cuts**)” — conflicts with settled engine knowledge. `animate-long/SKILL.md` and `CLAUDE.md` both record: **veo cannot execute crop-cut / gallery-tour discipline**; it **animates subjects** and ignores cut plans. “Tighter cuts” on veo means **editorial hard cuts between separate 4/6/8s clips**, not in-clip punch — extra scenes, extra spend, seam risk.

**Line 65 (Option C)** — “**hook (first 3s)**” — veo’s legal durations are **4/6/8s** (`pipeline/video_render.py` `_HF_DURATIONS`). A 3s hook window **cannot** be filled by one veo clip without trim/speed — which reintroduces the “speed-to-fit” tension `witness-cut` guardrails warn about for SHORT.

**Internal palette inconsistency:** **Line 28** lists GREEN “**tracking-drone (landscapes only)**”, but `longform/_build_scene_plan_two_goats.py` puts `tracking_drone_view` in GREEN globally with no landscape guard. If you copy the long plan verbatim, you may import a **known-bad move class** into face-heavy vertical scenes.

---

### 3. Hidden risks & single points of failure

**Option C hybrid (lines 63–67)** assumes a **mixed assembly mode** that **does not exist** in the eyewitness pipeline today:
- `witness-cut/SKILL.md`: SHORT = “slideshow / boomerang stills… **Reuse the shorts assembler**”; LONG = “`_assemble_16x9.py`” veo path.
- `v2/LONGFORM_SPEC.md` explicitly warns **not** to use `cli_assemble.py` for long-form — the viral 60s jigsaw assembler is a **different animal** (LLM edit plan, AS-G gates, Kling clips).
- There is ad-hoc precedent (`longform/06_Day_Of_Atonement/_build_pilot.py`: ffmpeg still slideshow), but **no spec’d 9:16 mixed veo+boomerang assembler**, no QC gates for hybrid seams, no idempotent re-run story.

**Christ landing NSFW:** Long-form has a **hybrid veo→Kling fallback** for bare-torso crosses (`animate-long/SKILL.md`, `HFVideoProvider`). Option C’s “**Christ landing**” veo spend has **no short-form fallback path** documented in `/witness-cut` or `/witness-world`. One NSFW block on the hero frame = **blocked pilot** or ad-hoc Kling (reopening the morph risk you rejected in **lines 38–39**).

**HF concurrency cap:** `STATE.md` documents **4 concurrent veo jobs** failing batches. Option B/C batch animation for even 6–8 scenes needs **serialization/idempotent refill** — not mentioned.

**16:9 still reuse:** `witness-world` requires aspect-honest reuse (`9:16 short / 16:9 long`). Long-form validated stills are **16:9**. Shorts need a **separate 9:16 world manifest** — “visually consistent with the long” (**line 60, 67**) is **look consistency**, not asset reuse; cost is understated.

---

### 4. Reuse — the plan ignores a $0 motion tier you already built

The options matrix is **A boomerang / B full veo / C hybrid veo** only.

`_assemble_16x9.py` already layers **ffmpeg Ken Burns** (7% push/pull) **on top of** veo+boomerang for long-form (“so even quiet scenes carry continuous motion”). That is **$0**, anti-slop-friendly, and avoids veo morph — but **not listed** as Option D or as the middle-beat fill for C.

Similarly, the legacy **HF Kling pro + curated anchors + `clip_anim_qc`** path (`animate/SKILL.md`) is the repo’s **locked shorts animation stack** — explicitly **not veo**. The plan dismisses Kling via **lines 38–39** (“morphed/danced”) without acknowledging **2026-06-18 re-bake-off** and `_curate_anchors` / filmstrip QC that exist precisely to mitigate that. You may be rejecting a **maintained** path in favor of an **unproven 9:16 veo** path.

---

### 5. Over-engineering / premature spend

**Lines 69–73** — recommend **C for the pilot, measured against A on a real A/B** — that is **three production tracks** (A baseline, C hybrid, and implied B if C wins) **before** a minimal proof:
1. **Two** 9:16 veo clips on EW01 hook still + Christ still (palette + NSFW + glitter-kill).
2. **One** ffmpeg Ken Burns middle beat at punchy pacing.
3. Ear-check against **punchy** audio, not calm.

`EYEWITNESS_SPEC.md` §11 budgets SHORT at **~$2** with **$0 animation**. Option B is silent on cost; long-form veo is **~$8–11 for ~24 scenes**. Even 8 short scenes at ~$0.40–1.50/clip blows the short cost model **4×+** with no retention hypothesis tested.

The plan asks panel opinion (**lines 75–80**) but **does not define A/B metrics** (3s hold, avg view duration, swipe-away, comment rate) or **control variables** (same punchy script, same thumbnail, same caption policy).

---

### 6. Missing steps, edge cases, verification gaps

| Gap | Why it matters |
|-----|----------------|
| **9:16 veo POC gate** | Required before Options B/C; absent from plan |
| **Scene count / beat map for punchy 4-beat short** | No still budget (6–10?); hook/turn/punch windows undefined |
| **Mixed assembler spec + LF-CLIP-style QC for shorts** | Hybrid C has no engineering home |
| **Caption/motion-on-still** (question 4, line 81) | `/caption` is offline WhisperX ivory — not motion design; plan asks but doesn’t decide |
| **First-frame thumbnail** (line 81) | Unaddressed; hook veo clip may be wrong for static thumbnail |
| **Spec/skill updates** | If C wins, `EYEWITNESS_SPEC.md`, `witness-cut`, cost model §11 all need revision — not listed |
| **Policy conflict with CLAUDE.md** | “**veo is long-form only**; Kling permanent for shorts” — eyewitness veo shorts need an **explicit exception** or the plan fights locked decisions |

**Line 32** — “face-forward Christ renders reverent on the **cheaper image model**” — true for **stills** (`witness-world`: NBP for Christ/face). Option B/C adds **veo motion on those faces** — a harder problem than still rendering; conflated in the plan.

---

### 7. Cost / spend justification

- **Option A:** aligns with §11 (~$2/short, $0 motion) — justified as baseline.
- **Option C:** “cheapest premium” (**line 66**) is plausible **only if** 2× veo ≈ **$1–3** and assembly is ffmpeg — but plan gives **no quote**, no test-gate (`animate-long` requires **2-clip approval before batch**), and ignores Ken Burns as cheaper “premium enough.”
- **Option B:** full veo short = **long-form animation economics on a product spec’d at $2** — not justified without retention data; highest over-build risk.

---

### 8. What the plan gets right (limited credit)

- Correctly identifies **painterly oil** as the anti-slop moat (**lines 31–32**).
- Correctly records **translate/zoom vs rotate POV** as the faithfulness axis (**lines 23–25**) — matches `_build_scene_plan_two_goats.py` GREEN/RED split.
- Honest uncertainty (**lines 72–73**) about beating genuinely punchy fast-cut retention — but undercuts itself by not updating for **already-punchy scripts**.

---

### Bottom line

The plan is a **pre-punchy-revision document** asking the right meta-question but recommending **paid hybrid veo** while **(a)** the script/audio already went punchy, **(b)** 9:16 veo faithfulness is unproven, **(c)** the hybrid assembler doesn’t exist, and **(d)** a **$0 Ken Burns** tier already shipped on long-form is omitted from the decision matrix. Do not meter Option C on EW01 until a **2-clip 9:16 POC + Ken Burns middle + punchy audio ear-check** completes.

VERDICT: REVISE
TOP FIXES:
1. Rebase the plan on current punchy shorts (~60–75s, 120–210w, racing middle) and drop Option C’s “calm middle beats” — or explicitly revert the punchy structure decision.
2. Add a mandatory **9:16 veo POC** (hook still + Christ landing, GREEN moves only, NSFW fallback, glitter-kill) before any hybrid/full veo recommendation; update `EYEWITNESS_SPEC.md` / cost §11 if veo shorts are in scope.
3. Expand the options matrix with **$0 ffmpeg Ken Burns / punchy slideshow** (reuse `_assemble_16x9.py` patterns) and name the **actual assembly owner** for mixed veo+boomerang — don’t assume `/witness-cut` supports hybrid today.
