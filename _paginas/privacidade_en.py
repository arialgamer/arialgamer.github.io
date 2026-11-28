# Nas páginas em inglês, espanhol, alemão, francês, italiano, japonês e chinês, os links de privacidade
# abrem direto na parte em inglês da página (as páginas de privacidade têm português e inglês).
import glob, re
n = 0
for lg in ['en', 'es', 'de', 'fr', 'it', 'ja', 'zh']:
    for arq in glob.glob(f'{lg}/index.html') + glob.glob(f'{lg}/*/index.html') + glob.glob(f'{lg}/*/*/index.html'):
        s = open(arq, encoding='utf8', newline='').read()
        novo = re.sub(r'href="(/(?:[a-z-]+-privacidade|acervo/privacidade)/)"', r'href="\1#en"', s)
        if novo != s: open(arq, 'w', encoding='utf8', newline='').write(novo); n += 1
print(n, 'páginas')
