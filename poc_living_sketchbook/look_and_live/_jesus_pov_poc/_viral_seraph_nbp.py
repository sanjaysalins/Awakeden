"""Jesus-POV style pivot, round 4 -- take Seraph Frieze (round 2, plate B) and strip it
down: near-black background, only a few graphic elements, high-contrast poster read --
the "viral edit" composition the user asked for, instead of the full sprawling-camp
establishing shot. Same fixed scene subject (Moses raising the bronze serpent), no crowd.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_viral_seraph_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_viral_seraph"
EPISODE = "look_and_live"

STYLES = [
    ("h_viral_seraph_witnesses", "Seraph Frieze — Viral Cut (with witnesses)",
     "Vertical 9:16 poster-style key art, rendered as a bold graphic animated-feature still, NOT an establishing shot. Near-black background — almost entirely empty negative space, only a faint dark violet gradient hinting at a horizon line low in frame, no tents, no crowd, no camp detail. One dominant graphic element: Moses, an elongated, angular, dignified silhouette in long robes cut into sharp triangular folds, strains with visible effort to plant a tall rough wooden pole upright, both hands gripping the timber, his body one strong diagonal gesture line, rendered almost entirely as bold dark silhouette with only a thin warm rim-light edge separating him from the black. At the top of the pole, a coiled bronze serpent effigy glows molten gold — the single brightest, most saturated point in the entire frame, its glow the only real light source, casting warm light down onto Moses's rim and the ground directly beneath. At the very bottom edge of frame, two or three small kneeling silhouette figures, arms lifted toward the pole, minimal and graphic, just enough to read as witnesses without becoming a crowd scene. Confident bold dark contour linework, flat graphic shapes, poster-clean composition, huge negative space, dramatic scale contrast between the tiny witnesses and the towering pole. AVOID: any text, lettering, numerals, captions, watermarks, or logos; no tents, no wide desert vista, no detailed environment; no photorealism; no gore; no crossbar or cross shape on the pole — a plain vertical stake only."),
    ("i_viral_seraph_stripped", "Seraph Frieze — Viral Cut (stripped)",
     "Vertical 9:16 poster-style key art, rendered as a bold graphic animated-feature still, NOT an establishing shot. Pure near-black background, almost entirely empty negative space, no ground detail, no horizon, no tents, no crowd, no camp — just enough dark gradient to feel like a stage, not a void. One single dominant graphic element fills the frame: Moses, an elongated, angular, dignified silhouette in long robes cut into sharp triangular folds, strains with visible effort to plant a tall rough wooden pole upright, both hands gripping the timber, body one strong diagonal gesture line, rendered almost entirely as bold dark silhouette with only a thin warm rim-light edge separating him from the black. At the top of the pole, a coiled bronze serpent effigy glows molten gold — the single brightest, most saturated point in the entire frame, its glow the only real light source in the whole image, throwing a tight pool of warm light straight down. Nothing else in frame. Confident bold dark contour linework, flat graphic shapes, extreme poster-clean minimalism, maximum negative space, the towering pole and glowing serpent doing all the storytelling alone. AVOID: any text, lettering, numerals, captions, watermarks, or logos; any crowd, any tents, any ground texture, any environment detail; no photorealism; no gore; no crossbar or cross shape on the pole — a plain vertical stake only."),
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

    print(f"[viral-seraph] {len(STYLES)} styles -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "viral_seraph_bakeoff", units=1, note=f"jesus_pov viral-seraph plate: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[viral-seraph] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
