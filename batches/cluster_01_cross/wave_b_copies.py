"""Wave B $0 sibling copies: QC-PASSED Wave A living-light clips -> Wave B pieces whose
stills are byte-identical and whose living_light entries carry the identical text (same
template prompt -> same clip_src_hash). Refuses (reports RENDER) on any mismatch."""
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
from run_piece import clip_src_hash, load_piece, animate_prompts  # noqa: E402

C1 = ROOT / "batches" / "cluster_01_cross"
COPIES = [
    ("it_is_finished_john1930", "forsaken_cry_ps221", "cross_at_dawn"),
    ("it_is_finished_john1930", "i_thirst_john1928", "cross_at_dawn"),
    ("it_is_finished_john1930", "into_thy_hands_luke2346", "cross_at_dawn"),
    ("pierced_zech1210", "forsaken_cry_ps221", "grace_poured_sky"),
    # Wave C
    ("pierced_zech1210", "woman_behold_john1926", "risen_mercy_hand"),
    ("pierced_zech1210", "thirty_pieces_zech11", "risen_mercy_hand"),
]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


for src_name, dst_name, slug in COPIES:
    src, dst = C1 / src_name, C1 / dst_name
    s_png, d_png = src / "visual" / f"{slug}.png", dst / "visual" / f"{slug}.png"
    if sha256(s_png) != sha256(d_png):
        print(f"RENDER {dst_name}/{slug}: stills differ - no copy")
        continue
    s_prompt = animate_prompts(load_piece(src))[slug]
    d_pj = load_piece(dst)
    d_prompt = animate_prompts(d_pj)[slug]
    if s_prompt != d_prompt:
        print(f"RENDER {dst_name}/{slug}: prompts differ - no copy")
        continue
    clips = dst / "visual" / "clips"
    old = clips / f"{slug}.mp4"
    if old.exists():
        park = clips / "_old_camera_only"
        park.mkdir(exist_ok=True)
        if (park / old.name).exists():
            (park / old.name).unlink()
        shutil.move(old, park / old.name)
    shutil.copy2(src / "visual" / "clips" / f"{slug}.mp4", clips / f"{slug}.mp4")
    an = d_pj["animate"]
    (clips / f"{slug}.src.sha").write_text(
        clip_src_hash(d_png, d_prompt, an.get("duration", 5), an.get("aspect_ratio", "9:16")),
        encoding="utf-8")
    print(f"COPIED {src_name} -> {dst_name}: {slug} ($0, hash-bound)")
