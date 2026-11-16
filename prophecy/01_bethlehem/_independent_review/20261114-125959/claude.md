# Independent review — claude (OK, 150s)

The review is done. I checked the plan against the real repo: the word times, the audio length, the fonts, the two D frames, and the locked `/livingpage` standard.

## Findings

**1. It skips the locked comic standard (biggest issue).**
- The plan says "one Remotion comp `ProphecyBethlehem`" with new page turns, riffle, dive and gutter light, all built from scratch.
- The `/livingpage` skill says it is for "EVERY motion-comic finishing pass, long or short". Its contract is `F:\slk\PycharmProjects\JesusInTheBible\v2\LIVINGPAGE_STANDARD.md`, and section 7 covers 9:16 shorts.
- None of its gates appear in the plan: the `--lint` choreography gate, `still_validate`, the `ship_gate.py --check` still ship gate, the DoD json, or the two-way doctrine bar check.
- So the plan rebuilds slams, takeover camera and sacred stillness that already exist, and drops the gates that go with them.
- Note: `build_livingpage_16x9.py` and `caption_layout.py` are not at the repo root. Find where they live before you either reuse or replace them.

**2. The lettering goes against the owner's own pick.**
- The comic bake-off memory (2026-11-09) says future comic episodes use "Mockers-look pills (translucent)… NOT Bangers balloons/splits". The owner wanted see-through boxes because solid ones were "hiding great clips".
- The plan uses solid cream boxes with 8 px hard shadows, solid white balloons, and Bangers for name tags, time slabs and verse chips.
- That is the losing look, so it needs the owner's OK before anything is built.

**3. The gold-word proof does not prove anything.**
- The plan calls the scribe's "In Bethlehem of Judaea" balloon "the fulfilment balloon". But in Matt 2:5 the scribe is only quoting Micah again.
- Linking a prophecy to a quote of itself proves nothing. A prophecy-series proof device should land on the event, which is the birth in panel 4A.
- Also open:
  - Where does the pinned gold word sit during pages 4 and 5 (23.3 s to 31 s)?
  - Is "Bethlehem" at 42.54 s (7A, "He did not begin in Bethlehem") gold too? That would break the "gold only the promised word" rule, and the plan doesn't say.

**4. The landing hold falls short of 3.0 s (INV-26).**
- The voice ends at 48.50 s and the file is 48.52 s long.
- 51.5 s at 30 fps is 1545 frames, which leaves a 2.98–3.00 s hold. Set it to 1546 or more frames and run `check_landing_hold.py`.

**5. Too much to read at once, against the plan's own rule.**
- Risk 3 says "one box at a time". But panel 2A shows three text items in 1.5 s: the name tag at 9.18, the chip at 9.86 and a box at 10.68. They come right after the time slab, which holds until 9.0.
- Page 1 has three captions plus speed lines in 7 s.
- For a second-language viewer this is the likeliest fail, and the plan only checks it after assembly.

**6. Clip model choices go against locked tiering.**
- C03 puts Seedance on Micah with "cloak moving… mouth open mid-word, hand raised". The locked tiering says Seedance invents motion on action, and gestures go to Kling.
- C04 asks Kling to hold a cued pose for about 9 s of a 10 s clip, with "pen never touches". That is a long hold that invites drift, and 10 s costs about double.
  - Better: split 3A into two shots, in line with the owner's "render more shots" rule.
- C04 (9.5 s of 10 s) and C08 (4.5 s of 5 s) leave almost no slack.
  - The fallback "land 0.4 s later" breaks word sync on the panel-land beats.

**7. Reused stills have unclear steps.**
- S04's "one edit: remove the white speed lines" names no tool or cost. Is it a $0 paint-out or a paid model edit?
- S05 crops "keeps [ox and donkey] at the edge or out". If they stay at the edge, they are still in the film. Decide: out.
- The D frames are 1296×2304 look tests and have not been through any still ship gate.

**8. The Herod's hall ref is weak.**
- R4 is chained from S01. But S01 is framed "seen from behind the scroll", so the hall may hardly show.
- That makes S07 and S08 wait on S01 and gives them a poor reference.

**9. Things the build needs that the plan doesn't have.**
- **Page turn:** "page lifts… curls" using CSS `rotateY` will give a flat card flip, not a curl. Test it at $0 first or call it a flip.
- **Sound:** there is no sound or score plan. The plan uses a paper sound, booms and 4 dB dips, but names no score source and no `/sfx` step.
- **Packaging:** the Packaging Card is missing, though the house rule says to design it with the plan.
- **Panel checks:** the 5 guardrail questions are not in the gate list.
- **Font:** Palatino Linotype is a system font, not a bundled one. The render may come out different on another machine.

**10. Small accuracy point.**
- 4B shows riders "toward a bright star" before they reach Jerusalem. Matthew only says the star "went before them" after they leave Herod (Matt 2:9).
- Have a Bible seat check this; it is minor.

What is good: there is no spend, clips are trimmed only, the sacred-stillness contrast is a strong idea, the cross is far off, the empty tomb has no stone (following the Kling rule), and the scroll text is typeset rather than drawn by the model.

VERDICT: REVISE
TOP FIXES:
1. Rebuild the plan on the locked `/livingpage` standard (9:16 section, its lint, still ship gate and DoD json). Only add the new pieces (riffle, gold word, scroll card), and add them as named extensions.
2. Switch the lettering to the owner-picked Mockers look (see-through pills, Kalam, gold chip), not solid boxes with Bangers, unless the owner OKs the change. Cut the text load to one item at a time (fix 2A and page 1).
3. Make the gold word land on the fulfilment (the birth in 4A), not on the scribe quoting it again. State where it sits from 23 s to 31 s and at 42.5 s. Set the end to 1546 or more frames for a true 3.0 s hold. Move C03 to Kling and split C04 into two shots.
