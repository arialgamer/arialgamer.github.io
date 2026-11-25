# Seção "Sobre a Arial Gamer" na home dos 8 idiomas: quem somos, compromissos, quanto custa cada jogo
# e links de confiança (página de desenvolvedor nas lojas, kit de imprensa, privacidade).
# Também põe o link "Sobre" no rodapé. Pode rodar de novo: troca a seção inteira.
#   python _paginas/sobre.py
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDIOMAS = [".", "en", "es", "de", "fr", "it", "ja", "zh"]
MARCA_INI = "  <!-- ================= SOBRE ================= -->"
MARCA_FIM = "  <!-- ================= /SOBRE ================= -->"
ANTES_DE = "  <!-- ================= APOIE"
CSS_ID = "/* ---------- Sobre a Arial Gamer ---------- */"

CSS = CSS_ID + """
.sobre .card { display: block }
.sobre .intro { display: grid; grid-template-columns: 1.3fr 1fr; gap: 34px; align-items: start }
.sobre .intro p { color: var(--muted); margin: 0 0 14px }
.sobre .intro p b { color: var(--ink) }
.sobre .nums { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px }
.sobre .num { padding: 16px 18px; border-radius: 18px; background: var(--glass); border: 1px solid var(--line) }
.sobre .num strong { display: block; font: 800 30px/1.1 var(--display, inherit); color: var(--ink) }
.sobre .num span { color: var(--muted); font-size: 14px }
.sobre .promessas { list-style: none; padding: 0; margin: 28px 0 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px }
.sobre .promessas li { padding: 16px; border-radius: 18px; background: var(--glass); border: 1px solid var(--line); font-size: 15px; line-height: 1.4 }
.sobre .promessas li b { display: block; margin-bottom: 4px; font-size: 16px }
.sobre h3 { margin: 34px 0 12px; font-size: 20px }
.sobre .precos { width: 100%; border-collapse: collapse; font-size: 15px }
.sobre .precos th { text-align: left; font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); font-weight: 700; padding: 0 12px 10px }
.sobre .precos td { padding: 12px; border-top: 1px solid var(--line); vertical-align: top }
.sobre .precos td:first-child a { font-weight: 700; color: var(--ink); text-decoration: none }
.sobre .precos td:first-child a:hover { text-decoration: underline }
.sobre .precos td.pr { font-weight: 700; white-space: nowrap }
.sobre .precos td.pv a { color: var(--muted); font-size: 14px }
.sobre .nota { color: var(--muted); font-size: 14px; margin: 10px 0 0 }
.sobre .confia { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px }
@media (max-width: 900px) { .sobre .intro { grid-template-columns: 1fr } .sobre .promessas { grid-template-columns: 1fr 1fr } }
@media (max-width: 640px) {
  .sobre .promessas { grid-template-columns: 1fr }
  .sobre .precos thead { display: none }
  .sobre .precos tr { display: grid; grid-template-columns: 1fr auto; gap: 2px 12px; padding: 12px 0; border-top: 1px solid var(--line) }
  .sobre .precos td { border: 0; padding: 0 }
  .sobre .precos td.pf { grid-column: 1 / -1; color: var(--muted); font-size: 14px }
  .sobre .precos td.pv { grid-column: 1 / -1 }
}
"""

# jogo: (rota da página, rota da privacidade)
ROTAS = {
    "deicida": ("deicida/", "/deicida-privacidade/"),
    "rota": ("rota-estelar/", "/rota-estelar-privacidade/"),
    "volei": ("volei-total/", "/volei-privacidade/"),
    "gol": ("gol-de-placa/", "/gol-privacidade/"),
    "xodo": ("xodo/", "/xodo-privacidade/"),
    "esconde": ("esconde-esconde/", "/esconde-privacidade/"),
    "gelada": ("gelada/", "/gelada-privacidade/"),
    "acervo": ("acervo/", "/acervo/privacidade/"),
}
NOMES = {"deicida": "Deicida", "rota": "Rota Estelar", "volei": "Vôlei Total", "gol": "Gol de Placa",
         "xodo": "Xodó", "esconde": "Esconde-Esconde", "gelada": "Gelada", "acervo": "Acervo"}
GP_DEV = "https://play.google.com/store/apps/dev?id=7102410817973589199"

T = {
 ".": dict(
  eyebrow="Quem faz", h2="Sobre a Arial Gamer", rodape="Sobre a Arial Gamer",
  p1="A <b>Arial Gamer</b> é um estúdio independente de jogos para celular, feito no Brasil. A gente faz jogos curtos e alegres para jogar sozinho, com a família ou com os amigos, em iPhone e Android.",
  p2="Cada jogo é feito do começo ao fim aqui: ideia, arte, programação, narração e tradução para 8 idiomas. Quem joga não vê propaganda e não precisa criar conta.",
  nums=[("7", "jogos lançados"), ("1", "app para colecionadores"), ("8", "idiomas"), ("0", "anúncios")],
  prom=[("🚫 Sem anúncios", "Em nenhum jogo, nunca."), ("🔒 Sem coleta de dados", "Os jogos não pedem cadastro e não guardam dados pessoais."), ("💳 Preço claro", "Você vê o valor antes de baixar. Sem pegadinha."), ("🌎 8 idiomas", "Português, inglês, espanhol, alemão, francês, italiano, japonês e chinês.")],
  h3p="Quanto custa cada jogo", th=("Jogo", "Preço", "Onde jogar", "Privacidade"),
  priv="Política",
  linhas={
   "deicida": ("Grátis", "iPhone, iPad e Android. Prólogo e 1ª fase liberados; as fases 2 a 10 chegam por compra dentro do jogo."),
   "rota": ("R$ 4,90", "iPhone, iPad e Android. Jogo completo, sem compras dentro do app."),
   "volei": ("R$ 4,90", "iPhone, iPad e Android. Jogo completo, sem compras dentro do app."),
   "gol": ("R$ 3,90", "iPhone, iPad e Android. Tudo liberado, sem compras dentro do app."),
   "xodo": ("R$ 2,90", "iPhone, iPad e Android. Jogo completo, sem compras dentro do app."),
   "esconde": ("R$ 2,90", "iPhone, iPad e Android. Os 24 lugares liberados, sem compras dentro do app."),
   "gelada": ("R$ 2,90", "iPhone, iPad e Android. Sem compras dentro do app."),
   "acervo": ("Grátis", "iPhone e Android. Premium opcional: R$ 9,90/mês ou R$ 79,90/ano."),
  },
  nota="Preços da App Store e do Google Play no Brasil; em outros países, a loja mostra o valor na moeda local.",
  h3c="Confira por conta própria", apple="Nossos jogos na App Store", gp="Nossos jogos no Google Play", press="Kit de imprensa",
  apple_url="https://apps.apple.com/br/developer/renato-nogueira/id6819882965", press_url="/imprensa/"),
 "en": dict(
  eyebrow="Who we are", h2="About Arial Gamer", rodape="About Arial Gamer",
  p1="<b>Arial Gamer</b> is an independent mobile game studio from Brazil. We make short, joyful games to play alone, with family or with friends, on iPhone and Android.",
  p2="Every game is made from start to finish here: idea, art, code, narration and translation into 8 languages. Players never see ads and never need an account.",
  nums=[("7", "games released"), ("1", "app for collectors"), ("8", "languages"), ("0", "ads")],
  prom=[("🚫 No ads", "In every game, always."), ("🔒 No data collection", "Our games need no sign-up and store no personal data."), ("💳 Clear pricing", "You see the price before you download. No tricks."), ("🌎 8 languages", "English, Portuguese, Spanish, German, French, Italian, Japanese and Chinese.")],
  h3p="What each game costs", th=("Game", "Price", "Where to play", "Privacy"),
  priv="Policy",
  linhas={
   "deicida": ("Free", "iPhone, iPad and Android. Prologue and level 1 unlocked; levels 2 to 10 coming as an in-app purchase."),
   "rota": ("Paid, one-time", "iPhone, iPad and Android. Full game, no in-app purchases."),
   "volei": ("Paid, one-time", "iPhone, iPad and Android. Full game, no in-app purchases."),
   "gol": ("Paid, one-time", "iPhone, iPad and Android. Everything unlocked, no in-app purchases."),
   "xodo": ("Paid, one-time", "iPhone, iPad and Android. Full game, no in-app purchases."),
   "esconde": ("Paid, one-time", "iPhone, iPad and Android. All 24 places unlocked, no in-app purchases."),
   "gelada": ("Paid, one-time", "iPhone, iPad and Android. No in-app purchases."),
   "acervo": ("Free", "iPhone and Android. Optional Premium subscription."),
  },
  nota="The App Store and Google Play show the exact price in your local currency.",
  h3c="Check for yourself", apple="Our games on the App Store", gp="Our games on Google Play", press="Press kit",
  apple_url="https://apps.apple.com/us/developer/renato-nogueira/id6819882965", press_url="/press/"),
 "es": dict(
  eyebrow="Quiénes somos", h2="Sobre Arial Gamer", rodape="Sobre Arial Gamer",
  p1="<b>Arial Gamer</b> es un estudio independiente de juegos para móviles, hecho en Brasil. Hacemos juegos cortos y alegres para jugar solo, en familia o con amigos, en iPhone y Android.",
  p2="Cada juego se hace de principio a fin aquí: idea, arte, programación, narración y traducción a 8 idiomas. Quien juega no ve anuncios ni necesita crear una cuenta.",
  nums=[("7", "juegos lanzados"), ("1", "app para coleccionistas"), ("8", "idiomas"), ("0", "anuncios")],
  prom=[("🚫 Sin anuncios", "En ningún juego, nunca."), ("🔒 Sin recopilar datos", "Los juegos no piden registro ni guardan datos personales."), ("💳 Precio claro", "Ves el precio antes de descargar. Sin trampas."), ("🌎 8 idiomas", "Español, portugués, inglés, alemán, francés, italiano, japonés y chino.")],
  h3p="Cuánto cuesta cada juego", th=("Juego", "Precio", "Dónde jugar", "Privacidad"),
  priv="Política",
  linhas={
   "deicida": ("Gratis", "iPhone, iPad y Android. Prólogo y nivel 1 desbloqueados; los niveles 2 a 10 llegarán como compra dentro del juego."),
   "rota": ("De pago, pago único", "iPhone, iPad y Android. Juego completo, sin compras dentro de la app."),
   "volei": ("De pago, pago único", "iPhone, iPad y Android. Juego completo, sin compras dentro de la app."),
   "gol": ("De pago, pago único", "iPhone, iPad y Android. Todo desbloqueado, sin compras dentro de la app."),
   "xodo": ("De pago, pago único", "iPhone, iPad y Android. Juego completo, sin compras dentro de la app."),
   "esconde": ("De pago, pago único", "iPhone, iPad y Android. Los 24 lugares desbloqueados, sin compras dentro de la app."),
   "gelada": ("De pago, pago único", "iPhone, iPad y Android. Sin compras dentro de la app."),
   "acervo": ("Gratis", "iPhone y Android. Suscripción Premium opcional."),
  },
  nota="La App Store y Google Play muestran el precio exacto en tu moneda local.",
  h3c="Compruébalo tú mismo", apple="Nuestros juegos en la App Store", gp="Nuestros juegos en Google Play", press="Kit de prensa",
  apple_url="https://apps.apple.com/es/developer/renato-nogueira/id6819882965", press_url="/es/press/"),
 "de": dict(
  eyebrow="Wer wir sind", h2="Über Arial Gamer", rodape="Über Arial Gamer",
  p1="<b>Arial Gamer</b> ist ein unabhängiges Studio für Handyspiele aus Brasilien. Wir machen kurze, fröhliche Spiele für allein, mit der Familie oder mit Freunden, auf iPhone und Android.",
  p2="Jedes Spiel entsteht hier von Anfang bis Ende: Idee, Grafik, Programmierung, Sprecher und Übersetzung in 8 Sprachen. Wer spielt, sieht keine Werbung und braucht kein Konto.",
  nums=[("7", "veröffentlichte Spiele"), ("1", "App für Sammler"), ("8", "Sprachen"), ("0", "Werbung")],
  prom=[("🚫 Keine Werbung", "In keinem Spiel, niemals."), ("🔒 Keine Datensammlung", "Unsere Spiele brauchen keine Anmeldung und speichern keine persönlichen Daten."), ("💳 Klare Preise", "Du siehst den Preis vor dem Download. Ohne Tricks."), ("🌎 8 Sprachen", "Deutsch, Englisch, Portugiesisch, Spanisch, Französisch, Italienisch, Japanisch und Chinesisch.")],
  h3p="Was jedes Spiel kostet", th=("Spiel", "Preis", "Wo spielen", "Datenschutz"),
  priv="Richtlinie",
  linhas={
   "deicida": ("Kostenlos", "iPhone, iPad und Android. Prolog und Level 1 frei; Level 2 bis 10 kommen als In-App-Kauf."),
   "rota": ("Einmalkauf", "iPhone, iPad und Android. Vollversion, keine In-App-Käufe."),
   "volei": ("Einmalkauf", "iPhone, iPad und Android. Vollversion, keine In-App-Käufe."),
   "gol": ("Einmalkauf", "iPhone, iPad und Android. Alles freigeschaltet, keine In-App-Käufe."),
   "xodo": ("Einmalkauf", "iPhone, iPad und Android. Vollversion, keine In-App-Käufe."),
   "esconde": ("Einmalkauf", "iPhone, iPad und Android. Alle 24 Orte frei, keine In-App-Käufe."),
   "gelada": ("Einmalkauf", "iPhone, iPad und Android. Keine In-App-Käufe."),
   "acervo": ("Kostenlos", "iPhone und Android. Optionales Premium-Abo."),
  },
  nota="Der App Store und Google Play zeigen den genauen Preis in deiner Landeswährung.",
  h3c="Überzeug dich selbst", apple="Unsere Spiele im App Store", gp="Unsere Spiele bei Google Play", press="Pressekit",
  apple_url="https://apps.apple.com/de/developer/renato-nogueira/id6819882965", press_url="/de/press/"),
 "fr": dict(
  eyebrow="Qui sommes-nous", h2="À propos d'Arial Gamer", rodape="À propos d'Arial Gamer",
  p1="<b>Arial Gamer</b> est un studio indépendant de jeux mobiles, fait au Brésil. Nous créons des jeux courts et joyeux à jouer seul, en famille ou entre amis, sur iPhone et Android.",
  p2="Chaque jeu est fait ici du début à la fin : idée, graphismes, programmation, narration et traduction en 8 langues. Les joueurs ne voient aucune publicité et n'ont pas besoin de compte.",
  nums=[("7", "jeux sortis"), ("1", "app pour collectionneurs"), ("8", "langues"), ("0", "publicité")],
  prom=[("🚫 Sans publicité", "Dans aucun jeu, jamais."), ("🔒 Aucune collecte de données", "Nos jeux ne demandent pas d'inscription et ne stockent aucune donnée personnelle."), ("💳 Prix clair", "Vous voyez le prix avant de télécharger. Sans piège."), ("🌎 8 langues", "Français, anglais, portugais, espagnol, allemand, italien, japonais et chinois.")],
  h3p="Combien coûte chaque jeu", th=("Jeu", "Prix", "Où jouer", "Confidentialité"),
  priv="Politique",
  linhas={
   "deicida": ("Gratuit", "iPhone, iPad et Android. Prologue et niveau 1 débloqués ; les niveaux 2 à 10 arriveront en achat intégré."),
   "rota": ("Payant, achat unique", "iPhone, iPad et Android. Jeu complet, sans achats intégrés."),
   "volei": ("Payant, achat unique", "iPhone, iPad et Android. Jeu complet, sans achats intégrés."),
   "gol": ("Payant, achat unique", "iPhone, iPad et Android. Tout débloqué, sans achats intégrés."),
   "xodo": ("Payant, achat unique", "iPhone, iPad et Android. Jeu complet, sans achats intégrés."),
   "esconde": ("Payant, achat unique", "iPhone, iPad et Android. Les 24 lieux débloqués, sans achats intégrés."),
   "gelada": ("Payant, achat unique", "iPhone, iPad et Android. Sans achats intégrés."),
   "acervo": ("Gratuit", "iPhone et Android. Abonnement Premium facultatif."),
  },
  nota="L'App Store et Google Play affichent le prix exact dans votre monnaie locale.",
  h3c="Vérifiez par vous-même", apple="Nos jeux sur l'App Store", gp="Nos jeux sur Google Play", press="Kit presse",
  apple_url="https://apps.apple.com/fr/developer/renato-nogueira/id6819882965", press_url="/fr/press/"),
 "it": dict(
  eyebrow="Chi siamo", h2="Chi è Arial Gamer", rodape="Chi è Arial Gamer",
  p1="<b>Arial Gamer</b> è uno studio indipendente di giochi per smartphone, fatto in Brasile. Creiamo giochi brevi e allegri da giocare da soli, in famiglia o con gli amici, su iPhone e Android.",
  p2="Ogni gioco nasce qui dall'inizio alla fine: idea, grafica, programmazione, narrazione e traduzione in 8 lingue. Chi gioca non vede pubblicità e non deve creare un account.",
  nums=[("7", "giochi pubblicati"), ("1", "app per collezionisti"), ("8", "lingue"), ("0", "pubblicità")],
  prom=[("🚫 Senza pubblicità", "In nessun gioco, mai."), ("🔒 Nessuna raccolta di dati", "I nostri giochi non chiedono registrazione e non salvano dati personali."), ("💳 Prezzo chiaro", "Vedi il prezzo prima di scaricare. Senza sorprese."), ("🌎 8 lingue", "Italiano, inglese, portoghese, spagnolo, tedesco, francese, giapponese e cinese.")],
  h3p="Quanto costa ogni gioco", th=("Gioco", "Prezzo", "Dove giocare", "Privacy"),
  priv="Informativa",
  linhas={
   "deicida": ("Gratis", "iPhone, iPad e Android. Prologo e livello 1 sbloccati; i livelli da 2 a 10 arriveranno come acquisto in-app."),
   "rota": ("A pagamento, una tantum", "iPhone, iPad e Android. Gioco completo, senza acquisti in-app."),
   "volei": ("A pagamento, una tantum", "iPhone, iPad e Android. Gioco completo, senza acquisti in-app."),
   "gol": ("A pagamento, una tantum", "iPhone, iPad e Android. Tutto sbloccato, senza acquisti in-app."),
   "xodo": ("A pagamento, una tantum", "iPhone, iPad e Android. Gioco completo, senza acquisti in-app."),
   "esconde": ("A pagamento, una tantum", "iPhone, iPad e Android. Tutti i 24 luoghi sbloccati, senza acquisti in-app."),
   "gelada": ("A pagamento, una tantum", "iPhone, iPad e Android. Senza acquisti in-app."),
   "acervo": ("Gratis", "iPhone e Android. Abbonamento Premium facoltativo."),
  },
  nota="L'App Store e Google Play mostrano il prezzo esatto nella tua valuta locale.",
  h3c="Verifica tu stesso", apple="I nostri giochi sull'App Store", gp="I nostri giochi su Google Play", press="Kit stampa",
  apple_url="https://apps.apple.com/it/developer/renato-nogueira/id6819882965", press_url="/it/press/"),
 "ja": dict(
  eyebrow="私たちについて", h2="Arial Gamer について", rodape="Arial Gamer について",
  p1="<b>Arial Gamer</b> はブラジルのインディーのスマホゲームスタジオです。ひとりでも、家族や友だちとでも遊べる、短くて楽しいゲームを iPhone と Android 向けに作っています。",
  p2="アイデア、アート、プログラム、ナレーション、8 言語への翻訳まで、すべてのゲームをここで一から作っています。広告は一切なく、アカウント登録も必要ありません。",
  nums=[("7", "リリース済みのゲーム"), ("1", "コレクター向けアプリ"), ("8", "言語"), ("0", "広告")],
  prom=[("🚫 広告なし", "どのゲームにも、ずっと。"), ("🔒 データ収集なし", "登録不要で、個人データは保存しません。"), ("💳 わかりやすい価格", "ダウンロード前に価格がわかります。"), ("🌎 8 言語", "日本語、英語、ポルトガル語、スペイン語、ドイツ語、フランス語、イタリア語、中国語。")],
  h3p="各ゲームの価格", th=("ゲーム", "価格", "対応機種", "プライバシー"),
  priv="ポリシー",
  linhas={
   "deicida": ("無料", "iPhone・iPad・Android。プロローグとステージ 1 は無料、ステージ 2〜10 はアプリ内課金で近日追加。"),
   "rota": ("買い切り", "iPhone・iPad・Android。完全版、アプリ内課金なし。"),
   "volei": ("買い切り", "iPhone・iPad・Android。完全版、アプリ内課金なし。"),
   "gol": ("買い切り", "iPhone・iPad・Android。すべて解放済み、アプリ内課金なし。"),
   "xodo": ("買い切り", "iPhone・iPad・Android。完全版、アプリ内課金なし。"),
   "esconde": ("買い切り", "iPhone・iPad・Android。24 か所すべて解放、アプリ内課金なし。"),
   "gelada": ("買い切り", "iPhone・iPad・Android。アプリ内課金なし。"),
   "acervo": ("無料", "iPhone・Android。プレミアムは任意のサブスクリプション。"),
  },
  nota="正確な価格は App Store と Google Play でお住まいの国の通貨で表示されます。",
  h3c="ストアで確認", apple="App Store のゲーム一覧", gp="Google Play のゲーム一覧", press="プレスキット",
  apple_url="https://apps.apple.com/jp/developer/renato-nogueira/id6819882965", press_url="/ja/press/"),
 "zh": dict(
  eyebrow="关于我们", h2="关于 Arial Gamer", rodape="关于 Arial Gamer",
  p1="<b>Arial Gamer</b> 是来自巴西的独立手机游戏工作室。我们为 iPhone 和 Android 制作简短、欢乐的游戏，可以一个人玩，也可以和家人朋友一起玩。",
  p2="每款游戏都由我们从头做到尾：创意、美术、编程、配音，以及 8 种语言的翻译。玩家不会看到广告，也不需要注册账号。",
  nums=[("7", "款已上线游戏"), ("1", "款收藏家应用"), ("8", "种语言"), ("0", "广告")],
  prom=[("🚫 无广告", "所有游戏，永远如此。"), ("🔒 不收集数据", "游戏无需注册，不保存个人数据。"), ("💳 价格透明", "下载前就能看到价格，没有套路。"), ("🌎 8 种语言", "中文、英语、葡萄牙语、西班牙语、德语、法语、意大利语和日语。")],
  h3p="每款游戏的价格", th=("游戏", "价格", "平台", "隐私"),
  priv="政策",
  linhas={
   "deicida": ("免费", "iPhone、iPad 和 Android。序章和第 1 关免费，第 2 至 10 关将以应用内购买推出。"),
   "rota": ("付费，一次买断", "iPhone、iPad 和 Android。完整版，无应用内购买。"),
   "volei": ("付费，一次买断", "iPhone、iPad 和 Android。完整版，无应用内购买。"),
   "gol": ("付费，一次买断", "iPhone、iPad 和 Android。全部解锁，无应用内购买。"),
   "xodo": ("付费，一次买断", "iPhone、iPad 和 Android。完整版，无应用内购买。"),
   "esconde": ("付费，一次买断", "iPhone、iPad 和 Android。24 个地点全部解锁，无应用内购买。"),
   "gelada": ("付费，一次买断", "iPhone、iPad 和 Android。无应用内购买。"),
   "acervo": ("免费", "iPhone 和 Android。可选高级订阅。"),
  },
  nota="App Store 和 Google Play 会以你所在地区的货币显示准确价格。",
  h3c="自己查看", apple="我们在 App Store 的游戏", gp="我们在 Google Play 的游戏", press="媒体资料包",
  apple_url="https://apps.apple.com/cn/developer/renato-nogueira/id6819882965", press_url="/zh/press/"),
}


def secao(L, pre):
    nums = "".join(f'<div class="num"><strong>{n}</strong><span>{t}</span></div>' for n, t in L["nums"])
    prom = "".join(f"<li><b>{a}</b>{b}</li>" for a, b in L["prom"])
    th = "".join(f"<th>{h}</th>" for h in L["th"])
    linhas = ""
    for j, (preco, onde) in L["linhas"].items():
        pag, priv = ROTAS[j]
        linhas += (f'<tr><td><a href="{pre}{pag}">{NOMES[j]}</a></td><td class="pr">{preco}</td>'
                   f'<td class="pf">{onde}</td><td class="pv"><a href="{priv}">{L["priv"]}</a></td></tr>')
    return f"""{MARCA_INI}
  <section class="extra sobre" id="sobre">
    <div class="wrap">
      <div class="card reveal">
        <div class="intro">
          <div>
            <p class="eyebrow">{L["eyebrow"]}</p>
            <h2>{L["h2"]}</h2>
            <p>{L["p1"]}</p>
            <p>{L["p2"]}</p>
          </div>
          <div class="nums">{nums}</div>
        </div>
        <ul class="promessas">{prom}</ul>
        <h3>{L["h3p"]}</h3>
        <table class="precos"><thead><tr>{th}</tr></thead><tbody>{linhas}</tbody></table>
        <p class="nota">{L["nota"]}</p>
        <h3>{L["h3c"]}</h3>
        <div class="confia">
          <a class="btn ghost" href="{L["apple_url"]}" target="_blank" rel="noopener"><svg><use href="#i-apple"/></svg>{L["apple"]}</a>
          <a class="btn ghost" href="{GP_DEV}" target="_blank" rel="noopener"><svg><use href="#i-play"/></svg>{L["gp"]}</a>
          <a class="btn ghost" href="{L["press_url"]}">{L["press"]}</a>
        </div>
      </div>
    </div>
  </section>
{MARCA_FIM}
"""


for d in IDIOMAS:
    L = T[d]
    p = os.path.join(RAIZ, d, "index.html")
    s = open(p, encoding="utf-8", newline="").read()
    pre = "/" if d == "." else f"/{d}/"
    nova = secao(L, pre)
    if MARCA_INI in s:
        s = re.sub(re.escape(MARCA_INI) + r".*?" + re.escape(MARCA_FIM) + r"\n", lambda m: nova, s, flags=re.S)
    else:
        i = s.index(ANTES_DE)
        s = s[:i] + nova + "\n" + s[i:]
    if CSS_ID in s:
        s = re.sub(re.escape(CSS_ID) + r".*?\n}\n", lambda m: CSS.strip("\n") + "\n", s, count=1, flags=re.S)
    else:
        i = s.index("</style>")
        s = s[:i] + CSS + s[i:]
    # link no rodapé (nav "Arial Gamer" do rodapé, não a de abas)
    m = re.search(r'(\n([ \t]*)<nav aria-label="Arial Gamer">(\r?\n))', s)
    if m and 'href="#sobre"' not in s[m.end():m.end() + 400]:
        ind = m.group(2) + "  "
        s = s[:m.end()] + f'{ind}<a href="#sobre">{L["rodape"]}</a>\n' + s[m.end():]
    open(p, "w", encoding="utf-8", newline="").write(s)
    print("ok", d)
