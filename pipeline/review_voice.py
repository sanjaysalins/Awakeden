"""Audio-first review layer.

The user reviews by EAR, not by reading. So every review summary, proposed change,
or decision is turned into a short SPOKEN digest (mp3) the user plays — instead of a
text report they'd have to read.

- Uses **edge-tts** (free, no API key, natural neural voice) for review digests;
  falls back to offline Windows SAPI if edge-tts is unavailable.
- This is the REVIEW voice (a clear, neutral narrator) — deliberately DIFFERENT from
  the gospel-narration voice (ElevenLabs), so the user never confuses "my report"
  with "the actual short". ElevenLabs is reserved for the final published narration.

CLI:
  .venv\\Scripts\\python.exe -m pipeline.review_voice "spoken text..." --out path.mp3
"""
from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

REVIEW_VOICE = "en-US-GuyNeural"   # clear, neutral; distinct from the gospel narrator
REVIEW_RATE = "-4%"                # a touch slower for easy listening


def speak(text: str, out_mp3: str | Path, *, voice: str = REVIEW_VOICE, rate: str = REVIEW_RATE) -> Path:
    """Render `text` to an mp3 the user can play. edge-tts first, SAPI fallback."""
    out = Path(out_mp3)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        import edge_tts

        async def _go():
            await edge_tts.Communicate(text, voice, rate=rate).save(str(out))
        asyncio.run(_go())
        if out.is_file() and out.stat().st_size > 0:
            return out
    except Exception as e:  # noqa - any edge-tts failure -> offline fallback
        print(f"[review_voice] edge-tts unavailable ({e}); using offline SAPI.", file=sys.stderr)
    return _sapi(text, out)


def _sapi(text: str, out: Path) -> Path:
    wav = out.with_suffix(".sapi.wav")
    # single-quoted here-string so $ / quotes in text are literal
    ps = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.SetOutputToWaveFile('{wav}'); $s.Rate = -2; "
        "$s.Speak([Console]::In.ReadToEnd()); $s.Dispose()"
    )
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                   input=text, text=True, encoding="utf-8", check=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(wav), str(out)], capture_output=True, check=True)
    wav.unlink(missing_ok=True)
    return out


def digest(title: str, sections: list[tuple[str, str]], decision: str = "") -> str:
    """Build a spoken-digest script from a title + (label, text) sections + a closing
    decision prompt. Returns the plain text to feed `speak`."""
    parts = [f"{title}.", ""]
    for label, body in sections:
        parts.append(f"{label}. {body}")
        parts.append("")
    if decision:
        parts.append(decision)
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("text")
    ap.add_argument("--out", default="review_digest.mp3")
    ap.add_argument("--voice", default=REVIEW_VOICE)
    args = ap.parse_args(argv)
    out = speak(args.text, args.out, voice=args.voice)
    print(f"[review_voice] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
