# Independent review — claude (OK, 286s)

Verified several of the document's own citations against the actual repo files (not just re-reading the prose), and cross-checked its tables against each other. Findings below.

## Findings

**1. "The Kiss That Cut Off the Bargain" is misidentified — the parking rationale is wrong.**
Parked-items section says: *"'The Kiss That Cut Off the Bargain' (Judas, backlog) — collides with #12. One Judas per season."* I read the actual file, `PythonProject1/jesus/narration/12 The Kiss That Cut Off the Bargain/v1/narration.md` — it is about the **prodigal son's return** (Luke 15:20, the father's kiss on the neck), not Judas's betrayal kiss. Files `10` and `11` in that same backlog folder are two more draft variants of the *same* prodigal-son piece. There is no Judas-kiss item in the backlog at all, so the stated collision with #12 (John 13, Judas) doesn't exist. This directly contradicts the document's own claim that Part 2's refs are *"verified... not guessed."*

**2. Isaiah 6 is placed in two contradictory season slots.**
Part 2's "Season-2 pool" table explicitly puts *"A Man of Unclean Lips | Isaiah 6:1-8"* under *"real candidates, sequenced after the current season closes."* But Part 4's "Proposed season shape after this pass: 18 episodes" table schedules it as episode 6 of the *current* season, and the season's headline rebalancing claim — *"Resulting balance: 8 OT / 10 NT"* — only works because Isaiah 6 is counted as one of the 3 new OT builds. Pick one: if Isaiah 6 stays in season 2 per Part 2's own classification, the current season is 7 OT / 10 NT over 17 episodes, not 8/10 over 18, and the OT-drift problem this whole exercise was trying to fix is only half-solved.

**3. The season-shape table contradicts the plan's own stated sequencing, including its own doctrine gate.**
"Immediate recommendation" says: *"Once #6 and #9's redesigns are panel-clean, they resume as the next two builds; Daniel 3 and Genesis 32 follow."* — i.e. order is Ye Are Not All Clean → Talitha Cumi → Yet the Dogs → Daniel 3 → Genesis 32. The table two paragraphs later orders it Ye Are Not All Clean → **Daniel 3 → Genesis 32** → Talitha Cumi → Yet the Dogs — the opposite order. Worse, Daniel 3 sits in the "Needs a build decision, doctrine-sensitive — **do not schedule** until panel-checked" table, yet the season-shape table schedules it as build #2, immediately after #12, with no panel gate shown as cleared.

**4. A "ready to plan now" episode silently disappears.**
"Where Art Thou? / Grace Spoken First" (Genesis 3) gets a full Who/Takeaway/Intention row under "Ready to plan now," including the explicit recommendation to merge it with the locked `44_Grace_Spoken_First` backlog script. It is then absent from the final 18-episode season-shape table with no note that it was cut, deferred, or folded elsewhere. A reader building from Part 4 alone would never know this candidate existed.

**5. The core "healing miracles dominate" numeric claim is overstated by 2x.**
Part 3 states: *"Healing miracles dominate: 6 of 10 shipped episodes are a body healed or raised."* I checked the actual 10 shipped folders (`poc_living_water_ink_style_test/swirls_episode_*`): Sheba (1 Kings 10), Ashes (Numbers 19, ceremonial purification, no illness), Jacob's Ladder (Genesis 28), Naaman (healing), Barrel (provision, not healing), the Bier (raising), Nathanael (John 1, no healing), She Loved Much (Luke 7, no healing), Nine Lepers (healing), the Cross/Simon (no healing). That's **3 clear healing/raising episodes**, not 6 — even a generous read of "Ashes" as healing-adjacent only gets to 4. This is the stated justification for steering new picks toward parable/Psalm/Acts/epistle territory; the real gap is real but roughly half the size claimed.

**6. No cost accounting for a 15→18 episode expansion, despite the project having its own spend gate.**
Part 4 recommends growing the season by 3 episodes (20%) with zero mention of $ impact, and the project's own `/cost` skill exists specifically to "pre-flight the spend of any metered batch, get explicit user OK, then log it to the ledger... BEFORE any HF/NBP/ElevenLabs/Kling run." Real shipped-episode costs in this series run ~$6-21 each (Bier ~$6, Barrel ~$9.43, Where Are the Nine ~$14.51, The Cross ~$21+) — so 3 extra episodes is a real, un-costed $20-65+ commitment that should be run past the user explicitly, not folded silently into a "proposed season shape."

**7. Minor citation slip on a Season-2 candidate.**
"A Cloud Like a Man's Hand" is glossed as *"cited in #14 (Luke 4:25)."* Luke 4:25 cites the **widow of Zarephath, 1 Kings 17** (already shipped as ep5, "Barrel") — not 1 Kings 18's cloud/rain scene, which is what this candidate episode is actually about. The "chains 5→this→14" claim overstates how directly #14 touches this specific candidate.

**8. Minor count mismatch.**
"the season's most over-used person (Sheba, Naaman, the Samaritan leper, Simon of Cyrene, Nathanael — 6 of 15 already lean outsider)" lists 5 names against a claimed count of 6.

These aren't cosmetic — items 2-4 mean the one concrete deliverable this document produces (the season-shape table) doesn't actually reconcile with its own supporting analysis, and item 1 means one of the "verified, not guessed" parking decisions rests on a misread source file.

VERDICT: REVISE
TOP FIXES:
1. Reconcile Isaiah 6's season assignment (Part 2 says season 2, Part 4's table counts it in season 1) and re-run the OT/NT math once that's fixed — the current 8/10 figure is only valid if Isaiah 6 stays.
2. Fix the sequencing contradiction between the "Immediate recommendation" prose and the season-shape table, and don't schedule Daniel 3 in any table until it has actually cleared the doctrine-sensitive panel gate the document itself requires.
3. Re-verify every backlog cross-reference against the actual file contents (not title guessing) — "The Kiss That Cut Off the Bargain" is the prodigal son, not Judas, which invalidates that parking decision; re-check the "6 of 10 healing miracles" count the same way.
