"""Contemporary register test, round 2 -- 4 more techniques (rotoscope, video-game
cinematic, living motion-comic, fixed Emberline retry), same beat, period-locked,
classical painting media still banned.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_contemporary_register/_render_round2_nbp.py
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
    ("5_traced_hour", "The Traced Hour — rotoscope prestige",
     "Rotoscoped prestige animation still, a single frame hand-traced over live actor performance footage. Vertical 9:16 composition, extreme close-up: Peter, a weathered Galilean fisherman in his fifties, face and upper shoulders in three-quarter view, lit from below-left by unseen firelight against deep night darkness. The exact instant of being seen after his third denial — eyes just caught by the Lord's turned gaze, lips barely parted, brow collapsing inward, wet lower lids catching light, a real specific ache, restrained, not theatrical. Photographically true anatomy and facial asymmetry traced in a slightly trembling dark-umber contour line that breaks and re-catches along the jaw and eyelids; flat muted naturalistic color fields painted inside the lines with small deliberate gaps and overshoots at the edges; a soft warm firelight bloom on the lower-left planes only, cool near-black field behind him. He wears a rough-spun undyed wool tunic, a coarse mantle pulled over one shoulder, a rope belt glimpsed at frame bottom, gray hair escaping a simple cloth head covering. AVOID: oil painting, watercolor, classical fine art, canvas texture, photorealism, smooth digital rendering, modern or ambiguous clothing, any text or lettering."),
    ("6_engine_realism", "Ember-Lit Engine Realism — video game cinematic",
     "A cinematic real-time-engine cutscene still, 9:16 vertical. Extreme close-up of Peter, a weathered first-century Judean fisherman in his fifties, face and upper shoulders, three-quarter view turned slightly left, at night in a courtyard. He wears a rough-spun undyed wool tunic with a coarse woven mantle pulled over one shoulder, visible individual fibers, a simple rope belt hinted at frame bottom — strictly ancient Judean dress, nothing modern. He has just been seen: the exact instant of recognition after his third denial — eyes wide and glassing with the first sting of tears, brow knotted, lips barely parted, jaw slack with shame. Not exaggerated; devastatingly restrained. Single firelight source from below-left: strong orange key with subsurface scattering glowing through his nose and ear cartilage, drifting ember particles, visible smoke haze and a soft volumetric light cone, cold blue-black ambient shadow on the far cheek. Stylized game-cinematic finish: smooth idealized skin planes, enlarged eye catchlights, teal-and-ember duotone grade. AVOID: oil painting, watercolor, classical fine art, canvas texture, photorealism, photographic noise, modern clothing, lettering, text, watermarks."),
    ("7_ember_and_slate", "Ember & Slate — living motion-comic",
     "Premium motion-comic still, 9:16 vertical, no text anywhere in frame. Extreme close-up of Peter the fisherman, face and upper shoulders, three-quarter view, night, the exact instant after his third denial as the Lord turns and looks at him. Expression restrained and real: lips barely parted, wet lower eyelids with small off-center catchlights, left brow a fraction higher, nasolabial crease deeper on one cheek only — shame and recognition at half intensity, never exaggerated. A weathered Galilean man in his fifties, once-broken nose, patchy gray-streaked beard, sun-creased skin. Strict first-century Judean dress: rough-spun undyed wool tunic, heavy wool mantle pulled over one shoulder, a glimpse of rope belt, loose head covering slipped back off his hair. Rendering: crisp closed-contour digital ink, thick tapering silhouette stroke, fine interior lines, no hatching; flat graphic color planes, one soft gradient per plane; warm ember-amber firelight from below-left; a single cold slate-cyan rim light from upper right edging brow, cheekbone and mantle. Dark smoky courtyard behind, simplified to graphic shapes. AVOID: oil painting, watercolor, canvas texture, classical fine art, photorealism, modern clothing, lettering, text, watermarks."),
    ("8_emberline_fixed", "Emberline — fixed framing",
     "Vertical 9:16 portrait-format image, completely upright and level — the camera is not tilted, not rotated; the figure stands normally, head at top, shoulders below. Graphic-novel prestige animation still, painterly rendering held inside bold ink contour lines whose weight follows darkness, not importance, the line breaking open wherever light strikes. Close-up: Peter's face and upper shoulders, head upright and centered, three-quarter view, filling the frame naturally. The exact instant of Luke 22:61 — the Lord has turned and looked upon him after the third denial: eyes just caught mid-glance, brow collapsing, lips parted on a breath he cannot finish, grief arriving before the tears. Night courtyard, firelight from below-left in bruised rose-copper — never default orange — against petrol green-black shadow, a pale celadon rim tracing his far cheek and mantle edge. First-century Judean dress only: rough-spun tunic, coarse woolen mantle, rope belt. Cinematic color grading and mood. AVOID: oil painting, watercolor, classical fine art, canvas texture, photorealism, modern clothing, any lettering or text, and any sideways, rotated, tilted, or Dutch-angle composition — frame orientation must be normal and upright."),
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

    print(f"[contemporary-register-r2] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "contemporary_register_test_r2", units=1, note=f"contemporary register r2: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[contemporary-register-r2] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
