// Blind Bartimaeus (Desert Storybook) - motion layer v1 "THE ROAD STOPS".
// Spec: poc_desert_storybook_heroes/bartimaeus/motion_v1/MOTION_DESIGN.md (Fable, 2026-11-14). $0, pure code.
// Base = film/bartimaeus_final_v1.mp4 (video only, public/bart/base.mp4), 1.0x, never re-cut. Audio muxed after render.
// Word frames = faster-whisper alignment (motion_v1/words.json), not the spec's ~ estimates.
// Layers: Stage(base + grade + punch/shake/drift) / DARK / ROAD / MARKS / TYPE / TRANS / GRAIN. All frames ABSOLUTE @30.
import React, { useEffect, useState } from "react";
import { AbsoluteFill, Easing, OffthreadVideo, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";

export const BV_FPS = 30;
export const BV_FRAMES = 2375;

// ---------- palette / type ----------
const PAPER = "#F6E9CC", SAND = "#E3C48D", UMBER = "#2E211A", MAROON = "#7A2E22", SAGE = "#5E7F6C", GOLD = "#E9B043", GLOW = "#FFF2C9";
const DISPLAY = "Fraunces, Georgia, serif";
const NOTE = "Kalam, cursive";
const FULL: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: 1920, overflow: "visible" };

// ---------- math ----------
type Pt = [number, number];
const clampO = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (f: number, a: number, b: number, from: number, to: number, easing?: (t: number) => number) =>
  interpolate(f, [a, b], [from, to], { ...clampO, easing });
const OUT = Easing.out(Easing.cubic);
const SINE = Easing.inOut(Easing.sin);
const BACK = Easing.out(Easing.back(1.4));
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const mod = (a: number, n: number) => ((a % n) + n) % n;
const rad = (d: number) => (d * Math.PI) / 180;

// ---------- cuts ----------
const CUT = [0, 90, 150, 300, 450, 624, 798, 900, 1011, 1152, 1254, 1344, 1470, 1680, 1830, 1950, 2070, BV_FRAMES];
const SHOT = ["s01", "s02", "s03", "s04", "s14", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s12", "s13", "s15", "s16", "s17"];
const shotIdx = (f: number) => { let i = 0; while (i < SHOT.length - 1 && f >= CUT[i + 1]) i++; return i; };
const HALT1 = 768, RESTART = 888, HALT2 = 2190, OPEN = 1470;

// ---------- face guards (ellipse cx,cy,rx,ry | box x1,y1,x2,y2) ----------
type G = { e?: [number, number, number, number]; b?: [number, number, number, number] };
const E = (cx: number, cy: number, rx: number, ry: number): G => ({ e: [cx, cy, rx, ry] });
const Bx = (x1: number, y1: number, x2: number, y2: number): G => ({ b: [x1, y1, x2, y2] });
const GUARD: Record<string, G[]> = {
  s01: [E(518, 560, 135, 165), Bx(150, 650, 460, 900), Bx(640, 730, 940, 960), Bx(105, 1350, 350, 1640)],
  s02: [E(385, 225, 95, 115), E(615, 335, 75, 95), E(765, 265, 90, 110), Bx(700, 265, 840, 440), E(1000, 290, 75, 95), E(45, 375, 55, 75),
    E(370, 455, 48, 58), E(480, 470, 48, 58), E(435, 540, 32, 38), E(335, 975, 135, 135), E(530, 575, 55, 75), Bx(480, 1070, 690, 1200)],
  s03: [E(262, 1070, 75, 90), Bx(320, 830, 1080, 1010)],
  s04: [E(585, 760, 75, 100), Bx(0, 800, 1080, 1060)],
  s14: [Bx(280, 420, 830, 620)],
  s05: [Bx(0, 330, 1080, 770), Bx(0, 40, 140, 300)], // measured on the clip f630-795: he drifts left; band covers every face + his hands
  s06: [Bx(360, 250, 700, 1350), Bx(0, 470, 230, 620), Bx(650, 470, 1080, 620), E(60, 740, 75, 95), E(990, 890, 85, 105)],
  s07: [E(662, 403, 85, 110), E(960, 440, 65, 75), E(370, 520, 75, 90), E(206, 600, 65, 80)],
  s08: [E(653, 545, 80, 90), E(990, 455, 60, 60), E(350, 930, 60, 50), Bx(0, 960, 450, 1080), Bx(620, 960, 1080, 1080)],
  s09: [E(538, 280, 105, 125), E(768, 500, 90, 105), Bx(370, 870, 530, 980), Bx(0, 660, 1080, 830), Bx(600, 1150, 900, 1260)],
  s10: [Bx(160, 220, 705, 870), Bx(560, 1000, 790, 1650)],
  s11: [E(480, 270, 95, 120), E(700, 460, 85, 100), E(640, 700, 50, 50), E(100, 600, 60, 60), E(52, 770, 60, 60), E(215, 640, 60, 60), E(865, 680, 60, 60), E(985, 590, 60, 60)],
  s12: [E(720, 770, 195, 235), Bx(560, 700, 790, 815), Bx(0, 40, 500, 1100)],
  s13: [E(317, 655, 65, 75), E(625, 440, 60, 70)],
  s15: [Bx(215, 710, 515, 1545), E(705, 1460, 40, 40)],
  s16: [Bx(178, 566, 615, 1240)],
  s17: [E(413, 460, 85, 105), E(722, 690, 80, 95), Bx(440, 430, 700, 700), E(710, 558, 50, 50)],
};

// ---------- fonts ----------
const useFonts = () => {
  const [h] = useState(() => delayRender("bart-fonts"));
  useEffect(() => {
    Promise.all([
      new FontFace("Fraunces", `url(${staticFile("Fraunces.ttf")})`, { weight: "100 900", style: "normal" }).load(),
      new FontFace("Fraunces", `url(${staticFile("Fraunces-Italic.ttf")})`, { weight: "100 900", style: "italic" }).load(),
      new FontFace("Kalam", `url(${staticFile("Kalam-Bold.ttf")})`, { weight: "700" }).load(),
    ]).then((ff) => { ff.forEach((x) => (document as any).fonts.add(x)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

// ---------- shared SVG defs ----------
const Defs: React.FC = () => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <filter id="gouache" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={3} />
        <feDisplacementMap in="SourceGraphic" scale={7} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="ragged" x="-20%" y="-5%" width="140%" height="110%">
        <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves={3} seed={11} />
        <feDisplacementMap in="SourceGraphic" scale={60} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={1} seed={7} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
    </defs>
  </svg>
);

const GuardMask: React.FC<{ id: string; shot: string }> = ({ id, shot }) => (
  <mask id={id} maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
    <rect x={0} y={0} width={1080} height={1920} fill="white" />
    {(GUARD[shot] || []).map((g, i) => g.e
      ? <ellipse key={i} cx={g.e[0]} cy={g.e[1]} rx={g.e[2]} ry={g.e[3]} fill="black" />
      : <rect key={i} x={g.b![0]} y={g.b![1]} width={g.b![2] - g.b![0]} height={g.b![3] - g.b![1]} fill="black" />)}
  </mask>
);

// =====================================================================
// D6 STAGE
// =====================================================================
const PUNCH: [number, number, number, number][] = [ // at, s, ox, oy
  [300, 1.04, 585, 760], [664, 1.05, 560, 520], [1077, 1.06, 620, 560]];
const SHAKE: [number, number, number][] = [[695, 7, 14], [1077, 6, 10]];
const DRIFT: Record<string, [number, number, number, number]> = { // s0, s1, ox, oy
  s01: [1.04, 1.0, 540, 600], s03: [1.0, 1.03, 540, 960], s14: [1.0, 1.03, 540, 960], s09: [1.0, 1.02, 540, 700],
  s10: [1.0, 1.03, 530, 600], s12: [1.0, 1.03, 677, 756] };
const stage = (f: number) => {
  const i = shotIdx(f), sh = SHOT[i];
  let s = 1, ox = 540, oy = 960;
  const d = DRIFT[sh];
  if (d) {
    const end = sh === "s01" ? 20 : CUT[i + 1];
    s = lerp(f, CUT[i], end, d[0], d[1]); ox = d[2]; oy = d[3];
  }
  for (const [at, ps, px, py] of PUNCH) {
    if (f < at || f > at + 26) continue;
    const k = f < at + 4 ? lerp(f, at, at + 4, 0, 1) : lerp(f, at + 4, at + 26, 1, 0, OUT);
    s *= 1 + (ps - 1) * k; ox = px; oy = py;
  }
  let tx = 0, ty = 0;
  for (const [at, amp, n] of SHAKE) {
    const k = f - at;
    if (k < 0 || k > n) continue;
    tx += amp * (1 - k / n) * Math.sin(k * 2.9); ty += amp * (1 - k / n) * Math.cos(k * 3.7);
  }
  return { s, ox, oy, tx, ty };
};
const grade = (f: number) => {
  const sat = f < OPEN ? 0.86 : lerp(f, OPEN, OPEN + 50, 0.86, 1.06, OUT);
  const br = f < OPEN ? 0.97 : lerp(f, OPEN, OPEN + 50, 0.97, 1.02, OUT);
  return `saturate(${sat.toFixed(3)}) brightness(${br.toFixed(3)})`;
};

// =====================================================================
// D3 THE DARK
// =====================================================================
const darkT = (f: number): number | null => {
  const sh = SHOT[shotIdx(f)];
  if (f >= OPEN) return f < OPEN + 50 ? lerp(f, OPEN, OPEN + 50, 190, -200, OUT) : null;
  const base: Record<string, number> = { s01: 150, s02: 150, s03: 60, s04: 60, s14: 60, s05: 150, s06: 60, s07: 60, s08: 150, s09: 100, s10: 150, s11: 100 };
  let T = base[sh] ?? 60;
  if (sh === "s02" && f < 98) T = lerp(f, 90, 98, 260, 150, OUT); // Press
  if (sh === "s08" && f >= 1077) T = lerp(f, 1077, 1087, 150, 100, OUT);
  if (sh === "s11" && f >= 1464) T = lerp(f, 1464, 1470, 100, 190);
  return T;
};
const roundedRect = (x0: number, y0: number, x1: number, y1: number, r: number, N: number): Pt[] => {
  r = Math.max(0, Math.min(r, (x1 - x0) / 2, (y1 - y0) / 2));
  const w = x1 - x0 - 2 * r, h = y1 - y0 - 2 * r, arc = (Math.PI / 2) * r;
  const segs: { len: number; at: (u: number) => Pt }[] = [
    { len: w, at: (u) => [x0 + r + u * w, y0] },
    { len: arc, at: (u) => [x1 - r + r * Math.sin(u * Math.PI / 2), y0 + r - r * Math.cos(u * Math.PI / 2)] },
    { len: h, at: (u) => [x1, y0 + r + u * h] },
    { len: arc, at: (u) => [x1 - r + r * Math.cos(u * Math.PI / 2), y1 - r + r * Math.sin(u * Math.PI / 2)] },
    { len: w, at: (u) => [x1 - r - u * w, y1] },
    { len: arc, at: (u) => [x0 + r - r * Math.sin(u * Math.PI / 2), y1 - r + r * Math.cos(u * Math.PI / 2)] },
    { len: h, at: (u) => [x0, y1 - r - u * h] },
    { len: arc, at: (u) => [x0 + r - r * Math.cos(u * Math.PI / 2), y0 + r - r * Math.sin(u * Math.PI / 2)] },
  ];
  const total = segs.reduce((a, s) => a + s.len, 0), pts: Pt[] = [];
  for (let k = 0; k < N; k++) {
    let d = (k / N) * total, j = 0;
    while (j < segs.length - 1 && d > segs[j].len) { d -= segs[j].len; j++; }
    pts.push(segs[j].at(segs[j].len ? d / segs[j].len : 0));
  }
  return pts;
};
const holePath = (T: number) => {
  const pts = roundedRect(T, T, 1080 - T, 1920 - T, 120, 120);
  const cx = 540, cy = 960;
  const w = pts.map((p, k) => {
    const off = 22 * Math.sin(k * 0.9) + 12 * Math.sin(k * 2.3);
    const dx = p[0] - cx, dy = p[1] - cy, L = Math.hypot(dx, dy) || 1;
    return [p[0] - (dx / L) * off, p[1] - (dy / L) * off] as Pt;
  });
  return "M" + w.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join("L") + "Z";
};
const Dark: React.FC<{ f: number }> = ({ f }) => {
  const T = darkT(f);
  if (T === null) return null;
  const outer = "M-40,-40H1120V1960H-40Z";
  return (
    <svg style={{ ...FULL, mixBlendMode: "multiply" }} viewBox="0 0 1080 1920">
      {/* no FaceGuard on the edge: hard guard boxes cut square notches into it (QC f700/f800) */}
      <g>
        <path d={outer + holePath(T)} fillRule="evenodd" fill={UMBER} opacity={0.58} />
        <path d={outer + holePath(T + 60)} fillRule="evenodd" fill={UMBER} opacity={0.25} />
      </g>
    </svg>
  );
};

// =====================================================================
// D1 THE ROAD (dust strokes / gold motes)
// =====================================================================
type Zone = "ground" | "left" | "right" | "all";
type RoadCfg = { dir: number; speed: number; gain: number; zones: Zone[]; color: string; motes?: boolean; n?: number; bob?: boolean };
const ROADCFG = (f: number): RoadCfg | null => {
  const sh = SHOT[shotIdx(f)];
  switch (sh) {
    case "s01": return { dir: 180, speed: 5, gain: 0.8, zones: ["ground"], color: SAND };
    case "s02": return { dir: 180, speed: 5, gain: f < 96 ? 0.8 : lerp(f, 96, 102, 0.8, 0.3), zones: ["ground"], color: SAND };
    case "s03": return { dir: 160, speed: 4, gain: 1, zones: ["ground", "right"], color: SAND };
    case "s04": return { dir: 90, speed: 5, gain: 1, zones: ["ground", "left", "right"], color: SAND };
    case "s05": return { dir: 0, speed: 6, gain: 1, zones: ["ground", "left", "right"], color: SAND };
    case "s06": return { dir: 0, speed: 6, gain: 0.6, zones: ["ground", "left", "right"], color: SAND };
    case "s07": return { dir: 180, speed: 3, gain: 0.7, zones: ["ground"], color: SAND };
    case "s12": return f < 1500 ? null : { dir: -90, speed: 1.6, gain: lerp(f, 1500, 1530, 0, 0.8), zones: ["all"], color: GOLD, motes: true, n: 60 };
    case "s13": return { dir: -90, speed: 4, gain: 0.9, zones: ["ground", "left", "right"], color: GOLD };
    case "s16": return f < 2010 ? null : { dir: -90, speed: 1.6, gain: lerp(f, 2010, 2040, 0, 0.8), zones: ["all"], color: GOLD, motes: true, n: 24 };
    case "s17": return { dir: 0, speed: 3, gain: 0.7, zones: ["ground", "right"], color: GOLD };
    default: return null;
  }
};
// road clock: distance travelled, 0 while halted, ramps back 888-900.
const ROADCLK: number[] = (() => {
  const c = [0];
  for (let f = 1; f <= BV_FRAMES; f++) {
    let v = 1;
    if (f >= HALT1 && f < RESTART) v = 0;
    else if (f >= RESTART && f < RESTART + 12) v = (f - RESTART) / 12;
    else if (f >= HALT2 && f < 2200) v = 0;
    else if (f >= 2200) v = 0;
    c.push(c[f - 1] + v);
  }
  return c;
})();
const halted = (f: number) => (f >= HALT1 && f < RESTART) || f >= HALT2;
const ZBOX: Record<Zone, [number, number, number, number]> = {
  ground: [-120, 1500, 1200, 1900], left: [0, 250, 110, 1500], right: [970, 250, 1080, 1500], all: [0, 0, 1080, 1920] };
const lens = (L: number, t: number) => `M${-L / 2},0Q0,${-t} ${L / 2},0Q0,${t} ${-L / 2},0Z`;

const Strokes: React.FC<{ f: number; cfg: RoadCfg; seed?: number; maskId?: string }> = ({ f, cfg, seed = 0, maskId }) => {
  const n = cfg.n ?? 46, out: React.ReactNode[] = [];
  const clk = cfg.motes ? f : ROADCLK[Math.min(f, BV_FRAMES)];
  const bob = cfg.motes || halted(f) ? 0 : -10 * Math.abs(Math.sin((Math.PI * f) / 16));
  for (let i = 0; i < n; i++) {
    const z = cfg.zones[i % cfg.zones.length];
    const [x0, y0, x1, y1] = ZBOX[z], w = x1 - x0, h = y1 - y0;
    const sp = cfg.speed * (0.7 + hash(i + 2 + seed) * 0.6);
    let vx = Math.cos(rad(cfg.dir)) * sp, vy = Math.sin(rad(cfg.dir)) * sp;
    let ang = cfg.dir;
    if (z === "left" || z === "right") { // lanes run along their long axis
      const sgn = Math.abs(vy) > 0.3 * sp ? Math.sign(vy) : 1;
      vx = 0; vy = sgn * sp * 0.8; ang = sgn > 0 ? 90 : -90;
    }
    let x = x0 + mod(hash(i + 31 + seed) * w + vx * clk, w);
    let y = y0 + mod(hash(i + 57 + seed) * h + vy * clk, h);
    if (cfg.motes) x += 6 * Math.sin(f / 40 + i);
    const L = (70 + hash(i + seed) * 130) * (cfg.motes ? 0.35 : 1);
    const t = (8 + hash(i + 9 + seed) * 14) * (cfg.motes ? 0.8 : 1);
    const op = (0.3 + hash(i + 5 + seed) * 0.35) * cfg.gain * (cfg.motes ? 1.4 : 1);
    out.push(
      <g key={i} transform={`translate(${x.toFixed(1)},${(y + bob).toFixed(1)}) rotate(${ang})`} opacity={Math.min(1, op)}>
        <path d={lens(L, t)} fill={cfg.color} />
        {cfg.motes ? <path d={lens(L * 0.5, t * 0.45)} fill={GLOW} /> : null}
      </g>);
  }
  return <g mask={maskId ? `url(#${maskId})` : undefined} filter="url(#gouache)">{out}</g>;
};
const Road: React.FC<{ f: number }> = ({ f }) => {
  const cfg = ROADCFG(f), sh = SHOT[shotIdx(f)];
  const extra = sh === "s17" ? { dir: -90, speed: 1.0, gain: 0.7, zones: ["all" as Zone], color: GOLD, motes: true, n: 30 } : null;
  if (!cfg && !extra) return null;
  return (
    <svg style={FULL} viewBox="0 0 1080 1920">
      <defs><GuardMask id="gr" shot={sh} /></defs>
      {cfg ? <Strokes f={f} cfg={cfg} maskId="gr" /> : null}
      {extra ? <Strokes f={f} cfg={extra} seed={400} maskId="gr" /> : null}
    </svg>
  );
};

// =====================================================================
// D2 CRY rings, D5 road line, marks
// =====================================================================
const arcPath = (cx: number, cy: number, r: number, a: number, span: number) => {
  const a0 = rad(a - span / 2), a1 = rad(a + span / 2);
  return `M${cx + r * Math.cos(a0)},${cy + r * Math.sin(a0)}A${r},${r} 0 0 1 ${cx + r * Math.cos(a1)},${cy + r * Math.sin(a1)}`;
};
const Ring: React.FC<{ f: number; at: number; M: Pt; a: number; r0: number; r1: number; col?: string; w?: number; edge?: number }> =
  ({ f, at, M, a, r0, r1, col = MAROON, w = 30, edge = 8 }) => {
    const k = f - at;
    if (k < 0 || k > 26) return null;
    const r = lerp(k, 0, 26, r0, r1, OUT), sw = k < 16 ? w : lerp(k, 16, 26, w, 6);
    return (
      <g filter="url(#gouache)">
        <path d={arcPath(M[0], M[1], r + sw / 2, a, 110)} stroke={PAPER} strokeWidth={edge} fill="none" strokeLinecap="round" />
        <path d={arcPath(M[0], M[1], r, a, 110)} stroke={col} strokeWidth={sw} fill="none" strokeLinecap="round" />
      </g>);
  };
const Cry: React.FC<{ f: number; M: Pt; a: number; n: number; at: number; r0: number; r1: number }> = (p) => (
  <>{Array.from({ length: p.n }, (_, i) => <Ring key={i} f={p.f} at={p.at + i * 5} M={p.M} a={p.a} r0={p.r0} r1={p.r1} />)}</>
);
const catmull = (P: Pt[], u: number): Pt => {
  const n = P.length - 1; if (u >= 1) return P[n];
  const t = Math.max(0, u) * n, i = Math.floor(t), k = t - i;
  const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(n, i + 2)];
  const c = (a: number, b: number, c2: number, d: number) =>
    0.5 * (2 * b + (-a + c2) * k + (2 * a - 5 * b + 4 * c2 - d) * k * k + (-a + 3 * b - 3 * c2 + d) * k * k * k);
  return [c(p0[0], p1[0], p2[0], p3[0]), c(p0[1], p1[1], p2[1], p3[1])];
};
const RoadLine: React.FC<{ f: number; P: Pt[]; at: number; per: number; until?: number }> = ({ f, P, at, per, until }) => {
  if (f < at || (until && f >= until)) return null;
  // sample by arc length: dash every 60 px
  const S: Pt[] = []; for (let k = 0; k <= 400; k++) S.push(catmull(P, k / 400));
  const cum = [0]; for (let k = 1; k < S.length; k++) cum.push(cum[k - 1] + Math.hypot(S[k][0] - S[k - 1][0], S[k][1] - S[k - 1][1]));
  const total = cum[cum.length - 1], nd = Math.floor(total / 60), shown = Math.min(nd, Math.floor((f - at) / per) + 1);
  const out: React.ReactNode[] = [];
  for (let d = 0; d < shown; d++) {
    const target = d * 60 + 17; let k = 0; while (k < cum.length - 1 && cum[k] < target) k++;
    const p = S[k], q = S[Math.min(S.length - 1, k + 1)], ang = Math.atan2(q[1] - p[1], q[0] - p[0]) * 180 / Math.PI;
    out.push(<rect key={d} x={-17} y={-6} width={34} height={12} rx={5} fill={PAPER} stroke={UMBER} strokeWidth={4}
      transform={`translate(${p[0].toFixed(1)},${p[1].toFixed(1)}) rotate(${ang.toFixed(1)})`} />);
  }
  return <g filter="url(#gouache)">{out}</g>;
};
const taper = (L: number, t: number) => `M0,${-t / 2}L${L},0L0,${t / 2}Q${-t},0 0,${-t / 2}Z`;

const Marks: React.FC<{ f: number }> = ({ f }) => {
  const sh = SHOT[shotIdx(f)];
  return (
    <svg style={FULL} viewBox="0 0 1080 1920">
      <defs><GuardMask id="gm" shot={sh} /></defs>
      <g mask="url(#gm)">
        {sh === "s01" ? <><Cry f={f} M={[518, 610]} a={-90} n={3} at={8} r0={140} r1={520} />
          <Cry f={f} M={[518, 610]} a={-90} n={3} at={58} r0={140} r1={520} /></> : null}
        {sh === "s02" && f < 106 ? (
          <g transform={`translate(0,1010) scale(1,${lerp(f, 96, 104, 1, 0.02, OUT)}) translate(0,-1010)`} filter="url(#gouache)">
            <path d={arcPath(350, 1010, 260, -60, 110)} stroke={MAROON} strokeWidth={30} fill="none" strokeLinecap="round" />
          </g>) : null}
        {sh === "s14" ? <>
          <RoadLine f={f} at={456} per={2} P={[[538, 1680], [672, 1363], [662, 1277], [538, 1162], [614, 1037], [614, 902], [480, 826]]} />
          {f >= 509 ? <g filter="url(#gouache)" stroke={UMBER} strokeWidth={12} strokeLinecap="round">
            <line x1={480} y1={698} x2={480} y2={698 + 84 * lerp(f, 509, 514, 0, 1)} />
            <line x1={452} y1={724} x2={452 + 56 * lerp(f, 514, 519, 0, 1)} y2={724} />
          </g> : null}</> : null}
        {sh === "s05" ? <Cry f={f} M={[440, 540]} a={-50} n={5} at={695} r0={180} r1={1500} /> : null}
        {(sh === "s07" || (sh === "s08" && f < 1022)) ? <>
          {[986, 994].map((at) => <Ring key={at} f={f} at={at} M={[1000, 430]} a={180} r0={80} r1={700} col={SAGE} w={22} edge={6} />)}</> : null}
        {sh === "s08" && f >= 1077 && f < 1100 ? (
          <g filter="url(#gouache)" opacity={lerp(f, 1088, 1100, 1, 0)}>
            {[-150, -165, 180, 165, 150].map((a, i) => (
              <path key={i} d={taper((300 + hash(i + 70) * 220) * lerp(f, 1077, 1087, 0.1, 1, OUT), 18)} fill={MAROON}
                transform={`translate(300,560) rotate(${a})`} />))}
          </g>) : null}

        {sh === "s13" ? <RoadLine f={f} at={1795} per={8} until={1824} P={[[317, 1580], [470, 1330], [590, 1080], [615, 820]]} /> : null}
        {sh === "s16" && f >= 2021 ? (() => {
          const top = lerp(f, 2021, 2081, 1920, 700, SINE);
          return <g>
            <defs><linearGradient id="wash" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stopColor={GLOW} stopOpacity={0.28} /><stop offset="1" stopColor={GLOW} stopOpacity={0} /></linearGradient></defs>
            <rect x={0} y={top} width={1080} height={1920 - top} fill="url(#wash)" />
          </g>;
        })() : null}
      </g>
    </svg>
  );
};


// D3 OPEN light: soft warm bloom from his eyes (a thin ring read as a UI circle in QC f1478).
const Bloom: React.FC<{ f: number }> = ({ f }) => {
  const k = f - OPEN;
  if (k < 0 || k > 90) return null;
  const r = lerp(k, 0, 50, 260, 1500, OUT), op = k < 8 ? lerp(k, 0, 8, 0, 0.55) : lerp(k, 8, 90, 0.55, 0, SINE);
  return (
    <svg style={{ ...FULL, mixBlendMode: "screen" }} viewBox="0 0 1080 1920">
      <defs>
        <radialGradient id="bl" cx={677} cy={756} r={r} gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor={GLOW} stopOpacity={0.9} /><stop offset="0.55" stopColor={GOLD} stopOpacity={0.35} /><stop offset="1" stopColor={GOLD} stopOpacity={0} />
        </radialGradient>
        <filter id="feather"><feGaussianBlur stdDeviation={45} /></filter>
        <mask id="hairOff" maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
          <rect width={1080} height={1920} fill="white" />
          <rect x={-100} y={-100} width={620} height={1250} fill="black" filter="url(#feather)" />
        </mask>
      </defs>
      <rect width={1080} height={1920} fill="url(#bl)" opacity={op} mask="url(#hairOff)" />
    </svg>);
};

// =====================================================================
// D4 LETTERING
// =====================================================================
type Mode = "stamp" | "set" | "still";
type Wd = { t: string; at: number; col?: string };
type RowP = { f: number; x: number; y: number; align?: "center" | "left" | "right"; words: Wd[]; size: number; font?: "display" | "kjv" | "note";
  mode: Mode; col?: string; stroke?: string; out?: [number, number]; until?: number; rot?: number; ls?: number; noOutline?: boolean; maxW?: number };
const Row: React.FC<RowP> = (p) => {
  const { f } = p;
  if (f < p.words[0].at - 1 || (p.until !== undefined && f >= p.until)) return null;
  const fam = p.font === "note" ? NOTE : DISPLAY;
  const italic = p.font === "kjv";
  const wght = p.font === "kjv" ? 600 : 800;
  const chars = p.words.map((w) => w.t).join(" ").length;
  const est = chars * p.size * (p.font === "note" ? 0.5 : italic ? 0.5 : 0.68) + chars * (p.ls ?? 2);
  const size = Math.min(p.size, p.size * ((p.maxW ?? 960) / est));
  const outOp = p.out ? lerp(f, p.out[0], p.out[1], 1, 0) : 1;
  if (outOp <= 0) return null;
  const stroke = p.noOutline ? (p.font === "note" ? 4 : 0) : 10;
  const strokeCol = p.stroke ?? UMBER;
  const base: React.CSSProperties = {
    fontFamily: fam, fontSize: size, fontStyle: italic ? "italic" : "normal", fontWeight: p.font === "note" ? 700 : wght,
    fontVariationSettings: p.font === "note" ? undefined : `'opsz' 144, 'SOFT' 100, 'wght' ${wght}`,
    letterSpacing: p.ls ?? (p.font === "display" || !p.font ? 2 : 0), lineHeight: 1, whiteSpace: "pre",
  };
  const tx = p.align === "left" ? "0%" : p.align === "right" ? "-100%" : "-50%";
  return (
    <div style={{ position: "absolute", left: p.x, top: p.y, transform: `translate(${tx},-50%) rotate(${p.rot ?? 0}deg)`, display: "flex",
      gap: size * 0.28, opacity: outOp, filter: "url(#gouache)" }}>
      {p.words.map((w, i) => {
        if (f < w.at) return <span key={i} style={{ ...base, visibility: "hidden" }}>{w.t}</span>;
        const k = f - w.at;
        let sc = 1, op = 1, dy = 0, r = 0;
        if (p.mode === "stamp") { sc = lerp(k, 0, 6, 1.28, 1, BACK); r = lerp(k, 0, 6, (hash(i + w.at) - 0.5) * 6, 0, OUT); }
        if (p.mode === "set") { op = lerp(k, 0, 8, 0, 1, OUT); dy = lerp(k, 0, 8, 10, 0, OUT); }
        const col = w.col ?? p.col ?? PAPER;
        return (
          <span key={i} style={{ position: "relative", display: "inline-block", transform: `translateY(${dy}px) scale(${sc}) rotate(${r}deg)`, opacity: op }}>
            {stroke ? <span style={{ ...base, position: "absolute", left: 5, top: 6, color: UMBER, opacity: 0.45, WebkitTextStroke: `${stroke * 2}px ${UMBER}`, strokeLinejoin: "round" as any }}>{w.t}</span> : null}
            {stroke ? <span style={{ ...base, position: "absolute", left: 0, top: 0, color: strokeCol, WebkitTextStroke: `${stroke * 2}px ${strokeCol}` }}>{w.t}</span> : null}
            <span style={{ ...base, position: "relative", color: col }}>{w.t}</span>
          </span>);
      })}
    </div>
  );
};
const words = (s: string, ats: number[], cols?: (string | undefined)[]): Wd[] => s.split(" ").map((t, i) => ({ t, at: ats[Math.min(i, ats.length - 1)], col: cols?.[i] }));

const Ribbon: React.FC<{ f: number; at: number; x0: number; y0: number; x1: number; y1: number; col: string; until: number }> = ({ f, at, x0, y0, x1, y1, col, until }) => {
  if (f < at || f >= until) return null;
  const w = (x1 - x0) * lerp(f, at, at + 10, 0, 1, OUT), h = y1 - y0, n = 28;
  const d = `M${x0},${y0}L${x1},${y0}L${x1 - n},${y0 + h * 0.33}L${x1},${y0 + h * 0.5}L${x1 - n},${y0 + h * 0.67}L${x1},${y1}L${x0},${y1}L${x0 + n},${y0 + h * 0.67}L${x0},${y0 + h * 0.5}L${x0 + n},${y0 + h * 0.33}Z`;
  return (
    <svg style={FULL} viewBox="0 0 1080 1920">
      <defs><clipPath id={`rb${at}`}><rect x={x0 - 10} y={y0 - 20} width={w + 10} height={h + 40} /></clipPath></defs>
      <path d={d} fill={col} opacity={0.88} clipPath={`url(#rb${at})`} filter="url(#gouache)" />
    </svg>);
};
const Swash: React.FC<{ f: number; at: number; x0: number; x1: number; y: number; col: string; until: number }> = ({ f, at, x0, x1, y, col, until }) => {
  if (f < at || f >= until) return null;
  const L = (x1 - x0) * lerp(f, at, at + 8, 0, 1, OUT);
  return <svg style={FULL} viewBox="0 0 1080 1920"><path d={`M${x0},${y}Q${x0 + L / 2},${y - 10} ${x0 + L},${y + 4}L${x0 + L},${y + 8}Q${x0 + L / 2},${y + 6} ${x0},${y + 14}Z`} fill={col} filter="url(#gouache)" /></svg>;
};

const Type: React.FC<{ f: number }> = ({ f }) => {
  const sh = SHOT[shotIdx(f)];
  const end = CUT[shotIdx(f) + 1];
  const R = (p: Omit<RowP, "f" | "until"> & { until?: number }) => <Row f={f} until={p.until ?? end} {...p} />;
  switch (sh) {
    case "s01": return <>
      {R({ x: 540, y: 215, words: [{ t: "Jesus, thou Son of David,", at: 6 }], size: 46, font: "note", mode: "set", noOutline: true })}
      {R({ x: 540, y: 302, words: words("HAVE MERCY", [58, 62]), size: 112, mode: "stamp", col: MAROON, stroke: PAPER })}
      {R({ x: 540, y: 400, words: words("ON ME", [72, 79]), size: 112, mode: "stamp", col: MAROON, stroke: PAPER })}</>;
    case "s02": return R({ x: 790, y: 1010, words: [{ t: "BE QUIET!", at: 130 }], size: 118, mode: "stamp", col: UMBER, stroke: PAPER, rot: -3, maxW: 560 });
    case "s03": return <>
      {R({ x: 720, y: 1420, words: [{ t: "BARTIMAEUS", at: 170 }], size: 104, mode: "stamp", maxW: 640 })}
      <Swash f={f} at={177} x0={420} x1={1010} y={1478} col={MAROON} until={end} />
      {R({ x: 720, y: 1520, words: [{ t: "a blind beggar by the road", at: 221 }], size: 46, font: "note", mode: "set", noOutline: true, maxW: 640 })}
      {R({ x: 700, y: 300, words: [{ t: "JERICHO", at: 260 }], size: 84, mode: "set", ls: 10 })}</>;
    case "s04": return <>
      {R({ x: 540, y: 260, words: [{ t: "“Son of David”", at: 313 }], size: 64, font: "kjv", mode: "set", col: MAROON, stroke: PAPER, out: [392, 402] })}
      {R({ x: 540, y: 330, words: [{ t: "means", at: 331 }], size: 52, font: "note", mode: "set", noOutline: true, out: [392, 402] })}
      {R({ x: 540, y: 440, words: words("GOD'S PROMISED KING", [338, 355, 365]), size: 96, mode: "stamp", out: [392, 402] })}</>;
    case "s14": return <>
      {R({ x: 540, y: 300, words: [{ t: "JERUSALEM", at: 456 }], size: 96, mode: "set", ls: 10 })}
      {R({ x: 540, y: 1240, words: words("WOULD HE STOP", [557, 557, 557]), size: 112, mode: "stamp" })}
      {R({ x: 540, y: 1380, words: words("FOR A BEGGAR?", [574, 574, 574], [undefined, undefined, MAROON]), size: 112, mode: "stamp" })}</>;
    case "s05": return <>
      {R({ x: 535, y: 215, words: [{ t: "Thou Son of David,", at: 695 }], size: 46, font: "note", mode: "set", noOutline: true })}
      {R({ x: 240, y: 265, align: "left", words: words("HAVE MERCY", [739, 744]), size: 124, mode: "stamp", col: MAROON, stroke: PAPER, maxW: 600 })}
      {R({ x: 830, y: 370, align: "right", words: words("ON ME.", [754, 760]), size: 124, mode: "stamp", col: MAROON, stroke: PAPER, maxW: 600 })}</>;
    case "s06": return <>
      {R({ x: 540, y: 1420, words: words("AND JESUS", [800, 804]), size: 104, mode: "still" })}
      {R({ x: 540, y: 1525, words: words("STOOD STILL", [812, 821]), size: 104, mode: "still" })}
      {R({ x: 1010, y: 1310, align: "right", words: [{ t: "Mark 10:49", at: 830 }], size: 38, font: "note", mode: "still", noOutline: true })}</>;
    case "s07": return <>
      {R({ x: 60, y: 250, align: "left", words: words("HE STOPPED", [924, 931]), size: 84, mode: "stamp", maxW: 520 })}
      {R({ x: 60, y: 350, align: "left", words: words("FOR ONE MAN", [940, 951, 959], [undefined, MAROON, MAROON]), size: 78, mode: "stamp", maxW: 470 })}</>;
    case "s08": return R({ x: 600, y: 262, words: words("HE CAME", [1060, 1060]), size: 100, mode: "stamp", out: [1125, 1135] });
    case "s09": return <>
      <Ribbon f={f} at={1158} x0={80} y0={1300} x1={1000} y1={1525} col={SAGE} until={end} />
      {R({ x: 540, y: 1372, words: words("What wilt thou that I", [1170, 1174, 1184, 1194, 1204]), size: 66, font: "kjv", mode: "set", noOutline: true, maxW: 880 })}
      {R({ x: 540, y: 1462, words: words("should do unto thee?", [1210, 1216, 1224, 1237]), size: 66, font: "kjv", mode: "set", noOutline: true, maxW: 880 })}</>;
    case "s10": {
      const st: [string, number, number, number][] = [["Lord,", 1261, 330, 62], ["that I", 1286, 420, 62], ["might", 1294, 510, 62], ["receive", 1304, 600, 62], ["my", 1315, 690, 62], ["sight.", 1324, 800, 84]];
      return <>{st.map(([t, at, y, s]) => <React.Fragment key={t}>{R({ x: 1030, y, align: "right", words: [{ t, at }], size: s, font: "kjv", mode: "set", col: MAROON, stroke: PAPER, maxW: 250 })}</React.Fragment>)}</>;
    }
    case "s11": return <>
      <Ribbon f={f} at={1350} x0={80} y0={1300} x1={1000} y1={1525} col={SAGE} until={end} />
      {R({ x: 540, y: 1372, words: words("Go thy way; thy faith", [1351, 1358, 1365, 1404, 1407]), size: 66, font: "kjv", mode: "set", noOutline: true, maxW: 880 })}
      {R({ x: 540, y: 1462, words: words("hath made thee whole.", [1418, 1437, 1444, 1453]), size: 66, font: "kjv", mode: "set", noOutline: true, maxW: 880 })}</>;
    case "s12": return <>
      {R({ x: 800, y: 265, words: words("AT ONCE HE", [1585, 1590, 1618]), size: 72, mode: "set", maxW: 500 })}
      {R({ x: 800, y: 365, words: words("COULD SEE.", [1624, 1628], [undefined, GOLD]), size: 96, mode: "set", maxW: 500 })}</>;
    case "s13": return <>
      {R({ x: 540, y: 285, words: words("HE FOLLOWED JESUS", [1737, 1756, 1771]), size: 88, mode: "stamp", out: [1790, 1798] })}
      {R({ x: 540, y: 285, words: [{ t: "up the road to Jerusalem", at: 1798 }], size: 48, font: "note", mode: "set", noOutline: true })}</>;
    case "s15": return <>
      {R({ x: 790, y: 560, words: [{ t: "HE DIED", at: 1859 }], size: 84, mode: "still", maxW: 500 })}
      {R({ x: 790, y: 660, words: [{ t: "FOR OUR SINS", at: 1886 }], size: 84, mode: "still", maxW: 500 })}</>;
    case "s16": return R({ x: 540, y: 1440, words: [{ t: "HE ROSE TO LIFE", at: 2021 }], size: 96, mode: "set", col: GOLD, until: 2079 });
    case "s17": return <>
      {R({ x: 540, y: 255, words: words("JESUS STOOD STILL", [2167, 2178, 2195]), size: 84, mode: "still" })}
      {R({ x: 540, y: 350, words: words("FOR ONE MAN.", [2207, 2224, 2232], [undefined, MAROON, MAROON]), size: 84, mode: "still" })}
      {R({ x: 540, y: 1500, words: [{ t: "Mark 10:46-52", at: 2300 }], size: 40, font: "note", mode: "set", noOutline: true })}</>;
    default: return null;
  }
};

// =====================================================================
// D7 TRANSITIONS
// =====================================================================
const DustWipe: React.FC<{ f: number; cut: number; dir: number; col?: string }> = ({ f, cut, dir, col = SAND }) => {
  if (f < cut - 6 || f > cut + 6) return null;
  const u = lerp(f, cut - 6, cut + 6, -1, 1);
  const vert = dir === -90;
  const span = vert ? 1920 + 700 : 1080 + 700;
  const c = u * (span / 2);
  const tf = vert ? `translate(0,${-c})` : `translate(${c},0)`;
  const strokes = Array.from({ length: 20 }, (_, i) => {
    const px = vert ? hash(i + 200) * 1080 : -350 + hash(i + 200) * 700;
    const py = vert ? -350 + hash(i + 210) * 700 : hash(i + 210) * 1920;
    return <path key={i} d={lens(90 + hash(i + 220) * 120, 10 + hash(i + 230) * 12)} fill={col === GOLD ? GLOW : UMBER} opacity={0.35}
      transform={`translate(${vert ? px : 540 + px},${vert ? 960 + py : py}) rotate(${vert ? -90 : 0})`} />;
  });
  return (
    <svg style={FULL} viewBox="0 0 1080 1920">
      <g transform={tf} opacity={0.92}>
        {vert ? <rect x={-60} y={960 - 350} width={1200} height={700} fill={col} filter="url(#ragged)" />
          : <rect x={540 - 350} y={-60} width={700} height={2040} fill={col} filter="url(#ragged)" />}
        <g filter="url(#gouache)">{strokes}</g>
      </g>
    </svg>);
};
const PageSweep: React.FC<{ f: number; cut: number; n: number }> = ({ f, cut, n }) => {
  const a = cut - n / 2, b = cut + n / 2;
  if (f < a || f > b) return null;
  const x = lerp(f, a, b, 1080 + 100, -1300 - 100, SINE); // sheet left edge
  const W = 1300;
  return (
    <svg style={FULL} viewBox="0 0 1080 1920">
      <defs>
        <linearGradient id="shL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stopColor={UMBER} stopOpacity={0.35} /><stop offset="1" stopColor={UMBER} stopOpacity={0} /></linearGradient>
        <linearGradient id="shR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor={UMBER} stopOpacity={0.35} /><stop offset="1" stopColor={UMBER} stopOpacity={0} /></linearGradient>
      </defs>
      <rect x={x - 90} y={0} width={90} height={1920} fill="url(#shL)" />
      <rect x={x + W} y={0} width={90} height={1920} fill="url(#shR)" />
      <path d={`M${x},0Q${x - 60},960 ${x},1920L${x + W},1920Q${x + W - 60},960 ${x + W},0Z`} fill={PAPER} />
      <rect x={x} y={0} width={W} height={1920} filter="url(#grain)" opacity={0.08} style={{ mixBlendMode: "multiply" }} />
    </svg>);
};
const Trans: React.FC<{ f: number }> = ({ f }) => (<>
  <DustWipe f={f} cut={150} dir={0} />
  <DustWipe f={f} cut={450} dir={-90} />
  <PageSweep f={f} cut={624} n={12} />
  <DustWipe f={f} cut={1680} dir={-90} col={GOLD} />
  <PageSweep f={f} cut={2070} n={16} />
</>);

// =====================================================================
export const BartimaeusV1: React.FC<{ debug?: boolean }> = ({ debug }) => {
  useFonts();
  const f = useCurrentFrame();
  const st = stage(f);
  const sh = SHOT[shotIdx(f)];
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Defs />
      <div style={{ ...FULL, transformOrigin: "0 0", filter: grade(f),
        transform: `translate(${st.tx + st.ox * (1 - st.s)}px,${st.ty + st.oy * (1 - st.s)}px) scale(${st.s})` }}>
        <OffthreadVideo src={staticFile("bart/base.mp4")} muted style={{ width: 1080, height: 1920 }} />
      </div>
      <Dark f={f} />
      <Road f={f} />
      <Marks f={f} />
      <Bloom f={f} />
      <AbsoluteFill><Type f={f} /></AbsoluteFill>
      <Trans f={f} />
      <svg style={{ ...FULL, mixBlendMode: "multiply", opacity: 0.05 }} viewBox="0 0 1080 1920"><rect width={1080} height={1920} filter="url(#grain)" /></svg>
      {debug ? <svg style={FULL} viewBox="0 0 1080 1920">{(GUARD[sh] || []).map((g, i) => g.e
        ? <ellipse key={i} cx={g.e[0]} cy={g.e[1]} rx={g.e[2]} ry={g.e[3]} fill="none" stroke="red" strokeWidth={4} />
        : <rect key={i} x={g.b![0]} y={g.b![1]} width={g.b![2] - g.b![0]} height={g.b![3] - g.b![1]} fill="none" stroke="red" strokeWidth={4} />)}
        <text x={20} y={1900} fill="red" fontSize={40}>{`f${f} ${sh}`}</text></svg> : null}
    </AbsoluteFill>
  );
};
