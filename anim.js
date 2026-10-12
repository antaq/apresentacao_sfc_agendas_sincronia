/* Entrada dos cards, como cartas postas na mesa: cada card cai de leve, com uma
   pequena inclinação, na ordem em que aparece na tela. Roda uma vez ao abrir o slide. */
(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var st = document.createElement('style');
  st.textContent =
    '@keyframes carta{0%{opacity:0;transform:translateY(var(--dy,-34px)) rotate(var(--rot,-2deg)) scale(1.05);box-shadow:0 22px 30px rgba(15,23,42,.18)}' +
    '60%{opacity:1}100%{opacity:1;transform:none;box-shadow:0 0 0 rgba(15,23,42,0)}}' +
    '@keyframes surge{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}' +
    '.anim-carta{animation:carta .62s cubic-bezier(.22,.9,.3,1) both;animation-delay:calc(var(--d,0) * 1s)}' +
    '.anim-surge{animation:surge .5s ease-out both;animation-delay:calc(var(--d,0) * 1s)}' +
    // barras horizontais crescem da esquerda para a direita
    '@keyframes barra-cresce{from{width:0}}' +
    '@keyframes barra-revela{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}' +
    '.oc-bar{animation:barra-cresce 1s cubic-bezier(.22,.8,.3,1) both;animation-delay:calc(var(--bd,.9) * 1s)}' +
    '.oc-bar + .oc-bar{animation-delay:calc(var(--bd,.9) * 1s + .2s)}' +
    '.bar-trk .seg{animation:barra-revela 1s cubic-bezier(.22,.8,.3,1) both;animation-delay:calc(var(--bd,.9) * 1s)}' +
    // tabelas: cabeçalho desce, cada linha desliza da esquerda e as células se acendem em cascata
    '@keyframes cabecalho{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}' +
    '@keyframes fila{from{opacity:0;transform:translateX(-16px)}to{opacity:1;transform:none}}' +
    '@keyframes celda{from{opacity:0}to{opacity:1}}' +
    '.anim-cab{animation:cabecalho .45s ease-out both;animation-delay:calc(var(--d,0) * 1s)}' +
    '.anim-fila{animation:fila .55s cubic-bezier(.22,.8,.3,1) both;animation-delay:calc(var(--d,0) * 1s)}' +
    '.anim-celda{animation:celda .5s ease-out both;animation-delay:calc(var(--d,0) * 1s)}' +
    // linhas do tempo: itens verticais descem; marcos do calendário avançam da esquerda para a direita
    '@keyframes linha-desce{from{opacity:0;clip-path:inset(0 0 100% 0);transform:translateX(-10px)}to{opacity:1;clip-path:inset(0 0 0 0);transform:none}}' +
    '@keyframes marco-avanca{from{opacity:0;clip-path:inset(0 100% 0 0)}to{opacity:1;clip-path:inset(0 0 0 0)}}' +
    '.anim-linha{animation:linha-desce .6s cubic-bezier(.22,.8,.3,1) both;animation-delay:calc(var(--d,0) * 1s)}' +
    '.anim-marco{animation:marco-avanca .6s cubic-bezier(.22,.8,.3,1) both;animation-delay:calc(var(--d,0) * 1s)}';
  document.head.appendChild(st);

  var CARTAS = '.rt,.inst,.niv-r,.pr,.enf,.nv,.card,.stat-card,.destaque,.area,.gef,.ri,.comp,.formula,' +
               '.frente,.crono,.prop,.descob,.consulta,.op-etapa,.op-perg,.pj,.sis,.ml,.recado,.tipos > div,.ben > span';
  var SURGE = '.titulo-sec';
  var TABELA = 'table.tbl';
  var LINHA = '.ps';
  var ANIM = [];                                   // tudo que recebeu --d, para o ajuste de duração
  var slide = document.querySelector('.slide');
  if (!slide) return;

  var todos = Array.prototype.slice.call(slide.querySelectorAll(CARTAS + ',' + SURGE + ',' + TABELA + ',' + LINHA)).filter(function (e) {
    var foot = slide.lastElementChild;
    if (foot.contains(e)) return false;
    var p = e.parentElement;                       // ignora cards dentro de outro card
    while (p && p !== slide) { if (p.matches(CARTAS)) return false; p = p.parentElement; }
    return true;
  });

  var passo = Math.min(0.15, 3.0 / Math.max(todos.length, 1));
  var t = 0.25, ant = null, n = 0;
  function marca(el, cls, d) { el.style.setProperty('--d', d.toFixed(2)); el.classList.add(cls); ANIM.push(el); }
  todos.forEach(function (e) {
    var pai = e.parentElement;
    if (ant && pai !== ant && !e.matches(SURGE)) t += 0.3;      // pausa entre grupos
    if (e.matches(SURGE)) { marca(e, 'anim-surge', t); t += passo * 0.5; }
    else if (e.matches(LINHA)) { marca(e, 'anim-linha', t); t += passo * 1.2; }
    else if (e.matches(TABELA)) {
      var cab = e.querySelector('thead tr');
      if (cab) { marca(cab, 'anim-cab', t); t += 0.2; }
      Array.prototype.forEach.call(e.querySelectorAll('tbody tr'), function (tr) {
        marca(tr, 'anim-fila', t);
        Array.prototype.forEach.call(tr.children, function (td, c) { marca(td, 'anim-celda', t + 0.12 + c * 0.1); });
        t += 0.17;
      });
    }
    else {
      var w = e.getBoundingClientRect().width;
      var largo = w > 900;
      var rot = (largo ? 0.5 : 1.5 + (n % 3) * 0.5) * (n % 2 ? 1 : -1);
      e.style.setProperty('--rot', rot + 'deg');
      e.style.setProperty('--dy', (largo ? -18 : -34) + 'px');
      marca(e, 'anim-carta', t);
      t += passo; n++;
    }
    ant = pai;
  });

  // Nenhum slide leva mais de ~3,3 s para ficar completo: comprime os atrasos se passar.
  var maximo = 2.7;
  if (t > maximo) {
    var f = maximo / t;
    ANIM.forEach(function (e) { e.style.setProperty('--d', (parseFloat(e.style.getPropertyValue('--d')) * f).toFixed(2)); });
  }

  // As barras começam logo depois do card que as contém (ou 0,9 s após abrir), uma linha após a outra.
  Array.prototype.forEach.call(slide.querySelectorAll('.oc-row,.bar-row'), function (row, i) {
    var card = row.closest('.anim-carta');
    var base = card ? parseFloat(card.style.getPropertyValue('--d')) + 0.5 : 0.9;
    row.style.setProperty('--bd', (base + i * 0.15).toFixed(2));
  });

  // Marcos do calendário: avançam em fila logo depois que o quadro do calendário pousa.
  Array.prototype.forEach.call(slide.querySelectorAll('.crono'), function (c) {
    var base = parseFloat(c.style.getPropertyValue('--d') || 0) + 0.45;
    Array.prototype.forEach.call(c.querySelectorAll('.marco'), function (m, i) {
      m.style.setProperty('--d', (base + i * 0.14).toFixed(2)); m.classList.add('anim-marco');
    });
  });
})();
