"""Real scene coverage test -- the graphic/bold/clean style the user flagged as
genuinely fresh (from the original Chosen Register round), now tested across
actual shot distances from the John 4 well-scene structure: wide, two-shot,
earned close-up, wide again. Proving the STYLE survives changing distance, not
just proving one portrait.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_well_scene_coverage/_render_nbp.py
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

_STYLE = (
    "A bold, restrained editorial illustration style — confident clean linework, "
    "flat graphic color planes for shadow and skin rather than photoreal "
    "rendering, expressive faces and postures kept legible even at a distance, "
    "minimal uncluttered staging. Strict first-century Judean/Samaritan dress: "
    "rough-spun tunics, mantles, rope belts, sandals, simple head coverings — no "
    "modern or ambiguous clothing. "
)
_AVOID = (" AVOID: any text, lettering, numerals, watermarks; photorealism; a "
          "crowded or busy composition; modern clothing.")

ITEMS = [
    ("1_wide_establishing", "Scene 1 — wide (the request)",
     _STYLE +
     "Vertical 9:16 wide establishing shot, midday, harsh open desert light. A "
     "stone well stands alone in open country, a worn dirt path leading to it. "
     "Jesus, full-length, sits on the well's low stone edge, travel-dust on his "
     "robe, unhurried. A woman with a clay waterpot balanced on her shoulder "
     "approaches on the path from the far distance, small in frame, caught "
     "mid-step, hesitating at the sight of him. Generous open sky and bare "
     "ground, large negative space, the two figures kept far apart in the frame "
     "on purpose — strangers, not yet close." + _AVOID),
    ("2_twoshot_water", "Scene 2 — medium two-shot (living water)",
     _STYLE +
     "Vertical 9:16 medium two-shot across the low stone well, midday light. "
     "Jesus, seated on the well's edge, gestures faintly as he speaks, calm and "
     "direct. Across from him, the woman now stands close, her clay waterpot set "
     "down on the ground beside her — the first sign she has chosen to stay. "
     "Both figures fully visible head to feet, the well between them in the "
     "middle of the frame, open desert and sky filling the space around them. "
     "Both faces turned toward each other, engaged, legible expressions even at "
     "this medium distance — his calm, hers skeptical and curious." + _AVOID),
    ("3_earned_closeup", "Scene 3 — the earned close-up (five husbands)",
     _STYLE +
     "Vertical 9:16 close-up, the one true close-up of the sequence. The woman's "
     "face and upper shoulders fill the frame, midday light flat and unforgiving, "
     "her expression caught guarded and startled at once — eyes widened slightly, "
     "lips parted, a flush of exposure at being known. Minimal background, soft "
     "blurred suggestion of the well and open desert behind her. Expressive but "
     "restrained, not exaggerated — the moment nothing is hidden anymore." + _AVOID),
    ("4_wide_she_runs", "Scene 6 — wide, moving (she runs to the city)",
     _STYLE +
     "Vertical 9:16 wide shot, midday. The woman, full-length, strides quickly "
     "away from the stone well toward a small distant hillside town visible on "
     "the horizon, her clay waterpot left behind on the ground at the well, "
     "abandoned and small in the foreground. Her body language is urgent, "
     "purposeful, arms swinging with motion. Jesus remains a small distant "
     "figure still seated at the well behind her. Wide open desert and sky, "
     "generous negative space, strong sense of distance covered." + _AVOID),
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

    print(f"[well-scene-coverage] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "well_scene_coverage", units=1, note=f"well scene coverage: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[well-scene-coverage] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
