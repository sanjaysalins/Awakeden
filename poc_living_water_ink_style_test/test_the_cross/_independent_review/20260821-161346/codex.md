# Independent review — codex (OK, 269s)

**Findings**

- **High:** Build order contradicts its own risk table. Step 1 says Talitha Cumi has “**no multi-ref complications**,” but the risk table says “**Affects #6 (Talitha, two Mark chunks)**,” and #6 is `Mark 5:21-24, 35-43`. That makes Talitha a bad “simple pilot” unless the pilot explicitly tests/fixes multi-ref handling.

- **High:** The plan treats a POC fork as production. It says “**swirls pages don't go through `cli_visual.py`**” and accepts “**full deterministic gates ... deferred**.” The real project contract routes visuals through SP/AS-style gates; `PRODUCTION_PIPELINE.md` also says assembly still remains a forked `northstar_shortform/` script. This plan needs substitute gates and an executable runner path, not just “northstar-style.”

- **High:** “**each independently verified clear**” is overclaimed. The same document later says governance “**Needs a fresh `independent_review.py ...` run ... not yet run**.” There is no collision matrix showing searches across manifest, narration folders, longform, POCs, and planned backlog.

- **Medium:** The motif taxonomy still has weak assignments. The rule says “**Fray — fear/doubt only**,” but #7 “**Weep Not**” is grief at a funeral, not clearly fear/doubt. This repeats the same class of taxonomy drift that caused the Martha cut.

- **Medium:** #14 invents a new swirl behavior. “**the swirl is actively pushed toward the frame's edge by the crowd's own rising hostility**” is neither the stated Stage 0-3 dosage system nor dead ink. It also risks violating the animation law that motif change happens between pages, not as in-clip story action.

- **Medium:** Cost bands conflict with the repo’s ceilings. “**Short: $20-46/episode ... + ~$5-6 narration**” can reach ~$52, above the project’s `$25` short ceiling; “**Long: $50-95**” exceeds the `$40` long ceiling while admitting “**zero ledger evidence**.” `/cost` signoff is named, but no page-count-based preflight estimate is required.

- **Medium:** Long-form is still not planned. “**LONG, 7 movements, 16:9**” does not map to the swirls long-form guidance: ~20-26 spreads, hero-spread ratio, and Focal Tour reuse. “**Consider a shortened ‘one movement’ spike**” should be a required gate, not optional.

VERDICT: REVISE
TOP FIXES:
1. Replace the pilot gate with explicit exit criteria: page count, ref-chain test, one Stain and one Fray on new content, caption/landing-hold checks, and a real assembly path.
2. Reconcile the swirls fork with production governance: define substitute gates or wire it into existing gate equivalents before any lock.
3. Attach a real collision/cost matrix with search method, `series.json` refs, and `/cost` preflight numbers against project ceilings.
