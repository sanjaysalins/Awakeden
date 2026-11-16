// usage: node qc_v6.mjs <outDir> <sec> <sec> ...   (stills of BethlehemV6 at given seconds, 0.35 scale)
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
import fs from "node:fs";
const [outDir, ...secs] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const comp = await selectComposition({ serveUrl, id: "BethlehemV6" });
for (const s of secs) {
  const fr = Math.round(Number(s) * 30);
  await renderStill({ composition: comp, serveUrl, output: path.join(outDir, `s${String(s).replace(".", "_")}.png`), frame: fr, scale: 0.4 });
  console.log("ok", s);
}
process.exit(0);
