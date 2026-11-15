# Faixa de números da home (0 anúncios, 11 mitologias...): um cartão por jogo, com o ícone,
# o número na cor do jogo e link para a seção do jogo. Aplica nos 8 idiomas; pode rodar de novo.
#   python _paginas/faixa_numeros.py
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDIOMAS = [".", "en", "es", "de", "fr", "it", "ja", "zh"]

# número -> (âncora, ícone, cor, brilho)
JOGOS = {
    "11": ("deicida", "deicida.png", "#ff8a3d", "rgba(255,96,40,.45)"),
    "31": ("rota", "rota.png", "#7fa8ff", "rgba(90,130,255,.45)"),
    "14": ("gol", "gol.png", "#3ddc84", "rgba(61,220,132,.4)"),
    "22": ("esconde", "esconde.png", "#b49cff", "rgba(180,156,255,.45)"),
    "100": ("gelada", "gelada.png", "#f6b83a", "rgba(246,184,58,.45)"),
}

ANCORA_CSS = "@media (min-width: 721px) { .facts .wrap { grid-template-columns: repeat(6, 1fr) } }"
CSS = """
/* ---------- Faixa de números: um cartão por jogo ---------- */
.facts { position: relative; overflow: hidden; isolation: isolate;
  background: radial-gradient(50% 140% at 15% 0%, rgba(255,96,40,.10), transparent 70%), radial-gradient(50% 140% at 85% 100%, rgba(90,130,255,.12), transparent 70%), linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01)) }
.facts::before { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background-image: radial-gradient(rgba(255,255,255,.10) 1px, transparent 1.4px); background-size: 26px 26px;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 20%, #000 80%, transparent); mask-image: linear-gradient(90deg, transparent, #000 20%, #000 80%, transparent) }
.facts .wrap { gap: 14px; padding-block: 38px }
.fact { position: relative; display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 20px 10px 18px; border-radius: 22px;
  text-decoration: none; color: inherit; overflow: hidden; isolation: isolate;
  background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,.02)); border: 1px solid rgba(255,255,255,.09);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.07); transition: transform .3s cubic-bezier(.2,.8,.2,1), border-color .3s, box-shadow .3s }
.fact::before { content: ""; position: absolute; left: -10%; right: -10%; bottom: -70%; height: 130%; z-index: -1;
  background: radial-gradient(closest-side, var(--glow), transparent); opacity: .55; transition: opacity .3s }
.fact::after { content: ""; position: absolute; left: 22%; right: 22%; top: 0; height: 2px; border-radius: 2px; background: var(--c); opacity: .8 }
a.fact:hover, a.fact:focus-visible { transform: translateY(-5px); border-color: color-mix(in srgb, var(--c) 55%, transparent); box-shadow: 0 18px 40px -20px var(--c), inset 0 1px 0 rgba(255,255,255,.1) }
a.fact:hover::before, a.fact:focus-visible::before { opacity: 1 }
.fact .ico { width: 58px; height: 58px; border-radius: 17px; margin-bottom: 8px; object-fit: cover;
  box-shadow: 0 10px 22px rgba(0,0,0,.45), 0 0 0 2px rgba(255,255,255,.14); transition: transform .3s cubic-bezier(.2,.8,.2,1) }
a.fact:hover .ico { transform: rotate(-7deg) scale(1.08) }
.facts .fact b { font-size: clamp(32px, 3.6vw, 46px); color: var(--c);
  background: linear-gradient(180deg, #fff 15%, var(--c) 95%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent }
.facts .fact span { font-size: 13.5px; line-height: 1.3; max-width: 18ch }
.fact.zero .ico { display: grid; place-items: center; font-size: 30px; line-height: 1; background: radial-gradient(circle at 32% 28%, #fff6c4, var(--gold) 55%, #d98f00) }
.facts .fact.zero span { color: var(--ink); font-weight: 700 }
@media (max-width: 720px) { .facts .wrap { gap: 12px; padding-block: 28px } .fact { padding: 16px 8px 14px } .fact .ico { width: 50px; height: 50px; border-radius: 15px } }
@media (prefers-reduced-motion: reduce) { .fact, .fact .ico, .fact::before { transition: none } a.fact:hover, a.fact:hover .ico { transform: none } }
"""

ZERO = re.compile(r'<div class="zero"><b>0</b><span>([^<]*)</span></div>')
ITEM = re.compile(r'<div><b>(\d+)</b><span>([^<]*)</span></div>')


def main():
    for l in IDIOMAS:
        p = os.path.join(RAIZ, l, "index.html")
        s = open(p, encoding="utf-8").read()
        a = s.index('<div class="facts"'); b = s.index("</div>\n  </div>", a)
        bloco = s[a:b]
        pre = "" if l == "." else "/"

        def item(m):
            num, txt = m.group(1), m.group(2)
            ancora, ico, cor, brilho = JOGOS[num]
            return (f'<a class="fact" href="#{ancora}" style="--c:{cor};--glow:{brilho}">'
                    f'<img class="ico" src="{pre}{ico}" alt="" width="58" height="58" loading="lazy"><b>{num}</b><span>{txt}</span></a>')

        novo = ZERO.sub(lambda m: f'<div class="fact zero" style="--c:var(--gold);--glow:rgba(255,210,63,.4)"><i class="ico" aria-hidden="true">🚫</i><b>0</b><span>{m.group(1)}</span></div>', bloco)
        novo = ITEM.sub(item, novo)
        s = s[:a] + novo + s[b:]
        if "Faixa de números: um cartão por jogo" not in s:
            s = s.replace(ANCORA_CSS, ANCORA_CSS + CSS, 1)
        open(p, "w", encoding="utf-8", newline="").write(s)
        print("ok:", l, novo.count('class="fact'), "cartões")


if __name__ == "__main__":
    main()
