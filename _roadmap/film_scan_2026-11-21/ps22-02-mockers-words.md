SLUG: ps22-02-mockers-words
STATUS: READY
VERDICT: FIX
FILLS: built by poc_comic_page/_living_comic/lc_compose.py, which PING-PONGS (forward, then reversed 1.5s tail, repeated) any clip shorter than its panel. Panels from episode_mockers.json (Y7): 0-8.2 golgotha_hill_wide clip 5.0s - reverse; 12.5-19.5 david_writing_psalm clip 4.0 vs 7.0 - reverse; 19.5-31.2 psalm_scroll_night clip 4.0 vs 11.7 - reverse (worst); 31.2-40.5 wagging_heads_close_v4 5.0 vs 9.3 - reverse; 44.4-56.3 face_on_cross 5.0 vs 11.9 - reverse (worst); 59.7-66.9 ninth_hour_darkness 5.0 vs 7.2 - reverse; 66.9-76.4 us_under_cross_shadow 5.0 vs 9.5 - reverse. 7 of 10 panels. (Found from the build code and clip lengths; not seen frame by frame.)
SLOP: 0-3 right thief has a head band that reads like a crown of thorns - low; city with red pitched-tile roofs under the cross - low
TEXT: 0-3 hook card "WHOSE WORDS ARE THESE?" not spoken (narrator says "Listen.") - mismatch; 12-19 gloss "DELIVER = RESCUE" - "rescue" is spoken ("let God rescue him") so ok; quote cards Matt 27:43, Ps 22:8, Luke 23:34, Matt 27:54 are spoken
END: hold=~3.0 (voice ends ~73.4, film 76.4) silent_end=yes (last 0.25s rms 0.0006)
FIX_IDEA: Paid ~5 new clips (the 11.7s and 11.9s panels need 2 each) or $0 shorten those panels to clip length (changes timing against the voice, so a new cut).
