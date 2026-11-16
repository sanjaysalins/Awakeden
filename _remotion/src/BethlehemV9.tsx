// Born in Bethlehem - FULL COMIC film v8 (59.0 s) = v6 picture re-keyed to words v4 / voice v4 (narration_v41.words.json). $0.
// Everything is keyed to REAL film seconds + word indices wt(i) of narration_v41.words.json; NO warp. Clips play at 1.0x, trim only.
// New in v8: scroll strip (ruler in Israel / from everlasting), Galilee map beat, no tax order / walkers.
import React from "react";
import { AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import RECTS from "../public/bethlehem/panel_rects.json";
// @ts-ignore
import WORDS from "../public/bethlehem/narration_v41.words.json";

export const BTH9_FRAMES = 1782, BTH9_FPS = 30;
const INK = "#121014", GOLD = "#F6B923", CREAM = "#FFF4D6", NIGHT = "#1B2E6A", NIGHT2 = "#0F1A40", ROAD = "#6A84C4", OCHRE = "#E2A842", OCHRE2 = "#96602A", SEA = "#2A96AA", RED = "#9E3B2A";
const PILL_FILL = "rgba(225,225,228,0.588)", PILL_EDGE = "rgba(20,18,16,0.67)";
const F = (s: number) => Math.round(s * 30);
const cl = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const L = (x: number, a: number, b: number, p: number, q: number, e?: (t: number) => number) => interpolate(x, [a, b], [p, q], { ...cl, easing: e });
const OUT = Easing.out(Easing.cubic), INOUT = Easing.inOut(Easing.cubic), BACK = Easing.out(Easing.back(1.8)), SINE = Easing.inOut(Easing.sin), IN = Easing.in(Easing.cubic);
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const draw = (p: number) => ({ pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - Math.max(0, Math.min(1, p)) });
const wt = (i: number): number => (WORDS as any[])[i].start;
const lerp = (a: number, b: number, u: number) => a + (b - a) * u;

// ---------------- panel rects (gutter tracking) ----------------
type G = [number, [number, number][]];
const gut = (clip: string, ct: number): [number, number, number, number] => {
  const k: G[] = (RECTS as any)[clip];
  let i = 0; while (i < k.length - 2 && k[i + 1][0] <= ct) i++;
  const [ta, ga] = k[i], [tb, gb] = k[i + 1], u = Math.max(0, Math.min(1, (ct - ta) / (tb - ta)));
  const m = (a: number, b: number) => a + (b - a) * u;
  return [m(ga[0][0], gb[0][0]), m(ga[0][1], gb[0][1]), m(ga[1][0], gb[1][0]), m(ga[1][1], gb[1][1])];
};
const X0 = 14, X1 = 1066;
type Rc = { x: number; y: number; w: number; h: number };
const boxAt = (clip: string, ct: number): [number, number, number, number] => {
  const k: [number, number[]][] = (RECTS as any)[clip + "_box"];
  let i = 0; while (i < k.length - 2 && k[i + 1][0] <= ct) i++;
  const [ta, ga] = k[i], [tb, gb] = k[i + 1], u = Math.max(0, Math.min(1, (ct - ta) / (tb - ta)));
  return [0, 1, 2, 3].map((j) => ga[j] + (gb[j] - ga[j]) * u) as [number, number, number, number];
};
const RCS = (clip: string, ct: number) => {
  const [a0, a1, b0, b1] = gut(clip, ct), [bt, bb, bl, br] = boxAt(clip, ct), x = Math.max(0, bl), w = Math.min(1079, br) - x + 1;
  return { top: { x, y: bt, w, h: a0 - bt } as Rc, mid: { x, y: a1 + 1, w, h: b0 - a1 - 1 } as Rc, bot: { x, y: b1 + 1, w, h: bb - b1 } as Rc, g: [a0, a1, b0, b1], box: { x, y: bt, w, h: bb - bt } as Rc };
};

// ---------------- the real film timeline (clip, film start, clip time at film start) ----------------
const T_WHIP1 = wt(13), T_WHIP2 = wt(62), T_WHIP3 = wt(74), WD = 4 / 30;       // 4.10, 23.86, 29.66
const T_P2B = T_WHIP1 - WD + 5.55, T_M1 = 13.95, T_TAKE = wt(48), T_P3 = T_TAKE - 0.06; // 18.42
const T_M2A = 36.78, T_GAL = 37.94, T_M2B = 44.64, T_P5 = wt(119) - 1.16, T_M3 = wt(134), T_END = 56.43;      // 52.26

// ---------------- generic bits ----------------
const Vid: React.FC<{ clip: string; from: number; to: number; ct0: number; style?: React.CSSProperties }> = ({ clip, from, to, ct0, style }) => (
  <Sequence from={F(from)} durationInFrames={Math.max(1, F(to) - F(from))} layout="none">
    <OffthreadVideo src={staticFile(`bethlehem/clips/${clip}.mp4`)} startFrom={F(ct0)} muted style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, objectFit: "cover", ...style }} />
  </Sequence>
);
const whip = (t: number, end: number, vertical = false) => {
  const s = L(t, end - WD, end, 0, 1, OUT), bl = t >= end - WD && t < end ? 14 * Math.sin(Math.PI * Math.min(1, (t - (end - WD)) / WD + 0.2)) : 0;
  const d = vertical ? 1920 : 1080;
  return { inc: { x: vertical ? 0 : (1 - s) * d, y: vertical ? (1 - s) * d : 0, b: bl }, out: { x: vertical ? 0 : -s * d, y: vertical ? -s * d : 0, b: bl } };
};
const shakeAt = (t: number, hit: number, amp = 2.2): [number, number] => { const k = (t - hit) * 30; if (k < 0 || k >= 6) return [0, 0]; const a = (6 - k) * amp; return [a * Math.sin(k * 2.7), a * Math.cos(k * 3.3)]; };
const PageBox: React.FC<{ a: number; b: number; x?: number; y?: number; blur?: number; children: React.ReactNode }> = ({ a, b, x = 0, y = 0, blur = 0, children }) => (
  <div style={{ position: "absolute", inset: 0, visibility: "visible", transform: `translate(${x}px,${y}px)`, filter: blur > 0.5 ? `blur(${blur}px)` : undefined, display: "block" }} data-a={a} data-b={b}>{children}</div>
);
const Streaks: React.FC<{ t: number; end: number; vertical?: boolean }> = ({ t, end, vertical }) => {
  if (t < end - WD - 1 / 30 || t > end + 1 / 30) return null;
  const o = L(t, end - WD, end - WD + 1 / 30, 0, 1) * L(t, end - 1 / 30, end + 1 / 30, 1, 0);
  return <svg style={{ position: "absolute", left: 0, top: 0, opacity: o }} width={1080} height={1920}>
    {Array.from({ length: 9 }).map((_, i) => vertical
      ? <line key={i} x1={60 + 120 * i + 20 * hash(i)} y1={0} x2={60 + 120 * i + 20 * hash(i)} y2={1920} stroke={INK} strokeWidth={2 + 3 * hash(i + 4)} opacity={0.35} />
      : <line key={i} x1={0} y1={100 + 200 * i + 30 * hash(i)} x2={1080} y2={100 + 200 * i + 30 * hash(i)} stroke={INK} strokeWidth={2 + 3 * hash(i + 4)} opacity={0.35} />)}
  </svg>;
};

// rack focus (grid_choreography): keys [time, focusPanel(0 top,1 mid,2 bottom,-1 none)]
const rackDims = (t: number, keys: [number, number][]): [number, number, number] => {
  const vec = (f: number) => (f < 0 ? [0, 0, 0] : [0, 1, 2].map((i) => (i === f ? 0 : 1)));
  let prev = [0, 0, 0], run = [0, 0, 0];
  for (const [kt, f] of keys) { if (t < kt) break; const tg = vec(f), u = L(t, kt, kt + 0.3, 0, 1, INOUT); run = tg.map((v, i) => prev[i] + (v - prev[i]) * u); prev = tg; }
  return run as [number, number, number];
};
// film check v3 fix: a calm night-sky panel covers P3's camels + Herod panels during the birth (no king under
// "Jesus, the King, was born"; no wise men beside the manger). One gold star over Bethlehem.
const NightCover: React.FC<{ r: Rc; t: number; op?: number; star?: boolean; seed?: number }> = ({ r, t, op = 1, star, seed = 0 }) => op <= 0.01 ? null : (
  <div style={{ position: "absolute", left: r.x, top: r.y, width: r.w, height: r.h, overflow: "hidden", opacity: op, background: `linear-gradient(${NIGHT2}, ${NIGHT})` }}>
    <svg style={{ position: "absolute", left: 0, top: 0 }} width={r.w} height={r.h}>
      {Array.from({ length: 70 }).map((_, i) => <circle key={i} cx={hash(i + seed) * r.w} cy={hash(i * 3 + 7 + seed) * r.h} r={1.2 + 2.2 * hash(i * 5 + 1 + seed)}
        fill={CREAM} opacity={0.35 + 0.45 * (0.5 + 0.5 * Math.sin(t * 1.3 + i))} />)}
      {star && <g transform={`translate(${r.w * 0.5},${r.h * 0.42}) scale(${1 + 0.05 * Math.sin(t * 2)})`}>
        <circle r={70} fill={GOLD} opacity={0.18} />
        <path d="M0,-46 L11,-11 L46,0 L11,11 L0,46 L-11,11 L-46,0 L-11,-11 Z" fill={GOLD} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      </g>}
    </svg>
    <div style={{ position: "absolute", inset: 0, border: `7px solid ${INK}` }} />
  </div>
);
const Dim: React.FC<{ r: Rc; a: number }> = ({ r, a }) => a <= 0.01 ? null : (
  <div style={{ position: "absolute", left: r.x, top: r.y, width: r.w, height: r.h, background: `rgba(10,12,30,${0.42 * a})`, backgroundImage: "radial-gradient(rgba(0,0,0,0.5) 1.4px, transparent 1.6px)", backgroundSize: "9px 9px", opacity: a }} />
);

// panel clone (for slams): the same clip, clipped to one panel, pushed
const PanelClone: React.FC<{ clip: string; from: number; ct0: number; to: number; r: Rc; scale: number; rot?: number; tx?: number; border?: number; shadow?: boolean; op?: number }> = ({ clip, from, ct0, to, r, scale, rot = 0, tx = 0, border = 8, shadow = true, op = 1 }) => (
  <div style={{ position: "absolute", left: r.x, top: r.y, width: r.w, height: r.h, boxSizing: "border-box", overflow: "hidden", border: `${border}px solid ${INK}`, background: "#000", opacity: op,
    boxShadow: shadow ? `10px 12px 0 rgba(18,16,20,${Math.min(1, op)})` : undefined, transform: `translateX(${tx}px) rotate(${rot}deg) scale(${scale})` }}>
    <Vid clip={clip} from={from} to={to} ct0={ct0} style={{ left: -r.x - border, top: -r.y - border }} />
  </div>
);

// ---------------- speed lines + impact burst ----------------
const Speed: React.FC<{ k: number; y0: number; y1: number; right?: boolean }> = ({ k, y0, y1, right }) => {
  if (k < 0 || k > 9) return null;
  const o = 0.8 * L(k, 0, 2, 0, 1) * L(k, 5, 9, 1, 0);
  return <svg style={{ position: "absolute", left: 0, top: 0, opacity: o }} width={1080} height={1920}>
    {Array.from({ length: 14 }).map((_, i) => { const y = y0 + (y1 - y0) * hash(i + 3), len = 50 + 130 * hash(i + 9);
      return right ? <line key={i} x1={1040} y1={y} x2={1040 - len} y2={y - 6} stroke={INK} strokeWidth={3 + 4 * hash(i)} strokeLinecap="round" />
        : <line key={i} x1={30} y1={y} x2={30 + len} y2={y - 6} stroke={INK} strokeWidth={3 + 4 * hash(i)} strokeLinecap="round" />; })}
  </svg>;
};
const Burst: React.FC<{ x: number; y: number; k: number; r?: number }> = ({ x, y, k, r = 70 }) => {
  if (k < 0 || k > 12) return null;
  const s = L(k, 0, 4, 0.3, 1, BACK), o = L(k, 7, 12, 1, 0);
  const pts = Array.from({ length: 24 }).map((_, i) => { const a = i * Math.PI / 12, rr = i % 2 ? r * 0.45 : r * (0.85 + 0.3 * hash(i)); return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`; }).join(" ");
  return <svg style={{ position: "absolute", left: 0, top: 0, opacity: o, overflow: "visible" }} width={1080} height={1920}>
    <g transform={`translate(${x},${y}) scale(${s})`}><polygon points={pts} fill="#FFFBEA" stroke={INK} strokeWidth={6} strokeLinejoin="round" /></g></svg>;
};

// ---------------- footprint (sandal sole): dashed = not done, gold = done ----------------
const SOLE = "M0,-26 C9,-26 12,-15 11,-4 C10,6 8,12 8,18 C8,26 -8,26 -8,18 C-8,12 -11,5 -11,-5 C-11,-16 -8,-26 0,-26 Z";
const Print: React.FC<{ x: number; y: number; ang: number; s?: number; t: number; at: number; goldAt?: number; side: number; out?: number }> = ({ x, y, ang, s = 1, t, at, goldAt, side, out }) => {
  if (t < at) return null;
  const k = (t - at) * 30, sc = s * L(k, 0, 3, 1.5, 1, OUT);
  const gold = goldAt !== undefined && t >= goldAt;
  const gk = gold ? (t - goldAt!) * 30 : 0;
  return (
    <g transform={`translate(${x + side * 13},${y}) rotate(${ang}) scale(${sc * (gold ? L(gk, 0, 3, 1.35, 1, OUT) : 1)})`} opacity={out === undefined ? 1 : out}>
      <path d={SOLE} fill={gold ? GOLD : "none"} stroke={gold ? INK : CREAM} strokeWidth={gold ? 4 : 3.5} strokeDasharray={gold ? undefined : "6 5"} strokeLinejoin="round" />
    </g>
  );
};

// ---------------- THE PROMISE PANEL: dashed ink frame -> the same frame as one solid gold line ----------------
const rectPts = (r: Rc, seed: number): [number, number][] => {
  const per = 2 * (r.w + r.h), n = Math.max(12, Math.round(per / 26)), o: [number, number][] = [];
  for (let i = 0; i <= n; i++) {
    const s = (i / n) * per, j = (hash(i + seed) - 0.5) * 3.6; let x = 0, y = 0;
    if (s < r.w) { x = r.x + s; y = r.y + j; } else if (s < r.w + r.h) { x = r.x + r.w + j; y = r.y + (s - r.w); }
    else if (s < 2 * r.w + r.h) { x = r.x + r.w - (s - r.w - r.h); y = r.y + r.h + j; } else { x = r.x + j; y = r.y + r.h - (s - 2 * r.w - r.h); }
    o.push([x, y]);
  }
  o[o.length - 1] = o[0]; return o;
};
const ptsD = (p: [number, number][]) => p.map((q, i) => `${i ? "L" : "M"}${q[0].toFixed(1)} ${q[1].toFixed(1)}`).join(" ");
const PF: React.FC<{ id: string; r: Rc; dashP: number; goldP: number; seed?: number; sw?: number; op?: number }> = ({ id, r, dashP, goldP, seed = 7, sw = 8, op = 1 }) => {
  if (dashP <= 0 && goldP <= 0) return null;
  const d = ptsD(rectPts(r, seed)), per = 2 * (r.w + r.h), dash = 26 / per, gap = 18 / per;
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, opacity: op, overflow: "visible" }} width={1080} height={1920}>
      <defs><mask id={id} maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}><path d={d} fill="none" stroke="#fff" strokeWidth={40} {...draw(dashP)} /></mask></defs>
      <g mask={`url(#${id})`}>
        <path d={d} fill="none" stroke={INK} strokeWidth={sw + 6} strokeLinecap="butt" pathLength={1} strokeDasharray={`${dash} ${gap}`} />
        <path d={d} fill="none" stroke={CREAM} strokeWidth={sw - 2} strokeLinecap="butt" pathLength={1} strokeDasharray={`${dash} ${gap}`} />
      </g>
      {goldP > 0 && <>
        <path d={d} fill="none" stroke={INK} strokeWidth={sw + 8} strokeLinejoin="round" {...draw(goldP)} />
        <path d={d} fill="none" stroke={GOLD} strokeWidth={sw} strokeLinejoin="round" {...draw(goldP)} />
      </>}
    </svg>
  );
};

// ---------------- small bits: crown, caption box, chip, big comic lettering ----------------
const Crown: React.FC<{ p: number }> = ({ p }) => (
  <g>
    <path d="M-34,16 L-40,-16 L-20,2 L0,-26 L20,2 L40,-16 L34,16 Z" fill={GOLD} fillOpacity={L(p, 0.6, 1, 0, 1)} stroke={INK} strokeWidth={5} strokeLinejoin="round" {...draw(p)} />
    <path d="M-33,24 L33,24" stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(p, 0.7, 1, 0, 1))} />
    {p >= 1 && [-40, 0, 40].map((x, i) => <circle key={i} cx={x} cy={i === 1 ? -28 : -18} r={4.5} fill={CREAM} stroke={INK} strokeWidth={2.5} />)}
  </g>
);
const Cap: React.FC<{ text: string; x: number; y: number; t: number; at: number; until?: number; size?: number }> = ({ text, x, y, t, at, until = 999, size = 40 }) => (t < at || t >= until) ? null : (
  <div style={{ position: "absolute", left: x, top: y, padding: "2px 14px", background: "#FFE14D", border: `4px solid ${INK}`, boxShadow: `5px 5px 0 ${INK}`, whiteSpace: "nowrap",
    fontFamily: "BangersB", fontSize: size, letterSpacing: 2, color: INK, opacity: L(t, until - 0.1, until, 1, 0), transform: `scale(${L((t - at) * 30, 0, 4, 1.4, 1, OUT)})`, transformOrigin: "0 0" }}>{text}</div>
);
const Chip: React.FC<{ text: string; left?: number; right?: number; top: number; rot?: number; op?: number; cream?: boolean; dashed?: boolean; size?: number }> = ({ text, left, right, top, rot = 0, op = 1, cream, dashed, size = 28 }) => (
  <div style={{ position: "absolute", left, right, top, height: size * 1.5, padding: "0 14px", boxSizing: "border-box", background: cream ? CREAM : GOLD, border: `3px ${dashed ? "dashed" : "solid"} ${INK}`,
    borderRadius: 16, fontFamily: "KalamB", fontSize: size, lineHeight: `${size * 1.28}px`, color: INK, whiteSpace: "nowrap", opacity: op, transform: `rotate(${rot}deg)` }}>{text}</div>
);
const Big: React.FC<{ text: string; k: number; left: number; top: number; rot: number; color: string; size?: number; stroke?: number }> = ({ text, k, left, top, rot, color, size = 140, stroke = 9 }) => k < 0 ? null : (
  <div style={{ position: "absolute", left, top, fontFamily: "BangersB", fontSize: size, lineHeight: `${size * 1.07}px`, color, WebkitTextStroke: `${stroke}px ${INK}`, paintOrder: "stroke fill", textShadow: `${stroke * 0.8}px ${stroke * 0.8}px 0 ${INK}`,
    whiteSpace: "nowrap", transform: `rotate(${L(k, 0, 6, rot * 2.2, rot, OUT)}deg) scale(${L(k, 0, 4, 1.6, 1, OUT)})`, opacity: L(k, 0, 1.5, 0, 1) }}>{text}</div>
);

// ---------------- read-along pill (owner-locked Mockers style) ----------------
const TXT: Record<number, string> = {};
type W = { t: string; at: number; m?: string[] };
const r = (a: number, b: number, marks: Record<number, string[]> = {}): W[] => { const o: W[] = []; for (let i = a; i <= b; i++) o.push({ t: TXT[i] ?? (WORDS as any[])[i].w, at: wt(i), m: marks[i] }); return o; };
type PillSpec = { a: number; b: number; cy: number | ((t: number) => number); lines: W[][]; sacred?: boolean; speech?: boolean; kjv?: boolean; hold2?: boolean; ul?: number; sp?: string; chip?: string };
const lowGut = (t: number) => {
  if (t >= T_P3 && t < T_WHIP2) return gut("P3", t - T_P3)[3] - 4;
  if (t >= T_WHIP2 && t < T_WHIP3) return gut("P4", t - (T_WHIP2 - WD))[2] - 62;
  return 1450;
};
const PILLS: PillSpec[] = [
  { a: 0.0, b: 3.28, cy: 1330, lines: [r(0, 3, { 3: ["gold"] }), r(4, 9)] },
  { a: 4.10, b: 5.88, cy: 1450, lines: [r(13, 15), r(16, 17)] },
  { a: 5.94, b: 8.26, cy: 1450, lines: [r(18, 21), r(22, 24)] },
  { a: 8.28, b: 11.2, cy: (t: number) => (t < T_P2B ? 1450 : 1720), lines: [r(25, 27, { 25: ["gold"] }), r(28, 31)] },
  { a: 11.24, b: 12.60, cy: 1720, kjv: true, lines: [r(32, 34)] },
  { a: 12.64, b: 13.84, cy: 1720, lines: [r(35, 37)] },
  { a: 14.98, b: 16.80, cy: 1450, lines: [r(40, 42), r(43, 44, { 44: ["gold"] })] },
  { a: 16.84, b: 18.36, cy: 1450, lines: [r(45, 47, { 47: ["gold"] })] },
  { a: 18.46, b: 20.60, cy: lowGut, sacred: true, lines: [r(48, 50), r(51, 52, { 52: ["gold"] })] },
  { a: 20.66, b: 22.48, cy: lowGut, sacred: true, lines: [r(53, 57)] },
  { a: 22.90, b: 24.66, cy: lowGut, lines: [r(58, 61), r(62, 64)] },
  { a: 25.18, b: 27.05, cy: lowGut, lines: [r(65, 67, { 66: ["gold"] }), r(68, 69)] },
  { a: 27.06, b: 28.78, cy: lowGut, speech: true, sp: "A SCRIBE", chip: "MATTHEW 2:5", lines: [r(70, 73, { 71: ["gold"] })] },
  { a: 29.66, b: 31.10, cy: 1450, lines: [r(74, 77, { 74: ["gold"] })] },
  { a: 32.04, b: 34.95, cy: 1450, lines: [r(78, 81), r(82, 84)] },
  { a: 35.00, b: 35.90, cy: 1450, lines: [r(85, 88, { 88: ["gold"] })] },
  { a: 35.92, b: 37.91, cy: 1450, sacred: true, lines: [r(89, 92)] },
  { a: 38.06, b: 39.70, cy: 1750, lines: [r(93, 95), r(96, 97, { 97: ["gold"] })] },
  { a: 39.76, b: 40.76, cy: 1750, lines: [r(98, 99)] },
  { a: 40.80, b: 42.45, cy: 1750, lines: [r(100, 103), r(104, 105)] },
  { a: 42.52, b: 44.10, cy: 1750, lines: [r(106, 108), r(109, 109, { 109: ["gold"] })] },
  { a: 44.12, b: 45.15, cy: 1750, lines: [r(110, 113, { 112: ["gold"] })] },
  { a: 45.20, b: 47.05, cy: 1450, sacred: true, lines: [r(114, 116), r(117, 118)] },
  { a: 47.14, b: 48.80, cy: 1450, sacred: true, lines: [r(119, 123)] },
  { a: 48.92, b: 50.66, cy: 1450, sacred: true, lines: [r(124, 128)] },
  { a: 50.82, b: 51.76, cy: 1450, sacred: true, lines: [r(129, 132)] },
  { a: 51.86, b: 53.47, cy: 1450, sacred: true, lines: [r(133, 137)] },
  { a: 53.50, b: 56.78, cy: 1440, sacred: true, hold2: true, ul: 55.44, lines: [r(138, 142), r(143, 146)] },
];
const PillView: React.FC<{ t: number; s: PillSpec }> = ({ t, s }) => {
  const { a, b, lines, sacred, speech, kjv, hold2 } = s;
  if (t < a || t >= b) return null;
  const cy = typeof s.cy === "function" ? s.cy(t) : s.cy;
  const age = (t - a) * 30;
  const op = L(t, a, a + (sacred ? 0.3 : 0.1), 0, 1) * L(t, b - 0.13, b, 1, 0);
  const h = lines.length * 62 + 40, top = cy - h / 2;
  const pop = speech ? L(age, 0, 6, 0.85, 1, BACK) : 1;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, opacity: op }}>
      {(speech || kjv) && ( // see-through tail up to the quoted voice (scribe / prophet)
        <svg style={{ position: "absolute", left: 0, top: 0, transform: `scale(${pop})`, transformOrigin: `540px ${cy}px` }} width={1080} height={1920}>
          {speech
            ? <path d={`M700 ${top + 4} C716 ${top - 40} 760 ${top - 86} 800 ${top - 118} C792 ${top - 70} 790 ${top - 30} 800 ${top + 4}`} fill={PILL_FILL} stroke={PILL_EDGE} strokeWidth={4} strokeLinejoin="round" />
            : <path d={`M500 ${top + 4} C510 ${top - 36} 540 ${top - 70} 575 ${top - 104} C580 ${top - 60} 590 ${top - 28} 610 ${top + 4}`} fill={PILL_FILL} stroke={PILL_EDGE} strokeWidth={4} strokeLinejoin="round" />}
        </svg>)}
      <div style={{ position: "absolute", left: 100, top, width: 880, height: h, boxSizing: "border-box", borderRadius: 46, background: PILL_FILL, border: `4px solid ${PILL_EDGE}`, transform: `scale(${pop})`,
        display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center", fontFamily: "KalamB", fontSize: 54, lineHeight: "62px", color: INK }}>
        {lines.map((row, li) => {
          const lo = hold2 && li === 1 ? L(t, row[0].at - 0.03, row[0].at + 0.25, 0, 1) : 1;
          return <div key={li} style={{ opacity: lo, position: "relative" }}>{row.map((w, wi) => {
            const k = (t - w.at) * 30, on = k >= 0;
            const gold = (w.m || []).includes("gold") && on, und = (w.m || []).includes("under2") && on;
            return <React.Fragment key={wi}>{wi > 0 ? " " : ""}<span style={{ display: "inline-block", position: "relative", opacity: on ? 1 : 0.38, transform: `scale(${on ? L(k, 0, 5, 1.07, 1, OUT) : 1})`,
              background: gold ? `rgba(246,185,35,${L(k, 0, 4, 0, 0.95)})` : undefined, borderRadius: 8, padding: "0 7px", margin: "0 -7px" }}>{w.t}
              {und && <svg style={{ position: "absolute", left: 0, top: 58, overflow: "visible" }} width={10} height={20}>
                <line x1={2} y1={0} x2={150} y2={-2} stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(k, 0, 6, 0, 1))} />
                <line x1={6} y1={9} x2={146} y2={8} stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(k, 2, 8, 0, 1))} /></svg>}
            </span></React.Fragment>;
          })}
            {hold2 && li === 1 && t >= s.ul! && <svg style={{ position: "absolute", left: 270, top: 52, overflow: "visible" }} width={340} height={20}>
              <path d="M2,6 C60,0 120,10 200,4 C250,0 300,8 338,4" fill="none" stroke={INK} strokeWidth={11} strokeLinecap="round" opacity={0.55} {...draw(L(t, s.ul!, s.ul! + 0.78, 0, 1, SINE))} />
              <path d="M2,6 C60,0 120,10 200,4 C250,0 300,8 338,4" fill="none" stroke={GOLD} strokeWidth={7} strokeLinecap="round" {...draw(L(t, s.ul!, s.ul! + 0.78, 0, 1, SINE))} /></svg>}
          </div>;
        })}
      </div>
      {speech && <>
        <Chip text={s.sp!} left={126 - L(age, 0, 6, 20, 0, OUT)} top={top + h - 14} />
        <Chip text={s.chip!} right={126 - L(age, 0, 6, 20, 0, OUT)} top={top + h - 14} />
      </>}
      {kjv && <>
        <Chip text="MICAH" left={126 - L(age, 0, 6, 20, 0, OUT)} top={top + h - 14} />
        <Chip text="MICAH 5:2" right={126 - L(age, 0, 6, 20, 0, OUT)} top={top + h - 14} />
      </>}
    </div>
  );
};

// ---------------- map panel (middle panel of the P1 page) - from the approved test ----------------
const MW = 1052, MH = 640;
const JER: [number, number] = [330, 170], BET: [number, number] = [610, 500];
const ROADPTS: [number, number][] = [[365, 215], [420, 290], [480, 350], [540, 410], [590, 455], [612, 470], [622, 482]];
const Hill: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g transform={`translate(${x},${y})`}>
    <path d="M-46,18 L-12,-26 L6,-6 L22,-22 L52,18 Z" fill="#24397E" stroke={INK} strokeWidth={5} strokeLinejoin="round" />
    {[0, 1, 2, 3].map((j) => <line key={j} x1={-30 + j * 9} y1={14} x2={-14 + j * 9} y2={-10 + j * 2} stroke={INK} strokeWidth={2} opacity={0.75} />)}
  </g>
);
const MapDefs: React.FC<{ pre: string }> = ({ pre }) => (
  <defs>
    <pattern id={`${pre}dots`} width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.6" fill="#000" opacity="0.32" /></pattern>
    <pattern id={`${pre}hatch`} width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="10" stroke={INK} strokeWidth="2.2" opacity="0.5" /></pattern>
    <radialGradient id={`${pre}nightg`} cx="0.45" cy="0.4" r="0.8"><stop offset="0" stopColor={NIGHT} /><stop offset="1" stopColor={NIGHT2} /></radialGradient>
  </defs>
);
const CityG: React.FC<{ pre: string }> = ({ pre }) => (
  <>
    <path d="M-170,40 L-170,-40 L-150,-40 L-150,-52 L-130,-52 L-130,-40 L-90,-40 L-90,-52 L-70,-52 L-70,-40 L-30,-40 L-30,-80 L10,-80 L10,-40 L60,-40 L60,-52 L80,-52 L80,-40 L120,-40 L120,-62 L150,-62 L150,40 Z" fill={OCHRE} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
    <path d="M120,-62 L150,-62 L150,40 L120,40 Z" fill={`url(#${pre}hatch)`} />
    <path d="M-25,-80 C-25,-118 5,-118 5,-80" fill={OCHRE} stroke={INK} strokeWidth={7} />
    <path d="M-22,40 L-22,4 C-22,-18 8,-18 8,4 L8,40 Z" fill={INK} />
    <path d="M-170,40 L150,40" stroke={OCHRE2} strokeWidth={8} />
  </>
);
const HousesG: React.FC<{ pre: string }> = ({ pre }) => (
  <>
    {[[-70, 0, 46, 40], [-22, -16, 52, 56], [34, 4, 44, 36]].map(([x, y, w, h], i) => (
      <g key={i}><rect x={x} y={y - h} width={w} height={h} fill={OCHRE} stroke={INK} strokeWidth={6} strokeLinejoin="round" />
        <rect x={x + w * 0.62} y={y - h} width={w * 0.38} height={h} fill={`url(#${pre}hatch)`} />
        <rect x={x + w * 0.35} y={y - h * 0.5} width={w * 0.24} height={h * 0.5} fill={INK} /></g>))}
    <path d="M-90,2 L90,2" stroke={INK} strokeWidth={6} />
  </>
);
const MapMid: React.FC<{ t: number }> = ({ t }) => (
  <svg width="100%" height="100%" viewBox={`0 0 ${MW} ${MH}`} preserveAspectRatio="xMidYMid slice" style={{ display: "block" }}>
    <MapDefs pre="m" />
    <rect width={MW} height={MH} fill="url(#mnightg)" />
    <rect width={MW} height={MH} fill="url(#mdots)" />
    <path d="M930,110 C990,120 1000,260 985,400 C972,520 950,600 905,600 C870,596 885,470 890,360 C895,250 880,104 930,110 Z" fill={SEA} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
    <path d="M930,110 C990,120 1000,260 985,400" fill="none" stroke={CREAM} strokeWidth={3} opacity={0.5} transform="translate(-14,6)" />
    {[[140, 120], [700, 130], [180, 420], [760, 300], [120, 560], [800, 520], [470, 600], [260, 300]].map(([x, y], i) => <Hill key={i} x={x} y={y} />)}
    <path d={`M${ROADPTS.map((p) => p.join(",")).join(" L")}`} fill="none" stroke={INK} strokeWidth={58} strokeLinecap="round" strokeLinejoin="round" />
    <path d={`M${ROADPTS.map((p) => p.join(",")).join(" L")}`} fill="none" stroke={ROAD} strokeWidth={44} strokeLinecap="round" strokeLinejoin="round" />
    <path d={`M${ROADPTS.map((p) => p.join(",")).join(" L")}`} fill="none" stroke="url(#mdots)" strokeWidth={44} strokeLinecap="round" strokeLinejoin="round" />
    <g transform={`translate(${JER[0]},${JER[1]})`}><CityG pre="m" /></g>
    <g transform={`translate(${BET[0]},${BET[1]})`}><HousesG pre="m" /></g>
    {ROADPTS.slice(0, 7).map((p, i) => {
      const q = ROADPTS[Math.min(i + 1, ROADPTS.length - 1)], ang = Math.atan2(q[1] - p[1], q[0] - p[0]) * 180 / Math.PI + 90;
      const pulse = i === 0 && t > 31.12 && t < 32.22 ? 1 + 0.18 * Math.sin((t - 31.12) * 9) : 1;
      return <Print key={i} x={p[0]} y={p[1]} ang={ang} s={0.95 * pulse} t={t} at={wt(76) + i * 2 / 30} goldAt={wt(88) + i * 2 / 30} side={i % 2 ? 1 : -1} />;
    })}
    <g transform={`translate(${BET[0]},${BET[1] - 110})`}><polygon points="0,-30 8,-9 30,-8 12,5 18,27 0,14 -18,27 -12,5 -30,-8 -8,-9" fill={GOLD} stroke={INK} strokeWidth={5} strokeLinejoin="round" /></g>
  </svg>
);


// ---------------- the GALILEE map (36.58-45): the one full-height map, a panel with white margin + ink border ----------------
const SPL: Rc = { x: 14, y: 14, w: 1052, h: 1892 };
const WH = 2900;
const NAZ: [number, number] = [330, 400], JERS: [number, number] = [520, 1500], BETS: [number, number] = [640, 1920];
const ROUTE: [number, number][] = [[345, 450], [390, 700], [430, 980], [480, 1250], [525, 1450], [575, 1650], [620, 1820], [640, 1900]];
const BETFR = { cx: 640, cy: 1840, w: 440, h: 210 };
const GALFR: Rc = { x: 30, y: 170, w: 970, h: 440 };
const T_GCAM0 = 42.49, T_GCAM1 = 43.79, GCAM = 980;
const camG = (t: number) => L(t, T_GCAM0, T_GCAM1, 0, GCAM, SINE);
const GStar: React.FC<{ gold: boolean; k: number }> = ({ gold, k }) => (
  <g transform={`translate(${BETS[0]},${BETS[1] - 170}) scale(${1.7 * L(k, 0, 6, 0.3, 1, BACK)})`}>
    {gold && <circle r={52} fill={GOLD} opacity={0.25} />}
    <polygon points="0,-30 8,-9 30,-8 12,5 18,27 0,14 -18,27 -12,5 -30,-8 -8,-9" fill={gold ? GOLD : CREAM} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
  </g>
);
const MapGal: React.FC<{ t: number }> = ({ t }) => {
  const cy = camG(t);
  const hills: [number, number][] = [[440, 160], [600, 900], [330, 1250], [700, 1650], [420, 1900], [880, 1900], [300, 2050], [140, 300], [700, 250], [200, 700], [760, 640], [180, 1100], [800, 1050], [260, 1500], [820, 1400], [180, 1800], [820, 1750], [420, 2150], [700, 2200], [240, 2500], [820, 2450], [520, 2700], [140, 2300], [760, 2020], [160, 2650], [880, 2750]];
  const roadD = `M${ROUTE.map((p) => p.join(",")).join(" L")}`;
  const kB = (t - wt(112)) * 30, [sx, sy] = shakeAt(t, wt(112), 3);
  const qk = (t - wt(100)) * 30;
  const frG = t >= wt(97) ? <PF id="pfgal" r={{ ...GALFR, y: GALFR.y - cy }} dashP={L(t, wt(97), wt(97) + 0.4, 0, 1)} goldP={0} seed={11} sw={8} op={L(t, 42.54, 42.84, 1, 0.55)} /> : null;
  const betR: Rc = { x: BETFR.cx - BETFR.w / 2, y: BETFR.cy - BETFR.h / 2 - cy, w: BETFR.w, h: BETFR.h };
  return (
    <div style={{ position: "absolute", left: SPL.x, top: SPL.y, width: SPL.w, height: SPL.h, overflow: "hidden", border: `7px solid ${INK}`, boxSizing: "border-box", background: NIGHT2, transform: `translate(${sx}px,${sy}px)` }}>
      <svg width={SPL.w} height={WH} viewBox={`0 0 ${SPL.w} ${WH}`} style={{ position: "absolute", left: 0, top: -cy, display: "block" }}>
        <MapDefs pre="s" />
        <rect width={SPL.w} height={WH} fill="url(#snightg)" />
        <rect width={SPL.w} height={WH} fill="url(#sdots)" />
        <path d={`M0,0 L80,0 C60,500 110,1000 50,1500 C20,2000 80,2500 40,${WH} L0,${WH} Z`} fill={SEA} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        <path d="M80,0 C60,500 110,1000 50,1500 C20,2000 80,2500 40,2900" fill="none" stroke={CREAM} strokeWidth={3} opacity={0.5} transform="translate(22,6)" />
        <path d="M800,330 C860,300 940,330 950,430 C958,520 880,560 820,520 C770,480 760,360 800,330 Z" fill={SEA} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        <path d="M870,550 C900,700 840,850 890,1000 C930,1150 880,1300 920,1500" fill="none" stroke={INK} strokeWidth={30} strokeLinecap="round" />
        <path d="M870,550 C900,700 840,850 890,1000 C930,1150 880,1300 920,1500" fill="none" stroke={SEA} strokeWidth={18} strokeLinecap="round" />
        <path d="M900,1520 C990,1540 1000,1800 985,2050 C970,2250 930,2380 880,2380 C840,2370 850,2150 856,1900 C860,1700 850,1530 900,1520 Z" fill={SEA} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        {hills.map(([x, y], i) => <g key={i} transform={`translate(${x},${y}) scale(1.6) translate(${-x},${-y})`}><Hill x={x} y={y} /></g>)}
        <path d={roadD} fill="none" stroke={INK} strokeWidth={86} strokeLinecap="round" strokeLinejoin="round" />
        <path d={roadD} fill="none" stroke={ROAD} strokeWidth={70} strokeLinecap="round" strokeLinejoin="round" />
        <path d={roadD} fill="none" stroke="url(#sdots)" strokeWidth={70} strokeLinecap="round" strokeLinejoin="round" />
        <g transform={`translate(${NAZ[0]},${NAZ[1]}) scale(2.1)`}><HousesG pre="s" /></g>
        <g transform={`translate(${JERS[0]},${JERS[1]}) scale(1.7)`}><CityG pre="s" /></g>
        <g transform={`translate(${BETS[0]},${BETS[1]}) scale(2.1)`}><HousesG pre="s" /></g>
        {t >= 43.0 && <GStar gold={t >= wt(109)} k={(t - 43.0) * 30} />}
      </svg>
      {frG}
      {t >= 42.54 && <PF id="pfbet" r={betR} dashP={L(t, 42.54, 42.87, 0, 1)} goldP={L(t, wt(109), wt(109) + 0.3, 0, 1, SINE)} seed={7} sw={t < wt(109) ? 8 : 10} />}
      <Cap text="NAZARETH" x={NAZ[0] + 130 - 7} y={NAZ[1] - 120 - cy} t={t} at={T_GAL + 0.25} size={52} />
      <Cap text="GALILEE" x={60} y={GALFR.y - 52 - cy} t={t} at={wt(97)} size={84} />
      {t >= wt(100) && t < 43.0 && <div style={{ opacity: L(t, 42.54, 42.94, 1, 0) }}><Big text="?" k={qk} left={600 - 7} top={335 - cy} rot={9} color={GOLD} size={330} stroke={12} /></div>}
      <Cap text="JERUSALEM" x={JERS[0] + 170 - 7} y={JERS[1] - 60 - cy} t={t} at={43.55} size={52} />
      <Cap text="BETHLEHEM" x={BETS[0] - 270 - 7} y={BETS[1] - 120 - cy} t={t} at={wt(109)} size={52} />
      <Burst x={BETS[0] - 7} y={BETS[1] - 170 - cy} k={kB} r={110} />
    </div>
  );
};

// the scroll strip (parchment): "ruler in Israel." then, in gold, "from everlasting."
const Scroll: React.FC<{ t: number; a: number; b: number }> = ({ t, a, b }) => {
  if (t < a || t >= b) return null;
  const age = (t - a) * 30, op = L(t, a, a + 0.1, 0, 1) * L(t, b - 0.25, b, 1, 0);
  const w1 = L(t, 11.27, 12.12, 0, 100, SINE), w2 = L(t, 13.86, 14.64, 0, 100, SINE);
  return (
    <div style={{ position: "absolute", left: 90, top: 1226, width: 900, height: 330, opacity: op, transform: `translateY(${L(age, 0, 6, -40, 0, OUT)}px) rotate(-1.2deg)` }}>
      <svg width={900} height={330} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <path d="M70,36 L830,36 C876,36 876,108 830,108 L830,224 C876,224 876,296 830,296 L70,296 C24,296 24,224 70,224 L70,108 C24,108 24,36 70,36 Z" fill="#F3E2B3" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
        <path d="M830,108 C800,108 800,36 830,36 M830,296 C800,296 800,224 830,224 M70,108 C100,108 100,36 70,36 M70,296 C100,296 100,224 70,224" fill="none" stroke={INK} strokeWidth={5} opacity={0.6} />
      </svg>
      <div style={{ position: "absolute", left: 90, top: 66, width: 720, fontFamily: "KalamB", fontSize: 76, lineHeight: "84px", color: INK, textAlign: "center" }}>
        <div style={{ clipPath: `inset(0 ${100 - w1}% 0 0)`, whiteSpace: "nowrap" }}>ruler in Israel.</div>
        <div style={{ position: "relative", whiteSpace: "nowrap", marginTop: 14 }}>
          <div style={{ position: "absolute", left: 60, right: 60, top: 10, height: 68, background: GOLD, borderRadius: 10, opacity: 0.95, clipPath: `inset(0 ${100 - w2}% 0 0)` }} />
          <div style={{ position: "relative", clipPath: `inset(0 ${100 - w2}% 0 0)` }}>from everlasting.</div>
        </div>
      </div>
      <Chip text="MICAH 5:2" right={30} top={278} rot={3} size={30} />
    </div>
  );
};

// ---------------- the film ----------------
export const BethlehemV9: React.FC = () => {
  const f = useCurrentFrame(), t = f / 30;
  const [h] = React.useState(() => delayRender("bv9fonts"));
  React.useEffect(() => {
    Promise.all([new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(), new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load()])
      .then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); continueRender(h); }).catch(() => continueRender(h));
  }, []);

  const w1 = whip(t, T_WHIP1), w2 = whip(t, T_WHIP2), w3 = whip(t, T_WHIP3, true);
  const K_KNEW = wt(3), K_GO = wt(12), K_HEROD = wt(66), K_WENT = wt(88);

  // A. hook
  const hookOn = t < T_WHIP1;
  const RH = RCS("P1", t);
  const [shHx, shHy] = (() => { const a = shakeAt(t, K_GO, 2.4), b = shakeAt(t, K_KNEW, 2.2); return [a[0] + b[0], a[1] + b[1]] as [number, number]; })();
  const rackH = rackDims(t, [[wt(2), 0], [wt(4), 2]]);
  const HRP: [number, number][] = [[550, 1870], [600, 1822], [650, 1782], [700, 1750], [750, 1720], [790, 1690], [806, 1657], [775, 1632], [750, 1620], [700, 1600], [650, 1595]];
  const hookPrints: [number, number, number, number][] = HRP.slice(0, 10).map(([x, y], i) => { const q = HRP[i + 1]; return [x, y, Math.atan2(q[0] - x, -(q[1] - y)) * 180 / Math.PI, 1.7 - 0.07 * i]; });
  const skK = (t - K_KNEW) * 30;

  // B. P2 Micah
  const p2On = t >= T_WHIP1 - WD && t < T_P2B, ctP2 = t - (T_WHIP1 - WD);
  const R2 = RCS("P2", Math.min(ctP2, 5.5));
  const rack2 = rackDims(t, [[T_WHIP1, 0], [wt(22), 2], [wt(26), 1]]);

  // C. P2 lamp + face (scroll strip) and M1 town + promise frame
  const p2bOn = t >= T_P2B && t < T_M1 + 0.1;
  const m1On = t >= T_M1 && t < T_TAKE + 0.1;
  const PR1: Rc = { x: 640, y: 690, w: 420, h: 210 };

  // F. P3 manger / camels
  const p3On = t >= T_P3 && t < T_WHIP2 + 1 / 30, ctP3 = t - T_P3;
  const R3 = RCS("P3", Math.min(5.8, Math.max(0, ctP3)));
  const rack3 = rackDims(t, [[T_P3, 0], [22.84, 1]]);
  const mangerFr = { ...R3.top, y: R3.top.y + 4, h: R3.top.h - 6 };
  const frTake = L(t, T_TAKE - 0.2, T_TAKE - 0.03, 0, 1, INOUT);
  const frRect: Rc = t < T_TAKE - 0.2 ? PR1 : t < T_TAKE ? { x: lerp(PR1.x, mangerFr.x, frTake), y: lerp(PR1.y, mangerFr.y, frTake), w: lerp(PR1.w, mangerFr.w, frTake), h: lerp(PR1.h, mangerFr.h, frTake) } : mangerFr;
  const dashP = L(t, wt(40), wt(40) + 10 / 30, 0, 1);
  const goldP = L(t, wt(50), wt(52) + 0.28, 0, 1, SINE);

  // G. P4 Herod
  const p4On = t >= T_WHIP2 - WD && t < T_WHIP3 + 1 / 30, ctP4 = t - (T_WHIP2 - WD);
  const R4 = RCS("P4", Math.min(8.6, ctP4));
  const rack4 = rackDims(t, [[T_WHIP2, -1], [wt(69) - 0.05, 1]]);
  const [shH4x, shH4y] = shakeAt(t, K_HEROD, 2.2);
  const kHerod = (t - K_HEROD) * 30;

  // H. P1b experts + map panel + wise men slam
  const p1bOn = t >= T_WHIP3 - WD && t < T_GAL + 0.1, ct1 = 1.3 + (t - (T_WHIP3 - WD));
  const [g1a, g1b, g2a, g2b] = gut("P1", Math.min(9.6, ct1)), RB = RCS("P1", Math.min(9.6, ct1));
  const top = { y0: 0, y1: g1a }, mid = { y0: g1b + 1, y1: g2a }, bot = { y0: g2b + 1, y1: 1920 };
  const mapWk = (t - 30.02) * 30, mwu = L(mapWk, 0, 8, 0, 1, INOUT);
  const mEdge = Array.from({ length: 34 }).map((_, i) => { const y = i * 30 - 10; return `${(mwu * 1180 - 60 + 40 * Math.sin(i * 1.7) + 26 * hash(i)).toFixed(0)}px ${y}px`; });
  const mapClip = mwu >= 1 ? undefined : `polygon(0px -20px, ${mEdge.join(", ")}, 0px 1000px)`;
  const rack1 = rackDims(t, [[T_WHIP3 - 0.14, -1], [wt(78), 0], [35.0, -1]]);
  const [shWx, shWy] = shakeAt(t, K_WENT, 2.2);
  const ck = (t - K_WENT) * 30, camelOn = ck >= 0;
  const camelX = L(ck, 0, 4, 1100, 0, OUT);
  const P3T = 2.4; const [, p3a, p3b] = gut("P3", P3T + Math.max(0, t - K_WENT));
  const RP: [number, number][] = [[560, 0.86], [512, 0.74], [560, 0.63], [606, 0.53], [570, 0.44], [530, 0.36], [565, 0.29]];
  const midH = mid.y1 - mid.y0;
  const mScale = Math.max(RB.mid.w / MW, midH / MH), mDX = RB.mid.x + (RB.mid.w - MW * mScale) / 2, mDY = mid.y0 + (midH - MH * mScale) / 2;
  const betS = { x: mDX + BET[0] * mScale, y: mDY + (BET[1] - 110) * mScale };
  const mapShown = t >= 30.02;

  // I. M2a iris from the mid-map star ("found the child")
  const m2aOn = t >= T_M2A && t < T_GAL + 0.45;
  const irisA = L((t - T_M2A) * 30, 0, 14, 0, 1500, INOUT);
  const maskA = `radial-gradient(circle at ${betS.x}px ${betS.y}px, #000 ${Math.max(0, irisA - 60)}px, transparent ${irisA}px)`;

  // J. Galilee map
  const galOn = t >= T_GAL && t < T_M2B + 1.0;
  const wipeK = (t - T_GAL) * 30, wu = L(wipeK, 0, 8, 0, 1, INOUT);
  const edgeS = Array.from({ length: 34 }).map((_, i) => { const y = i * 60 - 10; return `${(wu * 1180 - 60 + 40 * Math.sin(i * 1.7) + 26 * hash(i)).toFixed(0)}px ${y}px`; });
  const galClip = wu >= 1 ? undefined : `polygon(0px -20px, ${edgeS.join(", ")}, 0px 2000px)`;
  const betScr = { x: SPL.x + 7 + BETS[0], y: SPL.y + 7 + BETS[1] - 170 - camG(T_M2B) };
  const m2bOn = t >= T_M2B && t < T_P5 + 0.1;
  const irisB = L((t - T_M2B) * 30, 0, 20, 0, 1500, INOUT);
  const maskB = `radial-gradient(circle at ${betScr.x}px ${betScr.y}px, #000 ${Math.max(0, irisB - 60)}px, transparent ${irisB}px)`;

  // K. P5 sky / cross / tomb
  const p5On = t >= T_P5 && t < T_M3 + 0.9, ctP5 = t - T_P5;
  const R5 = RCS("P5", Math.min(6.4, ctP5));
  const rack5 = rackDims(t, [[T_P5, 0], [wt(124) - 0.05, 1], [wt(129) - 0.05, 2]]);
  const goldU = L(t, wt(119), wt(119) + 40 / 30, 0, 1, SINE), goldOp = L(t, 48.81, 49.36, 1, 0);

  // L. M3
  const m3On = t >= T_M3;
  const gk = L(t, T_M3, T_M3 + 22 / 30, 0, 1, INOUT);
  const tombR = RCS("P5", Math.min(6.4, T_M3 - T_P5)).bot;
  const m3R: Rc = { x: lerp(tombR.x, 0, gk), y: lerp(tombR.y, 0, gk), w: lerp(tombR.w, 1080, gk), h: lerp(tombR.h, 1920, gk) };

  const endP = L(t, T_END, T_END + 1.0, 0, 1, SINE);
  const endR: Rc = { x: 10, y: 10, w: 1060, h: 1900 };

  return (
    <AbsoluteFill style={{ background: "#fff", overflow: "hidden" }}>
      <Audio src={staticFile("bethlehem/narration_v41.mp3")} />
      {hookOn && <PageBox a={0} b={T_WHIP1} x={w1.out.x + shHx} y={w1.out.y + shHy} blur={w1.out.b}>
        <Vid clip="P1" from={0} to={T_WHIP1 + 0.1} ct0={0} />
        <Dim r={RH.top} a={rackH[0]} /><Dim r={RH.mid} a={rackH[1]} /><Dim r={RH.bot} a={rackH[2]} />
        {t >= wt(4) && <div style={{ position: "absolute", left: RH.bot.x, top: RH.bot.y, width: RH.bot.w, height: RH.bot.h, boxSizing: "border-box", border: `${L(t, wt(4), wt(4) + 0.2, 0, 10)}px solid ${INK}` }} />}
        {skK >= 0 && skK < 26 && <PanelClone clip="P1" from={0} ct0={0} to={T_WHIP1 + 0.1} r={RH.mid} scale={skK < 4 ? L(skK, 0, 4, 1, 1.08, OUT) : L(skK, 4, 26, 1.08, 1.0, INOUT)} border={8} op={L(skK, 20, 26, 1, 0)} />}
        <Speed k={skK} y0={RH.mid.y + 30} y1={RH.mid.y + RH.mid.h - 30} />
        <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>
          {hookPrints.map(([x, y, a, sc], i) => <Print key={i} x={x} y={y} ang={a} s={sc} t={t} at={K_GO + i * 2 / 30} side={i % 2 ? 1 : -1} />)}
        </svg>
        <Cap text="BETHLEHEM" x={400} y={1492} t={t} at={wt(9)} until={T_WHIP1} />
        <Big text="DID" k={(t - wt(10)) * 30} left={90} top={1296} rot={-4} color={CREAM} />
        <Big text="THEY" k={(t - wt(11)) * 30} left={330} top={1296} rot={3} color={CREAM} />
        <Big text="GO?" k={(t - wt(12)) * 30} left={640} top={1296} rot={-3} color={GOLD} />
      </PageBox>}
      {p2On && <PageBox a={0} b={0} x={w1.inc.x} y={w1.inc.y} blur={w1.inc.b}>
        <Vid clip="P2" from={T_WHIP1 - WD} to={T_P2B + 0.1} ct0={0} />
        <Dim r={R2.top} a={rack2[0]} /><Dim r={R2.mid} a={rack2[1]} /><Dim r={R2.bot} a={rack2[2]} />
        <Cap text="ABOUT 700 YEARS BEFORE" x={56} y={96} t={t} at={wt(14)} until={5.95} size={66} />
        {t >= wt(20) && t < 7.1 && <>
          <svg style={{ position: "absolute", left: 0, top: 0, opacity: L(t, 6.9, 7.1, 1, 0) }} width={1080} height={1920}>
            <path d="M214,168 C270,172 330,196 392,236" fill="none" stroke={INK} strokeWidth={8} strokeLinecap="round" {...draw(L(t, wt(20), wt(20) + 0.25, 0, 1, OUT))} />
            <path d="M392,236 l-34,-4 M392,236 l-14,-28" fill="none" stroke={INK} strokeWidth={8} strokeLinecap="round" {...draw(L(t, wt(20) + 0.2, wt(20) + 0.3, 0, 1))} />
          </svg>
          <div style={{ opacity: L(t, 6.9, 7.1, 1, 0) }}><Chip text="MICAH" left={44} top={130} rot={-3} cream size={34} /></div></>}
      </PageBox>}
      {p2bOn && <PageBox a={0} b={0}>
        <Vid clip="P2" from={T_P2B} to={T_M1 + 0.1} ct0={5.55} />
      </PageBox>}
      {m1On && <PageBox a={0} b={0}>
        <Vid clip="M1" from={T_M1} to={T_TAKE + 0.1} ct0={0} />
      </PageBox>}
      {p3On && <PageBox a={0} b={0} x={w2.out.x} y={w2.out.y} blur={w2.out.b}>
        <Vid clip="P3" from={T_P3} to={T_WHIP2 + 0.1} ct0={0} />
        <Dim r={R3.mid} a={rack3[1]} /><Dim r={R3.bot} a={rack3[2]} /><Dim r={R3.top} a={rack3[0]} />
        <NightCover r={R3.mid} t={t} star op={L(t, 22.84, 23.14, 1, 0)} />
        <NightCover r={R3.bot} t={t} seed={40} />
      </PageBox>}
      {p4On && <PageBox a={0} b={0} x={w2.inc.x + shH4x} y={w2.inc.y + shH4y} blur={w2.inc.b}>
        <Vid clip="P4" from={T_WHIP2 - WD} to={T_WHIP3 + 0.1} ct0={0} />
        <Dim r={R4.top} a={rack4[0]} /><Dim r={R4.mid} a={rack4[1]} /><Dim r={R4.bot} a={rack4[2]} />
        {kHerod >= 0 && kHerod < 26 && <PanelClone clip="P4" from={T_WHIP2 - WD} ct0={0} to={T_WHIP3 + 0.1} r={{ ...R4.top }} scale={kHerod < 4 ? L(kHerod, 0, 4, 1, 1.07, OUT) : L(kHerod, 4, 26, 1.07, 1.0, INOUT)} op={L(kHerod, 20, 26, 1, 0)} />}
        <Speed k={kHerod} y0={R4.top.y + 40} y1={R4.top.h - 40} right />
        <Cap text="JERUSALEM" x={26} y={22} t={t} at={T_WHIP2} until={K_HEROD - 0.05} />
        <Cap text="KING HEROD" x={26} y={22} t={t} at={K_HEROD} until={27.05} size={52} />
      </PageBox>}
      {p1bOn && <PageBox a={0} b={0} x={w3.inc.x + shWx} y={w3.inc.y + shWy} blur={w3.inc.b}>
        <Vid clip="P1" from={T_WHIP3 - WD} to={T_GAL + 0.2} ct0={1.3} />
        <div style={{ position: "absolute", left: RB.mid.x, top: mid.y0, width: RB.mid.w, height: midH, overflow: "hidden", clipPath: mapClip, opacity: mapWk < 0 ? 0 : 1 }}>
          <MapMid t={t} />
          <div style={{ position: "absolute", inset: 0, border: `7px solid ${INK}` }} />
          <Dim r={{ x: 0, y: 0, w: RB.mid.w, h: midH }} a={rack1[1]} />
        </div>
        {mapShown && mwu >= 1 && <>
          <Cap text="JERUSALEM" x={mDX + (JER[0] - 160) * mScale} y={mDY + (JER[1] + 60) * mScale} t={t} at={30.26} until={T_M2A} />
          <Cap text="BETHLEHEM" x={mDX + (BET[0] - 60) * mScale} y={mDY + (BET[1] + 22) * mScale} t={t} at={30.32} until={T_M2A} />
        </>}
        <div style={{ position: "absolute", left: 0, top: bot.y0, width: 1080, height: 1920 - bot.y0, overflow: "hidden" }}>
          <Dim r={{ x: RB.bot.x, y: 0, w: RB.bot.w, h: RB.bot.h }} a={rack1[2]} />
          <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920 - bot.y0}>
            {RP.map(([x, fy], i) => <Print key={i} x={x} y={(1920 - bot.y0) * fy} ang={-8 + 16 * hash(i)} s={L(fy, 0.29, 0.86, 0.55, 1.15)} t={t} at={wt(84) + i * 2 / 30} goldAt={wt(88) + 0.2 + i * 2 / 30} side={i % 2 ? 1 : -1} />)}
          </svg>
        </div>
        <Dim r={RB.top} a={rack1[0]} />
        {camelOn && <div style={{ position: "absolute", left: 0, top: top.y0 + 10, width: 1080, height: top.y1 - top.y0 + 30, transform: `translateX(${camelX}px) rotate(-3deg)`, transformOrigin: "50% 100%" }}>
          <div style={{ position: "absolute", inset: 0, overflow: "hidden", border: `8px solid ${INK}`, background: "#000", boxShadow: `10px 12px 0 ${INK}` }}>
            <Sequence from={F(K_WENT)} layout="none"><OffthreadVideo src={staticFile("bethlehem/clips/P3.mp4")} startFrom={F(P3T)} muted
              style={{ position: "absolute", left: 0, top: -(p3a) + (top.y1 - top.y0 + 30 - (p3b - p3a)) / 2, width: 1080, height: 1920, objectFit: "cover" }} /></Sequence>
          </div>
          <div style={{ position: "absolute", right: 40, bottom: -46, fontFamily: "BangersB", fontSize: 150, lineHeight: "150px", color: GOLD, WebkitTextStroke: `10px ${INK}`, paintOrder: "stroke fill",
            textShadow: `8px 8px 0 ${INK}`, transform: `rotate(-6deg) scale(${L(ck, 2, 6, 1.6, 1, OUT)})`, opacity: L(ck, 2, 3, 0, 1) }}>WENT</div>
        </div>}
        <Speed k={ck} y0={top.y0 + 40} y1={top.y1 - 20} />
        <Burst x={mDX + ROADPTS[6][0] * mScale} y={mDY + ROADPTS[6][1] * mScale} k={(t - (K_WENT + 12 / 30)) * 30} r={80} />
      </PageBox>}
      {m2aOn && <div style={{ position: "absolute", inset: 0, WebkitMaskImage: maskA, maskImage: maskA }}>
        <Vid clip="M2" from={T_M2A} to={T_GAL + 0.5} ct0={0.7} />
      </div>}
      {galOn && <div style={{ position: "absolute", inset: 0, clipPath: galClip }}><div style={{ position: "absolute", inset: 0, background: "#fff" }}><MapGal t={t} /></div></div>}
      {m2bOn && <div style={{ position: "absolute", inset: 0, WebkitMaskImage: maskB, maskImage: maskB }}>
        <Vid clip="M2" from={T_M2B} to={T_P5 + 0.1} ct0={2.6} />
      </div>}
      {p5On && <PageBox a={0} b={0}>
        <Vid clip="P5" from={T_P5} to={T_M3 + 1} ct0={0} />
        <Dim r={R5.top} a={rack5[0]} /><Dim r={R5.mid} a={rack5[1]} /><Dim r={R5.bot} a={rack5[2]} />
        {(() => {
          const ctt = ctP5, coreY = L(ctt, 2.5, 4.3, 205, 174), y0 = Math.max(150, coreY + 80), y1 = R5.g[1]; const hh = y1 - y0;
          if (t < wt(119) || goldOp <= 0) return null;
          const d = `M 540 ${y0} C ${540 + 55} ${y0 + hh * 0.3}, ${540 - 60} ${y0 + hh * 0.62}, 540 ${y1}`;
          return <svg style={{ position: "absolute", left: 0, top: 0, opacity: goldOp }} width={1080} height={1920}>
            <path d={d} fill="none" stroke={INK} strokeWidth={17} strokeLinecap="round" {...draw(goldU)} />
            <path d={d} fill="none" stroke={GOLD} strokeWidth={9} strokeLinecap="round" {...draw(goldU)} />
          </svg>;
        })()}
      </PageBox>}
      {m3On && <div style={{ position: "absolute", left: m3R.x, top: m3R.y, width: m3R.w, height: m3R.h, overflow: "hidden", boxSizing: "border-box", border: `${L(gk, 0, 1, 7, 0)}px solid ${INK}`, background: "#000" }}>
        <Sequence from={F(T_M3)} layout="none"><OffthreadVideo src={staticFile("bethlehem/clips/M3.mp4")} startFrom={0} muted style={{ position: "absolute", left: 0, top: 0, width: "100%", height: "100%", objectFit: "cover", filter: "saturate(0.7) sepia(0.2)" }} /></Sequence>
      </div>}
      <Scroll t={t} a={10.9} b={14.85} />
      {t >= wt(40) && t < T_WHIP2 && <PF id="pfx" r={frRect} dashP={dashP} goldP={goldP} seed={7} sw={t < wt(50) ? 8 : 10} op={L(t, 23.09, 23.54, 1, 0)} />}
      {t >= wt(40) && t < T_TAKE - 0.1 && <div style={{ opacity: L(t, wt(40) + 0.1, wt(40) + 0.25, 0, 1) * L(t, T_TAKE - 0.2, T_TAKE - 0.1, 1, 0) }}>
        <Chip text="MICAH 5:2" left={PR1.x + 12} top={PR1.y - 28} rot={-3} /></div>}
      {t >= wt(52) + 0.28 && t < 23.3 && <div style={{ opacity: L(t, wt(52) + 0.28, wt(52) + 0.6, 0, 1) * L(t, 22.84, 23.24, 1, 0) }}>
        <Chip text="MICAH 5:2" left={60} top={(R3.g[0] + R3.g[1]) / 2 - 33} rot={-2} size={46} />
        <Chip text="CAME TRUE" left={420} top={(R3.g[0] + R3.g[1]) / 2 - 33} rot={2} cream size={46} />
      </div>}
      <Streaks t={t} end={T_WHIP1} /><Streaks t={t} end={T_WHIP2} /><Streaks t={t} end={T_WHIP3} vertical />
      {PILLS.map((s, i) => <PillView key={i} t={t} s={s} />)}
      {t >= T_END && <>
        <PF id="pfend" r={endR} dashP={0} goldP={endP} seed={7} sw={12} />
        <div style={{ position: "absolute", left: 0, top: 1330, width: 1080, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
          <div style={{ position: "relative", height: 110, width: 520 }}><Chip text="PROMISED." left={0} top={0} cream dashed size={72} op={L(t, 57.03, 57.33, 0, 1)} /></div>
          <div style={{ position: "relative", height: 110, width: 560 }}><Chip text="CAME TRUE." left={0} top={0} size={72} op={L(t, 57.93, 58.23, 0, 1)} /></div>
        </div>
      </>}
    </AbsoluteFill>
  );
};
