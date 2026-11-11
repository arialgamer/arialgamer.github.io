# Gera as páginas dos 3 jogos nos 8 idiomas (/gelada/, /en/gelada/, /es/gelada/… e o mesmo para esconde-esconde e gol-de-placa)
# e o endereço curto de cada um (/gelada/baixar/…), que abre a loja certa do celular e mostra um QR code no computador.
# Textos em jogos_textos.py; a seção do jogo (lojas, novidades, vídeos), redes, Pix, formulário e rodapé vêm da página
# principal de cada idioma, então mudanças lá aparecem aqui ao rodar de novo:  python _paginas/jogos_paginas.py
# Substitui gerar.py e jogos_en.py para as páginas dos jogos.
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jogos_textos import S, G

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://arialgamer.com.br/"
ORDEM = ["pt", "en", "es", "de", "fr", "it", "ja", "zh"]
LANG = {"pt": "pt-BR", "en": "en", "es": "es", "de": "de", "fr": "fr", "it": "it", "ja": "ja", "zh": "zh-Hans"}
OG = {"pt": "pt_BR", "en": "en_US", "es": "es_ES", "de": "de_DE", "fr": "fr_FR", "it": "it_IT", "ja": "ja_JP", "zh": "zh_CN"}
NOME_IDIOMA = {"pt": "Português", "en": "English", "es": "Español", "de": "Deutsch", "fr": "Français", "it": "Italiano", "ja": "日本語", "zh": "中文"}
# jogo: pasta, nome, ícone, App Store, Google Play (None = ainda não saiu), imagem de capa
JOGOS = {
    "gelada": ("gelada", "Gelada", "gelada.png", "6819882963", "com.arial.gelada", "media/gelada-saude.jpg"),
    "esconde": ("esconde-esconde", "Esconde-Esconde", "esconde.png", "6819893974", "com.arial.escondeesconde", "media/esconde-lua.jpg"),
    "gol": ("gol-de-placa", "Gol de Placa", "gol.png", "6823608331", None, "media/gol-adulta.jpg"),
}
e = html.escape


def ler(p):
    return open(os.path.join(RAIZ, p), encoding="utf-8").read()


def entre(s, ini, fim, incluir_fim=False):
    a = s.index(ini); b = s.index(fim, a)
    return s[a:b + (len(fim) if incluir_fim else 0)]


def pre(cod):
    return "" if cod == "pt" else cod + "/"


def url_jogo(cod, k):
    return f"{SITE}{pre(cod)}{JOGOS[k][0]}/"


def caminho(url):
    return url.replace(SITE, "/")


def absoluto(s):
    """Links relativos da página principal em português (gelada/, media/…) viram absolutos (/gelada/, /media/…)."""
    return re.sub(r'(\s(?:src|href|poster|data-src))="(?!https?:|#|/|mailto:)', r'\1="/', s)


# Visual: o mesmo das páginas atuais dos jogos (CSS e ícones)
_modelo = ler("gelada/index.html")
CSS = entre(_modelo, "<style>", "</style>", True)
SPRITE = entre(_modelo, '<svg width="0"', "</svg>", True)

# Dados fixos de cada jogo (preço, categoria, vídeos) a partir da página em português que já está no ar
FIXO = {}
for _k, (_pasta, *_r) in JOGOS.items():
    _ld = json.loads(entre(ler(f"{_pasta}/index.html"), '<script type="application/ld+json">', "</script>")[len('<script type="application/ld+json">'):])
    _app = next(n for n in _ld["@graph"] if "VideoGame" in str(n["@type"]))
    FIXO[_k] = {"app": _app, "videos": [n for n in _ld["@graph"] if n["@type"] == "VideoObject"]}


def pedacos(cod):
    s = absoluto(ler("index.html" if cod == "pt" else f"{cod}/index.html"))
    P = {"secao": {}, "resumo": {}}
    for k in JOGOS:
        sec = entre(s, f'<section class="game {k}', "</section>", True)
        P["secao"][k] = sec
        P["resumo"][k] = re.sub(r"<[^>]+>", "", re.search(r'<p class="tag">(.*?)</p>', sec).group(1))
    P["resumo"]["acervo"] = re.sub(r"<[^>]+>", "", re.search(r'<p class="tag">(.*?)</p>', entre(s, '<section class="game acervo', "</section>")).group(1))
    navh = entre(s, '<header class="nav"', "</header>", True)
    P["siga"] = re.search(r'<li><a href="#siga">(.*?)</a></li>', navh).group(1)
    P["nav_dir"] = re.search(r'(    <a class="ig-round".*?\n    <a class="pill".*?</a>)', navh, re.S).group(1)
    P["redes"] = entre(s, "  <!-- ================= REDES", "</section>", True)
    P["apoie"] = entre(s, "  <!-- ================= APOIE", "</section>", True)
    P["contato"] = entre(s, "  <!-- ================= COMENTÁRIOS", "</section>", True)
    P["rodape"] = entre(s, "<footer>", "</footer>", True)
    P["script"] = s[s.rindex("<script>"):s.index("</script>", s.rindex("<script>")) + len("</script>")]
    P["som_on"] = re.search(r'<button class="sound" type="button" aria-label="([^"]*)"', s).group(1)
    return P


PED = {cod: pedacos(cod) for cod in ORDEM}


def secao_jogo(cod, k, T):
    sec = PED[cod]["secao"][k]
    sec = re.sub(r'<section class="game ' + k + r'[^"]*"', f'<section class="game solo {k}"', sec, count=1)
    sec = re.sub(r' class="reveal"| class=""', "", sec.replace(' reveal"', '"'))
    sec = re.sub(r"<h2>(.*?)</h2>", r"<h1>\1</h1>", sec, count=1)
    sec = re.sub(r'\n\s*<a class="more"[^\n]*</a>', "", sec)  # "Tudo sobre…" aponta para esta própria página
    return sec


def head(cod, k, T, url, ld):
    pasta, nome, icone, ios, android, capa = JOGOS[k]
    alt = "".join(f'<link rel="alternate" hreflang="{LANG[c]}" href="{url_jogo(c, k)}">\n' for c in ORDEM)
    alt += f'<link rel="alternate" hreflang="x-default" href="{url_jogo("pt", k)}">\n'
    titulo = T["titulo"] + " · Arial Gamer"
    return f"""<!doctype html>
<html lang="{LANG[cod]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-itunes-app" content="app-id={ios}">
<title>{e(titulo)}</title>
<meta name="description" content="{e(T["desc"])}">
<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#0d0a20">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Arial Gamer">
<meta property="og:locale" content="{OG[cod]}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(T["ogdesc"])}">
<meta property="og:image" content="{SITE}{capa}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/{icone}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Figtree:wght@400;500;600;700&display=swap">
{CSS}
</head>
<body class="no-js">
<!-- Página gerada por _paginas/jogos_paginas.py. Não edite à mão. -->

{SPRITE}
"""


def json_ld(cod, k, T, url, crumbs):
    F = FIXO[k]; pasta, nome, icone, ios, android, capa = JOGOS[k]
    app = dict(F["app"])
    app.update({"@id": url + "#app", "name": T["app"], "alternateName": nome, "description": T["desc"], "url": url,
                "genre": T["genero"], "inLanguage": LANG[cod]})
    org = {"@type": "Organization", "@id": SITE + "#org", "name": "Arial Gamer", "url": SITE, "logo": SITE + "logo-1080.jpg",
           "sameAs": ["https://www.tiktok.com/@arial.gamer", "https://www.instagram.com/arial.gamer/", "https://www.youtube.com/@arialgamer"]}
    mig = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE.rstrip("/") + u} for i, (n, u) in enumerate(crumbs)]}
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faq"]]}
    S_ = S[cod]
    assert len(T["videos"]) == len(F["videos"]), (cod, k)
    videos = [dict(v, name=n, description=f'{n}. {S_["video_sfx"]}', inLanguage=LANG[cod], about={"@id": url + "#app"}) for v, n in zip(F["videos"], T["videos"])]
    return {"@context": "https://schema.org", "@graph": [org, app, mig, faq] + videos}


def pagina(cod, k):
    T = G[k][cod]; S_ = S[cod]; P = PED[cod]
    pasta, nome, icone, ios, android, capa = JOGOS[k]
    url = url_jogo(cod, k)
    crumbs = [("Arial Gamer", f"/{pre(cod)}"), (nome, caminho(url))]
    menu = "\n".join(f'      <li><a href="{caminho(url_jogo(cod, j))}"{" aria-current=\"page\"" if j == k else ""}>{JOGOS[j][1]}</a></li>' for j in JOGOS)
    nav = f"""<header class="nav" id="nav">
  <div class="wrap">
    <a class="brand" href="/{pre(cod)}"><img src="/logo.png" alt="" width="38" height="38">Arial Gamer</a>
    <ul>
{menu}
      <li class="app"><a href="/{pre(cod)}acervo/">Acervo</a></li>
      <li><a href="#siga">{P["siga"]}</a></li>
    </ul>
{P["nav_dir"]}
  </div>
</header>
"""
    cards = "\n".join(f'        <article class="reveal"><div class="em">{em}</div><h3>{e(t)}</h3><p>{e(d)}</p></article>' for em, t, d in T["cards"])
    faq = "\n".join(f'        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in T["faq"])
    outros = [(caminho(url_jogo(cod, j)), JOGOS[j][2], JOGOS[j][1], P["resumo"][j]) for j in JOGOS if j != k]
    outros.append((f"/{pre(cod)}acervo/", "acervo.png", "Acervo", P["resumo"]["acervo"]))
    outros_html = "\n".join(f'        <a href="{u}"><img src="/{ic}" alt="" width="72" height="72"><span><b>{n}</b>{e(t)}</span></a>' for u, ic, n, t in outros)
    redes = P["redes"].replace('id="share"><svg><use href="#i-share"/></svg>', 'id="share"><svg><use href="#i-share"/></svg>', 1)
    redes = re.sub(r'(id="share"><svg><use href="#i-share"/></svg>)[^<]*', lambda m: m.group(1) + e(S_["partilhar"]), redes, count=1)
    # rodapé: nota do Gelada só na página do Gelada; idiomas apontam para este jogo; lista de jogos e apps
    rod = P["rodape"]
    if k != "gelada":
        rod = re.sub(r"\n    <span>.*?</span>", "", rod, count=1)
    rod = re.sub(r'\n    <nav aria-label="Jogos">.*?</nav>', "", rod, flags=re.S)
    jogos_nav = "\n".join(f'      <a href="{caminho(url_jogo(cod, j))}">{JOGOS[j][1]}</a>' for j in JOGOS) + f'\n      <a href="/{pre(cod)}acervo/">Acervo</a>'
    idiomas = "\n".join(f'      <a href="{caminho(url_jogo(c, k))}" hreflang="{LANG[c]}" lang="{LANG[c]}"{" aria-current=\"page\"" if c == cod else ""}>{NOME_IDIOMA[c]}</a>' for c in ORDEM)
    rod = re.sub(r'    <nav aria-label="Idioma / Language">.*?</nav>',
                 f'    <nav aria-label="Jogos">\n{jogos_nav}\n    </nav>\n    <nav aria-label="Idioma / Language">\n{idiomas}\n    </nav>', rod, count=1, flags=re.S)
    # script da página principal, com o compartilhar deste jogo e o rótulo do som no idioma certo
    js = P["script"]
    js = re.sub(r"const data = \{ title: 'Arial Gamer', text: '[^']*', url: '[^']*' \};",
                "const data = { title: document.title, text: " + json.dumps(S_["share"].format(n=nome), ensure_ascii=False) + ", url: location.href };", js)
    js = js.replace("video.muted ? 'Ligar o som' : 'Desligar o som'",
                    "video.muted ? " + json.dumps(P["som_on"], ensure_ascii=False) + " : " + json.dumps(S_["som_off"], ensure_ascii=False))
    assert "document.title" in js and S_["som_off"] in js, (cod, k)
    migalhas = f'<li><a href="/{pre(cod)}">Arial Gamer</a></li><li aria-current="page">{nome}</li>'
    corpo = f"""{nav}
<main id="topo">
  <nav class="crumbs" aria-label="{e(S_["aqui"])}"><div class="wrap"><ol>{migalhas}</ol></div></nav>

  {secao_jogo(cod, k, T)}

  <section class="block">
    <div class="wrap">
      <h2>{e(T["como_h2"])}</h2>
      <p class="sub">{e(T["como_sub"])}</p>
      <div class="cards">
{cards}
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>{e(S_["faq_h2"])}</h2>
      <p class="sub">{e(T["faq_sub"])}</p>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>{e(S_["outros_h2"])}</h2>
      <p class="sub">{e(S_["outros_sub"])}</p>
      <div class="others">
{outros_html}
      </div>
    </div>
  </section>

{redes}

{P["apoie"]}

{P["contato"]}
</main>

{rod}

{js}
</body>
</html>
"""
    conteudo = head(cod, k, T, url, json_ld(cod, k, T, url, crumbs)) + corpo
    d = os.path.join(RAIZ, *caminho(url).strip("/").split("/")); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(conteudo)
    return caminho(url)


def baixar(k):
    pasta, nome, icone, ios_id, android_id, capa = JOGOS[k]
    ios = "https://apps.apple.com/app/id" + ios_id
    android = f"https://play.google.com/store/apps/details?id={android_id}" if android_id else None
    T = G[k]["pt"]
    redir_and = f"\n  else if (/Android/.test(ua)) location.replace('{android}');" if android else ""
    botao_and = f'<a class="loja" href="{android}">Google Play</a>' if android else '<span class="loja breve">Android: em breve · coming soon</span>'
    pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baixar o {nome}</title>
<meta name="description" content="Baixe o {nome} na App Store{' ou no Google Play' if android else ''}.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITE}{pasta}/">
<meta property="og:title" content="{e(T["app"])}">
<meta property="og:description" content="{e(T["ogdesc"])}">
<meta property="og:image" content="{SITE}{capa}">
<link rel="icon" href="/favicon.png">
<script>
// Abre direto a loja do celular; no computador, mostra os botões e o QR code.
(function () {{
  var ua = navigator.userAgent;
  if (/iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1)) location.replace('{ios}');{redir_and}
}})();
</script>
<style>
:root {{ color-scheme: dark }}
body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: #0d0a20; color: #fff; font: 17px/1.5 system-ui, -apple-system, 'Segoe UI', sans-serif; text-align: center; padding: 24px 16px; box-sizing: border-box }}
main {{ max-width: 420px }}
img.icone {{ width: 96px; height: 96px; border-radius: 22px }}
h1 {{ font-size: 26px; margin: 14px 0 4px }}
p {{ margin: 0 0 22px; color: #c9c3e6 }}
.loja {{ display: block; margin: 10px 0; padding: 14px 18px; border-radius: 14px; background: #fff; color: #111; font-weight: 700; text-decoration: none }}
.breve {{ background: transparent; color: #aab; border: 1px dashed #556 }}
img.qr {{ width: 180px; height: 180px; margin-top: 18px; border-radius: 12px; background: #fff; padding: 8px }}
small {{ display: block; color: #9aa5b1; margin-top: 6px }}
small a {{ color: #fff }}
</style>
</head>
<body>
<main>
  <img class="icone" src="/{icone}" alt="">
  <h1>{nome}</h1>
  <p>{e(PED["pt"]["resumo"][k])}</p>
  <a class="loja" href="{ios}">App Store</a>
  {botao_and}
  <img class="qr" src="/{pasta}/baixar/qr.png" alt="QR code para baixar o {nome}">
  <small>Aponte a câmera do celular · Point your phone camera</small>
  <small><a href="/{pasta}/">Conheça o {nome} →</a></small>
</main>
</body>
</html>
"""
    d = os.path.join(RAIZ, pasta, "baixar"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(pagina)
    try:
        import qrcode
        qrcode.make(f"{SITE}{pasta}/baixar/", border=2).save(os.path.join(d, "qr.png"))
    except ImportError:
        print("aviso: sem a biblioteca qrcode, o qr.png não foi refeito (pip install qrcode)")


if __name__ == "__main__":
    feitas = [pagina(cod, k) for k in JOGOS for cod in ORDEM]
    for k in JOGOS:
        baixar(k)
    open(os.path.join(RAIZ, "_paginas", "jogos_urls.txt"), "w", encoding="utf-8").write("\n".join(feitas) + "\n")
    print(len(feitas), "páginas + 3 endereços /baixar/")
