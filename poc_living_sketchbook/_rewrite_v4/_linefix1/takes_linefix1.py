"""Jericho linefix1: re-record ONLY the two changed narrator lines, with the film's own voice/model/settings
(record_v4.py -> poc_castbible_look/_02_audio.synth: narrator LSi9zNCeliLuhIGGS0By, eleven_multilingual_v2, stability .65, similarity .75).
Takes a, b per line. Cap $0.30."""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]
key = None
for ln in (ROOT.parent / "PythonProject1" / ".env").read_text().splitlines():
    if ln.startswith("ELEVENLABS_API_KEY"): key = ln.split("=", 1)[1].strip().strip('"').strip("'")
assert key
V = "LSi9zNCeliLuhIGGS0By"
T = {"first": "When Jericho fell, the only family that walked out alive was a prostitute’s.".replace("’", "'"),
     "last": "Whatever they call you, her name is in His family. There is room for yours."}
tot = 0
for name, text in T.items():
    for take in ("a", "b"):
        out = H / f"{name}_{take}.mp3"
        if out.exists(): continue
        p = H / "_payload.json"
        p.write_text(json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.65, "similarity_boost": 0.75}}), encoding="utf-8")
        r = subprocess.run(["curl", "-s", "-f", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{V}", "-H", f"xi-api-key: {key}", "-H", "Content-Type: application/json", "-d", f"@{p}", "-o", str(out)], capture_output=True, text=True)
        assert r.returncode == 0 and out.stat().st_size > 1000, r.stderr[-200:]
        tot += len(text); print("ok", out.name, len(text), "chars", flush=True)
        p.unlink()
print("chars billed", tot)
