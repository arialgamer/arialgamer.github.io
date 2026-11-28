# Topo do site (8 idiomas): Deicida com luta (múmias e Sobek), Golaço com gols lisos, Turma Arial com vídeo navegando no app.
import re
for p in ['', 'en/', 'es/', 'de/', 'fr/', 'it/', 'ja/', 'zh/']:
    arq = p + 'index.html'
    s = open(arq, encoding='utf8', newline='').read()
    def tag(m):
        t = m.group(0)
        t = t.replace('topo/deicida-chamada.mp4', 'topo/deicida-luta.mp4').replace('deicida-chamada.jpg', 'deicida-topo-luta.jpg')
        return t
    s = re.sub(r'<video [^>]*>\s*<source src="[^"]*topo/deicida-chamada\.mp4"[^>]*>', tag, s)
    s = s.replace('topo/golaco-quadra.mp4', 'topo/golaco-gols.mp4')
    m = re.search(r'<img src="(/?)media/turma-topo\.jpg" alt="([^"]*)" loading="lazy" width="540" height="1170">', s)
    assert m, arq
    pre, alt = m.group(1), m.group(2)
    s = s[:m.start()] + f'<video data-auto muted loop playsinline preload="none" poster="{pre}media/turma-topo.jpg" aria-label="{alt}"><source src="{pre}media/topo/turma.mp4" type="video/mp4"></video>' + s[m.end():]
    open(arq, 'w', encoding='utf8', newline='').write(s)
    print(arq, s.count('deicida-luta'), s.count('golaco-gols'), s.count('topo/turma.mp4'))
