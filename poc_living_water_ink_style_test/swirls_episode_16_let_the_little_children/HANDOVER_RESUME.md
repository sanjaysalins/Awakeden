# HANDOVER / RESUME - Swirls "Let the Little Children Come" (Mark 10:13-16)

Written 2026-11-10 night. Owner stopped for the night. **Nothing paid for this episode yet ($0).**

## 2026-11-11: WORDS LOCKED (X3), owner said "lock"
- Written: `narration.md`, `narration-tagged.md`, `voices.json` (ep12 voices), `narration.v1_locked_20261111.md`.
- Guardrail panel r1 (`guardrail_r1/`, page `_GUARDRAIL_R1.html`): avg 6.8; fixed "sent them away" overclaim etc -> X4.
- Fresh blind r2 (`guardrail_r2/`, page `_GUARDRAIL_R2.html`): flat (avg 6.4), 2-round stop. 3 last fixes (no "gift", "came for a touch", new line 1) -> **X5 LOCKED** (owner yes). Files: `words_blind/X5.md`, `narration.v2_locked_X5_20261111.md`; narration.md + tagged updated.
- BUILD NOTE: put a plain on-screen pill "Let the children come to Me." under the Jesus "Suffer..." line (4 seats misread "suffer" as pain).
- Still weak: "kingdom of God"/"blessed" unexplained; real surprise (Jesus angry) lands ~15 s.
- VOICE DONE (owner yes): per_turn_synth --target 65 --pre/post-quote-pause 0.4 --stability 0.65 --natural -> narration.mp3 72.62 s (1.0x, ~$0.21, ledger logged). Page `_LISTEN_VOICE.html`. Last 0.3 s still has sound (RMS -21.8 dB): add a tail fade at build (ep12 click lesson).
- Voice APPROVED by owner.
- PICTURES DONE (owner yes up to ~$1.04): `pictures/00..08` (OpenArt nano-banana-pro 2K 9:16; job ids in `pictures/_jobs.txt`), 400cr ≈ $0.80, ledger logged. Scene 2 redone (v1 father looked like Jesus, kept in `pictures/_rejected/`). Review page `_PICTURES.html`.
- Owner still is 896x1200 (3:4), not 9:16: last frame needs a pad/blur-fill or outpaint at build.
- Pictures APPROVED by owner.
- CLIPS DONE (owner yes up to ~$2.85): `clips/c01..c09.mp4` (Kling v3 std 5s sound off, 125cr) + owner still outpainted to 9:16 (`pictures/09_owner_still_9x16.png`). Redos: c03 (mother walked away = "sent away" overclaim), c05 (5th child appeared); v1s in `clips/_rejected/`. 1415cr ≈ $2.83 logged. (Account balance also dropped for 4 lip-sync jobs from ANOTHER session, not ours.)
- Word times: `narration.alignment.json` (whisperx via `_align.py`).
- FIRST CUT: `build_v1.py` -> `EP16_PREVIEW_v1.mp4` (75.6 s, 3.0 s hold, Jesus -5.5 dB, 13 segments incl. 4 crop-reuses). Page `_PREVIEW_v1.html`.
- OWNER REJECTED v1 cut style (2026-11-11): "hate the backwards and freeze and the zoom in cuts ... spend more ... high production". Owner yes up to ~$8.25 for V2.
- V2 (in `v2/`, job ids `v2/_jobs.txt`): 8 new stills (`v2/stills/sA..sH`, all QC pass) + 17 Kling v3 PRO clips (`v2/clips/`, each longer than its slot, 1.0x, hard cuts). All clips in + QC pass EXCEPT sE: v1 rejected (kids ran toward camera + clones, in `v2/clips/_rejected/`), REDO job oZEfSBctWxp0RzTtwwJU was still RUNNING (slow) — download it as `v2/clips/sE.mp4`, QC (3 kids, nobody turns), then run `build_v2.py` -> `EP16_PREVIEW_v2.mp4` (fails loudly if any clip is shorter than its slot). Spend so far v2 ≈ 3680cr ≈ $7.36 (log to ledger when done).
- (old v1 next) NEXT ($0): owner approves cut (GATE 3) -> Remotion text pill "Let the children come to Me." under the Jesus line (~32.6-38.4 s) -> SFX -> score (ask owner which) -> packaging card + red team + publish pack.

## (old) RESUME FIRST
"Lock the words (X3)? It locks the words only, not money."
Page to show: `file:///F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_episode_16_let_the_little_children/_PICK_WORDS.html`

## Why this episode
- Owner gave an exact still to replicate: Jesus (long dark wavy hair, beard, kind smile, blue patched tunic with visible cross-stitches over a cream undershirt) holding two laughing little girls (one hugging from the side, braid; one on His shoulders, hair bun, hand in His hair), old stone arch, olive tree, warm sunlight. Style: warm pencil + watercolour storybook.
- Owner file: `C:\Users\sanjay\Downloads\Replicate_reference_image_faithf..._5a6e4f2a.jpg`. Copies: `style_ref_owner_still.jpg` (this folder) and `poc_living_water_ink_style_test\_style_refs\storybook_jesus_children_ref.jpg`.
- It does not fit "Yet the Dogs" (Mark 7; Jesus never meets the girl), so the owner said yes to a new episode on Mark 10:13-16, with this still as cover + last picture. "Yet the Dogs" moves one slot later.
- Folder number 16: #14 and #15 are reserved in the roster (This Day / Emmaus). This episode is NOT in `test_the_cross/SWIRLS_OF_LIFE_SERIES_PLAN_V6.md` yet; add it to the roster when locked.
- If the reference art is someone else's, copy the STYLE and character look, not the picture itself (told the owner).

## Words process done ($0, words-before-money rule)
- Brief: `words_blind/pack.md` (who: someone told "not now"; "suffer" = "let" must be glossed; Mark 10:15 never a threat; ending lands on the fixed still / Mark 10:16).
- 5 blind writers, `words_blind/panel_r1/`: fable_lonely, opus_judge, claude_depth, codex_hook, grok_plain. **All 5 converged**: they asked for a touch (10:13) -> He gave His arms (10:16).
- Candidates X (Fable spine) / Y (Opus spine): `words_blind/candidates.md`.
- Test 1 (blind, `words_blind/test_r1/panel_r1/`): X won 4/4 - Fable 7.5, Claude Bible 7.5, Codex hook 8, Sonnet newcomer 8. Fixes -> `X2.md`.
- Test 2 (fresh blind seats, `words_blind/test_r2/panel_r1/`): Fable 7, Grok Bible 7 (REVISE: add 10:15, "upset" soft, last line a slogan), Sonnet newcomer 8. Scores flat, 2-round rule -> stopped.
- Final candidate **X3** (`words_blind/X3.md`, 157 words, ~65 s). Fixes from test 2: "Angry.", one set-up + one payoff for "touch", ending names "the children", plain line for 10:15, last line hands the hook back: "Someone told you 'not now.' Look at who Jesus picked up."
- 0 wrong KJV words in any round. Still weak: 10:15 is a plain paraphrase ("Anyone who comes in, comes the way a little child does"), not KJV; simulated viewers only.

## Next steps after the lock (each paid step = its own quoted price + separate yes)
1. Make `narration.md` / `narration-tagged.md` / `voices.json` (narrator + Jesus voice UzI1NsMEV3ni5JRkRSls, as ep12). Jesus line = Mark 10:14 full quote.
2. Guardrail panel on the locked words ($0, blind, Fable seat).
3. Voice: per_turn_synth --natural (ep12 cost ~$0.21-0.22). Quote first.
4. Pictures in the owner's style: OpenArt, attach ONLY the style ref (+ one in-style character ref) - ep12 lesson: a scene image attached as ref dominates. Build a Jesus character ref from the owner still first. ~7-9 pages; nano-banana-pro ~40cr/page (~$0.08). Last page = owner still (or a faithful in-style redraw, ask owner). Quote first.
5. Kling v3 std clips, sound off (ep12: 11 clips ~$4.00). Quote first.
6. Build like ep12: `v3_retro/build_v3.py` pattern (cut on whisper word times, ping-pong tail, 3.0 s hold), Remotion text pills (`_remotion/src/Ep12Towel.tsx` pattern), SFX via sfxlib, score (ask owner: own score again?), then publish pack + packaging card + red team (see ep12 HANDOVER notes in memory).

## Rules in force
Nothing paid without quoted price + separate yes; a pick locks WORDS only; blind panels always include Fable; owner dyslexic (short, one question, full file:/// links, never auto-open); no AI wording in public text; no media to GitHub; commit only when asked; gentle mode ON (`C:\Users\sanjay\.claude\.gentle-state`=3: one bg job, one agent, BelowNormal, ffmpeg -threads 3).

## 2026-11-11 later: v2 approved, text layer, music
- v2 cut APPROVED by owner. F: was full mid-build (built on C: scratchpad, copied back once F: had 28 GB).
- Text layer v1: `_remotion/src/Ep16Children.tsx` (5 pills) -> `EP16_REMOTION_v1.mp4`. Owner: "beautiful, but is this the best motion graphics you can do" -> Fable design pass running, spec due at `motion_v2/MOTION_DESIGN.md` ($0, build in Remotion next).
- MUSIC (owner yes up to $3): `generate_score_piano.py` (ep12 copy, 2-part split at 53.90 s "And here is what He did"). Part 2 v1 faded to silence at 14 s (kept in `_score_rejected/`), redone longer with "no fade-out". ~$2.50 logged. `score_piano.mp3` 75.70 s.
- Mix: `EP16_SCORED_v1.mp4` = score at -15 dB ramping to -9 dB over 50-56 s, sidechain duck (0.12/2.5/20/250). Measured ducked music ~10-14 dB under voice. Page `_LISTEN_SCORE.html`. Awaiting owner OK.
- Next: owner OK music -> build motion v2 -> re-mix score onto it -> SFX ($0) -> packaging card + red team + publish pack -> add #16 to V6 roster.
- Motion v2 BUILT:  (comp Ep16ChildrenV2) -> EP16_REMOTION_v2.mp4 -> EP16_SCORED_v2.mp4 (same score mix). Page . Fixes vs spec: His arms 128px + wider wash; 8a bloom r165 multiply over slip. Risk R1 (slip on followers = motif, not quote) for the guardrail panel.
- Motion v2 BUILT: _remotion/src/Ep16ChildrenV2.tsx (comp Ep16ChildrenV2) -> EP16_REMOTION_v2.mp4 -> EP16_SCORED_v2.mp4 (same score mix). Page _MOTION_V2.html. Fixes vs spec: His arms 128px + wider wash; 8a bloom r165 multiply over slip. Risk R1 (slip on followers = motif, not quote) for the guardrail panel.

## 2026-11-11 evening: V3 (consistency)
- Owner: north stars = p07 (He lifts the boy) + owner still; rest looked off/inconsistent; v2 p09 clip = AI slop (girl passes through arm).
- v3/stills: 15 redrawn with ONLY p07 + owner still as refs ($1.20, p05 redo for giant Jesus). v3/clips: 16 Kling PRO (15 + calm p09), $6.10. Job ids v3/_jobs.txt. build_v3.py -> EP16_PREVIEW_v3.mp4 (=Remotion base now; v2 base backed up in _build_v3/). Text v2 made more see-through (60%) -> EP16_REMOTION_v3.mp4 -> EP16_SCORED_v3.mp4. Page _FILM_V3.html. Total ~$21.
- Next: owner OK -> SFX -> packaging card + red team + publish pack -> V6 roster #16.
