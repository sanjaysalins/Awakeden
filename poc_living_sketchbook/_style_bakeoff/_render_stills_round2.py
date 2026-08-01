"""Style bake-off round 2 -- 5 MORE complementary styles, 1 proof still each,
rendered CONCURRENTLY (user asked for speed). Same nano_banana_pro path as
round 1, same series-wide canon text, same NOTEXT/FULLBLEED framing rules,
same doctrine/period rules. Additive only: everything in _style_bakeoff/.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_bakeoff/_render_stills_round2.py
"""
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_StyleBakeoff"
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong, a carpenter's and traveler's frame. Eyes: warm deep brown, "
    "level and calm. Garment: simple undyed homespun ankle-length tunic with "
    "a woven cord sash, leather sandals."
)
NOTEXT = (
    "CRITICAL: absolutely NO lettering, numerals, words, handwriting, "
    "captions, or printed text ANYWHERE in the image -- every surface is "
    "blank textured stock."
)
FULLBLEED = (
    "CRITICAL FRAMING: the illustrated scene fills the ENTIRE frame edge to "
    "edge, corner to corner -- no large blank margin, no small inset drawing "
    "floating on empty paper; the artwork itself IS the page."
)

S7_WOODCUT = (
    "A bold woodblock/linocut relief print: thick carved black ink strokes, "
    "stark high-contrast black and white with a single warm ochre spot-color "
    "block, chunky faceted forms as if cut from wood grain, dramatic graphic "
    "power, deliberate tool-mark texture in every line, printed impression "
    "showing a faint ink-registration wobble at the edges. Hand-pulled "
    "print energy, not a vector graphic. " + NOTEXT
)
S8_SANGUINE = (
    "A Renaissance master's sanguine red-chalk figure study on warm cream "
    "paper: soft reddish-brown chalk built in layered hatching, delicate "
    "white-chalk highlights, tender observational intimacy, a quiet "
    "unfinished master-study energy -- some contours trail off unfinished "
    "at the page edge. Warm, close, deeply human. " + NOTEXT
)
S9_REEDPEN = (
    "A loose reed-pen and bistre-wash drawing in the manner of an old "
    "master's rapid travel sketch: very few, extremely confident calligraphic "
    "reed-pen strokes suggesting form with almost nothing drawn, broad soft "
    "wash pools of warm brown ink carrying shadow and mood, enormous "
    "quiet empty paper doing most of the work, a sense of having been "
    "drawn in under a minute from life. " + NOTEXT
)
S10_GLASS = (
    "A stained-glass window rendered as a flat hand-painted illustration: "
    "bold black leaded outlines dividing jewel-toned panes of cobalt blue, "
    "deep ruby, and warm gold, glowing as if backlit by real daylight, "
    "flattened medieval-glass figure proportions, rich mineral color with "
    "no gradient shading -- color and lead line alone build the form. "
    + NOTEXT
)
S11_SILHOUETTE = (
    "A dramatic flat graphic poster illustration: figures rendered as pure "
    "black silhouette with no internal detail, set against one bold "
    "saturated gradient sky color, enormous scale and empty negative space, "
    "a single sharp rim-light edge separating silhouette from sky, minimal "
    "and iconic like a hand-printed screenprint poster. " + NOTEXT
)

SHOTS = [
    ("style7_woodcut_lazarus", S7_WOODCUT,
     f"John 11:43-44 -- the raising of Lazarus: {JESUS} stands before a "
     f"dark rock-cut tomb doorway, one arm raised in command; from the "
     f"black doorway a bound grave-clothed figure emerges into the light, "
     f"wrappings trailing; a small crowd recoils in astonishment at the "
     f"tomb's edge. Judean hillside tombs behind. {FULLBLEED}"),
    ("style8_sanguine_well", S8_SANGUINE,
     f"John 4:7-26 -- the woman at the well: {JESUS} sits on the low stone "
     f"rim of Jacob's well at midday, speaking gently; a Samaritan woman "
     f"stands opposite holding a water jar on her shoulder, her face caught "
     f"mid-thought, listening. Plain stone well-head, a coiled rope, open "
     f"noon country behind. {FULLBLEED}"),
    ("style9_reedpen_emmaus", S9_REEDPEN,
     f"Luke 24:29-31 -- the road to Emmaus at dusk: {JESUS} walks between "
     f"two travelers along a quiet country road as evening light fails, "
     f"all three caught mid-stride in conversation, long dusk shadows, a "
     f"small ancient Judean village waiting ahead in the distance -- flat "
     f"mudbrick and pale limestone rooftops low against the hillside, one "
     f"lit window, no European architecture, no church towers or steeples "
     f"anywhere. {FULLBLEED}"),
    ("style10_glass_shepherd", S10_GLASS,
     f"John 10:11 -- the Good Shepherd: {JESUS} stands among a small flock "
     f"of sheep on a green hillside, one lamb carried across his shoulders "
     f"held by its legs, a shepherd's crook in his other hand, warm daylight "
     f"behind him. His face and hands are leaded glass panes of warm "
     f"sun-warmed amber and honey-brown flesh tone, the same family of warm "
     f"skin color used in traditional stained-glass figures -- never any "
     f"cool or green-toned glass pane anywhere on the skin. {FULLBLEED}"),
    ("style11_silhouette_water", S11_SILHOUETTE,
     f"Matthew 14:25 -- walking on the water: a lone robed figure walks "
     f"upright across the surface of a wide sea at night, small wind-driven "
     f"waves beneath his feet, a fishing boat with a few figures visible at "
     f"a distance, a vast dramatic night sky above holding one bright break "
     f"of moonlight. {FULLBLEED}"),
]


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        return False, blob.strip()[-250:]
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000, ""


def one(name, style, scene):
    out = OUT / f"{name}.png"
    if out.exists():
        return name, "skip"
    prompt = style + "\n\nSCENE: " + scene
    ok, err = run(prompt, out)
    if not ok:
        time.sleep(3)
        ok, err = run(prompt, out)
    if ok:
        try:
            cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[bakeoff-r2] {name}")
        except Exception:
            pass
        return name, "ok"
    return name, f"FAILED {err}"


def main():
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(one, n, s, sc): n for n, s, sc in SHOTS}
        for fut in as_completed(futs):
            name, status = fut.result()
            print(f"[{status}] {name}", flush=True)
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
