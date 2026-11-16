// comic_kit/layouts.tsx - layouts (page, panel, inset_panel, splash_border) + panel state machine + anchor device.
import React from "react";
import { Freeze, OffthreadVideo, Sequence, staticFile } from "remotion";
import {
  Box, EpCtx, Episode, FH, FW, INK, InkStroke, PAPER, PanelSpec, Pt, SceneSpec, ShotSpec, boilSeed, clamp, glide, lerp, pathD, prog, settle, slam, wobblePts, Move,
} from "./core";

export const FULL: Box = [0, 0, FW, FH];

// ---------- picture window maths (doc: anchor / push) ----------
export const zoomAt = (s: ShotSpec, f: number) => {
  const ff = s.freeze_f != null ? Math.min(f, s.freeze_f) : f;
  return lerp(s.z0, s.z1, clamp((ff - s.f_z0) / Math.max(1, s.f_z1 - s.f_z0)));
};
export const viewOf = (box: Box, s: ShotSpec, f: number) => {
  const z = zoomAt(s, f), c = Math.max(box[2] / FW, box[3] / FH), S = c * z;
  const vw = box[2] / (FW * S), vh = box[3] / (FH * S);
  return { vx: clamp(s.cx - vw / 2, 0, 1 - vw), vy: clamp(s.cy - vh / 2, 0, 1 - vh), S, vw, vh };
};

// ---------- panel state (moves) ----------
export interface PState { box: Box; tilt: number; scale: number; op: number; border: number; shadowK: number }
export const panelState = (scene: SceneSpec, p: PanelSpec, f: number): PState => {
  const moves = (scene.moves || []).filter((m) => m.panel === p.id).sort((a, b) => a.at - b.at);
  const b0 = p.border ?? 9;
  let st: PState = { box: p.box, tilt: p.tilt || 0, scale: 1, op: 1, border: b0, shadowK: b0 > 0 ? 1 : 0 };
  // moves that start from a full-bleed picture
  const fromFull = moves.find((m) => m.kind === "pull_out_to_page" || m.kind === "page_settle");
  if (fromFull && f < fromFull.at) st = { box: FULL, tilt: 0, scale: 1, op: 1, border: 0, shadowK: 0 };
  for (const m of moves) {
    const n = m.frames ?? 10;
    if (m.kind === "panel_slam") {
      if (f < m.at) st = { ...st, op: 0 };
      else st = { ...st, scale: slam(f, m.at) as number };
    } else if (m.kind === "panel_dive" && f >= m.at) {
      const e = glide(prog(f, m.at, n));
      st = { ...st, box: [lerp(st.box[0], 0, e), lerp(st.box[1], 0, e), lerp(st.box[2], FW, e), lerp(st.box[3], FH, e)], tilt: lerp(st.tilt, 0, e), border: lerp(b0, 0, e), shadowK: 1 - e, scale: 1 };
    } else if (m.kind === "pull_out_to_page" && f >= m.at) {
      const e = glide(prog(f, m.at, n)), t = m.box as Box;
      st = { box: [lerp(0, t[0], e), lerp(0, t[1], e), lerp(FW, t[2], e), lerp(FH, t[3], e)], tilt: lerp(0, m.tilt || 0, e), scale: 1, op: 1, border: lerp(0, b0 || 9, e), shadowK: e };
    } else if (m.kind === "panel_join" && f >= m.at) {
      const e = settle(prog(f, m.at, n)), t = m.to_box as Box, a = p.box, arc = (m.arc ?? 150) * Math.sin(Math.PI * e);
      st = { ...st, box: [lerp(a[0], t[0], e), lerp(a[1], t[1], e) - arc, lerp(a[2], t[2], e), lerp(a[3], t[3], e)], tilt: lerp(p.tilt || 0, m.tilt || 0, e) };
    } else if (m.kind === "panel_read" && f >= m.at) {
      // reading INTO a panel: box grows to the full frame, holds, then eases back onto the page
      const a = clamp(glide(prog(f, m.at, n)) - glide(prog(f, m.at + n + (m.hold ?? 20), m.out_frames ?? n)));
      const q = st.box;
      st = { ...st, box: [lerp(q[0], 0, a), lerp(q[1], 0, a), lerp(q[2], FW, a), lerp(q[3], FH, a)], tilt: lerp(st.tilt, 0, a), border: lerp(b0, 0, a), shadowK: 1 - a, scale: 1 };
    } else if (m.kind === "page_settle" && f >= m.at) {
      const e = settle(prog(f, m.at, n));
      st = { box: FULL, tilt: lerp(0, m.tilt ?? -0.7, e), scale: lerp(1, m.scale ?? 0.93, e), op: 1, border: lerp(0, 9, e), shadowK: e };
    }
  }
  return st;
};
export const cameraY = (scene: SceneSpec, f: number) => {
  let ty = 0;
  for (const m of scene.moves || []) if (m.kind === "page_glide" && f >= m.at) ty = -(m.dy as number) * glide(prog(f, m.at, m.frames ?? 10));
  return ty;
};

/** anchor: stick a mark to the picture. `pic` is normalised picture coords (from python matchTemplate track, or a fixed point). */
export const anchorScreen = (ep: Episode, a: { scene: string; panel: string; pic: Pt; track?: string }, f: number): Pt => {
  const sc = ep.scenes.find((s) => s.id === a.scene)!;
  const p = sc.panels.find((q) => q.id === a.panel)!;
  const st = panelState(sc, p, f);
  let pic = a.pic;
  if (a.track && ep.tracks && ep.tracks[a.track]) {
    const T = ep.tracks[a.track];
    pic = T.pts[Math.max(0, Math.min(T.pts.length - 1, f - T.f0))];
  }
  const v = viewOf(st.box, p.shot, f);
  return [st.box[0] + (pic[0] - v.vx) * FW * v.S, st.box[1] + (pic[1] - v.vy) * FH * v.S + cameraY(sc, f)];
};

// ---------- video ----------
export const ShotVideo: React.FC<{ shot: ShotSpec; box: Box; f: number; mount: number; assets: string }> = ({ shot, box, f, mount, assets }) => {
  const { vx, vy, S } = viewOf(box, shot, f);
  const t0 = Math.round(shot.t_in * 30);
  const s0 = shot.f_start - t0; // frame at which source frame 0 plays
  const src = staticFile(`${assets}/${shot.clip}.mp4`);
  const st: React.CSSProperties = { position: "absolute", left: -vx * FW * S, top: -vy * FH * S, width: FW * S, height: FH * S, maxWidth: "none" };
  const fz = shot.freeze_f;
  if (f < s0) {
    // before the shot's own start: hold source frame 0 (never run early)
    return <Sequence from={mount} layout="none"><Freeze frame={0}><OffthreadVideo src={src} muted startFrom={0} style={st} /></Freeze></Sequence>;
  }
  const from = Math.max(mount, s0);
  const startFrom = Math.max(0, t0 + (from - shot.f_start));
  const vid = <OffthreadVideo src={src} muted startFrom={startFrom} style={st} />;
  return (
    <Sequence from={from} layout="none">
      {fz != null ? <Freeze frame={Math.min(f, fz) - from}>{vid}</Freeze> : vid}
    </Sequence>
  );
};

export const PaperBg: React.FC<{ h?: number }> = ({ h = FH }) => (
  <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: h, background: PAPER, backgroundImage: "radial-gradient(circle, rgba(20,16,12,0.13) 2px, transparent 2.6px)", backgroundSize: "20px 20px" }} />
);

const BorderSvg: React.FC<{ w: number; h: number; b: number; seed: number; f: number }> = ({ w, h, b, seed, f }) => {
  if (b < 0.5) return null;
  const q = b / 2;
  return (
    <svg width={w + 40} height={h + 40} style={{ position: "absolute", left: -20, top: -20, overflow: "visible" }}>
      <g transform="translate(20,20)">
        <InkStroke pts={[[q, q], [w - q, q], [w - q, h - q], [q, h - q]]} close width={b} seed={seed} f={f} boil amp={2} />
      </g>
    </svg>
  );
};

/** panel: a live clip cropped into a box. 9 px wobbled ink border, hard ink drop shadow, tilt. */
export const PanelView: React.FC<{ panel: PanelSpec; st: PState; f: number; mount: number; assets: string; seed?: number }> = ({ panel, st, f, mount, assets, seed = 3 }) => {
  if (st.op <= 0 || f < mount || (panel.show && (f < panel.show[0] || f >= panel.show[1]))) return null;
  const [x, y, w, h] = st.box;
  const sh = panel.shadow || [12, 12];
  let filt: string | undefined;
  if (panel.filter) {
    const k = prog(f, panel.filter.f0, panel.filter.f1 - panel.filter.f0);
    filt = `brightness(${lerp(1, panel.filter.brightness, k)}) saturate(${lerp(1, panel.filter.saturate, k)})`;
  }
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, transform: `rotate(${st.tilt}deg) scale(${st.scale})`, opacity: st.op }}>
      {st.shadowK > 0.02 && <div style={{ position: "absolute", left: sh[0] * st.shadowK, top: sh[1] * st.shadowK, width: w, height: h, background: INK }} />}
      <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", filter: filt }}>
        <ShotVideo shot={panel.shot} box={[x, y, w, h]} f={f} mount={mount} assets={assets} />
      </div>
      <BorderSvg w={w} h={h} b={st.border} seed={seed + panel.id.length * 13} f={f} />
    </div>
  );
};
/** inset_panel: a small panel over a full-bleed shot (same as panel; never place over Jesus' face). */
export const InsetPanel = PanelView;

/** splash_border: one static ink border at the frame edge of a full-bleed shot. Does not animate. */
export const SplashBorder: React.FC<{ inset?: number; width?: number }> = ({ inset = 22, width = 10 }) => {
  const a = inset, b = FW - inset, c = FH - inset;
  const pts: Pt[] = [[a, a], [b, a], [b, c], [a, c], [a, a]];
  return (
    <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0 }}>
      <InkStroke pts={pts} width={width} seed={5} tone="two" f={0} amp={2} />
    </svg>
  );
};

/** page: full frame of paper with Ben-Day dots, holding panels (stack scene). */
export const StackScene: React.FC<{ scene: SceneSpec; f: number; style?: React.CSSProperties; assets: string }> = ({ scene, f, style, assets }) => {
  const ty = cameraY(scene, f);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, overflow: "hidden", ...style }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, transform: `translateY(${ty}px)` }}>
        {scene.paper && <PaperBg h={scene.page_h || FH} />}
        {scene.panels
          .map((p) => ({ p, st: panelState(scene, p, f) }))
          .sort((a, b) => (a.st.box[2] * a.st.box[3]) / (a.p.box[2] * a.p.box[3]) - (b.st.box[2] * b.st.box[3]) / (b.p.box[2] * b.p.box[3]))
          .map(({ p, st }) => (
            <PanelView key={p.id} panel={p} st={st} f={f} mount={p.mount ?? scene.f0} assets={assets} />
          ))}
      </div>
      {scene.splash && <SplashBorder inset={scene.splash.inset} width={scene.splash.width} />}
    </div>
  );
};
