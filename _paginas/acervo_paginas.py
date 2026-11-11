# Gera as páginas do Acervo nos 8 idiomas: /acervo/ (e /en/acervo/, /es/acervo/…), uma página por tipo de coleção
# (/acervo/relogios/, /en/acervo/watches/…) e o endereço curto /acervo/baixar/, que abre a loja certa do celular.
# Textos em acervo_textos.py; visual, telas e botões das lojas vêm das páginas principais de cada idioma.
# Rode de novo depois de mudar os textos ou a seção do Acervo nas páginas principais:  python _paginas/acervo_paginas.py
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acervo_textos import L, TIPOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://arialgamer.com.br/"
APP_ID = "6832553837"
IOS = "https://apps.apple.com/app/id" + APP_ID
ANDROID = "https://play.google.com/store/apps/details?id=com.arial.acervo"
ORDEM = ["pt", "en", "es", "de", "fr", "it", "ja", "zh"]
e = html.escape


def ler(p):
    return open(os.path.join(RAIZ, p), encoding="utf-8").read()


def entre(s, ini, fim):
    a = s.index(ini); b = s.index(fim, a)
    return s[a:b]


idx = ler("index.html")
CSS = entre(idx, "<style>", "</style>")[len("<style>"):]
SPRITE = entre(idx, '<svg width="0"', "</svg>") + "</svg>"
_g = ler("_paginas/gerar.py"); _a = _g.index('CSS_EXTRA = """') + len('CSS_EXTRA = """')
CSS_EXTRA = _g[_a:_g.index('"""', _a)] + """
.feats.lista { max-width: 760px }
.tipos { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px }
.tipos a { display: flex; align-items: center; gap: 14px; padding: 18px 20px; border-radius: 20px; background: var(--glass); border: 1px solid var(--line); text-decoration: none; transition: transform .2s, background .2s }
.tipos a:hover { transform: translateY(-2px); background: var(--glass-2) }
.tipos .em { font-size: 30px; line-height: 1 }
.tipos b { font-family: var(--display); font-size: 21px; line-height: 1.15 }
.planos { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; max-width: 860px }
.planos article { padding: 24px; border-radius: 20px; background: var(--glass); border: 1px solid var(--line) }
.planos article.pro { border-color: var(--c); box-shadow: 0 0 0 1px var(--c) inset }
.planos h3 { font-size: 24px; margin: 0 0 8px }
.planos p { margin: 0; color: var(--muted) }
.acervo.solo .lead { color: var(--muted); font-size: 18px; max-width: 52ch; margin: 0 0 22px }
.acervo.solo .more { margin-right: 18px }
.acervo.solo.tipo .info h1 { font-size: clamp(30px, 4.4vw, 50px); line-height: 1.08 }
@media (max-width: 860px) { .acervo.solo .head { align-items: flex-start } .acervo.solo .head img { width: 64px; height: 64px } .acervo.solo.tipo .info h1 { font-size: 30px } }
@media (max-width: 860px) { .tipos { grid-template-columns: 1fr 1fr } .planos { grid-template-columns: 1fr } }
@media (max-width: 520px) { .tipos { grid-template-columns: 1fr } }
"""

SCRIPT = """<script>
document.body.classList.remove('no-js');
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('solid', scrollY > 20);
addEventListener('scroll', onScroll, { passive: true }); onScroll();
const io = new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }), { threshold: .12 });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
</script>"""

PASTA_JOGO = {"gelada": "gelada", "esconde": "esconde-esconde", "gol": "gol-de-placa"}
ICONE_JOGO = {"gelada": "gelada.png", "esconde": "esconde.png", "gol": "gol.png"}


def pre(cod):
    return "" if cod == "pt" else cod + "/"


def pagina_idioma(cod):
    """Pedaços da página principal do idioma: seção do Acervo e resumo de cada jogo."""
    s = ler("index.html" if cod == "pt" else f"{cod}/index.html")
    sec = entre(s, '<section class="game acervo', "</section>")
    info = {
        "tag": re.search(r'<p class="tag">.*?</p>', sec).group(0),
        "precos": "".join(re.findall(r'<span class="price[^"]*">.*?</span>', sec)),
        "feats": re.search(r'<ul class="feats">.*?</ul>', sec, re.S).group(0),
        "lojas": re.search(r'<div class="stores">.*?</div>', sec, re.S).group(0),
        "tela": re.search(r'<div class="phone">.*?</div></div>', sec).group(0),
        "telas": re.search(r'<div class="wrap shots">.*?\n    </div>', sec, re.S).group(0),
        "jogos": {},
    }
    for k in PASTA_JOGO:
        g = entre(s, f'<section class="game {k}', "</section>")
        nome = re.search(r"<h2>(.*?)</h2>", g).group(1)
        tag = re.sub(r"<[^>]+>", "", re.search(r'<p class="tag">(.*?)</p>', g).group(1))
        info["jogos"][k] = (nome, tag)
    return {k: (re.sub(r'(\s(?:src|href))="(?!https?:|#|/)', r'\1="/', v) if isinstance(v, str) else v) for k, v in info.items()}


PEDACOS = {cod: pagina_idioma(cod) for cod in ORDEM}


def url_landing(cod):
    return f"{SITE}{pre(cod)}acervo/"


def url_tipo(cod, tid):
    slug = next(t[2][cod] for t in TIPOS if t[0] == tid)
    return f"{SITE}{pre(cod)}acervo/{slug}/"


def url_jogo(cod, k):
    return f"/{pre(cod)}{PASTA_JOGO[k]}/"


def caminho(url):
    return url.replace(SITE, "/")


def head(cod, titulo, desc, url, alternos, jsonld, imagem):
    T = L[cod]
    alt = "".join(f'<link rel="alternate" hreflang="{L[c]["lang"]}" href="{u}">\n' for c, u in alternos.items())
    alt += f'<link rel="alternate" hreflang="x-default" href="{alternos["pt"]}">\n'
    return f"""<!doctype html>
<html lang="{T["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#0d0a20">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Arial Gamer">
<meta property="og:locale" content="{T["og"]}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}{imagem}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=1)}
</script>
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/acervo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Figtree:wght@400;500;600;700&display=swap">
<style>{CSS}{CSS_EXTRA}</style>
</head>
<body class="no-js">
<!-- Página gerada por _paginas/acervo_paginas.py. Não edite à mão. -->

{SPRITE}
"""


def nav(cod):
    T = L[cod]; p = pre(cod)
    return f"""<header class="nav" id="nav">
  <div class="wrap">
    <a class="brand" href="/{p}"><img src="/logo.png" alt="" width="38" height="38">Arial Gamer</a>
    <ul>
      <li><a href="/{p}acervo/">Acervo</a></li>
      <li><a href="/{p}#jogos">{e(T["nav_jogos"])}</a></li>
    </ul>
    <a class="pill" href="/acervo/baixar/"><img src="/acervo.png" alt="" width="22" height="22" style="border-radius:6px">{e(T["baixar"])}</a>
  </div>
</header>
"""


def rodape(cod, alternos):
    T = L[cod]
    tipos = "\n".join(f'      <a href="{caminho(url_tipo(cod, tid))}">{e(T["tipos"][tid]["nome"])}</a>' for tid, _, _ in TIPOS)
    idiomas = "\n".join(f'      <a href="{caminho(u)}" hreflang="{L[c]["lang"]}" lang="{L[c]["lang"]}"{" aria-current=\"page\"" if c == cod else ""}>{L[c]["nome_idioma"]}</a>' for c, u in alternos.items())
    return f"""<footer>
  <div class="wrap">
    <img class="sig" src="/assinatura.svg" alt="Arial">
    <nav aria-label="Acervo">
      <a href="/{pre(cod)}acervo/">Acervo</a>
{tipos}
      <a href="/acervo/privacidade/">{e(T["privacidade"].rstrip(" →"))}</a>
    </nav>
    <nav aria-label="Idioma / Language">
{idiomas}
    </nav>
  </div>
</footer>
"""


def topo(cod, h1, texto, eyebrow, crumbs, links_extra="", tipo=False):
    P = PEDACOS[cod]
    tag = "" if tipo else P["tag"]
    migalhas = "".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in crumbs[:-1]) + f'<li aria-current="page">{e(crumbs[-1][0])}</li>'
    return f"""  <nav class="crumbs" aria-label="Arial Gamer"><div class="wrap"><ol>{migalhas}</ol></div></nav>

  <section class="game acervo solo{" tipo" if tipo else ""}" id="acervo">
    <div class="wrap">
      <div class="info">
        <div class="head">
          <img src="/acervo.png" alt="" width="84" height="84">
          <div><p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1></div>
        </div>
        {tag}
        <p class="lead">{e(texto)}</p>
        {P["precos"]}
        {P["lojas"]}
        {links_extra}
      </div>
      <div class="player">
        {P["tela"]}
      </div>
    </div>
"""


def jogos_bloco(cod):
    T = L[cod]; P = PEDACOS[cod]
    itens = "\n".join(f'        <a href="{url_jogo(cod, k)}"><img src="/{ICONE_JOGO[k]}" alt="" width="72" height="72"><span><b>{P["jogos"][k][0]}</b>{e(P["jogos"][k][1])}</span></a>' for k in PASTA_JOGO)
    return f"""  <section class="block">
    <div class="wrap">
      <h2>{e(T["jogos_h2"])}</h2>
      <p class="sub">{e(T["jogos_sub"])}</p>
      <div class="others">
{itens}
      </div>
    </div>
  </section>
"""


def faq_bloco(T, perguntas):
    itens = "\n".join(f'        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in perguntas)
    return f"""  <section class="block">
    <div class="wrap">
      <h2>{e(T["faq_h2"])}</h2>
      <div class="faq">
{itens}
      </div>
    </div>
  </section>
"""


def tipos_bloco(cod, h2, sub, menos=None):
    T = L[cod]
    itens = "\n".join(f'        <a href="{caminho(url_tipo(cod, tid))}"><span class="em">{em}</span><b>{e(T["tipos"][tid]["nome"])}</b></a>' for tid, em, _ in TIPOS if tid != menos)
    sub_html = f'\n      <p class="sub">{e(sub)}</p>' if sub else ""
    return f"""  <section class="block">
    <div class="wrap">
      <h2>{e(h2)}</h2>{sub_html}
      <div class="tipos">
{itens}
      </div>
    </div>
  </section>
"""


def app_ld(cod):
    T = L[cod]
    return {"@type": "MobileApplication", "@id": SITE + "acervo/#app", "name": "Acervo: Sua Coleção", "description": T["desc"],
            "url": url_landing(cod), "image": SITE + "acervo.png", "applicationCategory": "LifestyleApplication",
            "operatingSystem": "iOS, Android", "installUrl": [IOS, ANDROID], "inLanguage": [L[c]["lang"] for c in ORDEM],
            "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"},
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL", "availability": "https://schema.org/InStock"}}


ORG = {"@type": "Organization", "@id": SITE + "#org", "name": "Arial Gamer", "url": SITE, "logo": SITE + "logo-1080.jpg",
       "sameAs": ["https://www.tiktok.com/@arial.gamer", "https://www.instagram.com/arial.gamer/", "https://www.youtube.com/@arialgamer"]}


def faq_ld(perguntas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in perguntas]}


def migalhas_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": (SITE.rstrip("/") + u)} for i, (n, u) in enumerate(crumbs)]}


def salvar(url, conteudo):
    d = os.path.join(RAIZ, *caminho(url).strip("/").split("/")); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(conteudo)
    return caminho(url)


def landing(cod):
    T = L[cod]; P = PEDACOS[cod]; url = url_landing(cod)
    alternos = {c: url_landing(c) for c in ORDEM}
    crumbs = [("Arial Gamer", f"/{pre(cod)}"), ("Acervo", f"/{pre(cod)}acervo/")]
    ld = {"@context": "https://schema.org", "@graph": [ORG, app_ld(cod), migalhas_ld(crumbs), faq_ld(T["faq"])]}
    cards = "\n".join(f'        <article class="reveal"><div class="em">{em}</div><h3>{e(t)}</h3><p>{e(d)}</p></article>' for em, t, d in T["feats"])
    corpo = f"""{nav(cod)}
<main id="topo">
{topo(cod, "Acervo: Sua Coleção" if cod == "pt" else "Acervo", T["lead"], T["eyebrow"], crumbs, f'<a class="more" href="/acervo/privacidade/">{e(T["privacidade"])}</a>')}    {P["telas"]}
  </section>

  <section class="block">
    <div class="wrap">
      <h2>{e(T["feats_h2"])}</h2>
      <p class="sub">{e(T["feats_sub"])}</p>
      <div class="cards">
{cards}
      </div>
    </div>
  </section>

{tipos_bloco(cod, T["tipos_h2"], T["tipos_sub"])}
  <section class="block">
    <div class="wrap">
      <h2>{e(T["planos_h2"])}</h2>
      <p class="sub">{e(T["planos_sub"])}</p>
      <div class="planos">
        <article><h3>{e(T["gratis"][0])}</h3><p>{e(T["gratis"][1])}</p></article>
        <article class="pro"><h3>✨ {e(T["premium"][0])}</h3><p>{e(T["premium"][1])}</p></article>
      </div>
    </div>
  </section>

{faq_bloco(T, T["faq"])}
{jogos_bloco(cod)}</main>

{rodape(cod, alternos)}
{SCRIPT}
</body>
</html>
"""
    titulo = T["titulo"] + " · Arial Gamer"
    return salvar(url, head(cod, titulo, T["desc"], url, alternos, ld, "media/acervo-shot-colecao.jpg") + corpo)


def pagina_tipo(cod, tid, em):
    T = L[cod]; X = T["tipos"][tid]; url = url_tipo(cod, tid)
    alternos = {c: url_tipo(c, tid) for c in ORDEM}
    crumbs = [("Arial Gamer", f"/{pre(cod)}"), ("Acervo", f"/{pre(cod)}acervo/"), (X["nome"], caminho(url))]
    perguntas = [X["faq"]] + T["faq"][:3]
    ld = {"@context": "https://schema.org", "@graph": [ORG, app_ld(cod), migalhas_ld(crumbs), faq_ld(perguntas)]}
    campos = "\n".join(f'          <li><i>{em}</i><span><b>{e(t)}</b>: {e(d)}</span></li>' for t, d in X["campos"])
    ajuda = "\n".join(f'        <article class="reveal"><div class="em">{a}</div><h3>{e(t)}</h3><p>{e(d)}</p></article>' for a, t, d in [T["feats"][1], T["feats"][2], T["feats"][3]])
    corpo = f"""{nav(cod)}
<main id="topo">
{topo(cod, X["h1"], X["intro"], "Acervo: Sua Coleção" if cod == "pt" else "Acervo", crumbs, f'<a class="more" href="/{pre(cod)}acervo/">{e(T["ver_app"])}</a>', tipo=True)}  </section>

  <section class="block">
    <div class="wrap">
      <h2>{e(T["tipo_campos_h2"])}</h2>
      <ul class="feats lista">
{campos}
      </ul>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>{e(T["tipo_ajuda_h2"])}</h2>
      <div class="cards">
{ajuda}
      </div>
    </div>
  </section>

{faq_bloco(T, perguntas)}
{tipos_bloco(cod, T["tipo_outros_h2"], "", menos=tid)}</main>

{rodape(cod, alternos)}
{SCRIPT}
</body>
</html>
"""
    titulo = X["titulo"] + " · Acervo"
    return salvar(url, head(cod, titulo, X["desc"], url, alternos, ld, "media/acervo-shot-colecao.jpg") + corpo)


BAIXAR = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baixar o Acervo: Sua Coleção</title>
<meta name="description" content="Baixe o Acervo: Sua Coleção na App Store ou no Google Play.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITE}acervo/">
<meta property="og:title" content="Acervo: Sua Coleção">
<meta property="og:description" content="O catálogo da sua coleção, com o valor de cada item. Grátis para começar, sem anúncios.">
<meta property="og:image" content="{SITE}media/acervo-shot-colecao.jpg">
<link rel="icon" href="/favicon.png">
<script>
// Abre direto a loja do celular; no computador, mostra os dois botões e o QR code.
(function () {{
  var ua = navigator.userAgent;
  var ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  if (ios) location.replace('{IOS}');
  else if (/Android/.test(ua)) location.replace('{ANDROID}');
}})();
</script>
<style>
:root {{ color-scheme: dark }}
body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: #1B232E; color: #F1E6D3; font: 17px/1.5 system-ui, -apple-system, 'Segoe UI', sans-serif; text-align: center; padding: 24px 16px; box-sizing: border-box }}
main {{ max-width: 420px }}
img.icone {{ width: 96px; height: 96px; border-radius: 22px }}
h1 {{ font-size: 26px; margin: 14px 0 4px }}
p {{ margin: 0 0 22px; color: #D0AC72 }}
a.loja {{ display: block; margin: 10px 0; padding: 14px 18px; border-radius: 14px; background: #F1E6D3; color: #1B232E; font-weight: 700; text-decoration: none }}
img.qr {{ width: 180px; height: 180px; margin-top: 18px; border-radius: 12px; background: #fff; padding: 8px }}
small {{ display: block; color: #9aa5b1; margin-top: 6px }}
</style>
</head>
<body>
<main>
  <img class="icone" src="/acervo.png" alt="">
  <h1>Acervo: Sua Coleção</h1>
  <p>O catálogo da sua coleção, com o valor de cada item</p>
  <a class="loja" href="{IOS}">App Store</a>
  <a class="loja" href="{ANDROID}">Google Play</a>
  <img class="qr" src="/acervo/baixar/qr.png" alt="QR code para baixar o Acervo">
  <small>Aponte a câmera do celular · Point your phone camera</small>
</main>
</body>
</html>
"""


APPS = [  # nome, ícone, App Store, Google Play (None = ainda não saiu)
    ("Acervo: Sua Coleção", "acervo.png", IOS, ANDROID),
    ("Gelada", "gelada.png", "https://apps.apple.com/app/id6819882963", "https://play.google.com/store/apps/details?id=com.arial.gelada"),
    ("Esconde-Esconde", "esconde.png", "https://apps.apple.com/app/id6819893974", "https://play.google.com/store/apps/details?id=com.arial.escondeesconde"),
    ("Gol de Placa", "gol.png", "https://apps.apple.com/app/id6823608331", None),
]
_linhas = "\n".join(
    f'  <div class="app"><img src="/{ic}" alt=""><b>{e(n)}</b>'
    f'<a class="loja ios" href="{a}">App Store</a>'
    + (f'<a class="loja and" href="{g}">Google Play</a>' if g else '<span class="loja and breve">Android: em breve</span>')
    + "</div>" for n, ic, a, g in APPS)
BAIXAR_TODOS = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baixar os apps da Arial Gamer</title>
<meta name="description" content="Acervo, Gelada, Esconde-Esconde e Gol de Placa: baixe na App Store ou no Google Play.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITE}">
<meta property="og:title" content="Apps e jogos da Arial Gamer">
<meta property="og:description" content="Acervo, Gelada, Esconde-Esconde e Gol de Placa. Sem anúncios.">
<meta property="og:image" content="{SITE}logo-1080.jpg">
<link rel="icon" href="/favicon.png">
<style>
:root {{ color-scheme: dark }}
body {{ margin: 0; min-height: 100vh; background: #0d0a20; color: #fff; font: 17px/1.5 system-ui, -apple-system, 'Segoe UI', sans-serif; padding: 28px 16px; box-sizing: border-box }}
main {{ max-width: 460px; margin: 0 auto }}
h1 {{ font-size: 24px; text-align: center; margin: 10px 0 22px }}
.logo {{ display: block; width: 72px; height: 72px; border-radius: 18px; margin: 0 auto }}
.app {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding: 14px; margin: 10px 0; border-radius: 18px; background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.12) }}
.app img {{ width: 52px; height: 52px; border-radius: 13px }}
.app b {{ flex: 1; min-width: 120px }}
.loja {{ padding: 9px 14px; border-radius: 12px; background: #fff; color: #111; font-weight: 700; font-size: 15px; text-decoration: none }}
.breve {{ background: transparent; color: #aab; border: 1px dashed #556 }}
.ios-so .and, .and-so .ios {{ display: none }}
p {{ text-align: center; color: #aab; font-size: 15px }}
p a {{ color: #fff }}
</style>
</head>
<body>
<main>
  <img class="logo" src="/logo.png" alt="">
  <h1>Apps e jogos da Arial Gamer</h1>
{_linhas}
  <p>Sem anúncios em todos. <a href="/">Conheça no site →</a></p>
</main>
<script>
// No iPhone mostra só a App Store; no Android, só o Google Play; no computador, os dois.
var ua = navigator.userAgent;
if (/iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1)) document.body.className = 'ios-so';
else if (/Android/.test(ua)) document.body.className = 'and-so';
</script>
</body>
</html>
"""


if __name__ == "__main__":
    d = os.path.join(RAIZ, "baixar"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(BAIXAR_TODOS)
    feitas = []
    for cod in ORDEM:
        feitas.append(landing(cod))
        for tid, em, _ in TIPOS:
            feitas.append(pagina_tipo(cod, tid, em))
    d = os.path.join(RAIZ, "acervo", "baixar"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(BAIXAR)
    try:
        import qrcode
        qrcode.make(SITE + "acervo/baixar/", border=2).save(os.path.join(d, "qr.png"))
    except ImportError:
        print("aviso: sem a biblioteca qrcode, o qr.png não foi refeito (pip install qrcode)")
    open(os.path.join(RAIZ, "_paginas", "acervo_urls.txt"), "w", encoding="utf-8").write("\n".join(feitas) + "\n")
    print(len(feitas), "páginas + /acervo/baixar/")
