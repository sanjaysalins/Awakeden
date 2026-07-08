"""pipeline/thumbnails.py — $0 thumbnail stage: 16:9 + 9:16 + 1:1 per piece.

Design: the piece's hero FRAME (pulled from the finished _sfx video at its strongest
beat) cover-cropped, a bottom ink gradient, the title in ivory Georgia Bold caps, the
verse ref beneath, and the red AWAKEDEN wordmark with a red rule. Writes to
<piece>/publish/thumbs/. Also exports the standalone brand watermark assets
(_brand/awakeden_watermark*.png) for YouTube Studio's branding slot.

  .venv\\Scripts\\python.exe pipeline/thumbnails.py            # all pieces + assets
  .venv\\Scripts\\python.exe pipeline/thumbnails.py pierced    # substring filter
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
CL1 = ROOT / "batches" / "cluster_01_cross"
CL2 = ROOT / "batches" / "cluster_02_resurrection"
LONG = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1"

RED = (168, 35, 29)        # awakeden red
IVORY = (245, 240, 208)    # caption ivory
INK = (12, 10, 8)

GEORGIA_B = r"C:\Windows\Fonts\georgiab.ttf"
GEORGIA = r"C:\Windows\Fonts\georgia.ttf"
ARIAL_B = r"C:\Windows\Fonts\arialbd.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    for p in (path, GEORGIA_B, ARIAL_B):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _sfx_video(piece_dir: Path) -> Path:
    v = piece_dir / "visual"
    for pat in ("*_sfx.mp4", "_byteplus/*_scored.mp4", "*_scored.mp4"):
        hits = sorted(v.glob(pat))
        if hits:
            return hits[0]
    raise FileNotFoundError(f"no final video under {v}")


# piece -> (video-or-dir, hero-frame seconds, [title lines], ref)
PIECES: dict[str, tuple] = {
    "pierced_zech1210":            (CL1 / "pierced_zech1210", 12.5, ["THEY SHALL LOOK", "ON HIM"], "ZECHARIAH 12:10"),
    "thirty_pieces_zech11":        (CL1 / "thirty_pieces_zech11", 31.3, ["THIRTY PIECES", "OF SILVER"], "ZECHARIAH 11:13"),
    "crucifixion_foretold_ps2218": (CL1 / "crucifixion_foretold_ps2218", 31.7, ["THE DICE WERE", "PROPHESIED"], "PSALM 22:18"),
    "watch_one_hour_matt2640":     (CL1 / "watch_one_hour_matt2640", 11.2, ["COULD YE NOT", "WATCH ONE HOUR"], "MATTHEW 26:40"),
    "father_forgive_them":         (CL1 / "father_forgive_them", 18.0, ["FATHER,", "FORGIVE THEM"], "LUKE 23:34"),
    "today_paradise_luke2343":     (CL1 / "today_paradise_luke2343", 37.0, ["TODAY,", "PARADISE"], "LUKE 23:43"),
    "forsaken_cry_ps221":          (CL1 / "forsaken_cry_ps221", 27.2, ["THE FORSAKEN", "CRY"], "PSALM 22:1"),
    "i_thirst_john1928":           (CL1 / "i_thirst_john1928", 33.0, ["I THIRST"], "JOHN 19:28"),
    "woman_behold_john1926":       (CL1 / "woman_behold_john1926", 29.0, ["WOMAN, BEHOLD", "THY SON"], "JOHN 19:26"),
    "it_is_finished_john1930":     (CL1 / "it_is_finished_john1930", 37.0, ["IT IS", "FINISHED"], "JOHN 19:30"),
    "into_thy_hands_luke2346":     (CL1 / "into_thy_hands_luke2346", 21.5, ["INTO THY", "HANDS"], "LUKE 23:46"),
    "sign_of_jonah_matt1240":      (CL2 / "sign_of_jonah_matt1240", 54.0, ["THE SIGN", "OF JONAH"], "MATTHEW 12:40"),
    "psalm22_long": (LONG / "visual_16x9" / "LivingPage_Psalm22_16x9_scored_sfx.mp4",
                     12.0, ["THE SONG FROM", "THE CROSS"], "PSALM 22"),
}

SIZES = {"16x9": (1280, 720), "9x16": (1080, 1920), "1x1": (1080, 1080)}


def grab_frame(video: Path, t: float, out_png: Path) -> Image.Image:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                    "-i", str(video), "-frames:v", "1", str(out_png)], check=True)
    return Image.open(out_png).convert("RGB")


def cover_crop(img: Image.Image, w: int, h: int) -> Image.Image:
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    sw, sh = img.size
    # bias the crop toward the upper-middle (faces live high in our frames)
    x = (sw - w) // 2
    y = min((sh - h) // 3, sh - h)
    return img.crop((x, y, x + w, y + h))


def compose(frame: Image.Image, size_key: str, title: list[str], ref: str) -> Image.Image:
    w, h = SIZES[size_key]
    im = cover_crop(frame, w, h)
    dr = ImageDraw.Draw(im, "RGBA")

    # bottom ink gradient (title zone); 9:16 keeps the bottom fifth clear of text
    # because the Shorts UI covers it — the title sits in the upper third instead.
    grad_h = int(h * (0.42 if size_key != "9x16" else 0.30))
    for i in range(grad_h):
        a = int(235 * (i / grad_h) ** 1.4)
        y = h - grad_h + i if size_key != "9x16" else grad_h - i
        dr.line([(0, y), (w, y)], fill=INK + (a,))

    ts = int(w * (0.105 if size_key == "16x9" else 0.115))
    f_title = _font(GEORGIA_B, ts)
    f_ref = _font(GEORGIA, int(ts * 0.36))
    f_brand = _font(ARIAL_B, int(ts * 0.30))

    margin = int(w * 0.055)
    if size_key == "9x16":
        ty = int(h * 0.055) + int(ts * 0.2)
    else:
        block = len(title) * int(ts * 1.08) + int(ts * 0.55)
        ty = h - margin - block
    for line in title:
        dr.text((margin + 4, ty + 4), line, font=f_title, fill=(0, 0, 0, 210))  # shadow
        dr.text((margin, ty), line, font=f_title, fill=IVORY)
        ty += int(ts * 1.08)
    dr.rectangle([margin, ty + int(ts * 0.12), margin + int(w * 0.14), ty + int(ts * 0.12) + max(6, ts // 14)], fill=RED)
    dr.text((margin + int(w * 0.16), ty), ref, font=f_ref, fill=IVORY)

    # site wordmark (AWAK bone + EDEN red) — top-right (16:9, 1:1) / bottom-left (9:16)
    from pipeline.channel_dress import draw_wordmark, wordmark_width
    bsize = int(ts * 0.26)
    bw = wordmark_width(bsize)
    if size_key == "9x16":
        bx, by = margin, h - int(h * 0.16)
    else:
        bx, by = w - margin - bw, int(h * 0.045)
    draw_wordmark(im, bx, by, bsize, glow=False, shadow=True)
    return im


def brand_assets(out_dir: Path) -> None:
    """Site-identity marks: ONE word — AWAKEDEN with the split E — on transparent.
    The YouTube branding watermark is the same mark, corner-subtle."""
    from pipeline.channel_dress import (ARIAL_BLK, BONE, RED_BRIGHT,
                                        draw_split_char, font as cd_font,
                                        wordmark_width)
    out_dir.mkdir(parents=True, exist_ok=True)

    def one_word(im: Image.Image, x: float, y: float, size: int, tracking: float):
        dr = ImageDraw.Draw(im)
        f = cd_font(ARIAL_BLK, size)
        cx = x
        for i, ch in enumerate("AWAKEDEN"):
            if i == 4:
                draw_split_char(im, (cx, y), ch, f, size, BONE, RED_BRIGHT)
                dr = ImageDraw.Draw(im)
            else:
                dr.text((cx, y), ch, font=f,
                        fill=(BONE if i < 4 else RED_BRIGHT) + (255,))
            cx += dr.textlength(ch, font=f) + size * tracking

    for px, name in ((800, "awakeden_watermark.png"), (150, "awakeden_watermark_150.png")):
        im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        size = 40
        while wordmark_width(size, 0.08) < px * 0.94:
            size += 2
        size -= 2
        w = wordmark_width(size, 0.08)
        one_word(im, (px - w) / 2, px * 0.5 - size * 0.62, size, 0.08)
        im.save(out_dir / name)
    # horizontal wordmark (transparent)
    w = int(wordmark_width(220)) + 80
    im = Image.new("RGBA", (w, 320), (0, 0, 0, 0))
    one_word(im, 40, 40, 220, 0.14)
    im.save(out_dir / "awakeden_wordmark.png")
    print(f"brand assets -> {out_dir}")


def main() -> int:
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    brand_assets(ROOT / "_brand")
    made = []
    for name, (src, t, title, ref) in PIECES.items():
        if flt and flt not in name:
            continue
        video = src if src.suffix == ".mp4" else _sfx_video(src)
        pub = (src.parent if src.suffix == ".mp4" else src) / "publish" / "thumbs"
        if src.suffix == ".mp4":               # the long: publish/ lives beside v1
            pub = LONG / "publish" / "thumbs"
        frame = grab_frame(video, t, pub / "_frame.png")
        for key in SIZES:
            out = pub / f"thumb_{key}.jpg"
            compose(frame, key, title, ref).save(out, quality=92)
            made.append(out)
        print(f"{name}: 3 thumbs -> {pub}")
    print(f"\n{len(made)} thumbnails written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
