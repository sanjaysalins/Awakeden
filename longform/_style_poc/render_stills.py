"""Phase 1 stills bake-off: 3 looks x 3 beats = 9 stills (gpt_image_2, 9:16).
Reuses the proven HFProvider pattern: subprocess `hf generate create --wait`,
scrape image URL from stdout, download via urllib. Scratchpad only."""
import re, subprocess, urllib.request, json, sys
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
MODEL = "gpt_image_2"
ASPECT = "9:16"
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
OUT = Path(__file__).parent / "stills"
OUT.mkdir(parents=True, exist_ok=True)

ANTI_SLOP = ("photographic intent, intentional cinematic lighting, fine filmic grain, "
             "period-accurate ancient Near East and ancient Egypt, no modern objects, "
             "no plastic AI sheen, no waxy skin, no glitter, no over-saturation, "
             "restrained muted palette, masterful composition with negative space")

SHOTS = {
  # ---- A: CINEMATIC REALISM (prestige film still) ----
  "A_realism_M1_pit": "Cinematic anamorphic film still, 2.39:1 mood: a young Hebrew man cast down into a dry desert pit, shot looking down from the rim, a hard shaft of noon light and falling dust, a torn coat of many colours crumpled beside him, distant out-of-focus silhouettes of brothers turning away. Harsh naturalistic sun, deep shadow, 35mm grain, desaturated. " + ANTI_SLOP,
  "A_realism_M2_bread": "Cinematic anamorphic film still: gaunt road-worn brothers kneeling and bowing very low on the stone floor of a vast Egyptian granary hall, hands outstretched begging for grain, a tall robed Egyptian ruler standing above them in shadow with his face unseen, dusty shafts of light from high windows, sacks of grain. Warm low light, 35mm grain. " + ANTI_SLOP,
  "A_realism_M3_christ": "Cinematic anamorphic film still: a solitary robed figure on a bare hill at dawn seen from behind in silhouette, arms thrown wide open, soft rim light breaking through parting storm clouds, vast empty landscape, reverent and restrained, the figure not glowing. Face not shown. 35mm grain. " + ANTI_SLOP,
  # ---- B: DORE ENGRAVING ----
  "B_engraving_M1_pit": "Gustave Dore steel engraving, fine dense cross-hatching, high-contrast black ink on aged sepia paper, antique illustrated-Bible book plate: a young man cast into a deep desert pit, brothers above turning away, a discarded ornate coat, dramatic etched light rays. Masterful line work, no flat colour fills. " + ANTI_SLOP,
  "B_engraving_M2_bread": "Gustave Dore steel engraving, dense cross-hatching, high-contrast ink on aged sepia paper, antique Bible book plate: starving brothers bowing low before an enthroned Egyptian vizier in a vast pillared granary hall, outstretched begging hands, etched shafts of light. Masterful linework. " + ANTI_SLOP,
  "B_engraving_M3_christ": "Gustave Dore steel engraving, cross-hatched, high-contrast ink on aged sepia paper, antique Bible book plate: a robed Christ figure on a hilltop with arms outstretched wide, radiant broken clouds and etched light rays behind, tiny multitudes far below. Masterful linework. " + ANTI_SLOP,
  # ---- C: ELEMENTAL MACRO ----
  "C_macro_M1_silver": "Extreme macro hyperreal photograph: twenty old silver coins spilling and scattering across cracked desert clay, one coin spinning on its edge catching a blade of hard light, a single coloured thread from a torn garment caught beneath a coin, drifting dust motes. Very shallow depth of field, tactile, cinematic, no faces, symbol of betrayal. " + ANTI_SLOP,
  "C_macro_M2_bread": "Extreme macro hyperreal photograph: a pair of weathered cracked trembling hands cupped open, a single broken loaf of coarse ancient bread being placed into the open palms, golden grain scattered around, warm low side light. Very shallow depth of field, tactile mercy, no faces. " + ANTI_SLOP,
  "C_macro_M3_blood": "Extreme macro hyperreal photograph: a single drop of deep crimson blood falling into clear still water and blooming into soft red tendrils, one warm shaft of light passing through, near-black background. Reverent, tactile, no faces, symbol of His blood, cinematic. " + ANTI_SLOP,
}

def render(name, prompt):
    dest = OUT / f"{name}.png"
    if dest.exists():
        print(f"[skip] {name}", flush=True); return True
    print(f"[gen ] {name} ...", flush=True)
    r = subprocess.run([HF, "generate", "create", MODEL, "--prompt", prompt,
                        "--aspect_ratio", ASPECT, "--wait"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600)
    if r.returncode != 0:
        print(f"[FAIL] {name} rc={r.returncode}\n{(r.stderr or '')[-400:]}", flush=True); return False
    m = URL_RE.search(r.stdout or "")
    if not m:
        print(f"[FAIL] {name} no url\n{(r.stdout or '')[-400:]}", flush=True); return False
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())
    print(f"[ok  ] {name} -> {dest}", flush=True); return True

if __name__ == "__main__":
    ok = 0
    for name, prompt in SHOTS.items():
        try:
            if render(name, prompt): ok += 1
        except Exception as e:
            print(f"[ERR ] {name}: {e}", flush=True)
    print(f"\nDONE {ok}/{len(SHOTS)} stills in {OUT}", flush=True)
