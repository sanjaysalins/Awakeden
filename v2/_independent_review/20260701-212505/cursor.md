# Independent review — cursor (OK, 91s)

## Independent adversarial review — `MOTIONCOMIC_SPEC.md`

### 1. Contract conflicts the spec does not resolve (single points of failure)

**INV-13 is refined in prose but not in the binding invariant table.**

§3 MC-R2 says inked art → Kling and “**This overrides INV-13**.” But `v2/SPEC.md` §5 invariant **13** still reads: “shorts = direct-Kling; **long-form = veo3_1_lite/hybrid**.” `v2/LONGFORM_SPEC.md` **LF-INV-3** repeats veo-only for long-form. The spec never adds an `LF-INV-*` or conditional INV-13 row for `style: graphic_novel`. MC-G9 even names “**veo/Kling**” for hero budget — three different models in one gate name.

**The landscape POC you plan to promote still runs on veo, not Kling.**

`landscape_engine.py` lines 6–11 badge heroes as **`[VEO]`**. `landscape_motion_page.py` line 5: “**ONE real veo animation**.” `_hero_veo.py` animates via **`veo3_1_lite`**. MC-R2 says veo morphs ink; the promoted codebase contradicts MC-R2. “Refines INV-13” is asserted, not demonstrated for 16:9.

---

### 2. Feasibility — things the spec claims exist but do not (or are stale)

| Claim | Reality |
|---|---|
| §6: `_hf_animate_short.hf_animate` “**hardcoded 9:16 at line ~102**” | **Already parameterized** — `aspect_ratio: str = "9:16"` at line 99. Spec is stale. |
| §4 MC-G2: “**distinct-clip-per-panel**” | `check_comic_spec()` only checks **template variety** (`render_lint/verify.py` ~111–139). No slug-per-cell enforcement. |
| §4 MC-G8: “**≥1 dwarfing-scale wide**” folded into MC-G1 | `check_scene_subjects()` has **no epic-wide check** (~153–198). MC-G8 is vapor. |
| §4 MC-G3: `check_wound_continuity` | **Does not exist** anywhere in repo. |
| §4 MC-G5/G6: `check_captions`, `check_audio_mix` | **Do not exist.** |
| §4 MC-G9: “**wired**” via `landscape_validate.py` + `clip_reuse.py` | `LANDSCAPE_VALIDATION.md` line 3: “**validators NOT built yet**.” LV-B1 (≤1 hero/page) is **advisory warn-only**, not in `validate()` (~207–215). `clip_reuse.py` has **no** native-9:16 rail logic. |
| §2 stage **2d `/comic`** | No skill, no `pipeline/` module — only batch scripts (`build_mocomic_v2.py`, imports via `importlib`). |
| §2 **2b `/stills`** → BytePlus MC-R1 | `/stills` skill still points at `pipeline/visual_render.py` (NBP/HF). BytePlus lives in **`batches/.../byteplus_seedream.py`** — episode-local, not production. |
| §8 `cli_motioncomic.py` | **Not built.** `cli_pipeline.py` + `pipeline/orchestrator.py` already own gates/state — second orchestrator duplicates INV-15 “wrap, don’t fork.” |

---

### 3. Gate design gaps (honor-system dressed as fail-closed)

**Header:** “Every non-negotiable is backed by a gate.” **Registry:** most MC-G* rows say “**wire into** …” — i.e. **not wired**.

- **MC-G4** “never gibberish script” is **advisory** while MC-R9/INV-17 are non-negotiable — advisory cannot enforce.
- **MC-G7** 3-lens review is **manual** — same class of gap SPEC.md §4 flags as “Phase-1 targets.”
- **Existing CLIP-* gates conflict with MC-R2:** `pipeline/validators.py` **CLIP-VIRAL** requires **≥6 crop-cuts**, not slow push-in. Pilot `animate_v2.py` uses **INK_BASE push-in only** — no gallery tour. Spec §4 says “CLIP-* still apply unchanged” — they would **fail the ink path** unless a motion-comic exception is specified (it isn’t).
- **`/animate` skill** mandates curated-anchor **gallery** as default; MC-R2 mandates **push-in/hold only** — skill and spec fight; no `/animate-mocomic` skill.
- **Bible-Check (INV-25)** is in §2 pipeline; Cluster 1 pilot has **no `_bible_check/`** directory. Spec treats Bible-Check as standard while the “LOCKED” proof skipped it (grandfather vs going-forward ambiguity unstated).
- **IMG-COHERENT / still-review (INV-23)** absent from MC spec — MC-G3 extends IMG-* but drops the coherence + human sign-off chain the `/stills` skill treats as binding.

---

### 4. Architecture — reuse vs duplication

**Real reuse (good):** `render_lint/verify.py` (`check_scene_subjects`, `check_comic_spec`), `asset_index.py`, pilot-proven `INK_BASE` in `animate_v2.py`, `music_library`/`sound_library` pattern in `add_music_sfx.py`.

**Duplication / fork risk:**

- **`cli_motioncomic.py`** parallel to `cli_pipeline.py` instead of `style: graphic_novel` on existing orchestrator.
- **`comic_engine.py` vs `landscape_engine.py`** under `longform/_style_poc/ew04/_mocomic/` — §6 admits “**two copies unified**” but lists unification as a prerequisite, while §8 build order puts orchestrator **before** long pilot (step 4 vs 6).
- **`kinetic_caption.py`** duplicated: batch-local (`father_forgive_them/kinetic_caption.py`, hardcoded `PAGE_W=1080`) vs engine — not unified.
- **MC-R8 `asset_index.json`** vs **`clip_library/` + `clip_reuse.py`** (SPEC §6 reuse manifest) — two asset banks, no join spec. Long reuse depends on shorts clips indexed one way; clip_library another.
- **Short path drops `/assemble`** (§2) but §4 still lists **AS-G1..G9** “unchanged” — jigsaw/hero-bookend assembly doesn’t apply to comic-engine cuts; spec never says which AS gates are N/A or what replaces AS-G6/G7 gospel-pivot checks for comic layout.

---

### 5. Hidden risks & edge cases

**MC-R7 native 9:16 reuse:** Requires **pre-LOCKED shorts clips** for the same cluster/topic. Spec never states **long-after-short** ordering or what happens when reuse cells fail `clip_reuse` coherence/QC — long becomes all paid heroes, blowing §7 cost.

**LV-G1 vs MC-R7 “free pages”:** Landscape validation requires **≥1 animated cell per page** (veo, reuse clip, or Ken-Burns). A “free” page of static PNGs **fails LV-G1** unless every free page has KB motion — contradicts “ken-burns stills ($0)” if z=1.0 frozen stills are used.

**MC-R9 scroll exception:** “period Hebrew acceptable IF camera pushes to non-text subject” — animating text-bearing scrolls is exactly what INV-17 forbids; partial exception invites garbled glyphs on generative paths.

**MC-R4 kinetic captions:** Word-cascade + red keyword on crucifixion beats (“Nails through his hands”) risks **TikTok irreverence** vs static Scripture bars — brand tension on sacred content; no gate blocks kinetic treatment on prayer/Scripture windows (only type split caption vs redletter).

**MC-R6 ffmpeg zoom-snap:** “Active beats only” — no deterministic beat classifier; misapplied snap on a sacred beat is a doctrinal/brand fail with no gate.

**Human Gate 3:** §2 places it after **§3 AUDIO** (post-comic + score). Existing orchestrator Gate 3 is **pre-assembly clip QC**. Motion-comic merges comic + audio before review — excluding a bad clip may require **rebuilding the whole comic segment**, not cheap jigsaw replanning. Not addressed.

**§4 Stage 4 `/caption`:** “kinetic captions **BUILT-IN at 2d**; `/caption` only for fallback” — conflicts with **INV-16** (“caption is the final step on every finished clip”) and `/caption` skill unless “built-in” counts as caption — undefined.

---

### 6. Cost model — optimistic and incomplete

**Short ~$9–10:** Pilot math (~13 × $0.04 + ~13 × $0.65) ignores Vision audits, test-gate clip, rerolls, and **MC-G3 wound-continuity re-shoots**. Reasonable as floor, not budget ceiling.

**Long ~$8–10:** Omits **~$1.50 multi-voice audio** (`LONGFORM_SPEC.md` §7), **LF test-gate** (LF-INV-7), and failure mode where reuse is unavailable. Compares to “veo3 Baroque long” but MC-R7 savings assume **shorts already paid for**.

**“Opus/agent LLM $0 (in-chat)”** — true only in agent mode; production CLI runs revert to SPEC §7 ~$5–6 planning unless explicitly scoped.

**No `/cost` integration** for BytePlus (~$0.04/still) — spec cites `hf generate cost` only; BytePlus is the still provider (MC-R1).

---

### 7. Over-engineering before proof

§8 build order: parameterize → **`pipeline/motioncomic/` modules** → promote landscape → **orchestrator** → wire gates → **then** pilot cross-cluster long.

That builds infrastructure **before** one end-to-end 16:9 Kling-hero + native-reuse episode is LOCKED. The only LOCKED proof is a **9:16 short** with batch-local scripts. Promoting `landscape_engine.py` to production while it still says **VEO** and lives under `_style_poc/` is premature naming.

§9 A/B + `/learn` loop before MC-G5/G6/G3 exist means defects have nowhere deterministic to land — more process than teeth.

---

### 8. Doctrinal / brand risk (format-specific)

- **Graphic novel + kinetic TikTok captions** on the cross: format reads younger/faster than Baroque-oil + ivory captions; static red-letter bars help but plain-line kinetic treatment on “Father, forgive them” window needs explicit sacred-beat rules (none in MC-G5).
- **MC-R1** “God/the Father never depicted” is in `render_lint` `_ALWAYS` checks but MC-G3 routes through IMG-* — not guaranteed for BytePlus path without bible-check fact cards (pilot skipped).
- **Healed-scar risen body** (MC-R1): positive end-state wording is smart for BytePlus no-negative-channel, but **cross-episode continuity** via Vision-only `check_wound_continuity` is fragile — easy false pass/fail without reference stills in the audit prompt.

---

### Summary judgment

The spec accurately captures **what the Cluster 1 pilot learned** (BytePlus ref-lock, INK_BASE Kling push-in, template variety, score dynamics) and correctly identifies **`render_lint/verify.py`** as partial gate infrastructure. It **overstates production readiness**: landscape long-form is still a **veo POC**, most MC-G* gates are **unbuilt/unwired**, CLIP-VIRAL **conflicts** with MC-R2, INV-13/LF-INV-3 **are not actually amended**, and §8 proposes **duplicate orchestration** before the long-format recipe is proven on Kling.

---

VERDICT: REVISE

TOP FIXES:
1. **Resolve the three-way animation contract** — amend INV-13 / add `LF-INV-*` for `style: graphic_novel`, rewrite `landscape_engine`/`_hero_veo` from VEO→Kling (or cite a 16:9 ink bake-off), and define which CLIP-* gates are waived for INK_BASE push-in.
2. **Downgrade gate registry to honest status** — mark MC-G3/G5/G6/G8/G9 as TARGET; implement or remove false claims (“distinct-clip-per-panel,” “wired,” MC-G8 epic-wide); make MC-G4 fail-closed or drop “binding.”
3. **Prove before orchestrating** — one LOCKED 16:9 cross-cluster long via existing POC scripts + Kling heroes + native reuse *before* `cli_motioncomic.py` / `pipeline/motioncomic/`; extend `cli_pipeline.py` with `style` rather than fork; unify `kinetic_caption` + engines and state which AS/assembly gates apply to comic shorts.
