"""Seed the sound library with the CORE high-reuse biblical-times sounds.
Reuse-first (skips slugs already present). Measures each clip's real loudness and
registers it as a neutral, reusable entry. Metered ONLY for genuinely-new clips."""
import subprocess
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pipeline.assembly_align import _resolve_key                    # noqa: E402
from sound_library import SoundLibrary, SoundEntry                  # noqa: E402  (module in this dir)

SOUND_URL = "https://api.elevenlabs.io/v1/sound-generation"
TODAY = "2026-06-04"

# slug, category, dur_s, tags, prompt
CORE = [
    ("fire_crackling", "ambience", 18, ["fire","campfire","flames","crackle","hearth","embers"],
     "steady campfire crackling and popping, warm flames, glowing embers shifting, close, no music no voices"),
    ("sea_waves_shore", "ambience", 18, ["sea","waves","shore","water","galilee","lake"],
     "gentle lake water waves lapping on a stony shore, calm open water, distant, no music no voices"),
    ("boat_creak_oars", "ambience", 16, ["boat","wood","oars","rowing","fishing","water"],
     "wooden fishing boat creaking with oars dipping and pulling through water, steady rowing, open water, no music"),
    ("river_well_water", "ambience", 15, ["water","river","well","spring","flowing","stream"],
     "fresh water flowing and trickling from a stone spring into a well, gentle steady stream, no music no voices"),
    ("bread_tearing", "oneshot", 4, ["bread","tear","food","break","meal","crust"],
     "hands tearing a loaf of crusty bread apart, close up, crackling crust, single tear, no music"),
    ("coins_clinking", "oneshot", 4, ["coins","money","metal","silver","clink"],
     "metal coins clinking and spilling onto a wooden table, a handful of silver coins, close, no music"),
    ("shofar_blast", "oneshot", 6, ["shofar","horn","ram","trumpet","announce","festival"],
     "a single long ancient ram's horn shofar blast, resonant and raw, echoing across open land, no music"),
    ("crowd_shout_mob", "ambience", 12, ["crowd","shout","mob","angry","voices","jerusalem"],
     "an angry crowd of people shouting and clamouring, indistinct furious voices, outdoor mob, no music"),
    ("door_gate_creak", "oneshot", 5, ["door","gate","wood","creak","hinge","open"],
     "a heavy wooden door creaking open slowly on old hinges then closing with a thud, close, no music"),
    ("donkey_bray", "oneshot", 4, ["donkey","bray","animal","travel","rural"],
     "a donkey braying, two calls, outdoor rural setting, no music no other voices"),
    ("marketplace_chatter", "ambience", 16, ["market","crowd","town","chatter","bargaining","voices"],
     "busy ancient marketplace ambience, overlapping chatter and bargaining, footsteps and distant animals, no music"),
    ("footsteps_stone", "oneshot", 6, ["footsteps","stone","walking","sandals","interior","courtyard"],
     "sandaled footsteps walking on stone paving, echoing in a stone courtyard, steady pace, no music"),
    ("stone_roll_tomb", "oneshot", 6, ["stone","tomb","roll","grind","rock","resurrection"],
     "a large heavy stone grinding and rolling across a rock tomb entrance, deep scraping echo, no music"),
    ("veil_tearing", "oneshot", 5, ["veil","cloth","tear","rip","fabric","temple"],
     "a heavy thick fabric temple veil tearing and ripping from top to bottom, dramatic, reverberant, no music"),
    ("heavenly_choir_soft", "ambience", 16, ["choir","heavenly","voices","divine","ethereal","holy"],
     "soft ethereal wordless choir, distant angelic voices, gentle holy ambient swell, no percussion no rhythm"),
    ("soldiers_march_armor", "ambience", 12, ["soldiers","march","armor","roman","military","clank"],
     "a rank of Roman soldiers marching in unison on stone, armor and metal clinking, disciplined footsteps, no music"),
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


def main():
    lib = SoundLibrary()
    key = _resolve_key()
    spent = 0
    for slug, cat, dur, tags, prompt in CORE:
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
        path = lib.clip_path(slug)
        path.write_bytes(r.content)
        mean, mx = measure(path)
        credits = int(dur * 40)
        spent += credits
        lib.register(SoundEntry(
            slug=slug, category=cat, tags=tags, prompt=prompt, duration_s=float(dur),
            loopable=(cat == "ambience"), raw_mean_db=round(mean, 1), raw_max_db=round(mx, 1),
            credits_est=credits, reuse_scope="neutral", created=TODAY, used_in=[]))
        print(f"ok (mean {mean:.1f} / max {mx:.1f} dB, ~{credits} cr)")
    print(f"\n[spend] ~{spent} credits this run · library now {len(lib.entries)} clips")


if __name__ == "__main__":
    main()
