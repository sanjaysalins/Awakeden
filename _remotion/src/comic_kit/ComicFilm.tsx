// comic_kit/ComicFilm.tsx - generic renderer: episode.json -> scenes + transitions + doodles + pills. Driven by data only.
import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { EpCtx, Episode, INK, SceneSpec, clamp } from "./core";
import { StackScene } from "./layouts";
import { SplitScene } from "./pagemoves";
import { Fx, transitionFx } from "./transitions";
import { DoodleLayer, shakeOffset } from "./doodles";
import { normalizeEpisode } from "./pages";

const SceneView: React.FC<{ s: SceneSpec; f: number; style?: React.CSSProperties; assets: string }> = ({ s, f, style, assets }) =>
  s.type === "split" ? <SplitScene scene={s} f={f} style={style} assets={assets} /> : <StackScene scene={s} f={f} style={style} assets={assets} />;

const Lettering: React.FC<{ ep: Episode; f: number }> = ({ ep, f }) => {
  const one = (png: string, f0: number, f1: number, key: string) => {
    const op = clamp((f - f0) / 1.2) * clamp((f1 - f) / 1.2);
    if (op <= 0) return null;
    return <Img key={key} src={staticFile(`${ep.assets}/${png}`)} style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, opacity: op }} />;
  };
  return (
    <>
      {ep.hook && one(ep.hook.png, ep.hook.f0, ep.hook.f1, "hook")}
      {ep.pills.map((p, i) => one(p.png, p.f0, p.f1, "p" + i))}
    </>
  );
};

export const ComicFilm: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode: ep0, marks = false, hideKinds }) => {
  const epN: Episode = normalizeEpisode(ep0);
  const ep: Episode = hideKinds && hideKinds.length ? { ...epN, doodles: epN.doodles.filter((d) => !hideKinds.includes(d.kind)) } : epN;
  const f = useCurrentFrame();
  const active = ep.scenes.filter((s) => f >= s.f0 && f < s.f1);
  const ids = new Set(active.map((s) => s.id));
  const run = ep.transitions.filter((t) => f >= t.at && f < t.at + t.frames && ids.has(t.from) && ids.has(t.to));
  const fx = new Map<string, { fx: Fx; role: "a" | "b" }>();
  const overlays: React.ReactNode[] = [];
  const aTop = new Set<string>();
  for (const t of run) {
    const x = transitionFx(t, f);
    fx.set(t.from, { fx: x, role: "a" }); fx.set(t.to, { fx: x, role: "b" });
    if (x.aTop) aTop.add(t.from);
    if (x.overlay) overlays.push(<React.Fragment key={t.kind + t.at}>{x.overlay}</React.Fragment>);
  }
  // draw order: scene order, but an A that is "on top" goes after its B
  const order = [...active];
  for (const id of aTop) { const i = order.findIndex((s) => s.id === id); if (i >= 0) { const [a] = order.splice(i, 1); order.push(a); } }
  const sh = shakeOffset(ep, f);
  return (
    <EpCtx.Provider value={ep}>
      <AbsoluteFill style={{ background: marks ? "#000" : INK }}>
        <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, transform: `translate(${sh[0]}px, ${sh[1]}px)` }}>
          {!marks && order.map((s) => {
            const r = fx.get(s.id);
            if (r && ((r.role === "a" && r.fx.aHidden) || (r.role === "b" && r.fx.bHidden))) return null;
            const style = r ? (r.role === "a" ? r.fx.a : r.fx.b) : undefined;
            return <SceneView key={s.id} s={s} f={f} style={style} assets={ep.assets} />;
          })}
          {overlays}
          <div style={marks ? { position: "absolute", left: 0, top: 0, width: 1080, height: 1920, filter: "brightness(0) invert(1)" } : undefined}><DoodleLayer f={f} /></div>
        </div>
        {!marks && <Lettering ep={ep} f={f} />}
      </AbsoluteFill>
    </EpCtx.Provider>
  );
};
