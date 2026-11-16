# Independent review — gemini (OK, 159s)

Here is the adversarial review of the TWO DRIVERS ROADMAP. 

**1. Fatal Cost Hallucination (Cost / Spend)**
- **Claim:** `"Estimate | about $8-14 per short | Bethlehem about $8. Well about $13.69."` and `"Month | about 8 films, about $65-110"`
- **Finding:** This is mathematically impossible against the real codebase's locked cost model. `CLAUDE.md` explicitly states episodes cost `"~$23/episode, ±30%"` (Kling ~$11, Images ~$5, Opus ~$5-6, Audio ~$0.50). The plan is assuming a 50% discount that does not exist in the pipeline. If you scale this to 8 films a month, your budget will immediately blow past $110 to ~$184+. 

**2. Tool Duplication & Abuse of CLI Architecture (Reuse / Feasibility)**
- **Claim:** `"3. Blind hunt | 6 seats (Fable + Sonnet + claude / codex / gemini / grok CLIs). Each works alone. ... run_seats.py"`
- **Finding:** You are duplicating the existing engine and abusing the review tools. The codebase *already* has a Stage 0 generation step (`pipeline/engine.py`'s `discover_thread` using Opus 4.7) and a divergent Draft Tournament. Furthermore, the local CLIs (`claude`, `gemini`, `grok`, etc.) are explicitly designated in `CLAUDE.md` for *read-only adversarial review* via `independent_review.py`, NOT for bulk parallel text generation. Building a new `run_seats.py` script to scrape local CLI output for generation is massive over-engineering. Improve `discover_thread` instead.

**3. Verification Gap / Contradicting its Own Rules (Missing Steps)**
- **Claim 1:** `"Q3 | Machine check | Every quote passes kjv_check.py. 0 MISMATCH."`
- **Claim 2:** `"Not checked by machine... T2: the three wilderness answers all come from Deuteronomy (8:3, 6:16, 6:13). Only 8:3 was quote-checked here."`
- **Finding:** The plan explicitly mandates 100% machine checking for every quote (Q3), and then immediately admits it skipped checking two of the three quotes for episode T2. If the roadmap candidates aren't fully validated by the script, the "0 MISMATCH" claim is false.

**4. Fragile Waterfall Schedule (Hidden Risks / Single Points of Failure)**
- **Claim:** `"Thu | PAID voice, pictures, clips for film 1. QC every still and clip ... Fri | Build film 1."`
- **Finding:** This assumes a 100% pass rate in the engine. The real codebase is highly adversarial, containing strict gates (Vision content audits, SP-G1..G9, AS-G1..G7). If a Baroque NBP render fails the vision audit, or Kling hallucinates (which requires a REVISE loop and re-render), your Thursday-Friday pipeline instantly breaks. The schedule has zero slack built in for the engine's mandatory loop/revise cycles. 

VERDICT: REVISE
TOP FIXES:
1. Update the financial estimates to reflect the real ~$23/episode cost model from `CLAUDE.md`, or explicitly justify what pipeline tiers are being downgraded to hit $8.
2. Drop `run_seats.py` and the CLI-generation farm; integrate the new "blind hunt" scoring parameters directly into the existing API-driven `discover_thread` and tournament functions in `pipeline/engine.py`.
3. Run `kjv_check.py` on the missing T2 (Deuteronomy) and T8 (Acts) quotes to legitimately satisfy your own Q3 invariant before calling the candidates valid.
