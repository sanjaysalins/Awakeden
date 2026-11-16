#!/bin/bash
# usage: sheet.sh out.jpg cols width file1 file2 ...
out=$1; cols=$2; w=$3; shift 3
n=$#; args=(); fl=""; i=0
for f in "$@"; do args+=(-i "$f"); fl+="[$i:v]scale=$w:-1[s$i];"; i=$((i+1)); done
ins=""; for ((k=0;k<n;k++)); do ins+="[s$k]"; done
rows=$(( (n+cols-1)/cols ))
ffmpeg -y -loglevel error "${args[@]}" -filter_complex "${fl}${ins}xstack=inputs=$n:layout=$(for ((k=0;k<n;k++)); do c=$((k%cols)); r=$((k/cols)); echo -n "$((c*w))_$((r*w*16/9))|"; done | sed 's/|$//'):fill=black" -frames:v 1 -q:v 3 "$out"
