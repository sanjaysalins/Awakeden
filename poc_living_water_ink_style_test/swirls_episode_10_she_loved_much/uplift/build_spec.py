"""ep10 uplift: writes uplift.json (shots at 30 fps from the real word times in word_timings/ep10_words.txt)."""
import json
from pathlib import Path
UP = Path(__file__).resolve().parent
P = "swirls_episode_10_she_loved_much_"
T = [0, 2.00, 9.95, 13.90, 21.85, 25.00, 28.60, 32.50, 40.45, 43.40, 53.30, 58.30, 61.90, 68.85, 78.00, 83.90, 91.85, 98.40]
TOTAL = 3185   # shipped final frame count (106.167 s)
src = [("S01", "front", "front_cover.mp4", "No water for his feet."),
 ("S02", "F01", P + "f01_9x16.mp4", "No kiss. No oil. ... at his own table."),
 ("S03", "cover-notitle", "../_bakeoff_format_v2/B1/ep10_cover_notitle_try1.mp4", "A woman he hadn't invited walked in anyway"),
 ("S04", "F02", P + "f02_9x16.mp4", "A woman in the city, which was a sinner... behind him weeping,"),
 ("S05", "F03A", "uplift/clips/f03a_4s.mp4", "and began to wash his feet"),
 ("S06", "F03B", "uplift/clips/f03b_4s.mp4", "with tears... and kissed his feet,"),
 ("S07", "F03C", "uplift/clips/f03c_4s.mp4", "and anointed them with the ointment."),
 ("S08", "F04", P + "f04_9x16.mp4", "Simon thought it, not out loud"),
 ("S09", "F04B", "uplift/clips/f04b_3s.mp4", "Jesus answered anyway."),
 ("S10", "F05", P + "f05_9x16.mp4", "A creditor had two debtors"),
 ("S11", "F06", P + "f06_9x16.mp4", "Which of them will love him most?"),
 ("S12", "F06B", "uplift/clips/f06b_4s.mp4", "I suppose that he, to whom he forgave most."),
 ("S13", "F07", P + "f07_9x16.mp4", "Seest thou this woman?"),
 ("S14", "F08", P + "f08_9x16.mp4", "Her sins, which are many, are forgiven"),
 ("S15", "F08B", "uplift/clips/f08b_6s.mp4", "Forgiven first - love was the receipt"),
 ("S16", "F09", P + "f09_9x16.mp4", "Thy faith hath saved thee; go in peace."),
 ("S17", "F09B", "uplift/clips/f09b_7s.mp4", "Thy faith. That answer holds for whoever..."),
 ("S18", "back", "back_cover.mp4", "She came in carrying an alabaster box... + hold")]
fr = [int(t * 30 + 0.5) for t in T] + [TOTAL]
shots = [{"id": s[0], "page": s[1], "f0": fr[i], "f1": fr[i + 1], "src": s[2], "words": s[3]} for i, s in enumerate(src)]
(UP / "uplift.json").write_text(json.dumps({"fps": 30, "size": [1080, 1920], "total_frames": TOTAL, "shots": shots}, indent=1), encoding="utf-8")
for s in shots: print(s["id"], s["page"], s["f0"], s["f1"], round((s["f1"] - s["f0"]) / 30, 2), "s")
