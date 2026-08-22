"""$0 QC helper: 6-frame contact sheet of a clip (first/last + 4 evenly spaced),
plus a first-vs-last absolute-difference heatmap so "did anything grow/drift"
is visible, not guessed. Usage: python _contact_sheet.py <clip.mp4>"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

FFMPEG = "ffmpeg"


def main(mp4: Path) -> Path:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip())
    n = 6
    ts = [0.05] + [dur * i / (n - 1) for i in range(1, n - 1)] + [max(dur - 0.1, 0)]
    frames = []
    for i, t in enumerate(ts):
        out = mp4.with_name(f"_{mp4.stem}_frame{i}.png")
        subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(mp4),
                        "-frames:v", "1", str(out)], check=True)
        frames.append((t, Image.open(out).convert("RGB")))
    H = 640
    tiles = [(t, im.resize((int(im.width * H / im.height), H))) for t, im in frames]
    diff = ImageChops.difference(frames[0][1], frames[-1][1]).convert("L").point(lambda v: min(255, v * 4))
    diff = diff.resize(tiles[0][1].size)
    W = sum(im.width for _, im in tiles) + diff.width + 10 * (len(tiles) + 2)
    sheet = Image.new("RGB", (W, H + 30), "white")
    dr = ImageDraw.Draw(sheet)
    x = 10
    for t, im in tiles:
        sheet.paste(im, (x, 30)); dr.text((x, 8), f"t={t:.2f}s", fill="black"); x += im.width + 10
    sheet.paste(diff.convert("RGB"), (x, 30)); dr.text((x, 8), "|first-last| x4", fill="black")
    out = mp4.with_name(f"_{mp4.stem}_contact.png")
    sheet.save(out)
    for i in range(n):
        mp4.with_name(f"_{mp4.stem}_frame{i}.png").unlink(missing_ok=True)
    print(out, f"dur={dur:.2f}s", f"{frames[0][1].size}")
    return out


if __name__ == "__main__":
    main(Path(sys.argv[1]))
