# PS22 SHORTS REBUILD PLAN - inked living-page rebuild of the 5 legacy Baroque shorts

$0 paper pass, 2026-07-15. No renders, no spend, no edits to existing files.
Old Baroque cuts are legacy and will never upload; narration + audio are LOCKED and reused as-is.
Build standard: the gold master livingpage_short.spec.json (father_forgive_them, 16 beats / 57.15s)
gated by pipeline/rollout_gate.py (fullbleed <=60%, >=3 templates, stills <=2 uses/piece,
fx >=50% beats, cool pole >=7000K, landing warmest and <=5500K, >=2 living-light entries
in piece.json or an auditable user exception, landing lit, motion smooth, no cut ticks,
animate.duration pinned to 5).

## Locked narration sources (visuals-only rebuild)

| Short | Title | Verse | Locked v1 folder | MP3 | Last word | Beats target |
|---|---|---|---|---|---|---|
| ps22-02 | The Mockers' Words | Ps 22:7-8 | v2\pilot\mockers_words_ps22\v1 | 78.0s | 77.9s | 21 |
| ps22-04 | Declared to the Brethren | Ps 22:22 | longform\02_Psalm_22_Song_From_The_Cross\v1\shorts\04_Declared_To_The_Brethren | 59.0s | 58.2s | 16 |
| ps22-05 | He Hath Done This | Ps 22:31 | longform\02_Psalm_22_Song_From_The_Cross\v1\shorts\05_He_Hath_Done_This | 42.7s | 43.7s (STALE) | 12 |
| ps22-06 | The Ends of the Earth | Ps 22:27 | longform\02_Psalm_22_Song_From_The_Cross\v1\shorts\06_The_Ends_Of_The_Earth | 67.5s | 61.6s | 18 |
| ps22-07 | The Body Foretold | Ps 22:14-17 | longform\02_Psalm_22_Song_From_The_Cross\v1\shorts\07_The_Body_Foretold | 66.9s | 59.8s | 18 |

Beat pace = gold master 3.5-3.6s/beat. PRE-FLIGHT (all $0, before any spec is authored):
regenerate narration.alignment.json against the CURRENT mp3 for all five (ps22-05 alignment
ends 1.0s PAST its mp3 = proven stale; ps22-06/07 carry ~6-7s of tail past the last word -
confirm whether that is trailing silence and set spec total from the fresh alignment).
Memory: alignment-cache-staleness.

Proposed piece dirs (new, engine-owned, gold-master layout: piece.json + audio\ + visual\):
- batches\cluster_01_cross\mockers_words_ps227
- batches\cluster_01_cross\declared_brethren_ps2222
- batches\cluster_01_cross\he_hath_done_ps2231
- batches\cluster_01_cross\ends_of_earth_ps2227
- batches\cluster_01_cross\body_foretold_ps2214
All five stay in the Cross cluster (same psalm family as ps22-01/03/08) even though 04/05/06
draw risen-world stills from cluster_02 - the topical-fit gate governs per still, not per dir.

## Reuse mechanics (why this is nearly free)

- Byte-identical still copy into the new piece dir + the source piece's animate/living-light
  prompt copied VERBATIM = the Kling clip copies for $0, hash-bound (wave_b_copies.py pattern,
  batches\cluster_01_cross\wave_b_copies.py, clip_src_hash sidecar).
- Verified byte-identical across the bank (MD5-checked this pass): risen_mercy_hand (1 hash in
  10 pieces), us_under_cross_shadow, cross_at_dawn, bowed_head_finished, psalm_scroll_night,
  david_writing_psalm, crowd_mocking, grace_poured_sky, look_up_faces, seamless_robe_lots,
  soldiers_gambling, ninth_hour_darkness, stone_rolled_dawn, risen_christ_seeking,
  risen_christ_wounds. Two-variant slugs (copy still AND clip from the SAME source piece so
  the pair stays hash-bound): face_on_cross (A522 variant lives in crucifixion_foretold_ps2218 /
  forsaken_cry_ps221 / i_thirst_john1928; 2FF0 variant elsewhere), golgotha_hill_wide (234E in
  crucifixion_foretold / today_paradise / watch_one_hour / woman_behold; B6CD elsewhere),
  darkness_veil_torn (088E in forsaken / pierced).
- Writing stills (david_writing_psalm, psalm_scroll_night) have NO clips by rule - they play
  via $0 dyncam only. Never Kling-animate a scroll.
- Grid panels and non-LL beats play via $0 dyncam; Kling money is only for living light.
- Crown of thorns is already on every bank cross frame; any FRESH cross frame must carry it.
- Living-light candidates must be wound-FREE stills (Kling regenerates blood on wound-marked
  palms - hard rule). risen_mercy_hand (faint healed mark only) is the proven exception-safe
  landing LL; its LL clip in pierced_zech1210 has already copied $0 into 9+ pieces.

---

## ps22-02 THE MOCKERS' WORDS (Ps 22:7-8 + Matt 27:39-43) - 78.0s, 21 beats

Narration facts: 247 words, 78.0s mp3 (longest of the five - this ships as a ~78s short;
YouTube Shorts allows it, and the audio is locked). Speakers: narrator / david / mocker.
Arc: mocking crowd was reading from a script -> David wrote the taunt 1000 years early ->
Matthew records it nearly line for line -> "come down from the cross" -> He stayed ->
the song ends with the world turning -> CTA "come to the One who would not come down".

Beat skeleton (times approximate until fresh alignment):

| # | ~t | Content | Tpl | Still (source) | Sourcing |
|---|---|---|---|---|---|
| 1 | 0-4 | Hook: crowd mocking was reading a script | big_inset | crowd_mocking (crucifixion_foretold) + psalm_scroll_night | REUSE, clips $0 (scroll = dyncam) |
| 2 | 4-8 | they just didn't know it | full | crowd_mocking | REUSE (2nd use), clip $0 |
| 3 | 8-14 | 1000 years before, Psalm 22 recorded the mocking | two_v | david_writing_psalm + psalm_scroll_night (2nd) | REUSE, dyncam |
| 4 | 14-18 | red-letter DAVID: they shake the head... | full | FRESH wagging_heads_close | FRESH (Cross world; 3 mockers wagging heads, dusk, ink) |
| 5 | 18-22 | ...let him deliver him | full | wagging_heads_close (2nd, adjacent two-shot) | FRESH still reused |
| 6 | 22-28 | at the cross Matthew records it | stack_h | golgotha_hill_wide (crucifixion_foretold, 234E) + FRESH rulers_sneering | REUSE clip $0 + FRESH |
| 7 | 28-33 | red-letter MOCKER: He trusted in God... | full | rulers_sneering (2nd) | FRESH still reused |
| 8 | 33-36 | ...I am the Son of God | two_v | crowd silhouette = ninth_hour_darkness (forsaken) + face_on_cross (A522, crucifixion_foretold) | REUSE, clips $0 |
| 9 | 36-40 | they thought they were inventing the cruelty | hero_frac3 | psalm scroll world: david_writing_psalm (2nd) | REUSE, dyncam |
| 10 | 40-44 | they were reciting prophecy - unwilling witnesses | two_v | seamless_robe_lots + lots_cup_close (both crucifixion_foretold) | REUSE, clips $0 |
| 11 | 44-48 | red-letter MOCKER: save thyself, come down | full | two_thieves_wide (today_paradise, neutral) | REUSE, clip $0 |
| 12 | 48-52 | but He could have come down | full | face_on_cross (2nd use) | REUSE, clip $0 |
| 13 | 52-56 | He showed He was the Son by staying | hero_band3 | golgotha_hill_wide (2nd) | REUSE, clip $0 |
| 14 | 56-61 | the man they mocked is the One the song was about | big_inset | psalm_scroll_night + jesus_looks_down (crucifixion_foretold) | REUSE, clip $0 |
| 15 | 61-64 | they told the King to come down | full | jesus_looks_down (2nd) | REUSE, clip $0 |
| 16 | 64-68 | He stayed under scorn - theirs, and ours | stack_h | us_under_cross_shadow (crucifixion_foretold) | REUSE, clip $0 |
| 17 | 68-71 | a script they never finished | two_v | lots_cup_close (2nd) + ninth_hour_darkness (2nd) | REUSE |
| 18 | 71-74 | the song ends with the ends of the world turning | full | look_up_faces (forsaken/pierced) | REUSE, clip $0 |
| 19 | 74-76 | turning to Him | full | grace_poured_sky (pierced) LIVING LIGHT | REUSE, LL clip $0 |
| 20 | 76-77.5 | Turn, and come | full | risen_mercy_hand LIVING LIGHT | REUSE, LL clip $0 |
| 21 | 77.5-78 | ...to the One who would not come down (landing, warmest) | full | risen_mercy_hand (2nd, adjacent two-shot) | REUSE |

fx arc: open 7200K, cool pole 7800K at the taunts (beats 7-11), warm through the stay
(beats 12-16), land 4900K on the mercy hand. fx on >=11 beats.

Living-light plan: grace_poured_sky ($0 copy from pierced_zech1210, wound-free) +
risen_mercy_hand ($0 copy from pierced_zech1210, healed mark only). 2 entries, both $0. PASS.

Fresh renders: 2 stills (wagging_heads_close, rulers_sneering), dyncam only, no Kling.
Quote: 2 x 1.3 rolls x $0.05 = $0.13. Kling: 0 cr.

---

## ps22-04 DECLARED TO THE BRETHREN (Ps 22:22 + Heb 2:11-12) - 59.0s, 16 beats

Narration facts: 142 words, 59.0s mp3. Speakers: narrator / jesus / scripture.
Arc: psalm starts forsaken but does not end at the cross -> red-letter "I will declare thy
name unto my brethren" -> Hebrews puts the line in the risen Christ's mouth -> "not ashamed
to call them brethren" -> family -> CTA "He is calling you into that family".

| # | ~t | Content | Tpl | Still (source) | Sourcing |
|---|---|---|---|---|---|
| 1 | 0-3.5 | Hook: psalm starts forsaken | big_inset | ninth_hour_darkness (forsaken) + face_on_cross (A522, forsaken) | REUSE, clips $0 |
| 2 | 3.5-7 | but it does not end at the cross | full | ninth_hour_darkness (2nd) | REUSE, clip $0 |
| 3 | 7-11 | the same voice moves from anguish to praise | two_v | face_on_cross (2nd) + psalm_scroll_night | REUSE (scroll dyncam) |
| 4 | 11-16 | red-letter JESUS: I will declare thy name unto my brethren | full | FRESH risen_christ_congregation LIVING LIGHT | FRESH hero + fresh Kling LL |
| 5 | 16-19 | in the midst of the congregation | full | risen_christ_congregation (2nd, adjacent two-shot) | FRESH still reused |
| 6 | 19-23 | who is that praising voice? | stack_h | psalm_scroll_night (2nd) + look_up_faces (forsaken) | REUSE, clip $0 |
| 7 | 23-27 | Hebrews takes that line word for word | two_v | FRESH hebrews_scroll_lamp OR reuse coin-free scroll; decision: reuse psalm world = david_writing_psalm | REUSE, dyncam |
| 8 | 27-31 | ...puts it in the mouth of the risen Christ | hero_frac3 | risen_christ_wounds (empty_tomb / sign_of_jonah) | REUSE, clip $0 |
| 9 | 31-34 | the psalm's turn is Jesus, alive | full | stone_rolled_dawn (sign_of_jonah) LIVING LIGHT | REUSE, LL clip $0 |
| 10 | 34-37 | on the far side of the cross | two_v | stone_rolled_dawn (2nd) + cross_at_dawn (it_is_finished) | REUSE, clips $0 |
| 11 | 37-42 | red-letter SCRIPTURE: not ashamed to call them brethren | full | risen_christ_wounds (2nd) | REUSE, clip $0 |
| 12 | 42-45 | brothers. family. | stack_h | look_up_faces (2nd) + galilee_promise: NO (women-witnesses specific) -> us_under_cross_shadow | REUSE |
| 13 | 45-49 | the same Jesus who cried forsaken | hero_band3 | golgotha_hill_wide (B6CD, forsaken) | REUSE, clip $0 |
| 14 | 49-52 | now lives | full | risen_christ_seeking (empty_tomb) LIVING LIGHT | REUSE, LL clip $0 |
| 15 | 52-56 | not ashamed to call His own brethren | full | risen_christ_seeking (2nd, adjacent two-shot) | REUSE |
| 16 | 56-59 | He is calling you into that family (landing) | full | risen_christ_seeking via LL / caption CTA; landing lit | REUSE |

NOTE beat 14-16: risen_christ_seeking full-bleed on 14+15 as the adjacent two-shot, beat 16
lands on the fresh risen_christ_congregation LL if the two-shot rule pinches - author-time
choice; gate allows max 2 fb pairs and this piece has congregation (4+5) + seeking (14+15).
Beat 16 then plays risen_christ_congregation (2nd use is taken - so beat 16 = seeking 3rd use
VIOLATION). RESOLUTION pinned now: beats 14+15 = seeking two-shot, beat 16 = fresh
risen_christ_congregation is NOT available (2 uses at 4+5), so land on risen_mercy_hand
($0 LL copy) - the proven Christ-lit landing. Final still count stays legal.

fx arc: 7200K forsaken open, cool pole 7800K (beats 2-3), steady warm from the declare pivot,
land 4900-5200K. fx on >=8 beats.

Living-light plan (3 entries, all wound-free):
1. risen_christ_congregation - FRESH still (risen Christ standing among seated brethren,
   hands WOUND-FREE at his sides or raised in praise, warm hall light - design the light as
   the Kling target) + FRESH Kling LL clip: 7.5cr.
2. stone_rolled_dawn - $0 copy (sign_of_jonah_matt1240, verbatim prompt).
3. risen_mercy_hand - $0 copy (pierced_zech1210), carries the lit landing.

Fresh renders: 1 still ($0.065) + 1 Kling LL clip (7.5cr / $0.65).
Quote: $0.72 total ($0.065 stills + $0.65 Kling), 7.5 cr.

---

## ps22-05 HE HATH DONE THIS (Ps 22:31 + John 19:30) - 42.7s, 12 beats

Narration facts: 99 words, 42.7s mp3 (shortest; alignment STALE - regenerate first).
Speakers: narrator / scripture / jesus.
Arc: two final words ten centuries apart -> "that he hath done this" -> "It is finished" ->
same note: a finished work -> nothing left for you to finish -> CTA "come home to the One
who said it is done".

| # | ~t | Content | Tpl | Still (source) | Sourcing |
|---|---|---|---|---|---|
| 1 | 0-3.5 | Hook: two final words, ten centuries apart | big_inset | david_writing_psalm + bowed_head_finished (it_is_finished) | REUSE (scroll dyncam, clip $0) |
| 2 | 3.5-7 | the very same note: a finished work | two_v | psalm_scroll_night + carpenter_bench_rest (it_is_finished) | REUSE, clip $0 |
| 3 | 7-11 | psalm closes looking ahead to God's saving work | full | david_writing_psalm (2nd) | REUSE, dyncam |
| 4 | 11-14 | told to a people not yet born | stack_h | child_waking_dawn (into_thy_hands, neutral) + look_up_faces | REUSE, clips $0 |
| 5 | 14-17 | red-letter SCRIPTURE: that he hath done this. | full | psalm_scroll_night (2nd) | REUSE, dyncam |
| 6 | 17-19 | Done. | full | bowed_head_finished (2nd) | REUSE, clip $0 |
| 7 | 19-23 | as Jesus hung dying, John records His final word | hero_frac3 | vinegar_sponge_reed (it_is_finished; same John 19 moment, fit is scriptural not borrowed) | REUSE, clip $0 |
| 8 | 23-27 | red-letter JESUS: It is finished | full | face_on_cross (A522, i_thirst) | REUSE, clip $0 |
| 9 | 27-31 | different words, same note: a finished work | two_v | carpenter_bench_rest (2nd) + cross_at_dawn LIVING LIGHT | REUSE, LL clip $0 |
| 10 | 31-35 | what's left for you to finish? Nothing | full | cross_at_dawn (2nd) | REUSE |
| 11 | 35-39 | only Someone to come home to | full | father_lamp_doorway (forsaken, neutral homecoming) | REUSE, clip $0 |
| 12 | 39-42.7 | the One who said it is done (landing) | full | risen_mercy_hand LIVING LIGHT | REUSE, LL clip $0 |

fx arc: 7200K open, cool pole 7600K on the dying beats (7-8), land 4900K. fx on >=6 beats.

Living-light plan: cross_at_dawn ($0 copy from it_is_finished_john1930, empty cross =
wound-free) + risen_mercy_hand ($0 copy from pierced_zech1210). 2 entries, $0. PASS.

Fresh renders: NONE. Quote: $0.00, 0 cr. Fully bank-served.

---

## ps22-06 THE ENDS OF THE EARTH (Ps 22:27) - 67.5s, 18 beats

Narration facts: 175 words, 67.5s mp3 (last word 61.6s - verify tail at alignment regen).
Speakers: narrator / scripture.
Arc: one forsaken man dying alone -> the song ends with every nation turning -> red-letter
Ps 22:27 -> sounded impossible from one corner of the empire -> from the cross and the empty
tomb the gospel went out -> nation after nation -> "the ends of the world" includes you ->
CTA "still has room for you to turn to Him".

| # | ~t | Content | Tpl | Still (source) | Sourcing |
|---|---|---|---|---|---|
| 1 | 0-3.5 | Hook: one forsaken man, dying alone | big_inset | ninth_hour_darkness (forsaken) + face_on_cross (A522, forsaken) | REUSE, clips $0 |
| 2 | 3.5-7 | his own psalm ends with every nation turning | full | psalm_scroll_night | REUSE, dyncam |
| 3 | 7-11 | after the suffering, the song throws its arms open | stack_h | face_on_cross (2nd) + grace_poured_sky LIVING LIGHT | REUSE, LL clip $0 |
| 4 | 11-17 | red-letter SCRIPTURE: all the ends of the world shall remember and turn | full | FRESH nations_turning_wide | FRESH (many kindreds across varied lands bowing toward one light on the horizon, ink, no text) |
| 5 | 17-20 | and all the kindreds shall worship | full | nations_turning_wide (2nd, adjacent two-shot) | FRESH still reused |
| 6 | 20-24 | a man dying in one corner of the Roman Empire | hero_band3 | golgotha_hill_wide (B6CD, forsaken) | REUSE, clip $0 |
| 7 | 24-27 | his song says the ends of the earth will turn | two_v | psalm_scroll_night (2nd) + look_up_faces | REUSE, clip $0 |
| 8 | 27-30 | it sounded impossible | full | ninth_hour_darkness (2nd) | REUSE, clip $0 |
| 9 | 30-34 | but from that cross | full | us_under_cross_shadow (forsaken) | REUSE, clip $0 |
| 10 | 34-37 | and the empty tomb | full | stone_rolled_dawn (sign_of_jonah) LIVING LIGHT | REUSE, LL clip $0 |
| 11 | 37-41 | the gospel went out | hero_frac3 | nineveh_distant_walls (sign_of_jonah, neutral city plate) | REUSE, clip $0 |
| 12 | 41-45 | people in nation after nation have turned | stack_h | look_up_faces (2nd) + FRESH kindreds_worship | REUSE + FRESH |
| 13 | 45-48 | worshipping the One who died and rose | full | risen_christ_wounds (sign_of_jonah) | REUSE, clip $0 |
| 14 | 48-51 | that is the reach of the cross | full | golgotha_hill_wide (2nd) | REUSE, clip $0 |
| 15 | 51-55 | never a local tragedy - for the nations | two_v | kindreds_worship (2nd) + stone_rolled_dawn (2nd) | FRESH reused + REUSE |
| 16 | 55-59 | the ends of the world includes wherever you are | full | grace_poured_sky (2nd) | REUSE |
| 17 | 59-63 | the song has swept the whole earth | full | us_under_cross_shadow: NO (2nd use ok) -> us_under_cross_shadow (2nd) | REUSE |
| 18 | 63-67.5 | the Lord still has room for you to turn (landing) | full | risen_christ_wounds (2nd) + fx.rays landing | REUSE, clip $0 |

fx arc: 7300K open, cool pole 7800K on impossible (beat 8), warm from the tomb onward,
land 5000K + fx.rays on beat 18 (landing lit via rays; Christ in frame = risen_christ_wounds).

Living-light plan: grace_poured_sky ($0 copy from pierced_zech1210) + stone_rolled_dawn
($0 copy from sign_of_jonah_matt1240). Both wound-free. 2 entries, $0. PASS.
(Landing carries fx.rays; risen_christ_wounds is wound-marked so it is deliberately NOT an
LL entry - the rays overlay is $0 and gate-legal.)

Fresh renders: 2 stills (nations_turning_wide, kindreds_worship), dyncam only, no Kling.
Quote: 2 x 1.3 x $0.05 = $0.13, 0 cr.

---

## ps22-07 THE BODY FORETOLD (Ps 22:14-17) - 66.9s, 18 beats

Narration facts: 168 words, 66.9s mp3 (last word 59.8s - verify tail at alignment regen).
Speakers: narrator / david.
Arc: a king described a dying body like an eyewitness of a crucifixion he never saw ->
red-letter "I am poured out like water, all my bones out of joint" -> the way a body hangs
by the arms -> "I may tell all my bones: they look and stare upon me" -> David never saw a
cross -> Jesus bore that song on the tree willingly -> CTA "He still brings sinners home".

| # | ~t | Content | Tpl | Still (source) | Sourcing |
|---|---|---|---|---|---|
| 1 | 0-4 | Hook: a king described a dying body so exactly | big_inset | david_writing_psalm + face_on_cross (A522, crucifixion_foretold) | REUSE (scroll dyncam, clip $0) |
| 2 | 4-8 | ...it reads like an eyewitness account | full | david_writing_psalm (2nd) | REUSE, dyncam |
| 3 | 8-12 | Psalm 22. First person, someone else's death | two_v | psalm_scroll_night + golgotha_hill_wide (234E, crucifixion_foretold) | REUSE, clip $0 |
| 4 | 12-15 | watch the body of the dying man | full | FRESH body_suspended_wide | FRESH (distant reverent silhouette of the crucified body hanging by the arms, crown of thorns, weight visibly on the shoulders, storm sky, ink; NO gore) |
| 5 | 15-20 | red-letter DAVID: I am poured out like water... | full | blood_water_wood (pierced, neutral macro) | REUSE, clip $0 |
| 6 | 20-24 | ...all my bones are out of joint | full | body_suspended_wide (2nd, adjacent two-shot at 4+5 NOT possible - beats 4 and 6 are split by 5; author order pinned: 4 = blood_water_wood, 5-6 = body_suspended_wide two-shot) | see note |
| 7 | 24-28 | drained - every joint pulled loose, hanging by the arms | hero_frac3 | two_thieves_wide (today_paradise, neutral) | REUSE, clip $0 |
| 8 | 28-33 | red-letter DAVID: I may tell all my bones... | full | face_on_cross (2nd) | REUSE, clip $0 |
| 9 | 33-36 | ...they look and stare upon me | stack_h | crowd_mocking (crucifixion_foretold) + look_up_faces: NO (tearful, wrong mood) -> crowd_mocking single + ninth_hour_darkness | REUSE, clips $0 |
| 10 | 36-40 | he could count every bone, stretched, exposed | full | crowd_mocking (2nd) | REUSE, clip $0 |
| 11 | 40-44 | David never saw a cross | two_v | psalm_scroll_night (2nd) + ninth_hour_darkness (2nd) | REUSE |
| 12 | 44-47 | Rome had not taken it up yet | full | golgotha_hill_wide (2nd) | REUSE, clip $0 |
| 13 | 47-51 | yet his psalm names a body pulled apart and stared at | hero_band3 | us_under_cross_shadow (crucifixion_foretold) | REUSE, clip $0 |
| 14 | 51-54 | Jesus bore that song | full | nail_through_hand (fft, neutral) | REUSE, clip $0 |
| 15 | 54-57 | on the tree, willingly | full | bowed_head_finished (i_thirst) | REUSE, clip $0 |
| 16 | 57-60 | and He still... | full | cross_at_dawn LIVING LIGHT | REUSE, LL clip $0 |
| 17 | 60-63.5 | ...brings sinners | full | risen_mercy_hand LIVING LIGHT | REUSE, LL clip $0 |
| 18 | 63.5-66.9 | home. (landing, warmest) | full | risen_mercy_hand (2nd, adjacent two-shot) | REUSE |

Beat 4-6 order pinned: 4 = blood_water_wood intro macro, 5+6 = body_suspended_wide adjacent
full-bleed two-shot under the red-letter. Keeps both stills at 2 uses and the fb-pair legal.

fx arc: 7200K open, cool pole 7900K across the body beats (5-10, the piece's coldest run),
warm from beat 14, land 4900K. fx on >=10 beats.

Living-light plan: cross_at_dawn ($0 copy from it_is_finished_john1930) + risen_mercy_hand
($0 copy from pierced_zech1210). Both wound-free (empty cross / healed mark). 2 entries, $0.
PASS. (This is the wound-heaviest piece; if the user would rather not push cross_at_dawn to
a 6th piece, the fft-precedent 1-LL exception is the alternative - flag, user decides.)

Fresh renders: 1 still (body_suspended_wide), dyncam only, no Kling.
Quote: 1 x 1.3 x $0.05 = $0.065, 0 cr.

---

## TOTALS AND QUOTE

| Short | Fresh stills | Fresh Kling | Stills $ | Kling $ | Total $ | Credits |
|---|---|---|---|---|---|---|
| ps22-02 Mockers' Words | 2 | 0 | $0.13 | $0.00 | $0.13 | 0.0 cr |
| ps22-04 Declared to Brethren | 1 | 1 LL clip | $0.07 | $0.65 | $0.72 | 7.5 cr |
| ps22-05 He Hath Done This | 0 | 0 | $0.00 | $0.00 | $0.00 | 0.0 cr |
| ps22-06 Ends of the Earth | 2 | 0 | $0.13 | $0.00 | $0.13 | 0.0 cr |
| ps22-07 Body Foretold | 1 | 0 | $0.07 | $0.00 | $0.07 | 0.0 cr |
| **TOTAL (base)** | **6** | **1** | **$0.39** | **$0.65** | **~$1.04** | **7.5 cr** |

Contingency ceiling: +1 Kling re-roll on the ps22-04 fresh LL (7.5 cr / $0.65) + still
re-rolls already inside the 1.3x budget = worst case ~$1.70 / 15 cr.
Everything else in all five pieces is $0: byte-identical still copies, hash-bound clip
copies (wave_b_copies.py pattern), dyncam, PIL fx, grids, captions, score, sfx.
Ask-before-spending: the $1.04 base needs the user's OK before the single metered batch
(1 seedream wave of 6 stills + 1 Kling LL render), logged to data/spend_ledger.jsonl.

## STALENESS FLAGS (heavy bank reuse, 3+ pieces - shared with the longs lane)

The longs lane pulls the same 9:16 stills into vertical grid panels of 16:9 living pages,
so these counts are corpus-wide watch items (count = existing pieces + this plan):

| Still | Now | After plan | Flag |
|---|---|---|---|
| risen_mercy_hand | 10 | 13 (02, 04, 05, 07) | HEAVY - the standing landing; deliberate brand mark, but longs should NOT also land on it every time |
| face_on_cross (both variants) | 9 | 13 (02, 04, 05, 06, 07 - A522 variant) | HEAVY |
| us_under_cross_shadow | 9 | 12 (02, 06, 07) | HEAVY |
| golgotha_hill_wide (both variants) | 9 | 13 (02, 04, 06, 07) | HEAVY |
| psalm_scroll_night | 4 | 9 (all five) | HEAVY - but it IS the psalm-22 family mark |
| david_writing_psalm | 3 | 7 (02, 05, 07) | HEAVY within the psalm family |
| cross_at_dawn (LL) | 4 | 6 (05, 07) | flag - 6 pieces carry the same LL clip |
| crowd_mocking | 3 | 5 (02, 07) | flag |
| bowed_head_finished | 4 | 6 (05, 07) | flag |
| ninth_hour_darkness | 1 | 4 (02, 04, 06, 07) | flag |
| stone_rolled_dawn (LL) | 2 | 4 (04, 06) | flag |
| grace_poured_sky (LL) | 2 | 4 (02, 06) | flag |
| look_up_faces | 2 | 5 (02, 04, 05, 06) | flag |
| risen_christ_wounds | 2 | 4 (04, 06) | flag |
| risen_christ_seeking (LL) | 2 | 3 (04) | flag |

Run corpus_diversity.py after spec authoring; if it REVISEs on any of the HEAVY rows, the
cheapest relief valve is 1-2 extra fresh plates (+$0.07-0.13) swapped into the worst piece.

## BUILD ORDER (once user OKs the quote)

1. $0 pre-flight: regen the 5 alignments; create the 5 piece dirs; copy locked audio in.
2. ps22-05 first (fully $0, fastest gate PASS - proves the copy chain end to end).
3. Seedream wave: all 6 fresh stills in one batch (stills gate + bible-check fact cards +
   full-res eyeball before any Kling).
4. ps22-04 Kling LL render (the only paid clip), then wave-copy LL clips into all five.
5. Author 5 specs to the gold master (grids >=40%, >=3 templates, arcs, smooth), run
   pipeline\rollout_gate.py on all five, build through score/sfx, stills_gate + compare pages.
6. corpus_diversity.py + 5-CLI panel on the batch plan per the standing review gate.
