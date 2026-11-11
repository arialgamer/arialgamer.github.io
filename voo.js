/* Figurinhas dos jogos "voando" pelo site durante a rolagem (efeito de profundidade).
   Espalhadas pela página toda (uma a cada ~300 px, alternando os lados); cada uma mostra o jogo da seção em que está.
   Passam por cima, mas quando cruzam texto, botão, cartão ou vídeo deslizam para a borda (ou ficam transparentes); não bloqueiam toques.
   No celular ficam pela metade, saindo da borda (um pouco transparentes quando encostam no texto). Com "reduzir movimento" ligado, não flutuam. */
(() => {
  const BASE = '/media/voo/';
  const DO_JOGO = {
    gelada: ['cerveja', 'limao', 'nota10'], esconde: ['iglu', 'foguete', 'bau'], gol: ['gol', 'penalti'], acervo: ['relogio', 'moeda'],
  };
  const TODAS = ['cerveja', 'gol', 'iglu', 'limao', 'penalti', 'foguete', 'nota10', 'relogio', 'bau', 'moeda'];
  const parado = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const css = document.createElement('style');
  css.textContent = `
  .voo { position: fixed; inset: 0; pointer-events: none; z-index: 40; overflow: hidden }
  .voo i { position: absolute; top: 0; left: 0; width: var(--t); height: var(--t); will-change: transform; opacity: 0; transition: opacity .35s }
  .voo i.on { opacity: 1 }
  .voo i.on.sob { opacity: .3 }
  .voo i.on.meio { opacity: .62 }
  .voo img { width: 100%; height: 100%; display: block; border-radius: 22%; box-shadow: 0 14px 34px rgba(0,0,0,.45), 0 0 0 3px rgba(255,255,255,.85);
    animation: voo-boia var(--d) ease-in-out infinite alternate; transform: rotate(var(--g)) }
  @keyframes voo-boia { from { transform: translateY(-9px) rotate(var(--g)) } to { transform: translateY(11px) rotate(calc(var(--g) * -0.6)) } }
  @media (prefers-reduced-motion: reduce) { .voo img { animation: none } }`;
  document.head.appendChild(css);
  const caixa = document.createElement('div');
  caixa.className = 'voo';
  caixa.setAttribute('aria-hidden', 'true');
  document.body.appendChild(caixa);

  // sorteio fixo (mesma página = mesma arrumação)
  let semente = 7;
  const rnd = () => ((semente = (semente * 16807) % 2147483647) / 2147483647);

  let els = [], W = 0, H = 0, celular = false;
  function montar() {
    W = innerWidth; H = innerHeight; celular = W < 760;
    caixa.textContent = ''; els = []; semente = 7;
    const alto = document.documentElement.scrollHeight;
    const passo = celular ? 330 : 300;
    const secoes = [...document.querySelectorAll('section[id]')].map((s) => {
      const r = s.getBoundingClientRect();
      return { id: s.id, de: r.top + scrollY, ate: r.bottom + scrollY };
    });
    const usadas = [];
    for (let y = 120, k = 0; y < alto - 200 && k < 48; y += passo * (0.8 + rnd() * 0.5), k++) {
      const sec = secoes.find((s) => y >= s.de && y < s.ate);
      const lista = (sec && DO_JOGO[sec.id]) || TODAS;
      let nome = lista[Math.floor(rnd() * lista.length)];
      if (usadas.slice(-2).includes(nome)) nome = lista[(lista.indexOf(nome) + 1) % lista.length];
      usadas.push(nome);
      const lado = k % 2 ? 'r' : 'l';
      const prof = 0.2 + rnd() * 0.5; // mais perto = maior e mais rápido
      const t = celular ? Math.round(70 + prof * 40) : Math.round(100 + prof * 90);
      // celular: metade para fora; computador: até 22% da largura, a partir da borda
      const dentro = celular ? -t * (0.46 + rnd() * 0.08) : W * rnd() * 0.18 - t * 0.2;
      const x = lado === 'l' ? dentro : W - t - dentro;
      const i = document.createElement('i');
      const img = document.createElement('img');
      img.alt = ''; img.decoding = 'async'; img.loading = 'lazy'; img.src = BASE + nome + '.webp';
      img.style.setProperty('--d', `${2.4 + rnd() * 2}s`);
      img.style.setProperty('--g', `${Math.round((rnd() - 0.5) * 28)}deg`);
      i.style.setProperty('--t', t + 'px');
      i.appendChild(img);
      caixa.appendChild(i);
      els.push({ i, y, x, t, prof, lado, dx: 0 });
    }
  }

  // Está em cima de algo que a pessoa lê ou toca? (só a parte da figurinha que aparece na tela)
  const CONTEUDO = 'p,h1,h2,h3,h4,a,button,li,img,video,figure,.phone,.chip,.store,.btn,.price,.noads,.soon,dl,table,input,select,textarea,label';
  function cobre(x, y, t) {
    const x0 = Math.max(0, x), x1 = Math.min(W, x + t);
    if (x1 - x0 < 8) return false;
    for (const [fx, fy] of [[0.5, 0.5], [0.15, 0.2], [0.85, 0.2], [0.15, 0.8], [0.85, 0.8]]) {
      const px = x0 + (x1 - x0) * fx, py = y + t * fy;
      if (py < 0 || py > H) continue;
      for (const el of document.elementsFromPoint(px, py)) {
        if (el.closest('.voo')) continue;
        if (el.closest('.nav')) break;
        if (el.closest(CONTEUDO)) return true;
        break;
      }
    }
    return false;
  }

  let pedido = 0;
  function quadro() {
    pedido = 0;
    const s = scrollY;
    let mexendo = false;
    for (const e of els) {
      // profundidade: quanto mais "perto", mais rápido passa que a página (a partir do meio da tela)
      const natural = e.y - s;
      const ys = parado ? natural : natural + (natural - H / 2) * e.prof * 0.7;
      const vis = ys > -e.t - 40 && ys < H + 40;
      e.i.classList.toggle('on', vis);
      if (!vis) { e.dx = 0; continue; }
      // se cobre texto ou botão, desliza para fora (espiando na borda); só fica transparente se não houver jeito
      const fora = e.lado === 'l' ? -1 : 1;
      if (celular) {
        // celular: fica pela metade na borda; se encosta no texto, fica um pouco transparente
        e.i.classList.toggle('meio', cobre(e.x, ys, e.t));
        e.i.style.transform = `translate3d(${Math.round(e.x)}px, ${Math.round(ys)}px, 0)`;
        continue;
      }
      let alvo = null;
      for (const f of [0, 0.3, 0.55]) {
        const tentar = e.x + fora * e.t * f;
        if (!cobre(tentar, ys, e.t)) { alvo = e.t * f; break; }
      }
      e.i.classList.toggle('sob', alvo === null);
      if (alvo === null) alvo = e.t * 0.55;
      const novo = parado ? alvo : e.dx + (alvo - e.dx) * 0.18;
      if (Math.abs(novo - alvo) > 0.5) mexendo = true;
      e.dx = Math.abs(novo - alvo) > 0.5 ? novo : alvo;
      e.i.style.transform = `translate3d(${Math.round(e.x + fora * e.dx)}px, ${Math.round(ys)}px, 0)`;
    }
    if (mexendo) pedir();
  }
  const pedir = () => { if (!pedido) pedido = requestAnimationFrame(quadro); };
  addEventListener('scroll', pedir, { passive: true });
  let larg = innerWidth;
  addEventListener('resize', () => { if (innerWidth !== larg) { larg = innerWidth; montar(); } pedir(); });
  addEventListener('load', () => { montar(); pedir(); });
  montar(); quadro();
  setTimeout(() => { montar(); pedir(); }, 1500); // imagens e vídeos mudam a altura das seções
})();
