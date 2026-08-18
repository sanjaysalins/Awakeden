"""Jesus-POV style pivot, round 6 -- five distinct color-scheme + format treatments
of the same fixed scene (Jesus on the cross, full-length, Noon Frieze graphic
silhouette style), so the user can compare real alternatives instead of trusting
one theoretical color-schema write-up. Full-length figure is now a locked rule
after round 5's Plate E (a tight headshot) was rejected.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_cross_colors_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_cross_colors"
EPISODE = "look_and_live"

STYLES = [
    ("1_bone_beacon", "Bone & Beacon",
     "Vertical 9:16 illustration in a bold flat graphic animated-feature style: elongated, angular, dignified figures, confident dark contour linework, flat graphic shapes, no painterly rendering, minimal environmental detail, generous clean negative space. The entire frame is a vast, empty, sun-bleached warm cream-bone field (#F5EAD3), flat and unbroken. A single thin dark ink line marks the ground low in the frame. Rising from it, centered, a tall cross in saturated bronze-gold (#DF8F2E) commands the upper half of the frame — the only saturated color anywhere. On it, the full-length figure of Christ, head to feet completely visible, arms outstretched, body a deep warm near-black angular silhouette (#2B1D14) with elegant simplified contours. A noon sun directly overhead traces a hot near-white-gold rim light along the top edges of his head, shoulders and outstretched arms, blazing brightest at the crown. His head is upright, facing the viewer, with two tiny calm points of warm gold light at his eyes. One long soft dark shadow pools at the foot of the cross. Monumental, serene, reverent, like a temple frieze seen from below. AVOID: any text, lettering, numerals, captions or symbols; blood, wounds, gore; extra figures, crowds, birds, clouds, landscape detail; gradients, painterly texture; cropping the figure at any edge."),
    ("2_ember_indigo", "Ember Against Indigo",
     "A bold graphic animated-feature illustration in the style of 1990s theatrical animation with Gerald Scarfe-influenced character design: elongated, angular, dignified silhouette figures, confident dark contour linework, flat graphic color shapes, no painterly rendering, no realistic texture. Vertical 9:16 composition. A vast dusk sky fills the frame in a smooth flat-graphic gradient: deep indigo-violet at the top, sliding down through muted dusk violet to a single thin horizontal band of fading plum-rose light at a very low horizon; the darkest tones are blue-black indigo, never pure black. Ground is a simple flat dark-violet silhouette plane. Centered, rising from the low horizon, a tall simple wooden cross bearing a serene, dignified full-length figure of Christ — entire body visible head to feet, elongated angular stylized anatomy, head bowed gently, arms extended along the crossbeam. The figure and cross are edged in a hot molten bronze-gold rim light, the only warm color in the frame, glowing like the last ember of daylight against the cool field. Generous empty indigo negative space in the upper third. Reverent, still, monumental. AVOID: any text, lettering, numerals, captions, or symbols; blood, wounds, gore; photorealism, painterly brushwork, 3D rendering; extra figures, birds, clouds, clutter; cropped limbs or feet out of frame."),
    ("3_bone_shadow", "Bone and Shadow",
     "A bold graphic animated-feature illustration in a stylized theatrical silhouette style: elongated, angular, dignified figures with confident dark contour linework and flat graphic shapes, never painterly rendering. Vertical 9:16 portrait composition. Strict near-monochrome palette in a single warm sepia-umber hue family, varying only in lightness: a vast, almost empty field of pale bone-cream fills the upper two-thirds of the frame like blank warm parchment; a faint slightly darker parchment haze sits at the horizon line; a thin flat band of mid-value raw umber ground runs low across the bottom of the frame. Rising from that ground band, centered, a simple wooden cross bearing the crucified figure of Jesus, rendered as one deep espresso-umber silhouette — the darkest shape in the image. The figure is full-length and complete: head gently bowed, outstretched arms, torso, legs, and feet all clearly visible against the pale field. Serene, still, dignified, monumental, like a frieze. Minimal environmental detail, flat simplified shapes, generous clean negative space surrounding the cross on every side. AVOID: any text, lettering, numerals, captions, or watermarks; any second hue or accent color; gold, bronze, or glowing light effects; halos, rays, or rim lighting; gore, wounds, or blood; crowds, scenery, clouds, or clutter; photorealism or painterly texture."),
    ("4_against_deep", "Against the Deep",
     "Bold graphic animated-feature illustration in a stylized 1990s theatrical animated-musical design language: elongated, angular, dignified figures, confident dark contour linework, flat graphic shapes, minimal environmental detail, generous clean negative space. Vertical 9:16 poster composition. The entire frame is one flat field of deep petrol teal, hex #0E4A54, completely empty — no clouds, no horizon, no landscape, no texture. Positioned high in the upper two-thirds of the frame, viewed from a low upward-looking worshipper's angle: Jesus on a simple wooden cross, the full figure clearly visible from head to feet, arms outstretched along the crossbeam, head inclined gently, expression serene and dignified. The figure and the cross are rendered entirely in one luminous molten bronze-amber, hex #E8A13C, as a flat graphic shape with dark teal interior contour lines defining the loincloth drapery, the elegant angular limbs, and the feet resting together at the base of the upright. A thin warm rim of bronze glow separates the figure cleanly from the teal field. The lower third of the frame stays empty teal negative space, pulling the eye upward. Still, monumental, reverent. AVOID: any text, lettering, numerals, captions, or signage anywhere in the frame; blood, wounds, or gore; photorealism or painterly texture; background scenery, crowds, or clouds; cropping any part of the figure; literal light rays or starbursts."),
    ("5_potters_field", "Potter's Field",
     "Bold graphic animated-feature illustration in the style of a Gerald Scarfe-designed animated epic: elongated, angular, dignified figures, confident dark contour linework, flat graphic color shapes, no painterly rendering, minimal environmental detail, generous clean negative space. Vertical 9:16 composition. A full-length figure of Jesus on a simple wooden cross, entire body visible from head to feet, head bowed gently in peace, arms outstretched along the crossbeam, rendered as a muted dusty-rose and warm clay silhouette with soft ochre underlighting on the torso and limbs. The cross is a darker burnt-umber shape rising from a wide, empty band of flat terracotta ground filling the lower third of the frame. Sky is a single flat field of pale dusty rose, deepening to soft sienna at the upper corners. Frontal view from slightly below eye level, mourner's height. The entire palette is one warm earthen family — rose, terracotta, umber, ochre — with the figure carrying the warmest, most skin-like tone in the frame; no metallic gold, no glow effects, no light rays. Serene, intimate, reverent, vulnerable. AVOID: any text, lettering, numerals, captions, or signage anywhere; blood, wounds, gore; crowds or background figures; gold or metallic tones; halos or radiating light beams; photorealism; painterly brushwork; cropping the head or feet."),
]


def render_one(client, slug, prompt):
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

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    print(f"[cross-colors] {len(STYLES)} schemes -> {OUT_DIR}")
    ok, failed = [], []
    for slug, name, prompt in STYLES:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, slug, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "cross_color_bakeoff", units=1, note=f"jesus_pov cross-color scheme: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[cross-colors] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
