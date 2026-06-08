"""Pilot: layer SFX + ambience UNDER the finished #02 'Why Are You Afraid' viral_cut.

Level A (NO music) — atmosphere only, all clips REUSED from sound_library ($0).

Storm rages, then OBEYS. Forced-aligned: "...the wind and sea obeyed Him"
('obeyed' 30.82-31.12s). Design:
  * storm layers fade out by ~31.2s (the command)
  * a short HELD SILENCE (~31.2-32.6s) = the awe of sudden calm
  * then a GENTLER, DIFFERENT calm: muffled (low-passed) distant water + soft warm
    dawn air rising in slowly = the storm really died, peace returns.
Overall pulled ~4 dB quieter than the first pilot (user: 'a bit too loud').

  python sfx_pilots/enhance_storm02.py --plan     # show plan (free)
  python sfx_pilots/enhance_storm02.py --mix      # build enhanced cut (free, ffmpeg)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LIB = ROOT / "sound_library" / "clips"
INDEX = json.loads((ROOT / "sound_library" / "index.json").read_text(encoding="utf-8"))
RAW_MEAN = {e["slug"]: e["raw_mean_db"] for e in INDEX}

SRC = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\02 Why are you afraid\v3\assembly\viral_cut.mp4")
OUT = HERE / "02_storm_enhanced.mp4"

DUR = 53.022
STORM_OUT = 31.2          # storm obeys here ("obeyed" 30.82-31.12)
STORM_FADE = 1.6
CALM_START = 32.6         # after a ~1.4s held silence

# each layer is a dict:
#   label, slug, kind(storm-loop|calm-loop|oneshot), start, length, target_mean_db, filt, note
PLAN = [
    dict(label="waves",   slug="sea_waves_shore",   kind="storm-loop", start=0.0,  length=STORM_OUT,        tgt=-28.0, filt="", note="storm sea, present but underneath"),
    dict(label="wind",    slug="wind_desert_bleak", kind="storm-loop", start=0.0,  length=STORM_OUT,        tgt=-29.0, filt="", note="the wind that obeys"),
    dict(label="rumble",  slug="rumble_deep_sub",   kind="storm-loop", start=0.0,  length=STORM_OUT,        tgt=-35.0, filt="", note="low dread, far under"),
    dict(label="boat",    slug="boat_creak_oars",   kind="storm-loop", start=2.0,  length=STORM_OUT-2.0,    tgt=-37.0, filt="", note="faint boat creak"),
    dict(label="thunder1",slug="thunder_low_roll",  kind="oneshot",    start=0.5,  length=7.0,              tgt=-23.0, filt="", note="hit on 'drowning' (0.93s)"),
    dict(label="thunder2",slug="thunder_low_roll",  kind="oneshot",    start=11.3, length=7.0,              tgt=-25.0, filt="", note="hit on 'storm was loud' (~12.2s)"),
    # --- calm: different + gentle ---
    dict(label="calmwtr", slug="sea_waves_shore",   kind="calm-loop",  start=CALM_START, length=DUR-CALM_START, tgt=-36.0, filt="lowpass=f=1600", note="muffled distant water = stillness (low-passed)"),
    dict(label="calmair", slug="dawn_morning_warm", kind="calm-loop",  start=CALM_START+0.6, length=DUR-CALM_START-0.6, tgt=-34.0, filt="lowpass=f=3200", note="soft warm dawn air = peace returns"),
]


def show_plan():
    print("\n=== #02 Why Are You Afraid — SFX/ambience (NO music, all REUSE = $0) ===")
    for p in PLAN:
        gain = p["tgt"] - RAW_MEAN[p["slug"]]
        print(f"  {p['label']:<9} {p['slug']:<18} {p['kind']:<10} {p['start']:>5.1f}s +{p['length']:>4.1f}s  "
              f"tgt {p['tgt']:>5.1f}dB (gain {gain:+5.1f})  {p['note']}")
    print(f"\n  storm fades out by ~{STORM_OUT}s -> ~1.4s held silence -> gentle calm from {CALM_START}s.\n")


def mix():
    inputs = ["-i", str(SRC)]
    for p in PLAN:
        inputs += ["-i", str(LIB / f"{p['slug']}.mp3")]

    fc = ["[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[voc][vk]"]
    bed_labels = []
    for idx, p in enumerate(PLAN, start=1):
        gain = p["tgt"] - RAW_MEAN[p["slug"]]
        length = p["length"]
        f = f"[{idx}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
        if p["kind"] in ("storm-loop", "calm-loop"):
            f += f",aloop=loop=-1:size=2e9,atrim=0:{length}"
        else:
            f += f",atrim=0:{length}"
        if p["filt"]:
            f += f",{p['filt']}"
        f += f",volume={gain}dB"
        if p["kind"] == "storm-loop":
            f += f",afade=t=in:st=0:d=1.5,afade=t=out:st={length-STORM_FADE}:d={STORM_FADE}"
        elif p["kind"] == "calm-loop":
            f += f",afade=t=in:st=0:d=3.0,afade=t=out:st={length-2}:d=2.0"
        elif p["kind"] == "oneshot":
            f += f",afade=t=out:st={length-2}:d=2.0"
        if p["start"] > 0:
            f += f",adelay={int(p['start']*1000)}|{int(p['start']*1000)}"
        out = f"[L{idx}]"
        fc.append(f + out)
        bed_labels.append(out)

    fc.append("".join(bed_labels) + f"amix=inputs={len(bed_labels)}:normalize=0[beds]")
    # gentler duck + lower overall bed level
    fc.append("[beds][vk]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=320[bd]")
    fc.append("[voc][bd]amix=inputs=2:normalize=0,alimiter=limit=0.95,aresample=44100[mix]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", ";".join(fc),
           "-map", "0:v", "-map", "[mix]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)]
    print("[mix] building enhanced storm cut ...")
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"[mix] ffmpeg failed:\n{p.stderr[-1800:]}")
    print(f"[mix] ok -> {OUT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--mix", action="store_true")
    args = ap.parse_args()
    if not (args.plan or args.mix):
        args.plan = True
    if args.plan:
        show_plan()
    if args.mix:
        mix()


if __name__ == "__main__":
    main()
