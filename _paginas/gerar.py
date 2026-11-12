# Gera as páginas de cada jogo (/gelada/, /esconde-esconde/, /gol-de-placa/) a partir do index.html.
# Rode de novo depois de mudar o index.html:  python _paginas/gerar.py
# (Pastas que começam com "_" não são publicadas pelo GitHub Pages.)
import json, os, re, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://arialgamer.com.br/"
idx = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()

def entre(ini, fim, s=idx):
    a = s.index(ini); b = s.index(fim, a)
    return s[a:b]

css = entre("<style>", "</style>")[len("<style>"):]
sprite = entre('<svg width="0"', "</svg>") + "</svg>"
social = entre('  <!-- ================= REDES', "</main>")
footer = entre("<footer>", "</footer>") + "</footer>"
script = entre("<script>\ndocument.body", "</script>") + "</script>"
secoes = {
    "gelada": entre("  <section class=\"game gelada\"", "  <!-- ================= ESCONDE"),
    "esconde": entre("  <section class=\"game esconde", "  <!-- ================= GOL"),
    "gol": entre("  <section class=\"game gol\"", "  <!-- ================= REDES"),
}

def absoluto(s):
    # caminhos relativos viram absolutos (as páginas ficam em subpastas)
    return re.sub(r'(\s(?:src|poster|data-src|href))="(?!https?:|#|/|mailto:)', r'\1="/', s)

CSS_EXTRA = """
.crumbs { padding: calc(96px + env(safe-area-inset-top, 0px)) 0 0; font-size: 14px; color: var(--muted) }
.crumbs ol { list-style: none; display: flex; flex-wrap: wrap; gap: 8px; margin: 0; padding: 0 }
.crumbs li + li::before { content: "›"; margin-right: 8px; opacity: .6 }
.crumbs a { text-decoration: none } .crumbs a:hover { color: var(--ink) }
.game.solo { padding-top: 40px }
.info h1 { font-size: clamp(44px, 6vw, 72px); font-weight: 800 }
.block { padding: 80px 0; border-top: 1px solid var(--line) }
.block h2 { font-size: clamp(32px, 4.4vw, 48px); font-weight: 800; margin-bottom: 10px }
.block .sub { color: var(--muted); margin: 0 0 34px; max-width: 60ch; font-size: 18px }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px }
.cards article { padding: 22px; border-radius: 20px; background: var(--glass); border: 1px solid var(--line) }
.cards h3 { font-size: 22px; margin: 10px 0 6px }
.cards p { margin: 0; color: var(--muted); font-size: 16px; line-height: 1.5 }
.cards .em { font-size: 30px; line-height: 1 }
.faq { display: grid; gap: 10px; max-width: 860px }
.faq details { border-radius: 16px; background: var(--glass); border: 1px solid var(--line); padding: 0 20px }
.faq summary { cursor: pointer; font-weight: 700; font-size: 18px; padding: 18px 0; list-style: none; display: flex; justify-content: space-between; gap: 16px }
.faq summary::-webkit-details-marker { display: none }
.faq summary::after { content: "+"; font-size: 24px; line-height: 1; color: var(--muted); transition: transform .2s }
.faq details[open] summary::after { transform: rotate(45deg) }
.faq details p { margin: 0 0 18px; color: var(--muted) }
.others { display: grid; grid-template-columns: 1fr 1fr; gap: 14px }
.others a { display: flex; align-items: center; gap: 18px; padding: 18px; border-radius: 20px; background: var(--glass); border: 1px solid var(--line); text-decoration: none; transition: transform .2s, background .2s }
.others a:hover { transform: translateY(-2px); background: var(--glass-2) }
.others img { width: 72px; height: 72px; border-radius: 18px; flex: none }
.others b { display: block; font-family: var(--display); font-size: 24px; line-height: 1.1 }
.others span { color: var(--muted); font-size: 15px }
.nav a[aria-current="page"] { color: var(--ink); text-decoration: underline; text-underline-offset: 6px }
@media (max-width: 860px) {
  .cards { grid-template-columns: 1fr }
  .others { grid-template-columns: 1fr }
  .block { padding: 60px 0 }
}
"""

JOGOS = {
  "gelada": dict(
    pasta="gelada", nome="Gelada", nome_loja="Gelada: Bebidas Virtuais", icone="gelada.png",
    titulo="Gelada: simulador de cerveja e drinks no celular · Arial Gamer",
    descricao="Gelada transforma o celular num copo: encha de cerveja, vinho, drinks ou café, incline para beber e invente misturas. 100 bebidas, barman que fala e drink do dia. R$ 1,90 no iPhone e no Android. Sem anúncios. 0% álcool.",
    resumo="Cerveja, vinho, drinks e café no celular. Incline para beber e misture.",
    categoria="Simulação, Casual", os="iOS, Android", imagem="media/gelada-saude.jpg",
    lojas=["https://apps.apple.com/br/app/id6819882963", "https://play.google.com/store/apps/details?id=com.arial.gelada"],
    videos=[("gelada-saude", "Gelada: cerveja enchendo e sendo bebida no celular"), ("gelada-cuba-libre", "Gelada: Cuba Libre ganha nota 10"),
            ("gelada-caipirinha", "Gelada: caipirinha servida no balcão"), ("gelada-talhou", "Gelada: leite com suco de laranja talhou")],
    como_titulo="Como é o Gelada",
    como_sub="Lembra do app em que o celular virava um copo de cerveja? O Gelada traz a ideia de volta, muito mais completo.",
    cards=[("🍺", "Incline para beber", "A tela vira um copo. O líquido acompanha o celular, com ondas, bolhas e espuma. Leve o topo à boca e beba, com som de gole e vibração."),
           ("🍹", "100 bebidas", "Cervejas, vinhos, espumantes, coquetéis como mojito e caipirinha, e mais de 40 sem álcool: sucos, refrigerantes, cafés e chás."),
           ("🧪", "Modo misturar", "Combine até 4 bebidas. A ordem muda o resultado, como na vida real, e receitas clássicas como Cuba Libre e Gin Tônica são reconhecidas."),
           ("⭐", "Nota da mistura", "Cada mistura ganha nota de 0 a 10, com sabor e proporção. Leite com laranja? Talha. Três destilados juntos? Bomba!"),
           ("🗣️", "Barman que fala", "Um barman (ou uma barwoman) comenta suas misturas, comemora o brinde e te desafia, em 8 idiomas."),
           ("🎬", "Vídeo de pegadinha", "Grave o copo enchendo e mande para os amigos como se fosse de verdade.")],
    faq=[("O Gelada tem álcool de verdade?", "Não. As bebidas são 100% virtuais: é uma brincadeira no celular, com 0% de álcool. Beba com moderação na vida real."),
         ("Quanto custa?", "R$ 1,90 para baixar, no iPhone e no Android. Não tem anúncios nem assinatura."),
         ("Tem bebidas sem álcool?", "Sim, mais de 40: sucos como caju, açaí e acerola, refrigerantes, cafés, chás, caldo de cana, milkshake e vitamina. Menores de 18 anos veem só as sem álcool, e o responsável pode liberar as outras com um PIN."),
         ("Precisa de internet ou cadastro?", "Não. O Gelada funciona offline, sem cadastro, e não coleta dados."),
         ("Em quais idiomas?", "Português, inglês, espanhol, alemão, francês, italiano, chinês e japonês.")]),
  "esconde": dict(
    pasta="esconde-esconde", nome="Esconde-Esconde", nome_loja="Esconde-Esconde", icone="esconde.png",
    titulo="Esconde-Esconde: jogo de esconde-esconde para celular · Arial Gamer",
    descricao="Esconde-Esconde para celular: 22 lugares de dia e de noite, contra a máquina, passando o celular ou online com um amigo. Narrador, radar quente ou frio e modo para os pequenos. R$ 1,90 no iPhone e no Android. Sem anúncios.",
    resumo="Esconda-se e tente achar, contra a máquina ou um amigo.",
    categoria="Família, Casual", os="iOS, Android", imagem="media/esconde-lua.jpg",
    lojas=["https://apps.apple.com/br/app/id6819893974", "https://play.google.com/store/apps/details?id=com.arial.escondeesconde"],
    videos=[("esconde-lua", "Esconde-Esconde: escondido na lua"), ("esconde-maquina", "Esconde-Esconde: jogando contra a máquina"),
            ("esconde-pirata", "Esconde-Esconde: navio pirata"), ("esconde-geleira", "Esconde-Esconde: geleira"),
            ("esconde-dia-noite", "Esconde-Esconde: o mesmo lugar de dia e de noite")],
    como_titulo="Como é o Esconde-Esconde",
    como_sub="A brincadeira de sempre, feita para o celular: esconda-se, passe o aparelho e veja se a outra pessoa te encontra.",
    cards=[("☀️", "Dia e noite", "De dia tudo fica visível. À noite as luzes apagam e você procura com uma lanterna. A lua muda de fase como no céu de verdade."),
           ("👂", "Ouça os barulhinhos", "Quem se esconde às vezes se mexe e aparecem ondinhas de som. Mas pode ser a isca, a vaca do sítio ou o papagaio do navio!"),
           ("📡", "Radar quente ou frio", "O celular vibra mais forte quando você chega perto do esconderijo."),
           ("🤖", "A máquina aprende", "Três níveis de dificuldade. A máquina lembra onde você costuma se esconder e onde costuma procurar."),
           ("🎉", "Festa de 3 ou 4", "Passe o celular: cada um se esconde uma vez por rodada, e no fim tem classificação com medalhas."),
           ("🌧️", "Chuva e relâmpagos", "Às vezes chove e os barulhos ficam abafados. À noite, os relâmpagos iluminam tudo por um instante.")],
    faq=[("Quanto custa o Esconde-Esconde?", "R$ 1,90 para baixar, no iPhone e no Android. Não tem anúncios nem assinatura."),
         ("Dá para jogar com outra pessoa?", "Sim: passando o mesmo celular, em festa de 3 ou 4 pessoas, ou online com um amigo, cada um no seu celular, com código de sala."),
         ("É bom para crianças?", "Sim. É um jogo para a família, tem modo para os pequenos e narrador que conta tudo, sem anúncios."),
         ("Quais lugares tem?", "São 22, como casa, praia, sítio, geleira, navio pirata, estação espacial, castelo, terra dos dinossauros, circo e museu, todos de dia e de noite."),
         ("Precisa de cadastro?", "Não. O jogo não pede cadastro e não coleta dados.")]),
  "gol": dict(
    pasta="gol-de-placa", nome="Gol de Placa", nome_loja="Gol de Placa: Pênalti e Falta", icone="gol.png",
    titulo="Gol de Placa: jogo de pênalti e falta para celular · Arial Gamer",
    descricao="Gol de Placa: pênaltis e faltas em 3D no celular. Bata no ângulo ou seja o goleiro, monte o seu craque e jogue online com um amigo. Seleções, times, chuva, neve e narração. R$ 1,90 no iPhone. Sem anúncios.",
    resumo="Pênaltis e faltas em 3D: seja o batedor ou o goleiro.",
    categoria="Esporte, Futebol", os="iOS", imagem="media/gol-adulta.jpg",
    lojas=["https://apps.apple.com/br/app/id6823608331"],
    videos=[("gol-adulta", "Gol de Placa: versão adulta, com jogadores e torcida realistas"), ("gol-penalti", "Gol de Placa: cobrança de pênalti"), ("gol-falta-neve", "Gol de Placa: gol de falta na neve"),
            ("gol-defesa-chuva", "Gol de Placa: defesa do goleiro na chuva"), ("gol-noite", "Gol de Placa: gol à noite"),
            ("gol-craque", "Gol de Placa: montando o seu craque")],
    como_titulo="Como é o Gol de Placa",
    como_sub="Arraste o dedo da bola até o canto do gol e solte o chute. Ou vá para o gol e tente defender.",
    cards=[("⚽", "Chute de verdade", "A bola vai para onde você mirar: no ângulo, rasteira ou com curva para contornar a barreira. Bate na trave e estufa a rede."),
           ("🧤", "Ou seja o goleiro", "Toque no gol para pular. O goleiro mergulha, salta e encaixa a bola."),
           ("🏆", "Copa", "Quartas, semifinal e final em disputas de pênaltis, com morte súbita e taça no final."),
           ("🧑", "Monte o seu craque", "Pele, cabelo, chuteira, número e nome na camisa, e a comemoração: aviãozinho, dancinha, cambalhota…"),
           ("🌦️", "Clima e torcida", "Dia, noite com refletores, chuva e neve. Torcida com batucada, a ola e festa no gol."),
           ("📒", "Figurinhas e desafios", "Figurinhas para colecionar e desafios novos todo dia.")],
    faq=[("Quanto custa o Gol de Placa?", "R$ 1,90 para baixar na App Store. Não tem anúncios nem assinatura."),
         ("Tem para Android?", "Ainda não. A versão para Android está chegando; siga @arial.gamer para saber quando sair."),
         ("Dá para jogar com um amigo?", "Sim, online, cada um no seu celular."),
         ("É bom para crianças?", "Sim. É um jogo para a família, com bonecos de blocos, sem violência e sem anúncios. Também tem versão adulta, com jogadores realistas."),
         ("Precisa de cadastro?", "Não. O jogo não pede cadastro e não coleta dados.")]),
}
ORDEM = ["gelada", "esconde", "gol"]

def duracao(arq):
    # lê a duração do mp4 (caixa mvhd), sem precisar do ffmpeg
    b = open(os.path.join(RAIZ, "media", arq + ".mp4"), "rb").read()
    i = b.index(b"mvhd"); v = b[i + 4]
    if v == 1: esc = int.from_bytes(b[i + 24:i + 28], "big"); dur = int.from_bytes(b[i + 28:i + 36], "big")
    else: esc = int.from_bytes(b[i + 16:i + 20], "big"); dur = int.from_bytes(b[i + 20:i + 24], "big")
    s = round(dur / esc); return f"PT{s // 60}M{s % 60}S"

def jsonld(k, j):
    url = SITE + j["pasta"] + "/"
    app = {"@type": ["MobileApplication", "VideoGame"], "@id": url + "#app", "name": j["nome_loja"], "alternateName": j["nome"],
           "description": j["descricao"], "url": url, "image": SITE + j["icone"], "screenshot": SITE + j["imagem"],
           "applicationCategory": "GameApplication", "genre": j["categoria"], "operatingSystem": j["os"], "inLanguage": "pt-BR",
           "installUrl": j["lojas"], "downloadUrl": j["lojas"],
           "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"},
           "offers": {"@type": "Offer", "price": "1.90", "priceCurrency": "BRL", "availability": "https://schema.org/InStock"}}
    org = {"@type": "Organization", "@id": SITE + "#org", "name": "Arial Gamer", "url": SITE, "logo": SITE + "logo-1080.jpg",
           "sameAs": ["https://www.tiktok.com/@arial.gamer", "https://www.instagram.com/arial.gamer/", "https://www.youtube.com/@arialgamer"]}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Arial Gamer", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": j["nome"], "item": url}]}
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in j["faq"]]}
    vids = [{"@type": "VideoObject", "name": n, "description": n + ". Vídeo gravado no jogo.", "thumbnailUrl": SITE + f"media/{v}.jpg",
             "contentUrl": SITE + f"media/{v}.mp4", "uploadDate": "2026-11-05", "duration": duracao(v), "inLanguage": "pt-BR",
             "about": {"@id": url + "#app"}} for v, n in j["videos"]]
    return json.dumps({"@context": "https://schema.org", "@graph": [org, app, crumbs, faq] + vids}, ensure_ascii=False, indent=1)

def nav(atual):
    itens = "".join(f'      <li><a href="/{JOGOS[k]["pasta"]}/"{" aria-current=\"page\"" if k == atual else ""}>{JOGOS[k]["nome"]}</a></li>\n' for k in ORDEM)
    return f"""<header class="nav" id="nav">
  <div class="wrap">
    <a class="brand" href="/"><img src="/logo.png" alt="" width="38" height="38">Arial Gamer</a>
    <ul>
{itens}      <li><a href="#siga">Redes</a></li>
    </ul>
    <a class="ig-round" href="https://www.instagram.com/arial.gamer/" target="_blank" rel="noopener" aria-label="Instagram @arial.gamer"><svg><use href="#i-insta"/></svg></a>
    <a class="pill" href="https://www.tiktok.com/@arial.gamer" target="_blank" rel="noopener"><svg><use href="#i-tiktok"/></svg>Seguir</a>
  </div>
  <script src="/contador.js" defer></script>
</header>"""

def pagina(k):
    j = JOGOS[k]; url = SITE + j["pasta"] + "/"; e = html.escape
    sec = secoes[k]
    sec = re.sub(r"\s*<a class=\"more\"[^>]*>.*?</a>", "", sec)          # link "página do jogo" só existe na principal
    sec = sec.replace('<h2>', '<h1>', 1).replace('</h2>', '</h1>', 1)
    sec = sec.replace('class="game ', 'class="game solo ', 1).replace(' flip"', '"', 1)
    sec = sec.replace(' reveal"', '"').replace('"reveal"', '""')         # topo da página aparece sem animação
    cards = "\n".join(f'        <article class="reveal"><div class="em">{em}</div><h3>{e(t)}</h3><p>{e(d)}</p></article>' for em, t, d in j["cards"])
    faq = "\n".join(f'        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in j["faq"])
    outros = "\n".join(f'        <a href="/{JOGOS[o]["pasta"]}/"><img src="/{JOGOS[o]["icone"]}" alt="" width="72" height="72"><span><b>{JOGOS[o]["nome"]}</b>{e(JOGOS[o]["resumo"])}</span></a>' for o in ORDEM if o != k)
    scr = script.replace("'https://arialgamer.com.br/'", "location.href").replace(
        "'Olha esses jogos: Gelada, Esconde-Esconde e Gol de Placa 🎮'", repr(f"Olha esse jogo: {j['nome']} 🎮"))
    soc = social.replace("Compartilhar o site", "Compartilhar este jogo")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(j["titulo"])}</title>
<meta name="description" content="{e(j["descricao"])}">
<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-BR" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}en/{j["pasta"]}/">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#0d0a20">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Arial Gamer">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(j["titulo"])}">
<meta property="og:description" content="{e(j["resumo"])} Veja os vídeos e baixe.">
<meta property="og:image" content="{SITE}{j["imagem"]}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{jsonld(k, j)}
</script>
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/{j["icone"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Figtree:wght@400;500;600;700&display=swap">
<style>{css}{CSS_EXTRA}</style>
</head>
<body class="no-js">
<!-- Página gerada por _paginas/gerar.py a partir do index.html. Não edite à mão. -->

{sprite}

{nav(k)}

<main id="topo">
  <nav class="crumbs" aria-label="Você está em"><div class="wrap"><ol><li><a href="/">Arial Gamer</a></li><li aria-current="page">{j["nome"]}</li></ol></div></nav>

{absoluto(sec)}
  <section class="block">
    <div class="wrap">
      <h2>{e(j["como_titulo"])}</h2>
      <p class="sub">{e(j["como_sub"])}</p>
      <div class="cards">
{cards}
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>Perguntas frequentes</h2>
      <p class="sub">Tudo o que perguntam sobre o {e(j["nome"])}.</p>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>Outros jogos da Arial Gamer</h2>
      <p class="sub">Também por R$ 1,90 e sem anúncios.</p>
      <div class="others">
{outros}
      </div>
    </div>
  </section>

{absoluto(soc)}</main>

{absoluto(footer)}

{scr}
</body>
</html>
"""

for k in ORDEM:
    d = os.path.join(RAIZ, JOGOS[k]["pasta"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(pagina(k))
    print("ok", JOGOS[k]["pasta"])
