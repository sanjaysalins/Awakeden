"""Download the 15 v3 stills (OpenArt) and build a contact sheet (p07 north star last)."""
import subprocess, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = "https://cdn.openart.ai/openart-ai/production/2026-11/create-image/EsbOTmkjtrfHKP88sIj3/"
FILES = {
    "sA": "image_1794405986062_bfb5afca_1794405986341_f4b861da.png",
    "p01": "image_1794405991131_1a5409e0_1794405992292_cac9b6ce.png",
    "p02": "image_1794405992892_7463d936_1794405993304_6d67d13a.png",
    "sB": "image_1794405996260_366f1d2d_1794405996843_32360244.png",
    "p03": "image_1794405993803_f6b4f17c_1794405994736_24950686.png",
    "sC": "image_1794405999305_05b0ee75_1794406000352_cedf74d4.png",
    "p04": "image_1794405997144_882db148_1794405998355_642f57dd.png",
    "sD": "image_1794406000130_685ee165_1794406000813_03f13f9a.png",
    "p05": "image_1794406000027_31cdade1_1794406000336_aec7d67a.png",
    "sE": "image_1794406006224_30827859_1794406007369_84f41c2c.png",
    "sF": "image_1794406007160_d594926c_1794406007975_75d51420.png",
    "p06": "image_1794406008823_8db49a87_1794406010010_a5981e11.png",
    "p08": "image_1794406012061_c4784337_1794406013789_96099d49.png",
    "sG": "image_1794406014719_43662670_1794406015873_3b4e9023.png",
    "sH": "image_1794406015874_ca4c4985_1794406016514_ec469f31.png",
}
st = HERE / "stills"; st.mkdir(exist_ok=True)
tmp = HERE / "_tmp"; tmp.mkdir(exist_ok=True)
srcs = []
for n, u in FILES.items():
    p = st / f"{n}.png"
    if not p.exists():
        subprocess.run(["curl", "-s", "-f", "-o", str(p), B + u], check=True)
    srcs.append(p)
srcs.append(HERE.parent / "pictures" / "07_lifts_child.png")
for i, p in enumerate(srcs):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-vf", "scale=300:534,setsar=1", str(tmp / f"t{i}.jpg")], check=True)
args = []
for i in range(16):
    args += ["-i", str(tmp / f"t{i}.jpg")]
fc = "".join(f"[{i}]" for i in range(8)) + "hstack=8[a];" + "".join(f"[{i}]" for i in range(8, 16)) + "hstack=8[b];[a][b]vstack"
subprocess.run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", fc, str(HERE / "sheet_v3.jpg")], check=True)
print("ok", len(srcs))
