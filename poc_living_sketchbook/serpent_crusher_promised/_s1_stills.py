"""The Serpent-Crusher Promised (Seed of the Woman short #4, Romans 16:20)
-- step 1: 9 spreads, 9:16. No Adam/Eve this piece (narration never names
them) -- Christ reused from repo cast anchor; the serpent chains as a
DESIGN reference from this cluster's own approved art (short #1's
`first_gospel_in_the_curse/stills/s03_turns_to_serpent.png` and short #3's
`heel_vs_head/stills/s05_heel_and_head_insert.png` crushed-head design, plus
`heel_vs_head/stills/s06_own_blow_straining.png` and
`first_gospel_in_the_curse/stills/s07_gold_thread_in_curse.png` for their own
respective device shots).

kling_omni_image is the proven cheap default for this cluster (0.5cr);
seedream_v4_5 for the hero/consistency/landing shots (s05, s06, s09).

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/serpent_crusher_promised/_s1_stills.py
Run specific shots only:
  .venv\\Scripts\\python.exe poc_living_sketchbook/serpent_crusher_promised/_s1_stills.py s01_recap_curse s09_landing_stand_with_christ
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "kling_omni_image"
EPISODE = "LS_SerpentCrusherPromised"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

FGC_STILLS = ROOT / "poc_living_sketchbook" / "first_gospel_in_the_curse" / "stills"
HVH_STILLS = ROOT / "poc_living_sketchbook" / "heel_vs_head" / "stills"
SERPENT_TURNS_REF = FGC_STILLS / "s03_turns_to_serpent.png"
GOLD_THREAD_REF = FGC_STILLS / "s07_gold_thread_in_curse.png"
HEEL_HEAD_REF = HVH_STILLS / "s05_heel_and_head_insert.png"
STRAINING_REF = HVH_STILLS / "s06_own_blow_straining.png"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"
ARCH_REF = OUT / "s02_unfinished_arch.png"

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong. Eyes: warm deep brown, level and calm. Garment: simple "
    "undyed homespun ankle-length tunic with a woven cord sash -- THE SAME "
    "man as the reference image, identical face, beard, hair, and clothing."
)

# Proven winning language from heel_vs_head's own s05_heel_and_head_insert
# (6 rounds to land there -- reused VERBATIM per the reuse-first principle,
# rather than re-deriving a weaker paraphrase that drifts back to an alive,
# open-mouthed, or gory serpent). Split into a scale-agnostic DAMAGE
# description plus a separate CLOSE framing prefix -- an earlier version
# baked "close and large" into the shared text and it kept overriding
# every "small, distant" composition instruction downstream.
CRUSHED_HEAD_DAMAGE = (
    "a serpent's head only, no long body or coil attached, small in scale "
    "relative to the rest of the scene. This is unmistakably a SNAKE'S "
    "head, its whole outer shape long, low, and flat like a snake's -- an "
    "elongated pointed snout, a flat triangular skull silhouette, NOT a "
    "rounded human cranium, NOT a human forehead or jaw, NOT any kind of "
    "bare white bone skull anywhere in the image. The head stays covered "
    "almost entirely in dark grey-blue scale pattern with faint red "
    "accents, scales visible everywhere including right up to the edge "
    "of the damage. The head is clearly, visibly DAMAGED and lifeless: "
    "one side is dented and caved in, a dark fracture line cracking "
    "across the scales there, but the surface underneath the crack is "
    "dark and shadowed, not bright white bone. Both eyes are fully "
    "CLOSED -- drawn as two simple closed dark slits or lines, no round "
    "eyeball, no pupil, no white highlight or shine anywhere in the eye "
    "area, completely without life. The mouth is fully closed, gently "
    "shut, resting still -- NOT open, NOT gaping, NOT baring fangs, NOT "
    "showing the tongue, NOT in a striking or threatening pose of any "
    "kind, completely calm and peaceful in death, like a creature simply "
    "fallen still. The whole head reads unmistakably as ONE single "
    "broken, dead SNAKE'S head, not sleeping, not resting, not alert, "
    "and absolutely not aggressive or attacking."
)
CRUSHED_HEAD_DESC = "a single serpent's head, close and large. " + CRUSHED_HEAD_DAMAGE


# (name, refs, model, scene)
SHOTS = [
    ("s01_recap_curse", [], "seedream_v4_5",
     "A tight vertical stack of three faces in warm lamplight, portrait "
     "framing, filling the frame top to bottom -- exactly THREE people, "
     "no more, all dressed in the ANCIENT WORLD, first-century Judean "
     "or Roman clothing -- NOT modern dress, NOT a modern shirt collar "
     "or button placket on anyone, NOT a modern haircut on anyone. TOP: "
     "a white-bearded elder in three-quarter view, mid-word, one hand "
     "raised in a storyteller's gesture, wearing a plain undyed "
     "homespun robe with a rounded, collarless neckline and a simple "
     "head-wrap or loose mantle over his shoulders. CENTER: an adult "
     "listener with a short dark beard, calm knowing expression, "
     "someone who has heard this told many times before, wearing the "
     "same style of plain collarless homespun robe, hair worn longer "
     "and simply combed, no modern styling. BOTTOM, closest to a single "
     "small clay oil lamp: a child with simple unstyled hair, leaning "
     "in close, lips slightly parted, listening intently, wearing the "
     "same plain collarless homespun tunic. Loose graphite linework on "
     "the faces, muted warm watercolor wash in the lamp glow, cool "
     "ink-blue pooling in the shadows behind them, one small ink-red "
     "accent on the lamp flame. The wall behind them dissolves into "
     "blank cream paper and faint engineering-grid hairlines. All three "
     "figures are still, frozen mid-listening, no motion."),

    ("s02_unfinished_arch", [], MODEL,
     "A Roman triumphal arch, half-built, portrait framing, low angle "
     "looking up. Both stone piers stand complete in confident graphite "
     "linework with grey-cream watercolor wash, the curved courses of "
     "stone rising from each side -- but the crown of the arch is still "
     "open air, an empty gap between the two unfinished tops. Directly "
     "above the gap, a single large wedge-shaped stone block hangs "
     "suspended in taut rope slings from a wooden crane arm that crops "
     "in at the very top of the frame. Simple lashed wooden scaffolding "
     "leans against one pier; on a scaffold plank rest a plain mallet "
     "and a hanging plumb line, straight and still. Faint engineering-"
     "grid hairlines cross the sky as part of the page's own texture, "
     "not as labels or numbers. Soft pale sky wash behind the stone. "
     "Gold-leaf strip along the top edge, catching the suspended stone. "
     "Torn collage paper edge at the bottom of the frame."),

    ("s03_armor_set_aside", [], MODEL,
     "A QUIET still-life composition, portrait framing: a simple "
     "soldier's breastplate, helmet, and sword laid down flat on bare "
     "ground, set aside and untouched, no figure wearing or standing "
     "near them -- the armor sits empty and unclaimed. A soft unseen "
     "radiant column of warm calm light falls across the empty armor "
     "from above -- presence without a visible figure, peace rather "
     "than combat. Cool shadow around the edges of the frame, the light "
     "itself the only warmth."),

    ("s04_pauls_letter", [], MODEL,
     "A CLOSE, intimate composition, portrait framing: a pair of hands "
     "holding a reed pen over an unfinished letter on rough parchment, "
     "an ordinary plain writing table, a small oil lamp nearby -- the "
     "person's face and upper body are turned away or entirely out of "
     "frame, only the hands, the pen, and the parchment are visible. "
     "The parchment shows a few lines of unreadable script trailing off "
     "mid-page. Plain, unadorned Roman-era setting, warm lamplight, no "
     "ornamentation."),

    ("s05_feet_on_crushed_head", [HEEL_HEAD_REF], "seedream_v4_5",
     "HERO, CLOSE portrait framing, drawn in the SAME graphite-and-ink "
     "hand-illustrated sketch style as the rest of this piece -- NOT a "
     "photograph, loose confident linework throughout, not photoreal "
     "skin. An extreme low-angle crop at mid-shin height, as if looking "
     "straight down at the ground: a pair of ordinary bare human feet, "
     "weight resting naturally, standing on bare garden soil -- the legs "
     "continue naturally upward past the top edge of the frame, an "
     "ordinary standing pose, not a disembodied limb. Directly in front "
     "of and touching the same ground as the feet, small and close by, "
     + CRUSHED_HEAD_DESC + " A soft unseen radiant warm light surrounds "
     "the feet from above -- grace-light, calm and gentle, not a light "
     "of conquest or effort."),

    ("s06_empty_cross_shadow", [], "seedream_v4_5",
     "WIDE, portrait framing: a plain wooden cross standing empty "
     "against a quiet sky, no figure on it, the wood a uniform warm "
     "honey-tan color throughout, clean and bare -- its long shadow "
     "falling across bare ground below, well clear of the cross itself. "
     "Resting flat on the ground at the far end of the shadow, small and "
     "modest in scale -- no bigger than a hand's width in the frame, "
     "nowhere near as tall as the cross, not overlapping or touching the "
     "wooden beam at all -- " + CRUSHED_HEAD_DAMAGE + " The whole scene "
     "reads as already-finished, already-settled -- nothing in motion, "
     "nothing still being decided. The palette stays entirely in warm "
     "honey-tan wood tones, soft blue-grey shadow, and pale garden dust."),

    ("s07_night_watchman", [], MODEL,
     "A lone night watchman at a city wall, portrait framing, the "
     "darkest spread in the set. He leans hard into the stone parapet, "
     "both hands gripping the coping tightly, shoulders bunched, face "
     "drawn and hollow-eyed but dignified, staring outward into deep "
     "ink-blue watercolor wash. Plain rough cloak, no armor, no sword "
     "-- this is exhaustion, not a soldier. At his elbow, one small "
     "clay lamp with a low guttering flame, the single ink-red accent "
     "in the frame, and beside it two other small lamps lying dry and "
     "unlit. Scratched into the stone next to his hand, a small cluster "
     "of plain identical short scratch-marks in a simple tally pattern "
     "-- NOT numerals, NOT letters, NOT any readable text, just plain "
     "scratched lines. Below the wall, the sleeping city suggested only "
     "in loose graphite shapes, no detail. Night wash bleeding to a "
     "torn paper edge at the top of the frame; gold-leaf strip thin "
     "along the right edge. The whole figure held still, frozen in "
     "tension, no motion."),

    ("s08_gold_thread_bridge", [GOLD_THREAD_REF], "seedream_v4_5",
     "A single unmistakable diagonal RAY OF BRIGHT GOLD LIGHT, like a "
     "shaft of sunlight breaking through a gap, cutting across the frame "
     "from the upper corner all the way down to the lower portion of the "
     "image (matching the reference gold-thread design) -- painted in "
     "vivid saturated gold and yellow, clearly the brightest, most "
     "eye-catching shape in the whole composition, easily as wide and "
     "long as the serpent it touches. WIDE garden-clearing scene, "
     "portrait framing, plain pale cream and muted-grey garden ground -- "
     "in the lower portion of the frame, small in scale, occupying no "
     "more than a quarter of the frame's width, exactly where the gold "
     "ray lands, " + CRUSHED_HEAD_DAMAGE + " Everything except the gold "
     "ray stays pale, muted, and faded, as if this were an old "
     "illustration the light is now touching."),

    ("s09_landing_christ_in_arch", [JESUS_REF, ARCH_REF], "seedream_v4_5",
     f"{JESUS} His sleeves are long, covering His arms down to the "
     "wrist -- NOT sleeveless, NOT bare-armed. LANDING, sacred "
     "stillness, portrait framing: the SAME Roman stone archway from "
     "the reference image, now completely finished -- the wedge-shaped "
     "keystone fully seated at the crown of the arch, every rope and "
     "the crane gone, one plain mallet lying retired and still at the "
     "base of a pier, no scaffolding anywhere. Standing inside the open "
     "archway, framed by the stone, Christ faces directly toward the "
     "viewer, calm and reverent, seen from mid-shin upward -- the "
     "ground below dissolves into loose pale wash, unfeatured, no "
     "other object on it. His near hand is extended low and open "
     "toward the viewer, palm up, with one small closed, healed mark "
     "on the palm, faint muted ink-red only, flat against the skin, no "
     "wound texture, no blood. Warm radiant gold watercolor light "
     "floods through and around the archway behind Him, and the "
     "style's gold-leaf strip runs up along the inner curve of the "
     "stone arch itself instead of the frame's outer edge."),
]


def run(prompt, out, refs, model=MODEL):
    cmd = [HF, "generate", "create", model, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--wait"]
    cmd += ["--quality", "high"] if model == "seedream_v4_5" else ["--resolution", "2k"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    only = set(sys.argv[1:]) or None
    for name, refs, model, scene in SHOTS:
        if only and name not in only:
            continue
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        if refs and any(not Path(r).exists() for r in refs):
            print(f"[HOLD] {name}: missing ref {[str(r) for r in refs if not Path(r).exists()]}")
            continue
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (model={model}, refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs, model=model)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs, model=model)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", model, note=f"[serpent-crusher-promised] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
