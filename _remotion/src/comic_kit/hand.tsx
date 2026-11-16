// comic_kit/hand.tsx - the 6 hand-drawn marks (uplift kit K1..K6). Wordless strokes, never letters.
// Spec: _quality_uplift_20261116/design_comic/COMIC_UPLIFT_SPEC.md part 2b/2c. Frames are 30 fps, absolute.
//   thread (K1)         one gold hand line tying two matching things, ends in a small knot
//   ink_ring (K2)       a hand ellipse, two passes (full, then a lighter offset pass), around ONE word or object
//   ink_strike (K3)     one hand line through a caption word
//   ink_underline (K4)  one hand line under a caption word
//   tally (K5)          hand ticks that land one by one (counting what the voice counts)
//   route (K6)          a dotted path with an arrow head; dash:"gaze" = dashed sight line, no arrow
// A mark is data: { kind, at, frames?, until?, tone?, seed?, ... }. Points may be [x,y] or { track: [[frame,x,y],...] }.
// Marks boil (2 drawings, swap every 3 frames). Pictures never boil. Reuses InkStroke helpers from core.tsx.
import React from "react";
import { Box, Doodle, INK, Pt, boilSeed, clamp, mulberry, pathD, plen, prog, wobblePts } from "./core";

export const GOLD = "#F2C14E";
export const BONE_HEX = "#F4ECD8";
export type TrackPt = { track: [number, number, number][] };
export type AnyPt = Pt | TrackPt;

/** resolve a static or tracked point at frame f (linear between track samples, clamped at the ends). */
export const resolvePt = (p: AnyPt, f: number): Pt => {
  if (Array.isArray(p)) return p as Pt;
  const t = (p as TrackPt).track;
  if (!t.length) return [0, 0];
  if (f <= t[0][0]) return [t[0][1], t[0][2]];
  if (f >= t[t.length - 1][0]) return [t[t.length - 1][1], t[t.length - 1][2]];
  for (let i = 1; i < t.length; i++) {
    if (f <= t[i][0]) {
      const k = (f - t[i - 1][0]) / Math.max(1, t[i][0] - t[i - 1][0]);
      return [t[i - 1][1] + (t[i][1] - t[i - 1][1]) * k, t[i - 1][2] + (t[i][2] - t[i - 1][2]) * k];
    }
  }
  return [t[t.length - 1][1], t[t.length - 1][2]];
};

const colorOf = (tone?: string, def = "ink") => {
  const t = tone || def;
  return t === "gold" ? GOLD : t === "bone" ? BONE_HEX : INK;
};

/** one hand stroke: wobble + optional ink under-stroke (gold) + draw-on + boil. */
const HandStroke: React.FC<{
  pts: Pt[]; f: number; color: string; width?: number; seed?: number; draw?: [number, number]; boil?: boolean; amp?: number; under?: boolean; opacity?: number;
}> = ({ pts, f, color, width = 7, seed = 1, draw, boil = true, amp = 2, under = false, opacity = 1 }) => {
  let p = 1;
  if (draw) {
    if (f < draw[0]) return null;
    p = prog(f, draw[0], draw[1]);
  }
  const w = wobblePts(pts, boil ? boilSeed(f, seed) : seed, amp);
  const L = plen(w), d = pathD(w);
  const common = { fill: "none", strokeLinecap: "round" as const, strokeLinejoin: "round" as const, strokeDasharray: draw ? `${L}` : undefined, strokeDashoffset: draw ? L * (1 - p) : 0 };
  return (
    <g opacity={opacity}>
      {under && <path d={d} {...common} stroke={INK} strokeWidth={width + 3} transform="translate(2 2)" />}
      <path d={d} {...common} stroke={color} strokeWidth={width} />
    </g>
  );
};

const ellipsePts = (b: Box, grow: number, seed: number, start = -2.3): Pt[] => {
  const r = mulberry(seed * 131 + 7);
  const cx = b[0] + b[2] / 2, cy = b[1] + b[3] / 2, rx = b[2] / 2 + grow, ry = b[3] / 2 + grow * 0.7;
  const n = 26, out: Pt[] = [];
  for (let i = 0; i <= n; i++) {
    const a = start + (i / n) * Math.PI * 2 * 1.04; // a little over one turn: the ring never closes perfectly
    const k = 1 + (r() - 0.5) * 0.05;
    out.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
  }
  return out;
};

/** K1 thread: from -> to, soft S curve through 3 wobble points, small knot at the end. */
const Thread: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const a = resolvePt(d.from, f), b = resolvePt(d.to, f);
  const frames = d.frames ?? 16, dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
  const nx = -dy / L, ny = dx / L, bow = d.bow ?? 0.12 * L;
  const m1: Pt = [a[0] + dx * 0.33 + nx * bow, a[1] + dy * 0.33 + ny * bow];
  const m2: Pt = [a[0] + dx * 0.66 - nx * bow, a[1] + dy * 0.66 - ny * bow];
  const pts: Pt[] = d.via ? [a, ...(d.via as Pt[]), b] : [a, m1, m2, b];
  const end = d.until ?? Infinity;
  if (f >= end) return null;
  const knot = prog(f, d.knot_at ?? d.at + frames, 6);
  const kr = 15 * knot;
  const seed = d.seed ?? 11;
  return (
    <g>
      <HandStroke pts={pts} f={f} color={GOLD} under draw={[d.at, frames]} seed={seed} width={7} amp={2.2} />
      {knot > 0 && (
        <g>
          <circle cx={b[0]} cy={b[1]} r={kr + 1.5} fill="none" stroke={INK} strokeWidth={9} transform="translate(2 2)" />
          <circle cx={b[0]} cy={b[1]} r={kr} fill="none" stroke={GOLD} strokeWidth={7} />
        </g>
      )}
    </g>
  );
};

/** K2 ink_ring: two passes, 7 px (12 frames) then 4 px offset (8 frames). */
const InkRing: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const box = d.box as Box, c = colorOf(d.tone), seed = d.seed ?? 5;
  if (d.until != null && f >= d.until) return null;
  return (
    <g>
      <HandStroke pts={ellipsePts(box, 16, seed)} f={f} color={c} draw={[d.at, 12]} seed={seed} width={7} amp={2} />
      <g transform="translate(4 -3)">
        <HandStroke pts={ellipsePts(box, 22, seed + 3, -2.0)} f={f} color={c} draw={[d.at + 12, 8]} seed={seed + 3} width={4} amp={2} opacity={0.8} />
      </g>
    </g>
  );
};

/** K3 ink_strike: one line through a word, 6 frames. */
const InkStrike: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const [x, y, w, h] = d.box as Box;
  if (d.until != null && f >= d.until) return null;
  return <HandStroke pts={[[x - 8, y + h * 0.56], [x + w * 0.5, y + h * 0.5], [x + w + 8, y + h * 0.44]]} f={f} color={colorOf(d.tone)} draw={[d.at, d.frames ?? 6]} seed={d.seed ?? 7} width={7} amp={2.4} />;
};

/** K4 ink_underline: one line under a word, 8 frames. */
const InkUnderline: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const [x, y, w, h] = d.box as Box;
  if (d.until != null && f >= d.until) return null;
  const yy = y + h + 8;
  return <HandStroke pts={[[x - 4, yy + 2], [x + w * 0.5, yy], [x + w + 4, yy - 2]]} f={f} color={colorOf(d.tone)} draw={[d.at, d.frames ?? 8]} seed={d.seed ?? 9} width={7} amp={2} />;
};

/** K5 tally: n ticks, 3 frames each, 54 px tall, 6 px; the 5th crosses the first four. */
const Tally: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const [x, y] = d.xy as Pt, n = d.n ?? 3, c = colorOf(d.tone), seed = d.seed ?? 13;
  if (d.until != null && f >= d.until) return null;
  const ticks = Array.from({ length: n }, (_, i) => {
    const at = d.at + (d.gap_frames ? d.gap_frames * i : i * 3);
    if (i % 5 === 4) return <HandStroke key={i} pts={[[x - 10, y + 44], [x + 4 * 20, y + 6]]} f={f} color={c} draw={[at, 3]} seed={seed + i} width={6} amp={1.2} />;
    const xx = x + (i % 5) * 20;
    return <HandStroke key={i} pts={[[xx, y], [xx + 1.5, y + 54]]} f={f} color={c} draw={[at, 3]} seed={seed + i} width={6} amp={1.2} />;
  });
  return <g>{ticks}</g>;
};

/** K6 route: dotted path (dots 10 px, gap 22 px) that draws itself, arrow head at the end. dash:"gaze" = dashes, no arrow. */
const Route: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  if (f < d.at) return null;
  if (d.until != null && f >= d.until) return null;
  const pts = (d.pts as AnyPt[]).map((p) => resolvePt(p, f));
  const gaze = d.dash === "gaze";
  const frames = d.frames ?? 20;
  const p = prog(f, d.at, frames);
  const c = colorOf(d.tone), seed = d.seed ?? 17;
  const w = wobblePts(pts, boilSeed(f, seed), 1.6, 40);
  const L = plen(w), reach = L * p;
  const step = gaze ? 34 : 32; // dot 10 + gap 22
  const out: React.ReactNode[] = [];
  // walk the polyline
  let acc = 0, next = 0, i = 0;
  const tip: { pt: Pt; ang: number } = { pt: w[0], ang: 0 };
  for (let s = 1; s < w.length; s++) {
    const [x0, y0] = w[s - 1], [x1, y1] = w[s];
    const seg = Math.hypot(x1 - x0, y1 - y0) || 1, ang = Math.atan2(y1 - y0, x1 - x0);
    while (next <= acc + seg && next <= reach) {
      const t = (next - acc) / seg, px = x0 + (x1 - x0) * t, py = y0 + (y1 - y0) * t;
      if (gaze) out.push(<line key={i++} x1={px} y1={py} x2={px + Math.cos(ang) * 20} y2={py + Math.sin(ang) * 20} stroke={c} strokeWidth={6} strokeLinecap="round" />);
      else out.push(<circle key={i++} cx={px} cy={py} r={5.5} fill={c} />);
      tip.pt = [px, py]; tip.ang = ang;
      next += step;
    }
    acc += seg;
  }
  let head: React.ReactNode = null;
  if (!gaze && p >= 1) {
    const [tx, ty] = w[w.length - 1], a = tip.ang, k = prog(f, d.at + frames, 4);
    const l = 30 * k, sp = 0.55;
    head = <path d={`M${tx - Math.cos(a - sp) * l} ${ty - Math.sin(a - sp) * l}L${tx} ${ty}L${tx - Math.cos(a + sp) * l} ${ty - Math.sin(a + sp) * l}`} fill="none" stroke={c} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" />;
  }
  return <g>{out}{head}</g>;
};

/** one mark by kind (also registered in the doodle switch in doodles.tsx). */
export const HandMark: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  switch (d.kind) {
    case "thread": return <Thread d={d} f={f} />;
    case "ink_ring": return <InkRing d={d} f={f} />;
    case "ink_strike": return <InkStrike d={d} f={f} />;
    case "ink_underline": return <InkUnderline d={d} f={f} />;
    case "tally": return <Tally d={d} f={f} />;
    case "route": return <Route d={d} f={f} />;
    default: return null;
  }
};
export const HAND_KINDS = ["thread", "ink_ring", "ink_strike", "ink_underline", "tally", "route"];
export const isHandKind = (k: string) => HAND_KINDS.includes(k);
void clamp;
