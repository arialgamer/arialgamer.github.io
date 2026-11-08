# Arial Gamer

Página "link da bio" do TikTok [@arial.gamer](https://www.tiktok.com/@arial.gamer), com os jogos
Gelada, Esconde-Esconde e Gol de Placa: https://arialgamer.com.br (o endereço arialgamer.github.io redireciona para lá)

A fonte também fica no repositório dos apps (`renatoarial-source/Arial`), em `store/bio-site/`.

Sempre que um jogo mudar (versão aprovada, preço, novidade, Android), atualize esta página e a cópia em `store/bio-site/`.

## Fotos e vídeos

Ficam em `media/`. Os vídeos são verticais (540×960, H.264), com capa `.jpg` de mesmo nome; a página troca de vídeo pelo atributo `data-src` dos botões `.clip`.

- Gelada e Esconde-Esconde: cortados dos vídeos do kit do TikTok, sem a tela final.
- Gol de Placa: gravados do próprio jogo rodando no navegador.
- `media/lugares/`: foto de cada lugar do Esconde-Esconde, de dia e de noite.

## Sem anúncios, Apoie e Comentários

- "Sem anúncios" aparece no topo, nos números e ao lado do preço de cada jogo (em português; nos outros idiomas o selo de preço já diz isso).
- **Apoie o Arial Gamer** (`#apoie`): chave Pix arial83gamer@gmail.com com botão "Copiar chave".
- **Comentários e sugestões** (`#contato`): formulário enviado pelo [FormSubmit](https://formsubmit.co) (grátis, sem servidor) para renato@arialgamer.com.br, que o ImprovMX encaminha para o Gmail. Tem campo escondido contra robôs (`_honey`). Na primeira mensagem enviada do site publicado, o FormSubmit manda um e-mail "Activate Form": é só clicar uma vez.
- As duas áreas também aparecem nas páginas dos jogos (vêm do `index.html` pelo `gerar.py`). Os textos traduzidos ficam no fim da lista `T` de `idiomas.py` e das listas de `idiomas_mais.py`: se mudar uma frase em português, mude a chave lá também e rode os scripts de novo.
