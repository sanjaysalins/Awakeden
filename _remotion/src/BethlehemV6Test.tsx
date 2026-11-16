// Born in Bethlehem v6 COMIC motion test (36.3-45.0 s of the words-v3 film). Design: prophecy/01_bethlehem/comic_v6/COMIC_MOTION_DESIGN.md.
// $0. Times are REAL film seconds (words v3 voice); no warp. Clips 1.0x. Panel rects from comic_v6/panel_rects.json (gutter tracking).
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import RECTS from "../public/bethlehem/panel_rects.json";

export const BTH6T_FRAMES = 261, BTH6T_FPS = 30;
const T0 = 36.3;
const INK = "#121014", GOLD = "#F6B923", CREAM = "#FFF4D6", NIGHT = "#1B2E6A", NIGHT2 = "#0F1A40", ROAD = "#6A84C4", OCHRE = "#E2A842", OCHRE2 = "#96602A", SEA = "#2A96AA";
const PILL_FILL = "rgba(225,225,228,0.588)", PILL_EDGE = "rgba(20,18,16,0.67)";
const cl = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const L = (x: number, a: number, b: number, p: number, q: number, e?: (t: number) => number) => interpolate(x, [a, b], [p, q], { ...cl, easing: e });
const OUT = Easing.out(Easing.cubic), INOUT = Easing.inOut(Easing.cubic), BACK = Easing.out(Easing.back(1.8));
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const draw = (p: number) => ({ pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - Math.max(0, Math.min(1, p)) });

// ---- panel rects (gutter tracking) ----
type G = [number, [number, number][]];
const gut = (clip: "P1" | "P3", ct: number): [number, number, number, number] => {
  const k: G[] = (RECTS as any)[clip];
  let i = 0; while (i < k.length - 2 && k[i + 1][0] <= ct) i++;
  const [ta, ga] = k[i], [tb, gb] = k[i + 1], u = Math.max(0, Math.min(1, (ct - ta) / (tb - ta)));
  const m = (a: number, b: number) => a + (b - a) * u;
  return [m(ga[0][0], gb[0][0]), m(ga[0][1], gb[0][1]), m(ga[1][0], gb[1][0]), m(ga[1][1], gb[1][1])];
};
const X0 = 14, X1 = 1066; // page side margins

// ---- footprint (sandal sole) ----
const SOLE = "M0,-26 C9,-26 12,-15 11,-4 C10,6 8,12 8,18 C8,26 -8,26 -8,18 C-8,12 -11,5 -11,-5 C-11,-16 -8,-26 0,-26 Z";
const Print: React.FC<{ x: number; y: number; ang: number; s?: number; t: number; at: number; goldAt?: number; side: number }> = ({ x, y, ang, s = 1, t, at, goldAt, side }) => {
  if (t < at) return null;
  const k = (t - at) * 30, sc = s * L(k, 0, 3, 1.5, 1, OUT);
  const gold = goldAt !== undefined && t >= goldAt;
  const gk = gold ? (t - goldAt!) * 30 : 0;
  return (
    <g transform={`translate(${x + side * 13},${y}) rotate(${ang}) scale(${sc * (gold ? L(gk, 0, 3, 1.35, 1, OUT) : 1)})`}>
      <path d={SOLE} fill={gold ? GOLD : "none"} stroke={gold ? INK : CREAM} strokeWidth={gold ? 4 : 3.5} strokeDasharray={gold ? undefined : "6 5"} strokeLinejoin="round" />
    </g>
  );
};

// ---- the map, inked comic panel ----
const MW = 1052, MH = 640;
const JER: [number, number] = [330, 170], BET: [number, number] = [610, 500];
const ROADPTS: [number, number][] = [[365, 215], [420, 290], [480, 350], [540, 410], [590, 455], [612, 470], [622, 482]];
const MapPanel: React.FC<{ t: number }> = ({ t }) => {
  const hill = (x: number, y: number, i: number) => (
    <g key={i} transform={`translate(${x},${y})`}>
      <path d="M-46,18 L-12,-26 L6,-6 L22,-22 L52,18 Z" fill="#24397E" stroke={INK} strokeWidth={5} strokeLinejoin="round" />
      {[0, 1, 2, 3].map((j) => <line key={j} x1={-30 + j * 9} y1={14} x2={-14 + j * 9} y2={-10 + j * 2} stroke={INK} strokeWidth={2} opacity={0.75} />)}
    </g>);
  return (
    <svg width="100%" height="100%" viewBox={`0 0 ${MW} ${MH}`} preserveAspectRatio="xMidYMid slice" style={{ display: "block" }}>
      <defs>
        <pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.6" fill="#000" opacity="0.32" /></pattern>
        <pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="10" stroke={INK} strokeWidth="2.2" opacity="0.5" /></pattern>
        <radialGradient id="nightg" cx="0.45" cy="0.4" r="0.8"><stop offset="0" stopColor={NIGHT} /><stop offset="1" stopColor={NIGHT2} /></radialGradient>
      </defs>
      <rect width={MW} height={MH} fill="url(#nightg)" />
      <rect width={MW} height={MH} fill="url(#dots)" />
      {/* sea (Dead Sea) with hatched shore */}
      <path d="M930,110 C990,120 1000,260 985,400 C972,520 950,600 905,600 C870,596 885,470 890,360 C895,250 880,104 930,110 Z" fill={SEA} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
      <path d="M930,110 C990,120 1000,260 985,400" fill="none" stroke={CREAM} strokeWidth={3} opacity={0.5} transform="translate(-14,6)" />
      {[[140, 120], [700, 130], [180, 420], [760, 300], [120, 560], [800, 520], [470, 600], [260, 300]].map(([x, y], i) => hill(x, y, i))}
      {/* the short road: ink edges, light band */}
      <path d={`M${ROADPTS.map((p) => p.join(",")).join(" L")}`} fill="none" stroke={INK} strokeWidth={58} strokeLinecap="round" strokeLinejoin="round" />
      <path d={`M${ROADPTS.map((p) => p.join(",")).join(" L")}`} fill="none" stroke={ROAD} strokeWidth={44} strokeLinecap="round" strokeLinejoin="round" />
      <path d={`M${ROADPTS.map((p) => p.join(",")).join(" L")}`} fill="none" stroke="url(#dots)" strokeWidth={44} strokeLinecap="round" strokeLinejoin="round" />
      {/* Jerusalem: inked walls, towers, gate, hatched shadow side */}
      <g transform={`translate(${JER[0]},${JER[1]})`}>
        <path d="M-170,40 L-170,-40 L-150,-40 L-150,-52 L-130,-52 L-130,-40 L-90,-40 L-90,-52 L-70,-52 L-70,-40 L-30,-40 L-30,-80 L10,-80 L10,-40 L60,-40 L60,-52 L80,-52 L80,-40 L120,-40 L120,-62 L150,-62 L150,40 Z" fill={OCHRE} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        <path d="M120,-62 L150,-62 L150,40 L120,40 Z" fill="url(#hatch)" />
        <path d="M-25,-80 C-25,-118 5,-118 5,-80" fill={OCHRE} stroke={INK} strokeWidth={7} />
        <path d="M-22,40 L-22,4 C-22,-18 8,-18 8,4 L8,40 Z" fill={INK} />
        <path d="M-170,40 L150,40" stroke={OCHRE2} strokeWidth={8} />
      </g>
      {/* Bethlehem: small houses */}
      <g transform={`translate(${BET[0]},${BET[1]})`}>
        {[[-70, 0, 46, 40], [-22, -16, 52, 56], [34, 4, 44, 36]].map(([x, y, w, h], i) => (
          <g key={i}><rect x={x} y={y - h} width={w} height={h} fill={OCHRE} stroke={INK} strokeWidth={6} strokeLinejoin="round" />
            <rect x={x + w * 0.62} y={y - h} width={w * 0.38} height={h} fill="url(#hatch)" />
            <rect x={x + w * 0.35} y={y - h * 0.5} width={w * 0.24} height={h * 0.5} fill={INK} /></g>))}
        <path d="M-90,2 L90,2" stroke={INK} strokeWidth={6} />
      </g>
      {/* footprints on the short road: hollow on "close", gold on "went" */}
      {ROADPTS.slice(0, 7).map((p, i) => {
        const q = ROADPTS[Math.min(i + 1, ROADPTS.length - 1)], ang = Math.atan2(q[1] - p[1], q[0] - p[0]) * 180 / Math.PI + 90;
        const pulse = i === 0 && t > 37.9 && t < 39.0 ? 1 + 0.18 * Math.sin((t - 37.9) * 9) : 1;
        return <Print key={i} x={p[0]} y={p[1]} ang={ang} s={0.95 * pulse} t={t} at={37.30 + i * 2 / 30} goldAt={42.80 + i * 2 / 30} side={i % 2 ? 1 : -1} />;
      })}
      {/* Bethlehem star */}
      <g transform={`translate(${BET[0]},${BET[1] - 110})`}><polygon points="0,-30 8,-9 30,-8 12,5 18,27 0,14 -18,27 -12,5 -30,-8 -8,-9" fill={GOLD} stroke={INK} strokeWidth={5} strokeLinejoin="round" /></g>
    </svg>
  );
};

// ---- small comic caption box (owner OK 2026-11-15) ----
const Cap: React.FC<{ text: string; x: number; y: number; t: number; at: number }> = ({ text, x, y, t, at }) => t < at ? null : (
  <div style={{ position: "absolute", left: x, top: y, padding: "2px 14px", background: "#FFE14D", border: `4px solid ${INK}`, boxShadow: `5px 5px 0 ${INK}`,
    fontFamily: "BangersB", fontSize: 40, letterSpacing: 2, color: INK, transform: `scale(${L((t - at) * 30, 0, 4, 1.4, 1, OUT)})`, transformOrigin: "0 0" }}>{text}</div>
);

// ---- read-along pill (owner-locked Mockers style) ----
type W = { t: string; at: number; m?: string[] };
const Pill: React.FC<{ t: number; a: number; b: number; cy: number; lines: W[][]; sacred?: boolean }> = ({ t, a, b, cy, lines, sacred }) => {
  if (t < a || t >= b) return null;
  const op = L(t, a, a + (sacred ? 0.3 : 0.1), 0, 1) * L(t, b - 0.13, b, 1, 0);
  const h = lines.length * 62 + 40;
  return (
    <div style={{ position: "absolute", left: 100, top: cy - h / 2, width: 880, height: h, opacity: op, borderRadius: 46, background: PILL_FILL, border: `4px solid ${PILL_EDGE}`,
      display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center", fontFamily: "KalamB", fontSize: 54, lineHeight: "62px", color: INK }}>
      {lines.map((row, li) => <div key={li}>{row.map((w, wi) => {
        const k = (t - w.at) * 30, on = k >= 0;
        const gold = (w.m || []).includes("gold") && on, und = (w.m || []).includes("under2") && on;
        return <React.Fragment key={wi}>{wi > 0 ? " " : ""}<span style={{ display: "inline-block", position: "relative", opacity: on ? 1 : 0.38, transform: `scale(${on ? L(k, 0, 5, 1.07, 1, OUT) : 1})`,
          background: gold ? `rgba(246,185,35,${L(k, 0, 4, 0, 0.95)})` : undefined, borderRadius: 8, padding: "0 7px", margin: "0 -7px" }}>{w.t}
          {und && <svg style={{ position: "absolute", left: 0, top: 58, overflow: "visible" }} width={10} height={20}>
            <line x1={2} y1={0} x2={150} y2={-2} stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(k, 0, 6, 0, 1))} />
            <line x1={6} y1={9} x2={146} y2={8} stroke={INK} strokeWidth={5} strokeLinecap="round" {...draw(L(k, 2, 8, 0, 1))} /></svg>}
          </span></React.Fragment>;
      })}</div>)}
    </div>
  );
};

// ---- speed lines + impact burst ----
const Speed: React.FC<{ k: number; x0: number; y0: number; x1: number; y1: number }> = ({ k, x0, y0, x1, y1 }) => {
  if (k < 0 || k > 9) return null;
  const o = L(k, 0, 2, 0, 1) * L(k, 5, 9, 1, 0);
  return <svg style={{ position: "absolute", left: 0, top: 0, opacity: o }} width={1080} height={1920}>
    {Array.from({ length: 22 }).map((_, i) => { const y = y0 + (y1 - y0) * hash(i + 3), len = 120 + 260 * hash(i + 9);
      return <line key={i} x1={x1 + 40} y1={y} x2={x1 + 40 + len} y2={y - 6} stroke={INK} strokeWidth={3 + 5 * hash(i)} strokeLinecap="round" />; })}
  </svg>;
};
const Burst: React.FC<{ x: number; y: number; k: number; r?: number }> = ({ x, y, k, r = 70 }) => {
  if (k < 0 || k > 12) return null;
  const s = L(k, 0, 4, 0.3, 1, BACK), o = L(k, 7, 12, 1, 0);
  const pts = Array.from({ length: 24 }).map((_, i) => { const a = i * Math.PI / 12, rr = i % 2 ? r * 0.45 : r * (0.85 + 0.3 * hash(i)); return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`; }).join(" ");
  return <svg style={{ position: "absolute", left: 0, top: 0, opacity: o, overflow: "visible" }} width={1080} height={1920}>
    <g transform={`translate(${x},${y}) scale(${s})`}><polygon points={pts} fill="#FFFBEA" stroke={INK} strokeWidth={6} strokeLinejoin="round" /></g></svg>;
};

export const BethlehemV6Test: React.FC = () => {
  const f = useCurrentFrame(), t = T0 + f / 30;
  const [h] = React.useState(() => delayRender("bv6fonts"));
  React.useEffect(() => {
    Promise.all([new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(), new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load()])
      .then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); continueRender(h); }).catch(() => continueRender(h));
  }, []);
  const ct1 = 1.3 + (t - T0);                    // P1 clip time (1.0x)
  const [g1a, g1b, g2a, g2b] = gut("P1", ct1);    // gutters
  const top = { y0: 0, y1: g1a }, mid = { y0: g1b + 1, y1: g2a }, bot = { y0: g2b + 1, y1: 1920 };
  // whip in (3 frames) + page shake on "went"
  const whip = L(f, 0, 4, -260, 0, OUT), wblur = L(f, 0, 4, 10, 0);
  const sk = (t - 42.80) * 30, shake = sk >= 0 && sk < 6 ? (6 - sk) * 2.2 : 0;
  const sx = shake * Math.sin(sk * 2.7), sy = shake * Math.cos(sk * 3.3);
  // map panel brush-wipe in on "Bethlehem" (36.44, 8 frames)
  const wipeK = (t - 36.44) * 30, wu = L(wipeK, 0, 8, 0, 1, INOUT);
  const edge = Array.from({ length: 34 }).map((_, i) => { const y = i * 30 - 10; return `${(wu * 1180 - 60 + 40 * Math.sin(i * 1.7) + 26 * hash(i)).toFixed(0)}px ${y}px`; });
  const mapClip = wu >= 1 ? undefined : `polygon(0px -20px, ${edge.join(", ")}, 0px 1000px)`;
  // rack focus 39.04-41.9: experts bright, others dim + dots
  const rack = L(t, 39.04, 39.4, 0, 1) * L(t, 41.9, 42.2, 1, 0);
  const dim = (on: number) => on > 0 ? <div style={{ position: "absolute", inset: 0, background: `rgba(10,12,30,${0.42 * on})`, backgroundImage: "radial-gradient(rgba(0,0,0,0.5) 1.4px, transparent 1.6px)", backgroundSize: "9px 9px", opacity: on }} /> : null;
  // camel panel slam over the experts (42.80)
  const ck = (t - 42.80) * 30, camelOn = ck >= 0;
  const camelX = L(ck, 0, 4, 1100, 0, OUT);
  const P3T = 2.4; const [, p3a, p3b] = gut("P3", P3T + Math.max(0, t - 42.8)); // camel band = between P3 gutters
  // painted-road prints (bottom panel) - hollow on "went." 40.72, gold from 43.0
  const RP: [number, number][] = [[560, 0.86], [512, 0.74], [560, 0.63], [606, 0.53], [570, 0.44], [530, 0.36], [565, 0.29]];
  // M2 iris (44.0)
  const ik = (t - 44.0) * 30, irisR = L(ik, 0, 20, 0, 1500, INOUT);
  const midH = mid.y1 - mid.y0, sBet = { x: X0 + (BET[0] / MW) * (X1 - X0), y: mid.y0 + midH / 2 + (BET[1] - MH / 2) * ((X1 - X0) / MW) };
  const mapScale = Math.max((X1 - X0) / MW, midH / MH), mapDX = X0 + ((X1 - X0) - MW * mapScale) / 2, mapDY = mid.y0 + (midH - MH * mapScale) / 2;
  const betS = { x: mapDX + BET[0] * mapScale, y: mapDY + (BET[1] - 110) * mapScale };
  void sBet;
  return (
    <AbsoluteFill style={{ background: "#fff", overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, transform: `translate(${sx},${sy + whip}px)`, filter: wblur > 0.5 ? `blur(${wblur}px)` : undefined }}>
        <OffthreadVideo src={staticFile("bethlehem/clips/P1.mp4")} startFrom={Math.round(1.3 * 30)} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
        {/* top panel rack + camel slam */}
        <div style={{ position: "absolute", left: 0, top: top.y0, width: 1080, height: top.y1 - top.y0, overflow: "hidden" }}>{dim(0)}</div>
        {/* middle panel: the map */}
        <div style={{ position: "absolute", left: X0, top: mid.y0, width: X1 - X0, height: midH, overflow: "hidden", clipPath: mapClip, opacity: wipeK < 0 ? 0 : 1 }}>
          <MapPanel t={t} />
          <div style={{ position: "absolute", inset: 0, border: `7px solid ${INK}` }} />
          {dim(rack)}
        </div>
        {wipeK >= 0 && <>
          <Cap text="JERUSALEM" x={mapDX + (JER[0] - 160) * mapScale} y={mapDY + (JER[1] + 60) * mapScale} t={t} at={36.55} />
          <Cap text="BETHLEHEM" x={mapDX + (BET[0] - 60) * mapScale} y={mapDY + (BET[1] + 22) * mapScale} t={t} at={36.62} />
        </>}
        {/* bottom panel: painted road prints */}
        <div style={{ position: "absolute", left: 0, top: bot.y0, width: 1080, height: 1920 - bot.y0, overflow: "hidden" }}>
          {dim(rack)}
          <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920 - bot.y0}>
            {RP.map(([x, fy], i) => <Print key={i} x={x} y={(1920 - bot.y0) * fy} ang={-8 + 16 * hash(i)} s={L(fy, 0.29, 0.86, 0.55, 1.15)} t={t} at={40.72 + i * 2 / 30} goldAt={43.0 + i * 2 / 30} side={i % 2 ? 1 : -1} />)}
          </svg>
        </div>
        {/* camel panel slams over the experts */}
        {<div style={{ position: "absolute", left: 0, top: top.y0 + 10, width: 1080, height: top.y1 - top.y0 + 30, transform: `translateX(${camelX}px) rotate(-3deg)`, transformOrigin: "50% 100%", visibility: camelOn ? "visible" : "hidden" }}>
          <div style={{ position: "absolute", inset: 0, overflow: "hidden", border: `8px solid ${INK}`, background: "#000", boxShadow: `10px 12px 0 ${INK}` }}>
            <Sequence from={Math.round((42.80 - T0) * 30)} layout="none"><OffthreadVideo src={staticFile("bethlehem/clips/P3.mp4")} startFrom={Math.round(P3T * 30)} muted
              style={{ position: "absolute", left: 0, top: -(p3a) + (top.y1 - top.y0 + 30 - (p3b - p3a)) / 2, width: 1080, height: 1920, objectFit: "cover" }} /></Sequence>
          </div>
          <div style={{ position: "absolute", right: 40, bottom: -46, fontFamily: "BangersB", fontSize: 150, lineHeight: "150px", color: GOLD, WebkitTextStroke: `10px ${INK}`, paintOrder: "stroke fill",
            textShadow: `8px 8px 0 ${INK}`, transform: `rotate(-6deg) scale(${L(ck, 2, 6, 1.6, 1, OUT)})`, opacity: L(ck, 2, 3, 0, 1) }}>WENT</div>
        </div>}
        <Speed k={ck} x0={0} y0={top.y0 + 40} x1={0} y1={top.y1 - 20} />
        <Burst x={mapDX + ROADPTS[6][0] * mapScale} y={mapDY + ROADPTS[6][1] * mapScale} k={(t - (42.80 + 12 / 30)) * 30} r={80} />
      </div>
      {/* pills (above the shake) */}
      <Pill t={t} a={36.38} b={38.6} cy={1450} lines={[[{ t: "Bethlehem", at: 36.44, m: ["gold"] }, { t: "was", at: 37.0 }, { t: "close", at: 37.3 }, { t: "by.", at: 37.6 }]]} />
      <Pill t={t} a={38.98} b={41.9} cy={1450} lines={[[{ t: "The", at: 39.04 }, { t: "Bible", at: 39.3 }, { t: "never", at: 39.48, m: ["under2"] }, { t: "says", at: 39.74 }],
        [{ t: "the", at: 40.12 }, { t: "experts", at: 40.36 }, { t: "went.", at: 40.72 }]]} />
      <Pill t={t} a={42.06} b={43.1} cy={1450} lines={[[{ t: "The", at: 42.12 }, { t: "wise", at: 42.32 }, { t: "men", at: 42.56 }, { t: "went,", at: 42.8, m: ["gold"] }]]} />
      {/* M2: soft round panel opens from the Bethlehem star (sacred: no flash, no rays) */}
      {<div style={{ position: "absolute", inset: 0, visibility: ik >= 0 ? "visible" : "hidden", WebkitMaskImage: `radial-gradient(circle at ${betS.x}px ${betS.y}px, #000 ${Math.max(0, irisR - 60)}px, transparent ${irisR}px)`,
        maskImage: `radial-gradient(circle at ${betS.x}px ${betS.y}px, #000 ${Math.max(0, irisR - 60)}px, transparent ${irisR}px)` }}>
        <Sequence from={Math.round((44.0 - T0) * 30)} layout="none"><OffthreadVideo src={staticFile("bethlehem/clips/M2.mp4")} startFrom={Math.round(0.7 * 30)} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} /></Sequence>
      </div>}
      <Pill t={t} a={43.06} b={45.0} cy={1450} sacred lines={[[{ t: "and", at: 43.12 }, { t: "found", at: 44.1 }, { t: "the", at: 44.36 }, { t: "child.", at: 44.56 }]]} />
    </AbsoluteFill>
  );
};
