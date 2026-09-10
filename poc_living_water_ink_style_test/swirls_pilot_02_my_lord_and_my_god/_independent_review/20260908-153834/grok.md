# Independent review — grok (OK, 104s)

I'll read the full offloaded artifact and the related brief so I can judge the plan against the real project, not the truncated paste.Found the real files under the Swirls pilot. Next I'll read the run sheet, brief, and assembly plan against the existing pipeline constraints.Digging into contradictions between the run sheet and brief, plus prior Flow delivery failures.## Independent review — `FLOW_RUN_SHEET.md`

This is an execution plan for an unattended 18-generation Google Flow run. It is **not safe to hand to Flow as written**. Several claims are false against the companion brief and against this folder’s own history.

---

### 1. False consistency claim vs companion brief (blocking)

The sheet says: *“Nothing in this file contradicts that one — this file is the same content… If anything looks inconsistent… this one wins.”*

That is false on the load-bearing path:

| Claim | `FLOW_RUN_SHEET.md` | `GOOGLE_FLOW_BRIEF.md` |
|---|---|---|
| Reference Ingredients | R1/R2: **“Ingredients: none… made from the text alone”** | Step 1a/1b: attach **`thomas_ref_hd_face.png` + `thomas_ref_hd_full.png`** and **`jesus_ref_upscaled3x.png`** (already in this folder) |
| Human approval | **“without pausing for approval… Never stop the run”** | **“Do not start any story shot until both are approved”** |
| Clip length | hard **“8 seconds”** | **“8–10s”**, with assembly targets up to ~12.8s |

The brief’s own rationale for regenerating refs *through* Flow was to fix low-res likeness **using the existing HD files as Ingredients**. The run sheet drops that and regenerates from text alone, then declares itself the winner. That reintroduces the exact failure mode the brief says it fixed.

Those HD refs already exist here:
`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_02_my_lord_and_my_god\thomas_ref_hd_face.png` (and siblings).

---

### 2. Unattended “never stop” after known failures on this episode (single point of failure)

Section 0 / rule 5: *“I am not watching between steps… If it fails again, keep the better of the two… Never stop the run.”*

This folder already has **`_flow_delivery_v3` / `v4` / `v5`**, plus assembly experiments. The sheet itself admits prior defects on this exact episode (“door movement,” “blank/missing caption,” “entire batch” with no motion).

Pairing that history with:

- **1 unchanged retry only**
- **no prompt edit allowed**
- **keep a still that still fails checks, then animate it anyway**

guarantees cascade waste: a bad `STILL_0N` becomes a paid `CLIP_0N`. That is the opposite of this project’s GATE-2 pattern (exclude bad stills before paying for animation).

The generator cannot be its own adversarial QC. Project standing rule: verify by looking, and independent review — not self-score-and-continue.

---

### 3. Feasibility assumptions Flow / the agent likely cannot keep

- **“You send me exactly two messages”** — unrealistic for a tool that emits generation UI / progress / assets as it goes.
- **“Use Flow’s name, title, or note field”** / else track “7th image generated” — prior deliveries show Flow’s own auto filenames (`Man_reaching_out_with_tremor_…`, etc.). The FINAL REPORT’s tidy `01_front_cover.png` names are **operator rename work**, not something Flow will produce.
- **“pixel-identical” / “pixel-for-pixel” title checks** (CLIP_01, CLIP_06, CLIP_08) — an LLM agent watching playback cannot honestly certify pixel identity.
- **Cross-still check** on STILL_03: *“oil lamp… visibly lower/dimmer than in STILL_02”* conflicts with *“Each step stands alone… Carry nothing forward… except the images the step names”* — STILL_02 is not an Ingredient for S3; the agent is expected to remember a prior frame for a comparative QC it may not retain.
- **Split instruction is wrong:** *“split it at any `### Step` boundary”* — there is no heading `### Step`. Headings are `## Step R1` / `## Step S1` and `### S1-A`. Splitting at `### S1-A` can orphan still↔clip pairing.

---

### 4. Timing / assembly mismatch (plan fights its own assembly plan)

`ASSEMBLY_PLAN.md` needs roughly:

- F01 ~**11.4s**, F04 ~**12.8s**, Back Cover ~**11.6s** (+ ≥3.0s landing hold → cut ~**64.3s**)

The run sheet locks **8s** and still calls this a **“60-second episode.”** Forcing 8s on F01 / F04 / Back Cover **recreates the freeze-hold burden** the 6→8 shot split was meant to reduce. The brief already says generate at Flow’s normal 8–10s; the run sheet silently hardens the worse option.

CLIP_08 even says longer duration is handled *outside* Flow — correct for walk cycles — but then generating only 8s for an ~11.6s landing shot is a known pain point the sheet itself warns against fixing with boomerang.

---

### 5. Internal QC contradiction (CLIP_05)

CLIP_05 “Must not fail” says the hand-gap is *“identical in spirit first frame to last: closer than the still, perhaps”* while also requiring Thomas’s hand to be *“visibly closer… in the last frame than the first.”* Those are not the same check. An agent can pass or fail the same clip depending on which sentence it privileges.

---

### 6. Reuse / provider path

Locked Swirls default in this repo is **OpenArt** (stills + Kling via bridge), with HF only on deliberate `SWIRLS_GEN_PROVIDER=hf`. This plan is a full **Google Flow** parallel path after multiple Flow deliveries already landed in-folder. It does not:

- reuse `swirls_cover.py` / OpenArt bridge / existing Vision audits
- explain why another full Flow spend is better than fixing the best of v3–v5 or routing covers/interiors through the locked Swirls stack
- cite a spend estimate or user OK before 18–36 metered gens

That is premature full-batch spend before the unattended-agent idea is proven on a **2–3 shot smoke** (refs + one interior + one cover).

---

### 7. Style / Ingredient risk called out but not controlled

S1 attaches ink-wash `REF_THOMAS` into a **Dürer woodcut** cover *“for likeness only.”* Flow Ingredients do not reliably respect “likeness only, ignore style.” One bad style bleed pollutes the bookend hero. With no human gate after STILL_01, that bleed becomes CLIP_01 and the open of the cut.

---

### 8. Missing verification / handoff steps

Absent from the plan:

- Spend preflight + user OK (`/cost`)
- Human still gate before any clip spend
- Mapping Flow outputs → assembly filenames (operator step, not agent)
- Silent-strip / replace Flow ambient before mux with `narration.mp3` (brief notes assembly may keep or replace; sheet assumes ambient is fine)
- Run `check_landing_hold.py` after cut (ASSEMBLY_PLAN requires it; run sheet stops at FINAL REPORT)
- What to do when refs fail likeness across S2–S7 (sheet forbids regenerating refs after R2)

---

### Bottom line

The prompt hygiene (verbatim blocks, known trap checks, no-boomerang on walk cycle) shows real learning from prior failures. The **operating model** — unattended, never-stop, text-only refs, 8s-only, self-QC — undoes that learning and contradicts the companion brief on the exact fixes that mattered. Do not paste this into Flow until those are fixed.

VERDICT: FAIL
TOP FIXES:
1. Kill unattended never-stop: human approve R1/R2, then each STILL before its CLIP; bad stills are not animated.
2. Resolve the brief contradiction: R1/R2 must attach the existing HD refs (`thomas_ref_hd_*`, `jesus_ref_upscaled3x.png`), not “Ingredients: none.”
3. Align length/cost with `ASSEMBLY_PLAN.md`: allow 8–10s (prefer longer for F01/F04/Back Cover), add spend estimate + user OK, and smoke-test 2–3 shots before another full 18-gen run.
