# PLAN: turn one well-loved short into a repeatable, elevated formula (for red team)

## Goal (owner's words)
"My audience has loved the look and feel and length of 'The thief on the cross: why Jesus promised him paradise | Bible'. How can I get Fable to help me build a repeatable pipeline to take that and elevate it, and make it into something I can keep doing over and over again? Keeping the topic, the length, the hook etc. I will lean heavily also on motion graphics and doodles to elevate it. This is for a global audience in many languages using SRT, so consider that too."

## The source film (facts)
- File: batches/cluster_01_cross/today_paradise_short32/visual/today_paradise_short32_final.mp4, 38.0 s, 9:16.
- Builder: poc_comic_page/_ELEVATE/build_s32.py ($0 assembly from existing Kling clips of a longer parent piece). Captions: publish/captions.srt (English).
- Look: bold-ink colour comic (graphic-novel) clips, full-bleed, slow push-ins; faces in close-up; a big hook title card "PARADISE FOR A CRIMINAL?" for the first 2.2 s; a translucent rounded "pill" with each spoken line BAKED IN (English), with a speaker tab ("A MOCKER", "THE OTHER THIEF", "JESUS") and a verse chip ("LUKE 23:43"). Ends on a paradise-dawn garden image, 3 s landing hold.
- Locked words (KJV quotes verbatim):
  - [narrator] Jesus promised paradise to a criminal. Why?
  - [narrator] Two criminals were dying on crosses beside Him.
  - [mocker] If thou be Christ, save thyself and us.
  - [narrator] One wanted off the cross. The other asked for very little.
  - [penitent] Lord, remember me when thou comest into thy kingdom.
  - [narrator] He asked to be remembered. Someday.
  - [jesus] To day shalt thou be with me in paradise.
  - [narrator] Not someday. Today. Not just remembered. With Him. You can ask Him to remember you too.
- YouTube title: "The thief on the cross: why Jesus promised him paradise | Bible".
- Evidence it was "loved": owner's report. Retention / 3-second hold / share numbers have NOT yet been read.

## Proposed DNA of the film (my analysis)
- Length 38 s, 8 lines, ~85 words.
- Hook in 0-3 s is a paradox question.
- Twist built from two contrast pairs taken from the text's own words (mocker vs asker; "someday" vs "today").
- 3 voices: narrator + the human character(s) + Jesus.
- Landing: short echo of the twist + one soft invitation. 3 s hold.
- Look: bold-ink comic, full-screen clips, close faces.

## Identified problem for global/multi-language
English lines are baked into the picture as pills. With a non-English SRT on, viewers see two sets of text, and the pill sits where platform subtitles render. Fix: a word-free master film + a separate swappable lettering layer per language; bottom ~25% kept clear for subtitles.

## Doodles / motion graphics
Every doodle must read without words. Ideas: an ink circle drawn around the thief's face as he speaks; ink arrow from his cross to Jesus; a far-off calendar page ("someday") snapping to a close sunrise ("today"); split screen mocker turns away / thief turns in; ink underline beneath Jesus' words. Rule: 3-5 doodles per film, one idea each, not on every shot. (Repo already has many $0 deterministic devices: annotators-circle, marginalia, impact-burst, ink-transition, grid-choreography, line-boil, etc., and a Remotion project _remotion/.)

## Languages
- Bible quotes in other languages from a public-domain translation (e.g. Spanish Reina-Valera 1909, French Louis Segond 1910); never machine-translate Scripture.
- SRT lines short (max ~32 chars), min 1.2 s each; expect Spanish/German ~25% longer.
- Verse chips as numbers only ("23:43").
- Later, paid: dubbed voices per language (separate ask + price).

## Options offered
A (recommended): Fable designs the formula once, Sonnet builds the template.
 1. Fable watches the film cold and writes a Formula Card.
 2. Fable designs the doodle kit + word-free layout, shown as a mock page.
 3. Sonnet builds one template (episode words + timings in, film out) with gates: length, hook <=3 s, clear bottom zone, no baked English, 3 s hold.
 4. Pilot: rebuild the Thief film on the new template from its old clips ($0); owner compares old vs new.
 5. Then one new story end to end through the normal words-before-money gates.
 Cost steps 1-4 ~$0; a new story's clips ~$8-12 (a sibling short cost ~$8.55), quoted before spend.
B: wire into the full engine (cli_pipeline) now. Slower; locks the formula before it is proven.
C: a checklist, build by hand. Cheapest; no real lift.

Also: read the real analytics before copying.

## Standing house rules this plan must respect
Words before money (no paid step without its own quoted ask); blind panels with an independent Fable seat; global audience / simple words; KJV verbatim in English; every piece lands on Jesus; no AI wording in public text; owner is dyslexic (short, visual review pages); 5 guardrail questions on every episode.
