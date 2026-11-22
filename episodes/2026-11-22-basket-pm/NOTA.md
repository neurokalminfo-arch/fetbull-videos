# Nota 2026-11-22
La clave de ElevenLabs de la tarea programada volvió a dar 401 y el proxy de la sesión no deja descargar de elevenlabsusercontent.com, static.metricool.com ni del CDN de Higgsfield.
- Voz (Pablo, eleven_multilingual_v2, 478 caracteres) generada con el conector ElevenLabs; timing.json sale de una transcripción faster-whisper alineada palabra a palabra con el guion.
- `video_sin_audio.mp4` = render normal de `engine/story.html` (render.js) sin audio.
- La mezcla final se hizo en el sandbox de Higgsfield con este repo clonado: `audio.py` con la voz real + el mismo mux/loudnorm de `render.js` sobre `video_sin_audio.mp4` (final.mp4 md5 a7d4e0e6e1bf621d4b7329f97fe2664e, 26,1 s). Ese final.mp4 es el que se programó en Metricool (no está en el repo).
Para tener el final.mp4 en el repo: arreglar la clave y ejecutar `tts.py` → `audio.py` → `render.js` con el script.json tal cual.
