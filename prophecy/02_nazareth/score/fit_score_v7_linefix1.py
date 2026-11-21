r"""$0 linefix1: the score is the SAME paid score_v7.mp3, delayed 1.2 s (it fades in from silence over its first 2.5 s anyway) so every later score moment stays on its word; end fade (2.6 s) intact. -> score_v7_lf1.mp3 (61.05 s)"""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(H / "score_v7.mp3"), "-af", "adelay=1200:all=1", str(H / "score_v7_lf1.mp3")], check=True)
print("[done] score_v7_lf1.mp3")
