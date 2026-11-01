# Independent review — cursor (OK, 117s)

## Independent adversarial review — upload kit

### Integrity / process

- **YouTube — header vs body:** The kit says **「Gates: ALL PASS ✅」** and **「UK-G3 doctrine — no clickbait/overclaim tokens」**, but the in-engine red-team block on the same page is **`VERDICT: REVISE`** with an explicit title overclaim. Shipping metadata that ignores its own hostile audit is a trust problem for anyone copy-pasting “pre-checked” copy.

### Hooky but honest (title + repeated claims)

- **YouTube (Short) TITLE:** **`God Hung Up a Snake. It Was the Cure.`** — Numbers 21:9 does not call the brass serpent “the cure”; it says bitten men **「when he beheld the serpent of brass, he lived.」** The title drops **look/behold**, so it reads like the object itself healed them (mechanism bait). Your own red-team flagged this; alt **#2** (**「The Cure Looked Like the Thing That Was Killing Them」**) is closer to the text’s irony without asserting “it was the cure.”
- **Facebook TITLE:** **`God hung up a snake. It was the cure.`** — same compressed claim, lowercase variant.
- **Instagram (Reel) — first visible line:** **`God hung up a snake. It was the cure.`** — repeats the same overclaim in the ~125-character fold; weak honesty on the platform where the first line matters most.
- **Not bait-and-switch on the video:** `_spoken.txt` uses cure language and ends on Christ lifted up; descriptions match the piece. The issue is **metadata precision**, not promising a different topic.

### KJV verbatim

- **YouTube / Facebook descriptions:** The quoted Numbers 21:9 block matches project KJV cache verbatim (**「And Moses made a serpent of brass… when he beheld the serpent of brass, he lived.」**). **PASS** on altered words.
- **TikTok / Instagram:** ref-only (**「Numbers 21:9」**), no partial quote — fine.

### Doctrine (evangelical, Christ-pointing, grace)

- **YouTube DESCRIPTION:** **「Look at what was lifted up for you, and live.」** / **「Christ took your curse.」** — Christ-centered, typological, invitation not scare tactics. Aligns with narration (**「He became your curse… hung up Christ… so you could too」**).
- **Minor precision (not FAIL):** **「Christ took your curse」** is shorthand vs narration’s **「He became your curse」** / Galatians 3:13 idiom; acceptable for social, but **「became a curse for you」** is tighter if you want zero nitpick surface.

No obvious fear/gain-loss/works landmines in the copy.

### Platform fit

- **Artifact vs YouTube (Long-form 16:9):** Header says **「Format: short」** and points at a single living-sketchbook short MP4, yet the kit still includes a full **YouTube (Long-form 16:9)** block with the **same title, same 814-character description, and same tags** as the Short. `platform_specs.json` expects long-form descriptions **600+ chars with a fuller summary / optional chapters** — this is Short copy pasted into Long. Easy way to mis-upload or look lazy on a future 16:9 asset.
- **YouTube (Long-form) TAGS:** includes **`bible shorts`** alongside **`bible study`** — for a 16:9 long, that tag is **SEO dishonesty** (wrong intent keyword on the wrong format). Short block can keep it; Long block should not.
- **YouTube (Short) TAGS:** 12 keywords — within house 8–15; relevant (Numbers 21, bronze/brass serpent, types and shadows). Missing obvious search bridges (**`john 3:14`**, **`as Moses lifted up`**, **`nicodemus`**) is a missed opportunity, not stuffing.
- **TikTok DESCRIPTION — first line:** **`God hung up a snake.`** — clear hook; **Numbers 21:9** appears mid-caption (OK). Caption body uses **「Follow Awakeden」** (correct for social per brand split).
- **Instagram:** 8 hashtags — within 5–12 target; no clickable URLs in caption (correct). Hashtags are in a separate block — remind paste workflow to append them to the caption or first comment so they actually ship.

### SEO / templating

- **Repeated footer** on every platform: **「Find Jesus in the whole Bible, one panel at a time. Subscribe/Follow Awakeden. ✝」** — on-brand but **interchangeable** with sibling Types & Shadows shorts; title is doing most of the differentiation.
- **YouTube Short vs Long identical hashtags** except Long drops `#Numbers21` and `#KJV` — inconsistent strategy, not harmful on Short.

### Brand / CTA / links

- **CTA-to-Jesus:** Present via **「Find Jesus in the whole Bible…」**, **「Christ took your curse」**, **「Look… and live」** — not a stock **「come to Jesus」** closer. Good.
- **YouTube / Facebook footers:** **@awakeden**, **https://awakeden.com**, KJV PD line — not mangled.
- **Title case drift:** YouTube **「God Hung Up a Snake. It Was the Cure.」** vs Facebook **「It was the cure.」** — minor brand inconsistency.

---

VERDICT: REVISE  
TOP FIXES:  
1. Change the chosen title (and Facebook/Instagram opening line) so **looking/beholding** is in the hook — e.g. adopt alt **#2**, or **「God Hung Up a Snake. Looking at It Saved Them.」** — and stop marking UK-G3/all-gates PASS while red-team says REVISE.  
2. For this **short-only** asset: drop the **YouTube (Long-form 16:9)** section or mark it **N/A**; never paste **`bible shorts`** tags onto a long upload.  
3. Differentiate long-form copy if you keep that slot later (summary + **`#Shorts`/`#BibleShorts` only on Short**); optionally add **`john 3:14`** / **`lifted up`** tags for honest SEO on the bronze-serpent → Christ thread.
