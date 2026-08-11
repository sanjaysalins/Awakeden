"""POC -- what would Noah's gold-standard hand-ink caption style (the same
_short_captions.py burner used on Bronze Serpent/Storm/Two Goats/Jericho/
At-the-Door/Noah) look like on a piece from the OTHER short-form pipeline
(batches/ -- "living-page" motion-comic, bold in-panel comic-box captions
baked into the render itself)?

The real finished short (visual/forsaken_cry_ps221_sfx.mp4) can't be used
directly -- its captions are baked into each panel's own render, not a
separate layer that can be stripped. So this POC rebuilds a plain sequential
cut from the SAME 13 beats / SAME clips / SAME real narration + alignment
(read straight from livingpage_short.spec.json + audio/alignment.json,
nothing invented) -- simple pushin/static holds, no comic-panel motion
graphics, no baked text -- as a clean canvas to burn Noah's real caption
style onto. This is a caption-style test, not a re-edit: the visual cutting
itself is deliberately minimal.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/forsaken_cry_ps221/_poc_noah_style_captions.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(ROOT / "poc_living_sketchbook"))
sys.path.insert(0, str(ROOT / "poc_castbible_look"))
from _short_captions import burn  # noqa: E402
from _polite import be_polite  # noqa: E402  (reused as-is; this is a one-off POC script, not a per-episode fixture)

VIS = HERE / "visual"
CLIPS = VIS / "clips"
AUD = HERE / "audio"
SPEC = json.loads((VIS / "livingpage_short.spec.json").read_text(encoding="utf-8"))
WORK = HERE / "_poc_work"
SILENT = HERE / "_poc_silent.mp4"
MUXED = HERE / "_poc_muxed.mp4"
OUT = HERE / "_POC_noah_style_captions.mp4"

W, H = 1080, 1920


def seg_source(slug: str) -> Path:
    clip = CLIPS / f"{slug}.mp4"
    if clip.exists():
        return clip
    png = VIS / f"{slug}.png"
    if png.exists():
        return png
    raise SystemExit(f"no source for {slug}")


def build_beat(i: int, slug: str, dur: float, rebuild: bool) -> Path:
    out = WORK / f"beat_{i:02d}.mp4"
    if out.exists() and not rebuild:
        return out
    src = seg_source(slug)
    if src.suffix == ".mp4":
        raw_dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip())
        if raw_dur >= dur:
            cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-t", f"{dur:.3f}",
                   "-vf", f"scale={W}:{H}", "-an", "-c:v", "libx264", "-crf", "18",
                   "-pix_fmt", "yuv420p", str(out)]
        else:
            # hold the last frame to fill the remaining beat duration
            cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src),
                   "-vf", f"scale={W}:{H},tpad=stop_mode=clone:stop_duration={dur - raw_dur:.3f}",
                   "-t", f"{dur:.3f}", "-an", "-c:v", "libx264", "-crf", "18",
                   "-pix_fmt", "yuv420p", str(out)]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src), "-t", f"{dur:.3f}",
               "-vf", f"scale={W}:{H}", "-an", "-c:v", "libx264", "-crf", "18",
               "-pix_fmt", "yuv420p", str(out)]
    subprocess.run(cmd, check=True)
    return out


def main():
    be_polite()
    WORK.mkdir(exist_ok=True)
    total = SPEC["total"]
    beats = SPEC["beats"]

    seg_files = []
    for i, b in enumerate(beats):
        t0, t1 = b["t"]
        slug = b["clips"][0]["slug"]
        print(f"[beat {i:02d}] {t0:6.2f}-{t1:6.2f}  {slug}")
        seg_files.append(build_beat(i, slug, t1 - t0, rebuild=False))

    concat_list = WORK / "_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in seg_files) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(concat_list), "-c", "copy", str(SILENT)], check=True)
    print(f"[ok] {SILENT} silent cut built")

    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SILENT), "-i", str(AUD / "narration.mp3"),
                     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                     "-t", f"{total:.3f}", str(MUXED)], check=True)
    print(f"[ok] {MUXED} muxed with real narration")

    words = json.loads((AUD / "alignment.json").read_text(encoding="utf-8"))
    burn(MUXED, OUT, words, skip_windows=[], work_dir=HERE / "_poc_caption_frames")


if __name__ == "__main__":
    main()
