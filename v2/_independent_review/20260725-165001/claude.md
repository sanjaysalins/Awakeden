# Independent review — claude (OK, 270s)

I verified this plan against the actual codebase before judging. Most of its load-bearing claims check out — which makes the gaps that remain stand out sharply.

## What survives scrutiny (verified, not assumed)

- `LAYOUTS` names in §2 step 6 match `panel_animator/grid_choreography.py:40-48` exactly; `total_duration` multi-sweep exists (line 123-129).
- The clause-sized phrase builder is real (`build_phrase_board`, `pipeline/assembly_timing.py:220`).
- Technique-spec claims are honestly transcribed: Hailuo 2/2 clean, Seedance 1.5 Pro disqualified only on whole-page input (spec's own scoping note says per-panel was never re-tested — the plan's §4 "honest evidence note" matches), NBP ~$0.30/call ledger-verified, Kling $1.13. The $1.20/page stills line is 4 × the spec's verified $0.30/call — correct.
- No existing freeze lint to duplicate; `_comic_text_layer.py` POC and `COMIC_PAGE_ENGINE_DESIGN.md` both exist; the reuse story respects the locked `vertical-panels-cross-aspect-reuse` rule (no full-bleed reuse).
- Spend discipline (per-rung user OK, ledger, quote-first) matches the locked rules.

## Findings

**1. The validation ladder never touches the long-form input path — but the long is where the money is.** §9 claims "the long format runs the SAME pipeline (CP-1 math on a 6–8 min narration)" and §11 prices it at $85–180, yet Rung 3 only renders one 16:9 *page* from banked panels. Nothing validates word alignment on a 6–8 min narration (the shorts alignment path is validated at ~59s only), phrase-board page math at ~33 pages, or whether 7 layout shapes stay visually alive across 33 consecutive pages. A $0 dry-run of CP-1 on a real locked long narration's alignment belongs in the ladder before that spend is ever quoted.

**2. CP-5 "small, contained upgrade" understates a core rewrite.** `activeness()` (`grid_choreography.py:56-73`) is hard-wired to a uniform cyclic metronome — `cur = int(t // per_panel) % n`, neighbors via `(cur±1) % n` — and the attention-weighted pan (lines 197-204) assumes it. Narration-timed `focus` windows are variable-length, non-cyclic, and can revisit panels. That's a rewrite of the choreography core, not "render() accepts explicit focus windows." Also undefined: panel behavior in gaps between focus windows (the pan centroid at line 199 does something arbitrary when all activeness ≈ 0).

**3. Two looping mechanisms, no declared owner.** The grid's frame-wrap "freeze fix" is already implemented (line 181-183) but it's a hard last-frame→first-frame jump cut, not seamless. If CP-4 pre-extends every clip to exactly the page dwell, the grid wrap is dead code; if lengths ever mismatch, the wrap fires and CP-G8 won't catch it (a jump cut isn't "static"). The plan says the fix is "half-done, must be finished" but never states the rule: CP-4 owns looping, clip length must equal dwell exactly, and the in-grid wrap should become an assertion failure.

**4. CP-G8 is overclaimed ("kills this regression class permanently").** Non-focus cells are dimmed to 45% brightness with reduced contrast (lines 185-187), which compresses inter-frame pixel diffs; H.264 further smooths near-static regions; boomerang turnaround points are near-static by construction. A single fixed 0.8s threshold will false-FAIL dimmed breathing-stillness panels or pass slow melts. The project's own locked doctrine (`panel-variety-gate`, gate-calibration memory) says deterministic checks are a floor, not the ceiling — this gate needs calibration against known-good/known-bad pages before it's trusted, and the plan should say so instead of declaring the problem solved.

**5. The 10s-render escape hatch isn't priced.** CP-4: directional motion must forward-loop on "the clip's own low-motion tail, or get a 10s render." Action clips — the directional ones by definition — routinely end mid-motion with no low-motion tail. A 10s Kling render is ~2× the $1.13 line, and the §11 cost model prices 100% 5s clips. Related untested claim: a 5s clip boomeranged across a 16s dwell shows the same motion 3+ times inside one page hold — the POC evidence is 12s pages only, and Rung 1 is a single page.

**6. Bubble readability vs. spotlight dimming is undefined.** CP-6 text "persists to page end," but its panel spends most of the dwell dimmed to 45%. Dim the bubble too and the muted-viewing policy (§7, bubbles carry dialogue) breaks; keep it bright and it floats off its artwork. This decision will otherwise surface mid-build.

**7. Unstated operational dependency: the agent bridge.** `LLM_PROVIDER` defaults to `agent` (`config.py:29`) because the metered Anthropic key is dead. The CP-1 LLM pass, self-review, and independent audit all require the in-chat agent servicing the file bridge — no unattended runs. Feasible, but the build plan should name it; it's also the only reason the cost table's silent omission of LLM cost is correct.

**8. Small but spec-grade nits.** (a) §1 mislabels the alignment source: `pipeline/assembly_align.py` is ElevenLabs forced-alignment first, whisper fallback (lines 6, 141, 230) — ElevenLabs availability is on the critical path for the clock. (b) `round(T/12)` at T=390 is 32 under Python banker's rounding, not the "~33" the doc claims — pin the rounding rule, since CP-G6 gates on it. (c) CP-G6 FAILs dwell-out-of-band, but nothing defines the resolver when phrase-snapping pushes a page outside the band (merge? split? human?).

The bones are right: real reuse, honest evidence citations, paid validation gated per rung, human gates in the correct places. But the plan under-scopes its signature $0 feature (narration-timed spotlight), over-trusts its signature gate (freeze lint), and prices a long-form path no rung ever exercises.

VERDICT: REVISE
TOP FIXES:
1. Add a $0 long-form dry-run rung (CP-1 math + word alignment on a real locked 6–8 min narration) before the $85–180 long-form cost claims stand — no current rung touches the long-form input path.
2. Re-scope CP-5 honestly: narration-timed focus windows mean rewriting `activeness()` and the pan model (cyclic-metronome assumptions at `panel_animator/grid_choreography.py:56-73, 197-204`), defining gap/ambiguous-window behavior, and declaring CP-4 the sole loop owner (clip length == page dwell asserted; in-grid frame-wrap becomes an error, since its jump cut evades CP-G8).
3. Calibrate CP-G8 against known-good/known-bad pages before trusting it (45%-dimmed cells + H.264 compress frame diffs; boomerang turnarounds are near-static), and add the 10s-render fallback for tail-less action clips to the §11 cost model.
