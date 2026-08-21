# Swirls of Life — the whole Bible in living ink

JesusInTheBible · series design · 2026-08-20, revised 2026-08-21 · hand to producer

The plan for an ongoing long + short-form series in the validated storyboard-page format: a new series entry, a 15-episode starter slate, one concrete OT→NT ink arc, and the next six builds in order.

> **REVISED 2026-08-21** after a real 5/5-reviewer panel quorum (the 2026-08-20 run was DEGRADED, 2/5 — cursor and gemini both died on a headless "Workspace Trust" prompt, fixed same day). Full panel:
> `poc_living_water_ink_style_test/test_the_cross/_independent_review/20260821-085307/INDEX.md`. Changes made in response, and one finding checked and dismissed, are marked inline below with **[FIX]** / **[CHECKED]**. One finding is doctrine-adjacent and is flagged **[OPEN — NEEDS YOUR CALL]** rather than resolved unilaterally, per this project's own non-negotiable "sound doctrine, proven both ways" rule.

## 1. The framing decision: its own series

**Recommendation — decided, not left open:** Swirls of Life becomes its own `series.json` entry — a curated anthology that pulls the best-fit moments from across the whole catalog. It is not just a visual treatment sprayed over existing episodes.

**Why a series, not a treatment:**
- **The ink is a language viewers must learn.** The swirl dose (Stage 0→3) and DEAD INK (Stain, Fray) only carry meaning if a viewer sees them recur, episode after episode, under one recognizable brand. A treatment scattered across five series never teaches its own grammar.
- **The cross-episode devices need controlled ordering.** The OT→NT crossing arcs (section 3) and the season-long "dried rings" payoff are series-level machinery. They are impossible if episodes ship un-sequenced under different brands.
- **The format shapes the narration, not just the picture.** Dialogue-rich, multi-voice, page-based hooks need their own `hook_pattern` / `cta_pattern` / `guardrails` — the exact fields a series entry exists to feed the text engine.
- **The catalog has a real gap.** The Hem — validated TODAY — lives in no series. Talitha Cumi (Jairus) doesn't exist either. The new entry is their natural home.

**[FIX 2026-08-21] Who this series is for, and what it's trying to achieve** — decided after direct discussion with the user, filling a real gap (checked: no series in this catalog has ever stated this at the series level, only per-episode via `constitution.md`'s G8 "name the one real person" rule):

- **Series-level audience (new for this project, deliberate):** Swirls of Life is for the viewer who has quietly decided one specific thing about themselves disqualifies them from something — a failure, a status, a fear that won't quiet down — and who has stopped expecting that to change gradually. Per episode, the G8 rule still applies exactly as everywhere else (every Stain episode's "one real person" is whoever's carrying that episode's specific shame/uncleanness; every Fray episode's is whoever's specific fear/doubt it names) — DEAD INK effectively hands that per-episode targeting to you for free, since the motif IS the diagnosis. What's new at the SERIES level: because the ink is a language learned across episodes, a repeat viewer gets a second layer a first-time viewer doesn't — once you've seen the Stain dry once, you start recognizing it, and the recognition becomes an invitation to watch for it in your own story. A single episode must still work completely alone (never depend on prior viewing to land — see section 3's fix on the season arc); the series identity is a bonus for whoever stays, not a requirement for whoever doesn't.
- **The takeaway (per constitution.md G8: a CHANGE, never a fact):** the plan's own closing line already says it better than a new one would — **"the cut is the miracle — everything else is dosage."** Per episode: whatever you're carrying has a name, and it doesn't fade — it leaves, all at once, the moment Jesus is present, never through gradual effort. Series-level: this isn't new — the whole Bible was already pointing here (the OT→NT crossing arc, section 3).
- **What we're trying to achieve:** grace-anchored change, not information (project-wide rule, not special to this series) — and, per `PRODUCTION_PLAN.md`'s own explicit warning against building "a dedicated long per short... ~$2k+ of compilations nobody clicks," this series stays inside the project's existing flagship-long model: shorts are the first-class product, the 2 longs are flagship anchors that genuinely back a cluster of shorts (the Isaiah 53 long pays off the season's "dried rings," Passover anchors the OT-typology cluster) — not a 1:1 tax. No change needed to section 2's slate ratio; it already fits this shape.

**Dual-home policy** (answers the honest objection): most picks overlap an existing series. That's fine — the swirls entry lists its curated slate, and each `theme` string names the source series. A swirls rendition and a Baroque-oil rendition are different products for different surfaces. Rule: never produce the same episode in two styles at the same time.

**[FIX] Four of the 15 picks aren't "new" — they're REMAKES of already-shipped pieces.** The 2026-08-20 draft called eps 10/11/12/15 "new to the catalog." They aren't — checked against the real narration folder and `_website/manifest.yaml`:
- Ep 10 The Father Who Ran = `09 The Father Who Ran` (locked; manifest slug `the-father-who-ran`, already shipped).
- Ep 11 Look and Live = `42_God_Hung_Up_a_Snake` (locked, full `v1/visual/` done — images already paid for) **and** a separately-produced living-sketchbook short (manifest slug `bronze-serpent-01-look-and-live`).
- Ep 12 Ye Must Be Born Again = `47_Lifted_Up_in_Shame,_Lifted_Up_in_Glory` (manifest slug `bronze-serpent-03-son-of-man-lifted-up`).
- Ep 15 With His Stripes = `30 Smitten of God` (manifest slug `smitten-of-god`, has a rendered `narration.mp3`).

Checked the dual-home rule's actual trigger ("at the same time"): all four originals are already in `_website/manifest.yaml` as shipped/catalogued, not mid-pipeline — so a swirls remake doesn't collide with active production. But this is a REMAKE, and the plan must say so per episode (not "new"), and decide per episode whether to reuse the locked KJV thread/script (cheaper — skips the narration-tournament spend) or write fresh for the new dialogue-native page format. **Decision made here:** write fresh narration for all four — the swirls format's own `hook_pattern`/`cta_pattern`/multi-voice-page needs (section 1, above) don't fit a script written for Baroque long-form or living-sketchbook pacing — but reuse the verse spine / thread choice already locked, skipping Stage-0 thread discovery. This still costs the full narration-tournament + panel spend (~$5-6/episode), it just isn't starting from zero on which verses to use. Table and JSON entry below updated to say REMAKE, not new.

### Paste-ready series.json entry

Strict schema — `pipeline/series.py` reads only these keys, so it drops in clean. Motif + source-series notes ride in the `theme` strings.

```json
{
  "id": "swirls-of-life",
  "name": "Swirls of Life",
  "brand": "Either",
  "concept": "The whole Bible, old to new, told as found pages of hand-drawn animation development art. A blue-and-gold living ink motif marks the gospel entering each scene (dose Stage 0 absent -> Stage 3 diffused); its counterpart DEAD INK falls as the life rises -- the Stain (sin/guilt/uncleanness soaked into the paper itself) and the Fray (fear/doubt breaking a figure's own linework). Dialogue-rich, character-driven, one person's page at a time; every arc crosses at Jesus.",
  "hook_pattern": "The page shows the ache before a word lands (a stain in the paper / a line that will not hold still) -> Jesus enters the page -> the ink crosses",
  "cta_pattern": "Land on the diffused page -- the life no longer tied to one figure -- and invite the viewer to the Jesus who turns the page. Grace only; the hard cut IS the miracle (Mark 5:29, 'straightway').",
  "guardrails": "The ink grammar illustrates, never teaches on its own: the swirl signals the gospel's presence in the scene; it is not a substance that heals and is never named in the narration. Evil is damage, not a rival power -- the Stain and the Fray never move, never fight, never take living form, and are dispelled ONLY at hard cuts between pages, never within a clip. Stain has TWO distinct sub-cases, never conflated: (a) moral sin/guilt (Isaiah 1:18; Psalm 51:7) -- reserved for episodes the text itself frames as sin/debt/forgiveness (the paralytic Mark 2:5, the adulterous woman John 8:11, the prodigal Luke 15, Peter's denial John 21). (b) ceremonial/Levitical uncleanness-as-barrier (Leviticus 15) -- reserved for episodes the text frames as a barrier crossed, NEVER as personal guilt; narration and captions must never imply the person sinned or is guilty (The Hem, Mark 5:25-34, is the flagship case: her healing is tied to faith, Mark 5:34, not forgiveness -- the Stain there means 'the barrier the Law could not cross,' reversed at Jesus's touch: normally touching an unclean person made YOU unclean, here holiness flows outward instead). Fray = fear/doubt only (James 1:6; Matthew 14:31). Never assign either Stain sub-case to suffering or illness the text frames as neither sin nor ceremonial uncleanness (John 9:3 -- Bartimaeus stays motif-free), and never mark Christ with either motif -- the single sanctioned exception is the Isaiah 53 substitution episode (Isaiah 53:6; 1 Peter 2:24; 2 Corinthians 5:21), which requires full independent panel sign-off on that page. OT-type episodes cap the swirl at Stage 1-2; Stage 3 diffusion is reserved for pages where fulfilment in Christ is on-page (Hebrews 10:1). A motif placement must read on watch with the narration muted -- an indirect placement that needs prose to explain it gets redesigned (the Thomas F01 lesson). KJV verbatim in baked captions, contiguous fragments only, 2-4 words per handwrite line. Multi-voice whenever the scene has speakers.",
  "episodes": [
    { "title": "The Well", "primary_ref": "John 4:14",
      "refs": ["John 4:6-30"],
      "theme": "Living water -- SHIPPED pilot (northstar_shortform, both ratios); swirl-only. Shares Encounters 'The woman at the well'." },
    { "title": "The Hem", "primary_ref": "Mark 5:28",
      "refs": ["Mark 5:25-34"],
      "theme": "STAIN, ceremonial-uncleanness sub-case (Leviticus 15) -- the barrier the Law could not cross, dried at the touch (Mark 5:34, faith not forgiveness; never framed as her guilt). Normally touching an unclean person made YOU unclean -- here holiness flows outward instead. Core 2 pages VALIDATED 2026-08-20; expand to a full short. New to the catalog." },
    { "title": "My Lord and My God", "primary_ref": "John 20:28",
      "refs": ["John 20:24-29"],
      "theme": "FRAY (doubt) steadied at the cut where Jesus appears -- F01 validated, F02 pending. Shares Encounters 'Thomas after the resurrection'." },
    { "title": "Peace Be Still", "primary_ref": "Mark 4:39",
      "refs": ["Mark 4:35-41", "Psalm 107:29"],
      "theme": "FRAY on the disciples (Mark 4:40), never on Christ -- storm page F06 validated. Shares Miracles-as-Signs 'Calming the storm'; same event as QJA 'Why Are You Afraid' (Matthew's account)." },
    { "title": "Talitha Cumi", "primary_ref": "Mark 5:36",
      "refs": ["Mark 5:21-24", "Mark 5:35-43"],
      "theme": "FRAY on Jairus ('Be not afraid, only believe') -- Mark's own sandwich interleaves this with The Hem: shared street, shared crowd, cross-episode continuity for free. New to the catalog." },
    { "title": "Wherefore Didst Thou Doubt", "primary_ref": "Matthew 14:31",
      "refs": ["Matthew 14:25-33"],
      "theme": "FRAY flagship -- the motif's own proof text. Peter's line frays FR1->FR3 as he sees the wind; the fray dies at the caught hand. Shares Miracles-as-Signs 'Walking on water' (Matthew's account for Peter's dialogue)." },
    { "title": "Lovest Thou Me", "primary_ref": "John 21:17",
      "refs": ["John 21:15-17", "John 18:18", "John 21:9"],
      "theme": "STAIN (the denial's guilt) drying across three questions -- enact all three, never compress (QJA guardrail); the charcoal-fire echo (John 18:18 / 21:9) anchors the stain. Shares Encounters 'Peter restored' + QJA 'Do You Love Me'." },
    { "title": "Thy Sins Be Forgiven", "primary_ref": "Mark 2:5",
      "refs": ["Mark 2:1-12"],
      "theme": "STAIN dries at forgiveness BEFORE the man walks -- the text's own order; the scribes' inner reasoning gets its own voice. Shares Miracles-as-Signs 'Healing the paralytic with forgiveness'." },
    { "title": "Neither Do I Condemn Thee", "primary_ref": "John 8:11",
      "refs": ["John 8:2-11"],
      "theme": "STAIN on her -- and on every accuser, leaving eldest first (John 8:9). Jesus writes on the ground in an ink-and-paper style; gesture only, NEVER render what he wrote (Scripture doesn't say). Shares Encounters 'The woman caught in adultery'." },
    { "title": "The Father Who Ran", "primary_ref": "Luke 15:20",
      "refs": ["Luke 15:11-32"],
      "theme": "REMAKE (already shipped as '09 The Father Who Ran', locked, manifest slug the-father-who-ran) -- fresh dialogue-native narration for the swirls format, same verse spine. STAIN from the far country, its home-side edge ALREADY dried while he is yet a great way off (the D2 turning variant -- grace moves first). Multi-voice: narrator -> Jesus -> narrator -> son." },
    { "title": "Look and Live", "primary_ref": "Numbers 21:8",
      "refs": ["Numbers 21:4-9", "John 3:14-15"],
      "theme": "REMAKE (already shipped twice: '42_God_Hung_Up_a_Snake' Baroque long-form AND a living-sketchbook short, manifest slug bronze-serpent-01-look-and-live) -- fresh narration for the swirls format. OT half of the serpent arc. STAIN on the camp ('we have sinned', Num 21:7) dries per looker; swirl CAPPED at Stage 1 -- the type is not the fulfilment." },
    { "title": "Ye Must Be Born Again", "primary_ref": "John 3:16",
      "refs": ["John 3:1-16"],
      "theme": "REMAKE (already shipped as '47_Lifted_Up_in_Shame,_Lifted_Up_in_Glory', manifest slug bronze-serpent-03-son-of-man-lifted-up) -- fresh narration for the swirls format. NT half of the serpent arc -- Jesus himself quotes Numbers 21 (John 3:14); the Stage 3 the OT episode withheld is released at John 3:16, the anchor verse. FRAY FR1 on Nicodemus ('How can these things be?')." },
    { "title": "I AM Hath Sent Me", "primary_ref": "Exodus 3:14",
      "refs": ["Exodus 3:11-14", "Exodus 4:1-13", "John 8:58"],
      "theme": "FRAY on Moses (his objections, Exodus 3-4) against the steady bush that burns unconsumed; lands on John 8:58 'Before Abraham was, I am'. Shares Jesus-in-OT 'The Great I AM'." },
    { "title": "When I See the Blood", "primary_ref": "Exodus 12:13",
      "refs": ["Exodus 12:3-13", "John 1:29", "1 Corinthians 5:7"],
      "theme": "LONG-FORM (7 movements, 16:9). STAIN on every doorstep, Israelite and Egyptian alike -- the blood makes the difference, not the merit; Stage 3 released only at 'Behold the Lamb of God'. Shares Types & Shadows 'Passover Lamb' + Jesus-in-OT 'The Lamb of God'." },
    { "title": "With His Stripes", "primary_ref": "Isaiah 53:5",
      "refs": ["Isaiah 53:3-6", "1 Peter 2:24", "2 Corinthians 5:21"],
      "theme": "REMAKE (already shipped as '30 Smitten of God', manifest slug smitten-of-god, has a rendered narration.mp3) -- fresh narration for the swirls format. LONG-FORM season finale. The STAIN TRANSFER: the season's dried rings laid on Him -- the ONE sanctioned page where a motif touches Christ; full panel sign-off required on that page." }
  ]
}
```

**Locked rules this plan is built under** (from CLAUDE.md — binding, restated so the producer sees them):
- Sound doctrine, proven both ways — my own red-team AND the 5-CLI panel, never one alone.
- The whole canon, through Jesus — every episode lands on Him. The Stage-cap law (section 3) makes this visible in the ink itself.
- KJV verbatim; grace-anchored conviction, no fear/gain framing; multi-voice when the scene has speakers.
- This slate design is a SIGNIFICANT plan — run `independent_review.py "<plan.md>" --type plan` on it before committing series.json (**[FIX]** the 2026-08-20 draft omitted the required artifact-path argument here). `/cost` gate before any spend.

## 2. The starter slate — 15 episodes, old to new

Ten dialogue-native NT picks (Encounters / Miracles-as-Signs / Questions-Jesus-Asked), four already carrying today's validated test work, plus four OT entries so the series genuinely reads old-to-new. Every motif call is textually grounded — where the text doesn't call the affliction sin or fear, the episode gets *no* motif on purpose (John 9:3 discipline; Bartimaeus is the bench example of a story we'd run motif-free).

**[FIX] Status column split into three axes** (2026-08-20 draft collapsed these into one "validated" word — the panel caught this twice, independently, on Thomas F01 and Peace Be Still F06): **Art** = the still/page render style is proven. **Motif** = THIS episode's specific dead-ink placement is proven on watch. **Narration** = the locked KJV script exists. A page can be art-proven without being motif-proven (Thomas F01: the page renders fine, but the swirl placement didn't read — see the OPEN flag below).

| # | Episode | Text | Source series | Form | Dead ink | Art | Motif | Narration | Why it earns its place |
|---|---|---|---|---|---|---|---|---|---|
| 01 | The Well | John 4:6-30 | Encounters | SHORT | none — swirl only | proven | proven | locked (POC) | The pilot. 8 pages, both ratios, finished 69s film with 4-voice dialogue. Note: this is a POC cut (`poc_living_water_ink_style_test/`), not yet in the real catalog/series.json. |
| 02 | The Hem | Mark 5:25-34 | — not yet catalogued | SHORT | Stain | proven (2 pages) | proven (2 pages) | not written | The Stain's home story: 12 years unclean, dried "straightway" at the touch. Both pages passed on real playback — but that's 2 of ~6-10 pages a full episode needs. |
| 03 | My Lord and My God | John 20:24-29 | Encounters | SHORT | Fray | proven (F01) | **OPEN** — F01 placement didn't read, redesign is build 1 | not written | The Fray's home story. Doubt drawn as Thomas's own broken line against the disciples' steady ink; steadied at "then came Jesus." |
| 04 | Peace Be Still | Mark 4:35-41 | Miracles-as-Signs · QJA (Why Are You Afraid) | SHORT | Fray | proven (F06, storm/water only) | untested (Fray on disciples is build 3) | not written | "Why are ye so fearful?" (Mark 4:40) — Fray on every disciple, Christ's line dead steady. The storm page already survived the hardest ink-vs-water test. |
| 05 | Talitha Cumi | Mark 5:21-24, 35-43 | — not yet catalogued | SHORT | Fray | untested | untested | not written | Mark himself interleaves Jairus with The Hem. "Be not afraid, only believe" (5:36) is a Fray text verbatim — and the two episodes share street, crowd, and refs (continuity NOT free — see the risk table). |
| 06 | Wherefore Didst Thou Doubt | Matthew 14:25-33 | Miracles-as-Signs (Walking on water) | SHORT | Fray | untested | untested | not written | Matt 14:31 is the Fray's own proof text. Peter's line steady while he looks at Jesus, fraying FR1→FR3 as he sees the wind, dead at the caught hand. |
| 07 | Lovest Thou Me | John 21:15-17 | Encounters · QJA (Do You Love Me) | SHORT | Stain | untested | untested | not written | Three questions = three pages (the QJA guardrail: the repetition IS the restoration). The stain sits by the charcoal fire — the same fire he denied beside (John 18:18 / 21:9). |
| 08 | Thy Sins Be Forgiven | Mark 2:1-12 | Miracles-as-Signs | SHORT | Stain | untested | untested | not written | The text puts forgiveness before walking — so the stain dries one page BEFORE he stands. Two cuts, two miracles, exactly the passage's own order. Scribes' inner speech gets a voice. |
| 09 | Neither Do I Condemn Thee | John 8:2-11 | Encounters | SHORT | Stain | untested | untested | not written | A story about writing, in a style made of ink and paper. Stains on her AND on the accusers who leave eldest first (8:9). Never render what He wrote — gesture only. |
| 10 | The Father Who Ran | Luke 15:11-32 | Parables | SHORT | Stain | untested | untested | **REMAKE** — locked script exists (`09 The Father Who Ran`), fresh write planned | The validated D2 "turning" trick was built for this: the stain's home-side edge already dried while he is "yet a great way off." Grace moves first — in the geometry itself. |
| 11 | Look and Live | Numbers 21:4-9 | Types & Shadows (Bronze Serpent) | SHORT | Stain | untested | untested | **REMAKE** — locked script + full v1/visual already exist (`42_God_Hung_Up_a_Snake`) + a second shipped living-sketchbook short, fresh write planned | OT half of the serpent arc. "We have sinned" (21:7) grounds the camp-wide stain; the swirl is CAPPED at Stage 1 — the shadow is not the substance. |
| 12 | Ye Must Be Born Again | John 3:1-16 | Encounters (Nicodemus) | SHORT | Fray (light) | untested | untested | **REMAKE** — locked script exists (`47_Lifted_Up_in_Shame...`), fresh write planned | NT half of the arc — Jesus himself cites the serpent (3:14). The Stage 3 the OT episode withheld releases at John 3:16 (now the `primary_ref` — was miskeyed to 3:14). Nicodemus's careful night-questions = FR1. |
| 13 | I AM Hath Sent Me | Exodus 3:11-4:13 | Jesus-in-OT (The Great I AM) | SHORT | Fray | untested | untested | not written | Dialogue-native OT: Moses's objections (Fray) against a bush that burns steady and unconsumed. Lands on John 8:58 — the name Jesus takes. |
| 14 | When I See the Blood | Exodus 12:3-13 | Types & Shadows · Jesus-in-OT | LONG | Stain | untested | untested | not written | First long-form: a stain on EVERY doorstep, Israel's too — the blood makes the difference, not the merit. Stage 3 only at "Behold the Lamb" (John 1:29). |
| 15 | With His Stripes | Isaiah 53:3-6 | Jesus-in-OT (Suffering Servant) | LONG | Stain — the transfer | untested | untested | **REMAKE** — locked script + rendered narration.mp3 already exist (`30 Smitten of God`), fresh write planned | Season finale. The one sanctioned page where the Stain touches Christ: "the LORD hath laid on him the iniquity of us all." Every dried ring of the season, paid for here. |

**Motif balance:** 7 Stain · 6 Fray · 1 swirl-only · 1 transfer. **Tested ground, honestly:** only eps 1-4 have any rendered pixels at all, and of those only ep 1 (The Well) is a complete episode — the rest are 1-2 pages each. Zero of the 15 have a written narration script yet; four (10/11/12/15) have one already locked *for a different style* that a fresh swirls script would draw its verse choice from, not its text. No motif is ever decoration — each one cites its verse.

## 3. The OT→NT crossing arc — worked example

The DEAD INK system's crossing-arcs idea (swirl rising as stain falls, crossing at the gospel turn) scaled from two pages of one episode to **two episodes of one season**. The serpent pair proves it concretely:

**Plant — ep 11 · Look and Live · Numbers 21:4-9 — the type, deliberately unresolved**
- Camp pages: Stain D3 — the people's own words, "we have sinned" (21:7).
- The pole page: a bitten man looks up; at the page cut, *his* stain dries to the pale ring.
- Final page: swirl held at Stage 1 — one thread rising from the pole. Closing caption: "shall live" (21:8, verbatim fragment).
- The episode ends visibly incomplete in the ink grammar. A viewer who has learned the language *sees* that Stage 3 never came.
- (capped at Stage 1 — shadow, not substance)

→ John 3:14 makes the link — Jesus himself →

**Payoff — ep 12 · Ye Must Be Born Again · John 3:1-16 — the fulfilment releases the dose**
- Opens Stage 0 in the night room; Nicodemus's questions carry Fray FR1.
- The John 3:14 page rhymes the pole page's composition — same diagonal, same three-panel echo (pole / bitten man / the look).
- At John 3:16, the dose goes Stage 3 diffused — the release the OT episode withheld. The FR1 steadies at the same cut.
- (Stage 3 — fulfilment on-page)

**The Stage-cap law (new, series-level, gate-able):** OT-type episodes cap the swirl at Stage 1-2. Stage 3 diffusion is reserved for pages where fulfilment in Christ is on-page. This is the project's own spine — "the whole Bible, through Jesus" — made visible in the ink system itself, and it's doctrinally honest: the law had "a shadow of good things to come, and not the very image" (Hebrews 10:1). **[FIX] It is NOT yet deterministic** — the 2026-08-20 draft claimed "a $0 lint can check every OT page's dosage line before a credit is spent" as if it existed. It doesn't: `series.json`'s schema has no dosage/motif/status field (`theme` is free text) and no such linter is in the repo — three reviewers caught this independently. Fix: build the lint (a `panel_variety_lint.py`-style deterministic checker reading a real per-page dosage field, not the `theme` string) as its own step BEFORE build 5 claims to test it — added to the build sequence below.

**The season-level second arc — [FIX] scope narrowed.** The 2026-08-20 draft assumed viewers watch episodes 2, 7, 8, 9, 10, 11 in order before the Isaiah 53 finale pays off their "dried rings." Gemini's review is right to push back: YouTube Shorts are algorithmic and non-sequential, so a payoff that only lands for a viewer who happened to watch six specific episodes in order is mostly wasted on the actual audience. **Revised scope:** each episode's own dead-ink arc must read and land completely on its own (already true — every episode has its own Stage 0→dose→resolution). The season-long "rings" thread becomes a bonus layer for repeat/binge viewers and for the finale's own internal narration (which can reference "the ones who came before" in its own text, a self-contained callback, not a viewing-order dependency) — not a structural requirement the finale's meaning depends on. Same law applies to the Passover long (ep 14): Exodus movements cap at Stage 1; "Behold the Lamb of God" releases Stage 3 — that arc is fine as-is since it's self-contained within one long-form's 7 movements, not cross-episode.

## 4. Long-form vs short-form

**The ratio:** Season one: 13 shorts : 2 longs (~85/15). Steady state: about one long per 4-5 shorts, each long anchoring a cluster of shorts that share its texts. Shorts are the audience engine and the validated ground; longs are the depth anchor — and everything long-form is still untested in this style, so it earns its slots slowly.

**Short (60s) — validated:**
- 6-10 pages at ~7-9s per page (The Well: 8 pages / 69s).
- 9:16 primary; every shot gets a real AI clip by default.
- Swirl dose: the 0→3 arc runs once, page to page.
- DEAD INK: one motif, one descending arc, resolved at one cut.
- **[FIX] Cost: budget $20-46/episode, not $12-18.** The 2026-08-20 draft's $12-18 was a clean-run estimate with no regen buffer built in and no narration-stage Opus cost. Real comparables from the ledger: a regen-heavy living-sketchbook short (13 stills + 13 clips + retries) landed ~$46-class; The Well POC alone logged ~$33 in one day of iteration (not a clean single pass, but real cost of getting one short right). Add ~$5-6/episode for the narration tournament + panel + red-team (not included in either the old or new range above — say so explicitly per episode when actually spending). Treat $20-46 as the honest band until 3-4 episodes ship clean and give a tighter number.

**Long (6-8 min) — untested, designed:**
- ~20-26 spreads, NOT 45 — the page changes function: longer holds (~15-25s) with Focal Tour as a primary treatment on non-hero spreads (the Step-0 table already allows this for long-form). **[CHECKED]** Gemini's review flagged this as infeasible against `veo3_1_lite`'s 8s hard duration cap — checked against `.claude/skills/focal-tour/SKILL.md`: Focal Tour is $0 PIL+ffmpeg compositing over a still, no AI video generation at all, and its own example already runs a 16.62s duration. The 15-25s holds are real and buildable; the finding doesn't apply here.
- 16:9 (project rule) — inherits the open 16:9 risks (crowd inflation, aspect-dependent prompt reads, second-ratio ref-chaining).
- Dose paced per 7-movement envelope, not per page: sub-waves inside movements, whole movements at absence, overall arc still 0→3.
- DEAD INK works at length *if* dosed per movement — target: no more than half the movements carry a motif, so each change still reads as an event. D3→D2→D1 gets real room instead of adjacent pages.
- Real clips on hero spreads only (~1/3); veo-first tiering.
- **[FIX] Cost: budget $50-95/episode, not $22-30.** The 2026-08-20 draft's $22-30 doesn't match any real long-form in this project — ledger totals for comparable inked/Baroque longs: Passover ~$45+, Bronze Serpent ~$90+. Swirls storyboard-pages are a different, lighter-weight format (fewer full-render stills, more Focal-Tour-only spreads per section 4's own economy above), so the true number likely sits below Bronze Serpent's ~$90 — but there is zero swirls long-form ledger evidence yet, so $22-30 is not defensible as a stated estimate. Use $50-95 (roughly Passover-to-Bronze-Serpent bracket) until build 6 gives a real number, and get explicit `/cost` sign-off before spending regardless of which end it lands on.

**Does DEAD INK even work long?** Yes — arguably better, because the descending doses get room to breathe — but only with the per-movement rule above. The failure mode at length is motif fatigue: a stain on every spread stops meaning anything. The fix is the same discipline the swirl already has: absence is a dose. That's why ep 14 (Passover) is the long-form test bed before ep 15 (Isaiah 53) is allowed to carry the season's heaviest page.

## 5. The next six builds, in order

Sequenced so each build adds a new risk on top of proven ground — not all fifteen at once. **[FIX]** the 2026-08-20 draft called this "exactly one new risk" per build; three reviewers pointed out builds 5 and 6 each actually bundle several (OT-first + crowd-scale Stain + shared compositions + Stage-cap test, in one case; first-long + 16:9-at-scale + Focal-Tour-economy + DEAD-INK-at-length, in the other). Left bundled below — splitting into ten-plus micro-builds isn't worth the overhead — but named honestly instead of claimed as one-at-a-time.

**[FIX] Pipeline-integration decision (the panel's single biggest finding, 4 of 5 reviewers, independently):** none of today's validated pages go through the real production pipeline (`cli_visual.py`'s SP-G1-G9 gates, `cli_assemble.py`'s AS-G6/G7 hero-bookend gates) — every render lives as a one-off script in `poc_living_water_ink_style_test/test_the_cross/`. A swirls "page" (baked title, frame number, 3-panel row, one big illustration) is structurally different from a `scene_plan.json` scene, so this isn't a small adapter, it's real unscoped engineering. **Decision:** builds 1-6 below continue as hand-rolled scripts, same as today — do NOT assume `/narrate`/`/voice`/`cli_visual.py`/`cli_assemble.py` "just work" on pages (the 2026-08-20 draft's build 2 implied this and was wrong). Formally wiring swirls pages into the real gated pipeline is separate future engineering, scoped and costed on its own if/when the format proves out past build 6 — not bundled into this six-build spend.

1. **Finish Thomas — F02 + the swirl-legibility fix.** Render F02 ("My Lord and my God", already designed in `render_the_thomas.py`), and redesign F01's swirl placement — the user flagged it as "missing what the swirls are meant to be." New working rule to test: the dose anchors to the thing the narration names in that beat, never to an indirect idea that needs prose to explain. *Proves: the Fray between-pages cut + closes today's one open design flag.* ~$2-4
2. **The Hem — expand to the first full series episode.** Wrap ~4 new pages around the validated F04/F05 pair (the 12 years, the press of crowd, "Who touched my clothes?", the landing), write and lock the narration (hand-rolled scripts per the decision above, not a slash-command pipeline), then voice + assemble + score + caption using the existing `northstar_shortform/`-style assemble script as the template. This is the "ship one complete episode of the new series" milestone, on the most-tested ground we have. *Proves: full-episode Stain arc, hand-rolled end-to-end.* ~$20-30 (art/audio only, + ~$5-6 narration). **[RESOLVED 2026-08-21, user confirmed]** grok's review flagged a possible guardrail conflict: Stain = sin/guilt, but The Hem's 12-year hemorrhage is ritual *uncleanness* (Leviticus 15), not stated moral guilt. Resolved, not dropped: the `guardrails` string (section 1) now names ceremonial uncleanness as its own Stain sub-case, distinct from moral sin, with a hard rule that narration/captions never imply personal guilt for it — The Hem's own `theme` string (section 1) carries the reframed language ("the barrier the Law could not cross," healing tied to faith per Mark 5:34, not forgiveness). This build proceeds under that language.
3. **Peace Be Still — full episode, Fray added.** F06 already survived the hardest ink-vs-water test. Build the full short and add the Fray to the disciples — first test of the Fray on multiple figures at once (Thomas was a single figure), with Christ's line explicitly steady. *Proves: multi-figure Fray + second complete episode.* ~$20-30 (+ ~$5-6 narration)
4. **Wherefore Didst Thou Doubt — the Fray flagship.** Fresh ground, hardest water composition yet (a figure ON the sea — LAW 0.2/0.3 stress, under the Storm's validated triple lock: green-black sea, dose in the sky, no blue in any wave). Deliberately tests the one untested Fray direction: the fray worsening FR1→FR3 across pages before it dies at the caught hand. *Proves: fray escalation between pages + water discipline at its limit.* ~$20-30 (+ ~$5-6 narration)
5. **Build the Stage-cap lint, then Look and Live + Ye Must Be Born Again back to back.** **[FIX]** added the lint-build itself as a real prerequisite (see section 3's fix above) — a deterministic checker reading a real per-page dosage field, not the free-text `theme` string, modeled on `panel_variety_lint.py`'s pattern. Then one design pass, two REMAKE episodes (fresh narration, reused verse spine — see section 1), shared compositions (the pole page and its John 3:16 rhyme). First OT episode of the series, first crowd-scale Stain (the camp), and the first real test of the Stage-cap law with an actual lint enforcing it. *Proves: the lint exists + the cross-episode crossing arc + OT entry point.* ~$45-65 for the pair (+ ~$10-12 narration, two REMAKE episodes)
6. **When I See the Blood — the first long-form (16:9).** Only after five shorts have hardened the grammar. Tests everything section 4 designed: per-movement dose pacing, Focal-Tour-primary economy, DEAD INK at length, and 16:9 at scale with the known aspect-ratio gotchas. Hand-rolled long-form script (per the pipeline decision above) + the full panel discipline. *Proves: long-form viability — the gate for ep 15's finale.* ~$50-95

The Isaiah 53 finale deliberately sits after all of this — it needs the season's dried rings to exist before it can pay for them, and its one sanctioned Stain-touches-Christ page carries the heaviest doctrinal review of the whole season. It is also a REMAKE (section 1) — confirm reuse-vs-fresh-write before scoping its own build.

## 6. Open risks, honestly named

| Risk | Note |
|---|---|
| **[FIX] No production pipeline for this format** | Biggest finding, 4/5 reviewers independently. Every validated render is a hand-rolled script under `poc_living_water_ink_style_test/test_the_cross/` — none of it goes through `cli_visual.py`/`cli_assemble.py`'s real gates. Builds 1-6 explicitly stay hand-rolled (section 5); formal wiring is separate future engineering, not assumed spend. |
| **[FIX] Catalog collisions** | 4 of 15 slate picks (eps 10/11/12/15) already exist as shipped pieces in other styles, not "new" as the 2026-08-20 draft claimed. Resolved in section 1/2: relabeled REMAKE, fresh narration write decided, dual-home rule confirmed non-conflicting (originals already shipped, not concurrently active) — but the rule itself has no programmatic check (see below). |
| **[RESOLVED] Mark 5 Stain vs. the John 9:3 guardrail** | The Hem assigns Stain to ritual uncleanness, not text-stated sin. Resolved 2026-08-21 (user confirmed): the guardrail now defines ceremonial-uncleanness as its own Stain sub-case, never framed as guilt — see section 1's `guardrails` string and build 2. |
| **[FIX] Dual-home rule is manual-only** | Gemini's review: nothing in `pipeline/orchestrator.py` or `cli.py` programmatically blocks producing the same episode twice across series. No fix built this pass (real engineering) — mitigation for now: check the catalog by hand (as done in section 1) before starting any REMAKE build, every time, not just once at plan-commit. |
| **[FIX] Multi-ref loss in the pipeline** | Two reviewers independently found `pipeline/handoff.py` writes only `title` + `primary_ref` into `narration.creation.json` — `refs` beyond the primary verse can silently drop downstream. Affects any multi-passage episode here (Talitha Cumi, I AM Hath Sent Me, When I See the Blood, the serpent pair). Not fixed this pass; whoever builds those episodes needs to verify the wider refs actually reach the scene-plan stage, or hand-thread them. |
| Swirl legibility | Flagged today on Thomas F01 — an indirect symbolic placement didn't read on watch. Addressed first in build 1; until then, no placement whose meaning needs prose. |
| Fray second page | F02 designed, never rendered. The Fray's between-pages resolution is unproven until build 1 completes. |
| Fray escalation | FR1→FR3 worsening across pages has never been tested in either direction beyond a single dose. Build 4 tests it. |
| 16:9 at scale | Aspect-dependent prompt reads (the Golgotha skull), crowd inflation, second-ratio ref-chaining — all real, all only partly mitigated. Long-form is 16:9, so build 6 carries this deliberately. |
| Speech-bubble fix | The no-bubble clause has 2 clean data points, not proof. Keep it in every template; keep checking. |
| Long-form | Entirely untested in this style. That's why it's build 6, not build 2 — and why the finale waits behind it. |
| Talitha/Hem "shared continuity for free" | **[FIX]** cursor's review: shared street/crowd/refs between Talitha Cumi and The Hem isn't free — it's real ref-chaining identity-lock work (per the swirls skill's own per-episode chaining rule) that neither episode's build budgets or sequences. Note it as real cost if/when Talitha Cumi gets built. |
| Governance | This plan itself needs the external panel (`independent_review.py "<plan.md>" --type plan`) before series.json is committed; every episode keeps the standing narration gate, /cost gate, and eyeball-QC-at-1:1 rules. **[FIX]** re-run 2026-08-21 after fixing the `cursor-agent --trust` bug that killed 3/5 reviewers on the first pass — this revision reflects a real 5/5 quorum, all REVISE, findings addressed above. |

---
Swirls of Life · series design pass, 2026-08-20, revised 2026-08-21 after 5/5-quorum panel review · grounded in: constitution.md, series.json, SKILL.md, NORTH_STAR_PROMPT.md, NORTH_STAR_ANIMATION_PROMPT.md, and the validated Hem / Storm / Thomas / Cross test work.

*the cut is the miracle — everything else is dosage*
