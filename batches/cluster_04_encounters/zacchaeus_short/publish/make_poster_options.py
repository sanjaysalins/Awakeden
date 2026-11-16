r"""More 9:16 poster options ($0), same yellow look as poster_9x16 (option A).
B = look up / look down (t2 Zacchaeus on branch, t3 Jesus looking up). C = question title. D = huge Jesus face + small Zacchaeus in tree.
.venv\Scripts\python.exe <this>"""
from PIL import Image, ImageDraw
import make_poster_thumbs as P   # reuses ground/head/paste_shadow/text_c + cutouts (re-renders A too)
O = P.OUT; W, H = 1080, 1920; Y, K, R = P.YEL, P.BLK, P.RED
BEB = lambda s: P.F("BebasNeue-Regular.ttf", s)
def crisp(p):
    im = Image.open(p); a = im.split()[-1].point(lambda v: 255 if v > 110 else 0); im.putalpha(a); return im.crop(a.getbbox())
T2, T3 = crisp(O/"_t2_cut.png"), crisp(O/"_t3_cut.png")
T2 = T2.crop((int(T2.width*0.30), 0, T2.width, T2.height)); T2 = T2.crop(T2.getbbox())   # drop the branch-tip leaf blob
def scale(im, h): return im.resize((int(im.width*h/im.height), h), Image.LANCZOS)
def foot(dr, x=W//2): P.text_c(dr, x, H-95, "ZACCHAEUS · LUKE 19", P.F("bahnschrift.ttf", 44), K, 4, Y)

def B():
    im = P.ground(W, H, 11).convert("RGBA")
    z = scale(T2, 900); P.paste_shadow(im, z, (W-z.width+60, 40))            # up the tree, top right
    j = scale(T3, 1150); P.paste_shadow(im, j, (-40, H-j.height+60))         # looking up, bottom left
    dr = ImageDraw.Draw(im)
    P.text_c(dr, 330, 330, "HE CLIMBED", BEB(170), K, 7, Y); P.text_c(dr, 330, 490, "A TREE.", BEB(170), K, 7, Y)
    P.text_c(dr, 770, 1000, "JESUS", BEB(190), R, 7, Y); P.text_c(dr, 770, 1180, "FOUND HIM.", BEB(150), R, 7, Y)
    return im.convert("RGB")

def C():
    im = P.ground(W, H, 13).convert("RGBA")
    j = P.head(P.JES, 1850, 1.0); P.paste_shadow(im, j, ((W-j.width)//2 - 40, 330))
    z = P.head(P.ZAC, 820, 0.55); P.paste_shadow(im, z, (W-z.width+120, H-z.height))
    dr = ImageDraw.Draw(im)
    P.text_c(dr, W//2, 50, "WHO WAS LOOKING", BEB(170), K, 7, Y); P.text_c(dr, W//2, 205, "FOR WHOM?", BEB(170), R, 7, Y)
    P.text_c(dr, 300, H-110, "ZACCHAEUS · LUKE 19", P.F("bahnschrift.ttf", 44), K, 4, Y)
    return im.convert("RGB")

def D():
    im = P.ground(W, H, 17).convert("RGBA")
    j = P.head(P.JES, 2300, 1.0); P.paste_shadow(im, j, ((W-j.width)//2 - 60, 520))   # huge face, low
    z = scale(T2, 560); P.paste_shadow(im, z, (W-z.width-10, 300))                     # small, up in the tree
    dr = ImageDraw.Draw(im)
    P.text_c(dr, W//2, 50, "HE CLIMBED A TREE.", BEB(165), K, 7, Y)
    P.text_c(dr, W//2, H-330, "JESUS FOUND HIM.", BEB(175), R, 8, Y)
    foot(dr); return im.convert("RGB")

for n, f in [("B", B), ("C", C), ("D", D)]: f().save(O/f"poster_9x16_{n}.jpg", quality=92)
print("ok")

# ---- LOCKED option B (owner 2026-11-13): B-style 16x9 + 1x1, then install all as the real thumbs ----
def B_wide():
    """Jesus left looking up-right at Zacchaeus; words stacked on the right so they read top->bottom: ME? (by Zacchaeus) then YES. YOU."""
    w, h = 1280, 720; im = P.ground(w, h, 21).convert("RGBA")
    z = scale(T2, 400); P.paste_shadow(im, z, (w-z.width-10, 10))
    j = scale(T3, 760); P.paste_shadow(im, j, (-30, h-j.height+150))
    dr = ImageDraw.Draw(im)
    P.text_c(dr, 800, 40, "ME?", BEB(190), K, 7, Y)
    P.text_c(dr, 905, 430, "YES. YOU.", BEB(185), R, 7, Y)
    P.text_c(dr, 905, 640, "ZACCHAEUS · LUKE 19", P.F("bahnschrift.ttf", 30), K, 3, Y)
    return im.convert("RGB")

def B_square():
    w = h = 1080; im = P.ground(w, h, 23).convert("RGBA")
    z = scale(T2, 600); P.paste_shadow(im, z, (w-z.width+20, 20))
    j = scale(T3, 860); P.paste_shadow(im, j, (-40, h-j.height+260))
    dr = ImageDraw.Draw(im)
    P.text_c(dr, 300, 70, "ME?", BEB(260), K, 7, Y)
    P.text_c(dr, 800, 640, "YES.", BEB(210), R, 7, Y); P.text_c(dr, 800, 840, "YOU.", BEB(210), R, 7, Y)
    return im.convert("RGB")

if __name__ == "__main__":
    import json, shutil
    T = P.HERE/"thumbs"; old = T/"_old_v1"; old.mkdir(exist_ok=True)
    for f in T.glob("thumb_*.jpg"):
        if not (old/f.name).exists(): shutil.copy2(f, old/f.name)
    B_wide().save(T/"thumb_16x9.jpg", quality=92); B_square().save(T/"thumb_1x1.jpg", quality=92)
    shutil.copy2(O/"title_P1.jpg", T/"thumb_9x16.jpg"); shutil.copy2(O/"title_P1.jpg", T/"thumb_tiktok.jpg")   # run make_title_mockups.py first
    m = json.loads((T/"_meta.json").read_text(encoding="utf-8"))
    m["source"] = "LOCKED poster option B + title round 2 words ME? / YES. YOU. (owner 2026-11-13): make_title_mockups.py then make_poster_options.py; old thumbs in thumbs/_old_v1/"
    (T/"_meta.json").write_text(json.dumps(m, indent=2), encoding="utf-8"); print("installed")
