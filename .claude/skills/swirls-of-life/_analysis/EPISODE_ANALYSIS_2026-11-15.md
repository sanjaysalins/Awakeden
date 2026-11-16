# Swirls of Life — cross-episode analysis (2026-11-15)

Source: read-only extract of all 12 episode folders + 2 pilots in
`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\`, memory files, and
`data\spend_ledger.jsonl`. Costs are rough (ledger names are inconsistent).

## The storyboard-page format (what the owner wants repeatable)
Eps 1, 2, 4, 5, 7, 8, 10, 11, 13 + pilot 01 (Jacob's Ladder).
- Woodcut FRONT cover + woodcut BACK cover bookend the film.
- Interior pages (`panel_style="woodcut_hybrid"`): baked "SEQ:" title top-left, "F##" top-right,
  a row of 3 small labeled sketch panels, ONE large hero scene below, a short handwritten caption.
- Blue/gold "Swirls of Life" ink motif dosed by story stage (0 absent, 1 first trace, 2 present,
  3 diffused). Motif variants: Stain (dead ink, ep10), Fray (ep8, Thomas), swirl.
- Fable writes a design brief (1,100-1,400 lines on eps 10/13 — too big), Sonnet writes `episode.py`
  (PageSpec / CoverSpec / MANIFEST), driven by `swirls_episode.py plan|still|animate|verify|assemble`.
- Runtimes 62-106 s, 6-9 pages + 2 covers, 720x1280, cost $5-30, 3-6 fix rounds each.
- The audience loves the swirl look (owner, 2026-11-15).

## Pipeline as actually run (old)
words (hand-authored or Fable + 5-CLI panel rounds) -> per_turn_synth (--target N, atempo up to
1.95, too fast on ep5/ep8; later --natural) -> Fable brief -> refs cropped from first approved
render -> OpenArt nano-banana-pro stills (HF before 2026-08-27) -> V2 Vision audit -> OpenArt Kling 3
Omni clips (OpenArt has NO veo; veo tags silently render on Kling) -> swirls_assemble (freeze /
boomerang / tail-loop fill) -> felt-piano score (generate_score_piano.py, 2-part split) -> $0 SFX
(build_sfx.py, sfxlib) -> build_srt.py (no burned captions) -> publish pack.

## Recurring defects (ranked) and the fix that worked
1. Kling invents speech bubbles (ep4, ep5, ep7, ep8, pilot1). Wording never fixed it; REMOVING the
   figure's motion did.
2. Border / caption strip on covers (ep2, ep5, ep7, ep8; ep13 accepted a hairline). Resists both
   positive and negative wording; verify by pixel scan.
3. Character / costume / object drift (ep4 Naaman, ep5, ep7 bier, ep11 Samaritan outfit, pilot1
   everything). Fix: a ref for EVERY recurring subject + a face ref for close panels + one per
   costume state; redraw from the 1-2 north-star stills.
4. Motif rendered literally: cord, drip, flower, ring, puddle (pilot1, ep2, ep5, ep7, ep8). Motif
   must be inline in the scene text, "brushstroke + one direction + property negatives". Never
   animate the ink (AI hallucinates glows/blobs).
5. Baked text errors: shot-type label drawn ("MEDIUM TWO-SHOT", ep8/ep10), duplicate panel labels
   (ep5), stray digits, em-dashes (ep8 "AI slop"), caption fades in clip (ep7), verification text
   drawn (pilot2). Keep each string short; no verification verbs inside the prompt.
6. Clones / extra / vanishing / merging figures (ep13 F03, ep16). Fix: near/large + far/small depth.
7. Hard prop shapes: cross as X or log (ep13, 6 of 9 pages). Fix: camera-angle change after 2 failed
   wordings; check at full frame (tight crop fakes defects).
8. Fill / timing: backward boomerang (ep4 crowd, ep8 angels), dead freezes (ep1, ep2, ep4), freeze
   never trims long clips (ep1 +3.6 s, ep11 drift), duplicate -vf (pilot1, ep2). OWNER NOW BANS ALL FILL.
9. Score dead air (ep13 silent 0-63 s) / too loud (ep8) / duck not transferable (ep2, ep4).
10. Fixed PNG does not change shipped MP4 — must re-animate (ep7).
11. Invented motion / NSFW reading in clips (ep10 F03). Check literal first + last frame + pixel diff.

## Owner quotes worth keeping
- "now you are just doing a freeze, which hate" (ep1); "I still see freeze pain" (ep2)
- "hate the backwards and freeze and the zoom in cuts ... spend more ... high production" (ep16)
- "I feel some of our landing is too simple, it feels very tired, will you come, will you see" (ep4)
- "love this score, this perhaps the best north star score" (ep8 felt piano)
- "the ai slop in the image i.e. emdash and double dashes ect, it feels amaturish" (ep8)
- "the swirls... was missing in the middle pages" (ep2)
- ep10 narration+voice: "this is the standard we should maintain, almost a north star for me"
- "can we have a score right from the start to the end please" (ep13)

## Owner rules that now OVERRIDE the old skill docs
- No freeze / boomerang / ping-pong / zoom / crop fill. Every clip >= its slot, trim only, 1.0x,
  hard cuts; plan shot count from real line timings (memory feedback_no_freeze_boomerang_zoom_fill,
  feedback_no_pingpong_freeze_crop_fill). SKILL.md step 0 "Focal Tour gap-fill" is stale.
- Hero images always get real animation, no Ken Burns (feedback_hero_images_always_animated).
- OpenArt default, Higgsfield never automatic (SKILL.md still says hf).
- Dialogue: emotion cues + stability 0.3, 2 takes (feedback_dialogue_needs_emotion_cues).
- Words-before-money, 5 guardrail questions, global-audience test, packaging card, blind panels
  with a Fable seat, no AI wording in public text, landing hold >= 3.0 s.
- Elevate panel (2026-11-08): the gap is the viewer — first 2 s (old covers held 4-10 s), runtime
  too long, 720p, loop ending, new ending shape each time.

## Newer POC way (eps 6, 12, 16, Bartimaeus) — NOT the Swirls format, but steal the steps
Blind multi-writer words + guardrail panel; voice --natural with cues; SHOT_PLAN from timeline.json;
refs for every costume state BEFORE stills; Kling pro clips each longer than slot; build fails loudly
if a clip is short; 2-part score; Remotion text; blind film red team; packaging card + publish pack +
copy red team. Reference: `poc_desert_storybook_heroes\EPISODE_PLAYBOOK.md`,
`swirls_episode_16_let_the_little_children\HANDOVER_RESUME.md`.

## Shared code that exists
`test_the_cross\swirls_page.py` (PageSpec, still/anim prompt assembly, refs manifest),
`swirls_cover.py` (CoverSpec), `swirls_assemble.py` (fill modes — needs a trim-only mode),
`swirls_verify.py` (SW-L*/SW-F*/V2/SW-A* gates), `swirls_episode.py` (runner), `build_srt.py`,
`swirls_upload_tracker.py`, `openart_bridge.py` + `AGENT_BRIDGE.md`, per-episode copies of
`generate_score_piano.py` and `build_sfx.py`, `sfx_pilots\sfxlib`.
