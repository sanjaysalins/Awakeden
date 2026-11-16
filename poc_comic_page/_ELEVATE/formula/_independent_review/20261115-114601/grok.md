# Independent review — grok (OK, 313s)

I'll check the plan against the real files and tools it names, then red-team the formula itself.The plan should not be built as written. It freezes one owner's hunch into a factory, and several of its rules already fail the film they are copied from.

The lettering split and the "do not wire `cli_pipeline` yet" call are sound. The DNA, the language spec, the doodle kit, and steps 1–3 are not.

## Feasibility (checked against the repo)

The source file, the 38.0 s length, and the builder are real. `poc_comic_page/_ELEVATE/build_s32.py` sets `T.TOTAL = 38.0`, composites 1080×1920, and draws English as PNG overlays. `publish/captions.srt` exists. The named doodle devices and `_remotion/` exist. `cli_pipeline.py` exists, and it is a different product: `TODO.md` still has "Wire the shorts pipeline" open. Rejecting option B is right. The reason in the plan ("locks the formula before it is proven") is the weaker reason. The stronger one is that this short was not made by that engine.

The plan treats a word-free master as new work: "Fix: a word-free master film + a separate swappable lettering layer." That layer already exists. `build_s32.py` writes `work/s32_lett/p00.png`… and a `hook.png`, then `T.compose` overlays them. Clips are already clean. What is missing is a switch that leaves those PNGs off, plus a real SRT. A new template duplicates `pill_tabs` and `compose`.

"The pill sits where platform subtitles render" does not match the code. `pill_tabs` starts the card at `y0 = 1000` on a 1920-tall frame. The bottom 25% begins at y=1440. A 3-line pill ends near y=1246. The bottom band is already empty. The live bug is two copies of the same English words (center pill + bottom SRT), not a shared rectangle. "Bottom ~25% kept clear" does not fix that, and moving the pills "up" would put them on the faces. Those close-ups are the look (`cy` about .42–.55, zoom 1.3→1.5).

"$8–12 (a sibling short cost ~$8.55)" is not sourced. The board note for this film is voice about $0.08, because it reused the parent Kling clips. A new story with new stills is a different bill. The calendar doodle and the split screen are new pictures, so steps 1–4 are not "~$0" if those ideas are in the pilot.

The film is locked (`LOCKED.json`, 2026-11-09). Step 4 says "rebuild the Thief film on the new template" and never says the locked mp4 and the publish pack stay untouched.

## The formula does not match the film

"Hook in 0–3 s" and the gate "hook <=3 s" fail the source. In `build_s32.py` the first spoken span is `h=(0.0, 3.752)`. The title card is a separate overlay, 0.0–2.2 s, on top of that line. A template with this gate would reject the film it is trying to copy.

"8 lines, ~85 words" is the gloss grouping. The builder uses 11 pills plus the hook card. Counted from the locked block, the words are about 74. The landing is three cards (`Not someday. Today.` / `Not just remembered. With Him.` / `You can ask Him to remember you too.`), then a 3 s garden hold from 35.0–38.0. The slow push-in (the `z0, z1` pairs) is not in the DNA at all. That zoom is a large part of the look.

"3 voices" is wrong. The audio folder has four turns: narrator, mocker, penitent, Jesus. Many passages have no spoken line from Jesus. A formula that requires "narrator + the human character(s) + Jesus" cannot cover those stories, and it will invent a Jesus line to fill the slot.

"KJV quotes verbatim" is only half true. The Jesus card is "To day shalt thou be with me in paradise." The parent script in `build_tp.py` still has the full clause, "Verily I say unto thee, To day…". The short drops the first half. "Two criminals" is also a gloss (KJV: malefactors / thieves). The last line, "You can ask Him to remember you too.", is not in the text. The plan then locks "one soft invitation" as DNA for every future film. That spreads an extra-biblical closing line into the series. The gates in step 3 do not include a quote-versus-gloss check. `bible_gate.py` and `bib_validate.py` already exist and are not named. Neither are `check_landing_hold.py`, `caption_slop_check.py`, `cli_publish.py`, or `corpus_diversity.py`.

Step 3's gates are "length, hook <=3 s, clear bottom zone, no baked English, 3 s hold." The house rules in the footer (verbatim text, lands on Jesus, packaging, global-audience panel, five guardrail questions) are not steps. A footer gets skipped.

## Over-build, and the order is backwards

Option A builds a Formula Card, a doodle kit, and a generic "words in, film out" template before any proof. The hard part of a new story is clip choice, cast, and timing. Those are hand-set in `build_s32.py` (`SH`, `PL`). The $0 pilot reuses the old clips, so it never tests that hard part. Then step 5 hits it on a paid story.

"Fable watches the film cold" cannot happen from this brief. The brief already contains "Proposed DNA." One seat then writes the card that every later film copies. House rule is a blind panel (Fable plus the other seats), not one model legislating the format.

"Also: read the real analytics before copying" is a footnote. Step 1 still runs first. There is no metric, no threshold, and no kill rule if the owner prefers the old film. "Loved" is still only the owner's report, which the plan itself admits.

"Repeat" and "elevate" are one project here. Same length, same hook, same pairs, plus a new doodle layer, plus deleted pills. If the new cut wins, you will not know which change did it.

## (1) What is missing

- A blocking analytics read (3-second hold, average view, replays) with a number that stops the work.
- A rule that the locked mp4 and `publish/` are not replaced.
- Quote versus gloss tags. The code already has them (`who`, `ref` on quote pills only). The formula drops them.
- The fourth voice, and a path for passages where Jesus does not speak.
- A partial-verse rule. Foreign public-domain text must clip the same words, not restore the full verse.
- Who translates the narrator gloss. Scripture machine-translation is banned. The gloss has no owner.
- Voice cost. A new English story needs its own quoted ElevenLabs ask. The plan prices clips only.
- Platform split. `publish/` already has YouTube, TikTok, Instagram, and Facebook. One SRT does not serve all four. YouTube auto-translate can stack on an uploaded SRT.
- A single-variable test, a kill rule, and a second hand-built story before any template.
- Blind panels on the formula and on the doodles. Step 1 is one seat. Step 2 is "a mock page."

## (2) What I would do instead

Do not design a formula yet.

1. Pull the YouTube numbers. If the 3-second hold is ordinary, stop. The vibe is not a template.
2. Duplicate the film beside the locked master. Same clips, same audio, overlays off, one new SRT. Owner compares that pair only.
3. If that wins, add one doodle on one shot, using `compose` and `to_screen` in `build_tp.py`. No new art. No split screen. `build_w3.py` already records the owner direction as full-bleed, no splits.
4. Run the existing gates on that copy: `bible_gate.py`, `caption_slop_check.py`, `check_landing_hold.py`, plus one blind global-audience pass on the film only.
5. Make the next story by hand, same shape only where the text already has it. Template a piece only after two films shared it. Clip pick stays manual.

## (3) Biggest staleness risk

The closed device list. The plan names five doodle ideas and then says "3–5 doodles per film." Film 1 uses the whole menu. Film 2 repeats it. Viewers learn that a calendar snap means "not someday" and an underline means "Jesus is speaking."

Worse, "two contrast pairs taken from the text's own words" is a property of this passage (mocker/asker, someday/today). Locked as DNA, the next text gets a fake pair painted on, plus the same soft invitation. The films start to sound like one script with the nouns swapped. Nothing in the gates retires a device or checks `corpus_diversity.py`.

## (4) Language and SRT pitfalls the plan skips

The "max ~32 chars" and "min 1.2 s" rules fail this film's own `publish/captions.srt`.

- Shortest spoken line in the locked block, "He asked to be remembered. Someday.", is 35 characters. The Jesus fragment is 42. "Lord, remember me…" is 52. The landing sentence is 84. Zero of the eight lines fit in 32 characters.
- The published SRT already breaks the 1.2 s rule: "Why?" is 0.33 s, "Him." is 0.30 s, "Today." is 0.49 s, "With Him." is 0.47 s.
- It also orphans the verse: cue 8 ends on "into thy" and cue 9 is "kingdom." for 0.40 s. Copying that breaker is a bug, not a standard.
- English audio is the clock. The Jesus card lasts about 4.1 s (22.45–26.5). A public-domain line that restores "De cierto te digo" / "Je te le dis en vérité" does not fit that window. "~25% longer" is a slogan. This verse is not 25% longer. It is a different sentence if you translate the full verse while English keeps the clip.
- "To day" is two KJV words. A caption pass will "fix" it to "Today" and fail a verbatim check.
- "Verse chips as numbers only ('23:43')" drops the book. "23:43" is not unique across the Bible. Speaker tabs ("A MOCKER", "THE OTHER THIEF", "JESUS") stay English. The plan never translates them. The hook card "PARADISE FOR A CRIMINAL?" is also burned English, and it is the first 2.2 s. A word-free master deletes the thing most likely to be the hook.
- `pill_tabs` measures width with `textlength` and the Kalam font. That path does not shape Arabic, Hindi, or Thai, and a CJK "32 characters" is a different budget. RTL flips the tab side (speaker is the left chip, verse is the right chip).
- Burned lettering plus an SRT is still two texts. Pick one per platform. Burned type for a language people watch with sound off. Sidecar SRT when the platform draws its own captions. Not both.
- No characters-per-second cap, no two-line cap, no "do not break before a noun" rule, no UTF-8 rule, no one to approve the gloss translation.

## (5) Doodle and motion-graphic pitfalls

- A circle "around the thief's face" has no face box. The shot is a moving zoom (`z0`→`z1`). A screen-space circle drifts off the face within one shot. `to_screen()` already converts an anchor through that zoom. The plan does not use it.
- An arrow "from his cross to Jesus" has nowhere to land on a close-up. Only two shots are wide, about 1.3 s and 1.8 s (`two_thieves_wide`, `golgotha_hill_wide`). The other twelve are one face or one symbol.
- "Split screen mocker turns away / thief turns in" brings back a layout this look already dropped (`build_w3.py`: "full-bleed (no splits)"). It also needs new frames. It is not a $0 overlay.
- A calendar page is new art, and it is not word-free. Calendars mean different things in different countries. It draws the narrator's "someday/today" gloss, so the picture adds a claim.
- A circle on a face can read as "guilty" or "target." An arrow into Jesus can read as blame. No test of that reading is in the plan.
- `marginalia` is a word labeler. Listing it beside a word-free rule invites the device you just banned. `grid-choreography` fights full-bleed. `line-boil` on a push-in shimmers. `CLAUDE.md` already says those effects stay selective and spread thin. The plan lists the kit and sets no shot budget.
- Two compositors. The film is ffmpeg overlays in `compose()`. Pulling doodles through `_remotion/` is a second pipeline for the same pixels.
- Five ideas and a quota of 3–5 means no spare idea for film 2.

## Cost

Steps 1–4 are only ~$0 if the pilot is overlays on the existing clips and nobody regenerates art. The doodle section breaks that. The new-story clip quote is unfinished: no voice quote, no stills quote, no "stop if the hand-built copy loses." Spend is not justified until the word-free copy beats the locked film on a number you can read.

VERDICT: REVISE
TOP FIXES:
1. Stop the template. Read the real retention numbers first, then A/B one word-free copy beside the locked film, same clips and audio, locked mp4 left untouched.
2. Rewrite the language rules against publish/captions.srt and pill_tabs: one text system, a characters-per-second cap, quote-versus-gloss, the same clipped verse in every language, and a font path that can shape non-Latin scripts.
3. Drop the closed 5-doodle kit and the split-screen/calendar ideas. If a doodle survives the A/B, draw one of them with the existing overlay and to_screen(), and retire it after a few films so the next story cannot reuse the someday/today pair.
