"""Two-Thieves 38s short ($0 build). Locked words 2026-11-09, recorded audio + 3.0s landing hold.
Mockers-look: full-bleed clips, translucent pill + speaker tab + verse chip, hook card.
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/build_s32.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_tp as T
import build_w3 as W

EPD = T.ROOT / "batches/cluster_01_cross"
T.CL = EPD / "today_paradise_luke2343/visual/clips"
T.FILM = EPD / "today_paradise_short32/audio/narration_landing3s.mp3"
T.TOTAL = 38.0; T.FADE = 0.04
# turn starts from real segment durations (turns + 0.4s pre-quote silences)
S = dict(h=(0.0, 3.752), two=(3.752, 6.546), moc=(6.946, 10.866), one=(10.866, 14.536), pen=(14.936, 18.696),
         rem=(18.696, 22.047), jes=(22.447, 26.527), end=(26.527, 35.0))
# (t0, t1, clip, t_in, cx, cy, z0, z1)
SH = [(0.0, 1.9, "jesus_turns_to_thief", 0.0, .55, .42, 1.3, 1.5), (1.9, 3.752, "penitent_thief_face", 0.0, .42, .42, 1.3, 1.5),
      (3.752, 5.1, "two_thieves_wide", 0.0, .5, .5, 1.0, 1.12), (5.1, 6.946, "golgotha_hill_wide", 0.0, .5, .5, 1.0, 1.15),
      (6.946, 10.866, "mocker_taunts_jesus", 0.5, .5, .42, 1.15, 1.35),
      (10.866, 12.6, "mocker_thief_face", 0.0, .5, .42, 1.5, 1.7), (12.6, 14.936, "penitent_thief_face", 1.0, .42, .45, 1.3, 1.5),
      (14.936, 18.696, "confession_face_hands", 0.0, .55, .55, 1.3, 1.5),
      (18.696, 22.447, "kingdom_light_clouds", 0.0, .5, .4, 1.1, 1.3),
      (22.447, 26.527, "jesus_turns_to_thief", 1.5, .5, .42, 1.2, 1.4),
      (26.527, 29.4, "answer_light_profile", 0.0, .45, .5, 1.2, 1.4), (29.4, 32.0, "risen_mercy_hand", 0.0, .5, .45, 1.2, 1.4),
      (32.0, 35.0, "us_under_cross_shadow", 0.0, .5, .5, 1.0, 1.2), (35.0, 38.0, "paradise_dawn", 0.0, .5, .5, 1.05, 1.25)]
# pills: (t0, t1, text, who, ref, jesus)
PL = [(0.1, 3.7, "Jesus promised paradise to a criminal. Why?", None, None, False),
      (3.8, 6.9, "Two criminals were dying on crosses beside Him.", None, None, False),
      (6.95, 10.9, "If thou be Christ, save thyself and us.", "A MOCKER", "LUKE 23:39", False),
      (10.9, 14.9, "One wanted off the cross. The other asked for very little.", None, None, False),
      (14.95, 18.7, "Lord, remember me when thou comest into thy kingdom.", "THE OTHER THIEF", "LUKE 23:42", False),
      (18.7, 22.4, "He asked to be remembered. Someday.", None, None, False),
      (22.45, 26.5, "To day shalt thou be with me in paradise.", "JESUS", "LUKE 23:43", True),
      (26.55, 29.3, "Not someday. Today.", None, None, False),
      (29.4, 31.9, "Not just remembered. With Him.", None, None, False),
      (32.0, 35.3, "You can ask Him to remember you too.", None, None, False)]


def main():
    d = T.HERE / "work" / "s32_lett"; d.mkdir(parents=True, exist_ok=True)
    shots = [dict(t0=a, t1=b, clip=c, t_in=ti, cx=cx, cy=cy, z0=z0, z1=z1) for a, b, c, ti, cx, cy, z0, z1 in SH]
    ov = []
    for i, (a, b, text, who, ref, j) in enumerate(PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j); ov.append((str(p), a, b))
    h = d / "hook.png"; T.light_text(h, "PARADISE FOR A CRIMINAL?", 420, size=130, maxw=900); ov.append((str(h), 0.0, 2.2))
    T.compose("S32", shots, ov)


if __name__ == "__main__":
    main()
