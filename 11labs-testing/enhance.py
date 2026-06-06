"""11labs-testing — enhance the Well (John 4) viral_cut with an ElevenLabs music
bed + event-timed SFX, layered UNDER the existing narration.

Independent test. Reuse-first: the well-trickle + holy-choir beds already live in
sound_library (so they cost $0). The only METERED calls are:
  * Eleven Music  -> a ~59s reverent instrumental score   (--generate)
  * 1 new SFX     -> clay waterpot set-down + run-off       (--generate)

Steps:
  python enhance.py --plan        # show the layer plan (free)
  python enhance.py --generate    # METERED: make music + new sfx (gated, --yes)
  python enhance.py --mix         # build viral_cut_enhanced.mp4 (free, local ffmpeg)

Balance is read from /v1/user/subscription before+after generation so the EXACT
credit spend is reported (the boldest-colour rule).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

SRC_VIDEO = Path(r"G:\My Drive\0 Personal\0Company\jobs\0salinss\saltandlightkingdom"
                 r"\0 Christianity\0 People Who Encountered Jesus"
                 r"\08 The Well That Never Runs Dry\viral_cut.mp4")

LIB_CLIPS = ROOT / "sound_library" / "clips"
LAYERS = HERE / "layers"
WORK = HERE / "work"
OUT = HERE / "viral_cut_enhanced.mp4"
AB = HERE / "AB_original_vs_enhanced.mp4"

DUR = 59.0
RED = "\033[1;91m"
RST = "\033[0m"

MUSIC_PROMPT = (
    "A reverent, cinematic instrumental score for a sacred biblical short film about "
    "the woman at the well meeting Jesus. Slow, tender, hopeful. Warm sustained strings "
    "and soft piano over a gentle Middle-Eastern hint (duduk / oud), light shimmering "
    "pads. Begins intimate and searching, swells to a warm, redemptive, full-hearted "
    "climax of grace at the end. No percussion-driven beat, no drums, no vocals. "
    "Peaceful, holy, emotional, film-trailer underscore."
)

WATERPOT_PROMPT = (
    "a heavy clay water jar set down hastily on stone with a hollow ceramic thunk and a "
    "little water sloshing, then quick sandaled footsteps running away on dirt, close, no music no voices"
)

# layer plan: (label, source, kind, start_s, length_s, gain_db, extra)
#   reuse clips are pulled from sound_library; music/waterpot are generated here.
PLAN = [
    ("music",   "GEN:music.mp3",          "bed-full",   0.0,  DUR,  -17.0, "full-length score, ducked under voice"),
    ("well",    "river_well_water.mp3",   "bed-loop",   0.0,  DUR,  -20.0, "well-water trickle (REUSE) — we're at the well throughout"),
    ("village", "marketplace_chatter.mp3","bed-fade",   0.0,  11.0, -30.0, "faint noon village 'whispers' (REUSE), fades by ~10s"),
    ("waterpot","GEN:waterpot.mp3",       "oneshot",   37.8,   4.0,  -6.0, "jar drop + run-off @ 'she dropped her waterpot and ran' (38.08s)"),
    ("choir",   "heavenly_choir_soft.mp3","swell",     47.0,  12.0, -22.0, "holy choir swell (REUSE) under the gospel landing 'He still offers it'"),
]

MUSIC_URL = "https://api.elevenlabs.io/v1/music"
SFX_URL = "https://api.elevenlabs.io/v1/sound-generation"
SUB_URL = "https://api.elevenlabs.io/v1/user/subscription"


def credits_left(key: str) -> int | None:
    try:
        r = requests.get(SUB_URL, headers={"xi-api-key": key}, timeout=30)
        if r.status_code == 200:
            d = r.json()
            return int(d["character_limit"]) - int(d["character_count"])
    except Exception as e:
        print(f"  (balance check failed: {e})")
    return None


def show_plan():
    print("\n=== LAYER PLAN — Well / John 4 (under existing narration) ===")
    for label, src, kind, start, length, gain, note in PLAN:
        tag = "GEN " if src.startswith("GEN:") else "REUSE"
        print(f"  [{tag}] {label:<9} {kind:<9} {start:>5.1f}s +{length:>4.1f}s  {gain:>6.1f}dB  {note}")
    print("\n  REUSE = $0 (already in sound_library). GEN = metered ElevenLabs.")
    print(f"  metered this run: Eleven Music (~{int(DUR)}s) + 1 SFX (~4s)\n")


def generate(key: str, yes: bool):
    LAYERS.mkdir(exist_ok=True)
    before = credits_left(key)
    if before is not None:
        print(f"  credits available before: {before:,}")
    if not yes:
        print(f"\n{RED}>>> METERED RUN. Re-run with --yes to authorize ElevenLabs generation. <<<{RST}\n")
        return

    # 1) Eleven Music — instrumental score
    mpath = LAYERS / "music.mp3"
    if mpath.exists():
        print(f"[music] exists, skip {mpath.name}")
    else:
        print(f"[music] composing ~{int(DUR)}s instrumental score ...", flush=True)
        r = requests.post(MUSIC_URL,
                          headers={"xi-api-key": key, "Content-Type": "application/json",
                                   "Accept": "audio/mpeg"},
                          json={"prompt": MUSIC_PROMPT,
                                "music_length_ms": int(DUR * 1000),
                                "force_instrumental": True,
                                "model_id": "music_v1"},
                          timeout=300)
        if r.status_code != 200:
            print(f"{RED}[music] FAILED [{r.status_code}]: {r.text[:300]}{RST}")
            # music_generation scope is enabled (2026-06-06); a 401 here means it was revoked
            print("[music] continuing without music — check key scopes then re-run --generate")
        else:
            mpath.write_bytes(r.content)
            print(f"[music] ok -> {mpath}")

    # 2) waterpot SFX
    wpath = LAYERS / "waterpot.mp3"
    if wpath.exists():
        print(f"[sfx ] exists, skip {wpath.name}")
    else:
        print("[sfx ] generating waterpot drop + run-off ...", flush=True)
        r = requests.post(SFX_URL,
                          headers={"xi-api-key": key, "Content-Type": "application/json",
                                   "Accept": "audio/mpeg"},
                          json={"text": WATERPOT_PROMPT, "duration_seconds": 4.0,
                                "prompt_influence": 0.45},
                          timeout=180)
        if r.status_code != 200:
            sys.exit(f"[sfx ] failed [{r.status_code}]: {r.text[:400]}")
        wpath.write_bytes(r.content)
        print(f"[sfx ] ok -> {wpath}")

    after = credits_left(key)
    if before is not None and after is not None:
        print(f"\n{RED}>>> ACTUAL SPEND: {before - after:,} credits  ({before:,} -> {after:,}) <<<{RST}\n")


def _src_path(src: str) -> Path:
    if src.startswith("GEN:"):
        return LAYERS / src[4:]
    return LIB_CLIPS / src


def mix(drop=None):
    drop = set(drop or [])
    # use whatever layers are present; skip missing GEN layers + any --drop'd labels
    active = [row for row in PLAN if _src_path(row[1]).exists() and row[0] not in drop]
    skipped = [row[0] for row in PLAN
               if not _src_path(row[1]).exists() or row[0] in drop]
    if skipped:
        print(f"[mix] skipping layers: {skipped}")

    inputs = ["-i", str(SRC_VIDEO)]                       # [0] = video+narration
    for _, src, *_ in active:
        inputs += ["-i", str(_src_path(src))]

    fc = []
    # voice: stereo 44.1k; split into output + sidechain key
    fc.append("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
              "asplit=2[voc][vk]")

    bed_labels = []
    for idx, (label, src, kind, start, length, gain, _) in enumerate(active, start=1):
        a = f"[{idx}:a]"
        f = (f"{a}aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100")
        if kind == "bed-loop":
            f += f",aloop=loop=-1:size=2e9,atrim=0:{length}"
        elif kind in ("bed-full",):
            f += f",atrim=0:{length}"
        elif kind == "bed-fade":
            f += f",atrim=0:{length},afade=t=out:st={length-3}:d=3"
        elif kind == "swell":
            f += f",atrim=0:{length},afade=t=in:st=0:d=3,afade=t=out:st={length-2}:d=2"
        elif kind == "oneshot":
            f += f",atrim=0:{length}"
        f += f",volume={gain}dB"
        if start > 0:
            f += f",adelay={int(start*1000)}|{int(start*1000)}"
        out = f"[L{idx}]"
        fc.append(f + out)
        bed_labels.append(out)

    # sum beds -> duck under voice (sidechain) -> mix with voice
    fc.append("".join(bed_labels) + f"amix=inputs={len(bed_labels)}:normalize=0[beds]")
    fc.append("[beds][vk]sidechaincompress=threshold=0.05:ratio=6:attack=15:release=350[bedsduck]")
    fc.append("[voc][bedsduck]amix=inputs=2:normalize=0,"
              "alimiter=limit=0.95,aresample=44100[mix]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", ";".join(fc),
           "-map", "0:v", "-map", "[mix]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-shortest", str(OUT)]
    print("[mix] building enhanced cut ...")
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"[mix] ffmpeg failed:\n{p.stderr[-1500:]}")
    print(f"[mix] ok -> {OUT}")

    # side-by-side A/B (original left, enhanced right) for review
    ab = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
          "-i", str(SRC_VIDEO), "-i", str(OUT),
          "-filter_complex",
          "[0:v]scale=540:960,drawtext=text='ORIGINAL':x=20:y=20:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.5[l];"
          "[1:v]scale=540:960,drawtext=text='ENHANCED':x=20:y=20:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.5[r];"
          "[l][r]hstack=inputs=2[v];[1:a]anull[a]",
          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20",
          "-c:a", "aac", "-b:a", "192k", "-shortest", str(AB)]
    p2 = subprocess.run(ab, capture_output=True, text=True)
    if p2.returncode == 0:
        print(f"[mix] A/B -> {AB}")
    else:
        print(f"[mix] A/B skipped: {p2.stderr[-400:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--mix", action="store_true")
    ap.add_argument("--drop", default="", help="comma layer labels to exclude from the mix (e.g. choir)")
    ap.add_argument("--yes", action="store_true", help="authorize metered generation")
    args = ap.parse_args()

    if not any([args.plan, args.generate, args.mix]):
        args.plan = True

    if args.plan:
        show_plan()
    if args.generate:
        key = _resolve_key()
        if not key:
            sys.exit("ELEVENLABS_API_KEY not found")
        generate(key, args.yes)
    if args.mix:
        mix(drop=[s.strip() for s in args.drop.split(",") if s.strip()])


if __name__ == "__main__":
    main()
