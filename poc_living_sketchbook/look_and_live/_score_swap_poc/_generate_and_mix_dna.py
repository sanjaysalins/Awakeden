"""Look and Live -- score-swap POC round 2: THREE Eleven Music candidates built from the
technical musical-DNA research pass (see _DNA_SYNTHESIS.md), not the mood-word round used
for LOOKANDLIVE_MILESPOC. Same mixing recipe as _generate_and_mix.py (same SFX layers,
sidechain-ducking, no ease-down arc -- this POC wants continuous rise, never resolving),
just parameterized over 3 prompt variants (A/B/C) and run sequentially (one generation +
one ffmpeg pass at a time -- gentle on CPU, no parallel subprocesses).

Each variant writes its own raw/fitted mp3 + its own candidate mp4, alongside (not
overwriting) the existing LOOKANDLIVE_MILESPOC_cc_scored_sfx.mp4 candidate.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_score_swap_poc/_generate_and_mix_dna.py --yes
  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_score_swap_poc/_generate_and_mix_dna.py --yes --variant b
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa: E402
from pipeline.assembly_align import _resolve_key  # noqa: E402
from pipeline import cost  # noqa: E402

HERE = Path(__file__).resolve().parent
EP = HERE.parent
SND = ROOT / "sound_library" / "clips"

SRC = EP / "LOOKANDLIVE_living_sketchbook_cc.mp4"     # pre-score, captioned
TOTAL = 61.900          # matches ../_s5_score_sfx.py exactly (INV-26 hold baked into SRC)
OUTRO_MARGIN = 2.5       # generate a touch longer than TOTAL so trimming avoids Eleven's early-death tail

# Candidates synthesized from the 4-voice (Fable + claude + grok + codex) technical-DNA
# panel round -- see _DNA_SYNTHESIS.md for the full sourced breakdown (137 BPM, F minor,
# i-VI-III-VII loop, two-hand piano ostinato + tempo-synced echo, 3-stage layering).
# No named artist/song anywhere (ElevenLabs ToS hard-blocks that, confirmed 2026-08-16).
PROMPTS = {
    "a": (
        "Sacred instrumental for a reverent short film, 137 BPM, in a minor key, one "
        "continuous rising build that never resolves. A reverbed piano plays a repeating "
        "two-hand figure: a steady broken-chord ostinato under a simple, hypnotic melodic "
        "line, looping a slow four-chord minor progression -- tonic minor, then two warm "
        "major color-chords, then a fourth minor-adjacent chord -- the same chord shape "
        "returning again and again without ever resolving to a final cadence. A tempo-synced "
        "stereo echo trails every piano note, thickening the texture. The piece opens with "
        "piano alone in a vast cathedral reverb; a warm sustained string pad and a low "
        "felt-more-than-heard drone join first; then a solo cello and a distant pipe-organ "
        "swell arrive. In the final third the texture briefly thins, then swells again, "
        "gaining harmonic density and stereo width, as if gathering for an arrival it never "
        "reaches. No drums, no bassline, no drop, no vocals, no choir: pure continuous "
        "ascent, reverent and awe-filled, ending still mid-rise, suspended and unresolved."
    ),
    "b": (
        "Sacred ambient dream-trance instrumental, 137 BPM, reverent and awe-filled, never "
        "clubby: a bright reverbed piano plays a repeating broken-chord ostinato under a "
        "simple hypnotic melody, looping a slow four-chord minor progression that never "
        "resolves. A tempo-synced echo doubles every note. Piano begins alone; a warm string "
        "pad and a low sustained drone join first, then a solo cello and a distant pipe-organ "
        "swell. The arrangement continuously intensifies in harmonic density, loudness, and "
        "stereo width for the full length -- like the opening build of a classic 1990s "
        "dream-trance anthem, but sacred, not euphoric. No drums, no beat, no drop, no "
        "vocals: one unbroken ascent that never resolves into a pulse."
    ),
    "c": (
        "A 137 BPM sacred instrumental in a minor key that only ever builds, never resolves, "
        "in three patient stages. Stage one: a reverbed piano alone, playing a repeating "
        "broken-chord ostinato under a simple melodic figure, looping a four-chord minor "
        "progression, tempo-synced echo trailing every note, a very low sustained drone "
        "barely audible beneath it. Stage two: a warm string pad and a solo cello join, "
        "widening the space around the still-unchanged piano figure. Stage three: the "
        "texture briefly thins, then swells with a distant pipe-organ and rising harmonic "
        "density and stereo width, gathering toward an arrival that never comes. No drums, "
        "no bassline, no drop, no vocals, no choir: continuous devotional ascent, ending "
        "suspended, mid-rise, unresolved."
    ),
    # Round 3: user feedback on A/B/C was "wrong energy/tempo feel -- floatier than 137 BPM
    # dream-trance energy, more new-age ambient than a build clearly counting toward a drop."
    # Diagnosis: "sacred/cathedral/reverent/ambient" language likely anchored the model's
    # genre embedding toward new-age/ambient despite the stated BPM. This variant leads with
    # driving/hypnotic/urgent trance-energy language FIRST and explicitly excludes ambient/
    # new-age/meditative, keeping devotional color as a secondary layer, not the genre anchor.
    "d": (
        "Uptempo dream-trance instrumental, 137 BPM, driving and hypnotic, relentlessly "
        "building tension toward a drop that never arrives -- not ambient, not new-age, not "
        "meditative. A propulsive, insistent broken-chord piano ostinato repeats without "
        "pause under a simple melodic hook, doubled by a tight tempo-synced echo that "
        "thickens the pulse. The harmony loops a bittersweet minor-to-major four-chord "
        "progression, never resolving. Reverberant and expansive like a vast hall, but the "
        "energy stays urgent and forward-driving throughout -- layers stack one on top of "
        "another (a warm pad, a low pulsing drone, a solo cello, a distant swelling organ) "
        "each adding momentum, not just atmosphere. In the final third the tension tightens "
        "further -- rising density, rising stereo width, as if counting down to an arrival "
        "that never lands. No drums, no bassline, no drop, no vocals: pure surging momentum, "
        "sacred in spirit but urgent and alive, ending still mid-surge, unresolved."
    ),
}


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def _mean_db(path: Path, ss: float, d: float):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(ss), "-t", str(d), "-i", str(path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", out)
    return float(m.group(1)) if m else None


def generate(key: str, prompt: str, raw: Path, tag: str) -> None:
    import requests
    glen = TOTAL + OUTRO_MARGIN
    print(f"[music {tag}] composing ~{glen:.1f}s DNA-brief score ...", flush=True)
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": prompt, "music_length_ms": int(glen * 1000),
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"[music {tag}] FAILED [{r.status_code}]: {r.text[:300]}")
    raw.write_bytes(r.content)
    print(f"[music {tag}] ok -> {raw} ({dur(raw):.1f}s raw)")
    cost.record("look_and_live", "short", "score_swap_poc", "elevenlabs-music", "eleven_music_v1",
                units=1, est_usd="~1", mode="metered",
                note=f"DNA-brief round, variant {tag}: {dur(raw):.1f}s raw -> "
                     f"LOOKANDLIVE_DNA_{tag.upper()}_cc_scored_sfx.mp4 candidate")


def fit_to_total(raw: Path, music: Path, tag: str) -> None:
    """Trim/stretch the raw gen to fill TOTAL exactly -- NO ease-down arc (this POC wants
    continuous rise, never resolving). Same logic as _generate_and_mix.py."""
    draw = dur(raw)
    aud_end, t = draw, max(4.0, draw - 2.0)
    while t > draw * 0.55:
        m = _mean_db(raw, t, 2.0)
        if m is not None and m > -30.0:
            aud_end = min(draw, t + 2.0)
            break
        t -= 2.0
    aud_end = max(aud_end, draw * 0.6)
    target = TOTAL + OUTRO_MARGIN
    tempo = max(0.5, min(1.0, aud_end / target))
    af = (f"atrim=0:{aud_end:.2f},asetpts=PTS-STARTPTS,atempo={tempo:.4f},"
          f"afade=t=in:st=0:d=2,afade=t=out:st={target-2.5:.2f}:d=2.5")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", af,
         "-t", f"{target:.2f}", str(music)], check=True)
    print(f"[fit {tag}] audible 0-{aud_end:.1f}s of {draw:.1f}s raw -> stretched to fill "
          f"{target:.1f}s (atempo {tempo:.4f}), no ease-down")


def mix(music: Path, out: Path, tag: str, music_db: float = -8) -> None:
    if not SRC.exists():
        sys.exit(f"missing: {SRC}")
    filt = (
        f"[1:a]{AFMT},atrim=0:{TOTAL},volume={music_db}dB[mus];"
        f"[2:a]{AFMT},atrim=0:{TOTAL},afade=t=in:st=0:d=2,volume=-20dB[wind];"
        f"[3:a]{AFMT},atrim=0:3.859,"
        f"afade=t=in:st=0:d=0.5,afade=t=out:st=3.059:d=0.8,volume=-15dB[crowd1];"
        f"[4:a]{AFMT},atrim=0:5.221,adelay=26237|26237,"
        f"afade=t=in:st=26.237:d=0.8,afade=t=out:st=30.658:d=0.8,volume=-15dB[crowd2];"
        f"[5:a]{AFMT},atrim=0:4.645,adelay=7692|7692,"
        f"afade=t=in:st=7.692:d=1.0,afade=t=out:st=11.437:d=0.9,volume=-17dB[rumble];"
        f"[6:a]{AFMT},atrim=0:7.072,adelay=31458|31458,"
        f"afade=t=in:st=31.458:d=1.5,afade=t=out:st=37.53:d=1.0,volume=-18dB[dawn];"
        f"[mus][wind][crowd1][crowd2][rumble][dawn]amix=inputs=6:normalize=0[bed];"
        f"[0:a]{AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];"
        f"[bed][key]sidechaincompress={SIDECHAIN}[bedd];"
        f"[main][bedd]amix=inputs=2:normalize=0,"
        f"alimiter=limit=0.85:level=disabled,aresample=44100[mix]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(SRC),
         "-i", str(music),
         "-stream_loop", "-1", "-i", str(SND / "wind_desert_bleak.mp3"),
         "-i", str(SND / "crowd_murmur_distant.mp3"),
         "-i", str(SND / "crowd_murmur_distant.mp3"),
         "-i", str(SND / "rumble_deep_sub.mp3"),
         "-i", str(SND / "dawn_morning_warm.mp3"),
         "-filter_complex", filt,
         "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL}",
         "-movflags", "+faststart",
         str(out)],
        check=True,
    )
    print(f"[ok {tag}] {out}")


# D's raw generation reads louder/more energetic than A/B/C (mean_volume ~-13/-14dB vs
# ~-15/-14dB by the end, but starting far hotter: -17.3dB vs A/B's -24/-25dB open) -- per
# user feedback ("better, but volume could be a bit softer"), mixed 3dB quieter than the
# -8dB default.
MUSIC_DB = {"d": -13}


def run_variant(tag: str, key: str) -> None:
    raw = HERE / f"dna_{tag}_raw.mp3"
    music = HERE / f"dna_{tag}.mp3"
    out = HERE / f"LOOKANDLIVE_DNA_{tag.upper()}_cc_scored_sfx.mp4"
    if raw.exists():
        print(f"[music {tag}] raw already exists, skip generation -> {raw}")
    else:
        generate(key, PROMPTS[tag], raw, tag)
    fit_to_total(raw, music, tag)
    mix(music, out, tag, music_db=MUSIC_DB.get(tag, -8))


def main() -> None:
    if "--yes" not in sys.argv:
        sys.exit(">>> METERED (~$1 PER VARIANT, Eleven Music). Re-run with --yes to authorize. <<<")
    variants = [v.lower() for v in sys.argv if v.lower() in PROMPTS]
    if not variants:
        variants = ["a", "b", "c"]
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    for tag in variants:
        run_variant(tag, key)
    print(f"\n[done] {len(variants)} candidate(s) built. Listen and compare before promoting any.")


if __name__ == "__main__":
    main()
