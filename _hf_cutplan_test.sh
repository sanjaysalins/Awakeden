#!/usr/bin/env bash
# Test: VIRAL HARD-CUT cut-plan (not a smooth zoom) on a FROZEN flat painting.
# Goal = the editor jump-cuts between crops of one still; the painting never moves.
set -u
HF=~/bin/hf.exe
NBP="C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/06_The_Ends_Of_The_Earth/visual/nbp"
OUT="C:/Users/sanjay/PycharmProjects/JesusInTheBible/_hf_test"; mkdir -p "$OUT"

BASE="A still finished Baroque oil painting on flat canvas, filmed as a HARD-CUT video edit — like an editor jump-cutting between different crops of ONE frozen painting. The painting itself never moves, breathes, brightens or changes; only the FRAMING jumps. Sequence of HARD CUTS (instant jumps to a new static crop, NOT a smooth zoom, no dissolves): "
TAIL=" Between cuts the image holds perfectly still. No subject motion, no limbs moving, no morphing, no smooth zoom, no dissolve — every crop is the same frozen painting."

# per-clip cut sequences (specific crop targets I picked by looking at each still)
P03="Open on the full crucifixion wide. CUT to a mid framing on the robed crucified figure. CUT to a tight close-up of the face beneath the crown of thorns. CUT to a macro crop of one nailed hand on the crossbeam. CUT to the small crowd and the world horizon below. CUT back to the full wide."
P10="Open on the full tomb wide. CUT to a mid framing on the dark open doorway. CUT to a tight close-up of the great round stone rolled aside. CUT to a macro crop of the folded grave-linen inside the threshold. CUT back to the full wide."

run () { # $1 img stem, $2 seq, $3 tag
  echo "=== CUTPLAN TEST: $3 ==="
  blob=$("$HF" generate create kling3_0 --start-image "$NBP/$1.png" \
        --prompt "$BASE$2$TAIL" --duration 5 --mode pro --sound off --aspect_ratio 9:16 --wait 2>&1)
  echo "$blob" | tail -3
  url=$(echo "$blob" | grep -oiE 'https?://[^ "]+\.mp4' | head -1)
  [ -n "$url" ] && curl -s -L "$url" -o "$OUT/$3.mp4" && echo "SAVED $OUT/$3.mp4" || echo "NO URL ($3)"
}
run "03_all-the-ends-of-the-world" "$P03" "03_cutplan"
run "10_the-empty-tomb"            "$P10" "10_cutplan"
echo DONE
