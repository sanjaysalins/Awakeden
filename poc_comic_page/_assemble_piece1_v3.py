"""Piece 1 v3 ALIVE assembly: COVER + 5 elevated pages, global grade (deep
blacks + storm-blue shadows -- finding 5), stronger print-grade, then audio:
narration delayed under the cover, cold-to-warm score arc, word-timed slam
booms (+ the cover title slam), and the NAIL STRIKE under the THUD! beat.

  .venv\\Scripts\\python.exe poc_comic_page/_assemble_piece1_v3.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

NARR_MP3 = (ROOT.parent / "PythonProject1" / "jesus" / "narration" /
            "36_In_No_Wise_Cast_Out" / "v1" / "narration.mp3")
SCORE_FEAR = ROOT / "music_library" / "clips" / "lonely_searching_a.mp3"
SCORE_GRACE = ROOT / "music_library" / "clips" / "sacred_grace_rise_a.mp3"
BOOM = ROOT / "sound_library" / "clips" / "impact_low_boom.mp3"
NAIL = ROOT / "sound_library" / "clips" / "nail_strike_single.mp3"

PAGES = HERE / "_piece1" / "pages_v3"
PAGE_SOURCES = [
    PAGES / "cover_composite_v3.mp4",
    PAGES / "page1_composite_v3.mp4",
    PAGES / "page2_composite_v3.mp4",
    PAGES / "page3_composite_v3.mp4",
    PAGES / "page4_composite_v3.mp4",
    PAGES / "page5_composite_v3.mp4",
]
CONCAT_MP4 = PAGES / "_concat_silent_v3.mp4"
OUT_MP4 = HERE / "_piece1" / "IN_NO_WISE_GOLDSEAM_v3_ALIVE.mp4"

COVER_DUR = 1.3
CROSSFADE_START = 41.78 + COVER_DUR
CROSSFADE_DUR = 4.0
NAIL_T = 33.14 + 2.98 + COVER_DUR  # the THUD! slam on the nailed-scroll panel

PAGE_SLAMS = [0.0, 5.2,
              10.08, 13.68, 17.42,
              21.04, 24.06, 28.86, 31.14,
              33.14, 36.12, 39.64]
SLAMS = [0.25] + [t + COVER_DUR for t in PAGE_SLAMS]  # 0.25 = cover title slam


def probe_duration(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    for p in PAGE_SOURCES:
        if not p.exists():
            raise SystemExit(f"missing page: {p}")
    listfile = PAGES / "_concat_v3.txt"
    listfile.write_text("".join(f"file '{p.as_posix()}'\n" for p in PAGE_SOURCES))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listfile), "-vf", "tpad=stop_mode=clone:stop_duration=0.12",
                    "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", "30", str(CONCAT_MP4)], check=True)
    vdur = probe_duration(CONCAT_MP4)
    ndur = probe_duration(NARR_MP3)
    print(f"[concat] {CONCAT_MP4} -> {vdur:.3f}s   [narration] {ndur:.3f}s "
          f"(hold after last word {vdur - COVER_DUR - ndur:.2f}s)")

    # finding 5: deepen blacks + a breath of storm blue in the shadows,
    # BEFORE the halftone so the print texture sits on top
    graded0 = PAGES / "_concat_graded0_v3.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(CONCAT_MP4),
                    "-vf",
                    "curves=master='0/0 0.22/0.17 0.55/0.55 1/1',"
                    "colorbalance=bs=0.10:bm=0.02:bh=-0.03",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", "30", str(graded0)], check=True)

    graded = HERE / "_piece1" / "_concat_graded_v3.mp4"
    subprocess.run([sys.executable, str(ROOT / "panel_animator" / "print_grade.py"),
                    "--clip", str(graded0), "--out", str(graded),
                    "--halftone", "0.12", "--fringe", "1", "--grain", "6"], check=True)
    print(f"[print-grade] {graded} -> {probe_duration(graded):.3f}s")

    slam_parts, slam_labels = [], []
    for i, t in enumerate(SLAMS):
        ms = int(t * 1000)
        vol = 0.4 if i == 0 else 0.5
        slam_parts.append(
            f"[4:a]atrim=0:0.8,lowpass=f=800,volume={vol},"
            f"afade=t=out:st=0.45:d=0.35,adelay={ms}|{ms}[s{i}]")
        slam_labels.append(f"[s{i}]")
    slam_mix = "".join(slam_labels) + f"amix=inputs={len(SLAMS)}:normalize=0,{AFMT}[slams]"

    nail_ms = int(NAIL_T * 1000)
    delay_ms = int(COVER_DUR * 1000)
    fade_out_start = max(0.0, vdur - 1.5)
    grace_delay_ms = int(CROSSFADE_START * 1000)
    filt = (
        f"[1:a]adelay={delay_ms}|{delay_ms},{AFMT},apad=whole_dur={vdur:.3f},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur + 0.2:.3f},"
        f"afade=t=in:st=0:d=2,afade=t=out:st={CROSSFADE_START:.2f}:d={CROSSFADE_DUR},"
        f"volume=-8dB[musFear];"
        f"[3:a]{AFMT},adelay={grace_delay_ms}|{grace_delay_ms},atrim=0:{vdur + 0.2:.3f},"
        f"afade=t=in:st={CROSSFADE_START:.2f}:d={CROSSFADE_DUR},"
        f"afade=t=out:st={fade_out_start:.2f}:d=1.5,"
        f"volume=-8dB[musGrace];"
        f"[musFear][musGrace]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        f"[5:a]atrim=0:1.2,volume=0.55,adelay={nail_ms}|{nail_ms},{AFMT}[nail];"
        + ";".join(slam_parts) + ";"
        + slam_mix + ";"
        f"[main][musd][slams][nail]amix=inputs=4:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(graded), "-i", str(NARR_MP3),
                    "-i", str(SCORE_FEAR), "-i", str(SCORE_GRACE), "-i", str(BOOM),
                    "-i", str(NAIL),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur:.3f}",
                    str(OUT_MP4)], check=True)
    print(f"[mux] {OUT_MP4} -> {probe_duration(OUT_MP4):.3f}s")


if __name__ == "__main__":
    main()
