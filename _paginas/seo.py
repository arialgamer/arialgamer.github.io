# Ajustes para a busca do Google, aplicados direto nas páginas publicadas.
# Pode rodar quantas vezes quiser (não duplica nada). Rode de novo depois dos outros scripts:
#   python _paginas/seo.py
#
# - Não mexe em preços: eles ficam como estão nas páginas (iguais aos das lojas).
# - Cada jogo diz ao Google quais são as páginas dele nas lojas ("sameAs").
# - A marca Arial Gamer aponta para as redes e para as páginas de desenvolvedor nas lojas.
# - Título e descrição da home citam todos os jogos e apps.
import json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<script type="application/ld+json">'

ORG_SAMEAS = [
    "https://www.tiktok.com/@arial.gamer",
    "https://www.instagram.com/arial.gamer/",
    "https://www.youtube.com/@arialgamer",
    "https://play.google.com/store/apps/dev?id=7102410817973589199",
    "https://apps.apple.com/br/developer/renato-nogueira/id6819882965",
]

HOME_TITULO = ("<title>Arial Gamer · Jogos e apps para celular: Gelada, Esconde-Esconde, Gol de Placa e Acervo</title>",
               "<title>Arial Gamer · Jogos e apps para celular: Gol de Placa, Esconde-Esconde, Gelada, Deicida, Rota Estelar e Acervo</title>")
HOME_DESC_FIM = ("E o Acervo: Sua Coleção, app grátis para catalogar e avaliar coleções.",
                 "Novo: Rota Estelar (nave espacial por 31 planetas), já na App Store. Em breve: Deicida (ação contra os deuses do Egito). E o Acervo: Sua Coleção, app grátis para catalogar e avaliar coleções.")


def ajusta_no(n):
    tipo = str(n.get("@type", ""))
    if tipo == "Organization":
        n["sameAs"] = ORG_SAMEAS
    if "VideoGame" in tipo or "MobileApplication" in tipo:
        lojas = n.get("installUrl")
        if lojas:
            lojas = lojas if isinstance(lojas, list) else [lojas]
            lojas = [u for u in lojas if u.startswith("https://")]
            # O Gol de Placa já está no Google Play (alguns dados antigos só tinham a App Store)
            if any("id6823608331" in u for u in lojas) and not any("goldeplaca" in u for u in lojas):
                lojas.append("https://play.google.com/store/apps/details?id=com.arial.goldeplaca")
            n["sameAs"] = lojas
    for v in n.values():
        if isinstance(v, dict):
            ajusta_no(v)
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, dict):
                    ajusta_no(x)


def ajusta_jsonld(s):
    partes, pos = [], 0
    while True:
        a = s.find(TAG, pos)
        if a < 0:
            break
        a += len(TAG); b = s.index("</script>", a)
        bloco = s[a:b]
        d = json.loads(bloco)
        ajusta_no(d)
        recuo = 1 if '\n "' in bloco or '\n  {' in bloco else None
        novo = "\n" + json.dumps(d, ensure_ascii=False, indent=recuo) + "\n" if recuo else json.dumps(d, ensure_ascii=False)
        partes.append(s[pos:a]); partes.append(novo); pos = b
    partes.append(s[pos:])
    return "".join(partes)


def main():
    mudou = 0
    for pasta, _, arqs in os.walk(RAIZ):
        rel = os.path.relpath(pasta, RAIZ)
        if rel != "." and rel.split(os.sep)[0].startswith((".", "_")):
            continue
        for nome in arqs:
            if not nome.endswith(".html"):
                continue
            p = os.path.join(pasta, nome)
            s = open(p, encoding="utf-8").read()
            novo = ajusta_jsonld(s) if TAG in s else s
            if rel == ".":
                novo = novo.replace(*HOME_TITULO)
                if "Em breve: Deicida" not in novo and "Novo: Rota Estelar" not in novo:
                    novo = novo.replace(*HOME_DESC_FIM)
            if novo != s:
                open(p, "w", encoding="utf-8", newline="").write(novo)
                mudou += 1
                print("ajustado:", os.path.relpath(p, RAIZ))
    print(mudou, "arquivo(s) ajustado(s)")


if __name__ == "__main__":
    main()
