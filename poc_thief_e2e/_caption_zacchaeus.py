"""Caption the Zacchaeus final video via WhisperX forced alignment + the
serif_captions.py $0 renderer -- per COMIC_STRIP_NATIVE_SPEC.md's caption
decision (WhisperX default, no baked text in the art).

  .venv\\Scripts\\python.exe poc_thief_e2e/_caption_zacchaeus.py
"""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

VIDEO = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus" / "ZACCHAEUS_WITH_SCORE.mp4"
OUT_DIR = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus"
WAV = OUT_DIR / "_audio_for_align.wav"
WORDS_JSON = OUT_DIR / "words.json"

SPOKEN_TEXT = (
    "A rich tax collector, hated by everyone in Jericho, wanted just one look at Jesus. "
    "He was too short to see over the crowd, so he did something no grown man would ever do. "
    "He climbed a tree. When Jesus reached that spot, he stopped. He looked up. And he called "
    "this man by name: Zacchaeus, make haste, and come down; for to day I must abide at thy "
    "house. Not the religious leaders. Not the crowd who thought they deserved him more. A "
    "cheat, up a tree. Zacchaeus climbed down and said: Behold, Lord, the half of my goods I "
    "give to the poor; and if I have taken any thing from any man by false accusation, I "
    "restore him fourfold. One conversation changed what he did with his money, his life, his "
    "name. Jesus told him why: For the Son of man is come to seek and to save that which was "
    "lost. That's not just Zacchaeus's story. That's why Jesus came for you too."
)


def main():
    # 1. extract audio as 16kHz mono wav for whisperx
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(VIDEO), "-ar", "16000", "-ac", "1",
                     str(WAV)], check=True)

    # 2. forced-align the known script
    sys.path.insert(0, str(ROOT / "veed_io"))
    from aligner import forced_align_script
    words = forced_align_script(str(WAV), SPOKEN_TEXT)
    WORDS_JSON.write_text(json.dumps(words, indent=2), encoding="utf-8")
    print(f"[align] {len(words)} words aligned -> {WORDS_JSON}")

    # 3. burn captions via serif_captions.py
    out_final = OUT_DIR / "ZACCHAEUS_CAPTIONED.mp4"
    cmd = [sys.executable, "-m", "veed_io.serif_captions", "--video", str(VIDEO),
           "--words", str(WORDS_JSON), "--out", str(out_final)]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    print(r.stdout[-3000:])
    if r.returncode != 0:
        print("STDERR:", r.stderr[-3000:])
        raise SystemExit(1)
    print(f"\n[done] {out_final}")


if __name__ == "__main__":
    main()
