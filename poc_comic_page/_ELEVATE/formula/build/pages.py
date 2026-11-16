"""pages.py - python mirror of _remotion/src/comic_kit/pages.ts (page layouts as data). Boxes are [x, y, w, h] on a 1080x1920 page."""


def page_layout(kind, m=40, g=28, top=None, bottom=None):
    y0 = m if top is None else top; y1 = 1920 - (m if bottom is None else bottom); W = 1080 - 2 * m; H = y1 - y0
    if kind == "stack3":
        h = (H - 2 * g) / 3; return [[m, y0 + i * (h + g), W, h] for i in range(3)]
    if kind == "stack2":
        h = (H - g) / 2; return [[m, y0 + i * (h + g), W, h] for i in range(2)]
    if kind == "side2":
        w = (W - g) / 2; return [[m + i * (w + g), y0, w, H] for i in range(2)]
    if kind == "big_2small":
        hb = H * 0.55; hs = H - hb - g; w = (W - g) / 2; return [[m, y0, W, hb], [m, y0 + hb + g, w, hs], [m + w + g, y0 + hb + g, w, hs]]
    if kind == "big_inset":
        return [[m, y0, W, H * 0.8], [m + W * 0.5, y0 + H * 0.66, W * 0.5, H * 0.34]]
    return [[m, y0, W, H]]
