"""Jesus-POV style pivot, round 7 -- fix the consistency gap the user flagged:
round 6's cross renders didn't actually match round 5's "Moses raises the pole" /
"Nicodemus by lamplight" technique (those had gradient-shaded silhouettes with real
linework detail; round 6 drifted flatter/more icon-like on several plates). Text
prompts alone kept drifting across separate agent calls -- so this round attaches
the ACTUAL round-5 reference image (a_pole.png) to NBP as an image input, so the
model matches its real rendering technique instead of re-describing it from scratch.

Two variants: (a) same warm cream/gold/bronze family as the reference itself --
the strictest consistency test -- and (b) the dusk-indigo alternative, to see if
technique-consistency survives a color shift for this different beat's mood.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_cross_matched_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_cross_matched"
EPISODE = "look_and_live"

REF_IMAGE = Path(__file__).resolve().parent / "_noon_frieze" / "a_pole.png"

_MATCH_INSTRUCTION = (
    "Match the EXACT rendering technique of the attached reference image: the same "
    "elongated angular Hercules-lineage silhouette figures, the same weight and "
    "confident quality of dark contour ink linework, the same level of gradient "
    "shading and dimensional form on every silhouette (not a flat solid color fill "
    "-- the reference has real light-to-shadow gradient modeling on the figure, "
    "keep that same fidelity), the same warm minimal negative-space composition "
    "discipline. This must look like it was made by the same artist as the "
    "reference, frame to frame. "
)

_AVOID = (" AVOID: any text, lettering, numerals, captions, watermarks, or logos anywhere; "
          "no photorealism, no flat solid-fill silhouette with zero shading, no gore; "
          "the figure must be full-length, head to feet, never cropped to a headshot.")

STYLES = [
    ("a_cream_gold", "Cross, matched technique — cream & gold",
     _MATCH_INSTRUCTION +
     "Vertical 9:16 composition. A vast, warm sun-bleached cream-to-gold gradient sky "
     "and ground, in the same palette family as the reference image. Centered, a tall "
     "simple wooden cross bearing the full-length figure of Jesus, entire body clearly "
     "visible head to feet, arms outstretched along the crossbeam, head inclined gently, "
     "expression serene and dignified, direct calm presence. The cross and the rim of "
     "Christ's silhouette carry a warm reserved bronze-gold glow, the single most "
     "saturated color in the frame, echoing the same bronze used on the serpent effigy "
     "earlier in the story. Generous open negative space around the figure. Monumental, "
     "reverent, still." + _AVOID),
    ("b_dusk_indigo", "Cross, matched technique — dusk indigo",
     _MATCH_INSTRUCTION +
     "Vertical 9:16 composition. A cool dusk sky in a smooth gradient from deep "
     "indigo-violet at the top down to a thin band of fading plum-rose light at a low "
     "horizon -- the same rendering fidelity as the reference image, just a cooler "
     "evening palette instead of the reference's own warm daylight one. Centered, a "
     "tall simple wooden cross bearing the full-length figure of Jesus, entire body "
     "clearly visible head to feet, arms outstretched along the crossbeam, head "
     "inclined gently, serene and dignified. The cross and the rim of Christ's "
     "silhouette carry a warm reserved bronze-gold glow, the only warm color anywhere "
     "in the frame, like the last ember of daylight against the cool sky. Generous open "
     "negative space above the figure. Monumental, reverent, still." + _AVOID),
]


def render_one(client, genai_types, ref_bytes, slug, prompt):
    uploaded = client.files.upload(
        file=str(REF_IMAGE),
        config=genai_types.UploadFileConfig(display_name=REF_IMAGE.name, mime_type="image/png"),
    )
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [
            {"fileData": {"mimeType": "image/png", "fileUri": uploaded.uri}},
            {"text": prompt},
        ]}],
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

    if not REF_IMAGE.exists():
        sys.exit(f"reference image not found: {REF_IMAGE}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    print(f"[cross-matched] {len(STYLES)} variants -> {OUT_DIR} (ref: {REF_IMAGE.name})")
    ok, failed = [], []
    for slug, name, prompt in STYLES:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, genai_types, None, slug, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "cross_matched_technique", units=1, note=f"jesus_pov cross ref-matched: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[cross-matched] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
