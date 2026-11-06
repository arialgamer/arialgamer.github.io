# Gera o kit de imprensa em inglês: /press/ (página + arialgamer-presskit.zip).
# Rode:  python _paginas/press.py
import html, os, re, shutil, zipfile
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://arialgamer.com.br/"
OUT = os.path.join(RAIZ, "press"); os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
idx = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
css = idx[idx.index("<style>") + 7: idx.index("</style>")]
sprite = idx[idx.index('<svg width="0"'): idx.index("</svg>") + 6]
e = html.escape

# imagens do kit (cópias com nome claro)
IMGS = [
 ("logo-1080.jpg", "arial-gamer-logo.jpg", "Arial Gamer logo"),
 ("gelada.png", "gelada-icon.png", "Gelada app icon"),
 ("esconde.png", "esconde-esconde-icon.png", "Esconde-Esconde app icon"),
 ("gol.png", "gol-de-placa-icon.png", "Gol de Placa app icon"),
 ("media/gelada-saude.jpg", "gelada-pour.jpg", "Gelada: pouring and drinking a beer"),
 ("media/gelada-talhou.jpg", "gelada-mix-score.jpg", "Gelada: mix score, milk with orange juice curdled"),
 ("media/gelada-caipirinha.jpg", "gelada-bar-counter.jpg", "Gelada: bar counter"),
 ("media/esconde-lua.jpg", "esconde-esconde-moon.jpg", "Esconde-Esconde: hiding on the moon"),
 ("media/esconde-maquina.jpg", "esconde-esconde-vs-computer.jpg", "Esconde-Esconde: playing against the computer"),
 ("media/esconde-pirata.jpg", "esconde-esconde-pirate-ship.jpg", "Esconde-Esconde: pirate ship"),
 ("media/gol-adulta.jpg", "gol-de-placa-grown-up.jpg", "Gol de Placa: grown-up version with realistic players"),
 ("media/gol-shot-gol.jpg", "gol-de-placa-goal.jpg", "Gol de Placa: kids version, goal at night"),
 ("media/gol-shot-falta.jpg", "gol-de-placa-free-kick.jpg", "Gol de Placa: free kick in the snow"),
 ("media/gol-shot-craque.jpg", "gol-de-placa-build-your-player.jpg", "Gol de Placa: build your player"),
]
for src, dst, _ in IMGS:
    shutil.copyfile(os.path.join(RAIZ, src), os.path.join(OUT, "img", dst))
# banner horizontal (capa do YouTube) se existir na pasta de divulgação
capa = os.path.join(RAIZ, "divulgacao", "youtube-capa.jpg")
if os.path.exists(capa):
    Image.open(capa).convert("RGB").save(os.path.join(OUT, "img", "arial-gamer-banner.jpg"), quality=90)
    IMGS.insert(1, ("", "arial-gamer-banner.jpg", "Arial Gamer banner (2048×1152)"))

with zipfile.ZipFile(os.path.join(OUT, "arialgamer-presskit.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for _, dst, _ in IMGS:
        z.write(os.path.join(OUT, "img", dst), "arialgamer-presskit/" + dst)
    z.writestr("arialgamer-presskit/README.txt",
        "Arial Gamer press kit\nhttps://arialgamer.com.br/press/\n\nYou may use these images and videos to write about or feature "
        "Gelada, Esconde-Esconde and Gol de Placa.\nContact: arial83gamer@gmail.com\n")

GAMES = [
 dict(nome="Gelada", sub="Virtual drinks", icon="gelada-icon.png", page="en/gelada/",
      pitch="Remember the app that turned your phone into a glass of beer? Gelada brings it back with 100 drinks, a mix mode where the order of the ingredients changes the result (milk with orange juice curdles!), a talking bartender, a drink of the day and a prank video mode. 100% virtual, 0% alcohol.",
      facts=[("Platforms", "iPhone, Android"), ("Genre", "Simulation, casual, humor"), ("Languages", "8"), ("Ads", "None")],
      stores=[("App Store", "https://apps.apple.com/app/id6819882963"), ("Google Play", "https://play.google.com/store/apps/details?id=com.arial.gelada&hl=en")],
      video="media/gelada-talhou.mp4"),
 dict(nome="Esconde-Esconde", sub="Hide and seek", icon="esconde-esconde-icon.png", page="en/esconde-esconde/",
      pitch="A brand-new hide-and-seek game made for the phone: hide, pass the phone and see if the other player finds you, or challenge the computer, which learns your tricks. 22 places by day and by night, a flashlight, a hot-or-cold radar, decoys, rain and lightning, a narrator and a mode for little ones. Online play with a room code.",
      facts=[("Platforms", "iPhone, Android"), ("Genre", "Family, casual"), ("Players", "1–4, local or online"), ("Ads", "None")],
      stores=[("App Store", "https://apps.apple.com/app/id6819893974"), ("Google Play", "https://play.google.com/store/apps/details?id=com.arial.escondeesconde&hl=en")],
      video="media/esconde-lua.mp4"),
 dict(nome="Gol de Placa", sub="Penalties and free kicks", icon="gol-de-placa-icon.png", page="en/gol-de-placa/",
      pitch="A 3D penalty and free-kick game: drag from the ball to the corner and let it fly, or stand in goal and dive. Pick the kids version with colorful blocky players or the grown-up version with realistic players and fans. National teams and clubs, rain, snow and night games, a Cup mode, stickers, daily challenges, commentary in 14 languages and online play with a friend.",
      facts=[("Platforms", "iPhone (Android coming soon)"), ("Genre", "Sports, soccer, family"), ("Players", "1–2, local or online"), ("Ads", "None")],
      stores=[("App Store", "https://apps.apple.com/app/id6823608331")],
      video="media/gol-adulta.mp4"),
]

def bloco_jogo(g):
    facts = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in g["facts"])
    lojas = " ".join(f'<a class="btn ghost" href="{u}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in g["stores"])
    return f"""
    <article class="pk-game">
      <div class="pk-head"><img src="img/{g['icon']}" alt="{e(g['nome'])} icon" width="72" height="72"><div><p class="eyebrow">{e(g['sub'])}</p><h3>{e(g['nome'])}</h3></div></div>
      <p>{e(g['pitch'])}</p>
      <dl class="pk-facts">{facts}</dl>
      <div class="pk-acts"><a class="btn primary" href="/{g['page']}">Game page</a> {lojas} <a class="btn ghost" href="/{g['video']}" download>Gameplay video (MP4)</a></div>
    </article>"""

galeria = "\n".join(f'      <a href="img/{d}" download><img src="img/{d}" alt="{e(t)}" loading="lazy"><span>{e(t)}</span></a>' for _, d, t in IMGS)

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Press kit · Arial Gamer, mobile games made in Brazil</title>
<meta name="description" content="Press kit for Arial Gamer, an indie mobile game studio from Brazil: facts, logos, icons, screenshots, gameplay videos and contact for Gelada, Esconde-Esconde and Gol de Placa.">
<link rel="canonical" href="{SITE}press/">
<meta property="og:type" content="website">
<meta property="og:title" content="Arial Gamer press kit">
<meta property="og:description" content="Logos, screenshots, videos and facts about Gelada, Esconde-Esconde and Gol de Placa.">
<meta property="og:image" content="{SITE}press/img/arial-gamer-logo.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Figtree:wght@400;500;600;700&display=swap">
<style>{css}
.pk {{ padding: calc(110px + env(safe-area-inset-top, 0px)) 0 80px }}
.pk h1 {{ font-size: clamp(40px, 6vw, 68px); font-weight: 800; margin: 8px 0 14px }}
.pk h2 {{ font-size: clamp(28px, 4vw, 40px); font-weight: 800; margin: 64px 0 18px }}
.pk .lead {{ color: var(--muted); font-size: 19px; max-width: 62ch }}
.pk-facts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin: 18px 0 }}
.pk-facts div {{ background: var(--glass); border: 1px solid var(--line); border-radius: 14px; padding: 12px 14px }}
.pk-facts dt {{ color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: .08em }}
.pk-facts dd {{ margin: 4px 0 0; font-weight: 700 }}
.pk-game {{ background: var(--glass); border: 1px solid var(--line); border-radius: 22px; padding: 24px; margin-bottom: 16px }}
.pk-game p {{ color: var(--ink); opacity: .92 }}
.pk-head {{ display: flex; gap: 16px; align-items: center }}
.pk-head img {{ border-radius: 18px }}
.pk-head h3 {{ font-size: 32px; margin: 0 }}
.pk-acts {{ display: flex; flex-wrap: wrap; gap: 10px }}
.pk-acts .btn {{ min-height: 46px; font-size: 15px }}
.pk-gal {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px }}
.pk-gal a {{ display: block; text-decoration: none; background: var(--glass); border: 1px solid var(--line); border-radius: 16px; overflow: hidden }}
.pk-gal img {{ width: 100%; aspect-ratio: 3 / 4; object-fit: cover }}
.pk-gal span {{ display: block; padding: 8px 10px; font-size: 13px; color: var(--muted) }}
.pk-contact {{ background: var(--glass-2); border-radius: 22px; padding: 26px; border: 1px solid var(--line) }}
.pk-contact a {{ color: var(--gold) }}
</style>
</head>
<body>
{sprite}
<header class="nav solid" id="nav">
  <div class="wrap">
    <a class="brand" href="/en/"><img src="/logo.png" alt="" width="38" height="38">Arial Gamer</a>
    <ul>
      <li><a href="/en/gelada/">Gelada</a></li>
      <li><a href="/en/esconde-esconde/">Esconde-Esconde</a></li>
      <li><a href="/en/gol-de-placa/">Gol de Placa</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
    <a class="pill" href="arialgamer-presskit.zip" download>Download kit</a>
  </div>
</header>
<main class="pk">
  <div class="wrap">
    <p class="eyebrow">Press kit</p>
    <h1>Arial Gamer</h1>
    <p class="lead">Arial Gamer is an independent mobile game studio from Brazil. We make short, joyful games for phones that families and friends can play together: Gelada, Esconde-Esconde and Gol de Placa. All games are ad-free, need no sign-up, collect no data and are available in 8 languages.</p>
    <dl class="pk-facts">
      <div><dt>Studio</dt><dd>Arial Gamer</dd></div>
      <div><dt>Based in</dt><dd>Brazil</dd></div>
      <div><dt>Games</dt><dd>3 (iPhone and Android)</dd></div>
      <div><dt>Languages</dt><dd>EN, PT, ES, DE, FR, IT, ZH, JA</dd></div>
      <div><dt>Website</dt><dd><a href="/en/">arialgamer.com.br</a></dd></div>
      <div><dt>Social</dt><dd>@arial.gamer</dd></div>
    </dl>
    <div class="pk-acts"><a class="btn primary" href="arialgamer-presskit.zip" download>Download all images (ZIP)</a></div>

    <h2>Games</h2>
{''.join(bloco_jogo(g) for g in GAMES)}

    <h2>Logos and screenshots</h2>
    <p class="lead">Click any image to download it. You may use these images and videos to write about or feature our games.</p>
    <div class="pk-gal">
{galeria}
    </div>

    <h2>Videos</h2>
    <p class="lead">Short gameplay clips are on our YouTube channel <a href="https://www.youtube.com/@arialgamer" target="_blank" rel="noopener">@arialgamer</a> and on <a href="https://www.tiktok.com/@arial.gamer" target="_blank" rel="noopener">TikTok</a>. You can also download the MP4 files from each game above.</p>

    <h2 id="contact">Contact</h2>
    <div class="pk-contact">
      <p>For press, reviews, YouTube features or promo codes, write to <a href="mailto:arial83gamer@gmail.com">arial83gamer@gmail.com</a>.</p>
      <p>Instagram and TikTok: <a href="https://www.instagram.com/arial.gamer/" target="_blank" rel="noopener">@arial.gamer</a> · YouTube: <a href="https://www.youtube.com/@arialgamer" target="_blank" rel="noopener">@arialgamer</a></p>
    </div>
  </div>
</main>
</body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(PAGE)
print("ok press", len(IMGS), "imagens", os.path.getsize(os.path.join(OUT, "arialgamer-presskit.zip")) // 1024, "KB")
