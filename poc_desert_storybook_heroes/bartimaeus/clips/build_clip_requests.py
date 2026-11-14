"""17 Kling 3 Omni pro i2v requests, sound off (owner yes ~$6.02, 2026-11-14). Writes clip_requests.json."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
KEEP = (" Keep the exact painted gouache storybook look, the same faces, the same clothes and the same number of people as the first frame. "
        "Every person keeps their own body and stays one person. Smooth, gentle, natural motion. Camera steady unless said.")
S = [  # id, resource, seconds, motion
 ("s01","1qSFhJu0zr5Cu8FuYnOL",4,"The blind beggar keeps shouting with all his strength, head back, mouth open, his eyes stay closed the whole time; his reaching hands tremble and stretch forward. Dust drifts in the warm air behind him, blurred travellers' legs pass by. Slow push in toward his face."),
 ("s02","OiLtpwu8cOqUKiL7pMn8",5,"The people in the crowd frown and lean toward the shouting beggar; the man keeps his finger on his lips, the woman waves her hand at him to hush, the stern man leans down closer. The beggar's eyes stay closed. Dust drifts in the warm light."),
 ("s03","mZpk6OiFWBYVrgFgIiwR",5,"Wide calm shot: the stream of travellers walks slowly out of the town gate along the road, palm leaves sway in a light breeze, dust drifts. The small beggar sits still at the roadside, eyes closed. Very slow push in."),
 ("s04","FLDNrflDfv5SIFPSiArQ",5,"The big crowd walks slowly toward the camera along the road, raising soft golden dust; Jesus walks calmly at its centre, a head taller than the rest. Palms sway gently. Camera slowly drifts back as they come."),
 ("s05","op8yIyawpYyR3HVGJwwU",6,"On his knees, the blind man draws a deep breath and shouts even louder through his cupped hands, his back arching higher, his cloak slipping further off one shoulder; his eyes stay closed. Blurred travellers step back. Warm light, dust in the air. Slow push in."),
 ("s06","ujr5MtQOibhwV3eLwFaS",5,"Jesus stands completely still in the middle of the road, calm, listening, only his hair and mantle stir slightly in the breeze. All around him the crowd keeps flowing past on both sides, robes swinging, dust rising through the golden beam of light. Very slow push in toward Jesus."),
 ("s07","Wcno9qU56zpNgMxnXhfC",5,"Jesus looks toward the roadside with kind attention and makes one gentle beckoning motion with his raised hand, then holds it. The two travellers beside him turn and call out toward the roadside. Gentle breeze in robes."),
 ("s08","FKs7VBL3G5XalzbKbErC",5,"The blind man springs up to his feet and steps forward eagerly, one hand reaching ahead, eyes still closed; his thrown rust-brown cloak flies away behind him and falls to the dust. His wooden bowl stays on the ground. Camera follows him slightly."),
 ("s09","b5pGmcXOjkmUN1GlfuBq",4,"Jesus bends a little closer to the blind man, gentle and kind, speaking softly, his open hand steady. The blind man tilts his face up toward the voice, eyes still closed. Crowd softly blurred behind. Slow gentle push in."),
 ("s10","KfiFDlF3pQwiAh1SN8cj",4,"Close-up: the blind man speaks softly with trembling hope, his lips moving, his pressed hands tightening near his chin, a tear running slowly down his cheek; his eyes stay closed the whole time. Warm light. Very slow push in."),
 ("s11","22MyG19UqPDarCfONh5x",5,"Jesus speaks kindly with a soft smile, his hand resting gently on the blind man's shoulder. The blind man listens with his face lifted, eyes still closed, breathing in. Breeze moves their robes, dust glows in the golden light behind."),
 ("s12","iTuFfnmtAOf12vngB6Ns",7,"His eyes are already open and they stay wide open the whole time, never closing: he gazes up at Jesus in amazement, his face slowly breaking into a huge joyful smile, tears shining, his eyebrows lifting. Warm light grows gently brighter on his face. Very slow push in."),
 ("s13","ITmhfuL2noBkHW8Wwu1l",5,"Everyone walks slowly away from the camera up the road. Jesus walks ahead in the middle of the crowd, his back to us. The man in the tan tunic walks after him, gladly looking around, then ahead at Jesus. Long shadows, dust. Camera follows slowly behind them."),
 ("s14","EkgZ88JUNedH4avlwI4u",6,"Very wide landscape: the tiny figures walk slowly up the winding road toward the city on the hill; clouds drift slowly across the warm sky, light haze moves over the hills. The city and temple stay exactly as they are. Very slow push in toward the city."),
 ("s15","8AEbxajn8H8Cir9H9zZN",4,"Silent reverent shot: the plain wooden cross stands still on the hill; only the dusk clouds drift slowly across the orange and teal sky and the light slowly fades. No people. Very slow push in."),
 ("s16","GWISSZenmufVlcOf3RrU",4,"The empty tomb in a garden at sunrise: warm golden morning light slowly grows brighter, pouring out of the open doorway across the ground; leaves and grass stir gently in the breeze. The doorway, the rock and the folded cloth stay exactly as they are. Camera calm and steady."),
 ("s17","hhUcsD2bfxFxZsgQQqcX",7,"Jesus and the man walk slowly side by side along the road toward the hills, away from the camera; the man looks up at Jesus, Jesus looks down at him with a warm smile. Long golden shadows, glowing sunset sky, the small crowd far ahead. Camera slowly follows behind them."),
]
reqs = [{"model": "kling-3-omni", "mode": "image2video", "params": {"resolution": "pro", "duration": d, "generateSound": False, "videoCount": 1,
         "startFrame": {"type": "image", "id": "resource:" + r, "label": sid}, "prompt": m + KEEP}} for sid, r, d, m in S]
(H / "clip_requests.json").write_text(json.dumps({"ids": [s[0] for s in S], "requests": reqs}, indent=1), encoding="utf-8")
print(len(reqs), "clips,", sum(s[2] for s in S), "s,", sum(s[2] for s in S) * 35, "cr")
