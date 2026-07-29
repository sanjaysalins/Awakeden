#!/bin/bash
# Assemble the 8 POC clips into one 60s video: scale/pad to 1080x1920,
# speed-to-fit (boomerang for scenes needing more time than the raw clip,
# straight speed-up for scenes needing less) each clip to its scene_plan.json
# window, concat, then mux the narration track underneath.
set -e
cd "$(dirname "$0")"
CLIPS=clips
FIT=clips/_fit
mkdir -p "$FIT"

# scene_id native_duration target_duration extend(1)/compress(0)
declare -a ROWS=(
  "01 5.041667 8.0 1"
  "02 4.050000 5.0 1"
  "03 5.041667 14.0 1"
  "04 4.050000 9.0 1"
  "05 5.041667 4.0 0"
  "06 4.050000 7.0 1"
  "07 4.050000 5.0 1"
  "08 4.050000 11.4 1"
)

SCALE="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"

for row in "${ROWS[@]}"; do
  read -r sid native target extend <<< "$row"
  src="$CLIPS/$sid.mp4"
  out="$FIT/$sid.mp4"
  if [ "$extend" = "1" ]; then
    boom_dur=$(awk "BEGIN{print 2*$native}")
    factor=$(awk "BEGIN{print $target/$boom_dur}")
    boom="$FIT/${sid}_boom.mp4"
    # forward + reverse concat (boomerang), no audio
    ffmpeg -y -i "$src" -i "$src" -filter_complex \
      "[1:v]reverse[r];[0:v][r]concat=n=2:v=1:a=0,${SCALE}[v]" \
      -map "[v]" -an "$boom" -loglevel error
    ffmpeg -y -i "$boom" -filter:v "setpts=${factor}*PTS" -an -r 30 "$out" -loglevel error
    rm -f "$boom"
  else
    factor=$(awk "BEGIN{print $target/$native}")
    ffmpeg -y -i "$src" -filter_complex "${SCALE},setpts=${factor}*PTS[v]" -map "[v]" -an -r 30 "$out" -loglevel error
  fi
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")
  echo "[fit] $sid -> ${d}s (target $target)"
done

# concat via demuxer
LIST=$FIT/_list.txt
> "$LIST"
for row in "${ROWS[@]}"; do
  read -r sid _ _ _ <<< "$row"
  echo "file '$sid.mp4'" >> "$LIST"
done
ffmpeg -y -f concat -safe 0 -i "$LIST" -c copy _video_only.mp4 -loglevel error
echo "[concat] -> _video_only.mp4"
vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 _video_only.mp4)
echo "[concat] duration=${vd}s"

NARR="../../PythonProject1/jesus/narration/EW_Thief_POC/v1/narration.mp3"
ffmpeg -y -i _video_only.mp4 -i "$NARR" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest EW_Thief_POC_final.mp4 -loglevel error
echo "[final] -> EW_Thief_POC_final.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 EW_Thief_POC_final.mp4
