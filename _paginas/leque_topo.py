# Leque de celulares do topo com 9 jogos (Turma Arial à esquerda, Deicida no meio, Golaço Total logo à direita),
# nos 8 idiomas. Pode rodar mais de uma vez.   python _paginas/leque_topo.py
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQS = ["index.html"] + [f"{l}/index.html" for l in ("en", "es", "de", "fr", "it", "ja", "zh")]
ROTULO = {"index.html": "Vídeos dos nove jogos", "en": "Videos of the nine games", "es": "Videos de los nueve juegos",
          "de": "Videos der neun Spiele", "fr": "Vidéos des neuf jeux", "it": "Video dei nove giochi",
          "ja": "9つのゲームの動画", "zh": "九款游戏的视频"}

# (deslocamento %, giro, descida px, escala) do meio para fora; o lado direito é o espelho
POS = [(0, 0, -14, 1), (50, 6, 22, .88), (94, 12, 60, .76), (132, 17, 100, .66), (164, 22, 142, .56)]
HOVER = [(0, 0, -14, 1), (56, 8, 16, .88), (102, 14, 54, .76), (142, 19, 94, .66), (176, 24, 136, .56)]
CEL = [(0, 0, -14, 1), (42, 5, 14, .85), (76, 10, 36, .72), (104, 15, 58, .62), (128, 19, 80, .54)]
Z = [9, 7, 5, 3, 1]


def regras(tab, hover=False, sel=".fan"):
    out = []
    for i in range(1, 10):
        d = i - 5
        x, r, y, s = tab[abs(d)]
        sx = "-" if d < 0 else ""
        if d == 0:
            t = f"translateY({y}px)"
        else:
            t = f"translateX({sx}{x}%) rotate({sx}{r}deg) translateY({y}px) scale({s})"
        z = "" if hover else f"; z-index: {Z[abs(d)] - (1 if d > 0 and d != 0 else 0)}"
        if hover and d == 0:
            continue
        out.append(f"{sel}{':hover' if hover else ''} .phone:nth-child({i}) {{ transform: {t}{z} }}")
    return out


def css_novo():
    linhas = regras(POS) + regras(HOVER, hover=True)
    cel = " ".join(r.replace(".fan .phone", ".fan .phone") for r in regras(CEL))
    linhas.append("@media (max-width: 480px) { .fan .phone { width: 120px } " + re.sub(r"; z-index: \d+", "", cel) + " }")
    linhas.append(".fan .screen img { width: 100%; height: 100%; object-fit: cover; display: block }")
    return "\n".join(linhas)


def main():
    for rel in ARQS:
        p = os.path.join(RAIZ, rel)
        s = open(p, encoding="utf-8", newline="").read()
        if "media/golaco-topo.jpg" in s:
            print(rel, "já estava")
            continue
        nl = "\r\n" if "\r\n" in s else "\n"
        a = s.index(".fan .phone:nth-child(1) { transform: translateX(-146%)")
        b = s.index(nl, s.index(".fan .phone:nth-child(7) { transform: translateX(118%)"))
        s = s[:a] + css_novo().replace("\n", nl) + s[b:]
        f0 = s.index('<div class="fan"')
        # celulares: Turma Arial no começo e Golaço Total logo depois do Deicida
        m = re.compile(r'(<div class="fan" aria-label=")[^"]*(">\r?\n)([ \t]*)').search(s, f0)
        ind = m.group(3)
        lang = rel.split("/")[0] if "/" in rel else "index.html"
        pre = "" if rel == "index.html" else "/"
        turma = f'<div class="phone"><div class="screen"><img src="{pre}media/turma-topo.jpg" alt="Turma Arial" loading="lazy" width="540" height="1170"></div></div>{nl}{ind}'
        s = s[:m.start()] + m.group(1) + ROTULO[lang] + m.group(2) + ind + turma + s[m.end():]
        d = s.index("deicida-chamada.mp4", f0)
        fim = s.index("</div></div>" + nl, d) + len("</div></div>" + nl)
        golaco = f'{ind}<div class="phone"><div class="screen"><img src="{pre}media/golaco-topo.jpg" alt="Golaço Total" loading="lazy" width="540" height="1170"></div></div>{nl}'
        s = s[:fim] + golaco + s[fim:]
        open(p, "w", encoding="utf-8", newline="").write(s)
        print(rel, "ok")


if __name__ == "__main__":
    main()
