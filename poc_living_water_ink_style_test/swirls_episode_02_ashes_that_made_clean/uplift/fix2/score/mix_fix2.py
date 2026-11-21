"""ep02 fix2: re-score the fix2 picture with an EXISTING score (no new spend).
Usage: python mix_fix2.py epic|somber|trance
Picture = fix2 video stream (copied). Audio = narration.mp3 padded + score (ducked under the voice,
lifted ~+6 dB after the last word, slow 2.5 s fade to silence on the last frame) + SFX bed
(sfxlib, layers re-timed to the fix2 shot list). Writes ep02_fix2_<score>.mp4 next to this file."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[2]
ROOT = EP.parents[1]
sys.path.insert(0, str(ROOT / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

PIC = HERE.parent / "ep02_uplift_fix2_final.mp4"
NARR = EP / "narration.mp3"
AFMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
LAST_WORD = 58.90
FADE = 2.5
# gain / duck per score: epic + trance from their own shipped mixes; somber from assemble_ashes.py's sweep
SCORES = {
    "epic":   (EP / "score_epic.mp3",    2, "threshold=0.55:ratio=1.25:attack=20:release=400"),
    "somber": (EP / "score_somber.mp3",  2, "threshold=0.55:ratio=1.25:attack=20:release=400"),
    "trance": (EP / "score_final.mp3",   3, "threshold=0.7:ratio=1.15:attack=20:release=500"),
}
# fix2 shot times: F01 burning 10.80-16.73, F04 sprinkling 39.30-43.93, F05 hand clasp 49.60-58.10
LAYERS = [
    layer("wilderness_wind",    "wind_desert_bleak",   "loop",    0.0, 55.0, -38.0, fin=1.5, fout=4.0),
    layer("heifer_fire",        "fire_crackling",      "loop",   10.8,  6.2, -33.0, fin=1.0, fout=1.5),
    layer("purification_water", "river_well_water",    "loop",   39.0,  5.4, -32.0, fin=1.5, fout=1.5),
    layer("landing_choir",      "heavenly_choir_soft", "oneshot", 53.0, 8.9, -31.0, fin=2.5, fout=4.0),
]


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def main():
    name = sys.argv[1]
    score, gain, duck = SCORES[name]
    T = dur(PIC)
    lift = f"volume='1+min(max((t-{LAST_WORD})/0.8,0),1)':eval=frame"
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={T},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{T},volume={gain}dB[mus];"
        f"[mus][key]sidechaincompress={duck}[musd];"
        f"[musd]{lift},afade=t=out:st={T - FADE:.3f}:d={FADE}[muse];"
        f"[main][muse]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    mid = HERE / f"_mid_{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PIC), "-i", str(NARR), "-i", str(score),
                    "-filter_complex", filt, "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "pcm_s16le", "-t", f"{T:.3f}", str(mid).replace(".mp4", ".mov")], check=True)
    out = HERE / f"ep02_fix2_{name}.mp4"
    sfxlib.build(Path(str(mid).replace(".mp4", ".mov")), out, LAYERS)
    # sfxlib's -shortest drops the last ~4 video frames: take the full picture from PIC, audio from the sfx mix
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PIC), "-i", str(out), "-map", "0:v", "-map", "1:a",
                    "-c", "copy", "-movflags", "+faststart", str(out.with_suffix(".tmp.mp4"))], check=True)
    out.with_suffix(".tmp.mp4").replace(out)
    print(name, "->", out, f"{dur(out):.2f}s")


if __name__ == "__main__":
    main()
