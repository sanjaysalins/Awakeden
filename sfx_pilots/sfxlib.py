"""Shared SFX/ambience mix engine for the finished shorts (Level A: no music, $0).

Reuse-first: every layer pulls a clip from sound_library/clips and is gained to a
target mean dBFS (raw levels vary wildly, so measure-then-gain), then summed,
sidechain-ducked under the narration, and limited. Generalized from the approved
#02 storm pilot.

A layer is a dict:
  label   : str
  slug    : sound_library slug (clip = clips/<slug>.mp3)
  kind    : "loop" | "oneshot"
  start   : seconds into the clip
  length  : seconds
  tgt      : target mean dBFS (gain = tgt - raw_mean[slug])
  filt    : optional extra ffmpeg af chain (e.g. "lowpass=f=1600"), "" for none
  fin/fout: fade-in / fade-out seconds (default 1.0 / 1.5; oneshot fin 0)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LIB = ROOT / "sound_library" / "clips"
RAW_MEAN = {e["slug"]: e["raw_mean_db"]
            for e in json.loads((ROOT / "sound_library" / "index.json").read_text(encoding="utf-8"))}


def layer(label, slug, kind, start, length, tgt, filt="", fin=None, fout=None):
    if fin is None:
        fin = 0.0 if kind == "oneshot" else 1.0
    if fout is None:
        fout = 1.5
    return dict(label=label, slug=slug, kind=kind, start=start, length=length,
                tgt=tgt, filt=filt, fin=fin, fout=fout)


def show_plan(title, layers):
    print(f"\n=== {title} — SFX/ambience (NO music, all REUSE = $0) ===")
    for p in layers:
        if p["slug"] not in RAW_MEAN:
            print(f"  !! {p['slug']} not in sound_library"); continue
        gain = p["tgt"] - RAW_MEAN[p["slug"]]
        print(f"  {p['label']:<10} {p['slug']:<20} {p['kind']:<8} {p['start']:>5.1f}s "
              f"+{p['length']:>4.1f}s  tgt {p['tgt']:>5.1f}dB (gain {gain:+5.1f})")
    print()


def build(src: Path, out: Path, layers, scc="threshold=0.04:ratio=5:attack=15:release=320"):
    inputs = ["-i", str(src)]
    for p in layers:
        inputs += ["-i", str(LIB / f"{p['slug']}.mp3")]

    fc = ["[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[voc][vk]"]
    bed_labels = []
    for idx, p in enumerate(layers, start=1):
        gain = p["tgt"] - RAW_MEAN[p["slug"]]
        ln = p["length"]
        f = f"[{idx}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
        if p["kind"] == "loop":
            f += f",aloop=loop=-1:size=2e9,atrim=0:{ln}"
        else:
            f += f",atrim=0:{ln}"
        if p["filt"]:
            f += f",{p['filt']}"
        f += f",volume={gain}dB"
        if p["fin"] > 0:
            f += f",afade=t=in:st=0:d={p['fin']}"
        if p["fout"] > 0:
            f += f",afade=t=out:st={max(0.0, ln - p['fout'])}:d={p['fout']}"
        if p["start"] > 0:
            ms = int(p["start"] * 1000)
            f += f",adelay={ms}|{ms}"
        out_lbl = f"[L{idx}]"
        fc.append(f + out_lbl)
        bed_labels.append(out_lbl)

    fc.append("".join(bed_labels) + f"amix=inputs={len(bed_labels)}:normalize=0[beds]")
    fc.append(f"[beds][vk]sidechaincompress={scc}[bd]")
    fc.append("[voc][bd]amix=inputs=2:normalize=0,alimiter=limit=0.85:level=disabled,aresample=44100[mix]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", ";".join(fc),
           "-map", "0:v", "-map", "[mix]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"[mix] ffmpeg failed for {out.name}:\n{r.stderr[-1800:]}")
    return out


def measure(path: Path, regions=None):
    """Return (full_mean, full_max) and print region levels if given [(lbl,ss,to)]."""
    def vd(ss=None, to=None):
        cmd = ["ffmpeg", "-hide_banner"]
        if ss is not None:
            cmd += ["-ss", str(ss)]
        if to is not None:
            cmd += ["-to", str(to)]
        cmd += ["-i", str(path), "-af", "volumedetect", "-f", "null", "-"]
        out = subprocess.run(cmd, capture_output=True, text=True).stderr
        mean = mx = None
        for line in out.splitlines():
            if "mean_volume" in line:
                mean = line.split("mean_volume:")[1].strip()
            if "max_volume" in line:
                mx = line.split("max_volume:")[1].strip()
        return mean, mx
    fm, fx = vd()
    print(f"  FULL  mean {fm}  max {fx}")
    for lbl, ss, to in (regions or []):
        m, x = vd(ss, to)
        print(f"  {lbl:<14} mean {m}  max {x}")
