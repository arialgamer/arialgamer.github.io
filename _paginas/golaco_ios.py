# Golaço Total já na App Store (28/11/2026): botão da App Store ativo, textos, tabela "Onde jogar" e llms.txt, nos 8 idiomas.
# O Google Play continua "em breve".
import re, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ID = "6839199363"
T = {
    "pt": ("Baixar na", "Novo no iPhone · em breve no Android",
           "<b>Já na App Store</b>, para iPhone e iPad, por R$ 4,90: jogo completo, sem anúncios e sem compras dentro do app. No Google Play, em breve.",
           "iPhone e iPad; Android em breve. Jogo completo, sem compras dentro do app."),
    "en": ("Download on the", "New on iPhone · Android soon",
           "<b>Now on the App Store</b>, for iPhone and iPad: the full game, no ads and no in-app purchases. Coming soon to Google Play.",
           "iPhone and iPad; Android coming soon. Full game, no in-app purchases."),
    "es": ("Descárgalo en", "Nuevo en iPhone · pronto en Android",
           "<b>Ya en la App Store</b>, para iPhone y iPad: el juego completo, sin anuncios y sin compras dentro de la app. Muy pronto en Google Play.",
           "iPhone y iPad; Android muy pronto. Juego completo, sin compras dentro de la app."),
    "de": ("Laden im", "Neu auf dem iPhone · bald auf Android",
           "<b>Jetzt im App Store</b>, für iPhone und iPad: das komplette Spiel, ohne Werbung und ohne In-App-Käufe. Bald auch bei Google Play.",
           "iPhone und iPad; Android bald. Vollversion, ohne In-App-Käufe."),
    "fr": ("Télécharger dans", "Nouveau sur iPhone · bientôt sur Android",
           "<b>Déjà sur l'App Store</b>, pour iPhone et iPad : le jeu complet, sans pub et sans achats intégrés. Bientôt sur Google Play.",
           "iPhone et iPad ; Android bientôt. Jeu complet, sans achats intégrés."),
    "it": ("Scarica su", "Nuovo su iPhone · presto su Android",
           "<b>Già su App Store</b>, per iPhone e iPad: il gioco completo, senza pubblicità e senza acquisti in-app. Presto su Google Play.",
           "iPhone e iPad; Android presto. Gioco completo, senza acquisti in-app."),
    "ja": ("ダウンロード", "iPhone で配信開始・Android は近日",
           "<b>App Store で配信中</b>。iPhone と iPad 向けの完全版で、広告もアプリ内課金もありません。Google Play は近日公開。",
           "iPhone・iPad、Android は近日。完全版、アプリ内課金なし。"),
    "zh": ("下载于", "已登陆 iPhone · Android 即将推出",
           "<b>已登陆 App Store</b>，支持 iPhone 和 iPad：完整游戏，无广告，无应用内购买。即将登陆 Google Play。",
           "iPhone 和 iPad；Android 即将推出。完整版，无内购。"),
}

for lang, (baixar, eyebrow, soon, onde) in T.items():
    arq = RAIZ / ("index.html" if lang == "pt" else f"{lang}/index.html")
    s = arq.read_bytes().decode("utf-8")
    url = f"https://apps.apple.com/br/app/id{ID}" if lang == "pt" else f"https://apps.apple.com/app/id{ID}"
    ini = s.index('id="golaco"'); fim = s.index("</section>", ini)
    tr = s[ini:fim]
    tr, n = re.subn(r'<span class="store outline wait"><svg><use href="#i-apple"/></svg><span><small>[^<]*</small><strong>App Store</strong></span></span>',
                    f'<a class="store" href="{url}" target="_blank" rel="noopener"><svg><use href="#i-apple"/></svg><span><small>{baixar}</small><strong>App Store</strong></span></a>', tr)
    assert n == 1, (lang, "botão", n)
    tr, n = re.subn(r'<p class="eyebrow">[^<]*</p>', f'<p class="eyebrow">{eyebrow}</p>', tr, count=1); assert n == 1, (lang, "eyebrow")
    tr, n = re.subn(r'<div class="soon"><p>.*?</p></div>', f'<div class="soon"><p>{soon}</p></div>', tr, count=1, flags=re.S); assert n == 1, (lang, "soon")
    s = s[:ini] + tr + s[fim:]
    s, n = re.subn(r'(#golaco">Golaço Total</a></td><td class="pr">[^<]*</td><td class="pf">)[^<]*', lambda m: m.group(1) + onde, s)
    assert n == 1, (lang, "tabela", n)
    arq.write_bytes(s.encode("utf-8"))
    print(lang, "ok")

llms = RAIZ / "llms.txt"
t = llms.read_bytes().decode("utf-8")
t2 = t.replace("Coming soon to iPhone and Android (paid, no in-app purchases).", "On the App Store for iPhone and iPad; coming soon to Android (paid, no in-app purchases).")
assert t2 != t
llms.write_bytes(t2.encode("utf-8"))
print("llms.txt ok")
