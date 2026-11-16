// comic_kit/pages.ts - page layouts as data. Each returns panel boxes [x, y, w, h] on a 1080x1920 page (paper margin m, ink gutter g).
// An episode scene can say  layout: "stack3"  and omit panel boxes; build_thief_v2.py mirrors this (pages.py) because anchors need the boxes in python.
import type { Box } from "./core";
export type PageKind = "stack3" | "stack2" | "side2" | "big_2small" | "big_inset" | "splash" | "diag2";
export interface PageOpts { m?: number; g?: number; top?: number; bottom?: number }
export const pageLayout = (kind: PageKind, o: PageOpts = {}): Box[] => {
  const m = o.m ?? 40, g = o.g ?? 28, y0 = o.top ?? m, y1 = 1920 - (o.bottom ?? m), W = 1080 - 2 * m, H = y1 - y0;
  switch (kind) {
    case "stack3": { const h = (H - 2 * g) / 3; return [0, 1, 2].map((i) => [m, y0 + i * (h + g), W, h] as Box); }
    case "stack2": { const h = (H - g) / 2; return [0, 1].map((i) => [m, y0 + i * (h + g), W, h] as Box); }
    case "side2": { const w = (W - g) / 2; return [0, 1].map((i) => [m + i * (w + g), y0, w, H] as Box); }
    case "big_2small": { const hb = H * 0.55, hs = H - hb - g, w = (W - g) / 2; return [[m, y0, W, hb], [m, y0 + hb + g, w, hs], [m + w + g, y0 + hb + g, w, hs]]; }
    case "big_inset": return [[m, y0, W, H * 0.8], [m + W * 0.5, y0 + H * 0.66, W * 0.5, H * 0.34]];
    case "diag2": case "splash": default: return [[m, y0, W, H]];
  }
};
/** fill panel boxes from `scene.layout` when a panel declares no box (data-driven pages). */
export const normalizeEpisode = (ep: any): any => ({
  ...ep,
  scenes: ep.scenes.map((s: any) => {
    if (!s.layout) return s;
    const boxes = pageLayout(s.layout, s.layout_opts || {});
    return { ...s, paper: s.paper ?? true, panels: s.panels.map((p: any, i: number) => (p.box ? p : { ...p, box: boxes[i] })) };
  }),
});
