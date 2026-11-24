# OBSOLETO (24/11/2026): o Rota já está no Android; não rode este script, ele voltaria textos de "em breve no Android".
# Rota Estelar saiu no iPhone (App Store, R$ 4,90); Android em análise no Google Play.
# Troca o "Em breve" do Rota por "Já na App Store" nos 8 idiomas (home, página do jogo, cartões de
# "outros jogos", descrições para o Google, perguntas frequentes e dados estruturados).
# Pode rodar de novo (não duplica). Quando o Android sair, ajuste ANDROID abaixo e rode de novo.
#   python _paginas/rota_lancamento.py
import json, os, re, subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IOS_ID = "6833923100"
PRECO = "4.90"

L = {
    ".": dict(soon="Em breve", novo="Novo jogo", preco="🚀 Novo jogo · R$ 4,90", card="Já na App Store", store_small="Baixar na",
              ios=f"https://apps.apple.com/br/app/id{IOS_ID}",
              p="<b>Já na App Store</b> para iPhone e iPad: jogo completo, sem compras dentro do app. <b>No Android</b>, está em análise no Google Play e chega em breve.",
              meta=("Em breve no iPhone e no Android", "Já na App Store para iPhone, em breve no Android"),
              faq=[("Em breve, para iPhone e iPad na App Store e para Android no Google Play.", "Já saiu para iPhone e iPad na App Store, por R$ 4,90. No Android, está em análise no Google Play e chega em breve.")]),
    "en": dict(soon="Coming soon", novo="New game", preco="🚀 New game", card="Out now on the App Store", store_small="Download on the",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>Out now on the App Store</b> for iPhone and iPad: the full game, no in-app purchases. <b>On Android</b>, it is in review on Google Play and coming soon.",
               meta=("Coming soon to iPhone and Android", "Out now on the App Store for iPhone, coming soon to Android"),
               faq=[("It&#x27;s coming soon to iPhone and iPad on the App Store and to Android on Google Play.", "It&#x27;s out now on the App Store for iPhone and iPad, and coming soon to Android on Google Play."),
                    ("It's coming soon to iPhone and iPad on the App Store and to Android on Google Play.", "It's out now on the App Store for iPhone and iPad, and coming soon to Android on Google Play.")]),
    "es": dict(soon="Muy pronto", novo="Nuevo juego", preco="🚀 Nuevo juego", card="Ya en la App Store", store_small="Descárgalo en",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>Ya en la App Store</b> para iPhone y iPad: juego completo, sin compras dentro de la app. <b>En Android</b>, está en revisión en Google Play y llega muy pronto.",
               meta=("Muy pronto en iPhone y Android", "Ya en la App Store para iPhone, muy pronto en Android"),
               faq=[("Muy pronto en iPhone y iPad en la App Store, y en Android en Google Play.", "Ya disponible en la App Store para iPhone y iPad; muy pronto en Android en Google Play.")]),
    "de": dict(soon="Bald verfügbar", novo="Neues Spiel", preco="🚀 Neues Spiel", card="Jetzt im App Store", store_small="Laden im",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>Jetzt im App Store</b> für iPhone und iPad: das komplette Spiel ohne In-App-Käufe. <b>Für Android</b> wird es gerade bei Google Play geprüft und kommt bald.",
               meta=("Bald für iPhone und Android", "Jetzt im App Store für iPhone, bald für Android"),
               faq=[("Bald für iPhone und iPad im App Store und für Android bei Google Play.", "Jetzt im App Store für iPhone und iPad; bald auch für Android bei Google Play.")]),
    "fr": dict(soon="Bientôt", novo="Nouveau jeu", preco="🚀 Nouveau jeu", card="Disponible sur l&#x27;App Store", store_small="Télécharger dans",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>Disponible sur l&#x27;App Store</b> pour iPhone et iPad : le jeu complet, sans achats intégrés. <b>Sur Android</b>, il est en cours de validation sur Google Play et arrive bientôt.",
               meta=("Bientôt sur iPhone et Android", "Disponible sur l&#x27;App Store pour iPhone, bientôt sur Android"),
               faq=[("Bientôt sur iPhone et iPad sur l&#x27;App Store, et sur Android sur Google Play.", "Disponible sur l&#x27;App Store pour iPhone et iPad ; bientôt sur Android sur Google Play."),
                    ("Bientôt sur iPhone et iPad sur l'App Store, et sur Android sur Google Play.", "Disponible sur l'App Store pour iPhone et iPad ; bientôt sur Android sur Google Play.")]),
    "it": dict(soon="In arrivo", novo="Nuovo gioco", preco="🚀 Nuovo gioco", card="Già sull&#x27;App Store", store_small="Scarica su",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>Già sull&#x27;App Store</b> per iPhone e iPad: gioco completo, senza acquisti in-app. <b>Su Android</b> è in revisione su Google Play e arriva presto.",
               meta=("Presto su iPhone e Android", "Già sull&#x27;App Store per iPhone, presto su Android"),
               faq=[("Presto su iPhone e iPad sull&#x27;App Store e su Android su Google Play.", "Già disponibile sull&#x27;App Store per iPhone e iPad; presto su Android su Google Play."),
                    ("Presto su iPhone e iPad sull'App Store e su Android su Google Play.", "Già disponibile sull'App Store per iPhone e iPad; presto su Android su Google Play.")]),
    "ja": dict(soon="近日公開", novo="新作", preco="🚀 新作", card="App Store で配信中", store_small="ダウンロード",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>App Store で配信中</b>：iPhone・iPad 向け。アプリ内課金なしの完全版です。<b>Android 版</b>は Google Play で審査中、近日公開。",
               meta=("iPhone と Android で近日公開", "iPhone は App Store で配信中、Android は近日公開"),
               faq=[("近日、App Store の iPhone・iPad と Google Play の Android で公開予定。", "App Store で iPhone・iPad 版を配信中。Google Play の Android 版も近日公開。")]),
    "zh": dict(soon="即将推出", novo="新游戏", preco="🚀 新游戏", card="已登陆 App Store", store_small="下载于",
               ios=f"https://apps.apple.com/app/id{IOS_ID}",
               p="<b>已登陆 App Store</b>，支持 iPhone 和 iPad：完整版游戏，无应用内购买。<b>Android 版</b>正在 Google Play 审核中，即将推出。",
               meta=("即将登陆 iPhone 和 Android", "已登陆 App Store（iPhone），Android 版即将推出"),
               faq=[("即将登陆 App Store 上的 iPhone 和 iPad，以及 Google Play 上的 Android。", "现已登陆 App Store（iPhone 和 iPad），Google Play 上的 Android 版即将推出。")]),
}

TAG = '<script type="application/ld+json">'


def bloco_rota(s, fn):
    """Aplica fn em cada <section class="game ... rota ..."> ... </section>."""
    out, pos = [], 0
    for m in re.finditer(r'<section class="game[^"]*\brota\b[^"]*"', s):
        if m.start() < pos:
            continue
        fim = s.index("</section>", m.start())
        out.append(s[pos:m.start()]); out.append(fn(s[m.start():fim])); pos = fim
    out.append(s[pos:])
    return "".join(out)


def ajusta_ld(s, t):
    def no(n):
        if isinstance(n, dict):
            if "VideoGame" in str(n.get("@type", "")) and "Rota" in str(n.get("name", "")):
                n["installUrl"] = [t["ios"]]
                n["downloadUrl"] = [t["ios"]]
                n["sameAs"] = [t["ios"]]
                n["offers"] = {"@type": "Offer", "price": PRECO, "priceCurrency": "BRL", "availability": "https://schema.org/InStock"}
            for v in n.values():
                no(v) if isinstance(v, dict) else [no(x) for x in v] if isinstance(v, list) else None
    partes, pos = [], 0
    while True:
        a = s.find(TAG, pos)
        if a < 0:
            break
        a += len(TAG); b = s.index("</script>", a)
        d = json.loads(s[a:b])
        if "Rota" not in s[a:b]:
            partes.append(s[pos:b]); pos = b; continue
        no(d)
        recuo = 1 if '\n "' in s[a:b] or '\n  {' in s[a:b] else None
        novo = "\n" + json.dumps(d, ensure_ascii=False, indent=recuo) + "\n" if recuo else json.dumps(d, ensure_ascii=False)
        partes.append(s[pos:a]); partes.append(novo); pos = b
    partes.append(s[pos:])
    return "".join(partes)


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8").stdout.split()
    n = 0
    for f in files:
        l = f.split("/")[0] if f.split("/")[0] in L else "."
        t = L[l]
        p = os.path.join(RAIZ, f)
        s = open(p, encoding="utf-8").read(); s0 = s
        if "Rota Estelar" not in s:
            continue

        def secao(b):
            b = b.replace(f'<p class="eyebrow">{t["soon"]}</p>', f'<p class="eyebrow">{t["novo"]}</p>')
            b = b.replace(f'<span class="price">🚀 {t["soon"]}</span>', f'<span class="price">{t["preco"]}</span>')
            b = re.sub(r'(<div class="soon">\s*<p>).*?(</p>)', lambda m: m.group(1) + t["p"] + m.group(2), b, count=1, flags=re.S)
            b = b.replace(f'<span class="store outline wait"><svg><use href="#i-apple"/></svg><span><small>iPhone</small><strong>{t["soon"]}</strong></span></span>',
                          f'<a class="store" href="{t["ios"]}" target="_blank" rel="noopener"><svg><use href="#i-apple"/></svg><span><small>{t["store_small"]}</small><strong>App Store</strong></span></a>')
            return b
        s = bloco_rota(s, secao)
        # cartões "outros jogos"
        s = s.replace(f'<b>Rota Estelar</b>{t["soon"]} ·', f'<b>Rota Estelar</b>{t["card"]} ·')
        # descrições (só as do Rota: as que falam dos 31 planetas)
        velho, bom = t["meta"]
        s = re.sub(r'(31[^"<]{0,400}?)' + re.escape(velho), lambda m: m.group(1) + bom, s)
        for velho, bom in t["faq"]:
            s = s.replace(velho, bom)
        if TAG in s:
            s = ajusta_ld(s, t)
        if s != s0:
            open(p, "w", encoding="utf-8", newline="").write(s); n += 1
            print("ajustado:", f)
    print(n, "arquivo(s)")


if __name__ == "__main__":
    main()
