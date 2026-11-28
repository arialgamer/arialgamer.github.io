/* Fotos embaixo de cada jogo viram vídeo: clicar (ou tocar) numa foto abre uma janela com o vídeo daquela cena.
   O vídeo só carrega no clique e começa sem som (dá para ligar nos controles). Fecha no X, clicando fora ou com Esc.
   Foto sem vídeo na lista continua como está. */
(() => {
  // foto (nome do arquivo, sem .jpg) → vídeo (em /media, sem .mp4)
  const VIDEO = {
    'deicida-foto-heroi': 'deicida-chamada', 'deicida-foto-anubis': 'deicida-julgamento', 'deicida-foto-mercado': 'deicida-mumias',
    'deicida-foto-sobek': 'deicida-sobek', 'deicida-foto-jardim': 'deicida-mumias', 'deicida-foto-templo': 'deicida-barca',
    'golaco-quadra': 'fotos/golaco-quadra', 'golaco-areia': 'fotos/golaco-areia', 'golaco-craque': 'fotos/golaco-craque', 'golaco-times': 'fotos/golaco-times',
    'rota-shot-mapa': 'fotos/rota-mapa', 'rota-shot-hangar': 'fotos/rota-hangar', 'rota-shot-catalogo': 'fotos/rota-catalogo', 'rota-shot-guardiao': 'rota-guardiao',
    'volei-quadra': 'volei-jogo-quadra-2', 'volei-praia': 'volei-jogo-praia-2', 'volei-craque': 'fotos/volei-craque', 'volei-conquistas': 'fotos/volei-conquistas',
    'gol-shot-craque': 'gol-craque', 'gol-shot-gol': 'gol-noite', 'gol-shot-falta': 'gol-falta-neve', 'gol-shot-goleiro': 'gol-defesa-chuva',
    'xodo-retro': 'xodo-jogo-retro-2', 'xodo-minijogos': 'xodo-jogo-minijogo-2', 'xodo-album': 'fotos/xodo-album', 'xodo-inicio': 'xodo-jogo-moderno-2',
    'acervo-shot-detalhe': 'fotos/acervo-detalhe', 'acervo-shot-identificar': 'fotos/acervo-identificar', 'acervo-shot-relatorio': 'fotos/acervo-relatorio', 'acervo-shot-colecao': 'fotos/acervo-colecao',
  };
  const TXT = {
    pt: ['Fechar', 'Ver o vídeo'], en: ['Close', 'Watch the video'], es: ['Cerrar', 'Ver el vídeo'], de: ['Schließen', 'Video ansehen'],
    fr: ['Fermer', 'Voir la vidéo'], it: ['Chiudi', 'Guarda il video'], ja: ['閉じる', '動画を見る'], zh: ['关闭', '观看视频'],
  };
  // nome da foto sem pasta, sem extensão e sem o sufixo do idioma (xodo-album-en.jpg → xodo-album)
  const chave = (img) => img.getAttribute('src').split('/').pop().replace(/\.\w+$/, '').replace(/-(en|es|de|fr|it|ja|zh)$/, '');
  const [FECHAR, VER] = TXT[(document.documentElement.lang || 'pt').slice(0, 2)] || TXT.pt;

  const figuras = [...document.querySelectorAll('.shots figure')].filter((f) => {
    const img = f.querySelector('img');
    return img && VIDEO[chave(img)];
  });
  if (!figuras.length) return;

  const css = document.createElement('style');
  css.textContent = `
  .shots figure.tem-video { cursor: pointer }
  .shots figure.tem-video::after { content: ""; position: absolute; left: 50%; top: 50%; width: 58px; height: 58px; margin: -29px 0 0 -29px; border-radius: 50%;
    background: rgba(0,0,0,.5) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M8 5.5v13l11-6.5z'/%3E%3C/svg%3E") 56% 50% / 30px no-repeat;
    border: 2px solid rgba(255,255,255,.85); box-shadow: 0 8px 24px rgba(0,0,0,.4); transition: transform .25s, background-color .25s; pointer-events: none }
  .shots figure.tem-video:hover::after, .shots figure.tem-video:focus-visible::after { transform: scale(1.12); background-color: rgba(0,0,0,.7) }
  .shots figure.tem-video:focus-visible { outline: 3px solid var(--gold, #ffd23f); outline-offset: 3px }
  .gv { border: 0; padding: 0; background: transparent; max-width: min(94vw, 1100px); max-height: 92vh; overflow: visible; color: #fff }
  .gv::backdrop { background: rgba(5,4,12,.82); backdrop-filter: blur(6px) }
  .gv[open] { display: grid; gap: 10px; justify-items: center; animation: gv-entra .25s ease-out }
  @keyframes gv-entra { from { opacity: 0; transform: scale(.96) } }
  .gv video { display: block; max-width: min(94vw, 1100px); max-height: calc(92vh - 60px); width: auto; height: auto; border-radius: 18px; background: #000;
    box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 1px rgba(255,255,255,.12) }
  .gv p { margin: 0; font: 700 16px/1.3 var(--body, system-ui, sans-serif); text-align: center; text-shadow: 0 2px 8px rgba(0,0,0,.6) }
  .gv button { position: absolute; top: 10px; right: 10px; z-index: 1; width: 42px; height: 42px; border-radius: 50%; border: 0; cursor: pointer;
    background: rgba(255,255,255,.94); color: #111; font: 700 20px/1 system-ui, sans-serif; box-shadow: 0 6px 18px rgba(0,0,0,.45) }
  @media (prefers-reduced-motion: reduce) { .gv[open] { animation: none } .shots figure.tem-video::after { transition: none } }`;
  document.head.appendChild(css);

  const dlg = document.createElement('dialog');
  dlg.className = 'gv';
  dlg.innerHTML = `<button type="button" aria-label="${FECHAR}">✕</button><video controls muted loop playsinline preload="none"></video><p></p>`;
  document.body.appendChild(dlg);
  const video = dlg.querySelector('video');
  const legenda = dlg.querySelector('p');
  const fechar = () => dlg.close();
  dlg.querySelector('button').addEventListener('click', fechar);
  dlg.addEventListener('click', (e) => { if (e.target === dlg) fechar(); });
  dlg.addEventListener('close', () => { video.pause(); video.removeAttribute('src'); video.load(); });

  function abrir(fig) {
    const img = fig.querySelector('img');
    const nome = chave(img);
    const texto = (fig.querySelector('figcaption') || {}).textContent || img.alt || '';
    video.poster = img.currentSrc || img.src;
    video.src = '/media/' + VIDEO[nome] + '.mp4';
    video.setAttribute('aria-label', texto);
    legenda.textContent = texto;
    dlg.showModal();
    video.muted = true;
    video.play().catch(() => {});
  }

  for (const fig of figuras) {
    const texto = (fig.querySelector('figcaption') || {}).textContent || '';
    fig.classList.add('tem-video');
    fig.tabIndex = 0;
    fig.setAttribute('role', 'button');
    fig.setAttribute('aria-label', `${VER}: ${texto}`);
    fig.addEventListener('click', () => abrir(fig));
    fig.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrir(fig); } });
  }
})();
