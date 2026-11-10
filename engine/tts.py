"""Genera la voz con ElevenLabs (con tiempos por caracter) y calcula los tiempos de cada escena.
Uso: python3 engine/tts.py episodes/<id>        (necesita ELEVENLABS_API_KEY en el entorno)
Escribe voice.mp3 y timing.json dentro de la carpeta del episodio.
"""
import base64, json, os, re, sys, urllib.request

VOICE = "HIYif4jehvc9P9A8DYbX"  # Pablo - voz masculina, grave y segura (español peninsular)
SETTINGS = dict(stability=0.4, similarity_boost=0.8, style=0.35, use_speaker_boost=True, speed=1.06)

ep = sys.argv[1]
script = json.load(open(os.path.join(ep, "script.json")))
says = [s["say"].strip() for s in script["scenes"]]
text = " ".join(says)

key = os.environ["ELEVENLABS_API_KEY"]
voice = script.get("voice_id", VOICE)
body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                   "voice_settings": SETTINGS, "language_code": "es"}).encode()
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
                             data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=180))
open(os.path.join(ep, "voice.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
al = d["alignment"]
chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
assert "".join(chars) == text, "alignment mismatch"

scenes, pos = [], 0
for s in says:
    a, b = pos, pos + len(s)
    words = [(m.group(0), st[a + m.start()]) for m in re.finditer(r"[\wáéíóúñü]+", s, re.I)]
    scenes.append({"start": st[a], "end_speech": en[b - 1], "words": words})
    pos = b + 1
for i, sc in enumerate(scenes):
    sc["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else sc["end_speech"] + 1.8
json.dump({"scenes": scenes, "duration": scenes[-1]["end"]}, open(os.path.join(ep, "timing.json"), "w"), ensure_ascii=False, indent=1)
print(f"voz ok · {len(text)} caracteres · {scenes[-1]['end']:.1f}s")
