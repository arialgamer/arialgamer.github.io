# Golaço Total e Acervo ganham o player com vídeo automático e a fileira de videozinhos, como os outros jogos (8 idiomas).
import re
L = {
 'pt': ('', 'Escolha um vídeo do {}', 'Ligar o som', ['Gol na quadra', 'Gol na areia', 'Versão adulta', 'Meu craque'], ['Coleção', 'Quanto vale', 'Identificar', 'Relatório']),
 'en': ('/', 'Pick a {} video', 'Turn sound on', ['Goal on court', 'Goal on sand', 'Grown-up version', 'My star'], ['Collection', 'What it’s worth', 'Identify', 'Report']),
 'es': ('/', 'Elige un video de {}', 'Activar sonido', ['Gol en la cancha', 'Gol en la arena', 'Versión adulta', 'Mi crack'], ['Colección', 'Cuánto vale', 'Identificar', 'Informe']),
 'de': ('/', 'Wähle ein {}-Video', 'Ton einschalten', ['Tor in der Halle', 'Tor im Sand', 'Erwachsenen-Version', 'Mein Star'], ['Sammlung', 'Was es wert ist', 'Erkennen', 'Bericht']),
 'fr': ('/', 'Choisis une vidéo de {}', 'Activer le son', ['But en salle', 'But sur sable', 'Version adulte', 'Mon crack'], ['Collection', 'Combien ça vaut', 'Identifier', 'Rapport']),
 'it': ('/', 'Scegli un video di {}', "Attiva l'audio", ['Gol in campo', 'Gol sulla sabbia', 'Versione adulta', 'Il mio campione'], ['Collezione', 'Quanto vale', 'Identifica', 'Report']),
 'ja': ('/', '{}の動画を選ぶ', '音をオンにする', ['コートでゴール', '砂浜でゴール', '大人向け版', 'マイスター'], ['コレクション', '査定額', '写真で判定', 'レポート']),
 'zh': ('/', '选择 {} 视频', '打开声音', ['室内进球', '沙滩进球', '成人版', '我的球星'], ['收藏', '估值', '识别', '报告']),
}
GOL = ['media/golaco-gol-quadra', 'media/golaco-gol-areia', 'media/golaco-gol-adulta', 'media/fotos/golaco-craque']
ACE = ['media/fotos/acervo-colecao', 'media/fotos/acervo-detalhe', 'media/fotos/acervo-identificar', 'media/fotos/acervo-relatorio']

def player(pre, grupo, som, nomes, srcs, wide, nl):
    cl = ''.join(f'{nl}          <button class="clip" type="button" aria-pressed="{"true" if k == 0 else "false"}" data-src="{pre}{s}"><img src="{pre}{s}.jpg" alt="" loading="lazy"><span class="bar"><span></span></span>{n}</button>' for k, (n, s) in enumerate(zip(nomes, srcs)))
    return (f'<div class="player reveal" data-player>{nl}        <div class="phone{" wide" if wide else ""}"><div class="screen">{nl}'
            f'          <video muted playsinline preload="none" poster="{pre}{srcs[0]}.jpg"><source src="{pre}{srcs[0]}.mp4" type="video/mp4"></video>{nl}'
            f'          <button class="sound" type="button" aria-label="{som}"><svg><use href="#i-muted"/></svg></button>{nl}'
            f'        </div></div>{nl}        <div class="clips" role="group" aria-label="{grupo}">{cl}{nl}        </div>{nl}      </div>')

for lg, (pre, grupo, som, ng, na) in L.items():
    arq = 'index.html' if lg == 'pt' else f'{lg}/index.html'
    s = open(arq, encoding='utf8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    for id, nomes, srcs, nome, wide in [('golaco', ng, GOL, 'Golaço Total', True), ('acervo', na, ACE, 'Acervo', False)]:
        i = s.find(f'id="{id}"')
        m = re.compile(r'<div class="player reveal">\s*<div class="phone[^"]*"><div class="screen"><img [^>]*></div></div>\s*</div>').search(s, i)
        assert m and m.start() - i < 6000, (arq, id)
        s = s[:m.start()] + player(pre, grupo.format(nome), som, nomes, srcs, wide, nl) + s[m.end():]
    open(arq, 'w', encoding='utf8', newline='').write(s)
    print('ok', arq)
