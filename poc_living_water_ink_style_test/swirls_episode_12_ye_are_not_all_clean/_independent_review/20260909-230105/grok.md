# Independent review — grok (OK, 158s)

I'll review this Flow run sheet adversarially against the real codebase and the pilot pattern it claims to follow.Next I’ll compare this sheet against the pilot run sheet, the design brief, and the assembly plan — and check whether the referenced assets and Flow assumptions actually hold.The design brief’s F04/F06 rules and the ZONE-check wording look inconsistent — checking those next, plus whether the pilot’s “validated” claim holds up against actual Flow deliveries.## Independent review — `FLOW_RUN_SHEET.md` (Episode 12)

This is an execution plan for an unattended ~20-generation Google Flow run. It is **not safe to paste into Flow as written**. Several governing claims contradict the companion brief, the folder’s own NOTES, and the pilot’s real delivery history.

---

### 1. Governing ZONE rule contradicts the designed gospel-turn pages

**Section 0, rule 2** says the motif *“must never appear in the same frame as Judas, at any dose, on any page.”*

**Section 3** then hardens that into a machine rule:

> *“any still or clip where Judas is in frame AND the motif dose is above 0 — that never happens by design… the check is simply ‘does any blue or gold ink appear anywhere in this frame at all’”*

That is false against this sheet’s own Steps **S3/S4** (and `_DESIGN_BRIEF.md` F02/F03): Judas is in frame **and** swirl dose is **1**, with separation defined as *near Judas*, not *same frame*.

If Flow’s agent follows Section 3 literally, F02/F03 correctly showing the basin thread will **CRITICAL-fail**, burn the 3-attempt budget, then either ship a broken “best of three” or keep regenerating until the motif disappears — destroying the gospel-turn visual this episode is built on.

The per-step checklists (“no blue… **near** Judas”) are right. The global rule is wrong. Those two cannot both govern.

---

### 2. False “validated” / “route decided” framing

Opening claim: *“following the exact structural pattern **validated** on… My Lord and My God.”*

Pilot reality in-folder: `_flow_delivery_v3`…`v7`, wrong cover style/composition on v6, extra orphan files, shot fixes (`FLOW_FIX_SHOT6.md`). The pattern was **iterated after failures**, not proven as a clean one-paste unattended run.

Worse: `NOTES.md` still says:

> *“Decide generation route: OpenArt/HF (this series' locked default) or Google Flow… — **not yet decided** for this episode specifically.”*

and lists `episode.py` as **not yet done**.

This sheet jumps straight to “hand this whole file to Flow’s agent, once,” bypassing the locked OpenArt default (`SWIRLS_GEN_PROVIDER`, `openart_bridge.py`) and the missing episode implementation. That is premature spend on an undecided parallel path.

---

### 3. Attachment table vs Step S8 — internal contradiction

Global attach table:

> `| S8 Back Cover | none — no figure appears anywhere on this page |`

Step S8 itself:

> `Inputs: REF: REF_BASIN_TOWEL`  
> prompt: *“matching the attached basin-and-towel reference”*

One of these is wrong. An agent told “each step stands alone” and also given the summary table will attach inconsistently.

---

### 4. Brief contradictions papered over, not resolved cleanly

The sheet flags F04 Jesus vs `_DESIGN_BRIEF.md` §3 — good — but the mess is larger than admitted:

| Source | Claim |
|---|---|
| Brief header / §3 “Where Jesus appears” | Jesus **NOT** on F04 |
| Brief §6 F04 main scene | `{JESUS_BUILD}` handing sop to Judas |
| Brief §3 F04 refs list | `judas + judas_face + supper_room` (**no jesus**) |
| This sheet S5 | Attaches `REF_JESUS` |

John 13:26 needs Jesus in the sop beat, so S5’s *content* is defensible. Calling the brief “locked, all 10 open questions resolved” while still executing against an unresolved §3/§6/refs split is not. The brief must be patched **before** this becomes the winning generation doc.

Same class of issue on F02: brief §2 zone summary says *“Judas absent (F02)”*; §6 and S3 put Judas in the washing page. Pick one geometry and make every section say it.

---

### 5. Feasibility risks the pilot already proved

- **Models unset:** *“whatever this Flow project's image/video model is currently set to”* drops the brief’s per-shot lane (kling / veo / seedream) and the repo’s locked OpenArt cost controls. Spend is unbounded and non-reproducible.
- **Cost ceiling is not a number:** “multiply by up to 45” with no credits/$ estimate. CRITICAL is marked on almost every ref and many stills — worst case is closer to **3× many steps**, not a tidy 20–45.
- **No stills gate before video spend:** rule 5 *“Never stop the run.”* Pilot already animated wrong-style covers. Eight clips after unchecked stills is the expensive failure mode.
- **4 Ingredients on S3/S4** (Jesus + room + Judas + basin) exceeds the pilot’s typical 1–2. Style bleed / identity mix risk is higher, and there is **no** “if attach fails, fall back” path.
- **Jesus ref choice:** pilot deliberately used `jesus_ref_upscaled3x.png` for Ingredient quality; this sheet points at the smaller skill `jesus_ref.png`.
- **S1 CRITICAL “same woodcut as S8”** is unverifiable when S1 runs — S8 does not exist yet. Circular QC.
- **Paste-split vs unattended:** the doc is huge; “split at any `## Step`” breaks the “one message, no re-pasting” promise and invites context/Ingredient loss mid-run.
- **Baked handwrite strings as CRITICAL** (exact `SEQ:…`, panel captions, titles): Flow’s prior deliveries already mangled style/text. Expect retries → “keep best” → animate illegible lettering into CLIP_*.

---

### 6. Reuse / over-engineering

The established Swirls path is: design brief → `episode.py` PageSpecs → OpenArt bridge (locked) → Vision audit → animate. This sheet duplicates that pipeline as a giant prompt for a different vendor, before `episode.py` exists and before the route decision in `NOTES.md` is made. That is parallel infrastructure, not reuse.

Assembly timing reuse from `ASSEMBLY_PLAN.md` is real and good. Generation mechanics are not.

---

### 7. CLIP_08 / landing hold is a soft failure waiting to happen

CLIP_08 asks for ~12.5–13s of **visibly alive** blue-gold drift. Flow’s “longest available” is often still below that; assembly freeze-holds would kill the “not frozen dead” requirement that INV-26 + this design both need. The plan notes the tension but has no concrete generation+assembly recipe that satisfies both.

---

### Bottom line

Creative intent (ordinary Judas, basin-anchored motif, zone separation on F02/F03) is serious. As an **executable Flow plan**, the sheet’s global ZONE wording, undecided OpenArt-vs-Flow route, S8 attach bug, unset models/cost, and “never stop / no stills gate” posture make it unsafe to run.

VERDICT: FAIL
TOP FIXES:
1. Rewrite Section 0 rule 2 + Section 3 ZONE check to match F02/F03 reality: ban motif **near Judas / on Judas**, not “anywhere in the same frame”; delete the false “Judas + dose>0 never happens.”
2. Do not paste into Flow until `NOTES.md` route decision is explicit (OpenArt locked default vs Flow exception), with a real credit/$ ceiling and pinned still+video models — and add a human stills gate before Phase 3 clip spend.
3. Fix internal contradictions before execution: S8 Ingredients vs attach table; patch `_DESIGN_BRIEF.md` §3/§6/F04 refs so Jesus-on-F04 and Judas-on-F02 are one consistent locked story; replace circular S1↔S8 woodcut CRITICAL with a concrete style checklist verifiable at generation time.
