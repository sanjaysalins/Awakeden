# Isaiah 53 - INKED GRAPHIC-NOVEL REBUILD PLAN (paper pass, $0)

Rebuild of the long-form film in the inked living-page standard, replacing the
legacy Baroque oil version (never to be uploaded). AUDIO IS LOCKED - visuals only.
Template: longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/livingpage_full.spec.json

## 1. Audio facts

- Source: longform/01_Isaiah_53_Suffering_Servant/v1/narration.mp3 (+ narration.alignment.json, 1235 aligned words)
- Last aligned word ends 405.02s; speech runs ~6:45. Confirm exact mp3 tail with ffprobe when the spec is built (ps22 spec total = mp3 duration, not last-word end).
- Multi-voice: narrator + the_LORD (Isa 52:13) + eunuch (Acts 8:34). All KJV spans are tagged speakers.
- ps22 beat density: 99 beats / 418.2s = 14.2 beats/min. Target here: 95 beats over ~405s = 14.1 beats/min. Matched.
- Movement structure (timestamps from narration.alignment.json):

| Mv | Name                                   | Window (s)      | Len   | Beats |
|----|----------------------------------------|-----------------|-------|-------|
| M1 | The riddle (700 years early)           | 0.0 - 37.8      | 37.8  | 9     |
| M2 | The picture breaks (exalted vs marred) | 37.8 - 89.7     | 51.9  | 12    |
| M3 | The transaction (wounded for us)       | 89.7 - 160.3    | 70.6  | 17    |
| M4 | The honest question (Israel?)          | 160.3 - 228.3   | 68.0  | 16    |
| M5 | The Ethiopian (Acts 8)                 | 228.3 - 285.4   | 57.1  | 13    |
| M6 | Pleased to bruise / toward morning     | 285.4 - 342.0   | 56.6  | 13    |
| M7 | The arm has a name (CTA)               | 342.0 - ~407    | 63+   | 15    |
|    | TOTAL                                  |                 | ~405  | 95    |

Living-page devices carried over from ps22: word-timed slams from alignment.json,
takeover dive, one BORDER-BREAK (on "And then the picture breaks" at 49.9s - the
line literally names the device), synthesized heartbeat building from "You do not
have to clean yourself up" (385.9) and STOPPING DEAD on "His name is Jesus"
(400.4), sacred red-letter beats perfectly still, reuse rule max 2 uses per still
and never twice full-bleed.

## 2. Sourcing legend

- R16    = REUSE-16:9: byte-identical ps22 inked still (visual_16x9_inked/*.png)
- R16C   = REUSE-16:9 CLIP: ps22 inked 16:9 clip (visual_16x9_inked/clips/*.mp4), same aspect, $0 motion
- P916   = PANEL-9:16: shorts still (batches/cluster_01_cross|cluster_02_resurrection/*/visual/*.png), VERTICAL COLUMN PANELS ONLY (triptych_v col ~640x1080 vs 9:16 = ~5% crop), never full-bleed
- P916C  = PANEL-9:16 CLIP: finished shorts Kling clip in a vertical column panel, $0 motion (per the upgraded reuse rule; full-bleed 16:9 use of a 9:16 clip stays forbidden)
- RR     = RE-RENDER-16:9: same world/prompt + same ref re-rendered at 16:9, BytePlus seedream-4-5-251128, ~$0.05/roll
- FR     = FRESH-16:9: new prompt, BytePlus, ~$0.05/roll
- KLING  = paid hero clip, 7.5 cr (~$0.65)

Refs: all needed character anchors already exist in ref_library/characters/ -
ISAIAH, JESUS (face_on_cross world), ETHIOPIAN_EUNUCH, PHILIP (the evangelist,
not PHILIP_THE_APOSTLE), ISRAEL_NATION, SHEEP_FLOCK, SCRIBES_PHARISEES, CROWD.
No new refs required.

## 3. Beat-by-beat skeleton (95 beats)

Times are approximate anchors; the spec pass word-times every slam from
narration.alignment.json. tpl values are the ps22/engine set: full, two_v,
triptych_v, big_inset, quad (quad only for 16:9 sources - landscape cells crop
9:16 badly).

### M1 - The riddle (0.0 - 37.8) - 9 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 1  | 0.0-6.3     | Hook: a prophet writes a death 700 years early         | full       | RR isaiah_writing_lamplight (from cluster-1 prophet-at-scroll world, ISAIAH ref) + KLING living light | Film-open hero: lamp flame breathing |
| 2  | 6.3-10.0    | "before a Roman nail was ever driven"                  | two_v      | R16 roman_nails_pouch + R16 quill_ink_drop                              | Nail vs quill time bridge; slam NAIL |
| 3  | 10.0-14.0   | "a prophet in Jerusalem"                               | full       | FR jerusalem_700bc_wide                                                 | Pre-Roman city, dyncam swoop |
| 4  | 14.0-18.5   | "wrote down the death of a man he had never met"       | two_v      | R16 hebrew_scroll_edge_light + P916 face_on_cross (column)              | Scroll never animates |
| 5  | 18.5-21.9   | "the wounds, the silence, the grave, the rich man"     | triptych_v | P916C nail_through_hand + P916C bowed_head_finished + P916C body_laid_in_tomb | $0 motion columns, one slam per noun |
| 6  | 21.9-27.3   | KJV "Who hath believed our report?"                    | full       | R16 synagogue_listeners_lean                                            | Sacred still |
| 7  | 27.3-31.5   | "This is Isaiah fifty-three"                           | full       | R16 first_century_reader                                                | dyncam push |
| 8  | 31.5-35.0   | "the most astonishing accident in all literature"      | full       | R16 seventy_scribes_lamps                                               |  |
| 9  | 35.0-37.8   | "someone outside of time... how God would save the world" | full    | R16 convergence_on_cross                                                | dyncam arc |

### M2 - The picture breaks (37.8 - 89.7) - 12 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 10 | 37.8-40.1   | "It opens with God Himself pointing"                   | full       | R16 parting_storm_light (still crop)                                    | Light shaft; NO figure of the Father |
| 11 | 40.1-46.2   | KJV the_LORD "Behold, my servant... very high"         | full       | FR servant_exalted_light                                                | Sacred still; servant silhouette under heaven-light, no depiction of God |
| 12 | 46.2-49.9   | "You brace yourself for a conquering king"             | full       | R16 war_helmet_spear_rest                                               | dyncam push |
| 13 | 49.9-53.5   | "And then the picture breaks."                         | full       | R16C face_anguish_closeup ($0 clip)                                     | BORDER-BREAK beat |
| 14 | 53.5-58.5   | KJV "visage so marred more than any man"               | full       | R16 cry_profile_dark                                                    | Slam MARRED |
| 15 | 58.5-61.5   | "A face beaten past recognising"                       | full       | R16 spit_shout_macro                                                    | Macro |
| 16 | 61.5-64.7   | hold: "more than the sons of men"                      | full       | R16 tear_track_macro                                                    | Quiet beat |
| 17 | 64.7-71.5   | KJV "no form nor comeliness... no beauty"              | triptych_v | P916C crowd_mocking + P916 face_on_cross (2nd, new crop) + P916C look_up_faces | $0 columns |
| 18 | 71.5-77.5   | KJV "despised and rejected... man of sorrows"          | full       | R16C mockers_wag_heads ($0 clip)                                        |  |
| 19 | 77.5-82.0   | "does not arrive in armour. He arrives in agony."      | two_v      | R16 war_helmet_spear_rest (2nd crop) + R16 hung_by_arms                 | Slam AGONY |
| 20 | 82.0-85.5   | "The world looks at him - and looks away"              | full       | R16 hill_crowd_watching_storm                                           | dyncam pullback |
| 21 | 85.5-89.7   | "exalted + despised are the same man - the whole gospel in one breath" | two_v | FR servant_exalted_light (2nd crop) + R16C face_anguish_closeup (2nd, macro crop) | The tension pair |

### M3 - The transaction (89.7 - 160.3) - 17 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 22 | 89.7-93.1   | "the centre of the chapter - every line a transaction" | full       | R16 scholar_hand_on_text                                                |  |
| 23 | 93.1-96.5   | KJV "Surely he hath borne our griefs"                  | full       | R16C substitute_shadow ($0 clip)                                        | Sacred-adjacent |
| 24 | 96.5-99.1   | "Our griefs. Not his own."                             | two_v      | P916 mourners_only_son + P916C us_under_cross_shadow                    | Columns |
| 25 | 99.1-104.5  | KJV "But he was wounded for our transgressions"        | full       | RR nail_through_hand_16x9 (cluster-1 world, 16:9 re-render)             | Slam WOUNDED; dyncam ONLY, never Kling (blood rule) |
| 26 | 104.5-110.0 | KJV "...chastisement of our peace... with his stripes we are healed" | triptych_v | P916C darkness_veil_torn + P916 cross_at_dawn + P916C grace_poured_sky | $0 columns |
| 27 | 110.0-115.5 | "Stay on the small words. Our transgressions. Our peace. His wounds." | triptych_v | P916C jesus_praying_close + P916C bowed_head_finished (2nd) + P916C nail_through_hand (2nd crop) | One word-slam per column |
| 28 | 115.5-121.0 | "not a brave example - a substitution"                 | full       | R16 substitute_shadow (2nd, tighter still crop)                         | Slam SUBSTITUTION |
| 29 | 121.0-128.4 | "one stands in the place of many, takes what they had earned" | full | RR us_under_cross_shadow_16x9 (cluster-1 signature world at 16:9)       | Signature wide |
| 30 | 128.4-134.0 | KJV "All we like sheep have gone astray"               | full       | FR sheep_astray_hills (SHEEP_FLOCK ref)                                 | Slam ASTRAY |
| 31 | 134.0-138.0 | "we have turned every one to his own way"              | two_v      | FR sheep_astray_hills (2nd crop) + R16 roads_converge_valley            | Diverging ways |
| 32 | 138.0-140.5 | KJV "and the LORD hath laid on him the iniquity of us all" | full   | R16C golgotha_three_crosses_ridge ($0 clip)                             | Slam LAID ON HIM |
| 33 | 140.5-142.5 | hold on the verse                                      | full       | R16C golgotha_three_crosses_ridge (same clip continues)                 | Takeover dive candidate |
| 34 | 142.5-145.0 | "All of us. Every one."                                | full       | R16 ends_of_earth_faces                                                 | Faces mosaic |
| 35 | 145.0-148.0 | "the straying is named - then the rescue: laid on him" | two_v      | P916C look_up_faces (2nd) + P916C risen_mercy_hand                      | Columns |
| 36 | 148.0-154.1 | KJV "brought as a lamb to the slaughter... sheep before her shearers is dumb" | full | FR lamb_to_slaughter + KLING living light                    | HERO. Blood-free lamb, no wound marks |
| 37 | 154.1-157.8 | "No defence. No curse on his accusers."                | full       | FR jesus_silent_accusers (JESUS ref; pre-cross, bound before accusers)  |  |
| 38 | 157.8-160.3 | "Silent."                                              | two_v      | P916 bowed_head_finished (still) + P916 cross_at_dawn (2nd crop)        | Sacred stillness |

### M4 - The honest question (160.3 - 228.3) - 16 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 39 | 160.3-164.5 | "Now - an honest question."                            | full       | R16 scholars_debate_two                                                 |  |
| 40 | 164.5-168.5 | "many thoughtful Jewish readers: the Servant is Israel" | full      | R16 first_century_reader (2nd crop)                                     |  |
| 41 | 168.5-172.0 | "a suffering people, despised among the nations"       | full       | FR israel_servant_nation (ISRAEL_NATION ref; exile road, wide)          | Respectful, never caricature |
| 42 | 172.0-177.5 | "a real text behind them. Earlier in this same book"   | full       | R16 scholar_hand_on_text (2nd crop)                                     |  |
| 43 | 177.5-183.0 | KJV "Thou art my servant, O Israel"                    | full       | FR israel_servant_nation (2nd crop)                                     | Sacred still |
| 44 | 183.0-188.5 | "not a dodge - the natural first guess"                | full       | R16 scholars_debate_two (2nd crop)                                      |  |
| 45 | 188.5-192.0 | "It deserves a serious answer, not a sneer."           | two_v      | R16 two_scrolls_compared + R16 greek_ot_scroll                          | Scrolls never animate |
| 46 | 192.0-195.8 | "what the chapter does that no nation can survive. First, the sufferer is sinless" | full | R16 hebrew_scroll_edge_light (2nd crop)                | Punch SINLESS |
| 47 | 195.8-201.0 | KJV "grave with the wicked, with the rich in his death" | two_v     | R16 execution_stakes_field + P916C body_laid_in_tomb (2nd)              | Wicked stakes vs rich tomb |
| 48 | 201.0-206.5 | KJV "done no violence, neither any deceit in his mouth" | triptych_v | P916C jesus_praying_close (2nd) + P916 willing_offering + P916 mourners_only_son (2nd crop) | Columns |
| 49 | 206.5-211.5 | "No people in history described that way"              | full       | R16 ends_of_earth                                                       | dyncam pullback |
| 50 | 211.5-215.5 | "Second, he dies for the people:"                      | full       | R16C pierced_hands_feet ($0 clip)                                       |  |
| 51 | 215.5-218.5 | KJV "for the transgression of my people was he stricken" | full     | R16C pierced_hands_feet (clip continues, tighter frame)                 | Slam STRICKEN |
| 52 | 218.5-220.5 | "stands in their place - so he cannot simply be them"  | full       | R16 convergence_on_cross (2nd crop)                                     |  |
| 53 | 220.5-223.4 | "A single grave. A rich man's tomb. A sinless life."   | triptych_v | P916C three_days_dark_tomb + P916 tomb_stone_sealed + P916C body_laid_in_tomb (dedupe at spec pass) | One slam per column |
| 54 | 223.4-228.3 | "This is not a people. This is a person."              | full       | R16C cry_face_tears ($0 clip)                                           | Slam A PERSON |

### M5 - The Ethiopian (228.3 - 285.4) - 13 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 55 | 228.3-233.0 | "the only question that matters. Who is he?"           | full       | R16 two_scrolls_compared (2nd crop)                                     | Punch WHO IS HE |
| 56 | 233.0-237.6 | "The New Testament records the exact moment"           | full       | R16 seventy_scribes_lamps (2nd crop)                                    |  |
| 57 | 237.6-243.0 | "A man from Ethiopia, riding home in his chariot"      | full       | FR chariot_desert_road_wide (ETHIOPIAN_EUNUCH ref)                      | dyncam swoop |
| 58 | 243.0-248.0 | "reading this very chapter aloud"                      | full       | FR chariot_desert_road_wide (2nd, tight crop on the scroll)             |  |
| 59 | 248.0-255.1 | KJV "led as a sheep to the slaughter..." (Acts 8:32)   | full       | R16 greek_ot_scroll (2nd, macro crop)                                   | The eunuch reads GREEK; scroll never animates |
| 60 | 255.1-258.5 | "Philip, sent by the Spirit, comes alongside"          | full       | FR philip_eunuch_scroll (PHILIP + ETHIOPIAN_EUNUCH refs)                | Two-shot over the open scroll |
| 61 | 258.5-262.5 | KJV eunuch "of whom speaketh the prophet this?"        | full       | FR philip_eunuch_scroll (2nd crop, on the eunuch's face)                | Sacred still (spoken KJV) |
| 62 | 262.5-267.4 | "Luke gives the answer in one unforgettable line"      | full       | R16 quill_ink_drop (2nd crop)                                           |  |
| 63 | 267.4-271.5 | KJV "and preached unto him JESUS"                      | full       | R16 roads_converge_valley (2nd crop)                                    | Slam JESUS |
| 64 | 271.5-274.0 | hold on JESUS                                          | full       | R16C golgotha_three_crosses_ridge (2nd use, still crop)                 | Sacred hold |
| 65 | 274.0-278.5 | "began at the same scripture - the road led straight to Jesus of Nazareth" | two_v | P916 prophet_scroll (column) + P916C risen_christ_wounds (column) | Prophecy-to-fulfilment pair |
| 66 | 278.5-282.0 | "The report Isaiah wondered if anyone would believe"   | full       | RR isaiah_writing_lamplight (2nd crop)                                  |  |
| 67 | 282.0-285.4 | "the New Testament answers: this is the man."          | two_v      | P916C us_under_cross_shadow (2nd) + P916C risen_mercy_hand (2nd)        | Columns |

### M6 - Pleased to bruise / toward morning (285.4 - 342.0) - 13 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 68 | 285.4-289.0 | "one line heavier than all the wounds"                 | full       | R16 storm_over_jerusalem                                                |  |
| 69 | 289.0-294.0 | KJV "Yet it pleased the LORD to bruise him"            | full       | R16 ninth_hour_darkness                                                 | Sacred still; darkness + cross, NO figure of the Father |
| 70 | 294.0-299.0 | "Pleased. Not because the Father delights in pain"     | full       | R16C cry_ninth_hour ($0 clip)                                           |  |
| 71 | 299.0-303.0 | "He delights in what the cross would accomplish: a people brought home" | full | R16C kindreds_bowing ($0 clip)                              |  |
| 72 | 303.0-307.1 | "he poured out his soul unto death. He gave it."       | full       | R16 poured_out_bones                                                    | Slam HE GAVE IT |
| 73 | 307.1-308.7 | "quietly, the chapter turns toward morning"            | full       | R16C parting_storm_light ($0 clip, 2nd use of slug)                     | Tone pivot |
| 74 | 308.7-313.0 | KJV "he shall see his seed, he shall prolong his days" | full       | R16C nations_streaming_wide ($0 clip)                                   |  |
| 75 | 313.0-316.9 | KJV "...the pleasure of the LORD shall prosper in his hand" | full  | R16C dawn_empty_cross ($0 clip)                                         |  |
| 76 | 316.9-321.0 | KJV "shall see of the travail of his soul, and shall be satisfied" | full | R16 morning_birds_hill                                          | Quiet dawn |
| 77 | 321.0-327.0 | "bruised to death does not live - unless death is not the end of him" | triptych_v | P916C stone_rolled_dawn + P916C tomb_doorway_dawn + P916C linen_left_lying | $0 columns; the empty-tomb triptych |
| 78 | 327.0-332.0 | "Isaiah does not spell out an empty tomb - a shape only resurrection fills" | full | R16C empty_tomb_open ($0 clip)                            |  |
| 79 | 332.0-336.5 | "a shadow the New Testament would bring into full light" | two_v    | R16 grave_clothes_folded_macro + P916C risen_christ_wounds (2nd)        | Healed scars, no fresh blood |
| 80 | 336.5-342.0 | "one word: satisfied. The travail was not wasted. It was enough." | full | R16C finished_work ($0 clip)                                     | Slam ENOUGH |

### M7 - The arm has a name (342.0 - ~407) - 15 beats

| #  | ~t          | Line / subject                                         | tpl        | Source                                                                 | Notes |
|----|-------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|-------|
| 81 | 342.0-346.5 | "So come back to where Isaiah began"                   | full       | RR isaiah_writing_lamplight (still crop; caps at 2 spec uses with #66 - resolve at spec pass, hero clip open is a clip use) | Bookend to beat 1 |
| 82 | 346.5-350.5 | KJV reprise "Who hath believed our report?"            | full       | R16 synagogue_listeners_lean (2nd crop)                                 | Sacred still |
| 83 | 350.5-354.0 | "The arm of the LORD is not a thing. It is a person."  | full       | R16C hand_reaching_closeup ($0 clip)                                    | Slam A PERSON (echo of #54) |
| 84 | 354.0-357.5 | "It has a face, marred more than any man's"            | full       | R16 cry_profile_dark (2nd crop)                                         |  |
| 85 | 357.5-360.5 | "It has hands, wounded for transgressions never his own" | full     | R16 pierced_hands_feet (2nd use, still crop)                            |  |
| 86 | 360.5-366.0 | "And it has your name in verse six."                   | full       | R16 hebrew_scroll_edge_light (macro; 3rd slug use - swap one earlier use to greek_ot_scroll at spec pass if the 2-use gate flags) | Writing still, dyncam only |
| 87 | 366.0-372.0 | KJV "we have turned every one to his own way - is yours, and mine" | full | RR us_under_cross_shadow_16x9 (2nd crop)                          | You in the frame |
| 88 | 372.0-378.0 | KJV "the LORD hath laid on him the iniquity of us all" | triptych_v | P916C grace_poured_sky (2nd) + P916C hands_of_light_open + P916C father_lamp_doorway | $0 columns; grace imagery |
| 89 | 378.0-382.3 | "Every way you turned that was your own - laid on him." | full      | R16 hung_by_arms (2nd crop)                                             |  |
| 90 | 382.3-385.9 | "Already carried. Already taken away."                 | two_v      | P916C stone_rolled_dawn (2nd) + P916C tomb_doorway_dawn (2nd)           | Columns |
| 91 | 385.9-391.0 | "You do not have to clean yourself up before you come" | full       | R16C kneeling_at_cross ($0 clip)                                        | HEARTBEAT starts building here |
| 92 | 391.0-396.6 | "wounded for YOUR transgressions, and bore them in your place" | full | RR nail_through_hand_16x9 (2nd crop)                              | dyncam only, never Kling |
| 93 | 396.6-400.4 | "The report is true. The arm of the LORD has a name."  | full       | RR risen_christ_seeking_16x9 (partial reveal crop)                      | Slow reveal |
| 94 | 400.4-403.6 | "His name is Jesus."                                   | full       | RR risen_christ_seeking_16x9 + KLING living light                       | HERO. Heartbeat STOPS DEAD at 400.4. Sacred still + living light only |
| 95 | 403.6-end   | "Have you believed the report?"                        | full       | hold hero (same clip), final word-timed caption, then silence           | No new image; let it land |

## 4. Counted totals and quote

Distinct visual sources: 75 (for 95 beats; ps22 used 79 for 99 - matched density)

| Bucket                                        | Count | Cost each        | Cost    |
|-----------------------------------------------|-------|------------------|---------|
| REUSE-16:9 ps22 stills (byte-identical)       | 26    | $0               | $0      |
| REUSE-16:9 ps22 inked clips (same aspect, $0 motion) | 15 | $0            | $0      |
| PANEL-9:16 shorts stills (vertical columns)   | 5     | $0               | $0      |
| PANEL-9:16 shorts Kling clips (vertical columns, $0 motion) | 17 | $0     | $0      |
| RE-RENDER-16:9 (same world + ref at 16:9)     | 4     | $0.05 x 1.3 rolls | $0.26  |
| FRESH-16:9 (new prompts)                      | 8     | $0.05 x 1.3 rolls | $0.52  |
| PAID Kling hero clips                         | 3     | 7.5 cr (~$0.65)  | $1.95   |
| TOTAL                                         | 75 sources / 3 paid clips |  | **~$2.73 (22.5 Kling cr + ~$0.78 BytePlus)** |

Headroom: +1 Kling re-roll + 2 extra still rolls = ceiling ~$3.50.
Compare: original Baroque build class ~$23/episode. This rebuild is ~88% reuse by source count and ~97% $0 by beat.

The 4 RE-RENDERs: isaiah_writing_lamplight, nail_through_hand_16x9,
us_under_cross_shadow_16x9, risen_christ_seeking_16x9.
The 8 FRESH: jerusalem_700bc_wide, servant_exalted_light, sheep_astray_hills,
lamb_to_slaughter, jesus_silent_accusers, israel_servant_nation,
chariot_desert_road_wide, philip_eunuch_scroll.
The 3 PAID Kling heroes: beat 1 (Isaiah lamplight, film open), beat 36 (lamb to
the slaughter), beat 94 (risen Christ, "His name is Jesus" close).

## 5. Risks / flags

1. TOPICAL-FIT EXCLUSIONS (ps22 bank): all David-world stills (david_*,
   shepherd_boy_sling, jerusalem_night_lyre, old_king_hands_rings) and ps22
   thread-specific frames (worm_*, dogs_encompass, lion_*, disputed_word_marks,
   the_turn, risen_hero_come, livingpage_poster, alexandria_harbor_night) are
   NOT used. Isaiah's prophet world is its own re-render, not David's.
2. HERO SCOPE: ps22's risen_hero_come stays with ps22. Isaiah 53 gets its own
   full-bleed close hero (risen_christ_seeking re-rendered at 16:9 with the
   JESUS/face_on_cross ref). asset_index reuse_scope=hero rows are never
   crossed between pieces.
3. DOCTRINE-SENSITIVE FRAMES: beats 10-11 ("God Himself pointing" / the_LORD
   speaking) and 69 ("it pleased the LORD") must never depict the Father -
   light, sky, darkness only. Beats 41/43 (Israel as servant) must be dignified
   exile imagery, no caricature. Red-letter/the_LORD beats are sacred stills
   (perfectly still, no slam stacking).
4. WRITING STILLS NEVER ANIMATE generatively: hebrew_scroll_edge_light,
   greek_ot_scroll, two_scrolls_compared, quill_ink_drop, prophet_scroll,
   scholar_hand_on_text, and both scroll crops in M5. Dyncam pan/push only;
   letters garble under Kling.
5. NO FRESH BLOOD ON ANY KLING-BOUND FRAME (hard rule - Kling regenerates blood
   on wound-marked palms): lamb_to_slaughter hero must be a clean, unmarked
   lamb; risen_christ_seeking hero shows healed scars only. nail_through_hand_16x9
   is dyncam-only and is never sent to Kling.
6. CROWN OF THORNS on every cross frame - inherited automatically from the
   gated ps22/cluster-1 reuses; the only fresh Christ frames are pre-cross
   (jesus_silent_accusers - no crown, correct for the trial scene, document in
   its fact card) and the risen hero (scars, no crown - flag to /bible-check).
7. ASPECT RULE AS UPGRADED: 9:16 stills AND clips serve VERTICAL COLUMN panels
   only (triptych_v / two_v columns, ~5% crop); never full-bleed 16:9, never
   landscape quad cells. All full-bleed beats are 16:9 sources.
8. MAX-2-USES: beats 81/86 note two slugs that touch 3 planned appearances
   (isaiah_writing_lamplight, hebrew_scroll_edge_light) and beat 53 reuses
   body_laid_in_tomb a 3rd time; the spec pass must dedupe against the 2-use /
   never-2x-full-bleed gate (bank depth: ~200 unused 9:16 stills + 40 unused
   ps22 stills makes swaps trivial).
9. AUDIO TAIL: alignment ends 405.02s; ffprobe the locked narration.mp3 for the
   true total before setting spec "total" (ps22 pattern). If an SFX/score bed
   is added later it follows the standing $0 /sfx stage, unchanged audio.
10. CHARACTER REFS: every peopled fresh/re-render still binds a ref -
    ISAIAH (beats 1/66/81), JESUS (36 by type, 37, 92-94), ETHIOPIAN_EUNUCH
    (57/58/60/61), PHILIP the evangelist (60/61), ISRAEL_NATION (41/43),
    SHEEP_FLOCK (30/31). All already exist in ref_library/characters/.
