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
import { WomanWellV1, WW_FRAMES, WW_FPS } from "./WomanWellV1";
import { WomanWellV2, W2_FRAMES, W2_FPS } from "./WomanWellV2";
import { WomanWellV3, W3_FRAMES, W3_FPS } from "./WomanWellV3";
import { BethlehemAnimatic, BA_FRAMES, BA_FPS } from "./BethlehemAnimatic";
import { BethlehemV1, BV1_FRAMES, BV1_FPS } from "./BethlehemV1";
import { BethlehemV2, BTH2_FRAMES, BTH2_FPS } from "./BethlehemV2";
import { BethlehemV3, BTH3_FRAMES, BTH3_FPS } from "./BethlehemV3";
import { BethlehemV4, BTH4_FRAMES, BTH4_FPS } from "./BethlehemV4";
import { BethlehemV5, BTH5_FRAMES, BTH5_FPS } from "./BethlehemV5";
import { BethlehemV6Test, BTH6T_FRAMES, BTH6T_FPS } from "./BethlehemV6Test";
import { BethlehemV6, BTH6_FRAMES, BTH6_FPS } from "./BethlehemV6";
import { BethlehemV8, BTH8_FRAMES, BTH8_FPS } from "./BethlehemV8";
import { BethlehemV9, BTH9_FRAMES, BTH9_FPS } from "./BethlehemV9";
import { ImmanuelV2, IMM_FRAMES, IMM_FPS } from "./ImmanuelV2";
import { BartimaeusV1, BV_FRAMES, BV_FPS } from "./BartimaeusV1";
import { BartimaeusV2, BV2_FRAMES, BV2_FPS } from "./BartimaeusV2";
import { ThiefComic, THIEF_FRAMES, THIEF_FPS, thiefDefaults } from "./ThiefComic";
import { NazarethComic, NAZARETH_FRAMES, NAZARETH_FPS, nazarethDefaults } from "./NazarethComic";
import { NazarethComicV2, NAZARETH2_FRAMES, NAZARETH2_FPS, nazareth2Defaults } from "./NazarethComicV2";
import { NazarethComicV3, NAZARETH3_FRAMES, NAZARETH3_FPS, nazareth3Defaults } from "./NazarethComicV3";
import { NazarethComicV4, NAZARETH4_FRAMES, NAZARETH4_FPS, nazareth4Defaults } from "./NazarethComicV4";
import { NazarethComicV5, NAZARETH5_FRAMES, NAZARETH5_FPS, nazareth5Defaults } from "./NazarethComicV5";
import { NazarethComicV6, NAZARETH6_FRAMES, NAZARETH6_FPS, nazareth6Defaults } from "./NazarethComicV6";
import { UpliftFilm } from "./UpliftFilm";

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
      <Composition id="WomanWellV1" component={WomanWellV1} durationInFrames={WW_FRAMES} fps={WW_FPS} width={1080} height={1920} />
      <Composition id="WomanWellV2" component={WomanWellV2} durationInFrames={W2_FRAMES} fps={W2_FPS} width={1080} height={1920} defaultProps={{ debug: false }} />
      <Composition id="WomanWellV3" component={WomanWellV3} durationInFrames={W3_FRAMES} fps={W3_FPS} width={1080} height={1920} defaultProps={{ debug: false }} />
      <Composition id="BethlehemAnimatic" component={BethlehemAnimatic} durationInFrames={BA_FRAMES} fps={BA_FPS} width={1080} height={1920} defaultProps={{ safe: false, hud: true }} />
      <Composition id="BethlehemV1" component={BethlehemV1} durationInFrames={BV1_FRAMES} fps={BV1_FPS} width={1080} height={1920} defaultProps={{ hud: false }} />
      <Composition id="BethlehemV2" component={BethlehemV2} durationInFrames={BTH2_FRAMES} fps={BTH2_FPS} width={1080} height={1920} defaultProps={{ hud: false }} />
      <Composition id="BethlehemV3" component={BethlehemV3} durationInFrames={BTH3_FRAMES} fps={BTH3_FPS} width={1080} height={1920} defaultProps={{ hud: false }} />
      <Composition id="BethlehemV4" component={BethlehemV4} durationInFrames={BTH4_FRAMES} fps={BTH4_FPS} width={1080} height={1920} defaultProps={{ hud: false }} />
      <Composition id="BethlehemV5" component={BethlehemV5} durationInFrames={BTH5_FRAMES} fps={BTH5_FPS} width={1080} height={1920} defaultProps={{ hud: false }} />
      <Composition id="BTH6-TEST" component={BethlehemV6Test} durationInFrames={BTH6T_FRAMES} fps={BTH6T_FPS} width={1080} height={1920} />
      <Composition id="BethlehemV6" component={BethlehemV6} durationInFrames={BTH6_FRAMES} fps={BTH6_FPS} width={1080} height={1920} />
      <Composition id="BTH8" component={BethlehemV8} durationInFrames={BTH8_FRAMES} fps={BTH8_FPS} width={1080} height={1920} />
      <Composition id="BTH9" component={BethlehemV9} durationInFrames={BTH9_FRAMES} fps={BTH9_FPS} width={1080} height={1920} />
      <Composition id="ImmanuelV2" component={ImmanuelV2} durationInFrames={IMM_FRAMES} fps={IMM_FPS} width={1080} height={1920} />
      <Composition id="BartimaeusV1" component={BartimaeusV1} durationInFrames={BV_FRAMES} fps={BV_FPS} width={1080} height={1920} defaultProps={{ debug: false }} />
      <Composition id="BartimaeusV2" component={BartimaeusV2} durationInFrames={BV2_FRAMES} fps={BV2_FPS} width={1080} height={1920} defaultProps={{ debug: false }} />
      <Composition id="ThiefComic" component={ThiefComic} durationInFrames={THIEF_FRAMES} fps={THIEF_FPS} width={1080} height={1920} defaultProps={thiefDefaults} />
      <Composition id="NazarethComic" component={NazarethComic} durationInFrames={NAZARETH_FRAMES} fps={NAZARETH_FPS} width={1080} height={1920} defaultProps={nazarethDefaults} />
      <Composition id="NazarethComicV2" component={NazarethComicV2} durationInFrames={NAZARETH2_FRAMES} fps={NAZARETH2_FPS} width={1080} height={1920} defaultProps={nazareth2Defaults} />
      <Composition id="NazarethComicV3" component={NazarethComicV3} durationInFrames={NAZARETH3_FRAMES} fps={NAZARETH3_FPS} width={1080} height={1920} defaultProps={nazareth3Defaults} />
      <Composition id="NazarethComicV4" component={NazarethComicV4} durationInFrames={NAZARETH4_FRAMES} fps={NAZARETH4_FPS} width={1080} height={1920} defaultProps={nazareth4Defaults} />
      <Composition id="NazarethComicV5" component={NazarethComicV5} durationInFrames={NAZARETH5_FRAMES} fps={NAZARETH5_FPS} width={1080} height={1920} defaultProps={nazareth5Defaults} />
      <Composition id="NazarethComicV6" component={NazarethComicV6} durationInFrames={NAZARETH6_FRAMES} fps={NAZARETH6_FPS} width={1080} height={1920} defaultProps={nazareth6Defaults} />
      <Composition id="UpliftFilm" component={UpliftFilm} durationInFrames={1772} fps={30} width={1080} height={1920} defaultProps={{ film: { src: "uplift/none.mp4", frames: 1772, turns: [], marks: [] } }} calculateMetadata={({ props }) => ({ durationInFrames: props.film.frames })} />
    </>
  );
};
