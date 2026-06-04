"""Isaiah 53 — FULL cinematic soundstage build.

- Sources sounds from the shared sound_library (reuse-first; generates only gaps).
- Generates new clips into the library (tagged, reusable across episodes).
- Measures each clip's real loudness, then computes per-clip gain to hit a target
  level (so nothing is silent or buried — the trap we hit on the first pass).
- Layered, crossfaded, sidechain-ducked ffmpeg mix -> narration.immersive_cinematic.mp3
Metered ONLY when a clip is missing from the library. Re-runs are free.
"""
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key            # noqa: E402
from sound_library.sound_library import SoundLibrary, SoundEntry  # noqa: E402

V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
EPISODE = "longform/01_Isaiah_53_Suffering_Servant"
SOUND_URL = "https://api.elevenlabs.io/v1/sound-generation"
TODAY = "2026-06-04"

# ---- catalogue of clips this episode needs (library slugs) -------------------
# role: "bed" (looped, ducked, target MEAN) | "shot" (one-shot, target MAX)
CLIPS = [
    # slug, role, gen_dur, tags, prompt
    ("air_hollow_desolate", "bed", 22, ["air","hollow","desolate","bleak","ambient","drone"],
     "low hollow desolate wind and empty air, bleak and still, cavernous lonely atmosphere, dark ambient room tone, no music no voices"),
    ("crowd_murmur_distant", "bed", 14, ["crowd","murmur","voices","jeering","distant","people"],
     "distant murmuring crowd of people, faint muttering and jeering far away, outdoor, indistinct voices, no music"),
    ("impact_low_boom", "shot", 4, ["impact","boom","sub","hit","cinematic","ominous"],
     "one deep cinematic low boom impact, dark sub hit, single ominous thud, reverberant, no music"),
    ("flock_sheep_field", "bed", 18, ["sheep","flock","field","pastoral","animals","bleating"],
     "small flock of sheep bleating softly in an open field, gentle, distant, calm pastoral ambience, no music"),
    ("chariot_wheels_road", "bed", 20, ["chariot","cart","wheels","wood","road","travel"],
     "wooden cart wheels rolling on a dry dirt road, creaking wood, steady travel, open air, no music"),
    ("horse_hooves_walk", "bed", 18, ["horse","hooves","walk","road","travel","animal"],
     "single horse hooves walking steadily on dry dirt road, clip clop, calm pace, outdoor, no music"),
    ("footsteps_dirt_approach", "shot", 4, ["footsteps","walking","dirt","approach","steps"],
     "footsteps walking on dry dirt and gravel approaching, a few steps, outdoor, no music"),
    ("thunder_low_roll", "shot", 7, ["thunder","rumble","storm","sky","ominous"],
     "one long low distant thunder roll, deep rumble rolling away, ominous, no rain, no music"),
    ("rumble_deep_sub", "bed", 20, ["rumble","sub","drone","low","tension","dark"],
     "deep sustained low sub rumble, dark ominous drone tone, heavy tension atmosphere, continuous, no melody no music"),
    ("dawn_morning_warm", "bed", 22, ["dawn","morning","birds","birdsong","warm","hope","peaceful"],
     "gentle dawn ambience, distant birdsong, soft warm morning air, peaceful hopeful stillness, no music"),
]

# ---- placement plan (absolute seconds on the 476.5s timeline) ----------------
# beds:  (slug, start, end, fade_in, fade_out, target_mean_db)
# NOTE: absolute times are on the v3 RE-LOCKED audio (482.9s; KJV + editorial re-render
# 2026-06-04). Re-derive via longform/_pilot_cue_times.py if the audio is re-rendered again.
BEDS = [
    ("wind_desert_bleak",     0,  47, 2, 4, -29),
    ("air_hollow_desolate",  53, 289, 4, 8, -32),
    ("crowd_murmur_distant", 71,  86, 3, 4, -30),
    ("rumble_deep_sub",     112, 142, 3, 6, -30),   # exchange weight (nail @117.5)
    ("flock_sheep_field",   174, 198, 2, 4, -28),
    ("chariot_wheels_road", 285, 340, 2, 5, -26),
    ("horse_hooves_walk",   287, 337, 2, 5, -29),
    ("rumble_deep_sub",     337, 368, 2, 6, -28),   # "it pleased the LORD" weight
    ("dawn_morning_warm",   364, 482, 4, 8, -28),
    ("heavenly_choir_soft", 369, 482, 6, 9, -33),   # library: holy swell on the
                                                     # resurrection turn -> "His name is Jesus"
]
# shots: (slug, anchor_s, target_max_db)
SHOTS = [
    ("impact_low_boom",          60.4, -7),    # "his visage was so marred"
    ("nail_strike_single",      117.5, -9),    # "wounded for our transgressions"
    ("footsteps_dirt_approach", 298.3, -12),   # Philip approaches the chariot
    ("thunder_low_roll",        339.2, -6),    # "Yet it pleased the LORD to bruise him"
]


def measure(path: Path) -> tuple[float, float]:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path),
                          "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mean = mx = -60.0
    for line in out.splitlines():
        if "mean_volume:" in line:
            mean = float(line.split("mean_volume:")[1].split("dB")[0])
        elif "max_volume:" in line:
            mx = float(line.split("max_volume:")[1].split("dB")[0])
    return mean, mx


def ensure_clips(lib: SoundLibrary):
    key = _resolve_key()
    spent = 0
    for slug, role, dur, tags, prompt in CLIPS:
        if lib.by_slug(slug):
            print(f"[lib  ] reuse {slug}")
            continue
        if not key:
            sys.exit("ELEVENLABS_API_KEY not found")
        print(f"[gen  ] {slug} ({dur}s) ...", end=" ", flush=True)
        r = requests.post(SOUND_URL,
                          headers={"xi-api-key": key, "Content-Type": "application/json",
                                   "Accept": "audio/mpeg"},
                          json={"text": prompt, "duration_seconds": float(dur),
                                "prompt_influence": 0.4}, timeout=180)
        if r.status_code != 200:
            sys.exit(f"\nfailed [{r.status_code}]: {r.text[:300]}")
        tmp = lib.clip_path(slug)
        tmp.write_bytes(r.content)
        mean, mx = measure(tmp)
        credits = int(dur * 40)
        spent += credits
        lib.register(SoundEntry(
            slug=slug, category=("ambience" if role == "bed" else "oneshot"),
            tags=tags, prompt=prompt, duration_s=float(dur), loopable=(role == "bed"),
            raw_mean_db=round(mean, 1), raw_max_db=round(mx, 1), credits_est=credits,
            reuse_scope="neutral", created=TODAY, used_in=[EPISODE]))
        print(f"ok (mean {mean:.1f} / max {mx:.1f} dB, ~{credits} cr)")
    for slug, *_ in BEDS + SHOTS:
        lib.note_use(slug, EPISODE)
    if spent:
        print(f"[spend] ~{spent} credits this run")


def clamp(v, lo=-40, hi=30):
    return max(lo, min(hi, v))


# "Foreground" sounds = human voices (crowd/chatter/choir) AND distinct animal CALLS
# (a sheep bleat / donkey bray grabs the ear like a voice). These compete with the
# narration, so they: (1) skip the FULL-mode bed_boost, (2) get an extra cut, and
# (3) duck deeper/faster (drop under speech, fill only the gaps). Atmospheric beds
# (wind/fire/water/rumble) and rhythmic travel (hooves/cart) are left at full presence.
# Reusable across episodes. User direction 2026-06-04 (crowd, then lambs too loud).
VOICED_TAGS = {"voices", "voice", "murmur", "chatter", "crowd", "choir",
               "shout", "mob", "singing", "jeering", "people", "wailing"}
ANIMAL_CALL_TAGS = {"sheep", "bleating", "goat", "goats", "donkey", "bray",
                    "rooster", "crowing", "dog", "dogs", "barking", "cattle", "lowing"}
FOREGROUND_TAGS = VOICED_TAGS | ANIMAL_CALL_TAGS
FOREGROUND_EXTRA_DB = -7         # extra attenuation on top of the bed target
FOREGROUND_DUCK = (0.02, 6, 200) # (threshold, ratio, release) — deeper/faster than other beds


def is_foreground(entry) -> bool:
    return bool(set(t.lower() for t in entry.tags) & FOREGROUND_TAGS)


def _bed_chain(parts, inputs, idx, lib, n, spec, bed_boost, extra_db=0.0):
    slug, start, end, fi, fo, tgt_mean = spec
    e = lib.by_slug(slug)
    gain = clamp((tgt_mean + bed_boost + extra_db) - (e.raw_mean_db or -25))
    dur = end - start
    inputs += ["-stream_loop", "-1", "-i", str(lib.clip_path(slug))]
    lbl = f"b{n}"
    parts.append(
        f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,"
        f"atrim=0:{dur},afade=t=in:st=0:d={fi},afade=t=out:st={dur-fo}:d={fo},"
        f"volume={gain:.1f}dB,adelay={int(start*1000)}|{int(start*1000)}[{lbl}];")
    return f"[{lbl}]"


def build(lib: SoundLibrary, out_name: str, bed_boost: float,
          duck_thresh: float, duck_ratio: float, duck_release: int):
    voice = V1 / "narration.mp3"
    inputs = ["-i", str(voice)]            # index 0
    parts = ["[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=3[v][key][key2];"]
    plain_labels, fg_labels = [], []
    idx = 1
    for n, spec in enumerate(BEDS):
        e = lib.by_slug(spec[0])
        if is_foreground(e):
            # foreground (voices / animal calls): NO bed_boost + extra cut
            fg_labels.append(_bed_chain(parts, inputs, idx, lib, n, spec, 0.0, FOREGROUND_EXTRA_DB))
        else:
            plain_labels.append(_bed_chain(parts, inputs, idx, lib, n, spec, bed_boost))
        idx += 1

    # plain beds: normal duck under the voice
    parts.append("".join(plain_labels) +
                 f"amix=inputs={len(plain_labels)}:normalize=0:duration=longest[plainmix];")
    parts.append(f"[plainmix][key]sidechaincompress=threshold={duck_thresh}:ratio={duck_ratio}:"
                 f"attack=5:release={duck_release}[plainbeds];")
    # foreground beds: deeper/faster duck so they never sit on top of the narration
    vt, vr, vrel = FOREGROUND_DUCK
    parts.append("".join(fg_labels) +
                 f"amix=inputs={len(fg_labels)}:normalize=0:duration=longest[fgmix];")
    parts.append(f"[fgmix][key2]sidechaincompress=threshold={vt}:ratio={vr}:"
                 f"attack=2:release={vrel}[fgbeds];")

    shot_labels = []
    for n, (slug, anchor, tgt_max) in enumerate(SHOTS):
        e = lib.by_slug(slug)
        gain = clamp(tgt_max - (e.raw_max_db or -8))
        inputs += ["-i", str(lib.clip_path(slug))]
        lbl = f"s{n}"
        parts.append(
            f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,"
            f"volume={gain:.1f}dB,adelay={int(anchor*1000)}|{int(anchor*1000)}[{lbl}];")
        shot_labels.append(f"[{lbl}]")
        idx += 1
    parts.append("".join(shot_labels) +
                 f"amix=inputs={len(shot_labels)}:normalize=0:duration=longest[shots];")
    parts.append("[v][plainbeds][fgbeds][shots]amix=inputs=4:normalize=0:duration=first[mix];")
    parts.append("[mix]alimiter=limit=0.95:level=disabled[out]")

    fc = "".join(parts)
    out = V1 / out_name
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", fc,
           "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", str(out)]
    print(f"[mix  ] {len(BEDS)} beds + {len(SHOTS)} shots (bed_boost {bed_boost:+}dB) -> {out.name}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{res.stderr[-1800:]}")
    print(f"[done ] {out}")


if __name__ == "__main__":
    lib = SoundLibrary()
    ensure_clips(lib)
    # balanced: beds sit under the voice, fill the gaps
    build(lib, "narration.immersive_cinematic.mp3", bed_boost=0,
          duck_thresh=0.04, duck_ratio=4, duck_release=300)
    # full: beds louder + lighter ducking so they stay present under the words
    build(lib, "narration.immersive_cinematic_full.mp3", bed_boost=6,
          duck_thresh=0.08, duck_ratio=2.5, duck_release=350)
