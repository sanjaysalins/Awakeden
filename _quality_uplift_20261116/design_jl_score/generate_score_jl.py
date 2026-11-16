r"""DRAFT, NOT RUN. Cinematic score for Swirls "Jacob's Ladder" (film 56.5 s). Design: DESIGN.md.
Spends money (ElevenLabs music_v1, ~72 s, about $1.00). Needs the owner's yes + the --go flag.
Copy of prophecy/02_nazareth/score/generate_score.py with JL numbers. Free-text music_v1 only (never composition_plan / music_v2).
  F:\slk\PycharmProjects\JesusInTheBible\.venv\Scripts\python.exe generate_score_jl.py --go          (pay + join)
  F:\slk\PycharmProjects\JesusInTheBible\.venv\Scripts\python.exe generate_score_jl.py --join-only   ($0)
Retake ONE part: rename its raw file, run --go again (gen_music re-uses any part file that exists)."""
import subprocess, sys
from pathlib import Path
import numpy as np
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
OUTD = Path(r"C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\jl\score_cine")  # F: is full
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
P1, P2, FIT = OUTD / "part1_raw.mp3", OUTD / "part2_raw.mp3", OUTD / "score.mp3"
TOTAL, SPLIT, XF, FADE = 56.5, 36.5, 0.3, 2.5   # split = middle of the 35.45-37.55 s dawn silence
GEN1, GEN2 = 44.0, 28.0                          # used 36.65 / 20.15 -> +7.3 / +7.8 s spare (music_v1 fades its own last ~5 s)
PART1 = ('Cinematic orchestral film score, instrumental only, slow 66 bpm, starts in D minor and turns to F major, reverent, '
 'ancient and timeless, continuous sound with no silence or gaps anywhere. Warm string orchestra with deep cellos and double '
 'basses, concert harp, one soft French horn. No drums, no percussion, no kick, no bass guitar, no synthesizer, no electronic '
 'sounds, no piano, no choir, no vocals, no trailer hits, no horror sounds. Begins at once with low cellos and basses playing a '
 'quiet, restless, short bowed pulse in D minor, a man running away at night, tense but never loud. Around 6 seconds in, the '
 'pulse stops and one bare low string note hangs alone like an unanswered question. Around 10 seconds in, very still and lonely: '
 'one soft high violin note over a low held note, cold night air. Around 13 seconds in, the harp enters softly and the harmony '
 'warms toward F major. Around 15 seconds in, the harp plays four slow rising steps, F, G, A, C, like a ladder, with warm strings '
 'opening underneath. Around 18 seconds in, the harp plays the four steps rising again and then the same notes falling back down, '
 'C, A, G, F. Around 21 seconds in, low strings and the soft French horn hold one deep, broad, warm chord, great and calm. Around '
 '23 seconds in, everything holds perfectly still on that one quiet chord, no melody at all, for two seconds. Around 25 seconds '
 'in, the strings bloom gently and tenderly with the harp, full of kindness. Around 28 seconds in, the four falling steps once '
 'more, settling. Around 30 seconds in, the strings thin to a hushed, high, shimmering held note, awe and wonder, never scary. '
 'Around 35 seconds in, one calm, warm F major string chord like first light at dawn, and it sustains to the very end.')
PART2 = ('Cinematic orchestral film score, instrumental only, F major, slow 60 bpm, warm, reverent and full of grace, ancient and '
 'timeless, continuous sound with no silence or gaps anywhere, continuing the same piece. Warm string orchestra, concert harp, '
 'one French horn. No drums, no percussion, no synthesizer, no electronic sounds, no piano, no choir, no vocals, no trailer hits. '
 'Begins at once on a calm, warm, sustained F major string chord, like first light at dawn. Around 2 seconds in, the harp gently '
 'plays four slow rising steps, F, G, A, C, like a ladder. Around 7 seconds in, the strings begin to rise and open. Around 9 '
 'seconds in, the full string orchestra opens wide into a broad, bright, golden swell with the French horn, like the sky opening, '
 'the biggest moment, noble and never harsh. Around 11 seconds in, the harp plays the four steps rising and then falling, C, A, G, '
 'F, inside the swell. Around 14 seconds in, the swell eases and the rising steps start once more and stop unfinished on the C. '
 'Around 16 seconds in, the four falling steps come down slowly, C, A, G, F, and land home on F with a full, warm F major chord, '
 'strings, harp and French horn together, held and ringing to the very end with no fade.')


def per_sec_db(p, used):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", "22050", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768
    db = [round(20 * np.log10(max(np.sqrt(np.mean(x[i * 22050:(i + 1) * 22050] ** 2)), 1e-9)), 1) for i in range(len(x) // 22050)]
    print(p.name, "per-second RMS:", db)
    bad = [i for i, v in enumerate(db[:int(used) + 1]) if v < -45]
    if bad: sys.exit(f"[FAIL] {p.name}: near-silent seconds {bad} inside the used {used:.1f} s. Retake this part only.")


if __name__ == "__main__":
    if "--go" not in sys.argv and "--join-only" not in sys.argv: sys.exit(__doc__)
    from generate_score_piano import check_timeline_sweep  # noqa: E402
    OUTD.mkdir(parents=True, exist_ok=True)
    if "--go" in sys.argv:
        from pipeline.assembly_align import _resolve_key  # noqa: E402
        from generate_score_v2 import gen_music  # noqa: E402  (music_v1, force_instrumental, dead-intro check)
        key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
        gen_music(PART1, GEN1, P1, key); gen_music(PART2, GEN2, P2, key)
    l1, l2 = SPLIT + XF / 2, TOTAL - SPLIT + XF / 2
    per_sec_db(P1, l1); per_sec_db(P2, l2)
    fc = (f"[0:a]atrim=0:{l1:.3f}[a];[1:a]atrim=0:{l2:.3f},afade=t=out:st={l2 - FADE:.2f}:d={FADE}[b];"
          f"[a][b]acrossfade=d={XF}:c1=tri:c2=tri[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", fc, "-map", "[o]", "-t", f"{TOTAL:.3f}", str(FIT)], check=True)
    check_timeline_sweep(FIT, window=5.0)
    print("[done]", FIT)
