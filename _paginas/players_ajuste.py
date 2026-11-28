# 1) Golaço e Acervo na página principal: sem botão de som (os vídeos são mudos).
# 2) Página do Acervo (8 idiomas): player com vídeo automático e videozinhos, com o script do player.
# 3) Páginas dos jogos (8 idiomas): fotos viram vídeo (galeria.js).
import re, glob, os
LS = ['', 'en/', 'es/', 'de/', 'fr/', 'it/', 'ja/', 'zh/']
for p in LS:
    arq = p + 'index.html'
    s = open(arq, encoding='utf8', newline='').read()
    for id in ['golaco', 'acervo']:
        i = s.find(f'id="{id}"'); j = s.find('<div class="clips"', i)
        seg = re.sub(r'\r?\n\s*<button class="sound"[^\n]*</button>', '', s[i:j])
        s = s[:i] + seg + s[j:]
    open(arq, 'w', encoding='utf8', newline='').write(s)

# rótulos da página principal de cada idioma, reaproveitados na página do Acervo
JS = """<script>
// Player do Acervo: vídeo automático (sem som), troca pelos videozinhos e avança sozinho
(() => {
  const reduzir = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-player]').forEach((p) => {
    const video = p.querySelector('video'); video.muted = true; video.defaultMuted = true;
    const clips = [...p.querySelectorAll('.clip')]; let i = 0;
    const select = (k) => { i = k; clips.forEach((c, n) => { c.setAttribute('aria-pressed', n === k); c.querySelector('.bar span').style.width = '0'; });
      const base = clips[k].dataset.src; video.poster = base + '.jpg'; video.src = base + '.mp4'; video.play().catch(() => {}); };
    clips.forEach((c, n) => c.addEventListener('click', () => select(n)));
    video.addEventListener('ended', () => select((i + 1) % clips.length));
    video.addEventListener('timeupdate', () => { if (video.duration) clips[i].querySelector('.bar span').style.width = (video.currentTime / video.duration * 100) + '%'; });
    new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting && !reduzir) { video.preload = 'auto'; video.play().catch(() => {}); } else video.pause(); }), { threshold: .4 }).observe(video);
  });
})();
</script>"""
for p in LS:
    home = open(p + 'index.html', encoding='utf8', newline='').read()
    i = home.find('id="acervo"'); m = re.search(r'<div class="player reveal" data-player>.*?</div>\s*</div>\s*</div>', home[i:], re.S)
    bloco = m.group(0).replace('class="player reveal"', 'class="player"')
    pre = '/' if p == '' else ''
    bloco = bloco.replace('src="media/', 'src="/media/').replace('poster="media/', 'poster="/media/')
    arq = p + 'acervo/index.html'
    s = open(arq, encoding='utf8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    mm = re.compile(r'<div class="player">\s*<div class="phone"><div class="screen"><img [^>]*></div></div>\s*</div>').search(s)
    assert mm, arq
    s = s[:mm.start()] + bloco.replace('\r\n', '\n').replace('\n', nl) + s[mm.end():]
    if 'Player do Acervo' not in s: s = s.replace('</body>', JS.replace('\n', nl) + nl + '</body>', 1)
    open(arq, 'w', encoding='utf8', newline='').write(s); print('acervo', arq)

for p in LS:
    for d in ['deicida', 'rota-estelar', 'volei-total', 'gol-de-placa', 'xodo', 'esconde-esconde', 'gelada', 'acervo']:
        arq = f'{p}{d}/index.html'
        if not os.path.exists(arq): continue
        s = open(arq, encoding='utf8', newline='').read()
        if 'galeria.js' in s: continue
        nl = '\r\n' if '\r\n' in s else '\n'
        s = s.replace('</body>', f'<script src="/galeria.js" defer></script>{nl}</body>', 1)
        open(arq, 'w', encoding='utf8', newline='').write(s)
print('ok')
