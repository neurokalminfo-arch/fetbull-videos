# Nota 2026-11-26
La clave de ElevenLabs de la tarea programada sigue dando 401 y el proxy de la sesión no deja descargar de elevenlabsusercontent.com.
- Voz (Pablo, eleven_multilingual_v2, 495 caracteres, 25,7 s) generada con el conector ElevenLabs; timing.json sale de una transcripción faster-whisper alineada palabra a palabra con el guion.
- `video_sin_audio.mp4` = render normal de `engine/story.html` (render.js) sin audio.
- La mezcla final (audio.py con la voz real + mismo mux/loudnorm de render.js) se hace en el sandbox de Higgsfield; ese final.mp4 es el que se programa en Metricool (no está en el repo).
Para tener el final.mp4 en el repo: arreglar la clave y ejecutar `tts.py` → `audio.py` → `render.js` con el script.json tal cual.
- final.mp4 (md5 2ac05e7bc8781face8005c48b4ebb112, 27,4 s) programado en Metricool para el 26-11 a las 19:00 (post 443417928, Instagram Reel + TikTok).
