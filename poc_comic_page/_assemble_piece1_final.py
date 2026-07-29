"""Piece 1 assembly step 3 (final): concat the 5 Gold Seam pages, print-grade,
mux narration + ducked score + word-timed slam hits. Adapted from
rung2/_assemble_final_v2.py -- narration/timing/score/slams are UNCHANGED (same
piece, same words, only the pictures changed), so every timestamp carries over
verbatim. Captions are already baked into each page composite (this build's
compositor draws them inline), so all 5 pages feed straight in -- no separate
"_with_text" pass needed.

  .venv\\Scripts\\python.exe poc_comic_page/_assemble_piece1_final.py
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
# cold-to-warm score arc (user feedback: one flat cue didn't move with the story):
# SCORE_FEAR (sparse, unresolved) under the fear pages 1-4, crossfading into
# SCORE_GRACE (building, climax) right at the page4->5 turn -- the same moment
# the door-creak SFX lands (_sfx_piece1.py, 43.4-45.4s).
SCORE_FEAR = ROOT / "music_library" / "clips" / "lonely_searching_a.mp3"
SCORE_GRACE = ROOT / "music_library" / "clips" / "sacred_grace_rise_a.mp3"
BOOM = ROOT / "sound_library" / "clips" / "impact_low_boom.mp3"
CROSSFADE_START = 41.78  # ~2s before the page4->5 turn (43.78s)
CROSSFADE_DUR = 4.0

PAGES = HERE / "_piece1" / "pages_v2"
PAGE_SOURCES = [
    PAGES / "page1_composite_v2.mp4",
    PAGES / "page2_composite_v2.mp4",
    PAGES / "page3_composite_v2.mp4",
    PAGES / "page4_composite_v2.mp4",
    PAGES / "page5_composite_v2.mp4",
]
CONCAT_MP4 = PAGES / "_concat_silent_piece1.mp4"
OUT_MP4 = HERE / "_piece1" / "IN_NO_WISE_GOLDSEAM_v2_period.mp4"

SLAMS = [0.0, 5.2,
         10.08, 13.68, 17.42,
         21.04, 24.06, 28.86, 31.14,
         33.14, 36.12, 39.64]


def probe_duration(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    for p in PAGE_SOURCES:
        if not p.exists():
            raise SystemExit(f"missing page: {p}")
    listfile = PAGES / "_concat_piece1.txt"
    listfile.write_text("".join(f"file '{p.as_posix()}'\n" for p in PAGE_SOURCES))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listfile), "-vf", "tpad=stop_mode=clone:stop_duration=0.12",
                    "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", "30", str(CONCAT_MP4)], check=True)
    vdur = probe_duration(CONCAT_MP4)
    ndur = probe_duration(NARR_MP3)
    print(f"[concat] {CONCAT_MP4} -> {vdur:.3f}s   [narration] {ndur:.3f}s "
          f"(landing hold {vdur - ndur:.2f}s)")

    graded = HERE / "_piece1" / "_concat_graded_piece1.mp4"
    subprocess.run([sys.executable, str(ROOT / "panel_animator" / "print_grade.py"),
                    "--clip", str(CONCAT_MP4), "--out", str(graded),
                    "--halftone", "0.08", "--fringe", "1", "--grain", "5"], check=True)
    print(f"[print-grade] {graded} -> {probe_duration(graded):.3f}s")

    slam_parts, slam_labels = [], []
    for i, t in enumerate(SLAMS):
        ms = int(t * 1000)
        vol = 0.32 if t == 0.0 else 0.5
        slam_parts.append(
            f"[4:a]atrim=0:0.8,lowpass=f=800,volume={vol},"
            f"afade=t=out:st=0.45:d=0.35,adelay={ms}|{ms}[s{i}]")
        slam_labels.append(f"[s{i}]")
    slam_mix = "".join(slam_labels) + f"amix=inputs={len(SLAMS)}:normalize=0,{AFMT}[slams]"

    fade_out_start = max(0.0, vdur - 1.5)
    grace_delay_ms = int(CROSSFADE_START * 1000)
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur:.3f},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur + 0.2:.3f},"
        f"afade=t=in:st=0:d=2,afade=t=out:st={CROSSFADE_START:.2f}:d={CROSSFADE_DUR},"
        f"volume=-8dB[musFear];"
        f"[3:a]{AFMT},adelay={grace_delay_ms}|{grace_delay_ms},atrim=0:{vdur + 0.2:.3f},"
        f"afade=t=in:st={CROSSFADE_START:.2f}:d={CROSSFADE_DUR},"
        f"afade=t=out:st={fade_out_start:.2f}:d=1.5,"
        f"volume=-8dB[musGrace];"
        f"[musFear][musGrace]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        + ";".join(slam_parts) + ";"
        + slam_mix + ";"
        f"[main][musd][slams]amix=inputs=3:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(graded), "-i", str(NARR_MP3),
                    "-i", str(SCORE_FEAR), "-i", str(SCORE_GRACE), "-i", str(BOOM),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur:.3f}",
                    str(OUT_MP4)], check=True)
    print(f"[mux] {OUT_MP4} -> {probe_duration(OUT_MP4):.3f}s")


if __name__ == "__main__":
    main()
