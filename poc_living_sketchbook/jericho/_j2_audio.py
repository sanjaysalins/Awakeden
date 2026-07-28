"""Jericho — step 2: narration synth (9 lines, narrator + Scripture voice for
the spies' spoken line per the 4-rule reader test). KJV quotes are verbatim
substrings verified against pipeline.scripture 2026-07-28. Writes per-line
mp3s + timing.json (with per-word proportional timing for the verse reveals)
+ narration.mp3.

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j2_audio.py
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config

spec = importlib.util.spec_from_file_location(
    "_a2", ROOT / "poc_castbible_look" / "_02_audio.py")
A = importlib.util.module_from_spec(spec)
# reuse only synth/dur helpers; do our own line list + output dir
A.AUD = Path(__file__).resolve().parent / "audio"
A.AUD.mkdir(parents=True, exist_ok=True)
spec.loader.exec_module(A)
A.AUD = Path(__file__).resolve().parent / "audio"

NARR = config.VOICE_MAP["narrator"]
SCRIPT_V = config.VOICE_MAP["disciples"]  # the spies speak

LINES = [
    ("l1", NARR, "Jericho had the strongest walls in the world. And God told His army to march around them... in silence."),
    ("l2", NARR, "Six days they circled. Thirteen laps in all. Not one arrow. Just feet on sand... and one scarlet cord, hanging from one window."),
    ("l3", NARR, "Inside those walls lived Rahab. A woman with a past... who hid God's spies, and believed. Their answer:"),
    ("l4", SCRIPT_V, "“Bind this line of scarlet thread in the window.”"),
    ("l5", NARR, "On the seventh day the trumpets tore the sky. “The people shouted with a great shout... the wall fell down flat.”"),
    ("l6", NARR, "Every stone came down. One window stood."),
    ("l7", NARR, "Scripture says it plainly: “By faith the harlot Rahab perished not.” Not spared for being good. Spared for believing."),
    ("l8", NARR, "Now read Jesus' family tree: “Salmon begat Booz of Rachab.” The woman behind the scarlet cord became His family."),
    ("l9", NARR, "There is a scarlet line running from her window to a cross. His blood. Bind everything to it."),
]

GAP = 0.32


def main():
    timing, t, inputs = [], 0.0, []
    for name, voice, text in LINES:
        mp3 = A.AUD / f"{name}.mp3"
        if not mp3.exists():
            print(f"[tts] {name} ...")
            A.synth(voice, text, mp3)
        d = A.dur(mp3)
        # proportional-by-character word timing inside the line (honest approx)
        words = text.split()
        chars = [len(w) for w in words]
        total_c = sum(chars)
        wt, acc = [], 0
        for w, c in zip(words, chars):
            w0 = t + d * acc / total_c
            acc += c
            w1 = t + d * acc / total_c
            wt.append(dict(w=w, s=round(w0, 3), e=round(w1, 3)))
        timing.append(dict(name=name, start=round(t, 3), end=round(t + d, 3),
                           dur=round(d, 3), text=text, words=wt))
        t += d + GAP
        inputs.append(mp3)
    total = t - GAP
    (A.AUD / "timing.json").write_text(json.dumps(dict(total=round(total, 3),
                                                       gap=GAP, lines=timing), indent=2))
    filt = "".join(f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo[a{i}];"
                   for i in range(len(inputs)))
    chain = ""
    for i in range(len(inputs)):
        chain += f"[a{i}]"
        if i < len(inputs) - 1:
            filt += f"aevalsrc=0:d={GAP}:s=44100,aformat=channel_layouts=stereo[g{i}];"
            chain += f"[g{i}]"
    filt += chain + f"concat=n={2 * len(inputs) - 1}:v=0:a=1[out]"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in inputs:
        cmd += ["-i", str(p)]
    cmd += ["-filter_complex", filt, "-map", "[out]", str(A.AUD / "narration.mp3")]
    subprocess.run(cmd, check=True)
    print(f"[ok] narration.mp3 -> {A.dur(A.AUD / 'narration.mp3'):.2f}s")
    for row in timing:
        print(f"  {row['name']}: {row['start']:6.2f}-{row['end']:6.2f}  {row['text'][:52]}")


if __name__ == "__main__":
    main()
