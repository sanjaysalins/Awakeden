SLUG: isaiah-53-suffering-servant
STATUS: READY
VERDICT: FIX
FILLS: Engine = comic_engine._temporal (static clip shorter than slot = boomerang forward+REVERSE; directional = slow-mo). Reverse confirmed by pixel mirror test at 14.1 s (mirror diff 3.4 vs 22 forward). 12 beats / 30 panels are boomerang (slot 4.3-7.1 s, clip 4-5 s, so each plays forward then backward):
  0.0 s isaiah_writing_lamplight - boomerang
  9.1 s nail_through_hand, bowed_head_finished, body_laid_in_tomb (triptych) - boomerang x3
  64.7 s crowd_mocking, face_on_cross, look_up_faces - boomerang x3
  84.2 s face_anguish_closeup - boomerang
  107.9 s jesus_praying_close, bowed_head_finished, nail_through_hand - boomerang x3 (bowed_head and nail re-used from 9.1 s)
  137.2 s look_up_faces, risen_mercy_hand, hands_of_light_open - boomerang x3
  148.0 s lamb_to_slaughter - boomerang
  218.5 s tomb_stone_sealed - boomerang
  318.1 s stone_rolled_dawn, tomb_doorway_dawn, linen_left_lying - boomerang x3
  347.3 s cry_face_tears - boomerang
  371.5 s grace_poured_sky, hands_of_light_open, father_lamp_doorway - boomerang x3
  389.4 s cry_ninth_hour - boomerang
  Slow-mo over 1.15x (forward, not reversed): 298.1 s poured_out_bones x1.88; 308.7 s nations_streaming_wide x1.48; 347.3 s hand_reaching_closeup x1.31; 331.8 s finished_work x1.25 (also 292.5 s kindreds_bowing x1.11, 123.2 s x1.03)
  Ken Burns on still (dyncam, $0 camera move): 72 of 144 panels; 38 full-bleed beats = 155 s = 38% of the film (e.g. 4.3 s jerusalem_700bc_wide, 31.6 s convergence_on_cross 6.3 s, 40.1 s servant_exalted_light 6.9 s)
SLOP: NONE visible at 3 s sampling. Style is consistent comic look, no extra/missing people seen, no anachronisms (Roman helmet/spear/nails are right for the period). Low: 3 shots re-used 3x (risen_christ_seeking at the close - documented as designed).
TEXT: NONE. All 95 beat captions are condensed paraphrases of the spoken narration (checked against narration.spoken.txt); red-letter lines are the spoken KJV quotes. Note: captions are shortened, not verbatim.
END: hold=3.28 silent_end=yes (last word 405.02 s, film 408.30 s; audio fades smoothly to -82 dB over the last ~3.5 s; A/V durations match)
FIX_IDEA: Replace the boomerang panels with the existing forward clips trimmed to slot (or a fresh 8 s render for the 12 beats), $0 for trims where clip >= slot else about 12 new clips (the 3-panel beats could share one new clip); cheapest honest $0 option = shorten those 12 beats to the clip length (4-5 s) and absorb the 1-2 s per beat into neighbours.
