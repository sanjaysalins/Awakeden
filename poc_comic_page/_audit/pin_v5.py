"""Pin verified v5 hook files as the postable final (backs up any old pin to FINAL_VIDEO.txt.prev_v4)."""
import sys, os, subprocess, shutil
sys.path.insert(0, '.')
import build_upload_tracker as b
from pipeline import release_state as rs
def dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],capture_output=True,text=True).stdout.strip())
for s in rs.gather()[0]:
    if s.slug not in b.V5: continue
    v5 = b.V5[s.slug][0]
    if abs(dur(v5) - dur(s.video)) > 0.05: print(s.slug, 'SKIP duration mismatch'); continue
    pin = s.source_dir / 'FINAL_VIDEO.txt'
    if pin.is_file():
        bk = s.source_dir / 'FINAL_VIDEO.txt.prev_v4'
        if not bk.exists(): shutil.copy2(pin, bk)
    rel = os.path.relpath(v5, s.source_dir).replace(chr(92), '/')
    pin.write_text(rel + chr(10), encoding='utf-8'); print(s.slug, 'pinned')
