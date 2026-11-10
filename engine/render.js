// Uso: node engine/render.js episodes/<id> [--preview 2.5,8,14]
// Necesita voice.mp3 + timing.json (tts.py) y mix.wav (audio.py) para el render final.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const ep = path.resolve(process.argv[2]);
const prev = process.argv[3] === '--preview' ? process.argv[4].split(',').map(Number) : null;
const script = JSON.parse(fs.readFileSync(path.join(ep, 'script.json')));
const timing = JSON.parse(fs.readFileSync(path.join(ep, 'timing.json')));
const FPS = 30, LEAD = 0.3, dur = timing.duration + LEAD;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.addInitScript(d => { window.DATA = d; }, { script, timing });
  await p.goto('file://' + path.join(__dirname, 'template.html'));
  await p.evaluate(() => Promise.all([document.fonts.ready, ...[...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))]));
  const bad = await p.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')));
  if (bad.length) { console.error('FALTAN IMÁGENES:', bad.join(', ')); process.exit(1); }
  if (prev) {
    for (const t of prev) { await p.evaluate(t => render(t), t); await p.screenshot({ path: path.join(ep, `prev_${t}.jpg`), type: 'jpeg', quality: 85 }); }
    await b.close(); return;
  }
  const tmp = path.join(ep, 'video_tmp.mp4'), silent = path.join(ep, 'silent_tmp.mp4');
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.ceil(dur * FPS);
  for (let f = 0; f < N; f++) {
    await p.evaluate(t => render(t), f / FPS - LEAD);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', path.join(ep, 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '2', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp]);
  fs.renameSync(tmp, path.join(ep, 'final.mp4')); fs.unlinkSync(silent);
  console.log('ok', path.join(ep, 'final.mp4'), dur.toFixed(1) + 's');
})();
