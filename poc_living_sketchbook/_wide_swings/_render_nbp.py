"""Wide-swing register test -- 4 genuinely divergent traditions (Prince of Egypt,
dramatic anime, Ethiopian/Coptic manuscript icon, Persian miniature), same beat,
period-locked.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_wide_swings/_render_nbp.py
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
    ("1_ember_gouache", "Ember Gouache — Prince of Egypt",
     "Hand-painted 1990s theatrical animation still, gouache matte-painting quality, vertical 9:16 frame. Extreme close-up, face and upper shoulders, three-quarter view: Peter the fisherman, a weathered first-century Judean man, at the exact instant of being seen — the Lord has just turned and looked upon him after his third denial. His expression is real and specific, not exaggerated: lips barely parting, inner brows knotting upward, eyes glassing with the first shock of recognition and grief. Night courtyard; a charcoal fire below frame-left throws warm ochre-vermilion light up across his jaw and cheekbone; all else falls into deep ultramarine-violet shadow, never pure black. Strict first-century Judean dress: rough-spun undyed wool tunic, heavy earth-striped mantle pulled over one shoulder, twisted rope belt hinted at the chest, coarse woven head covering slipped back onto his shoulders. Semi-realistic elongated proportions, dimensional painted core-shadow modeling on the face, confident warm burnt-umber contour lines that thin where firelight strikes, visible dry-brush tooth in the shadows. AVOID: photorealism, photography, 3D render, flat cel shading, cartoon exaggeration, modern or ambiguous clothing, buttons, zippers, any lettering, text, watermarks."),
    ("2_ember_gekiga", "Ember Gekiga — dramatic anime",
     "Serious dramatic anime film still, mature gekiga register of prestige adult animation, vertical cinematic composition. Wordless night close-up of Peter, a weathered Galilean fisherman in his fifties: face and upper shoulders, three-quarter view, in the high priest's courtyard. Strict first-century Judean dress: rough-spun undyed wool tunic, coarse woven mantle pulled over one shoulder, rope belt hinted at the lower frame edge. Firelight from a brazier below-left throws warm amber up across his jaw, cheekbone, and knotted brow; all else falls into deep desaturated indigo night with a thin warm rim on his shoulder. The exact instant of being seen and recognized: eyes lifted and locked off-frame, hooded lids heavy, inner brows drawn upward, lips barely parted, one tear welling but not falling — grief held in restraint, not exaggerated. Adult proportions: small irises, creased eyelids, nasolabial folds, gray-flecked beard, slight facial asymmetry. Character in sophisticated four-tone cel shading with softly blended shadow terminators; background a painterly gouache courtyard in atmospheric darkness, smoke drifting. AVOID: photorealism, live-action look, big-eyed cute anime faces, modern or ambiguous clothing, buttons, zippers, any text, lettering, or watermark."),
    ("3_gondar_emberline", "Gondar Emberline — Ethiopian icon",
     "Hand-painted Ethiopian Orthodox manuscript illumination in the warm narrative Gondarine style, opaque mineral pigment on parchment, vertical 9:16 composition. Extreme close-up: the apostle Peter, head and upper shoulders only, three-quarter view turned slightly left, at the exact instant he is seen and recognized after his denial — night courtyard, lit only by fire glow from below-left. Peter is a weathered first-century Judean fisherman: rough-spun undyed wool tunic, a coarse brown-striped mantle pulled over one shoulder, a simple cloth head covering slipping back from gray-streaked hair, full gray-flecked beard. His enormous almond eyes carry everything: pupils dragged hard toward an unseen figure off-frame, whites catching one flat firelight glint, lower lids pressed upward, brows knotted at the center, lips barely parted — shame and grief arriving together, restrained and human, not exaggerated. Bold confident dark-umber outlines of varying weight; flat color fields of ochre, burnt sienna, madder red, parchment cream, deep indigo night; the firelight painted as one flat warm-orange field across the left of his face; visible parchment grain. AVOID: photorealism, 3D rendering, soft painterly blending, modern or ambiguous clothing, any text or lettering, gold-leaf background, halo, stiff frontal Byzantine symmetry."),
    ("4_herat_ember", "The Herat Ember — Persian miniature",
     "A classical Persian miniature painting in the fifteenth-century Herat manuscript style, 9:16 vertical. Close-up of Peter, a weathered first-century Judean fisherman, face and upper shoulders in three-quarter view, at night beside a courtyard fire. Capture the exact instant of being seen and recognized after his denial: eyes glassing with unshed tears, brow just broken, lips barely parted in silent grief — specific, restrained, aching, with fine individualized features. His face is the sparsest, calmest zone on the page. Skin is a flat ivory-ochre field with no Western shading; all light is drawn, not blended: brush-drawn vermilion and saffron-gold flame-tongues from below-left rim his jaw and cheek as crisp gilded lines. Ultra-fine single-hair linework everywhere else: every grey beard hair a separate stroke, rough-spun wool tunic and striped mantle rendered as dense micro-woven textile pattern, rope belt at the shoulder line, coarse head covering slipped back. Flattened perspective, jewel-tone lapis-lazuli night ground, tiny saffron sparks. AVOID: photorealism, 3D render, soft gradients, modern clothing, buttons, zippers, any text, lettering, script panels, watermark."),
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

    print(f"[wide-swings] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "wide_swings_test", units=1, note=f"wide swing: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[wide-swings] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
