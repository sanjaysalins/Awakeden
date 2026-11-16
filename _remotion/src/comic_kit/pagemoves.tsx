// comic_kit/pagemoves.tsx - page moves (gutter_shift, panel_join, page_settle) + the split page used by T7 ink_slash_split.
// panel_join and page_settle are `Move` kinds evaluated by layouts.panelState(); gutter_shift is evaluated here (SplitScene).
import React from "react";
import { BONE, FH, FW, INK, InkStroke, PanelSpec, Pt, SceneSpec, clamp, glide, lerp, outCubic, prog, wedgePts, Poly } from "./core";
import { PaperBg, ShotVideo } from "./layouts";

export const gutterShiftDx = (scene: SceneSpec, f: number) => {
  let dx = 0;
  for (const s of scene.shifts || []) dx += (s.dx as number) * glide(prog(f, s.at, s.frames ?? 8));
  return dx;
};

const filt = (p: PanelSpec, f: number) => {
  if (!p.filter) return undefined;
  const k = prog(f, p.filter.f0, p.filter.f1 - p.filter.f0);
  return `brightness(${lerp(1, p.filter.brightness, k)}) saturate(${lerp(1, p.filter.saturate, k)})`;
};

/** Two live pictures on one page, split by a slanted gutter. panels[0] = left, panels[1] = right. */
export const SplitScene: React.FC<{ scene: SceneSpec; f: number; style?: React.CSSProperties; assets: string }> = ({ scene, f, style, assets }) => {
  const [L, R] = scene.panels;
  const sl = scene.slash as { p0: Pt; p1: Pt; width: number; gutter: number; frames: number };
  const k = f - scene.f0, dx = gutterShiftDx(scene, f);
  const xl = (y: number) => sl.p0[0] + ((sl.p1[0] - sl.p0[0]) * y) / FH + dx;
  const drawn = prog(k, 0, Math.round(sl.frames / 2)); // stroke draws top to bottom
  const open = prog(k, Math.round(sl.frames / 2), Math.round(sl.frames / 2));
  const g = k < sl.frames / 2 ? 0 : lerp(sl.width, sl.gutter, glide(open));
  const m = (scene.margin as number) || 0, lo = m, hi = FW - m, cl = (x: number) => Math.max(lo, Math.min(hi, x));
  const leftPoly = k < sl.frames / 2 ? `${lo}px ${m}px,${hi}px ${m}px,${hi}px ${FH - m}px,${lo}px ${FH - m}px` : `${lo}px ${m}px,${cl(xl(m) - g / 2)}px ${m}px,${cl(xl(FH - m) - g / 2)}px ${FH - m}px,${lo}px ${FH - m}px`;
  const rightPoly = `${cl(xl(m) + g / 2)}px ${m}px,${hi}px ${m}px,${hi}px ${FH - m}px,${cl(xl(FH - m) + g / 2)}px ${FH - m}px`;
  const lw = Math.min(cl(xl(m) - g / 2), cl(xl(FH - m) - g / 2)) - lo, rw = hi - Math.max(cl(xl(m) + g / 2), cl(xl(FH - m) + g / 2));
  const poly = (pts: string) => pts.split(",").map((q) => q.replace(/px/g, "").split(" ").map(Number) as Pt);
  const tx = (1 - outCubic(open)) * 340;
  const hatch = scene.hatch as { at: number; frames: number; pitch: number; opacity: number } | undefined;
  const hk = hatch ? prog(f, hatch.at, hatch.frames) * hatch.opacity : 0;
  const lines: React.ReactNode[] = [];
  if (hk > 0) for (let c = -FH; c < FW + FH; c += hatch!.pitch) lines.push(<line key={c} x1={c} y1={0} x2={c - FH} y2={FH} stroke={INK} strokeWidth={5} />);
  const edgeL: Pt[] = [[xl(0) - g / 2, -10], [xl(FH) - g / 2, FH + 10]], edgeR: Pt[] = [[xl(0) + g / 2, -10], [xl(FH) + g / 2, FH + 10]];
  // the brush slash itself while it draws (84 px, ink)
  const yd = drawn * FH;
  const brush = k < sl.frames / 2 + 1 ? wedgePts([0, 0], 0, 0, 0, 0) : null;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, overflow: "hidden", ...style }}>
      <PaperBg />
      <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, clipPath: `polygon(${leftPoly})`, filter: filt(L, f) }}>
        <ShotVideo shot={L.shot} box={[0, 0, FW, FH]} f={f} mount={L.mount ?? scene.f0} assets={assets} />
        {hk > 0 && <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0, opacity: hk }}>{lines}</svg>}
      </div>
      {k >= sl.frames / 2 && (
        <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, clipPath: `polygon(${rightPoly})` }}>
          <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, transform: `translateX(${tx}px)`, filter: filt(R, f) }}>
            <ShotVideo shot={R.shot} box={[0, 0, FW, FH]} f={f} mount={R.mount ?? scene.f0} assets={assets} />
          </div>
        </div>
      )}
      <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0 }}>
        {k < sl.frames / 2 + 1 && drawn > 0 && (
          <g clipPath="url(#slashclip)">
            <clipPath id="slashclip"><rect x={0} y={0} width={FW} height={Math.max(2, yd)} /></clipPath>
            <line x1={sl.p0[0]} y1={sl.p0[1]} x2={sl.p1[0]} y2={sl.p1[1]} stroke={BONE} strokeWidth={sl.width + 16} />
            <line x1={sl.p0[0]} y1={sl.p0[1]} x2={sl.p1[0]} y2={sl.p1[1]} stroke={INK} strokeWidth={sl.width} />
          </g>
        )}
        {m > 0 && k >= sl.frames / 2 && lw > 24 && <InkStroke pts={poly(leftPoly)} close width={9} seed={11} f={f} boil />}
        {m > 0 && k >= sl.frames / 2 && rw > 24 && <InkStroke pts={poly(rightPoly)} close width={9} seed={12} f={f} boil />}
        {m > 0 && k < sl.frames / 2 && <InkStroke pts={poly(leftPoly)} close width={9} seed={11} f={f} boil />}
        {m === 0 && k >= sl.frames / 2 && g > 0 && xl(FH) - g / 2 > -40 && <InkStroke pts={edgeL} width={9} seed={11} f={f} boil />}
        {m === 0 && k >= sl.frames / 2 && g > 0 && xl(0) + g / 2 < FW + 40 && <InkStroke pts={edgeR} width={9} seed={12} f={f} boil />}
      </svg>
    </div>
  );
};
