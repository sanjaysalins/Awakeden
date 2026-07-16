"""Chain the post-build steps once livingpage_full_preview.mp4 exists:
  1. copy/rename it to BronzeSerpent_16x9.mp4 (the *_16x9.mp4 glob _add_score_inked.py needs)
  2. run the score mix (Suno library, $0)
  3. run the SFX bed ($0, sound_library)
  4. print the final file:/// link
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
PREVIEW = OUT / "livingpage_full.spec_preview.mp4"
FILM = OUT / "BronzeSerpent_16x9.mp4"
PY = str(HERE.parents[1] / ".venv" / "Scripts" / "python.exe")

if not PREVIEW.is_file():
    sys.exit(f"missing build output: {PREVIEW}")

if not FILM.is_file():
    shutil.copy2(PREVIEW, FILM)
    print(f"[copy] {PREVIEW.name} -> {FILM.name}")
else:
    print(f"[skip] {FILM.name} already present")

print("\n=== SCORE ===")
r = subprocess.run([PY, str(HERE / "_add_score_inked.py"), "--yes"], cwd=str(HERE))
if r.returncode != 0:
    sys.exit("score step failed")

print("\n=== SFX ===")
r = subprocess.run([PY, str(HERE / "_sfx_bronze_inked.py")], cwd=str(HERE))
if r.returncode != 0:
    sys.exit("sfx step failed")

final = OUT / "BronzeSerpent_16x9_scored_sfx.mp4"
print(f"\n[FINAL] file:///{str(final).replace(chr(92), '/')}")
