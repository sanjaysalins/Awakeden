// usage: node qc_stills.mjs <outDir> <debug 0|1> <frame> <frame> ...
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
import fs from "node:fs";
const [outDir, debug, ...frames] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const inputProps = { debug: debug === "1" };
const comp = await selectComposition({ serveUrl, id: "WomanWellV2", inputProps });
for (const fr of frames) {
  await renderStill({ composition: comp, serveUrl, output: path.join(outDir, `f${String(fr).padStart(4, "0")}.jpg`), frame: Number(fr), inputProps, imageFormat: "jpeg", jpegQuality: 90 });
  console.log("ok", fr);
}
process.exit(0);
