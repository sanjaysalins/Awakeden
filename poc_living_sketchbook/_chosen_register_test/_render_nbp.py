"""Chosen-register visual test -- can the style carry "the Lord turned, and looked
upon Peter" (Luke 22:61), the single wordless beat the whole scene hinges on?
Two directions, each on the same close-up + the same wide staging shot, so facial
expressiveness and minimalist staging can be judged side by side.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_chosen_register_test/_render_nbp.py
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

_PAINTERLY_AVOID = (" AVOID: any text, lettering, numerals, watermarks; flat "
                     "silhouette rendering with no facial detail; a crowded or busy "
                     "composition; photorealism; gore.")
_GRAPHIC_AVOID = (" AVOID: any text, lettering, numerals, watermarks; a fully flat "
                   "featureless silhouette face; a crowded or busy composition; "
                   "photorealism; gore.")

ITEMS = [
    ("a_painterly_close", "Painterly Chosen — the look (close-up)",
     "A restrained, cinematic painterly illustration, semi-realistic proportioned "
     "figures with genuine facial detail and expression -- warm, dimensional "
     "brushwork on skin and features, not a flat silhouette. Vertical 9:16 close-up "
     "composition: Peter's face, three-quarter view, firelit from below-left, eyes "
     "wide and caught mid-breath, the exact instant of being seen and recognized -- "
     "a real, subtle, aching expression, not exaggerated. Deep soft-focus darkness "
     "fills most of the frame around him; only his face and the edge of his shoulder "
     "catch the warm firelight. Minimal, uncluttered, nothing else in the frame "
     "competing for attention. Muted warm palette: firelight amber, deep umber "
     "shadow, desaturated night blue at the edges." + _PAINTERLY_AVOID),
    ("b_painterly_wide", "Painterly Chosen — the courtyard (wide)",
     "A restrained, cinematic painterly illustration, semi-realistic proportioned "
     "figures with genuine facial detail, warm dimensional brushwork. Vertical 9:16 "
     "wide shot: a small night courtyard, one low fire as the only light source, "
     "figures seated around it in loose silhouette against the flames, one man "
     "(Peter) seated at the edge of the firelight, hood low, face partly lit, tense "
     "posture. Generous dark negative space fills the upper two-thirds of the frame "
     "-- night sky, stone walls barely visible. Minimal staging, only the fire and "
     "the seated figures, nothing decorative. Muted warm palette: firelight amber "
     "and umber against deep desaturated night blue." + _PAINTERLY_AVOID),
    ("c_graphic_close", "Graphic Chosen — the look (close-up)",
     "A bold, restrained editorial illustration style -- confident clean linework "
     "defining real facial features and expression (eyes, brows, the set of the "
     "mouth), flat graphic color planes for shadow and skin rather than photoreal "
     "rendering, but the face stays genuinely expressive, not a blank silhouette. "
     "Vertical 9:16 close-up composition: Peter's face, three-quarter view, firelit "
     "from below-left, caught mid-breath at the instant of being recognized, a real "
     "subtle aching expression. Deep flat dark negative space fills most of the "
     "frame; only his face and shoulder catch warm graphic firelight. Minimal, "
     "uncluttered. Muted warm palette: firelight amber, deep umber, desaturated "
     "night blue." + _GRAPHIC_AVOID),
    ("d_graphic_wide", "Graphic Chosen — the courtyard (wide)",
     "A bold, restrained editorial illustration style -- confident clean linework, "
     "flat graphic color planes, expressive faces kept legible even at a distance. "
     "Vertical 9:16 wide shot: a small night courtyard, one low fire as the only "
     "light source, figures seated around it in graphic silhouette-and-line against "
     "the flames, one man (Peter) at the edge of the firelight, hood low, tense "
     "posture, face partly lit and legible. Generous dark flat negative space fills "
     "the upper two-thirds of the frame. Minimal staging, only the fire and the "
     "seated figures. Muted warm palette: firelight amber and umber against deep "
     "desaturated night blue." + _GRAPHIC_AVOID),
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

    print(f"[chosen-register] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "chosen_register_test", units=1, note=f"chosen-register test: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[chosen-register] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
