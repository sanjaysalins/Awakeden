// comic_kit/doodles.tsx - the 14 doodles D1..D14. All wordless: wedges, dots, lines. Marks boil (3-frame swap), pictures never do.
// Every doodle is data: { kind, at, until?, tone?, seed?, pos?:{xy|anchor}, ...params } read from episode.json.
import React from "react";
import {
  BONE, Box, Doodle, EpCtx, Episode, FH, FW, INK, InkStroke, PILL_ZONE, Poly, Pt, Tone, blob, boilSeed, clamp, glide, lerp, markStyle, mulberry, outCubic, pathD, prog, rad, slam, wedgePts, wobblePts,
} from "./core";
import { anchorScreen } from "./layouts";
import { HandMark } from "./hand";

export const resolvePos = (ep: Episode, d: { pos?: Doodle["pos"] }, f: number): Pt => {
  const p = d.pos;
  if (!p) return [FW / 2, FH / 2];
  if (p.anchor) return anchorScreen(ep, p.anchor, f);
  return p.xy as Pt;
};
/** jolt (D10): the picture kicks `amp` px for `frames` frames. Also drives the page shake of panel_slam. */
export const shakeOffset = (ep: Episode, f: number): Pt => {
  let x = 0, y = 0;
  const kick = (at: number, amp: number, fr: number, seed: number) => {
    const k = f - at;
    if (k >= 0 && k < fr) { const g = mulberry(seed * 31 + k * 7); x += (g() * 2 - 1) * amp * (1 - k / fr); y += (g() * 2 - 1) * amp * (1 - k / fr); }
  };
  for (const d of ep.doodles) if (d.kind === "jolt") kick(d.at, d.amp ?? 8, d.frames ?? 4, 3);
  for (const s of ep.scenes) for (const m of s.moves || []) if (m.kind === "panel_slam" && (m.shake ?? 0) > 0) kick(m.at, m.shake, 4, 5);
  return [x, y];
};

const T = (d: Doodle, def: Tone): Tone => d.tone || def;
const fade = (f: number, d: Doodle, n = 5) => (d.until != null ? clamp((d.until - f) / n) : 1);

// ---- D1 ink_splat: one blot + 9 flecks, static after it lands ----
const InkSplat: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const c = resolvePos(ep, d, f), r = d.r ?? 20, s = slam(f, d.at);
  if (s == null) return null;
  const g = mulberry((d.seed ?? 1) * 17);
  const flecks = Array.from({ length: 9 }, () => { const a = d.dir != null ? rad(d.dir) + (g() - 0.5) * 2.4 : g() * 6.283, dd = r * (1.5 + g() * 1.6), rr = 3 + g() * 5; return [c[0] + Math.cos(a) * dd, c[1] + Math.sin(a) * dd, rr] as Pt3; });
  const tone = T(d, "ink");
  const m = markStyle(tone);
  return (
    <g opacity={fade(f, d)}>
      <Poly pts={blob(c, r, (d.seed ?? 1) * 5)} tone={tone} scale={s} about={c} />
      {flecks.map((q, i) => <circle key={i} cx={c[0] + (q[0] - c[0]) * s} cy={c[1] + (q[1] - c[1]) * s} r={q[2]} fill={m.fill} stroke={m.stroke} strokeWidth={3} />)}
    </g>
  );
};
type Pt3 = [number, number, number];

// ---- D3 shock_lines: a crown of short wedges round a head ----
const ShockLines: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const c = resolvePos(ep, d, f), s = slam(f, d.at);
  if (s == null) return null;
  const n = d.n ?? 8, [a0, a1] = d.arc as [number, number], r0 = d.r0 ?? 450, [ra, rb] = (d.r1 as [number, number]) ?? [560, 640];
  const end = d.until ?? d.at + (d.frames ?? 10), flyK = prog(f, end - 4, 4);
  const g = mulberry(boilSeed(f, d.seed ?? 3));
  const items = Array.from({ length: n }, (_, i) => {
    const a = lerp(a0, a1, (i + 0.5) / n) + (g() - 0.5) * 5, r1 = (i % 2 ? rb : ra) + (g() - 0.5) * 36, fly = flyK * 150;
    return <Poly key={i} pts={wedgePts(c, a, r0 + fly, r1 + fly, 26, 3)} tone={T(d, "ink")} scale={s} about={c} opacity={1 - flyK * 0.6} />;
  });
  return <g>{items}</g>;
};

// ---- D4 border_build: an ink frame draws itself, one side at a time ----
const BorderBuild: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  let [x0, y0, x1, y1] = d.box as number[];
  if (d.pic_box && d.anchor) { // anchored corners (normalised picture coords)
    const a = anchorScreen(ep, { ...d.anchor, pic: d.pic_box[0] }, f), b = anchorScreen(ep, { ...d.anchor, pic: d.pic_box[1] }, f);
    [x0, y0, x1, y1] = [a[0], a[1], b[0], b[1]];
  }
  const fp = d.frames_per_side ?? 8, op = fade(f, d, 5);
  const sides: Pt[][] = [[[x0, y0], [x1, y0]], [[x1, y0], [x1, y1]], [[x1, y1], [x0, y1]], [[x0, y1], [x0, y0]]];
  return <g opacity={op}>{sides.map((s, i) => <InkStroke key={i} pts={s} width={9} seed={(d.seed ?? 2) + i} tone={T(d, "two")} draw={[d.at + i * fp, fp]} f={f} boil />)}</g>;
};

// ---- D5 pill_edge: spiky = shout, dashed = whisper. Pill fill and words untouched (drawn under the pill PNG). ----
const roundRectPts = (b: Box, r: number, grow = 0): Pt[] => {
  const [x, y, w, h] = [b[0] - grow, b[1] - grow, b[2] + grow * 2, b[3] + grow * 2], R = r + grow, o: Pt[] = [];
  const arc = (cx: number, cy: number, a0: number) => { for (let i = 0; i <= 6; i++) { const a = rad(a0 + (i / 6) * 90); o.push([cx + Math.cos(a) * R, cy + Math.sin(a) * R]); } };
  arc(x + w - R, y + R, 270); arc(x + w - R, y + h - R, 0); arc(x + R, y + h - R, 90); arc(x + R, y + R, 180);
  return o;
};
const PillEdge: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, f }) => {
  const box = d.pill as Box, r = d.radius ?? 46;
  if (d.style === "dashed") {
    const pts = roundRectPts(box, r, 14);
    return <g opacity={fade(f, d, 4)}><InkStroke pts={pts} close width={8} tone="two" seed={9} f={f} dash="34 24" amp={0} /></g>;
  }
  const base = roundRectPts(box, r, 0);
  // resample every 47 px and push alternate points out along the normal by 26-60 px
  const per: Pt[] = [...base, base[0]], seg: { p: Pt; n: Pt }[] = [];
  let acc = 0, next = 0;
  for (let i = 1; i < per.length; i++) {
    const [ax, ay] = per[i - 1], [bx, by] = per[i], L = Math.hypot(bx - ax, by - ay) || 1, nx = (by - ay) / L, ny = -(bx - ax) / L;
    while (next <= acc + L) { const t = (next - acc) / L; seg.push({ p: [ax + (bx - ax) * t, ay + (by - ay) * t], n: [nx, ny] }); next += 23.5; }
    acc += L;
  }
  const g = mulberry(Math.floor(boilSeed(f, d.seed ?? 4)));
  const pts: Pt[] = [];
  seg.forEach((s, i) => { const h = i % 2 ? 0 : 26 + g() * 34; pts.push([s.p[0] + s.n[0] * h, s.p[1] + s.n[1] * h]); });
  const m = markStyle(d.tone || "ink");
  return <path d={pathD(pts, true)} fill={m.fill} stroke={m.stroke} strokeWidth={5} strokeLinejoin="miter" opacity={fade(f, d, 3)} />;
};

// ---- D6 shout_fan: wedges from a mouth, pop on chosen words ----
const ShoutFan: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const pops = d.pops as number[], c = resolvePos(ep, d, f);
  if (f < pops[0]) return null;
  const last = pops[pops.length - 1], end = d.until ?? last + 18;
  let j = 0; pops.forEach((p, i) => { if (f >= p) j = i; });
  const k = f - pops[j], s = slam(f, pops[j]) as number, big = (d.big as number[] | undefined)?.includes(j) ? 1.15 : 1;
  const [a0, a1] = d.arc as [number, number], n = d.n ?? 6, g = mulberry(boilSeed(f, d.seed ?? 6));
  const flyK = prog(f, end - 6, 6);
  const items = Array.from({ length: n }, (_, i) => {
    const a = lerp(a0, a1, (i + 0.5) / n) + (g() - 0.5) * 4, ro = ((i % 2 ? 300 : 210) + (g() - 0.5) * 30) * big * (k < 12 ? 1 : 0.82);
    return <Poly key={i} pts={wedgePts(c, a, (d.inner ?? 84) + flyK * 160, ro + flyK * 160, 22, 3)} tone={T(d, "bone")} scale={s} about={c} opacity={1 - flyK * 0.7} />;
  });
  return <g>{items}</g>;
};

// ---- D7 speed_lines: radial / focus / parallel ----
const SpeedLines: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const c = resolvePos(ep, d, f), n = d.n ?? 9, r0 = d.r0 ?? 420, [a0, a1] = (d.arc as [number, number]) ?? [0, 360];
  const g = mulberry(boilSeed(f, d.seed ?? 8)), inP = clamp((f - d.at) / 3), outP = d.until != null ? clamp((d.until - f) / 4) : 1;
  const items = Array.from({ length: n }, (_, i) => {
    const a = lerp(a0, a1, (i + 0.5) / n) + (g() - 0.5) * 6, len = (d.len ?? 640) * (0.8 + g() * 0.4);
    if (d.mode === "parallel") { const off = (i / n - 0.5) * 1400; const dir = rad(a0); const px = c[0] - Math.sin(dir) * off, py = c[1] + Math.cos(dir) * off; return <Poly key={i} pts={wedgePts([px, py], a0, -len / 2, len / 2, 7, 1)} tone={T(d, "bone")} />; }
    return <Poly key={i} pts={wedgePts(c, a, r0, r0 + len, 1, 9 + g() * 6)} tone={T(d, "bone")} />;
  });
  return <g opacity={Math.min(inP, outP)}>{items}</g>;
};

// ---- D8 drops: sweat / tear ----
const tear = (c: Pt, r: number): Pt[] => {
  const o: Pt[] = [[c[0], c[1] - r * 1.7]];
  for (let i = 0; i <= 10; i++) { const a = rad(-30 + (i / 10) * 240); o.push([c[0] + Math.cos(a + Math.PI / 2 * 0) * r * 0.9 * (i === 0 ? 1 : 1), c[1] + r * 0.4 + Math.sin(a) * r * 0.9]); }
  return o;
};
const Drops: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const c = resolvePos(ep, d, f), n = d.n ?? 3, fr = d.frames ?? 24, dir = rad(d.dir ?? 270), g = mulberry((d.seed ?? 3) * 13);
  const items: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    const st = d.at + i * 4, p = prog(f, st, fr), r = 10 + g() * 7, dist = 80 + g() * 30, side = (i - (n - 1) / 2) * 46;
    if (f < st || p >= 1) continue;
    const x = c[0] + Math.cos(dir) * dist * p - Math.sin(dir) * side, y = c[1] + Math.sin(dir) * dist * p + Math.cos(dir) * side;
    const op = p > 0.7 ? 1 - (p - 0.7) / 0.3 : 1;
    items.push(<Poly key={i} pts={tear([x, y], r)} tone={T(d, "bone")} opacity={op} />);
  }
  return <g>{items}</g>;
};

// ---- D9 motion_ticks: groups of 3 short strokes that slide the way the body moves ----
const MotionTicks: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const c = resolvePos(ep, d, f), fr = d.frames ?? 14, p = prog(f, d.at, fr), a = rad(d.dir ?? 270), len = d.len ?? 110, n = d.n ?? 3;
  const slide = outCubic(p) * len, op = p > 0.75 ? 1 - (p - 0.75) / 0.25 : 1;
  const ux = Math.cos(a), uy = Math.sin(a);
  return (
    <g opacity={op}>
      {Array.from({ length: n }, (_, i) => {
        const off = (i - (n - 1) / 2) * 26, sx = c[0] - uy * off + ux * slide, sy = c[1] + ux * off + uy * slide;
        return <InkStroke key={i} pts={[[sx, sy], [sx + ux * 56, sy + uy * 56]]} width={6} tone={T(d, "bone")} seed={(d.seed ?? 5) + i} f={f} amp={1} />;
      })}
    </g>
  );
};

// ---- D11 crosshatch_shade: diagonal hatching fades over a region (someone fades out of the story) ----
const Crosshatch: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const [x, y, w, h] = d.region as Box, k = prog(f, d.at, d.frames ?? 10) * (d.opacity ?? 0.75), pitch = d.pitch ?? 46, lines: React.ReactNode[] = [];
  for (let c = -h; c < w; c += pitch) lines.push(<line key={c} x1={x + c} y1={y} x2={x + c + h} y2={y + h} stroke={INK} strokeWidth={5} />);
  return <g opacity={k} clipPath={`inset(${y}px ${FW - x - w}px ${FH - y - h}px ${x}px)`}>{lines}</g>;
};

// ---- D12 halftone_vignette: dots close in from the edges, none in the middle, none in the pill ----
const HalftoneVignette: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, f }) => {
  const c = d.center as Pt, rx = d.rx ?? 470, ry = d.ry ?? 560, rmax = d.rmax ?? 10.5, pitch = d.pitch ?? 24, inP = prog(f, d.at, 8), m = markStyle(d.tone || "bone");
  const tf = d.top_fade as { y: number; f0: number; f1: number } | undefined;
  const dots: React.ReactNode[] = [];
  for (let row = 0; row * pitch < FH + pitch; row++) for (let col = 0; col * pitch < FW + pitch; col++) {
    const x = col * pitch + (row % 2 ? pitch / 2 : 0), y = row * pitch, dd = Math.hypot((x - c[0]) / rx, (y - c[1]) / ry);
    let r = rmax * clamp((dd - 0.8) / 0.55) * inP;
    const rc = d.rect as Box | undefined;
    if (rc && (x < rc[0] || x > rc[0] + rc[2] || y < rc[1] || y > rc[1] + rc[3])) continue;
    if (tf && y < tf.y) r *= 1 - prog(f, tf.f0, tf.f1 - tf.f0);
    if (r < 0.8) continue;
    if (x > PILL_ZONE[0] - 6 && x < PILL_ZONE[0] + PILL_ZONE[2] + 6 && y > PILL_ZONE[1] - 6 && y < PILL_ZONE[1] + PILL_ZONE[3] + 6) continue;
    dots.push(<circle key={row * 100 + col} cx={x} cy={y} r={r} fill={m.fill} stroke={m.stroke} strokeWidth={2.5} />);
  }
  return <g>{dots}</g>;
};

// ---- D13 rays: soft (5-6 thin lines) / burst (17 wedges). Always a clear ring round the centre. ----
const Rays: React.FC<{ d: Doodle; ep: Episode; f: number }> = ({ d, ep, f }) => {
  const c = resolvePos(ep, d, f), [a0, a1] = d.arc as [number, number], n = d.n ?? 6, cr = d.clear_r ?? 230, g = mulberry(boilSeed(f, d.seed ?? 12));
  const op = (d.opacity ?? 1) * clamp((f - d.at) / 8) * (d.until != null ? clamp((d.until - f) / 8) : 1);
  if (d.mode === "burst") {
    const s = slam(f, d.at) ?? 1, end = d.until ?? d.at + 22, flyK = prog(f, end - 8, 8);
    return <g opacity={1 - flyK * 0.6}>{Array.from({ length: n }, (_, i) => <Poly key={i} pts={wedgePts(c, lerp(a0, a1, (i + 0.5) / n) + (g() - 0.5) * 4, cr + flyK * 160, cr + 260 + (i % 2) * 120 + flyK * 160, 3, 26)} tone={T(d, "bone")} scale={s} about={c} />)}</g>;
  }
  return (
    <g opacity={op}>
      {Array.from({ length: n }, (_, i) => {
        const a = rad(lerp(a0, a1, (i + 0.5) / n) + (g() - 0.5) * 3), L = (d.len ?? 520) * (0.8 + g() * 0.4);
        return <InkStroke key={i} pts={[[c[0] + Math.cos(a) * cr, c[1] + Math.sin(a) * cr], [c[0] + Math.cos(a) * (cr + L), c[1] + Math.sin(a) * (cr + L)]]} width={6} tone={T(d, "two")} seed={i + 1} f={f} amp={1} />;
      })}
    </g>
  );
};

// ---- D14 crack_lines: 3 jagged ink lines across a panel (feeds panel_shatter) ----
const CrackLines: React.FC<{ d: Doodle; f: number }> = ({ d, f }) => {
  const [x, y, w, h] = d.panel as Box, n = d.n ?? 3, g = mulberry((d.seed ?? 4) * 11), fr = d.frames ?? 4;
  return (
    <g>
      {Array.from({ length: n }, (_, i) => {
        const pts: Pt[] = []; let px = x + (w * (i + 0.5)) / n + (g() - 0.5) * 60;
        for (let yy = y; yy <= y + h; yy += h / 6) { pts.push([px, yy]); px += (g() - 0.5) * 110; }
        return <InkStroke key={i} pts={pts} width={7} tone="two" seed={i + 3} draw={[d.at, fr]} f={f} amp={1.5} />;
      })}
    </g>
  );
};

/** panel_shatter (T13): kit device, unused by the Thief film. children = a frozen frame of the panel. */
export const PanelShatter: React.FC<{ box: Box; f: number; at: number; frames?: number; shards?: number; children: React.ReactNode }> = ({ box, f, at, frames = 12, shards = 6, children }) => {
  const [x, y, w, h] = box, p = prog(f, at, frames), g = mulberry(77), c: Pt = [w / 2 + (g() - 0.5) * 80, h / 2 + (g() - 0.5) * 80];
  const ring: Pt[] = [[0, 0], [w / 2, 0], [w, 0], [w, h / 2], [w, h], [w / 2, h], [0, h], [0, h / 2]];
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h }}>
      {Array.from({ length: shards }, (_, i) => {
        const a = ring[Math.floor((i * ring.length) / shards)], b = ring[Math.floor(((i + 1) * ring.length) / shards) % ring.length];
        const poly = `${c[0]}px ${c[1]}px,${a[0]}px ${a[1]}px,${b[0]}px ${b[1]}px`, dir = (g() - 0.5) * 2;
        return <div key={i} style={{ position: "absolute", inset: 0, clipPath: `polygon(${poly})`, transform: `translate(${dir * 120 * p}px, ${p * p * 1400}px) rotate(${dir * 40 * p}deg)`, transformOrigin: `${c[0]}px ${c[1]}px`, opacity: 1 - p * 0.3 }}>{children}</div>;
      })}
    </div>
  );
};

/** The doodle layer: one full-frame svg, under the pills. */
export const DoodleLayer: React.FC<{ f: number }> = ({ f }) => {
  const ep = React.useContext(EpCtx);
  const live = ep.doodles.filter((d) => f >= d.at && (d.until == null || f < d.until + 1));
  return (
    <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
      {live.map((d, i) => {
        const k = `${d.kind}${i}`;
        switch (d.kind) {
          case "ink_splat": return <InkSplat key={k} d={d} ep={ep} f={f} />;
          case "shock_lines": return <ShockLines key={k} d={d} ep={ep} f={f} />;
          case "border_build": return <BorderBuild key={k} d={d} ep={ep} f={f} />;
          case "pill_edge": return <PillEdge key={k} d={d} ep={ep} f={f} />;
          case "shout_fan": return <ShoutFan key={k} d={d} ep={ep} f={f} />;
          case "speed_lines": return <SpeedLines key={k} d={d} ep={ep} f={f} />;
          case "drops": return <Drops key={k} d={d} ep={ep} f={f} />;
          case "motion_ticks": return <MotionTicks key={k} d={d} ep={ep} f={f} />;
          case "crosshatch_shade": return <Crosshatch key={k} d={d} f={f} />;
          case "halftone_vignette": return <HalftoneVignette key={k} d={d} ep={ep} f={f} />;
          case "rays": return <Rays key={k} d={d} ep={ep} f={f} />;
          case "crack_lines": return <CrackLines key={k} d={d} f={f} />;
          case "thread": case "ink_ring": case "ink_strike": case "ink_underline": case "tally": case "route": return <HandMark key={k} d={d} f={f} />; // uplift kit K1-K6 (hand.tsx)
          default: return null; // jolt (shake), page_dots (layout) have no layer
        }
      })}
    </svg>
  );
};
