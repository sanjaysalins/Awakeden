#!/bin/bash
# Fit segments 2-8 to their real narration windows: trim shared transition
# edges, boomerang N times if the target is much longer than the source
# (avoids an unnaturally slow single-direction stretch), then a mild setpts
# stretch to hit the exact target, scaled/padded to 1080x1920 throughout.
set -e
cd "$(dirname "$0")/clips"
OUT=_full
SCALE="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"

fit() {
  local src=$1 out=$2 trim_start=$3 trim_end=$4 cycles=$5 target=$6
  local dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
  local start=0; local length=$dur
  if [ "$trim_start" = "1" ]; then start=0.9; length=$(awk "BEGIN{print $length-0.9}"); fi
  if [ "$trim_end" = "1" ]; then length=$(awk "BEGIN{print $length-0.9}"); fi
  local base="$OUT/${out%.mp4}_base.mp4"
  ffmpeg -y -ss $start -i "$src" -t $length -vf "$SCALE" -an -c:v libx264 -pix_fmt yuv420p -r 30 "$base" -loglevel error
  local work="$base"
  for i in $(seq 1 $cycles); do
    local nxt="$OUT/${out%.mp4}_b${i}.mp4"
    ffmpeg -y -i "$work" -i "$work" -filter_complex "[1:v]reverse[r];[0:v][r]concat=n=2:v=1:a=0[v]" -map "[v]" -an "$nxt" -loglevel error
    work="$nxt"
  done
  local cur_dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$work")
  local factor=$(awk "BEGIN{print $target/$cur_dur}")
  ffmpeg -y -i "$work" -filter:v "setpts=${factor}*PTS" -an -r 30 "$OUT/$out" -loglevel error
  local final=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$out")
  echo "[fit] $out -> ${final}s (target $target, cycles=$cycles)"
}

fit 02.mp4                    02_fit.mp4 1 1 1 5.0
fit 03.mp4                    03_fit.mp4 1 1 2 14.0
fit 04.mp4                    04_fit.mp4 1 1 2 9.0
fit _camera_variety/05_pullback.mp4  05_fit.mp4 1 1 0 4.0
fit _camera_variety/06_tracking.mp4  06_fit.mp4 1 1 1 7.0
fit _grid/parallax_07.mp4     07_fit.mp4 1 1 0 5.0
fit _grid/08_boomerang.mp4    08_fit.mp4 1 0 0 11.4
