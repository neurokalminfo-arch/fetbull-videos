"""Música original generada por código + efectos + voz -> mix.wav
Uso: python3 engine/audio.py episodes/<id>
Lee voice.mp3, timing.json y script.json ("music": {"bpm":124,"key":"A","mood":"dark"} opcional).
Sin samples externos: todo se sintetiza aquí, así que no hay problemas de derechos.
"""
import json, os, subprocess, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

SR = 44100
LEAD = 0.3  # mismo desfase que render.js
ep = sys.argv[1]
script = json.load(open(os.path.join(ep, "script.json")))
timing = json.load(open(os.path.join(ep, "timing.json")))
dur = timing["duration"] + LEAD
N = int(dur * SR) + SR
rng = np.random.default_rng(abs(hash(script.get("topic", ""))) % 2**32)

def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def lp(x, f): b, a = butter(2, f / (SR / 2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f / (SR / 2), "high"); return lfilter(b, a, x)
def add(buf, x, t):
    i = int(t * SR)
    if i < 0: x, i = x[-i:], 0
    n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n]

m = script.get("music", {})
bpm = m.get("bpm", 124)
beat = 60 / bpm
roots = {"A": 55.0, "C": 65.41, "D": 73.42, "E": 41.2, "G": 49.0, "F": 43.65}[m.get("key", "A")]
# progresion menor i - VI - III - VII
prog = [0, -4, 3, -2]
minor = [0, 3, 7, 10, 12]

# --- instrumentos ---
def kick():
    t = np.arange(int(0.35 * SR)) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.95
def clap():
    t = np.arange(int(0.22 * SR)) / SR
    n = bp(rng.standard_normal(len(t)), 900, 4500)
    env = np.exp(-t * 22) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0) * (t < 0.03))
    return n * env * 0.5
def hat(open_=False):
    t = np.arange(int((0.18 if open_ else 0.05) * SR)) / SR
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * (18 if open_ else 70)) * 0.22
def bass(freq, length):
    t = np.arange(int(length * SR)) / SR
    saw = 2 * ((freq * t) % 1) - 1
    x = 0.6 * np.sin(2 * np.pi * freq * t) + 0.35 * lp(saw, 380)
    return x * np.minimum(1, t * 80) * np.minimum(1, (length - t) * 40) * 0.55
def pluck(freq, length=0.22):
    t = np.arange(int(length * SR)) / SR
    x = sum(np.sign(np.sin(2 * np.pi * freq * h * t)) / h for h in (1, 2))
    return lp(x, 2600) * np.exp(-t * 14) * 0.12
def pad(freqs, length):
    t = np.arange(int(length * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.3 * t)) for f in freqs)
    return lp(x, 1200) * np.minimum(1, t * 3) * np.minimum(1, (length - t) * 3) * 0.05

music = np.zeros(N)
side = np.ones(N)  # bombeo tipo sidechain
nbeats = int(dur / beat) + 2
k, c, h = kick(), clap(), hat()
for b in range(nbeats):
    t = b * beat
    bar, pos = divmod(b, 4)
    add(music, k, t)
    i = int(t * SR); L = int(0.22 * SR)
    if i < N: side[i:i + L] = np.minimum(side[i:i + L], 0.35 + 0.65 * np.linspace(0, 1, len(side[i:i + L])) ** 0.7)
    if pos in (1, 3): add(music, c, t)
    add(music, h, t + beat / 2)
    if b % 2: add(music, hat(True) * 0.6, t + beat * 0.75)
    root = roots * 2 ** (prog[bar % 4] / 12)
    if pos == 0:
        add(music, pad([root * 4, root * 4 * 2 ** (3 / 12), root * 4 * 2 ** (7 / 12)], beat * 4), t)
    add(music, bass(root, beat * 0.45), t + beat / 2)
    for s in range(2):  # arpegio en semicorcheas alternas
        add(music, pluck(root * 8 * 2 ** (minor[(b * 2 + s) % 5] / 12)), t + s * beat / 2 + beat / 4)
music *= side
# corte de energia antes de la ultima escena y vuelta (efecto "drop")
last = timing["scenes"][-1]["start"] + LEAD
i0, i1 = int((last - 0.55) * SR), int(last * SR)
music[i0:i1] *= np.linspace(1, 0.15, i1 - i0)

# --- efectos ---
fx = np.zeros(N)
def whoosh(length=0.45, up=True):
    t = np.arange(int(length * SR)) / SR
    n = rng.standard_normal(len(t))
    p = t / length if up else 1 - t / length  # barrido de grave a agudo
    out = bp(n, 200, 900) * (1 - p) + bp(n, 1500, 7000) * p
    env = np.sin(np.pi * t / length) ** 2
    return out * env * 0.5
def impact():
    t = np.arange(int(0.9 * SR)) / SR
    boom = np.sin(2 * np.pi * np.cumsum(35 + 80 * np.exp(-t * 12)) / SR) * np.exp(-t * 4)
    crack = hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 30) * 0.3
    return (boom + crack) * 0.8
add(fx, impact(), LEAD + 0.05)
for sc in timing["scenes"][1:]:
    add(fx, whoosh(), sc["start"] + LEAD - 0.3)
for t in script.get("sfx_hits", []):  # golpes extra opcionales (segundos de voz)
    add(fx, clap() * 1.5, t + LEAD)

# --- voz ---
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ep, "voice.mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
voice = np.frombuffer(raw, np.float32).astype(np.float64)
vbuf = np.zeros(N); add(vbuf, voice, LEAD)
env = lp(np.abs(vbuf), 6)
env = env / (env.max() + 1e-9)
duck = 1 - 0.55 * np.clip(env * 4, 0, 1)

mix = vbuf * 1.0 + music * 0.30 * duck + fx * 0.35
# final: la musica sube al terminar la voz
end_v = timing["scenes"][-1]["end_speech"] + LEAD
j = int(end_v * SR)
mix[j:] += music[j:] * 0.12 * np.minimum(1, np.arange(N - j) / (0.4 * SR))
mix = mix[:int(dur * SR)]
fade = int(0.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.9
with wave.open(os.path.join(ep, "mix.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("audio ok", round(dur, 1), "s")
