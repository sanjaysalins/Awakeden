// Immanuel (Prophecy Ep 02) - silent-plus-voice comic film v2 (63.8 s = voice 60.8 s + 3.0 s hold). $0.
// Same look/lettering as BethlehemV6.tsx (word pills, place/scripture tags, big comic words, shake/speed lines, gold end card).
// Every clip plays at 1.0x, trim only, hard cuts. Times are REAL film seconds from the whisper word times of audio_v2/narration.mp3.
import React from "react";
import { AbsoluteFill, Audio, Easing, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import WORDS from "../public/immanuel/words.json";

export const IMM_FRAMES = 1963, IMM_FPS = 30; // 65.44 s (v2.2)
const INK = "#121014", GOLD = "#F6B923", CREAM = "#FFF4D6";
const PILL_FILL = "rgba(225,225,228,0.588)", PILL_EDGE = "rgba(20,18,16,0.67)";
const F = (s: number) => Math.round(s * 30);
const cl = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const L = (x: number, a: number, b: number, p: number, q: number, e?: (t: number) => number) => interpolate(x, [a, b], [p, q], { ...cl, easing: e });
const OUT = Easing.out(Easing.cubic), BACK = Easing.out(Easing.back(1.8)), SINE = Easing.inOut(Easing.sin);
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const draw = (p: number) => ({ pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - Math.max(0, Math.min(1, p)) });
const wt = (i: number): number => (WORDS as any[])[i].s;
const we = (i: number): number => (WORDS as any[])[i].e;

// ---------------- slots (film seconds; clip plays from its own 0) ----------------
const SLOTS: { clip: string; a: number; b: number }[] = [
  { clip: "P1_v2", a: 0.00, b: 12.04 },
  { clip: "G1", a: 12.04, b: 17.74 },
  { clip: "M1", a: 17.74, b: 24.74 },
  { clip: "P2", a: 24.74, b: 32.78 },
  { clip: "M2_long", a: 32.78, b: 45.40 },
  { clip: "P3", a: 45.40, b: 53.09 },
  { clip: "P4_v2", a: 53.09, b: 59.19 },
  { clip: "M3_v2", a: 59.19, b: 65.44 },
];
const T_END = 62.64; // after the last word (62.443)

const Vid: React.FC<{ clip: string; a: number; b: number }> = ({ clip, a, b }) => (
  <Sequence from={F(a)} durationInFrames={Math.max(1, F(b) - F(a))} layout="none">
    <OffthreadVideo src={staticFile(`immanuel/clips/${clip}.mp4`)} startFrom={0} muted style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, objectFit: "cover" }} />
  </Sequence>
);
const shakeAt = (t: number, hit: number, amp = 2.2): [number, number] => { const k = (t - hit) * 30; if (k < 0 || k >= 6) return [0, 0]; const a = (6 - k) * amp; return [a * Math.sin(k * 2.7), a * Math.cos(k * 3.3)]; };

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

// ---------------- lettering bits (same as Bethlehem V6) ----------------
const Cap: React.FC<{ text: string; x: number; y: number; t: number; at: number; until?: number; size?: number }> = ({ text, x, y, t, at, until = 999, size = 40 }) => (t < at || t >= until) ? null : (
  <div style={{ position: "absolute", left: x, top: y, padding: "2px 14px", background: "#FFE14D", border: `4px solid ${INK}`, boxShadow: `5px 5px 0 ${INK}`, whiteSpace: "nowrap",
    fontFamily: "BangersB", fontSize: size, letterSpacing: 2, color: INK, opacity: L(t, until - 0.1, until, 1, 0), transform: `scale(${L((t - at) * 30, 0, 4, 1.4, 1, OUT)})`, transformOrigin: "0 0" }}>{text}</div>
);
const Chip: React.FC<{ text: string; left?: number; right?: number; top: number; rot?: number; op?: number; cream?: boolean; dashed?: boolean; size?: number }> = ({ text, left, right, top, rot = 0, op = 1, cream, dashed, size = 28 }) => (
  <div style={{ position: "absolute", left, right, top, height: size * 1.5, padding: "0 14px", boxSizing: "border-box", background: cream ? CREAM : GOLD, border: `3px ${dashed ? "dashed" : "solid"} ${INK}`,
    borderRadius: 16, fontFamily: "KalamB", fontSize: size, lineHeight: `${size * 1.28}px`, color: INK, whiteSpace: "nowrap", opacity: op, transform: `rotate(${rot}deg)` }}>{text}</div>
);
const Big: React.FC<{ text: string; t: number; at: number; until: number; left: number; top: number; rot: number; color: string; size?: number; stroke?: number }> = ({ text, t, at, until, left, top, rot, color, size = 140, stroke = 9 }) => {
  const k = (t - at) * 30; if (k < 0 || t >= until) return null;
  return <div style={{ position: "absolute", left, top, fontFamily: "BangersB", fontSize: size, lineHeight: `${size * 1.07}px`, color, WebkitTextStroke: `${stroke}px ${INK}`, paintOrder: "stroke fill", textShadow: `${stroke * 0.8}px ${stroke * 0.8}px 0 ${INK}`,
    whiteSpace: "nowrap", transform: `rotate(${L(k, 0, 6, rot * 2.2, rot, OUT)}deg) scale(${L(k, 0, 4, 1.6, 1, OUT)})`, opacity: L(k, 0, 1.5, 0, 1) * L(t, until - 0.12, until, 1, 0) }}>{text}</div>;
};

// ---------------- read-along pills ----------------
const TXT: Record<number, string> = { 4: "God", 5: "no.", 21: "\"fear", 22: "not,\"", 36: "\"save", 37: "me.\"", 41: "sign:", 35: "king:", 42: "Behold,", 57: "Seven hundred", 72: "Joseph:", 73: "Joseph,", 86: "wife:", 92: "JESUS:",
  115: "means:", 125: "He", 134: "He", 140: "promised:", 145: "always.", 30: "refused.", 141: "I", 98: "people", 17: "of" };
type W = { t: string; at: number; m?: string[] };
const r = (a: number, b: number, marks: Record<number, string[]> = {}): W[] => { const o: W[] = []; for (let i = a; i <= b; i++) o.push({ t: TXT[i] ?? (WORDS as any[])[i].w, at: wt(i), m: marks[i] }); return o; };
type PillSpec = { a: number; b: number; cy: number; lines: W[][]; sacred?: boolean };
const RAW: { lines: W[][]; sacred?: boolean; cy?: number }[] = [
  { lines: [r(0, 2), r(3, 5)] },
  { lines: [r(6, 8, { 8: ["gold"] })] },
  { lines: [r(9, 10), r(11, 14)] },
  { lines: [r(15, 18)] },
  { lines: [r(19, 22, { 21: ["gold"] })] },
  { lines: [r(23, 25), r(26, 28)] },
  { lines: [r(29, 31, { 30: ["gold"] })] },
  { lines: [r(32, 35)] },
  { lines: [r(36, 37, { 36: ["gold"] })] },
  { lines: [r(38, 41)] },
  { lines: [r(42, 46)], sacred: true },
  { lines: [r(47, 50)], sacred: true },
  { lines: [r(51, 53), r(54, 56, { 56: ["gold"] })], sacred: true },
  { lines: [r(57, 59, { 57: ["gold"] })] },
  { lines: [r(60, 62)] },
  { lines: [r(63, 65), r(66, 68)] },
  { lines: [r(69, 72)] },
  { lines: [r(73, 77)], sacred: true },
  { lines: [r(78, 83, { 78: ["gold"] })], sacred: true },
  { lines: [r(84, 86)], sacred: true },
  { lines: [r(87, 92, { 92: ["gold"] })], sacred: true },
  { lines: [r(93, 96), r(97, 101, { 96: ["gold"] })], sacred: true },
  { lines: [r(102, 103)] },
  { lines: [r(104, 110)] },
  { lines: [r(111, 113, { 113: ["gold"] })] },
  { lines: [r(114, 118, { 116: ["gold"] })] },
  { lines: [r(119, 123), r(124, 129)] },
  { lines: [r(130, 133), r(134, 138, { 135: ["gold"] })] },
  { lines: [r(139, 140)] },
  { lines: [r(141, 145)], sacred: true },
  { lines: [r(146, 149, { 148: ["gold"] })], sacred: true },
];
// pill position per slot: keep pills off faces (slot 2 low, slot 6 single-line on the gutter, slot 7 on the cloud panel)
const cyFor = (a: number) => (a >= 12.04 && a < 17.74 ? 1640 : a >= 45.25 && a < 52.95 ? 1262 : a >= 52.95 && a < 59.09 ? 1100 : 1450);
const PILLS: PillSpec[] = RAW.map((p, i) => {
  const first = p.lines[0][0].at, lastRow = p.lines[p.lines.length - 1], last = lastRow[lastRow.length - 1];
  const lastIdx = (WORDS as any[]).findIndex((w, k) => Math.abs(w.s - last.at) < 1e-6 && k >= 0);
  const nextA = i + 1 < RAW.length ? RAW[i + 1].lines[0][0].at : 99;
  return { a: first - 0.04, b: Math.min(we(lastIdx) + 0.42, nextA - 0.02), cy: p.cy ?? cyFor(first), lines: p.lines, sacred: p.sacred };
});
const PillView: React.FC<{ t: number; s: PillSpec }> = ({ t, s }) => {
  const { a, b, lines, sacred } = s;
  if (t < a || t >= b) return null;
  const op = L(t, a, a + (sacred ? 0.3 : 0.1), 0, 1) * L(t, b - 0.13, b, 1, 0);
  const h = lines.length * 62 + 40, top = s.cy - h / 2;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, opacity: op }}>
      <div style={{ position: "absolute", left: 100, top, width: 880, height: h, boxSizing: "border-box", borderRadius: 46, background: PILL_FILL, border: `4px solid ${PILL_EDGE}`,
        display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center", fontFamily: "KalamB", fontSize: 54, lineHeight: "62px", color: INK }}>
        {lines.map((row, li) => (
          <div key={li} style={{ position: "relative" }}>{row.map((w, wi) => {
            const k = (t - w.at) * 30, on = k >= 0;
            const gold = (w.m || []).includes("gold") && on;
            return <React.Fragment key={wi}>{wi > 0 ? " " : ""}<span style={{ display: "inline-block", position: "relative", opacity: on ? 1 : 0.38, transform: `scale(${on ? L(k, 0, 5, 1.07, 1, OUT) : 1})`,
              background: gold ? `rgba(246,185,35,${L(k, 0, 4, 0, 0.95)})` : undefined, borderRadius: 8, padding: "0 7px", margin: "0 -7px" }}>{w.t}</span></React.Fragment>;
          })}</div>
        ))}
      </div>
    </div>
  );
};

// ---------------- gold promise frame (end card), same as Bethlehem ----------------
type Rc = { x: number; y: number; w: number; h: number };
const rectPts = (rc: Rc, seed: number): [number, number][] => {
  const per = 2 * (rc.w + rc.h), n = Math.max(12, Math.round(per / 26)), o: [number, number][] = [];
  for (let i = 0; i <= n; i++) {
    const s = (i / n) * per, j = (hash(i + seed) - 0.5) * 3.6; let x = 0, y = 0;
    if (s < rc.w) { x = rc.x + s; y = rc.y + j; } else if (s < rc.w + rc.h) { x = rc.x + rc.w + j; y = rc.y + (s - rc.w); }
    else if (s < 2 * rc.w + rc.h) { x = rc.x + rc.w - (s - rc.w - rc.h); y = rc.y + rc.h + j; } else { x = rc.x + j; y = rc.y + rc.h - (s - 2 * rc.w - rc.h); }
    o.push([x, y]);
  }
  o[o.length - 1] = o[0]; return o;
};
const GoldFrame: React.FC<{ r: Rc; p: number; sw?: number }> = ({ r: rc, p, sw = 12 }) => {
  if (p <= 0) return null;
  const d = rectPts(rc, 7).map((q, i) => `${i ? "L" : "M"}${q[0].toFixed(1)} ${q[1].toFixed(1)}`).join(" ");
  return <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1080} height={1920}>
    <path d={d} fill="none" stroke={INK} strokeWidth={sw + 8} strokeLinejoin="round" {...draw(p)} />
    <path d={d} fill="none" stroke={GOLD} strokeWidth={sw} strokeLinejoin="round" {...draw(p)} />
  </svg>;
};

// ---------------- the film ----------------
export const ImmanuelV2: React.FC = () => {
  const f = useCurrentFrame(), t = f / 30;
  const [h] = React.useState(() => delayRender("imm2fonts"));
  React.useEffect(() => {
    Promise.all([new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(), new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load()])
      .then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); continueRender(h); }).catch(() => continueRender(h));
  }, []);

  const [shx, shy] = (() => {
    const hits = [wt(5), wt(30), wt(37), wt(56), wt(113), wt(138), wt(145)];
    let sx = 0, sy = 0; for (const hh of hits) { const [a, b] = shakeAt(t, hh, 2.2); sx += a; sy += b; } return [sx, sy];
  })();
  const endP = L(t, T_END, T_END + 1.0, 0, 1, SINE);

  return (
    <AbsoluteFill style={{ background: "#fff", overflow: "hidden" }}>
      <Audio src={staticFile("immanuel/narration.mp3")} />
      <div style={{ position: "absolute", inset: 0, transform: `translate(${shx}px,${shy}px)` }}>
        {SLOTS.map((s, i) => <Vid key={i} clip={s.clip} a={s.a} b={s.b} />)}
        {/* 1 hook + Ahaz */}
        <Big text="NO." t={t} at={wt(5)} until={3.0} left={380} top={110} rot={-4} color={CREAM} size={150} />
        <Cap text="KING AHAZ" x={26} y={22} t={t} at={wt(9)} until={10.25} size={56} />
        <Speed k={(t - wt(30)) * 30} y0={400} y1={1000} />
        {/* 2 gold to Assyria */}
        <Cap text="2 KINGS 16:7" x={26} y={22} t={t} at={12.12} until={17.7} size={52} />
        <Big text="SAVE ME" t={t} at={wt(36)} until={16.8} left={250} top={130} rot={-3} color={GOLD} size={130} />
        <Burst x={540} y={330} k={(t - wt(36)) * 30 - 2} r={90} />
        {/* 3 Isaiah */}
        <Cap text="ISAIAH 7:14" x={26} y={22} t={t} at={17.86} until={24.61} size={56} />
        <Big text="IMMANUEL" t={t} at={wt(56)} until={24.61} left={150} top={140} rot={-3} color={GOLD} size={130} />
        <Cap text="GOD WITH US" x={150} y={300} t={t} at={wt(56) + 0.5} until={24.61} size={58} />
        {/* 4 Mary / Joseph */}
        <Cap text="700 YEARS LATER" x={26} y={22} t={t} at={wt(57)} until={32.83} size={64} />
        {/* 5 angel */}
        <Cap text="MATTHEW 1:20-21" x={26} y={22} t={t} at={33.0} until={45.25} size={52} />
        <Big text="FEAR NOT" t={t} at={wt(78)} until={38.0} left={170} top={150} rot={-3} color={CREAM} size={130} />
        <Big text="JESUS" t={t} at={wt(92)} until={43.75} left={300} top={150} rot={3} color={GOLD} size={140} />
        {/* 6 child saves */}
        <Big text="HE SAVES" t={t} at={wt(111)} until={51.05} left={170} top={140} rot={-3} color={GOLD} size={140} />
        <Big text="GOD WITH US" t={t} at={wt(116)} until={53.05} left={90} top={140} rot={3} color={CREAM} size={120} />
        {/* 7 cross / tomb */}
        <Cap text="AT THE CROSS" x={26} y={22} t={t} at={54.35} until={57.05} size={56} />
        <Cap text="THE THIRD DAY" x={26} y={22} t={t} at={57.35} until={59.09} size={56} />
      </div>
      {PILLS.map((s, i) => <PillView key={i} t={t} s={s} />)}
      {/* end card (slot 8, after the last word) */}
      {t >= T_END && <>
        <GoldFrame r={{ x: 10, y: 10, w: 1060, h: 1900 }} p={endP} />
        <div style={{ position: "absolute", left: 0, top: 1330, width: 1080, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
          <div style={{ position: "relative", height: 110, width: 640 }}><Chip text="GOD WITH US" left={0} top={0} size={72} op={L(t, T_END + 0.2, T_END + 0.5, 0, 1)} /></div>
          <div style={{ position: "relative", height: 70, width: 480 }}><Chip text="MATTHEW 1:23" left={0} top={0} cream size={46} op={L(t, T_END + 0.9, T_END + 1.2, 0, 1)} /></div>
        </div>
      </>}
    </AbsoluteFill>
  );
};
