# Acervo, planos em 28/11/2026 (8 idiomas): o plano grátis ganha 1 avaliação completa (busca na web) por conta e o
# Premium anual tem teste grátis de 7 dias para quem nunca assinou. O plano grátis com 1 item já tinha sido atualizado
# (commit 4303ddc). Muda a página principal, a página do Acervo, as páginas por categoria e as perguntas frequentes.
import glob, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

TROCAS = {
 "pt": [("1 item com até 3 fotos, relatório e nuvem, sem anúncios.", "1 item com até 3 fotos, relatório, nuvem e 1 avaliação completa para ver quanto ele vale, sem anúncios."),
        ("<b>Grátis:</b> 1 item com até 3 fotos, relatório e nuvem.", "<b>Grátis:</b> 1 item com até 3 fotos, relatório, nuvem e 1 avaliação completa."),
        ("1 item com até 3 fotos, relatório e nuvem.</p>", "1 item com até 3 fotos, relatório, nuvem e 1 avaliação completa para ver quanto ele vale.</p>"),
        ("R$ 9,90/mês ou R$ 79,90/ano.", "R$ 9,90/mês ou R$ 79,90/ano, com 7 dias grátis no anual para quem nunca assinou."),
        ("No Premium, o app pesquisa", "No Premium (e 1 vez no plano grátis), o app pesquisa")],
 "en": [("1 item with up to 3 photos, report and cloud, with no ads.", "1 item with up to 3 photos, report, cloud and 1 full valuation to see what it’s worth, with no ads."),
        ("as a monthly or yearly subscription.", "as a monthly or yearly subscription, with a 7-day free trial on the yearly plan if you’ve never subscribed."),
        ("<b>Free:</b> 1 item with up to 3 photos, report and cloud.", "<b>Free:</b> 1 item with up to 3 photos, report, cloud and 1 full valuation."),
        ("every AI valuation, monthly or yearly.", "every AI valuation, monthly or yearly (7 days free on the yearly plan)."),
        ("1 item with up to 3 photos, report and cloud.</p>", "1 item with up to 3 photos, report, cloud and 1 full valuation to see what it’s worth.</p>"),
        ("Monthly or yearly, at your country’s store price.", "Monthly or yearly, at your country’s store price. The yearly plan has 7 days free if you’ve never subscribed."),
        ("iPhone and Android. Optional Premium subscription.", "iPhone and Android. Optional Premium subscription, with 7 days free on the yearly plan."),
        ("With Premium, the app searches", "With Premium (and once on the free plan), the app searches")],
 "es": [("1 artículo con hasta 3 fotos, informe y nube, sin anuncios.", "1 artículo con hasta 3 fotos, informe, nube y 1 valoración completa para ver cuánto vale, sin anuncios."),
        ("con suscripción mensual o anual.", "con suscripción mensual o anual, y 7 días gratis en el plan anual si nunca te suscribiste."),
        ("<b>Gratis:</b> 1 artículo con hasta 3 fotos, informe y nube.", "<b>Gratis:</b> 1 artículo con hasta 3 fotos, informe, nube y 1 valoración completa."),
        ("toda la valoración con IA, mensual o anual.", "toda la valoración con IA, mensual o anual (7 días gratis en el plan anual)."),
        ("1 artículo con hasta 3 fotos, informe y nube.</p>", "1 artículo con hasta 3 fotos, informe, nube y 1 valoración completa para ver cuánto vale.</p>"),
        ("Mensual o anual, al precio de la tienda de tu país.", "Mensual o anual, al precio de la tienda de tu país. El plan anual tiene 7 días gratis si nunca te suscribiste."),
        ("iPhone y Android. Suscripción Premium opcional.", "iPhone y Android. Suscripción Premium opcional, con 7 días gratis en el plan anual."),
        ("Con Premium, la app busca", "Con Premium (y una vez en el plan gratis), la app busca")],
 "de": [("1 Objekt mit bis zu 3 Fotos, Bericht und Cloud, ohne Werbung.", "1 Objekt mit bis zu 3 Fotos, Bericht, Cloud und 1 vollständige Bewertung, um zu sehen, was es wert ist, ohne Werbung."),
        ("als Monats- oder Jahresabo.", "als Monats- oder Jahresabo, mit 7 Tagen gratis beim Jahresabo, wenn du noch nie abonniert hast."),
        ("<b>Kostenlos:</b> 1 Objekt mit bis zu 3 Fotos, Bericht und Cloud.", "<b>Kostenlos:</b> 1 Objekt mit bis zu 3 Fotos, Bericht, Cloud und 1 vollständige Bewertung."),
        ("alle KI-Bewertungen, monatlich oder jährlich.", "alle KI-Bewertungen, monatlich oder jährlich (7 Tage gratis beim Jahresabo)."),
        ("1 Objekt mit bis zu 3 Fotos, Bericht und Cloud.</p>", "1 Objekt mit bis zu 3 Fotos, Bericht, Cloud und 1 vollständige Bewertung, um zu sehen, was es wert ist.</p>"),
        ("Monatlich oder jährlich, zum Preis des Stores in deinem Land.", "Monatlich oder jährlich, zum Preis des Stores in deinem Land. Das Jahresabo hat 7 Tage gratis, wenn du noch nie abonniert hast."),
        ("iPhone und Android. Optionales Premium-Abo.", "iPhone und Android. Optionales Premium-Abo, mit 7 Tagen gratis beim Jahresabo."),
        ("Mit Premium sucht die App", "Mit Premium (und einmal im kostenlosen Tarif) sucht die App")],
 "fr": [("1 objet avec jusqu’à 3 photos, rapport et cloud, sans publicité.", "1 objet avec jusqu’à 3 photos, rapport, cloud et 1 estimation complète pour savoir ce qu’il vaut, sans publicité."),
        ("avec un abonnement mensuel ou annuel.", "avec un abonnement mensuel ou annuel, et 7 jours gratuits sur l’annuel si vous ne vous êtes jamais abonné."),
        ("<b>Gratuit :</b> 1 objet avec jusqu’à 3 photos, rapport et cloud.", "<b>Gratuit :</b> 1 objet avec jusqu’à 3 photos, rapport, cloud et 1 estimation complète."),
        ("toute l’estimation par IA, au mois ou à l’année.", "toute l’estimation par IA, au mois ou à l’année (7 jours gratuits sur l’annuel)."),
        ("1 objet avec jusqu’à 3 photos, rapport et cloud.</p>", "1 objet avec jusqu’à 3 photos, rapport, cloud et 1 estimation complète pour savoir ce qu’il vaut.</p>"),
        ("Au mois ou à l’année, au prix de la boutique de votre pays.", "Au mois ou à l’année, au prix de la boutique de votre pays. L’annuel a 7 jours gratuits si vous ne vous êtes jamais abonné."),
        ("iPhone et Android. Abonnement Premium facultatif.", "iPhone et Android. Abonnement Premium facultatif, avec 7 jours gratuits sur l’annuel."),
        ("Avec Premium, l’app cherche", "Avec Premium (et une fois avec l’offre gratuite), l’app cherche")],
 "it": [("1 oggetto con fino a 3 foto, report e cloud, senza pubblicità.", "1 oggetto con fino a 3 foto, report, cloud e 1 valutazione completa per sapere quanto vale, senza pubblicità."),
        ("con abbonamento mensile o annuale.", "con abbonamento mensile o annuale, e 7 giorni gratis sull’annuale se non ti sei mai abbonato."),
        ("<b>Gratis:</b> 1 oggetto con fino a 3 foto, report e cloud.", "<b>Gratis:</b> 1 oggetto con fino a 3 foto, report, cloud e 1 valutazione completa."),
        ("tutta la valutazione con IA, mensile o annuale.", "tutta la valutazione con IA, mensile o annuale (7 giorni gratis sull’annuale)."),
        ("1 oggetto con fino a 3 foto, report e cloud.</p>", "1 oggetto con fino a 3 foto, report, cloud e 1 valutazione completa per sapere quanto vale.</p>"),
        ("Mensile o annuale, al prezzo dello store del tuo paese.", "Mensile o annuale, al prezzo dello store del tuo paese. L’annuale ha 7 giorni gratis se non ti sei mai abbonato."),
        ("iPhone e Android. Abbonamento Premium facoltativo.", "iPhone e Android. Abbonamento Premium facoltativo, con 7 giorni gratis sull’annuale."),
        ("Con Premium, l’app cerca", "Con Premium (e una volta con il piano gratis), l’app cerca")],
 "ja": [("アイテム 1 点、写真 3 枚まで、レポートとクラウド、広告なし。", "アイテム 1 点、写真 3 枚まで、レポートとクラウド、価値がわかる完全な評価 1 回、広告なし。"),
        ("Premium（月額または年額）では、アイテム無制限、写真 20 枚まで、AI による評価が使えます。", "Premium（月額または年額）では、アイテム無制限、写真 20 枚まで、AI による評価が使えます。年額プランは、初めての方なら 7 日間無料。"),
        ("<b>無料：</b> アイテム 1 点、写真 3 枚まで、レポートとクラウド。", "<b>無料：</b> アイテム 1 点、写真 3 枚まで、レポートとクラウド、完全な評価 1 回。"),
        ("すべての AI 評価。月額または年額。", "すべての AI 評価。月額または年額（年額は 7 日間無料）。"),
        ("アイテム 1 点、写真 3 枚まで、レポートとクラウド。</p>", "アイテム 1 点、写真 3 枚まで、レポートとクラウド、価値がわかる完全な評価 1 回。</p>"),
        ("月額または年額、あなたの国のストア価格で。", "月額または年額、あなたの国のストア価格で。年額プランは、初めての方なら 7 日間無料。"),
        ("iPhone・Android。プレミアムは任意のサブスクリプション。", "iPhone・Android。プレミアムは任意のサブスクリプション（年額は 7 日間無料）。"),
        ("Premium では、eBay を参考に", "Premium（無料プランでも 1 回）では、eBay を参考に")],
 "zh": [("1 件藏品，最多 3 张照片，含报告和云端，没有广告。", "1 件藏品，最多 3 张照片，含报告、云端和 1 次完整估值，看看它值多少，没有广告。"),
        ("Premium（按月或按年订阅）提供不限藏品、每件最多 20 张照片和 AI 估值。", "Premium（按月或按年订阅）提供不限藏品、每件最多 20 张照片和 AI 估值。从未订阅过的用户，年度订阅可免费试用 7 天。"),
        ("<b>免费：</b> 1 件藏品，最多 3 张照片，含报告和云端。", "<b>免费：</b> 1 件藏品，最多 3 张照片，含报告、云端和 1 次完整估值。"),
        ("全部 AI 估值，按月或按年订阅。", "全部 AI 估值，按月或按年订阅（年度订阅免费试用 7 天）。"),
        ("1 件藏品，最多 3 张照片，含报告和云端。</p>", "1 件藏品，最多 3 张照片，含报告、云端和 1 次完整估值，看看它值多少。</p>"),
        ("按月或按年订阅，价格以你所在国家的应用商店为准。", "按月或按年订阅，价格以你所在国家的应用商店为准。从未订阅过的用户，年度订阅可免费试用 7 天。"),
        ("iPhone 和 Android。可选高级订阅。", "iPhone 和 Android。可选高级订阅（年度订阅免费试用 7 天）。"),
        ("在 Premium 中，应用会参考 eBay", "在 Premium 中（免费版也可用 1 次），应用会参考 eBay")],
}
LANGS = ["en", "es", "de", "fr", "it", "ja", "zh"]
usadas = {l: [0] * len(t) for l, t in TROCAS.items()}
mudou = []
for arq in sorted(set(glob.glob("index.html") + glob.glob("*/index.html") + glob.glob("*/*/index.html") + glob.glob("*/*/*/index.html"))):
    arq = arq.replace(os.sep, "/")
    if arq.startswith(("_paginas", "play-dev-page", "divulgacao")) or "privacidade" in arq: continue
    top = arq.split("/")[0]; l = top if top in LANGS else "pt"
    s = open(arq, encoding="utf8", newline="").read(); o = s
    for k, (a, b) in enumerate(TROCAS[l]):
        if b in s: continue
        c = s.count(a)
        if c: s = s.replace(a, b); usadas[l][k] += c
    if s != o: open(arq, "w", encoding="utf8", newline="").write(s); mudou.append(arq)
for l, us in usadas.items():
    for k, n in enumerate(us):
        if n == 0: print("NÃO ACHEI", l, TROCAS[l][k][0][:70])
print(len(mudou), "páginas"); print("\n".join(mudou))
