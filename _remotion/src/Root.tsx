import { Composition } from "remotion";
import { Trailer, TRAILER_FPS, TRAILER_FRAMES } from "./Trailer";
import { PocInk, PocPrint } from "./Poc";
import { PocKineticType, POC_KT_FPS, POC_KT_FRAMES } from "./PocKineticType";
import { EW01Open, EW01Climax, EW01Range, OPEN_FRAMES, CLIMAX_FRAMES, RANGE_FRAMES, FPS } from "./EW01Slices";
import { DnaPocFilm, POC_FRAMES as DNAPOC_FRAMES, POC_FPS as DNAPOC_FPS } from "./DnaPocFilm";
import { DnaTrailerHook, HOOK_FRAMES, HOOK_FPS } from "./DnaTrailerHook";
import { DnaSplashHook, SPLASH_FRAMES, SPLASH_FPS } from "./DnaSplashHook";
import { TalithaCumi, TC_FRAMES, TC_FPS } from "./TalithaCumi";
import { Ep12Towel, EP12_FRAMES, EP12_FPS } from "./Ep12Towel";
import { Ep16Children, EP16_FRAMES, EP16_FPS } from "./Ep16Children";
import { Ep16ChildrenV2 } from "./Ep16ChildrenV2";
import { ZaccPreview, ZP_FRAMES, ZP_FPS } from "./ZaccPreview";
import { MaryMarthaV1, MM_FRAMES, MM_FPS } from "./MaryMarthaV1";
import { MaryMarthaV2 } from "./MaryMarthaV2";
import { MaryMarthaV3, MM3_FRAMES } from "./MaryMarthaV3";
import { MaryMarthaV4, MM4_FRAMES } from "./MaryMarthaV4";
import { SecondFireV1, SF_FRAMES, SF_FPS } from "./SecondFireV1";

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
      <Composition id="TalithaCumi" component={TalithaCumi} durationInFrames={TC_FRAMES} fps={TC_FPS} width={1080} height={1920} />
      <Composition id="Ep12Towel" component={Ep12Towel} durationInFrames={EP12_FRAMES} fps={EP12_FPS} width={1080} height={1920} />
      <Composition id="Ep16Children" component={Ep16Children} durationInFrames={EP16_FRAMES} fps={EP16_FPS} width={1080} height={1920} />
      <Composition id="Ep16ChildrenV2" component={Ep16ChildrenV2} durationInFrames={EP16_FRAMES} fps={EP16_FPS} width={1080} height={1920} />
      <Composition id="ZaccPreview" component={ZaccPreview} durationInFrames={ZP_FRAMES} fps={ZP_FPS} width={1080} height={1920} />
      <Composition id="MaryMarthaV1" component={MaryMarthaV1} durationInFrames={MM_FRAMES} fps={MM_FPS} width={1080} height={1920} />
      <Composition id="MaryMarthaV2" component={MaryMarthaV2} durationInFrames={MM_FRAMES} fps={MM_FPS} width={1080} height={1920} />
      <Composition id="MaryMarthaV3" component={MaryMarthaV3} durationInFrames={MM3_FRAMES} fps={MM_FPS} width={1080} height={1920} />
      <Composition id="MaryMarthaV4" component={MaryMarthaV4} durationInFrames={MM4_FRAMES} fps={MM_FPS} width={1080} height={1920} />
      <Composition id="SecondFireV1" component={SecondFireV1} durationInFrames={SF_FRAMES} fps={SF_FPS} width={1080} height={1920} defaultProps={{ DENSITY: 1 }} />
    </>
  );
};
