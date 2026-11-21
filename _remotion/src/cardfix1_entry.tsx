// cardfix1 entry (own root, so the shared Root.tsx is untouched). Render: npx remotion render src/cardfix1_entry.tsx MaryMarthaV4CF out.mp4 --frames=0-178
import React from "react";
import { Composition, registerRoot } from "remotion";
import { MaryMarthaV4, MM4_FRAMES, MM_FPS } from "./MaryMarthaV4_cardfix1";
const Root: React.FC = () => (
  <Composition id="MaryMarthaV4CF" component={MaryMarthaV4} durationInFrames={MM4_FRAMES} fps={MM_FPS} width={1080} height={1920} />
);
registerRoot(Root);
