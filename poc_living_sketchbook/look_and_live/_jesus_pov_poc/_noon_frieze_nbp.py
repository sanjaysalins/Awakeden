"""Jesus-POV style pivot, round 5 -- "Noon Frieze": the bright-daylight sibling of
Seraph Frieze (round 2/4's graphic silhouette language), tested across 5 DIFFERENT
scenes from the actual 13-scene plan -- including complex, multi-figure beats --
to check whether one consistent look and feel holds up across the whole story, not
just one hero shot. Subject blocks pulled from the real scene_plan.json for scenes
3, 5, 8, 13 (dying camp / bitten man / Nicodemus / the climax face); the pole scene
reuses the established round-2/3/4 composition for a same-style continuity check.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_noon_frieze_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_noon_frieze"
EPISODE = "look_and_live"

_BASE = ("Bold graphic animated-feature silhouette style, same lineage as a Hercules-inspired "
         "2D theatrical look: elongated, angular, dignified figures built from confident dark "
         "contour linework and flat graphic color shapes, minimal environmental detail, "
         "generous clean negative space, poster-clear composition — never cluttered or "
         "literally rendered, only the essential elements for this beat are shown. ")

_AVOID = (" AVOID: any text, lettering, numerals, captions, watermarks, or logos anywhere; "
          "no photorealism, no dense literal detail, no gore.")

STYLES = [
    ("a_pole", "Moses raises the pole",
     _BASE +
     "Warm, bright, sun-bleached daylight palette: a soft graduated pale cream-to-gold sky, "
     "minimal ground texture, hazy warm light — figures read as bold dark graphic silhouette "
     "shapes against the light rather than glowing shapes against black. Moses, an elongated "
     "angular dignified silhouette in long robes cut into sharp triangular folds, plants a tall "
     "rough wooden pole upright in the pale sand, both hands gripping the timber, body one "
     "strong diagonal gesture line. At the top of the pole, a bronze serpent effigy rendered as "
     "a warm bronze-gold graphic shape, catching the bright sun. A few small dark silhouette "
     "figures — three or four, some kneeling, some collapsed — scattered near his feet, reduced "
     "to simple graphic gesture shapes, not detailed individuals. Wide open negative space above "
     "and around, minimal ground detail, clean vertical 9:16 poster composition." + _AVOID),
    ("b_dying_camp", "The dying camp",
     _BASE +
     "Warm, bright, sun-bleached daylight palette: pale cream-to-gold sky, hazy bright light, "
     "minimal texture. A vast wilderness encampment rendered as a rhythmic frieze of repeated, "
     "simplified tent silhouette shapes receding toward the horizon — bold flat dark shapes, not "
     "individually detailed — with a scattering of small fallen or kneeling figure silhouettes "
     "among them, also reduced to simple graphic gesture shapes. Faint warm bronze glints "
     "half-hidden in the pale sand at the edges, hinting at more serpents. Even though the scene "
     "has many elements, every element stays a bold simplified graphic shape — no dense literal "
     "detail, no photographic clutter — so the frame still reads clean and poster-like despite "
     "the scale. Vertical 9:16 composition, high descending angle over the camp." + _AVOID),
    ("c_nicodemus", "Nicodemus by lamplight",
     _BASE +
     "A night interior, but NOT rendered as a near-black void — instead warm lamp-glow fills "
     "much of the frame: a low clay oil lamp between two seated figures throws soft warm "
     "amber-gold light across a generous portion of the scene, graduating into deep but not "
     "empty violet-shadow at the edges. Two elongated, angular graphic silhouette figures: an "
     "older learned man leaning forward across the lamp, face caught mid-question in the warm "
     "light; across from him, at the bottom edge of frame, another figure's resting sleeve and "
     "open hand. Minimal room detail — just enough shadow-shape to suggest a room, no literal "
     "clutter. Bold dark contour linework on both figures, flat graphic shapes, the lamp's warm "
     "glow doing most of the work instead of black negative space. Vertical 9:16 composition." + _AVOID),
    ("d_bitten_man", "The bitten man",
     _BASE +
     "Warm, bright, sun-bleached daylight palette: pale cream-to-gold background, hazy warm "
     "light, mostly empty negative space. A single bold dark graphic silhouette figure: a man "
     "risen on one elbow in the pale sand, two small dark marks visible on his bare forearm, his "
     "face turning upward as if hearing a call. Minimal ground shape beneath him, everything "
     "else left as open pale negative space. No crowd, no tents, no clutter — one figure, one "
     "gesture, one moment. Vertical 9:16 composition." + _AVOID),
    ("e_the_face", "The climax face — look at me",
     _BASE +
     "Warm, bright, sun-bleached daylight palette: soft pale cream-to-gold background, minimal "
     "negative space. A close portrait of a face rendered as a bold graphic dark silhouette "
     "shape, with only the eyes picked out in warm light, meeting the viewer directly in "
     "unbroken eye contact, calm and dignified. Behind the head, the barest suggestion of a "
     "plain wooden crossbeam as a simple dark graphic shape, nothing more. Extremely minimal, "
     "poster-clean, almost entirely negative space around the single close subject. Vertical "
     "9:16 composition, face in upper two-thirds." + _AVOID),
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

    print(f"[noon-frieze] {len(STYLES)} scenes -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "noon_frieze_consistency", units=1, note=f"jesus_pov noon-frieze scene: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[noon-frieze] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
