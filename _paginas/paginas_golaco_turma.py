# Páginas próprias do Golaço Total (/golaco/) e da Turma Arial (/turma/) nos 8 idiomas, no mesmo modelo das páginas
# dos outros jogos (a base é a página do Vôlei Total de cada idioma). A seção do jogo vem da página principal de cada
# idioma; textos em golaco_turma_textos.py. Depois liga as páginas novas no resto do site: menus, rodapés, "Outros jogos",
# link "Tudo sobre…" na página principal, sitemap e llms.txt.   python _paginas/paginas_golaco_turma.py
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from golaco_turma_textos import GOLACO, TURMA

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
SITE = "https://arialgamer.com.br/"
LANGS = ["pt", "en", "es", "de", "fr", "it", "ja", "zh"]
e = html.escape
APPLE = {"golaco": "6839199363", "turma": "6839198223"}
PLAY = {"golaco": None, "turma": "com.arial.turma"}
PASTA = {"golaco": "golaco", "turma": "turma"}
NOME = {"golaco": "Golaço Total", "turma": "Turma Arial"}
ICONE = {"golaco": "golaco.png", "turma": "turma.png"}
CAPA = {"golaco": "media/golaco-gol-quadra.jpg", "turma": "media/turma-topo.jpg"}
TILES = {"gol": "gol-de-placa", "volei": "volei-total", "deicida": "deicida", "rota": "rota-estelar", "esconde": "esconde-esconde",
         "xodo": "xodo", "acervo": "acervo", "gelada": "gelada"}


def pre(l): return "" if l == "pt" else l + "/"
def ler(p): return open(p, encoding="utf8", newline="").read()
def gravar(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w", encoding="utf8", newline="").write(s)


def absoluto(s):
    return re.sub(r'(\s(?:src|href|poster|data-src))="(?!https?:|#|/|mailto:)', r'\1="/', s)


def secao_home(l, k):
    """A seção do produto na página principal do idioma, ajustada para a página própria."""
    h = ler(pre(l) + "index.html")
    ini = h.index(f'id="{k}"'); ini = h.rindex("<section", 0, ini); fim = h.index("</section>", ini) + len("</section>")
    s = h[ini:fim]
    s = s.replace(' data-vista="jogos"', "").replace(" reveal", "").replace(' class="reveal"', "")
    if l == "pt": s = absoluto(s)
    if k == "golaco":
        s = s.replace('class="game golaco wide flip"', 'class="game solo golaco wide"')
        s = re.sub(r"<h2>(.*?)</h2>", r"<h1>\1</h1>", s, count=1)
    else:
        s = re.sub(r"<h2>(.*?)</h2>", r"<h1>\1</h1>", s, count=1)
        p = "/" + pre(l)
        for a, d in TILES.items():
            s = s.replace(f'href="#{a}"', f'href="{p}{d}/"')
        # celular do meio do leque: o vídeo do app sendo usado
        s = re.sub(r'(<div class="tv-fan">.*?</div></div>)<div class="phone"><div class="screen"><img src="/media/turma-inicio\.jpg" alt="([^"]*)"[^>]*></div></div>',
                   r'\1<div class="phone"><div class="screen"><video data-auto muted loop playsinline preload="none" poster="/media/turma-topo.jpg" aria-label="\2"><source src="/media/topo/turma.mp4" type="video/mp4"></video></div></div>', s, count=1, flags=re.S)
    s = re.sub(r'\s*<a class="more" href="[^"]*">[^<]*</a>', "", s)
    return s


def css_turma():
    h = ler("index.html")
    a = h.index(".turma-vitrine {"); b = h.index("\n", h.index("@media (max-width: 560px) { .tv-tiles"))
    return (h[a:b] + "\n.turma-vitrine h1 { font-size: clamp(40px, 5.4vw, 66px); font-weight: 800; margin: 0 } .turma-vitrine h1 span { color: #e9b949 }"
            "\n.turma-vitrine { padding-top: 34px } .tv-fan video { width: 100%; height: 100%; object-fit: cover; display: block }\n")


def css_golaco():
    h = ler("index.html")
    return "".join(m.group(0) + "\n" for m in re.finditer(r"^\.golaco[^{]*\{[^}]*\}", h, re.M))


def bloco_cards(T):
    cards = "".join(f'\n        <article class="reveal"><div class="em">{em}</div><h3>{e(h3)}</h3><p>{e(p)}</p></article>' for em, h3, p in T["cards"])
    return (f'  <section class="block">\n    <div class="wrap">\n      <h2>{e(T["como"])}</h2>\n      <p class="sub">{e(T["como_sub"])}</p>\n'
            f'      <div class="cards">{cards}\n      </div>\n    </div>\n  </section>')


def bloco_faq(T, h2):
    itens = "".join(f"\n        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in T["faq"])
    return (f'  <section class="block">\n    <div class="wrap">\n      <h2>{h2}</h2>\n      <p class="sub">{e(T["faq_sub"])}</p>\n'
            f'      <div class="faq">{itens}\n      </div>\n    </div>\n  </section>')


def outros_lista(l):
    """Entradas de 'Outros jogos e apps' de todos os produtos, no idioma (das páginas existentes + Golaço e Turma)."""
    ent = {}
    for base in ["volei-total", "deicida"]:
        s = ler(f"{pre(l)}{base}/index.html")
        bl = s[s.index('<div class="others">'):s.index("</div>", s.index('<div class="others">'))]
        for m in re.finditer(r'<a href="/(?:[a-z]{2}/)?([a-z-]+)/"><img[^>]*></a>|<a href="/(?:[a-z]{2}/)?([a-z-]+)/">.*?</a>', bl, re.S):
            ent.setdefault(m.group(1) or m.group(2), m.group(0))
    p = "/" + pre(l)
    ent["golaco"] = f'<a href="{p}golaco/"><img src="/golaco.png" alt="" width="72" height="72"><span><b>Golaço Total</b>{e(GOLACO[l]["outro"])}</span></a>'
    ent["turma"] = f'<a href="{p}turma/"><img src="/turma.png" alt="" width="72" height="72"><span><b>Turma Arial</b>{e(TURMA[l]["outro"])}</span></a>'
    return ent


ORDEM_OUTROS = ["turma", "deicida", "golaco", "rota-estelar", "volei-total", "gol-de-placa", "xodo", "esconde-esconde", "gelada", "acervo"]


def pagina(l, k):
    T = (GOLACO if k == "golaco" else TURMA)[l]
    nome = NOME[k]; pasta = PASTA[k]
    url = f"{SITE}{pre(l)}{pasta}/"
    s = ler(f"{pre(l)}volei-total/index.html")
    nl = "\r\n" if "\r\n" in s else "\n"
    s = s.replace("\r\n", "\n")
    # ---------- head ----------
    hi = s.index("</head>"); head = s[:hi]; corpo = s[hi:]
    head = re.sub(r"<title>.*?</title>", f"<title>{e(T['title'], quote=False)}</title>", head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(T["desc"]), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(T["title"]), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(T["og"]), head, count=1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + SITE + CAPA[k], head, count=1)
    head = head.replace("volei-total/", pasta + "/")
    if k == "turma": head = head.replace("</style>", css_turma() + "</style>", 1)
    if k == "golaco": head = head.replace("</style>", css_golaco() + "</style>", 1)
    # JSON-LD
    a = head.index('<script type="application/ld+json">') + len('<script type="application/ld+json">'); b = head.index("</script>", a)
    ld = json.loads(head[a:b])
    for n in ld["@graph"]:
        t = n.get("@type")
        if isinstance(t, list) and "MobileApplication" in t:
            lojas = [f"https://apps.apple.com/{'br/' if l == 'pt' else ''}app/id{APPLE[k]}"] + ([f"https://play.google.com/store/apps/details?id={PLAY[k]}"] if PLAY[k] else [])
            n.update({"image": SITE + ICONE[k], "screenshot": SITE + CAPA[k], "@id": url + "#app", "installUrl": lojas, "sameAs": lojas,
                      "name": nome, "alternateName": nome, "description": T["desc"], "url": url, "genre": T["genre"],
                      "operatingSystem": "iOS, Android" if PLAY[k] else "iOS"})
            if k == "turma":
                n["@type"] = ["MobileApplication"]; n["applicationCategory"] = "EntertainmentApplication"
                n["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": n.get("offers", {}).get("priceCurrency", "BRL"), "availability": "https://schema.org/InStock"}
        elif t == "BreadcrumbList":
            n["itemListElement"][-1].update({"name": nome, "item": url})
        elif t == "FAQPage":
            n["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in T["faq"]]
    head = head[:a] + "\n" + json.dumps(ld, ensure_ascii=False, indent=1) + "\n" + head[b:]
    # ---------- corpo ----------
    corpo = corpo.replace("volei-total/", pasta + "/") if False else corpo
    # menu: a página atual marcada; Vôlei volta a ser link comum
    corpo = corpo.replace(' aria-current="page">Vôlei Total</a>', ">Vôlei Total</a>", 1)
    corpo = re.sub(r'href="/(?:[a-z]{2}/)?(?:#' + k + r'|' + k + r'/)">', f'href="/{pre(l)}{pasta}/" aria-current="page">', corpo, count=1)
    corpo = re.sub(r'<li aria-current="page">Vôlei Total</li>', f'<li aria-current="page">{e(nome)}</li>', corpo, count=1)
    # seção do jogo
    i = corpo.index('<section class="game solo volei'); j = corpo.index("</section>", i) + len("</section>")
    corpo = corpo[:i] + secao_home(l, k).lstrip() + corpo[j:]
    # "Como é", perguntas e outros jogos
    blocos = [m for m in re.finditer(r'  <section class="block">.*?</section>', corpo, re.S)]
    como, faq, outros = blocos[0], blocos[1], blocos[2]
    h2_faq = re.search(r"<h2>(.*?)</h2>", faq.group(0)).group(1)
    ent = outros_lista(l)
    lista = "".join(f"\n        {ent[x]}" for x in ORDEM_OUTROS if x != pasta and x in ent)
    novo_outros = re.sub(r'<div class="others">.*?</div>', f'<div class="others">{lista}\n      </div>', outros.group(0), count=1, flags=re.S)
    corpo = corpo[:como.start()] + bloco_cards(T) + corpo[como.end():faq.start()] + bloco_faq(T, h2_faq) + corpo[faq.end():outros.start()] + novo_outros + corpo[outros.end():]
    # rodapé: links de idioma apontam para esta página
    f = corpo.index('aria-label="Idioma / Language"'); g = corpo.index("</nav>", f)
    corpo = corpo[:f] + corpo[f:g].replace("volei-total/", pasta + "/").replace(' aria-current="page"', "") + corpo[g:]
    corpo = re.sub(r'(<a href="/' + (re.escape(pre(l)) if l != "pt" else "") + pasta + r'/")>', r'\1 aria-current="page">', corpo[:f + 2000][:0] + corpo, count=0) if False else corpo
    s = (head + corpo).replace("\n", nl)
    gravar(f"{pre(l)}{pasta}/index.html", s)
    return f"{pre(l)}{pasta}/index.html"


def ligar_no_site():
    """Menus, rodapés e 'Outros jogos' das outras páginas passam a apontar para /golaco/ e /turma/; 'Tudo sobre' na home."""
    import glob
    n = 0
    for arq in sorted(set(glob.glob("*/index.html") + glob.glob("*/*/index.html") + glob.glob("index.html"))):
        arq = arq.replace(os.sep, "/")
        if arq.startswith(("_paginas", "play-dev-page", "divulgacao")): continue
        s = ler(arq); o = s
        # menu e rodapé das páginas internas: âncora da home vira a página própria
        s = re.sub(r'href="/((?:[a-z]{2}/)?)#(golaco|turma)"', lambda m: f'href="/{m.group(1)}{m.group(2)}/"', s)
        # "Outros jogos e apps": entra quem falta (Golaço e Turma), na ordem do site
        if '<div class="others">' in s and "/golaco/" not in s[s.index('<div class="others">'):s.index("</div>", s.index('<div class="others">'))]:
            top = arq.split("/")[0]; l = top if top in LANGS else "pt"
            if f"{pre(l)}" == "" and top in LANGS: pass
            ent = outros_lista(l)
            atual = re.search(r"/(?:[a-z]{2}/)?([a-z-]+)/index\.html$", "/" + arq)
            eu = atual.group(1) if atual else None
            nl = "\r\n" if "\r\n" in s else "\n"
            lista = "".join(f"{nl}        {ent[x]}" for x in ORDEM_OUTROS if x != eu and x in ent)
            s = re.sub(r'<div class="others">.*?</div>', lambda m: f'<div class="others">{lista}{nl}      </div>', s, count=1, flags=re.S)
        if s != o: gravar(arq, s); n += 1
    # "Tudo sobre…" nas seções da página principal
    for l in LANGS:
        arq = pre(l) + "index.html"; s = ler(arq)
        m = re.search(r'<a class="more" href="([^"]*)volei-total/">([^<]*)</a>', s)
        base, txt = m.group(1), m.group(2)
        for k in ["golaco", "turma"]:
            if f'class="more" href="{base}{k}/"' in s: continue
            t = txt.replace("Vôlei Total", NOME[k])
            if l == "pt" and k == "turma": t = t.replace("sobre o ", "sobre a ")
            ini = s.index(f'id="{k}"'); fim = s.index("</section>", ini)
            if k == "golaco":
                st = s.index('<div class="stores">', ini); st = s.index("</div>", st) + len("</div>")
            else:
                st = s.index('<div class="stores">', ini); st = s.index("</div>", st) + len("</div>")
            ind = "\n        " if k == "golaco" else "\n          "
            nl = "\r\n" if "\r\n" in s[st:st + 300] else "\n"
            s = s[:st] + ind.replace("\n", nl) + f'<a class="more" href="{base}{k}/">{e(t)}</a>' + s[st:]
        gravar(arq, s)
    print(n, "páginas ligadas")


def sitemap_llms():
    s = ler("sitemap.xml")
    nl = "\r\n" if "\r\n" in s else "\n"
    for k in ["golaco", "turma"]:
        for l in LANGS:
            u = f"{SITE}{pre(l)}{k}/"
            if f"<loc>{u}</loc>" in s: continue
            linha = f"  <url><loc>{u}</loc><lastmod>2026-11-28</lastmod><priority>{'0.9' if l == 'pt' else '0.8'}</priority></url>{nl}"
            s = s.replace("</urlset>", linha + "</urlset>")
    gravar("sitemap.xml", s)
    t = ler("llms.txt")
    t = t.replace("https://arialgamer.com.br/en/#golaco", "https://arialgamer.com.br/en/golaco/").replace("https://arialgamer.com.br/en/#turma", "https://arialgamer.com.br/en/turma/")
    gravar("llms.txt", t)


if __name__ == "__main__":
    for l in LANGS:
        for k in ["golaco", "turma"]:
            print("ok", pagina(l, k))
    ligar_no_site()
    sitemap_llms()
