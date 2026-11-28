# Turma Arial já na App Store (28/11/2026): botão da App Store ativo na vitrine da Turma, tabela "Onde jogar" e llms.txt, nos 8 idiomas.
import re, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ID = "6839198223"
BAIXAR = {"pt": "Baixar na", "en": "Download on the", "es": "Descárgalo en", "de": "Laden im", "fr": "Télécharger dans",
          "it": "Scarica su", "ja": "ダウンロード", "zh": "下载于"}
ONDE = {
    "pt": "iPhone, iPad e Android. Sem anúncios e sem compras.",
    "en": "iPhone, iPad and Android. No ads, no purchases.",
    "es": "iPhone, iPad y Android. Sin anuncios ni compras.",
    "de": "iPhone, iPad und Android. Ohne Werbung und ohne Käufe.",
    "fr": "iPhone, iPad et Android. Sans pub ni achats.",
    "it": "iPhone, iPad e Android. Senza pubblicità né acquisti.",
    "ja": "iPhone・iPad・Android。広告なし、課金なし。",
    "zh": "iPhone、iPad 和 Android。无广告，无内购。",
}

for lang in BAIXAR:
    arq = RAIZ / ("index.html" if lang == "pt" else f"{lang}/index.html")
    s = arq.read_bytes().decode("utf-8")
    url = f"https://apps.apple.com/br/app/id{ID}" if lang == "pt" else f"https://apps.apple.com/app/id{ID}"
    # 1) botão "Em breve na App Store" da vitrine da Turma vira link
    ini = s.index('id="turma"')
    fim = s.index("</section>", ini)
    trecho = s[ini:fim]
    novo, n = re.subn(r'<span class="store outline wait"><svg><use href="#i-apple"/></svg><span><small>[^<]*</small><strong>App Store</strong></span></span>',
                      f'<a class="store" href="{url}" target="_blank" rel="noopener"><svg><use href="#i-apple"/></svg><span><small>{BAIXAR[lang]}</small><strong>App Store</strong></span></a>',
                      trecho)
    assert n == 1, (lang, "botão", n)
    s = s[:ini] + novo + s[fim:]
    # 2) tabela "Onde jogar"
    s, n = re.subn(r'(#turma">Turma Arial</a></td><td class="pr">[^<]*</td><td class="pf">)[^<]*', lambda m: m.group(1) + ONDE[lang], s)
    assert n == 1, (lang, "tabela", n)
    arq.write_bytes(s.encode("utf-8"))
    print(lang, "ok")

llms = RAIZ / "llms.txt"
t = llms.read_bytes().decode("utf-8")
t2 = t.replace("On Google Play; coming soon to iPhone.", "On the App Store and Google Play.")
assert t2 != t
llms.write_bytes(t2.encode("utf-8"))
print("llms.txt ok")
