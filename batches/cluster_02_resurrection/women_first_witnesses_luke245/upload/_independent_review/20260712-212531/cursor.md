# Independent review — cursor (OK, 60s)

## Adversarial findings

### Ship-readiness / internal contradictions (blocking)

- **Header vs body:** The kit says **“Gates: FAILURES ❌”** and **“UK-G2 KJV-strict — could not resolve KJV text for”** (with blank **Anchor:**), yet the intro claims copy is **“pre-checked, red-teamed and panel-reviewed”** and the in-engine red-team says **“VERDICT: PASS … nothing blocks publication.”** Those cannot all be true. `upload_kit.json` has `"all_gates_pass": false` and empty `anchor_ref` / `anchor_kjv` — UK-G2 never ran against an anchor verse.
- **UK-G7 is a false green:** It is marked ✅ **“plain ASCII”** while every footer ends with **“✝”** (non-ASCII). UK-G7 only checks em-dash/curly-quote slop, not ✝, but the label overclaims. Worse: verse front-load is **skipped** because `anchor_ref` is empty — so YT/FB never got the “Luke in first 157 chars” check the gate is supposed to enforce.

### HOOKY BUT HONEST — title overcompression / bait risk

- **YouTube (Short) TITLE:** **“Even the Apostles Called the Resurrection an Idle Tale”** — KJV Luke 24:11 says **“their words seemed to them as idle tales”** (the *report*), not “the resurrection.” The title swaps the grammatical object and makes it sound as if the apostles named the resurrection itself nonsense. That is sensational compression, not a straight text hook.
- **YouTube (Long-form) TITLE:** **“…Women No Court Would Believe”** — Luke never mentions courts or legal weight. That is apologetic inference stacked into the title as if it were the biblical headline.
- **TikTok DESCRIPTION:** **“They called the first Easter report an ‘idle tale’”** — **“Easter”** is not in Luke/KJV. For a KJV-forward brand, that is mild calendar bait unrelated to the cited text.

### KJV verbatim

- **Individual fragments match KJV** (verified against project cache): 24:11, 24:5–6, 24:5–7 wordings are intact.
- **YouTube (Short) / Facebook DESCRIPTION** — the block in quote marks joins **24:11 → 24:5–6** with **“...”** in **reverse chapter order**. Citation **“(Luke 24:11, 5-6)”** discloses it, but a casual reader still sees one continuous “Scripture quote” that does not exist in that sequence. Under a strict KJV-strict lens, that is reordering inside quotation marks — the red-team’s “not a KJV-accuracy failure” is too generous.
- **UK-G2 failure is real:** With no anchor, the deterministic gate did **not** certify any quoted span. The ✅/❌ mismatch means publish copy is unvalidated by the project’s own fail-closed rule.

### Doctrine

- **Grace-anchored CTA is sound:** **“the risen Christ is seeking you”** / **“Stop seeking the living among the dead”** — invitation, not fear/gain-loss. Matches the video landing (`piece.json` / livingpage spec).
- **Apologetic history stated too flatly:** **YouTube (Short) DESCRIPTION** — **“whose word carried almost no weight in that world's courts”** and **“No one inventing a resurrection would have opened it there”** are not Luke; they are background argument. The short *does* deliver them (livingpage captions), so it is not a bait-and-switch vs the mp4 — but the copy presents inference as near-certainty (**“almost no weight”**, **“No one inventing”**).
- **YouTube (Long-form) DESCRIPTION** adds **“supported His ministry from their own means”** (Luke 8:3). The **82s short** never says that — only **“Luke named these women long before, Mary Magdalene, and Joanna.”** If the long block is used for this asset, metadata overclaims what the viewer hears.

### Platform fit

- **Wrong block for this asset:** **Format: short** · video path `…_sfx.mp4` · 9:16 · ~82s. The full **YouTube (Long-form 16:9)** section (title, 1490-char description, long tags) is for an asset that does not exist here. High paste risk: wrong title length, wrong framing, extra claims.
- **YouTube (Short) fold:** First ~157 characters are **“The very first report that Jesus had risen was dismissed as nonsense - by His own apostles…”** — no **“Luke”**, no KJV hook above the mobile “more” fold. Weak for YT Short discovery.
- **TikTok / Instagram:** First lines are punchy and on-thread. Hashtag counts are sane (TikTok 6, IG 11).
- **Tags:** Mostly real search terms (`Mary Magdalene`, `Luke 24`, `empty tomb`). **“Easter”** is seasonal, not text-native, but relevant to resurrection content.

### SEO honesty / templating

- **Facebook vs YouTube (Short):** Facebook drops **“He still sends His word to the overlooked”** present in the YT Short description — same video, diluted hook on one platform.
- **Chosen title** is memorable but trades accuracy for shock; **title option 2** (**“The First Witnesses of the Risen Christ Were Women”**) is more honest but blander — the kit picked click over precision.
- **Awakeden footer** is consistent; links (`@awakeden`, `awakeden.com`) look intact. CTA-to-Jesus is present on all platforms.

---

VERDICT: REVISE  
TOP FIXES:  
1. Set `anchor_ref` + `anchor_kjv` (e.g. Luke 24:11), re-run UK-G2 until green, and reconcile the header — remove **“pre-checked”** / red-team **PASS** while **Gates: FAILURES** remains.  
2. Rewrite **YouTube (Short) TITLE** to match Luke’s object (report/words as idle tales), not **“the Resurrection an Idle Tale.”**  
3. Delete or clearly mark **YouTube (Long-form 16:9)** as **do-not-use** for this short-only file; trim long-only claims (e.g. **“from their own means”**) from any copy tied to `women_first_witnesses_luke245_sfx.mp4`.
