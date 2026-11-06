# Gera /en/gelada/, /en/esconde-esconde/ e /en/gol-de-placa/ a partir das páginas em português dos jogos.
# Rode depois de gerar.py:  python _paginas/jogos_en.py
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idiomas import T, LUGARES, troca_texto, IDIOMAS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://arialgamer.com.br/"
e = html.escape
EN = IDIOMAS["en"]

JOGOS = {
 "gelada": dict(pasta="gelada", nome="Gelada", icone="gelada.png", imagem="media/gelada-saude.jpg",
   loja="Gelada: Virtual Drinks", os="iOS, Android",
   titulo="Gelada: virtual beer and cocktail simulator for your phone · Arial Gamer",
   descricao="Gelada turns your phone into a glass: fill it with beer, wine, cocktails or coffee, tilt to drink and invent mixes. 100 drinks, a talking bartender and a drink of the day. iPhone and Android, no ads, 0% alcohol.",
   resumo="Beer, wine, cocktails and coffee on your phone. Tilt to drink and mix.",
   lojas=["https://apps.apple.com/app/id6819882963", "https://play.google.com/store/apps/details?id=com.arial.gelada&hl=en"],
   como="What is Gelada like", como_sub="Remember the app that turned your phone into a glass of beer? Gelada brings it back, and does a lot more.",
   cards=[("🍺", "Tilt to drink", "The screen becomes a glass. The liquid follows your phone, with waves, bubbles and foam. Bring the top to your mouth and drink, with gulp sounds and vibration."),
          ("🍹", "100 drinks", "Beers, wines, sparkling wine, cocktails like mojito and caipirinha, and 40+ alcohol-free drinks: juices, sodas, coffees and teas."),
          ("🧪", "Mix mode", "Combine up to 4 drinks. The order changes the result, like in real life, and classic recipes like Cuba Libre and Gin & Tonic are recognized."),
          ("⭐", "Mix score", "Every mix gets a 0–10 score with taste and ratio. Milk with orange juice? It curdles. Three spirits together? Bomb!"),
          ("🗣️", "Talking bartender", "A bartender reviews your mixes, cheers with you and challenges you, in 8 languages."),
          ("🎬", "Prank video", "Record the glass filling up and send it to friends as if it were real.")],
   faq=[("Does Gelada have real alcohol?", "No. The drinks are 100% virtual: it is a game on your phone, with 0% alcohol. Drink responsibly in real life."),
        ("Which phones does it run on?", "iPhone and Android. There are no ads and no subscription."),
        ("Are there alcohol-free drinks?", "Yes, more than 40: juices, sodas, coffees, teas, milkshakes and smoothies. Under-18s only see alcohol-free drinks, and a parent can unlock the rest with a PIN."),
        ("Does it need internet or sign-up?", "No. Gelada works offline, without sign-up, and collects no data."),
        ("Which languages?", "English, Portuguese, Spanish, German, French, Italian, Chinese and Japanese.")]),
 "esconde": dict(pasta="esconde-esconde", nome="Esconde-Esconde", icone="esconde.png", imagem="media/esconde-lua.jpg",
   loja="Esconde-Esconde: Hide & Seek", os="iOS, Android",
   titulo="Esconde-Esconde: hide and seek game for your phone · Arial Gamer",
   descricao="Hide and seek on your phone: 22 places by day and night, against the computer, passing the phone around or online with a friend. Narrator, hot or cold radar and a mode for little ones. iPhone and Android, no ads.",
   resumo="Hide and seek against the computer or a friend.",
   lojas=["https://apps.apple.com/app/id6819893974", "https://play.google.com/store/apps/details?id=com.arial.escondeesconde&hl=en"],
   como="What is Esconde-Esconde like", como_sub="The classic game, made for your phone: hide, pass the phone and see if the other person finds you.",
   cards=[("☀️", "Day and night", "By day everything is visible. At night the lights go out and you search with a flashlight. The moon has real phases."),
          ("👂", "Listen for noises", "Hiders sometimes move and little sound waves appear. But it might be the decoy, the farm cow or the ship's parrot!"),
          ("📡", "Hot or cold radar", "The phone vibrates harder as you get closer to the hiding spot."),
          ("🤖", "The computer learns", "Three difficulty levels. The computer remembers where you usually hide and where you usually search."),
          ("🎉", "Party for 3 or 4", "Pass the phone around: everyone hides once per round, and at the end there is a ranking with medals."),
          ("🌧️", "Rain and lightning", "Sometimes it rains and noises get muffled. At night, lightning lights everything up for a moment.")],
   faq=[("Which phones does it run on?", "iPhone and Android. There are no ads and no subscription."),
        ("Can I play with someone else?", "Yes: passing the same phone, at a party of 3 or 4, or online with a friend, each on their own phone with a room code."),
        ("Is it good for kids?", "Yes. It is a family game with a mode for little ones and a narrator who tells everything, with no ads."),
        ("Which places are there?", "22, like house, beach, farm, glacier, pirate ship, space station, castle, dinosaur land, circus and museum, all by day and by night."),
        ("Does it need sign-up?", "No. The game needs no sign-up and collects no data.")]),
 "gol": dict(pasta="gol-de-placa", nome="Gol de Placa", icone="gol.png", imagem="media/gol-adulta.jpg",
   loja="Gol de Placa: Penalty Kicks", os="iOS",
   titulo="Gol de Placa: penalty and free kick soccer game for your phone · Arial Gamer",
   descricao="Gol de Placa: 3D penalties and free kicks on your phone. Hit the top corner or be the goalkeeper, build your player and play online with a friend. National teams, clubs, rain, snow and commentary. On iPhone, no ads.",
   resumo="3D penalties and free kicks: be the kicker or the goalkeeper.",
   lojas=["https://apps.apple.com/app/id6823608331"],
   como="What is Gol de Placa like", como_sub="Drag from the ball to the corner of the goal and shoot. Or stand in goal and try to save it.",
   cards=[("⚽", "Real shots", "The ball goes where you aim: top corner, low along the grass or curled around the wall. It hits the post and ripples the net."),
          ("🧤", "Or be the goalkeeper", "Tap the goal to dive. The keeper dives, jumps and catches the ball."),
          ("🏆", "Cup", "Quarterfinal, semifinal and final in penalty shootouts, with sudden death and a trophy at the end."),
          ("🧑", "Build your player", "Skin, hair, boots, number and name on the shirt, plus the celebration: airplane, dance, somersault…"),
          ("🌦️", "Weather and fans", "Day, night under floodlights, rain and snow. Fans with drums, the wave and a party for every goal."),
          ("📒", "Stickers and challenges", "Stickers to collect and new challenges every day.")],
   faq=[("Which phones does it run on?", "iPhone, with no ads and no subscription. The Android version is coming soon; follow @arial.gamer to know when."),
        ("Can I play with a friend?", "Yes, online, each on their own phone."),
        ("Is it good for kids?", "Yes. It is a family game with blocky players, no violence and no ads. There is also a grown-up version with realistic players."),
        ("Does it need sign-up?", "No. The game needs no sign-up and collects no data."),
        ("Which languages?", "8 languages in the game and commentary in 14.")]),
}
ORDEM = ["gelada", "esconde", "gol"]

def jsonld(k, j):
    url = f"{SITE}en/{j['pasta']}/"
    app = {"@type": ["MobileApplication", "VideoGame"], "@id": url + "#app", "name": j["loja"], "alternateName": j["nome"],
           "description": j["descricao"], "url": url, "image": SITE + j["icone"], "screenshot": SITE + j["imagem"],
           "applicationCategory": "GameApplication", "operatingSystem": j["os"], "inLanguage": "en",
           "installUrl": j["lojas"], "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"}}
    org = {"@type": "Organization", "@id": SITE + "#org", "name": "Arial Gamer", "url": SITE, "logo": SITE + "logo-1080.jpg",
           "sameAs": ["https://www.tiktok.com/@arial.gamer", "https://www.instagram.com/arial.gamer/", "https://www.youtube.com/@arialgamer"]}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Arial Gamer", "item": SITE + "en/"},
        {"@type": "ListItem", "position": 2, "name": j["nome"], "item": url}]}
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in j["faq"]]}
    return json.dumps({"@context": "https://schema.org", "@graph": [org, app, crumbs, faq]}, ensure_ascii=False, indent=1)

def blocos(k, j):
    cards = "\n".join(f'        <article class="reveal"><div class="em">{em}</div><h3>{e(t)}</h3><p>{e(d)}</p></article>' for em, t, d in j["cards"])
    faq = "\n".join(f'        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in j["faq"])
    outros = "\n".join(f'        <a href="/en/{JOGOS[o]["pasta"]}/"><img src="/{JOGOS[o]["icone"]}" alt="" width="72" height="72"><span><b>{JOGOS[o]["nome"]}</b>{e(JOGOS[o]["resumo"])}</span></a>' for o in ORDEM if o != k)
    return f"""  <section class="block">
    <div class="wrap">
      <h2>{e(j["como"])}</h2>
      <p class="sub">{e(j["como_sub"])}</p>
      <div class="cards">
{cards}
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>Frequently asked questions</h2>
      <p class="sub">Everything people ask about {e(j["nome"])}.</p>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2>More games by Arial Gamer</h2>
      <p class="sub">No ads, in 8 languages.</p>
      <div class="others">
{outros}
      </div>
    </div>
  </section>

"""

def gerar(k):
    j = JOGOS[k]; url = f"{SITE}en/{j['pasta']}/"
    s = open(os.path.join(RAIZ, j["pasta"], "index.html"), encoding="utf-8").read()
    # cabeçalho
    s = s.replace('<html lang="pt-BR">', '<html lang="en">', 1)
    s = re.sub(r"<title>.*?</title>", f"<title>{e(j['titulo'])}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(j["descricao"])}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = s.replace('<meta property="og:locale" content="pt_BR">', '<meta property="og:locale" content="en_US">')
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(j["titulo"])}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(j["resumo"])} Watch the videos and download.">', s, count=1)
    a = s.index('<script type="application/ld+json">') + len('<script type="application/ld+json">'); b = s.index("</script>", a)
    s = s[:a] + "\n" + jsonld(k, j) + "\n" + s[b:]
    s = s.replace("Gerada por _paginas/gerar.py", "Gerada por _paginas/jogos_en.py")
    # navegação e trilha
    for o in ORDEM:
        p = JOGOS[o]["pasta"]
        s = s.replace(f'<a href="/{p}/"', f'<a href="/en/{p}/"')
    s = s.replace('<a class="brand" href="/">', '<a class="brand" href="/en/">', 1)
    s = s.replace('aria-label="Você está em"><div class="wrap"><ol><li><a href="/">', 'aria-label="You are here"><div class="wrap"><ol><li><a href="/en/">', 1)
    # blocos próprios da página (como é, perguntas, outros jogos)
    a = s.index('  <section class="block">'); b = s.index('  <!-- ================= REDES')
    s = s[:a] + blocos(k, j) + s[b:]
    # textos que vêm da página principal
    corpo_i = s.index("<body")
    head, corpo = s[:corpo_i], s[corpo_i:]
    for velho, novo in zip(["🍺 R$ 1,90", "🙈 R$ 1,90 · todos os cenários R$ 1,90", "⚽ Novo jogo · R$ 1,90"], EN["precos"][1:]):
        corpo, _ = troca_texto(corpo, velho, novo)
    for linha in T:
        corpo, _ = troca_texto(corpo, linha[0], linha[1])
    for p_, en_, _es in LUGARES:
        corpo, _ = troca_texto(corpo, p_ + " de dia", en_ + " by day")
        corpo, _ = troca_texto(corpo, p_ + " à noite", en_ + " at night")
        corpo = re.sub(r"(<figcaption>\S+ )" + re.escape(p_) + "(</figcaption>)", lambda m: m.group(1) + en_ + m.group(2), corpo)
    corpo, _ = troca_texto(corpo, "Compartilhar este jogo", "Share this game")
    corpo = corpo.replace(repr(f"Olha esse jogo: {j['nome']} 🎮"), repr(f"Check out this game: {j['nome']} 🎮"))
    corpo = corpo.replace("https://apps.apple.com/br/app/", "https://apps.apple.com/app/")
    corpo = re.sub(r'(play\.google\.com/store/apps/details\?id=[\w.]+)"', r'\1&amp;hl=en"', corpo)
    for o in ORDEM:
        p = JOGOS[o]["pasta"]
        corpo = corpo.replace(f'<a href="/{p}/">', f'<a href="/en/{p}/">')
    s = head + corpo
    d = os.path.join(RAIZ, "en", j["pasta"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(s)
    # sobras em português, para conferir
    rest = [w for w in ["Perguntas", "Baixar na", "Disponível", "Escolha um", "Redes sociais", "Siga a", "jogos no ar", "Você está"] if w in s]
    print("ok en/" + j["pasta"], "| sobras:", rest)

for k in ORDEM:
    gerar(k)
