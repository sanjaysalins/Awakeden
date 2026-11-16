// comic_kit/transitions.tsx - the 16 cut transitions T1..T16 (those that run between two scenes) as pure style functions.
// T1 panel_slam, T2 panel_dive, T4 page_glide, T10 pull_out_to_page live on a panel/scene (see layouts.tsx panelState/cameraY).
// Each function returns Fx: CSS for outgoing A and incoming B (+ which is on top) and an overlay of drawn marks.
import React from "react";
import {
  BONE, FH, FW, INK, InkStroke, PAPER, Poly, Pt, TransitionSpec, Tone, blob, boilSeed, clamp, glide, lerp, mulberry, outCubic, prog, rad, wedgePts, wobblePts, pathD, Box,
} from "./core";

export interface Fx { a: React.CSSProperties; b: React.CSSProperties; aTop?: boolean; overlay?: React.ReactNode; aHidden?: boolean; bHidden?: boolean }

export const svgMask = (inner: string): React.CSSProperties => {
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='${FW}' height='${FH}' viewBox='0 0 ${FW} ${FH}'>${inner}</svg>`;
  const u = `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
  return { WebkitMaskImage: u, maskImage: u, WebkitMaskSize: `${FW}px ${FH}px`, maskSize: `${FW}px ${FH}px`, WebkitMaskRepeat: "no-repeat", maskRepeat: "no-repeat" } as React.CSSProperties;
};
const farthest = (c: Pt) => Math.max(Math.hypot(c[0], c[1]), Math.hypot(FW - c[0], c[1]), Math.hypot(c[0], FH - c[1]), Math.hypot(FW - c[0], FH - c[1]));
const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0 }}>{children}</svg>;
/** transition marks never cross the pill zone (x 70-1010, y 974-1250): the pill and its tabs stay clear. */
const SvgNoPill: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0 }}>
    <defs><clipPath id="nopill"><path clipRule="evenodd" d={`M0 0H${FW}V${FH}H0Z M70 974H1010V1250H70Z`} /></clipPath></defs>
    <g clipPath="url(#nopill)">{children}</g>
  </svg>
);

/** halftone dots as an SVG mask string. mode radial: opens from `center`. rise: climbs from the bottom with a 240 px band of dots. */
export const halftoneMask = (mode: string, p: number, center: Pt, pitch = 22): string => {
  const out: string[] = [];
  const Rmax = farthest(center) + 320, R = p * Rmax, band = 240, ye = FH - p * (FH + band);
  for (let row = 0; row * pitch < FH + pitch; row++) {
    for (let col = 0; col * pitch < FW + pitch; col++) {
      const x = col * pitch + (row % 2 ? pitch / 2 : 0), y = row * pitch;
      let k: number;
      if (mode === "rise") k = clamp((y - ye) / band);
      else k = clamp((R - Math.hypot(x - center[0], y - center[1])) / 300);
      const r = 16.5 * k;
      if (r > 0.4) out.push(`<circle cx='${x}' cy='${y}' r='${r.toFixed(1)}' fill='white'/>`);
    }
  }
  return out.join("");
};

const speedLinesRadial = (f: number, at: number, center: Pt, n = 30, r0 = 240, arc: [number, number] = [0, 360]): React.ReactNode => {
  const g = mulberry(Math.floor(boilSeed(f, 41)));
  const items: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    const a = arc[0] + ((i + 0.5) / n) * (arc[1] - arc[0]) + (g() - 0.5) * 8, r1 = 1500, w = 12 + g() * 16;
    items.push(<Poly key={i} pts={wedgePts(center, a, r0 + g() * 160, r1, w, 1)} tone="bone" />);
  }
  return <SvgNoPill>{items}</SvgNoPill>;
};

export const transitionFx = (t: TransitionSpec, f: number): Fx => {
  const n = t.frames, p = prog(f, t.at, n);
  switch (t.kind) {
    case "whip_pan": { // T3 vertical only, 10 bone streaks for 3 frames
      const e = glide(p), s = t.dir === "down" ? 1 : -1;
      const g = mulberry(7 + Math.floor(f));
      const streaks = f - t.at < 3 ? Array.from({ length: 10 }, (_, i) => <rect key={i} x={g() * FW} y={g() * 300 - 100} width={5 + g() * 9} height={900 + g() * 1000} fill={BONE} opacity={0.85} />) : null;
      return { a: { transform: `translateY(${s * FH * e}px)` }, b: { transform: `translateY(${-s * FH * (1 - e)}px)` }, aTop: false, overlay: streaks && <SvgNoPill>{streaks}</SvgNoPill> };
    }
    case "slam_cut": { // T5 B arrives as a tilted full-frame panel at scale 1.25 and snaps flat
      const e = outCubic(p);
      return { a: {}, b: { transform: `rotate(${(t.tilt ?? 3) * (1 - e)}deg) scale(${1 + 0.25 * (1 - e)})` } };
    }
    case "speed_zoom": { // T6 A zooms to 1.9 about a point, 30 radial speed lines, B lands from 1.18 to 1.0
      const c = (t.center || [540, 900]) as Pt, za = Math.max(2, Math.round(n * 0.6));
      const pa = prog(f, t.at, za), pb = prog(f, t.at + za, n - za);
      const aS = lerp(1, 1.9, glide(pa)), bS = lerp(1.18, 1, outCubic(pb));
      return {
        a: { transform: `scale(${aS})`, transformOrigin: `${c[0]}px ${c[1]}px` }, b: { transform: `scale(${bS})`, transformOrigin: `${c[0]}px ${c[1]}px` },
        bHidden: f < t.at + za, overlay: f - t.at < n ? speedLinesRadial(f, t.at, c, 30, 240, (t.lines_arc || [0, 360]) as [number, number]) : null,
      };
    }
    case "ink_slash_split": // T7 handled inside the split scene (pagemoves.tsx); B simply sits on top
      return { a: {}, b: {} };
    case "halftone_dissolve": { // T8
      const c = (t.center || [540, 960]) as Pt;
      return { a: {}, b: p >= 1 ? {} : svgMask(halftoneMask(t.mode || "radial", p, c)) };
    }
    case "page_flip_up": { // T9 A is a page hinged at the top; lifts up and away, darkening as it tips
      const e = glide(p), ang = 104 * e;
      return { a: { transformOrigin: "50% 0%", transform: `perspective(2200px) rotateX(${ang}deg)`, filter: `brightness(${1 - 0.65 * e})` }, b: {}, aTop: true, aHidden: p >= 1 };
    }
    case "border_fall": { // T11 the whole page drops out of the bottom with a 5 degree tip
      const e = p * p * (3 - 2 * p) * 0.35 + p * p * 0.65;
      return { a: { transformOrigin: "0% 100%", transform: `translateY(${e * 2300}px) rotate(${5 * e}deg)` }, b: {}, aTop: true, aHidden: p >= 1 };
    }
    case "punch_cut": // T12
      return { a: {}, b: {} };
    case "ink_bleed": { // T14 B blots in from a point with a ragged edge and a thin ink rim leading it
      const o = (t.origin || [540, 960]) as Pt, R = p * (farthest(o) + 260), g = mulberry(31);
      const ph = Array.from({ length: 24 }, () => g() * 6.28);
      const pts: Pt[] = Array.from({ length: 72 }, (_, i) => { const a = (i / 72) * Math.PI * 2; const nz = 0.1 * Math.sin(a * 5 + ph[0]) + 0.07 * Math.sin(a * 9 + ph[1]) + 0.04 * Math.sin(a * 17 + ph[2]); const r = R * (1 + nz); return [o[0] + Math.cos(a) * r, o[1] + Math.sin(a) * r] as Pt; });
      const rim: Pt[] = pts.map((q) => [o[0] + (q[0] - o[0]) * 1.012, o[1] + (q[1] - o[1]) * 1.012] as Pt);
      return {
        a: {}, b: p >= 1 ? {} : { clipPath: `polygon(${pts.map((q) => `${q[0].toFixed(1)}px ${q[1].toFixed(1)}px`).join(",")})` },
        overlay: t.rim !== false && p > 0 && p < 1 ? <Svg><path d={pathD(rim, true)} fill="none" stroke={INK} strokeWidth={7} /></Svg> : null,
      };
    }
    case "iris": { // T15 an ink ring opens (or closes) from a point; B is inside the ring
      const c = (t.center || [540, 960]) as Pt, R = glide(p) * (farthest(c) + 40);
      return {
        a: {}, b: p >= 1 ? {} : { clipPath: `circle(${R}px at ${c[0]}px ${c[1]}px)` },
        overlay: t.ring !== false && p > 0 && p < 1 ? <Svg><circle cx={c[0]} cy={c[1]} r={R} fill="none" stroke={BONE} strokeWidth={26} /><circle cx={c[0]} cy={c[1]} r={R} fill="none" stroke={INK} strokeWidth={14} /></Svg> : null,
      };
    }
    case "gutter_wipe": { // T16 a bar of paper with two ink edges sweeps; B is behind it. Vertical only.
      const band = t.band ?? 64, down = t.dir !== "up", e = glide(p);
      const yb = down ? -band + e * (FH + band) : FH - e * (FH + band); // bar top
      const mid = yb + band / 2;
      const clip = down ? `inset(0px 0px ${Math.max(0, FH - mid)}px 0px)` : `inset(${Math.max(0, mid)}px 0px 0px 0px)`;
      const ov = p > 0 && p < 1 ? (
        <Svg>
          <rect x={0} y={yb} width={FW} height={band} fill={PAPER} />
          <line x1={0} y1={yb} x2={FW} y2={yb} stroke={INK} strokeWidth={9} /><line x1={0} y1={yb + band} x2={FW} y2={yb + band} stroke={INK} strokeWidth={9} />
        </Svg>
      ) : null;
      return { a: {}, b: p >= 1 ? {} : { clipPath: clip }, overlay: ov };
    }
    case "panel_shatter": // T13 is a panel effect: see doodles.tsx <PanelShatter/> (kit device, unused in this film)
    default:
      return { a: {}, b: {} };
  }
};
