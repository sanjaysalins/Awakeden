#!/usr/bin/env python
"""EW04 LANDSCAPE motion-page — the mixed-fidelity proof.

ONE wide 16:9 graphic-novel page where every region MOVES, but paid in one place:
  - HERO cell (top-left, 16:9)  = the ONE real veo animation  (hero_serpent_wide.mp4)
  - RIGHT column (9:16)         = an EXISTING shorts clip dropped in WHOLE (no crop)
  - 2 BOTTOM cells              = stills + Ken Burns ($0 cheats)
PIL furniture (parchment caption + inked borders) composited OVER via ffmpeg ($0).

KEEP-BOX discipline: the 9:16 clip fills its column natively (zero crop). The two
Ken-Burns cells are WIDE, so each still carries a keep-box bias so the must-show
element survives the crop (serpents-on-ground low, face centred).

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/landscape_motion_page.py
"""
import importlib.util, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
# reuse the look-test helpers (fill_bias / sanitize / colors / FONT)
spec = importlib.util.spec_from_file_location("lt", HERE / "landscape_looktest.py")
lt = importlib.util.module_from_spec(spec); spec.loader.exec_module(lt)

STILLS = HERE.parent / "stills"
ANIM = HERE.parent / "anim"
LAND = HERE / "_landscape"
TMP = LAND / "_motion_tmp"; TMP.mkdir(parents=True, exist_ok=True)
OUT = LAND / "EW04_landscape_motion_page.mp4"

PAGE_W, PAGE_H = 2560, 1440
M, G, BORDER, FPS, SECS = 56, 30, 12, 30, 8
PAPER_HEX = "0xFCF9F1"
PAPER, INK, PARCH = lt.PAPER, lt.INK, lt.PARCH
FONT = lt.FONT

# ---- geometry: hero (16:9) top-left, 9:16 column right, 2 KB cells bottom-left ----
def _even(n):
    return int(n) - int(n) % 2          # libx264 needs even dims

CW = PAGE_W - 2 * M                      # content width  2448
CH = PAGE_H - 2 * M                      # content height 1328
COL_W = _even(round(CH * 9 / 16))        # 746  (true 9:16 column)
LEFT_W = CW - COL_W - G                  # 1672
HERO_H = _even(round(LEFT_W * 9 / 16))   # 940  (true 16:9 hero)
STRIP_Y = M + HERO_H + G                 # 1026
STRIP_H = CH - HERO_H - G                # 358
KB_W = _even((LEFT_W - G) // 2)          # 820

HERO = (M, M, LEFT_W, HERO_H)
COL = (M + LEFT_W + G, M, COL_W, CH)
KB1 = (M, STRIP_Y, KB_W, STRIP_H)
KB2 = (M + KB_W + G, STRIP_Y, KB_W, STRIP_H)

CAP = "Lift the cure high on a pole -- all who look, live."


def ff(args):
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + args, check=True)


def kenburns_cell(still, dest, w, h, bias, zmax):
    """Crop the portrait still to the cell aspect at the keep-box bias (so the
    must-show element survives), then a slow push-in to zmax filling the cell."""
    crop = lt.fill_bias(Image.open(STILLS / still).convert("RGB"), w * 3, h * 3, *bias)
    src = TMP / f"_src_{dest.stem}.png"; crop.save(src)
    frames = SECS * FPS
    rate = (zmax - 1.0) / frames
    vf = (f"zoompan=z='min(1+{rate:.6f}*on,{zmax})':d={frames}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={FPS},setsar=1")
    ff(["-loop", "1", "-i", str(src), "-t", str(SECS), "-r", str(FPS), "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", str(dest)])


def column_clip(clip, dest, w, h):
    """Loop the 9:16 shorts clip to SECS and scale to the column (native, no crop)."""
    ff(["-stream_loop", "-1", "-i", str(ANIM / clip), "-t", str(SECS),
        "-vf", f"scale={w}:{h}:flags=lanczos,fps={FPS},setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", str(dest)])


def furniture_png(dest):
    page = Image.new("RGBA", (PAGE_W, PAGE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(page)
    for (x, y, w, h) in (HERO, COL, KB1, KB2):
        d.rectangle([x, y, x + w, y + h], outline=INK, width=BORDER)
    # parchment caption, top-left corner over the hero
    lt._box(d, M + 12, M + 12, M + 12 + 760, CAP, 46, PARCH, INK)
    page.save(dest)


def main():
    hero = LAND / "hero_serpent_wide.mp4"
    if not hero.exists():
        raise SystemExit("missing hero veo clip — run _hero_veo.py first")

    col = TMP / "col.mp4"
    column_clip("EW04__08_bitten_multitude.mp4", col, COL[2], COL[3])
    kb1 = TMP / "kb1.mp4"
    kenburns_cell("02b_serpents_spread.png", kb1, KB1[2], KB1[3], (0.5, 0.72), 1.14)
    kb2 = TMP / "kb2.mp4"
    kenburns_cell("04b_face_to_life.png", kb2, KB2[2], KB2[3], (0.5, 0.32), 1.12)
    furn = TMP / "furniture.png"
    furniture_png(furn)
    print("[clips] hero(veo) + column(reuse) + 2 ken-burns + furniture ready")

    # inputs: 0=hero 1=col 2=kb1 3=kb2 4=furniture(png)
    fc = (
        f"color=c={PAPER_HEX}:s={PAGE_W}x{PAGE_H}:d={SECS}:r={FPS}[bg];"
        f"[0:v]scale={HERO[2]}:{HERO[3]}:flags=lanczos,fps={FPS},setsar=1[h];"
        f"[bg][h]overlay={HERO[0]}:{HERO[1]}[a];"
        f"[a][1:v]overlay={COL[0]}:{COL[1]}[b];"
        f"[b][2:v]overlay={KB1[0]}:{KB1[1]}[c];"
        f"[c][3:v]overlay={KB2[0]}:{KB2[1]}[d];"
        f"[d][4:v]overlay=0:0[out]"
    )
    ff(["-i", str(hero), "-i", str(col), "-i", str(kb1), "-i", str(kb2),
        "-loop", "1", "-i", str(furn),
        "-filter_complex", fc, "-map", "[out]", "-t", str(SECS), "-r", str(FPS),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
        "-movflags", "+faststart", str(OUT)])
    print(f"\nmotion page -> {OUT}")
    # a still preview frame for one-click eyeball
    ff(["-ss", "4", "-i", str(OUT), "-frames:v", "1", str(LAND / "_motion_page_frame.png")])


if __name__ == "__main__":
    main()
