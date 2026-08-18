"""Jesus-POV style pivot -- render Fable's 10 divergent visual-style concepts via NBP
(Nano Banana Pro, gemini-3-pro-image-preview), one still each, all against the SAME
test scene (Christ's face at the "Look at me" climax) so they compare fairly.

Sequential (not parallel) on purpose -- keeps this a light, one-call-at-a-time batch
rather than 10 concurrent processes. No reference-image attachment this round: each
style defines Jesus's rendering fresh from the fixed physical description baked into
its own prompt (see the gallery artifact for the full writeups).

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_style_bakeoff_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_style_bakeoff"
EPISODE = "look_and_live"

STYLES = [
    ("01_bronze_register", "Bronze Register",
     "Risograph screen-print poster illustration, vertical portrait composition. Upper-body portrait of a lean thirty-something Judean man with shoulder-length wavy dark brown hair parted in the middle, a full neat dark beard, straight nose, olive Mediterranean complexion weathered by outdoor life, warm dark brown eyes making direct, unbroken eye contact with the viewer — calm, steady, gently compassionate, dignified, unsentimental. Behind his shoulders a single bare rough-hewn wooden crossbeam spans the frame horizontally, printed flat and grainy. Exactly two ink colors on warm off-white paper: deep indigo-navy for all linework, beard, hair and shadow; burnt bronze-copper orange for skin midtones and the wood; every highlight is bare unprinted paper, brightest on his face and eyes. Coarse visible halftone dots, rough hand-cut stencil edges, flat ink with heavy paper grain, slight plate misregistration at the frame edges and crossbeam while the face stays in crisp perfect register. Gig-poster boldness, reverent tone. AVOID: any lettering, text, numerals, logos or symbols; no photorealism; no smooth airbrush gradients; no third ink color; no halo; no wounds, blood or crown of thorns; no soft-focus glow; no full crucifixion scene."),
    ("02_hewn_light", "Hewn Light",
     "Vertical dalle de verre stained-glass panel viewed straight-on, backlit from within against surrounding darkness: an upper-body portrait of Jesus making direct, unbroken eye contact with the viewer — a lean thirty-something Judean man, shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, warm dark brown eyes with a calm steady gaze, gentle compassionate expression, olive Mediterranean complexion weathered by outdoor life, straight nose, unlined forehead, one strong work-roughened hand visible near his chest. His face and skin are built from chipped amber and honey slab-glass facets, his robe from deep cobalt and sapphire slabs; behind his shoulders one bare horizontal wooden crossbeam in oxblood and bark-amber glass spans the frame — only the beam, nothing on it. Thick irregular charcoal-black hand-hewn matrix lines separate every piece of glass, brutalist and faceted; every facet glows as if low sun burns behind the panel, chipped edges catching tiny white-gold sparks; a ring of pale clear glass radiates softly behind his head. Illustrative, monumental, dignified, reverent. AVOID: no lettering, text, numerals, captions or symbols resembling writing; no photorealism; no full crucifixion, no figure on the beam, no wounds or gore; no thin ornate Art Nouveau leading; no tears or sentimental expression."),
    ("03_gouged_light", "Gouged Light",
     "White-line woodblock print, vertical 9:16 composition. An upper-body portrait of Jesus emerging from a solid black hand-printed ink field: a lean thirty-something Judean man of medium-tall build, shoulder-length wavy dark brown hair parted in the middle, a full neat dark beard, warm dark eyes meeting the viewer in direct, calm, unbroken eye contact, gentle compassionate dignified expression, olive Mediterranean complexion weathered by outdoor life, straight nose, unlined forehead, simple rough-woven robe. Every form is described only by white carved gouge lines cut out of the black — bold, confident chisel strokes following the contours of face, hair, and cloth like topographic ridges, warm cream paper showing through each cut. Behind and above him, a single bare rough-hewn wooden crossbeam spans the frame horizontally, its grain rendered in long parallel gouges — only the empty beam. A hand-rolled metallic bronze-copper ink pass rims the left side of his face and shoulder, slightly misregistered like edition-print slippage. Visible wood grain and ink-squash texture in the black field, deckle-edged handmade paper feel, stark high contrast, austere and human. AVOID: no lettering, text, numerals, captions, or watermarks anywhere; no crucified figure, nails, or blood; no halo; no smooth gradients or gray midtones; no photorealism; no extra colors beyond black ink, cream paper, and the single bronze accent; no sentimental soft-focus glow."),
    ("04_copper_seam", "The Copper Seam",
     "Layered cut-paper diorama portrait, vertical 9:16 composition. Upper body of a lean thirty-something Judean man constructed entirely from hand-torn and knife-cut paper layers: shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, olive Mediterranean complexion rendered in warm oat and umber paper tones, straight nose, unlined forehead, strong roughened hands suggested at frame edge, calm steady dark brown eyes cut as fine concentric paper rings with a tiny copper-foil catchlight, gazing directly and gently at the viewer, dignified and human. Every torn paper edge in his face, hair, and robe is finely gilded with burnished bronze-copper leaf, glinting like mended seams. Behind him one bare horizontal wooden crossbeam cut from wood-grain paper, set two layers deeper, softly shadowed — beam only. Background of deep indigo-to-umber layered paper. Warm tungsten theatre lighting from lower left, real physical cast shadows between layers, visible paper fiber and deckle texture, handcrafted museum-diorama depth, illustrative not photorealistic. AVOID: any lettering, text, numerals, captions or symbols; no photorealistic skin; no glossy plastic or 3D-render look; no cute or whimsical craft style; no visible glue, tape or fingerprints; no halo; no full crucifixion, nails or blood; no serpent; no doll-like or comedic face."),
    ("05_scarred_gold_apse", "Scarred-Gold Apse Fragment",
     "Ancient Byzantine wall mosaic fragment, sixth-century apse style, vertical portrait composition. Upper-body frontal portrait of a lean thirty-something Judean man: shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, warm dark brown eyes making direct unbroken eye contact with the viewer, calm steady compassionate expression, olive Mediterranean skin weathered by outdoor life, straight nose, strong roughened workman's hands. Behind his shoulders, a single bare wooden crossbeam rendered in umber and bronze tesserae — only the horizontal beam, nothing more. Plain unlettered soot-dimmed gold halo. The entire image built from thousands of small hand-cut glass and stone tesserae set at irregular angles in visible pinkish mortar; gold-leaf ground darkened by centuries of candle smoke, glinting unevenly under raking side light. Outer edges excavation-damaged: tesserae fallen away revealing rough mortar and faint red sinopia underdrawing — face and eyes completely intact and undamaged. Muted palette of oxidized gold, deep umber, olive, dried-blood red, bone white. Illustrative, flattened iconographic perspective, monumental and dignified. AVOID: any lettering, text, numerals, inscriptions, or symbols in the halo or background; no photorealism; no cracks or damage crossing the face or eyes; no glossy pristine finish; no soft sentimental glow; no full crucifixion scene; no blood; no tears."),
    ("06_lifted_standard", "The Lifted Standard",
     "Hand-pulled linocut poster portrait in three inks on warm unbleached cream paper: carbon black, deep oxblood red, and bare cream paper serving as all light. Upper-body portrait of a lean thirty-something Judean man, shoulder-length wavy dark brown hair parted in the middle carved as bold black shapes, full neat dark beard, olive weathered complexion built from angular cut planes of cream and black, straight nose, unlined forehead. His warm dark brown eyes meet the viewer directly with a calm, steady, compassionate gaze — the eyes rendered with finer, gentler carved linework than anything else, perfectly registered while the surrounding colour layers sit slightly off-register, ink-boss texture and gouge marks visible throughout. Behind him a single massive horizontal black bar: a bare wooden crossbeam with gouged woodgrain, spanning the full frame width at shoulder height. One strong oxblood-red diagonal band rises behind his shoulder to the top edge. Monumental, frontal, dignified, human. Vertical 9:16 composition, flat graphic depth, paper tooth visible. AVOID: any lettering, text, numerals, captions or emblems; no political symbols; no halo; no photorealism; no full crucifixion, wounds or blood; no soft glow or sentimentality; no grunge distress filters; no grotesque facial distortion."),
    ("07_brazen_vigil", "The Brazen Vigil",
     "Vertical cinematic film still, deep night, near-total darkness. Upper-body portrait of a lean thirty-something Judean man in a simple undyed rough-woven robe: shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, olive Mediterranean complexion weathered by outdoor life, straight nose, unlined forehead, warm dark brown eyes looking directly into the camera with a calm, steady, gently compassionate gaze — dignified, unsentimental. Behind and slightly above his shoulders, a single bare rough-hewn horizontal wooden crossbeam, its top edge rim-lit, receding into blackness. Lighting: one hard warm bronze-amber key from low frame-left, like firelight from an unseen camp fire below the frame; deep crushed true-black shadows swallow everything outside the beam; soft halation bloom on the brightest skin highlights; heavy fine 65mm film grain; desaturated near-monochrome bronze-and-black color grade, shot like an anamorphic movie frame, shallow depth of field. AVOID: no lettering, text, numerals, captions, or watermarks; no halo or divine glow; no wounds, blood, nails, or crown of thorns; no full cross, only the single beam; no serpent; no second light source, no blue or teal fill; no soft airbrushed devotional finish; no tears or theatrical expression."),
    ("08_unbroken_signal", "The Unbroken Signal",
     "Upper-body portrait of a lean thirty-something Judean man, medium-tall build, shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, warm dark brown eyes making direct steady eye contact with the viewer, gentle dignified compassionate expression, olive Mediterranean skin weathered by outdoor work, straight nose, unlined forehead; a single bare rough wooden crossbeam runs horizontally behind his shoulders. Painted in a flat matte hand-illustrated devotional style — muted antique gold ground, deep umber and bone-white palette, soft frontal lighting like candlelit iconography, visible gouache brush texture. The outer edges of the frame are heavily corrupted by digital signal damage: horizontal scan-line displacement slices, red-cyan chromatic aberration tearing, coarse pixel-block dropout mosaics, static noise — and this corruption decays smoothly toward the center, dissolving completely into a pristine untouched oval of calm around his head, face, and chest, as if the glitch cannot cross into his stillness. His face, eyes, and skin are perfectly clean and painterly, zero distortion. Vertical 9:16 composition, face in upper third. AVOID: any lettering, text, numerals, captions, watermarks or symbols; no glitch artifacts on his face, eyes, hair or hands; no photorealism; no halo ring; no full crucifixion scene, no nails, no blood, no crown of thorns; no neon cyberpunk colors; not grotesque, not horror."),
    ("09_kept_cloth", "The Kept Cloth",
     "A hand-embroidered votive textile portrait, photographed flat and filling the frame: upper body of a lean thirty-something Judean man, shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, warm dark brown eyes gazing directly and calmly at the viewer, gentle dignified expression, olive weathered complexion, straight nose, strong workman's hands. His face and skin rendered in dense directional satin-stitch and split-stitch embroidery thread that follows the contours of the face like brushstrokes; hair and beard in layered stem-stitch. Behind his shoulders, a horizontal wooden crossbeam suggested by an area of deliberately unwoven cloth — raw exposed warp threads and frayed weft — the fabric left open where the beam crosses. Coarse handwoven linen ground with visible weave texture, slight pucker around dense stitching. Folk-tapestry palette: madder red, indigo, walnut brown, undyed flax; fine couched metallic gold thread only in the eye catchlights and one thin halo line of running stitch. Soft raking light from upper left catching thread sheen. Vertical 9:16 composition, head upper third. AVOID: no lettering, text, numerals, or captions anywhere; no printed or painted look, no smooth digital gradients; no photorealistic human skin; no cross-stitch pixel grid; no sampler borders or decorative frames; no crown of thorns, no wounds, no blood; not cartoonish, not cute."),
    ("10_bronze_beneath", "The Bronze Beneath",
     "Vertical 9:16 scratchboard engraving portrait, fine-line intaglio style. Upper-body portrait of a lean thirty-something Judean man facing forward, direct unbroken eye contact with the viewer: shoulder-length wavy dark brown hair parted in the middle, full neat dark beard, warm dark brown eyes with a calm steady gaze, gentle compassionate expression, olive Mediterranean complexion weathered by outdoor life, straight nose, unlined forehead, strong roughened hands loosely at rest. Behind his shoulders, a single bare wooden crossbeam rendered in sparse horizontal scoring — only the beam, nothing else. The entire image is built from thousands of fine tapered engraved strokes scratched out of a solid black ground; the revealed lines glow warm metallic bronze-gold, not white, brightest where cuts are deepest; contour-following parallel lines wrap the forms of the face like banknote engraving; most of the frame remains solid uncut black. Single raking light implied purely by stroke density. AVOID: no lettering, text, numerals, captions, signatures or watermarks; no white paper tone or grey wash; no colors other than black and bronze-gold; no oil-paint, watercolor or pencil texture; no photorealism; no halo, crown of thorns, blood, wounds or full crucifixion scene; no sentimental softness."),
]


def render_one(client, genai_types, slug, prompt):
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

    print(f"[bakeoff] {len(STYLES)} styles -> {OUT_DIR}")
    ok, failed = [], []
    for slug, name, prompt in STYLES:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, genai_types, slug, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "style_bakeoff", units=1, note=f"jesus_pov style plate: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)  # gentle pacing between calls, not a parallel burst

    print(f"\n[bakeoff] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
