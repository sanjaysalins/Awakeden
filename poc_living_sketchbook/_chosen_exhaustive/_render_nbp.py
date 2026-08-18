"""Chosen-register exhaustive bake-off -- 10 distinct non-photoreal rendering
techniques, all tested on the exact same beat (Luke 22:61, "the Lord turned, and
looked upon Peter"), all period-locked to first-century Judean dress.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_chosen_exhaustive/_render_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
EPISODE = "fresh_takes_poc"

ITEMS = [
    ("01_oil_chiaroscuro", "Ember Tenebroso — oil chiaroscuro",
     "A vertical 9:16 oil painting in dramatic single-source chiaroscuro, confident visible alla-prima brushwork, thick impasto in the light, thin transparent umber glazes in the shadow. Extreme close-up of Peter, a weathered Galilean fisherman around fifty, head and upper shoulders, three-quarter view, night courtyard, lit only by a low fire from below-left. The precise instant he is seen and recognized after his third denial: eyes wet and glassing, brow just beginning to break, lips barely parted — dawning shame and grief, restrained and human, not theatrical. He wears strict first-century Judean dress: a rough-spun undyed wool tunic, a coarse woven mantle pulled over one shoulder, no other garments visible. Warm ochre, burnt sienna, and one touch of vermilion model the firelit side; the shadow side melts into deep translucent brown-black with lost edges; a single warm catchlight in each eye; background near-black with a faint ember glow low-left. AVOID: modern clothing, buttons, zippers, collars, photorealism, smooth airbrush rendering, digital sheen, exaggerated cartoon expression, any text, lettering, or watermark."),
    ("02_charcoal_study", "Ember Study — charcoal figure study",
     "Raw charcoal and graphite life drawing on warm grey toned paper, 9:16 vertical. Extreme close-up of Peter the fisherman, a first-century Judean man in his fifties, face and upper shoulders, three-quarter view. Night; a fire out of frame below-left throws light up across his jaw, cheekbone, and brow. The instant he realizes he has been seen after denying his Lord a third time: eyes wet and welling, lips just parted, brow beginning to break — grief and recognition, quiet and specific, not exaggerated. Rough-spun wool tunic, a heavy mantle bunched at one shoulder, coarse grey-streaked beard, weathered skin, hair disheveled under a slipped-back head cloth. Smudged compressed-charcoal shadows, visible cross-hatching, searching construction lines left in, highlights lifted with an eraser. One transparent amber watercolor wash glazed only over the firelit lower-left planes of the face and the tunic edge, a fleck of amber in the wet eyes; everything else pure graphite grey-black. AVOID: modern clothing, photorealism, photographic rendering, digital smoothness, any lettering, text, or watermark, full color, cartoonish exaggeration."),
    ("03_gouache_wash", "Ember Wash — loose gouache portrait",
     "A loose gouache portrait painting on cream cold-press watercolor paper, visible individual brushstrokes never blended smooth, wet-on-wet bleeds where warm colors meet, slivers of bare paper left as highlights. Close-up of Peter, a weathered Galilean fisherman in his fifties, face and upper shoulders, three-quarter view, at night beside a courtyard fire. He wears a rough-spun undyed wool tunic, a heavy earth-brown mantle pulled over one shoulder, first-century Judean dress. Firelight strikes from below-left in warm burnt sienna and cadmium orange blooms; the right side of his face falls into dry-brushed Payne's grey and indigo shadow. His expression is the exact quiet instant of being seen and recognized — eyes wet and stricken, lips just parted, grief arriving, nothing exaggerated. Outer edges of mantle and head dissolve unfinished into raw paper. Palette strictly limited to fire oranges and night blue-greys. AVOID: modern clothing, photorealism, smooth digital rendering, airbrush blending, text, lettering, watermarks, signatures. 9:16 vertical."),
    ("04_ink_wash", "Emberwash — ink-wash grisaille",
     "Vertical 9:16 ink-wash painting on textured cold-press paper, a monochrome sumi grisaille built from exactly five values — reserved paper-white, pale mist wash, mid grey wash, deep charcoal wash, charged near-black. Close-up of Peter, face and upper shoulders, three-quarter view: a weathered Galilean fisherman, grey-threaded curled beard, rough-spun wool tunic and heavy mantle gathered at the shoulders, a glimpse of rope belt — strict first-century Judean dress. Night courtyard dissolves into soft dark washes behind him. Firelight from below-left, source out of frame: one warm amber glaze breaks the monochrome only on his lit planes — underside of jaw, left cheekbone, the wet lower lids of his eyes. The exact instant he is seen and recognized after his third denial: brows knotting, lips parting, eyes glassing — real, restrained, aching, not exaggerated. Crisp tonal edges at brow and eyelids, wet-in-wet softness elsewhere, minimal dry-brush line in the beard. AVOID: modern clothing, buttons, zippers, collars, photorealism, smooth digital rendering, cartoon exaggeration, any lettering, text, or watermark."),
    ("05_visdev_concept", "Ember Study — vis-dev concept paint",
     "Animated-feature visual development concept painting, 9:16 vertical. Close-up of Peter the apostle — face and upper shoulders, three-quarter view — at the exact instant he is seen and recognized after his third denial: eyes just lifting toward someone off-frame, wet-rimmed, brows knotting, lips parting as breath fails; grief arriving, restrained and real, never theatrical. A weathered Galilean fisherman, gray-threaded beard, wind-burnt skin, wearing a rough-spun undyed wool tunic with a coarse woven mantle pulled over one shoulder — strict first-century Judean dress. Night courtyard; charcoal-fire light from below-left carves warm ember orange up his jaw and brow, all else falling into cold slate-blue dark. Loose confident brushwork: big blocked value shapes, hard chisel-edged strokes, edges deliberately lost into shadow, raw gray ground showing through at the fringes; only the eyes and near cheek fully resolved — a working painter's fast color key, not a finished frame. AVOID: modern clothing, buttons, seams, zippers, photorealism, camera realism, smooth airbrush blending, flat vector silhouette, any text, lettering, watermark, signature."),
    ("06_egg_tempera", "The Sienese Ember — egg tempera",
     "Egg tempera panel painting, matte dry surface, fine visible cross-hatched brushstrokes building dimensional form over a green-earth verdaccio underlayer that ghosts through the shadows. Vertical close-up: Peter, a weathered Galilean fisherman in his fifties, face and upper shoulders in three-quarter view, the exact instant he realizes Jesus has turned and looked at him after his third denial. Expression specific and restrained — eyes wet and widening, brows knotted upward, lips just parting, shame and grief surfacing, never theatrical. Firelit from below-left at night: warm ochre and cinnabar glow on cheek and beard, cool terre-verte darkness above. Strict first-century Judean dress: rough-spun undyed wool tunic, heavy mantle drawn over one shoulder, hint of rope belt. Sun-creased asymmetrical skin, grey-streaked unkempt beard, real individual anatomy. Earthy mineral palette — ochre, sienna, terre verte, bone black, lead-white lights — with subtle gesso tooth and fine craquelure. AVOID: modern clothing, photorealism, gold halo, Byzantine flatness, airbrushed digital smoothness, any lettering or text."),
    ("07_pastel_chalk", "Firelit Chalk — soft pastel portraiture",
     "Soft chalk pastel portrait on toothy warm-gray paper, visible chalk grain and finger-smudged blended transitions, velvety layered shadows, handmade tactile texture, no digital smoothness. Close-up of Peter, a weathered middle-aged first-century Judean fisherman, face and upper shoulders, three-quarter view, at night beside a courtyard fire. Warm firelight strikes him from below-left in layered ochre, terracotta, and pale rose strokes; the rest falls into soft charcoal-dark paper shadow. His expression is the exact quiet instant of being seen and recognized — eyes wet and stricken, lips just parting, brow collapsing inward with grief and shame, restrained and real, not exaggerated. He wears a rough-spun undyed wool tunic and a heavy earth-toned mantle pulled at the shoulder, coarse woven texture rendered in broken chalk strokes. Vertical 9:16 composition, intimate framing. AVOID: photorealism, digital painting smoothness, modern clothing, buttons, zippers, collars, any text, lettering, watermarks, exaggerated cartoon expression."),
    ("08_engraved_glaze", "Gilded Burin — engraving + color glaze",
     "Antique copperplate engraving with a thin translucent warm watercolor glaze over it, 9:16 vertical. Close-up of Peter, a weathered Judean fisherman in his fifties, face and upper shoulders, three-quarter view, at night, lit from below-left by unseen firelight. The exact instant of being seen: eyes just lifted and locked, brows drawn faintly upward, lips barely parted, the beginning of grief — restrained, real, not exaggerated. Dense fine cross-hatched linework builds his form like an old book illustration: tight parallel hatching along cheek and brow, open cross-hatch in mid-shadow, near-solid stippled dark under jaw and eye sockets. A thin burnt-sienna-to-amber glaze warms only the firelit side of his face, eye rims, and near shoulder; the night side and background remain pure uncolored engraving on cream paper. Bare-paper highlights; wet glint in the eye. First-century Judean dress only: rough-spun wool tunic, coarse mantle over one shoulder, visible woven texture. AVOID: modern clothing, buttons, collars, zippers, photorealism, smooth digital painting, lettering, text, watermarks, signatures."),
    ("09_cinematic_matte", "The Keyframe Register — cinematic matte character paint",
     "Finished animated-feature key frame, muted cinematic gouache matte-painting style, painterly but fully resolved — theatrical animation drama polish, not concept art, not photoreal. Vertical 9:16 close-up: Peter, a weathered Galilean fisherman in his fifties, face and upper shoulders, three-quarter view, at night in a courtyard. He wears a rough-spun undyed wool tunic with a coarse woven mantle pulled over one shoulder, first-century Judean dress. Firelight from below-left is the only light: warm amber on his lit cheek, brow and beard, the rest falling into desaturated slate-blue night shadow. His expression is the exact instant of being seen and recognized after a denial — eyes just met, lips barely parted, grief arriving; specific and restrained, not theatrical. Visible soft gouache brushwork modeling the face planes, controlled edges, near-monochrome palette with one warm source, atmospheric depth behind him, subtle halation, painterly matte-painted background. AVOID: modern clothing, zippers, buttons, photorealism, photographic skin, 3D render look, sketch lines, exaggerated cartoon expression, any text or lettering."),
    ("10_graphite_oil", "Firelit Pentimento — graphite/oil hybrid",
     "A graphite-and-oil hybrid illustration on toothy cream paper, 9:16 vertical. Close-up of Peter, a weathered Galilean fisherman around fifty, face and upper shoulders in three-quarter view, the exact instant he realizes the Lord has turned and is looking at him after his third denial: lips just parting, brow buckling, eyes glassing with the first sting of tears — a real, aching, restrained expression, not theatrical. Night courtyard, charcoal-fire glow from below-left. The firelit planes of his face and the top fold of his mantle carry thin warm oil glazes of raw sienna and ochre; the shadowed side of his face, hair, beard, and far shoulder remain bare graphite with visible cross-hatching and construction lines showing through; his eyes and tear-line rendered in sharp graphite even within the lit area. He wears a rough-spun undyed wool tunic and coarse woolen mantle, strict first-century Judean dress. AVOID: modern clothing, buttons, zippers, photorealism, smooth airbrushed digital rendering, exaggerated cartoon expression, any lettering, text, or watermarks."),
]


def render_one(client, genai_types, prompt):
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [{"text": prompt}]}],
        config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
    )
    candidates = getattr(resp, "candidates", None) or []
    if not candidates:
        raise RuntimeError("NBP returned no candidates")
    parts = candidates[0].content.parts if candidates[0].content else []
    for p in parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            return p.inline_data.data
    raise RuntimeError(f"NBP returned no image bytes (finish_reason={getattr(candidates[0], 'finish_reason', '?')})")


def main() -> None:
    from google import genai
    from google.genai import types as genai_types

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    print(f"[chosen-exhaustive] {len(ITEMS)} stills -> {OUT_DIR}")
    ok, failed = [], []
    for slug, name, prompt in ITEMS:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, genai_types, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "chosen_exhaustive", units=1, note=f"chosen-exhaustive: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[chosen-exhaustive] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
