# Menu do cabeçalho das páginas de cada jogo e da imprensa (8 idiomas): entram Turma Arial e Golaço Total,
# apontando para a seção deles na página principal do mesmo idioma (eles ainda não têm página própria).
import re, glob
n = 0
for arq in sorted(glob.glob('*/index.html') + glob.glob('*/*/index.html')):
    s = open(arq, encoding='utf8', newline='').read()
    i = s.find('<header'); j = s.find('</header>', i)
    if i < 0: continue
    h = s[i:j]
    m = re.search(r'([ \t]*)<li><a href="(/(?:[a-z]{2}/)?)deicida/"[^>]*>Deicida</a></li>(\r?\n)', h)
    if not m or 'golaco' in h: continue
    ind, pre, nl = m.group(1), m.group(2), m.group(3)
    turma = f'{ind}<li><a href="{pre}#turma">Turma Arial</a></li>{nl}'
    golaco = f'{ind}<li><a href="{pre}#golaco">Golaço Total</a></li>{nl}'
    h2 = h[:m.start()] + turma + m.group(0) + golaco + h[m.end():]
    s = s[:i] + h2 + s[j:]
    open(arq, 'w', encoding='utf8', newline='').write(s); n += 1
print(n, 'páginas')
