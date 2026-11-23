# Nota 2026-11-23
La clave de ElevenLabs de la tarea programada volvió a dar 401 y el proxy de la sesión no deja descargar de elevenlabsusercontent.com.
- Voz (Pablo, eleven_multilingual_v2, 492 caracteres) generada con el conector ElevenLabs; timing.json sale de una transcripción faster-whisper alineada palabra a palabra con el guion.
- `video_sin_audio.mp4` = render normal de `engine/story.html` (render.js) sin audio.
- La mezcla final (audio.py con la voz real + mismo mux/loudnorm de render.js) se hizo en el sandbox de Higgsfield (final.mp4 md5 dc7ee7876ef4d6652dac44f7eefbb876, 28,1 s). Ese final.mp4 es el que se programó en Metricool para el 23-11 a las 19:00 (no está en el repo).
Para tener el final.mp4 en el repo: arreglar la clave y ejecutar `tts.py` → `audio.py` → `render.js` con el script.json tal cual.
