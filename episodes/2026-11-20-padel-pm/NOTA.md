# Nota 2026-11-20
La clave de ElevenLabs de la tarea programada dio 401 (invalid_api_key) y el proxy de la sesión no deja descargar de elevenlabsusercontent.com.
- La voz (Pablo, eleven_multilingual_v2) se generó con el conector ElevenLabs; los tiempos por palabra (timing.json) salen de su transcripción (scribe_v1).
- `video_musica.mp4` = render normal de `engine/story.html` con la música de `engine/audio.py` pero SIN voz.
- La mezcla final (audio.py con la voz real + mux con este vídeo, -14 LUFS) se hizo en el sandbox del conector ElevenLabs; ese final.mp4 es el que se publicó en Metricool.
Para tener el final.mp4 en el repo: arreglar la clave y ejecutar `tts.py` → `audio.py` → `render.js` con el script.json tal cual.
