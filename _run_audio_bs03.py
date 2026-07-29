import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import handoff

v1 = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\47_Lifted_Up_in_Shame,_Lifted_Up_in_Glory\v1")
code = handoff.run_audio_pipeline(v1, enforce_lock=True)
print(f"AUDIO PIPELINE EXIT CODE: {code}")
sys.exit(code)
