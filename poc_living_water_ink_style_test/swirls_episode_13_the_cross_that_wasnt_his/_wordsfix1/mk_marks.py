import re
from pathlib import Path
H = Path(__file__).resolve().parent
s = (Path(r"C:/Users/sanjay/AppData/Local/Temp/uplift_fix/ep13/marks_overlay_fix.py")).read_text().replace("\r", "")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep("UP = Path(r'C:/Users/sanjay/AppData/Local/Temp/uplift_fix/ep13/uplift')", "UP = Path(r'F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_episode_13_the_cross_that_wasnt_his/_wordsfix1')")
rep('SHIPPED = EP / "swirls_episode_13_the_cross_that_wasnt_his_final_piano_sfx.mp4"', 'SHIPPED = UP / "_new_sfx.mp4"')
rep('base = UP / "work" / f"base_{MODE}.mp4"', 'base = UP / "work" / "base.mp4"')
rep('out = UP / f"ep13_uplift_fix1.mp4"', 'out = UP / "ep13_wordsfix1_nofix.mp4"')
# drop M5 (F04 circle) and M3 (F05 camp square): those pages are gone
i = s.index("# M5 RED circle"); j = s.index("# M4 same square")
s = s[:i] + s[j:]
# M4 retimed to 'burned'(1248) / 'outside'(1260) on F05B (slot 1140-1288)
i = s.index("# M4 same square"); j = s.index("# M7 underline")
s = s[:i] + '''# M4 camp square redrawn, arrow OUT, F05B right margin, at "outside"@42.02 s (frame 1260)
MARKS.append(dict(id="M4", device="S5 in/out plan (out)", shot="S08", word="outside", word_t=42.02, until=1285,
    strokes=[S(box(800, 650, 920, 790), 1250, 10, width=4), S(box(840, 695, 880, 735), 1259, 5, width=4),
             S(arrow_pts((860, 715), (1040, 715), 0.0), 1262, 9, width=4), S(head((860, 715), (1040, 715), 24), 1271, 3, width=4)]))
''' + s[j:]
rep('shot="S13", word="forth", word_t=69.86, until=2180,', 'shot="S11", word="forth", word_t=58.49, until=1839,')
rep("S([(88, 1836), (372, 1834)], 2094, 10)", "S([(88, 1836), (372, 1834)], 1753, 10)")
rep('shot="S16", word="forced", word_t=82.80, until=2690,', 'shot="S13", word="forced", word_t=66.56, until=2195,')
rep("S(rect_pts(28, 162, 362, 520), 2482, 10, width=6, second=True)", "S(rect_pts(28, 162, 362, 520), 1995, 10, width=6, second=True)")
(H / "marks_wordsfix1.py").write_text(s, encoding="utf-8")
print("ok")
