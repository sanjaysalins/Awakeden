import sys, cv2, numpy as np
for p in sys.argv[1:]:
    cap=cv2.VideoCapture(p); fr=[]
    while True:
        r,f=cap.read()
        if not r: break
        fr.append(f)
    blue=[int(((f[int(.3*f.shape[0]):,:,0].astype(int)-f[int(.3*f.shape[0]):,:,2].astype(int))>35).sum()) for f in fr]
    g=[cv2.cvtColor(cv2.resize(f,(360,640)),cv2.COLOR_BGR2GRAY).astype(np.float32) for f in fr]
    d=np.mean([np.mean(np.abs(g[i]-g[i+1])) for i in range(len(g)-1)])
    print(p, len(fr),"frames blue first/mid/last", blue[0], blue[len(blue)//2], blue[-1], "meandiff %.2f"%d)
