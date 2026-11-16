// Prophecy 01 "Born in Bethlehem" - film v4: MOTION_DESIGN_v2 (Fable) "The map in the margin".
// One hand-inked map of Judaea comes back three times (far away / close by / the wise men went) and carries the WENT spine.
// Base = the same clips (1.0x, trim only) + the v3 read-along lettering. Pure function of the frame. Voice untouched.
import React from "react";
import { AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore  (read only - v3 owns this file; v4 patches the pills in memory)
import D from "../public/bethlehem/film_v3_data.json";

export const BTH4_FPS = 30;
export const BTH4_FRAMES = 1779;

const GOLD = "#E8A81C", INK = "#141210", CREAM = "#FFEEBE", PAPER = "#FBF8F0", SEPIA = "#2A1A0E", PARCH = "#EFDFB8", SEA = "#9FC3C4";
const PILL_FILL = "rgba(225,225,228,0.588)", PILL_EDGE = "rgba(20,18,16,0.67)";
const F = (s: number) => Math.round(s * 30);
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const L = (f: number, a: number, b: number, x: number, y: number, e?: (t: number) => number) => interpolate(f, [a, b], [x, y], { ...cl, easing: e });
const OUT = Easing.out(Easing.cubic), IN = Easing.in(Easing.cubic), INOUT = Easing.inOut(Easing.cubic), SINE = Easing.inOut(Easing.sin), BACK = Easing.out(Easing.back(1.8));
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const mix = (a: number, b: number, t: number) => a + (b - a) * t;
type P3 = [number, number, number];
const lerpPts = (pts: P3[], t: number): [number, number] => {
  if (t <= pts[0][0]) return [pts[0][1], pts[0][2]];
  for (let i = 0; i < pts.length - 1; i++) if (t <= pts[i + 1][0]) {
    const u = (t - pts[i][0]) / (pts[i + 1][0] - pts[i][0]);
    return [mix(pts[i][1], pts[i + 1][1], u), mix(pts[i][2], pts[i + 1][2], u)];
  }
  const p = pts[pts.length - 1]; return [p[1], p[2]];
};

// ---------- measured tracks (clip time -> px on the 1080x1920 frame) ----------
const P1_TOWN: P3[] = [[0.5, 810, 1490], [3.5, 800, 1490], [6.0, 720, 1480], [9.5, 770, 1436]];
const P3_CAMEL: P3[] = [[0, 640, 1250], [3.05, 580, 1225], [4.5, 537, 1220], [5.67, 442, 1130]]; // camel panel top y, bottom y
const P5_CORE: P3[] = [[2.5, 540, 205], [3.7, 540, 184], [4.3, 540, 174]];
const P5_STAR_BOTTOM: P3[] = [[2.5, 0, 551], [3.7, 0, 486], [4.3, 0, 456]];
const M1_TOWN: [number, number] = [907, 800];
const TOMB_DOOR: [number, number] = [540, 1120];
const LAMP_FLAME: [number, number] = [567, 1085];
const M3_SUN: [number, number] = [162, 553];

// ---------- segments ----------
type Seg = { c: string; a: number; b: number; inPt: number; pre: number; post: number; top?: boolean };
const SEG: Seg[] = [
  { c: "P1", a: 0, b: 4.0, inPt: 0, pre: 0, post: 0.2 },            // 0 hook (the time-scroll covers it by f124)
  { c: "P2", a: 4.0, b: 9.1, inPt: 0, pre: 0, post: 0 },             // 1 Micah page (under the time-scroll until f166)
  { c: "M1", a: 9.1, b: 14.1, inPt: 0, pre: 0, post: 0 },            // 2 Micah points
  { c: "P2", a: 14.1, b: 15.85, inPt: 5.55, pre: 0, post: 0 },       // 3 lamp
  { c: "P2", a: 15.85, b: 17.8, inPt: 8.0, pre: 0, post: 0 },        // 4 Micah's face (map A covers from f534)
  { c: "P3", a: 664 / 30, b: 27.8, inPt: 0, pre: 0, post: 0.1 },       // 5 manger / camels (revealed when map A folds away)
  { c: "P4", a: 27.8, b: 1029 / 30, inPt: 0, pre: 10 / 30, post: 13 / 30 }, // 6 Herod / scribe
  { c: "P1", a: 37.4, b: 1186 / 30, inPt: 1.5, pre: 5 / 30, post: 9 / 30 }, // 7 the experts
  { c: "M2", a: 1236 / 30, b: 43.5, inPt: 0.7, pre: 0, post: 18 / 30, top: true }, // 8 Mary and the child (above map C: star iris)
  { c: "P5", a: 43.5, b: 51.7, inPt: 0, pre: 6 / 30, post: 0, top: true },  // 9 sky / crosses / tomb
  { c: "M3", a: 51.7, b: 59.3, inPt: 0, pre: 0, post: 0, top: true },       // 10 the risen Jesus
];
const clipT = (s: Seg, f: number) => Math.max(0, s.inPt - s.pre) + (f / 30 - (s.a - s.pre));
const frontX = (u: number, y: number) => L(u, 0, 1, -360, 1560) + 0.21 * (y - 960) + 28 * Math.sin(y / 90 + 1.7);
const wipeX = (u: number, y: number) => L(u, 0, 1, 1500, -440) + 0.25 * (y - 960) + 16 * Math.sin(y / 110 + 0.6);

const p1Town = (f: number): [number, number] => lerpPts(P1_TOWN, clipT(f < 600 ? SEG[0] : SEG[7], f));

const segStyle = (i: number, f: number): React.CSSProperties => {
  const st: React.CSSProperties = {};
  switch (i) {
    case 1: if (f >= 265) { st.transform = `scale(${L(f, 265, 272, 1, 2.1, IN)})`; st.transformOrigin = "540px 300px"; } break;
    case 2: st.transform = `scale(${L(f, 273, 283, 1.14, 1, OUT)})`; break;
    case 6: { // gold footprint trail wipe, right -> left
      if (f < 836) {
        const u = INOUT(Math.max(0, Math.min(1, (f - 823) / 12)));
        const pts: string[] = [];
        for (let y = -60; y <= 1980; y += 60) pts.push(`${wipeX(u, y).toFixed(0)}px ${y}px`);
        st.clipPath = `polygon(1100px -60px, ${pts.join(", ")}, 1100px 1980px)`;
      }
      break; }
    case 8: { // soft iris from the Bethlehem star on the map, calm
      const [sx, sy] = irisCentre();
      const r = L(f, 1236, 1260, 0, 1900, INOUT);
      if (r < 1) return { opacity: 0 };
      if (r < 1900) { const m = `radial-gradient(circle at ${sx}px ${sy}px, #000 ${Math.max(0, r - 110)}px, transparent ${r}px)`; st.WebkitMaskImage = m; st.maskImage = m; }
      break; }
    case 9: { // nightfall, top -> bottom, calm
      const e = L(f, 1299, 1323, -160, 2080, SINE);
      if (e < 2080) { const m = `linear-gradient(to bottom, #000 ${e - 160}px, transparent ${e}px)`; st.WebkitMaskImage = m; st.maskImage = m; }
      break; }
  }
  return st;
};

// ---------- hand-drawn helpers ----------
const Rough: React.FC = () => (
  <defs>
    {[0, 1, 2].map((k) => (
      <filter key={k} id={`rg${k}`} filterUnits="userSpaceOnUse" x={-200} y={-200} width={1480} height={2320}>
        <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves={2} seed={3 + k * 7} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={k === 0 ? 7 : 8} xChannelSelector="R" yChannelSelector="G" />
      </filter>))}
  </defs>
);
const boil = (f: number, on = true) => `url(#rg${on ? Math.floor(f / 4) % 3 : 0})`;
// smooth path through points (Catmull-Rom sampled)
const sample = (pts: [number, number][], per = 14): [number, number][] => {
  const o: [number, number][] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let k = 0; k < per; k++) {
      const t = k / per, t2 = t * t, t3 = t2 * t;
      o.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
        0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]);
    }
  }
  o.push(pts[pts.length - 1]); return o;
};
const toD = (d: [number, number][]) => d.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ");
const cum = (d: [number, number][]) => { const c = [0]; for (let i = 1; i < d.length; i++) c.push(c[i - 1] + Math.hypot(d[i][0] - d[i - 1][0], d[i][1] - d[i - 1][1])); return c; };
const along = (d: [number, number][], c: number[], u: number): [number, number, number] => {
  const t = Math.max(0, Math.min(1, u)) * c[c.length - 1];
  let i = 1; while (i < c.length - 1 && c[i] < t) i++;
  const k = (t - c[i - 1]) / Math.max(1e-6, c[i] - c[i - 1]);
  return [mix(d[i - 1][0], d[i][0], k), mix(d[i - 1][1], d[i][1], k), Math.atan2(d[i][1] - d[i - 1][1], d[i][0] - d[i - 1][0])];
};
const dashSegs = (d: [number, number][], c: number[], dash: number, gap: number) => {
  const tot = c[c.length - 1], o: { a: [number, number, number]; b: [number, number, number]; u: number }[] = [];
  for (let t = 0; t < tot; t += dash + gap) o.push({ a: along(d, c, t / tot), b: along(d, c, Math.min(tot, t + dash) / tot), u: t / tot });
  return o;
};
const draw = (p: number) => ({ pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - Math.max(0, Math.min(1, p)) });

const star8 = (r: number, ir = 0.38) => [0, 1, 2, 3, 4, 5, 6, 7].map((i) => { const a = -Math.PI / 2 + i * Math.PI / 4, rr = i % 2 ? r * ir : r; return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`; }).join(" ");
const GStar: React.FC<{ x: number; y: number; land: number; f: number; size?: number; calm?: boolean; op?: number }> = ({ x, y, land, f, size = 60, calm, op = 1 }) => {
  if (f < land) return null;
  const k = f - land;
  const sc = calm ? L(k, 0, 14, 0, 1, SINE) : k < 8 ? (k < 4 ? L(k, 0, 4, 0, 1.3, OUT) : L(k, 4, 8, 1.3, 1, SINE)) : 1 + 0.07 * Math.sin((k - 8) / 40 * Math.PI * 2);
  return (
    <g transform={`translate(${x},${y})`} opacity={op}>
      {!calm && k < 10 && <circle r={L(k, 0, 10, 20, size * 1.5)} fill="none" stroke={INK} strokeWidth={4} opacity={L(k, 0, 10, 1, 0)} />}
      <g transform={`scale(${sc}) rotate(${calm ? 0 : 6 * Math.sin(k / 23)})`}>
        <polygon points={star8(size / 2)} fill="none" stroke={CREAM} strokeWidth={10} strokeLinejoin="round" />
        <polygon points={star8(size / 2)} fill={GOLD} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
      </g>
    </g>
  );
};
// sandal print: 42 long, pointing up (-y)
const SOLE = "M0,-22 C10,-22 13,-9 9,2 C7,6 -7,6 -9,2 C-13,-9 -10,-22 0,-22Z M-7,11 C-7,8 7,8 7,11 C8,17 5,22 0,22 C-5,22 -8,17 -7,11Z";
const Print: React.FC<{ x: number; y: number; ang: number; s?: number; pop: number; gold?: number; f: number; op?: number; side?: number; pulse?: number; blink?: [number, number]; sw?: number }> =
  ({ x, y, ang, s = 1, pop, gold, f, op = 1, side = 0, pulse, blink, sw = 4 }) => {
    if (f < pop) return null;
    const k = f - pop;
    let sc = k < 5 ? (k < 3 ? L(k, 0, 3, 0, 1.25, OUT) : L(k, 3, 5, 1.25, 1)) : 1;
    const g = gold === undefined ? 0 : L(f, gold, gold + 3, 0, 1);
    if (gold !== undefined && f >= gold && f < gold + 6) sc *= 1 + 0.3 * Math.sin((f - gold) / 6 * Math.PI);
    if (pulse !== undefined && f >= pulse && f < pulse + 12) sc *= 1 + 0.3 * Math.sin((f - pulse) / 12 * Math.PI);
    let o = op;
    if (blink && f >= blink[0] && f < blink[1]) o *= 0.62 + 0.38 * Math.cos((f - blink[0]) / 20 * Math.PI * 2);
    return (
      <g transform={`translate(${x},${y}) rotate(${ang * 180 / Math.PI + 90}) translate(${side * 9 * s},0) scale(${sc * s})`} opacity={o}>
        <path d={SOLE} fill={g > 0.5 ? GOLD : "rgba(255,248,230,0.9)"} stroke={INK} strokeWidth={sw} strokeLinejoin="round" />
        
      </g>
    );
  };
const Crown: React.FC<{ p: number; gold?: boolean; w?: number }> = ({ p, gold = true, w = 5 }) => (
  <g>
    <path d="M-34,16 L-40,-16 L-20,2 L0,-26 L20,2 L40,-16 L34,16 Z" fill={gold ? GOLD : "rgba(255,248,230,0.9)"} fillOpacity={L(p, 0.6, 1, 0, 1)} stroke={INK} strokeWidth={w} strokeLinejoin="round" {...draw(p)} />
    <path d="M-33,24 L33,24" stroke={INK} strokeWidth={w} strokeLinecap="round" {...draw(L(p, 0.7, 1, 0, 1))} />
    {gold && p >= 1 && [-40, 0, 40].map((x, i) => <circle key={i} cx={x} cy={i === 1 ? -28 : -18} r={4.5} fill={CREAM} stroke={INK} strokeWidth={2.5} />)}
  </g>
);
const Tag: React.FC<{ text: string; cx: number; cy: number; p: number; size?: number; font?: string; w?: number; gold?: number; right?: boolean }> = ({ text, cx, cy, p, size = 72, font = "FellR", w = 380, gold = 0, right }) => (
  <div style={{ position: "absolute", left: right ? cx - w : cx - w / 2, top: cy - size * 0.7, width: w, height: size * 1.4, textAlign: right ? "right" : "center", clipPath: `inset(-20px ${(1 - Math.max(0, Math.min(1, p))) * 100}% -20px -20px)` }}>
    <span style={{ fontFamily: font, fontSize: size, lineHeight: `${size * 1.4}px`, color: SEPIA, whiteSpace: "nowrap", padding: "0 12px", borderRadius: 10,
      background: gold > 0 ? `rgba(232,168,28,${gold})` : undefined, textShadow: "0 0 6px #EFDFB8, 0 0 6px #EFDFB8, 0 0 10px #EFDFB8" }}>{text}</span>
  </div>
);

// =====================================================================================
//  THE MAP (world units = px at zoom 1; north is up; the east is screen right)
// =====================================================================================
const NAZ: [number, number] = [640, 450], JER: [number, number] = [650, 860], BET: [number, number] = [560, 1230];
const COAST = sample([[262, -40], [240, 160], [215, 400], [186, 700], [150, 1000], [108, 1300], [62, 1600], [20, 1960]]);
const JORDAN = sample([[826, 478], [840, 520], [800, 560], [830, 660], [806, 760], [832, 850], [818, 930], [836, 1002]]);
const MJ = sample([[590, 590], [560, 660], [515, 730], [440, 800], [420, 920], [430, 1080], [468, 1218]]); const MJc = cum(MJ);
const EAST = sample([[1420, 560], [1280, 470], [1150, 520], [1090, 660], [1000, 760], [930, 740], [880, 820], [830, 840], [792, 832]]); const EASTc = cum(EAST);
const ROAD = sample([[664, 872], [692, 960], [676, 1070], [682, 1226]]); const ROADc = cum(ROAD);
const HILLS: [number, number][] = [[470, 300], [760, 640], [520, 700], [720, 760], [380, 640], [330, 880], [740, 1010], [340, 1110], [720, 1250], [430, 1330], [620, 1400], [300, 1420], [520, 1560], [760, 1480], [420, 480], [330, 250]];
const DUNES: [number, number][] = [[960, 380], [1010, 960], [960, 1160], [1000, 1420], [1180, 820], [1230, 400], [1280, 960], [940, 600], [1130, 1200], [1330, 700]];
const WAVES: [number, number][] = [[90, 220], [150, 420], [60, 560], [110, 760], [40, 960], [70, 1180], [20, 1380], [170, 100]];

type Cam = { wx: number; wy: number; s: number; sx: number; sy: number };
const toScreen = (c: Cam, p: [number, number]): [number, number] => [c.sx + (p[0] - c.wx) * c.s, c.sy + (p[1] - c.wy) * c.s];
const camOf = (mode: "A" | "B" | "C", f: number): Cam => {
  if (mode === "A") {
    const k = L(f, 556, 606, 0, 1, INOUT), k2 = L(f, 626, 664, 0, 1, SINE);
    return { wx: mix(640, 560, k) + 10 * k2, wy: mix(470, 960, k) + 30 * k2, s: mix(1.7, 1.0, k) + 0.07 * k2, sx: 540, sy: mix(900, 960, k) };
  }
  if (mode === "B") { const k = L(f, 1030, 1118, 0, 1, SINE); return { wx: 600, wy: 1040, s: mix(1.55, 1.8, k), sx: 540, sy: 800 }; }
  const k = L(f, 1214, 1238, 0, 1, INOUT);
  return { wx: mix(700, 610, k), wy: mix(880, 1040, k), s: mix(0.85, 1.6, k), sx: 540, sy: 800 };
};
const irisCentre = (): [number, number] => { const c = camOf("C", 1260); const p = toScreen(c, BET); return [p[0], p[1] - 128 * c.s]; };

const Town: React.FC<{ kind: "small" | "city"; p: number }> = ({ kind, p }) => {
  const fo = L(p, 0.55, 1, 0, 1);
  const st = { stroke: INK, strokeWidth: 2.7, strokeLinejoin: "round" as const, strokeLinecap: "round" as const };
  if (kind === "small") return (
    <g>
      <path d="M-58,2 C-30,-6 30,-6 58,2" fill="none" {...st} strokeWidth={2.4} {...draw(p * 1.4)} />
      <g fill="#F7EACB" fillOpacity={fo}>
        <path d="M-40,0 L-40,-26 L-14,-26 L-14,0" {...st} {...draw(p * 1.3)} />
        <path d="M-14,0 L-14,-44 L16,-44 L16,0" {...st} {...draw(p * 1.3 - 0.15)} />
        <path d="M16,0 L16,-22 L42,-22 L42,0" {...st} {...draw(p * 1.3 - 0.3)} />
        <path d="M-6,-44 C-6,-58 8,-58 8,-44" {...st} {...draw(p * 1.3 - 0.3)} />
      </g>
      <g opacity={fo} fill={SEPIA}><rect x={-31} y={-14} width={7} height={14} /><rect x={-3} y={-16} width={8} height={16} /><rect x={-4} y={-34} width={5} height={7} /><rect x={25} y={-12} width={7} height={12} /></g>
    </g>);
  return (
    <g>
      <g fill="#F7EACB" fillOpacity={fo}>
        <path d="M-30,-30 L-30,-52 L-8,-52 L-8,-30 M2,-30 C2,-66 40,-66 40,-30" {...st} {...draw(p * 1.3 - 0.25)} />
        <path d="M-62,0 L-62,-34 L-52,-34 L-52,-28 L-42,-28 L-42,-34 L-30,-34 L-30,-28 L-18,-28 L-18,-34 L-6,-34 L-6,-28 L6,-28 L6,-34 L18,-34 L18,-28 L30,-28 L30,-34 L42,-34 L42,-28 L52,-28 L52,-34 L62,-34 L62,0 Z" {...st} {...draw(p * 1.3)} />
        <path d="M-78,0 L-78,-50 L-58,-50 L-58,0 M58,0 L58,-50 L78,-50 L78,0" {...st} {...draw(p * 1.3 - 0.1)} />
      </g>
      <path d="M-10,0 L-10,-14 C-10,-24 10,-24 10,-14 L10,0" fill={SEPIA} fillOpacity={fo} {...st} strokeWidth={2.4} {...draw(p * 1.3 - 0.3)} />
      <path d="M-92,3 C-40,-3 40,-3 92,3" fill="none" {...st} strokeWidth={2.4} {...draw(p * 1.4)} />
    </g>);
};
const Camel: React.FC<{ ph: number }> = ({ ph }) => {
  const sw = (o: number) => 9 * Math.sin(ph + o);
  const leg = (x: number, o: number) => <line x1={x} y1={52} x2={x + sw(o)} y2={80} stroke={SEPIA} strokeWidth={5.5} strokeLinecap="round" />;
  return (
    <g transform="translate(-48,-80)">
      {leg(31, 0)}{leg(40, Math.PI)}{leg(70, Math.PI * 0.5)}{leg(79, Math.PI * 1.5)}
      <path d="M22,50 C16,44 12,32 12,21 C12,14 6,13 1,16 L0,21 C4,23 7,23 8,24 C8,36 11,46 20,54 C36,60 70,60 86,52 L88,60 M86,52 C86,40 76,31 65,31 C61,12 47,13 43,30 C34,27 24,30 22,50 Z" fill={SEPIA} stroke={SEPIA} strokeWidth={3} strokeLinejoin="round" />
      <path d="M40,31 C46,24 60,24 66,32 L64,44 L42,44 Z" fill={GOLD} stroke={SEPIA} strokeWidth={2.5} strokeLinejoin="round" />
    </g>);
};
const Walkers: React.FC<{ ph: number }> = ({ ph }) => (
  <g transform={`translate(0,${-1.5 * Math.abs(Math.sin(ph))})`}>
    <line x1={-25} y1={-46} x2={-27} y2={0} stroke={SEPIA} strokeWidth={3} strokeLinecap="round" />
    <path d="M-14,0 L-10,-34 C-10,-40 -18,-40 -18,-46 C-18,-56 -4,-56 -4,-46 C-4,-40 -9,-40 -8,-34 L-2,0 Z" fill={SEPIA} stroke={SEPIA} strokeWidth={2} strokeLinejoin="round" />
    <path d="M4,0 L8,-28 C7,-33 3,-34 3,-39 C3,-48 17,-48 17,-39 C17,-34 13,-33 13,-28 L20,0 Z" fill="#5C6E8C" stroke={SEPIA} strokeWidth={2.5} strokeLinejoin="round" />
  </g>
);

const MapView: React.FC<{ f: number; mode: "A" | "B" | "C" }> = ({ f, mode }) => {
  const c = camOf(mode, f);
  const A = mode === "A", B = mode === "B", C = mode === "C";
  const base = A ? L(f, 526, 548, 0, 1) : 1;
  const jer = A ? L(f, 590, 604, 0, 1) : 1;
  const naz = A ? L(f, 534, 548, 0, 1) : 1;
  const bet = A ? L(f, 588, 602, 0, 1) : 1;
  const mj = A ? L(f, 630, 660, 0, 1, SINE) : 0;
  const road = A ? 0 : B ? L(f, 1052, 1068, 0, 1) : 1;
  const east = C ? L(f, 1195, 1221, 0, 1, SINE) : 0;
  const sN = toScreen(c, NAZ), sJ = toScreen(c, JER), sB = toScreen(c, BET);
  const g = `translate(${(c.sx - c.wx * c.s).toFixed(2)},${(c.sy - c.wy * c.s).toFixed(2)}) scale(${c.s.toFixed(4)})`;
  const ink = { fill: "none", stroke: SEPIA, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  const mjHead = along(MJ, MJc, mj);
  const prints = [0, 1, 2, 3, 4, 5, 6].map((i) => along(ROAD, ROADc, 0.08 + i * 0.14));
  const eastDash = dashSegs(EAST, EASTc, 30, 20), mjDash = dashSegs(MJ, MJc, 20, 16);
  const starLand = A ? 649 : B ? 1044 : 0;
  const starPos: [number, number] = [sB[0], sB[1] - 128 * c.s];
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, overflow: "hidden", background: PARCH }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 30% 22%, rgba(255,250,228,0.75), rgba(255,250,228,0) 55%), radial-gradient(ellipse at 78% 80%, rgba(196,150,84,0.28), rgba(196,150,84,0) 50%), radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 62%, rgba(110,72,30,0.42) 100%)" }} />
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>
        <Rough />
        <defs>
          <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={5} /><feColorMatrix type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0 0.08  0 0 0 0.16 0" /></filter>
        </defs>
        <rect width={1080} height={1920} filter="url(#grain)" />
        <g filter={boil(f)}>
          <g transform={g}>
            {/* sea */}
            <path d={`${toD(COAST)} L-900 1960 L-900 -40 Z`} fill={SEA} opacity={0.75 * base} />
            <path d={toD(COAST)} {...ink} strokeWidth={7} {...draw(base * 1.6)} />
            <path d={toD(COAST)} {...ink} strokeWidth={2} opacity={0.5} transform="translate(-14,4)" {...draw(base * 1.6 - 0.3)} />
            {WAVES.map(([x, y], i) => <path key={i} d={`M${x},${y} q10,-12 20,0 t20,0 t20,0`} {...ink} strokeWidth={3.2} opacity={0.75} {...draw(base * 2.4 - 0.7 - i * 0.08)} />)}
            {/* Sea of Galilee, Jordan, Dead Sea (no labels) */}
            <path transform="translate(22,84)" d="M800,268 C836,262 852,300 842,338 C834,376 806,396 788,372 C768,346 770,276 800,268Z" {...ink} fill={SEA} fillOpacity={0.75 * L(base, 0.5, 1, 0, 1)} strokeWidth={4.5} {...draw(base * 1.8 - 0.2)} />
            <path d={toD(JORDAN)} {...ink} stroke="#6E9A9E" strokeWidth={8} {...draw(base * 1.8 - 0.5)} />
            <path d={toD(JORDAN)} {...ink} strokeWidth={1.6} transform="translate(5,0)" opacity={0.6} {...draw(base * 1.8 - 0.5)} />
            <path d="M836,1002 C872,1010 880,1090 870,1170 C862,1250 850,1318 826,1322 C800,1322 806,1240 808,1160 C808,1090 806,1004 836,1002Z" {...ink} fill={SEA} fillOpacity={0.75 * L(base, 0.6, 1, 0, 1)} strokeWidth={4.5} {...draw(base * 1.8 - 0.6)} />
            {/* hills, dunes */}
            {HILLS.map(([x, y], i) => <path key={i} d={`M${x - 34},${y + 16} L${x - 6},${y - 20} L${x + 8},${y - 2} L${x + 24},${y - 18} L${x + 50},${y + 16} M${x - 6},${y - 20} L${x - 2},${y + 2} M${x + 24},${y - 18} L${x + 28},${y + 2}`} {...ink} strokeWidth={3.4} opacity={0.62} {...draw(base * 3 - 1.2 - hash(i) * 0.8)} />)}
            {DUNES.map(([x, y], i) => <path key={i} d={`M${x - 50},${y} q25,-22 50,0 q25,-20 50,0`} {...ink} strokeWidth={3} opacity={0.5} {...draw(base * 3 - 1.4 - hash(i + 40) * 0.6)} />)}
            {/* compass */}
            <g transform="translate(240,1660) scale(1.6)" opacity={L(base, 0.7, 1, 0, 0.85)}>
              <circle r={44} {...ink} strokeWidth={2.4} /><polygon points={star8(58, 0.22)} fill="#F7EACB" stroke={SEPIA} strokeWidth={2.6} strokeLinejoin="round" /><path d="M0,-58 L8,-12 L-8,-12Z" fill={SEPIA} />
            </g>
            {/* Mary and Joseph's road */}
            {A && mjDash.filter((d) => d.u <= mj - 0.001).map((d, i) => <line key={i} x1={d.a[0]} y1={d.a[1]} x2={d.b[0]} y2={d.b[1]} stroke={SEPIA} strokeWidth={7} strokeLinecap="round" />)}
            {/* the wise men's road from the east */}
            {C && eastDash.filter((d) => d.u <= east - 0.001).map((d, i) => <g key={i}><line x1={d.a[0]} y1={d.a[1]} x2={d.b[0]} y2={d.b[1]} stroke={SEPIA} strokeWidth={15} strokeLinecap="round" /><line x1={d.a[0]} y1={d.a[1]} x2={d.b[0]} y2={d.b[1]} stroke={GOLD} strokeWidth={9} strokeLinecap="round" /></g>)}
            {/* the short road */}
            {road > 0 && <><path d={toD(ROAD)} {...ink} strokeLinecap="butt" strokeWidth={48} opacity={0.8} {...draw(road)} /><path d={toD(ROAD)} {...ink} strokeLinecap="butt" strokeWidth={41} stroke="#F3E6C4" {...draw(road * 1.02)} /></>}
            {/* towns */}
            {jer > 0 && <g transform={`translate(${JER[0]},${JER[1]}) scale(1.64)`}><Town kind="city" p={jer} /></g>}
            {naz > 0 && <g transform={`translate(${NAZ[0]},${NAZ[1]}) scale(1.9)`}><Town kind="small" p={naz} /></g>}
            {bet > 0 && <g transform={`translate(${BET[0]},${BET[1]}) scale(1.9)`}><Town kind="small" p={bet} /></g>}
            {/* footprints on the short road: hollow = not taken, gold = taken */}
            {!A && prints.map((p, i) => <Print key={i} x={p[0]} y={p[1]} ang={p[2]} s={0.86} sw={4} side={i % 2 ? 0.8 : -0.8} f={f}
              pop={B ? 1070 + 2 * i : 0} gold={C ? 1221 + 2.6 * i : undefined} blink={B && i === 0 ? [1092, 1118] : undefined} />)}
            {/* the tax order */}
            {A && f >= 616 && <g transform={`translate(440,430) scale(${2 * L(f, 616, 624, 0, 1, BACK)}) rotate(-8)`} opacity={L(f, 654, 664, 1, 0.0)}>
              <path d="M-34,-24 L30,-24 C40,-24 40,-12 30,-12 L30,26 L-34,26 C-44,26 -44,14 -34,14 Z" fill="#F7EACB" stroke={SEPIA} strokeWidth={3.4} strokeLinejoin="round" />
              <path d="M-22,-10 L18,-10 M-22,0 L18,0 M-22,10 L4,10" {...ink} strokeWidth={2.6} />
              <circle cx={20} cy={18} r={11} fill="#9E3B2A" stroke={SEPIA} strokeWidth={3} />
              <path d="M40,-4 C52,-12 62,-12 72,-4 M72,-4 l-12,-3 M72,-4 l-4,-11" {...ink} strokeWidth={3.4} {...draw(L(f, 622, 632, 0, 1))} />
            </g>}
            {/* walkers and camels */}
            {A && naz >= 1 && <g transform={`translate(${mjHead[0]},${mjHead[1]}) scale(${2.1 * L(f, 552, 560, 0, 1, BACK) * L(f, 656, 664, 1, 0.7)})`}><Walkers ph={mj > 0 && mj < 1 ? f * 0.7 : 0} /></g>}
            {C && [0, 1, 2].map((i) => { const u = east * 1.02 - 0.02 - i * 0.12; if (u <= 0) return null; const p = along(EAST, EASTc, u);
              return <g key={i} transform={`translate(${p[0]},${p[1]}) scale(${1.5 * L(f, 1226, 1234, 1, 0)})`}><Camel ph={f * 0.75 + i * 1.3} /></g>; })}
          </g>
        </g>
        {/* fold creases + frame (screen space) */}
        <path d="M0,640 L1080,640 M0,1280 L1080,1280" stroke="rgba(110,72,30,0.20)" strokeWidth={3} />
        <rect x={22} y={22} width={1036} height={1876} fill="none" stroke={SEPIA} strokeWidth={5} filter={boil(0, false)} opacity={0.85} />
        <rect x={36} y={36} width={1008} height={1848} fill="none" stroke={SEPIA} strokeWidth={2} filter={boil(0, false)} opacity={0.6} />
        {/* the Bethlehem star (screen space, constant size) */}
        {bet >= 1 && f >= starLand && <GStar x={starPos[0]} y={starPos[1]} land={starLand} f={f} size={C ? L(f, 1234, 1240, 64, 84, OUT) : 64} />}
        {C && f >= 1234 && f < 1250 && <g transform={`translate(${starPos[0]},${starPos[1]})`} opacity={L(f, 1242, 1250, 1, 0)}>
          {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => { const a = i * Math.PI / 6 + 0.26, r0 = 62, r1 = r0 + L(f, 1234, 1244, 0, i % 2 ? 60 : 96, OUT);
            return <line key={i} x1={Math.cos(a) * r0} y1={Math.sin(a) * r0} x2={Math.cos(a) * r1} y2={Math.sin(a) * r1} stroke={GOLD} strokeWidth={6} strokeLinecap="round" />; })}
        </g>}
      </svg>
      {/* labels (screen space) */}
      {A && <Tag text="Nazareth" cx={sN[0]} cy={sN[1] - 110 * c.s - 54} p={L(f, 546, 558, 0, 1)} />}
      {A && <Tag text="Bethlehem" cx={sB[0] + 10} cy={sB[1] + 16 * c.s + 44} p={L(f, 596, 608, 0, 1)} gold={L(f, 649, 654, 0, 0.9)} />}
      {!A && <Tag text="Jerusalem" right size={64} w={440} cx={sJ[0] - 128 * c.s - 4} cy={sJ[1] - 40 * c.s} p={B ? L(f, 1036, 1046, 0, 1) : 1} />}
      {!A && <Tag text="Bethlehem" cx={sB[0] + 10} cy={sB[1] + 16 * c.s + 44} p={B ? L(f, 1044, 1054, 0, 1) : 1} gold={B ? L(f, 1044, 1049, 0, 0.9) : 0.9} />}
      {C && <div style={{ opacity: L(f, 1213, 1221, 1, 0) }}>
        <Tag text="the east" cx={toScreen(c, [1090, 330])[0]} cy={Math.max(250, toScreen(c, [1090, 330])[1])} p={L(f, 1196, 1206, 0, 1)} font="FellI" w={300} />
        <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}><g transform={`translate(${toScreen(c, [1090, 330])[0]},${Math.max(250, toScreen(c, [1090, 330])[1]) + 46})`}>
          <path d="M-70,0 C-30,8 20,8 70,0 M70,0 l-18,-12 M70,0 l-16,14" fill="none" stroke={SEPIA} strokeWidth={5} strokeLinecap="round" {...draw(L(f, 1202, 1210, 0, 1))} /></g></svg>
      </div>}
    </div>
  );
};

// map layer with its own entrances / exits
const MapLayer: React.FC<{ f: number }> = ({ f }) => {
  if (f >= 525 && f < 680) { // A: unfold (bottom fold first), fold away (top fold first, reveals the manger)
    const folding = f < 535 || f >= 664;
    if (!folding) return <MapView f={f} mode="A" />;
    return (
      <div style={{ position: "absolute", inset: 0, perspective: 2600 }}>
        {[0, 1, 2].map((i) => {
          let rot = 0, vis = true;
          if (f < 535) { const s0 = 525 + 2 * (2 - i); if (f < s0) vis = false; rot = L(f, s0, s0 + 5, 88, 0, OUT); }
          else { const s0 = 664 + 4 * i; rot = L(f, s0, s0 + 8, 0, -90, IN); if (f >= s0 + 8) vis = false; }
          if (!vis) return null;
          return (
            <div key={i} style={{ position: "absolute", left: 0, top: i * 640, width: 1080, height: 640, overflow: "hidden", transformOrigin: "50% 100%", transform: `rotateX(${rot}deg)`,
              filter: `brightness(${1 - Math.abs(rot) / 150})`, boxShadow: "0 18px 40px rgba(0,0,0,0.45)" }}>
              <div style={{ position: "absolute", left: 0, top: -i * 640, width: 1080, height: 1920 }}><MapView f={f} mode="A" /></div>
            </div>);
        })}
      </div>);
  }
  if (f >= 1029 && f < 1127) { // B: unrolls like a scroll (top -> bottom), is put down
    const y = L(f, 1029, 1041, -40, 1990, INOUT);
    const dn = f >= 1117 ? L(f, 1117, 1126, 0, 1, IN) : 0;
    return (
      <div style={{ position: "absolute", inset: 0, transform: `translateY(${dn * 2000}px) rotate(${dn * 7}deg)`, transformOrigin: "20% 100%", filter: dn ? "drop-shadow(0 -20px 30px rgba(0,0,0,0.5))" : undefined }}>
        <div style={{ position: "absolute", inset: 0, clipPath: y < 1990 ? `inset(0 0 ${Math.max(0, 1920 - y)}px 0)` : undefined }}><MapView f={f} mode="B" /></div>
        {y < 1990 && <Roller y={y} />}
      </div>);
  }
  if (f >= 1186 && f < 1262) { // C: lifted back up, then the star iris opens M2 above it
    const up = L(f, 1186, 1195, 1, 0, OUT);
    return (
      <div style={{ position: "absolute", inset: 0, transform: `translateY(${up * 2000}px) rotate(${-up * 6}deg)`, transformOrigin: "80% 100%", filter: up ? "drop-shadow(0 -20px 30px rgba(0,0,0,0.5))" : undefined }}>
        <MapView f={f} mode="C" />
      </div>);
  }
  return null;
};
const Roller: React.FC<{ y: number; vertical?: boolean; x?: number }> = ({ y, vertical, x = 0 }) => vertical ? (
  <div style={{ position: "absolute", left: x - 34, top: -30, width: 68, height: 1980, borderRadius: 30, background: "linear-gradient(90deg,#4a2e14,#b98846 45%,#6b4520 80%,#3a220e)", border: `5px solid ${INK}`, boxShadow: "0 0 40px rgba(0,0,0,.45)" }} />
) : (
  <div style={{ position: "absolute", left: -30, top: y - 34, width: 1140, height: 68, borderRadius: 30, background: "linear-gradient(180deg,#4a2e14,#b98846 45%,#6b4520 80%,#3a220e)", border: `5px solid ${INK}`, boxShadow: "0 24px 40px rgba(0,0,0,.45)" }} />
);

// =====================================================================================
//  The 700-years time scroll (cut 1): f116-176
// =====================================================================================
const WHEEL2 = (ang: number) => (<>
  <g transform="translate(-400,0)"><g transform={`rotate(${-ang}) scale(1.1)`}>
    {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => { const a = i * Math.PI / 6; return <line key={i} x1={Math.cos(a) * 76} y1={Math.sin(a) * 76} x2={Math.cos(a) * (i % 2 ? 100 : 114)} y2={Math.sin(a) * (i % 2 ? 100 : 114)} stroke={SEPIA} strokeWidth={6} strokeLinecap="round" />; })}
    <circle r={62} fill={GOLD} stroke={SEPIA} strokeWidth={7} /></g></g>
  <g transform="translate(400,0)"><g transform={`rotate(${-ang}) scale(1.1)`}>
    <path d="M20,-62 A64,64 0 1 0 20,62 A48,48 0 1 1 20,-62Z" fill="#FBF3DA" stroke={SEPIA} strokeWidth={7} strokeLinejoin="round" /></g></g>
</>);
const TimeScroll: React.FC<{ f: number; ready: boolean }> = ({ f, ready }) => {
  if (f < 116 || f >= 177) return null;
  const xL = L(f, 116, 125, 1140, -80, OUT), xR = L(f, 165, 176, 1160, -80, INOUT);
  const off = L(f, 119, 152, 0, 2300, OUT) + 1.2 * Math.max(0, f - 152);
  const n = 700; // 2026-11-15 film panel: a counting 100..700 read as "100"; show 700 only
  const tick = f < 132 && f >= 119 && (f - 119) % 2 === 0 ? 1.12 : 1;
  const ang = -off * 0.42;
  const ticks: React.ReactNode[] = [];
  for (let i = 0; i < 9; i++) { const x = ((i * 170 + off) % 1530) - 220; ticks.push(<path key={i} d={`M${x},1236 L${x + 3},1362`} stroke={SEPIA} strokeWidth={i % 2 ? 5 : 8} strokeLinecap="round" />);
    ticks.push(<path key={"s" + i} d={`M${x + 85},1276 L${x + 86},1324`} stroke={SEPIA} strokeWidth={4} strokeLinecap="round" opacity={0.7} />); }
  const tx: React.CSSProperties = { fontFamily: "BangersB", fontSize: 132, lineHeight: "146px", color: SEPIA, letterSpacing: 3 };
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <div style={{ position: "absolute", inset: 0, clipPath: `inset(0 ${Math.max(0, 1080 - xR)}px 0 ${Math.max(0, xL)}px)`, background: PARCH }}>
        <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, rgba(255,250,228,0.8), rgba(255,250,228,0) 60%), radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 60%, rgba(110,72,30,0.4) 100%)" }} />
        <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>
          <Rough />
          <path d="M-20,34 L1100,30 M-20,1886 L1100,1890" stroke={SEPIA} strokeWidth={6} opacity={0.8} />
          <g filter={boil(f)} transform="translate(0,90)">
            {/* the days run backwards: sun and moon wheel */}
            <g transform="translate(540,1300)">
              <path d="M-400,0 A400,400 0 0 1 400,0" fill="none" stroke={SEPIA} strokeWidth={3} strokeDasharray="4 16" strokeLinecap="round" opacity={0.7} />
              <g transform={`rotate(${ang})`}>
                {WHEEL2(ang)}
                <g transform="translate(0,-400)"><g transform={`rotate(${-ang}) scale(1.25)`}>
                  {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => { const a = i * Math.PI / 6; return <line key={i} x1={Math.cos(a) * 76} y1={Math.sin(a) * 76} x2={Math.cos(a) * (i % 2 ? 100 : 114)} y2={Math.sin(a) * (i % 2 ? 100 : 114)} stroke={SEPIA} strokeWidth={6} strokeLinecap="round" />; })}
                  <circle r={62} fill={GOLD} stroke={SEPIA} strokeWidth={7} /></g></g>
                <g transform="translate(0,400)"><g transform={`rotate(${-ang}) scale(1.25)`}>
                  <path d="M20,-62 A64,64 0 1 0 20,62 A48,48 0 1 1 20,-62Z" fill="#FBF3DA" stroke={SEPIA} strokeWidth={7} strokeLinejoin="round" /></g></g>
              </g>
            </g>
            <rect x={-20} y={1302} width={1120} height={560} fill={PARCH} />
            <path d="M-20,1300 C300,1292 700,1308 1100,1298" fill="none" stroke={SEPIA} strokeWidth={9} strokeLinecap="round" />
            {ticks}
            {/* long arrow back */}
            <path d="M900,1490 C700,1472 420,1506 190,1486 M190,1486 l44,-34 M190,1486 l46,30" fill="none" stroke={SEPIA} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" {...draw(L(f, 126, 142, 0, 1, OUT))} />
          </g>
        </svg>
        {ready && <div style={{ position: "absolute", left: 0, top: 360, width: 1080, textAlign: "center", transform: `scale(${L(f, 119, 127, 0.7, 1, BACK)})`, transformOrigin: "50% 100px", opacity: L(f, 119, 122, 0, 1) }}>
          <div style={tx}>ABOUT <span style={{ display: "inline-block", width: 240, color: GOLD, WebkitTextStroke: `10px ${SEPIA}`, paintOrder: "stroke fill", transform: `scale(${tick})` }}>{n}</span> YEARS</div>
          <div style={tx}>EARLIER</div>
        </div>}
      </div>
      {xL > -70 && <Roller y={0} vertical x={xL} />}
      {f >= 165 && <Roller y={0} vertical x={xR} />}
    </div>
  );
};

// =====================================================================================
//  Doodles on the art
// =====================================================================================
const Ring: React.FC<{ cx: number; cy: number; rx: number; ry: number; p: number; w?: number; col?: string }> = ({ cx, cy, rx, ry, p, w = 7, col = CREAM }) => {
  const d = `M${cx - rx},${cy + 6} C${cx - rx},${cy - ry * 1.25} ${cx + rx},${cy - ry * 1.3} ${cx + rx + 4},${cy} C${cx + rx},${cy + ry * 1.3} ${cx - rx * 0.9},${cy + ry * 1.3} ${cx - rx - 8},${cy - 4} C${cx - rx - 6},${cy - ry * 1.05} ${cx - rx * 0.2},${cy - ry * 1.25} ${cx + rx * 0.5},${cy - ry * 1.02}`;
  return <g><path d={d} fill="none" stroke={INK} strokeWidth={w + 6} strokeLinecap="round" {...draw(p)} /><path d={d} fill="none" stroke={col} strokeWidth={w} strokeLinecap="round" {...draw(p)} /></g>;
};
const roadPrints = (tx: number, ty: number) => { const o: [number, number, number][] = []; for (let i = 0; i < 7; i++) { const u = i / 6; o.push([140 + (tx - 150 - 140) * u, ty + 104 - 52 * u - 26 * Math.sin(u * Math.PI), -0.12 - 0.1 * Math.cos(u * Math.PI)]); } return o; };

const Marks: React.FC<{ f: number }> = ({ f }) => {
  const els: React.ReactNode[] = [];
  let calm = false;
  // hook: ring + star on "where", hollow sandal prints on "go?"
  if (f < 124) {
    const [tx, ty] = p1Town(f);
    els.push(<Ring key="hr" cx={tx + 6} cy={ty - 14} rx={128} ry={56} p={L(f, 38, 50, 0, 1, OUT)} />);
    els.push(<GStar key="hs" x={tx} y={ty - 62} land={40} f={f} size={58} />);
    roadPrints(tx, ty).forEach(([x, y, a], i) => els.push(<Print key={"hp" + i} x={x} y={y} ang={a} s={1.7} side={i % 2 ? 1 : -1} pop={105 + 2 * i} f={f} />));
  }
  // P2: name tag arrow for Micah
  if (f >= 195 && f < 262) {
    const o = L(f, 254, 261, 1, 0);
    els.push(<g key="ma" opacity={o}><path d="M352,838 C420,800 470,812 520,852 M520,852 l-34,-8 M520,852 l-10,-32" fill="none" stroke={INK} strokeWidth={13} strokeLinecap="round" strokeLinejoin="round" {...draw(L(f, 199, 209, 0, 1, OUT))} />
      <path d="M352,838 C420,800 470,812 520,852 M520,852 l-34,-8 M520,852 l-10,-32" fill="none" stroke={CREAM} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" {...draw(L(f, 199, 209, 0, 1, OUT))} /></g>);
  }
  // cut 2: ink doorway around the top panel, we walk through it
  if (f >= 254 && f < 273) {
    const d = "M24,636 L22,150 C22,-30 1058,-30 1058,150 L1056,636 Z";
    els.push(<g key="door" transform={f >= 265 ? `translate(540,300) scale(${L(f, 265, 272, 1, 2.1, IN)}) translate(-540,-300)` : undefined}>
      <path d={d} fill="none" stroke={INK} strokeWidth={22} strokeLinejoin="round" {...draw(L(f, 254, 265, 0, 1, INOUT))} />
      <path d={d} fill="none" stroke={CREAM} strokeWidth={8} strokeLinejoin="round" {...draw(L(f, 255, 266, 0, 1, INOUT))} /></g>);
  }
  // M1: Micah names the town; out of it a ruler would come
  if (f >= 334 && f < 416) {
    const o = L(f, 408, 415, 1, 0), [tx, ty] = M1_TOWN;
    els.push(<g key="m1" opacity={o}>
      <Ring cx={tx + 14} cy={ty - 8} rx={150} ry={74} p={L(f, 334, 348, 0, 1, OUT)} col={GOLD} />
      <GStar x={tx + 20} y={ty - 96} land={340} f={f} size={62} />
      {f >= 381 && <g transform={`translate(${tx + 20},${L(f, 381, 398, ty - 130, ty - 214, OUT)}) scale(2.1)`}><Crown p={L(f, 381, 396, 0, 1)} /></g>}
      {f >= 386 && [-44, 0, 44].map((dx, i) => <path key={i} d={`M${tx + 20 + dx},${ty - 132} l0,-22`} stroke={GOLD} strokeWidth={7} strokeLinecap="round" opacity={L(f, 398, 406, 1, 0)} {...draw(L(f, 386 + i, 394 + i, 0, 1))} />)}
    </g>);
  }
  // P3: the star they followed, from the east, + gold steps (wise men)
  if (f >= 755 && f < 826) {
    const ct = clipT(SEG[5], f); const [top, bot] = lerpPts(P3_CAMEL, ct);
    const o = L(f, 817, 825, 1, 0), p = L(f, 757, 800, 0, 1, OUT);
    const y0 = top + 150, hx = mix(1010, 250, p), hy = y0 - 46 * Math.sin(p * Math.PI * 0.9);
    const tr: string[] = []; for (let i = 0; i <= 24; i++) { const u = p * i / 24; tr.push(`${i ? "L" : "M"}${mix(1010, 250, u).toFixed(0)},${(y0 - 46 * Math.sin(u * Math.PI * 0.9)).toFixed(0)}`); }
    els.push(<g key="ws" opacity={o}>
      <path d={tr.join(" ")} fill="none" stroke={INK} strokeWidth={13} strokeLinecap="round" strokeDasharray="26 22" />
      <path d={tr.join(" ")} fill="none" stroke={GOLD} strokeWidth={7} strokeLinecap="round" strokeDasharray="26 22" />
      <GStar x={hx} y={hy} land={755} f={f} size={104} />
      {Array.from({ length: 14 }).map((_, k) => <Print key={k} x={1020 - 66 * k} y={bot - 44 + 8 * Math.sin(k * 1.3)} ang={Math.PI} s={0.8} side={k % 2 ? 1 : -1} pop={762 + Math.round(2.8 * k)} gold={0} f={f} />)}
    </g>);
  }
  // cut 6: the gold footprints lead the wipe
  if (f >= 820 && f < 842) {
    const u = INOUT(Math.max(0, Math.min(1, (f - 823) / 12)));
    const pts: string[] = []; for (let y = -60; y <= 1980; y += 60) pts.push(`${wipeX(u, y).toFixed(0)},${y}`);
    if (f >= 823 && f < 836) els.push(<g key="wl"><polyline points={pts.join(" ")} fill="none" stroke={INK} strokeWidth={16} /><polyline points={pts.join(" ")} fill="none" stroke={GOLD} strokeWidth={7} /></g>);
    for (let i = 0; i < 7; i++) { const y = 640 + i * 190, x0 = wipeX(0, y), x1 = wipeX(1, y); const px = mix(x0, x1, 0.22 + 0.09 * i) , pop = 820 + i * 1.6;
      els.push(<Print key={"wp" + i} x={px} y={y} ang={Math.PI * 0.92} s={2.3} side={i % 2 ? 1 : -1} pop={Math.round(pop)} gold={0} f={f} op={L(f, 834, 841, 1, 0)} />); }
  }
  // P1 experts: the town, the short road, nobody on it
  if (f >= 1126 && f < 1194) {
    const [tx, ty] = p1Town(f);
    els.push(<Ring key="er" cx={tx + 6} cy={ty - 14} rx={128} ry={56} p={1} />);
    els.push(<GStar key="es" x={tx} y={ty - 62} land={1000} f={f} size={58} />);
    roadPrints(tx, ty).forEach(([x, y, a], i) => els.push(<Print key={"ep" + i} x={x} y={y} ang={a} s={1.7} side={i % 2 ? 1 : -1} pop={1000} f={f} pulse={i === 0 ? 1172 : undefined} />));
  }
  // nightfall: a few drawn stars ride the top of the falling night (sky only, calm)
  if (f >= 1299 && f < 1326) {
    calm = true;
    const e = L(f, 1299, 1323, -160, 2080, SINE);
    for (let i = 0; i < 7; i++) { const x = 90 + i * 150 + 40 * hash(i + 3), y = e - 110 - 60 * hash(i + 9);
      if (y > 20 && y < 300) els.push(<g key={"ns" + i} transform={`translate(${x},${y})`} opacity={0.9 * L(y, 200, 300, 1, 0)}><polygon points={star8(13 + 9 * hash(i), 0.3)} fill={CREAM} stroke={INK} strokeWidth={2} strokeLinejoin="round" /></g>); }
  }
  // the one gold line: He came down from heaven. Sky panel only; stops above the cross.
  if (f >= 1381 && f < 1437) {
    calm = true;
    const ct = clipT(SEG[9], f);
    const [cx, cy] = lerpPts(P5_CORE, ct); const [, by] = lerpPts(P5_STAR_BOTTOM, ct);
    const y0 = cy + 30, y1 = by - 16, h = y1 - y0;
    const d = `M ${cx} ${y0} C ${cx + 70} ${y0 + h * 0.3}, ${cx - 80} ${y0 + h * 0.62}, ${cx} ${y1}`;
    const p = L(f, 1381, 1417, 0, 1, SINE), op = L(f, 1420, 1436, 1, 0);
    const side: [number, number, number, number][] = [[0.18, 70, 1, 15], [0.36, -78, -1, 11], [0.55, 66, 1, 13], [0.72, -60, -1, 10], [0.88, 58, 1, 12]];
    els.push(
      <g key="gl" opacity={op}>
        <path d={d} fill="none" stroke={GOLD} strokeWidth={26} opacity={0.22} strokeLinecap="round" {...draw(p)} />
        <path d={d} fill="none" stroke={GOLD} strokeWidth={9} strokeLinecap="round" {...draw(p)} />
        <path d={d} fill="none" stroke={CREAM} strokeWidth={2.5} strokeLinecap="round" {...draw(p)} />
        {side.map(([u, dx, , r], i) => { const a = L(p, u, u + 0.14, 0, 1, SINE); if (a <= 0) return null;
          return <g key={i} transform={`translate(${cx + dx},${y0 + h * u}) scale(${a})`} opacity={0.9}><polygon points={star8(r, 0.3)} fill={GOLD} stroke={CREAM} strokeWidth={1.5} strokeLinejoin="round" /></g>; })}
      </g>);
  }
  // dawn: a few drawn rays from the rising sun, far from Him
  if (f >= 1578) {
    calm = true;
    const [sx, sy] = M3_SUN;
    const o = 0.85 * L(f, 1700, 1716, 1, 0.7);
    for (let i = 0; i < 9; i++) { const a = (150 + i * 16.5) * Math.PI / 180, r0 = 78, r1 = (i % 2 ? 150 : 205);
      const d = `M${sx + Math.cos(a) * r0},${sy + Math.sin(a) * r0} L${sx + Math.cos(a) * r1},${sy + Math.sin(a) * r1}`;
      els.push(<g key={"dr" + i} opacity={o}><path d={d} stroke={GOLD} strokeWidth={7} strokeLinecap="round" {...draw(L(f, 1578 + i * 4, 1612 + i * 4, 0, 1, SINE))} /><path d={d} stroke={CREAM} strokeWidth={2} strokeLinecap="round" {...draw(L(f, 1578 + i * 4, 1612 + i * 4, 0, 1, SINE))} /></g>); }
  }
  return <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}><Rough /><g filter={boil(f, !calm)}>{els}</g></svg>;
};

// ---------- full-frame transition overlays ----------
const FLAME = "M0,60 C-45,40 -40,-10 -8,-50 C-5,-70 2,-85 0,-100 C20,-70 48,-20 40,25 C36,48 20,60 0,60 Z";
const Overlays: React.FC<{ f: number }> = ({ f }) => {
  const els: React.ReactNode[] = [];
  if (f >= 270 && f < 277) els.push(<div key="fl" style={{ position: "absolute", inset: 0, background: CREAM, opacity: f < 273 ? L(f, 270, 272, 0, 0.6) : L(f, 273, 275, 0.6, 0) }} />);
  if (f >= 416 && f < 431) { // cut 3: one broad ink brush swipe, the way Micah points
    const u1 = Math.pow(Math.max(0, Math.min(1, (f - 416) / 7)), 1.6), u2 = 1 - Math.pow(1 - Math.max(0, Math.min(1, (f - 423) / 7)), 1.6);
    const a: string[] = [], b: string[] = [];
    for (let y = -60; y <= 1980; y += 40) { a.push(`${(frontX(u1, y) + 26 * hash(y)).toFixed(0)},${y}`); b.push(`${(frontX(u2, y) - 60 + 18 * Math.sin(y / 70 + 4.1) - 50 * hash(y + 5)).toFixed(0)},${y}`); }
    els.push(<svg key="ink" style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}><polygon points={[...a, ...b.reverse()].join(" ")} fill={INK} />
      {[0, 1, 2, 3, 4, 5].map((i) => { const y = 180 + i * 300 + 60 * hash(i); return <line key={i} x1={frontX(u2, y) - 40} y1={y} x2={frontX(u2, y) + 210 + 120 * hash(i + 2)} y2={y + 44} stroke={PAPER} strokeWidth={5 + 6 * hash(i + 7)} strokeLinecap="round" opacity={0} />; })}</svg>);
  }
  if (f >= 468 && f < 485) { // cut 4: the lamp flame grows, fills the frame, and clears on Micah's face
    const s = Math.exp(L(f, 468, 475, Math.log(1.2), Math.log(170), IN));
    const o = f < 474 ? L(f, 468, 474, 0.9, 0.45, SINE) : L(f, 474, 480, 0.45, 0, SINE); // softened 2026-11-15: no full cream flash
    els.push(<svg key="flm" style={{ position: "absolute", left: 0, top: 0, opacity: o }} width={1080} height={1920}>
      <defs><radialGradient id="flg" cx="0.5" cy="0.62" r="0.6"><stop offset="0" stopColor="#FFF6D8" /><stop offset="0.55" stopColor="#FFD77A" /><stop offset="1" stopColor="#F2A534" /></radialGradient></defs>
      <g transform={`translate(${LAMP_FLAME[0]},${LAMP_FLAME[1]}) scale(${s}) translate(0,20)`}><path d={FLAME} fill="url(#flg)" stroke={INK} strokeWidth={7 / s} strokeLinejoin="round" /></g></svg>);
  }
  if (f >= 1539 && f < 1563) {
    const r = L(f, 1539, 1551, 0, 140, SINE), o = f < 1551 ? 1 : L(f, 1551, 1563, 1, 0, SINE);
    els.push(<div key="dawn" style={{ position: "absolute", inset: 0, opacity: o, background: `radial-gradient(circle at ${TOMB_DOOR[0]}px ${TOMB_DOOR[1]}px, #FFF3D6 ${r}%, rgba(255,243,214,0) ${r + 25}%)` }} />);
  }
  if (f >= 1551 && f < 1564) els.push(<div key="dawn2" style={{ position: "absolute", inset: 0, background: "#FFF3D6", opacity: L(f, 1551, 1563, 1, 0, SINE) }} />);
  if (f >= 1543 && f < 1556) { // drawn rays, only while the frame is full of light
    const o = Math.min(L(f, 1543, 1548, 0, 0.8), L(f, 1551, 1556, 0.8, 0));
    els.push(<svg key="rays" style={{ position: "absolute", left: 0, top: 0, opacity: o }} width={1080} height={1920}>
      {Array.from({ length: 18 }).map((_, i) => { const a = i * Math.PI / 9 + 0.1, r0 = 330 + 60 * hash(i), r1 = r0 + L(f, 1543, 1553, 60, 420 + 200 * hash(i + 4), SINE);
        return <line key={i} x1={TOMB_DOOR[0] + Math.cos(a) * r0} y1={TOMB_DOOR[1] + Math.sin(a) * r0} x2={TOMB_DOOR[0] + Math.cos(a) * r1} y2={TOMB_DOOR[1] + Math.sin(a) * r1} stroke={GOLD} strokeWidth={8} strokeLinecap="round" />; })}</svg>);
  }
  return <>{els}</>;
};

// ---------- lettering (v3 read-along pills, patched for v4) ----------
const PILLS: any[] = (D.pills as any[]).map((p) => {
  const q = JSON.parse(JSON.stringify(p));
  const mark = (t: string, m: string) => q.lines.forEach((r: any[]) => r.forEach((w: any) => { if (w.t === t) w.m = [...(w.m || []), m]; }));
  if (q.id === "h1") q.cy = 1318;
  if (q.id === "m1" || q.id === "m2") q.cy = 1440;
  if (q.id === "j3") q.cy = 705;
  if (q.id === "w1") mark("King.", "crownG");
  if (q.id === "w2") { q.lines[0][0].m = ["crownI"]; }
  if (q.id === "w2") q.cy = 1290; // 2026-11-15: up into the gutter, off Herod's eyes
  if (q.id === "sp") { q.end = 34.3; q.cy = 1290; }
  if (q.id === "cb") { q.cy = 1440; q.end = 37.2; }
  if (q.id === "n1") { q.cy = 1318; q.end = 39.6; }
  if (q.id === "n2a") { q.cy = 1440; }
  return q;
});
const KPill: React.FC<{ it: any; f: number }> = ({ it, f }) => {
  const s = F(it.start), e = F(it.end);
  if (f < s || f >= e) return null;
  const sacred = it.mode === "sacred" || it.mode === "final";
  const age = f - s;
  let op = sacred ? L(age, 0, 9, 0, 1) : L(age, 0, 3, 0, 1);
  op *= L(f, e - 4, e, 1, 0);
  const lines = it.lines as any[][];
  const h = lines.length * 62 + 40, top = it.cy - h / 2;
  const speech = it.mode === "speech";
  const lineEls = lines.map((row, li) => {
    if (it.mode === "final" && li === 1 && f < 1653) return <div key={li} style={{ opacity: 0 }}>{row.map((w: any) => w.t).join(" ")}</div>;
    const lo = it.mode === "final" && li === 1 ? L(f, 1653, 1661, 0, 1) : 1;
    return (
      <div key={li} style={{ opacity: lo, position: "relative" }}>
        {row.map((w: any, wi: number) => {
          const wf = F(w.at) - 1, k = f - wf;
          let o = 1, sc = 1;
          if (it.mode === "pop") { if (k < 0) o = 0; else sc = L(k, 0, 4, 1.25, 1, OUT); }
          else if (it.mode === "read" || speech) { o = k < 0 ? 0.38 : L(k, 0, 2, 0.38, 1); sc = k >= 0 ? L(k, 0, 5, 1.07, 1, OUT) : 1; }
          const m: string[] = w.m || [];
          const ga = m.includes("gold") ? L(f, wf + 1, wf + 5, 0, 1) : 0;
          const ls = m.includes("spread") ? L(f, F(44.88), F(45.5), 0, 5, SINE) : 0;
          const crown = m.includes("crownG") || m.includes("crownI");
          return (
            <React.Fragment key={wi}>
              <span style={{ display: "inline-block", position: "relative", opacity: o, transform: `scale(${sc})`, letterSpacing: ls,
                background: ga ? `rgba(232,168,28,${ga})` : undefined, borderRadius: 8, padding: "0 7px", margin: "0 -7px" }}>
                {w.t}
                {crown && f >= wf + 1 && (
                  <svg style={{ position: "absolute", left: "50%", top: -44, overflow: "visible" }} width={2} height={2}>
                    <g transform={m.includes("crownI") ? `translate(${6 * Math.sin(f / 5)},${-2 + 2 * Math.sin(f / 3.1)}) rotate(${-13 + 9 * Math.sin(f / 4.3)}) scale(0.78)` : "scale(0.78)"}>
                      <Crown p={L(f, wf + 1, wf + 9, 0, 1)} gold={m.includes("crownG")} w={5.5} /></g>
                  </svg>)}
                {m.includes("empty") && f >= wf + 1 && <span style={{ position: "absolute", inset: "4px -4px 2px -4px", border: `4px solid ${INK}`, borderRadius: 10,
                  clipPath: `inset(0 ${100 - L(f, wf + 1, wf + 7, 0, 100)}% 0 0)` }} />}
                {m.includes("ticks") && f >= wf + 1 && (
                  <svg style={{ position: "absolute", right: -18, top: -14, overflow: "visible" }} width={30} height={30}>
                    <path d="M4 18 L14 4 M14 24 L28 12" stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(f, wf + 1, wf + 4, 0, 1))} />
                  </svg>)}
                {(m.includes("under2") || m.includes("wavy")) && f >= wf + 1 && (
                  <svg style={{ position: "absolute", left: 0, top: 58, overflow: "visible" }} width={10} height={20}>
                    {m.includes("under2") ? <>
                      <line x1={0} y1={0} x2={uw(w.t)} y2={-2} stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(f, wf + 1, wf + 7, 0, 1))} />
                      <line x1={4} y1={9} x2={uw(w.t) - 4} y2={8} stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(f, wf + 3, wf + 9, 0, 1))} />
                    </> : <path d={`M0 0 Q ${uw(w.t) * 0.25} 9 ${uw(w.t) * 0.5} 0 T ${uw(w.t)} 0`} fill="none" stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(f, wf + 1, wf + 9, 0, 1))} />}
                  </svg>)}
                {m.includes("star") && f >= wf + 1 && (
                  <svg style={{ position: "absolute", right: -16, top: -18, overflow: "visible" }} width={24} height={24}><g transform={`translate(12,12) scale(${L(f, wf + 1, wf + 6, 0, 1, BACK)})`}>
                    <polygon points={star8(13)} fill={GOLD} stroke={INK} strokeWidth={3} strokeLinejoin="round" /></g></svg>)}
              </span>{wi < row.length - 1 ? " " : ""}
            </React.Fragment>
          );
        })}
        {it.mode === "final" && li === 1 && f >= 1655 && (
          <div style={{ position: "absolute", left: "50%", top: 64, transform: "translateX(-50%)", width: 380, height: 8 }}>
            <div style={{ position: "absolute", left: 0, top: 2, height: 2, width: `${L(f, 1655, 1680, 0, 100, SINE)}%`, background: INK, opacity: 0.6 }} />
            <div style={{ position: "absolute", left: 0, top: 0, height: 6, width: `${L(f, 1655, 1680, 0, 100, SINE)}%`, background: GOLD, borderRadius: 3 }} />
          </div>)}
      </div>
    );
  });
  const pop = speech ? L(age, 0, 6, 0.85, 1, BACK) : 1;
  const onMap = (f >= 534 && f < 664) || (f >= 1041 && f < 1118) || (f >= 1195 && f < 1240);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, opacity: op }}>
      {speech && ( // hand-drawn balloon tail, up to the scribe
        <svg style={{ position: "absolute", left: 0, top: 0, transform: `scale(${pop})`, transformOrigin: `540px ${it.cy}px` }} width={1080} height={1920}>
          <Rough /><g filter={boil(f)}>
            <path d={`M700 ${top + 4} C716 ${top - 40} 760 ${top - 86} 800 ${top - 118} C792 ${top - 70} 790 ${top - 30} 800 ${top + 4}`} fill="#F4F2EC" stroke={INK} strokeWidth={5} strokeLinejoin="round" /></g>
        </svg>)}
      <div style={{ position: "absolute", left: 100, top, width: 880, height: h, boxSizing: "border-box", borderRadius: 46, background: speech ? "rgba(244,242,236,0.94)" : onMap ? "rgba(248,244,232,0.86)" : PILL_FILL,
        border: `${speech ? 5 : 4}px solid ${speech ? INK : PILL_EDGE}`, display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center",
        fontFamily: "KalamB", fontSize: 54, lineHeight: "62px", color: INK, transform: `scale(${pop})` }}>{lineEls}</div>
      {speech && <>
        <Chip text="A SCRIBE" left={126 - L(age, 0, 6, 20, 0, OUT)} top={top + h - 14} />
        <Chip text="MATTHEW 2:5" right={126 - L(age, 0, 6, 20, 0, OUT)} top={top + h - 14} />
      </>}
    </div>
  );
};
let _ctx: CanvasRenderingContext2D | null = null;
const uw = (t: string) => { if (!_ctx) _ctx = document.createElement("canvas").getContext("2d"); _ctx!.font = "54px KalamB"; return _ctx!.measureText(t).width; };
const Chip: React.FC<{ text: string; left?: number; right?: number; top: number; rot?: number; op?: number }> = ({ text, left, right, top, rot = 0, op = 1 }) => (
  <div style={{ position: "absolute", left, right, top, height: 42, padding: "0 14px", boxSizing: "border-box", background: GOLD, border: `3px solid ${INK}`,
    borderRadius: 16, fontFamily: "KalamB", fontSize: 28, lineHeight: "36px", color: INK, whiteSpace: "nowrap", opacity: op, transform: `rotate(${rot}deg)` }}>{text}</div>
);

const QuestionCard: React.FC<{ f: number }> = ({ f }) => {
  if (f < 96 || f >= 138) return null; // 2026-11-15: hold GO? ~0.4 s longer, fade out
  const words: [string, number, number, string][] = [["DID", 96, -3, CREAM], ["THEY", 100, 2, CREAM], ["GO?", 106, -2, GOLD]];
  return (
    <div style={{ position: "absolute", left: 0, top: 1226, width: 1080, textAlign: "center", whiteSpace: "nowrap", opacity: L(f, 130, 137, 1, 0) }}>
      {words.map(([w, at, r, c], i) => {
        if (f < at) return <span key={i} style={{ display: "inline-block", opacity: 0, fontFamily: "BangersB", fontSize: 140, margin: "0 16px" }}>{w}</span>;
        const k = f - at;
        return <span key={i} style={{ display: "inline-block", fontFamily: "BangersB", fontSize: 140, lineHeight: "150px", color: c, WebkitTextStroke: "9px #4a2a12",
          paintOrder: "stroke fill", margin: "0 16px", transform: `scale(${L(k, 0, 4, 1.6, 1, OUT)}) rotate(${L(k, 0, 6, r, 0, OUT)}deg)` }}>{w}</span>;
      })}
    </div>
  );
};
const NameTag: React.FC<{ f: number }> = ({ f }) => {
  if (f < 195 || f >= 262) return null;
  const k = f - 195;
  return (
    <div style={{ position: "absolute", left: 96, top: 786, width: 256, height: 104, opacity: L(f, 254, 261, 1, 0), transform: `rotate(${L(k, 0, 7, -12, -4, BACK)}deg) scale(${L(k, 0, 6, 0.4, 1, BACK)})`,
      background: "#F4E6C2", border: `5px solid ${INK}`, borderRadius: 14, boxShadow: "6px 8px 0 rgba(0,0,0,0.45)", textAlign: "center", fontFamily: "KalamB", fontSize: 70, lineHeight: "104px", color: SEPIA }}>Micah</div>
  );
};
const Scroll2: React.FC<{ f: number }> = ({ f }) => {
  if (f < 462 || f >= 532) return null;
  const rise = L(f, 462, 466, 60, 0, OUT), a = L(f, 462, 466, 0, 1) * L(f, 527, 531, 1, 0);
  const open = L(f, 466, 475, 0, 1, INOUT);
  const pw = 80 + 760 * open, cx = 540, cy = 1085, ph = 250;
  const deck = (y: number, seed: number) => { let d = ""; for (let x = 0; x <= 840; x += 40) d += `${x === 0 ? "M" : "L"}${x} ${y + (hash(seed + x) - 0.5) * 10} `; return d; };
  const sc = D.scroll as any;
  return (
    <div style={{ position: "absolute", left: 0, top: rise, width: 1080, height: 1920, opacity: a }}>
      <div style={{ position: "absolute", left: cx - pw / 2, top: cy - ph / 2, width: pw, height: ph, overflow: "hidden" }}>
        <svg style={{ position: "absolute", left: (pw - 840) / 2, top: 0 }} width={840} height={ph}>
          <defs><linearGradient id="parch" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#F3E3B8" /><stop offset="1" stopColor="#E4CC98" /></linearGradient></defs>
          <path d={`${deck(6, 3)} L840 ${ph - 6} ${deck(ph - 6, 9).replace("M", "L").split(" L").reverse().join(" L")} Z`} fill="url(#parch)" opacity={0.97} stroke={INK} strokeWidth={5} />
        </svg>
        <div style={{ position: "absolute", left: (pw - 840) / 2, top: 0, width: 840, height: ph, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
          {sc.lines.map((ln: string[], li: number) => (
            <div key={li} style={{ fontFamily: "FellR", fontSize: 70, lineHeight: "82px", whiteSpace: "pre" }}>
              {ln.map((wd, wi) => { const t0 = F(sc.wt[li][wi]); const p = Math.max(0, Math.min(1, (f - t0) / 6)); const dry = L(f, t0, t0 + 10, 0, 1);
                return <span key={wi} style={{ display: "inline-block", clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`, color: dry < 1 ? `rgb(${42 * dry},${26 * dry},${14 * dry})` : SEPIA }}>{wd}{wi < ln.length - 1 ? " " : ""}</span>; })}
            </div>))}
        </div>
      </div>
      {[cx - pw / 2 - 32, cx + pw / 2 - 12].map((x, i) => (
        <div key={i} style={{ position: "absolute", left: x, top: cy - 150, width: 44, height: 300, borderRadius: 16, border: `4px solid ${INK}`, boxSizing: "border-box", background: "linear-gradient(90deg,#5a3a1c,#b07c3e 45%,#5a3a1c)", boxShadow: "0 4px 10px rgba(0,0,0,.35)" }} />))}
      {open > 0.98 && <Chip text="MICAH 5:2" right={1080 - 940 + L(f, 475, 481, -30, 0, OUT)} top={cy - ph / 2 - 26} rot={L(f, 475, 481, -6, 0, OUT)} />}
    </div>
  );
};
const EastTag: React.FC<{ f: number }> = ({ f }) => { // "the east" on the camel panel, tracked
  if (f < 784 || f >= 826) return null;
  const [top] = lerpPts(P3_CAMEL, clipT(SEG[5], f));
  const k = f - 784;
  return (
    <div style={{ position: "absolute", left: 742, top: top + 26, width: 250, height: 76, opacity: L(f, 817, 825, 1, 0), transform: `rotate(${L(k, 0, 7, 10, 3, BACK)}deg) scale(${L(k, 0, 6, 0.4, 1, BACK)})`,
      background: "#F4E6C2", border: `5px solid ${INK}`, borderRadius: 14, boxShadow: "6px 8px 0 rgba(0,0,0,0.45)", textAlign: "center", fontFamily: "FellI", fontSize: 54, lineHeight: "70px", color: SEPIA }}>the east</div>
  );
};

// ---------- prophecy marks (2026-11-15, owner yes: make the prophecy read) ----------
const RED = "#9E3B2A";
const Stamp: React.FC<{ f: number; at: number; text: string; size: number; left: number; top: number; rot: number; op?: number }> = ({ f, at, text, size, left, top, rot, op = 1 }) => {
  const k = f - at;
  return (
    <div style={{ position: left < 0 ? "relative" : "absolute", display: "inline-block", left: left < 0 ? undefined : left, top: left < 0 ? undefined : top, opacity: op * L(k, 0, 2, 0, 1), transform: `rotate(${rot}deg) scale(${L(k, 0, 5, 1.8, 1, OUT)})`, transformOrigin: "50% 50%",
      border: `7px solid ${RED}`, outline: `3px solid ${RED}`, outlineOffset: 5, borderRadius: 14, padding: "4px 26px", background: "rgba(251,243,218,0.92)",
      fontFamily: "BangersB", fontSize: size, lineHeight: `${size * 1.1}px`, letterSpacing: 4, color: RED, whiteSpace: "nowrap" }}>{text}</div>
  );
};
const ProphecyMarks: React.FC<{ f: number }> = ({ f }) => {
  const els: React.ReactNode[] = [];
  // 1. the time scroll says what this is: a prophecy
  if (f >= 138 && f < 170) els.push(<div key="pr" style={{ position: "absolute", left: 0, top: 690, width: 1080, textAlign: "center" }}>
    <Stamp f={f} at={138} text="A PROPHECY" size={96} left={-1} top={0} rot={-5} op={L(f, 160, 167, 1, 0)} /></div>);
  // 2. the birth: the promise is kept (on the night sky, never on the manger)
  if (f >= F(24.0) && f < F(25.1)) els.push(<div key="kp" style={{ position: "absolute", left: 470, top: 790, opacity: L(f, F(25.1) - 5, F(25.1), 1, 0) }}>
    <Stamp f={f} at={F(24.0)} text="CAME TRUE ✓" size={80} left={0} top={0} rot={-8} />
    {f >= F(24.0) + 4 && <Chip text="MICAH 5:2" left={150} top={118} rot={-3} />}</div>);
  // 3. the scribe is reading Micah's own words
  if (f >= F(32.24) && f < 1001) { const o = L(f, 994, 1000, 1, 0);
    els.push(<svg key="sr" style={{ position: "absolute", left: 0, top: 0, opacity: o }} width={1080} height={1920}><Ring cx={812} cy={1128} rx={128} ry={92} p={L(f, F(32.24), F(32.24) + 12, 0, 1, OUT)} col={GOLD} /></svg>);
    if (f >= F(32.24) + 8) els.push(<div key="sc" style={{ opacity: o }}><Chip text="MICAH 5:2" left={530} top={1170} rot={-4} /></div>); }
  return <>{els}</>;
};

const EndMark: React.FC<{ f: number }> = ({ f }) => {
  if (f < 1710) return null;
  const a = L(f, 1710, 1722, 0, 1, SINE), t = L(f, 1722, 1737, 0, 1);
  return (
    <div style={{ position: "absolute", left: 90, top: 1370, width: 900, height: 132, opacity: a }}>
      <div style={{ position: "absolute", left: 270, top: -18, width: 360, height: 8, background: GOLD, borderRadius: 4 }} />
      <div style={{ position: "absolute", inset: 0, borderRadius: 66, background: PILL_FILL, border: `4px solid ${PILL_EDGE}`, display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: "FrauncesB", fontSize: 62, letterSpacing: 8, color: INK, opacity: t }}>PROMISED. CAME TRUE.</div>
    </div>
  );
};

export const BethlehemV4: React.FC<{ hud?: boolean }> = ({ hud = false }) => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("bv4fonts"));
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    Promise.all([
      new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
      new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load(),
      new FontFace("FellR", `url(${staticFile("IMFeENrm28P.ttf")})`).load(),
      new FontFace("FellI", `url(${staticFile("IMFeENit28P.ttf")})`).load(),
      new FontFace("FrauncesB", `url(${staticFile("Fraunces.ttf")})`).load(),
    ]).then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); setReady(true); continueRender(h); }).catch(() => continueRender(h));
  }, []);
  const clip = (s: Seg, i: number) => {
    const from = F(s.a - s.pre), to = F(s.b + s.post);
    return (
      <Sequence key={i} from={from} durationInFrames={to - from} premountFor={30}>
        <div style={{ position: "absolute", inset: 0, ...segStyle(i, f) }}>
          <OffthreadVideo src={staticFile(`bethlehem/clips/${s.c}.mp4`)} startFrom={F(Math.max(0, s.inPt - s.pre))} muted style={{ width: 1080, height: 1920, objectFit: "cover", filter: s.c === "M3" ? "saturate(0.7) sepia(0.2)" : undefined }} />
        </div>
      </Sequence>
    );
  };
  return (
    <AbsoluteFill style={{ background: PAPER, overflow: "hidden" }}>
      <Audio src={staticFile("bethlehem/narration_v2_lev.mp3")} />
      {SEG.map((s, i) => (s.top ? null : clip(s, i)))}
      {f < 1262 && <Marks f={f} />}
      {ready && <MapLayer f={f} />}
      {SEG.map((s, i) => (s.top ? clip(s, i) : null))}
      {f >= 1262 && <Marks f={f} />}
      <Overlays f={f} />
      {ready && (
        <>
          <TimeScroll f={f} ready={ready} />
          <QuestionCard f={f} />
          <NameTag f={f} />
          <EastTag f={f} />
          <Scroll2 f={f} />
          <ProphecyMarks f={f} />
          {PILLS.map((it) => <KPill key={it.id} it={it} f={f} />)}
          <EndMark f={f} />
        </>
      )}
      {hud && <div style={{ position: "absolute", left: 18, top: 1862, padding: "4px 14px", background: "rgba(0,0,0,0.7)", color: "#fff", fontFamily: "KalamB", fontSize: 26, borderRadius: 10 }}>{(f / 30).toFixed(2)} s · f{f}</div>}
    </AbsoluteFill>
  );
};
