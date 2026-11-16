// comic_kit/core.tsx - shared values + the 4 core devices: ink_stroke, boil, anchor, guard.
// Spec: poc_comic_page/_ELEVATE/formula/design/comic_full/COMIC_FULL_DESIGN.md (section 1). Frames are 30 fps, absolute.
import React from "react";

export type Pt = [number, number];
export type Box = [number, number, number, number]; // x, y, w, h
export const FW = 1080, FH = 1920;
export const INK = "#14100C", BONE = "#F3E9D2", PAPER = "#FAF0D6";
export const PILL_ZONE: Box = [70, 974, 940, 276];
export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const prog = (f: number, at: number, frames: number) => clamp((f - at) / Math.max(1, frames));
export const rad = (d: number) => (d * Math.PI) / 180;

// ---- easing ----
export const bezier = (x1: number, y1: number, x2: number, y2: number) => (x: number) => {
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  let t = x;
  for (let i = 0; i < 8; i++) {
    const e = ((ax * t + bx) * t + cx) * t - x;
    const d = (3 * ax * t + 2 * bx) * t + cx;
    if (Math.abs(e) < 1e-5 || !d) break;
    t -= e / d;
  }
  return ((ay * t + by) * t + cy) * t;
};
export const glide = bezier(0.6, 0, 0.3, 1);
export const settle = bezier(0.3, 0.8, 0.2, 1);
export const outCubic = (t: number) => 1 - Math.pow(1 - clamp(t), 3);
/** "slam": scale 1.30, then 0.97 at +3, then 1.00 at +5. Returns null before `at`. */
export const slam = (f: number, at: number): number | null => {
  const k = f - at;
  if (k < 0) return null;
  if (k >= 5) return 1;
  return k <= 3 ? lerp(1.3, 0.97, k / 3) : lerp(0.97, 1.0, (k - 3) / 2);
};

// ---- seeded noise ----
export const mulberry = (a: number) => () => {
  a |= 0;
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
/** boil: a held mark is drawn twice with two seeds, swapping every `hold` frames. Only marks boil, never pictures. */
export const boilSeed = (f: number, seed: number, hold = 3, sets = 2) => seed + (Math.floor(Math.max(0, f) / hold) % sets) * 7919;

export const plen = (pts: Pt[]) => {
  let L = 0;
  for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  return L;
};
/** +/- amp px seeded wobble along the length (resampled every `step` px). Computed in JS, no feTurbulence. */
export const wobblePts = (pts: Pt[], seed: number, amp = 2, step = 28): Pt[] => {
  const r = mulberry(Math.floor(seed * 9973 + 17));
  const out: Pt[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
    const L = Math.hypot(x1 - x0, y1 - y0) || 1;
    const n = Math.max(1, Math.round(L / step));
    const nx = -(y1 - y0) / L, ny = (x1 - x0) / L;
    for (let k = 0; k < n; k++) {
      const t = k / n;
      const w = i === 0 && k === 0 ? 0 : (r() * 2 - 1) * amp;
      out.push([x0 + (x1 - x0) * t + nx * w, y0 + (y1 - y0) * t + ny * w]);
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
};
export const pathD = (pts: Pt[], close = false) => "M" + pts.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join("L") + (close ? "Z" : "");

// ---- tone: two-tone rule (a mark must read on any picture) ----
export type Tone = "ink" | "bone" | "two";
export const markStyle = (tone: Tone): { fill: string; stroke: string; sw: number } =>
  tone === "ink" ? { fill: INK, stroke: BONE, sw: 5 } : { fill: BONE, stroke: INK, sw: 6 };

/** ink_stroke: the only way a line is drawn. */
export const InkStroke: React.FC<{
  pts: Pt[]; width?: number; seed?: number; tone?: Tone; draw?: [number, number]; f: number; boil?: boolean; amp?: number; close?: boolean; opacity?: number; dash?: string;
}> = ({ pts, width = 8, seed = 1, tone = "ink", draw, f, boil = false, amp = 2, close = false, opacity = 1, dash }) => {
  let p = 1;
  if (draw) {
    if (f < draw[0]) return null;
    p = prog(f, draw[0], draw[1]);
  }
  const w = wobblePts(close ? [...pts, pts[0]] : pts, boil ? boilSeed(f, seed) : seed, amp);
  const L = plen(w);
  const d = pathD(w);
  const da = draw ? `${L}` : dash;
  const off = draw ? L * (1 - p) : 0;
  const common = { fill: "none", strokeLinecap: "square" as const, strokeLinejoin: "miter" as const, strokeDasharray: da, strokeDashoffset: off };
  return (
    <g opacity={opacity}>
      {tone !== "ink" && <path d={d} {...common} stroke={BONE} strokeWidth={tone === "two" ? width + 10 : width} />}
      {tone !== "bone" && <path d={d} {...common} stroke={INK} strokeWidth={width} />}
    </g>
  );
};

// ---- shapes shared by doodles ----
export const wedgePts = (c: Pt, angDeg: number, r0: number, r1: number, w0: number, w1 = 0): Pt[] => {
  const a = rad(angDeg), ux = Math.cos(a), uy = Math.sin(a), nx = -uy, ny = ux;
  return [
    [c[0] + ux * r0 + nx * w0, c[1] + uy * r0 + ny * w0],
    [c[0] + ux * r1 + nx * w1, c[1] + uy * r1 + ny * w1],
    [c[0] + ux * r1 - nx * w1, c[1] + uy * r1 - ny * w1],
    [c[0] + ux * r0 - nx * w0, c[1] + uy * r0 - ny * w0],
  ];
};
export const Poly: React.FC<{ pts: Pt[]; tone: Tone; opacity?: number; scale?: number; about?: Pt }> = ({ pts, tone, opacity = 1, scale = 1, about }) => {
  const m = markStyle(tone === "two" ? "bone" : tone);
  const o = about || [0, 0];
  const q = pts.map((p) => [o[0] + (p[0] - o[0]) * scale, o[1] + (p[1] - o[1]) * scale] as Pt);
  return <path d={pathD(q, true)} fill={m.fill} stroke={m.stroke} strokeWidth={m.sw} strokeLinejoin="miter" opacity={opacity} />;
};
export const blob = (c: Pt, r: number, seed: number, n = 14): Pt[] => {
  const g = mulberry(seed);
  const o: Pt[] = [];
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2, rr = r * (0.75 + g() * 0.5);
    o.push([c[0] + Math.cos(a) * rr, c[1] + Math.sin(a) * rr]);
  }
  return o;
};

// ---- data types (episode.json) ----
export interface ShotSpec { clip: string; t_in: number; f_start: number; cx: number; cy: number; z0: number; z1: number; f_z0: number; f_z1: number; freeze_f?: number | null }
export interface PanelSpec {
  id: string; shot: ShotSpec; box: Box; tilt?: number; border?: number; shadow?: [number, number]; mount?: number; show?: [number, number];
  filter?: { f0: number; f1: number; brightness: number; saturate: number };
}
export interface Move { kind: string; panel?: string; at: number; frames?: number; [k: string]: any }
export interface SceneSpec {
  id: string; type?: "stack" | "split"; f0: number; f1: number; paper?: boolean; page_h?: number; panels: PanelSpec[]; moves?: Move[];
  splash?: { inset: number; width: number }; [k: string]: any;
}
export interface Pos { xy?: Pt; anchor?: { scene: string; panel: string; pic: Pt; track?: string } }
export interface Doodle { kind: string; at: number; until?: number; frames?: number; tone?: Tone; seed?: number; pos?: Pos; [k: string]: any }
export interface TransitionSpec { kind: string; from: string; to: string; at: number; frames: number; [k: string]: any }
export interface Episode {
  fps: number; frames: number; assets: string; scenes: SceneSpec[]; transitions: TransitionSpec[];
  doodles: Doodle[]; pills: { png: string; f0: number; f1: number; box: Box; radius: number }[]; hook?: { png: string; f0: number; f1: number };
  tracks?: Record<string, { f0: number; pts: Pt[] }>; no_draw?: { box: Box; f0: number; f1: number; label: string }[];
}
export const EpCtx = React.createContext<Episode>(null as any);

/** guard: fail-closed list of violations for a set of marks at frame f (used by dev checks; the pixel gate is gates_comic.py). */
export const guardViolations = (ep: Episode, f: number, marks: { box: Box; kind: string }[]): string[] => {
  const out: string[] = [];
  for (const m of marks) {
    for (const z of ep.no_draw || []) {
      if (f >= z.f0 && f < z.f1 && m.box[0] < z.box[0] + z.box[2] && m.box[0] + m.box[2] > z.box[0] && m.box[1] < z.box[1] + z.box[3] && m.box[1] + m.box[3] > z.box[1]) out.push(`${m.kind} hits no-draw ${z.label}`);
    }
  }
  return out;
};
