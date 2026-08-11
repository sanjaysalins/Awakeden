"""Loader for the Stationer's case (MEDIUM_SELECTION.md sec.2) -- the
registry of "tipped-in paper medium" prompt recipes for the living-sketchbook
pipeline. Sibling to how style_manifest.json serves the technique-variant
axis, but for the coarser "what OBJECT does this page pretend to be" axis.

Reads `poc_living_sketchbook/_style_identity_bakeoff/medium_manifest.json`,
resolves each entry's `anchor_ref` against `pipeline/medium_anchors.py`, and
exposes a `Medium` per id with a `.prompt(subject)` helper that goes through
`medium_anchors.build_prompt()` -- the only legal way to assemble a medium
prompt, per that module's own docstring.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pipeline import medium_anchors

MANIFEST_PATH = (Path(__file__).resolve().parents[1] / "poc_living_sketchbook"
                  / "_style_identity_bakeoff" / "medium_manifest.json")

HOME = "md_sketch"


@dataclass(frozen=True)
class Medium:
    id: str
    name: str
    anchor_text: str
    figure_mode: str  # figure_forward | distant_marks | artifact_only
    status: str
    entry: dict  # the full manifest record -- anything not promoted to a field lives here

    def prompt(self, subject: str, guardrails: bool = True) -> str:
        """Assemble the final render prompt for one spread's subject text.
        Never hand-concatenate `anchor_text` at a call site -- go through
        this (or medium_anchors.build_prompt directly)."""
        return medium_anchors.build_prompt(self.anchor_text, subject, guardrails=guardrails)


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_mediums(path: Path = MANIFEST_PATH) -> dict[str, Medium]:
    manifest = load_manifest(path)
    out: dict[str, Medium] = {}
    for mid, entry in manifest.items():
        anchor_text = getattr(medium_anchors, entry["anchor_ref"])
        out[mid] = Medium(
            id=mid,
            name=entry["name"],
            anchor_text=anchor_text,
            figure_mode=entry["figure_mode"],
            status=entry["status"],
            entry=entry,
        )
    return out


MEDIUMS = load_mediums()
