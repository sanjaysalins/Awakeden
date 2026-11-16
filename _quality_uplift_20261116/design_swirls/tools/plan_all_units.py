import sys, importlib.util, json, subprocess
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test")
sys.path.insert(0, str(R)); sys.path.insert(0, str(R/"test_the_cross"))
import swirls_assemble as sa
eps = ["swirls_episode_02_ashes_that_made_clean","swirls_episode_07_the_bier_he_touched","swirls_episode_08_can_any_good_thing","swirls_episode_10_she_loved_much","swirls_episode_11_where_are_the_nine","swirls_episode_13_the_cross_that_wasnt_his","swirls_pilot_01_jacobs_ladder"]
out = {}
for e in eps:
    d = R/e
    try:
        spec = importlib.util.spec_from_file_location("ep_"+e, d/"episode.py")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        man = m.MANIFEST
        st = sa.plan_units(man)
        nl = sa.dur(man.narration)
        print(f"\n=== {e}  narration={nl:.2f}s hold={man.outro_hold} size={man.w}x{man.h} timing={'real' if (d/'unit_timing.json').exists() else 'proportional'}")
        t = 0
        for u, s in zip(man.units, st):
            n = s['native']; sl = s['slot']
            gap = (sl - n) if n else None
            print(f"  {s['tag']:14s} {t:6.2f}-{t+sl:6.2f} slot={sl:5.2f} native={n if n is None else round(n,2)} fill={0 if gap is None or gap<0 else round(gap,2)} mode={s['mode']} tail={u.tail_loop_seconds} src={u.src.name}")
            t += sl
        out[e] = st
    except Exception as ex:
        print("ERR", e, repr(ex))
    print("  -- all mp4 in folder:")
    for p in sorted(d.glob("*.mp4*")):
        try:
            r = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height:format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.split()
            print("    ", p.name, " ".join(r))
        except Exception as ex: print("    ", p.name, "ERR")
