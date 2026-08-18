# Jesus-POV POC — Look and Live retold in Christ's own first-person voice

**Status: DRAFT script only. Nothing spent, no voice/visuals built yet.** Retargets
`poc_living_sketchbook/look_and_live/` (Numbers 21:8, "look, not effort") from third-person
narration into a first-person retelling spoken AS Jesus, addressed directly to "you" (the
viewer) — not literally named, per the user's call, so it stays a shippable format rather than
a one-off.

## Doctrinal anchor (why first-person is legitimate, not invented)

Jesus Himself made this exact comparison, in His own recorded words: **John 3:14-15** — "And as
Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up: That
whosoever believeth in him should not perish, but have eternal life." He is the one who drew the
serpent -> cross line, to Nicodemus, in the dark. That's the load-bearing fact that makes a
first-person retelling doctrinally sound rather than invented: we're not putting new words in
His mouth about the *meaning* — we're dramatizing Him telling the *story* He already, on record,
told about Himself. The "I told Moses..." framing for Numbers 21:8 leans on classical Trinitarian
doctrine (the Son as agent of the Father's acts, `opera ad extra` undivided) rather than claiming
a specific Numbers-21 Christophany — devotionally faithful, not dogmatically overclaimed.

## Draft script (~150 words, target ~60s)

> I didn't send a doctor. I sent a snake.
>
> The camp was dying of the very thing that bit them, and Moses lifted a bronze one on a pole
> at my word: **"...it shall come to pass, that every one that is bitten, when he looketh upon
> it, shall live."** Not a cure for the wound. Just a look at the thing that was killing them.
>
> Years later, a teacher came to me in the dark. **"How can these things be?"** he asked. I told
> him about that pole. **"...as Moses lifted up the serpent in the wilderness, even so must the
> Son of man be lifted up."** I meant myself. I meant the cross.
>
> You're still reaching for your own cure — your own fixing, your own effort. I hung mine in
> plain sight instead, shaped exactly like your curse.
>
> Look at what was lifted up for you. Look at me. And live.

**KJV sources, verified verbatim (elisions marked with a leading "..." per this project's own
convention):**
- Numbers 21:8 — "And the LORD said unto Moses, Make thee a fiery serpent, and set it upon a
  pole: **and it shall come to pass, that every one that is bitten, when he looketh upon it,
  shall live.**"
- John 3:9 — "Nicodemus answered and said unto him, **How can these things be?**"
- John 3:14 — "**And as Moses lifted up the serpent in the wilderness, even so must the Son of
  man be lifted up:**"

## What changes in emphasis, first-person vs. the original third-person cut

1. **Ownership, not report.** "I sent a snake" / "I told Moses" / "I hung mine" replaces "God
   put a bronze one on a pole" — the narrator no longer describes an act, He claims it. This is
   the single biggest lever available in this format and it's why it's worth the experiment.
2. **Direct address, not general appeal.** "You're still reaching for your own cure" and "Look
   at me, and live" land as Christ's own words to the one specific viewer in front of the
   screen, not a third party inviting them toward someone else. The CTA stops being "look to
   Jesus" (an instruction) and becomes "look at me" (an invitation, spoken by the one being
   looked at).
3. **A real memory, not a citation.** The Nicodemus beat is staged as something Jesus is
   recalling happening TO him ("a teacher came to me in the dark") rather than a fact being
   reported. This is also the natural home for a second voice (see below) — it's a flashback
   inside the monologue, not a cutaway.
4. **The identical central image survives untouched.** "Shaped exactly like your curse" / "look,
   not effort" — the whole point of Look and Live's own thread — is preserved; only who is
   saying it changes. Per this project's own locked rule (never swap threads to placate
   feedback), the thread stays; only the voice changes.

## Dialogue / multi-voice ("great dialogue when needed")

This project already has a validated, in-use **`jesus` ElevenLabs voice**
(`tlETan7Okc4pzjD0z62P`, `config.py` `VOICE_MAP`) — used across the existing narration tree for
Jesus's quoted lines. For this POC it becomes the FULL narrator voice (every line, not just
quotes). One genuine second-voice beat: Nicodemus's **"How can these things be?"** — a real
KJV line, a real second speaker, staged as a flashback exchange inside Jesus's own telling
(inverts the existing multi-voice convention where "Jesus tells the story, inner characters get
a voice" — here Jesus IS the narrator and a character gets pulled into HIS telling). Candidate
voice for Nicodemus: `father` (`UzI1NsMEV3ni5JRkRSls`, older/gravitas) reused — fits an elder
"ruler of the Jews" better than the younger `disciples` voice. Open call, not locked.

## Visual pacing — a real fork worth deciding before building anything

Look and Live currently exists in the **living-sketchbook** style (`_s1_stills.py`/`_s2_animate.py`
in this folder) — hand-drawn spread pacing, calmer per-spread holds, camera-locked paper. The
user's ask ("dynamic, engaging, almost hypnotic, like the viral edit cuts") describes something
closer to this project's OTHER visual grammar: the **shorts viral-cut pipeline**
(`cli_visual.py`/`cli_assemble.py`, HF Kling pro gallery-tour cut-plans, hero bookend + AS-G*
phrase-level jigsaw assembly) — hard crop-cuts timed to the spoken phrase, built specifically for
fast/dynamic/hypnotic pacing. These are two different rendering engines with different stills,
not a settings toggle — matching the user's stated intent likely means building fresh stills +
animation in the viral-cut grammar rather than reusing Look and Live's existing living-sketchbook
clips. Worth confirming before spending on new renders. The score-swap work from earlier today
(candidate D — driving, hypnotic, 137 BPM) is a strong natural pairing for this pacing: cutting
the visual jigsaw to lock onto that track's own rising pulse would reinforce the hypnotic feel
across both audio and image at once.

## Not done yet

1. User read/feedback on the script itself (wording, doctrine, emphasis).
2. Pick: living-sketchbook (reuse Look and Live's stills/clips, calmer) vs. viral-cut jigsaw
   (fresh stills + Kling gallery-tour animation, faster/hypnotic) for the visual engine.
3. Confirm Nicodemus's voice pick (or another).
4. Only then: build a narration.md + voices.json pair for this script, subprocess the existing
   `narration_pipeline.py` verify->tag->audit + `per_turn_synth.py` (reuse, not duplicate) to
   get a duration-locked multi-voice MP3 — HUMAN GATE 1 (ear-check) before any visual spend.
