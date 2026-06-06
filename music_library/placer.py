"""placer.py — lay a library music bed under a finished narrated clip.

GENERALIZES the proven `11labs-testing/enhance.py` mix() (forced-align + sidechaincompress
duck + adelay/fades/alimiter/mux) into a reusable, library-driven placer. The only new
logic vs the Well POC: trim-to-in-point, align the bed's swell to the CTA, duck under the
verbatim KJV quote, and an optional hook-opening bed that crossfades into the CTA-safe
primary. Design + rationale: PLACER.md.

Status: BUILT here; PROVEN at the pilot (needs real Suno audio + the STT gate). Run
`--selfcheck` now (validates wiring/metadata without audio); run the full render at pilot.

  python placer.py --selfcheck --primary sacred_grace_rise_a
  python placer.py --video <clip.mp4> --primary sacred_grace_rise_a \
      [--hook lonely_searching_a] [--layer glory_holy_stillness_a] \
      [--quote "whosoever drinketh"] [--out out.mp4]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
from music_library import MusicLibrary  # noqa: E402

VOICE_TARGET_LUFS = -16.0   # narration sits here; beds are placed UNDER it
BED_UNDER_DB = -20.0        # primary bed gain under the voice (pre-sidechain)
LAYER_UNDER_DB = -26.0      # glory pad even lower
KJV_DUCK_DB = -10.0         # extra dip on the bed across the verbatim quote
WORD_RECOVERY_MIN = 0.98    # pilot acceptance gate


def _approved(lib: MusicLibrary, slug: str | None):
    if not slug:
        return None
    e = lib.by_slug(slug)
    if not e:
        sys.exit(f"[placer] no such track: {slug}")
    if e.status != "approved":
        sys.exit(f"[placer] {slug} is status={e.status} — approve it first (approve.py)")
    return e


def _spoken(script_path: Path | None) -> str:
    if not script_path:
        return ""
    raw = script_path.read_text(encoding="utf-8")
    body = raw.split("----")[0]
    return " ".join(ln.strip() for ln in body.splitlines() if ln.strip())


def _align(wav: Path, script: str):
    from veed_io.aligner import forced_align_script
    return forced_align_script(str(wav), script)


def _cta_time(words: list[dict], script: str) -> float:
    """t_cta = start time of the final sentence (the closing CTA). Robust default."""
    sents = [s for s in re.split(r"(?<=[.!?])\s+", script.strip()) if s.strip()]
    if not sents or not words:
        return words[-1]["start"] if words else 0.0
    n_last = len(re.findall(r"[A-Za-z0-9']+", sents[-1]))
    idx = max(0, len(words) - n_last)
    return float(words[idx]["start"])


def detect_swell(path: Path, win_s: float = 3.0) -> float:
    """Time (s) of peak loudness = the track's swell/climax. Decodes a low-rate mono
    envelope and returns the centre of the loudest `win_s` window (RMS)."""
    import numpy as np
    sr = 1000
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
                          "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32)
    if x.size == 0:
        return 0.0
    p = x * x                                   # power
    w = max(1, int(win_s * sr))
    csum = np.cumsum(np.insert(p, 0, 0.0))
    rms = (csum[w:] - csum[:-w]) / w             # windowed mean power
    i = int(np.argmax(rms))                      # window start index
    return round((i + w / 2) / sr, 1)            # centre time of loudest window


def _bed_dur(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=nw=1:nk=1", str(path)],
                                capture_output=True, text=True).stdout.strip() or 0)


def _quote_span(words: list[dict], quote: str | None):
    """Locate a verbatim quote substring in the aligned words -> (q0, q1) seconds."""
    if not quote:
        return None
    keys = [re.sub(r"[^a-z0-9']", "", w.lower()) for w in quote.split()]
    toks = [re.sub(r"[^a-z0-9']", "", w["w"].lower()) for w in words]
    for i in range(len(toks) - len(keys) + 1):
        if toks[i:i + len(keys)] == keys:
            return float(words[i]["start"]), float(words[i + len(keys) - 1]["end"])
    return None


def selfcheck(lib, primary, hook, layer):
    p = _approved(lib, primary)
    print(f"[selfcheck] primary {primary}: approved, swell_s={p.swell_s}, lufs={p.lufs_i}")
    if p.swell_s is None and p.energy in ("build", "climax", "swell-and-rest"):
        print("  WARNING: arc bed has no swell_s — placer cannot align it to the CTA")
    if hook:
        h = _approved(lib, hook)
        print(f"[selfcheck] hook {hook}: approved (mood={h.mood})")
    if layer:
        ly = _approved(lib, layer)
        if ly.mood != "glory":
            sys.exit(f"[selfcheck] layer {layer} is mood={ly.mood}; only glory_* may layer")
        print(f"[selfcheck] layer {layer}: approved glory pad")
    # prove the reuse chain imports
    from veed_io.aligner import forced_align_script, transcribe_align  # noqa: F401
    print("[selfcheck] reuse chain OK (forced_align_script + transcribe_align import)")
    print("[selfcheck] PASS — wiring is sound; full render needs pilot audio.")


def render(lib, video, script_path, primary, hook, layer, quote, out, cta_override=None,
           ambience=None):
    p = _approved(lib, primary)
    h = _approved(lib, hook)
    ly = _approved(lib, layer)
    work = HERE / "_work"; work.mkdir(exist_ok=True)
    wav = work / "narration16k.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video),
                    "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    script = _spoken(Path(script_path)) if script_path else ""
    words = _align(wav, script) if script else []
    dur = _bed_dur(Path(video))
    bed_dur = _bed_dur(lib.clip_path(primary))
    t_cta = cta_override if cta_override is not None else (_cta_time(words, script) if words else dur * 0.8)
    span = _quote_span(words, quote)
    swell = p.swell_s or 0.0
    # start the bed so its swell (at `swell` into the track) lands at clip time t_cta;
    # clamp into the track so the window exists.
    bed_start = min(max(0.0, swell - t_cta), max(0.0, bed_dur - dur))
    landed = swell - bed_start   # where the swell actually lands in the clip after clamping
    print(f"[placer] clip={dur:.1f}s  bed={bed_dur:.0f}s  t_cta={t_cta:.1f}s  swell@track={swell:.1f}s "
          f" -> bed_start={bed_start:.1f}s  swell lands @ clip {landed:.1f}s  kjv_span={span}")

    # primary bed: trim a clip-length window starting at bed_start, fade, gain, then duck.
    fc = ["[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[voc][vk]"]
    fin = "afade=t=in:st=11:d=3" if h else "afade=t=in:st=0:d=0.5"   # crossfade in after the hook
    pf = (f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
          f"atrim={bed_start}:{bed_start + dur},asetpts=PTS-STARTPTS,"
          f"{fin},afade=t=out:st={dur - 1.5}:d=1.5,volume={BED_UNDER_DB}dB")
    if span:                                     # extra dip across the verbatim quote
        pf += f",volume=enable='between(t,{span[0]},{span[1]})':volume={KJV_DUCK_DB}dB"
    fc.append(pf + "[bed]")
    beds = ["[bed]"]
    inputs = ["-i", str(video), "-i", str(lib.clip_path(primary))]
    nxt = 2
    if h:                                        # optional hook-opening bed, crossfade ~12s
        inputs += ["-i", str(lib.clip_path(hook))]
        fc.append(f"[{nxt}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
                  f"atrim=0:14,afade=t=out:st=11:d=3,volume={BED_UNDER_DB}dB[hook]")
        beds.append("[hook]"); nxt += 1
    if ly:                                        # optional glory pad under the landing
        inputs += ["-i", str(lib.clip_path(layer))]
        ld = max(0.0, t_cta - 2)
        fc.append(f"[{nxt}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
                  f"atrim=0:{dur - ld},adelay={int(ld*1000)}|{int(ld*1000)},"
                  f"afade=t=in:st=0:d=2,volume={LAYER_UNDER_DB}dB[pad]")
        beds.append("[pad]"); nxt += 1
    # optional sound_library ambience beds (water, etc.) — looped to clip length, low + ducked
    sfx_dir = ROOT / "sound_library" / "clips"
    for j, (slug, gain) in enumerate(ambience or []):
        sp = sfx_dir / f"{slug}.mp3"
        if not sp.exists():
            sys.exit(f"[placer] no sound_library clip: {slug} ({sp})")
        inputs += ["-i", str(sp)]
        fc.append(f"[{nxt}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
                  f"aloop=loop=-1:size=2e9,atrim=0:{dur},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:st=0:d=1,afade=t=out:st={dur-1.5}:d=1.5,volume={gain}dB[amb{j}]")
        beds.append(f"[amb{j}]"); nxt += 1
    fc.append("".join(beds) + f"amix=inputs={len(beds)}:normalize=0[bedmix]")
    fc.append("[bedmix][vk]sidechaincompress=threshold=0.05:ratio=6:attack=15:release=350[duck]")
    fc.append("[voc][duck]amix=inputs=2:normalize=0,alimiter=limit=0.95,aresample=44100[mix]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[mix]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"[placer] ffmpeg failed:\n{r.stderr[-1500:]}")
    print(f"[placer] wrote {out}")

    # acceptance gate: STT word-recovery on the muxed audio (intelligibility under music)
    if script:
        gate(out, script)
    lib.note_use(primary, Path(video).parent.name)


def gate(out_mp4: Path, script: str):
    from veed_io.aligner import transcribe_align
    work = HERE / "_work"; gwav = work / "gate16k.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(out_mp4),
                    "-vn", "-ac", "1", "-ar", "16000", str(gwav)], check=True)
    heard = transcribe_align(str(gwav))
    sk = set(re.sub(r"[^a-z0-9']", "", w["w"].lower()) for w in heard)
    want = [re.sub(r"[^a-z0-9']", "", t.lower()) for t in re.findall(r"[A-Za-z0-9']+", script)]
    rec = sum(1 for t in want if t in sk) / max(1, len(want))
    ok = rec >= WORD_RECOVERY_MIN
    print(f"[gate] word-recovery {rec*100:.1f}%  ({'PASS' if ok else 'FAIL'} vs {WORD_RECOVERY_MIN*100:.0f}%)")
    if not ok:
        print("[gate] music is burying the narration — duck harder / pick a sparser bed.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video"); ap.add_argument("--script")
    ap.add_argument("--primary", required=True)
    ap.add_argument("--hook"); ap.add_argument("--layer"); ap.add_argument("--quote")
    ap.add_argument("--out", default=str(HERE / "placer_out.mp4"))
    ap.add_argument("--cta", type=float, default=None, help="override CTA time (s) for swell alignment")
    ap.add_argument("--ambience", default="",
                    help="sound_library SFX beds under the music, e.g. 'river_well_water:-18'")
    ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args()
    lib = MusicLibrary()
    if a.selfcheck:
        selfcheck(lib, a.primary, a.hook, a.layer)
        return
    if not a.video:
        sys.exit("--video required (or use --selfcheck)")
    ambience = []
    for tok in (t.strip() for t in a.ambience.split(",") if t.strip()):
        slug, _, g = tok.partition(":")
        ambience.append((slug, float(g) if g else -19.0))
    render(lib, a.video, a.script, a.primary, a.hook, a.layer, a.quote, Path(a.out), a.cta, ambience)


if __name__ == "__main__":
    main()
