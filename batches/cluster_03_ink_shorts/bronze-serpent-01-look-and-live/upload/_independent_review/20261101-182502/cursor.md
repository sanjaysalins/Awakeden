# Independent review — cursor (OK, 107s)

## Findings (adversarial pass)

### HOOKY BUT HONEST / bait-and-switch
- **YouTube (Short) DESCRIPTION:** *“Just a look at the very thing that was killing them”* — The **live fiery serpents** killed them; the **bronze serpent on the pole** did not. Same imprecision as the locked narration. Not full clickbait, but it **over-tightens the paradox** and a Bible-literate viewer can read it as sloppy exegesis in metadata that claims red-team PASS.
- **YouTube (Short) DESCRIPTION:** *“The cure was shaped like the curse”* — Numbers 21 never calls the bite or the pole “the curse”; that’s **typology language** (Gal. 3:13 territory) sold as if it were the OT line. Honest curiosity hook is fine; this reads like **doctrine compressed into a slogan** the anchor text doesn’t say.
- **Artifact header vs body:** **Format: short** and the file is `…LOOKANDLIVE_living_sketchbook_cc_scored_sfx.mp4`, yet a full **“YouTube (Long-form 16:9)”** block exists with the **same title, description, and tags**. That’s an **operational bait-and-switch**: paste the wrong section and you publish **short copy on a long upload** (or imply a 16:9 asset that isn’t this file).

### KJV verbatim
- **Facebook / YouTube quoted block:** *“Make thee a fiery serpent, and set it upon a pole: and it shall come to pass, that every one that is bitten, when he looketh upon it, shall live.”* — Matches the KJV cache for Numbers 21:8 **as an excerpt** (no altered words inside the quotes).
- **Not a quote violation, but a honesty flag:** Attribution **“(Numbers 21:8, KJV)”** on a span that **drops** *“And the LORD said unto Moses,”* — defensible as partial quote, but viewers expecting a **full verse** may treat it as trimmed without warning (only Facebook says `Numbers 21:8`; YouTube says `21:8-9` while still quoting 21:8 only in the block).
- **Prose vs KJV (not inside quotes, still on-brand risk):** *“God told Moses to put a **bronze** one on a pole”* (YouTube/TikTok) while the kit’s own KJV line and 21:9 use **“serpent of brass.”** Not UK-G2-fail material, but **“KJV bible” tag + KJV footer** next to non-KJV metal vocabulary is a **trust paper cut**.

### Doctrine (evangelical, Christ-pointing, grace)
- **Strength:** John tie-in is explicit (*“Jesus pointed back to it… John 3:14”*); no fear/gain-loss boilerplate in the upload copy (the narration’s *“our own effort”* line is wisely **omitted** from these captions).
- **Weakness — gospel completion:** John 3:14–15 ties **looking (typologically) to the Son lifted up** and **life to believing in him**. The kit stops at **“Look at what was lifted up for you, and live”** without **faith/believe** language. That matches Numbers’ **look → live** but **under-specifies John’s bridge** for cold traffic — looks like **look-only soteriology** unless the video audio carries “believe” clearly.
- **YouTube (Short) DESCRIPTION:** *“as a **picture** of Himself”* — John 3:14 is **“even so must the Son of man be lifted up”** (parallel/event), not “picture.” Acceptable typology, but **soft paraphrase** where a hostile reader will ask for the **actual KJV wording** on a Christ claim.

### Platform fit
- **TikTok DESCRIPTION first line:** *“Numbers 21:8-9. The cure for snakebite was a look at a snake on a pole.”* — Compliant, dull: **reference-first**, then **repeats the YouTube title** instead of a **scroll-stop hook** (e.g. alt title #4 *“Why Did God Ask Israel Only to Look?”* energy). House spec wants **hook in the first line**; this is **SEO-safe, not TikTok-native**.
- **Instagram Reel DESCRIPTION first line:** Same pattern — *“Numbers 21:8-9. The cure for snakebite…”* Only ~125 characters show before “more”; you burn fold space on **citation**, not paradox or Christ hook.
- **YouTube (Long-form 16:9) TAGS:** includes **`bible shorts`** while the artifact declares **short** — **SEO dishonesty** if that block is used for a long upload.
- **YouTube (Long-form 16:9) DESCRIPTION:** ~828 characters vs house **target_min 600** — passes length, but **no long-form affordances** (chapters, “deep dive” framing, distinct title). It’s **short copy wearing a long label**.
- **Hashtag counts:** YouTube (5), TikTok (5), Facebook (3), Instagram (8) — within `platform_specs.json` targets; **sane**.
- **Facebook TITLE:** *“The cure for snakebite was a look at a snake”* (sentence case) vs YouTube **Title Case** — minor **cross-platform brand inconsistency**, not fatal.

### SEO honesty / templating
- **TAGS (YouTube Short and Long blocks):** `numbers 21, bronze serpent, serpent on a pole, look and live, …` — **relevant**, not stuffed; **`john 3 14`** is appropriate.
- **Forgettable / templated:** Chosen title **#1** is honest but **long and descriptive**; it **mirrors the opening sentence** of the YouTube description (*“You would think the cure… would be anything but a snake”* is stronger in body than title). Alt **#4** (*“Why Did God Ask Israel Only to Look?”*) is unused and likely **stronger honest click** for Shorts.
- **Boilerplate:** *“Find Jesus in the whole Bible, one panel at a time. Subscribe/Follow Awakeden. ✝”* on every platform — **on-brand**, but TikTok/IG **share identical spines**; little **platform-specific payoff** after the fold.

### Brand / CTA / links
- **CTA-to-Jesus:** Present via **Jesus / John 3:14** and *“Find Jesus in the whole Bible…”* — passes a **marker check**, but the **landing line** *“Look at what was lifted up for you, and live”* is **cluster-generic** (could fit multiple atonement shorts); **doesn’t name cross, Son of man, or believe**.
- **Footer/links:** YouTube/Facebook **Follow + https://awakeden.com + KJV PD line** — look **intact**. Instagram/TikTok correctly **omit clickable URLs** in caption (spec-correct).

### Meta / process skepticism
- **✔ Verification / Red-team `VERDICT: PASS`** — Treat as **overconfident** given the **phantom long-form block**, **brass/bronze prose**, **“thing that was killing them”** slip, and **John 3:14 paraphrase without 3:15 believe**. Gates may PASS substring KJV; **upload quality for humans** still has gaps.

---

VERDICT: REVISE  
TOP FIXES:  
1. **Remove or clearly gate the “YouTube (Long-form 16:9)” section** for this **short-only** asset; if kept, **rewrite tags** (drop `bible shorts`), **differentiate title/description**, and don’t duplicate the Short block verbatim.  
2. **Fix precision in the hook body:** say **Moses made/raised the serpent of brass** (match KJV metal word in prose), and rephrase *“the thing that was killing them”* to **the image/shape of what killed them** (or live snakes vs bronze image).  
3. **Strengthen TikTok/Instagram first lines and the Christ landing:** lead with the paradox question/hook (not `Numbers 21:8-9.` first), and tie **John 3:14–15** with at least one **plain “believe / Son of man lifted up”** clause so the CTA isn’t look-only for strangers.
