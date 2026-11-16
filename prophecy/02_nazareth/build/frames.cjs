// frames.cjs <outdir> f1 f2 ... : headless still renders of ThiefComic at given frames (one bundle). Low concurrency.
const { createRequire } = require("module");
const req = createRequire("F:/slk/PycharmProjects/JesusInTheBible/_remotion/package.json");
const { bundle } = req("@remotion/bundler"); const { renderStill, selectComposition } = req("@remotion/renderer");
const path = require("path");
(async () => {
  const out = process.argv[2], frames = process.argv.slice(3).map(Number);
  const root = "F:/slk/PycharmProjects/JesusInTheBible/_remotion";
  const bundled = await bundle({ entryPoint: path.join(root, "src/index.ts"), publicDir: path.join(root, "public") });
  const inputProps = { episode: JSON.parse(require("fs").readFileSync(process.env.EP, "utf8")), marks: !!process.env.MARKS };
  const comp = await selectComposition({ serveUrl: bundled, id: process.env.COMP || "NazarethComic", inputProps });
  for (const f of frames) {
    await renderStill({ composition: comp, serveUrl: bundled, inputProps, frame: f, output: path.join(out, (process.env.MARKS ? "m" : "f") + String(f).padStart(4, "0") + ".png"), imageFormat: "png", chromiumOptions: { gl: "angle" }, timeoutInMS: 120000 });
    console.log("frame", f);
  }
  process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });
