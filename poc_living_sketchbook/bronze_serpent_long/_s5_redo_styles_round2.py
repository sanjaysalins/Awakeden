"""living-sketchbook -- Bronze Serpent LONG pilot: STILLS REDO ROUND 2.

User asked directly (2026-08-02) to recreate 4 stills in genuinely different
rendering styles from the style-lab bake-off library, tracing the passage's
own dramatic arc: darkness of the curse (47) -> the sky itself turns to
gold (49) -> the glow bleeds outward (50) -> cool retrospect (53). Design by
Fable (see conversation record); this script applies it.

Style picks (all production_approved, none reused elsewhere in this episode
except sl13 which is being FREED from s50, not reused here):
  s47 -> sv11_ink_wash_chiaroscuro_and_scratched_light (dread-with-one-light)
  s49 -> sl17_gold_leaf_as_structure (glory beat -- the register FLIPS here;
         gold_leaf_conflict=true, deliberately used since this is a genuine
         glory beat, matching the episode's own s67 Gilded Proclamation
         precedent of a gold ground reserved for Christ's glory)
  s50 -> sl06_wet_in_wet_bleed (the glow bleeding outward = the beat's own
         doctrine -- "I... will draw all men unto me" -- enacted in the medium)
  s53 -> sv05_cyanotype_blue_focus (testimony/memory register -- "I know
         that now" looking back from the far side of a long life)

KNOWN spacing-rule tension (recorded, not silently avoided): these 4 sit
within a 6-spread span, well under pipeline/style_variety.py's normal
min-gap-8 rule. Deliberate human override -- the styles trace the passage's
own arc, all locked page material (paper/torn-edge/halftone/grid) stays
identical across all 4, and base-style spreads (48/51/52) sit between them
as breathers. Recorded here per SKILL.md sec.4's override discipline, not
loosening the lint itself.

Doctrine content (wound-lock, no-gore, gold=Christ's-glory-only, reverent/
restrained) is UNCHANGED from the already-redone content in _s4_animate.py's
prompts for these spreads -- only the rendering TECHNIQUE changes here.

Old stills archived to <name>.v2_style_superseded.png (v1 archives already
exist from the earlier redo round on some of these). Old animated clips for
all 4 go stale the moment the still changes -- re-animate after eye-approval,
do NOT re-animate before the new still is approved.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s5_redo_styles_round2.py
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _s2_stills as s2

MOSES = s2.MOSES
JESUS = s2.JESUS
FULLBLEED = s2.FULLBLEED

STYLE_SV11_CHIAROSCURO = (
    "Dramatic editorial documentary sketch illustration using expressive "
    "graphite, black-brown ink wash, dry-brush shadow, scratched-back "
    "highlights, and restrained muted watercolor on aged warm cream paper. "
    "Create strong chiaroscuro through deep pooled ink, feathered wash "
    "edges, dry-brush interruptions, pale untouched paper highlights, "
    "scraped pigment, and sharp selective contour lines. Aged archival "
    "paper-collage aesthetic: warm cream and kraft textured stock, narrow "
    "torn edges, subtle offset-halftone grain, faint engineering-grid "
    "hairlines, water stains, visible paper fibres, muted ink-red and "
    "ink-blue accents, soft raking museum light, and one narrow distressed "
    "strip of gold leaf at the outer edge. CRITICAL: absolutely NO "
    "lettering, numerals, words, handwriting, dates, captions, newsprint, "
    "printed book-page text, ruler markings, labels, stamps, pseudo-script, "
    "symbolic writing, or text-like decoration anywhere. Every visible "
    "paper layer is blank textured stock."
)

STYLE_SL17_GOLD_GROUND = (
    "Editorial documentary sketch illustration on aged warm cream paper: "
    "gold leaf is not an accent but the compositional backbone -- a broad "
    "burnished gold field forms the entire sky and horizon band, cracked "
    "and worn like an icon panel, with the graphite-and-ink figure drawn "
    "dark and reverent against it. Byzantine flatness meeting loose "
    "documentary linework. Minimal muted watercolor wash elsewhere. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured "
    "stock, torn and cut-paper edges, subtle offset-halftone dot texture, "
    "faint engineering-grid hairlines, soft raking museum light, tactile "
    "hand-made feel, muted ink-red and ink-blue accents. CRITICAL: "
    "absolutely NO lettering, numerals, words, newsprint, printed "
    "book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

STYLE_SL06_WET_IN_WET = (
    "Editorial documentary sketch illustration on aged warm cream paper: "
    "watercolor applied wet-into-wet so pigment blooms, backruns and "
    "cauliflower edges form freely, color migrating well beyond the ink "
    "lines and pooling at the paper's low points, a cockled, slightly "
    "buckled damp paper texture -- the ink linework kept minimal and "
    "sharp so it cuts through the soft bleed. Aged-print paper-collage "
    "aesthetic: warm cream and kraft textured stock, torn and cut-paper "
    "edges, subtle offset-halftone dot texture, faint engineering-grid "
    "hairlines, soft raking museum light, tactile hand-made feel, muted "
    "ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or "
    "captions ANYWHERE on ANY layer -- every paper surface is BLANK "
    "textured stock."
)

STYLE_SV05_CYANOTYPE = (
    "Editorial documentary sketch illustration, heavily leaning towards a "
    "vintage cyanotype mixed-media aesthetic: loose graphite-and-ink "
    "linework used only for minimal structure, submerged beneath heavy, "
    "deep indigo and Prussian blue watercolor wash on aged warm cream "
    "paper. The blue wash replaces all neutrals. Aged-print paper-collage "
    "aesthetic: warm cream and kraft textured stock, torn and cut-paper "
    "edges, prominent offset-halftone dot texture, faint engineering-grid "
    "hairlines, soft raking museum light, tactile hand-made feel, muted "
    "ink-red accents used sparingly, a thin strip of gold leaf at one "
    "edge for dramatic warm contrast. CRITICAL: absolutely NO lettering, "
    "numerals, words, newsprint, printed book-page text, handwriting, "
    "ruler markings, dates, or captions ANYWHERE on ANY layer -- every "
    "paper surface is BLANK textured stock."
)

# (name, style, refs-tag, scene)
REDOS = [
    ("s47_golgotha_midshot", STYLE_SV11_CHIAROSCURO, "jesus2",
     f"A three-quarter angle view of {JESUS} lifted up on the plain wooden "
     f"cross, the camera positioned slightly below and to one side rather "
     f"than dead-on, His bowed head seen in near-profile -- the "
     f"composition's ONE pale scratched-light passage falls only on His "
     f"bowed head, His shoulders, and the grain of the wooden crossbeam, "
     f"while the darkened supernatural sky and the bare hill below merge "
     f"into a single connected mass of deep pooled black-brown ink wash "
     f"pressing in around Him from every side -- no visible wound, no "
     f"blood, restrained, sacred, never graphic, the weight of the "
     f"darkness itself carrying the sense of a curse being borne. "
     f"{FULLBLEED}"),

    ("s49_christ_radiant_begin", STYLE_SL17_GOLD_GROUND, "jesus2",
     f"{JESUS} lifted up on the plain wooden cross, both hands affixed to "
     f"the crossbeam by a single small dark nail each, fingers naturally "
     f"relaxed and gently curled from the nail's own position -- NOT "
     f"gripping, clutching, or actively holding on to the wood -- head "
     f"still bowed, and the register turning from suffering to glory: the "
     f"darkened sky of the earlier spreads is gone, and behind Him the "
     f"entire sky is the burnished, cracked gold-leaf ground itself, an "
     f"icon panel's field of glory -- the gold touches ONLY that "
     f"sky-ground around Christ; His body, the cross, and the bare hill "
     f"stay plain graphite, ink, and muted wash, no visible wound, no "
     f"blood, restrained and sacred. {FULLBLEED}"),

    ("s50_christ_close_words", STYLE_SL06_WET_IN_WET, "jesus2",
     f"A close reverent shot on {JESUS}'s face and upper form, lifted on "
     f"the cross, His expression calm and resolved, about to speak -- His "
     f"face, eyes, and beard held in the sharpest, most precise ink "
     f"linework in the frame, while the gathering warm glow around His "
     f"head and shoulders is painted wet-into-wet, the warm pigment "
     f"blooming and bleeding softly outward from His form into the damp "
     f"paper beyond it, as though the light itself is spreading through "
     f"the page -- no visible wound, no blood, the warm gold tones "
     f"reserved only for this glow, never elsewhere in the frame. "
     f"{FULLBLEED}"),

    ("s53_moses_know_that_now", STYLE_SV05_CYANOTYPE, "moses2",
     f"A waist-up three-quarter shot, noticeably wider than a pure face "
     f"close-up so his whole gesture reads clearly: {MOSES}'s gaze "
     f"lowered inward rather than toward the viewer, one weathered hand "
     f"raised to rest against his own chest, visible together with his "
     f"robe, his staff, and the fall of his beard -- a small rueful, "
     f"honest half-smile of hard-won understanding, eyes steady -- the "
     f"whole figure submerged in the cool archival blue of a memory "
     f"looked back on from the far side of a long life, testimony rather "
     f"than present-tense drama. {FULLBLEED}"),
]


def main():
    for name, style, tag, scene in REDOS:
        out = s2.OUT / f"{name}.png"
        if out.exists():
            archived = s2.OUT / f"{name}.v2_style_superseded.png"
            if not archived.exists():
                out.rename(archived)
                print(f"[archive] {name} -> {archived.name}")
        refs = s2.resolve_refs(tag)
        prompt = style + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = s2.run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = s2.run(prompt, out, refs)
        if ok:
            try:
                s2.cost.record_hf(s2.EPISODE, "long", "stills_restyle_round2", s2.MODEL, note=f"[bronzeserpentlong-restyle2] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {s2.OUT}")


if __name__ == "__main__":
    main()
