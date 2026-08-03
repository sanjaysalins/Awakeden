"""living-sketchbook -- Bronze Serpent LONG pilot: redo the 12 user-flagged
spreads (see `_redo_notes.json`, exported from `_REDO_NOTES.html`).

Diagnosis per spread (see chat record / RESUME.md for the full writeup):
- s06: real defect -- the reaching hand overlapped/covered the face.
- s57: real defect -- the original prompt literally said "Moses, small...
  Jesus, larger", which rendered as a dwarfism-looking scale error, not a
  subtle emphasis effect.
- s49: real defect -- the hand read as gripping/holding the crossbeam
  rather than pinned by a nail (ambiguous crucifixion imagery).
- s66: REAL BUG, not a style issue -- the prompt (still correct, unchanged
  below) asks for a Moses face close-up; the actual render was a copy of
  the landing's torn-page/small-Christ composition, ignoring the prompt
  entirely. Clean re-roll, same prompt.
- s68: NOT included here. Already corrected in the 16:9 redo pass and
  confirmed good; the earlier "looks similar" flag was very likely s66's
  broken render (above) creating an apparent duplicate. Left untouched.
- s22, s35, s50, s61: genuine repetition among several "Moses reflects"
  close-ups -- given a distinct PRODUCTION_APPROVED style-lab variant each
  (validated against `pipeline/style_variety.py`'s budget/spacing/theology
  guardrail before this script was written -- 4 variant-spreads, 0 fails,
  min gap 11+ throughout, well under the 68-spread budget of 10).
- s40, s47, s53: genuine repetition too, but too close (by spread number)
  to another variant-assigned spread to also take one under the
  min_spread_gap=8 rule -- fixed instead with genuinely different
  BLOCKING/framing (wide vs close, angle change), same discipline the
  short used for its own s07/s09/s11 pose-collision fix.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s3_redo_flagged.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _s2_stills as s2  # reuse HF/MODEL/OUT/MOSES/JESUS/BRONZE_SERPENT/FULLBLEED/MOSES_REF/JESUS_REF/run()/cost

# ---------------------------------------------------------------------------
# 4 new STYLE constants -- the reusable TECHNIQUE paragraph from each
# production_approved style-lab variant, re-merged with this episode's own
# locked paper-collage/gold-leaf/no-lettering closing so the page material
# stays consistent episode-wide (only the drawing TECHNIQUE differs).
# ---------------------------------------------------------------------------

STYLE_SL04_UNDERDRAWING = (
    "Editorial documentary sketch illustration: finished ink linework "
    "sitting on top of clearly visible graphite construction underdrawing "
    "-- ghosted proportion lines, discarded first attempts at limb "
    "positions, faint blocking boxes still showing through. The drawing "
    "looks caught mid-process, not resolved. Muted watercolor wash applied "
    "loosely over both layers, drawn on aged warm cream paper. Aged-print "
    "paper-collage aesthetic: warm cream and kraft textured stock, torn "
    "and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile "
    "hand-made feel, muted ink-red and ink-blue accents, a thin strip of "
    "gold leaf at one edge. CRITICAL: absolutely NO lettering, numerals, "
    "words, newsprint, printed book-page text, handwriting, ruler "
    "markings, dates, or captions ANYWHERE on ANY layer -- every paper "
    "surface is BLANK textured stock."
)

STYLE_SL13_CHARCOAL_ERASER = (
    "Editorial documentary sketch illustration: soft charcoal laid down "
    "as broad smudged tone across the whole sheet, then the image LIFTED "
    "OUT with a kneaded eraser -- highlights are erased, not painted. "
    "Visible fingerprints, smears, dust and hand-drag across the surface. "
    "Minimal ink accents, almost no colour beyond a single muted ink-red "
    "note, drawn on aged warm cream paper. Aged-print paper-collage "
    "aesthetic: warm cream and kraft textured stock, torn and cut-paper "
    "edges, subtle offset-halftone dot texture, faint engineering-grid "
    "hairlines, soft raking museum light, tactile hand-made feel, a thin "
    "strip of gold leaf at one edge. CRITICAL: absolutely NO lettering, "
    "numerals, words, newsprint, printed book-page text, handwriting, "
    "ruler markings, dates, or captions ANYWHERE on ANY layer -- every "
    "paper surface is BLANK textured stock."
)

STYLE_SV09_MONOTYPE = (
    "Experimental editorial documentary illustration resembling a unique "
    "hand-pulled monotype combined with graphite drawing, dry-brush ink, "
    "charcoal dust, and restrained watercolor. Use uneven ink transfer, "
    "compressed black-brown shadows, rubbed textures, accidental "
    "fingerprints, ghost impressions, scraped pigment, lifted highlights, "
    "smudged contours, and areas where the ink appears partially lost "
    "during printing. Printed on aged warm cream and kraft paper fibres "
    "with narrow torn edges, subtle offset-halftone grain, faint "
    "engineering-grid hairlines, worn surface abrasion, soft raking "
    "museum light, muted ink-red and ink-blue accents, and one thin "
    "fragment of imperfect gold leaf along an outer edge. CRITICAL: "
    "absolutely NO lettering, numerals, words, newsprint, printed pages, "
    "book text, handwriting, captions, dates, ruler markings, labels, "
    "stamps, seals, archival notes, pseudo-script, or marks resembling "
    "typography anywhere. Every paper layer must remain completely blank "
    "textured stock."
)

STYLE_SV15_ABSTRACTION_FOCAL = (
    "Experimental editorial documentary sketch illustration balancing "
    "precise observational drawing with bold controlled abstraction. Use "
    "finely rendered graphite and ink only at the central focal point, "
    "while the surrounding figure and environment dissolve into "
    "watercolor blooms, dry-brush masses, charcoal smudges, erased "
    "contours, torn-paper silhouettes, halftone grain, translucent "
    "washes, and loose gestural marks. Aged warm cream and kraft "
    "paper-collage aesthetic with visible fibres, narrow torn margins, "
    "faint engineering-grid hairlines, subtle offset-print texture, muted "
    "ink-red and ink-blue accents, shallow layered-paper shadows, soft "
    "raking museum light, surface abrasion, and one thin irregular strip "
    "of distressed gold leaf at the outer edge. CRITICAL: absolutely NO "
    "lettering, numerals, words, printed text, newsprint, handwriting, "
    "dates, captions, labels, ruler markings, stamps, seals, "
    "inscriptions, pseudo-script, or marks resembling typography "
    "anywhere. Every visible paper surface must remain blank textured "
    "stock."
)

FULLBLEED = s2.FULLBLEED
MOSES = s2.MOSES
JESUS = s2.JESUS
BRONZE_SERPENT = s2.BRONZE_SERPENT

# (name, style_const, refs_tag, scene)
REDOS = [
    # s06 -- CONTENT FIX: hand was overlapping/covering the face.
    ("s06_dying_hand_eye", s2.STYLE, "",
     f"Extreme close-up, a single ordinary wilderness-worn Hebrew man's "
     f"open, empty, reaching hand held clearly to ONE SIDE of his face -- "
     f"the hand and the eye occupy separate, non-overlapping regions of "
     f"the frame, the hand never crosses in front of or obscures any part "
     f"of the face -- and beyond it, his own eye, fully visible and "
     f"unobstructed, weary, searching, lifted upward and outward rather "
     f"than reaching or grasping -- no other body part, no wound, no "
     f"blood, no second person anywhere in the frame, the composition "
     f"built entirely around the theme of a look rather than a climb or "
     f"a grasp. {FULLBLEED}"),

    # s22 -- VARIETY: sl04 visible-underdrawing (fits "still processing,
    # not yet resolved" -- Moses surprised/listening).
    ("s22_moses_listening", STYLE_SL04_UNDERDRAWING, "moses",
     f"A mid close-up on {MOSES}'s face, head tilted slightly as though "
     f"listening intently to an unseen voice, brows drawn in surprise "
     f"and searching thought, staff loosely in one hand at his side. "
     f"{FULLBLEED}"),

    # s35 -- VARIETY: sv09 hand-pulled monotype (fits the vulnerable,
    # half-remembered register of "I will be honest with you").
    ("s35_moses_honest_close", STYLE_SV09_MONOTYPE, "moses",
     f"A close, intimate mid-shot: {MOSES}'s face turned directly toward "
     f"the viewer, his expression open and searching, about to speak "
     f"plainly, staff loosely at his side -- the monotype's own ghost "
     f"impressions and rubbed edges gathering softly at the OUTER edges "
     f"of the composition only, his eyes and the center of his face "
     f"staying the clearest, most legible passage in the frame. "
     f"{FULLBLEED}"),

    # s40 -- CONTENT FIX: genuinely different BLOCKING (wide vs the tight
    # close-up cluster at s22/s35/s61), same content/meaning.
    ("s40_moses_resolve_returning", s2.STYLE, "moses",
     f"A wide mid-shot, a genuinely different body scale from any nearby "
     f"spread: {MOSES}'s full upper body and the entire {BRONZE_SERPENT} "
     f"on its pole both clearly visible together in the same frame, his "
     f"one hand resting on the base of the pole beside him, but his eyes "
     f"lifted up and away from it toward the open sky, his whole posture "
     f"-- not just his face -- shifting from a dread-laden stoop toward "
     f"settled, upright resolve and trust. {FULLBLEED}"),

    # s47 -- CONTENT FIX: genuinely different camera angle from the
    # frontal Golgotha shots at s45/s51 (three-quarter/low, not frontal).
    ("s47_golgotha_midshot", s2.STYLE, "jesus",
     f"A three-quarter angle view of {JESUS} lifted up on the plain "
     f"wooden cross, the camera positioned slightly below and to one "
     f"side rather than dead-on, so the weight and grain of the wooden "
     f"crossbeam reads clearly against the sky and His bowed head is "
     f"seen in near-profile rather than frontally -- no visible wound, "
     f"no blood, the darkened sky pressing low behind Him -- restrained, "
     f"sacred, leading toward the quote about bearing a curse. "
     f"{FULLBLEED}"),

    # s49 -- CONTENT FIX: the hand read as gripping the beam rather than
    # pinned by a nail -- made explicit and unambiguous.
    ("s49_christ_radiant_begin", s2.STYLE, "jesus",
     f"{JESUS} lifted up on the plain wooden cross, both hands affixed "
     f"to the crossbeam by a single small dark nail each, fingers "
     f"naturally relaxed and gently curled from the nail's own position "
     f"-- NOT gripping, clutching, or actively holding on to the wood -- "
     f"a soft warm glow beginning to gather around His form, the "
     f"register shifting from the darkened-sky suffering of the earlier "
     f"spreads toward glory, head still bowed but the light growing, "
     f"gold reserved only for this glow, never elsewhere in the frame. "
     f"{FULLBLEED}"),

    # s50 -- VARIETY: sl13 charcoal-and-eraser (structurally prevents the
    # smooth/cartoon look -- the glow becomes a LIFTED highlight, not a
    # painted/airbrushed one).
    ("s50_christ_close_words", STYLE_SL13_CHARCOAL_ERASER, "jesus",
     f"A close reverent shot on {JESUS}'s face and upper form, lifted on "
     f"the cross, the gathering warm glow around His head and shoulders "
     f"rendered as charcoal LIFTED OUT with a kneaded eraser rather than "
     f"painted or airbrushed light, His expression calm and resolved, "
     f"about to speak. {FULLBLEED}"),

    # s53 -- CONTENT FIX: genuinely wider framing than the pure face-crop
    # cluster (s22/s35/s61), including his hand-on-chest gesture and robe.
    ("s53_moses_know_that_now", s2.STYLE, "moses",
     f"A waist-up three-quarter shot, noticeably wider than a pure face "
     f"close-up so his whole gesture reads clearly: {MOSES}'s gaze "
     f"lowered inward rather than toward the viewer, one weathered hand "
     f"raised to rest against his own chest, visible together with his "
     f"robe, his staff, and the fall of his beard -- a small rueful, "
     f"honest half-smile of hard-won understanding, eyes steady. "
     f"{FULLBLEED}"),

    # s57 -- CONTENT FIX: the ORIGINAL prompt's "small... larger" wording
    # is exactly what produced the dwarfism-looking scale error. Replaced
    # with depth-based (not body-size-based) visual weight.
    ("s57_bridge_moses_christ", s2.STYLE, "moses,jesus",
     f"A composition bridging both figures, BOTH rendered at natural, "
     f"anatomically consistent human proportions -- do NOT shrink, "
     f"distort, or dwarf either figure's body size relative to the "
     f"other: {MOSES} stands in the near foreground, closer to the "
     f"viewer, and beyond him, further back in the same ground plane, "
     f"{JESUS} stands radiant with a warm gold glow -- the visual "
     f"emphasis shifts from Moses toward the glowing figure of Christ "
     f"through LIGHT and gaze direction alone, never through an "
     f"unnatural difference in their actual body proportions, gold "
     f"reserved only for that glow. {FULLBLEED}"),

    # s61 -- VARIETY: sv15 controlled abstraction, one precise focal
    # point -- his eyes are the natural focus for "That is you. That is me."
    ("s61_moses_thatisyou", STYLE_SV15_ABSTRACTION_FOCAL, "moses",
     f"An intimate close-up on {MOSES}'s face, direct and searching, "
     f"addressing the viewer as though speaking to them personally, a "
     f"shared vulnerability in his expression -- the single precise "
     f"focal point of the whole composition is his eyes and brow, "
     f"rendered in fine crisp graphite-and-ink detail, while his hair, "
     f"beard, robe, and the space around him dissolve outward into "
     f"soft watercolor blooms and charcoal smudge. {FULLBLEED}"),

    # s66 -- CLEAN RE-ROLL: prompt is unchanged (it was already correct --
    # the earlier render ignored it and produced a copy of the landing
    # composition instead; this is a model-execution failure, not a
    # prompt problem).
    ("s66_moses_direct_question", s2.STYLE, "moses",
     f"The most intimate direct-address spread of the film: an extreme "
     f"close-up on {MOSES}'s face alone, filling the frame corner to "
     f"corner, his eyes locked directly on the viewer, a final "
     f"searching, personal question in his expression. {FULLBLEED}"),
]


def resolve_refs(tag):
    refs = []
    if not tag:
        return refs
    if "moses" in tag:
        refs.append(s2.MOSES_REF)
        if s2.MOSES_REF2.exists():
            refs.append(s2.MOSES_REF2)
    if "jesus" in tag:
        refs.append(s2.JESUS_REF)
        if s2.JESUS_REF2.exists():
            refs.append(s2.JESUS_REF2)
    return refs


def main():
    for name, style, tag, scene in REDOS:
        out = s2.OUT / f"{name}.png"
        if out.exists():
            archived = s2.OUT / f"{name}.v1_flagged.png"
            if not archived.exists():
                out.rename(archived)
                print(f"[archive] {name} -> {archived.name}")
        refs = resolve_refs(tag)
        prompt = style + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = s2.run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = s2.run(prompt, out, refs)
        if ok:
            try:
                s2.cost.record_hf(s2.EPISODE, "long", "stills_redo", s2.MODEL, note=f"[bronzeserpentlong-redo] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {s2.OUT}")


if __name__ == "__main__":
    main()
