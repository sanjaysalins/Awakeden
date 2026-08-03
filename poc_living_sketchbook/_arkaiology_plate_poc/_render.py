"""POC: does ArkAIology's "NBP Plate Pack" recipe (sibling project,
`ArkAIology/poc_nbp_kling_style_test/`) translate to Bronze Serpent content?

That pack's discipline (verbatim-borrowed here, not reinvented):
  - ONE plate generates first with no reference and becomes `style_ref.png`;
    every other plate in the set attaches it as an NBP reference image so the
    whole set shares palette/line-weight, per `ARKAIOLOGY_REF_SUFFIX` in the
    source repo's `prompts.py`.
  - Flat even light, no rim light/flare/shallow DoF, exactly one antique-gold
    accent per plate, wide reserved-empty margins, zero baked text/letters
    (any labels are meant to be added afterward in Remotion -- not this POC's
    concern, we're only testing the STILL recipe).
  - Ivory/kraft-collage paper, graphite+ink over muted watercolour, light
    halftone grain -- the same family of materials Bronze Serpent LONG's own
    living-sketchbook stills already use, so this is a compatibility test,
    not a style import from nothing.

DOCTRINE NOTE (episode-specific, applied here even though the source pack
doesn't have this rule): this episode keeps gold reserved for Christ's glory
only -- the bronze serpent and the golden calf are both deliberately painted
UN-gilded elsewhere in Bronze Serpent LONG (see stills/s13, s37, s28, s55).
The source recipe's "one gold accent per plate" is kept (for recipe fidelity)
but the accent is placed as NEUTRAL DESIGN SCAFFOLDING -- a margin fleck, a
map line, a divider rule -- and NEVER painted onto the bronze serpent itself
or the cross, so this POC doesn't quietly violate the episode's own locked
rule (the comparison-split plate's gold divider follows the source pack's
OWN precedent exactly -- its gold rule was already a neutral centre divider,
not gilding on either figure).

3 plates, ~$1.50 total (NBP_USD_PER_IMG = $0.50 x 3):
  1. bronze_plate_artifact_hero -- the bronze serpent alone, isolated (no
     ref; becomes style_ref.png for the other two)
  2. bronze_plate_map_wilderness -- the wilderness route (ref = plate 1)
  3. bronze_plate_comparison_split -- bronze serpent | the cross, mirrored
     (ref = plate 1) -- same pairing idea as the LONG pilot's own
     s46_thesis_pair, restaged in this plate-pack register

  .venv\\Scripts\\python.exe poc_living_sketchbook/_arkaiology_plate_poc/_render.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

EPISODE = "POC_ArkaiologyPlatePack_BronzeSerpent"
NBP_MODEL = "gemini-3-pro-image-preview"
ASPECT = "16:9"
HERE = Path(__file__).resolve().parent
OUT = HERE / "plates"
OUT.mkdir(exist_ok=True)

REF_SUFFIX = ("Match the illustration style, palette, paper texture and line weight of "
              "the attached reference image (style_ref.png) exactly. Do not copy its "
              "subject or composition.")

COMMON_TAIL = (
    "\n\nLighting: flat, even and diffuse. No rim light, no god rays, no lens flare, no "
    "bokeh, no shallow depth of field, no dramatic chiaroscuro.\n\nMedium: illustration on "
    "paper. Not a photograph, not a 3D render, not flat vector art.\n\nStrictly forbidden: "
    "no text, no letters, no numbers, no glyphs, no script, no writing, no signage, no "
    "labels, no captions, no watermark and no signature anywhere in the image.\n\nFormat: "
    "16:9. Generous margins. Nothing important within 8% of any edge."
)

PLATES = [
    dict(
        id="bronze_plate_artifact_hero",
        ref=None,
        prompt=(
            "Editorial documentary illustration of a single bronze serpent figure, cast in "
            "dull weathered bronze gone dark green-brown with age (never gilded, never "
            "shining gold), coiled once around a plain unadorned wooden pole and mounted "
            "upright, isolated and alone. Graphite and ink linework over muted watercolour "
            "wash, on an aged cream and kraft paper-collage ground with torn edges and "
            "faint foxing. Light halftone grain. Palette: warm cream, kraft tan, graphite "
            "grey, dull bronze-green, ink black -- the bronze itself stays completely "
            "un-gilded and dark, with one antique gold accent placed only as a small "
            "gold-leaf fleck resting in the lower-right margin, never touching the serpent "
            "or the pole.\n\nComposition: the serpent and pole are centred and upright, "
            "occupying the middle 35% of the frame width and 75% of the height, isolated "
            "on a clean cream paper field. Wide empty margins on both the left and the "
            "right, deliberately reserved and containing nothing. Soft contact shadow "
            "beneath the pole's base only.\n\nMood: museum plate. Reverent, clinical, "
            "quiet -- an object of memory, not an object of worship."
            + COMMON_TAIL
        ),
    ),
    dict(
        id="bronze_plate_map_wilderness",
        ref="bronze_plate_artifact_hero",
        prompt=(
            f"{REF_SUFFIX}\n\nEditorial documentary illustration of a stylised top-down map "
            "of an arid wilderness region: rugged hill country to the west, a long "
            "north-south mountain range to the east, and a dry winding wadi threading "
            "between them. Hand-drawn cartographic feel: hatched relief for hills, dotted "
            "stipple for desert, no watercolour on the dry wadi bed itself. Graphite and ink "
            "linework on an aged cream and kraft paper-collage ground with torn edges and "
            "faint foxing. Light halftone grain. Palette: warm cream, kraft tan, graphite "
            "grey, ink black, and one antique gold accent -- the wadi's dry course traced as "
            "a single thin antique-gold line, the only gold in the frame.\n\nComposition: "
            "the mountain range runs vertically through the right third. The wadi crosses "
            "diagonally from lower-left to upper-right, its line the map's one visual "
            "throughline. The upper-left quadrant is kept sparse and open, deliberately "
            "reserved. No cities marked, no roads, no borders, no compass rose, no scale "
            "bar, no cartouche, no legend.\n\nMood: an old survey sheet of a hard country. "
            "Precise but hand-made."
            + COMMON_TAIL
        ),
    ),
    dict(
        id="bronze_plate_comparison_split",
        ref="bronze_plate_artifact_hero",
        prompt=(
            f"{REF_SUFFIX}\n\nEditorial documentary illustration of two objects mounted on "
            "poles, one on the left and one on the right, mirrored toward the centre: on the "
            "left, the dull weathered bronze serpent coiled on its plain wooden pole "
            "(un-gilded, dark green-brown); on the right, a plain wooden cross of the same "
            "height and proportion, bare and unadorned. Identical scale and vertical "
            "placement, differing only in what each pole carries. Graphite and ink linework "
            "over muted watercolour wash, on an aged cream and kraft paper-collage ground "
            "with torn edges and faint foxing. Light halftone grain. Palette: warm cream, "
            "kraft tan, graphite grey, dull bronze-green, ink black, and one antique gold "
            "accent -- a thin gold rule running vertically down the exact centre of the "
            "frame between the two poles, touching neither object.\n\nComposition: a hard "
            "vertical gutter of completely blank cream paper runs down the exact centre of "
            "the frame, 14% of the frame width, full height, containing nothing but the gold "
            "rule and deliberately reserved otherwise. The serpent-pole occupies the left "
            "43%, the cross the right 43%. Symmetrical balance.\n\nMood: a controlled "
            "comparison. The same shape, carrying two different things."
            + COMMON_TAIL
        ),
    ),
    dict(
        id="bronze_plate_timeline_backplate",
        ref="bronze_plate_artifact_hero",
        prompt=(
            f"{REF_SUFFIX}\n\nEditorial documentary illustration of a near-empty field of "
            "aged cream paper with a horizontal band of slightly darker kraft paper collaged "
            "across the vertical centre, torn along both of its long edges. Faint foxing "
            "spots scattered across the sheet. Light halftone grain. Palette: warm cream, "
            "kraft tan, graphite grey, and one antique gold accent -- a single small "
            "gold-leaf fleck resting on the band, left of centre.\n\nComposition: the kraft "
            "band occupies the central 22% of the frame height and runs the full width, "
            "bleeding off both the left and right edges. Clean empty cream paper above and "
            "below the band, both zones deliberately reserved and containing nothing. No "
            "marks, no tick marks, no scale, no lines, no other elements of any kind."
            "\n\nMood: a blank ledger before anything is written -- centuries waiting to be "
            "named."
            + COMMON_TAIL
        ),
    ),
    dict(
        id="bronze_plate_wilderness_dusk",
        ref="bronze_plate_artifact_hero",
        prompt=(
            f"{REF_SUFFIX}\n\nEditorial documentary illustration of a wide desert wilderness "
            "at dusk: low rolling dunes and scrub in the foreground and middle distance, a "
            "cluster of small tent silhouettes far off near the horizon (too distant for any "
            "individual figure or face to be visible), and a low warm horizon line. Graphite "
            "and ink linework over muted watercolour wash, on an aged cream and kraft "
            "paper-collage ground with torn edges and faint foxing. Light halftone grain. "
            "Palette: warm cream, kraft tan, graphite grey, ink black, and one antique gold "
            "accent -- a thin warm gold line along the horizon where the last light "
            "catches.\n\nComposition: the horizon sits on the lower third-line. The sky "
            "above occupies the upper two-thirds as flat unmarked cream paper, completely "
            "empty and deliberately reserved. The distant tents sit small and off-centre on "
            "the horizon line itself.\n\nMood: threshold -- a day ending, a story about to "
            "be told, or one just closed."
            + COMMON_TAIL
        ),
    ),
    dict(
        id="bronze_plate_big_stat_backplate",
        ref="bronze_plate_artifact_hero",
        prompt=(
            f"{REF_SUFFIX}\n\nEditorial documentary illustration consisting almost entirely "
            "of empty aged cream paper with torn collage edges and faint foxing. In the "
            "extreme lower-right corner only, a faint ghosted graphite illustration of a "
            "coiled serpent motif, drawn very lightly at no more than 20% opacity, bleeding "
            "partly off the corner. Light halftone grain across the sheet. Palette: warm "
            "cream, kraft tan, graphite grey, and one antique gold accent -- a single short "
            "horizontal gold rule spanning 15% of the frame width, positioned in the "
            "lower-left quadrant.\n\nComposition: the upper-left 75% of the frame is "
            "completely empty paper, deliberately reserved and containing absolutely "
            "nothing. No border, no frame, no other elements of any kind.\n\nMood: blank, "
            "deliberate, waiting for a single number to land."
            + COMMON_TAIL
        ),
    ),
]


class NBPClient:
    def __init__(self) -> None:
        if not config.GEMINI_API_KEY:
            raise SystemExit("GEMINI_API_KEY not set -- check PythonProject1/.env.")
        from google import genai
        self._client = genai.Client(api_key=config.GEMINI_API_KEY)
        self._uploaded: dict[str, str] = {}

    def _upload(self, path: Path) -> str:
        key = str(path)
        if key not in self._uploaded:
            self._uploaded[key] = self._client.files.upload(file=key).uri
        return self._uploaded[key]

    def generate(self, prompt: str, ref_png: Path | None = None) -> bytes:
        parts: list = []
        if ref_png is not None and ref_png.exists():
            parts.append({"fileData": {"mimeType": "image/png", "fileUri": self._upload(ref_png)}})
        parts.append({"text": prompt})
        resp = self._client.models.generate_content(
            model=NBP_MODEL,
            contents=[{"parts": parts}],
            config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ASPECT}},
        )
        candidates = getattr(resp, "candidates", None) or []
        if not candidates:
            raise RuntimeError("NBP returned no candidates")
        cand_parts = candidates[0].content.parts if candidates[0].content else []
        for p in cand_parts:
            if getattr(p, "inline_data", None) and p.inline_data.data:
                data = p.inline_data.data
                return base64_decode_if_str(data)
        finish = getattr(candidates[0], "finish_reason", "?")
        raise RuntimeError(f"NBP returned no image bytes (finish_reason={finish})")


def base64_decode_if_str(data):
    if isinstance(data, str):
        import base64
        return base64.b64decode(data)
    return data


def png_path(plate_id: str) -> Path:
    return OUT / f"{plate_id}.png"


def main():
    nbp = NBPClient()
    for plate in PLATES:
        out = png_path(plate["id"])
        if out.exists():
            print(f"[skip] {plate['id']} already have {out.name}")
            continue
        ref_png = png_path(plate["ref"]) if plate["ref"] else None
        if plate["ref"] and not ref_png.exists():
            print(f"[FAIL] {plate['id']} needs {plate['ref']} rendered first")
            continue
        img = nbp.generate(plate["prompt"], ref_png=ref_png)
        out.write_bytes(img)
        cost.record_nbp(EPISODE, "still", "poc_plate_pack", units=1, note=plate["id"])
        print(f"[OK] {plate['id']} -> {out}")
    print(f"cumulative POC spend: ~${cost.episode_total_usd(EPISODE):.2f}")


if __name__ == "__main__":
    main()
