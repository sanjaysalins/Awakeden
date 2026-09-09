# Episode 12 — "Ye Are Not All Clean" (John 13:1-30, Judas) — status 2026-09-09

## Where this stands

**Narration LOCKED 2026-09-09.** `narration.md` in this folder is final — 15 rounds of the 5-CLI
independent-review panel across two full passes (a Sonnet hand-edit lineage, then a genuine Fable
creative rewrite per the user's request to find more conviction). Doctrine, KJV verbatim, and
no-fear-framing confirmed clean by every reviewer in every round of the final (Fable) lineage.
User approved lock on the one remaining open item (the CTA's exact closing shape — a genuine
producer-level call, not a defect) 2026-09-09. Full history:
memory `project_ye_are_not_all_clean_episode_12`, `_NARRATION_PANEL_STATUS.html` in this folder,
and `_independent_review/` (15 timestamped rounds).

**Locked text:**

> Judas walked out into the night on feet Jesus had washed.
>
> John says the devil had already "put into the heart of Judas Iscariot, Simon's son, to betray
> him." Jesus knew. He knew as He poured the water. He knew as He dried their feet with the towel.
>
> Then He told them, "ye are clean, but not all." And He quoted the old word for betrayal, from
> Scripture: "He that eateth bread with me hath lifted up his heel against me."
>
> He handed Judas the sop — a piece of dipped bread. "That thou doest, do quickly." Some at the
> table thought he had gone to buy food. Judas "went immediately out: and it was night."
>
> Jesus did not wash those feet because Judas earned it. He washed them knowing Judas would
> betray Him anyway. That is what His love does when it already knows the worst.
>
> He knows your heart, every corner of it, like that. He has not put the towel down — bring Him
> your worst.

169 words. $0 gate: PASS (`narration_gate.py`).

## Plan-only verification pass — DONE, both real risks cleared (2026-09-08)

1. **Zone-separation storyboard (QUAD-lock "never touch" vs. John 13's literal foot-washing
   contact): holds.** John 13:1-11 dramatizes only ONE individual exchange (Peter's protest,
   v6-9) — nothing in the text forces a panel singling out Judas's own feet at the basin. Judas's
   distinct beat naturally lands later, at the sop (13:21-30) — bread, not feet, no basin, no
   swirl-motif staging there. So the page design v4 of the series plan already proposed — "Jesus's
   swirl centers on the basin where he washes the OTHER disciples; Judas's stain stays local to his
   own feet, a clean-paper band between them" — is achievable, not just asserted. Full writeup:
   memory `project_swirls_backlog_v6`.
2. **`pipeline/handoff.py` truncating the wide John 13:1-30 ref span: does not apply.** Confirmed by
   direct code check — grepped the whole `poc_living_water_ink_style_test/` tree for any use of
   `pipeline.handoff` or `write_narration_folder`. Zero matches, anywhere. The Swirls pipeline never
   routes narration through that main-engine code — narration is hand/Fable-written straight into
   each episode's own `narration.md`. This "risk" had been copy-pasted across v4→v5→v6 of the series
   plan (and re-flagged again by the independent panel) without anyone ever checking whether the
   code path it names is even in the Swirls build's execution path. It isn't.

## The landing decision — RESOLVED 2026-09-09

User chose to keep the binding G8 CTA-to-Jesus requirement over a format exemption. First closing
beat (Sonnet-written, small addition) went through 9 panel rounds; then, per the user's explicit
request for "another perspective from Fable and the panel" to find more conviction, a fresh Fable
creative pass replaced it with the "washed anyway / knew he'd betray anyway" turn above — 6 more
panel rounds, now LOCKED. See memory `project_ye_are_not_all_clean_episode_12` for the full
round-by-round history, including the note on which specific fixes worked and which introduced new
problems (useful precedent for future episodes on this same "washed ≠ saved" territory).

## Voice synthesis — DONE 2026-09-09

Ran the real pipeline: `PythonProject1/jesus/narration_pipeline.py --stage verify` → `--stage tag`
→ `--stage audit` (agent-bridge serviced live, 3 requests: verify, tag, audit — all passed, tag
validation/speaker validation/round-trip prose all clean), then
`PythonProject1/jesus/narration/per_turn_synth.py --target 65 --pre-quote-pause 0.4 --stability 0.65
--natural` (real ElevenLabs spend, user-approved). One tonal tag fix applied from the audit's own
finding (dropped `[deliberate]` off paragraph 4 — it fought the text's own "do quickly"/
"immediately" urgency).

**Result:** `narration.mp3`, 74.55s, natural pace (no time-stretch — `narrator_atempo_factor: 1.0`
in `narration.meta.json`), voice `LSi9zNCeliLuhIGGS0By` (series-standard narrator). Ran 9.56s over
the 65s target ceiling; per this project's standing rule (never compress to hit a target, trim
words instead if it matters — see `feedback_narration_process_gold_standard`), this was accepted
as-is rather than compressed. **HUMAN GATE 1 — APPROVED 2026-09-09** (user: "lock it").

## Next steps now that the narration is locked, voiced, and GATE 1 approved

1. Now the `/swirls-of-life` skill's own Step 0 — the Fable "design machine" pass over the locked
   narration + `NORTH_STAR_PROMPT.md` + `NORTH_STAR_ANIMATION_PROMPT.md` — to produce the full
   shot-by-shot still+animation design table, including the Stain-motif dosage per page
   (`stainDose + swirlStage <= 4`, this page's own AT-CAP 2+2 shape already sanity-checked against
   ep7 F04 / ep10 F07 precedent).
2. Decide generation route: OpenArt/HF (this series' locked default) or Google Flow (now proven
   end-to-end on "My Lord and My God," see memory `project_google_flow_pilot_process`) — not yet
   decided for this episode specifically.
