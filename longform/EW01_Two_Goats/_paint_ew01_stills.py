"""EW01 painted-comic REBUILD — Stage 1 stills (2026-07-23).

Renders painted-comic stills (nano_banana_pro via HF) for the e2e POC scenes
(1-5, 16-19; scene 20 already done). Frozen painted-comic recipe: STYLE BLOCK
(dark chiaroscuro for the law era, bright/warm for the Christ beats) + AVOID +
canon refs chained (aaron_pc_ref / christ_pc_ref). Every SHOT reserves an
in-scene quiet dead zone for the Remotion type, period-locked to the desert
TABERNACLE (not a stone temple / colonnade). NO baked text — Remotion draws it.

Budget: this is the PAINTED-COMIC rebuild, a NEW scope separate from the ink
migration's $40 ceiling. Gate on EW01 rows dated >= 2026-07-23 only.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_paint_ew01_stills.py --dry-run
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_paint_ew01_stills.py --only 1,2
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_paint_ew01_stills.py
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_painted"
REFS = HERE / "v1" / "visual_16x9_inked" / "_painted_comic_test"
AARON = REFS / "aaron_pc_ref.png"
CHRIST = REFS / "christ_pc_ref.png"
SLUG = "EW01_Two_Goats"

PC_START = "2026-07-23"
PC_CEILING = 18.0

STYLE_DARK = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework "
              "and dry-brush texture over rich muted earth-tone painting, dramatic single strong key "
              "light with deep chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not "
              "smooth airbrushed, not a 3D render, no halftone dots, no vintage newsprint.")
STYLE_BRIGHT = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework "
                "and dry-brush texture over rich luminous earth-tone painting, a warm radiant bright "
                "key light with soft lifted shadows and a bright airy overall exposure, glowing golden "
                "highlights, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, not a "
                "3D render, no halftone dots, no vintage newsprint.")
AVOID = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
         "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
         "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
         "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
         "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
         "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
MATCH_DARK = "Match the inked chiaroscuro rendering of the reference image(s)."
MATCH_BRIGHT = "Match the inked rendering of the reference image(s), but keep the bright warm luminous exposure."
FULLBLEED = ("The illustration bleeds fully to all four edges of the frame: NO drawn border, NO "
             "frame, NO rough dark edge-frame or ragged black margin, NO vignette-frame around the art.")

# (id, slug, light 'dark'|'bright', ref, SHOT)
SCENES = [
    (1, "once_a_year", "dark", AARON,
     "The high priest Aaron in golden vestments, small and alone, standing before the towering "
     "curtained Tabernacle tent-court at first light; behind and far below him a vast hushed "
     "multitude of Israelites kept low in shadow; an immense pale dawn sky above; the sacred tent "
     "severe and dominant. Ancient Near-Eastern desert tabernacle of woven curtains and wooden "
     "frames, not a stone temple. Let the lower foreground fall into quiet shadow"),
    (2, "laid_aside_gold", "dark", None,
     "Still-life in a single shaft of light: a golden high-priestly breastplate, ephod and ornate "
     "garments laid upon a worn wooden bench; two weathered ordinary human hands (thumb and four "
     "fingers each, wrists straight, nothing fused or reversed) gently releasing the gold; plain "
     "folded white linen waiting beside it; deep shadow all around. Inside the dim tabernacle tent "
     "of hanging woven curtains, NOT a stone wall or stone room. Keep the dark background quiet and simple"),
    (3, "plain_white_linen", "dark", None,
     "The aged high priest, long gray hair and full gray beard, now in plain white linen, standing "
     "still and arrested (not walking) before a great heavy veil at the end of a dim tabernacle "
     "passage of hanging curtains, seen from behind, head slightly bowed at the threshold; hanging "
     "oil lamps lighting the heavy curtain; his back to us. Ancient Near-Eastern desert tabernacle, "
     "not a stone colonnade. Let the near foreground fall into quiet shadow"),
    (4, "went_in_alone", "dark", None,
     "A small linen-robed silhouette of the high priest before an immense tabernacle veil; through a "
     "narrow parting gap, thick darkness and a single faint golden glow of the mercy seat beyond; the "
     "towering curtain swallowing him. Ancient Near-Eastern desert tabernacle. Deep shadow; keep the "
     "lower frame quiet and dark"),
    (5, "cloud_mercy_seat", "dark", None,
     "The Ark of the Covenant alone in the deep darkness of the Holy of Holies: a gold-covered chest "
     "with two golden cherubim wrought upon its lid, their wings stretched toward each other over the "
     "mercy seat, a radiant cloud of glory glowing softly above it; woven tabernacle curtain walls "
     "receding into shadow; the aged high priest prostrate on the ground before it, tiny beneath the "
     "light; bare and holy, only the Ark, the cloud and the man. Ancient Near-Eastern desert "
     "tabernacle (tent on desert ground, not a stone temple floor). Keep the surrounding shadow simple"),
    (16, "shadow_body_came", "dark", None,
     "The long shadow of a cross falls across an old bronze altar and two goats, cast by an unseen "
     "figure of light off-frame; the shadow stretches toward a luminous open doorway growing pale in "
     "the far dark; the old order dim, the coming light rising. Ancient Near-Eastern tabernacle "
     "interior. Absolutely NO physical cross or wooden cross object anywhere, ONLY a faint "
     "cross-shaped SHADOW on the ground and the altar. Let one side fall into quiet shadow"),
    (17, "entered_in_once", "bright", CHRIST,
     "Christ as the true High Priest standing at a torn radiant veil, one hand laid upon the parted "
     "curtain, paused (not walking) at the threshold of holy light, seen from behind and side; warm "
     "glory opening ahead, darkness behind; a simple luminous undyed white robe, NOT any "
     "high-priestly breastplate, ephod or jewelled vestments. Setting is hanging woven tabernacle "
     "curtains only: absolutely NO stone columns, NO pillars, NO classical or Greco-Roman "
     "architecture of any kind. Let the lower-left fall into quiet shadow with nothing important there"),
    (18, "iniquity_of_us_all", "bright", CHRIST,
     "A unified fulfillment canvas, warm but rendered with HEAVY bold black ink linework and dry-brush "
     "texture and strong deep chiaroscuro shadow throughout (NOT soft, NOT pale, NOT washed-out "
     "watercolour, NOT airbrushed): the figure of Christ central with arms gently open in a simple "
     "luminous undyed white robe; soft-edged to the mid-left, a single goat lying peacefully at rest "
     "upon a low stone altar as if asleep, its pale coat clean and whole; soft-edged to the mid-right, "
     "a second goat walking away into the pale wilderness; a faint cross of soft light above Christ; "
     "the two resolving into the one Priest at the centre. Ancient Near-Eastern setting, no "
     "high-priestly vestments. Let the lower-left corner fall into quiet shadow"),
    (19, "without_the_gate", "bright", None,
     "ONE single lone figure only — the glowing risen Christ, one man entirely alone (absolutely NO "
     "second person, NO companion, NO other figure anywhere in the frame), seen from behind, standing "
     "on a dusty road outside the city wall, looking up the bare hill toward a closed gate; both hands "
     "ordinary human hands (thumb and four fingers, wrists straight); Jerusalem's skyline of low "
     "flat-roofed stone houses and simple square watchtowers behind the rampart wall; warm evening "
     "haze and golden light. Ancient Near-Eastern period. Keep the lower foreground quiet"),
]


def pc_spend() -> float:
    return round(sum(cost._usd(r.get("est_usd")) for r in cost.load()
                     if r.get("episode") == SLUG and r.get("ts", "") >= PC_START), 2)


def gen(slug_id: str, shot: str, light: str, ref) -> Path | None:
    style = STYLE_DARK if light == "dark" else STYLE_BRIGHT
    match = MATCH_DARK if light == "dark" else MATCH_BRIGHT
    prompt = f"{style} Compose this frame: {shot}. {AVOID} {FULLBLEED}"
    cmd = [HF, "generate", "create", "nano_banana_pro", "--prompt",
           prompt + (f" {match}" if ref else ""),
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    if ref:
        cmd += ["--image", str(ref)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"       no url: {blob.strip()[-250:]}")
        return None
    out = OUT / f"{slug_id}.png"
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out if out.exists() and out.stat().st_size > 1000 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--override", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()} if a.only else None
    OUT.mkdir(parents=True, exist_ok=True)
    scenes = [s for s in SCENES if only is None or s[0] in only]

    print(f"[budget] painted-comic spent so far: ${pc_spend():.2f} / ${PC_CEILING:.0f} ceiling")
    est_each = 2 * cost.CREDITS_TO_USD  # ~2cr/still
    print(f"[plan] {len(scenes)} still(s), ~${est_each:.2f} each -> ~${len(scenes)*est_each:.2f}")
    for sid, slug, light, ref, _ in scenes:
        print(f"   #{sid:02d} {light:<6} ref={'aaron' if ref is AARON else 'christ' if ref is CHRIST else '-':<6} {slug}")
    if a.dry_run:
        return

    ok = fail = skip = 0
    for sid, slug, light, ref, shot in scenes:
        name = f"{sid:02d}_{slug}"
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000 and not a.force:
            print(f"[skip] {out.name}"); skip += 1; continue
        proj = pc_spend() + est_each
        if proj > PC_CEILING and not a.override:
            print(f"[STOP] #{sid:02d} would push painted-comic to ~${proj:.2f} > ${PC_CEILING:.0f}. "
                  f"Re-run with --override."); fail += 1; break
        print(f"[img ] #{sid:02d} {light} {slug} ...", flush=True)
        t = time.time()
        res = gen(name, shot, light, ref)
        if res:
            cost.record_hf(SLUG, "long", "stills", "nano_banana_pro",
                           note=f"[painted-comic] #{sid:02d} {slug}")
            print(f"       ok ({time.time()-t:.0f}s) -> {res.name}"); ok += 1
        else:
            print("       FAILED"); fail += 1
    print(f"\n[done] rendered {ok}, skipped {skip}, failed {fail}")
    print(f"[budget] painted-comic total now ~${pc_spend():.2f} / ${PC_CEILING:.0f}")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
