# Independent review — cursor (OK, 90s)

Independent adversarial review of **Swirls of Life v2**. Claims checked against `_website/manifest.yaml`, `data/series.json`, `batches/batch_manifest.json`, `pipeline/handoff.py`, `pipeline/visual_runner.py`, `.claude/skills/swirls-of-life/`, and `poc_living_water_ink_style_test/`.

---

## Critical findings

### 1. The catalog-collision claim is not credible — and at least one pick violates the plan’s own premise

The opening block states every passage was checked against the full catalog and **“confirmed clear”**, with detail **“not repeated here”** (line 5). That is the entire justification for v2 existing. A plan whose reason-for-being is collision avoidance cannot treat the audit as optional appendix material.

I found a direct hit:

- **#16 “The Name She Knew”** (`John 19:38-42 + John 20:11-18`) overlaps **`the-empty-tomb`** in `_website/manifest.yaml` — `ref: John 20:8`, `public_status: studio_complete`, sourced from `batches/cluster_02_resurrection/empty_tomb_john208`. Hook: *“Someone took the body. That was Mary's first thought at the empty tomb.”*

That contradicts the user mandate quoted in line 5: *“drop every story already made anywhere in this catalog, in any style.”* The finale’s Mary-at-the-tomb beat is not “clear.”

### 2. Internal arithmetic is wrong in three places

- **“The slate — 15 episodes”** (line 23) vs numbered rows **#1–#16** = **16 episodes** (14 shorts + 2 longs).
- Opening line: **“17 candidate passages”** checked — only **16** appear in the slate. The 17th is never named.
- **“Ratio: 14 shorts : 2 longs”** is correct; the **“15 episodes”** header is not.

Sloppy counting on a collision-sensitive rebuild undermines trust in the audit itself.

### 3. Factual error undermines the season-arc logic

**#3 “The Ladder He Saw”** says Jacob’s dream *“Pays off one chapter later, in Jesus's own mouth (see #8, Nathanael).”*

Genesis 28 does not pay off one chapter later. The payoff is cross-episode (#3 OT → #8 NT). That wording looks like copy-paste drift and suggests the pairing wasn’t reviewed carefully.

---

## Feasibility vs real codebase / tools

### 4. “No production pipeline” is admitted — then ignored in cost, build order, and season scope

Open risks table (line ~84): *“No production pipeline for this format… full deterministic gates deferred.”*  
`PRODUCTION_PIPELINE.md` is explicit: assembly **“remains `northstar_shortform/`'s hand-built assemble script, forked per episode”** until enough episodes ship.

The plan budgets **$450–920** for the full slate and sequences 16 builds anyway. There is no step for:
- per-episode `assemble.py` fork,
- long-form (16:9, 7 movements) swirls assembly path at all,
- motif/stage linting (deferred in skill docs).

**Long-form #15 and #16** assume *“7 movements, 16:9”* with **“zero ledger evidence for this format's own long-form yet”** (cost section). That is planning spend on an unproven shape.

### 5. First-build step contradicts the locked skill workflow

Build order step 1: **“first build spends nothing beyond one still”** and calls Melchizedek/Talitha **“simple, single-scene, low-risk.”**

Against the real toolchain:

- `SKILL.md` Step 0: design **the whole shot list** (still + animation + fill plan) **before rendering anything**.
- John 4 northstar POC shipped as **8 shots** (`northstar_shortform/assemble.py` `SHOT_STEMS` = 8 clips + narration + score + 3.0s hold).
- **Talitha Cumi** is **not** single-scene: `Mark 5:21-24, 35-43` is a **sandwich/interleaved** pericope.
- **Melchizedek** is **three verses** (`Genesis 14:18-20`). A 60s gospel-five-beat short requires substantial invented staging — tension with the design brief on line 13: *“never assuming anything not brought from thin air.”*

“One still” is not a valid proof gate for this format.

### 6. Multi-ref episodes will break if the main narration pipeline is used — v2 never mentions this

v1 independent review flagged `pipeline/handoff.py` writing only `primary_ref` and `visual_runner._episode_from_creation()` rebuilding `refs` as `[primary_ref]`. **Still true:**

```121:121:pipeline/handoff.py
        "episode": {"title": episode.title, "primary_ref": episode.primary_ref},
```

```90:97:pipeline/visual_runner.py
def _episode_from_creation(d: dict) -> Episode:
    ...
        refs=[str(d.get("primary_ref", "")).strip()] if d.get("primary_ref") else [],
```

Affected slate entries v2 never addresses:

- **#6 Talitha Cumi** (two Mark chunks),
- **#15 Luke 4:16-30** (wide pericope),
- **#16** (two John passages).

If narration goes through `cli.py` → `handoff.py`, supporting refs silently drop. v2 dropped v1’s risk table entry entirely.

### 7. Swirls does not plug into `cli_visual.py` / `cli_assemble.py`

`PRODUCTION_PIPELINE.md`: *“A swirls page… is not a `cli_visual.py` scene.”* The plan never states which path produces finished MP4s. Reusing the Baroque/Kling gallery-tour assembly stage would be a category error. Budget and timeline assume a pipeline that is explicitly **not** the main engine.

---

## Dead-ink / doctrinal / motif risks

### 8. Motif assignments stretch or violate the plan’s own taxonomy

Dead-ink rules (lines 17–21) define **Stain** as two sub-cases only (moral sin/guilt vs ceremonial/Levitical uncleanness) and **Fray** as fear/**doubt** (James 1:6, Matthew 14:31).

Several picks don’t fit cleanly:

| Episode | Claim | Problem |
|---|---|---|
| **#9 Martha** | Fray | Text is anxiety/busyness, not doubt. Fray proof texts are doubt-specific. |
| **#10 Woman at the Border** | Stain (uncleanness — **Gentile outsider status**) | Third stain category not in the rules. Risk of framing ethnic status as Levitical uncleanness. |
| **#13 Peter’s feet** | Stain (**shame at being served**) | Shame ≠ sin/guilt ≠ ceremonial uncleanness. Taxonomy gap. |
| **#5 Widow’s barrel** | Fray | “Fear of death” ≠ Matthew 14:31 doubt. Motif forced onto obedience/faith story. |
| **#2 Numbers 19** | Stain + OT swirl cap 1–2 | Whole chapter is ritual law with no named “one real person” — conflicts with line 9 (*“motif IS the diagnosis”*) and line 21 (Stage 3 reserved for on-page Christ fulfilment; Hebrews 9 link is off-page). |

**#14 Simon of Cyrene** is honestly marked motif-light — but then line 9’s series promise (*“Every episode's dead-ink motif… hands you that episode's own 'one real person'”*) doesn’t hold for 4+ episodes (3 swirl-only OT, Simon, both long-forms partially).

### 9. Finale mechanism is doctrinally cleaner but catalog-colliding and unreviewed

Risk table acknowledges the finale device is **“new, unproven”** and **“hasn't been panel-reviewed yet.”** Fair. But it doesn’t acknowledge the **John 20 collision** with a shipped resurrection short — a bigger problem than motif novelty.

---

## Hidden risks / single points of failure

### 10. Dropping all validated POC stories removes the only proof of motif grammar on real pages

Line 5: drops Well, Hem, Thomas, Storm test — *“nothing carried over.”*  
Risk table admits **“Zero rendered pixels for any episode in this slate.”**

The **template** (`NORTH_STAR_ANIMATION_PROMPT.md`, `swirls_page.py`) is proven; **Stain/Fray/swirl dosing on new subjects** is not. Re-proving should be an explicit gate (e.g., one Stain + one Fray + one swirl-only before season commit). Build order doesn’t require that.

### 11. **#7 “Wherefore Didst Thou Doubt”** is the same miracle event as an existing series entry

Not shipped in manifest, but `data/series.json` / `batch_manifest.json` already has **“Walking on water”** (`Mark 6:50`, miracles-signs, **planned**). v2’s freshness bar (line 13) and collision bar (line 5) are different tests; this passes one and fails the other. Plan doesn’t reconcile them.

### 12. **#1 Melchizedek** duplicates a planned long-form anchor elsewhere

`batches/batch_manifest.json`: `{ "title": "Melchizedek", "series": "types-shadows", "status": "planned" }`.  
`longform/LONGFORM_TYPES_SHADOWS_SLATE.md`: Melchizedek is **#5** in the Types & Shadows set (Gen 14 + Psalm 110 → Heb 7).

Not “already produced,” but strategic duplication the plan doesn’t flag.

### 13. **#14 Simon / cross carry** — no NSFW animation fallback called out

Cross-cluster work already treats Simon-of-Cyrene road scenes as a checkable visual fact. Swirls uses HF `kling3_0` / `veo3_1_lite` (`swirls_page.py`). Project history: HF refuses some bare-torso cross stills; direct-Kling is the fallback elsewhere. Plan is silent; Simon is a likely spend trap.

### 14. Luke 4 crossing-arc dependency is soft in build order

**#15** explicitly names **Naaman (#4)** and **widow of Zarephath (#5)** in Jesus’s sermon. Build order step 4 only says *“once several shorts have proven the grammar”* — not **after #4 and #5 ship**. Season payoff can be built before its proof-text shorts exist.

---

## Over-engineering / premature building

### 15. Season-scale commitment before format proof on new content

16 episodes, 2 long-forms, **$450–920**, governance still **“In progress”** (line ~89), no `series.json` draft (v1 had a JSON block; v2 has none). This is a full season plan before a single new-slate pixel exists — opposite of the project’s own `PRODUCTION_PIPELINE.md` guidance: formalize scripts now, **gates after 4–5 clean episodes**.

Reasonable: parameterized `swirls_page.py`.  
Premature: full slate lock + long-form finale + crossing-arc long before one new short ships clean.

---

## Reuse gaps

### 16. Doesn’t wire existing assets the codebase already has

- **`swirls_page.py`** exists (`poc_living_water_ink_style_test/test_the_cross/`) — plan cites it in risks but build order doesn’t say “all new renders go through `PageSpec` + `swirls_page.py`.”
- **`northstar_shortform/`** is the only validated 60s assembly path — not referenced in build order or cost.
- **`cli.py` narration tournament** (~$5–6/ep in cost model) — no note that swirls may need **fresh** narration for dialogue-native pages (v1 decided this explicitly for remakes; v2 is silent for all-new stories).
- **`independent_review.py --type plan`** — correctly listed; **Fable creative-critique** mentioned but not scoped.

---

## Cost / spend

### 17. Cost band is inherited, not earned

- Shorts **$20–46/ep art/audio** + **$5–6 narration** — “until 3–4 episodes ship clean.”
- **Zero ledger evidence** for swirls long-form; still budgets **$50–95/ep × 2**.
- Full season **$450–920** before any regen overrun — with admitted zero pixels and per-episode assembly forks unbudgeted.
- **`/cost` sign-off before each build** (good) is undercut by committing to 16 episodes in the plan document itself.

John 4 northstar `_REPORT.html` path suggests real shorts land higher than the low end once regens, multi-voice, and fill devices are included.

---

## Missing verification steps

The plan should require, before `series.json` touch:

1. **Attach the collision matrix** (passage × manifest × narration folder × longform × poc_*), not “on request.”
2. **Replace or re-scope #16** (and re-check any John 20 / Mary Magdalene adjacent pieces).
3. **Fix multi-ref handoff** or document manual `creation.json` threading for #6, #15, #16.
4. **Define first proof episode** with explicit exit criteria (N shots, one Stain, one Fray, one assembly fork, landing-hold green).
5. **Motif assignment review** for #2, #5, #9, #10, #13, #14 against the two-sub-case Stain rule.
6. **Long-form feasibility spike** (one 16:9 movement end-to-end) before locking two long-forms.

---

VERDICT: REVISE  
TOP FIXES:  
1. Publish the full collision audit inline and remove/replace **#16 “The Name She Knew”** — it overlaps shipped **`the-empty-tomb` (John 20:8, studio_complete)** and breaks the plan’s core “nothing already made” mandate.  
2. Reconcile episode counts (**15 vs 16 vs 17**), fix the **Genesis 28 “one chapter later”** error, and add explicit pipeline steps: **`swirls_page.py` → per-episode `northstar_shortform` fork → multi-ref handoff fix** (or manual override) before any `cli.py` narration on #6/#15/#16.  
3. Replace **“one still” first build** with a bounded proof gate (one full short: Step-0 shot list + 8-ish pages + assembly + one Stain + one Fray validated on **new** content) before locking the **$450–920** 16-episode season or the two unproven long-forms.
