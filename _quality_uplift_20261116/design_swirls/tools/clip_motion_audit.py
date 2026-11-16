import sys, subprocess, numpy as np
from pathlib import Path
try:
    import cv2
except Exception as e:
    print("no cv2", e); sys.exit()
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test")
eps = ["swirls_episode_02_ashes_that_made_clean","swirls_episode_07_the_bier_he_touched","swirls_episode_08_can_any_good_thing","swirls_episode_10_she_loved_much","swirls_episode_11_where_are_the_nine","swirls_episode_13_the_cross_that_wasnt_his","swirls_pilot_01_jacobs_ladder"]
def frame(p, t):
    r = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",str(p),"-frames:v","1","-vf","scale=360:640,format=gray","-f","rawvideo","-"],capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(640,360).astype(np.float32)
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout)
for e in eps:
    d = R/e
    clips = [p for p in sorted(d.glob("*.mp4")) if ("_9x16.mp4" in p.name and p.name.count(".")==1) or p.name in ("front_cover.mp4","back_cover.mp4")]
    if "jacobs" in e: clips.append(d/"_style_test_durer_woodcut"/"front_cover_woodcut.mp4")
    for p in clips:
        try:
            D = dur(p); a = frame(p, 0.1); b = frame(p, D-0.15)
            raw = float(np.mean(np.abs(a-b)))
            W = np.eye(2,3,dtype=np.float32)
            try:
                cc, W = cv2.findTransformECC(a/255, b/255, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT, 200, 1e-6))
                bw = cv2.warpAffine(b, W, (360,640), flags=cv2.INTER_LINEAR+cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
                m = np.zeros_like(a); m[40:600,30:330]=1
                al = float(np.sum(np.abs(a-bw)*m)/np.sum(m)); z = float(np.sqrt(abs(np.linalg.det(W[:,:2]))))
            except Exception as ex:
                al = -1; z = 0
            tag = "CAMERA-ONLY (still stand-in?)" if 0 <= al < 2.2 and raw > al*1.5 else ("near-frozen" if raw < 2.0 else "")
            print(f"{e[15:32]:18s} {p.name[-28:]:28s} {D:5.2f}s raw={raw:5.2f} aligned={al:5.2f} zoom={z:.3f} {tag}")
        except Exception as ex:
            print(p.name, "ERR", ex)
