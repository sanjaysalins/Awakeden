# Red team C: Swirls ep02 The Ashes That Made Clean (2026-11-16)

old: F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_02_ashes_that_made_clean\THE_ASHES_BOOK_final_sfx.mp4
new: F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_02_ashes_that_made_clean\uplift\ep02_uplift_final.mp4
Frames: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\ (1 fps both films as sheet_0..10.jpg, top row = old, bottom row = new; full-res grids g_*.jpg; zooms z*.jpg, d_*.jpg)

## VERDICT: NEEDS PAID FIX (do not lock yet; do not go back to old either)

## Is the new one clearly better than the old?
Yes in design, no in finish. New has 12 shots instead of 6, each picture now matches its spoken line, the old "smoke puffing out of the grave" is gone, and the landing "He touched what makes us unclean" now has its own real animated page (F05). But 3 of the 7 new pages bring new defects the old film did not have (a different-looking man, a walking glitch, a garbled doodle).

## Checks that PASS
- Audio unchanged: stream-copy MD5 identical old vs new (bac739ff0d413796b762109e3e10139e), decoded MD5 identical too. Same length 61.93 s, 1858 frames.
- No stretched clips: all 7 new clips are longer than their slots (3.04/6.04/6.04/8.04/4.04/4.04/9.04 s vs slots 2.93/5.97/5.93/7.0/3.67/3.4/8.5 s); cut script is trim-only 1.0x. No mirror/boomerang signature in frame-diff test. Hard cuts at 3.93, 7.87, 10.8, 16.73, 22.7, 28.63, 32.3, 39.3, 46.2, 49.6, 58.1.
- Landing hold: last word ends 58.90, file ends 61.93 = 3.03 s.
- No burned captions added. Storyboard-page look kept. Hero F05 is a real animated clip.
- KJV: nothing on screen contradicts Numbers 19:11-12, 17-19 or Hebrews 9:13-14 / 13:12 (clean person, hyssop, water, third + seventh day, outside the camp / outside the wall are all right).
- Marks: box on "the burning" (F01), 7 tally strokes (F02C), circle on "stain" (F03), underline on "unclean" (F05) are tied to the spoken word, not on any face, do not cover captions.

## Defects, most severe first

1. **16.7-22.7 s (F02C) and 28.6-32.3 s (F03A): the unclean man is a different person.** Rule: recurring people keep the same face and clothes. F02 / F02B / F03 / F04 = short black hair, clean shaven, short-sleeve cream tunic. F02C = longer brown hair, long-sleeve tan robe. F03A = older, brown mid-length hair, stubble, long-sleeve robe, and a more photo-real drawing style than the rest. F02D and F05 put him in a BROWN tunic (F05 also adds a leather belt). A newcomer can read this as 3 different men. NEW in the uplift (old film had one consistent man). Fix: paid. Redraw F02C + F03A from the F02 still as north-star ref and re-animate; recolour tunic on F02D/F05 in the same pass. Rough $3-6, not verified against a quote. CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_G.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_H.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_C.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_M.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_A.jpg

2. **22.7-26.5 s (F02D): the clean man walks across the panel in front of the seated man, hides him, his feet smear/tangle (about 24.2-24.6 s), and the hyssop ends up poked into the seated man's face/mouth (about 25.8-26.2 s).** Rules: no invented content / reverent, not comic; also the text is "sprinkle", and no sprinkling is shown here. The blue ink stripe on the jug travels with the jug the whole shot (ink motif moving, clearly visible). NEW. Fix: paid, one re-animate of F02D with the man already standing still beside him and only the hyssop hand moving (rough $0.5-1). CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\d_f02d.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_A.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_B.jpg

3. **58.1-61.9 s (back cover): the blue/gold ink thread on Jesus' wrist whips around - loop, then S-curve, then straight.** Rule: Swirls ink motif must never be animated; this is far beyond "small movement". Carried over from the old film (there it ran 11.5 s, now 3.8 s). Fix: free - patch the thread area with a static crop from back_cover.png (wrist is nearly still), or use a calmer take. CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_K.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\sheet_9.jpg

4. **About 25.5-28.6 s (F02D tally doodle): reads as garbled letters "HOH IOI".** Seven tally strokes with thick ovals drawn over stroke 3 and stroke 7. Rule: marks never cluttered, never adding words not spoken / no garbled text. NEW. Fix: free - redraw as plain strokes with one thin ring, or just darken strokes 3 and 7. CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\zt.jpg, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_B.jpg

5. **About 21-22.7 s (F02C): a dark furry tail-like shape grows out behind the seated man.** The cloak end turns dark and stretches. Rule: no objects appearing. NEW. Fix: free - paint the static ground patch from an early frame over that corner. Would be solved anyway by fix 1. CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\zc.jpg

6. **16.7-22.7 s (F02C): eight stones under the label "seven stones" / "unclean seven days".** Rule: right number. NEW. Fix: free paint-out of one stone, or in the fix-1 redraw. (F02C is also the stillest shot, mean motion about 1/10 of the others - reads close to a still.) CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\zstones.jpg

7. **10.8-16.7 s (F01): the blue ink line inside the smoke bends and changes shape with the smoke.** Ink motif moving, clearly visible but less than the back cover. Carried over from old. Fix: free patch is hard here (smoke moves); accept, or paid re-animate about $0.5. CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_J.jpg

8. **About 53.5-55 s (F05): the man's right hand flips and briefly reads as a malformed fist before it clasps Jesus' hand; about 56.5 s the sleeve opening turns into a flat black hole.** Rule: no invented content. Short, but it is the hero shot. He also stares at the camera, not at the hand. NEW. Fix: accept, or paid re-animate about $1. CONFIRMED: C:\Users\sanjay\AppData\Local\Temp\rt_ep02\d_f05.jpg

9. **43.2-44.9 s: "the blood of Christ" is spoken over the Old Testament sprinkling page (F04); the cross page (F04B) only arrives at 46.2 s.** Rule: picture helps a newcomer follow. Fix: needs a longer F04B clip (have 4.04 s, need 6.4 s) = paid about $0.5; or accept. CONFIRMED by cut times + srt.

10. Small, accept: F03A mouth moves as if he is speaking and a hair lock pops out at 32.2 s (C:\Users\sanjay\AppData\Local\Temp\rt_ep02\d_f03a.jpg); F02B sketch panel "rubbing" hands blur into a finger blob (C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_C.jpg); F04B city wall looks like a medieval castle (SUSPECTED era issue, C:\Users\sanjay\AppData\Local\Temp\rt_ep02\g_F.jpg); F01 red heifer has horns and reads as a bull (old still); back-cover baked text "Ready to be made clean?" differs from spoken "Ready to let Him make you clean?" (old).

## Top 5 for this film
1. Different man on F02C and F03A, brown tunic on F02D/F05 (paid).
2. F02D walk-across: feet smear, hyssop in the face, no sprinkle shown (paid).
3. Back-cover ink thread whipping (free patch).
4. F02D tally doodle reads as garbled letters (free).
5. F02C dark "tail" + eight stones (free, or gone with fix 1).

Not done: I did not listen to the audio (hash check only), and I did not look at the builder report, gate_report.json or _REVIEW.html. Cost numbers are rough guesses, not quotes.
