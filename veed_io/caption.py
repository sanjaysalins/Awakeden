"""One-command captioner: video in -> styled captioned video out.

Does the whole offline pipeline in a single call:
    extract audio (ffmpeg) -> word timings (faster_whisper) -> burn captions
    (veed_io.serif_captions, the LOCKED Inter/quote-lockup style).

No API calls, $0 per video.

Run (via PowerShell — its ffmpeg/libass works; the Bash-tool ffmpeg segfaults):

    .venv\\Scripts\\python.exe -m veed_io.caption --video "CLIP.mp4"
    .venv\\Scripts\\python.exe -m veed_io.caption --video "CLIP.mp4" --out "OUT.mp4" --guides

Overrides are passed straight through to the renderer:
    --color #RRGGBB   --shadow N   --no-indent   --guides   --model small.en
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from . import aligner, prosody, serif_captions

_WORD_RE = re.compile(r"[A-Za-z0-9']+")
# common speaker labels to drop from a narration script
_SPEAKER_RE = re.compile(
    r"(?mi)^\s*(narrator|jesus|voice|son|father|god|peter|disciple[s]?)\s*:\s*")


def _key(token: str) -> str:
    """Normalised match key for a token (lowercase alphanumerics only)."""
    return "".join(_WORD_RE.findall(token.lower()))


def load_script_text(path: str) -> str:
    """Read a narration script (txt/md) and return just the spoken words.

    Strips markdown markup and leading speaker labels. Alignment tolerates the
    rest, so this only needs to be roughly clean.
    """
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    text = _SPEAKER_RE.sub(" ", text)
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s.*$", " ", text)   # md headings
    text = re.sub(r"[*_`>#\[\]]", " ", text)               # md emphasis/links
    return re.sub(r"\s+", " ", text).strip()


def align_words_to_script(asr_words: list[dict], script_text: str) -> list[dict]:
    """Keep ASR timings but replace the words with the exact script words.

    Sequence-aligns the recognised tokens to the script tokens (difflib) so
    mis-hears are corrected and dropped/added words are handled gracefully.
    """
    if not asr_words:
        return asr_words
    script_tokens = [t for t in script_text.split() if _key(t)]
    if not script_tokens:
        return asr_words

    asr_keys = [_key(w["w"]) for w in asr_words]
    scr_keys = [_key(t) for t in script_tokens]
    ops = difflib.SequenceMatcher(None, asr_keys, scr_keys, autojunk=False).get_opcodes()

    out: list[dict] = []
    prev_end = float(asr_words[0]["start"])
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            for k in range(j2 - j1):
                aw = asr_words[i1 + k]
                out.append({"w": script_tokens[j1 + k],
                            "start": float(aw["start"]), "end": float(aw["end"])})
                prev_end = float(aw["end"])
        elif tag == "replace":
            s, e = float(asr_words[i1]["start"]), float(asr_words[i2 - 1]["end"])
            n = j2 - j1
            for k in range(n):
                out.append({"w": script_tokens[j1 + k],
                            "start": round(s + (e - s) * k / n, 3),
                            "end": round(s + (e - s) * (k + 1) / n, 3)})
            prev_end = e
        elif tag == "delete":
            prev_end = float(asr_words[i2 - 1]["end"])          # heard, not in script -> drop
        elif tag == "insert":                                   # in script, not heard
            nxt = float(asr_words[i1]["start"]) if i1 < len(asr_words) else prev_end + (j2 - j1) * 0.3
            s, e = prev_end, max(nxt, prev_end + 0.05)
            n = j2 - j1
            for k in range(n):
                out.append({"w": script_tokens[j1 + k],
                            "start": round(s + (e - s) * k / n, 3),
                            "end": round(s + (e - s) * (k + 1) / n, 3)})
            prev_end = e
    return out


def _extract_audio(video: str, wav_path: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", video,
         "-vn", "-ac", "1", "-ar", "16000", wav_path],
        check=True,
    )


def _probe_video(video: str) -> tuple[int, int, float]:
    """(width, height, duration_seconds) via ffprobe."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration",
         "-of", "default=nw=1:nk=0", video],
        capture_output=True, text=True,
    ).stdout
    w = h = 0
    dur = 0.0
    for line in out.splitlines():
        if line.startswith("width="):
            w = int(line.split("=")[1])
        elif line.startswith("height="):
            h = int(line.split("=")[1])
        elif line.startswith("duration="):
            try:
                dur = float(line.split("=")[1])
            except ValueError:
                dur = 0.0
    return w, h, dur


def _resolve_aligner(aligner_choice: str, video: str) -> str:
    """auto -> whisperx for long-form/landscape (exact timing), else whisper."""
    if aligner_choice != "auto":
        return aligner_choice
    try:
        import whisperx  # noqa: F401
    except ImportError:
        return "whisper"
    w, h, dur = _probe_video(video)
    landscape = w > h
    if landscape or dur >= 120.0:
        return "whisperx"
    return "whisper"


def transcribe_words(wav_path: str, model_size: str = "base.en") -> list[dict]:
    """Offline word-level transcription via faster_whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "faster-whisper is not installed. Run:  pip install faster-whisper"
        ) from exc
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(wav_path, word_timestamps=True)
    words: list[dict] = []
    for seg in segments:
        for w in (seg.words or []):
            token = w.word.strip()
            if token:
                words.append({
                    "w": token,
                    "start": round(float(w.start), 3),
                    "end": round(float(w.end), 3),
                })
    return words


def caption_video(
    video: str,
    out: str | None = None,
    *,
    model_size: str = "base.en",
    fonts_dir: str = "veed_io/fonts",
    words_json: str | None = None,
    script: str | None = None,
    colour_hex: str | None = None,
    shadow: int | None = None,
    indent_after: bool = True,
    dynamic: bool = True,
    style: str = "ivory",
    aligner_choice: str = "auto",
    guides: bool = False,
    keep_intermediate: bool = False,
) -> str:
    """Caption ``video`` end-to-end and return the output path.

    ``dynamic`` (default on) drives the enlarged key word + italic off the
    REAL vocal emphasis measured from the audio, so the big word moves between
    lines 1-3 phrase to phrase. ``dynamic=False`` is the locked static look.
    """
    video = str(video)
    if out is None:
        p = Path(video)
        out = str(p.with_name(f"{p.stem}_captioned.mp4"))

    wj = str(Path(out).with_suffix(".words.json"))
    use_aligner = "whisper" if (words_json and Path(words_json).is_file()) \
        else _resolve_aligner(aligner_choice, video)

    # Keep a wav around for the whole call so prosody can run AFTER force-align
    # (when the final word windows are known). One temp dir, cleaned at the end.
    with tempfile.TemporaryDirectory() as td:
        wav = str(Path(td) / "audio.wav")
        have_wav = False
        script_text = load_script_text(script) if script else None

        # 1) word timings — reuse a provided words.json, else transcribe/align.
        if words_json and Path(words_json).is_file():
            words = json.load(open(words_json, encoding="utf-8"))
            print(f"using existing word timings: {words_json} ({len(words)} words)")
        elif use_aligner == "whisperx" and script_text:
            # EXACT path: phoneme forced-alignment of the known script.
            print("extracting audio ...")
            _extract_audio(video, wav)
            have_wav = True
            print(f"forced-aligning script to audio (whisperx, {model_size}) ...")
            words = aligner.forced_align_script(wav, script_text, model_size)
        elif use_aligner == "whisperx":
            print("extracting audio ...")
            _extract_audio(video, wav)
            have_wav = True
            print(f"transcribing + aligning (whisperx, {model_size}) ...")
            words = aligner.transcribe_align(wav, model_size)
            print(f"  {len(words)} words")
        else:
            print("extracting audio ...")
            _extract_audio(video, wav)
            have_wav = True
            print(f"transcribing offline (faster_whisper, {model_size}) ...")
            words = transcribe_words(wav, model_size)
            print(f"  {len(words)} words transcribed")
            if script_text:           # difflib swap to exact words (whisper path)
                before = len(words)
                words = align_words_to_script(words, script_text)
                print(f"force-aligned to script: {before} -> {len(words)} words "
                      f"(words now exact, timing from audio)")

        # 1c) measure per-word vocal emphasis (loudness) for dynamic placement.
        if dynamic and not all("rms" in w for w in words):
            if not have_wav:
                print("extracting audio for emphasis ...")
                _extract_audio(video, wav)
            print("measuring vocal emphasis (offline) ...")
            words = prosody.word_loudness(wav, words)

    Path(wj).write_text(json.dumps(words, ensure_ascii=False, indent=1),
                        encoding="utf-8")

    # 2) burn the captions (dynamic emphasis layout, or locked static).
    print(f"rendering captions ({'dynamic' if dynamic else 'static'}) ...")
    serif_captions.render(
        video, wj, out, fonts_dir,
        colour_hex=colour_hex, shadow=shadow,
        indent_after=indent_after, guides=guides, dynamic=dynamic, style=style,
    )

    if not keep_intermediate and not words_json:
        # leave words.json (handy for re-tweaks); only the temp wav was removed.
        pass
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="One-command offline captioner (audio -> timings -> burn).")
    ap.add_argument("--video", required=True, help="input video")
    ap.add_argument("--out", help="output mp4 (default: <video>_captioned.mp4)")
    ap.add_argument("--model", default="base.en",
                    help="faster_whisper model (base.en default; small.en more accurate)")
    ap.add_argument("--fonts", default="veed_io/fonts")
    ap.add_argument("--words", help="reuse an existing words.json (skip transcription)")
    ap.add_argument("--script", help="exact narration script (txt/md) to force-align "
                    "to — corrects mis-heard words, keeps audio timing")
    ap.add_argument("--style", choices=sorted(serif_captions.STYLES), default="ivory",
                    help="caption look: ivory(locked)/glow/pop/impact/karaoke/minimal")
    ap.add_argument("--color", help="override the base text colour hex")
    ap.add_argument("--shadow", type=int, default=None,
                    help="soft shadow depth override (default: per style)")
    ap.add_argument("--no-indent", dest="indent_after", action="store_false",
                    help="disable the quote-lockup indent (on by default)")
    ap.add_argument("--guides", action="store_true",
                    help="overlay the Shorts no-go zones (red) for QA")
    ap.add_argument("--static", dest="dynamic", action="store_false",
                    help="locked static look (big word always mid, italic on all "
                         "connectors); default is dynamic emphasis-driven placement")
    ap.add_argument("--aligner", choices=["auto", "whisper", "whisperx"],
                    default="auto",
                    help="word-timing engine. auto = whisperx (exact phoneme "
                         "forced-align) for long-form/16:9, faster_whisper for shorts")
    ap.set_defaults(indent_after=True, dynamic=True)
    args = ap.parse_args(argv)

    try:
        out = caption_video(
            args.video, args.out,
            model_size=args.model, fonts_dir=args.fonts, words_json=args.words,
            script=args.script, colour_hex=args.color, shadow=args.shadow,
            indent_after=args.indent_after, guides=args.guides, dynamic=args.dynamic,
            style=args.style, aligner_choice=args.aligner,
        )
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"\ndone -> {Path(out).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
