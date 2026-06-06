# Independent review — claude (OK, 186s)

I verified the plan's load-bearing claims against the codebase. The catalog math is honest; the *plan* around it has real holes. Findings below, each tied to an exact line.

---

## What checks out (credit where due)
- **"10 series / 76 episodes"** — verified. Episode counts per series sum to exactly 76. ✓
- **"21 longs"** — the 🎬 entries sum to 21. ✓
- **"Psalm 22 long ... mp3 already done"** — `longform\02_Psalm_22_Song_From_The_Cross\v1\narration.mp3` exists. ✓
- **"Isaiah 53 ... READY TO POST"** — `longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9\Isaiah53_16x9_captioned.mp4` exists. ✓

---

## Findings

**1. The anchor-long funnel is internally contradictory (worst problem).**
Strategy: *"long-forms = the deep, researched meal... shorts are distilled cuts."* But the **series-anchor** (1/series) is then assigned to "back" up to **8 topically-distinct shorts**. Example: *"Names and Titles ... (series deep-dive)"* is the listed backer for Logos, Lamb of God, Son of Man, Alpha & Omega, Immanuel, etc. One 6-8 min deep-dive cannot be the "research foundation" that 8 different-topic shorts are "distilled from." For the ~50 shorts whose only backer is an anchor, *"backed by: ...(series deep-dive)"* is a nominal label, not the funnel the strategy promises. Either admit the anchor is a catalog placeholder, or commit flagships to the rich texts.

**2. The long-first rule creates a 21-long bottleneck the plan never schedules.**
*"Shorts awaiting their long ... 73."* Go-forward rule = long before short. So **73 of 76 shorts are blocked behind 21 longs**. The priority list builds ONE long (Psalm 22) and stops — **19 longs and ~67 shorts have no sequence, no cadence, no per-week throughput**. At any realistic long build-rate that's many months before the short catalog can flow, and the plan doesn't confront it.

**3. State is accurate but artifact paths are missing — the catalog isn't operable.**
The *"_cut_"* shorts have **zero artifacts in the narration tree**. The real cuts live in `C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\adhoc\<topic>\` (verified: `...\adhoc\psalms22-part2\scene_*.viral.mp4`, `...\adhoc\the-suffering-servant\...`). The catalog records a status word but **no absolute path** to any deliverable — you can't open what's marked done. This violates the standing "always show full paths" rule and makes the doc non-operational.

**4. "~$1940 to take everything to a cut" is opaque and undercosts longs.**
CLAUDE.md's own model is **~$23/short × 76 = ~$1,750 for shorts alone** — before a single long. 21 longs are 6-8 min, more scenes, NBP + veo, and Isaiah 53's *redo* alone was ~$18-20 on top of a full build. Realistic "everything to a cut" is closer to **$2,800-3,500**. The $1,940 shows no derivation. If it's "remaining work only," say so and show the subtraction. Also: *a cut is not the goal* — captioning + upload (the last two pipeline stages) are excluded.

**5. Distribution — the channel's actual purpose — is essentially absent.**
*"COMPLETE (uploaded) 0."* Yet there is **no posting plan**: no platforms (the user's own tracker = YT/TT/FB/IG ×4), no upload-kit step (title/desc/hashtags per clip — already a standing requirement), no cadence, no coordination of which shorts ride which long's launch. Priority #5 *"Post Isaiah 53"* has zero process behind it. A plan whose success metric is "uploaded" must define how things get uploaded.

**6. Doctrinal guardrail tension not surfaced — the scapegoat short.**
types-shadows guardrail: *"No inventing types the Bible never names... unless you can show NT warrant."* *"The Day of Atonement / scapegoat <Hebrews 9:12>"* — Heb 9:12 warrants the Day-of-Atonement *sacrifice*, but the **scapegoat** (Lev 16 goat sent away) has **no explicit NT type-statement** — exactly the debated case the series' own guardrail flags. The plan reproduces it without noting the warrant gap. More broadly: the plan *asserts* guardrails per series but has **no per-episode doctrinal pre-flight gate** tied to them.

**7. The enforced panel review is missing from the pipeline model.**
The project's defining discipline — ENFORCED independent panel on *every* LOCKED narration and significant plan — does not appear as a stage in *"planned -> narration -> mp3 -> ..."*. As modeled, the catalog can mark a narration done without the mandatory gate. Insert it between narration and mp3.

**8. "76 shorts" double-counts near-duplicates.**
*"It is finished <John 19:30>"* appears as **two** catalog shorts (words-from-cross **and** last-week, both flagged "cross-filed") and both count toward 76. Same for *"The Sign of Jonah"* (jesus-in-ot) vs *"Jonah - three days and nights"* (types-shadows) — two shorts, one event. Decide: dedupe, or differentiate-by-lens and state how. As-is the headline 76 overstates *distinct* content.

**9. Minor: tiering mislabel.** *"Tier-3 short backed by the anchor"* — Tier-3 is a **short**, not a long tier; it's mixed into a "long TIERING" list. Relabel so the three tiers aren't apples-and-oranges.

**10. Minor: orphans left undecided.** *"He Said It Under the Lamps ... orphan"* and the off-catalog Prodigal are correctly separated but get no decision (greenlight a parables series, or shelve?). A plan should make the call or flag it as an explicit user decision.

---

VERDICT: REVISE
TOP FIXES:
1. Resolve the funnel contradiction: a single series-anchor cannot be the "research meal" for 8 distinct-topic shorts — either downgrade those "backed by anchor" claims to honest placeholders or assign real flagships; and add a build schedule/cadence for the 21-long, 73-short bottleneck the long-first rule creates.
2. Add the missing arms that make it a *plan*: a distribution section (platforms, per-clip upload kit, cadence, short↔long launch coordination) and the enforced panel-review stage in the pipeline; move the goalpost from "to a cut" to "uploaded."
3. Fix the numbers and operability: show the cost derivation (shorts alone ≈ $1,750 by the project's own $23 model, so longs are undercosted), record the full absolute artifact path on every non-planned row, and dedupe/clarify the cross-filed John 19:30 and Jonah shorts plus the scapegoat NT-warrant gap.
