"""Calibration loop CLI — show where the self-review is blind vs the external panel.

  python _calibrate.py            # print the calibration report + proposal candidates

The report aggregates, by defect class, every real defect the external panel/user
caught that the internal self-review + independent audit rated PASS — i.e. the
engine's blind spots. Classes that keep slipping and are not yet hard gates are
flagged as PROPOSAL CANDIDATES. Approve a proposal and the agent strengthens the
self-review prompt / adds a gate so that blind spot closes (propose-I-approve).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pipeline import learning

print(learning.report())
