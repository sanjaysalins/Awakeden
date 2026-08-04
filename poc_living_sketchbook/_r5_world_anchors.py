"""living-sketchbook -- world/object anchors for the Day of Atonement episode.

Extends cast-bible (people) to recurring OBJECTS/SETTINGS per the
repeated-element census standing rule (SKILL.md sec.2, added 2026-08-03).
Renders 5 of the 8 catalogued elements in world/TABERNACLE_WORLD.md -- the
3 skipped (door-curtain, Holy Place, blood basin) are folded into another
render or are low-drift-risk text-only per that doc's own reasoning.

16:9 (not the 1:1 used for character busts) -- this is a LONG episode,
matching the aspect the actual stills render at (see bronze_serpent_long/
_s2_stills.py).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_r5_world_anchors.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_e1", ROOT / "poc_castbible_look" / "episode_door" / "_e1_anchors.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

WORLD = Path(__file__).resolve().parent / "world"
WORLD.mkdir(parents=True, exist_ok=True)
EPISODE = "LS_DayOfAtonement"

TABERNACLE_CANON = (
    "A low, rectangular tent shrine standing inside a wide courtyard "
    "fenced by plain white linen hangings on bronze pillars. The tent's "
    "outward roof is plain, weathered reddish-brown and grey animal hide "
    "-- humble and unornamented from the outside, nothing gold visible "
    "from without. Gold only shows at the structure's base, in a glimpse "
    "of gold-overlaid wooden wall-boards beneath the hide covering. A "
    "curtain of blue, purple, and scarlet with fine linen needlework -- "
    "no figures woven into it -- hangs across the entrance. Desert "
    "wilderness setting, low raking light, long shadows across sand."
)
VEIL_CANON = (
    "A heavy hanging curtain of deep blue, purple, and scarlet wool woven "
    "with fine linen, with ancient winged sacred beings woven directly "
    "into the fabric in gold thread -- the SAME golden winged form as the "
    "cherubim on the ark's mercy seat: solemn, otherworldly, composite "
    "winged shapes, faces obscured or turned away, wings dominant. NOT "
    "cute Western cherub-babies, no halos, no rounded infant faces, "
    "nothing Renaissance or Baroque -- these are ancient Near Eastern "
    "sacred emblems, not Christian religious art. Hung from gold hooks on "
    "four gold-clad wooden pillars. Richer and more ornamented than a "
    "plain doorway hanging -- this is the sacred inner curtain of the "
    "tabernacle, shown whole and intact, floor to ceiling, filling most "
    "of the frame."
)
HOLYOFHOLIES_CANON = (
    "A small, perfectly square, windowless chamber, utterly dark except "
    "for a low golden cloud-glow filling the space -- and otherwise "
    "EMPTY. In the center: a gold-overlaid wooden chest about waist-high, "
    "its lid two facing golden cherubim with wings stretched up and "
    "inward, their faces bowed toward the space between them. Nothing "
    "else stands in this room -- no other furniture, no chair, no seat "
    "for a man, bare stone and gold-lit shadow on every side."
)
ALTAR_CANON = (
    "A large, waist-to-shoulder-high foursquare altar of dark weathered "
    "bronze, a raised horn projecting from each of its four corners, its "
    "surface scorched and stained dark from repeated burning -- rough, "
    "heavy, functional metal. Standing alone in an open sunlit courtyard "
    "under open sky, sand and worn stone underfoot."
)
GOAT_CANON = (
    "An ordinary young wilderness goat standing calm and still, short "
    "coarse brown-and-cream coat, plain and unremarkable -- a common "
    "sin-offering animal, nothing distinguished about its appearance, "
    "shown whole from the side against a plain sandy backdrop. The "
    "goat's own coat is clean, dry brown-and-cream fur only -- no red or "
    "blue ink, no wet marks, no drips or streaks of any color anywhere on "
    "the animal's body or legs. Any ink-red or ink-blue accent from the "
    "page style stays confined to the paper border, never touching the "
    "goat itself."
)

ANCHORS = [
    ("tabernacle_ref", TABERNACLE_CANON,
     "Wide establishing view, the whole tent structure and courtyard "
     "fence visible, golden hour light.", "16:9"),
    ("veil_ref", VEIL_CANON,
     "Frontal view of the curtain filling the frame, floor to ceiling, "
     "soft raking museum light picking out the woven gold cherubim.", "16:9"),
    ("holyofholies_ref", HOLYOFHOLIES_CANON,
     "Wide interior view, the ark centered in frame, deep shadow at the "
     "edges, the only light the glowing cloud above the mercy seat.", "16:9"),
    ("altar_ref", ALTAR_CANON,
     "Three-quarter view of the whole altar, sky visible above, harsh "
     "midday desert light.", "16:9"),
    ("goat_ref", GOAT_CANON,
     "Full-body side view of the goat, standing on sand, soft even "
     "daylight.", "16:9"),
]


def run(prompt, out, ar):
    import re
    import subprocess
    cmd = [E.HF, "generate", "create", E.MODEL, "--prompt", prompt,
           "--aspect_ratio", ar, "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, canon, framing, ar in ANCHORS:
        out = WORLD / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = E.STYLE + "\n\nSCENE: " + canon + " " + framing
        print(f"[ref] {name} ...", flush=True)
        ok = run(prompt, out, ar)
        if not ok:
            ok = run(prompt, out, ar)
        if ok:
            cost.record_hf(EPISODE, "long", "world_anchor", E.MODEL, note=f"[dayofatonement] {name}")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
