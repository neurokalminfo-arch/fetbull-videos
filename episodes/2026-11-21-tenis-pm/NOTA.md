# Nota 2026-11-21
La clave de ElevenLabs de la tarea programada volvió a dar 401 y el proxy de la sesión no deja descargar de elevenlabsusercontent.com.
- La voz (Pablo, eleven_multilingual_v2) se generó con el conector ElevenLabs; los tiempos por palabra (timing.json) salen de una transcripción faster-whisper alineada con el guion.
- `video_musica.mp4` = render normal de `engine/story.html` con música de `engine/audio.py` pero SIN voz.
- La mezcla final (audio.py con la voz real + mismo mux/loudnorm de render.js sobre este vídeo) se hizo en el sandbox de Higgsfield; ese final.mp4 es el que se programó en Metricool (no está en el repo).
- La voz tiene 529 caracteres (algo por encima del límite de 500).
