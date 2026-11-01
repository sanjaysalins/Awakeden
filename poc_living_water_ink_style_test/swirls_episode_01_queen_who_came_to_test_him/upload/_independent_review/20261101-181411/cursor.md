# Independent review — cursor (OK, 52s)

Independent adversarial review of the upload metadata (cross-checked against `narration.md`, the episode SRT, and `data/kjv_cache.json`).

---

### HOOKY BUT HONEST / bait-and-switch

- **YouTube (Short) TITLE — “Jesus Noticed.”** The narration says Jesus **“pointed straight back to her, to make a claim about Himself”** — active Christological claim, not passive observation. “Noticed” reads like a curiosity/relationship hook (“Jesus saw her journey”) and softens the punch line **“a greater than Solomon is here.”** Not a flat lie, but the second sentence oversells intimacy vs what the text and video deliver.

- **YouTube (Short) DESCRIPTION — “find out if Jesus is real.”** The locked narration ends with **“to find out if it is true”** (referring to the greater-than-Solomon claim in front of the hearers), not an apologetics line about **Jesus’s existence**. Metadata shifts the CTA toward “is Christianity true?” — a different promise than the video’s landing. Mild **bait-and-switch** vs the actual CTA (**“Just ask Him your hardest question”**).

- **Opening hook — “test a rumor.”** KJV (1 Kings 10:1) is **“heard of the fame”** and **“prove him with hard questions”**; doubt is **“believed not the words”** (10:7), not “rumor.” Colloquially fair, but **“rumor”** slightly sensationalizes royal **fame/report** language.

- **YouTube vs body — “desert” vs “continent.”** TITLE: **“Crossed a Desert”**; DESCRIPTION: **“crossed a continent.”** Same paragraph family, different geography — not fatal, but looks templated and weakens trust on a history-adjacent hook.

- **In-engine red-team** admits metadata **omits** Matthew’s judgment/condemnation clause. The **video does speak** “rise up in the judgment with this generation…” (with ellipsis). Description-only readers get a **sanitized** Matthew; watchers hear judgment. That is selective framing, not necessarily false — but **“ALL PASS”** on doctrine/platform honesty understates the mismatch between **upload copy** and **finished short**.

---

### KJV verbatim

- **1 Kings block quote (YouTube Short/Long, Facebook partial):** The embedded clause from **“It was a true report…”** through **“…the half was not told me”** matches the repo KJV corpus for 10:6–7 (stopping before **“: thy wisdom and prosperity…”**). **PASS** for that quoted span.

- **Matthew 12:42 (YouTube Short/Long, Facebook):** Marked KJV:
  > `"behold, a greater than Solomon is here"`
  
  Corpus KJV: **“and, behold, a greater than Solomon is here.”**  
  The quoted string **drops the leading “and,”** and uses a lowercase **“behold”** where the verse clause is **“; and, behold,”**. If UK-G2 means “any KJV-attributed quotation is punctuation/word exact,” this is a **FAIL**, not the red-team’s PASS.

- **TikTok / Instagram:** Matthew line is **unquoted** paraphrase (**“a greater than Solomon is here”**) — not claimed as KJV; OK, but **inconsistent** with YouTube’s strict-quote standard.

---

### Doctrine / framing

- **Christ-pointing:** **“greater than Solomon”** + hardest-question invite — evangelical, grace-anchored, no works/gain-loss. **PASS.**

- **Judgment omitted in descriptions** while present in audio — avoids fear framing in metadata but creates **copy vs content** tension (see above). Not heresy; **editorial skew**.

- **“find out if Jesus is real”** — edges toward **evidence/testing Jesus** rather than **encountering the one who is already “here”** (as narration puts it: **“A greater than Solomon is already in front of you”**). Not fear-based, but **works-adjacent “verify me”** tone vs the video’s **presence/ask** landing.

---

### Platform fit

- **Header: `Format: short`** but a full **“YouTube (Long-form 16:9)”** block duplicates Short copy — wrong operator signal; easy to paste into a long upload by mistake.

- **YouTube (Long-form 16:9) TAGS — `bible shorts`:** Wrong keyword bucket for 16:9 long-form; **SEO dishonesty** if that block is used.

- **TikTok DESCRIPTION first line:** **“1 Kings 10.”** — citation stub, not a scroll-stop hook; title energy (**desert / rumor / Jesus**) is buried.

- **Instagram Reel first line:** Same — **“1 Kings 10.”** before the story; weak for Reels preview.

- **Facebook TITLE:** **“Jesus noticed.”** (lowercase **noticed**) vs YouTube **“Jesus Noticed.”** — inconsistent brand/hook on the same episode.

- **Hashtag counts:** Short YT 5, Long YT 3, TikTok 5, FB 3, IG 8 — **sane**, not stuffed.

- **Tags field:** **“matthew 12 42”**, **“queen of sheba”**, **“greater than solomon”** — real search terms aligned to content. **PASS** (except **bible shorts** on long block).

---

### SEO / templated feel

- **YouTube Short + Long-form:** Descriptions are **byte-identical** — lazy for two products; long-form usually wants chapter context, series link, or chapter timestamps (even for a re-cut).

- **Repeated brand tail** (“Find Jesus in the whole Bible, one panel at a time…”) — on-brand but **series-template**; fine if intentional.

- **Alt title 4 — “A Greater Than Solomon Is Here”:** Ungrammatical in standard English without **“Someone”** or **“One”** — good that it is not chosen, but shows title pool quality ceiling.

---

### Brand / CTA / footer

- **CTA-to-Jesus:** **“Bring Him your hardest question”** — present; aligns with narration (video: **“Just ask Him…”**). **PASS** with the **“Jesus is real”** wording caveat above.

- **Footer:** **Subscribe/Follow Awakeden**, **@awakeden** URL, **https://awakeden.com**, KJV PD line — **not mangled**.

- **Status line:** **“Gates: ALL PASS ✅”** and **“pre-checked, red-teamed and panel-reviewed”** while **Matthew KJV attribution is debatable** and **long-form/tags contradict `Format: short`** — **overclaims readiness** (same pattern flagged in other cluster upload reviews).

---

VERDICT: REVISE  
TOP FIXES:  
1. Fix **Matthew 12:42** KJV-attributed text to include **“and, behold,”** (or quote a longer exact substring from the corpus) — do not label a trimmed clause as KJV if UK-G2 is strict.  
2. Remove or rewrite the **YouTube (Long-form 16:9)** block for a **short-only** asset; drop **`bible shorts`** from any long-form tag set and stop duplicating Short copy verbatim.  
3. Replace **“find out if Jesus is real”** with language that matches the video (**“if it is true”** / **greater than Solomon is here**) and soften or replace **“Jesus Noticed”** with honest Christ-claim wording (**“Jesus pointed back to her”** / **“a greater than Solomon is here”**).
