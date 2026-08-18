"""Jesus-POV style pivot, round 2 -- render Fable's 4 "Prince of Egypt / Hercules"
animated-feature style concepts via NBP, all against the SAME real Bible scene
(Moses raising the bronze serpent over the dying wilderness camp, Numbers 21:8 --
no Jesus in frame, per the user's explicit redirect away from portrait-only tests).

Sequential on purpose, same as the first round's _style_bakeoff_nbp.py.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_epic_bakeoff_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_epic_bakeoff"
EPISODE = "look_and_live"

STYLES = [
    ("a_ember_horizon", "Ember Horizon",
     "Vertical 9:16 hand-painted animated-feature production still, in the tradition of late-1990s theatrical animated biblical epics. Wide establishing shot at desert dusk. Foreground: Moses, a weathered semi-realistic proportioned man in dusty ochre and deep-red robes, both hands gripping a tall rough wooden pole, shoulders straining as he plants it upright into the sand; at the pole's top a coiled bronze serpent effigy catches the last low sun in a single hot amber glint. Middle distance: afflicted Israelites scattered across the camp — some collapsed in the dust, one rising on an elbow, several turning their faces upward toward the pole — painted as simplified gesture figures. Far distance: thousands of tents dissolving into warm dust haze toward the horizon. Enormous sky filling the upper frame: ember-orange horizon graduating through rose and violet to deep indigo, long backlit cloud bands. Lighting: one low sun, hot rim-light on figures, mile-long cool blue-violet shadows raking the sand, strong atmospheric perspective. Medium: gouache matte-painting backgrounds with visible dry-brush texture, clean-lined cel-style characters with painterly planar shading, cinematic epic scale. AVOID: any text, lettering, numerals, captions, watermarks or signatures; photorealism; 3D CGI render look; cartoon exaggeration; modern objects; extra floating figures in the sky."),
    ("b_seraph_frieze", "Seraph Frieze",
     "Vertical 9:16 cinematic wide establishing shot at dusk, rendered as a late-1990s theatrical 2D animated-feature production still: hand-painted matte-painting background with bold cel-shaded characters on top. Foreground: Moses, an elongated angular dignified silhouette in long robes cut into sharp triangular folds, strains with visible effort to plant a tall rough wooden pole upright in the sand, both hands gripping the timber, his body one strong diagonal gesture line. At the top of the pole a coiled bronze serpent effigy catches the last low sun — the single brightest molten-gold highlight in the frame. Middle distance: a vast wilderness encampment, tents receding to the horizon through warm dust haze; afflicted Israelites read as a rhythmic frieze of repeated graphic silhouettes — some collapsed in the dust, some rising on one elbow, some turning their faces upward toward the pole — flat tonal bands, minimal facial detail. Palette: burnt umber, terracotta, dusty ochre sand, deep violet-blue shadow masses; one molten amber key light raking low from the horizon, long stylized shadows, warm rim light carving every silhouette. Huge graded dusk sky with simplified poster-flat cloud shapes. Confident dark contour linework of varying weight; clean graphic color shapes on figures, painterly texture only in the background. AVOID: any text, lettering, numerals, captions, or watermarks; photorealism; comedic or cartoonish exaggeration; modern objects; extra supernatural figures."),
    ("c_ember_and_ink", "Ember & Ink",
     "Vertical 9:16 cinematic frame from a hand-drawn 1990s theatrical animated feature, rendered as a production cel composite: a lush painterly matte-painting background with clean cel-shaded characters layered over it. A vast wilderness encampment at dusk — hundreds of tents receding to a hazy horizon beneath an enormous gradient sky of dusty rose, burning amber, and deep ultramarine, painted in soft gouache and airbrush strokes with atmospheric perspective dissolving distant detail into warm dust haze; the background has no outlines at all. In the lower foreground, Moses — an elderly, powerful robed figure — strains to plant a tall rough wooden pole upright in the sand, both hands gripping the timber, body angled with real physical effort; atop the pole a bronze serpent effigy blazes in the last low sunlight, the hottest, warmest highlight in the entire frame. Across the middle distance, afflicted Israelites: some collapsed in the dust, some rising on one elbow, some turning their faces upward toward the pole. All figures drawn with confident dark contour lines, flat two-tone cel shading, and a hard-edged golden rim light, popping cleanly off the painterly plate. Long violet shadows, single low golden key light from the horizon, epic wide establishing composition. AVOID: any text, lettering, numerals, captions, watermarks, photorealism, 3D CGI render, panel borders."),
    ("d_keypaint", "Ember Horizon Key-Paint",
     "Traditional gouache visual-development concept painting for a 1990s hand-drawn animated epic feature — a loose, confident pre-production color-key study on toned paper, not a finished frame. Tall vertical cinematic composition. A vast Sinai wilderness encampment at dusk beneath an enormous sky filling the upper half of the frame: banded burnt orange, amber, and dust-hazed rose fading into deep violet-blue overhead. In the lower foreground, Moses — a broad-shouldered elderly Hebrew man in windswept ochre robes — strains to plant a tall rough timber pole upright in the sand, both hands gripping the wood, body angled with real physical effort; a coiled bronze serpent effigy fixed at the pole's top catches the last low sun as the single hottest glint in the picture. Behind him hundreds of dark tent shapes stretch to the horizon, dissolving into warm haze; afflicted Israelites appear as loose two-stroke gestural figures — some collapsed in the dust, some rising on one elbow, some lifting their faces toward the pole. Broad flat brushstrokes, dry-brush scumbled dust, lost-and-found edges, big simple value masses, minimal facial detail, visible paper tooth, long violet shadows, dramatic rim light. AVOID: any text, lettering, numerals, captions, watermarks, or signatures; photorealism; 3D-render look; crisp detail in the distance; neon color."),
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

    print(f"[epic-bakeoff] {len(STYLES)} styles -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "epic_style_bakeoff", units=1, note=f"jesus_pov epic-style plate: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[epic-bakeoff] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
