#!/usr/bin/env bash
set -u
HF=~/bin/hf.exe
NBP="C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/06_The_Ends_Of_The_Earth/visual/nbp"
OUT="C:/Users/sanjay/PycharmProjects/JesusInTheBible/_hf_test"; mkdir -p "$OUT"
PROMPT="A flat antique oil painting on canvas, filmed as a static art photograph hanging on a wall. The painted figure and every brushstroke are part of the flat canvas and physically cannot move, breathe, sway, or change. Only the CAMERA moves: a punchy cinematic push-in and a hard reframe across the surface of the painting. The body stays absolutely rigid and motionless — no limbs move, no arms move, no swaying, no gestures — exactly like filming a still painting on a wall."
for item in "01_one-man-alone|01_frozen_pro" "03_all-the-ends-of-the-world|03cross_frozen_pro"; do
  IFS='|' read -r stem tag <<< "$item"
  img=$(ls "$NBP/${stem}.png" 2>/dev/null); [ -z "$img" ] && img="$NBP/${stem%%_*}_"*.png
  echo "=== FROZEN PRO TEST: $tag ($stem) ==="
  blob=$("$HF" generate create kling3_0 --start-image "$NBP/${stem}.png" --prompt "$PROMPT" --duration 5 --mode pro --sound off --aspect_ratio 9:16 --wait 2>&1)
  echo "$blob" | tail -4
  url=$(echo "$blob" | grep -oiE 'https?://[^ "]+\.mp4' | head -1)
  [ -n "$url" ] && curl -s -L "$url" -o "$OUT/${tag}.mp4" && echo "SAVED $OUT/${tag}.mp4" || echo "NO URL ($tag)"
done
echo DONE
