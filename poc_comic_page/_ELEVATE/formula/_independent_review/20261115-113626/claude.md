# Independent review — claude (OK, 143s)

**Red-team review: the plan to turn the Thief short into a repeatable formula**

I checked the plan against the real files: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\build_s32.py`, `build_w3.py`, `build_tp.py`, the English captions.srt, and the parent clips folder.

## Feasibility and false assumptions

1. **"English lines are baked into the picture."** This is false at the build level. In `build_s32.py`, the pills are separate PNG overlays (`PL` → `W.pill_tabs` → `T.compose(..., ov)`). The clips themselves have no text. A word-free master already costs $0: just run `compose` without `PL` and the hook card. Plan step 2 ("Fable designs the word-free layout") is solving a problem that does not exist.
2. **"The pill sits where platform subtitles render."** This is not what the code shows. `pill_tabs` puts the pill at y0=1000 of 1920, about the vertical middle. The fix, "keep the bottom ~25% clear for subtitles", is also wrong. The bottom ~20% is where Shorts, TikTok and Reels put their own buttons (title, channel name, likes), and captions draw just above that. You need a measured safe zone for each platform, not a guessed 25%.
3. **The source film fails its own proposed gate.** The gate says hook ≤3 s. But the hook line ends at 3.71 s ("Why?" runs 3.38–3.71 in captions.srt).
4. **The source captions.srt breaks the plan's own subtitle rule** ("min 1.2 s each"). It has stray single words split onto their own cues:
   - "Him." lasts 0.30 s.
   - "kingdom." lasts 0.40 s.
   - "Why?" lasts 0.33 s.

   Any template that copies today's SRT step carries this defect into every language.
5. **The cost model is built on a cut-down.** S32 is a $0 cut-down that reuses about 14 clips from the parent piece `today_paradise_luke2343`. A new story has no parent clips. It needs about 14 fresh shots, each longer than its slot, because the owner's rule bans freeze, boomerang and zoom fill. The "$8–12" figure leans on one sibling. The Bartimaeus memory note lists about $13.69 for the woman-at-the-well short. Re-quote from the real shot count.
6. **There is already a composer to reuse.** Memory records a "Living Comic machine" with an `episode.json` composer and 8 gates. `build_s32.py` is also 51 lines with every number hard-coded (`S`, `SH`, `PL`). The template should generalise `build_s32.py` into `episode.json` in, film out. Step 3 should start from these, not from a blank page.

## (1) What is missing

- **Analytics come first, not as an aside.** Today they appear only as "Also: read the real analytics". With one film and only the owner's report, you cannot tell look from topic. "Thief on the cross" is a high-search topic. Compare S32 against its siblings that share the same look (Barabbas, Mockers, Thirty Pieces) on:
  - retention curve
  - swipe-away rate
  - traffic source (search vs feed)

  If the siblings did worse, the look is not the cause.
- **The distribution model is never chosen.** A YouTube upload is one file, so a "swappable lettering layer per language" means N separate uploads. That splits views, comments and the algorithm signal. The real choices are:
  - (a) one upload, English audio, no burned narration text, a human-made SRT per language;
  - (b) one upload with dubbed audio tracks via YouTube multi-language audio;
  - (c) a separate channel per language.

  Each one changes the whole template.
- **The hook card and speaker tabs are English too.** "PARADISE FOR A CRIMINAL?", "A MOCKER" and "JESUS" all disappear under a "no baked English" gate. That deletes the 0–2 s stake, the thing the owner says works. Each needs either a per-language version or a word-free visual stand-in, such as a colour or icon per speaker.
- **Who translates the narrator lines?** The plan covers Scripture (public-domain Bibles) but not the narrator's own lines. They need a native-speaker check. The twist must survive translation: "someday / today", "remembered / with Him", and the KJV spelling "To day".
- **Titles, descriptions and thumbnails per language.** The packaging rule and the PACKAGING-READY gate would apply once per language.
- **A gate for the hard-coded timings.** The shot cuts in `SH` are typed in by hand from English turn lengths. Any re-record or dub breaks them. Timings should come from the words.json alignment.

## (2) What I'd do instead

1. Read the analytics for S32 and 3 siblings. Write down which part actually earned the retention.
2. Generalise `build_s32.py` into `build_formula.py` + `episode.json`, reusing the Living Comic composer. Pills, hook and tabs become a text layer keyed by line id, read from `lines.<lang>.json`.
3. Pilot ONE language (Spanish, RV1909) on the Thief film at $0, with a native reviewer. Release it as SRT-only, then read its numbers before scaling.
4. Add 2 doodles to the Thief rebuild, not 3–5. Test with blind panel seats and real seed viewers, not just the owner's old-vs-new look.
5. Only then pick a new story, and only one that fits the formula naturally: a speaking human, a Jesus line, and two contrast pairs native to the text.

## (3) Risk the formula goes stale

- **Template phrasing.**
  - Hook: "X for a Y?" every week becomes clickbait.
  - Landing: "You can ask Him to … too" is the same tired call-to-action shape that memory `feedback_swirls_landing_fatigue` already flags.
- **Shoehorning stories.** Few stories naturally have mocker-vs-asker plus someday-vs-today within ~85 words. Forcing other stories into that shape will distort them. This breaks the "freshness = faithful depth" and "earned landing" rules.

  Fix: lock the timing and look only. Ban repeats of the same hook or landing sentence pattern, using narration_gate's stale-corpus check. Allow 1-voice and 2-voice variants.

## (4) Multi-language / SRT pitfalls not covered

- **Auto-translate.** YouTube auto-translates the English SRT, KJV quotes included. That is the machine-translated Scripture the plan bans. Upload human tracks for each target language.
- **Right-to-left languages** (Arabic, Hebrew, Urdu, Farsi): SRT direction marks and punctuation. A left→right arrow or split screen can read backwards to these viewers.
- **Scripts that need other fonts.** The 32-character limit does not fit CJK, Devanagari or Thai. These need different line-length rules, and the pill font (`BA.KAL`) probably has no glyphs for them.
- **Verse references.** The book name is dropped ("23:43"). Then the reference no longer says which book. Use the localised book name instead.
- **Small conventions.** Capitalised "Him", quote marks (« » / „ “) and number formats vary by language.
- **English audio + foreign SRT.** The 3-voice acting carries less, and the reading speed needed at 38 s for languages ~25% longer may go over ~17 characters per second.

## (5) Doodle / motion-graphic pitfalls

- **The circle around the face will slide off.** The clips are pushed in by `compose` (z0→z1, cx/cy). A static circle will drift off the face. It must follow the same zoom/pan maths. Also, the `annotators-circle` skill is built for words on flat verse cards, not faces in moving clips.
- **The "calendar page" doodle has two problems.** Paper calendars did not exist in the 1st century, and calendars are drawn differently across cultures. A calendar also needs numbers, which breaks "reads without words". Use the sun's position (far sun → rising sun) instead.
- **Reverence.** No ink marks on Jesus's face or on crucifixion frames. Add a sacred-frame no-doodle zone.
- **Owner history.** Memory says the owner turned down "clever" Python compositing 3 times (`feedback_simple_fill_over_clever`). That is a real chance the doodle layer cheapens the look the audience loved. Test 2 doodles before building a kit of them.
- **Safe zones and style.** Doodles must stay clear of the caption and UI zones. Their line weight must match the bold-ink comic style, not look like a stock vector arrow. Do not split doodle rendering between Remotion and ffmpeg without one clear owner.

VERDICT: REVISE
TOP FIXES:
1. Read the S32 vs sibling-shorts analytics (retention, swipe-away, traffic source) BEFORE designing anything. Pick the language distribution model (SRT-only vs dubbed multi-audio vs per-language uploads), because the template depends on it.
2. Drop the "design a word-free layout" step: the pills are already separate overlays in build_s32.py. Generalise build_s32.py into the existing episode.json composer with a lines.<lang>.json text layer. Replace the guessed "bottom 25%" with measured per-platform safe zones (the pill is at y=1000 today). Fix the hook gate, which the source fails at 3.71 s.
3. Fix the SRT step: no stray one-word cues (today's file has 0.3 s "Him."), human tracks per language to stop YouTube auto-translating KJV, rules for right-to-left and CJK scripts, and native review of the narrator lines. Pilot ONE language and only 2 doodles on the Thief rebuild, tested with blind panel seats and real seed viewers, before 3–5 doodles or a new paid story.
