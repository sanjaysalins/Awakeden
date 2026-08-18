# Independent review — grok (OK, 216s)

I'll verify this plan against the real codebase — existing tools, paths, and prior work — before judging feasibility and risks.Checking the recommendation, Noon Frieze lighting claims, and whether the cited tools/gates actually exist.Found an early render script and a missing recommendation file — checking those next, plus how this conflicts with the Jesus-POV draft.## Findings

### 1. Parent plan is missing (false dependency)
Cites `_SECOND_LOOK_RECOMMENDATION.md` as the approved 6-step plan and source of “The Vantage.” That file is **not in the repo**. Only `_PLANT_SPEC.md`, `_plants_nbp.py`, and a partial `_plants/` folder exist. Claims of user sign-off, the 6-step sequence, and “The Vantage’s word-locked snap” are **unverifiable** from this artifact alone.

### 2. Plant 3 lighting claim is false
Phrase: *“low sun (already established in the Noon Frieze default palette — this plant needs no new lighting setup).”*

Noon Frieze is coded as **bright, sun-bleached daylight** (`_noon_frieze_nbp.py`: “Warm, bright, sun-bleached daylight”). Long crossbar shadows need **low sun**. That is a **new lighting setup**, not a free property of Noon Frieze. Style consistency and Plant 3 fight each other.

### 3. Plant 1 fails the spec’s own guardrail
§5: inventing poles that “wouldn’t plausibly be there” → fail.

Plant 1 then places two uprights at ~30° for a Golgotha read and calls that “nothing invented.” Numbers 21 does not put flanking poles there; existing `a_pole.png` has **one** pole only. Geometry for three crosses is the invented detail the guardrail bans.

Already-rendered `F:\slk\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_second_look_format\_plants\1_moses_raises.png`: the two “tent poles” are short stakes at Moses’s feet — they do **not** read as Golgotha. Plant 1 is failing in practice, not just on paper.

### 4. §1 vs §3 contradiction
§1: second reading by **composition alone** — “nothing added.”

§3 Turn then requires:
- Plant 2: a **second rendered Christ asset**
- Plant 3: pull-back to an **actual cross**
- Plant 4: freeze-match to **Christ’s pose**

That is added content, not composition-only. Act-1 loop plants and Turn reveals are conflated.

### 5. Pilot script conflict
Cited material is `look_and_live/_jesus_pov_poc/`. Its `_SCRIPT_DRAFT.md` opens as Jesus from line 1 (“I didn’t send a doctor…”). This spec holds Jesus’s name/voice out of the first **45s**. Same pilot folder, opposite voice rules. **No Act-1 narration** (who speaks Numbers 21 for 45s?) is specified.

### 6. Word-lock cites the wrong stage
§3: snap on “**lifted**” via “caption stage’s existing word-alignment JSON.”

In this repo, caption/alignment runs **after** assemble (`assemble` → `sfx` → `caption`). That JSON is not available when you cut the Turn. Need audio-stage timing (`per_turn_synth` / early align) or an explicit reorder — neither is written.

### 7. “Existing image gate” is overstated
§4: “through the existing image gate.”

`_plants_nbp.py` is ad-hoc NBP with a style ref. It does **not** run `pipeline/visual_render.py`’s `verify_image`, nor `/bible-check` fact cards. Spend can proceed without the fail-closed audit the phrase implies.

### 8. Timing math does not add up
Turn window **0:45–0:52** = 7s. Four plants × ~0.7s = 2.8s of picture. John 3:14–15 spoken is usually longer than 7s. Spec never says whether verse text is cut, sped, or the window is wrong.

### 9. Plant 4 ignores known animator limits
“Whichever animation provider… one-frame hold at full arm extension.”

Project lock: veo does **not** reliably do designed/cued holds; that tier is Kling. Spec treats hold as a free prompt detail. It is not.

### 10. Blind test + kill criteria underspecified
§4: “fresh reviewers,” no count, no who, no pass fraction. Plant 2 is load-bearing (highest-risk + Turn snap + extra asset) with **no kill/fallback** if the blind test or silhouette match fails.

### 11. Cost / premature build
No `$` estimate; no `/cost` pre-flight. Yet `_plants_nbp.py` already spent, and Plant 3’s prompt says the shadow “**unmistakably** reads as a cross” — that **breaks** the §4 target (“invisible unprimed”) before the test runs.

### 12. Assembly / CTA gap
Loop = final frame = opening frame. No statement whether this reuses `cli_assemble.py` + AS-G6/AS-G7 + ≥3s landing hold, or a bespoke cut. Nothing after **0:52** for conviction/CTA beyond the quote itself.

### 13. Soft exception logging
“If this pilot ships, it should be logged” — no file/process named (`structures.json`, `STATE.md`, constitution). Easy to fold into the default by accident.

---

**What is sound:** stills-first, no animation until §4; naming the 45s Jesus-hold as an explicit exception; Plant 2 risk flagged; doctrinal open questions are the right questions.

**What is not:** missing parent doc, false lighting claim, Plant 1 vs own guardrail, §1/§3 split, wrong alignment source, no Act-1 script, no cost/kill bar — and spend already drifting past the written gate.

VERDICT: REVISE
TOP FIXES:
1. Put `_SECOND_LOOK_RECOMMENDATION.md` in-repo (or stop citing it); define Act-1 narrator/script (non-Jesus 45s) and a real timing source for the “lifted” snap that exists *before* assemble — not caption JSON.
2. Fix Plant 1/3 honesty: drop or reframe the three-pole Golgotha invent; replace the false “Noon Frieze = low sun” note with an explicit lighting choice; add Plant 2 kill/fallback before more spend.
3. Separate Act-1 composition-only plants from Turn *added* reveals; state assemble/CTA/landing reuse (or bespoke) + a $ pre-flight; stop prompts that say the plant is “unmistakable” before the blind test.
