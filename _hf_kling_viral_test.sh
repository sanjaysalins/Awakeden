#!/usr/bin/env bash
# HF Kling 3.0 with a VIRAL motion prompt (per higgsfield-generate prompt-engineering:
# describe MOTION not the frame, dynamic verbs, positive phrasing, concise).
# Does it morph the hand/face on a punchy edit like direct-Kling does?
set -u
HF=~/bin/hf.exe
BASE="C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/02_Psalm_22_Song_From_The_Cross/v1/shorts"
OUT="C:/Users/sanjay/PycharmProjects/JesusInTheBible/_hf_test"
mkdir -p "$OUT"
# MOTION-ONLY, viral, dynamic camera, frozen subject (positive phrasing, no redescribe)
PROMPT="High-energy viral edit: fast cinematic camera moves over the image — a quick punch-in, a hard snap to a tight close crop, then a fast pull-back to the full frame, restless dynamic reframing. Camera motion only; every figure, face and hand stays perfectly frozen, still and tack-sharp, brushwork unchanged."

declare -a IMGS=(
  "$BASE/04_Declared_To_The_Brethren/visual/nbp/09_the-wounded-hand-on-the-shoulder.png|04_09_hand_HFVIRAL"
  "$BASE/06_The_Ends_Of_The_Earth/visual/nbp/01_one-man-alone.png|06_01_face_HFVIRAL"
)
for item in "${IMGS[@]}"; do
  IFS='|' read -r img tag <<< "$item"
  echo "=== HF KLING VIRAL: $tag ==="
  blob=$("$HF" generate create kling3_0 --start-image "$img" --prompt "$PROMPT" \
        --duration 5 --mode std --sound off --aspect_ratio 9:16 --wait 2>&1)
  echo "$blob" | tail -6
  url=$(echo "$blob" | grep -oiE 'https?://[^ "]+\.mp4' | head -1)
  if [ -n "$url" ]; then
    curl -s -L "$url" -o "$OUT/${tag}.mp4" && echo "SAVED $OUT/${tag}.mp4"
  else
    echo "NO MP4 URL for $tag (NSFW block or error)"
  fi
done
echo "=== DONE ==="
