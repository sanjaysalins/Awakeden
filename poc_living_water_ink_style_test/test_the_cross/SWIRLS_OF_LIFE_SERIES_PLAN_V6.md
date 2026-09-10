# Swirls of Life — season direction (v6)

JesusInTheBible · series design · 2026-09-08 · supersedes v5 (draft, never
locked) after adversarial panel review

> **How this document was built.** Fable (this project's design model) did
> an independent ideation pass over the season — reassessing the 5 unbuilt
> v4 episodes and proposing new candidates. That became v5, a draft. v5 went
> to `independent_review.py --type plan`, the project's standing 5-CLI
> adversarial panel. **Panel was DEGRADED both runs: only 3 of 5 voices
> answered (cursor, claude, gemini — all independently verdict REVISE; grok
> and codex failed to respond twice in a row, an apparent environment issue,
> not a content problem).** Per this project's own rule, a degraded panel is
> not treated as a lock — but the 3 reviews that landed were unusually
> specific and cross-verified real errors against actual repo files, not
> just opinions. **I re-checked every one of their sharpest claims against
> the actual codebase myself before accepting any of them** (grep'd
> `NORTH_STAR_PROMPT.md` for the QUAD-lock rule, confirmed the `.locked`
> file on the Genesis-3 backlog script, confirmed `papermakers-mark`'s real
> pipeline home, checked the KJV cache for the disputed Mark-7 citation,
> hand-counted the shipped episodes for the healing-miracle claim). Every
> fix below is either a self-verified correction or an explicit judgment
> call handed back to the user — never a reviewer's verdict taken on faith.

## The new standing gate — apply to every episode below

Before any episode in this list is finalized (not just narrated — at
candidate-selection time):

1. **Who is this for? Who NEEDS to hear this?** Name ONE real kind of
   person — not "everyone." (Restates the main engine's own constitution
   G8 question #4, pulled forward to backlog-selection time, not just
   narration-draft time — this is a discipline to apply by hand each time,
   not a new automated gate script.)
2. **What is their takeaway?** Not a fact — a CHANGE: one true thing about
   Christ that reorders how they see Him. Information alone fails this.
3. **What is our intention with this episode?** The specific strategic
   reason THIS story earns its place THIS season — a motif the system
   hasn't proven, an OT→NT rhyme, a real gap in what's been covered, a
   named risk worth taking. "It's a good story" is not an answer.

## The dead-ink system (unchanged from v4)

Swirl (Christ's presence, Stage 0→3, OT-capped at 1-2 unless fulfilment is
on-page) · Stain (moral sin/guilt OR ceremonial/Levitical uncleanness, never
a third case) · Fray (fear/doubt ONLY, earned by the text's own vocabulary)
· **QUAD lock**, confirmed verbatim in `.claude/skills/swirls-of-life/
NORTH_STAR_PROMPT.md`: chromatic reservation, **zone separation — "a
stated band of clean paper between them; they never touch"**, form
separation, plus high-tide exclusion (`stainDose + swirlStage <= 4`) ·
swirl-only when forcing a diagnosis would be invention.

### "Wax resist" (hardness/refusal) — UNPROVEN, not adopted, not scheduled on

Fable's review named a real gap: hardness/refusal (the Nazareth crowd's
wrath, the Pharisee's self-trust, Jonah's anger) earns neither Fray
(no fear/doubt vocabulary) nor Stain (no confessed guilt). Proposed idea:
the paper simply doesn't take the swirl where that person stands — a dry
patch amid Stage-3 ink. **Two independent reviewers (cursor, gemini)
flagged this as a real feasibility risk, not just a doctrine question**:
generative image/video models are bad at negative spatial constraints
("swirl everywhere except this outline"), and this project's own history
already includes failed "hold position" attempts on far simpler two-figure
composition asks. **Verdict: do not treat this as load-bearing for any
episode until a single cheap still-image POC proves it renders cleanly.**
Until then, #14 (the one episode that needs it) should plan for the honest
fallback — the hostile crowd rendered with no dead-ink mark at all, letting
the narration alone name their hostility, same as any story this season
that's correctly left un-diagnosed.

## Part 1 — Reassessing the 5 remaining v4 items

### #6 Talitha Cumi (Mark 5:21-24, 35-43) — REDESIGN before build

No reviewer objection to this fix. Problem: the sandwich structure puts two
diagnoses on one page. Jairus is Fray ("Be not afraid, only believe," 5:36
— Jesus's own words). The bleeding woman is Stain/uncleanness — but that
would be a **fifth** ceremonial-uncleanness Stain this season (heifer,
Naaman, Nain, the nine already shipped); that category is proven, a fifth
doesn't earn its place.

- **Fix:** Jairus-POV only. The woman stays undiagnosed on the page — one
  panel, a blur at the hem, camera stays on Jairus's face.
- Who: the one who asked, and it got worse while they waited — watching
  Jesus stop for someone else while their own crisis burns.
- Takeaway: Jesus isn't troubled by "too late." He stopped on purpose, then
  turned to Jairus, not the crowd. *Talitha cumi* — Mark's own preserved
  Aramaic — is the hook.
- Intention: the "too late" person hasn't been named yet this season.

### #9 The Woman at the Border (Mark 7:24-30) — RE-AIM, citation corrected

**Fix applied:** the draft cited "great faith" (Matt 15:28) for a Mark 7
episode — I checked the KJV cache and confirmed Mark's own account does not
contain that phrase; it's Matthew's parallel, a different Gospel. For a
KJV-verbatim series this is a real error, now corrected: the takeaway
below uses Mark's own text instead.

- Problem found (still stands): correctly swirl-only (the daughter's
  affliction is demonic, not Levitical — a Stain would misdiagnose it), but
  "outsider/border" is the season's most over-used person-shape (Sheba,
  Naaman, the Samaritan leper, Simon of Cyrene — plus this one as
  originally framed).
- **Fix — retitle:** *"Yet the Dogs"* or *"The Crumb."* Drop "border" from
  the frame.
- Who: the one who's asked and got what felt like a no or silence, and is
  about to stop asking.
- Takeaway (Mark 7:29-30, corrected): "for this saying go thy way" — Jesus
  answers her ARGUMENT, not just her request. She goes home to find the
  devil already gone. A crumb from Him is a whole deliverance.
- Intention: the only episode where a human presses Jesus in dialogue and
  He visibly yields the exchange — a structural beat the season hasn't
  used.

### #12 Ye Are Not All Clean (John 13:1-30) — STILL THE TOP PICK, but needs a short verification pass first, not zero-overhead

**This is the one real correction that changes what happens next.** v5
called this "GREENLIT, build now, no plan overhead." That was wrong on two
counts, both self-verified:

1. **The QUAD-lock "never touch" rule is real** (confirmed above, quoted
   verbatim from `NORTH_STAR_PROMPT.md`), and foot-washing is literal
   contact. But — checking v4's own text — **this was already answered
   once**: v4 specifies "Jesus's swirl centers on the basin where he washes
   the other disciples; Judas's stain stays local to his own feet, a
   clean-paper band between them, same as any other page." v5 simply
   dropped that sentence when it copied the episode forward. The design
   answer exists; it needs restating and then a real page-by-page
   storyboard check (does the actual wash-Judas's-feet beat, which John
   13:1-11 doesn't exempt him from, stay off-panel or off-frame?) before
   spend, not just before publish.
2. **No `swirls_episode_12_*` folder exists yet**, and v4's own open-risks
   table flagged `pipeline/handoff.py` as writing only `primary_ref` — a
   real risk for John 13:1-30's wide span that v5 never mentioned.

**Fix: keep #12 as the next build, but the first step is a short plan-only
/scene-plan-style pass** (verify the zone-separation storyboard holds
panel-by-panel, confirm the wide ref span survives the handoff pipeline)
**before any paid stills.** This is a design/verification session, not a
redesign — the underlying idea (a Stain that doesn't clear) is still sound
and still the strongest untested motif behaviour available.

- Who: the insider who's been at the table for years, already served,
  already washed, and is quietly already gone.
- Takeaway: Jesus washed the feet of the man He knew would betray Him.
  Grace wasn't withheld — it was refused, sop still in hand. The basin is
  still there.
- Intention: fills the moral-sin Stain gap (of the 5 shipped Stains, 4 are
  ceremonial uncleanness — see the corrected count below — only 1, She
  Loved Much, is moral sin). "Ye are not all clean" is Jesus's own
  clean/unclean vocabulary, moral not ceremonial. `stainDose + swirlStage
  <= 4` caps Judas at dose 1 while the room runs Stage 3 — a small dark dot
  walking out of a page alive with light.
- **Open, not silently decided:** landing on "and it was night" (13:30)
  with no CTA phrase breaks this season's landing-fatigue problem — but the
  main engine's constitution (G8) binds every short to a CTA-to-Jesus
  landing. Swirls has already drifted this direction once (ep 13's
  delayed-swirl closing caption). Worth an explicit call: is Swirls formally
  exempt from the strict CTA-phrase requirement, in favor of its own "the
  cut is the miracle" ethos — or does "and it was night" need a small added
  beat that still points somewhere? Flagging for you to decide, not
  assuming either way.

### #14 This Day Is This Scripture Fulfilled (Luke 4:16-30, long-form) — real, but scope corrected to what's actually buildable

Luke 4:25-27 does genuinely cite the widow of Zarephath (shipped ep 5) and
Naaman (shipped ep 4) by name — that part holds.

**Fix applied:** v5 claimed "the sketchbook turns back to pages 4 and 5...
no other format can do this," implying a literal page-turn compositing
shipped clips. **Checked against what actually shipped**: ep 8's own
callback (`swirls_episode_08_can_any_good_thing/episode.py`) is Jacob's
ladder **redrawn small**, as a pinned storyboard thumbnail — a fresh
illustration referencing the earlier story, not footage of the earlier
episode reused. No swirls pipeline exists for compositing prior episodes'
rendered clips into a new page. **Corrected intention:** use the exact same
proven technique ep 8 already validated — a small redrawn callback panel
citing eps 4 and 5 — not a new, unbuilt page-turn device. Same emotional
payoff, zero new tooling risk.

- Who: the one for whom Jesus is too familiar to be Lord. "Is not this
  Joseph's son?"
- Takeaway: the most explicit "this day" in the Gospels, met with a cliff.
  Familiarity is its own unbelief. He closes the book mid-verse (stops
  before "the day of vengeance," 4:20) and walks through the crowd's
  middle.
- Intention: the reason the season is a season, not a playlist — proven via
  the redrawn-callback technique, not an unbuilt one.
- **Still open, unchanged from v4:** `PRODUCTION_PIPELINE.md` describes
  long-form as ~20-26 spreads with hero-ratio + Focal Tour, not "7
  movements" as a page count — that mapping still needs doing before this
  builds, and there's zero swirls 16:9 long-form precedent yet. v4 named
  this; v5 dropped it; restored here.

### #15 Road to Emmaus (Luke 24:13-35, long-form, finale) — unchanged, no reviewer objection

Fray is textually exact ("sad," "we trusted," "slow of heart to believe"),
the delayed clear is textual ("their eyes were holden" until the bread),
and Luke 24:27 — "beginning at Moses and all the prophets… the things
concerning himself" — is the series' thesis statement in Christ's own
mouth. Same long-form-tooling open item as #14 applies.

## Part 2 — New candidates

Checked against the project's existing (PythonProject1) narration backlog
by reading actual files, not guessing from titles — several v5 claims here
were wrong and are corrected below.

### Ready to plan (doctrine-clean, no tooling blockers)

| Working title | Passage | Motif | OT/NT | Who | Takeaway | Intention |
|---|---|---|---|---|---|---|
| Until the Breaking of the Day | Genesis 32:22-32 | Fray | OT | the one running back to a promise they fled 20 years ago | blessed AND limping, together | first RETURN episode — a redrawn-echo callback to ep 3 (the Ladder), same proven ep-8 technique |
| Where Art Thou? | Genesis 3:8-21, citing 3:15 | Stain/sin, **covered not cleared** | OT | the one hiding from God, assuming He's coming to condemn | His first word to fallen man is a question, not a sentence | **fix applied:** do NOT merge with the backlog script `44_Grace_Spoken_First` — confirmed `.locked` (`PythonProject1/jesus/narration/44_Grace_Spoken_First/v1/.locked`), a different visual pipeline (Baroque HF), and already consumed once more by `poc_living_sketchbook/first_gospel_in_the_curse/`. Write this fresh and swirls-native, per this project's own standing rule that a format shift gets its own write, citing 3:15 within it — don't touch the locked asset. |

### Doctrine-gated — pending explicit sound-doctrine-both-ways review, not scheduled

| Working title | Passage | Why it's flagged |
|---|---|---|
| But If Not | Daniel 3:16-28 | KJV says "like the Son of God" (3:25) then "his angel" (3:28) — narration must NOT assert "this was Jesus." Real, open theological question (disputed among sound interpreters), not KJV-explicit. Needs its own dedicated doctrine check, both ways, before a word of narration is written. |
| Nevertheless (Gethsemane) | Luke 22:39-46 + Hebrews 5:7 | Hebrews 5:7 ("was heard in that he feared") would put Fray ON CHRIST HIMSELF for the first time. One reviewer (gemini) raised a real visual-language risk on top of the doctrine risk: dead ink has only ever marked human affliction in this series — a viewer may read Fray on Jesus as a defect/sin mark regardless of what the narration says, because "visual metaphors don't come with footnotes." Needs the doctrine check AND a legibility check before this is treated as buildable at all. |

### Season-2 pool (not this season's budget — see cost note below)

| Working title | Passage | Motif | Note |
|---|---|---|---|
| A Man of Unclean Lips | Isaiah 6:1-8 | Stain/sin | tests the OT-cap rule at its edge — keep the cap at Stage 2 even though John 12:41 identifies the glory as Christ's; don't except this one |
| A Cloud Like a Man's Hand | 1 Kings 18:36-46 | swirl-only | same Elijah/drought arc as shipped ep 5 (1 Kings 17). **Fix:** Luke 4:25 (#14's own citation) names the WIDOW (1 Kings 17, already ep 5), not this cloud/rain scene — dropped the overstated "cited in #14" claim. Still pairs naturally with ep 5 on its own merit. |
| Two Men Went Up | Luke 18:9-14 | Stain/sin (self-diagnosed) | the season's first PARABLE (currently zero); forces a real design decision — where does the swirl live when Jesus is TELLING the story, not standing in it (proposal: the margin, touching the publican's line at "justified") |
| Doest Thou Well to Be Angry? | Jonah 4 | swirl-only | the insider who resents grace reaching the wrong people; ends on God's unanswered question |
| For Jonathan's Sake | 2 Samuel 9 | Fray | earned via David's own "Fear not" (9:7); season has no David yet; do NOT force a Stain — lameness isn't Levitical uncleanness for a layman |
| Carest Thou Not? | Mark 4:35-41 | Fray (Stage 3) | most textually-earned Fray in the Gospels. **Fix:** removed the claim that `papermakers-mark` is "already built for this" — confirmed that device lives in `panel_animator/` (the Living-Sketchbook pipeline), not `swirls_page.py`. Would need a genuine swirls-native port, not a drop-in. |
| Of Whom Speaketh the Prophet This? | Acts 8:26-40 | swirl-only | first Acts episode; deliberate rhyme with #15's Luke 24:27; hold swirl at Stage 2 |
| Can These Bones Live? | Ezekiel 37:1-14 | swirl-only | only Spirit-forward episode; maps bones→sinews→flesh→breath to swirl stages |
| He Never Said Yes | John 5:2-9, Bethesda | TBD, likely swirl-only | confirmed backlog script `PythonProject1/jesus/narration/18 He Never Said Yes` (John 5:6) — 38-year infirmity isn't clearly Levitical, needs its own motif check, don't assume Stain |

### Parked, with reasons

- **Genesis 22 "Where Is the Lamb"** — sharp, but the most-preached type in
  Christendom; hold for freshness.
- **Hosea 3 "Fifteen Pieces of Silver"** — earns Stain/sin fully, but first
  adultery page in this style (real NSFW render risk); the 15/30-silver
  Judas rhyme is coincidence, not a text link.
- **Zacchaeus** — same person-shape as shipped She Loved Much. Redundant now.
- **Bronze serpent (Numbers 21)** — already built twice elsewhere in this
  project in other styles.
- **"Not Plan B" (backlog, Galatians 4:4)** — real protoevangelium
  fulfilment thread, but Galatians 4:4 is Paul's reflection, not a drawable
  scene — weak fit for this format.
- **"The Pronouns That Preached the Gospel" (backlog, 1 Peter)** — same
  problem, epistle not narrative.
- ~~**"The Kiss That Cut Off the Bargain"**~~ — **removed.** v5 parked this
  as a Judas item colliding with #12. I read the actual file: it's about
  the **prodigal son's return** (Luke 15:20, the father's kiss), not Judas.
  There is no Judas-kiss item in the backlog; the stated collision doesn't
  exist. (Files 10 and 11 in that folder are two more draft variants of
  the same prodigal-son piece — not relevant here either.)

## Part 3 — Season-level gaps, numbers corrected

- **Healing miracles: corrected count.** v5 claimed "6 of 10 shipped are a
  body healed or raised." I hand-checked all 10: only **3 are clearly
  healing/raising** (Naaman, the Bier, the Nine Lepers) — Ashes is
  ceremonial purification, not illness; Sheba, Jacob's Ladder, Barrel
  (provision, not healing), Nathanael, She Loved Much, and the Cross carry
  none. Generously counting Ashes as healing-adjacent gets to 4, not 6. The
  underlying gap is still real (nothing yet from a parable, a Psalm, Acts,
  an epistle, or most of the OT) — it's just roughly half the size v5
  claimed, worth knowing before treating it as an urgent rebalance.
- **Stain sub-type is lopsided:** 4 of 5 shipped Stains are ceremonial
  uncleanness, 1 (She Loved Much) is moral sin. Going forward: no more
  uncleanness Stains this season — every new Stain (Judas, Genesis 3, and
  any season-2 picks) should be moral.
- **"Outsider" is worn out:** Sheba, Naaman, the Samaritan leper, Simon of
  Cyrene — 4 of 10 shipped, plus #9 as originally framed (now re-aimed away
  from it). The under-served person is the **insider** — hard, resentful,
  performing, or leaving (Judas, the Nazareth crowd, Jonah, the Pharisee).
  New picks should skew here.
- **OT/NT is drifting NT:** all 5 remaining v4 items are NT. Left alone the
  season ends 5 OT / 10+ NT for a series whose spine is the whole canon.
  Genesis 32 (ready now) and the season-2 OT picks are the correction.
- **Persons of the Trinity:** the Spirit has never appeared on a page
  (Ezekiel 37, season 2); the Father is never who Jesus turns to on-page
  (Gethsemane, doctrine-gated, not yet clean to build).
- **Landing fatigue** (memory `feedback_swirls_landing_fatigue`): #12's
  "and it was night" and Jonah 4's unanswered question are real FORM fixes
  — closing on a question or a withheld resolution instead of a CTA phrase
  — but see #12's open CTA-vs-constitution note above; this isn't free to
  do without an explicit call.

## Part 4 — What actually happens next

**#12 "Ye Are Not All Clean" stays the top pick** — but the next concrete
step is a short **plan-only verification pass** (restate the zone-
separation storyboard from v4, page-by-page; confirm the John 13:1-30 wide
ref span survives `pipeline/handoff.py`), not stills spend. If that passes,
build #12.

**Cost — a real decision, not assumed.** v5 quietly grew the season from
15 to 18 episodes with no cost sign-off, and this project's own `/cost`
skill exists specifically to gate that. Real shipped-episode costs run
$6-21 each. Two honest paths, your call:

1. **Cost-neutral:** stay at 15 — the 5 v4 items (redesigned per Part 1)
   plus nothing new. Genesis 32 and Genesis 3 wait for a deliberate "yes,
   grow the season" decision.
2. **Grow the season:** add Genesis 32 now (ready, doctrine-clean, ~$6-21)
   and treat Genesis 3, Daniel 3 (if it clears doctrine), and the season-2
   pool as an explicitly-approved expansion, episode by episode, each
   still going through its own `/cost` pre-flight before spend — never
   bundled as an assumed package.

**Daniel 3 and Isaiah 6 — contradiction fixed.** v5 listed Daniel 3 as both
"ready to plan" and "do not schedule," and put Isaiah 6 in both the
season-2 pool and the season-1 build table. Fixed here: **Daniel 3 stays
doctrine-gated only** (not scheduled anywhere until it clears). **Isaiah 6
stays in the season-2 pool only** (not part of this season's build
sequence).

**Build order, if you choose path 2 above:**
#12 (after its verification pass) → #6 redesign → #9 re-aim → Genesis 32 →
Genesis 3 → #14 (after the long-form tooling gap is closed and eps 4/5 are
live) → #15 (finale, last).

## Part 5 — 30-episode target (user decision, 2026-09-08)

User's call, after reviewing this document: **hold all posting — including
the 6 already-finished-and-locked episodes (Naaman ep4, Barrel ep5, Bier
ep7, She Loved Much ep10, Where Are the Nine ep11, The Cross That Wasn't
His ep13) — until the season reaches 30 episodes**, not 15 or 18. This
explicitly supersedes the "post the 6 finished episodes now" recommendation
carried in `RESUME.md` across the last several sessions — noted here so
the reversal is on the record, not silently dropped.

**Counting the pool above:** 10 shipped + 5 v4-remaining (redesigned) + 2
new ready-now (Genesis 32, Genesis 3) + 2 doctrine-gated (Daniel 3,
Gethsemane) + 9 season-2-pool = **28.** Two more are needed to reach 30.

### Two additions to close the gap to 30

Pulled from the ORIGINAL v1 series plan (`SWIRLS_OF_LIFE_SERIES_PLAN.md`,
2026-08-20) — topics that plan validated but v4 replaced with different
stories when the season pivoted. Not yet run through Fable/the 5-CLI panel
individually (unlike everything above); the 3-question gate is applied
here directly, same discipline, lower ceremony since these are
well-established, doctrinally uncontroversial passages.

| Working title | Passage | Motif | Who | Takeaway | Intention |
|---|---|---|---|---|---|
| My Lord and My God | John 20:24-29 (Thomas) | Fray | the one who says "I need to see it myself before I'll believe it" | Jesus doesn't rebuke the doubt — He meets it, shows the wounds, invites the touch | the doubt motif's most famous home story; season has doubt-ADJACENT (Sheba) but never a direct doubting-disciple story |
| The Father Who Ran | Luke 15:11-32 (the prodigal) | Stain/sin | the one who thinks they've spent their chances past repair | the father is running before the apology is even finished — grace moves first | second parable (with the publican in the season-2 pool); a locked backlog narration draft already exists for this exact passage (`PythonProject1/jesus/narration/09 The Father Who Ran` etc. — 3 draft variants) — still needs a fresh swirls-format write per this project's standing rule, but the doctrine/thread work is already validated, lowering build risk |

**Full 30-episode roster, in build-priority order (10 shipped + 20 to build):**

Shipped (10): Sheba · Ashes · Jacob's Ladder · Naaman · Barrel · the Bier ·
Nathanael · She Loved Much · the Nine Lepers · the Cross/Simon.

To build (20, roughly in order): Ye Are Not All Clean (#12, pending verify
pass) → Talitha Cumi redesign (#6) → Yet the Dogs (#9) → Until the Breaking
of the Day (Genesis 32) → Where Art Thou (Genesis 3) → My Lord and My God
(Thomas) → The Father Who Ran → This Day Is This Scripture Fulfilled (#14,
long) → Road to Emmaus (#15, long, finale) → A Man of Unclean Lips (Isaiah
6) → A Cloud Like a Man's Hand (1 Kings 18) → Two Men Went Up (the
publican) → Doest Thou Well to Be Angry? (Jonah 4) → For Jonathan's Sake (2
Sam 9) → Carest Thou Not? (the storm) → Of Whom Speaketh the Prophet This?
(Acts 8) → Can These Bones Live? (Ezekiel 37) → He Never Said Yes
(Bethesda) → But If Not (Daniel 3, IF it clears doctrine) → Nevertheless
(Gethsemane, IF it clears doctrine — and if either doctrine-gated pick
doesn't clear, promote one PARKED item — Genesis 22 is the next-best
fallback — to keep the count at 30).

**Cost, stated plainly, not buried:** 20 more episodes at this series' own
observed real range ($6-21/episode shipped so far, plus ~$0.50-6 narration
each) is roughly **$150-450+ in remaining spend**, before the two
long-forms (#14, #15) which historically cost more than shorts in the main
engine. This is a real number, not a formality — each individual episode
still goes through its own `/cost` pre-flight before spend, same as every
episode has so far; this total is the honest ballpark for planning
purposes only.

## Panel status, for the record

3/5 reviewed (cursor, claude, gemini — all REVISE, findings addressed
above); grok and codex failed to respond on two separate attempts. Worth
one more retry on a future session in case it's a transient CLI issue, but
not worth blocking this document on a third attempt today.
