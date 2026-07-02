#!/usr/bin/env python
"""Layer a $0 cinematic score + a forced-placed SFX bed under the finished motion-comic.

Layer stack (user-locked): narration (base, on top) -> MUSIC bed (ducked) -> ambient/SFX
accents (ducked), each keyed off the narration voice. Score = TWO music_library Suno excerpts
chained with a crossfade (dark `lonely_searching` -> grace `sacred_grace_rise`, the grace swell
landing on the CTA close). SFX = single-shot accents placed at the TRUE beat times. No choir pad.

Tier-1 review upgrades (adversarial sound review):
  - CLEARING: music + SFX dip to near-silence ~16.0-22.3s so "Father, forgive them" lands into a
    cleared room, then the score breathes back under it (the prayer is the line the piece exists for).
  - PRAYER REVERB: a gated hall-reverb send on the narration ONLY across the Jesus window (16.7-22.6),
    so the prayer hangs in the air / sits in a bigger acoustic space than the narrator.
  - BELL: one soft low bell toll on the word "Father" (16.94), long decay, then gone (sacred marker,
    not a choir).
  - THINNED CTA: score eases DOWN (not up) under "come, and receive it by faith" -> intimacy, not a
    triumphant swell (fits the grace-anchored 'felt in the bones' close, avoids the hype read).
All $0 — no API. Ear-review gated.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/add_music_sfx.py
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MUS = ROOT / "music_library" / "clips"
SND = ROOT / "sound_library" / "clips"
BP = HERE / "visual" / "_byteplus"
SRC = BP / "father_forgive_them_mocomic_v2.mp4"
MUSIC_WAV = BP / "_score_music.wav"
BELL_WAV = BP / "_bell.wav"
OUT = BP / "father_forgive_them_mocomic_v2_scored.mp4"

OUTRO = 2.5          # hold last frame + let the grace ring out
MUS_GAIN = -13.0     # score under the voice
REV_GAIN = -7.0      # prayer reverb-send level
BELL_GAIN = -15.0    # soft low toll on "Father"
FMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"

# score arc: dark open -> grace close.  (track, start_s, len_s)
DARK  = ("lonely_searching_a", 0.0, 32.0)
GRACE = ("sacred_grace_rise_a", 164.9, 33.0)
GRACE_TRIM = -4.0
XFADE = 6.0

# SFX accents at the TRUE timeline (start_s, slug, gain_db, len_s)
SFX = [
    (0.20, "nail_strike_single",  -5.0, 3.0),
    (4.20, "coins_clinking",     -12.0, 4.0),
    (7.00, "crowd_murmur_distant", -17.0, 14.0),
    (23.80, "coins_clinking",    -13.0, 4.0),
    (36.40, "thunder_low_roll",  -11.0, 7.0),
    (37.00, "rumble_deep_sub",   -19.0, 10.0),
    (43.00, "veil_tearing",      -11.0, 5.0),
    (47.60, "dawn_morning_warm", -18.0, 9.5),
]
BELL_AT = 16.94   # "Father"

# --- time-based automation expressions (t in seconds) ---
# clearing: full -> 0.30 over 15.9-16.3, hold to 21.8, back to full by 22.6
CLEAR = ("if(lt(t,15.9),1,if(lt(t,16.3),1-0.7*(t-15.9)/0.4,"
         "if(lt(t,21.8),0.3,if(lt(t,22.6),0.3+0.7*(t-21.8)/0.8,1))))")
# CTA thinning: full -> 0.45 over 48.5-50.5, hold (intimate close)
CTA = "if(lt(t,48.5),1,if(lt(t,50.5),1-0.55*(t-48.5)/2,0.45))"
# reverb-send gate: only audible across the Jesus prayer window
REVG = ("if(lt(t,16.7),0,if(lt(t,17.0),(t-16.7)/0.3,"
        "if(lt(t,22.0),1,if(lt(t,22.8),1-(t-22.0)/0.8,0))))")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True).stdout.strip())


def build_music(total):
    (dt, ds, dl), (gt, gs, gl) = DARK, GRACE
    fc = (f"[0:a]{FMT},atrim={ds}:{ds+dl},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2[d];"
          f"[1:a]{FMT},atrim={gs}:{gs+gl},asetpts=PTS-STARTPTS,volume={GRACE_TRIM}dB[g];"
          f"[d][g]acrossfade=d={XFADE}:c1=exp:c2=exp[mc];"
          f"[mc]silenceremove=stop_periods=-1:stop_threshold=-50dB:stop_duration=0.25,asetpts=PTS-STARTPTS[m]")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(MUS / f"{dt}.mp3"), "-i", str(MUS / f"{gt}.mp3"),
                    "-filter_complex", fc, "-map", "[m]", str(MUSIC_WAV)], check=True)
    print(f"[music] {dt}[{ds:.0f}:+{dl:.0f}] xfade{XFADE:.0f} {gt}[{gs:.0f}:+{gl:.0f}] -> {dur(MUSIC_WAV):.1f}s")
    return dur(MUSIC_WAV)


def build_bell():
    """A soft low bell: two detuned partials with a long exponential decay (~3.4s), $0 synth."""
    fc = ("sine=frequency=196:duration=3.4[a];sine=frequency=293.66:duration=3.4[b];"
          "sine=frequency=98:duration=3.4[c];[a][b][c]amix=inputs=3:normalize=0,"
          "afade=t=out:st=0:d=3.4:curve=exp,volume=0.6[bell]")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", "anullsrc",  # placeholder input; filtergraph uses lavfi sources
                    "-filter_complex", fc, "-map", "[bell]", "-t", "3.4", str(BELL_WAV)], check=True)


def main():
    if not SRC.exists():
        raise SystemExit(f"no comic: {SRC}")
    V = dur(SRC)
    total = V + OUTRO
    music_real = build_music(total)
    build_bell()
    atempo = max(0.90, min(1.02, music_real / total))
    fade_out = max(0.0, total - 1.5)

    inputs = ["-i", str(SRC), "-i", str(MUSIC_WAV)]
    for _, slug, _, _ in SFX:
        inputs += ["-i", str(SND / f"{slug}.mp3")]
    bell_idx = 2 + len(SFX)
    inputs += ["-i", str(BELL_WAV)]

    parts = [
        # score: fit length, fade in/out, base gain
        f"[1:a]{FMT},atempo={atempo:.4f},asetpts=PTS-STARTPTS,atrim=0:{total+0.2:.2f},"
        f"afade=t=in:st=0:d=2,afade=t=out:st={fade_out:.2f}:d=1.5,volume={MUS_GAIN}dB[musraw]",
        # hold last frame for the outro tail
        f"[0:v]tpad=stop_mode=clone:stop_duration={OUTRO}[vout]",
        # narration -> main (kept) + key (duck trigger) + revsrc (reverb send)
        f"[0:a]{FMT},apad=pad_dur={OUTRO},asplit=3[main][key][revsrc]",
        # prayer reverb send: hall tail, gated to the Jesus window only
        f"[revsrc]aecho=0.8:0.88:55|110|165:0.35|0.25|0.18,volume={REV_GAIN}dB,"
        f"volume='{REVG}':eval=frame[revg]",
    ]
    # SFX accents
    sfx_labels = []
    for i, (st, slug, g, ln) in enumerate(SFX):
        inp = 2 + i; lbl = f"s{i}"
        parts.append(f"[{inp}:a]{FMT},atrim=0:{ln},asetpts=PTS-STARTPTS,"
                     f"afade=t=out:st={max(0.0, ln-0.6):.2f}:d=0.6,volume={g}dB,"
                     f"adelay={int(st*1000)}:all=1[{lbl}]")
        sfx_labels.append(f"[{lbl}]")
    parts.append(f"{''.join(sfx_labels)}amix=inputs={len(SFX)}:normalize=0,apad=whole_dur={total:.2f}[sfxraw]")
    # bell toll on "Father" (kept OUT of the clearing dip so it rings through)
    parts.append(f"[{bell_idx}:a]{FMT},volume={BELL_GAIN}dB,adelay={int(BELL_AT*1000)}:all=1,"
                 f"apad=whole_dur={total:.2f}[bellg]")
    # duck score + SFX under the voice
    parts.append("[musraw][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd0]")
    parts.append("[sfxraw][key]sidechaincompress=threshold=0.06:ratio=1.6:attack=10:release=200[sfxd0]")
    # time automation: clearing on both; CTA-thinning on the score
    parts.append(f"[musd0]volume='{CLEAR}':eval=frame,volume='{CTA}':eval=frame[musd]")
    parts.append(f"[sfxd0]volume='{CLEAR}':eval=frame[sfxd]")
    parts.append("[main][musd][sfxd][revg][bellg]amix=inputs=5:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
    fc = ";".join(parts)

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", fc, "-map", "[vout]", "-map", "[mix]",
           "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", str(OUT)]
    print(f"[mix] score + {len(SFX)} SFX + prayer-clearing + reverb + bell + thinned CTA ...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"[mix] ffmpeg failed:\n{p.stderr[-1800:]}")
    print(f"[mix] done -> {OUT}  ({dur(OUT):.1f}s)")
    print(f"\n  file:///{str(OUT).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
