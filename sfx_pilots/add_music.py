"""Layer a bespoke cinematic ElevenLabs INSTRUMENTAL score UNDER a finished viral_cut_sfx.mp4.

Reusable across shorts. Music is generated to the exact video length, then sidechain-ducked
beneath the existing narration+SFX mix (the voice always sits on top), and the result is
captioned. METERED (Eleven Music) — gated behind --yes; reports the credit delta.

  python sfx_pilots/add_music.py "<v1 folder>" --prompt "<score prompt>" --yes
Outputs beside the cut: music.mp3, viral_cut_sfx_music.mp4, viral_cut_sfx_music_captioned.mp4
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

RED, RST = "\033[1;91m", "\033[0m"
MUSIC_URL = "https://api.elevenlabs.io/v1/music"
SUB_URL = "https://api.elevenlabs.io/v1/user/subscription"


def credits_left(key):
    try:
        r = requests.get(SUB_URL, headers={"xi-api-key": key}, timeout=30)
        if r.status_code == 200:
            d = r.json(); return int(d["character_limit"]) - int(d["character_count"])
    except Exception as e:
        print(f"  (balance check failed: {e})")
    return None


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True).stdout.strip()
    return float(out)


def build_one(folder, prompt, gain=-8.0, script=None, yes=False, regen=False, outro=2.5):
    v1 = Path(folder); asm = v1 / "assembly"
    src = asm / "viral_cut_sfx.mp4"
    if not src.exists():
        print(f"  ! no {src}"); return False
    D = dur(src)
    music = asm / "music.mp3"
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")

    if regen and music.exists():
        music.unlink()
    if music.exists():
        print(f"[music] exists, skip {music}")
    else:
        if not yes:
            print(f"\n{RED}>>> METERED. --yes to authorize Eleven Music (~{int(D)}s) for {v1.name}. <<<{RST}\n"); return False
        glen = D + outro  # generate the score a touch longer so it RINGS OUT over the end-hold
        print(f"[music] composing ~{glen:.0f}s score for {v1.name} ...", flush=True)
        r = requests.post(MUSIC_URL, headers={"xi-api-key": key, "Content-Type": "application/json",
                          "Accept": "audio/mpeg"},
                          json={"prompt": prompt, "music_length_ms": int(glen * 1000),
                                "force_instrumental": True, "model_id": "music_v1"}, timeout=300)
        if r.status_code != 200:
            print(f"{RED}[music] FAILED [{r.status_code}]: {r.text[:300]}{RST}"); return False
        music.write_bytes(r.content); print(f"[music] ok -> {music}")

    out = asm / "viral_cut_sfx_music.mp4"
    return _mix_and_caption(src, music, out, D, gain, script, outro)


def _mix_and_caption(src, music, out, D, gain, script, outro=2.5):
    T = D + outro   # final length: narration ends at D, then a held-frame breathing tail
    fc = (f"[0:v]tpad=stop_mode=clone:stop_duration={outro}[v];"  # hold the last frame for the tail
          f"[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,apad=pad_dur={outro},asplit=2[main][key];"
          f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,atrim=0:{T},"
          f"afade=t=in:st=0:d=2,afade=t=out:st={T-2.5:.2f}:d=2.5,volume={gain}dB[mus];"
          # GENTLE duck keyed on the VOICE; the tail's silence un-ducks the music so it rings out
          f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];"
          f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-i", str(music),
           "-filter_complex", fc, "-map", "[v]", "-map", "[mix]",
           "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-t", f"{T:.2f}", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[mix] ffmpeg failed:\n{p.stderr[-1200:]}"); return False
    print(f"[mix] ok -> {out}")
    if script:
        subprocess.run([str(ROOT / ".venv/Scripts/python.exe"), "-m", "veed_io.caption",
                        "--video", str(out), "--script", script], check=False)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder"); ap.add_argument("--prompt", required=True)
    ap.add_argument("--gain", type=float, default=-17.0)
    ap.add_argument("--script", default=None); ap.add_argument("--yes", action="store_true")
    ap.add_argument("--regen", action="store_true")
    a = ap.parse_args()
    build_one(a.folder, a.prompt, a.gain, a.script, a.yes, a.regen)


if __name__ == "__main__":
    main()
