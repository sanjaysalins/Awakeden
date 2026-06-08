"""Psalm 22 long-form SOUNDSTAGE — layer SFX/ambience UNDER the locked narration.mp3,
sidechain-ducked under the voice. Audio-only (the film isn't built yet) -> narration.immersive.mp3.

Level A discipline (same as the approved shorts): all clips REUSED from sound_library ($0),
gentle levels (measure-then-gain), the cross's sacred lines kept clear, the bleak crucifixion
half blooming into warmth + the worshipping congregation at THE TURN (Movement 6).

  python longform/_soundstage_ps22.py --plan      # show plan (free)
  python longform/_soundstage_ps22.py --mix       # build narration.immersive.mp3 (free, ffmpeg)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible")
LIB = ROOT / "sound_library" / "clips"
RAW_MEAN = {e["slug"]: e["raw_mean_db"]
            for e in json.loads((ROOT / "sound_library" / "index.json").read_text(encoding="utf-8"))}

V1 = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1"
SRC = V1 / "narration.mp3"
OUT = V1 / "narration.immersive.mp3"
DUR = 418.20


def L(label, slug, kind, start, length, tgt, filt="", fin=None, fout=None):
    if fin is None:
        fin = 0.0 if kind == "oneshot" else 2.0
    if fout is None:
        fout = 2.5
    return dict(label=label, slug=slug, kind=kind, start=start, length=length,
                tgt=tgt, filt=filt, fin=fin, fout=fout)


# ── 7-movement plan (times from alignment.json) ──────────────────────────────
# M1 cry/dark · M2 mockers · M3 wounds (pierced/lots) · M4 honest question (sparse)
# M5 cross again · M6 THE TURN (death->life, warmth+choir+shofar) · M7 finished/landing
PLAN = [
    # ── M1 THE CRY — dark, forsaken (0 - ~60s; cry @10-15, 30)
    L("dark_air",  "air_hollow_desolate", "loop",   0.0,  60.0, -30.0, fin=3.0, fout=5.0),
    L("dread",     "rumble_deep_sub",     "loop",   0.0,  56.0, -34.0, fin=3.0, fout=5.0),
    L("ninth_hr",  "thunder_low_roll",    "oneshot", 5.0,  7.0,  -24.0),     # cried out into the dark
    # ── M2 THE MOCKERS (~60 - ~102s; worm 66, scorn 72, deliver 78)
    L("mockers",   "crowd_shout_mob",     "loop",  60.0,  42.0, -32.0, filt="lowpass=f=2600", fin=3.0, fout=4.0),
    # ── M3 THE WOUNDS (~100 - ~176s): water/joint 103-105, pierced 124.8, lots 147.5
    L("strain",    "rumble_deep_sub",     "loop", 100.0,  76.0, -35.0, fin=3.0, fout=4.0),
    L("crowd3",    "crowd_murmur_distant","loop", 100.0,  76.0, -36.0, fin=3.0, fout=4.0),
    L("pierce",    "nail_strike_single",  "oneshot", 0.0,  3.0,  -22.0),     # they pierced my hands and my feet  (TIME SET BELOW)
    L("lots",      "coins_clinking",      "oneshot", 0.0,  4.0,  -24.0),     # cast lots upon my vesture          (TIME SET BELOW)
    # ── M4 HONEST QUESTION (~176 - ~246s): sparse, reflective — let the argument land
    L("reflect",   "wind_desert_bleak",   "loop", 176.0,  70.0, -38.0, filt="lowpass=f=1600", fin=4.0, fout=5.0),
    # ── M5 CROSS AGAIN (~246 - ~286s): forsaken 256.6, divided 270.8
    L("cross5",    "air_hollow_desolate", "loop", 246.0,  40.0, -34.0, fin=4.0, fout=5.0),
    L("divide",    "coins_clinking",      "oneshot", 0.0,  4.0,  -28.0),     # soldiers divided them up           (TIME SET BELOW)
    # ── M6 THE TURN (~288 - ~355s): death -> life. warmth carries to the end; choir = the worship peak
    L("turn_warm", "dawn_morning_warm",   "loop", 288.0, 130.0, -31.0, filt="lowpass=f=3200", fin=5.0, fout=6.0),
    L("choir",     "heavenly_choir_soft", "loop", 300.0,  78.0, -34.0, fin=6.0, fout=8.0),   # the worshipping congregation (borderline-musical; offer to pull)
    L("nations",   "shofar_blast",        "oneshot", 0.0,  6.0,  -27.0, filt="lowpass=f=2500"),  # all the ends of the world (TIME SET BELOW)
    # ── M7 HE HATH DONE THIS / landing (~355 - 418s): finished, then warm welcome; congregation choir returns
    L("finished",  "veil_tearing",        "oneshot", 0.0,  5.0,  -26.0),     # It is finished                     (TIME SET BELOW)
    L("join",      "heavenly_choir_soft", "loop", 404.0,  14.0, -35.0, fin=4.0, fout=4.0),   # come and join the ones who praise him
]

# anchor times patched in from alignment.json at runtime (word -> layer label)
ANCHOR_FOR = {"pierce": "pierced", "lots": "lots", "divide": "divided",
              "nations": "ends", "finished": "finished"}


def patch_anchor_times():
    words = json.loads((V1 / "alignment.json").read_text(encoding="utf-8"))
    import re

    def time_of(needle, nth=0):
        hits = [w for w in words if re.sub(r"[^a-z]", "", w["w"].lower()) == needle]
        return hits[nth]["start"] if len(hits) > nth else None

    # specific picks (some words repeat; choose the right occurrence by approx window)
    def pick(needle, lo, hi):
        import re as _re
        for w in words:
            if _re.sub(r"[^a-z]", "", w["w"].lower()) == needle and lo <= w["start"] <= hi:
                return w["start"]
        return None

    picks = {
        "pierce": pick("pierced", 92, 163),
        "lots":   pick("lots", 92, 163),
        "divide": pick("divided", 228, 283) or pick("divided", 0, DUR),
        "nations":pick("ends", 283, 360) or pick("ends", 0, DUR),
        "finished": pick("finished", 338, DUR) or pick("finished", 0, DUR),
    }
    for p in PLAN:
        if p["label"] in picks and picks[p["label"]] is not None:
            # start the oneshot slightly before the word so the hit lands ON it
            lead = 0.3 if p["label"] in ("pierce", "lots", "divide", "finished") else 0.0
            p["start"] = max(0.0, picks[p["label"]] - lead)
    return picks


def show_plan():
    picks = patch_anchor_times()
    print("\n=== Psalm 22 long-form SOUNDSTAGE (Level A, all REUSE = $0) ===")
    print(f"  anchored beats: { {k: (round(v,1) if v else None) for k,v in picks.items()} }")
    for p in PLAN:
        if p["slug"] not in RAW_MEAN:
            print(f"  !! {p['slug']} missing"); continue
        gain = p["tgt"] - RAW_MEAN[p["slug"]]
        print(f"  {p['label']:<10} {p['slug']:<20} {p['kind']:<8} {p['start']:>6.1f}s "
              f"+{p['length']:>4.1f}s  tgt {p['tgt']:>5.1f}dB (gain {gain:+5.1f})")
    print()


def mix():
    patch_anchor_times()
    inputs = ["-i", str(SRC)]
    for p in PLAN:
        inputs += ["-i", str(LIB / f"{p['slug']}.mp3")]

    fc = ["[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[voc][vk]"]
    beds = []
    for idx, p in enumerate(PLAN, start=1):
        gain = p["tgt"] - RAW_MEAN[p["slug"]]
        ln = p["length"]
        f = f"[{idx}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
        f += f",aloop=loop=-1:size=2e9,atrim=0:{ln}" if p["kind"] == "loop" else f",atrim=0:{ln}"
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
        fc.append(f + f"[L{idx}]")
        beds.append(f"[L{idx}]")

    fc.append("".join(beds) + f"amix=inputs={len(beds)}:normalize=0[beds]")
    fc.append("[beds][vk]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=350[bd]")
    fc.append("[voc][bd]amix=inputs=2:normalize=0,alimiter=limit=0.85:level=disabled,aresample=44100[mix]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", ";".join(fc), "-map", "[mix]",
           "-c:a", "libmp3lame", "-q:a", "2", str(OUT)]
    print("[mix] building Psalm 22 soundstage ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"[mix] ffmpeg failed:\n{r.stderr[-2000:]}")
    print(f"[mix] ok -> {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--mix", action="store_true")
    a = ap.parse_args()
    if not (a.plan or a.mix):
        a.plan = True
    if a.plan:
        show_plan()
    if a.mix:
        mix()
