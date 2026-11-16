"""9:16 thumb mock-ups for the title round 2 candidates ($0). Same B picture, different words."""
from PIL import ImageDraw
import make_poster_options as M
P = M.P; W, H = M.W, M.H
def b(top, bot, name, bx=770, by=1000):
    im = P.ground(W, H, 11).convert("RGBA")
    z = M.scale(M.T2, 900); P.paste_shadow(im, z, (W-z.width+60, 40))
    j = M.scale(M.T3, 1150); P.paste_shadow(im, j, (-40, H-j.height+60))
    dr = ImageDraw.Draw(im)
    for k, (s, sz) in enumerate(top): P.text_c(dr, 330, 330+k*int(sz*0.95), s, M.BEB(sz), M.K, 7, M.Y)
    for k, (s, sz) in enumerate(bot): P.text_c(dr, bx, by+k*int(sz*0.95), s, M.BEB(sz), M.R, 7, M.Y)
    im.convert("RGB").save(M.O/f"title_{name}.jpg", quality=90)
b([("ME?", 260)], [("YES.", 210), ("YOU.", 210)], "P1", bx=860, by=1180)
b([("COME", 200), ("DOWN.", 200)], [("TODAY.", 200)], "P2")
b([("BUT WHO", 170)], [("FOUND", 190), ("WHO?", 190)], "P3")
print("ok")
