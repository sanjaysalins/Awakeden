"""Assemble the v2 LIVING-COMIC cut: concat the 5 v2 pages (with-text where
they exist), then mux narration + ducked score + word-timed slam hits in one
pass. $0 deterministic ffmpeg.

Audio design (B's finishing treatment applied to C, user-approved 2026-07-26):
  - narration.mp3, apad=whole_dur to the video's exact length (INV-26)
  - score: music_library sacred_grace_rise_a (approved S1 rise track),
    -8dB, 2s fade-in, fades out only in the final 1.5s so the swell carries
    the held landing page; sidechain-ducked under the narration via the
    shared pipeline/score_mix constants
  - slams: impact_low_boom lowpassed to a paper-and-ink thump (NOT a
    superhero BOOM -- reverence rule), one per panel entrance, word-timed

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_assemble_final_v2.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

NARR_MP3 = (ROOT.parent / "PythonProject1" / "jesus" / "narration" /
            "36_In_No_Wise_Cast_Out" / "v1" / "narration.mp3")
SCORE = ROOT / "music_library" / "clips" / "sacred_grace_rise_a.mp3"
BOOM = ROOT / "sound_library" / "clips" / "impact_low_boom.mp3"

PAGE_SOURCES = [
    HERE / "page1_composite_v2.mp4",
    HERE / "page2_with_text_v2.mp4",
    HERE / "page3_with_text_v2.mp4",
    HERE / "page4_composite_v2.mp4",
    HERE / "page5_with_text_v2.mp4",
]
CONCAT_MP4 = HERE / "_concat_silent_v2.mp4"
OUT_MP4 = HERE / "IN_NO_WISE_comic_v2.mp4"

# absolute slam times = page start + word-snapped rel t_ins (see
# _compose_pages_v2.py header); page5 is the still landing -- no slams
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
    listfile = HERE / "_concat_v2.txt"
    listfile.write_text("".join(f"file '{p.as_posix()}'\n" for p in PAGE_SOURCES))
    # +0.12s last-frame hold: the 30fps concat lands at 57.633s which puts the
    # landing hold at 2.98s -- a hair under the INV-26 3.0s minimum
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listfile), "-vf", "tpad=stop_mode=clone:stop_duration=0.12",
                    "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", "30", str(CONCAT_MP4)], check=True)
    vdur = probe_duration(CONCAT_MP4)
    ndur = probe_duration(NARR_MP3)
    print(f"[concat] {CONCAT_MP4} -> {vdur:.3f}s   [narration] {ndur:.3f}s "
          f"(landing hold {vdur - ndur:.2f}s)")

    # print-grade halftone pass (gentle: keep the caption text crisp)
    graded = HERE / "_concat_graded_v2.mp4"
    subprocess.run([sys.executable, str(ROOT / "panel_animator" / "print_grade.py"),
                    "--clip", str(CONCAT_MP4), "--out", str(graded),
                    "--halftone", "0.08", "--fringe", "1", "--grain", "5"], check=True)
    print(f"[print-grade] {graded} -> {probe_duration(graded):.3f}s")

    # one slam voice per entrance: short lowpassed thump, delayed into place
    slam_parts, slam_labels = [], []
    for i, t in enumerate(SLAMS):
        ms = int(t * 1000)
        vol = 0.32 if t == 0.0 else 0.5     # gentler opening hit
        slam_parts.append(
            f"[3:a]atrim=0:0.8,lowpass=f=800,volume={vol},"
            f"afade=t=out:st=0.45:d=0.35,adelay={ms}|{ms}[s{i}]")
        slam_labels.append(f"[s{i}]")
    slam_mix = "".join(slam_labels) + f"amix=inputs={len(SLAMS)}:normalize=0,{AFMT}[slams]"

    fade_out_start = max(0.0, vdur - 1.5)
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur:.3f},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur + 0.2:.3f},"
        f"afade=t=in:st=0:d=2,afade=t=out:st={fade_out_start:.2f}:d=1.5,"
        f"volume=-8dB[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        + ";".join(slam_parts) + ";"
        + slam_mix + ";"
        f"[main][musd][slams]amix=inputs=3:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(graded), "-i", str(NARR_MP3),
                    "-i", str(SCORE), "-i", str(BOOM),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur:.3f}",
                    str(OUT_MP4)], check=True)
    print(f"[mux] {OUT_MP4} -> {probe_duration(OUT_MP4):.3f}s")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
                        "-of", "csv=p=0", str(OUT_MP4)], capture_output=True, text=True)
    print(f"[streams] {r.stdout.strip()}")


if __name__ == "__main__":
    main()
