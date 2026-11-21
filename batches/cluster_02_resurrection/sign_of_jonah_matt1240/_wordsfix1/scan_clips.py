import subprocess, numpy as np, json
from pathlib import Path
C=Path(r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection\sign_of_jonah_matt1240\visual\_wordsfix1_pool\clips")
used="jonah_cast_overboard great_fish_rising storm_ship_waves nineveh_distant_walls lot_falls_jonah jesus_and_scribes jonah_in_the_deep three_days_dark_tomb jonah_sinking_down body_laid_in_tomb stone_rolled_dawn jonah_on_shore mercy_hand_into_deep man_rising_from_water risen_christ_wounds".split()
out={}
for s in used:
    r=subprocess.run(["ffmpeg","-v","error","-i",str(C/f"{s}.mp4"),"-vf","scale=48:84,format=gray","-f","rawvideo","-"],capture_output=True)
    a=np.frombuffer(r.stdout,np.uint8).reshape(-1,84,48).astype(float); n=len(a)
    fwd=np.mean([np.abs(a[i]-a[i+1]).mean() for i in range(n-1)])
    # palindrome test: frame i vs frame n-1-i
    pal=np.mean([np.abs(a[i]-a[n-1-i]).mean() for i in range(n//2)])
    stat=np.mean([np.abs(a[i]-a[0]).mean() for i in range(n)])
    # freeze: trailing identical frames
    tail=sum(1 for i in range(n-1,0,-1) if np.abs(a[i]-a[i-1]).mean()<0.05)
    out[s]=dict(frames=n,step=round(fwd,2),pal=round(pal,2),first_last=round(np.abs(a[0]-a[-1]).mean(),2),frozen_tail_frames=tail)
    print(s,out[s])
