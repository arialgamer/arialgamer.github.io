# Vídeo vertical do Rota Estelar, já no iPhone e no Android (1080x1920, ~20 s, sem música: escolha o som no app).
# Usa as gravações do jogo em media/ e gera divulgacao/rota-lancamento.mp4 (pt) e divulgacao/en/rota-launch.mp4 (en).
#   python _paginas/video_rota.py  <ícone 512px da loja>
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1080, 1920
F_BLACK = "C:/Windows/Fonts/seguibl.ttf"
F_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
GOLD = (255, 210, 63); ORANGE = (255, 181, 71); BLUE = (127, 168, 255); INK = (246, 242, 255)

TEXTOS = {
    "pt": dict(saida="divulgacao/rota-lancamento.mp4", selo="JÁ NO IPHONE E NO ANDROID", sub="Jogo de nave para celular",
               cenas=[("rota-chefe", 0.0, "Um chefe gigante", "em cada planeta"),
                      ("rota-meteoros", 1.0, "Chuva de", "meteoros"),
                      ("rota-criaturas", 2.0, "20 criaturas", "e 10 naves"),
                      ("rota-tempestade", 1.0, "31 planetas", "de verdade")],
               fim=["Rota Estelar", "Já no iPhone e no Android", "App Store e Google Play", "", "Sem anúncios · sem compras no app"]),
    "en": dict(saida="divulgacao/en/rota-launch.mp4", selo="OUT NOW ON IPHONE AND ANDROID", sub="Space shooter for your phone",
               cenas=[("rota-chefe", 0.0, "A giant boss", "on every planet"),
                      ("rota-meteoros", 1.0, "Meteor", "showers"),
                      ("rota-criaturas", 2.0, "20 creatures", "and 10 ships"),
                      ("rota-tempestade", 1.0, "31 real", "planets")],
               fim=["Rota Estelar", "Out now on iPhone and Android", "App Store and Google Play", "", "No ads · no in-app purchases"]),
}


def fonte(p, t): return ImageFont.truetype(p, t)


def texto_c(d, y, s, f, cor, sombra=True):
    w = d.textlength(s, font=f)
    x = (W - w) / 2
    if sombra:
        d.text((x + 4, y + 5), s, font=f, fill=(0, 0, 0, 170))
    d.text((x, y), s, font=f, fill=cor)


def pilula(d, y, s, f, fundo, cor):
    w = d.textlength(s, font=f); h = f.size + 34
    x0 = (W - w) / 2 - 34
    d.rounded_rectangle((x0, y, x0 + w + 68, y + h), radius=h // 2, fill=fundo)
    d.text(((W - w) / 2, y + 12), s, font=f, fill=cor)


def camada_cena(t, l1, l2, icone, caminho, primeira):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # topo: ícone + nome + selo
    ic = icone.resize((150, 150)); m = Image.new("L", (150, 150), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 149, 149), 34, fill=255)
    im.paste(ic, ((W - 150) // 2, 150), m)
    texto_c(d, 320, "ROTA ESTELAR", fonte(F_BLACK, 92), INK)
    pilula(d, 450, t["selo"], fonte(F_BLACK, 40), GOLD + (255,), (42, 23, 3))
    # legenda da cena (embaixo do vídeo)
    texto_c(d, 1290, l1, fonte(F_BLACK, 104), INK)
    texto_c(d, 1410, l2, fonte(F_BLACK, 104), ORANGE)
    texto_c(d, 1760, "@arial.gamer", fonte(F_BOLD, 40), (220, 214, 245))
    im.save(caminho)


def camada_fim(t, icone, caminho):
    im = Image.new("RGBA", (W, H), (5, 8, 22, 205)); d = ImageDraw.Draw(im)
    brilho = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(brilho)
    bd.ellipse((W / 2 - 330, 360, W / 2 + 330, 1020), fill=(90, 130, 255, 120))
    im.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(90)))
    ic = icone.resize((380, 380)); m = Image.new("L", (380, 380), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 379, 379), 86, fill=255)
    im.paste(ic, ((W - 380) // 2, 470), m)
    nome, loja, plat, andr, extra = t["fim"]
    texto_c(d, 900, nome, fonte(F_BLACK, 120), INK)
    pilula(d, 1080, loja, fonte(F_BLACK, 54), GOLD + (255,), (42, 23, 3))
    texto_c(d, 1215, plat, fonte(F_BOLD, 56), INK)
    if andr: texto_c(d, 1300, andr, fonte(F_BOLD, 50), BLUE)
    texto_c(d, 1390 if andr else 1310, extra, fonte(F_BOLD, 40), (200, 192, 230))
    texto_c(d, 1640, "arialgamer.com.br", fonte(F_BLACK, 58), ORANGE)
    texto_c(d, 1720, "@arial.gamer", fonte(F_BOLD, 40), (220, 214, 245))
    im.save(caminho)


def roda(args):
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + args, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)


def gera(lang, icone, tmp):
    t = TEXTOS[lang]; partes = []
    DUR = 3.6
    fundo = ("[0:v]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.28:saturation=1.2[bg];"
             "[0:v]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2-110[v];[v][1:v]overlay=0:0")
    for i, (clip, ini, l1, l2) in enumerate(t["cenas"]):
        png = os.path.join(tmp, f"{lang}-c{i}.png"); camada_cena(t, l1, l2, icone, png, i == 0)
        out = os.path.join(tmp, f"{lang}-p{i}.mp4")
        fade = f",fade=t=in:st=0:d=0.35" if i == 0 else ""
        roda(["-ss", str(ini), "-t", str(DUR), "-i", os.path.join(RAIZ, "media", clip + ".mp4"), "-i", png,
              "-filter_complex", fundo + f",fps=30,format=yuv420p{fade}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "19", out])
        partes.append(out)
    # tela final sobre o vídeo do chefe, desfocado
    png = os.path.join(tmp, f"{lang}-fim.png"); camada_fim(t, icone, png)
    out = os.path.join(tmp, f"{lang}-fim.mp4")
    roda(["-ss", "5", "-t", "4.4", "-i", os.path.join(RAIZ, "media", "rota-chefe.mp4"), "-i", png,
          "-filter_complex", "[0:v]scale=-2:1920,crop=1080:1920,boxblur=30:2[bg];[bg][1:v]overlay=0:0,fps=30,format=yuv420p,fade=t=out:st=4.0:d=0.4",
          "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "19", out])
    partes.append(out)
    lista = os.path.join(tmp, f"{lang}.txt")
    open(lista, "w").write("".join(f"file '{p.replace(os.sep, '/')}'\n" for p in partes))
    destino = os.path.join(RAIZ, t["saida"]); os.makedirs(os.path.dirname(destino), exist_ok=True)
    # trilha de áudio muda (algumas redes recusam vídeo sem áudio)
    roda(["-f", "concat", "-safe", "0", "-i", lista, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
          "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", destino])
    # capa
    capa = destino.replace(".mp4", "-capa.jpg")
    roda(["-ss", "1.2", "-i", destino, "-frames:v", "1", "-q:v", "2", capa])
    print("ok:", t["saida"])


if __name__ == "__main__":
    icone = Image.open(sys.argv[1]).convert("RGB")
    with tempfile.TemporaryDirectory() as tmp:
        for lang in TEXTOS:
            gera(lang, icone, tmp)
