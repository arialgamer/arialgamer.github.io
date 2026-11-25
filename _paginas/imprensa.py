# -*- coding: utf-8 -*-
"""Gera o kit de imprensa nos 8 idiomas a partir de press/index.html (inglês).

  PT  -> /imprensa/        EN -> /press/ (fonte)
  ES, DE, FR, IT, JA, ZH -> /<idioma>/press/

As imagens e o ZIP ficam só em /press/ e as outras versões apontam para lá.
Idempotente: roda quantas vezes quiser (python _paginas/imprensa.py).
"""
import io, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, 'press', 'index.html')
SITE = 'https://arialgamer.com.br'

LANGS = ['pt', 'en', 'es', 'de', 'fr', 'it', 'ja', 'zh']
URL = {'pt': '/imprensa/', 'en': '/press/', 'es': '/es/press/', 'de': '/de/press/',
       'fr': '/fr/press/', 'it': '/it/press/', 'ja': '/ja/press/', 'zh': '/zh/press/'}
HOME = {'pt': '/', 'en': '/en/', 'es': '/es/', 'de': '/de/', 'fr': '/fr/', 'it': '/it/', 'ja': '/ja/', 'zh': '/zh/'}
HTML_LANG = {'pt': 'pt-BR', 'en': 'en', 'es': 'es', 'de': 'de', 'fr': 'fr', 'it': 'it', 'ja': 'ja', 'zh': 'zh-Hans'}
PLAY_HL = {'pt': 'pt-BR', 'en': 'en', 'es': 'es', 'de': 'de', 'fr': 'fr', 'it': 'it', 'ja': 'ja', 'zh': 'zh-CN'}
LABEL = {'pt': 'Português', 'en': 'English', 'es': 'Español', 'de': 'Deutsch', 'fr': 'Français',
         'it': 'Italiano', 'ja': '日本語', 'zh': '中文'}
LANGS_ARIA = {'pt': 'Idioma', 'en': 'Language', 'es': 'Idioma', 'de': 'Sprache', 'fr': 'Langue',
              'it': 'Lingua', 'ja': '言語', 'zh': '语言'}

# ---------------------------------------------------------------- textos
T = {
'pt': {
 'Contact': 'Contato', 'Download kit': 'Baixar o kit', 'Press kit': 'Kit de imprensa',
 'Arial Gamer is an independent mobile game studio from Brazil. We make short, joyful games for phones that families and friends can play together: Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde and Gelada. All games are ad-free, need no sign-up, collect no data and are available in 8 languages. In 2026 we also launched Acervo, an app to catalog and value collections. New: Deicida, a cinematic hack and slash against the gods of 11 mythologies (out now on Android), and Rota Estelar, a space shooter for the whole family. New on iPhone: Vôlei Total, arcade volleyball, and Xodó, a virtual pet with Brazilian animals.':
 'A Arial Gamer é um estúdio independente de jogos para celular, do Brasil. Fazemos jogos curtos e alegres para jogar em família e com os amigos: Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde e Gelada. Todos os jogos são sem anúncios, sem cadastro, não coletam dados e estão em 8 idiomas. Em 2026 também lançamos o Acervo, um app para catalogar e avaliar coleções. Novidades: Deicida, um hack and slash cinematográfico contra os deuses de 11 mitologias (já no Android), e Rota Estelar, um jogo de nave para toda a família. Novos no iPhone: Vôlei Total, vôlei de arcade, e Xodó, um bichinho virtual com animais brasileiros.',
 'Studio': 'Estúdio', 'Based in': 'Sede', 'Brazil': 'Brasil', 'Games': 'Jogos',
 '7, all out now on iPhone and Android': '7, todos já lançados no iPhone e no Android',
 'Apps': 'Apps', 'Acervo (iPhone and Android)': 'Acervo (iPhone e Android)', 'Languages': 'Idiomas',
 'Website': 'Site', 'Social': 'Redes sociais', 'Download all images (ZIP)': 'Baixar todas as imagens (ZIP)',
 'Hack and slash · Out now on iPhone and Android': 'Hack and slash · Já no iPhone e no Android',
 'A cinematic hack and slash for phones: a mortal whose family was sacrificed to Ra comes back from the judgment of the Duat to hunt down and slay the gods of Egypt. The journey spans 11 mythologies, one per chapter: Egyptian, Mesopotamian, Aztec, Maya, Inca, Celtic, Slavic, Finnish, Roman, Norse and, last of all, Greek. Chapter I, Egypt, has 10 levels with a god as the boss of each one, from Sobek to Ra. Twin khopesh, combos, dodges, parries and slow-motion finishers, 3 powers per mythology (from the gods of levels 1, 5 and 10, while the other gods make them stronger), and epic narration with allies and bosses. Free on iPhone and Android: the prologue and the first level of Egypt are unlocked; levels 2 to 10 are coming soon as an in-app purchase. No ads.':
 'Um hack and slash cinematográfico para celular: um mortal cuja família foi sacrificada a Rá volta do julgamento do Duat para caçar e matar os deuses do Egito. A jornada passa por 11 mitologias, uma por capítulo: egípcia, mesopotâmica, asteca, maia, inca, celta, eslava, finlandesa, romana, nórdica e, por último, grega. O Capítulo I, Egito, tem 10 fases, cada uma com um deus como chefe, de Sobek a Rá. Duas khopesh, combos, esquivas, parry e golpes finais em câmera lenta, 3 poderes por mitologia (tomados dos deuses da 1ª, da 5ª e da 10ª fase; os outros deuses deixam esses poderes mais fortes) e narração épica com aliados e chefes. Grátis no iPhone e no Android: o prólogo e a primeira fase do Egito estão liberados; as fases 2 a 10 chegam em breve como compra no app. Sem anúncios.',
 'Platforms': 'Plataformas', 'Android (iPhone coming soon)': 'Android (iPhone em breve)', 'Genre': 'Gênero',
 'Action, hack and slash': 'Ação, hack and slash', 'Ads': 'Anúncios', 'None': 'Nenhum',
 'Game page': 'Página do jogo', 'Gameplay video (MP4)': 'Vídeo do jogo (MP4)',
 'Space shooter · Out now on iPhone and Android': 'Jogo de nave · Já no iPhone e no Android',
 'A landscape space shooter for kids and the whole family: drag your finger to fly from Earth to the most distant planet ever discovered, 28 million light-years away, while the ship fires on its own. 31 real planets with real science facts, 20 cartoon creatures, a giant boss on every planet, meteor showers, alien ruins and electric storms, 10 ships, 6 weapons, a narrator and an Easy mode. The full game, with no in-app purchases. Out now on the App Store for iPhone and iPad and on Google Play for Android.':
 'Um jogo de nave na horizontal para crianças e toda a família: arraste o dedo para voar da Terra até o planeta mais distante já descoberto, a 28 milhões de anos-luz, enquanto a nave atira sozinha. 31 planetas de verdade com curiosidades científicas reais, 20 criaturas de desenho, um chefe gigante em cada planeta, chuvas de meteoros, ruínas alienígenas e tempestades elétricas, 10 naves, 6 armas, narrador e modo Fácil. O jogo completo, sem compras no app. Já na App Store para iPhone e iPad e no Google Play.',
 'iPhone, Android': 'iPhone, Android', 'Action, space shooter, family': 'Ação, nave espacial, família',
 'Arcade volleyball · Out now on iPhone and Android': 'Vôlei de arcade · Já no iPhone e no Android',
 'Fast, arcade-style volleyball inspired by the 90s classics: 6v6 indoor with rotations and jump serves, 2v2 on the beach, a Super Spike in slow motion and on fire, a male or female commentator, a cheering crowd, an 8-team tournament and 2 players on the same phone. Original teams, two visual styles and 13 achievements. Paid download, the full game, with no ads and no in-app purchases. Out now on the App Store for iPhone and iPad and on Google Play for Android.':
 'Vôlei rápido, estilo arcade, inspirado nos clássicos dos anos 90: 6x6 na quadra com rodízio e saque viagem, 2x2 na praia, Super Cortada em câmera lenta e pegando fogo, narrador ou narradora, torcida vibrando, torneio com 8 seleções e 2 jogadores no mesmo celular. Times originais, dois estilos visuais e 13 conquistas. Jogo pago e completo, sem anúncios e sem compras no app. Já na App Store para iPhone e iPad e no Google Play.',
 'iPhone (Android coming soon)': 'iPhone (Android em breve)', 'Sports, volleyball, arcade': 'Esporte, vôlei, arcade',
 'Players': 'Jogadores', '1–2, same device': '1–2, no mesmo aparelho', 'Google Play: coming soon': 'Google Play: em breve',
 'Penalties and free kicks': 'Pênaltis e faltas',
 'A 3D penalty and free-kick game: drag from the ball to the corner and let it fly, or stand in goal and dive. Pick the kids version with colorful blocky players or the grown-up version with realistic players and fans. National teams and clubs, rain, snow and night games, a Cup mode, stickers, daily challenges, commentary in 14 languages and online play with a friend.':
 'Pênaltis e faltas em 3D: arraste da bola até o ângulo e solte, ou vá para o gol e salte. Escolha a versão infantil, com jogadores coloridos de bloquinhos, ou a versão adulta, com jogadores e torcida realistas. Seleções e clubes, jogos com chuva, neve e à noite, modo Copa, figurinhas, desafios diários, narração em 14 idiomas e partida online com um amigo.',
 'Sports, soccer, family': 'Esporte, futebol, família', '1–2, local or online': '1–2, local ou online',
 'Virtual pet · Out now on iPhone and Android': 'Bichinho virtual · Já no iPhone e no Android',
 'The 90s keychain virtual pet is back, with Brazilian animals: a capybara, a golden lion tamarin, an armadillo, a macaw, a river dolphin and an anteater. Hatch an egg, name your pet and look after it in real time, even with the app closed. It never dies, perfect for kids. Shake to bathe it, blow into the microphone to dry it, play 3 mini-games and fill an album with 18 forms. Retro or modern look. Paid download, no ads and no in-app purchases. Out now on the App Store for iPhone and iPad and on Google Play for Android.':
 'O bichinho virtual de chaveiro dos anos 90 está de volta, com animais brasileiros: capivara, mico-leão-dourado, tatu, arara, boto e tamanduá. Choque um ovo, dê um nome ao bichinho e cuide dele em tempo real, mesmo com o app fechado. Ele nunca morre, ideal para crianças. Chacoalhe para dar banho, sopre no microfone para secar, jogue 3 minijogos e complete um álbum com 18 formas. Visual retrô ou moderno. Jogo pago, sem anúncios e sem compras no app. Já na App Store para iPhone e iPad e no Google Play.',
 'Simulation, virtual pet, family': 'Simulação, bichinho virtual, família', 'Hide and seek': 'Esconde-esconde',
 'A brand-new hide-and-seek game made for the phone: hide, pass the phone and see if the other player finds you, or challenge the computer, which learns your tricks. 24 places by day and by night, a flashlight, a hot-or-cold radar, decoys, rain and lightning, a narrator and a mode for little ones. Online play with a room code.':
 'Um esconde-esconde novinho, feito para o celular: esconda-se, passe o celular e veja se o outro jogador te acha, ou desafie a máquina, que aprende os seus truques. 24 lugares de dia e de noite, lanterna, radar quente ou frio, iscas, chuva e relâmpagos, narrador e modo para os pequenos. Partida online com código de sala.',
 'Family, casual': 'Família, casual', '1–4, local or online': '1–4, local ou online', 'Virtual drinks': 'Bebidas virtuais',
 'Remember the app that turned your phone into a glass of beer? Gelada brings it back with 100 drinks, a mix mode where the order of the ingredients changes the result (milk with orange juice curdles!), a talking bartender, a drink of the day and a prank video mode. 100% virtual, 0% alcohol.':
 'Lembra do app que transformava o celular num copo de cerveja? O Gelada traz isso de volta com 100 bebidas, um modo de misturas em que a ordem dos ingredientes muda o resultado (leite com laranja talha!), um barman que fala, a bebida do dia e um modo de vídeo para pegadinhas. 100% virtual, 0% álcool.',
 'Simulation, casual, humor': 'Simulação, casual, humor', 'Collection catalog': 'Catálogo de coleções',
 'Acervo: Your Collection': 'Acervo: Sua Coleção',
 'Acervo is the catalog of your collection, with what each item is worth. Photograph watches, coins, stamps, trading cards, vinyl records or diecast cars, and the app identifies them from the photos with AI and shows the low, typical and high price on the used market in your currency. Collectors can share a single item by link, choosing what it shows, and find groups, forums and other Acervo collectors who own the same model; contact details are exchanged only if both accept. It works offline, syncs to the cloud and has no ads. Free to start, with an optional Premium subscription.':
 'O Acervo é o catálogo da sua coleção, com quanto vale cada item. Fotografe relógios, moedas, selos, cards, discos de vinil ou miniaturas, e o app identifica tudo pelas fotos com IA e mostra o preço baixo, típico e alto no mercado de usados, na sua moeda. Dá para compartilhar um item por link, escolhendo o que ele mostra, e encontrar grupos, fóruns e outros colecionadores do Acervo que têm o mesmo modelo; o contato só é trocado se os dois aceitarem. Funciona offline, sincroniza na nuvem e não tem anúncios. Grátis para começar, com assinatura Premium opcional.',
 'Category': 'Categoria', 'Lifestyle, collecting': 'Estilo de vida, colecionismo', 'App page': 'Página do app',
 'Logos and screenshots': 'Logos e telas',
 'Click any image to download it. You may use these images and videos to write about or feature our games and apps.':
 'Clique em qualquer imagem para baixar. Você pode usar estas imagens e vídeos para escrever sobre nossos jogos e apps ou divulgá-los.',
 'Videos': 'Vídeos', 'Short gameplay clips are on our YouTube channel': 'Trechos curtos dos jogos estão no nosso canal do YouTube',
 'and on': 'e no', '. You can also download the MP4 files from each game above.': '. Você também pode baixar os arquivos MP4 de cada jogo acima.',
 'For press, reviews, YouTube features or promo codes, write to': 'Para imprensa, análises, vídeos no YouTube ou códigos promocionais, escreva para',
 'Instagram and TikTok:': 'Instagram e TikTok:', '· YouTube:': '· YouTube:',
},
'es': {
 'Contact': 'Contacto', 'Download kit': 'Descargar kit', 'Press kit': 'Kit de prensa',
 'LEAD': 'Arial Gamer es un estudio independiente de juegos para móviles de Brasil. Hacemos juegos cortos y alegres para jugar en familia y con amigos: Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde y Gelada. Todos los juegos son sin anuncios, sin registro, no recogen datos y están en 8 idiomas. En 2026 también lanzamos Acervo, una app para catalogar y valorar colecciones. Novedades: Deicida, un hack and slash cinematográfico contra los dioses de 11 mitologías (ya en Android), y Rota Estelar, un juego de naves para toda la familia. Nuevos en iPhone: Vôlei Total, vóley arcade, y Xodó, una mascota virtual con animales brasileños.',
 'Studio': 'Estudio', 'Based in': 'Sede', 'Brazil': 'Brasil', 'Games': 'Juegos',
 '7, all out now on iPhone and Android': '7, todos ya disponibles en iPhone y Android',
 'Apps': 'Apps', 'Acervo (iPhone and Android)': 'Acervo (iPhone y Android)', 'Languages': 'Idiomas',
 'Website': 'Web', 'Social': 'Redes sociales', 'Download all images (ZIP)': 'Descargar todas las imágenes (ZIP)',
 'Hack and slash · Out now on iPhone and Android': 'Hack and slash · Ya en iPhone y Android',
 'DEICIDA': 'Un hack and slash cinematográfico para móviles: un mortal cuya familia fue sacrificada a Ra vuelve del juicio de la Duat para cazar y matar a los dioses de Egipto. El viaje recorre 11 mitologías, una por capítulo: egipcia, mesopotámica, azteca, maya, inca, celta, eslava, finlandesa, romana, nórdica y, por último, griega. El Capítulo I, Egipto, tiene 10 fases, cada una con un dios como jefe, de Sobek a Ra. Dos khopesh, combos, esquivas, bloqueos y remates a cámara lenta, 3 poderes por mitología (arrebatados a los dioses de las fases 1, 5 y 10; los demás dioses los hacen más fuertes) y una narración épica con aliados y jefes. Gratis en iPhone y Android: el prólogo y la primera fase de Egipto están desbloqueados; las fases 2 a 10 llegarán pronto como compra en la app. Sin anuncios.',
 'Platforms': 'Plataformas', 'Android (iPhone coming soon)': 'Android (iPhone próximamente)', 'Genre': 'Género',
 'Action, hack and slash': 'Acción, hack and slash', 'Ads': 'Anuncios', 'None': 'Ninguno',
 'Game page': 'Página del juego', 'Gameplay video (MP4)': 'Vídeo del juego (MP4)',
 'Space shooter · Out now on iPhone and Android': 'Juego de naves · Ya en iPhone y Android',
 'ROTA': 'Un juego de naves en horizontal para niños y toda la familia: desliza el dedo para volar desde la Tierra hasta el planeta más lejano jamás descubierto, a 28 millones de años luz, mientras la nave dispara sola. 31 planetas reales con datos científicos reales, 20 criaturas de dibujos animados, un jefe gigante en cada planeta, lluvias de meteoros, ruinas alienígenas y tormentas eléctricas, 10 naves, 6 armas, narrador y modo Fácil. El juego completo, sin compras en la app. Ya en la App Store para iPhone y iPad y en Google Play.',
 'iPhone, Android': 'iPhone, Android', 'Action, space shooter, family': 'Acción, naves, familia',
 'Arcade volleyball · Out now on iPhone and Android': 'Vóley arcade · Ya en iPhone y Android',
 'VOLEI': 'Vóley rápido de estilo arcade, inspirado en los clásicos de los 90: 6 contra 6 en pista con rotaciones y saque en salto, 2 contra 2 en la playa, un Súper Remate a cámara lenta y en llamas, comentarista hombre o mujer, público animando, un torneo de 8 selecciones y 2 jugadores en el mismo móvil. Equipos originales, dos estilos visuales y 13 logros. Juego de pago y completo, sin anuncios ni compras en la app. Ya en la App Store para iPhone y iPad y en Google Play.',
 'iPhone (Android coming soon)': 'iPhone (Android próximamente)', 'Sports, volleyball, arcade': 'Deportes, vóley, arcade',
 'Players': 'Jugadores', '1–2, same device': '1–2, en el mismo dispositivo', 'Google Play: coming soon': 'Google Play: próximamente',
 'Penalties and free kicks': 'Penaltis y faltas',
 'GOL': 'Penaltis y faltas en 3D: arrastra desde el balón hasta la escuadra y suéltalo, o ponte en la portería y lánzate. Elige la versión infantil, con jugadores de bloques de colores, o la versión adulta, con jugadores y afición realistas. Selecciones y clubes, partidos con lluvia, nieve y de noche, modo Copa, cromos, retos diarios, narración en 14 idiomas y partidas online con un amigo.',
 'Sports, soccer, family': 'Deportes, fútbol, familia', '1–2, local or online': '1–2, local u online',
 'Virtual pet · Out now on iPhone and Android': 'Mascota virtual · Ya en iPhone y Android',
 'XODO': 'Vuelve la mascota virtual de llavero de los 90, con animales brasileños: un carpincho, un tití león dorado, un armadillo, un guacamayo, un delfín rosado y un oso hormiguero. Abre un huevo, ponle nombre a tu mascota y cuídala en tiempo real, incluso con la app cerrada. Nunca muere, ideal para niños. Agita el móvil para bañarla, sopla en el micrófono para secarla, juega 3 minijuegos y completa un álbum con 18 formas. Estilo retro o moderno. Juego de pago, sin anuncios ni compras en la app. Ya en la App Store para iPhone y iPad y en Google Play.',
 'Simulation, virtual pet, family': 'Simulación, mascota virtual, familia', 'Hide and seek': 'Escondite',
 'ESCONDE': 'Un escondite totalmente nuevo hecho para el móvil: escóndete, pasa el móvil y mira si el otro jugador te encuentra, o desafía a la máquina, que aprende tus trucos. 24 lugares de día y de noche, linterna, radar frío o caliente, señuelos, lluvia y relámpagos, narrador y un modo para los peques. Partidas online con código de sala.',
 'Family, casual': 'Familia, casual', '1–4, local or online': '1–4, local u online', 'Virtual drinks': 'Bebidas virtuales',
 'GELADA': '¿Te acuerdas de la app que convertía el móvil en un vaso de cerveza? Gelada la recupera con 100 bebidas, un modo de mezclas en el que el orden de los ingredientes cambia el resultado (¡la leche con zumo de naranja se corta!), un barman que habla, la bebida del día y un modo de vídeo para bromas. 100% virtual, 0% alcohol.',
 'Simulation, casual, humor': 'Simulación, casual, humor', 'Collection catalog': 'Catálogo de colecciones',
 'Acervo: Your Collection': 'Acervo: Tu Colección',
 'ACERVO': 'Acervo es el catálogo de tu colección, con lo que vale cada pieza. Fotografía relojes, monedas, sellos, cromos, discos de vinilo o coches en miniatura, y la app los identifica por las fotos con IA y muestra el precio bajo, típico y alto en el mercado de segunda mano, en tu moneda. Puedes compartir una pieza por enlace, eligiendo lo que muestra, y encontrar grupos, foros y otros coleccionistas de Acervo que tienen el mismo modelo; los contactos solo se intercambian si ambos aceptan. Funciona sin conexión, se sincroniza en la nube y no tiene anuncios. Gratis para empezar, con suscripción Premium opcional.',
 'Category': 'Categoría', 'Lifestyle, collecting': 'Estilo de vida, coleccionismo', 'App page': 'Página de la app',
 'Logos and screenshots': 'Logos y capturas',
 'CLICK': 'Haz clic en cualquier imagen para descargarla. Puedes usar estas imágenes y vídeos para escribir sobre nuestros juegos y apps o darlos a conocer.',
 'Videos': 'Vídeos', 'Short gameplay clips are on our YouTube channel': 'Hay clips cortos de los juegos en nuestro canal de YouTube',
 'and on': 'y en', '. You can also download the MP4 files from each game above.': '. También puedes descargar los archivos MP4 de cada juego más arriba.',
 'For press, reviews, YouTube features or promo codes, write to': 'Para prensa, análisis, vídeos en YouTube o códigos promocionales, escribe a',
 'Instagram and TikTok:': 'Instagram y TikTok:', '· YouTube:': '· YouTube:',
},
'de': {
 'Contact': 'Kontakt', 'Download kit': 'Kit laden', 'Press kit': 'Pressekit',
 'LEAD': 'Arial Gamer ist ein unabhängiges Studio für Handyspiele aus Brasilien. Wir machen kurze, fröhliche Spiele, die Familien und Freunde zusammen spielen können: Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde und Gelada. Alle Spiele sind werbefrei, brauchen kein Konto, sammeln keine Daten und gibt es in 8 Sprachen. 2026 haben wir außerdem Acervo veröffentlicht, eine App, um Sammlungen zu katalogisieren und zu bewerten. Neu: Deicida, ein filmreifes Hack and Slash gegen die Götter von 11 Mythologien (jetzt für Android), und Rota Estelar, ein Weltraum-Shooter für die ganze Familie. Neu auf dem iPhone: Vôlei Total, Arcade-Volleyball, und Xodó, ein virtuelles Haustier mit brasilianischen Tieren.',
 'Studio': 'Studio', 'Based in': 'Sitz', 'Brazil': 'Brasilien', 'Games': 'Spiele',
 '7, all out now on iPhone and Android': '7, alle erschienen für iPhone und Android',
 'Apps': 'Apps', 'Acervo (iPhone and Android)': 'Acervo (iPhone und Android)', 'Languages': 'Sprachen',
 'Website': 'Website', 'Social': 'Soziale Medien', 'Download all images (ZIP)': 'Alle Bilder laden (ZIP)',
 'Hack and slash · Out now on iPhone and Android': 'Hack and Slash · Jetzt für iPhone und Android',
 'DEICIDA': 'Ein filmreifes Hack and Slash fürs Handy: Ein Sterblicher, dessen Familie Ra geopfert wurde, kehrt vom Totengericht der Duat zurück, um die Götter Ägyptens zu jagen und zu töten. Die Reise führt durch 11 Mythologien, eine pro Kapitel: ägyptisch, mesopotamisch, aztekisch, Maya, Inka, keltisch, slawisch, finnisch, römisch, nordisch und zuletzt griechisch. Kapitel I, Ägypten, hat 10 Level mit je einem Gott als Boss, von Sobek bis Ra. Zwei Khopesch, Combos, Ausweichen, Parieren und Finisher in Zeitlupe, 3 Kräfte pro Mythologie (von den Göttern der Level 1, 5 und 10; die übrigen Götter machen sie stärker) und epische Erzählung mit Verbündeten und Bossen. Kostenlos für iPhone und Android: Prolog und erstes Level in Ägypten sind freigeschaltet; die Level 2 bis 10 kommen bald als In-App-Kauf. Keine Werbung.',
 'Platforms': 'Plattformen', 'Android (iPhone coming soon)': 'Android (iPhone folgt bald)', 'Genre': 'Genre',
 'Action, hack and slash': 'Action, Hack and Slash', 'Ads': 'Werbung', 'None': 'Keine',
 'Game page': 'Spielseite', 'Gameplay video (MP4)': 'Gameplay-Video (MP4)',
 'Space shooter · Out now on iPhone and Android': 'Weltraum-Shooter · Jetzt für iPhone und Android',
 'ROTA': 'Ein Weltraum-Shooter im Querformat für Kinder und die ganze Familie: Zieh mit dem Finger, um von der Erde zum fernsten je entdeckten Planeten zu fliegen, 28 Millionen Lichtjahre entfernt, während das Schiff von selbst feuert. 31 echte Planeten mit echten Wissenschaftsfakten, 20 Cartoon-Kreaturen, ein Riesenboss auf jedem Planeten, Meteorschauer, Alien-Ruinen und Gewitterstürme, 10 Schiffe, 6 Waffen, ein Erzähler und ein Einfach-Modus. Das komplette Spiel, ohne In-App-Käufe. Jetzt im App Store für iPhone und iPad und bei Google Play.',
 'iPhone, Android': 'iPhone, Android', 'Action, space shooter, family': 'Action, Weltraum-Shooter, Familie',
 'Arcade volleyball · Out now on iPhone and Android': 'Arcade-Volleyball · Jetzt für iPhone und Android',
 'VOLEI': 'Schneller Arcade-Volleyball nach dem Vorbild der 90er-Klassiker: 6 gegen 6 in der Halle mit Rotation und Sprungaufschlag, 2 gegen 2 am Strand, ein Super-Schmetterball in Zeitlupe und in Flammen, Kommentator oder Kommentatorin, jubelndes Publikum, ein Turnier mit 8 Teams und 2 Spieler auf demselben Handy. Eigene Teams, zwei Grafikstile und 13 Erfolge. Kostenpflichtig und vollständig, ohne Werbung und ohne In-App-Käufe. Jetzt im App Store für iPhone und iPad und bei Google Play.',
 'iPhone (Android coming soon)': 'iPhone (Android folgt bald)', 'Sports, volleyball, arcade': 'Sport, Volleyball, Arcade',
 'Players': 'Spieler', '1–2, same device': '1–2, auf einem Gerät', 'Google Play: coming soon': 'Google Play: bald verfügbar',
 'Penalties and free kicks': 'Elfmeter und Freistöße',
 'GOL': 'Elfmeter und Freistöße in 3D: Zieh vom Ball in den Winkel und lass ihn fliegen, oder stell dich ins Tor und hechte. Wähle die Kinderversion mit bunten Klötzchen-Spielern oder die Erwachsenenversion mit realistischen Spielern und Fans. Nationalteams und Vereine, Spiele bei Regen, Schnee und Nacht, ein Pokal-Modus, Sticker, tägliche Herausforderungen, Kommentar in 14 Sprachen und Online-Spiele mit Freunden.',
 'Sports, soccer, family': 'Sport, Fußball, Familie', '1–2, local or online': '1–2, lokal oder online',
 'Virtual pet · Out now on iPhone and Android': 'Virtuelles Haustier · Jetzt für iPhone und Android',
 'XODO': 'Das virtuelle Schlüsselanhänger-Haustier der 90er ist zurück, mit brasilianischen Tieren: Wasserschwein, Goldgelbes Löwenäffchen, Gürteltier, Ara, Flussdelfin und Ameisenbär. Brüte ein Ei aus, gib deinem Haustier einen Namen und kümmere dich in Echtzeit darum, auch bei geschlossener App. Es stirbt nie, ideal für Kinder. Schütteln zum Baden, ins Mikrofon pusten zum Trocknen, 3 Minispiele und ein Album mit 18 Formen. Retro- oder moderner Look. Kostenpflichtig, ohne Werbung und ohne In-App-Käufe. Jetzt im App Store für iPhone und iPad und bei Google Play.',
 'Simulation, virtual pet, family': 'Simulation, virtuelles Haustier, Familie', 'Hide and seek': 'Verstecken',
 'ESCONDE': 'Ein ganz neues Versteckspiel fürs Handy: Versteck dich, gib das Handy weiter und schau, ob der andere dich findet, oder fordere den Computer heraus, der deine Tricks lernt. 24 Orte bei Tag und Nacht, eine Taschenlampe, ein Heiß-oder-kalt-Radar, Köder, Regen und Blitze, ein Erzähler und ein Modus für die Kleinen. Online-Spiele mit Raumcode.',
 'Family, casual': 'Familie, Casual', '1–4, local or online': '1–4, lokal oder online', 'Virtual drinks': 'Virtuelle Drinks',
 'GELADA': 'Erinnerst du dich an die App, die dein Handy in ein Bierglas verwandelte? Gelada bringt sie zurück, mit 100 Getränken, einem Mix-Modus, in dem die Reihenfolge der Zutaten das Ergebnis ändert (Milch mit Orangensaft gerinnt!), einem sprechenden Barkeeper, dem Drink des Tages und einem Video-Modus für Streiche. 100 % virtuell, 0 % Alkohol.',
 'Simulation, casual, humor': 'Simulation, Casual, Humor', 'Collection catalog': 'Sammlungskatalog',
 'Acervo: Your Collection': 'Acervo: Deine Sammlung',
 'ACERVO': 'Acervo ist der Katalog deiner Sammlung, mit dem Wert jedes Stücks. Fotografiere Uhren, Münzen, Briefmarken, Sammelkarten, Schallplatten oder Modellautos, und die App erkennt sie per KI anhand der Fotos und zeigt den niedrigen, typischen und hohen Gebrauchtmarktpreis in deiner Währung. Sammler können ein einzelnes Stück per Link teilen, mit selbst gewählten Angaben, und Gruppen, Foren und andere Acervo-Sammler mit demselben Modell finden; Kontaktdaten werden nur ausgetauscht, wenn beide zustimmen. Funktioniert offline, synchronisiert mit der Cloud und hat keine Werbung. Kostenlos zum Start, mit optionalem Premium-Abo.',
 'Category': 'Kategorie', 'Lifestyle, collecting': 'Lifestyle, Sammeln', 'App page': 'App-Seite',
 'Logos and screenshots': 'Logos und Screenshots',
 'CLICK': 'Klicke auf ein Bild, um es herunterzuladen. Du darfst diese Bilder und Videos verwenden, um über unsere Spiele und Apps zu schreiben oder sie vorzustellen.',
 'Videos': 'Videos', 'Short gameplay clips are on our YouTube channel': 'Kurze Gameplay-Clips findest du auf unserem YouTube-Kanal',
 'and on': 'und auf', '. You can also download the MP4 files from each game above.': '. Die MP4-Dateien jedes Spiels kannst du auch oben herunterladen.',
 'For press, reviews, YouTube features or promo codes, write to': 'Für Presse, Tests, YouTube-Videos oder Promo-Codes schreib an',
 'Instagram and TikTok:': 'Instagram und TikTok:', '· YouTube:': '· YouTube:',
},
'fr': {
 'Contact': 'Contact', 'Download kit': 'Télécharger le kit', 'Press kit': 'Kit presse',
 'LEAD': 'Arial Gamer est un studio indépendant de jeux mobiles basé au Brésil. Nous créons des jeux courts et joyeux, à jouer en famille et entre amis : Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde et Gelada. Tous nos jeux sont sans publicité, sans inscription, ne collectent aucune donnée et sont disponibles en 8 langues. En 2026, nous avons aussi lancé Acervo, une app pour cataloguer et estimer des collections. Nouveautés : Deicida, un hack and slash cinématographique contre les dieux de 11 mythologies (déjà sur Android), et Rota Estelar, un shoot spatial pour toute la famille. Nouveaux sur iPhone : Vôlei Total, du volley arcade, et Xodó, un animal virtuel avec des animaux brésiliens.',
 'Studio': 'Studio', 'Based in': 'Siège', 'Brazil': 'Brésil', 'Games': 'Jeux',
 '7, all out now on iPhone and Android': '7, tous disponibles sur iPhone et Android',
 'Apps': 'Apps', 'Acervo (iPhone and Android)': 'Acervo (iPhone et Android)', 'Languages': 'Langues',
 'Website': 'Site web', 'Social': 'Réseaux sociaux', 'Download all images (ZIP)': 'Télécharger toutes les images (ZIP)',
 'Hack and slash · Out now on iPhone and Android': 'Hack and slash · Disponible sur iPhone et Android',
 'DEICIDA': 'Un hack and slash cinématographique pour mobile : un mortel dont la famille a été sacrifiée à Râ revient du jugement de la Douat pour traquer et tuer les dieux d’Égypte. Le voyage traverse 11 mythologies, une par chapitre : égyptienne, mésopotamienne, aztèque, maya, inca, celte, slave, finnoise, romaine, nordique et, pour finir, grecque. Le chapitre I, l’Égypte, compte 10 niveaux, chacun avec un dieu pour boss, de Sobek à Râ. Deux khopesh, combos, esquives, parades et coups de grâce au ralenti, 3 pouvoirs par mythologie (pris aux dieux des niveaux 1, 5 et 10 ; les autres dieux les rendent plus forts) et une narration épique avec alliés et boss. Gratuit sur iPhone et Android : le prologue et le premier niveau de l’Égypte sont débloqués ; les niveaux 2 à 10 arrivent bientôt en achat intégré. Sans publicité.',
 'Platforms': 'Plateformes', 'Android (iPhone coming soon)': 'Android (iPhone bientôt)', 'Genre': 'Genre',
 'Action, hack and slash': 'Action, hack and slash', 'Ads': 'Publicité', 'None': 'Aucune',
 'Game page': 'Page du jeu', 'Gameplay video (MP4)': 'Vidéo de gameplay (MP4)',
 'Space shooter · Out now on iPhone and Android': 'Shoot spatial · Disponible sur iPhone et Android',
 'ROTA': 'Un shoot spatial à l’horizontale pour les enfants et toute la famille : fais glisser ton doigt pour voler de la Terre jusqu’à la planète la plus lointaine jamais découverte, à 28 millions d’années-lumière, pendant que le vaisseau tire tout seul. 31 vraies planètes avec de vraies infos scientifiques, 20 créatures de dessin animé, un boss géant sur chaque planète, pluies de météores, ruines extraterrestres et orages électriques, 10 vaisseaux, 6 armes, un narrateur et un mode Facile. Le jeu complet, sans achats intégrés. Disponible sur l’App Store pour iPhone et iPad et sur Google Play.',
 'iPhone, Android': 'iPhone, Android', 'Action, space shooter, family': 'Action, shoot spatial, famille',
 'Arcade volleyball · Out now on iPhone and Android': 'Volley arcade · Disponible sur iPhone et Android',
 'VOLEI': 'Du volley rapide façon arcade, inspiré des classiques des années 90 : 6 contre 6 en salle avec rotations et services sautés, 2 contre 2 sur la plage, un Super Smash au ralenti et en feu, un commentateur ou une commentatrice, un public qui vibre, un tournoi à 8 équipes et 2 joueurs sur le même téléphone. Équipes originales, deux styles visuels et 13 succès. Jeu payant et complet, sans publicité ni achats intégrés. Disponible sur l’App Store pour iPhone et iPad et sur Google Play.',
 'iPhone (Android coming soon)': 'iPhone (Android bientôt)', 'Sports, volleyball, arcade': 'Sport, volley, arcade',
 'Players': 'Joueurs', '1–2, same device': '1–2, sur le même appareil', 'Google Play: coming soon': 'Google Play : bientôt',
 'Penalties and free kicks': 'Penalties et coups francs',
 'GOL': 'Des penalties et coups francs en 3D : glisse du ballon vers la lucarne et frappe, ou mets-toi dans les buts et plonge. Choisis la version enfants, avec des joueurs colorés en blocs, ou la version adulte, avec des joueurs et des supporters réalistes. Sélections et clubs, matchs sous la pluie, la neige et de nuit, un mode Coupe, des vignettes, des défis quotidiens, des commentaires en 14 langues et des parties en ligne avec un ami.',
 'Sports, soccer, family': 'Sport, football, famille', '1–2, local or online': '1–2, en local ou en ligne',
 'Virtual pet · Out now on iPhone and Android': 'Animal virtuel · Disponible sur iPhone et Android',
 'XODO': 'L’animal virtuel porte-clés des années 90 est de retour, avec des animaux brésiliens : un capybara, un tamarin lion doré, un tatou, un ara, un dauphin de rivière et un fourmilier. Fais éclore un œuf, donne un nom à ton animal et occupe-t’en en temps réel, même app fermée. Il ne meurt jamais, idéal pour les enfants. Secoue pour le laver, souffle dans le micro pour le sécher, joue à 3 mini-jeux et remplis un album de 18 formes. Look rétro ou moderne. Jeu payant, sans publicité ni achats intégrés. Disponible sur l’App Store pour iPhone et iPad et sur Google Play.',
 'Simulation, virtual pet, family': 'Simulation, animal virtuel, famille', 'Hide and seek': 'Cache-cache',
 'ESCONDE': 'Un tout nouveau cache-cache pensé pour le téléphone : cache-toi, passe le téléphone et vois si l’autre joueur te trouve, ou défie l’ordinateur, qui apprend tes astuces. 24 lieux de jour comme de nuit, une lampe torche, un radar chaud ou froid, des leurres, la pluie et les éclairs, un narrateur et un mode pour les petits. Parties en ligne avec un code de salon.',
 'Family, casual': 'Famille, casual', '1–4, local or online': '1–4, en local ou en ligne', 'Virtual drinks': 'Boissons virtuelles',
 'GELADA': 'Tu te souviens de l’app qui transformait ton téléphone en verre de bière ? Gelada la fait revivre avec 100 boissons, un mode mélange où l’ordre des ingrédients change le résultat (le lait avec du jus d’orange tourne !), un barman qui parle, la boisson du jour et un mode vidéo pour les blagues. 100 % virtuel, 0 % alcool.',
 'Simulation, casual, humor': 'Simulation, casual, humour', 'Collection catalog': 'Catalogue de collections',
 'Acervo: Your Collection': 'Acervo : Ta Collection',
 'ACERVO': 'Acervo est le catalogue de ta collection, avec la valeur de chaque pièce. Photographie montres, pièces de monnaie, timbres, cartes à collectionner, vinyles ou voitures miniatures : l’app les identifie à partir des photos grâce à l’IA et indique le prix bas, typique et haut sur le marché de l’occasion, dans ta devise. Les collectionneurs peuvent partager une pièce par lien, en choisissant ce qu’elle montre, et trouver des groupes, des forums et d’autres collectionneurs Acervo qui possèdent le même modèle ; les coordonnées ne sont échangées que si les deux acceptent. Fonctionne hors ligne, se synchronise dans le cloud et n’a pas de publicité. Gratuit pour commencer, avec un abonnement Premium facultatif.',
 'Category': 'Catégorie', 'Lifestyle, collecting': 'Style de vie, collection', 'App page': 'Page de l’app',
 'Logos and screenshots': 'Logos et captures d’écran',
 'CLICK': 'Clique sur une image pour la télécharger. Tu peux utiliser ces images et vidéos pour écrire sur nos jeux et nos apps ou les présenter.',
 'Videos': 'Vidéos', 'Short gameplay clips are on our YouTube channel': 'De courts extraits de gameplay sont sur notre chaîne YouTube',
 'and on': 'et sur', '. You can also download the MP4 files from each game above.': '. Tu peux aussi télécharger les fichiers MP4 de chaque jeu ci-dessus.',
 'For press, reviews, YouTube features or promo codes, write to': 'Pour la presse, les tests, les vidéos YouTube ou les codes promo, écris à',
 'Instagram and TikTok:': 'Instagram et TikTok :', '· YouTube:': '· YouTube :',
},
'it': {
 'Contact': 'Contatti', 'Download kit': 'Scarica il kit', 'Press kit': 'Kit stampa',
 'LEAD': 'Arial Gamer è uno studio indipendente di giochi per smartphone dal Brasile. Creiamo giochi brevi e allegri da giocare in famiglia e con gli amici: Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde e Gelada. Tutti i giochi sono senza pubblicità, senza registrazione, non raccolgono dati e sono disponibili in 8 lingue. Nel 2026 abbiamo lanciato anche Acervo, un’app per catalogare e valutare le collezioni. Novità: Deicida, un hack and slash cinematografico contro gli dèi di 11 mitologie (già su Android), e Rota Estelar, uno sparatutto spaziale per tutta la famiglia. Nuovi su iPhone: Vôlei Total, pallavolo arcade, e Xodó, un animaletto virtuale con animali brasiliani.',
 'Studio': 'Studio', 'Based in': 'Sede', 'Brazil': 'Brasile', 'Games': 'Giochi',
 '7, all out now on iPhone and Android': '7, tutti già usciti su iPhone e Android',
 'Apps': 'App', 'Acervo (iPhone and Android)': 'Acervo (iPhone e Android)', 'Languages': 'Lingue',
 'Website': 'Sito web', 'Social': 'Social', 'Download all images (ZIP)': 'Scarica tutte le immagini (ZIP)',
 'Hack and slash · Out now on iPhone and Android': 'Hack and slash · Già su iPhone e Android',
 'DEICIDA': 'Un hack and slash cinematografico per smartphone: un mortale la cui famiglia è stata sacrificata a Ra torna dal giudizio del Duat per dare la caccia agli dèi d’Egitto e ucciderli. Il viaggio attraversa 11 mitologie, una per capitolo: egizia, mesopotamica, azteca, maya, inca, celtica, slava, finlandese, romana, norrena e, per ultima, greca. Il Capitolo I, l’Egitto, ha 10 livelli, ognuno con un dio come boss, da Sobek a Ra. Due khopesh, combo, schivate, parate e colpi finali al rallentatore, 3 poteri per mitologia (strappati agli dèi dei livelli 1, 5 e 10; gli altri dèi li rendono più forti) e una narrazione epica con alleati e boss. Gratis su iPhone e Android: il prologo e il primo livello dell’Egitto sono sbloccati; i livelli da 2 a 10 arriveranno presto come acquisto in-app. Senza pubblicità.',
 'Platforms': 'Piattaforme', 'Android (iPhone coming soon)': 'Android (iPhone in arrivo)', 'Genre': 'Genere',
 'Action, hack and slash': 'Azione, hack and slash', 'Ads': 'Pubblicità', 'None': 'Nessuna',
 'Game page': 'Pagina del gioco', 'Gameplay video (MP4)': 'Video di gioco (MP4)',
 'Space shooter · Out now on iPhone and Android': 'Sparatutto spaziale · Già su iPhone e Android',
 'ROTA': 'Uno sparatutto spaziale in orizzontale per bambini e tutta la famiglia: trascina il dito per volare dalla Terra al pianeta più lontano mai scoperto, a 28 milioni di anni luce, mentre la nave spara da sola. 31 pianeti veri con curiosità scientifiche reali, 20 creature da cartone animato, un boss gigante su ogni pianeta, piogge di meteoriti, rovine aliene e tempeste elettriche, 10 navi, 6 armi, un narratore e una modalità Facile. Il gioco completo, senza acquisti in-app. Già sull’App Store per iPhone e iPad e su Google Play.',
 'iPhone, Android': 'iPhone, Android', 'Action, space shooter, family': 'Azione, sparatutto spaziale, famiglia',
 'Arcade volleyball · Out now on iPhone and Android': 'Pallavolo arcade · Già su iPhone e Android',
 'VOLEI': 'Pallavolo veloce in stile arcade, ispirata ai classici degli anni ’90: 6 contro 6 in palestra con rotazioni e battute in salto, 2 contro 2 in spiaggia, una Super Schiacciata al rallentatore e in fiamme, telecronista uomo o donna, pubblico in festa, un torneo a 8 squadre e 2 giocatori sullo stesso telefono. Squadre originali, due stili grafici e 13 obiettivi. Gioco a pagamento e completo, senza pubblicità né acquisti in-app. Già sull’App Store per iPhone e iPad e su Google Play.',
 'iPhone (Android coming soon)': 'iPhone (Android in arrivo)', 'Sports, volleyball, arcade': 'Sport, pallavolo, arcade',
 'Players': 'Giocatori', '1–2, same device': '1–2, sullo stesso dispositivo', 'Google Play: coming soon': 'Google Play: in arrivo',
 'Penalties and free kicks': 'Rigori e punizioni',
 'GOL': 'Rigori e punizioni in 3D: trascina dal pallone all’incrocio e tira, oppure mettiti in porta e tuffati. Scegli la versione per bambini, con giocatori colorati a blocchi, o quella per adulti, con giocatori e tifosi realistici. Nazionali e club, partite con pioggia, neve e di notte, una modalità Coppa, figurine, sfide giornaliere, telecronaca in 14 lingue e partite online con un amico.',
 'Sports, soccer, family': 'Sport, calcio, famiglia', '1–2, local or online': '1–2, in locale o online',
 'Virtual pet · Out now on iPhone and Android': 'Animaletto virtuale · Già su iPhone e Android',
 'XODO': 'Torna l’animaletto virtuale portachiavi degli anni ’90, con animali brasiliani: un capibara, un tamarino leone dorato, un armadillo, un ara, un delfino di fiume e un formichiere. Fai schiudere un uovo, dai un nome al tuo animaletto e prenditene cura in tempo reale, anche con l’app chiusa. Non muore mai, perfetto per i bambini. Scuoti per lavarlo, soffia nel microfono per asciugarlo, gioca a 3 minigiochi e completa un album con 18 forme. Stile retrò o moderno. Gioco a pagamento, senza pubblicità né acquisti in-app. Già sull’App Store per iPhone e iPad e su Google Play.',
 'Simulation, virtual pet, family': 'Simulazione, animaletto virtuale, famiglia', 'Hide and seek': 'Nascondino',
 'ESCONDE': 'Un nascondino tutto nuovo pensato per il telefono: nasconditi, passa il telefono e vedi se l’altro giocatore ti trova, oppure sfida il computer, che impara i tuoi trucchi. 24 luoghi di giorno e di notte, una torcia, un radar caldo o freddo, esche, pioggia e fulmini, un narratore e una modalità per i più piccoli. Partite online con codice stanza.',
 'Family, casual': 'Famiglia, casual', '1–4, local or online': '1–4, in locale o online', 'Virtual drinks': 'Bevande virtuali',
 'GELADA': 'Ti ricordi l’app che trasformava il telefono in un bicchiere di birra? Gelada la riporta in vita con 100 bevande, una modalità mix in cui l’ordine degli ingredienti cambia il risultato (il latte con il succo d’arancia caglia!), un barista che parla, la bevanda del giorno e una modalità video per gli scherzi. 100% virtuale, 0% alcol.',
 'Simulation, casual, humor': 'Simulazione, casual, umorismo', 'Collection catalog': 'Catalogo di collezioni',
 'Acervo: Your Collection': 'Acervo: La Tua Collezione',
 'ACERVO': 'Acervo è il catalogo della tua collezione, con il valore di ogni pezzo. Fotografa orologi, monete, francobolli, carte collezionabili, vinili o modellini di auto: l’app li riconosce dalle foto con l’IA e mostra il prezzo basso, tipico e alto sul mercato dell’usato, nella tua valuta. I collezionisti possono condividere un pezzo tramite link, scegliendo cosa mostra, e trovare gruppi, forum e altri collezionisti Acervo che hanno lo stesso modello; i contatti vengono scambiati solo se entrambi accettano. Funziona offline, si sincronizza nel cloud e non ha pubblicità. Gratis per iniziare, con abbonamento Premium facoltativo.',
 'Category': 'Categoria', 'Lifestyle, collecting': 'Stile di vita, collezionismo', 'App page': 'Pagina dell’app',
 'Logos and screenshots': 'Loghi e screenshot',
 'CLICK': 'Clicca su un’immagine per scaricarla. Puoi usare queste immagini e questi video per scrivere dei nostri giochi e delle nostre app o per presentarli.',
 'Videos': 'Video', 'Short gameplay clips are on our YouTube channel': 'Brevi clip di gioco sono sul nostro canale YouTube',
 'and on': 'e su', '. You can also download the MP4 files from each game above.': '. Puoi anche scaricare i file MP4 di ogni gioco qui sopra.',
 'For press, reviews, YouTube features or promo codes, write to': 'Per stampa, recensioni, video su YouTube o codici promozionali, scrivi a',
 'Instagram and TikTok:': 'Instagram e TikTok:', '· YouTube:': '· YouTube:',
},
'ja': {
 'Contact': 'お問い合わせ', 'Download kit': 'キットをダウンロード', 'Press kit': 'プレスキット',
 'LEAD': 'Arial Gamer はブラジルのインディーモバイルゲームスタジオです。家族や友だちと一緒に遊べる、短くて楽しいスマホゲームを作っています：Deicida、Rota Estelar、Gol de Placa、Esconde-Esconde、Gelada。すべてのゲームは広告なし、登録不要、データ収集なしで、8か国語に対応しています。2026年にはコレクションを記録して評価するアプリ Acervo もリリースしました。新作：11の神話の神々に挑むシネマティックなハックアンドスラッシュ Deicida（Android で配信中）と、家族みんなで楽しめる宇宙シューティング Rota Estelar。iPhone の新作：アーケードバレーボール Vôlei Total と、ブラジルの動物たちと暮らすバーチャルペット Xodó。',
 'Studio': 'スタジオ', 'Based in': '拠点', 'Brazil': 'ブラジル', 'Games': 'ゲーム',
 '7, all out now on iPhone and Android': '7作品、すべて配信中（iPhone と Android）',
 'Apps': 'アプリ', 'Acervo (iPhone and Android)': 'Acervo（iPhone と Android）', 'Languages': '対応言語',
 'Website': 'ウェブサイト', 'Social': 'SNS', 'Download all images (ZIP)': 'すべての画像をダウンロード（ZIP）',
 'Hack and slash · Out now on iPhone and Android': 'ハックアンドスラッシュ · iPhone と Android で配信中',
 'DEICIDA': 'スマホ向けのシネマティックなハックアンドスラッシュ。家族をラーへの生贄にされた人間が、ドゥアトの審判から戻り、エジプトの神々を狩り、討ち取ります。旅は1章につき1つ、全11の神話をめぐります：エジプト、メソポタミア、アステカ、マヤ、インカ、ケルト、スラヴ、フィンランド、ローマ、北欧、そして最後にギリシャ。第1章エジプトは全10ステージで、各ステージのボスはセベクからラーまでの神々です。2本のケペシュ、コンボ、回避、パリィ、スローモーションのフィニッシュ、神話ごとに3つの力（ステージ1・5・10の神から奪い、ほかの神々を倒すと強くなる）、仲間やボスとの壮大なナレーション。iPhone と Android で無料：プロローグとエジプトの最初のステージをプレイ可能。ステージ2〜10はまもなくアプリ内購入で登場します。広告なし。',
 'Platforms': 'プラットフォーム', 'Android (iPhone coming soon)': 'Android（iPhone 近日公開）', 'Genre': 'ジャンル',
 'Action, hack and slash': 'アクション、ハックアンドスラッシュ', 'Ads': '広告', 'None': 'なし',
 'Game page': 'ゲームページ', 'Gameplay video (MP4)': 'プレイ動画（MP4）',
 'Space shooter · Out now on iPhone and Android': '宇宙シューティング · iPhone と Android で配信中',
 'ROTA': '子どもと家族みんなのための横画面の宇宙シューティング。指でなぞって、地球から2800万光年先、これまでに発見された最も遠い惑星まで飛びます。射撃は自動です。本物の科学知識つきの実在する31の惑星、20体のアニメ風クリーチャー、すべての惑星にいる巨大ボス、流星群、異星の遺跡、雷の嵐、10機の宇宙船、6種類の武器、ナレーター、かんたんモード。アプリ内課金なしの完全版。iPhone・iPad 向け App Store と Google Play で配信中。',
 'iPhone, Android': 'iPhone、Android', 'Action, space shooter, family': 'アクション、宇宙シューティング、ファミリー',
 'Arcade volleyball · Out now on iPhone and Android': 'アーケードバレーボール · iPhone と Android で配信中',
 'VOLEI': '90年代の名作に着想を得た、スピーディーなアーケード風バレーボール。ローテーションとジャンプサーブのある6人制インドア、2人制ビーチ、スローモーションで燃えるスーパースパイク、男性または女性の実況、沸き立つ観客、8チームのトーナメント、1台のスマホで2人プレイ。オリジナルチーム、2つのビジュアルスタイル、13の実績。買い切りの完全版で、広告もアプリ内課金もありません。iPhone・iPad 向け App Store と Google Play で配信中。',
 'iPhone (Android coming soon)': 'iPhone（Android 近日公開）', 'Sports, volleyball, arcade': 'スポーツ、バレーボール、アーケード',
 'Players': 'プレイ人数', '1–2, same device': '1〜2人、同じ端末で', 'Google Play: coming soon': 'Google Play：近日公開',
 'Penalties and free kicks': 'PKとフリーキック',
 'GOL': '3DのPKとフリーキック。ボールからゴールの隅へなぞってシュート、またはゴールに立ってダイブ。カラフルなブロックの選手が登場するキッズ版と、リアルな選手と観客のおとな版を選べます。代表チームとクラブ、雨・雪・ナイトゲーム、カップモード、ステッカー、デイリーチャレンジ、14か国語の実況、友だちとのオンライン対戦。',
 'Sports, soccer, family': 'スポーツ、サッカー、ファミリー', '1–2, local or online': '1〜2人、ローカルまたはオンライン',
 'Virtual pet · Out now on iPhone and Android': 'バーチャルペット · iPhone と Android で配信中',
 'XODO': '90年代のキーホルダー型バーチャルペットが、ブラジルの動物たちと一緒に帰ってきました：カピバラ、ゴールデンライオンタマリン、アルマジロ、コンゴウインコ、アマゾンカワイルカ、アリクイ。卵をかえして名前をつけ、アプリを閉じていてもリアルタイムでお世話します。死なないので子どもにもぴったり。振ってお風呂、マイクに息を吹きかけて乾かし、3つのミニゲームで遊び、18種類の姿が載るアルバムを集めましょう。レトロまたはモダンな見た目。買い切りで、広告もアプリ内課金もありません。iPhone・iPad 向け App Store と Google Play で配信中。',
 'Simulation, virtual pet, family': 'シミュレーション、バーチャルペット、ファミリー', 'Hide and seek': 'かくれんぼ',
 'ESCONDE': 'スマホのために作られた新しいかくれんぼ。隠れてスマホを渡し、相手に見つかるか試したり、あなたの作戦を学習するコンピューターに挑戦したり。昼と夜の24の場所、懐中電灯、温度で知らせるレーダー、おとり、雨と稲妻、ナレーター、小さな子ども向けモード。ルームコードでオンライン対戦。',
 'Family, casual': 'ファミリー、カジュアル', '1–4, local or online': '1〜4人、ローカルまたはオンライン', 'Virtual drinks': 'バーチャルドリンク',
 'GELADA': 'スマホをビールのグラスに変えるアプリを覚えていますか？ Gelada が100種類のドリンクとともに復活。材料を入れる順番で結果が変わるミックスモード（牛乳とオレンジジュースは分離します！）、話すバーテンダー、今日のドリンク、いたずら動画モードも。100%バーチャル、アルコール0%。',
 'Simulation, casual, humor': 'シミュレーション、カジュアル、ユーモア', 'Collection catalog': 'コレクション管理',
 'Acervo: Your Collection': 'Acervo：あなたのコレクション',
 'ACERVO': 'Acervo は、アイテムごとの価値がわかるコレクションのカタログです。腕時計、硬貨、切手、トレーディングカード、レコード、ミニカーを撮影すると、AI が写真から識別し、中古市場での安値・相場・高値をあなたの通貨で表示します。表示内容を選んでアイテムをリンクで共有したり、同じモデルを持つグループ、フォーラム、ほかの Acervo コレクターを見つけたりできます。連絡先は双方が承諾した場合にのみ交換されます。オフラインで動作し、クラウドに同期し、広告はありません。無料で始められ、Premium サブスクリプションは任意です。',
 'Category': 'カテゴリ', 'Lifestyle, collecting': 'ライフスタイル、コレクション', 'App page': 'アプリページ',
 'Logos and screenshots': 'ロゴとスクリーンショット',
 'CLICK': '画像をクリックするとダウンロードできます。これらの画像や動画は、私たちのゲームやアプリの記事・紹介に自由にお使いください。',
 'Videos': '動画', 'Short gameplay clips are on our YouTube channel': '短いプレイ動画は YouTube チャンネル',
 'and on': 'と', '. You can also download the MP4 files from each game above.': 'で公開しています。上の各ゲームから MP4 ファイルもダウンロードできます。',
 'For press, reviews, YouTube features or promo codes, write to': '取材、レビュー、YouTube での紹介、プロモコードのご依頼はこちらへ：',
 'Instagram and TikTok:': 'Instagram と TikTok：', '· YouTube:': '· YouTube：',
},
'zh': {
 'Contact': '联系我们', 'Download kit': '下载资料包', 'Press kit': '媒体资料包',
 'LEAD': 'Arial Gamer 是一家来自巴西的独立手机游戏工作室。我们制作简短、欢乐、适合家人和朋友一起玩的手机游戏：Deicida、Rota Estelar、Gol de Placa、Esconde-Esconde 和 Gelada。所有游戏都没有广告，无需注册，不收集任何数据，并支持 8 种语言。2026 年我们还推出了 Acervo，一款用来整理和估价收藏品的应用。新作：Deicida，一款对抗 11 个神话众神的电影级砍杀动作游戏（已在 Android 上线），以及适合全家的太空射击游戏 Rota Estelar。iPhone 新作：街机排球 Vôlei Total，以及与巴西动物相伴的电子宠物 Xodó。',
 'Studio': '工作室', 'Based in': '所在地', 'Brazil': '巴西', 'Games': '游戏',
 '7, all out now on iPhone and Android': '7 款，均已上线（iPhone 和 Android）',
 'Apps': '应用', 'Acervo (iPhone and Android)': 'Acervo（iPhone 和 Android）', 'Languages': '语言',
 'Website': '网站', 'Social': '社交媒体', 'Download all images (ZIP)': '下载全部图片（ZIP）',
 'Hack and slash · Out now on iPhone and Android': '砍杀动作 · 已在 iPhone 和 Android 上线',
 'DEICIDA': '一款手机上的电影级砍杀动作游戏：一个家人被献祭给拉神的凡人，从杜亚特的审判中归来，追杀埃及众神。旅程跨越 11 个神话，每章一个：埃及、美索不达米亚、阿兹特克、玛雅、印加、凯尔特、斯拉夫、芬兰、罗马、北欧，最后是希腊。第一章埃及共 10 关，每关的首领都是一位神，从索贝克到拉。双持赫帕什弯刀、连招、闪避、格挡和慢动作终结技，每个神话 3 种能力（夺自第 1、5、10 关的神；击败其他神会让它们更强），以及与盟友和首领的史诗级旁白。iPhone 和 Android 免费：序章和埃及第一关已解锁；第 2 至 10 关即将以应用内购买形式推出。没有广告。',
 'Platforms': '平台', 'Android (iPhone coming soon)': 'Android（iPhone 即将推出）', 'Genre': '类型',
 'Action, hack and slash': '动作、砍杀', 'Ads': '广告', 'None': '无',
 'Game page': '游戏页面', 'Gameplay video (MP4)': '游戏视频（MP4）',
 'Space shooter · Out now on iPhone and Android': '太空射击 · 已在 iPhone 和 Android 上线',
 'ROTA': '一款适合孩子和全家的横屏太空射击游戏：用手指滑动，从地球飞向迄今发现的最遥远的行星，远在 2800 万光年之外，飞船会自动开火。31 颗真实行星和真实的科学知识，20 种卡通生物，每颗行星都有巨型首领，还有流星雨、外星遗迹和雷暴，10 艘飞船、6 种武器、旁白和简单模式。完整版游戏，没有应用内购买。已在 App Store（iPhone 和 iPad）及 Google Play 上线。',
 'iPhone, Android': 'iPhone、Android', 'Action, space shooter, family': '动作、太空射击、家庭',
 'Arcade volleyball · Out now on iPhone and Android': '街机排球 · 已在 iPhone 和 Android 上线',
 'VOLEI': '快节奏的街机风格排球，灵感来自 90 年代经典：6 对 6 室内排球，含轮转和跳发球；2 对 2 沙滩排球；慢动作燃烧的超级扣杀；男声或女声解说、欢呼的观众、8 队锦标赛，以及同一部手机上的双人对战。原创球队、两种画面风格和 13 项成就。付费完整版，没有广告，也没有应用内购买。已在 App Store（iPhone 和 iPad）及 Google Play 上线。',
 'iPhone (Android coming soon)': 'iPhone（Android 即将推出）', 'Sports, volleyball, arcade': '体育、排球、街机',
 'Players': '玩家人数', '1–2, same device': '1–2 人，同一设备', 'Google Play: coming soon': 'Google Play：即将推出',
 'Penalties and free kicks': '点球和任意球',
 'GOL': '3D 点球和任意球：从球滑向球门死角射门，或者站在门前扑救。可选择彩色积木球员的儿童版，或真实球员和球迷的成人版。国家队和俱乐部，雨天、雪天和夜间比赛，杯赛模式、贴纸、每日挑战、14 种语言的解说，还能和朋友在线对战。',
 'Sports, soccer, family': '体育、足球、家庭', '1–2, local or online': '1–2 人，本地或在线',
 'Virtual pet · Out now on iPhone and Android': '电子宠物 · 已在 iPhone 和 Android 上线',
 'XODO': '90 年代的钥匙扣电子宠物回来了，还带来了巴西动物：水豚、金狮面狨、犰狳、金刚鹦鹉、亚马逊河豚和食蚁兽。孵化一颗蛋，给宠物起名，并实时照顾它，即使关闭应用也一样。它永远不会死，非常适合孩子。摇一摇给它洗澡，对着麦克风吹气把它吹干，玩 3 个小游戏，集满 18 种形态的图鉴。复古或现代风格。付费游戏，没有广告，也没有应用内购买。已在 App Store（iPhone 和 iPad）及 Google Play 上线。',
 'Simulation, virtual pet, family': '模拟、电子宠物、家庭', 'Hide and seek': '捉迷藏',
 'ESCONDE': '一款专为手机打造的全新捉迷藏游戏：藏好后把手机交给对方，看他能不能找到你，或者挑战会学习你套路的电脑。白天和夜晚共 24 个地点，手电筒、冷热雷达、诱饵、雨和闪电、旁白，还有适合小朋友的模式。可用房间码在线对战。',
 'Family, casual': '家庭、休闲', '1–4, local or online': '1–4 人，本地或在线', 'Virtual drinks': '虚拟饮品',
 'GELADA': '还记得那个把手机变成一杯啤酒的应用吗？Gelada 让它回归了：100 种饮品；混合模式中配料的顺序会改变结果（牛奶加橙汁会结块！）；会说话的调酒师、每日饮品，以及恶作剧视频模式。100% 虚拟，0% 酒精。',
 'Simulation, casual, humor': '模拟、休闲、幽默', 'Collection catalog': '收藏目录',
 'Acervo: Your Collection': 'Acervo：你的收藏',
 'ACERVO': 'Acervo 是你的收藏目录，能显示每件藏品的价值。拍下手表、硬币、邮票、集换式卡牌、黑胶唱片或合金车模，应用会用 AI 根据照片识别它们，并以你的货币显示二手市场的低价、常见价和高价。收藏者可以通过链接分享单件藏品并选择显示的内容，还能找到拥有相同型号的群组、论坛和其他 Acervo 收藏者；只有双方都同意时才会交换联系方式。支持离线使用、云端同步，没有广告。可免费开始使用，Premium 订阅为可选。',
 'Category': '类别', 'Lifestyle, collecting': '生活方式、收藏', 'App page': '应用页面',
 'Logos and screenshots': '标志和截图',
 'CLICK': '点击任意图片即可下载。你可以使用这些图片和视频来报道或介绍我们的游戏和应用。',
 'Videos': '视频', 'Short gameplay clips are on our YouTube channel': '简短的游戏片段发布在我们的 YouTube 频道',
 'and on': '和', '. You can also download the MP4 files from each game above.': '上。你也可以在上方每款游戏处下载 MP4 文件。',
 'For press, reviews, YouTube features or promo codes, write to': '媒体报道、评测、YouTube 介绍或兑换码，请写信至',
 'Instagram and TikTok:': 'Instagram 和 TikTok：', '· YouTube:': '· YouTube：',
},
}

# Chaves curtas usadas acima para os parágrafos longos (as mesmas do PT, em inglês).
LONG = {}
for k in T['pt']:
    for tag, start in [('LEAD', 'Arial Gamer is an independent'), ('DEICIDA', 'A cinematic hack and slash'),
                       ('ROTA', 'A landscape space shooter'), ('VOLEI', 'Fast, arcade-style'),
                       ('GOL', 'A 3D penalty'), ('XODO', 'The 90s keychain'), ('ESCONDE', 'A brand-new hide'),
                       ('GELADA', 'Remember the app'), ('ACERVO', 'Acervo is the catalog'), ('CLICK', 'Click any image')]:
        if k.startswith(start):
            LONG[tag] = k
for l in T:
    for tag, en in LONG.items():
        if tag in T[l]:
            T[l][en] = T[l].pop(tag)

# Legendas das imagens: "Jogo: descrição"
CAP = {
 'pouring and drinking a beer': {'pt': 'enchendo e bebendo uma cerveja', 'es': 'sirviendo y bebiendo una cerveza', 'de': 'Bier einschenken und trinken', 'fr': 'verser et boire une bière', 'it': 'versare e bere una birra', 'ja': 'ビールを注いで飲む', 'zh': '倒啤酒和喝啤酒'},
 'mix score, milk with orange juice curdled': {'pt': 'nota da mistura, leite com laranja talhou', 'es': 'nota de la mezcla, la leche con zumo de naranja se cortó', 'de': 'Mix-Wertung, Milch mit Orangensaft ist geronnen', 'fr': 'note du mélange, le lait au jus d’orange a tourné', 'it': 'voto del mix, il latte con il succo d’arancia ha cagliato', 'ja': 'ミックスの採点、牛乳とオレンジジュースが分離', 'zh': '混合评分，牛奶加橙汁结块了'},
 'bar counter': {'pt': 'balcão do bar', 'es': 'barra del bar', 'de': 'Bartheke', 'fr': 'comptoir du bar', 'it': 'bancone del bar', 'ja': 'バーカウンター', 'zh': '吧台'},
 'hiding on the moon': {'pt': 'escondido na Lua', 'es': 'escondido en la Luna', 'de': 'Verstecken auf dem Mond', 'fr': 'caché sur la Lune', 'it': 'nascosto sulla Luna', 'ja': '月でかくれんぼ', 'zh': '躲在月球上'},
 'playing against the computer': {'pt': 'jogando contra a máquina', 'es': 'jugando contra la máquina', 'de': 'gegen den Computer spielen', 'fr': 'contre l’ordinateur', 'it': 'contro il computer', 'ja': 'コンピューターと対戦', 'zh': '对战电脑'},
 'pirate ship': {'pt': 'navio pirata', 'es': 'barco pirata', 'de': 'Piratenschiff', 'fr': 'bateau pirate', 'it': 'nave pirata', 'ja': '海賊船', 'zh': '海盗船'},
 'grown-up version with realistic players': {'pt': 'versão adulta com jogadores realistas', 'es': 'versión adulta con jugadores realistas', 'de': 'Erwachsenenversion mit realistischen Spielern', 'fr': 'version adulte avec des joueurs réalistes', 'it': 'versione per adulti con giocatori realistici', 'ja': 'リアルな選手のおとな版', 'zh': '真实球员的成人版'},
 'kids version, goal at night': {'pt': 'versão infantil, gol à noite', 'es': 'versión infantil, gol de noche', 'de': 'Kinderversion, Tor bei Nacht', 'fr': 'version enfants, but de nuit', 'it': 'versione per bambini, gol di notte', 'ja': 'キッズ版、ナイトゲームのゴール', 'zh': '儿童版，夜间进球'},
 'free kick in the snow': {'pt': 'falta na neve', 'es': 'falta en la nieve', 'de': 'Freistoß im Schnee', 'fr': 'coup franc sous la neige', 'it': 'punizione sotto la neve', 'ja': '雪の中のフリーキック', 'zh': '雪中任意球'},
 'build your player': {'pt': 'monte o seu jogador', 'es': 'crea a tu jugador', 'de': 'erstelle deinen Spieler', 'fr': 'crée ton joueur', 'it': 'crea il tuo giocatore', 'ja': '自分の選手を作ろう', 'zh': '打造你的球员'},
 'the hero with twin khopesh in the desert': {'pt': 'o herói com duas khopesh no deserto', 'es': 'el héroe con dos khopesh en el desierto', 'de': 'der Held mit zwei Khopesch in der Wüste', 'fr': 'le héros et ses deux khopesh dans le désert', 'it': 'l’eroe con due khopesh nel deserto', 'ja': '砂漠に立つ二刀のケペシュの主人公', 'zh': '沙漠中手持双赫帕什的英雄'},
 'villagers on the barque, on the Nile at dawn': {'pt': 'aldeões na barca, no Nilo ao amanhecer', 'es': 'aldeanos en la barca, en el Nilo al amanecer', 'de': 'Dorfbewohner auf der Barke, auf dem Nil im Morgengrauen', 'fr': 'villageois sur la barque, sur le Nil à l’aube', 'it': 'abitanti sulla barca, sul Nilo all’alba', 'ja': '夜明けのナイル川、舟に乗る村人たち', 'zh': '黎明时尼罗河上船里的村民'},
 "Anubis weighs the hero's heart in the Duat": {'pt': 'Anúbis pesa o coração do herói no Duat', 'es': 'Anubis pesa el corazón del héroe en la Duat', 'de': 'Anubis wiegt das Herz des Helden in der Duat', 'fr': 'Anubis pèse le cœur du héros dans la Douat', 'it': 'Anubi pesa il cuore dell’eroe nel Duat', 'ja': 'ドゥアトで主人公の心臓を量るアヌビス', 'zh': '阿努比斯在杜亚特称量英雄的心脏'},
 'level 1, a market courtyard on the banks of the Nile': {'pt': 'fase 1, um pátio de mercado às margens do Nilo', 'es': 'fase 1, un patio de mercado a orillas del Nilo', 'de': 'Level 1, ein Markthof am Ufer des Nils', 'fr': 'niveau 1, une cour de marché au bord du Nil', 'it': 'livello 1, un cortile di mercato sulle rive del Nilo', 'ja': 'ステージ1、ナイル河畔の市場の中庭', 'zh': '第 1 关，尼罗河畔的集市庭院'},
 'Sobek, the crocodile god, with his mummies': {'pt': 'Sobek, o deus crocodilo, com suas múmias', 'es': 'Sobek, el dios cocodrilo, con sus momias', 'de': 'Sobek, der Krokodilgott, mit seinen Mumien', 'fr': 'Sobek, le dieu crocodile, et ses momies', 'it': 'Sobek, il dio coccodrillo, con le sue mummie', 'ja': 'ワニの神セベクとミイラたち', 'zh': '鳄鱼神索贝克和他的木乃伊'},
 'giant boss at Jupiter': {'pt': 'chefe gigante em Júpiter', 'es': 'jefe gigante en Júpiter', 'de': 'Riesenboss am Jupiter', 'fr': 'boss géant sur Jupiter', 'it': 'boss gigante su Giove', 'ja': '木星の巨大ボス', 'zh': '木星上的巨型首领'},
 'exploration route through real planets': {'pt': 'rota de exploração por planetas de verdade', 'es': 'ruta de exploración por planetas reales', 'de': 'Erkundungsroute durch echte Planeten', 'fr': 'route d’exploration à travers de vraies planètes', 'it': 'rotta di esplorazione tra pianeti veri', 'ja': '実在する惑星をめぐる探査ルート', 'zh': '穿越真实行星的探索航线'},
 'giant Guardian': {'pt': 'Guardião gigante', 'es': 'Guardián gigante', 'de': 'riesiger Wächter', 'fr': 'Gardien géant', 'it': 'Guardiano gigante', 'ja': '巨大なガーディアン', 'zh': '巨型守护者'},
 'hangar with 10 ships': {'pt': 'hangar com 10 naves', 'es': 'hangar con 10 naves', 'de': 'Hangar mit 10 Schiffen', 'fr': 'hangar avec 10 vaisseaux', 'it': 'hangar con 10 navi', 'ja': '10機の宇宙船が並ぶ格納庫', 'zh': '停放 10 艘飞船的机库'},
 '6v6 indoor match': {'pt': 'partida 6x6 na quadra', 'es': 'partido 6 contra 6 en pista', 'de': '6 gegen 6 in der Halle', 'fr': 'match 6 contre 6 en salle', 'it': 'partita 6 contro 6 in palestra', 'ja': '6人制インドアの試合', 'zh': '6 对 6 室内比赛'},
 '2v2 beach volleyball': {'pt': 'vôlei de praia 2x2', 'es': 'vóley playa 2 contra 2', 'de': 'Beachvolleyball 2 gegen 2', 'fr': 'beach-volley 2 contre 2', 'it': 'beach volley 2 contro 2', 'ja': '2人制ビーチバレー', 'zh': '2 对 2 沙滩排球'},
 'the retro 90s egg with a green LCD screen': {'pt': 'o ovo retrô dos anos 90 com tela LCD verde', 'es': 'el huevo retro de los 90 con pantalla LCD verde', 'de': 'das Retro-Ei der 90er mit grünem LCD-Bildschirm', 'fr': 'l’œuf rétro des années 90 avec écran LCD vert', 'it': 'l’uovo retrò anni ’90 con schermo LCD verde', 'ja': '緑の液晶画面のレトロな90年代のたまご', 'zh': '带绿色液晶屏的 90 年代复古蛋'},
 'modern look, a newborn capybara': {'pt': 'visual moderno, uma capivara recém-nascida', 'es': 'estilo moderno, un carpincho recién nacido', 'de': 'moderner Look, ein neugeborenes Wasserschwein', 'fr': 'look moderne, un bébé capybara', 'it': 'stile moderno, un capibara appena nato', 'ja': 'モダンな見た目、生まれたてのカピバラ', 'zh': '现代风格，刚出生的水豚'},
 'album with 18 animal forms': {'pt': 'álbum com 18 formas dos bichos', 'es': 'álbum con 18 formas de animales', 'de': 'Album mit 18 Tierformen', 'fr': 'album avec 18 formes d’animaux', 'it': 'album con 18 forme di animali', 'ja': '18種類の姿が載るアルバム', 'zh': '收录 18 种动物形态的图鉴'},
 'a watch collection with its estimated total value': {'pt': 'uma coleção de relógios com o valor total estimado', 'es': 'una colección de relojes con su valor total estimado', 'de': 'eine Uhrensammlung mit geschätztem Gesamtwert', 'fr': 'une collection de montres et sa valeur totale estimée', 'it': 'una collezione di orologi con il valore totale stimato', 'ja': '推定総額つきの腕時計コレクション', 'zh': '附估计总价值的手表收藏'},
 'an item with its low, typical and high market price': {'pt': 'um item com o preço baixo, típico e alto no mercado', 'es': 'una pieza con su precio bajo, típico y alto en el mercado', 'de': 'ein Stück mit niedrigem, typischem und hohem Marktpreis', 'fr': 'une pièce avec son prix bas, typique et haut sur le marché', 'it': 'un pezzo con il prezzo basso, tipico e alto sul mercato', 'ja': '市場の安値・相場・高値がわかるアイテム', 'zh': '显示市场低价、常见价和高价的藏品'},
 'identification from photos fills in name, model and year': {'pt': 'a identificação pelas fotos preenche nome, modelo e ano', 'es': 'la identificación por fotos rellena nombre, modelo y año', 'de': 'die Erkennung per Foto füllt Name, Modell und Jahr aus', 'fr': 'l’identification par photo remplit nom, modèle et année', 'it': 'il riconoscimento dalle foto compila nome, modello e anno', 'ja': '写真から識別して名前・モデル・年を自動入力', 'zh': '通过照片识别，自动填写名称、型号和年份'},
 'collection report with total value and appreciation': {'pt': 'relatório da coleção com valor total e valorização', 'es': 'informe de la colección con valor total y revalorización', 'de': 'Sammlungsbericht mit Gesamtwert und Wertsteigerung', 'fr': 'rapport de collection avec valeur totale et plus-value', 'it': 'report della collezione con valore totale e rivalutazione', 'ja': '総額と値上がりがわかるコレクションレポート', 'zh': '含总价值和增值的收藏报告'},
}
ICON = {'pt': 'Ícone do {}', 'es': 'Icono de {}', 'de': '{} App-Icon', 'fr': 'Icône de {}', 'it': 'Icona di {}', 'ja': '{}のアイコン', 'zh': '{} 图标'}
LOGO = {'pt': ('Logo da Arial Gamer', 'Banner da Arial Gamer (2048×1152)'), 'es': ('Logo de Arial Gamer', 'Banner de Arial Gamer (2048×1152)'),
        'de': ('Arial-Gamer-Logo', 'Arial-Gamer-Banner (2048×1152)'), 'fr': ('Logo d’Arial Gamer', 'Bannière d’Arial Gamer (2048×1152)'),
        'it': ('Logo di Arial Gamer', 'Banner di Arial Gamer (2048×1152)'), 'ja': ('Arial Gamer のロゴ', 'Arial Gamer のバナー（2048×1152）'),
        'zh': ('Arial Gamer 标志', 'Arial Gamer 横幅（2048×1152）')}
HEAD = {
 'pt': ('Kit de imprensa · Arial Gamer, jogos para celular feitos no Brasil', 'Kit de imprensa da Arial Gamer, estúdio indie de jogos e apps para celular do Brasil (Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde, Gelada, Vôlei Total, Xodó e o app Acervo): informações, logos, ícones, telas, vídeos e contato.', 'Kit de imprensa da Arial Gamer'),
 'es': ('Kit de prensa · Arial Gamer, juegos para móviles hechos en Brasil', 'Kit de prensa de Arial Gamer, estudio indie de juegos y apps para móviles de Brasil (Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde, Gelada, Vôlei Total, Xodó y la app Acervo): datos, logos, iconos, capturas, vídeos y contacto.', 'Kit de prensa de Arial Gamer'),
 'de': ('Pressekit · Arial Gamer, Handyspiele aus Brasilien', 'Pressekit von Arial Gamer, einem Indie-Studio für Handyspiele und Apps aus Brasilien (Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde, Gelada, Vôlei Total, Xodó und die App Acervo): Fakten, Logos, Icons, Screenshots, Videos und Kontakt.', 'Arial Gamer Pressekit'),
 'fr': ('Kit presse · Arial Gamer, jeux mobiles faits au Brésil', 'Kit presse d’Arial Gamer, studio indépendant de jeux et d’apps mobiles du Brésil (Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde, Gelada, Vôlei Total, Xodó et l’app Acervo) : infos, logos, icônes, captures, vidéos et contact.', 'Kit presse Arial Gamer'),
 'it': ('Kit stampa · Arial Gamer, giochi per smartphone made in Brasile', 'Kit stampa di Arial Gamer, studio indie brasiliano di giochi e app per smartphone (Deicida, Rota Estelar, Gol de Placa, Esconde-Esconde, Gelada, Vôlei Total, Xodó e l’app Acervo): dati, loghi, icone, screenshot, video e contatti.', 'Kit stampa Arial Gamer'),
 'ja': ('プレスキット · Arial Gamer、ブラジル発のスマホゲーム', 'ブラジルのインディーモバイルゲーム・アプリスタジオ Arial Gamer のプレスキット（Deicida、Rota Estelar、Gol de Placa、Esconde-Esconde、Gelada、Vôlei Total、Xodó、アプリ Acervo）：概要、ロゴ、アイコン、スクリーンショット、動画、連絡先。', 'Arial Gamer プレスキット'),
 'zh': ('媒体资料包 · Arial Gamer，巴西制作的手机游戏', 'Arial Gamer 媒体资料包。Arial Gamer 是来自巴西的独立手机游戏与应用工作室（Deicida、Rota Estelar、Gol de Placa、Esconde-Esconde、Gelada、Vôlei Total、Xodó 和应用 Acervo）：资料、标志、图标、截图、视频和联系方式。', 'Arial Gamer 媒体资料包'),
}
GAMES = ['Deicida', 'Rota Estelar', 'Vôlei Total', 'Gol de Placa', 'Xodó', 'Esconde-Esconde', 'Gelada', 'Acervo']

LANGBAR_CSS = '.pk-langs { display: flex; flex-wrap: wrap; gap: 6px 14px; margin: 0 0 18px; font-size: 14px } .pk-langs a { color: var(--muted); text-decoration: none } .pk-langs a:hover { color: var(--ink) } .pk-langs a[aria-current] { color: var(--ink); font-weight: 700 }'


def hreflangs():
    out = ['<!-- idiomas-kit -->']
    for l in LANGS:
        out.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (HTML_LANG[l], SITE, URL[l]))
    out.append('<link rel="alternate" hreflang="x-default" href="%s/press/">' % SITE)
    out.append('<!-- /idiomas-kit -->')
    return '\n'.join(out)


def langbar(cur):
    links = []
    for l in LANGS:
        cur_attr = ' aria-current="page"' if l == cur else ''
        links.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (URL[l], HTML_LANG[l], HTML_LANG[l], cur_attr, LABEL[l]))
    return '<!-- langbar --><nav class="pk-langs" aria-label="%s">%s</nav><!-- /langbar -->' % (LANGS_ARIA[cur], ''.join(links))


def prepare_source(s):
    """Coloca hreflang, barra de idiomas e CSS na fonte em inglês (idempotente)."""
    s = re.sub(r'\n?<!-- idiomas-kit -->.*?<!-- /idiomas-kit -->', '', s, flags=re.S)
    s = s.replace('<link rel="canonical" href="https://arialgamer.com.br/press/">',
                  '<link rel="canonical" href="https://arialgamer.com.br/press/">\n' + hreflangs(), 1)
    s = re.sub(r'<!-- langbar -->.*?<!-- /langbar -->', '', s, flags=re.S)
    s = re.sub(r'(<main class="pk">\s*<div class="wrap">)(\s*)', lambda m: m.group(1) + m.group(2) + langbar('en') + m.group(2), s, count=1)
    if '.pk-langs' not in s:
        s = s.replace('</style>', LANGBAR_CSS + '\n</style>', 1)
    return s


def translate(src, l):
    s = src
    tr = T[l]
    head, body = s.split('</head>', 1)
    # cabeçalho
    title, desc, ogt = HEAD[l]
    head = head.replace('<html lang="en">', '<html lang="%s">' % HTML_LANG[l])
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, head)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % ogt, head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % desc, head)
    head = head.replace('<link rel="canonical" href="https://arialgamer.com.br/press/">',
                        '<link rel="canonical" href="%s%s">' % (SITE, URL[l]))
    # corpo: textos entre tags (longos primeiro)
    for en in sorted(tr, key=len, reverse=True):
        body = re.sub(r'>(\s*)' + re.escape(en) + r'(\s*)<', lambda m: '>' + m.group(1) + tr[en] + m.group(2) + '<', body)
    # legendas e alt das imagens
    def cap(text):
        if text == 'Arial Gamer logo': return LOGO[l][0]
        if text == 'Arial Gamer banner (2048×1152)': return LOGO[l][1]
        for g in GAMES:
            if text in (g + ' app icon', g + ' icon'): return ICON[l].format(g)
            if text.startswith(g + ': '):
                d = text[len(g) + 2:]
                if d in CAP: return g + ': ' + CAP[d][l]
                if d in tr: return g + ': ' + tr[d]
        return text
    body = re.sub(r'alt="([^"]*)"', lambda m: 'alt="%s"' % cap(m.group(1)), body)
    body = re.sub(r'<span>([^<]*)</span></a>', lambda m: '<span>%s</span></a>' % cap(m.group(1)), body)
    # links
    body = body.replace('href="/en/"', 'href="%s"' % HOME[l])
    body = re.sub(r'href="/en/([^"]*)"', lambda m: 'href="%s%s"' % (HOME[l], m.group(1)), body)
    body = body.replace('href="arialgamer-presskit.zip"', 'href="/press/arialgamer-presskit.zip"')
    body = body.replace('src="img/', 'src="/press/img/').replace('href="img/', 'href="/press/img/')
    body = re.sub(r'(play\.google\.com/store/apps/details\?id=[\w.]+)(?:&(?:amp;)?hl=en)?', lambda m: m.group(1) + '&amp;hl=' + PLAY_HL[l], body)
    body = re.sub(r'<!-- langbar -->.*?<!-- /langbar -->', langbar(l), body, flags=re.S)
    return head + '</head>' + body


def main():
    src = io.open(SRC, encoding='utf-8', newline='').read()
    src = prepare_source(src)
    io.open(SRC, 'w', encoding='utf-8', newline='').write(src)
    for l in LANGS:
        if l == 'en':
            continue
        out = translate(src, l)
        path = os.path.join(R, URL[l].strip('/').replace('/', os.sep), 'index.html')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
        print('ok', URL[l])


if __name__ == '__main__':
    main()
