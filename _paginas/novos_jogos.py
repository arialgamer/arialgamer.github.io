# Coloca a Turma Arial e o Golaço Total em todo o site (8 idiomas) e acerta o que estava descasado:
# rodapé (jogos e privacidade), "Siga a Arial Gamer", números e preços do "Sobre", fatos do topo,
# texto de baixo do título, botão da Google Play da Turma e destaque do "Sem anúncios" (luz amarela piscando).
# Pode rodar mais de uma vez: cada troca confere se já foi feita.   python _paginas/novos_jogos.py
import os, re, glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["pt", "en", "es", "de", "fr", "it", "ja", "zh"]
HL = {"pt": "", "en": "&amp;hl=en", "es": "&amp;hl=es", "de": "&amp;hl=de", "fr": "&amp;hl=fr", "it": "&amp;hl=it", "ja": "&amp;hl=ja", "zh": "&amp;hl=zh-CN"}

GOLACO_FRASE = {
 "pt": "Jogue futsal e futebol de areia 5 contra 5. ",
 "en": "Play 5-a-side futsal and beach football. ",
 "es": "Juega futsal y fútbol playa 5 contra 5. ",
 "de": "Spiel Futsal und Beachsoccer 5 gegen 5. ",
 "fr": "Joue au futsal et au beach soccer à 5 contre 5. ",
 "it": "Gioca a futsal e beach soccer 5 contro 5. ",
 "ja": "5人制のフットサルとビーチサッカーで遊ぼう。",
 "zh": "踢一场五人制室内足球或沙滩足球。",
}
CAUDA_VELHA = {"pt": "Sete jogos", "en": "Seven games", "es": "Siete juegos", "de": "Sieben Spiele", "fr": "Sept jeux",
               "it": "Sette giochi", "ja": "ひとりでも友だちとでも遊べる7つのゲーム", "zh": "七款游戏"}
CAUDA_NOVA = {
 "pt": "Oito jogos para jogar sozinho ou com um amigo, a Turma Arial, grátis, para curtir com a turma, e o Acervo, para catalogar a sua coleção.",
 "en": "Eight games to play alone or with a friend, the free Turma Arial app to enjoy with your crew, and Acervo, to catalog your collection.",
 "es": "Ocho juegos para jugar solo o con un amigo, Turma Arial, gratis, para disfrutar con tu grupo, y Acervo, para catalogar tu colección.",
 "de": "Acht Spiele für allein oder mit Freunden, die kostenlose App Turma Arial für deine Clique und Acervo, um deine Sammlung zu erfassen.",
 "fr": "Huit jeux à jouer seul ou avec un ami, l'app gratuite Turma Arial à partager entre amis, et Acervo, pour cataloguer votre collection.",
 "it": "Otto giochi da fare da solo o con un amico, l'app gratuita Turma Arial da usare con gli amici e Acervo, per catalogare la tua collezione.",
 "ja": "ひとりでも友だちとでも遊べる8つのゲーム。仲間と楽しむ無料アプリ Turma Arial。そして、コレクションを整理する Acervo。",
 "zh": "八款游戏，一个人或和朋友一起玩。还有和朋友一起玩的免费应用 Turma Arial，以及帮你登记收藏的 Acervo。",
}
FATO_GOLACO = {"pt": "seleções no Golaço Total", "en": "national teams in Golaço Total", "es": "selecciones en Golaço Total",
               "de": "Nationalteams in Golaço Total", "fr": "sélections dans Golaço Total", "it": "nazionali in Golaço Total",
               "ja": "Golaço Totalの代表チーム", "zh": "Golaço Total 中的国家队"}
FATO_TURMA = {"pt": "espaços na Turma Arial, grátis", "en": "spaces in the free Turma Arial app", "es": "espacios en Turma Arial, gratis",
              "de": "Bereiche in der Gratis-App Turma Arial", "fr": "espaces dans Turma Arial, gratuit", "it": "spazi in Turma Arial, gratis",
              "ja": "無料アプリ Turma Arial のスペース", "zh": "免费应用 Turma Arial 的空间"}
NUM_JOGOS = {"pt": "jogos", "en": "games", "es": "juegos", "de": "Spiele", "fr": "jeux", "it": "giochi", "ja": "ゲーム", "zh": "款游戏"}
NUM_APPS = {"pt": "apps: Turma Arial e Acervo", "en": "apps: Turma Arial and Acervo", "es": "apps: Turma Arial y Acervo",
            "de": "Apps: Turma Arial und Acervo", "fr": "apps : Turma Arial et Acervo", "it": "app: Turma Arial e Acervo",
            "ja": "アプリ（Turma Arial・Acervo）", "zh": "款应用：Turma Arial 和 Acervo"}
PR_TURMA = {"pt": "Grátis", "en": "Free", "es": "Gratis", "de": "Kostenlos", "fr": "Gratuit", "it": "Gratis", "ja": "無料", "zh": "免费"}
PF_TURMA = {
 "pt": "Android (Google Play). Em breve no iPhone e iPad. Sem anúncios e sem compras.",
 "en": "Android (Google Play). Coming soon to iPhone and iPad. No ads, no purchases.",
 "es": "Android (Google Play). Muy pronto en iPhone y iPad. Sin anuncios ni compras.",
 "de": "Android (Google Play). Bald für iPhone und iPad. Ohne Werbung und ohne Käufe.",
 "fr": "Android (Google Play). Bientôt sur iPhone et iPad. Sans pub ni achats.",
 "it": "Android (Google Play). Presto su iPhone e iPad. Senza pubblicità né acquisti.",
 "ja": "Android（Google Play）。iPhone・iPad 版は近日公開。広告なし、課金なし。",
 "zh": "Android（Google Play）。iPhone 和 iPad 版即将推出。无广告，无内购。",
}
PF_GOLACO = {
 "pt": "Em breve no iPhone, iPad e Android. Jogo completo, sem compras dentro do app.",
 "en": "Coming soon to iPhone, iPad and Android. Full game, no in-app purchases.",
 "es": "Muy pronto en iPhone, iPad y Android. Juego completo, sin compras dentro de la app.",
 "de": "Bald für iPhone, iPad und Android. Vollversion, ohne In-App-Käufe.",
 "fr": "Bientôt sur iPhone, iPad et Android. Jeu complet, sans achats intégrés.",
 "it": "Presto su iPhone, iPad e Android. Gioco completo, senza acquisti in-app.",
 "ja": "iPhone・iPad・Android で近日公開。完全版、アプリ内課金なし。",
 "zh": "即将登陆 iPhone、iPad 和 Android。完整版，无内购。",
}

JOGOS = [  # (nome, caminho da página do jogo ou None = âncora da página inicial, âncora, privacidade)
 ("Turma Arial", None, "turma", "turma-privacidade/"),
 ("Deicida", "deicida/", None, "deicida-privacidade/"),
 ("Golaço Total", None, "golaco", "golaco-privacidade/"),
 ("Rota Estelar", "rota-estelar/", None, "rota-estelar-privacidade/"),
 ("Vôlei Total", "volei-total/", None, "volei-privacidade/"),
 ("Gol de Placa", "gol-de-placa/", None, "gol-privacidade/"),
 ("Xodó", "xodo/", None, "xodo-privacidade/"),
 ("Esconde-Esconde", "esconde-esconde/", None, "esconde-privacidade/"),
 ("Gelada", "gelada/", None, "gelada-privacidade/"),
 ("Acervo", "acervo/", None, "acervo/privacidade/"),
]

CSS_NOVO = """
/* ---------- destaque do texto de baixo do título e do "Sem anúncios" (luz amarela) ---------- */
.hero p.lead { color: var(--ink); max-width: 46ch; padding: 14px 18px; border-left: 4px solid var(--gold); background: rgba(255,210,63,.07); border-radius: 0 16px 16px 0 }
.noads { position: relative; border: 2px solid var(--gold); animation: noadsBrilho 2.2s ease-in-out infinite }
.noads i { font-size: 30px; filter: drop-shadow(0 0 6px rgba(255,210,63,.7)) }
.luz { position: absolute; width: 12px; height: 12px; border-radius: 50%; background: #ffd23f; box-shadow: 0 0 8px 3px rgba(255,210,63,.9); animation: luzPisca 1.1s ease-in-out infinite }
.luz.a { top: -7px; right: -7px } .luz.b { bottom: -7px; left: -7px; animation-delay: .55s }
.fact.zero { position: relative; border-color: var(--gold) }
@keyframes luzPisca { 0%, 100% { opacity: 1; transform: scale(1) } 50% { opacity: .15; transform: scale(.7) } }
@keyframes noadsBrilho { 0%, 100% { box-shadow: 0 0 12px rgba(255,210,63,.2) } 50% { box-shadow: 0 0 0 4px rgba(255,210,63,.15), 0 0 26px rgba(255,210,63,.55) } }
@media (prefers-reduced-motion: reduce) { .noads, .luz { animation: none } }
@media (max-width: 560px) { .grid6 { grid-template-columns: repeat(2, 1fr) !important } .grid6 a { aspect-ratio: 4 / 3 } }
"""


def lang_de(caminho):
    rel = os.path.relpath(caminho, RAIZ).replace("\\", "/")
    p = rel.split("/")[0]
    return p if p in LANGS[1:] else "pt"


def prefixo(s):
    """Prefixo dos links de jogo neste arquivo (ex.: '', '/', '/en/', '../'), a partir do link do Deicida no rodapé."""
    bloco = re.search(r'<div class="fjogos">.*?</nav>', s, re.S).group(0)
    return re.search(r'<a href="([^"]*)deicida/">', bloco).group(1)


def home(pre, lang):
    if lang == "pt":
        return pre if pre not in ("", "./") else ""
    return pre


def rodape(s, lang):
    pre = prefixo(s)
    # Jogos e apps
    m = re.search(r'(<div class="fjogos">\s*<p class="ftit">[^<]*</p>\s*<nav aria-label="[^"]*">)(.*?)(\n\s*</nav>)', s, re.S)
    ind = re.search(r'\n(\s*)<a ', m.group(2)).group(1)
    linhas = []
    for nome, pag, anc, _ in JOGOS:
        href = pre + pag if pag else (pre if pre else "") + "#" + anc
        linhas.append(f'\n{ind}<a href="{href}">{nome}</a>')
    s = s[:m.start(2)] + "".join(linhas) + s[m.end(2):]
    # Privacidade: mesmo jeito de escrever do link do Deicida
    m = re.search(r'(<div class="fpriv">\s*<p class="ftit">[^<]*</p>\s*<nav aria-label="[^"]*">)(.*?)(\n\s*</nav>)', s, re.S)
    ind = re.search(r'\n(\s*)<a ', m.group(2)).group(1)
    d = re.search(r'<a href="([^"]*)deicida-privacidade/">([^<]*)</a>', m.group(2))
    ppre, rotulo = d.group(1), d.group(2)
    linhas = [f'\n{ind}<a href="{ppre}{priv}">{rotulo.replace("Deicida", nome)}</a>' for nome, _, _, priv in JOGOS]
    s = s[:m.start(2)] + "".join(linhas) + s[m.end(2):]
    return s


def siga(s, lang):
    if "<span>Turma Arial</span></a>" in s:
        return s
    g = s.index('<div class="grid6">')
    m = re.compile(r'(\r?\n)([ \t]*)(<a href="([^"]*)deicida/"[^>]*>.*?</a>)').search(s, g)
    if not m or m.start() > s.index("</div>", g):
        print("  (sem Deicida na grade do Siga)")
        return s
    nl, ind, pre = m.group(1), m.group(2), m.group(4)
    turma = f'{nl}{ind}<a href="{pre}#turma"><img src="/media/turma-inicio.jpg" alt="" loading="lazy"><span>Turma Arial</span></a>'
    golaco = f'{nl}{ind}<a href="{pre}#golaco"><img src="/media/golaco-quadra.jpg" alt="" loading="lazy"><span>Golaço Total</span></a>'
    return s[:m.start()] + turma + m.group(0) + golaco + s[m.end():]


def css(s):
    if "noadsBrilho" in s:
        return s
    s = s.replace(".grid6 { grid-template-columns: repeat(4, 1fr) }", ".grid6 { grid-template-columns: repeat(5, 1fr) }")
    i = s.index("</style>")
    return s[:i] + CSS_NOVO + s[i:]


def pagina_inicial(s, lang):
    # texto de baixo do título
    m = re.search(r'<p class="lead">([^<]*)</p>', s)
    lead = m.group(1)
    if GOLACO_FRASE[lang] not in lead:
        fim = re.search(r'[.。]\s?', lead).end()
        lead = lead[:fim] + GOLACO_FRASE[lang] + lead[fim:]
        lead = lead[:lead.index(CAUDA_VELHA[lang])] + CAUDA_NOVA[lang]
        s = s[:m.start(1)] + lead + s[m.end(1):]
    # luzes no "Sem anúncios" (topo e número 0)
    if 'class="luz a"' not in s:
        s = s.replace('<p class="noads"><i aria-hidden="true">🚫</i>',
                      '<p class="noads"><span class="luz a" aria-hidden="true"></span><span class="luz b" aria-hidden="true"></span><i aria-hidden="true">🚫</i>', 1)
        s = re.sub(r'(<div class="fact zero"[^>]*>)', r'\1<span class="luz a" aria-hidden="true"></span>', s, count=1)
    # fatos do topo
    if 'href="#golaco" style' not in s:
        m = re.search(r'<a class="fact" href="#deicida"[^>]*><img class="ico" src="([^"]*)deicida\.png".*?</a>', s)
        img = m.group(1)
        golaco = (f'\n      <a class="fact" href="#golaco" style="--c:#38d47a;--glow:rgba(56,212,122,.4)"><img class="ico" src="{img}golaco.png" alt="" width="58" height="58" loading="lazy">'
                  f'<b>16</b><span>{FATO_GOLACO[lang]}</span></a>')
        s = s[:m.end()] + golaco + s[m.end():]
        m = re.search(r'<div class="fact zero".*?</div>', s)
        turma = (f'\n      <a class="fact" href="#turma" style="--c:#e9b949;--glow:rgba(233,185,73,.4)"><img class="ico" src="{img}turma.png" alt="" width="58" height="58" loading="lazy">'
                 f'<b>8</b><span>{FATO_TURMA[lang]}</span></a>')
        s = s[:m.end()] + turma + s[m.end():]
        s = s.replace("@media (min-width: 721px) { .facts .wrap { grid-template-columns: repeat(4, 1fr) } }",
                      "@media (min-width: 721px) { .facts .wrap { grid-template-columns: repeat(5, 1fr) } }")
        s = s.replace("@media (min-width: 1180px) { .facts .wrap { grid-template-columns: repeat(8, 1fr) } }",
                      "@media (min-width: 1180px) { .facts .wrap { grid-template-columns: repeat(5, 1fr) } }")
    # Turma Arial já está no Google Play
    a, b = s.index('id="turma"'), s.index("</section>", s.index('id="turma"'))
    sec = s[a:b]
    if "com.arial.turma" not in sec:
        disp = re.search(r'details\?id=com\.arial\.voleitotal[^"]*"[^>]*><svg><use href="#i-play"/></svg><span><small>([^<]*)</small>', s).group(1)
        sec = re.sub(r'<span class="store outline wait"><svg><use href="#i-play"/></svg><span><small>[^<]*</small><strong>Google Play</strong></span></span>',
                     f'<a class="store" href="https://play.google.com/store/apps/details?id=com.arial.turma{HL[lang]}" target="_blank" rel="noopener"><svg><use href="#i-play"/></svg><span><small>{disp}</small><strong>Google Play</strong></span></a>', sec)
        s = s[:a] + sec + s[b:]
    # Sobre: números
    s = re.sub(r'<div class="num"><strong>7</strong><span>[^<]*</span></div><div class="num"><strong>1</strong><span>[^<]*</span></div>',
               f'<div class="num"><strong>8</strong><span>{NUM_JOGOS[lang]}</span></div><div class="num"><strong>2</strong><span>{NUM_APPS[lang]}</span></div>', s)
    # Sobre: tabela de preços
    if "turma-privacidade/\">" not in s[s.index('class="precos"'):s.index("</table>", s.index('class="precos"'))]:
        t0 = s.index('class="precos"'); t1 = s.index("</table>", t0)
        tab = s[t0:t1]
        rota = re.search(r'<tr><td><a href="([^"]*)rota-estelar/">Rota Estelar</a></td><td class="pr">([^<]*)</td><td class="pf">[^<]*</td><td class="pv"><a href="([^"]*)rota-estelar-privacidade/">([^<]*)</a></td></tr>', tab)
        pre, pr_pago, ppre, pol = rota.groups()
        pr_golaco = "R$ 4,90" if lang == "pt" else pr_pago
        lin_turma = (f'<tr><td><a href="{pre}#turma">Turma Arial</a></td><td class="pr">{PR_TURMA[lang]}</td><td class="pf">{PF_TURMA[lang]}</td>'
                     f'<td class="pv"><a href="{ppre}turma-privacidade/">{pol}</a></td></tr>')
        lin_golaco = (f'<tr><td><a href="{pre}#golaco">Golaço Total</a></td><td class="pr">{pr_golaco}</td><td class="pf">{PF_GOLACO[lang]}</td>'
                      f'<td class="pv"><a href="{ppre}golaco-privacidade/">{pol}</a></td></tr>')
        tab = tab.replace("<tbody>", "<tbody>" + lin_turma, 1)
        fim_deicida = tab.index("</tr>", tab.index("deicida/")) + len("</tr>")
        tab = tab[:fim_deicida] + lin_golaco + tab[fim_deicida:]
        s = s[:t0] + tab + s[t1:]
    return s


def main():
    arquivos = [f for f in glob.glob(os.path.join(RAIZ, "**", "index.html"), recursive=True)
                if "play-dev-page" not in f and "_paginas" not in f]
    mudou = []
    for f in arquivos:
        s0 = open(f, encoding="utf-8", newline="").read()
        if 'class="fjogos"' not in s0:
            continue
        lang = lang_de(f)
        s = rodape(s0, lang)
        if 'class="grid6"' in s:
            s = siga(s, lang)
        s = css(s)
        rel = os.path.relpath(f, RAIZ).replace("\\", "/")
        if rel in ("index.html",) or re.fullmatch(r"(en|es|de|fr|it|ja|zh)/index\.html", rel):
            s = pagina_inicial(s, lang)
        if s != s0:
            open(f, "w", encoding="utf-8", newline="").write(s)
            mudou.append(rel)
    print(len(mudou), "páginas atualizadas")
    for r in mudou:
        print(" ", r)


if __name__ == "__main__":
    main()
