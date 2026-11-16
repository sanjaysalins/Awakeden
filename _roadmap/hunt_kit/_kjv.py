"""Reuse the existing KJV checker (prophecy/01_bethlehem/fresh_hunt/kjv_check.py) - one copy of the logic."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "prophecy" / "01_bethlehem" / "fresh_hunt"))
from kjv_check import check, verse, K  # noqa: F401
