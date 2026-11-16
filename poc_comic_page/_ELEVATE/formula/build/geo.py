"""geo.py - comic kit geometry shared with the Remotion kit (same maths as comic_kit/layouts.tsx).
Doc `anchor`: z = z0+(z1-z0)*i/n ; vx = clamp(cx-0.5/z,0,1-1/z) ; screen=((ax-vx)*z*1080, ...)  (generalised to any box)."""
FW, FH = 1080, 1920
clamp = lambda v, a=0.0, b=1.0: max(a, min(b, v))


def zoom_at(shot, f):
    f = min(f, shot["freeze_f"]) if shot.get("freeze_f") is not None else f
    p = clamp((f - shot["f_z0"]) / max(1, shot["f_z1"] - shot["f_z0"]))
    return shot["z0"] + (shot["z1"] - shot["z0"]) * p


def view(box, shot, f):
    """box=[x,y,w,h] in screen px -> (vx,vy,S,vw,vh) picture window (normalised) + px-per-picture-px."""
    x, y, w, h = box
    z = zoom_at(shot, f); c = max(w / FW, h / FH); S = c * z
    vw, vh = w / (FW * S), h / (FH * S)
    vx = clamp(shot["cx"] - vw / 2, 0, 1 - vw); vy = clamp(shot["cy"] - vh / 2, 0, 1 - vh)
    return vx, vy, S, vw, vh


def to_screen(pic, box, shot, f):
    vx, vy, S, _, _ = view(box, shot, f)
    return box[0] + (pic[0] - vx) * FW * S, box[1] + (pic[1] - vy) * FH * S


def to_pic(scr, box, shot, f):
    vx, vy, S, _, _ = view(box, shot, f)
    return vx + (scr[0] - box[0]) / (FW * S), vy + (scr[1] - box[1]) / (FH * S)
