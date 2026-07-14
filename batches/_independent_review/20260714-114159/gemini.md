# Independent review — gemini (OK, 183s)

Here are the findings from an independent, adversarial review of the v2 rollout plan:

**1. Hidden Risks & Single Points of Failure (Gate Bypass)**
The plan claims the rollout gate is *"WIRED INTO the runner: `run_piece --stage animate` refuses paid renders"*. However, `run_piece.py` (line 346) wraps the gate in a conditional: `if (pj["animate"].get("living_light") or {}):`. 
*   **The flaw:** If a piece completely omits `living_light` clips from its manifest, this evaluates to `{}` and silently bypasses the gate entirely. It will render anyway, directly violating the "≥2 living_light clips" rule because the gate never runs to catch the omission.

**2. Feasibility & False Assumptions (Chronological Impossibility)**
The plan for Wave D states: *"de-dup stills: reuse_check FIRST... then bible-check fact cards"*.
*   **The flaw:** This is chronologically impossible. `run_piece.reuse_check` requires the exact prompt and reference image to compare against siblings. Those prompts are generated *by* the fact cards. You cannot check for reuse before you know what prompt you are checking. 

**3. Verification Gaps (Grade Arc Silently Passes)**
The machine gate claims to enforce a *"cold→warm grade arc with DIRECTION"*.
*   **The flaw:** In `pipeline/rollout_gate.py` (line 70), the temperature check is wrapped in `if temps:`. If a piece has `fx` (like `rays` or `dust`) on ≥50% of beats to satisfy the FX minimum, but omits `temp` entirely, the `temps` array is empty. The script skips the check and silently passes the piece without it actually having the required grade arc.

**4. Cost / Spend (Misaligned Ceilings & Sloppy Math)**
*   **Misaligned Ceilings:** The plan relies on a *"pre-flight `pipeline.cost summary` vs the $25/short ceiling"* to manage spend, but sets a *"HARD STOP-LOSS: 485cr cumulative"* (~$45-50). The per-episode ceiling is mathematically useless here; just two episodes hitting $24 would blow past the entire corpus stop-loss without ever triggering the per-episode warning.
*   **Double-Counting:** The budget math calculates `12 pieces × 2 clips = 24 × 7.5cr = 180cr`, applies the 2.3x multiplier to get `~415cr` (which covers ALL 12 pieces), and then inexplicably adds `+ Wave D stills/clips ≈ 110cr` on top of it to reach `~525cr`. Wave D is already included in the 12 pieces.

**5. Reuse (Duplicated Audio Systems)**
The plan relies on a human checklist to *"verify no doubled audio vs the piece's sfx-bed builder (spec beat `sfx` and the `_sfx.py` bed are separate systems)"*.
*   **The flaw:** This is a duplication of systems that introduces manual toil and risk of error. The pipeline should unify the audio injection rather than relying on human eye-checks to prevent the two separate systems from doubling up.

VERDICT: FAIL
TOP FIXES:
1. Remove the `if` condition in `run_piece.py` line 346 so the rollout gate runs unconditionally on `--stage animate`, preventing pieces without `living_light` from silently bypassing the rules.
2. Fix `rollout_gate.py` line 70 to fail if `temps` is empty, ensuring the cold→warm grade arc is actually present rather than silently passing missing temperatures.
3. Fix the chronological impossibility in Wave D: author the bible-check fact cards FIRST to generate the prompts, then run `reuse_check` against those prompts.
