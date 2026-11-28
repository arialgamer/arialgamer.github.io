# Vídeos rodando liso no site (8 idiomas, página principal e páginas dos jogos):
# - o player começa a baixar o vídeo um pouco antes de aparecer na tela (antes só baixava ao aparecer, e travava no começo);
# - quando o vídeo passa da metade, já baixa o próximo videozinho (a troca não fica com a tela parada);
# - os vídeos do leque do topo começam a baixar assim que a página termina de abrir (passar o mouse não trava).
import glob

PLAYER_ANTES = "}), { threshold: .4 }).observe(video);"
PLAYER_DEPOIS = PLAYER_ANTES + """
  // começa a baixar um pouco antes de aparecer na tela
  new IntersectionObserver((es, o) => es.forEach((e) => { if (e.isIntersecting) { video.preload = 'auto'; if (video.readyState === 0 && video.paused) video.load(); o.disconnect(); } }), { rootMargin: '800px 0px' }).observe(video);
  // da metade do vídeo em diante, já baixa o próximo videozinho
  let aquecido = -1;
  video.addEventListener('timeupdate', () => {
    const n = (i + 1) % clips.length;
    if (clips.length > 1 && aquecido !== n && video.duration && video.currentTime > video.duration * 0.5) { aquecido = n; fetch(clips[n].dataset.src + '.mp4').catch(() => {}); }
  });"""

LEQUE_ANTES = "document.querySelectorAll('video[data-auto]').forEach((v) => { v.muted = true; v.defaultMuted = true; v.volume = 0; playIfVisible.observe(v); });"
LEQUE_DEPOIS = LEQUE_ANTES + """
// leque do topo: baixa os vídeos assim que a página termina de abrir, para não travar ao passar o mouse
addEventListener('load', () => setTimeout(() => document.querySelectorAll('video[data-auto]').forEach((v) => { if (v.preload !== 'auto') { v.preload = 'auto'; if (v.readyState === 0 && v.paused) v.load(); } }), 300));"""

arqs = sorted(set(glob.glob('index.html') + glob.glob('*/index.html') + glob.glob('*/*/index.html')))
for arq in arqs:
    s = open(arq, encoding='utf8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    novo = s
    if PLAYER_ANTES in novo and 'da metade do vídeo em diante' not in novo:
        novo = novo.replace(PLAYER_ANTES, PLAYER_DEPOIS.replace('\n', nl), 1)
    if LEQUE_ANTES in novo and 'leque do topo: baixa os vídeos' not in novo:
        novo = novo.replace(LEQUE_ANTES, LEQUE_DEPOIS.replace('\n', nl), 1)
    if novo != s:
        open(arq, 'w', encoding='utf8', newline='').write(novo)
        print('ok', arq)
