"""Minimal episode spec for Swirls ep12 (Ye Are Not All Clean, v3 retro cut). This episode was
built outside episode.py (v3_retro/ + Remotion); the publish/thumbnail engine only reads
FRONT_COVER.title / .subtitle from here. front_cover.png = v3_retro/pages/p11.png (the towel)."""
from types import SimpleNamespace
FRONT_COVER = SimpleNamespace(title="Holding the Towel", subtitle="John 13")

# Tracker shim: swirls_upload_tracker.py reads MANIFEST.scores[*].out for the final (pre-SFX)
# cut (a hard link to v3_retro/EP12_REMOTION_v1.mp4) and pins its _sfx sibling
# (swirls_episode_12_ye_are_not_all_clean_v3_final_sfx.mp4) in FINAL_VIDEO.txt.
from pathlib import Path as _P
MANIFEST = SimpleNamespace(scores={"owner_arpeggiated_ostinato": SimpleNamespace(
    out=_P(__file__).resolve().parent / "swirls_episode_12_ye_are_not_all_clean_v3_final.mp4")})
