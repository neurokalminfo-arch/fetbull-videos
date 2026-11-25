# Nota 2026-11-25
La clave de ElevenLabs de la tarea programada sigue dando 401 y el proxy de la sesión no deja descargar de elevenlabsusercontent.com (ni del CDN de Higgsfield).
- Voz (Pablo, eleven_multilingual_v2, 502 caracteres, 29,7 s) generada con el conector ElevenLabs; timing.json sale de una transcripción faster-whisper alineada palabra a palabra con el guion.
- `video_sin_audio.mp4` = render normal de `engine/story.html` (render.js) sin audio.
- `bed.wav` = música + efectos de audio.py (con la bajada de música calculada desde las palabras de timing.json, sin la voz). En el sandbox de Higgsfield solo se suma la voz (+0,3 s) a bed.wav con ffmpeg y se monta con el mismo loudnorm de render.js; ese final.mp4 es el que se programa en Metricool (no está en el repo).
Para tener el final.mp4 en el repo: arreglar la clave y ejecutar `tts.py` → `audio.py` → `render.js` con el script.json tal cual.
