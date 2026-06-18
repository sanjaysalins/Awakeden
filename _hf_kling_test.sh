#!/usr/bin/env bash
# HF Kling 3.0 hallucination sample test vs direct-Kling.
# Simple gentle-push prompt (NOT the punch-in cut-plan that breaks direct-Kling).
set -u
HF=~/bin/hf.exe
BASE="C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/02_Psalm_22_Song_From_The_Cross/v1/shorts"
OUT="C:/Users/sanjay/PycharmProjects/JesusInTheBible/_hf_test"
mkdir -p "$OUT"
PROMPT="A finished Baroque devotional oil painting, held as a fixed photograph. The ONLY motion is a slow, gentle cinematic camera push-in and a very slight drift across the static image. Nothing inside the painting moves, changes, brightens, bleeds, or appears: every figure, face, hand, and fold of cloth stays completely frozen and unchanged. Subtle, restrained, reverent."

declare -a IMGS=(
  "$BASE/04_Declared_To_The_Brethren/visual/nbp/09_the-wounded-hand-on-the-shoulder.png|04_09_hand"
  "$BASE/06_The_Ends_Of_The_Earth/visual/nbp/01_one-man-alone.png|06_01_face"
)
for item in "${IMGS[@]}"; do
  IFS='|' read -r img tag <<< "$item"
  echo "=== HF KLING TEST: $tag ==="
  blob=$("$HF" generate create kling3_0 --start-image "$img" --prompt "$PROMPT" \
        --duration 5 --mode std --sound off --aspect_ratio 9:16 --wait 2>&1)
  echo "$blob" | tail -8
  url=$(echo "$blob" | grep -oiE 'https?://[^ "]+\.mp4' | head -1)
  if [ -n "$url" ]; then
    curl -s -L "$url" -o "$OUT/${tag}_HF.mp4" && echo "SAVED $OUT/${tag}_HF.mp4"
  else
    echo "NO MP4 URL for $tag (NSFW block or error)"
  fi
done
echo "=== DONE ==="
