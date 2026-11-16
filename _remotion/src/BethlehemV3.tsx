// Prophecy 01 "Born in Bethlehem" - film v3: v2 words + MOTION_DESIGN_v1 (Fable) "hollow steps, gold steps, one gold line".
// Base = PixVerse clips (1.0x, trim only). Every cut has its own transition; lettering reads along with the voice.
// Data: public/bethlehem/film_v3_data.json (built by prophecy/01_bethlehem/motion_v3/make_data.py). Pure function of the frame.
import React from "react";
import { AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import D from "../public/bethlehem/film_v3_data.json";

export const BTH3_FPS = 30;
export const BTH3_FRAMES = D.frames as number;

const GOLD = "#E8A81C", INK = "#141210", CREAM = "#FFEEBE", PAPER = "#FBF8F0", SEPIA = "#2A1A0E";
const PILL_FILL = "rgba(225,225,228,0.588)", PILL_EDGE = "rgba(20,18,16,0.67)";
const F = (s: number) => Math.round(s * 30);
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const L = (f: number, a: number, b: number, x: number, y: number, e?: (t: number) => number) => interpolate(f, [a, b], [x, y], { ...cl, easing: e });
const OUT = Easing.out(Easing.cubic), IN = Easing.in(Easing.cubic), INOUT = Easing.inOut(Easing.cubic), SINE = Easing.inOut(Easing.sin), BACK = Easing.out(Easing.back(1.8));
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const lerpPts = (pts: [number, number, number][], t: number): [number, number] => {
  if (t <= pts[0][0]) return [pts[0][1], pts[0][2]];
  for (let i = 0; i < pts.length - 1; i++) if (t <= pts[i + 1][0]) {
    const u = (t - pts[i][0]) / (pts[i + 1][0] - pts[i][0]);
    return [pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u, pts[i][2] + (pts[i + 1][2] - pts[i][2]) * u];
  }
  const p = pts[pts.length - 1]; return [p[1], p[2]];
};

// ---------- measured tracks (clip time -> px on the 1080x1920 frame) ----------
const P1_TOWN: [number, number, number][] = [[0.5, 810, 1490], [3.5, 800, 1490], [6.0, 720, 1480], [9.5, 770, 1436]];
const P3_CAMEL_FLOOR: [number, number, number][] = [[7.4, 0, 955], [8.6, 0, 870], [9.9, 0, 855]];
const P5_CORE: [number, number, number][] = [[2.5, 540, 205], [3.7, 540, 184], [4.3, 540, 174]];
const P5_STAR_BOTTOM: [number, number, number][] = [[2.5, 0, 551], [3.7, 0, 486], [4.3, 0, 456]];
const M1_TOWN: [number, number] = [907, 800];
const TOMB_DOOR: [number, number] = [540, 1120];

// ---------- segments (edl + transition pre/post windows, seconds) ----------
type Seg = { c: string; a: number; b: number; inPt: number; pre: number; post: number };
const E = D.edl as [string, number, number, number][];
const SEG: Seg[] = E.map(([c, a, b, inPt]) => ({ c, a, b, inPt, pre: 0, post: 0 }));
// cut 3 ink wipe: incoming P2 pre-rolls 10 f; cut 4 lamp splice: 2 f mix; cut 6 webtoon: P4 pre 9 f (shifts P4 0.3 s);
// cut 7 page turn back: P1 pre 5 f + P4 post 5 f; cut 9 iris: P1 stays to 41.93; cut 10 nightfall: P5 pre 6 f (shift), M2 post 18 f
SEG[3].pre = 10 / 30; SEG[6].pre = 9 / 30; SEG[7].pre = 5 / 30; SEG[6].post = 5 / 30;
SEG[8].post = 41.93 - 40.5; SEG[10].pre = 6 / 30; SEG[9].post = 18 / 30;
const clipT = (s: Seg, f: number) => Math.max(0, s.inPt - s.pre) + (f / 30 - (s.a - s.pre)); // clip time shown at film frame f

// ---------- per-segment transition style ----------
const segStyle = (i: number, f: number): React.CSSProperties | null => {
  const s = SEG[i];
  const A = F(s.a), B = F(s.b);
  const st: React.CSSProperties = {};
  switch (i) {
    case 1: { // out of cut 2: zoom-through into Micah's top panel
      if (f >= 265) { const k = L(f, 265, 272, 1, 1.9, IN); st.transform = `scale(${k})`; st.transformOrigin = "540px 280px"; }
      break; }
    case 2: { // in of cut 2
      st.transform = `scale(${L(f, 273, 282, 1.12, 1, OUT)})`; break; }
    case 3: { // in of cut 3: ink wipe left->right
      if (f < A) {
        const u = INOUT(Math.max(0, Math.min(1, (f - (A - 10)) / 10)));
        const pts: string[] = [];
        for (let y = -60; y <= 1980; y += 60) pts.push(`${frontX(u, y).toFixed(0)}px ${y}px`);
        st.clipPath = `polygon(-10px -60px, ${pts.join(", ")}, -10px 1980px)`;
      }
      break; }
    case 4: break; // hard splice hidden under the lamp flare
    case 5: { // out of cut 6 webtoon scroll
      if (f >= 825) st.transform = `translateY(${L(f, 825, 834, 0, -1920, INOUT)}px)`; break; }
    case 6: {
      st.transform = `translateY(${L(f, 825, 834, 1920, 0, INOUT)}px)`;
      if (f >= 997) { st.transform = `translateX(${L(f, 997, 1007, 0, 60)}px)`; st.filter = `brightness(${L(f, 997, 1007, 1, 0.85)})`; }
      break; }
    case 7: { // page turn back to page one
      const x = L(f, 997, 1007, -1080, 0, OUT); st.transform = `translateX(${x}px)`; if (x < -1) st.boxShadow = "40px 0 40px rgba(0,0,0,0.35)";
      if (f >= 1118) { st.transform = `translateY(${L(f, 1118, 1122, 0, 420, IN)}px) scaleY(${L(f, 1118, 1122, 1, 1.06, IN)})`; st.filter = `blur(${L(f, 1118, 1122, 0, 6)}px)`; }
      break; }
    case 8: { // whip-pan in
      st.transform = `translateY(${L(f, 1122, 1126, -420, 0, OUT)}px) scaleY(${L(f, 1122, 1126, 1.06, 1, OUT)})`;
      if (f < 1126) st.filter = `blur(${L(f, 1122, 1126, 6, 0)}px)`;
      break; }
    case 9: { // route iris from the star, calm
      const [sx, sy] = starP1(f);
      const r = L(f, 1236, 1258, 0, 1800, INOUT);
      if (r < 1) return { opacity: 0 };
      if (r < 1800) { const m = `radial-gradient(circle at ${sx}px ${sy - 90}px, #000 ${Math.max(0, r - 80)}px, transparent ${r}px)`; st.WebkitMaskImage = m; st.maskImage = m; }
      break; }
    case 10: { // nightfall wipe top->bottom, calm
      const e = L(f, 1299, 1323, -160, 2080, SINE);
      if (e < 2080) { const m = `linear-gradient(to bottom, #000 ${e - 160}px, transparent ${e}px)`; st.WebkitMaskImage = m; st.maskImage = m; }
      break; }
  }
  return st;
};
const frontX = (u: number, y: number) => L(u, 0, 1, -300, 1500) + 0.21 * (y - 960) + 28 * Math.sin(y / 90 + 1.7);

// P1 star/town position for the current frame (P1 used in segs 0, 7, 8)
const p1Town = (f: number): [number, number] => {
  const t = f / 30;
  const s = t < 4.5 ? SEG[0] : t < 37.4 ? SEG[7] : SEG[8];
  return lerpPts(P1_TOWN, clipT(s, f));
};
const starP1 = (f: number): [number, number] => { const [x, y] = p1Town(f); return [x, y - 40]; };

// ---------- drawn marks ----------
const Star: React.FC<{ x: number; y: number; land: number; f: number; out?: number; size?: number }> = ({ x, y, land, f, out, size = 52 }) => {
  if (f < land || (out !== undefined && f >= out + 5)) return null;
  const k = f - land;
  const sc = k < 8 ? (k < 4 ? L(k, 0, 4, 0, 1.25, OUT) : L(k, 4, 8, 1.25, 1, SINE)) : 1 + 0.08 * Math.sin((k - 8) / 40 * Math.PI * 2);
  const op = out !== undefined ? L(f, out, out + 5, 1, 0) : 1;
  const r = size / 2, ir = r * 0.36;
  const pts = [0, 1, 2, 3, 4, 5, 6, 7].map((i) => { const a = -Math.PI / 2 + i * Math.PI / 4, rr = i % 2 ? ir : r; return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`; }).join(" ");
  const ring = k < 10 ? <circle r={L(k, 0, 10, 20, 70)} fill="none" stroke={INK} strokeWidth={4} opacity={L(k, 0, 10, 1, 0)} /> : null;
  return (
    <g transform={`translate(${x},${y})`} opacity={op}>
      {ring}
      <g transform={`scale(${sc})`}>
        <polygon points={pts} fill="none" stroke={CREAM} strokeWidth={9} strokeLinejoin="round" />
        <polygon points={pts} fill={GOLD} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
      </g>
    </g>
  );
};
const Dot: React.FC<{ x: number; y: number; pop: number; gold?: number; f: number; op?: number; pulse?: number; blink?: [number, number] }> = ({ x, y, pop, gold, f, op = 1, pulse, blink }) => {
  if (f < pop) return null;
  const k = f - pop;
  let sc = k < 5 ? (k < 3 ? L(k, 0, 3, 0, 1.2, OUT) : L(k, 3, 5, 1.2, 1)) : 1;
  const g = gold === undefined ? 0 : L(f, gold, gold + 3, 0, 1);
  if (gold !== undefined && f >= gold && f < gold + 6) sc *= 1 + 0.25 * Math.sin((f - gold) / 6 * Math.PI);
  if (pulse !== undefined && f >= pulse && f < pulse + 10) sc *= 1 + 0.3 * Math.sin((f - pulse) / 10 * Math.PI);
  let o = op;
  if (blink && f >= blink[0] && f < blink[1]) o *= 0.675 + 0.325 * Math.cos((f - blink[0]) / 20 * Math.PI * 2);
  const fill = g > 0.5 ? GOLD : "rgba(255,248,230,0.85)";
  return (
    <g transform={`translate(${x},${y}) scale(${sc})`} opacity={o}>
      <circle r={13} fill={fill} stroke={INK} strokeWidth={5} />
      <circle r={16} fill="none" stroke={CREAM} strokeWidth={2} />
    </g>
  );
};
const routeDots = (tx: number, ty: number) => { const out: [number, number][] = []; const x0 = 150, x1 = tx - 120; for (let i = 0; i < 7; i++) out.push([x0 + (x1 - x0) * i / 6, ty + 34 + (i % 2 ? -8 : 6)]); return out; };

const Marks: React.FC<{ f: number }> = ({ f }) => {
  const els: React.ReactNode[] = [];
  // hook: star on "where" (38), 7 hollow dots on "go?" (107..119), wiped at 120
  if (f < 120) {
    const [tx, ty] = p1Town(f);
    els.push(<Star key="hs" x={tx} y={ty - 40} land={38} f={f} />);
    routeDots(tx, ty).forEach(([x, y], i) => els.push(<Dot key={"hd" + i} x={x} y={y} pop={107 + 2 * i} f={f} />));
  }
  // Micah names the town (M1)
  if (f >= 340 && f < 414) els.push(<Star key="ms" x={M1_TOWN[0]} y={M1_TOWN[1] - 80} land={340} out={408} f={f} />);
  // wise men: 16 gold dots from the east along the camel panel floor (P3, clip t 7.4..10)
  if (f >= 755 && f < 826) {
    const ct = clipT(SEG[5], f); const [, fy] = lerpPts(P3_CAMEL_FLOOR, ct);
    const fade = L(f, 819, 825, 1, 0);
    for (let k = 0; k < 16; k++) els.push(<Dot key={"wd" + k} x={1010 - 58 * k} y={fy - 40 + 10 * Math.sin(k * 1.3)} pop={755 + Math.round(2.8 * k)} gold={755} f={f} op={fade} />);
  }
  // "close by" + silence + "never went" + "the wise men went" (P1 segs 7/8), iris at 1236
  if (f >= 1044 && f < 1243 && !(f >= 1118 && f < 1126)) {
    const [tx, ty] = p1Town(f);
    const fade = L(f, 1236, 1242, 1, 0);
    els.push(<Star key="cs" x={tx} y={ty - 40} land={f >= 1122 ? 1100 : 1044} f={f} />);
    routeDots(tx, ty).forEach(([x, y], i) => els.push(
      <Dot key={"cd" + i} x={x} y={y} pop={f >= 1122 ? 1000 : 1070 + 2 * i} gold={1216 + 3 * i} f={f} op={fade}
        pulse={i === 0 ? 1172 : undefined} blink={i === 0 ? [1090, 1122] : undefined} />));
  }
  // the one gold line: from the galaxy core down to just above the cross (P5 star panel), 1381-1417, fade 1420-1436
  if (f >= 1381 && f < 1437) {
    const ct = clipT(SEG[10], f);
    const [cx, cy] = lerpPts(P5_CORE, ct); const [, by] = lerpPts(P5_STAR_BOTTOM, ct);
    const y0 = cy + 30, y1 = by - 14, h = y1 - y0;
    const d = `M ${cx} ${y0} C ${cx + 60} ${y0 + h * 0.3}, ${cx - 70} ${y0 + h * 0.62}, ${cx} ${y1}`;
    const p = L(f, 1381, 1417, 0, 1, SINE), op = L(f, 1420, 1436, 1, 0);
    els.push(
      <g key="gl" opacity={op}>
        <path d={d} fill="none" stroke={GOLD} strokeWidth={16} opacity={0.25} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
        <path d={d} fill="none" stroke={GOLD} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
      </g>);
  }
  return <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>{els}</svg>;
};

// ---------- full-frame transition overlays ----------
const LEAF_C = ["#F4EAD2", "#F1E3C3", "#EEDDB6", "#EAD6A8", "#E6CF9C", "#EAD6A8", "#EEDDB6"];
const Leaves: React.FC<{ f: number; start: number; n: number; dir: 1 | -1 }> = ({ f, start, n, dir }) => (
  <>{Array.from({ length: n }).map((_, k) => {
    const u = (f - (start + 2 * k)) / 6;
    if (u < 0 || u > 1) return null;
    const x = dir === 1 ? -1080 + 2160 * u : 1080 - 2160 * u;
    return (
      <div key={k} style={{ position: "absolute", left: x, top: 0, width: 1080, height: 1920, background: LEAF_C[k % 7],
        boxShadow: `${dir === 1 ? -40 : 40}px 0 40px rgba(0,0,0,0.25)`,
        backgroundImage: "repeating-linear-gradient(to bottom, transparent 0 300px, rgba(90,58,24,0.10) 300px 303px)" }} />
    );
  })}</>
);
const Overlays: React.FC<{ f: number }> = ({ f }) => {
  const els: React.ReactNode[] = [];
  if (f >= 270 && f < 277) els.push(<div key="fl" style={{ position: "absolute", inset: 0, background: CREAM, opacity: f < 273 ? L(f, 270, 272, 0, 0.85) : L(f, 273, 276, 0.85, 0) }} />);
  if (f >= 413 && f < 424) { // ink band riding the wipe front
    const u = INOUT(Math.max(0, Math.min(1, (f - 413) / 10)));
    const a: string[] = [], b: string[] = [];
    for (let y = -60; y <= 1980; y += 60) { a.push(`${frontX(u, y).toFixed(0)},${y}`); b.push(`${(frontX(u, y) - 140 + 18 * Math.sin(y / 70 + 4.1)).toFixed(0)},${y}`); }
    els.push(<svg key="ink" style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}><polygon points={[...a, ...b.reverse()].join(" ")} fill={INK} /></svg>);
  }
  if (f >= 472 && f < 481) els.push(<div key="lf" style={{ position: "absolute", inset: 0, background: "rgb(255,196,110)", mixBlendMode: "screen", opacity: 0.55 * Math.sin(L(f, 472, 480, 0, 1) * Math.PI) }} />);
  if (f >= 1539 && f < 1563) {
    const r = L(f, 1539, 1551, 0, 140, SINE), o = f < 1551 ? 1 : L(f, 1551, 1563, 1, 0, SINE);
    els.push(<div key="dawn" style={{ position: "absolute", inset: 0, opacity: o, background: `radial-gradient(circle at ${TOMB_DOOR[0]}px ${TOMB_DOOR[1]}px, #FFF3D6 ${r}%, rgba(255,243,214,0) ${r + 25}%)` }} />);
  }
  if (f >= 1551 && f < 1564) els.push(<div key="dawn2" style={{ position: "absolute", inset: 0, background: "#FFF3D6", opacity: L(f, 1551, 1563, 1, 0, SINE) }} />);
  return <>{els}</>;
};

// ---------- lettering ----------
const KPill: React.FC<{ it: any; f: number }> = ({ it, f }) => {
  const s = F(it.start), e = F(it.end);
  if (f < s || f >= e) return null;
  const sacred = it.mode === "sacred" || it.mode === "final";
  const age = f - s;
  let op = sacred ? L(age, 0, 9, 0, 1) : L(age, 0, 3, 0, 1);
  op *= L(f, e - 4, e, 1, 0);
  const lines = it.lines as any[][];
  const h = lines.length * 62 + 40, top = it.cy - h / 2;
  const lineEls = lines.map((row, li) => {
    if (it.mode === "final" && li === 1 && f < 1653) return <div key={li} style={{ opacity: 0 }}>{row.map((w: any) => w.t).join(" ")}</div>;
    const lo = it.mode === "final" && li === 1 ? L(f, 1653, 1661, 0, 1) : 1;
    return (
      <div key={li} style={{ opacity: lo, position: "relative" }}>
        {row.map((w: any, wi: number) => {
          const wf = F(w.at) - 1, k = f - wf;
          let o = 1, sc = 1;
          if (it.mode === "pop") { if (k < 0) o = 0; else sc = L(k, 0, 4, 1.25, 1, OUT); }
          else if (it.mode === "read" || it.mode === "speech") { o = k < 0 ? 0.38 : L(k, 0, 2, 0.38, 1); sc = k >= 0 ? L(k, 0, 5, 1.07, 1, OUT) : 1; }
          const m: string[] = w.m || [];
          const ga = m.includes("gold") ? L(f, wf + 1, wf + 5, 0, 1) : 0;
          const ls = m.includes("spread") ? L(f, F(44.88), F(45.5), 0, 5, SINE) : 0;
          return (
            <React.Fragment key={wi}>
              <span style={{ display: "inline-block", position: "relative", opacity: o, transform: `scale(${sc})`, letterSpacing: ls,
                background: ga ? `rgba(232,168,28,${ga})` : undefined, borderRadius: 8, padding: "0 7px", margin: "0 -7px" }}>
                {w.t}
                {m.includes("empty") && f >= wf + 1 && <span style={{ position: "absolute", inset: "4px -4px 2px -4px", border: `4px solid ${INK}`, borderRadius: 10,
                  clipPath: `inset(0 ${100 - L(f, wf + 1, wf + 7, 0, 100)}% 0 0)` }} />}
                {m.includes("ticks") && f >= wf + 1 && (
                  <svg style={{ position: "absolute", right: -18, top: -14, overflow: "visible" }} width={30} height={30}>
                    <path d="M4 18 L14 4 M14 24 L28 12" stroke={INK} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - L(f, wf + 1, wf + 4, 0, 1)} />
                  </svg>)}
                {(m.includes("under2") || m.includes("wavy")) && f >= wf + 1 && (
                  <svg style={{ position: "absolute", left: 0, top: 58, overflow: "visible" }} width={10} height={20}>
                    {m.includes("under2") ? <>
                      <line x1={0} y1={0} x2={uw(w.t)} y2={-2} stroke={INK} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - L(f, wf + 1, wf + 7, 0, 1)} />
                      <line x1={4} y1={9} x2={uw(w.t) - 4} y2={8} stroke={INK} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - L(f, wf + 3, wf + 9, 0, 1)} />
                    </> : <path d={`M0 0 Q ${uw(w.t) * 0.25} 9 ${uw(w.t) * 0.5} 0 T ${uw(w.t)} 0`} fill="none" stroke={INK} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - L(f, wf + 1, wf + 9, 0, 1)} />}
                  </svg>)}
                {m.includes("star") && f >= wf + 1 && (
                  <svg style={{ position: "absolute", right: -16, top: -18, overflow: "visible" }} width={24} height={24}><g transform={`translate(12,12) scale(${L(f, wf + 1, wf + 6, 0, 1, BACK)})`}>
                    <polygon points="0,-12 3,-3 12,0 3,3 0,12 -3,3 -12,0 -3,-3" fill={GOLD} stroke={INK} strokeWidth={3} strokeLinejoin="round" /></g></svg>)}
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
  const pop = it.mode === "speech" ? L(age, 0, 6, 0.85, 1, BACK) : 1;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, opacity: op }}>
      {it.mode === "speech" && (
        <svg style={{ position: "absolute", left: 0, top: 0, opacity: L(f, 1002, 1006, 1, 0) }} width={1080} height={1920}>
          <path d={`M400 ${top + h - 3} L430 ${top + h + 38} L462 ${top + h - 3}`} fill={PILL_FILL} stroke={PILL_EDGE} strokeWidth={4} strokeLinejoin="round" />
        </svg>)}
      <div style={{ position: "absolute", left: 100, top, width: 880, height: h, boxSizing: "border-box", borderRadius: 46, background: PILL_FILL,
        border: `4px solid ${PILL_EDGE}`, display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center",
        fontFamily: "KalamB", fontSize: 54, lineHeight: "62px", color: INK, transform: `scale(${pop})` }}>{lineEls}</div>
      {it.mode === "speech" && <>
        <Chip text="A SCRIBE" left={126 - L(age, 0, 6, 20, 0, OUT)} top={top - 30} />
        <Chip text="MATTHEW 2:5" right={126 - L(age, 0, 6, 20, 0, OUT)} top={top - 30} />
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
  if (f < 96 || f >= 120) return null;
  const words: [string, number, number, string][] = [["DID", 96, -3, CREAM], ["THEY", 100, 2, CREAM], ["GO?", 106, -2, GOLD]];
  return (
    <div style={{ position: "absolute", left: 0, top: 1290, width: 1080, textAlign: "center", whiteSpace: "nowrap" }}>
      {words.map(([w, at, r, c], i) => {
        if (f < at) return <span key={i} style={{ display: "inline-block", opacity: 0, fontFamily: "BangersB", fontSize: 140, margin: "0 16px" }}>{w}</span>;
        const k = f - at;
        return <span key={i} style={{ display: "inline-block", fontFamily: "BangersB", fontSize: 140, lineHeight: "150px", color: c, WebkitTextStroke: "9px #4a2a12",
          paintOrder: "stroke fill", margin: "0 16px", transform: `scale(${L(k, 0, 4, 1.6, 1, OUT)}) rotate(${L(k, 0, 6, r, 0, OUT)}deg)` }}>{w}</span>;
      })}
    </div>
  );
};
const CounterSlab: React.FC<{ f: number }> = ({ f }) => {
  const s = 119, e = F(6.2);
  if (f < s || f >= e) return null;
  const n = Math.min(700, 100 + 100 * Math.floor((f - s) / 2));
  const tick = f < 132 && (f - s) % 2 === 0 ? 1.12 : 1;
  const op = L(f, e - 5, e, 1, 0), sc = L(f - s, 0, 8, 0.7, 1, BACK);
  const st: React.CSSProperties = { fontFamily: "BangersB", fontSize: 104, lineHeight: "114px", color: CREAM, WebkitTextStroke: "9px #4a2a12", paintOrder: "stroke fill", letterSpacing: 2 };
  return (
    <div style={{ position: "absolute", left: 0, top: 400, width: 1080, textAlign: "center", opacity: op, transform: `scale(${sc})`, transformOrigin: "50% 0" }}>
      <div style={st}>ABOUT <span style={{ display: "inline-block", width: 190, transform: `scale(${tick})` }}>{n}</span> YEARS</div>
      <div style={st}>EARLIER</div>
    </div>
  );
};
const Scroll2: React.FC<{ f: number }> = ({ f }) => {
  if (f < 465 || f >= 530) return null;
  const rise = L(f, 465, 469, 60, 0, OUT), a = L(f, 465, 469, 0, 1);
  const open = L(f, 469, 477, 0, 1, INOUT) * L(f, 524, 529, 1, 0, INOUT);
  const pw = 80 + 720 * open, cx = 540, cy = 1065, ph = 226;
  const deck = (y: number, seed: number) => { let d = ""; for (let x = 0; x <= 800; x += 40) d += `${x === 0 ? "M" : "L"}${x} ${y + (hash(seed + x) - 0.5) * 10} `; return d; };
  const sc = D.scroll as any;
  return (
    <div style={{ position: "absolute", left: 0, top: rise, width: 1080, height: 1920, opacity: a }}>
      <div style={{ position: "absolute", left: cx - pw / 2, top: cy - ph / 2, width: pw, height: ph, overflow: "hidden" }}>
        <svg style={{ position: "absolute", left: (pw - 800) / 2, top: 0 }} width={800} height={ph}>
          <defs><linearGradient id="parch" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#EFDDB0" /><stop offset="1" stopColor="#E4CC98" /></linearGradient></defs>
          <path d={`${deck(6, 3)} L800 ${ph - 6} ${deck(ph - 6, 9).replace("M", "L").split(" L").reverse().join(" L")} Z`} fill="url(#parch)" opacity={0.94} stroke="#5C3A18" strokeWidth={3} />
        </svg>
        <div style={{ position: "absolute", left: (pw - 800) / 2, top: 0, width: 800, height: ph, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
          {sc.lines.map((ln: string[], li: number) => (
            <div key={li} style={{ fontFamily: "FellR", fontSize: 64, lineHeight: "74px", whiteSpace: "pre" }}>
              {ln.map((wd, wi) => { const t0 = F(sc.wt[li][wi]); const p = Math.max(0, Math.min(1, (f - t0) / 6)); const dry = L(f, t0, t0 + 10, 0, 1);
                return <span key={wi} style={{ display: "inline-block", clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`, color: dry < 1 ? `rgb(${42 * dry},${26 * dry},${14 * dry})` : SEPIA }}>{wd}{wi < ln.length - 1 ? " " : ""}</span>; })}
            </div>))}
        </div>
      </div>
      {[cx - pw / 2 - 30, cx + pw / 2 - 10].map((x, i) => (
        <div key={i} style={{ position: "absolute", left: x, top: cy - 135, width: 40, height: 270, borderRadius: 14, background: "linear-gradient(90deg,#5a3a1c,#b07c3e 45%,#5a3a1c)", boxShadow: "0 4px 10px rgba(0,0,0,.35)" }}>
          <div style={{ position: "absolute", left: 6, top: -14, width: 28, height: 28, borderRadius: 14, background: "#5a3a1c" }} />
          <div style={{ position: "absolute", left: 6, bottom: -14, width: 28, height: 28, borderRadius: 14, background: "#5a3a1c" }} />
        </div>))}
      {open > 0.98 && <Chip text="MICAH 5:2" right={1080 - 920 + L(f, 477, 483, -30, 0, OUT)} top={cy - ph / 2 - 26} rot={L(f, 477, 483, -6, 0, OUT)} />}
    </div>
  );
};
const EndMark: React.FC<{ f: number }> = ({ f }) => {
  if (f < 1710) return null;
  const a = L(f, 1710, 1722, 0, 1, SINE), t = L(f, 1722, 1737, 0, 1);
  return (
    <div style={{ position: "absolute", left: 240, top: 1398, width: 600, height: 84, opacity: a }}>
      <div style={{ position: "absolute", left: 180, top: -12, width: 240, height: 6, background: GOLD, borderRadius: 3 }} />
      <div style={{ position: "absolute", inset: 0, borderRadius: 42, background: PILL_FILL, border: `4px solid ${PILL_EDGE}`, display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: "FrauncesB", fontSize: 36, letterSpacing: 7, color: INK, opacity: t }}>PROMISED, THEN KEPT</div>
    </div>
  );
};

export const BethlehemV3: React.FC<{ hud?: boolean }> = ({ hud = false }) => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("bv3fonts"));
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    Promise.all([
      new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
      new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load(),
      new FontFace("FellR", `url(${staticFile("IMFeENrm28P.ttf")})`).load(),
      new FontFace("FrauncesB", `url(${staticFile("Fraunces.ttf")})`).load(),
    ]).then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); setReady(true); continueRender(h); }).catch(() => continueRender(h));
  }, []);
  const riffleUnder = f >= 116 && f < 120; // during cut 1 the hook marks sit below the leaves
  return (
    <AbsoluteFill style={{ background: PAPER, overflow: "hidden" }}>
      <Audio src={staticFile("bethlehem/narration_v2_lev.mp3")} />
      {SEG.map((s, i) => {
        const from = F(s.a - s.pre), to = F(s.b + s.post);
        const st = segStyle(i, f) || {};
        return (
          <Sequence key={i} from={from} durationInFrames={to - from} premountFor={30}>
            <div style={{ position: "absolute", inset: 0, ...st }}>
              <OffthreadVideo src={staticFile(`bethlehem/clips/${s.c}.mp4`)} startFrom={F(Math.max(0, s.inPt - s.pre))} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
            </div>
          </Sequence>
        );
      })}
      {riffleUnder && <Marks f={f} />}
      <Overlays f={f} />
      <Leaves f={f} start={116} n={7} dir={1} />
      <Leaves f={f} start={530} n={3} dir={-1} />
      {!riffleUnder && <Marks f={f} />}
      {ready && (
        <>
          <QuestionCard f={f} />
          <CounterSlab f={f} />
          <Scroll2 f={f} />
          {(D.pills as any[]).map((it) => <KPill key={it.id} it={it} f={f} />)}
          <EndMark f={f} />
        </>
      )}
      {hud && <div style={{ position: "absolute", left: 18, top: 1862, padding: "4px 14px", background: "rgba(0,0,0,0.7)", color: "#fff", fontFamily: "KalamB", fontSize: 26, borderRadius: 10 }}>{(f / 30).toFixed(2)} s · f{f}</div>}
    </AbsoluteFill>
  );
};
