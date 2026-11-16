// Prophecy 01 "Born in Bethlehem" - $0 ANIMATIC (placeholder art). Spec: prophecy/01_bethlehem/COMIC_DESIGN_v2.md sec 5.
// All data (pages, panels, text items, times) lives in public/bethlehem/animatic_data.json so the machine checks read the same numbers.
// Everything is a pure function of the frame. 1080x1920 @30, 1548 frames.
import React from "react";
import { AbsoluteFill, Audio, Easing, delayRender, continueRender, interpolate, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import D from "../public/bethlehem/animatic_data.json";

export const BA_FPS = 30;
export const BA_FRAMES = 1548;

const PAPER = "#F1E6CF", INK = "#141210", GOLD = "rgb(232,168,28)", CREAM = "rgb(255,238,190)", SEPIA = "#2A1A0E";
const PILL_FILL = "rgba(225,225,228,0.588)", PILL_EDGE = "rgba(20,18,16,0.67)";
const F = (s: number) => Math.round(s * 30);
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (f: number, a: number, b: number, x: number, y: number, e?: (t: number) => number) =>
  interpolate(f, [a, b], [x, y], { ...cl, easing: e });
const OUT = Easing.out(Easing.cubic), INOUT = Easing.inOut(Easing.cubic), SINE = Easing.inOut(Easing.sin);
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

const SLOT: Record<string, [number, number, number, number]> = {
  FULL: [12, 12, 1056, 1896], INSET: [24, 1204, 1032, 580], "ROW-A": [24, 200, 1032, 580], "ROW-B": [24, 800, 1032, 580],
};

// ---------- fonts + text measuring ----------
let _ctx: CanvasRenderingContext2D | null = null;
const measure = (text: string, size: number, fam = "KalamB") => {
  if (!_ctx) _ctx = document.createElement("canvas").getContext("2d");
  _ctx!.font = `${size}px ${fam}`;
  return _ctx!.measureText(text).width;
};

// ---------- hand-wobbled border ----------
const wobblePath = (x: number, y: number, w: number, h: number, seed: number) => {
  const pts: [number, number][] = [];
  const edge = (x0: number, y0: number, x1: number, y1: number, k: number) => {
    const len = Math.hypot(x1 - x0, y1 - y0), n = Math.max(2, Math.round(len / 70));
    for (let i = 0; i < n; i++) {
      const t = i / n, j = (hash(seed * 31 + k * 7 + i) - 0.5) * 4.4;
      const nx = -(y1 - y0) / len, ny = (x1 - x0) / len;
      pts.push([x0 + (x1 - x0) * t + nx * j, y0 + (y1 - y0) * t + ny * j]);
    }
  };
  edge(x, y, x + w, y, 1); edge(x + w, y, x + w, y + h, 2); edge(x + w, y + h, x, y + h, 3); edge(x, y + h, x, y, 4);
  return "M" + pts.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" L") + " Z";
};

// ---------- small parts ----------
const Chip: React.FC<{ text: string; left?: number; right?: number; top: number; op?: number; fs?: number }> = ({ text, left, right, top, op = 1, fs = 28 }) => (
  <div style={{ position: "absolute", left, right, top, height: 42, padding: "0 14px", boxSizing: "border-box", background: GOLD, border: `3px solid ${INK}`,
    borderRadius: 16, fontFamily: "KalamB", fontSize: fs, lineHeight: "36px", color: INK, whiteSpace: "nowrap", opacity: op }}>{text}</div>
);

const GoldSpan: React.FC<{ a: number; children: React.ReactNode }> = ({ a, children }) => (
  <span style={{ background: `rgba(232,168,28,${a})`, borderRadius: 8, padding: "0 7px", margin: "0 -7px" }}>{children}</span>
);

const pillGeom = (it: any, cy: number) => { const h = it.lines.length * 62 + 40; return { h, top: cy - h / 2 }; };

export const Pill: React.FC<{ it: any; f: number; cy: number; sacred: boolean }> = ({ it, f, cy, sacred }) => {
  const s = F(it.start), e = F(it.end);
  if (f < s || f >= e) return null;
  const age = f - s;
  let op = sacred ? lerp(age, 0, 6, 0, 1) : lerp(age, 0, 4, 0, 1);
  if (it.id === "p10") op *= lerp(f, e - 6, e, 1, 0);
  const sc = sacred ? 1 : lerp(age, 0, 5, 0.95, 1, OUT);
  const { h, top } = pillGeom(it, cy);
  const lineEls = it.lines.map((ln: string, li: number) => {
    const g = it.gold;
    if (g && ln.includes(g.word)) {
      const [a, b] = ln.split(g.word);
      const ga = lerp(f, F(g.from), F(g.from) + 5, 0, 1) * (f < F(g.to) ? 1 : 0);
      return <div key={li}>{a}<GoldSpan a={ga}>{g.word}</GoldSpan>{b}</div>;
    }
    return <div key={li}>{ln}</div>;
  });
  let underline: React.ReactNode = null;
  if (it.underline) {
    const ln = it.lines[0], pre = ln.slice(0, ln.indexOf(it.underline.word));
    const W = measure(ln, 54), x0 = 510 - W / 2 + measure(pre, 54), ww = measure(it.underline.word, 54);
    const blockTop = top + (h - it.lines.length * 62) / 2, y = blockTop + 56;
    const pr = lerp(f, F(it.underline.at), F(it.underline.at) + 8, 0, 1, OUT);
    underline = (
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>
        <path d={`M${x0} ${y} Q${x0 + ww * 0.5} ${y + 5} ${x0 + ww} ${y - 2}`} fill="none" stroke={INK} strokeWidth={5} strokeLinecap="round"
          pathLength={1} strokeDasharray={1} strokeDashoffset={1 - pr} />
      </svg>
    );
  }
  const tabX = 96, chipR = 1080 - 924;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, opacity: op }}>
      {it.kind === "speech" && (
        <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>
          <path d={`M400 ${top + h - 3} L430 ${top + h + 38} L462 ${top + h - 3}`} fill={PILL_FILL} stroke={PILL_EDGE} strokeWidth={4} strokeLinejoin="round" />
        </svg>
      )}
      <div style={{ position: "absolute", left: 70, top, width: 880, height: h, boxSizing: "border-box", borderRadius: 46, background: PILL_FILL,
        border: `4px solid ${PILL_EDGE}`, display: "flex", flexDirection: "column", justifyContent: "center", textAlign: "center",
        fontFamily: "KalamB", fontSize: 54, lineHeight: "62px", color: INK, transform: `scale(${sc})` }}>{lineEls}</div>
      {underline}
      {it.tab && <Chip text={it.tab} left={tabX} top={top - 30} />}
      {it.chip && <Chip text={it.chip} right={chipR} top={top - 30} />}
    </div>
  );
};

export const Slab: React.FC<{ it: any; f: number }> = ({ it, f }) => {
  const s = F(it.start), e = F(it.end);
  if (f < s || f >= e) return null;
  const sc = lerp(f - s, 0, 8, 0.7, 1, Easing.out(Easing.back(1.8))), op = lerp(f, e - 5, e, 1, 0);
  return (
    <div style={{ position: "absolute", left: 0, top: 400, width: 1080, textAlign: "center", opacity: op, transform: `scale(${sc})`, transformOrigin: "50% 0" }}>
      {it.lines.map((ln: string, i: number) => (
        <div key={i} style={{ fontFamily: "BangersB", fontSize: 104, lineHeight: "114px", color: CREAM, WebkitTextStroke: "9px #4a2a12",
          paintOrder: "stroke fill", letterSpacing: 2 }}>{ln}</div>
      ))}
    </div>
  );
};

// ---------- placeholder picture ----------
const Placeholder: React.FC<{ p: any; w: number; h: number; lf: number }> = ({ p, w, h, lf }) => {
  const big = p.slot === "FULL";
  const grey = p.model === "Kling pro" ? ["#c9c4bb", "#aea89d"] : ["#c4c7cb", "#a6abb1"];
  const clipT = Math.min(p.clipLen, Math.max(0, lf / 30));
  const art = p.art;
  return (
    <div style={{ position: "absolute", inset: 0, background: art ? "#222" : `linear-gradient(160deg, ${grey[0]}, ${grey[1]})`, overflow: "hidden" }}>
      {art ? <img src={staticFile(art)} style={{ width: w, height: h, objectFit: "cover" }} /> :
        <div style={{ position: "absolute", inset: 0, backgroundImage: "repeating-linear-gradient(45deg, rgba(0,0,0,0.045) 0 14px, transparent 14px 28px)" }} />}
      <div style={{ position: "absolute", left: big ? 40 : 28, top: big ? 640 : 22, width: w - (big ? 80 : 56), fontFamily: "KalamB", color: art ? "#fff" : "#2b2d30",
        textShadow: art ? "0 2px 6px #000" : "none" }}>
        <div style={{ fontSize: big ? 110 : 84, lineHeight: 1 }}>{p.still}</div>
        <div style={{ fontSize: big ? 40 : 30, marginTop: 8 }}>{p.clip} · {p.model} · {p.clipLen} s clip</div>
        {!art && <div style={{ fontSize: big ? 46 : 34, marginTop: 14, lineHeight: 1.2, fontFamily: "KalamB" }}>{p.desc}</div>}
        {art && <div style={{ fontSize: big ? 38 : 28, marginTop: 10, color: "#ffd35a" }}>PLACEHOLDER - look test frame (not the film still)</div>}
      </div>
      <div style={{ position: "absolute", left: big ? 40 : 28, bottom: big ? 300 : 16, fontFamily: "KalamB", fontSize: big ? 34 : 26, color: art ? "#fff" : "#44474b",
        textShadow: art ? "0 2px 6px #000" : "none" }}>
        clip time {clipT.toFixed(1)} / {p.clipLen.toFixed(1)} s
      </div>
    </div>
  );
};

const Panel: React.FC<{ p: any; f: number }> = ({ p, f }) => {
  const [x, y, w, h] = SLOT[p.slot];
  const t0 = F(p.on[0]), k = f - t0;
  const isInset = p.slot !== "FULL";
  const wait = p.waiting ? [F(p.waiting[0]), F(p.waiting[1])] : null;
  const seed = p.id.charCodeAt(0) + p.id.charCodeAt(1);
  const path = wobblePath(x, y, w, h, seed);
  const keyline = p.slot === "INSET";
  const kp = (z: number) => wobblePath(x - 8, y - 8, w + 16, h + 16, seed + 3);
  // waiting frame (7B): empty ink frame draws slowly in silence
  if (wait && f >= wait[0] && f < t0) {
    const pr = lerp(f, wait[0], wait[1], 0, 1, SINE), a = lerp(f, wait[0], wait[0] + 6, 0, 1);
    return (
      <svg style={{ position: "absolute", left: 0, top: 0, opacity: 1 }} width={1080} height={1920}>
        <path d={kp(0)} fill="none" stroke={PAPER} strokeWidth={20} opacity={a} />
        <rect x={x} y={y} width={w} height={h} fill={PAPER} opacity={a} />
        <path d={path} fill="none" stroke={INK} strokeWidth={7} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - pr} />
      </svg>
    );
  }
  if (f < t0) return null;
  const lands = isInset && (p.land === "shake" || p.land === "slide");
  const dy = lands ? lerp(k, 0, 4, 80, 0, OUT) : 0;
  const op = lands ? lerp(k, 0, 2, 0, 1) : 1;
  const bp = lands ? lerp(k, 0, 8, 0, 1) : 1;
  const bloomP = p.bloom ? lerp(k, 0, 14, 0, 1, OUT) : 1;
  const blur = p.bloom ? 16 * (1 - bloomP) : 0, pop = p.bloom ? 0.35 + 0.65 * bloomP : 1;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, transform: `translateY(${dy}px)`, opacity: op }}>
      {keyline && <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}><path d={kp(0)} fill="none" stroke={PAPER} strokeWidth={20} /></svg>}
      <div style={{ position: "absolute", left: x + 3, top: y + 3, width: w - 6, height: h - 6, overflow: "hidden", opacity: pop, filter: blur > 0.2 ? `blur(${blur}px)` : undefined }}>
        <Placeholder p={p} w={w - 6} h={h - 6} lf={k} />
      </div>
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1080} height={1920}>
        <path d={path} fill="none" stroke={INK} strokeWidth={7} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - bp} />
      </svg>
    </div>
  );
};

// ---------- scroll card (global overlay) ----------
export const ScrollCard: React.FC<{ strips: any[]; openAt: number; closeAt: number; f: number }> = ({ strips, openAt, closeAt, f }) => {
  const oF = F(openAt), cF = F(closeAt);
  if (f < oF || f >= cF + 6) return null;
  const open = lerp(f, oF, oF + 12, 0, 1, INOUT) * lerp(f, cF, cF + 6, 1, 0, INOUT);
  const pw = 800 * open, cx = 510;
  const roller = (x: number) => (
    <div style={{ position: "absolute", left: x, top: 940, width: 40, height: 250, borderRadius: 12, background: "linear-gradient(90deg,#5a3a1c,#b07c3e 45%,#5a3a1c)",
      boxShadow: "0 4px 10px rgba(0,0,0,.35)" }} />
  );
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920 }}>
      <div style={{ position: "absolute", left: cx - pw / 2, top: 952, width: pw, height: 226, overflow: "hidden", background: "rgba(236,214,160,0.92)",
        borderTop: "3px solid #5C3A18", borderBottom: "3px solid #5C3A18", boxSizing: "border-box" }}>
        <div style={{ position: "absolute", left: (800 - pw) / 2 * 0 + (pw - 800) / 2, top: 0, width: 800, height: 226 }}>
          {strips.map((it, i) => {
            const s = F(it.start), nxt = i < strips.length - 1 ? F(strips[i + 1].start) : F(it.end);
            const enter = i === 0 ? 0 : lerp(f, s, s + 8, 220, 0, INOUT);
            const exit = i < strips.length - 1 ? lerp(f, nxt, nxt + 8, 0, -220, INOUT) : 0;
            if (f < s || (i < strips.length - 1 && f >= nxt + 8) || (i === strips.length - 1 && f >= F(it.end) + 6)) return null;
            return (
              <div key={it.id} style={{ position: "absolute", left: 0, top: 0, width: 800, height: 226, display: "flex", flexDirection: "column", justifyContent: "center",
                alignItems: "center", transform: `translateY(${enter + exit}px)` }}>
                {it.lines.map((ln: string, li: number) => (
                  <div key={li} style={{ fontFamily: "KalamB", fontSize: 60, lineHeight: "70px", color: SEPIA, whiteSpace: "pre" }}>
                    {ln.split(" ").map((wd: string, wi: number) => {
                      const a = clamp01((f - F(it.wt[li][wi])) / 6);
                      return <span key={wi} style={{ display: "inline-block", opacity: a, clipPath: `inset(0 ${(1 - a) * 100}% 0 0)` }}>{wd}{wi < ln.split(" ").length - 1 ? " " : ""}</span>;
                    })}
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </div>
      {roller(cx - pw / 2 - 40)}{roller(cx + pw / 2)}
      {open > 0.98 && <Chip text={strips[0].chip} right={1080 - 892} top={960} />}
    </div>
  );
};

// ---------- gold word (global overlay, table 2.2) ----------
export const GoldWord: React.FC<{ f: number }> = ({ f }) => {
  const FS = 60, ln1 = "But\u00A0thou,\u00A0Bethlehem";
  const W = measure(ln1, FS), pre = measure("But\u00A0thou,\u00A0", FS), ww = measure("Bethlehem", FS);
  const strip = { x: 510 - W / 2 + pre - 12, y: 1065 - 40, w: ww + 24, h: 80, fs: FS };
  const homeW = measure("Bethlehem", 54) + 44;
  const home = { x: 70, y: 210, w: homeW, h: 72, fs: 54 };
  const tabW = measure("Bethlehem", 28) + 34;
  const tab = { x: 96, y: 1041 - 30, w: tabW, h: 42, fs: 28 };
  type K = { f: number; r: typeof home; a: number; dx?: number };
  const ks: K[] = [
    { f: F(15.46), r: strip, a: 0 }, { f: F(15.46) + 4, r: strip, a: 1 }, { f: F(16.70), r: strip, a: 1 }, { f: F(16.70) + 8, r: home, a: 1 },
    { f: F(22.92), r: home, a: 1 }, { f: F(22.92) + 12, r: tab, a: 1 }, { f: F(23.54), r: tab, a: 1 }, { f: F(23.54) + 8, r: home, a: 1 },
    { f: F(26.9), r: home, a: 1 }, { f: F(26.9) + 10, r: home, a: 0, dx: -60 },
  ];
  if (f < ks[0].f || f >= ks[ks.length - 1].f) return null;
  let i = 0; while (i < ks.length - 2 && f >= ks[i + 1].f) i++;
  const A = ks[i], B = ks[i + 1], u = A.f === B.f ? 1 : clamp01((f - A.f) / (B.f - A.f)), e = SINE(u);
  const mix = (a: number, b: number) => a + (b - a) * e;
  const r = { x: mix(A.r.x, B.r.x), y: mix(A.r.y, B.r.y), w: mix(A.r.w, B.r.w), h: mix(A.r.h, B.r.h), fs: mix(A.r.fs, B.r.fs) };
  const a = mix(A.a, B.a), dx = mix(A.dx || 0, B.dx || 0);
  return (
    <div style={{ position: "absolute", left: r.x + dx, top: r.y, width: r.w, height: r.h, boxSizing: "border-box", background: GOLD, border: `3px solid ${INK}`, borderRadius: 14,
      opacity: a, fontFamily: "KalamB", fontSize: r.fs, lineHeight: `${r.h - 6}px`, textAlign: "center", color: INK, whiteSpace: "nowrap" }}>Bethlehem</div>
  );
};

// ---------- page ----------
const centerY = (pg: number) => (pg === 9 ? 1461 : 1092);

const Page: React.FC<{ pg: any; next: any; f: number }> = ({ pg, next, f }) => {
  const m0 = F(pg.mount[0]), m1 = F(pg.mount[1]);
  if (f < m0 || f >= m1) return null;
  let x = 0, y = 0, br = 1, sh = false;
  if (pg.trans === "slide" || pg.trans === "soft") {
    const p = (pg.trans === "soft" ? INOUT : OUT)(clamp01((f - F(pg.start)) / pg.tf));
    x = (1 - p) * 1080; sh = p < 1;
  }
  if (next && (next.trans === "slide" || next.trans === "soft")) {
    const q = (next.trans === "soft" ? INOUT : OUT)(clamp01((f - F(next.start)) / next.tf));
    x -= 60 * q; br = 1 - 0.15 * q;
  }
  // shake from panels that land with a hit
  let sx = 0, sy = 0;
  for (const p of D.panels) if (p.page === pg.n && p.land === "shake") {
    const k = f - F(p.on[0]);
    if (k >= 0 && k < 5) { const d = 1 - k / 5; sx += 6 * Math.sin(k * 2.6) * d; sy += 6 * Math.cos(k * 3.3 + 1) * d; }
  }
  const panels = D.panels.filter((p: any) => p.page === pg.n);
  const items = D.items.filter((it: any) => it.page === pg.n && (it.kind === "pill" || it.kind === "speech"));
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, background: PAPER, transform: `translate(${x + sx}px, ${y + sy}px)`,
      filter: br < 1 ? `brightness(${br})` : undefined, boxShadow: sh ? "-40px 0 40px rgba(0,0,0,0.35)" : undefined }}>
      {panels.map((p: any) => <Panel key={p.id} p={p} f={f} />)}
      {items.map((it: any) => <Pill key={it.id} it={it} f={f} cy={centerY(pg.n)} sacred={pg.sacred} />)}
    </div>
  );
};

const Riffle: React.FC<{ f: number }> = ({ f }) => {
  const s0 = F(6.95), cols = ["#F4EAD2", "#F1E3C3", "#EEDDB6", "#EAD6A8", "#E6CF9C"];
  return (
    <>
      {cols.map((c, k) => {
        const u = (f - (s0 + Math.round(4.75 * k))) / 5;
        if (u < 0 || u > 1) return null;
        return <div key={k} style={{ position: "absolute", left: 1080 - 2160 * u, top: 0, width: 1080, height: 1920, background: c, boxShadow: "-30px 0 40px rgba(0,0,0,0.25)" }} />;
      })}
    </>
  );
};

export type BAProps = { safe?: boolean; hud?: boolean };

export const BethlehemAnimatic: React.FC<BAProps> = ({ safe = false, hud = true }) => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("bethfonts"));
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    Promise.all([
      new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
      new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load(),
    ]).then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); setReady(true); continueRender(h); }).catch(() => continueRender(h));
  }, []);

  const pages = D.pages as any[];
  const cur = [...pages].reverse().find((p) => f >= F(p.start)) || pages[0];
  const t = f / 30;
  const slabs = D.items.filter((it: any) => it.kind === "slab");
  const c3 = D.items.filter((it: any) => it.id.startsWith("c3"));
  const c8 = D.items.filter((it: any) => it.id === "c8");
  if (!ready) return <AbsoluteFill style={{ background: PAPER }} />;
  const evs = D.events.filter((e: any) => f >= F(e.t) && f < F(e.t) + 10).map((e: any) => e.type.toUpperCase());

  return (
    <AbsoluteFill style={{ background: PAPER, overflow: "hidden" }}>
      <Audio src={staticFile("bethlehem/narration.mp3")} />
      {pages.map((pg, i) => <Page key={pg.n} pg={pg} next={pages[i + 1]} f={f} />)}
      <Riffle f={f} />
      {slabs.map((it: any) => <Slab key={it.id} it={it} f={f} />)}
      <ScrollCard strips={c3} openAt={14.40} closeAt={21.74} f={f} />
      <ScrollCard strips={c8} openAt={39.30} closeAt={41.54} f={f} />
      <GoldWord f={f} />
      {safe && <div style={{ position: "absolute", left: 60, top: 200, width: 900, height: 1340, border: "4px dashed #ff0066", boxSizing: "border-box" }} />}
      {hud && (
        <div style={{ position: "absolute", left: 18, top: 1862, padding: "4px 14px", background: "rgba(0,0,0,0.7)", color: "#fff", fontFamily: "KalamB", fontSize: 26, borderRadius: 10 }}>
          PAGE {cur.n}/10 {cur.name} · {t.toFixed(2)} s · f{f}{evs.length ? " · " + evs.join(" ") : ""}{f >= F(48.5) ? " · LANDING HOLD" : ""}
        </div>
      )}
    </AbsoluteFill>
  );
};
