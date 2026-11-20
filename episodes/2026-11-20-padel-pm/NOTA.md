# Nota 2026-11-20
La clave de ElevenLabs de la tarea programada dio 401 (invalid_api_key) y el proxy de la sesión no deja descargar de elevenlabsusercontent.com.
- La voz (Pablo, eleven_multilingual_v2) se generó con el conector ElevenLabs; los tiempos por palabra (timing.json) salen de su transcripción (scribe_v1).
- `video_musica.mp4` = render normal de `engine/story.html` con la música de `engine/audio.py` pero SIN voz.
- La mezcla final se hizo en el sandbox de Higgsfield con el flujo del repo: `audio.py` con la voz real y el mismo mux/loudnorm de `render.js` sobre el vídeo de `video_musica.mp4` (md5 773d27d2e6452d76f0daa8cb9055c6fd). Ese final.mp4 se subió a Higgsfield y es el que se programó en Metricool (no está en el repo).
Para tener el final.mp4 en el repo: arreglar la clave y ejecutar `tts.py` → `audio.py` → `render.js` con el script.json tal cual.
