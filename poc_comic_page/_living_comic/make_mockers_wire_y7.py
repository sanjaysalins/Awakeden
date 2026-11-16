import json
P="episode_mockers.json"; ep=json.load(open(P,encoding="utf-8"))
B="batches/cluster_01_cross/mockers_words_ps227/visual/"
M={"m01_cross_dying":"clips/golgotha_hill_wide.mp4","m02_leader_shouts":"clips/rulers_sneering.mp4","m03_back_to_david":"clips/david_writing_psalm.mp4",
"m04_psalm_scroll":"clips/psalm_scroll_night.mp4","m05_passersby":"clips/wagging_heads_close_v4.mp4","m06_come_down":"clips/crowd_mocking.mp4",
"m07_he_stayed":"clips/face_on_cross.mp4","m08_forgive":"clips/jesus_looks_down.mp4","m09_he_died":"clips/ninth_hour_darkness.mp4","m10_landing":"clips/us_under_cross_shadow.mp4"}
for p in ep["panels"]: p["clip_src"]=B+M[p["id"]]; p["status"]="clip wired"
ep["status"]="Y7 words + recording + clips wired; composing"
ep["output"]="poc_comic_page/_living_comic/out/the_mockers_y7.mp4"
json.dump(ep,open(P,"w",encoding="utf-8"),indent=1)
