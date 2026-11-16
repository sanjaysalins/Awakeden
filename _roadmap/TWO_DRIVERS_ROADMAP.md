# TWO DRIVERS ROADMAP — v2

Salt and Light Kingdom. 2026-11-16. Status: **DRAFT v2, after red team.** $0 spent.
v1 (Fable design + appended fixes) is kept at `_roadmap\TWO_DRIVERS_ROADMAP.v1.md`. v2 folds in 3 review rounds
(round 1: cursor + gemini; round 2: claude + codex + fresh Fable seat; red team: codex + fresh Fable + fresh Sonnet). Grok timed out every round.
Every `Ref "quote"` in this file is machine-checked by `_roadmap\kjv_check_roadmap.py` (section 9).
Claims that are not quotes (counts, order, who said what) sit in each hunt's FACTS list and are checked by hand.

---

## 0. Answer to the owner's challenge

AI cannot give new revelation. We never pretend it can.
AI can read all 66 books at once and find links that are **already in the text**.
The bar: **old in the text, new to the viewer.** Never new doctrine.
Bethlehem scored about 6/10 for "new" because the topic was locked before we hunted.
**Now: hunt the link first. No strong link, no film.**
Honest odds: about 30-40% of the 24 ideas below may fail their own hunt (50-65% of the classic ones). That is the point — we fail cheap, on paper.

---

## 1. The two drivers

| | **Driver 1: THE THREAD** | **Driver 2: THE ENCOUNTER** |
|---|---|---|
| Headline is | A **verse-to-verse link** (OT to NT) | A **scene** with Jesus and its "so what" |
| Promise | "Two verses, far apart, lock together on Jesus." | "One moment with Jesus. One true thing for you." |
| Ends on | Jesus as the one the Bible pointed to | Jesus as the one you can trust today |

**Which driver?** If the headline is a link, Driver 1. If the headline is a scene, Driver 2 (a link inside it is the surprise, never the title).

### Hard tests

| # | Test | Pass means |
|---|---|---|
| Q1 | Anchors | Driver 1: one OT + one NT verse, exact KJV. Driver 2: two anchors, may be from the same chapter. |
| Q2 | Spoken label | Every link carries one label from 2a and the film **says it out loud**. |
| Q3 | Quote check | Every quote passes the KJV checker. 0 MISMATCH. |
| Q4 | FACTS check | Every non-quote claim is on the FACTS list and hand-checked against the KJV text. |
| Q5 | Newness | Hunt judges: ANGLE FRESH 7.0+ (shortlist). Real seed viewers: 60%+ "I had not seen this" (the true gate). |
| Q6 | Lands on Jesus | Last spoken beat is about Him, from the piece's own verses. Driver 2 then adds one line for you (grace first). |
| Q7 | One line | A newcomer can say the insight in one plain sentence. |

### Banned

Calling an echo a prophecy · a title that leads with an ECHO · numerology / codes · "the church got it wrong" · fear or gain/loss framing · Hebrew/Greek claims beyond plain lexicon facts · stock closers (`narration_gate.py`) · hard KJV words carrying the landing · "nobody has seen this" · putting motives or feelings in a text that does not state them · any AI wording in public text.

Locked spine stays: every piece lands on Jesus, KJV word for word, grace-anchored, doctrine checked both ways.

---

## 2. The insight engine

### 2a. One label set (used everywhere)

| Label | Means | Film says |
|---|---|---|
| **PROPHECY** | The OT looks forward and the NT says it was fulfilled in Jesus. | "The Bible itself says this pointed to Him." |
| **NT-STATED** | The NT itself makes the link, but the OT text was history, a pattern or a vision, not a forecast (e.g. Hosea 11:1, John 12:41, Hebrews 10:20). | "The New Testament makes this link." |
| **ECHO** | Same words or shape in two places. The Bible does not state the link. | "The Bible does not say these are linked. But look at the words." |
| **DETAIL** | Something in the passage itself that most people read past. | "It is right there in the verse." |

The strongest label sets the headline. An ECHO is never the title claim.

### 2b. The hunt ($0)

| Step | What | Status |
|---|---|---|
| 1 | Concordance-loom: verbatim word matches for the passage | exists (`/concordance-loom`) |
| 2 | BRIEF with a **kill list** (the 4-6 angles "told a million times") | template to build |
| 3 | 6 blind seats: Fable + Sonnet (subagents in the live session) + claude / codex / gemini / grok CLIs. Each gives angles + exact quotes + label + "what it does NOT prove" + FACTS list | script to generalise |
| 4 | KJV quote check + hand FACTS check | quote checker exists |
| 5 | Neutral cards, no authors, random order | by hand today |
| 6 | 6 fresh blind judges score FRESH / TRUE / SOUND / CLEAR / JESUS (+ GROWTH for Driver 2) | script to generalise |
| 7 | Bank the winner and the losers | `INSIGHT_BANK.md` to build |
| 8 | Seed viewers (5-10 real people): "Had you seen this before?" | form to build |

### 2c. Bars

| Score | Bar (median of 6 judges) |
|---|---|
| ANGLE FRESH | 7.0+ to shortlist. 6.0-6.9 = "classic, told well", at most 1 in 4 films. Under 6 = bank only. |
| TRUE | 8.0+ |
| SOUND | All PASS. Any factual flag = fix or drop. |
| CLEAR | 7.0+ |
| JESUS | 8.0+ |
| GROWTH (Driver 2) | 7.0+ |
| FILM FRESH (blind film check, later) | 6.5+. Under = fix words once, then ship or shelve. |

AI judges cannot know what churchgoers have seen; expect them to be off by 1-2 points. Seed viewers decide.

### 2d. What lifts newness

Hunt before the topic locks · two-hop chains (OT → OT → NT) · loom first, not memory · kill list on every brief · both verses side by side on screen · real seed viewers.

---

## 3. Driver 2's "so what"

| Test | Pass | Fail |
|---|---|---|
| S1 From the text | Uses a word or act from the passage's own KJV | "So trust God more." |
| S2 About Him first | What Jesus is like or did, then what it means for you | A to-do list |
| S3 One true sentence | A newcomer can repeat it | Church words |
| S4 Life-size | Touches one real thing: fear, shame, failure, being unseen, purpose, loss | Abstract |

Write the "so what" as one line during the hunt. It says what Jesus did in the scene; any line for the viewer must be backed by a verse that speaks to all believers (judges check this under SOUND). Use the earned-landing-word pattern. No pushing questions. The 5 guardrail questions must return the same take-away from every seat.

---

## 4. The rhythm (one person + Claude)

**Step 0 — build the tools (1-2 days, $0):** a topic-generic hunt folder (`_roadmap\hunt_kit\`, topic-dir argument, Fable + Sonnet seats, no import from the ArkAIology repo), `INSIGHT_BANK.md`, FACTS template, GROWTH judge prompt, seed-viewer form.

**Step 1 — pilot E9 end to end.** Pass if: ANGLE FRESH 7.0+, seed viewers 60%+ "new to me", 0 SOUND flags, and we log real cost (including redos) and real owner minutes.

**Step 2 — 1 film a week for 4 weeks.** Hunt every day ($0) to stock the bank.

**Step 3 — faster only if the measured numbers allow** (bank holds 6+ passed ideas, cost and owner time on target).

| Lane | Pace | Cost |
|---|---|---|
| HUNT | 1 a day | $0 (CLI plan usage) |
| WORDS | 1 a week (blind writers → judge table → global-audience test → guardrail panel) | $0 |
| FILM | 1 a week; each paid step quoted, each needs a yes | about $8-14 (some past films ran to $21) |
| Owner | about 15-30 min a day, one page | — |

Slack: assume one redo per film. If a still or clip fails, the film slides a week. Never skip a gate to keep the day.

---

## 5. Roadmap: 24 candidates

Not re-proposed (already made): Isaiah 53, Psalm 22, Zechariah 12:10, Thirty Pieces, Genesis 3:15, Bethlehem, Immanuel, Nazareth, Passover Lamb, Bronze Serpent, Jonah, Two Goats, Manna, Isaiah 40:3 (Swirls "Only a Voice"), and the encounter shorts (Zacchaeus, the well, Mary and Martha, the second fire, Bartimaeus, the storm, the thief, the Swirls episodes).
Before each hunt: grep the catalogue for overlap (especially T3 vs Nazareth, E4, E8, T5).
**★ = first 3. HOLD = do not hunt until fixed.** All are candidates; each must pass its own hunt.

### DRIVER 1: THE THREAD

**Arc 1 — "Written before He came"**

| # | Working title | Anchors (KJV) | Angle | Label |
|---|---|---|---|---|
| T1 | Which King was promised a kingdom with no end? | 2 Samuel 7:13 "I will stablish the throne of his kingdom for ever" → Luke 1:33 "of his kingdom there shall be no end"; Hebrews 1:5 "I will be to him a Father, and he shall be to me a Son" | Gabriel's words to Mary carry God's old promise to David: throne, kingdom, for ever. Hebrews applies the same promise to Jesus. | NT-STATED (Hebrews 1:5); Luke = ECHO |
| T2 | Why did Jesus have to go to Egypt? | Hosea 11:1 "called my son out of Egypt" → Matthew 2:15 "Out of Egypt have I called my son"; Deuteronomy 8:3 "man doth not live by bread only" → Matthew 4:4 "Man shall not live by bread alone" | Hosea looked back at Israel. Matthew says Jesus fills that story: Egypt, water, wilderness, and He answers each test from Deuteronomy. | NT-STATED (Matthew says "fulfilled"; Hosea looked back). Wilderness road = ECHO |
| ★ T3 | Why did Jesus go to Galilee? | Matthew 4:12 "heard that John was cast into prison, he departed into Galilee" → Isaiah 9:1 "at the first he lightly afflicted the land of Zebulun and the land of Naphtali"; Isaiah 9:2 "The people that walked in darkness have seen a great light" → Matthew 4:16 "The people which sat in darkness saw great light" | After John's arrest Jesus goes to Galilee and settles in Capernaum, in Zabulon and Nephthalim. Matthew 4:13 "dwelt in Capernaum" — and says this fulfils Isaiah: the people which sat in darkness saw great light. | PROPHECY (Matthew 4:14). No "first to fall / first to see" claim. |
| T4 | Who did Moses say to listen to? | Deuteronomy 18:15 "unto him ye shall hearken" → Acts 3:22 "A prophet shall the Lord your God raise up unto you"; Matthew 17:5 "hear ye him" | Moses said: one day, listen to Him. On the mountain, with Moses there, the voice says the same about Jesus. | PROPHECY (Acts 3:22); mountain = ECHO |

**Arc 2 — "He quoted it Himself"**

| # | Working title | Anchors (KJV) | Angle | Label |
|---|---|---|---|---|
| T5 | Were they inside a prophecy and did not know? | Zechariah 9:9 "lowly, and riding upon an ass" → John 12:16 "These things understood not his disciples at the first" | The disciples walked through an old verse and missed it. John admits it. | PROPHECY (Matthew 21:4) |
| T6 | Did the crowd sing the song that warned them? | Psalm 118:26 "Blessed be he that cometh in the name of the LORD" → Matthew 21:9 "Blessed is he that cometh in the name of the Lord"; Psalm 118:22 "The stone which the builders refused is become the head stone of the corner" → Matthew 21:42 "The stone which the builders rejected" | The crowd cried out verse 26. Four verses up, the same song speaks of the stone the builders refused. Soon after, in the temple, Jesus quotes that line. | PROPHECY (Jesus applies it) |
| T7 HOLD | Who ate bread with Him and turned? | Psalm 41:9 "which did eat of my bread, hath lifted up his heel against me" → John 13:18 "He that eateth bread with me hath lifted up his heel against me" | Jesus applies David's psalm to Judas. (David's Kidron/Olivet road = ECHO only; 2 Samuel 17:23 "his counsel was not followed" is Ahithophel's stated reason, not remorse.) | NT-STATED |
| T8 | What question could no one answer? | Psalm 110:1 "The LORD said unto my Lord, Sit thou at my right hand" → Matthew 22:45 "If David then call him Lord, how is he his son?" → Matthew 22:46 "no man was able to answer him a word" | Why would King David call his own descendant "my Lord"? | PROPHECY (Jesus and Acts 2:34 apply it) |

**Arc 3 — "Now read it again"**

| # | Working title | Anchors (KJV) | Angle | Label |
|---|---|---|---|---|
| T9 | What one sentence got Jesus killed? | Daniel 7:13 "one like the Son of man came with the clouds of heaven" → Matthew 26:63 "But Jesus held his peace" → Matthew 26:64 "Hereafter shall ye see the Son of man sitting on the right hand of power, and coming in the clouds of heaven" | Jesus is silent, then gives one answer built from two old verses (Psalm 110 and Daniel 7). The high priest knew what He was claiming. | PROPHECY (Jesus applies it) |
| T10 HOLD | What did the torn curtain open? | Matthew 27:51 "the veil of the temple was rent in twain from the top to the bottom" → Hebrews 10:20 "through the veil, that is to say, his flesh" | Lead on Hebrews only. No cherubim-on-Herod's-veil claim (no verse says it). | NT-STATED |
| T11 | Why did Peter point at a grave? | Psalm 16:10 "neither wilt thou suffer thine Holy One to see corruption" → Acts 2:29 "his sepulchre is with us unto this day" → Acts 2:31 "spake of the resurrection of Christ" | The first sermon gave a reason: David's grave is still there, so the song was not about David. | PROPHECY (Acts 2:30-31) |
| ★ T12 | Whose glory did Isaiah see? | Isaiah 6:5 "the King, the LORD of hosts"; Isaiah 6:10 "shut their eyes" → John 12:40 "He hath blinded their eyes" → John 12:41 "These things said Esaias, when he saw his glory, and spake of him" | John quotes Isaiah's temple vision (6:10), then adds one quiet line: Isaiah saw **His** glory — Jesus'. About 800 years apart. "His glory" is John's own word. | NT-STATED (not a prediction) |

### DRIVER 2: THE ENCOUNTER

**Arc 1 — "He sees you"**

| # | Working title | Anchors (KJV) | Angle | Label | So what |
|---|---|---|---|---|---|
| E1 | What had Jesus done to earn it? | Mark 1:11 "Thou art my beloved Son, in whom I am well pleased"; Matthew 12:18 "in whom my soul is well pleased" | The Father says "well pleased" before one sermon or miracle. Matthew links the words to Isaiah's Servant. | DETAIL + NT-STATED | With Him, love comes before work. |
| E2 HOLD | Why could Jesus not go into the city? | Mark 1:44 "See thou say nothing to any man" → Mark 1:45 "could no more openly enter into the city, but was without in desert places" | Needs rework: the man disobeyed, and Mark gives that as the cause. No "swap" claim. | DETAIL | — |
| E3 | What did she grab? | Numbers 15:38 "fringes in the borders of their garments" → Luke 8:44 "touched the border of his garment" → Mark 5:34 "Daughter, thy faith hath made thee whole" | She reached for the fringe the law gave. He calls her "Daughter". | DETAIL + ECHO (fringe) | He did not pull away from her shame; He called her Daughter. |
| E4 | How did she know Him? | John 20:15 "supposing him to be the gardener" → John 20:16 "Jesus saith unto her, Mary"; John 10:3 "he calleth his own sheep by name" | She knew Him by one word: her name. (Eden "garden" = small ECHO only.) | DETAIL + ECHO | He knows your name. |

**Arc 2 — "He grows you"**

| # | Working title | Anchors (KJV) | Angle | Label | So what |
|---|---|---|---|---|---|
| E5 | What happens when you tell God to leave? | Isaiah 6:5 "Woe is me! for I am undone" → Isaiah 6:8 "Here am I; send me"; Luke 5:8 "Depart from me; for I am a sinful man, O Lord" → Luke 5:10 "Fear not; from henceforth thou shalt catch men" | Two men see who God is, fall apart, and get a job. Pairs with T12. | ECHO | Feeling unfit did not stop Him calling Peter. |
| E6 | How did a blind man see more each time? | John 9:11 "A man that is called Jesus" → John 9:17 "He is a prophet" → John 9:38 "Lord, I believe. And he worshipped him"; John 9:35 "when he had found him" | A man, a prophet, Lord. And when he is thrown out, Jesus finds him. | DETAIL | Jesus went looking for the man everyone threw out. |
| E7 (retitle) | Who said "it is I" on the sea? | Mark 6:48 "would have passed by them"; Job 9:8 "treadeth upon the waves of the sea"; Job 9:11 "he passeth on also" → Mark 6:50 "Be of good cheer: it is I; be not afraid" | Job's words about God — walks on the sea, passes by — show up in Mark's scene. Title on Mark 6:50 "it is I", not on the echo. Mark does not say why He would have passed by; no motive claim. | ECHO (Mark does not state it) | The One who walks on what scares you says: it is I. |
| E8 | What did Jesus do before Peter failed? | Luke 22:32 "I have prayed for thee, that thy faith fail not: and when thou art converted, strengthen thy brethren" → Luke 22:61 "the Lord turned, and looked upon Peter" | "When", not "if". The prayer came before the fall. | DETAIL | Your worst day did not surprise Him. |

**Arc 3 — "He sends you"**

| # | Working title | Anchors (KJV) | Angle | Label | So what |
|---|---|---|---|---|---|
| ★ E9 | Why did Jesus say no to the man He healed? | Mark 5:12 "all the devils besought him"; Mark 5:17 "they began to pray him to depart"; Mark 5:18 "prayed him that he might be with him" → Mark 5:19 "how great things the Lord hath done for thee" → Mark 5:20 "how great things Jesus had done for him" | In Mark 5:1-20, three ask Him: the devils, the town, the healed man. (Mark 5:10 is a fourth plea from the devils.) The devils' and the town's are granted. The healed man asks to stay with Jesus — "Jesus suffered him not" — and is sent home. Jesus says "how great things the Lord hath done for thee"; Mark says he told "how great things Jesus had done for him". | DETAIL | A "no" from Him can be a mission. |
| E10 | What did Jesus see that no one counted? | Mark 12:40 "Which devour widows' houses" → Mark 12:43 "this poor widow hath cast more in" → Mark 12:44 "all that she had, even all her living" | Read the line before: He has just named men who eat up widows' houses. Then He watches one widow. | DETAIL | He sees what nobody counts. |
| E11 (retitle) | When did they know Him? | Luke 24:16 "their eyes were holden" → Luke 24:31 "their eyes were opened, and they knew him"; Luke 24:27 "in all the scriptures the things concerning himself"; Genesis 3:7 "the eyes of them both were opened" | Title on Luke. Genesis 3:7 word-match = ECHO, small. | DETAIL + ECHO | He walks with you before you know it is Him. |
| E12 HOLD | What was Jesus doing as He left? | Luke 24:50 "he lifted up his hands, and blessed them" → Luke 24:51 "while he blessed them, he was parted from them" | Drop the Aaron link (Hebrews 7:11 "not be called after the order of Aaron"). Rework on Luke alone. | DETAIL | — |

### Order

| When | Driver 1 | Driver 2 |
|---|---|---|
| Step 0 | build tools | — |
| Pilot | — | ★ E9 |
| Weeks 1-4 (1 film a week) | ★ T12, ★ T3 | E5 (pairs with T12), E8 |
| After that (if numbers allow) | T6, T8, T11, T1, T2, T4, T5, T9 | E6, E10, E1, E3, E4 |
| Fix first | T7, T10 | E2, E12; re-title E7, E11 |

Why these 3: E9 sits in one chapter, needs no outside claim, and has a fresh detail (Lord / Jesus). T12 is stated by the NT itself. T3 is a PROPHECY Matthew states, kept to what Isaiah and Matthew say.

---

## 6. Risks (best guesses, wide error bars)

| Risk | Odds | Response |
|---|---|---|
| An idea fails its hunt | ~30-40% overall; ~50-65% of the classic ones (T1, T2, T4, T6, T11, E3, E4, E5, E6) | Bank keeps spares |
| AI judges misjudge "fresh" | off by 1-2 points | Seed viewers decide |
| An ECHO heard as prophecy | medium | Spoken label; blind film check asks "what kind of link?" |
| Shared AI blind spot on doctrine | low-medium | Quote check + FACTS check + owner read + a pastor/teacher on ECHO pieces when possible |
| Owner time runs out | medium | One page a day; slow down before dropping a gate |
| Insight does not lift views | unknown, ~50/50 in 10 films | First 2 seconds + seed viewers matter more |
| Cost creep | medium | Quote before every paid step; ledger |

## 7. Measures

ANGLE FRESH median · seed viewers "new to me" (target 60%+) · global-audience who/what/why · Driver 2 take-away match across seats · hunt pass rate (track) · 48-hour retention and comments quoting the link (track 10 films) · cost incl. redos and owner minutes per film.

## 8. Open tool gaps (Step 0)

- `prophecy\01_bethlehem\fresh_hunt\run_seats.py` / `run_judges.py` read files from their own folder, take only a seat-name argument, run 4 CLIs only, and import from `F:\slk\PycharmProjects\ArkAIology`. Needs a topic-dir version with Fable + Sonnet seats.
- Missing: `INSIGHT_BANK.md`, BRIEF/kill-list template, FACTS template, GROWTH judge prompt, seed-viewer form, cards script.

## 9. KJV check

Script: `F:\slk\PycharmProjects\JesusInTheBible\_roadmap\kjv_check_roadmap.py` — reads every `Ref "quote"` in this file and checks it against `data\kjv_full`. Checks words and order only (ignores case and punctuation).

## 11. Challenge gates (owner, 2026-11-16; hardened after Fable + Codex red team)

Why: the E9 pilot hunted one chapter only, skipped the loom, used a kill list we wrote ourselves, never gave the "why" of the link, and showed the owner the idea only after words existed. Fixed in code (`_roadmap\hunt_kit\`, see its README):

1. `loom.py` first (ours only); `loom.md`, `SUNDAY_SCHOOL.md` (5+ bullets, incl. most-cited cross-references), `BRIEF.md`, `KJV_PACK.md` checked at run_seats, run_judges, gate, owner_card (REFUSED, exit 1). Kill list = machine-made; hand edits logged at its bottom.
2. One shared prompt per stage: `HUNT_PROMPT.md` (brief + kill list + KJV) and `JUDGE_PROMPT.md` (with kill list).
3. ANCHOR gate: `ANCHOR-1` (inside the passage), `ANCHOR-2` (another book, not a Gospel parallel), `WHY-VERSE`, `LABEL`. Quotes need 4+ real words, a real verse, exact KJV. PROPHECY/NT-STATED need an NT WHY-VERSE; ECHO needs a shared 3-word phrase or a loom match; DETAIL alone fails.
4. No waiver: any SOUND flag fails the card; reword and re-judge with new judge files.
5. `gate.py`: 5+ distinct judge files, every card fully parsed (else "unparsed"), files newer than CARDS.md (else "stale"); medians FRESH 7, TRUE 8, CLEAR 7, JESUS 8, GROWTH 7 (Driver 2), DEPTH 7 (link strength, not book count); one non-Claude judge at FRESH+DEPTH bars; COMMON yes/partly from 2+ judges fails; CONTEXT PASS from codex and gemini (`context_check.py`).
6. `owner_card.py` only for a PASS card in a current GATE.md; the question "Had you seen this before?" comes first. `owner_answer.py` records it; words start only on NO.
7. Seed viewers (with "said it back correctly") are needed before PUBLISH, not before words; % goes in `INSIGHT_BANK.md`.

These override earlier sections where stricter. Example: Driver 2 DETAIL-only episodes (a surprise inside one chapter) now fail; Q1 "may be from the same chapter" no longer holds. Seats may answer "NO HONEST LINK" and that is a good answer.
