# PAGE PLAN REPORT — LONG

Source: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1`

- T (last word end): 473.980s
- T (ffprobe mp3): 474.230s
- T used: 473.980s
- N_pages: 39
- Final page count after repair: 39

## ESCALATIONS
- ESCALATE: alignment word stream has 68 leading zero-duration junk tokens (e.g. ['4-voice', 'long-form', 'read:', 'narrator', '(default)']...) that are not spoken narration — traced to a multi-line <!-- --> HTML comment in narration-tagged.md not being fully stripped by pipeline/assembly_timing.py::_parse_tagged_chunks (it only checks if a line STARTS WITH '<!--', so continuation lines of a multi-line comment block leak into the transcript that pipeline/assembly_align.py::transcript() feeds to whisper alignment). This corrupts phrase 0's word span and inflates page 1's phrase/panel count. NOT fixed here (outside poc_comic_page/, a design decision per the brief) — reported for Fable/user triage.

## Pages

### Page 1
- t0-t1: 0.00s - 12.80s
- dwell: 12.80s
- phrases: 19
- panels: 4
- layout: 2x2
- text: 4-voice long-form read: narrator (default) · scripture (KJV narration/prophets) · god (Num 21:8 first-person command) · jesus (John 3:14-15 + 12:32, His own words). Words are FROZEN — this file only adds speaker tags; spoken text is verified equal to the LOCKED narration.md. 2026-07-03: hand-mirrored the v1.5 panel fixes (M2 Num 21:7 full span + request-vs- confession rewording; M6 "might live") — verified word-equal to narration.md v1.5. --> A whole camp is dying of snakebite — and God's remedy is not to kill the snakes, or heal the wounds, or hand out an antidote. He tells them to look at a piece of metal on a pole. Look, and live.

### Page 2
- t0-t1: 12.80s - 23.68s
- dwell: 10.88s
- phrases: 4
- panels: 3
- layout: 3-big-left
- text: It is one of the strangest cures in the Bible. It happens near the end of the wilderness years. Israel is worn down by the long road, and the old bitterness boils over.

### Page 3
- t0-t1: 23.68s - 37.04s
- dwell: 13.36s
- phrases: 5
- panels: 3
- layout: 3-big-top
- text: "Wherefore have ye brought us up out of Egypt to die in the wilderness? for there is no bread, neither is there any water; and our soul loatheth this light bread."

### Page 4
- t0-t1: 37.04s - 48.76s
- dwell: 11.72s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: They have bread from heaven — and they despise it, and accuse the God who has carried them this far. And then the ground itself turns against them. "And the LORD sent fiery serpents among the people,

### Page 5
- t0-t1: 48.76s - 59.72s
- dwell: 10.96s
- phrases: 6
- panels: 4
- layout: 2x2
- text: and they bit the people; and much people of Israel died." Picture the camp. The venom is already moving, and there is nothing a bitten man can do to stop it —

### Page 6
- t0-t1: 59.72s - 72.50s
- dwell: 12.78s
- phrases: 6
- panels: 4
- layout: 2x2
- repairs: ['2x2 repeats consecutively (only legal layout at panel_count=4)']
- text: he cannot run from a poison inside his own blood. And notice what the people ask for. They come to Moses and confess: "We have sinned, for we have spoken against the LORD, and against thee;

### Page 7
- t0-t1: 72.50s - 84.44s
- dwell: 11.94s
- phrases: 6
- panels: 4
- layout: 2x2
- repairs: ['2x2 repeats consecutively (only legal layout at panel_count=4)']
- text: pray unto the LORD, that he take away the serpents from us." Their confession is real — they name the sin itself. But look at the cure they ask for: take away the serpents,

### Page 8
- t0-t1: 84.44s - 96.86s
- dwell: 12.42s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: make the threat go away. That would not save a single person already bitten; the venom is already in the blood. Even as they confess, their request reaches only for the danger outside.

### Page 9
- t0-t1: 96.86s - 109.42s
- dwell: 12.56s
- phrases: 4
- panels: 3
- layout: 3-big-top
- text: And that is the human problem in miniature: we admit we have sinned, and still we beg God mostly to change our circumstances — when the poison is already within.

### Page 10
- t0-t1: 109.42s - 121.76s
- dwell: 12.34s
- phrases: 6
- panels: 4
- layout: 2x2
- text: Now watch what God actually does — because He does not do what they asked. He does not take the serpents away. He says to Moses: "Make thee a fiery serpent, and set it upon a pole:

### Page 11
- t0-t1: 121.76s - 132.78s
- dwell: 11.02s
- phrases: 6
- panels: 4
- layout: 2x2
- repairs: ['2x2 repeats consecutively (only legal layout at panel_count=4)']
- text: and it shall come to pass, that every one that is bitten, when he looketh upon it, shall live." Sit with how strange that is. The cure is shaped like the curse.

### Page 12
- t0-t1: 132.78s - 145.74s
- dwell: 12.96s
- phrases: 4
- panels: 3
- layout: 3-big-left
- text: The thing lifted up is a serpent — a bronze likeness of the very thing killing them — raised on a pole for all to see. God does not clear the serpents from the camp;

### Page 13
- t0-t1: 145.74s - 158.96s
- dwell: 13.22s
- phrases: 6
- panels: 4
- layout: 2x2
- text: He turns the dying eye toward the image of the judgment itself. And the cure costs the bitten man nothing he can boast in — not a potion to brew, not a wound to lance, not a snake to fight.

### Page 14
- t0-t1: 158.96s - 169.70s
- dwell: 10.74s
- phrases: 7
- panels: 4
- layout: 2x2
- repairs: ['2x2 repeats consecutively (only legal layout at panel_count=4)']
- text: "Every one that is bitten, when he looketh upon it, shall live." One act. Look. "And Moses made a serpent of brass, and put it upon a pole,

### Page 15
- t0-t1: 169.70s - 182.46s
- dwell: 12.76s
- phrases: 6
- panels: 4
- layout: 2x2
- repairs: ['2x2 repeats consecutively (only legal layout at panel_count=4)']
- text: and it came to pass, that if a serpent had bitten any man, when he beheld the serpent of brass, he lived." Now move forward roughly fourteen hundred years, into a quiet night-time conversation.

### Page 16
- t0-t1: 182.46s - 194.00s
- dwell: 11.54s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: A religious leader named Nicodemus has come to Jesus in the dark, trying to understand who He is. And Jesus reaches back — past the temple, past the law —

### Page 17
- t0-t1: 194.00s - 206.98s
- dwell: 12.98s
- phrases: 4
- panels: 3
- layout: 3-big-top
- text: to a snake on a pole in the desert. "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up: That whosoever believeth in him should not perish,

### Page 18
- t0-t1: 206.98s - 217.50s
- dwell: 10.52s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: but have eternal life." Stop on that. This is not a preacher centuries later finding a clever picture in the Old Testament. This is Jesus Himself,

### Page 19
- t0-t1: 217.50s - 229.96s
- dwell: 12.46s
- phrases: 4
- panels: 3
- layout: 3-big-top
- text: naming that pole as a portrait of His own cross. And He means it precisely. Later, John tells us what that phrase pointed to: "And I, if I be lifted up from the earth,

### Page 20
- t0-t1: 229.96s - 243.00s
- dwell: 13.04s
- phrases: 6
- panels: 4
- layout: 2x2
- text: will draw all men unto me." John adds the note: "This he said, signifying what death he should die." "Lifted up" was the cross. By Jesus' own word,

### Page 21
- t0-t1: 243.00s - 253.86s
- dwell: 10.86s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: the wilderness pole was a picture of Calvary. And the passage flows straight on into the verse the whole world knows: "For God so loved the world, that he gave his only begotten Son…"

### Page 22
- t0-t1: 253.86s - 266.32s
- dwell: 12.46s
- phrases: 6
- panels: 4
- layout: 2x2
- text: The snake on the pole and "God so loved the world" sit in the same breath of Scripture. Now, be fair to the doubts, because there are two. First: doesn't a bronze snake on a pole just become an idol?

### Page 23
- t0-t1: 266.32s - 279.34s
- dwell: 13.02s
- phrases: 4
- panels: 3
- layout: 3-big-left
- text: Scripture itself answers that — bluntly. Centuries later Israel did begin burning incense to it, and a godly king named Hezekiah "brake in pieces the brasen serpent

### Page 24
- t0-t1: 279.34s - 290.60s
- dwell: 11.26s
- phrases: 6
- panels: 4
- layout: 2x2
- text: that Moses had made." The bronze never had power; God did. Looking was never magic — it was trust, aimed where God told them to aim it.

### Page 25
- t0-t1: 290.60s - 304.26s
- dwell: 13.66s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: Scripture smashes the relic itself, so that you never mistake the sign for the Savior. Second, and deeper: isn't a serpent a strange picture of Christ? In the Bible the serpent is the tempter and the curse.

### Page 26
- t0-t1: 304.26s - 315.98s
- dwell: 11.72s
- phrases: 6
- panels: 4
- layout: 2x2
- text: Exactly — and that is the point, not the problem. What hung on that pole was the likeness of the very thing killing them; what hung on the cross was the One of whom Scripture says

### Page 27
- t0-t1: 315.98s - 329.90s
- dwell: 13.92s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: God "hath made him to be sin for us, who knew no sin" — the One "being made a curse for us: for it is written, Cursed is every one that hangeth on a tree."

### Page 28
- t0-t1: 329.90s - 340.60s
- dwell: 10.70s
- phrases: 4
- panels: 3
- layout: 3-big-top
- text: Christ did not become a sinner. He was lifted up bearing our curse, in the likeness of the judgment we deserved — so the look of faith could find it there and live.

### Page 29
- t0-t1: 340.60s - 353.10s
- dwell: 12.50s
- phrases: 4
- panels: 3
- layout: 3-big-left
- text: And this is not a stretch read into the text; it is the meaning Jesus put there Himself. So hold the two scenes together. In the wilderness the cure was never in the dying man —

### Page 30
- t0-t1: 353.10s - 363.98s
- dwell: 10.88s
- phrases: 6
- panels: 4
- layout: 2x2
- text: he could not neutralize the venom or earn his way back to health. It hung entirely outside him, on a pole. That is the cross. We are all bitten;

### Page 31
- t0-t1: 363.98s - 377.14s
- dwell: 13.16s
- phrases: 4
- panels: 3
- layout: 3-big-left
- text: the poison of sin is already in us, and no self-improvement reaches it. So God lifted up His Son, who "his own self bare our sins in his own body on

### Page 32
- t0-t1: 377.14s - 388.70s
- dwell: 11.56s
- phrases: 5
- panels: 3
- layout: 3-big-top
- text: the tree." The curse fell on the lifted One, so that everyone who looks to Him might live. It cost the bitten Israelite nothing but a turn of the eyes. It cost the Son everything.

### Page 33
- t0-t1: 388.70s - 402.90s
- dwell: 14.20s
- phrases: 6
- panels: 4
- layout: 2x2
- text: There is one more detail here, and it may be the kindest of all: the cure was a look. God could have asked for a climb, a payment, a proof of strength. He asked for the one thing a dying man can still do.

### Page 34
- t0-t1: 402.90s - 412.72s
- dwell: 9.82s
- phrases: 3
- panels: 2
- layout: 2v
- text: You can be too weak to stand and still lift your eyes. The most poisoned person in the camp was no further from healing than the least —

### Page 35
- t0-t1: 412.72s - 424.14s
- dwell: 11.42s
- phrases: 4
- panels: 3
- layout: 3-big-left
- text: both were saved the same way, by looking away from themselves to the One lifted up. So the invitation is as wide as the word Jesus chose: "whosoever."

### Page 36
- t0-t1: 424.14s - 437.68s
- dwell: 13.54s
- phrases: 5
- panels: 3
- layout: 3-big-top
- text: You do not have to get the poison out first, or feel strong, or be certain your faith is large enough. Faith is not a great work you produce; it is the empty-handed look of someone who has stopped trying to

### Page 37
- t0-t1: 437.68s - 447.86s
- dwell: 10.18s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: save themselves. You only have to stop staring at the bite, and look up. The serpent in the wilderness was God teaching the world one motion that saves.

### Page 38
- t0-t1: 447.86s - 460.64s
- dwell: 12.78s
- phrases: 4
- panels: 3
- layout: 3-big-top
- text: He lifted His Son on a cross for exactly that — so that whosoever turns their eyes to Him "should not perish, but have eternal life." You have stared at the bite long enough.

### Page 39 **(LAST PAGE)**
- t0-t1: 460.64s - 473.98s
- dwell: 13.34s
- phrases: 5
- panels: 3
- layout: 3-big-left
- text: The cure was never inside you — it is lifted up, outside you, already finished. Lift your eyes from the poison to the Saviour. What He has done on that cross is enough.

## CHECKS
- sum_dwells_eq_T: PASS — sum=473.980s vs T=473.980s
- boundaries_are_phrase_ends: PASS — all interior boundaries match a phrase end
- dwells_in_band_or_repaired: PASS — all pages in 8-16s band or carry a logged repair
- n_pages_matches_formula: PASS — formula=39 recheck=39
- no_unlogged_consecutive_layout_repeat: PASS — no unlogged consecutive repeats

## ESCALATIONS (repeat)
- ESCALATE: alignment word stream has 68 leading zero-duration junk tokens (e.g. ['4-voice', 'long-form', 'read:', 'narrator', '(default)']...) that are not spoken narration — traced to a multi-line <!-- --> HTML comment in narration-tagged.md not being fully stripped by pipeline/assembly_timing.py::_parse_tagged_chunks (it only checks if a line STARTS WITH '<!--', so continuation lines of a multi-line comment block leak into the transcript that pipeline/assembly_align.py::transcript() feeds to whisper alignment). This corrupts phrase 0's word span and inflates page 1's phrase/panel count. NOT fixed here (outside poc_comic_page/, a design decision per the brief) — reported for Fable/user triage.