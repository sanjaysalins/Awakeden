// usage: node qc_bth4.mjs <outDir> <scale> <frame> <frame> ...   (BethlehemV4 check stills; no browser, no studio)
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
import fs from "node:fs";
const [outDir, scale, ...frames] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const inputProps = { hud: false };
const comp = await selectComposition({ serveUrl, id: "BethlehemV4", inputProps });
for (const fr of frames) {
  await renderStill({ composition: comp, serveUrl, output: path.join(outDir, `f${String(fr).padStart(4, "0")}.jpg`), frame: Number(fr), inputProps, imageFormat: "jpeg", jpegQuality: 85, scale: Number(scale) });
}
console.log("done", frames.length);
process.exit(0);
