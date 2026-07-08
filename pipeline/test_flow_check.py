"""flow_check tests (P2-3, 2026-07-08): the deterministic morph pre-filter must
auto-PASS a pure camera move and ESCALATE a dissolve-morph. Fail-open contract:
anything ambiguous escalates to the vision layer; a PASS must be bulletproof.

Builds tiny synthetic clips with ffmpeg (hermetic — no repo media needed).
Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_flow_check.py
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from pipeline import flow_check as FC


@pytest.fixture(scope="module")
def clips():
    """One clean zoom clip + one dissolve-morph clip over detailed synthetic art."""
    d = Path(tempfile.mkdtemp())
    rng = np.random.default_rng(7)

    def art(seed):
        r = np.random.default_rng(seed)
        img = np.zeros((480, 270), dtype=np.uint8) + 235
        for _ in range(60):  # inked-line-ish strokes
            x, y = r.integers(10, 260), r.integers(10, 470)
            w, h = r.integers(5, 60), r.integers(2, 6)
            img[y:y + h, x:x + w] = r.integers(0, 80)
        return img

    a, b = d / "a.png", d / "b.png"
    Image.fromarray(art(1)).save(a)
    Image.fromarray(art(2)).save(b)
    zoom, morph = d / "zoom.mp4", d / "morph.mp4"
    # zoompan at target res jitters (integer quantization); render the pan at 4x
    # then downscale so the camera move is smooth like a real Kling push-in
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", "3",
                    "-i", str(a),
                    "-vf", "scale=1080:1920,setsar=1,"
                           "zoompan=z='1+0.25*on/72':x='iw/2-(iw/zoom/2)':"
                           "y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=24,scale=270:480",
                    "-t", "3", "-pix_fmt", "yuv420p", str(zoom)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-loop", "1", "-t", "3", "-i", str(a),
                    "-loop", "1", "-t", "3", "-i", str(b),
                    "-filter_complex",
                    "[0:v]scale=270:480,setsar=1[x];[1:v]scale=270:480,setsar=1[y];"
                    "[x][y]xfade=transition=dissolve:duration=2.4:offset=0.3,fps=24",
                    "-pix_fmt", "yuv420p", str(morph)], check=True)
    return zoom, morph


def test_camera_only_zoom_passes(clips):
    zoom, _ = clips
    r = FC.flow_check(zoom, write=False)
    assert r["verdict"] == "PASS", r


def test_dissolve_morph_escalates(clips):
    _, morph = clips
    r = FC.flow_check(morph, write=False)
    assert r["verdict"] == "ESCALATE", r


def test_sidecar_written(clips):
    zoom, _ = clips
    FC.flow_check(zoom, write=True)
    side = zoom.with_suffix(".flowqc.json")
    assert side.exists()
    import json
    d = json.loads(side.read_text(encoding="utf-8"))
    assert d["verdict"] in ("PASS", "ESCALATE") and "max_residual" in d
