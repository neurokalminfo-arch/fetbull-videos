# Fábrica diaria de vídeos FetBull

Cada ejecución crea **1 vídeo corto** (1080x1920, 25–35 s) y lo deja programado en Metricool para Instagram (@fet.bull, Reel) y TikTok (@fetbull_insole).
Hay dos ejecuciones al día: slot `am` = **10:00** y slot `pm` = **19:00** (hora de Madrid).

## Pasos de cada ejecución
1. Lee los temas ya usados: `grep -h '"topic"' episodes/*/script.json`. No repitas tema ni gancho de los últimos 30 días.
2. Elige deporte y nivel con la rotación (abajo) y escribe `episodes/AAAA-MM-DD-<deporte>-<slot>/script.json`.
3. `python3 engine/tts.py <ep>` (necesita `ELEVENLABS_API_KEY`) → `python3 engine/audio.py <ep>` → `node engine/render.js <ep> --preview t1,t2,t3,t4` y **mira los fotogramas** (texto completo, nada cortado, foto del producto visible si la hay). Corrige y repite. Después `node engine/render.js <ep>`.
4. Borra los `prev_*.jpg`, luego `git add -A && git commit && git push origin main`. URL pública:
   `https://raw.githubusercontent.com/neurokalminfo-arch/fetbull-videos/main/episodes/<id>/final.mp4` (comprueba con curl que da 200).
5. Programa en Metricool (`createScheduledPost`, `draft: false`, `autoPublish: true`, zona `Europe/Madrid`):
   - blogId **7796032** (marca Fetbull) · providers `[instagram, tiktok]` · `instagramData: {type: REEL, showReelOnFeed: true}` · `tiktokData.title` = `tiktok_title` · texto = caption + hashtags.
   - Si Metricool da "internal error while storing the media", reintenta tras unos segundos.
   - NO toques las marcas Valkyra, neurokalm, Airnaze ni La Gran Pregunta.

## Rotación (para equilibrar)
- Deportes: ~40 % pádel, ~35 % baloncesto, ~25 % resto (tenis, vóley, running, gym). Nunca el mismo deporte dos vídeos seguidos.
- Nivel (`level`): `principiante` (la mayoría de la audiencia: ha jugado pocas veces), `avanzado` (compite, juega ligas) o `todos` (con la escena `levels` que da una versión para cada uno). Aprox. 50 % principiante, 20 % avanzado, 30 % todos.
- Mañana (am): preparación, calentamiento, técnica para el partido de hoy. Tarde (pm): el partido after-work, cansancio, recuperación, lo que pasó en pista.

## Cómo hablamos (de la investigación de audiencia)
- **Principiante**: juega con amigos 1–2 veces por semana. Quiere mejorar rápido sin jerga, no hacer el ridículo y no acabar con gemelos, rodillas o planta del pie cargados al día siguiente. Le sirven: colocación, split step, no correr a la pared, calentar 10 min, elegir zapatilla, cómo aterrizar. Explica cada término técnico la primera vez.
- **Avanzado**: compite. Quiere detalle y credibilidad: primer paso explosivo, cambios de dirección, aterrizajes tras remate o salto, fatiga en el tercer set o el último cuarto, recuperación entre partidos.
- Temas que conectan en cualquier nivel: errores típicos ("no es el brazo, son los pies"), mitos, lo que hacen los pros, cómo calentar, cargar menos piernas, zapatillas gastadas, saltar y caer bien (rodillas que no se van hacia dentro), tobillos en baloncesto.
- Estructura: **gancho** de 2 s que identifique ("¿Llegas tarde a la bola?") → error/situación → **consejo concreto** (1–3 pasos) → puente natural a FORGE → **CTA de comentario**.
- La investigación de TikTok indica que pedir un comentario concreto funciona mejor que pedir like o "sígueme". CTA = "Comenta <PALABRA> y te enseño X" (y luego se hace ese vídeo) + "FORGE en el perfil".
- Voz: segunda persona, directa, enérgica, como un entrenador que sabe y te habla claro. Español de España. Sin anglicismos innecesarios.

## FORGE: lo que SÍ se puede decir (sale de fetbull.com/products/forge)
- Plantilla con **placa de carbono** que flexiona y recupera la forma en el despegue (impulso).
- **Talón con amortiguación PORON®** para los aterrizajes.
- **Soporte de arco** para la estabilidad en giros y cambios de dirección.
- Pensada para sesiones largas y cómoda. Se adapta a la zapatilla en 2–3 usos. Tallas 35–46, se puede recortar.
- Deportes: baloncesto, vóley, pádel, tenis, running, gym.

## Lo que NO se dice
- Ni porcentajes (+22 %, +13 %), ni precio ni descuentos, ni "previene lesiones", "cura", "elimina el dolor", ni ningún claim médico.
- Ni promesas de rendimiento ("saltarás más"). Se describe lo que es y para qué está pensada.
- Ni datos de estudios que no sean ciertos y generales. Ante la duda, sin cifra.
- FORGE aparece en **una sola escena** (la penúltima): con foto real (`zone.type: "product"`) si hay fotos en `assets/product/`; si no, **sin foto** con `zone.type: "chips"` y sus 2–3 rasgos reales (formato aprobado el 2026-11-11). Nunca dibujes ni generes el producto. Cierra con "FORGE, en nuestro perfil" para crear curiosidad. Si el tema es de técnica pura, el puente es "todo empieza en el apoyo" o algo similar.

## Fotos reales del producto
En `assets/product/` (solo fotos reales de FORGE, nunca generadas). Rota la foto en cada vídeo. Si una escena `product` apunta a una foto que no existe, `render.js` se detiene. Si la carpeta está vacía, haz el vídeo sin foto (escena `chips`, ver arriba) y publícalo con normalidad; menciónalo en el resumen, sin PushNotification.

## Formato de script.json
```json
{"slot":"am|pm","sport":"padel|basket|tenis|voley|running|gym","level":"principiante|avanzado|todos","topic":"...",
 "scenes":[{"say":"texto que dice la voz","kicker":"frase pequeña con *acento*","title":["LÍNEA 1","línea *acento*"],"small":false,"zone":{...}}],
 "caption":"texto del post con emojis y pregunta final","hashtags":["#padel","..."],"tiktok_title":"título corto",
 "music":{"bpm":124,"key":"A"}}
```
- 5–6 escenas, **420–500 caracteres de voz** en total (créditos de ElevenLabs).
- `*palabra*` = color lima. Títulos: 1–3 líneas, máx. ~12 caracteres por línea.
- `zone.type`:
  - `court`: pista dibujada del deporte con jugador animado. `path` [[x,y],...] 0..1 (y=0 arriba = rival; en pádel/tenis la red está en y=0.5); `ball` opcional [[x,y],[x,y]]; `marks` [{x,y,t,at}]. Baloncesto: medio campo con canasta arriba.
  - `steps` (items `{n,t,s,at}`, máx. 3), `chips` (`{t,at}`), `tip` (`text`, `at`), `vs` (items `{k:"no"|"si",t}`), `levels` (items `{k:"SI ESTÁS EMPEZANDO"|"SI YA COMPITES",t,at}`), `big` (`text`, `sub`), `product` (`img`, `tag`, `at`, items `{t,at}` con 2–3 rasgos reales), `cta` (items `{icon: comment|save|share|link, t, at}`).
- `at` = palabra exacta que dice la voz en esa escena; el elemento aparece justo ahí.
- `music.bpm` 118–132 y `key` (A, C, D, E, F, G): cámbialos de un vídeo a otro.

## Motor
- `engine/tts.py`: voz (Pablo, masculina) con tiempos por carácter → `voice.mp3` + `timing.json`.
- `engine/audio.py`: música original sintetizada por código + efectos (golpe inicial, whoosh entre escenas) + voz, con la música bajando cuando habla → `mix.wav`.
- `engine/render.js`: dibuja `engine/template.html` fotograma a fotograma con Playwright y monta con ffmpeg (-14 LUFS) → `final.mp4`.
- Nunca subas claves a este repositorio (es público).
