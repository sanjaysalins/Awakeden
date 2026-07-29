"""Synth the EW01 Two Goats TRAILER cold-open VO (2026-07-22).

A dramatic, quick-hits-and-waves read for the ~30s cold-open trailer that sells
the 9-minute film. Reuses the house synth pattern (ElevenLabs REST
/text-to-speech/{voice}/with-timestamps) and the Grounded Narrator voice.
eleven_v3 primary (honors the [whispers] audio tag as a silent directive), with
an eleven_multilingual_v2 fallback (which reads brackets literally, so tags are
stripped for it). Records the char spend to the ledger.

Copy is derived from the already-locked, panel-approved narration — same thread
(two goats = one offering, both pointing at Christ), hooks from the real mystery
of the text, never clickbait.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_trailer_vo.py
"""
import base64
import re
import subprocess
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT = HERE / "v1" / "visual_16x9_inked" / "_trailer"
OUT.mkdir(parents=True, exist_ok=True)
VO = OUT / "trailer_vo.mp3"

VOICE = config.VOICE_MAP["narrator"]          # LSi9zNCeliLuhIGGS0By — Grounded Narrator
API_BASE = "https://api.elevenlabs.io/v1"

# Trailer script — three waves cresting on the reveal, landing on Christ.
# "..." and line breaks pace the quick hits; [whispers] is an eleven_v3 audio tag.
SCRIPT = """Once a year... one man... one door.
And behind it, a holiness that could kill him.

They brought him two goats.
He killed one. He set the other free.
...Why two?

Same blood. Same door. Every single year.
It was never enough.

Until one Priest walked in...
and sat down.

The veil tore. From the top.
The door never closed again.

One goat died. One goat went free.
[whispers] And both of them were pointing at Him."""


def load_key() -> str:
    env = ROOT.parent / "PythonProject1" / ".env"
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("ELEVENLABS_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no ELEVENLABS_API_KEY in PythonProject1/.env")


def strip_tags(t: str) -> str:  # non-v3 models read [tags] literally
    return re.sub(r"\[[^\]]+\]\s*", "", t)


def synth(key: str, text: str, model: str, voice_settings: dict):
    url = f"{API_BASE}/text-to-speech/{VOICE}/with-timestamps"
    headers = {"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"}
    payload = {"text": text, "model_id": model, "voice_settings": voice_settings}
    return requests.post(url, headers=headers, params={"output_format": "mp3_44100_128"},
                         json=payload, timeout=300)


def dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True).stdout.strip())


def main():
    key = load_key()
    attempts = [
        ("eleven_v3", SCRIPT, {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": True}),
        ("eleven_multilingual_v2", strip_tags(SCRIPT),
         {"stability": 0.4, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True}),
    ]
    audio = used = usedtext = None
    for model, text, vs in attempts:
        print(f"[synth] {model} ({len(text)} chars, voice={VOICE[:8]}...)")
        r = synth(key, text, model, vs)
        if r.status_code == 200:
            audio = base64.b64decode(r.json()["audio_base64"])
            used, usedtext = model, text
            break
        print(f"  HTTP {r.status_code}: {r.text[:200]}")
    if audio is None:
        raise SystemExit("synth failed on all models")

    VO.write_bytes(audio)
    rec = cost.record_eleven("EW01_Two_Goats", "long", "trailer-vo", len(usedtext),
                             note=f"[trailer] cold-open VO ({used})")
    print(f"\n[done] {VO}")
    print(f"       model={used}  {len(usedtext)} chars  {dur(VO):.1f}s  ~${cost._usd(rec.get('est_usd')):.3f}")


if __name__ == "__main__":
    main()
