/* Contador de acessos no topo, à direita: total geral e os 3 países com mais acessos (bandeira + número).
   Conta uma vez por visita (sessionStorage): navegar entre as páginas do site não soma de novo.
   Os números vêm da função contador_site do Supabase, que guarda só país e total (nada de IP). */
(() => {
  const URL = 'https://xmppelpzwtvxztesnspc.supabase.co/rest/v1/rpc/contador_site';
  const CHAVE = 'sb_publishable_BGtadk9ufzC4EfN7-7Aucg_EkB1fljt';
  const lang = document.documentElement.lang || 'pt-BR';
  const ROTULO = { pt: 'acessos', en: 'visits', es: 'visitas', de: 'Besuche', fr: 'visites', it: 'visite', ja: 'アクセス', zh: '访问' };
  const rotulo = ROTULO[lang.slice(0, 2)] || ROTULO.en;

  const nav = document.querySelector('.nav .wrap');
  if (!nav) return;

  let contar = false;
  try { contar = !sessionStorage.getItem('ag_visita'); sessionStorage.setItem('ag_visita', '1'); } catch { contar = false; }
  const regiao = (navigator.languages || [navigator.language]).map(l => (String(l).match(/-([A-Za-z]{2})\b/) || [])[1]).find(Boolean);

  const css = document.createElement('style');
  css.textContent = `
  .nav .wrap { position: relative }
  .visitas { position: absolute; right: 0; top: calc(100% + 6px); display: flex; align-items: center; gap: 10px; padding: 5px 12px; border-radius: 999px;
    background: rgba(13,10,32,.72); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid var(--line, rgba(255,255,255,.1));
    color: var(--ink, #f6f2ff); font: 600 13px/1.2 var(--body, system-ui, sans-serif); white-space: nowrap; font-variant-numeric: tabular-nums;
    opacity: 0; transform: translateY(-4px); transition: opacity .4s, transform .4s }
  .visitas.on { opacity: 1; transform: none }
  .visitas b { font-weight: 800 }
  .visitas .tot { display: inline-flex; align-items: center; gap: 6px }
  .visitas .tot svg { width: 15px; height: 15px; opacity: .8 }
  .visitas .tot small { color: var(--muted, #b8b0d6); font-weight: 600; font-size: 12px }
  .visitas .pais { display: inline-flex; align-items: center; gap: 5px; padding-left: 10px; border-left: 1px solid var(--line, rgba(255,255,255,.1)) }
  .visitas img { width: 18px; height: 13.5px; border-radius: 2px; object-fit: cover; box-shadow: 0 0 0 1px rgba(255,255,255,.18) }
  @media (max-width: 480px) { .visitas { gap: 8px; padding: 4px 10px; font-size: 12px } .visitas .pais { padding-left: 8px } .visitas .tot small { display: none } }
  `;
  document.head.appendChild(css);

  const num = n => { try { return new Intl.NumberFormat(lang).format(n); } catch { return String(n); } };
  let nomes = null;
  const nomePais = p => { try { nomes = nomes || new Intl.DisplayNames([lang], { type: 'region' }); return nomes.of(p) || p; } catch { return p; } };

  fetch(URL, {
    method: 'POST',
    headers: { apikey: CHAVE, 'Content-Type': 'application/json' },
    body: JSON.stringify({ p_contar: contar, p_pais: regiao || null }),
  })
    .then(r => (r.ok ? r.json() : Promise.reject(r.status)))
    .then(d => {
      if (!d || !(d.total > 0)) return;
      const box = document.createElement('div');
      box.className = 'visitas';
      box.setAttribute('role', 'status');
      const tot = document.createElement('span');
      tot.className = 'tot';
      tot.title = `${num(d.total)} ${rotulo}`;
      tot.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 5C6.5 5 2.7 9.2 1.5 12c1.2 2.8 5 7 10.5 7s9.3-4.2 10.5-7C21.3 9.2 17.5 5 12 5zm0 11.5a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9zm0-2.3a2.2 2.2 0 1 0 0-4.4 2.2 2.2 0 0 0 0 4.4z"/></svg>';
      const b = document.createElement('b');
      b.textContent = num(d.total);
      const s = document.createElement('small');
      s.textContent = rotulo;
      tot.append(b, s);
      box.appendChild(tot);
      for (const t of (d.top || []).slice(0, 3)) {
        if (!/^[A-Z]{2}$/.test(t.pais)) continue;
        const p = document.createElement('span');
        p.className = 'pais';
        p.title = `${nomePais(t.pais)}: ${num(t.total)} ${rotulo}`;
        const img = document.createElement('img');
        img.src = `https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/flags/4x3/${t.pais.toLowerCase()}.svg`;
        img.alt = nomePais(t.pais);
        img.width = 18; img.height = 14;
        const n = document.createElement('span');
        n.textContent = num(t.total);
        p.append(img, n);
        box.appendChild(p);
      }
      nav.appendChild(box);
      requestAnimationFrame(() => requestAnimationFrame(() => box.classList.add('on')));
    })
    .catch(() => {});
})();
