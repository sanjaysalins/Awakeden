import cv2,numpy as np,json,sys
CLIP="F:/slk/PycharmProjects/JesusInTheBible/_remotion/public/sf/s%02d.mp4"
orb=cv2.SIFT_create(2500)
res={}
for n in range(1,18):
    cap=cv2.VideoCapture(CLIP%n); fps=cap.get(cv2.CAP_PROP_FPS); N=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        frames.append(cv2.cvtColor(cv2.resize(f,(1080,1920)),cv2.COLOR_BGR2GRAY))
    kp0,d0=orb.detectAndCompute(frames[0],None)
    bf=cv2.BFMatcher()
    out=[]
    step=max(1,int(round(fps/4)))
    idx=list(range(0,len(frames),step))
    if idx[-1]!=len(frames)-1: idx.append(len(frames)-1)
    for i in idx:
        kp,d=orb.detectAndCompute(frames[i],None)
        m=bf.knnMatch(d0,d,k=2)
        good=[a for a,b in (x for x in m if len(x)==2) if a.distance<0.75*b.distance]
        if len(good)<8: out.append((i/fps,1,0,0,len(good)));continue
        A=np.float32([kp0[g.queryIdx].pt for g in good]);B=np.float32([kp[g.trainIdx].pt for g in good])
        M,inl=cv2.estimateAffinePartial2D(A,B,method=cv2.RANSAC,ransacReprojThreshold=6)
        s=float(np.hypot(M[0,0],M[1,0]))
        out.append((round(i/fps,3),round(s,4),round(float(M[0,2]),1),round(float(M[1,2]),1),int(inl.sum())))
    res[n]=out
    print(n,"fps",fps,len(frames)," last:",out[-1], "mid:",out[len(out)//2])
json.dump(res,open("track.json","w"))
