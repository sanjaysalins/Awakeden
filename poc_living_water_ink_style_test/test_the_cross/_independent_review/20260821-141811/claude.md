# Independent review — claude (OK, 225s)

## Independent Review — Swirls of Life v2 Series Plan

I verified the plan's central claim (full-catalog collision clearance) against the actual repo files it cites, and checked its own internal arithmetic and doctrine rules against each other. Three concrete problems survive:

### 1. The collision check the whole rebuild exists to fix is itself incomplete

The document's premise is that v1 failed because it didn't verify against `data/series.json` etc. carefully enough, and that v2 was "checked against the full catalog... confirmed clear." That's not true for at least two of the 17 candidates:

- **Episode #1, "Melchizedek Blesses Abraham" (Genesis 14:18-20).** `data/series.json` already has a greenlit episode literally titled `"Melchizedek"`, `primary_ref: "Hebrews 7:3"`, theme `"Priest forever (as type, not appearance)"`, sitting in the existing Types & Shadows series alongside Passover Lamb / Bronze Serpent / Manna / Rock in Wilderness. This is the exact same figure, the exact same NT payoff (Hebrews 7), in the exact same master planning file the plan claims to have checked.
- **Episode #7, "Wherefore Didst Thou Doubt" (Matthew 14:25-33).** `data/series.json` already has `"Walking on water"`, `primary_ref: "Mark 6:50"`, theme `"Lord over chaos - Be not afraid"` — the Synoptic parallel of the same night, same miracle, same "why are you afraid" beat the plan's own doubt-Fray angle leans on.

Neither is in `_website/manifest.yaml` (not yet produced/published), so this isn't a repeat of v1's worst failure mode — but `data/series.json` is the file `pipeline/series.py`/`cli.py`'s own "pick series+episode" picker reads from. Shipping two differently-titled-but-same-subject slots into that file risks operator confusion at pick time and duplicate narration folders (`cli.py` derives the output folder name from the title). At minimum this needs to be named as a real open item, not asserted away.

### 2. The document contradicts its own headline numbers

- Header says **"The slate — 15 episodes"**, but the table has 14 shorts (rows 1-14) + 2 long-form (rows 15-16) = **16**, matching the "Ratio: 14 shorts : 2 longs" line further down. The header count is simply wrong.
- **"Motif balance: 5 Stain · 5 Fray · 3 swirl-only · 1 unique · 2 long-form"** doesn't match the table it's summarizing. Actual tally from the table: Stain = 6 (#2, #4, #10, #11, #12, #13), Fray = 5 (#5-#9), swirl-only = 2 (#1, #3), none = 1 (#14). That's 6/5/2/1, not 5/5/3.

Small errors individually, but this is a document whose entire value proposition is "we checked carefully this time" — a self-contradicting headcount in the summary line undercuts that claim.

### 3. Two episodes violate the plan's own "never conflated" doctrine rule

The dead-ink section states explicitly: *"Stain... Two sub-cases, never conflated: moral sin/guilt... and ceremonial/Levitical uncleanness-as-barrier."* Two rows assign Stain to a third, undefined category:

- **#10, Woman at the Border**: tagged `Stain (uncleanness — Gentile outsider status)`. Gentile ethnicity is not Levitical ceremonial uncleanness — conflating "Gentile" with "unclean" is close to the exact doctrine this project's own Acts-10 theology (and the wider Bible) works hard to reverse ("what God hath cleansed, that call not thou common"). Given this project's locked NON-NEGOTIABLE on doctrine verified two ways, and that the immediately-preceding commit (`1fc3118`) was specifically about not conflating Stain sub-cases on The Hem, this is a real doctrinal landmine, not a labeling nitpick.
- **#13, Thou Shalt Never Wash My Feet**: tagged `Stain (shame at being served)`. Shame-at-being-served is neither sin/guilt nor ceremonial uncleanness — a third, silently-introduced category.

Neither is flagged in the "Open risks, honestly named" table, even though that table exists specifically to surface exactly this kind of thing.

### Other notes (lower weight)
- Tooling claims check out: `independent_review.py --type plan` exists, `swirls_page.py` and `NORTH_STAR_ANIMATION_PROMPT.md` exist and are the real validated artifacts.
- Cost arithmetic ($450-920) is internally consistent with the stated per-episode ranges.
- The deliberate double-use of Naaman/the widow of Zarephath (both standalone shorts AND named inside the Luke 4 long-form) is intentional and stated as such — not a hidden collision, just worth the user's eyes given repeat-viewer overlap.

VERDICT: REVISE
TOP FIXES:
1. Re-run the collision check against `data/series.json` specifically for title/passage overlap (not just "already produced") — resolve or consciously override the Melchizedek and Walking-on-water/Matthew-14 slot collisions before touching the file.
2. Fix the episode-count header (15→16) and the motif-balance tally (5/5/3→6/5/2) so the summary matches the table.
3. Either define a third Stain sub-case (and update the "never conflated" rule to say so) or retag #10 and #13 to a sub-case the doctrine section actually defines — get this past the 5-CLI panel explicitly on the Gentile-as-uncleanness framing before lock.
