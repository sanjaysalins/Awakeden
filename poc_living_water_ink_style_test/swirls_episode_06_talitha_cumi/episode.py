"""Minimal episode spec for Swirls ep6 (Talitha Cumi, vector-style POC). This episode was built
outside episode.py (style_poc_vector/ + Remotion); the publish/thumbnail engine only reads
FRONT_COVER.title / .subtitle from here."""
from types import SimpleNamespace
FRONT_COVER = SimpleNamespace(title="Little Girl, Get Up", subtitle="Mark 5:35-43")

# Tracker shim: swirls_upload_tracker.py reads MANIFEST.scores[*].out for the final (pre-SFX)
# cut and pins its _sfx sibling (swirls_episode_06_talitha_cumi_final_sfx.mp4) in FINAL_VIDEO.txt.
from pathlib import Path as _P
MANIFEST = SimpleNamespace(scores={"piano_ep7_reuse": SimpleNamespace(
    out=_P(__file__).resolve().parent / "swirls_episode_06_talitha_cumi_final.mp4")})
