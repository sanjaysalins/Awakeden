# Independent review — codex (OK, 438s)

Option A needs revision before template work. The plan has not established what viewers valued, and its localization workflow can overwrite reviewed captions.

These findings come from the builders, caption files, publishing code and device definitions. Actual player behaviour and audience response still need testing.

1. **The evidence comes after the commitment.**  
   “**Also: read the real analytics before copying**” belongs before A1, not after A5. One owner report cannot establish whether viewers liked the topic, performance, comic look, caption pills or brevity. Read retention, viewed-versus-swiped-away, completion, shares per engaged view and traffic sources alongside comparable shorts. Those comparisons can guide hypotheses; they cannot isolate causes.

   A4’s “**owner compares old vs new**” tests owner preference. It does not establish audience improvement or repeatability. Define success and a stopping rule before building.

2. **The proposed DNA contains an editorial assumption disguised as Scripture.**  
   “**contrast pairs taken from the text’s own words**” overstates the evidence: “Someday” is narrator interpretation, not wording in Luke 23:42. The source also omits the thief’s acknowledgement of guilt and Jesus’ innocence in verses 40–41. Repeating “asked for very little → received much” could progressively flatten the passage’s meaning.

   The measurements also need correction: the locked script contains **74 whitespace-separated words**, and `voices.json` specifies **four speakers**. Distinguish eight spoken turns, ten lettering events and fourteen shots before deriving template constraints.

3. **A3 understates the actual input contract.**  
   “**episode words + timings in, film out**” omits clip selection, source in-points, framing, zooms, speaker identity, visual continuity and motion anchors. Those are manually specified in [build_s32.py](F:/slk/PycharmProjects/JesusInTheBible/poc_comic_page/_ELEVATE/build_s32.py:15).

   Either those decisions remain manual, or this is also an editorial planning system. Say which. Otherwise the “template” merely relocates substantial episode work into undocumented inputs.

   There is already an unlettered intermediate at `poc_comic_page/_ELEVATE/work/tp_S32/base.mp4`. A small experimental export can start there.

4. **The localization architecture is unresolved.**  
   “**word-free master film + a separate swappable lettering layer per language**” describes production assets, but does not specify what viewers receive. Uploading an SRT does not swap lettering in the video picture.

   Choose between a common picture with selectable subtitles and separate picture exports with localized lettering. YouTube supports additional audio tracks on a single Short, but that does not provide language-switched graphic overlays. [YouTube’s multi-language documentation](https://support.google.com/youtube/answer/13338784?hl=en)

   This also affects the hook. Removing “PARADISE FOR A CRIMINAL?” changes the opening experience; the spoken “Why?” starts at **3.383 seconds**. The claimed “hook ≤3 s” needs reassessment in the clean version.

5. **The subtitle rules fail against the existing file—and publishing can undo repairs.**  
   “**max ~32 chars, min 1.2 s each**” is not implemented by the current workflow. In [captions.srt](F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/today_paradise_short32/publish/captions.srt:1):

   - “Why?” lasts **0.326 seconds**.
   - “Him.” lasts **0.300 seconds**.
   - A Scripture cue runs to **43 characters**, followed by “kingdom.” for **0.402 seconds**.

   The existing generator defaults to 42 characters, splits after reaching its threshold, and permits 0.3-second cues. More seriously, [publish_pack.py](F:/slk/PycharmProjects/JesusInTheBible/pipeline/publish_pack.py:368) rewrites `captions.srt` from alignment data during pack refreshes.

   Fix and reuse that path. Preserve reviewed, language-labelled caption sources. Verify phrase grouping, reading speed, overlaps and reveal timing; simply extending every short cue can create new collisions.

6. **“Many languages” is treated as English with longer strings.**  
   “**expect Spanish/German ~25% longer**” is inadequate for planning. The missing cases include:

   - Arabic direction, punctuation and mixed-direction verse references.
   - CJK and Thai segmentation; the current pill renderer uses whitespace splitting.
   - Font coverage and shaping for localized picture lettering.
   - Different word order moving the crucial reveal within a sentence.
   - Speaker identification after removing the speaker tabs.

   “**Verse chips as numbers only (‘23:43’)**” also removes the book identity. That is ambiguous for newcomers.

   Public-domain status does not establish readability or editorial suitability. Record the exact edition and source, and have a fluent reviewer check both Scripture excerpts and surrounding narration. Keep quotation and interpretation distinguishable.

   Also address platform-generated translations: eligible YouTube channels can have automatic dubbing enabled by default. Unreviewed output could bypass “never machine-translate Scripture.” Check publication settings. [YouTube’s automatic-dubbing guidance](https://support.google.com/youtube/answer/15569972?hl=en)

7. **The safe-zone claim is an untested approximation.**  
   “**bottom ~25% kept clear**” does not verify the actual platform interface, caption size or right-hand controls. Test representative phones, caption settings and each intended platform.

   Nor can SRT reproduce the pill’s typography and speaker styling: YouTube accepts basic UTF-8 SRT without styling markup. [Supported caption formats](https://support.google.com/youtube/answer/2734698?hl=en)

   Avoid rebuilding a duplicate caption system unless the pilot demonstrates that picture lettering adds enough value to justify its localization burden.

8. **The named doodle tools are not interchangeable components.**  
   “**Repo already has many $0 deterministic devices**” overstates their applicability. `annotators-circle` is designed to mark approved words already on a page; `marginalia` adds text labels to stills. Neither directly supplies tracked, word-free annotations on moving faces.

   The Thief builder uses ffmpeg and raster overlays; `_remotion/` is another rendering path. Specify the chosen compositor, timing interface and coordinates before estimating integration effort. Reuse compatible primitives instead of treating the device names as a finished kit.

9. **The doodle quota risks repeating a failure already documented here.**  
   “**3–5 doodles per film**” rewards quantity without requiring a storytelling benefit. [_remotion/src/MaryMarthaV2.tsx](F:/slk/PycharmProjects/JesusInTheBible/_remotion/src/MaryMarthaV2.tsx:1) explicitly records that the owner found the previous doodles forced.

   Specific problems with these proposals:

   - A face circle needs to follow both the added camera push and movement inside the generated clip.
   - An arrow between crosses may become unclear across crops and cuts.
   - A calendar-to-sunrise transition could imply “next morning,” weakening “today.”
   - “An underline beneath Jesus’ words” depends on lettering, contradicting the word-free requirement.
   - Drawing, subtitles and an expressive face can compete for attention at the decisive moment.

   Allow **zero** doodles. Require each effect to clarify something observable, then test it in motion at phone size. A mock page cannot establish that.

10. **The verification and cost gates are incomplete.**  
    A3 lists length, hook timing, bottom clearance, English removal and landing hold. It omits quotation fidelity, visual accuracy, newcomer comprehension, speaker attribution and the specified independent film review.

    Put the five guardrail questions at explicit checkpoints, with a fresh Fable reviewer who has not seen the design rationale. Reuse existing checks where applicable, including `narration_gate.py`; assess how `corpus_diversity.py` handles this script format before relying on it.

    “**a sibling short cost ~$8.55**” is also unreconciled evidence. The supporting [handover](F:/slk/PycharmProjects/JesusInTheBible/poc_comic_page/_ELEVATE/HANDOVER_RESUME.md:21) lists amounts adding to **$10.19** unless some entries overlap. It mixes tests, stills, clips and recordings. Establish a comparable acquisition budget with retry allowance, plus localization and review effort. “~$0” can reasonably mean no additional generation spend; it should not imply negligible production work.

If designing this from scratch, I would use this sequence:

1. **Establish the baseline.** Confirm the exact published version and inspect its performance alongside comparable films.
2. **Define a flexible editorial promise.** One clear question, one tension grounded in the passage, one decisive answer involving Jesus, and one earned takeaway. Keep 38 seconds as a target; avoid mandatory voice counts and contrast pairs.
3. **Run a small comparison edit.** Hold audio and cuts constant. Compare existing lettering with clean-picture subtitles, then test one purposeful motion intervention separately.
4. **Prove localization immediately.** Finish one priority language through translation, timing, upload and native-speaker review before expanding. Separately stress-test the renderer with a different writing system.
5. **Test transfer before abstraction.** Manually produce two substantially different stories. Extract only the repeated mechanics that survived all three films.

**The biggest staleness risk is copying the rhetorical skeleton.** Repeated paradox questions, two opposing characters, “Not X. Y,” and the same soft invitation will become predictable even with fresh artwork. Track recent hooks, sentence patterns, emotional turns, endings and visual motifs. Reject stories that require invented contrasts to fit the formula.

VERDICT: REVISE
TOP FIXES:
1. Move analytics and a controlled comparison edit ahead of template construction.
2. Choose the localization delivery model and protect reviewed captions from regeneration.
3. Prove the formula on different stories; remove fixed doodle and rhetorical quotas.
