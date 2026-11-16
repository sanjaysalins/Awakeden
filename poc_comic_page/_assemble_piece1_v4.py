"""Piece 1 v4 HOOK assembly ($0, local ffmpeg only). Built from the v4 page
composites (bigger upright captions, no THUD!), with:
  - NO cover: voice starts at 0s (audio reused from the first v4 cut)
  - 1.5s cold open on the inked hand-on-door close-up + the hook question
  - print-grade halftone with an OPAQUE texture (the old RGBA blend turned the
    paper olive-green: 196,181,141 -> 159,169,104)
  - 'IN NO WISE = NEVER' card, JOHN 6:37 tag, 'SO COME.' card, new end title

  .venv\\Scripts\\python.exe poc_comic_page/_assemble_piece1_v4.py
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE / "_piece1"
PAGES = P / "pages_v4"
W = P / "_v4_hook"
STILL = P / "stills_v2" / "p1b_hesitant_hand.png"
AUDIO = W / "audio_v4.m4a"
TEX = W / "halftone_opaque.png"
OUT = P / "IN_NO_WISE_GOLDSEAM_v4_HOOK.mp4"
FONT_I = "fontfile='C\\:/Windows/Fonts/impact.ttf'"
FONT_B = "fontfile='C\\:/Windows/Fonts/arialbd.ttf'"
GOLD = "0xF2C14E"


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def dt(text, font, size, color, y, enable, boxa=0.62, bw=20):
    return (f"drawtext={font}:text='{text}':fontsize={size}:fontcolor={color}:box=1:"
            f"boxcolor=black@{boxa}:boxborderw={bw}:x=(w-text_w)/2:y={y}:enable='{enable}'")


def main():
    srcs = [PAGES / f"page{i}_composite_v3.mp4" for i in range(1, 6)]
    for s in srcs:
        if not s.exists():
            raise SystemExit(f"missing {s}")
    lst = PAGES / "_concat_v4.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in srcs))
    concat = PAGES / "_concat_silent_v4.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-vf", "tpad=stop_mode=clone:stop_duration=0.12", "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", "-r", "30", str(concat)])
    print("[concat]", dur(concat))

    graded0 = PAGES / "_graded0_v4.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(concat), "-vf",
         "curves=master='0/0 0.22/0.17 0.55/0.55 1/1',colorbalance=bs=0.10:bm=0.02:bh=-0.03",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(graded0)])

    # print grade: blend in gbrp (RGB). The default yuv blend vs an RGB texture shifts hue to green
    pg = PAGES / "_printgrade_v4.mp4"
    d0 = dur(graded0)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(graded0), "-loop", "1", "-t", f"{d0:.3f}",
         "-i", str(TEX), "-filter_complex",
         "[0:v]format=gbrp[a];[1:v]format=gbrp[b];"
         "[a][b]blend=all_mode=multiply:all_opacity=0.04[ht];"
         "[ht]rgbashift=rh=-1:bh=1[fr];[fr]noise=alls=6:allf=t+u,format=yuv420p[out]",
         "-map", "[out]", "-t", f"{d0:.3f}", "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", str(pg)])

    # cold open still: inked close-up, slow push, 1.5s, covers the opening of page 1
    ftxt = W / "vf_v4.txt"
    parts = [
        # hook question 0-3.6s
        dt("AFRAID GOD WILL", FONT_I, 104, "white", 1380, "between(t,0,2.0)", bw=22),
        dt("TURN YOU AWAY?", FONT_I, 104, GOLD, 1530, "between(t,0,2.0)", bw=22),
        # source tag during the spoken quote (the big caption already shows the words)
        dt("JOHN 6\\:37", FONT_B, 46, GOLD, 1560, "between(t,18.7,23.7)", boxa=0.66, bw=14),
        # decode card
        dt("IN NO WISE", FONT_I, 110, "white", 1290, "between(t,25.7,28.0)", boxa=0.66),
        dt("= NEVER", FONT_I, 130, GOLD, 1440, "between(t,25.7,28.0)", boxa=0.66),
        # the ask, for the muted viewer
        dt("SO COME.", FONT_I, 150, GOLD, 1450, "between(t,44.9,46.3)", boxa=0.66, bw=24),
        # end title
        dt("HE WILL NEVER TURN AWAY", FONT_I, 84, "white", 1640, "gte(t,57.6)", bw=18),
        dt("THE ONE WHO COMES", FONT_I, 84, GOLD, 1760, "gte(t,57.6)", bw=18),
    ]
    ftxt.write_text(",\n".join(parts))
    body = PAGES / "_body_v4.mp4"
    fc = (
        "[1:v]scale=-2:1920,crop=1080:1920:300:0,"
        "zoompan=z='1+0.0013*in':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30[co];"
        "[0:v][co]overlay=enable='between(t,0,2.0)':x=0:y=0[mid];"
        f"[mid]{','.join(parts)}[out]"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", str(pg), "-loop", "1", "-framerate", "30", "-t", "2.1", "-i", str(STILL),
         "-filter_complex", fc, "-map", "[out]", "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", "-r", "30", str(body)])

    tmp = P / "_v4_nowm.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(body), "-i", str(AUDIO), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "copy", "-t", f"{dur(AUDIO):.3f}", str(tmp)])
    print("[mux]", dur(tmp), "video", dur(body))
    tmp.replace(OUT)
    print("[done]", OUT)


if __name__ == "__main__":
    main()
