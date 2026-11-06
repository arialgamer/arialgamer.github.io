# Gera o site em inglês (/en/) e em espanhol (/es/) a partir do index.html em português.
# Rode de novo depois de mudar o index.html:  python _paginas/idiomas.py
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idiomas_mais import IDIOMAS_MAIS, TRAD, TRAD_LUG, DIA_NOITE

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://arialgamer.com.br/"
pt = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()

# ---------- textos (português, inglês, espanhol) ----------
T = [
 ("Redes", "Social", "Redes"),
 ("Seguir", "Follow", "Seguir"),
 ("Jogos para celular", "Mobile games", "Juegos para móvil"),
 ("feitos no Brasil", "made in Brazil", "hechos en Brasil"),
 ("Encha um copo e incline para beber. Esconda-se até atrás da lua. Bata o pênalti ou defenda no último minuto. Três jogos para jogar sozinho ou com um amigo.",
  "Fill a glass and tilt to drink. Hide behind the moon. Take the penalty or save it in the last minute. Three games to play alone or with a friend.",
  "Llena un vaso e inclina para beber. Escóndete detrás de la luna. Patea el penal o atájalo en el último minuto. Tres juegos para jugar solo o con un amigo."),
 ("Conhecer os jogos", "See the games", "Ver los juegos"),
 ("Ver no TikTok", "Watch on TikTok", "Ver en TikTok"),
 ("Vídeos dos três jogos", "Videos of the three games", "Videos de los tres juegos"),
 ("Gelada: cerveja enchendo e sendo bebida no celular", "Gelada: beer filling up and being drunk on the phone", "Gelada: cerveza llenándose y bebida en el móvil"),
 ("Gol de Placa: cobrança de pênalti", "Gol de Placa: penalty kick", "Gol de Placa: cobro de penal"),
 ("Esconde-Esconde: escondido na estação espacial", "Esconde-Esconde: hiding on the space station", "Esconde-Esconde: escondido en la estación espacial"),
 ("jogos no ar", "games out now", "juegos disponibles"),
 ("cada jogo", "languages in each game", "idiomas en cada juego"),
 ("bebidas no Gelada", "drinks in Gelada", "bebidas en Gelada"),
 ("lugares no Esconde-Esconde", "places in Esconde-Esconde", "lugares en Esconde-Esconde"),
 ("Ícone do Gelada", "Gelada icon", "Ícono de Gelada"),
 ("Bebidas virtuais", "Virtual drinks", "Bebidas virtuales"),
 ("Cerveja, drinks e até café no seu celular. Encha o copo e incline para beber 🍺", "Beer, cocktails and even coffee on your phone. Fill the glass and tilt to drink 🍺", "Cerveza, cócteles y hasta café en tu móvil. Llena el vaso e inclina para beber 🍺"),
 ("100 bebidas", "100 drinks", "100 bebidas"),
 (": cervejas, vinhos, drinks e cafés", ": beers, wines, cocktails and coffees", ": cervezas, vinos, cócteles y cafés"),
 ("Barman que fala", "Talking bartender", "Barman que habla"),
 ("e nota de 0 a 10 para a sua mistura", "and a 0–10 score for your mix", "y nota de 0 a 10 para tu mezcla"),
 ("Drink do dia", "Drink of the day", "Trago del día"),
 (": uma receita nova para provar", ": a new recipe to try", ": una receta nueva para probar"),
 ("Incline o celular", "Tilt your phone", "Inclina el móvil"),
 ("e beba de verdade, sem álcool", "and drink for real, alcohol-free", "y bebe de verdad, sin alcohol"),
 ("Em dezembro:", "In December:", "En diciembre:"),
 ("edição de Natal, com Gemada e Ponche 🎄", "Christmas edition, with eggnog and punch 🎄", "edición de Navidad, con rompope y ponche 🎄"),
 ("Baixar na", "Download on the", "Descárgalo en"),
 ("Disponível no", "Get it on", "Disponible en"),
 ("Ligar o som", "Turn sound on", "Activar sonido"),
 ("Escolha um vídeo do Gelada", "Pick a Gelada video", "Elige un video de Gelada"),
 ("Saúde!", "Cheers!", "¡Salud!"),
 ("Nota 10", "Perfect 10", "Nota 10"),
 ("Talhou!", "Curdled!", "¡Se cortó!"),
 ("Ícone do Esconde-Esconde", "Esconde-Esconde icon", "Ícono de Esconde-Esconde"),
 ("Para a família", "For the family", "Para la familia"),
 ("Esconda-se e tente achar, contra a máquina ou um amigo 🙈", "Hide and seek against the computer or a friend 🙈", "Escóndete y busca, contra la máquina o un amigo 🙈"),
 ("Online com um amigo", "Online with a friend", "Online con un amigo"),
 (", cada um no seu celular, com código de sala", ", each on their own phone, with a room code", ", cada uno en su móvil, con código de sala"),
 ("22 lugares", "22 places", "22 lugares"),
 (": praia, geleira, navio pirata, estação espacial…", ": beach, glacier, pirate ship, space station…", ": playa, glaciar, barco pirata, estación espacial…"),
 ("Radar quente ou frio", "Hot or cold radar", "Radar frío o caliente"),
 (", do jeito que você preferir", ", the way you like it", ", como prefieras"),
 ("Modo para os pequenos", "Mode for little ones", "Modo para los pequeños"),
 ("e narrador que conta tudo", "and a narrator who tells you everything", "y narrador que lo cuenta todo"),
 ("Chegando:", "Coming soon:", "Muy pronto:"),
 ("os 22 lugares liberados para quem baixa, sem compras dentro do app", "all 22 places unlocked with the download, no in-app purchases", "los 22 lugares incluidos en la descarga, sin compras dentro de la app"),
 ("Escolha um vídeo do Esconde-Esconde", "Pick an Esconde-Esconde video", "Elige un video de Esconde-Esconde"),
 ("Na lua", "On the moon", "En la luna"),
 ("Contra a máquina", "Against the computer", "Contra la máquina"),
 ("Navio pirata", "Pirate ship", "Barco pirata"),
 ("Geleira", "Glacier", "Glaciar"),
 ("Dia e noite", "Day and night", "Día y noche"),
 ("Lugares para se esconder, de dia ou de noite", "Places to hide, by day or by night", "Lugares para esconderse, de día o de noche"),
 ("Ícone do Gol de Placa", "Gol de Placa icon", "Ícono de Gol de Placa"),
 ("Novo jogo", "New game", "Juego nuevo"),
 ("Pênaltis e faltas: seja o batedor ou o goleiro ⚽🧤", "Penalties and free kicks: be the kicker or the goalkeeper ⚽🧤", "Penales y tiros libres: sé el pateador o el portero ⚽🧤"),
 ("e goleiro elástico", "and a stretchy goalkeeper", "y portero elástico"),
 ("Seleções e times", "National teams and clubs", "Selecciones y clubes"),
 (", com torcida realista", ", with realistic fans", ", con hinchada realista"),
 ("Chuva, neve e noite", "Rain, snow and night", "Lluvia, nieve y noche"),
 ("no estádio", "at the stadium", "en el estadio"),
 ("Narrador em 14 idiomas", "Commentary in 14 languages", "Narrador en 14 idiomas"),
 ("e versão adulta", "and a grown-up version", "y versión adulta"),
 ("De 14/11 a 13/12:", "Nov 14 to Dec 13:", "Del 14/11 al 13/12:"),
 ("evento Pênaltis da Copa, temporada das finais 🏆", "Cup Penalties event, finals season 🏆", "evento Penales de la Copa, temporada de finales 🏆"),
 ("tudo liberado para quem baixa (faltas, goleiro, seleções, times e torneio), sem compras dentro do app", "everything unlocked with the download (free kicks, goalkeeper, teams and tournament), no in-app purchases", "todo incluido en la descarga (tiros libres, portero, selecciones, clubes y torneo), sin compras dentro de la app"),
 ("100 conquistas no Game Center, uma para cada figurinha do álbum 🏅", "100 Game Center achievements, one for each sticker in the album 🏅", "100 logros en Game Center, uno por cada figurita del álbum 🏅"),
 ("Em breve", "Coming soon", "Muy pronto"),
 ("Escolha um vídeo do Gol de Placa", "Pick a Gol de Placa video", "Elige un video de Gol de Placa"),
 ("Versão adulta", "Grown-up version", "Versión adulta"),
 ("Pênalti", "Penalty", "Penal"),
 ("Falta na neve", "Free kick in the snow", "Tiro libre en la nieve"),
 ("Defesa na chuva", "Save in the rain", "Atajada bajo la lluvia"),
 ("Gol à noite", "Night goal", "Gol de noche"),
 ("Meu craque", "My player", "Mi crack"),
 ("Tela Meu craque: cabelo, chuteira, comemoração, número 10 e nome Arial na camisa", "My player screen: hair, boots, celebration, number 10 and the name Arial on the shirt", "Pantalla Mi crack: pelo, botines, festejo, número 10 y el nombre Arial en la camiseta"),
 ("Monte o seu craque", "Build your player", "Crea tu crack"),
 ("Jogadora comemora gol à noite e ganha a figurinha Gol à noite", "A player celebrates a night goal and earns the Night goal sticker", "Una jugadora festeja un gol de noche y gana la figurita Gol de noche"),
 ("Gol! E figurinha nova", "Goal! And a new sticker", "¡Gol! Y figurita nueva"),
 ("Cobrança de falta com barreira e neve no gramado", "Free kick with a wall and snow on the pitch", "Tiro libre con barrera y nieve en la cancha"),
 ("Falta com barreira, na neve", "Free kick with a wall, in the snow", "Tiro libre con barrera, en la nieve"),
 ("Goleiro se esticando para defender na chuva", "Goalkeeper stretching to save in the rain", "Portero estirándose para atajar bajo la lluvia"),
 ("Agora defenda!", "Now save it!", "¡Ahora ataja!"),
 ("Redes sociais", "Social media", "Redes sociales"),
 ("Siga a Arial Gamer", "Follow Arial Gamer", "Sigue a Arial Gamer"),
 ("Desafios, novidades e bastidores dos jogos no TikTok, no Instagram e no YouTube. Conseguiu achar onde a gente se escondeu? Responde nos comentários.",
  "Challenges, news and behind the scenes on TikTok, Instagram and YouTube. Found where we were hiding? Tell us in the comments.",
  "Desafíos, novedades y detrás de escena en TikTok, Instagram y YouTube. ¿Encontraste dónde nos escondimos? Cuéntanos en los comentarios."),
 ("Compartilhar o site", "Share the site", "Compartir el sitio"),
 ("Vídeo do Esconde-Esconde no TikTok", "Esconde-Esconde video on TikTok", "Video de Esconde-Esconde en TikTok"),
 ("Vídeo do Gelada no TikTok", "Gelada video on TikTok", "Video de Gelada en TikTok"),
 ("Vídeo do Gol de Placa no TikTok", "Gol de Placa video on TikTok", "Video de Gol de Placa en TikTok"),
 ("Gelada: bebidas 100% virtuais, 0% álcool. Beba com moderação.", "Gelada: 100% virtual drinks, 0% alcohol. Drink responsibly.", "Gelada: bebidas 100% virtuales, 0% alcohol. Bebe con moderación."),
 ("Privacidade", "Privacy", "Privacidad"),
 ("Privacidade Gelada", "Gelada privacy", "Privacidad Gelada"),
 ("Privacidade Esconde-Esconde", "Esconde-Esconde privacy", "Privacidad Esconde-Esconde"),
 ("Privacidade Gol de Placa", "Gol de Placa privacy", "Privacidad Gol de Placa"),
]
LUGARES = [("Casa", "House", "Casa"), ("Praia", "Beach", "Playa"), ("Sítio", "Farm", "Granja"), ("Acampamento", "Campsite", "Campamento"),
  ("Geleira", "Glacier", "Glaciar"), ("Parque", "Theme park", "Parque"), ("Escola", "School", "Escuela"), ("Navio pirata", "Pirate ship", "Barco pirata"),
  ("Estação espacial", "Space station", "Estación espacial"), ("Casa assombrada", "Haunted house", "Casa embrujada"),
  ("Vila do Papai Noel", "Santa's village", "Aldea de Papá Noel"), ("Fundo do mar", "Under the sea", "Fondo del mar"), ("Castelo", "Castle", "Castillo"),
  ("Terra dos dinossauros", "Dinosaur land", "Tierra de dinosaurios"), ("Circo", "Circus", "Circo"), ("Supermercado", "Supermarket", "Supermercado"),
  ("Museu", "Museum", "Museo"), ("Deserto e pirâmides", "Desert and pyramids", "Desierto y pirámides")]

IDIOMAS = {
 "en": dict(lang="en", og="en_US", i=1,
   titulo="Arial Gamer · Mobile games made in Brazil: Gelada, Esconde-Esconde and Gol de Placa",
   desc="Arial Gamer makes mobile games in Brazil for iPhone and Android: Gelada (virtual beer and cocktail simulator, tilt to drink), Esconde-Esconde (hide and seek, 22 places) and Gol de Placa (3D penalties and free kicks). No ads, 8 languages.",
   ogdesc="Gelada 🍺, Esconde-Esconde 🙈 and Gol de Placa ⚽: watch the videos and download the games.",
   share="Check out these games: Gelada, Esconde-Esconde and Gol de Placa 🎮",
   precos=["No ads", "🍺 No ads · 0% alcohol", "🙈 No ads · for the whole family", "⚽ New game · No ads"],
   facts_preco="8", nome_idioma="English",
   apps={"gelada": ("Gelada: Virtual Drinks", "Beer, wine, cocktails and coffee on your phone. Fill the glass, tilt to drink and invent mixes. 100 drinks, a talking bartender and a drink of the day. 0% alcohol."),
         "esconde": ("Esconde-Esconde: Hide & Seek", "Hide and seek on your phone: 22 places by day and night, against the computer, passing the phone around or online with a friend. Family fun."),
         "gol": ("Gol de Placa: Penalty Kicks", "3D penalties and free kicks: hit the top corner or be the goalkeeper, build your player, play national teams and clubs, and play online with a friend.")}),
 "es": dict(lang="es", og="es_ES", i=2,
   titulo="Arial Gamer · Juegos para móvil hechos en Brasil: Gelada, Esconde-Esconde y Gol de Placa",
   desc="Arial Gamer crea juegos para móvil en Brasil, para iPhone y Android: Gelada (simulador de cerveza y cócteles, inclina para beber), Esconde-Esconde (escondite, 22 lugares) y Gol de Placa (penales y tiros libres en 3D). Sin anuncios, 8 idiomas.",
   ogdesc="Gelada 🍺, Esconde-Esconde 🙈 y Gol de Placa ⚽: mira los videos y descarga los juegos.",
   share="Mira estos juegos: Gelada, Esconde-Esconde y Gol de Placa 🎮",
   precos=["Sin anuncios", "🍺 Sin anuncios · 0% alcohol", "🙈 Sin anuncios · para toda la familia", "⚽ Juego nuevo · Sin anuncios"],
   facts_preco="8", nome_idioma="Español",
   apps={"gelada": ("Gelada: Bebidas Virtuales", "Cerveza, vino, cócteles y café en tu móvil. Llena el vaso, inclina para beber e inventa mezclas. 100 bebidas, barman que habla y trago del día. 0% alcohol."),
         "esconde": ("Esconde-Esconde: Escondite", "El escondite en tu móvil: 22 lugares de día y de noche, contra la máquina, pasando el móvil u online con un amigo. Para jugar en familia."),
         "gol": ("Gol de Placa: Penaltis", "Penales y tiros libres en 3D: clávala al ángulo o sé el portero, crea tu crack, juega con selecciones y clubes, y online con un amigo.")}),
}

def troca_texto(s, a, b):
    # troca só texto entre tags e valores de alt/aria-label/title (nunca URLs)
    n = 0
    def f(m):
        nonlocal n; n += 1; return m.group(1) + b + m.group(2)
    s = re.sub(r"(>\s*)" + re.escape(a) + r"(\s*<)", f, s)
    s = re.sub(r'((?:alt|aria-label|title)=")' + re.escape(a) + r'(")', f, s)
    return s, n

def absoluto(s):
    return re.sub(r'(\s(?:src|poster|data-src|href))="(?!https?:|#|/|mailto:)', r'\1="/', s)

def gerar(cod, L):
    i = L.get("i", 1); s = pt
    head, corpo = s[:s.index("<body")], s[s.index("<body"):]
    head = re.sub(r'<link rel="alternate" hreflang=[^>]*>\n', '', head)
    corpo = re.sub(r'    <nav aria-label="Idioma / Language">.*?</nav>\n', '', corpo, flags=re.S)
    # links "Tudo sobre…" e a lista de jogos do rodapé levam a páginas só em português
    corpo = re.sub(r'\s*<a class="more"[^>]*>.*?</a>', "", corpo)
    corpo = re.sub(r'\s*<nav aria-label="Jogos">.*?</nav>', "", corpo, flags=re.S)
    # seletor de idioma no rodapé (antes de traduzir os rótulos)
    corpo = corpo.replace('    <nav aria-label="Privacidade">', idiomas_nav(cod) + '    <nav aria-label="Privacidade">', 1)
    # preços em reais saem; no lugar, "sem anúncios"
    for velho, novo in zip(["🍺 R$ 1,90", "🙈 R$ 1,90 · todos os cenários R$ 1,90", "⚽ Novo jogo · R$ 1,90"], L["precos"][1:]):
        corpo, n = troca_texto(corpo, velho, novo); assert n, velho
    corpo, n = troca_texto(corpo, "R$ 1,90", L["facts_preco"]); assert n
    faltou = []
    extra = cod not in ("en", "es")
    for linha in T:
        alvo = TRAD[cod][linha[1]] if extra else linha[i]
        corpo, n = troca_texto(corpo, linha[0], alvo)
        if not n: faltou.append(linha[0])
    for p, en_nome, es_nome in LUGARES:
        nome = TRAD_LUG[cod][en_nome] if extra else (en_nome if cod == "en" else es_nome)
        dia, noite = DIA_NOITE[cod] if extra else ((" by day", " at night") if cod == "en" else (" de día", " de noche"))
        corpo, _ = troca_texto(corpo, p + " de dia", nome + dia)
        corpo, _ = troca_texto(corpo, p + " à noite", nome + noite)
        corpo = re.sub(r"(<figcaption>\S+ )" + re.escape(p) + "(</figcaption>)", lambda m: m.group(1) + nome + m.group(2), corpo)
    # lojas: página internacional da App Store e Google Play no idioma
    corpo = corpo.replace("https://apps.apple.com/br/app/", "https://apps.apple.com/app/")
    corpo = re.sub(r'(play\.google\.com/store/apps/details\?id=[\w.]+)"', r'\1&amp;hl=' + L.get("hl", cod) + '"', corpo)
    corpo = corpo.replace("'Olha esses jogos: Gelada, Esconde-Esconde e Gol de Placa 🎮'", repr(L["share"]))
    corpo = corpo.replace("'https://arialgamer.com.br/'", f"'{SITE}{cod}/'")
    # cabeçalho
    head = head.replace('<html lang="pt-BR">', f'<html lang="{L["lang"]}">')
    head = re.sub(r"<title>.*?</title>", f"<title>{L['titulo']}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{L["desc"]}">', head)
    head = head.replace(f'<link rel="canonical" href="{SITE}">', f'<link rel="canonical" href="{SITE}{cod}/">\n' + hreflang())
    head = head.replace(f'<meta property="og:url" content="{SITE}">', f'<meta property="og:url" content="{SITE}{cod}/">')
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{L["titulo"]}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{L["ogdesc"]}">', head)
    head = head.replace('<meta property="og:locale" content="pt_BR">', f'<meta property="og:locale" content="{L["og"]}">')
    a = head.index('<script type="application/ld+json">') + len('<script type="application/ld+json">'); b = head.index("</script>", a)
    head = head[:a] + "\n" + jsonld(cod, L) + "\n" + head[b:]
    html = absoluto(head + corpo)
    html = html.replace("<body", "<!-- Página gerada por _paginas/idiomas.py a partir do index.html. Não edite à mão. -->\n<body", 1)
    d = os.path.join(RAIZ, cod); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    print("ok", cod, "| sem tradução:", faltou)

def hreflang():
    pares = [("pt-BR", ""), ("en", "en/"), ("es", "es/")] + [(L["lang"], c + "/") for c, L in IDIOMAS_MAIS.items()] + [("x-default", "")]
    return "".join(f'<link rel="alternate" hreflang="{h}" href="{SITE}{p}">\n' for h, p in pares)

def idiomas_nav(atual):
    itens = [("pt", "", "Português"), ("en", "en/", "English"), ("es", "es/", "Español")] + [(c, c + "/", L["nome_idioma"]) for c, L in IDIOMAS_MAIS.items()]
    links = "\n".join(f'      <a href="/{p}" hreflang="{c}" lang="{c}"{" aria-current=\"page\"" if c == atual else ""}>{n}</a>' for c, p, n in itens)
    return f'    <nav aria-label="Idioma / Language">\n{links}\n    </nav>\n'

def jsonld(cod, L):
    lojas = {"gelada": ["https://apps.apple.com/app/id6819882963", f"https://play.google.com/store/apps/details?id=com.arial.gelada&hl={L.get("hl", cod)}"],
             "esconde": ["https://apps.apple.com/app/id6819893974", f"https://play.google.com/store/apps/details?id=com.arial.escondeesconde&hl={L.get("hl", cod)}"],
             "gol": ["https://apps.apple.com/app/id6823608331"]}
    org = {"@type": "Organization", "@id": SITE + "#org", "name": "Arial Gamer", "url": SITE, "logo": SITE + "logo-1080.jpg",
           "alternateName": ["arialgamer", "arialgamer.com.br"],
           "sameAs": ["https://www.tiktok.com/@arial.gamer", "https://www.instagram.com/arial.gamer/", "https://www.youtube.com/@arialgamer"]}
    site = {"@type": "WebSite", "name": "Arial Gamer", "url": f"{SITE}{cod}/", "inLanguage": L["lang"], "publisher": {"@id": SITE + "#org"}}
    apps = [{"@type": ["MobileApplication", "VideoGame"], "name": nome, "description": desc, "url": f"{SITE}{cod}/#{k}",
             "image": SITE + {"gelada": "gelada.png", "esconde": "esconde.png", "gol": "gol.png"}[k],
             "applicationCategory": "GameApplication", "operatingSystem": "iOS" if k == "gol" else "iOS, Android",
             "inLanguage": ["pt-BR", "en", "es", "de", "fr", "it", "zh", "ja"], "installUrl": lojas[k], "author": {"@id": SITE + "#org"}}
            for k, (nome, desc) in L["apps"].items()]
    return json.dumps({"@context": "https://schema.org", "@graph": [org, site] + apps}, ensure_ascii=False, indent=1)

def atualizar_pt():
    p = os.path.join(RAIZ, "index.html"); s = open(p, encoding="utf-8").read()
    s = re.sub(r'<link rel="alternate" hreflang=[^>]*>\n', '', s)
    s = s.replace(f'<link rel="canonical" href="{SITE}">\n', f'<link rel="canonical" href="{SITE}">\n' + hreflang(), 1)
    s = re.sub(r'    <nav aria-label="Idioma / Language">.*?</nav>\n', '', s, flags=re.S)
    nav = idiomas_nav("pt").replace('href="/"', 'href="./"').replace('href="/', 'href="')
    s = s.replace('    <nav aria-label="Privacidade">', nav + '    <nav aria-label="Privacidade">', 1)
    open(p, "w", encoding="utf-8", newline="").write(s)

atualizar_pt()
pt = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
for cod, L in {**IDIOMAS, **IDIOMAS_MAIS}.items():
    gerar(cod, L)
