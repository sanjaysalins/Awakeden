"""3 new SFX x 2 takes for Bartimaeus (owner yes ~$0.40 cap $0.60, 2026-11-14). ElevenLabs sound-generation."""
import sys, requests
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]; sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402
SFX = {
 "hush": ("A few people in an outdoor crowd hushing someone, soft overlapping 'shh' sounds, outdoors, no words, no music", 3.0),
 "cloak": ("A heavy wool cloak thrown off and landing on a dusty road, one quick cloth whoosh and soft thump, outdoors, no music", 2.0),
 "birds": ("Gentle evening birdsong at sunset in a warm quiet desert village, sparse soft chirps, light breeze, calm, no music", 10.0),
}
key = _resolve_key() or sys.exit("no key")
for name, (prompt, secs) in SFX.items():
    for take in (1, 2):
        out = HERE / f"{name}_t{take}.mp3"
        if out.exists():
            continue
        print(f"  sfx {out.name} ...", flush=True)
        r = requests.post("https://api.elevenlabs.io/v1/sound-generation",
                          headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                          json={"text": prompt, "duration_seconds": secs, "prompt_influence": 0.4}, timeout=180)
        if r.status_code != 200:
            sys.exit(f"SFX FAILED [{r.status_code}]: {r.text[:300]}")
        out.write_bytes(r.content)
print("done")
