# Menu no celular (8 idiomas, todas as páginas com o cabeçalho): abaixo de 1261 px o menu do topo sumia e não havia
# como navegar. Agora aparece um botão ☰ que abre a lista (fecha ao tocar num item, fora do menu ou no Esc).
import glob, re, os

ROTULO = {'pt': ('Abrir o menu', 'Fechar o menu'), 'en': ('Open menu', 'Close menu'), 'es': ('Abrir el menú', 'Cerrar el menú'),
          'de': ('Menü öffnen', 'Menü schließen'), 'fr': ('Ouvrir le menu', 'Fermer le menu'), 'it': ('Apri il menu', 'Chiudi il menu'),
          'ja': ('メニューを開く', 'メニューを閉じる'), 'zh': ('打开菜单', '关闭菜单')}
CSS = ('.nav .wrap { position: relative } .nav .menu-btn { display: none } '
       '@media (max-width: 1260px) { '
       '.nav .menu-btn { display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; padding: 0; border-radius: 50%; border: 1px solid var(--line, rgba(255,255,255,.14)); background: var(--glass, rgba(255,255,255,.08)); color: var(--ink, #fff); cursor: pointer; flex-shrink: 0 } '
       '.nav .menu-btn svg { width: 20px; height: 20px } .nav .menu-btn .x { display: none } .nav.aberto .menu-btn .x { display: block } .nav.aberto .menu-btn .l { display: none } '
       '.nav.aberto { background: rgba(13,10,32,.94); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px) } '
       '.nav.aberto ul { display: flex; flex-direction: column; position: absolute; top: calc(100% + 6px); right: 0; min-width: 240px; max-height: calc(100vh - 96px); overflow: auto; margin: 0; padding: 8px; gap: 2px; '
       'background: rgba(13,10,32,.97); border: 1px solid var(--line, rgba(255,255,255,.14)); border-radius: 18px; box-shadow: 0 20px 50px rgba(0,0,0,.5) } '
       '.nav.aberto ul li { display: block !important } .nav.aberto ul a { padding: 11px 14px; font-size: 15px } '
       '.nav.aberto ul li.app { margin: 4px 0 0; padding: 4px 0 0; border-left: 0; border-top: 1px solid var(--line, rgba(255,255,255,.14)) } }'
       '@media (prefers-reduced-motion: no-preference) { .nav.aberto ul { animation: menu-abre .18s ease-out } @keyframes menu-abre { from { opacity: 0; transform: translateY(-6px) } } }')
BOTAO = ('<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="{a}" data-fechar="{f}">'
         '<svg class="l" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>'
         '<svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg></button>')
JS = ("<script>(() => { const nav = document.getElementById('nav'), b = nav && nav.querySelector('.menu-btn'); if (!b) return; const abrir = b.getAttribute('aria-label'), fechar = b.dataset.fechar;"
      " const poe = (a) => { nav.classList.toggle('aberto', a); b.setAttribute('aria-expanded', a); b.setAttribute('aria-label', a ? fechar : abrir); };"
      " b.addEventListener('click', (e) => { e.stopPropagation(); poe(!nav.classList.contains('aberto')); });"
      " nav.querySelectorAll('ul a').forEach((a) => a.addEventListener('click', () => poe(false)));"
      " document.addEventListener('click', (e) => { if (!nav.contains(e.target)) poe(false); });"
      " document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('aberto')) { poe(false); b.focus(); } }); })();</script>")

n = 0
arqs = sorted(set(glob.glob('index.html') + glob.glob('*/index.html') + glob.glob('*/*/index.html') + glob.glob('*/*/*/index.html')))
for arq in arqs:
    arq = arq.replace('\\', '/')
    if arq.startswith(('_paginas', 'play-dev-page', 'divulgacao')): continue
    s = open(arq, encoding='utf8', newline='').read()
    i = s.find('<header class="nav" id="nav">')
    if i < 0 or 'class="menu-btn"' in s: continue
    j = s.find('</header>', i)
    h = s[i:j]
    if '<ul>' not in h: continue
    nl = '\r\n' if '\r\n' in s else '\n'
    top = arq.split('/')[0]; lg = top if top in ROTULO else 'pt'
    a, f = ROTULO[lg]
    h2 = h.replace('<ul>', '<ul id="nav-menu">', 1)
    # botão no fim da linha do cabeçalho (depois dos botões das redes)
    k = h2.rfind('</div>')
    h2 = h2[:k] + '  ' + BOTAO.format(a=a, f=f) + nl + '  ' + h2[k:]
    h2 = h2.rstrip(' ') + JS + nl
    s = s[:i] + h2 + s[j:]
    # CSS no fim do primeiro <style>
    st = s.find('</style>')
    s = s[:st] + CSS + nl + s[st:]
    open(arq, 'w', encoding='utf8', newline='').write(s); n += 1
print(n, 'páginas')

# celular: abre espaço para o botão ☰ (o botão "Seguir" vira só o ícone do TikTok; em telas bem estreitas o YouTube sai do topo; o contador de visitas some com o menu aberto)
EXTRA = ('@media (max-width: 560px) { .nav .pill { font-size: 0; gap: 0; width: 42px; height: 42px; padding: 0; justify-content: center; flex-shrink: 0 } .nav .pill svg { margin: 0 } } '
         '@media (max-width: 420px) { .nav .wrap { gap: 8px } } @media (max-width: 340px) { .nav .yt-round { display: none } } .nav.aberto .visitas { visibility: hidden }')
m = 0
for arq in arqs:
    arq = arq.replace(os.sep, '/')
    if arq.startswith(('_paginas', 'play-dev-page', 'divulgacao')): continue
    s = open(arq, encoding='utf8', newline='').read()
    if 'class="menu-btn"' not in s or '.nav .pill { font-size: 0' in s: continue
    s = s.replace(CSS, CSS + EXTRA, 1)
    open(arq, 'w', encoding='utf8', newline='').write(s); m += 1
print(m, 'páginas com espaço no celular')
