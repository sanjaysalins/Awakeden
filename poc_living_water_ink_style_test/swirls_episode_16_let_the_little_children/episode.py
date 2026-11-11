"""Minimal episode spec for Swirls ep16 (Let the Little Children, Mark 10:13-16, v3 cut).
Built outside swirls_episode.py (build_v3.py + Remotion Ep16ChildrenV2 + felt-piano score);
the publish/thumbnail engine reads FRONT_COVER, the tracker reads MANIFEST.scores[*].out.
LOCKED by owner 2026-11-11 ("its beautiful, lock it"). front_cover.png = the owner's own still."""
from pathlib import Path as _P
from types import SimpleNamespace
FRONT_COVER = SimpleNamespace(title="Jesus Held the Children", subtitle="Mark 10:13-16")
MANIFEST = SimpleNamespace(scores={"felt_piano": SimpleNamespace(
    out=_P(__file__).resolve().parent / "swirls_episode_16_let_the_little_children_v3_final.mp4")})
