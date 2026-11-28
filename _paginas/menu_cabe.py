# Cabeçalho: com 11 itens no menu (Turma e Golaço entraram), o fim do menu passava da tela a partir de 1261 px.
# Nessas larguras o cabeçalho fica mais largo (até 1560 px), os itens ficam um pouco mais juntos e o item "Redes"
# sai do menu (os botões das redes já estão ao lado).
import glob
REGRA = '@media (min-width: 1261px) { .nav .wrap { width: min(1560px, calc(100% - 40px)) } .nav ul { gap: 2px } .nav ul a { padding: 8px 7px; font-size: 13.5px } .nav ul li:has(> a[href$="#siga"]) { display: none } .nav ul li.app { margin-left: 6px; padding-left: 6px } }'
ANCORA = "@media (max-width: 1260px) { .nav ul { display: none }"
n = 0
for arq in sorted(set(glob.glob('index.html') + glob.glob('*/index.html') + glob.glob('*/*/index.html') + glob.glob('*/*/*/index.html'))):
    s = open(arq, encoding='utf8', newline='').read()
    if ANCORA not in s or '(min-width: 1261px) { .nav .wrap { width: min(1560px' in s: continue
    i = s.find('</style>', s.find(ANCORA))
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s[:i] + REGRA + nl + s[i:]
    open(arq, 'w', encoding='utf8', newline='').write(s); n += 1
print(n, 'páginas')
