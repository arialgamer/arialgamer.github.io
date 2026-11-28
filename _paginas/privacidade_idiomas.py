# Políticas de privacidade em 8 idiomas: a cada página (que tinha português e inglês) somam-se espanhol, alemão,
# francês, italiano, japonês e chinês, traduzidos frase a frase do inglês (privacidade_textos.py e
# privacidade_acervo_textos.py). Os links de privacidade das páginas em cada idioma passam a abrir a parte daquele idioma,
# e quem chega sem âncora vê a parte do idioma do celular.   python _paginas/privacidade_idiomas.py
import os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from privacidade_textos import T as T1, L
from privacidade_acervo_textos import T as T2

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
T = {**T1, **T2}
NOMES = {"es": "Español", "de": "Deutsch", "fr": "Français", "it": "Italiano", "ja": "日本語", "zh": "中文"}
LANG = {"es": "es", "de": "de", "fr": "fr", "it": "it", "ja": "ja", "zh": "zh-Hans"}
PAGINAS = ["turma-privacidade", "deicida-privacidade", "golaco-privacidade", "rota-estelar-privacidade", "volei-privacidade", "gol-privacidade",
           "xodo-privacidade", "esconde-privacidade", "gelada-privacidade", "acervo/privacidade"]
UNIDADE = re.compile(r'(<(h2|h3|p|li|span|td|th|summary|dt|dd)(\s[^>]*)?>)(.*?)(</\2>)', re.S)
SCRIPT = ("<script>if (!location.hash) { var l = (navigator.language || '').slice(0, 2).toLowerCase();"
          " if (l !== 'pt' && document.getElementById(l)) location.replace('#' + l); else if (l !== 'pt' && document.getElementById('en')) location.replace('#en'); }</script>")

faltam = set()
for p in PAGINAS:
    arq = p + "/index.html"
    s = open(arq, encoding="utf8", newline="").read()
    if 'id="es"' in s: print("já tem", arq); continue
    nl = "\r\n" if "\r\n" in s else "\n"
    i = s.index('<section id="en"'); j = s.index("</section>", i) + len("</section>")
    en = s[i:j]
    novas = []
    for k, lg in enumerate(L):
        def troca(m):
            txt = m.group(4).strip()
            if not txt or "<li" in txt or "<ul" in txt: return m.group(0)
            if txt not in T: faltam.add(txt); return m.group(0)
            return m.group(1) + m.group(4).replace(txt, T[txt][k]) + m.group(5)
        sec = UNIDADE.sub(troca, en)
        sec = sec.replace('<section id="en" lang="en">', f'<section id="{lg}" lang="{LANG[lg]}">', 1)
        novas.append(sec)
    s = s[:j] + "".join(nl + nl + "  " + x for x in novas) + s[j:]
    # menu de idiomas do topo da página
    s = re.sub(r'(<nav>\s*<a href="#pt">[^<]*</a>\s*<a href="#en">[^<]*</a>)', lambda m: m.group(1) + "".join(f'<a href="#{lg}">{NOMES[lg]}</a>' for lg in L), s, count=1)
    s = s.replace("</body>", SCRIPT + nl + "</body>", 1)
    open(arq, "w", encoding="utf8", newline="").write(s)
    print("ok", arq)

if faltam:
    print("FRASES SEM TRADUÇÃO:"); [print(" -", f) for f in sorted(faltam)]

# links de privacidade nas páginas de cada idioma: abrem a parte do idioma
n = 0
for lg in L:
    for arq in glob.glob(f"{lg}/index.html") + glob.glob(f"{lg}/*/index.html") + glob.glob(f"{lg}/*/*/index.html"):
        s = open(arq, encoding="utf8", newline="").read()
        novo = re.sub(r'href="(/(?:[a-z-]+-privacidade|acervo/privacidade)/)#en"', rf'href="\1#{lg}"', s)
        if novo != s: open(arq, "w", encoding="utf8", newline="").write(novo); n += 1
print(n, "páginas com o link de privacidade no idioma")
