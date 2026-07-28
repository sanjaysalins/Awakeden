"""cast-bible look POC — step 2: 2-voice ~30s narration, direct ElevenLabs.
KJV verbatim: Gen 7:16 "and the LORD shut him in" (narrator, attribution
frame); John 10:9 first clause (JESUS voice, red-letter). Per-line mp3s ->
line-timing json -> concat narration.mp3.

  .venv\\Scripts\\python.exe poc_castbible_look/_02_audio.py
"""
import json
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config  # noqa

HERE = Path(__file__).resolve().parent
AUD = HERE / "audio"
AUD.mkdir(exist_ok=True)

# key lives in PythonProject1/.env
key = None
for ln in (ROOT.parent / "PythonProject1" / ".env").read_text().splitlines():
    if ln.startswith("ELEVENLABS_API_KEY"):
        key = ln.split("=", 1)[1].strip().strip('"').strip("'")
assert key, "no ELEVENLABS_API_KEY"

NARRATOR = config.VOICE_MAP["narrator"]
JESUS = config.VOICE_MAP["jesus"]

LINES = [
    ("l1", NARRATOR,
     "One man spent a lifetime building a box the size of a city block... "
     "because God said rain was coming."),
    ("l2", NARRATOR,
     "And when the rain came, Scripture says something you'd never expect. "
     "Noah didn't shut the door. “And the LORD shut him in.”"),
    ("l3", NARRATOR,
     "One ark. One door. One hand that closed it."),
    ("l4", JESUS,
     "“I am the door: by me if any man enter in, he shall be saved.”"),
    ("l5", NARRATOR,
     "The rain was never the story. The door is... and it is still open."),
]

GAP = 0.35  # s of silence between lines


def synth(voice_id, text, out):
    payload = AUD / "_payload.json"
    payload.write_text(json.dumps({
        "text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.65, "similarity_boost": 0.75}}),
        encoding="utf-8")
    r = subprocess.run(
        ["curl", "-s", "-f", "-X", "POST",
         f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
         "-H", f"xi-api-key: {key}", "-H", "Content-Type: application/json",
         "-d", f"@{payload}", "-o", str(out)],
        capture_output=True, text=True)
    if r.returncode != 0 or not out.exists() or out.stat().st_size < 1000:
        raise RuntimeError(f"tts failed for {out.name}: {r.stderr[-200:]}")


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    timing, t = [], 0.0
    inputs = []
    for name, voice, text in LINES:
        mp3 = AUD / f"{name}.mp3"
        if not mp3.exists():
            print(f"[tts] {name} ({'jesus' if voice == JESUS else 'narrator'}) ...")
            synth(voice, text, mp3)
        d = dur(mp3)
        timing.append(dict(name=name, start=round(t, 3), end=round(t + d, 3),
                           dur=round(d, 3), text=text))
        t += d + GAP
        inputs.append(mp3)
    total = t - GAP
    print(f"[timing] total {total:.2f}s")
    (AUD / "timing.json").write_text(json.dumps(dict(total=round(total, 3),
                                                     gap=GAP, lines=timing), indent=2))
    # concat with gaps
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
    cmd += ["-filter_complex", filt, "-map", "[out]", str(AUD / "narration.mp3")]
    subprocess.run(cmd, check=True)
    print(f"[ok] {AUD / 'narration.mp3'} -> {dur(AUD / 'narration.mp3'):.2f}s")
    for row in timing:
        print(f"  {row['name']}: {row['start']:6.2f} - {row['end']:6.2f}  {row['text'][:50]}")


if __name__ == "__main__":
    main()
