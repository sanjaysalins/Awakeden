"""Add a Cinematic-Orchestral Suno score to a finished long-form 16:9 video.

Chains pre-approved tracks from music_library/clips/ with a crossfade, then
sidechain-ducks the score under the existing narration+SFX mix. $0 — no API.

Usage:
    python longform/_add_score_lf.py <episode_dir> [--yes] [--regen]

Outputs:
    <visual_16x9/<stem>_scored.mp4>
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MUSIC_LIB = ROOT / "music_library" / "clips"

# Per-episode score recipe.  Add new entries as more long-forms are produced.
#   segments: Suno slug names (played in order, xfade_s overlap between each pair)
#   xfade_s:  crossfade duration in seconds at each join point
#   gain_db:  score level under the narration (narration standard is -8 dB)
#   outro_s:  tail hold after narration ends (last frame clone + score ring-out)
EPISODES: dict[str, dict] = {
    "01_Isaiah_53_Suffering_Servant": {
        "segments": ["lonely_searching_a", "sacred_grace_rise_a"],
        "xfade_s": 6.0,
        "gain_db": -11.0,
        "outro_s": 2.5,
    },
    # Psalm 22 (418.2s) — ache (M1-M4) -> grace enters M5 -> climaxes M6 turn -> resolves M7.
    # Closer is sacred_grace_rise_b (229.9s) so the score covers the final "Come and join"
    # CTA (~416.6s); the _a take (197.9s) would leave the close bare. NOTE: _b is a "pending"
    # audition take in music_library (same grace recipe as _a) — swap if the user prefers _a.
    "02_Psalm_22_Song_From_The_Cross": {
        "segments": ["lonely_searching_a", "sacred_grace_rise_b"],
        "xfade_s": 6.0,
        "gain_db": -11.0,
        "outro_s": 2.5,
    },
    # Passover Lamb (509.5s) — ancient Egypt night + the lamb + the strange detail (M1-M3,
    # searching/solemn) -> the centuries-early cross-match + the honest objection (M4-M5,
    # holy weight) -> the exchange + invitation + risen-Christ hero close (M6-M7, grace rising).
    # 3 segments cover the full 509.5s; grace-rise lands on the M7 invitation/hero.
    "03_The_Passover_Lamb": {
        "segments": ["lonely_searching_a", "glory_holy_stillness_a", "sacred_grace_rise_b"],
        "xfade_s": 6.0,
        "gain_db": -11.0,
        "outro_s": 2.5,
    },
    # Bronze Serpent (467.6s) — the dying camp + the venom + the strange cure on the pole
    # (M1-M3, lonely/searching) -> the centuries-early cross-match + Nicodemus + the honest
    # objection / Hezekiah (M4-M5, holy weight) -> the exchange + the look + whosoever + the
    # risen-Christ hero close (M6-M7, grace rising). Same proven 3-segment arc as #03; grace
    # lands on the M7 invitation/hero. Full cinematic-orchestral, no choir pad (SFX carries ambience).
    "04_The_Bronze_Serpent": {
        "segments": ["lonely_searching_a", "glory_holy_stillness_a", "sacred_grace_rise_b"],
        "xfade_s": 6.0,
        "gain_db": -11.0,
        "outro_s": 2.5,
    },
    # Seed of the Woman (503.3s) — Eden, the fall, the first promise spoken into the serpent's
    # curse (M1-M3, lonely/searching) -> the centuries-early match "made of a woman" + the honest
    # objection (M4-M5, holy weight) -> the head/heel exchange + the cross + the empty tomb + the
    # invitation/risen-Christ hero close (M6-M7, grace rising). Same proven 3-segment arc as #03/#04;
    # grace lands on the M7 invitation/hero. Full cinematic-orchestral, no choir pad (SFX = ambience).
    "05_The_Seed_Of_The_Woman": {
        "segments": ["lonely_searching_a", "glory_holy_stillness_a", "sacred_grace_rise_b"],
        "xfade_s": 6.0,
        "gain_db": -11.0,
        "outro_s": 2.5,
    },
    # EW01 Two Goats (589.2s) — EPIC cinematic-orchestral (freshly generated, ElevenLabs Music):
    # ASCENT (solemn Day-of-Atonement weight, the ritual that never finishes) -> xfade ~289s ->
    # TRIUMPH (a vast swell that peaks right at the reveal ~340s "the body came / He sat down",
    # then resolves into radiant grace for the close). Full strings+horns+organ, no choir, no
    # percussion. -9dB (more present than the gentle library) under the narration sidechain-duck.
    "EW01_Two_Goats": {
        "segments": ["epic_atonement_ascent_a", "epic_atonement_triumph_a"],
        "xfade_s": 6.0,
        "gain_db": -9.0,
        "outro_s": 2.5,
    },
}


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def run(episode_dir: Path, yes: bool, regen: bool) -> None:
    ep_name = episode_dir.name
    recipe = EPISODES.get(ep_name)
    if not recipe:
        sys.exit(
            f"No score recipe for '{ep_name}'.\n"
            f"Known episodes: {list(EPISODES)}"
        )

    visual_dir = episode_dir / "v1" / "visual_16x9"
    candidates = [
        c for c in sorted(visual_dir.glob("*_16x9.mp4"))
        if "_scored" not in c.name
        and "_captioned" not in c.name
        and ".bak." not in c.name
        and ".frozen." not in c.name
    ]
    if not candidates:
        sys.exit(f"No *_16x9.mp4 found in {visual_dir}")
    src = candidates[0]

    out = src.with_name(src.stem + "_scored.mp4")
    if out.exists() and not regen:
        print(f"[score] already exists — skip (--regen to redo): {out}")
        return

    V = dur(src)
    outro = recipe["outro_s"]
    total = V + outro
    gain = recipe["gain_db"]
    xfade_s = recipe["xfade_s"]
    segments = [MUSIC_LIB / (s + ".mp3") for s in recipe["segments"]]
    for seg in segments:
        if not seg.exists():
            sys.exit(f"Missing music segment: {seg}")

    seg_durations = [dur(s) for s in segments]
    chained_dur = sum(seg_durations) - xfade_s * (len(segments) - 1)

    print(f"[score] source  : {src.name} ({V:.1f}s)")
    print(f"[score] segments: {[s.name for s in segments]}")
    print(f"[score] arc     : {' -> '.join(f'{d:.0f}s' for d in seg_durations)} "
          f"(xfade {xfade_s}s) = {chained_dur:.1f}s")
    print(f"[score] target  : {total:.1f}s  gain={gain}dB  outro={outro}s")
    print(f"[score] output  : {out}")

    if not yes:
        print("\n  $0 (Suno library, no API spend). Re-run with --yes to mix.\n")
        return

    # Build filter_complex -------------------------------------------------
    # Inputs: 0=video  1..N=music segments
    # Chain music with acrossfade, duck under narration via sidechaincompress.
    n = len(segments)
    fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"

    if n == 1:
        music_chain = f"[1:a]{fmt}[music_raw]"
    else:
        parts = []
        for i in range(n):
            parts.append(f"[{i+1}:a]{fmt}[s{i}]")
        # Chain crossfades: s0+s1→x01; x01+s2→x012; ...
        prev = "s0"
        for i in range(1, n):
            nxt = f"x{i}"
            parts.append(f"[{prev}][s{i}]acrossfade=d={xfade_s:.1f}:c1=exp:c2=exp[{nxt}]")
            prev = nxt
        parts.append(f"[{prev}]anull[music_raw]")
        music_chain = "; ".join(parts)

    fade_out_start = max(0.0, total - 2.5)
    fc = (
        f"{music_chain}; "
        # Trim/fade/gain the chained score
        f"[music_raw]atrim=0:{total+0.2:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=2,"
        f"afade=t=out:st={fade_out_start:.2f}:d=2.5,"
        f"volume={gain}dB[mus]; "
        # Hold the last frame of video for outro
        f"[0:v]tpad=stop_mode=clone:stop_duration={outro}[vout]; "
        # Split narration+SFX into main (output) and key (sidechain trigger)
        f"[0:a]{fmt},apad=pad_dur={outro},asplit=2[main][key]; "
        # Duck score whenever voice is present
        f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd]; "
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )

    inputs = ["-i", str(src)] + [x for seg in segments for x in ["-i", str(seg)]]
    cmd = (
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        + inputs
        + ["-filter_complex", fc,
           "-map", "[vout]", "-map", "[mix]",
           "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k",
           "-t", f"{total:.3f}",
           str(out)]
    )

    print("[score] mixing (may take ~30s)...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[score] ffmpeg FAILED:\n{p.stderr[-2000:]}")
        sys.exit(1)

    final_dur = dur(out)
    print(f"[score] done  -> {out}  ({final_dur:.1f}s)")
    print(f"\n  file:///{ str(out).replace(chr(92), '/') }")


def main() -> None:
    ap = argparse.ArgumentParser(description="Add Suno orchestral score to long-form 16x9 video")
    ap.add_argument("episode_dir", help="Episode folder, e.g. longform/01_Isaiah_53_Suffering_Servant")
    ap.add_argument("--yes", action="store_true", help="Run the mix (it is free, but confirm intent)")
    ap.add_argument("--regen", action="store_true", help="Re-run even if _scored.mp4 already exists")
    args = ap.parse_args()
    run(Path(args.episode_dir).resolve(), args.yes, args.regen)


if __name__ == "__main__":
    main()
