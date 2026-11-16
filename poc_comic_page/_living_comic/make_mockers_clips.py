"""4 missing Mockers clips (approved 'A', quoted ~$3-4.50). Motion-only prompts, sound off."""
import subprocess, re, sys, os
V = r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\mockers_words_ps227\visual"
HF = os.path.expanduser("~/bin/hf.exe")
J = [
 ("david_writing_psalm", "seedance1_5", ["--duration","4","--resolution","720p","--aspect_ratio","9:16","--generate_audio","false"],
  "The old king writes slowly by lamplight. The pen moves gently across the page. The lamp flame flickers softly. Slow camera push in. Painted ink style stays exactly the same."),
 ("psalm_scroll_night", "seedance1_5", ["--duration","4","--resolution","720p","--aspect_ratio","9:16","--generate_audio","false"],
  "The lamp flame flickers gently and warm light drifts across the scroll. The scroll and its writing stay still and unchanged. Slow camera push in."),
 ("rulers_sneering", "kling3_0", ["--mode","pro","--sound","off","--duration","5","--aspect_ratio","9:16"],
  "The leaders sneer and one raises a hand to point upward, then holds. Robes sway slightly. Slow camera push in. No new people appear."),
 ("wagging_heads_close", "kling3_0", ["--mode","pro","--sound","off","--duration","5","--aspect_ratio","9:16"],
  "The passers-by shake their heads side to side, slowly, then settle. Slow camera push in. No new people appear. Painted style stays the same."),
]
for name, model, extra, prompt in J:
    out = os.path.join(V, "clips", name + ".mp4")
    if os.path.exists(out): print("skip", name); continue
    cmd = [HF, "generate", "create", model, "--start-image", os.path.join(V, name + ".png"), "--prompt", prompt, "--wait"] + extra
    print("[clip]", name, model, flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + (r.stderr or ""); m = re.search(r"https?://\S+?\.mp4", blob)
    if not m: print("  FAIL", blob[-400:]); continue
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", out], check=True)
    print("  ok", out, os.path.getsize(out), flush=True)
