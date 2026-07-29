import { Composition } from "remotion";
import { Trailer, TRAILER_FPS, TRAILER_FRAMES } from "./Trailer";
import { PocInk, PocPrint } from "./Poc";
import { PocKineticType, POC_KT_FPS, POC_KT_FRAMES } from "./PocKineticType";
import { EW01Open, EW01Climax, EW01Range, OPEN_FRAMES, CLIMAX_FRAMES, RANGE_FRAMES, FPS } from "./EW01Slices";
import { DnaPocFilm, POC_FRAMES as DNAPOC_FRAMES, POC_FPS as DNAPOC_FPS } from "./DnaPocFilm";
import { DnaTrailerHook, HOOK_FRAMES, HOOK_FPS } from "./DnaTrailerHook";
import { DnaSplashHook, SPLASH_FRAMES, SPLASH_FPS } from "./DnaSplashHook";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Trailer"
        component={Trailer}
        durationInFrames={TRAILER_FRAMES}
        fps={TRAILER_FPS}
        width={1920}
        height={1080}
      />
      <Composition id="PocInk" component={PocInk} durationInFrames={90} fps={30} width={1920} height={1080} />
      <Composition id="PocPrint" component={PocPrint} durationInFrames={60} fps={30} width={1920} height={1080} />
      <Composition id="PocKineticType" component={PocKineticType} durationInFrames={POC_KT_FRAMES} fps={POC_KT_FPS} width={1920} height={1080} />
      <Composition id="EW01Open" component={EW01Open} durationInFrames={OPEN_FRAMES} fps={FPS} width={1920} height={1080} />
      <Composition id="EW01Climax" component={EW01Climax} durationInFrames={CLIMAX_FRAMES} fps={FPS} width={1920} height={1080} />
      <Composition id="EW01Range" component={EW01Range} durationInFrames={RANGE_FRAMES} fps={FPS} width={1920} height={1080} />
      <Composition id="DnaPocFilm" component={DnaPocFilm} durationInFrames={DNAPOC_FRAMES} fps={DNAPOC_FPS} width={1920} height={1080} />
      <Composition id="DnaTrailerHook" component={DnaTrailerHook} durationInFrames={HOOK_FRAMES} fps={HOOK_FPS} width={1920} height={1080} />
      <Composition id="DnaSplashHook" component={DnaSplashHook} durationInFrames={SPLASH_FRAMES} fps={SPLASH_FPS} width={1920} height={1080} />
    </>
  );
};
