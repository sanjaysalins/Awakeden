# Independent review — gemini (OK, 76s)

Here is the independent, adversarial review of the proposed comic design plan.

### 1. Over-engineering & Feasibility (Remotion Reality Check)
*   **"each word a little wet, then dry." (Section 1.5, LIVING SCROLL)** You list this under "$0 graphics" built in Remotion. A wet-to-dry ink reveal per word requires highly complex custom SVG masking or Canvas engineering in React. This is massive premature over-engineering for a POC.
*   **"PAGE TURN... CSS 3D rotateY, paper back face, moving shadow" (Section 1.4)** Realistic 3D page curls with back-faces and dynamic shadows in raw Remotion/CSS are notoriously brittle and difficult to synchronize. If this component doesn't already exist in `_remotion/src/`, this is a multi-day build disguised as a simple transition.
*   **"a thin gold thread draws between them." (Section 1.5, GOLD WORD)** The first gold word appears on Page 3B. The second appears on Page 5B. They are separated by two page turns, a RIFFLE, and a DIVE. You cannot draw a persistent thread between two DOM elements that are never on screen at the same time.

### 2. Unjustified Spend & Ignored Reuse
*   **Zero-headroom paid clips:** You are paying to animate S02 (empty night road), S11 (vast night sky thick with stars), and S13 (three crosses far off). `CLAUDE.md` strictly forbids this: *"judge each shot's own cinematic headroom BEFORE spending — a shot that would only ever read as a camera push... should go straight to the $0 dynamic_cam3d push"*. These should be $0 static Ken Burns pushes, not `veo3_1_lite` renders.
*   **Ignoring existing clip reuse:** You plan to reuse stills (`D_barabbas_micah.png`, `D_barabbas_manger.png`) to generate brand new clips (C04, C05). `CLAUDE.md` explicitly demands *"Reuse-first for 9:16 grid panels: before generating a new panel clip... check the shorts' own rendered clips... for a topically-matched one"*. If the Barabbas stills exist, the Barabbas clips likely exist too. Re-animating them wastes credits.
*   **Kling Duration Risk:** C04 calls for **"Kling 10 s"**. Standard Kling generation is 5s. Pushing to 10s requires a costly extension or Kling Pro 10s mode, which spikes the cost and drastically increases the risk of hallucination (the pen scribbling).

### 3. Missing Verification & Self-Contradiction
*   **Missing standard gates:** The plan completely ignores the `visual_tags.json` and `panel_variety_lint.py` requirements from `CLAUDE.md`. You cannot ship a multi-panel comic grid without tagging these 14 stills and running the deterministic panel-variety gate to prevent visual redundancy.
*   **Violating own typography rules:** Section 1.3 strictly sets **"max 7 words a line"**. Yet Section 2 scripts Page 3B with `out of thee shall he come forth unto me` (9 words) and Page 8C with `and rose from the dead on the third day.` (9 words). The plan fails its own safety limits for screen space.

VERDICT: REVISE
TOP FIXES:
1. Strip the unproven, over-engineered Remotion effects (wet-to-dry ink, 3D CSS page curls, cross-page threads) and stick to standard 2D masking/wipes unless the components already exist.
2. Cut the animation spend: swap zero-headroom shots (S02, S11, S13) to $0 `dynamic_cam3d` pushes, and reuse the existing Barabbas clips for C04/C05 instead of re-rendering.
3. Fix the self-contradictory 9-word text lines to respect your 7-word limit, and explicitly add the `panel_variety_lint.py` tagging step to the pipeline.
