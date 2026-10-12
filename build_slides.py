#!/usr/bin/env python3
"""Gera as telas da apresentação da SFC no Agendas em Sincronia (13/10/2026).

Ciclo de Workshops sobre as Agendas da ANTAQ, bloco da tarde (SEPH, SFC, SESGI
e SGE). Pedido da organização: o rito do PAF, a conexão com as outras agendas,
os projetos em andamento e as melhorias a encaminhar em conjunto (cerca de 1 h).

Herda o esqueleto e nove telas do deck do PAF 2027 ao Diretor-Geral
(../apresentacao_paf_diretoria/build_slides.py), remapeadas por POSICAO, e
acrescenta as telas novas (fix=True), que já levam a posição final. Capa (01)
e encerramento (25) são escritos à mão; 04, 09, 14 e 21 são divisórias.

Para regerar: python3 build_slides.py
"""

from pathlib import Path

DST = Path(__file__).resolve().parent
TOTAL = 25
RODAPE = "Agendas em Sincronia · O Plano de Fiscalização e as Agendas da ANTAQ · SFC · 13/10/2026"
# Fator global de texto. Cada slide declara o `base` em que foi fechado; este
# fator multiplica todos eles de uma vez. Em 0.90 o texto do corpo encolhe 10%,
# e a folga que sobra vira respiro vertical entre os cards (row-gap, abaixo).
TEXT_SCALE = 0.90

BASE_CSS = """
body { margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }
.slide { width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden; background:#ffffff; }
.font-montserrat { font-family:'Montserrat',sans-serif; }
.text-brand { color:#003366; }
.bg-brand { background-color:#003366; }
.text-accent { color:#0066CC; }
.bg-accent { background-color:#0066CC; }
.header-bar { height:10px; background:#003366; width:100%; }
.secondary-bar { height:4px; background:#0066CC; width:100%; }

.stat-card {
  background: linear-gradient(135deg, #003366, #004d99);
  border-radius: 16px;
  padding: 20px 18px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
}
.stat-card::after {
  content: '';
  position: absolute; top: -30px; right: -30px;
  width: 80px; height: 80px;
  border-radius: 50%;
  background: rgba(255,255,255,0.06);
}
.stat-num {
  font-family: 'Montserrat', sans-serif;
  font-weight: 900;
  font-size: calc(48px * var(--tz));
  line-height: 1;
}
.card {
  display: flex; align-items: flex-start; gap: 16px;
  padding: 14px 20px;
  background: #F8FAFC;
  border-radius: 14px;
  border-left: 5px solid #0066CC;
}
.card-green  { background: linear-gradient(135deg,#F0FDF4,#DCFCE7); border-left-color:#22C55E; }
.card-amber  { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left-color:#F59E0B; }
.card-red    { background: linear-gradient(135deg,#FEF2F2,#FEE2E2); border-left-color:#EF4444; }
.ico {
  width:50px; height:50px; border-radius:12px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
}
/* As colunas dos slides de duas metades centram o proprio conteudo: a folga
   vertical fica dividida em cima e embaixo, em vez de sobrar toda no rodape.
   O contêiner de conteudo quase sempre E o proprio grid (`class="flex-1 ...
   grid"`), e nao um grid dentro dele — por isso os dois seletores. */
.slide > .flex-1 > .flex.flex-col,
.slide > .flex-1 > .grid > .flex.flex-col { justify-content:center; }

table.tbl { width:100%; border-collapse:collapse; }
table.tbl th {
  background:#F1F5F9; color:#475569; text-align:left;
  font-family:'Montserrat',sans-serif; font-weight:700;
  text-transform:uppercase; letter-spacing:0.06em;
  padding:10px 14px; font-size:calc(15px * var(--tz));
}
table.tbl td { padding:11px 14px; border-top:1px solid #E2E8F0; color:#334155; font-size:calc(18px * var(--tz)); }
table.tbl tr:nth-child(even) td { background:#FAFBFC; }
.num { text-align:right; font-variant-numeric:tabular-nums; }
table.tbl th.num { text-align:right; }
.pill {
  display:inline-block; padding:3px 12px; border-radius:999px;
  font-family:'Montserrat',sans-serif; font-weight:700;
  font-size:calc(14px * var(--tz)); letter-spacing:0.04em;
}
.pill-a { background:#DCFCE7; color:#166534; }
.pill-b { background:#DBEAFE; color:#1E40AF; }
.pill-c { background:#FEE2E2; color:#991B1B; }
.pill-gold { background:#FEF3C7; color:#92400E; }
.formula {
  background:#0F172A; color:#E2E8F0; border-radius:14px;
  padding:18px 24px; font-family:'Courier New',monospace;
  font-size:calc(20px * var(--tz)); letter-spacing:0.02em;
}
.destaque {
  background: linear-gradient(135deg,#003366,#0066CC);
  color:#fff; border-radius:16px; padding:16px 24px;
}
.legenda { color:#64748B; font-size:calc(15px * var(--tz)); line-height:1.5; }
.novo-tag {
  display:inline-flex; align-items:center; gap:7px;
  background:#FFD700; color:#003366; border-radius:999px;
  padding:3px 14px; font-family:'Montserrat',sans-serif;
  font-weight:900; font-size:calc(13px * var(--tz));
  letter-spacing:0.1em; text-transform:uppercase;
}

/* Respiro vertical entre os cards.
   Os utilitarios gap-* do Tailwind valem para as duas direcoes, e mexer no
   `gap` cheio estreitaria as colunas dos grids de duas metades. Por isso aqui
   so o `row-gap` e reescrito: um card fica mais longe do card de baixo, e a
   largura das colunas continua exatamente a mesma. Esta folha vem depois do
   CDN no <head>, entao vence no desempate por ordem. */
.gap-2 { row-gap:18px; }
.gap-3 { row-gap:30px; }
.gap-4 { row-gap:32px; }
.gap-5 { row-gap:34px; }
.gap-6 { row-gap:34px; }
.gap-8 { row-gap:38px; }
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
<style>{css}</style>
</head>
<body>
<div class="slide">
  <div class="header-bar"></div>
  <div class="secondary-bar"></div>

  <div class="px-16 pt-7 pb-6">
    <div class="flex items-center gap-4">
      <div style="width:5px; align-self:stretch;" class="bg-accent"></div>
      <div>
        <p class="font-montserrat font-bold text-gray-400 text-lg uppercase tracking-widest" style="margin-bottom:10px;">{kicker}</p>
        <p class="text-5xl font-montserrat font-bold text-brand uppercase tracking-tight">{titulo}</p>
      </div>
      <div class="ml-auto flex items-center gap-3">
        {tag}
        <img src="assets/logo-antaq-azul.png" alt="ANTAQ" style="height:32px;">
        <p class="font-montserrat font-bold text-gray-400 tracking-wider" style="font-size:12px; line-height:1.35; white-space:nowrap;">SFC<br/>GRAT · GPF · GCOR</p>
      </div>
    </div>
  </div>

{body}

  <div class="px-16 pb-4 flex justify-between items-center border-t border-gray-100 pt-3 mx-8">
    <p class="text-gray-400 text-sm">{rodape}</p>
    <p class="text-gray-300 text-sm font-mono">{n} / {total}</p>
  </div>
</div>
<script src="zoom.js"></script>
<script>document.addEventListener("keydown",function(e){{if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){{e.preventDefault();window.parent.postMessage({{type:"slide-nav",key:e.key}},"*");}}}});</script>
</body>
</html>
"""

TAG_NOVO = '<span class="novo-tag"><i class="fas fa-star"></i> Novidade 2027</span>'

SLIDES: list[dict] = []
def slide(n, title, kicker, titulo, body, extra_css="", tag="", base=1.0):
    SLIDES.append(
        dict(n=n, title=title, kicker=kicker, titulo=titulo, body=body,
             extra_css=extra_css, tag=tag, base=base)
    )



# Acréscimos deste deck ao CSS comum: etiqueta de bloco, fonte, gráficos de barra.
BASE_CSS += """
.bloco-tag {
  display:inline-flex; align-items:center; gap:8px;
  border-radius:999px; padding:4px 16px; font-family:'Montserrat',sans-serif; white-space:nowrap;
  font-weight:900; font-size:calc(13px * var(--tz)); letter-spacing:0.08em; text-transform:uppercase;
}
.bt-risco { background:#FEE2E2; color:#991B1B; }
.bt-tema  { background:#DBEAFE; color:#1E3A8A; }
.bt-geral { background:#FEF3C7; color:#92400E; }
.bt-oper  { background:#DCFCE7; color:#166534; }
.fonte { color:#94A3B8; font-size:calc(13px * var(--tz)); line-height:1.4; }
.titulo-sec { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(21px * var(--tz)); }
.sub-sec { color:#64748B; font-size:calc(15px * var(--tz)); }
.num-badge {
  width:38px; height:38px; border-radius:50%; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  background:#003366; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900;
  font-size:calc(17px * var(--tz));
}
.card p { margin:0; }
.card-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(19px * var(--tz)); }
.card-d { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.45; margin-top:3px !important; }

/* Barras: trilho cinza, segmentos com 2px de folga entre si e rótulo direto. */
.bar-row { display:grid; grid-template-columns: var(--rot, 300px) 1fr; align-items:center; gap:14px; }
.bar-rot { color:#334155; font-size:calc(17px * var(--tz)); line-height:1.25; text-align:right; }
.bar-rot strong { color:#003366; }
.bar-trk { display:flex; gap:2px; height:42px; }
.seg {
  height:100%; display:flex; align-items:center; justify-content:center;
  font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(17px * var(--tz));
  color:#fff; min-width:0; overflow:hidden; white-space:nowrap;
}
.seg:first-child { border-radius:4px 0 0 4px; }
.seg:last-child  { border-radius:0 4px 4px 0; }
.seg:only-child  { border-radius:4px; }
.leg-row { display:flex; flex-wrap:wrap; gap:22px; color:#475569; font-size:calc(16px * var(--tz)); }
.leg-row span { display:inline-flex; align-items:center; gap:7px; }
.leg-row i.sw { width:18px; height:18px; border-radius:3px; display:inline-block; }
/* Título com tamanho fixo em todos os slides: não acompanha o fator de texto,
   para que títulos longos não quebrem linha quando o corpo cresce. */
.slide p.text-5xl { font-size:54px !important; line-height:1.1 !important; }
"""

TAG_GERAL = '<span class="bloco-tag bt-geral"><i class="fas fa-compass"></i> Visão geral</span>'
TAG_RISCO = '<span class="bloco-tag bt-risco"><i class="fas fa-gauge-high"></i> Bloco 1 · Grupo de risco</span>'
TAG_TEMA = '<span class="bloco-tag bt-tema"><i class="fas fa-layer-group"></i> Bloco 2 · Temáticas</span>'
TAG_OPER = '<span class="bloco-tag bt-oper"><i class="fas fa-screwdriver-wrench"></i> Operacionais</span>'
NT = "NT nº 27/2026/GPF/SFC"

# Escala de alcance: ordinal, então rampa sequencial de um azul só (mais escuro =
# mais alcance) e cinza neutro para "sem aderência". Rótulo direto em todo segmento.
C_INT, C_PAR, C_IND, C_SEM = "#003366", "#2F6FB3", "#8DB8E6", "#CBD5E1"
# Situação das matérias: categorias de estado, cada uma com rótulo e legenda.
C_ATD, C_CNV, C_NOV, C_ART, C_FORA = "#15803D", "#0066CC", "#D97706", "#7C3AED", "#64748B"


def barra(rotulo, segs, total, titulo=""):
    """Uma linha de barra empilhada. segs = [(valor, cor, cor_texto), ...]."""
    partes = []
    for v, cor, txt in segs:
        if not v:
            continue
        partes.append(
            f'<div class="seg" style="width:{100 * v / total:.2f}%;background:{cor};color:{txt};" '
            f'title="{titulo}{v}">{v}</div>'
        )
    return (f'<div class="bar-row"><div class="bar-rot">{rotulo}</div>'
            f'<div class="bar-trk">{"".join(partes)}</div></div>')


# ===========================================================================
# BLOCO 2 — FISCALIZAÇÕES TEMÁTICAS (NT 27/2026)
# ===========================================================================

# ---------------------------------------------------------------------------
# 08 — Contexto e premissa
# ---------------------------------------------------------------------------
slide(
    8,
    "Temáticas — contexto e premissa",
    f"Fiscalizações temáticas · {NT}",
    "Por que e com que acervo",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-6 flex flex-col gap-3">
      <p class="titulo-sec">Origem da demanda</p>
      <div class="card">
        <div class="num-badge">1</div>
        <div>
          <p class="card-t">Deliberação-DG nº 96/2025</p>
          <p class="card-d">Referendada pelo Acórdão nº 41-2026-ANTAQ: discutir previamente a proposta
          do PAF com as unidades finalísticas e as Diretorias, para captar temáticas ainda não mapeadas.</p>
        </div>
      </div>
      <div class="card">
        <div class="num-badge">2</div>
        <div>
          <p class="card-t">Ofício Circular nº 2/2026/SFC/ANTAQ</p>
          <p class="card-d">Consulta à SRG, à SESGI, à SOG e à SEPH sobre fiscalizações temáticas
          relevantes, com prazo encerrado em <strong>17/08/2026</strong>.</p>
        </div>
      </div>
      <div class="card card-amber">
        <div class="num-badge" style="background:#B45309;">3</div>
        <div>
          <p class="card-t">O limite da consulta interna</p>
          <p class="card-d">As fontes da Agência registram o que já chegou a ela. O problema que
          <strong>não gera autuação nem manifestação</strong> fica invisível ao planejamento — daí a
          avaliação das contribuições externas.</p>
        </div>
      </div>
    </div>

    <div class="col-span-6 flex flex-col gap-3">
      <p class="titulo-sec">O acervo já existia: revisão da Agenda Regulatória 2025-2028</p>
      <div class="grid grid-cols-4 gap-3">
        <div class="stat-card"><p class="stat-num">99</p><p class="text-blue-200 text-sm font-semibold mt-2">contribuições validadas<br/>(17/04 a 05/06/2026)</p></div>
        <div class="stat-card"><p class="stat-num">90</p><p class="text-blue-200 text-sm font-semibold mt-2">do público externo,<br/>em 65 formulários</p></div>
        <div class="stat-card"><p class="stat-num">8</p><p class="text-blue-200 text-sm font-semibold mt-2">de unidades internas<br/>(3 da SFC)</p></div>
        <div class="stat-card"><p class="stat-num">1</p><p class="text-blue-200 text-sm font-semibold mt-2">do Poder Concedente<br/>(MPor)</p></div>
      </div>
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(21px * var(--tz));">Tomada de Subsídios dispensada neste ciclo</p>
        <p class="text-blue-100 text-lg mt-1">
          <strong>Mesmo universo de respondentes</strong> que uma consulta própria buscaria (Res. ANTAQ nº 40/2021, art. 2º);
          <strong>volume e aderência</strong> — 4 eixos, 25 subgrupos, gargalos concretos da operação;
          e o <strong>custo</strong> de repetir: fadiga de participação, sobreposição com o ciclo regulatório
          e prazo da DC em 31/10/2026. O acervo foi examinado <strong>na íntegra</strong>, sem recorte prévio.
        </p>
      </div>
      <div class="card card-green">
        <div class="ico" style="background:#BBF7D0;"><i class="fas fa-calendar-plus text-green-700 text-2xl"></i></div>
        <div>
          <p class="card-t">Para os próximos ciclos</p>
          <p class="card-d">Consulta externa no calendário regular do PAF, aberta no 1º semestre e articulada
          com a SRG, gestora da participação social no ciclo regulatório.</p>
        </div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Relatório Técnico nº 4/2026/CGGR/SRG · Processo nº 50300.009940/2026-03. Fonte: {NT}, itens 2 e 3.</p>
""",
    tag=TAG_TEMA,
    base=1.48,
)

# ---------------------------------------------------------------------------
# 10 — Confronto com os três instrumentos
# ---------------------------------------------------------------------------
_esc = lambda i, p, d, s: [(i, C_INT, "#fff"), (p, C_PAR, "#fff"), (d, C_IND, "#003366"), (s, C_SEM, "#334155")]
slide(
    10,
    "Temáticas — confronto com os instrumentos",
    f"Resultados · {NT}, itens 5.2 a 5.5",
    "Quem já alcança as 99 demandas",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-8">
    <div class="col-span-7 flex flex-col justify-center gap-5" style="--rot:250px;">
      <div>
        <p class="titulo-sec">Alcance de cada instrumento sobre as 99 demandas</p>
        <p class="sub-sec">número de demandas por grau de alcance</p>
      </div>
      <div class="leg-row">
        <span><i class="sw" style="background:{C_INT};"></i>Integral</span>
        <span><i class="sw" style="background:{C_PAR};"></i>Parcial</span>
        <span><i class="sw" style="background:{C_IND};"></i>Indireta</span>
        <span><i class="sw" style="background:{C_SEM};"></i>Sem aderência</span>
      </div>
      {barra("<strong>Agenda Regulatória</strong><br/>2025-2028", _esc(42, 27, 7, 23), 99)}
      {barra("<strong>Agenda de Estudos</strong><br/>2025/2028", _esc(28, 45, 7, 19), 99)}
      {barra("<strong>Fiscalizações temáticas</strong><br/>PAF 2026", _esc(43, 32, 0, 24), 99)}
      <div class="grid grid-cols-2 gap-4 mt-2">
        <div class="card">
          <div class="ico" style="background:#DBEAFE;"><i class="fas fa-book text-accent text-2xl"></i></div>
          <div><p class="card-t">Agenda Regulatória</p>
          <p class="card-d">Tema 2.6 é o principal de 5 blocos (31 demandas). Os temas 1.1 a 1.4, de
          Navegação Interior, não foram alcançados.</p></div>
        </div>
        <div class="card">
          <div class="ico" style="background:#DBEAFE;"><i class="fas fa-flask text-accent text-2xl"></i></div>
          <div><p class="card-t">Agenda de Estudos</p>
          <p class="card-d">24 dos 27 estudos alcançados; ficam sem demanda P11, P16 e P20
          (navegação interior e passageiros).</p></div>
        </div>
      </div>
    </div>

    <div class="col-span-5 flex flex-col justify-center gap-4">
      <div class="destaque flex items-center gap-5">
        <p class="font-montserrat font-black" style="font-size:calc(60px * var(--tz)); line-height:1;">70</p>
        <p class="text-blue-100 text-xl">demandas, em 11 blocos, são alcançadas <strong>pelos três instrumentos</strong> ao mesmo tempo</p>
      </div>
      <div class="descob">
        <div class="flex items-center gap-4 mb-3">
          <p class="font-montserrat font-black text-brand" style="font-size:calc(48px * var(--tz)); line-height:1;">14</p>
          <p class="card-t">demandas, em 6 blocos,<br/>sem cobertura em nenhum instrumento</p>
        </div>
        <ul>
          <li>Inovação e cibersegurança</li>
          <li>Avaliação de resultado regulatório</li>
          <li>Terminais de passageiros e biometria</li>
          <li>Resíduos de embarcações</li>
          <li>Modelo de fiscalização e supervisão regulatória</li>
          <li>Padronização e compartilhamento de dados marítimos</li>
        </ul>
        <p class="legenda mt-3">Esses blocos descobertos orientam o critério de <strong>complementaridade</strong> na escolha das novas temáticas.</p>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {NT}, itens 5.2 a 5.5.</p>
""",
    extra_css="""
.descob { background:#FFFBEB; border:1px solid #FDE68A; border-radius:16px; padding:18px 22px; }
.descob p { margin:0; }
.descob ul { margin:0; padding:0; list-style:none; display:grid; grid-template-columns:1fr 1fr; gap:8px 18px; }
.descob li { color:#334155; font-size:calc(16px * var(--tz)); padding-left:20px; position:relative; line-height:1.35; }
.descob li::before { content:''; position:absolute; left:2px; top:calc(8px * var(--tz)); width:9px; height:9px; border-radius:2px; background:#D97706; }
""",
    tag=TAG_TEMA,
    base=1.61,
)

# ---------------------------------------------------------------------------
# 13 — Proposta: manter quatro, substituir três
# ---------------------------------------------------------------------------
slide(
    13,
    "Temáticas — proposta para o PAF 2027",
    f"Proposta PAF 2027 · {NT}, itens 6.1 a 6.3",
    "Manter quatro, substituir três",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-4">
    <div class="flex-1 grid grid-cols-12 gap-6">
      <div class="col-span-7 flex flex-col gap-3">
        <p class="titulo-sec"><i class="fas fa-circle-check" style="color:#15803D;"></i> Manter, com escopo ajustado</p>
        <div class="prop">
          <span class="prop-n">I</span>
          <div><p class="card-t">Diagnóstico do desempenho das APs</p>
          <p class="card-d">6 blocos, 17 demandas. Absorve 2 matérias de novo ciclo e 3 conversíveis; avalia APs ainda não fiscalizadas e retoma as avaliações mais antigas.</p></div>
        </div>
        <div class="prop">
          <span class="prop-n">II</span>
          <div><p class="card-t">Estrutura de fiscalização das APs</p>
          <p class="card-d">Instituições restantes; articulação com o GT do tema 2.8 da Agenda Regulatória para as matérias sem método.</p></div>
        </div>
        <div class="prop">
          <span class="prop-n">III</span>
          <div><p class="card-t">Diagnóstico dos Convênios de Delegação</p>
          <p class="card-d">Convênios restantes; mantida pela articulação com a fiscalização em curso do <strong>TCU</strong>, não pelo volume de demandas.</p></div>
        </div>
        <div class="prop" style="border-color:#FDE68A; background:#FFFBEB;">
          <span class="prop-n" style="background:#D97706;">IV</span>
          <div><p class="card-t">Serviços em terminais de contêineres <span class="pill pill-gold">novo nome</span></p>
          <p class="card-d">Hoje &ldquo;Preço em terminais de contêineres&rdquo;: maior alcance do conjunto (36 demandas) e 7 das 9 matérias de novo ciclo.</p></div>
        </div>
      </div>

      <div class="col-span-5 flex flex-col gap-3">
        <p class="titulo-sec"><i class="fas fa-magnifying-glass" style="color:#B45309;"></i> Avaliar</p>
        <div class="card card-amber">
          <div><p class="card-t">Transporte misto · Atraso e omissão de navios de contêineres</p>
          <p class="card-d">O universo de regulados permite concluir já neste ciclo, sem repetição no curto prazo.</p></div>
        </div>
        <p class="titulo-sec"><i class="fas fa-arrow-right-arrow-left" style="color:#B91C1C;"></i> Substituir</p>
        <div class="card card-red">
          <div><p class="card-t">Contabilização de TPB no REB</p>
          <p class="card-d">Eliminar ou suceder por tema de afretamento (outorgas e critérios), com o mesmo universo de regulados e o acervo já constituído.</p></div>
        </div>
        <div class="destaque">
          <p class="font-montserrat font-bold" style="font-size:calc(19px * var(--tz));">Por que &ldquo;Serviços&rdquo; e não &ldquo;Preço&rdquo;</p>
          <p class="text-blue-100 text-base mt-1">6 das 7 matérias pendentes tratam das <strong>condições de prestação</strong>:
          qualidade, tempestividade, rastreabilidade, continuidade e isonomia. O preço passa a ser uma dimensão —
          a cobrança e a transparência tarifária continuam integralmente apuradas, e afasta-se a leitura restritiva do escopo pelos regulados.</p>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-4 conta">
      <i class="fas fa-scale-balanced text-accent text-2xl"></i>
      <p><strong>Quantidade mantida em 7 temáticas</strong>, pela capacidade operacional da equipe e a complexidade dos temas:
      <span class="pill pill-a">4 mantidas</span> + <span class="pill pill-gold">3 vagas</span> a preencher na próxima etapa.</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Reperfilamento: Lei nº 12.815/2013, art. 3º, II; Lei nº 10.233/2001, art. 20, II, &ldquo;a&rdquo;. Fonte: {NT}, itens 6.1, 6.2 e 6.3.</p>
""",
    extra_css="""
.prop { display:flex; gap:16px; align-items:flex-start; background:#F0FDF4; border:1px solid #BBF7D0; border-radius:14px; padding:12px 18px; }
.prop p { margin:0; }
.prop-n {
  min-width:44px; height:44px; border-radius:12px; background:#15803D; color:#fff; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(18px * var(--tz));
}
.conta { background:#F8FAFC; border-radius:14px; padding:12px 20px; }
.conta p { margin:0; color:#334155; font-size:calc(17px * var(--tz)); }
""",
    tag=TAG_TEMA,
    base=1.39,
)
# ---------------------------------------------------------------------------
# 15 — Três vagas: candidatos e consulta às URs
# ---------------------------------------------------------------------------
slide(
    15,
    "Temáticas — candidatos às três vagas",
    f"Proposta PAF 2027 · {NT}, itens 5.13 a 6.5 e 7",
    "Candidatos às três vagas",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-6 flex flex-col gap-3">
      <p class="titulo-sec">Ancorados na Agenda Regulatória <span class="text-gray-400">· 37 demandas</span></p>
      <table class="tbl">
        <thead><tr><th>Tema</th><th class="num">Dem.</th><th>Agenda Regulatória</th><th>Estudos</th></tr></thead>
        <tbody>
          <tr><td><strong>Agentes intermediários</strong> na cadeia de contêineres</td><td class="num">13</td><td>2.5 · não iniciado (2027)</td><td>P14 · a iniciar</td></tr>
          <tr><td><strong>Navegação interior</strong> em estiagem severa</td><td class="num">4</td><td>sem tema relacionado</td><td>P6 (indireto) · concluído</td></tr>
          <tr><td><strong>Pátios de triagem</strong> e acessos ao porto organizado</td><td class="num">2</td><td>3.5 · não iniciado (2026)</td><td>P1 · em andamento</td></tr>
          <tr style="background:#FFFBEB;"><td><strong>Apoio marítimo</strong>: outorgas e afretamento</td><td class="num"><strong>18</strong></td><td>2.7 · fase inicial; 2.4 · não iniciado</td><td>P21, P17 e P27</td></tr>
        </tbody>
      </table>
      <p class="legenda">Matéria regulatória em fase inicial ou estudo não concluído: a fiscalização gera <strong>evidência de campo</strong>
      aproveitável, sem sobrepor trabalho avançado. Apoio marítimo é o maior bloco da consulta, hoje apurado só no TPB.</p>

    </div>

    <div class="col-span-6 flex flex-col gap-2">
      <p class="titulo-sec">Reuniões de avaliação e Superintendências finalísticas</p>
      <div class="cand cand-c"><span>I</span>Recepção de resíduos de embarcações e reporte de dados ambientais</div>
      <div class="cand cand-c"><span>II</span>Inovação e cibersegurança das Autoridades Portuárias</div>
      <div class="cand cand-c"><span>III</span>Reincidência e efetividade das penalidades na navegação interior</div>
      <div class="cand"><span>IV</span>Transparência aos usuários, com expansão a TUPs e arrendamentos</div>
      <div class="cand"><span>V</span>Transporte marítimo de animais vivos e planos de contingência</div>
      <div class="cand"><span>VI</span>Retirada de resíduos de embarcações: efetividade e rastreabilidade</div>
      <div class="cand"><span>VII</span>Produtividade de arrendamentos</div>
      <div class="cand"><span>VIII</span>Manutenção de infraestruturas terrestres nos portos organizados</div>
      <div class="cand"><span>IX</span>Equipamentos e forma de embarque e desembarque de granel sólido</div>
      <p class="legenda mt-1"><span class="pill pill-gold">I a III</span> alcançam blocos <strong>sem cobertura</strong> em qualquer instrumento (complementaridade).
      I e VI incidem sobre o mesmo objeto: apreciar em conjunto, para temática única ou delimitação expressa.</p>

      <div class="consulta">
        <p class="card-t"><i class="fas fa-building-columns text-accent"></i> 10 matérias das Superintendências finalísticas</p>
        <div class="grid grid-cols-5 gap-2 mt-2">
          <div class="mt"><b>2</b><span>execução imediata — viraram os temas IV e VI ao lado</span></div>
          <div class="mt"><b>1</b><span>já contemplada na fiscalização de contêineres</span></div>
          <div class="mt"><b>2</b><span>para o GEF Investimentos</span></div>
          <div class="mt"><b>2</b><span>condicionadas a MAPA/ANVISA ou método conjunto</span></div>
          <div class="mt"><b>3</b><span>dependem de método — sem descarte</span></div>
        </div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">GEF: Grupo Especializado de Fiscalização. Fonte: {NT}, itens 5.13 a 5.17, 6.3 a 6.5 e Quadros 3 e 6.</p>
""",
    extra_css="""
.cand { display:flex; align-items:center; gap:14px; background:#F8FAFC; border-radius:10px; padding:6px 14px;
  color:#334155; font-size:calc(17px * var(--tz)); line-height:1.3; }
.cand span { min-width:40px; font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(15px * var(--tz)); }
.cand-c { background:#FFFBEB; border:1px solid #FDE68A; }
.consulta { background:#F8FAFC; border-radius:14px; padding:12px 16px; }
.consulta p { margin:0; }
.mt { background:#fff; border:1px solid #E2E8F0; border-radius:10px; padding:8px 10px; display:flex; flex-direction:column; gap:2px; }
.mt b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(26px * var(--tz)); line-height:1; }
.mt span { color:#64748B; font-size:calc(14.5px * var(--tz)); line-height:1.3; }
""",
    tag=TAG_TEMA,
    base=1.28,
)

# ===========================================================================
# 17 — FISCALIZAÇÕES OPERACIONAIS (adaptado de operacionais-paf2027-dg.pptx)
# ===========================================================================
def _etapa(num, titulo, texto, ultimo=False):
    seta = "" if ultimo else '<i class="fas fa-chevron-right op-seta"></i>'
    return (f'<div class="op-etapa"><span class="op-num">{num}</span>'
            f'<p class="op-t">{titulo}</p><p class="op-d">{texto}</p>{seta}</div>')


def _pergunta(num, texto):
    return f'<div class="op-perg"><span class="op-num">{num}</span><p>{texto}</p></div>'


slide(
    17,
    "Fiscalizações operacionais no PAF 2027",
    "Proposta PAF 2027 · Fiscalizações operacionais",
    "Fiscalizações operacionais",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col op-col">
    <p class="op-lead">A fiscalização organizada para <strong>resolver problemas regulatórios conhecidos</strong>:
    dirigida a um problema do setor, e não a um agente específico.</p>

    <div>
      <p class="titulo-sec"><i class="fas fa-compass-drafting text-accent"></i> Planejar <span class="sub-sec">· nesta ordem</span></p>
      <div class="op-linha">
        {_etapa("01", "Problema", "O que prejudica o usuário ou o serviço, e por que persiste.")}
        {_etapa("02", "Evidência", "O que precisa ser medido em campo, e o dado que a Agência já recebe e não usa.")}
        {_etapa("03", "Instrumento", "O que resolve com as ferramentas de hoje e o que falta criar: norma, dado, sistema, articulação com outros órgãos.")}
        {_etapa("04", "Abordagem diferenciada", "Precisa do apoio da SFC, da aprovação da Diretoria ou de outras áreas da ANTAQ?", ultimo=True)}
      </div>
    </div>

    <div>
      <p class="titulo-sec"><i class="fas fa-chart-line text-accent"></i> Medir os resultados <span class="sub-sec">· no ciclo seguinte</span></p>
      <div class="op-linha">
        {_pergunta("01", "Resolvemos o problema?")}
        {_pergunta("02", "Houve avanço ou melhoria em relação ao problema original?")}
        {_pergunta("03", "Precisamos de uma nova abordagem?")}
        {_pergunta("04", "A fiscalização sozinha consegue resolver?")}
      </div>
    </div>

    <div class="grid grid-cols-12 op-base">
      <div class="col-span-7 destaque flex items-center gap-5">
        <i class="fas fa-arrow-right-arrow-left text-3xl" style="color:#FFD700;"></i>
        <p style="margin:0;"><strong>A ordem importa.</strong> Hoje o caminho costuma ser o inverso: o instrumento vem dado
        de antemão e o problema só aparece no relatório. Assim, a fiscalização passa a gerar <strong style="color:#FFD700;">evidência
        de campo para aperfeiçoar a norma</strong>.</p>
      </div>
      <div class="col-span-5 card card-green">
        <div class="ico" style="background:#BBF7D0;"><i class="fas fa-map-location-dot text-green-700 text-2xl"></i></div>
        <div><p class="card-t">A escala decorre do problema</p>
        <p class="card-d">Operação coordenada quando o problema é comum a várias regiões; localizada quando é de uma só.</p></div>
      </div>
    </div>
  </div>
""",
    extra_css="""
.op-col { justify-content:space-evenly; gap:18px; }
.op-lead { margin:0; color:#475569; font-size:calc(20px * var(--tz)); line-height:1.4; }
.op-lead strong { color:#003366; }
.op-linha { display:grid; grid-template-columns:repeat(4, 1fr); gap:36px; margin-top:12px; }
.op-etapa, .op-perg { position:relative; background:#F1F5F8; border-radius:16px; padding:18px 22px; }
.op-etapa p, .op-perg p { margin:0; }
.op-num { font-family:'Montserrat',sans-serif; font-weight:900; color:#E2A03F; font-size:calc(30px * var(--tz)); line-height:1; }
.op-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#21295C; font-size:calc(21px * var(--tz)); margin-top:8px !important; }
.op-d { color:#56616F; font-size:calc(16px * var(--tz)); line-height:1.45; margin-top:4px !important; }
.op-seta { position:absolute; right:-27px; top:50%; transform:translateY(-50%); color:#E2A03F; font-size:20px; }
.op-perg { display:flex; align-items:center; gap:16px; }
.op-perg p { font-family:'Montserrat',sans-serif; font-weight:700; color:#21295C; font-size:calc(18px * var(--tz)); line-height:1.3; }
.op-base { gap:24px; }
.op-base .destaque p { font-size:calc(17px * var(--tz)); line-height:1.45; }
""",
    tag=TAG_OPER,
    base=1.5,
)


# ===========================================================================
# VISÃO GERAL
# ===========================================================================
NTM = "minuta da NT de Metodologia do PAF 2027 (rodada de validação de 29/09/2026)"

slide(
    2,
    "PAF 2027 — duas frentes",
    "Plano Anual de Fiscalização 2027 · proposta em consolidação",
    "O PAF 2027 em duas frentes",
    """
  <div class="flex-1 px-16 pb-2 flex flex-col gap-4">
    <div class="flex-1 grid grid-cols-2 gap-6">
      <div class="frente">
        <div class="frente-top" style="background:linear-gradient(135deg,#7F1D1D,#B91C1C);">
          <i class="fas fa-gauge-high"></i>
          <div><p class="frente-k">Frente 1</p><p class="frente-t">Fiscalizações do grupo de risco</p></div>
        </div>
        <div class="frente-body">
          <p class="frente-q">Quem fiscalizar, e com que intensidade?</p>
          <p>Cada outorga recebe uma nota de risco (<strong>IPR 2.0</strong>) e uma faixa de A1 a C4.
          A faixa define a ação: presencial no Grupo C, remota no B, sorteio no A.</p>
          <div class="grid grid-cols-3 gap-3 mt-1">
            <div class="kpi"><b>2.466</b><span>outorgas avaliadas</span></div>
            <div class="kpi"><b>&asymp;669</b><span>no PAF 2027</span></div>
            <div class="kpi"><b>45,9 mil</b><span>horas · 83% da capacidade</span></div>
          </div>
          <p class="frente-f"><i class="fas fa-file-lines"></i> Minuta da NT de Metodologia do PAF 2027 · IPR 2.0 (NT 11, 12, 19 e 20/2026)</p>
        </div>
      </div>

      <div class="frente">
        <div class="frente-top" style="background:linear-gradient(135deg,#003366,#0066CC);">
          <i class="fas fa-layer-group"></i>
          <div><p class="frente-k">Frente 2</p><p class="frente-t">Fiscalizações temáticas</p></div>
        </div>
        <div class="frente-body">
          <p class="frente-q">Que problema do setor examinar a fundo?</p>
          <p>Ações transversais sobre um tema, e não sobre uma outorga. Para 2027, a escolha partiu das
          <strong>99 contribuições</strong> da revisão da Agenda Regulatória, como pede a Deliberação-DG nº 96/2025.</p>
          <div class="grid grid-cols-3 gap-3 mt-1">
            <div class="kpi"><b>7</b><span>temáticas (quantidade mantida)</span></div>
            <div class="kpi"><b>4</b><span>mantidas, com escopo ajustado</span></div>
            <div class="kpi"><b>3</b><span>vagas a preencher</span></div>
          </div>
          <p class="frente-f"><i class="fas fa-file-lines"></i> Nota Técnica nº 27/2026/GPF/SFC · SEI 3024667</p>
        </div>
      </div>
    </div>

    <div class="crono">
      <p class="titulo-sec mb-2">Calendário até a Diretoria Colegiada</p>
      <div class="grid grid-cols-5 gap-3">
        <div class="marco feito"><b>29/09</b><span>Rodada de validação do IPR e equalização aprovada</span></div>
        <div class="marco feito"><b>30/09</b><span>Data de referência do ciclo 2027 (corte cadastral)</span></div>
        <div class="marco feito"><b>02/10</b><span>Encerrada a consulta às Unidades Regionais; extração oficial e sorteio do Grupo A</span></div>
        <div class="marco hoje"><b>13/10 · hoje</b><span>Agendas em Sincronia: a proposta apresentada às demais agendas</span></div>
        <div class="marco"><b>Até 31/10</b><span>Submissão do PAF 2027 à Diretoria Colegiada</span></div>
      </div>
    </div>
  </div>
""",
    extra_css="""
.frente { border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; display:flex; flex-direction:column; }
.frente-top { color:#fff; padding:16px 24px; display:flex; align-items:center; gap:16px; }
.frente-top i { font-size:calc(30px * var(--tz)); opacity:0.9; }
.frente-top p { margin:0; }
.frente-k { font-family:'Montserrat',sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:0.12em; font-size:calc(13px * var(--tz)); opacity:0.8; }
.frente-t { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(26px * var(--tz)); }
.frente-body { flex:1; padding:18px 24px; display:flex; flex-direction:column; justify-content:space-between; gap:10px; }
.frente-body p { margin:0; color:#475569; font-size:calc(17px * var(--tz)); line-height:1.5; }
.frente-body strong { color:#003366; }
.frente-body p.frente-q { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(22px * var(--tz)); }
.frente-body p.frente-f { color:#94A3B8; font-size:calc(13.5px * var(--tz)); }
.kpi { background:#F8FAFC; border-radius:12px; padding:10px 14px; display:flex; flex-direction:column; }
.kpi b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(30px * var(--tz)); line-height:1.1; }
.kpi span { color:#64748B; font-size:calc(14px * var(--tz)); }
.crono { background:#F8FAFC; border-radius:16px; padding:14px 20px; }
.crono p { margin:0; }
.marco { border-top:5px solid #CBD5E1; padding-top:8px; display:flex; flex-direction:column; gap:3px; }
.marco b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(19px * var(--tz)); }
.marco span { color:#64748B; font-size:calc(14px * var(--tz)); line-height:1.35; }
.marco.feito { border-top-color:#0066CC; }
.marco.hoje { border-top-color:#FFD700; }
.marco.hoje b { color:#92400E; }
""",
    tag=TAG_GERAL,
    base=1.61,
)


# ===========================================================================
# BLOCO 1 — FISCALIZAÇÕES DO GRUPO DE RISCO (IPR 2.0)
# ===========================================================================

# Colunas das faixas: um matiz por grupo (verde A, azul B, vermelho C), com o tom
# escurecendo dentro do grupo conforme a intensidade da ação. Rótulo direto em cada coluna.
_FAIXAS = [
    ("A1", 272, "monitoramento", "#4ADE80"), ("A2", 159, "monitoramento", "#16A34A"),
    ("B1", 906, "documental", "#60A5FA"), ("B2", 502, "à distância", "#1D4ED8"),
    ("C1", 286, "programada", "#F87171"), ("C2", 194, "sem aviso", "#EF4444"),
    ("C3", 77, "intensiva", "#B91C1C"), ("C4", 30, "intervenção", "#7F1D1D"),
]


def _colunas_faixa():
    vmax = 1000
    grade = "".join(
        f'<div class="cc-grid" style="bottom:{100 * g / vmax:.1f}%;"></div>' for g in (250, 500, 750)
    )
    cols = "".join(
        f'<div class="cc-col" title="{f}: {v} outorgas">'
        f'<div class="cc-b" style="height:{100 * v / vmax:.2f}%;background:{cor};"></div>'
        f'<div class="cc-v" style="bottom:calc({100 * v / vmax:.2f}% + 8px);">{v:,}</div></div>'.replace(",", ".")
        for f, v, _, cor in _FAIXAS
    )
    eixo = "".join(f"<div><b>{f}</b><span>{sol}</span></div>" for f, _, sol, _ in _FAIXAS)
    return f"""
      <div class="cc">
        <div class="cc-plot">{grade}{cols}</div>
        <div class="cc-x">{eixo}</div>
        <div class="cc-g">
          <div style="grid-column:span 2; border-color:#16A34A;"><strong>Grupo A</strong> · menor risco<br/>monitoramento e <strong>sorteio auditável</strong> · 431</div>
          <div style="grid-column:span 2; border-color:#1D4ED8;"><strong>Grupo B</strong> · intermediário<br/>ação <strong>remota</strong> · 1.408</div>
          <div style="grid-column:span 4; border-color:#B91C1C;"><strong>Grupo C</strong> · maior risco<br/>ação <strong>presencial</strong>, até intervenção técnica com possível cautelar · 587</div>
        </div>
      </div>"""


# ---------------------------------------------------------------------------
# 03 — Do risco à solução fiscal
# ---------------------------------------------------------------------------
slide(
    3,
    "Grupo de risco — do risco à ação fiscal",
    "Fiscalização Responsiva · PPF 2025-2028",
    "Do risco à ação fiscal",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-5 flex flex-col gap-3">
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(24px * var(--tz));">Índice de Perfil de Risco (IPR)</p>
        <p class="text-blue-100 text-lg mt-1">Cada outorga recebe uma <strong>nota de 0 a 100</strong> e uma
        <strong>faixa de A1 a C4</strong>. A intensidade da ação fiscal é proporcional ao risco — é o modelo
        de Fiscalização Responsiva do PPF 2025-2028.</p>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-file-signature text-accent text-2xl"></i></div>
        <div><p class="card-t">A unidade é a outorga, não a empresa</p>
        <p class="card-d">Uma EBN com quatro linhas de travessia tem quatro IPRs: o risco de uma travessia no
        Oiapoque não é o de outra em Manaus.</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-scale-balanced text-accent text-2xl"></i></div>
        <div><p class="card-t">A nota mistura duas coisas</p>
        <p class="card-d"><strong>O que a empresa já fez</strong> (autuações, reincidência, NoCI descumprida, denúncias
        que viraram sanção) e <strong>o que ela é</strong> (risco da atividade, porte, acesso, maturidade e há quanto
        tempo ninguém a visita).</p></div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-user-check text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">O índice prioriza; a chefia decide</p>
        <p class="card-d">O IPR indica a ordem, sem substituir o juízo técnico: toda inclusão ou exclusão fora da regra
        fica registrada, com autor e fundamento.</p></div>
      </div>
    </div>

    <div class="col-span-7 flex flex-col gap-3">
      <div>
        <p class="titulo-sec">Outorgas por faixa e a solução fiscal de cada uma</p>
        <p class="sub-sec">2.426 outorgas ativas no ciclo 2027 (2.466 do universo, menos 40 com CNPJ baixado ou suspenso)</p>
      </div>
      {_colunas_faixa()}
      <p class="legenda">A correspondência faixa &rarr; solução fiscal é parametrizada e versionada, não fixada em programa.
      A navegação marítima é documental em qualquer faixa (61 outorgas do Grupo C).</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {NTM}, Quadro 2.</p>
""",
    extra_css="""
.cc { display:flex; flex-direction:column; flex:1; }
.cc-plot { position:relative; flex:1; min-height:calc(240px * var(--tz)); display:grid; grid-template-columns:repeat(8,1fr); column-gap:16px; align-items:stretch; border-bottom:2px solid #94A3B8; padding:0 6px; }
.cc-grid { position:absolute; left:0; right:0; border-top:1px dashed #E2E8F0; }
.cc-col { position:relative; z-index:1; }
.cc-v { position:absolute; left:-8px; right:-8px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; color:#0F172A; font-size:calc(22px * var(--tz)); line-height:1; }
.cc-b { position:absolute; left:0; right:0; bottom:0; border-radius:6px 6px 0 0; }
.cc-x { display:grid; grid-template-columns:repeat(8,1fr); column-gap:16px; padding:8px 6px 0; }
.cc-x div { text-align:center; line-height:1.2; }
.cc-x b { display:block; font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(19px * var(--tz)); }
.cc-x span { color:#64748B; font-size:calc(13.5px * var(--tz)); }
.cc-g { display:grid; grid-template-columns:repeat(8,1fr); column-gap:16px; padding:10px 6px 0; }
.cc-g div { border-top:4px solid; padding-top:6px; text-align:center; color:#475569; font-size:calc(15px * var(--tz)); line-height:1.3; }
.cc-g strong { color:#003366; font-family:'Montserrat',sans-serif; }
""",
    tag=TAG_RISCO,
    base=1.45,
)

# ---------------------------------------------------------------------------
# 05 — O que entra no PAF 2027
# ---------------------------------------------------------------------------
slide(
    5,
    "Grupo de risco — composição do PAF 2027",
    "Composição · regra por grupo, não número fixo",
    "O que entra no PAF 2027",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-7 flex flex-col gap-3">
      <div class="comp comp-c">
        <div class="comp-n">587</div>
        <div><p class="card-t"><span class="pill pill-c">Grupo C</span> &nbsp;entra inteiro</p>
        <p class="card-d">As outorgas de maior risco. Fiscalizá-las é obrigação do modelo, não escolha de escopo: o Grupo C é o <strong>piso</strong> do plano.</p></div>
      </div>
      <div class="comp comp-b">
        <div class="comp-n">52</div>
        <div><p class="card-t"><span class="pill pill-b">Grupo B</span> &nbsp;entra na medida do que cabe</p>
        <p class="card-d">Das 1.408, as primeiras do ranking até o limite da força de trabalho. Ordem estrita: não se pula uma outorga de maior risco para incluir outra que caberia.</p></div>
      </div>
      <div class="comp comp-a">
        <div class="comp-n">&asymp;30</div>
        <div><p class="card-t"><span class="pill pill-a">Grupo A</span> &nbsp;entra por sorteio</p>
        <p class="card-d">Fração das 431 de menor risco — 10%, 7% ou 5% conforme o risco da atividade — para que ninguém fique fora do radar.</p></div>
      </div>
      <div class="destaque flex items-center gap-6">
        <p class="font-montserrat font-black" style="font-size:calc(54px * var(--tz)); line-height:1;">&asymp;669</p>
        <p class="text-blue-100 text-lg">outorgas e <strong>45.880 horas</strong>. Substitui o recorte informal de <strong>200 outorgas</strong> dos ciclos anteriores —
        inferior ao próprio Grupo C, que sozinho tem quase o triplo.</p>
      </div>
    </div>

    <div class="col-span-5 flex flex-col gap-3">
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-id-card text-accent text-2xl"></i></div>
        <div><p class="card-t">Todo CNPJ conferido na Receita Federal</p>
        <p class="card-d">49 outorgas com CNPJ baixado ou suspenso: <strong>40 saíram da lista</strong> e 9 ficaram por decisão
        fundamentada (sucessão já reconhecida). Nenhum bloqueio sem tratamento. Sair da lista não é sair do universo:
        a área de outorgas recebe o dossiê do CNPJ para decidir sobre o instrumento.</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-dice text-accent text-2xl"></i></div>
        <div><p class="card-t">Sorteio que qualquer um pode refazer</p>
        <p class="card-d">A Agência publica a lista de elegíveis e a sua impressão digital <strong>antes</strong> de conhecer
        a semente — um pulso futuro do <strong>NIST Randomness Beacon</strong>. Mesma lista + mesma semente = mesmas sorteadas.</p></div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-circle-check text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">Sorteio feito na extração oficial de 02/10</p>
        <p class="card-d">Junto com os demais dados do PAF, no encerramento da consulta às Unidades Regionais: a Diretoria recebe o plano já com a lista nominal do Grupo A.</p></div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Protocolos IPR-CADASTRO-V1 e IPR-SORTEIO-V1. Fonte: {NTM}, itens 3.2, 3.4 e 5.</p>
""",
    extra_css="""
.comp { display:flex; align-items:center; gap:22px; border-radius:14px; padding:12px 20px; border:1px solid; }
.comp p { margin:0; }
.comp-n { min-width:120px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(46px * var(--tz)); line-height:1; color:#003366; }
.comp-c { background:#FEF2F2; border-color:#FECACA; }
.comp-b { background:#EFF6FF; border-color:#BFDBFE; }
.comp-a { background:#F0FDF4; border-color:#BBF7D0; }
""",
    tag=TAG_RISCO,
    base=1.61,
)

# ---------------------------------------------------------------------------
# 06 — O plano cabe em quem o executa
# ---------------------------------------------------------------------------
def _ocup(nome, antes, depois):
    cor = "#B91C1C" if antes > 130 else "#C2410C"
    w_antes = min(antes, 400) / 400 * 100
    w_dep = depois / 400 * 100
    return f"""
      <div class="oc-row">
        <div class="oc-rot"><strong>{nome}</strong></div>
        <div class="oc-trk">
          <div class="oc-lim"></div>
          <div class="oc-bar" style="width:{w_antes:.1f}%; background:{cor}; opacity:0.28;"></div>
          <div class="oc-bar" style="width:{w_dep:.1f}%; background:#0066CC; top:9px; height:18px;"></div>
        </div>
        <div class="oc-val"><span style="color:{cor};">{antes}%</span> &rarr; <strong>{depois}%</strong></div>
      </div>"""

slide(
    6,
    "Grupo de risco — força de trabalho e equalização",
    "Força de trabalho · equalização entre unidades",
    "O plano cabe em quem o executa?",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-7 flex flex-col gap-3">
      <div class="formula" style="text-align:center; line-height:1.6;">
        ocupação = horas que o plano exige &divide; horas disponíveis para o PAF<br/>
        <span style="color:#94A3B8; font-size:calc(16px * var(--tz));">horas disponíveis = 35% de todas as horas do plano de trabalho no PGD, igual para toda unidade · inclui os 20 do CNU</span>
      </div>
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(22px * var(--tz));">Cabe na Agência, mas não cabe onde a carga está.</p>
        <p class="text-blue-100 text-lg mt-1">O plano exige <strong>45.880 h</strong> das <strong>55.560 h</strong> disponíveis: 83% no agregado nacional.
        Pela jurisdição, porém, quatro unidades passam do limite.</p>
      </div>
      <div>
        <p class="titulo-sec">Ocupação antes e depois da equalização</p>
        <div class="leg-row mt-1">
          <span><i class="sw" style="background:#B91C1C; opacity:0.28;"></i>pela jurisdição</span>
          <span><i class="sw" style="background:#0066CC;"></i>após a equalização aprovada</span>
          <span><i class="sw" style="background:#003366; width:3px;"></i>limite de 100%</span>
        </div>
      </div>
      {_ocup("URESN · Santana", 395, 96)}
      {_ocup("GREBL · Belém", 146, 100)}
      {_ocup("GREMN · Manaus", 123, 100)}
      {_ocup("UREPL", 105, 91)}
      <p class="legenda">Demais 10 unidades: de 23% a 88% antes; receptoras ficam entre 55% e 88% depois. Nenhuma receptora passa de 90%.</p>
    </div>

    <div class="col-span-5 flex flex-col gap-3">
      <div class="grid grid-cols-3 gap-3">
        <div class="stat-card"><p class="stat-num">30</p><p class="text-blue-200 text-sm font-semibold mt-2">movimentos<br/>(9.531 h)</p></div>
        <div class="stat-card"><p class="stat-num">8</p><p class="text-blue-200 text-sm font-semibold mt-2">transferências<br/>(765 h)</p></div>
        <div class="stat-card"><p class="stat-num">22</p><p class="text-blue-200 text-sm font-semibold mt-2">missões de apoio<br/>(7 campo · 15 remotas)</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-route text-accent text-2xl"></i></div>
        <div><p class="card-t">Oiapoque: uma ida só</p>
        <p class="card-d">56 travessias sob jurisdição de Santana: a <strong>URESL</strong> faz a vistoria e a <strong>GREST</strong> as fases de
        escritório (NT 2/2024 — só a Fase 2 exige ir ao local).</p></div>
      </div>
      <div class="card card-green">
        <div class="ico" style="background:#BBF7D0;"><i class="fas fa-magnifying-glass-chart text-green-700 text-2xl"></i></div>
        <div><p class="card-t">Por que 35% das horas</p>
        <p class="card-d">É o que as unidades de fato dedicaram ao PAF. Auditado nos planos de trabalho já executados no
        <strong>Hefesto</strong> (jan/2025 a jul/2026): a média nacional foi <strong>35,7%</strong>.</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-landmark text-accent text-2xl"></i></div>
        <div><p class="card-t">A jurisdição não muda</p>
        <p class="card-d">A equalização diz quem <strong>executa</strong> no ciclo, não quem <strong>responde</strong>. A regra propõe; cada movimento é aprovado com autor e fundamento.
        Os 30 foram aprovados em 29/09.</p></div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-users text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">O limite é de lotação no Norte</p>
        <p class="card-d">GREBL e GREMN ficam exatamente em 100%. A cobertura do Grupo B (52 de 1.408, <strong>3,7%</strong>) só cresce com reforço nessas unidades.</p></div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Protocolos IPR-DIMENSIONA-V1 e IPR-EQUALIZA-V1. Régua de 35%: painel IPR-PAF (decisão da GPF de 25/08/2026), média medida nos planos de trabalho do PGD. Fonte: {NTM}, itens 6 a 8 e Quadros 5 e 6.</p>
""",
    extra_css="""
.oc-row { display:grid; grid-template-columns:230px 1fr 170px; align-items:center; gap:14px; }
.oc-rot { color:#334155; font-size:calc(18px * var(--tz)); }
.oc-rot strong { color:#003366; }
.oc-trk { position:relative; height:36px; background:#F1F5F9; border-radius:4px; }
.oc-bar { position:absolute; left:0; top:0; height:36px; border-radius:0 4px 4px 0; }
.oc-lim { position:absolute; left:25%; top:-4px; bottom:-4px; width:3px; background:#003366; z-index:2; }
.oc-val { font-family:'Montserrat',sans-serif; font-size:calc(20px * var(--tz)); color:#003366; }
""",
    tag=TAG_RISCO,
    base=1.28,
)


# ===========================================================================
# TELAS NOVAS DO AGENDAS EM SINCRONIA
# Levam já a posição final no deck (fix=True), ao contrário das herdadas do
# deck do PAF ao DG, que são remapeadas por POSICAO no fim do arquivo.
# ===========================================================================
TAG_B1 = '<span class="bloco-tag bt-b1"><i class="fas fa-compass-drafting"></i> Bloco 1 · PPF 2025-2028</span>'
TAG_B2 = '<span class="bloco-tag bt-b2"><i class="fas fa-route"></i> Bloco 2 · Rito do PAF</span>'
TAG_B3 = '<span class="bloco-tag bt-b3"><i class="fas fa-link"></i> Bloco 3 · Conexões</span>'
TAG_B4 = '<span class="bloco-tag bt-b4"><i class="fas fa-rocket"></i> Bloco 4 · Projetos</span>'
TAG_CTX = '<span class="bloco-tag bt-geral"><i class="fas fa-compass"></i> Contexto</span>'

BASE_CSS += """
.bt-b1 { background:#DBEAFE; color:#1E3A8A; }
.bt-b2 { background:#FEE2E2; color:#991B1B; }
.bt-b3 { background:#EDE9FE; color:#5B21B6; }
.bt-b4 { background:#DCFCE7; color:#166534; }
.quem {
  display:inline-flex; align-items:center; gap:6px; border-radius:999px; padding:2px 11px;
  font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(12.5px * var(--tz));
  letter-spacing:0.04em; background:#EDE9FE; color:#5B21B6; white-space:nowrap;
}
"""

TRILHA = "Trilha Técnica da Fiscalização, Aula 8 — Planejamento e Inteligência (SFC/GPF, 2026)"
PROJ = "Projetos SFC 2026, apresentação à Diretoria Colegiada (ago/2026)"


def novo(n, *a, **k):
    slide(n, *a, **k)
    SLIDES[-1]["fix"] = True


# ---------------------------------------------------------------------------
# 02 — Roteiro
# ---------------------------------------------------------------------------
def _bloco(num, titulo, pergunta, itens, minutos, cor):
    lis = "".join(f"<li>{i}</li>" for i in itens)
    return f"""
      <div class="rt" style="--c:{cor};">
        <div class="rt-top"><span class="rt-n">{num}</span><span class="rt-min"><i class="far fa-clock"></i> {minutos}</span></div>
        <p class="rt-t">{titulo}</p>
        <p class="rt-q">{pergunta}</p>
        <ul class="rt-l">{lis}</ul>
      </div>"""


novo(
    2,
    "Roteiro — Agendas em Sincronia",
    "Agendas em Sincronia · 13 de outubro de 2026",
    "O que vamos conversar",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-7">
    <p class="rt-lead">Quatro blocos: a <strong>agenda da fiscalização</strong>, o <strong>rito do PAF</strong>, a <strong>conexão com as outras agendas</strong>
    e os <strong>projetos e melhorias</strong> que podemos encaminhar juntos.</p>
    <div class="flex-1 grid grid-cols-4 gap-5">
      {_bloco("01", "A agenda da fiscalização", "Como a SFC decide o que fiscalizar?",
              ["Premissas do PPF 2025-2028", "Fiscalização Responsiva", "Fiscalização em 3 Níveis", "Grupos Especializados (GEF)"],
              "10 min", "#1E3A8A")}
      {_bloco("02", "O rito do PAF", "Quem faz o quê, e como o plano anual é montado?",
              ["Do Regimento à Diretoria Colegiada", "PAF 2027 em duas frentes", "O que entra no plano", "O plano cabe na equipe?"],
              "12 min", "#991B1B")}
      {_bloco("03", "Conexão com as outras agendas", "O que a fiscalização recebe das agendas, e o que devolve?",
              ["99 contribuições da Agenda Regulatória", "Confronto com a Agenda de Estudos", "Temáticas de 2027", "Mapa de conexões"],
              "15 min", "#5B21B6")}
      {_bloco("04", "Projetos e melhorias", "O que está em curso, e o que dá para fazer junto?",
              ["Normas, sistemas e capacitação", "SisPAT e SAI", "Seis propostas de melhoria"],
              "13 min", "#166534")}
    </div>
    <div class="destaque flex items-center gap-6">
      <i class="fas fa-comments text-3xl" style="color:#FFD700;"></i>
      <p class="text-lg" style="margin:0;">Cerca de <strong>50 minutos de exposição</strong> e <strong style="color:#FFD700;">10 minutos de conversa</strong>
      no fim, sobre as propostas do Bloco 4.</p>
    </div>
  </div>
""",
    extra_css="""
.rt-lead { margin:0; color:#475569; font-size:calc(19px * var(--tz)); line-height:1.45; }
.rt-lead strong { color:#003366; }
.rt { border:1px solid #E2E8F0; border-top:8px solid var(--c); border-radius:16px; padding:18px 22px;
      display:flex; flex-direction:column; gap:10px; background:#fff; }
.rt p { margin:0; }
.rt-top { display:flex; justify-content:space-between; align-items:center; }
.rt-n { font-family:'Montserrat',sans-serif; font-weight:900; color:var(--c); font-size:calc(46px * var(--tz)); line-height:1; }
.rt-min { font-family:'Montserrat',sans-serif; font-weight:700; color:#64748B; font-size:calc(15px * var(--tz));
          background:#F1F5F9; border-radius:999px; padding:3px 12px; }
.rt-t { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(23px * var(--tz)); line-height:1.2; }
.rt-q { color:#64748B; font-style:italic; font-size:calc(16px * var(--tz)); line-height:1.4; }
.rt-l { margin:4px 0 0; padding:0; list-style:none; display:flex; flex-direction:column; gap:8px; }
.rt-l li { position:relative; padding-left:22px; color:#334155; font-size:calc(17px * var(--tz)); line-height:1.35; }
.rt-l li::before { content:''; position:absolute; left:2px; top:calc(8px * var(--tz)); width:10px; height:10px; border-radius:2px; background:var(--c); }
""",
    tag=TAG_CTX,
    base=1.81,
)

# ---------------------------------------------------------------------------
# 03 — Onde a fiscalização entra no planejamento
# ---------------------------------------------------------------------------
def _inst(nome, quem, nota="", foco=False):
    cls = "inst foco" if foco else "inst"
    nota_html = f'<span class="inst-n">{nota}</span>' if nota else ""
    return f'<div class="{cls}"><p class="inst-t">{nome}</p><p class="inst-q">{quem}</p>{nota_html}</div>'


novo(
    3,
    "Onde a fiscalização entra no planejamento",
    "Instrumentos de planejamento da ANTAQ",
    "Onde a fiscalização entra",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-8 flex flex-col gap-3 nivs">
      <div class="niv">
        <div class="niv-r" style="background:#003366;"><i class="fas fa-chess-king"></i><span>Estratégico</span></div>
        <div class="niv-c grid grid-cols-2 gap-3">
          {_inst("PEI 2025-2028", "SGE · aprovado pela Diretoria", "RI, art. 11, XIV")}
          {_inst("Plano de Gestão Anual (PGA)", "SGE · desdobramento anual do PEI")}
        </div>
      </div>
      <div class="niv">
        <div class="niv-r" style="background:#0066CC;"><i class="fas fa-chess-knight"></i><span>Tático</span></div>
        <div class="niv-c grid grid-cols-3 gap-3">
          {_inst("Agenda Regulatória", "SRG", "RI, art. 11, XVI")}
          {_inst("Agenda Plurianual de Estudos", "SEPH", "RI, art. 11, XVI")}
          {_inst("Agenda Ambiental e de Segurança Aquaviária", "SESGI", "RI, art. 11, XVI")}
          {_inst("PDTIC", "SGE", "RI, art. 11, XV")}
          {_inst("PPF 2025-2028", "SFC · Plano Plurianual de Fiscalização", "RI, art. 11, X", foco=True)}
          {_inst("PDP, PCA e Plano de Integridade", "demais instrumentos táticos")}
        </div>
      </div>
      <div class="niv">
        <div class="niv-r" style="background:#64748B;"><i class="fas fa-chess-pawn"></i><span>Operacional</span></div>
        <div class="niv-c grid grid-cols-2 gap-3">
          {_inst("PAF · Plano Anual de Fiscalização", "SFC · o que fiscalizar no ano", "RI, art. 11, X", foco=True)}
          {_inst("Planos de trabalho do PGD", "todas as unidades · entregas e horas")}
        </div>
      </div>
    </div>

    <div class="col-span-4 flex flex-col gap-4">
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(21px * var(--tz)); margin:0;">O Plano de Fiscalização também é uma agenda</p>
        <p class="text-blue-100 text-lg mt-2" style="margin-bottom:0;">Aprovado pela Diretoria Colegiada, como as demais. O PPF fixa o
        modelo para quatro anos; o PAF diz, a cada ano, <strong style="color:#FFD700;">quem, o quê e com que intensidade</strong> fiscalizar.</p>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-arrow-down text-accent text-2xl"></i></div>
        <div><p class="card-t">As agendas orientam a fiscalização</p>
        <p class="card-d">Norma nova, estudo em curso e meta institucional mudam o que vale a pena verificar em campo.</p></div>
      </div>
      <div class="card card-green">
        <div class="ico" style="background:#BBF7D0;"><i class="fas fa-arrow-up text-green-700 text-2xl"></i></div>
        <div><p class="card-t">A fiscalização devolve evidência</p>
        <p class="card-d">O que se vê em campo mostra se a norma funciona, onde falta estudo e onde falta dado.</p></div>
      </div>
      <p class="legenda" style="margin:0;">Sincronizar é fazer as duas setas girarem no mesmo calendário.</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Níveis conforme o Guia do Workshop de Planejamento ANTAQ 2026 (SGE/GGGP), item 4; o PPF e o PAF foram posicionados pela SFC. Regimento Interno da ANTAQ, art. 11.</p>
""",
    extra_css="""
.nivs { justify-content:center; }
.niv { display:grid; grid-template-columns:220px 1fr; gap:14px; align-items:stretch; }
.niv-r { border-radius:14px; color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px;
         font-family:'Montserrat',sans-serif; font-weight:900; text-transform:uppercase; letter-spacing:0.04em; font-size:calc(13px * var(--tz)); padding:0 8px; text-align:center; }
.niv-r i { font-size:calc(28px * var(--tz)); opacity:0.85; }
.inst { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:10px 14px; display:flex; flex-direction:column; gap:2px; }
.inst p { margin:0; }
.inst-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(17px * var(--tz)); line-height:1.25; }
.inst-q { color:#64748B; font-size:calc(14px * var(--tz)); line-height:1.3; }
.inst-n { color:#94A3B8; font-size:calc(12px * var(--tz)); }
.inst.foco { background:#FEF9C3; border:2px solid #EAB308; }
.inst.foco .inst-t { color:#713F12; }
""",
    tag=TAG_CTX,
    base=1.55,
)

# ---------------------------------------------------------------------------
# 05 — PPF 2025-2028: premissas e enfoques (Trilha Técnica, aula 8, telas 5 e 8)
# ---------------------------------------------------------------------------
def _premissa(n, t, d):
    return (f'<div class="pr"><span class="pr-n">{n}</span><div><p class="pr-t">{t}</p>'
            f'<p class="pr-d">{d}</p></div></div>')


def _enfoque(ic, cor, t, enf, pergunta, d):
    return f"""
      <div class="enf" style="--c:{cor};">
        <div class="enf-ic"><i class="fas {ic}"></i></div>
        <div class="enf-b">
          <p class="enf-k">{enf}</p>
          <p class="enf-t">{t}</p>
          <p class="enf-q">{pergunta}</p>
          <p class="enf-d">{d}</p>
        </div>
      </div>"""


novo(
    5,
    "PPF 2025-2028 — premissas e enfoques",
    "Plano Plurianual de Fiscalização 2025-2028",
    "Cinco premissas, três enfoques",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-8">
    <div class="col-span-5 flex flex-col gap-3">
      <p class="titulo-sec">Premissas basilares</p>
      {_premissa("01", "Redução de custos de fiscalização", "Métodos mais simples e menos onerosos para a Agência e para o regulado.")}
      {_premissa("02", "Promoção da conformidade normativa", "Ação preventiva, que detecta a infração cedo.")}
      {_premissa("03", "Integração de soluções tecnológicas", "Monitoramento automatizado e cruzamento de dados.")}
      {_premissa("04", "Foco no risco e proporcionalidade", "A intensidade da ação acompanha o risco identificado.")}
      {_premissa("05", "Transparência e governança", "Execução fiscalizatória visível e auditável.")}
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <p class="titulo-sec">Três enfoques complementares</p>
      {_enfoque("fa-gauge-high", "#B91C1C", "Fiscalização Responsiva", "Enfoque no mercado regulado",
                "Quem fiscalizar, e com que intensidade?",
                "Cada outorga recebe uma nota de risco; a intensidade da ação é proporcional a ela.")}
      {_enfoque("fa-layer-group", "#0066CC", "Fiscalização em 3 Níveis", "Enfoque nos normativos",
                "Como verificar cada obrigação?",
                "Cada dispositivo é classificado em monitoramento, ação à distância ou ação presencial.")}
      {_enfoque("fa-users-gear", "#15803D", "Grupos Especializados (GEF)", "Enfoque nas equipes",
                "Quem executa os temas mais complexos?",
                "Equipes dedicadas a áreas específicas, com conhecimento aprofundado.")}
      <div class="destaque">
        <p class="text-lg" style="margin:0;">Os três se encontram no PAF: <strong style="color:#FFD700;">o risco escolhe o regulado</strong>,
        o nível escolhe o meio de verificar e o GEF dá a profundidade.</p>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: PPF 2025-2028; {TRILHA}, telas 5 e 8.</p>
""",
    extra_css="""
.pr { display:flex; gap:16px; align-items:flex-start; background:#F8FAFC; border-radius:14px; padding:14px 18px; border-left:5px solid #0066CC; }
.pr p { margin:0; }
.pr-n { font-family:'Montserrat',sans-serif; font-weight:900; color:#0066CC; font-size:calc(26px * var(--tz)); line-height:1; min-width:40px; }
.pr-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(19px * var(--tz)); line-height:1.25; }
.pr-d { color:#64748B; font-size:calc(15.5px * var(--tz)); line-height:1.4; margin-top:2px !important; }
.enf { display:flex; gap:18px; align-items:stretch; border:1px solid #E2E8F0; border-radius:16px; overflow:hidden; }
.enf-ic { width:96px; flex-shrink:0; background:var(--c); color:#fff; display:flex; align-items:center; justify-content:center; font-size:calc(36px * var(--tz)); }
.enf-b { padding:12px 18px 12px 0; display:flex; flex-direction:column; gap:2px; }
.enf-b p { margin:0; }
.enf-k { font-family:'Montserrat',sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:var(--c); font-size:calc(12.5px * var(--tz)); }
.enf-t { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(23px * var(--tz)); line-height:1.2; }
.enf-q { font-style:italic; color:#334155; font-size:calc(17px * var(--tz)); }
.enf-d { color:#64748B; font-size:calc(15.5px * var(--tz)); line-height:1.4; }
""",
    tag=TAG_B1,
    base=1.57,
)

# ---------------------------------------------------------------------------
# 07 — Fiscalização em 3 Níveis (Trilha, telas 13 e 14; NT de arquitetura da F3N)
# ---------------------------------------------------------------------------
def _nivel(n, t, d, cor, ic):
    return f"""
      <div class="nv" style="--c:{cor};">
        <div class="nv-top"><span class="nv-n">Nível {n}</span><i class="fas {ic}"></i></div>
        <p class="nv-t">{t}</p>
        <p class="nv-d">{d}</p>
      </div>"""


def _passo(quando, txt, estado=""):
    return f'<div class="ps {estado}"><b>{quando}</b><span>{txt}</span></div>'


novo(
    7,
    "Fiscalização em 3 Níveis",
    "Enfoque nos normativos · PPF 2025-2028",
    "Fiscalização em 3 Níveis",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-8">
    <div class="col-span-7 flex flex-col gap-4">
      <p class="lead3">Cada <strong>obrigação</strong> das normas e dos contratos é classificada pelo meio mais barato que ainda permite verificá-la.</p>
      <div class="grid grid-cols-3 gap-4">
        {_nivel(1, "Monitoramento", "Sistemas automatizados identificam possíveis infrações em tempo real, por cruzamento de dados.", "#15803D", "fa-satellite-dish")}
        {_nivel(2, "Ação à distância", "Análise documental, evidência audiovisual ou inspeção remota assistida, sem deslocamento.", "#0066CC", "fa-laptop")}
        {_nivel(3, "Ação presencial", "Inspeção e coleta de evidência in loco, dirigida aos pontos de maior risco e complexidade.", "#B91C1C", "fa-person-hiking")}
      </div>
      <div class="prog"><span>menor custo · maior escala</span><span>maior custo · maior precisão</span></div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-ranking-star text-accent text-2xl"></i></div>
        <div><p class="card-t">Três eixos priorizam cada obrigação</p>
        <p class="card-d"><strong>Probabilidade</strong> de descumprimento × <strong>impacto</strong> sobre usuários, meio ambiente e concorrência ×
        <strong>custo</strong> de verificação. Nem toda infração prevista na norma é verificada presencialmente.</p></div>
      </div>
    </div>

    <div class="col-span-5 flex flex-col gap-3">
      <p class="titulo-sec">Onde estamos</p>
      <div class="pss">
        {_passo("2023", "Processo nº 50300.012639/2023-26 abre o mapeamento de níveis de fiscalização.", "feito")}
        {_passo("Abr/2026", "Nota Técnica da GPF fixa a arquitetura: método ANTT/ANEEL adaptado, classificação dispositivo a dispositivo das Resoluções.", "feito")}
        {_passo("2026", "Primeira aplicação: Res. ANTAQ nº 65/2021, produtos perigosos em instalações portuárias (a atividade de maior risco, IRA 81).", "agora")}
        {_passo("Próximo", "Lacunas de Nível 1 viram demanda do PDTIC; integração com Estatístico Aquaviário, SisPAT e Sistema de Desempenho Portuário.")}
      </div>
      <div class="destaque">
        <p class="text-lg" style="margin:0;">O Nível 1 depende de <strong style="color:#FFD700;">dado que já existe em outras áreas</strong>.
        É aqui que a fiscalização mais precisa das outras agendas.</p>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {TRILHA}, telas 13 e 14; Nota Técnica de arquitetura da Fiscalização em 3 Níveis (GPF/SFC, abr/2026) e nota de aplicação à Res. nº 65/2021, em elaboração. IRA: Indicador de Risco da Atividade.</p>
""",
    extra_css="""
.lead3 { margin:0; color:#475569; font-size:calc(20px * var(--tz)); line-height:1.4; }
.lead3 strong { color:#003366; }
.nv { border-radius:16px; border:1px solid #E2E8F0; border-top:8px solid var(--c); padding:16px 18px; display:flex; flex-direction:column; gap:6px; }
.nv p { margin:0; }
.nv-top { display:flex; justify-content:space-between; align-items:center; color:var(--c); }
.nv-top i { font-size:calc(26px * var(--tz)); }
.nv-n { font-family:'Montserrat',sans-serif; font-weight:900; text-transform:uppercase; letter-spacing:0.08em; font-size:calc(14px * var(--tz)); }
.nv-t { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(23px * var(--tz)); line-height:1.15; }
.nv-d { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.45; }
.prog { display:flex; justify-content:space-between; color:#fff; border-radius:999px; padding:6px 18px;
        background:linear-gradient(90deg,#15803D,#0066CC,#B91C1C); font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(14px * var(--tz)); }
.pss { display:flex; flex-direction:column; gap:10px; }
.ps { display:grid; grid-template-columns:120px 1fr; gap:14px; align-items:baseline; border-left:5px solid #CBD5E1; padding:6px 0 6px 14px; }
.ps b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(18px * var(--tz)); }
.ps span { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.4; }
.ps.feito { border-left-color:#0066CC; }
.ps.agora { border-left-color:#FFD700; background:#FFFBEB; border-radius:0 10px 10px 0; }
""",
    tag=TAG_B1,
    base=1.76,
)

# ---------------------------------------------------------------------------
# 08 — Grupos Especializados de Fiscalização (Trilha, telas 16 e 17; Projetos SFC 2026)
# ---------------------------------------------------------------------------
novo(
    8,
    "Grupos Especializados de Fiscalização (GEF)",
    "Enfoque nas equipes · PPF 2025-2028",
    "Grupos especializados (GEF)",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-8">
    <div class="col-span-5 flex flex-col gap-4">
      <p class="lead3">Equipes dedicadas a temas estratégicos, com conhecimento aprofundado: execução mais precisa, <strong>menos erro e menos retrabalho</strong>.</p>
      <div class="areas">
        <div class="area on"><i class="fas fa-building-columns"></i><span>Investimentos portuários</span><em>ativo</em></div>
        <div class="area on"><i class="fas fa-boxes-stacked"></i><span>Logística de contêineres</span><em>ativo</em></div>
        <div class="area"><i class="fas fa-people-line"></i><span>Transporte de passageiros</span><em>área prevista</em></div>
        <div class="area"><i class="fas fa-radiation"></i><span>Cargas perigosas</span><em>área prevista</em></div>
      </div>
      <p class="titulo-sec">O que a especialização entrega</p>
      <div class="ben">
        <span><i class="fas fa-shield-halved"></i> Autonomia e confiança</span>
        <span><i class="fas fa-coins"></i> Menos custo com retrabalho</span>
        <span><i class="fas fa-seedling"></i> Crescimento profissional</span>
        <span><i class="fas fa-face-smile"></i> Satisfação e saúde no trabalho</span>
      </div>
    </div>

    <div class="col-span-7 flex flex-col gap-4">
      <div class="gef">
        <div class="gef-top" style="background:linear-gradient(135deg,#7C2D12,#C2410C);"><i class="fas fa-boxes-stacked"></i> GEF Contêineres</div>
        <div class="gef-b">
          <p class="gef-d">Apura as reclamações de cobrança na cadeia de contêineres e conduz o rito de autocomposição da Portaria SFC nº 1/2026; o ProTEU, sistema do rito, está em prototipação.</p>
          <div class="grid grid-cols-3 gap-3">
            <div class="kpi"><b>386</b><span>processos em 2025, ~237 com acordo</span></div>
            <div class="kpi"><b>R$ 25 mi</b><span>em cobranças canceladas (2025)</span></div>
            <div class="kpi"><b>350</b><span>NACs em 2026: 50 com acordo, 270 em andamento</span></div>
          </div>
        </div>
      </div>
      <div class="gef">
        <div class="gef-top" style="background:linear-gradient(135deg,#003366,#0066CC);"><i class="fas fa-building-columns"></i> GEF Investimentos</div>
        <div class="gef-b">
          <p class="gef-d">Criado em 2024 para verificar os compromissos de investimento dos contratos de arrendamento e dos TUPs, agora com o SAI.</p>
          <div class="grid grid-cols-3 gap-3">
            <div class="kpi"><b>110</b><span>empreendimentos (54 TUPs, 56 arrendamentos)</span></div>
            <div class="kpi"><b>R$ 124,9 bi</b><span>de investimento previsto e atualizado</span></div>
            <div class="kpi"><b>81</b><span>empreendimentos fiscalizados em 2026</span></div>
          </div>
        </div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-link text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">Já conversa com a Agenda Regulatória</p>
        <p class="card-d">A NT 27/2026 encaminha ao GEF Investimentos duas matérias vindas da consulta da Agenda Regulatória:
        investimentos das Autoridades Portuárias pactuados em revisão tarifária e sua efetividade no serviço.</p></div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {TRILHA}, telas 16 e 17; {PROJ}, telas 3 e 10 (carteira do GEF Investimentos em base ago/2025); NT nº 27/2026/GPF/SFC, item 8.2, VII.</p>
""",
    extra_css="""
.lead3 { margin:0; color:#475569; font-size:calc(20px * var(--tz)); line-height:1.4; }
.lead3 strong { color:#003366; }
.areas { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.area { display:flex; align-items:center; gap:10px; border:1px dashed #CBD5E1; border-radius:12px; padding:10px 14px; color:#64748B; font-size:calc(16px * var(--tz)); flex-wrap:wrap; }
.area i { font-size:calc(20px * var(--tz)); }
.area em { font-style:normal; margin-left:auto; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(12px * var(--tz)); text-transform:uppercase; letter-spacing:0.06em; }
.area.on { border:1px solid #93C5FD; background:#EFF6FF; color:#003366; }
.area.on i, .area.on em { color:#0066CC; }
.ben { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.ben span { background:#F0FDF4; border-radius:12px; padding:10px 14px; color:#166534; font-size:calc(16px * var(--tz)); display:flex; gap:10px; align-items:center; }
.gef { border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; }
.gef-top { color:#fff; padding:12px 22px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(22px * var(--tz)); display:flex; gap:12px; align-items:center; }
.gef-b { padding:14px 22px; display:flex; flex-direction:column; gap:12px; }
.gef-b p { margin:0; }
.gef-d { color:#475569; font-size:calc(16.5px * var(--tz)); line-height:1.45; }
.kpi { background:#F8FAFC; border-radius:12px; padding:10px 14px; display:flex; flex-direction:column; }
.kpi b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(28px * var(--tz)); line-height:1.1; }
.kpi span { color:#64748B; font-size:calc(14px * var(--tz)); line-height:1.3; }
""",
    tag=TAG_B1,
    base=1.50,
)

# ---------------------------------------------------------------------------
# 10 — O rito do PAF: quem faz o quê
# ---------------------------------------------------------------------------
def _rito(n, quem, t, base_legal, cor="#003366"):
    return f"""
      <div class="ri" style="--c:{cor};">
        <span class="ri-n">{n}</span>
        <p class="ri-q">{quem}</p>
        <p class="ri-t">{t}</p>
        <p class="ri-b">{base_legal}</p>
      </div>"""


novo(
    10,
    "O rito do PAF — quem faz o quê",
    "Plano Anual de Fiscalização · Regimento Interno",
    "O rito do PAF: quem faz o quê",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-5">
    <div class="grid grid-cols-6 gap-4 ritos">
      {_rito("1", "GPF", "Propõe as diretrizes e o plano", "RI, art. 80, III, &ldquo;a&rdquo;, e VI")}
      {_rito("2", "Gerências e Unidades Regionais", "Apoiam a elaboração: consulta técnica", "RI, art. 84, IX, &ldquo;a&rdquo;")}
      {_rito("3", "GCOR", "Consolida e equaliza a carga entre unidades", "RI, art. 78, II e V")}
      {_rito("4", "SFC", "Consolida e submete à Diretoria", "RI, art. 76, VIII")}
      {_rito("5", "Diretoria Colegiada", "Aprova o Plano de Fiscalização", "RI, art. 11, X", "#92400E")}
      {_rito("6", "Toda a SFC", "Executa e mede: EPAF mensal, meta &ge; 90%", "PAF 2025: 96% executado", "#15803D")}
    </div>

    <div class="flex-1 grid grid-cols-12 gap-6">
      <div class="col-span-6 flex flex-col gap-3">
        <p class="titulo-sec">Quatro tipos de fiscalização no PAF</p>
        <div class="tipos">
          <div><i class="fas fa-gauge-high" style="color:#B91C1C;"></i><p><strong>Grupo de risco</strong><br/>o núcleo do plano: a nota de risco escolhe a outorga e a intensidade</p></div>
          <div><i class="fas fa-layer-group" style="color:#0066CC;"></i><p><strong>Temáticas</strong><br/>um problema do setor, examinado em vários regulados ao mesmo tempo</p></div>
          <div><i class="fas fa-screwdriver-wrench" style="color:#15803D;"></i><p><strong>Operacionais</strong><br/>dirigidas a um problema regulatório conhecido, e não a um agente</p></div>
          <div><i class="fas fa-file-contract" style="color:#7C3AED;"></i><p><strong>Rito próprio</strong><br/>novas outorgas, embarcações em construção, investimentos, concessões</p></div>
        </div>
      </div>
      <div class="col-span-6 flex flex-col gap-3">
        <p class="titulo-sec">Onde as outras áreas já entram</p>
        <div class="card">
          <div class="ico" style="background:#DBEAFE;"><i class="fas fa-gavel text-accent text-2xl"></i></div>
          <div><p class="card-t">Deliberação-DG nº 96/2025</p>
          <p class="card-d">Discutir a proposta do PAF com as unidades finalísticas e as Diretorias antes de submetê-la.</p></div>
        </div>
        <div class="card">
          <div class="ico" style="background:#DBEAFE;"><i class="fas fa-envelope-open-text text-accent text-2xl"></i></div>
          <div><p class="card-t">Ofício Circular nº 2/2026/SFC</p>
          <p class="card-d">Consulta à SRG, à SESGI, à SOG e à SEPH sobre temas a fiscalizar, encerrada em 17/08/2026.</p></div>
        </div>
        <div class="card card-green">
          <div class="ico" style="background:#BBF7D0;"><i class="fas fa-clock text-green-700 text-2xl"></i></div>
          <div><p class="card-t">PGD e planejamento</p>
          <p class="card-d">A capacidade da fiscalização é medida nos planos de trabalho do PGD, e a GCOR acompanha as metas do PGA (RI, art. 78, VI e VII).</p></div>
        </div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Regimento Interno da ANTAQ, arts. 11, 76, 78, 80 e 84. Tipos de fiscalização: {TRILHA}, tela 19. EPAF de 2025: {PROJ}. Ofício e Deliberação: NT nº 27/2026/GPF/SFC, item 2.</p>
""",
    extra_css="""
.ritos { position:relative; }
.ri { position:relative; background:#F8FAFC; border-radius:16px; border-top:7px solid var(--c); padding:14px 16px 12px; display:flex; flex-direction:column; gap:4px; }
.ri p { margin:0; }
.ri-n { position:absolute; top:10px; right:14px; font-family:'Montserrat',sans-serif; font-weight:900; color:#CBD5E1; font-size:calc(34px * var(--tz)); line-height:1; }
.ri-q { font-family:'Montserrat',sans-serif; font-weight:900; color:var(--c); font-size:calc(19px * var(--tz)); line-height:1.2; padding-right:30px; }
.ri-t { color:#334155; font-size:calc(16px * var(--tz)); line-height:1.4; }
.ri-b { color:#94A3B8; font-size:calc(13px * var(--tz)); margin-top:auto !important; padding-top:4px; }
.tipos { display:grid; grid-template-columns:1fr 1fr; gap:12px; flex:1; }
.tipos div { display:flex; gap:14px; align-items:flex-start; background:#F8FAFC; border-radius:14px; padding:14px 18px; }
.tipos i { font-size:calc(26px * var(--tz)); margin-top:4px; width:30px; text-align:center; }
.tipos p { margin:0; color:#64748B; font-size:calc(15.5px * var(--tz)); line-height:1.4; }
.tipos strong { color:#003366; font-family:'Montserrat',sans-serif; font-size:calc(18px * var(--tz)); }
""",
    tag=TAG_B2,
    base=1.53,
)

# ---------------------------------------------------------------------------
# 19 — Mapa de conexões: o que a fiscalização recebe e devolve
# ---------------------------------------------------------------------------
def _cx(ic, agenda, quem, recebe, devolve):
    return f"""
      <tr>
        <td><div class="cx-a"><i class="fas {ic}"></i><div><strong>{agenda}</strong><span class="quem">{quem}</span></div></div></td>
        <td>{recebe}</td>
        <td>{devolve}</td>
      </tr>"""


novo(
    19,
    "Mapa de conexões com as agendas",
    "Conexões · o que a fiscalização recebe e o que devolve",
    "Onde o PAF toca as outras agendas",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col justify-center">
    <table class="tbl cx">
      <thead><tr><th style="width:27%;">Agenda</th><th style="width:36%;"><i class="fas fa-arrow-down"></i> A fiscalização recebe</th><th><i class="fas fa-arrow-up"></i> A fiscalização devolve</th></tr></thead>
      <tbody>
      {_cx("fa-scale-balanced", "Agenda Regulatória e ciclo regulatório", "SRG",
           "Normas novas a implantar (Res. 135 e 138/2026) e as <strong>99 contribuições</strong> da revisão da Agenda, base das temáticas de 2027",
           "Evidência de campo para AIR e Avaliação de Resultado Regulatório; matérias sem método vão ao GT do <strong>tema 2.8</strong>")}
      {_cx("fa-book-open", "Agenda Plurianual de Estudos", "SEPH",
           "Diagnóstico setorial: <strong>24 dos 27 estudos</strong> alcançam as demandas da consulta",
           "Dado de campo para estudos em curso (P1, P14, P21); pauta para os que ficaram sem demanda (P11, P16, P20)")}
      {_cx("fa-leaf", "Agenda Ambiental e de Segurança Aquaviária", "SESGI · GMS",
           "Índice de Desempenho Ambiental e subsídios à fiscalização (RI, art. 54, V)",
           "Verificação em campo de <strong>resíduos de embarcações</strong>; método conjunto para riscos climáticos")}
      {_cx("fa-chart-column", "Estatística e desempenho", "SESGI · GEA",
           "Estatístico Aquaviário (alimenta o IPR) e Sistema de Desempenho Portuário",
           "Conferência da qualidade do dado informado à Agência, que ainda depende de método amostral")}
      {_cx("fa-sitemap", "PEI, PGA, PGD e PDTIC", "SGE",
           "Metas do PGA e as horas dos planos de trabalho do PGD: <strong>55.560 h</strong> disponíveis ao PAF 2027",
           "EPAF e indicadores de efetividade; demandas de <strong>Nível 1</strong> ao PDTIC; o limite de lotação no Norte")}
      {_cx("fa-file-signature", "Outorgas", "SOG",
           "Cadastro de outorgas: o universo de <strong>2.466</strong> avaliado pelo IPR",
           "Dossiê dos <strong>49 CNPJs</strong> baixados ou suspensos; afretamento e apoio marítimo, o maior bloco da consulta (18 demandas)")}
      </tbody>
    </table>
  </div>
  <p class="fonte px-16 pb-1">Fonte: NT nº 27/2026/GPF/SFC, itens 5 e 8.2; minuta da NT de Metodologia do PAF 2027, itens 3 e 6; NT do IPR 2.0 (Quadro de indicadores); Regimento Interno, art. 54.</p>
""",
    extra_css="""
table.cx td { vertical-align:middle; font-size:calc(16.5px * var(--tz)); line-height:1.4; padding:12px 14px; }
table.cx td strong { color:#003366; }
table.cx th { font-size:calc(14px * var(--tz)); }
.cx-a { display:flex; gap:14px; align-items:center; }
.cx-a i { color:#5B21B6; font-size:calc(24px * var(--tz)); width:32px; text-align:center; flex-shrink:0; }
.cx-a > div { display:flex; flex-direction:column; align-items:flex-start; gap:4px; }
.cx-a strong { font-family:'Montserrat',sans-serif; font-size:calc(17px * var(--tz)); line-height:1.25; }
""",
    tag=TAG_B3,
    base=1.71,
)

# ---------------------------------------------------------------------------
# 22 — Projetos em andamento
# ---------------------------------------------------------------------------
def _proj(ic, cor, nome, status, txt, quem):
    return f"""
      <div class="pj" style="--c:{cor};">
        <div class="pj-top"><i class="fas {ic}"></i><p class="pj-t">{nome}</p></div>
        <p class="pj-s">{status}</p>
        <p class="pj-d">{txt}</p>
        <p class="pj-q"><span class="quem">{quem}</span></p>
      </div>"""


novo(
    22,
    "Projetos em andamento na SFC",
    "Portfólio 2026 · com quem cada projeto conversa",
    "Projetos em andamento",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-3">
    <div class="pjg-r"><span><i class="fas fa-scale-balanced"></i> Normas</span></div>
    <div class="grid grid-cols-3 gap-4">
      {_proj("fa-gavel", "#B91C1C", "Res. ANTAQ nº 135/2026", "Vigência em 14/10/2026",
             "Novo marco da fiscalização, que revoga a Res. 3.259/2014. A SFC edita os atos complementares em até 90 dias.", "SRG · Agenda Regulatória")}
      {_proj("fa-ship", "#B91C1C", "Res. ANTAQ nº 138/2026", "Vigência em 15/02/2027",
             "Passageiros, misto e travessia na navegação interior: adequar procedimentos, sistemas e as Res. 75 e 13.", "SRG · Agenda Regulatória")}
      {_proj("fa-money-bill-wave", "#B91C1C", "Valores de multa", "Pendente",
             "Independe de AIR. Pela Res. 135/2026, o valor passa a definir a natureza da infração e a competência de julgamento.", "SRG · Diretoria")}
    </div>
    <div class="pjg-r"><span><i class="fas fa-laptop-code"></i> Sistemas e capacitação</span></div>
    <div class="grid grid-cols-3 gap-4">
      {_proj("fa-satellite-dish", "#0066CC", "Fiscalização Eletrônica (3 Níveis)", "Normas, sistema e implantação",
             "Monitoramento automatizado por cruzamento de dados da ANTAQ e de outros órgãos; implantação começa por 3 obrigações.", "SGE · PDTIC · SESGI")}
      {_proj("fa-boxes-stacked", "#0066CC", "ProTEU", "Em fase de prototipação",
             "Sistema para as denúncias e a autocomposição na cadeia de contêineres.", "SGE · TI")}
      {_proj("fa-chalkboard-user", "#15803D", "Enafis e Dia de Fiscal", "Dia de Fiscal: 21 e 22/10",
             "80 participantes no Enafis (Paranaguá, 21 a 25/09); o Dia de Fiscal leva a visão da fiscalização a servidores de outras áreas.", "Todas as áreas · PDP")}
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {PROJ}, telas 6 a 8 (status de ago/2026, com as datas definidas depois). SisPAT, SAI e SFIS Novo na tela seguinte.</p>
""",
    extra_css="""
.pjg-r { display:flex; align-items:center; gap:12px; }
.pjg-r span { font-family:'Montserrat',sans-serif; font-weight:900; text-transform:uppercase; letter-spacing:0.1em; color:#64748B; font-size:calc(14px * var(--tz)); display:flex; gap:8px; align-items:center; }
.pjg-r::after { content:''; flex:1; height:1px; background:#E2E8F0; }
.pj { border:1px solid #E2E8F0; border-left:6px solid var(--c); border-radius:14px; padding:12px 18px; display:flex; flex-direction:column; gap:5px; }
.pj p { margin:0; }
.pj-top { display:flex; gap:12px; align-items:center; }
.pj-top i { color:var(--c); font-size:calc(22px * var(--tz)); width:calc(30px * var(--tz)); flex-shrink:0; text-align:center; }
.pj-t { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(19px * var(--tz)); line-height:1.2; }
.pj-s { font-family:'Montserrat',sans-serif; font-weight:700; color:var(--c); font-size:calc(14.5px * var(--tz)); text-transform:uppercase; letter-spacing:0.05em; }
.pj-d { color:#475569; font-size:calc(15.5px * var(--tz)); line-height:1.42; }
.pj-q { margin-top:auto !important; padding-top:2px; }
""",
    tag=TAG_B4,
    base=1.77,
)

# ---------------------------------------------------------------------------
# 23 — SisPAT e SAI: dado estruturado que serve a outras agendas
# ---------------------------------------------------------------------------
novo(
    23,
    "SisPAT, SAI e SFIS Novo",
    "Sistemas da fiscalização · dado estruturado",
    "SisPAT e SAI",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-2 gap-8">
    <div class="sis">
      <div class="sis-top" style="background:linear-gradient(135deg,#003366,#0066CC);">
        <i class="fas fa-warehouse"></i>
        <div><p class="sis-k">Em operação desde abr/2026</p><p class="sis-t">SisPAT · Inventário de bens dos portos organizados</p></div>
      </div>
      <div class="sis-b">
        <div class="grid grid-cols-3 gap-3">
          <div class="stat-card"><p class="stat-num">161</p><p class="text-blue-200 text-sm font-semibold mt-2">empresas entregaram o inventário</p></div>
          <div class="stat-card"><p class="stat-num">90.985</p><p class="text-blue-200 text-sm font-semibold mt-2">bens, 100% georreferenciados</p></div>
          <div class="stat-card"><p class="stat-num">82.147</p><p class="text-blue-200 text-sm font-semibold mt-2">bens reversíveis mapeados</p></div>
        </div>
        <p class="sis-d">R$ 54,9 bi de valor justo declarado em <strong>29 portos organizados</strong> e 1.432 contratos. A SFC inicia a
        fiscalização de consistência dos inventários.</p>
        <p class="sis-x"><i class="fas fa-link"></i> Base para reversão e extinção contratual; atende à Res. 43/2021.</p>
      </div>
    </div>

    <div class="sis">
      <div class="sis-top" style="background:linear-gradient(135deg,#14532D,#15803D);">
        <i class="fas fa-helmet-safety"></i>
        <div><p class="sis-k">Workshop de lançamento em 17/09/2026</p><p class="sis-t">SAI · Acompanhamento de investimentos</p></div>
      </div>
      <div class="sis-b">
        <div class="grid grid-cols-3 gap-3">
          <div class="stat-card" style="background:linear-gradient(135deg,#14532D,#15803D);"><p class="stat-num">110</p><p class="text-green-100 text-sm font-semibold mt-2">empreendimentos (TUPs e arrendamentos)</p></div>
          <div class="stat-card" style="background:linear-gradient(135deg,#14532D,#15803D);"><p class="stat-num">R$ 124,9 bi</p><p class="text-green-100 text-sm font-semibold mt-2">de investimento previsto</p></div>
          <div class="stat-card" style="background:linear-gradient(135deg,#14532D,#15803D);"><p class="stat-num">8,4%</p><p class="text-green-100 text-sm font-semibold mt-2">executado (R$ 10,5 bi)</p></div>
        </div>
        <p class="sis-d">Troca o RAPIR em PDF, contrato a contrato, por <strong>base estruturada</strong> com API, correção monetária e trilha
        de auditoria. Atende à Recomendação I da Auditoria nº 06/2022.</p>
        <p class="sis-x"><i class="fas fa-link"></i> Painel da carteira para a Diretoria e os órgãos de controle.</p>
      </div>
    </div>
  </div>
  <div class="px-16 pb-2">
    <div class="destaque flex items-center gap-6">
      <i class="fas fa-database text-3xl" style="color:#FFD700;"></i>
      <p class="text-lg" style="margin:0;">O dado nasce na fiscalização e passa a <strong style="color:#FFD700;">servir às outras agendas</strong>. Na mesma linha,
      o <strong>SFIS Novo</strong> leva o controle fiscal para o Oracle APEX, com migração da base atual.</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {PROJ}, telas 7, 9 e 10. SisPAT: posição em 19/08/2026. SAI: carteira do GEF Investimentos, valores em base ago/2025.</p>
""",
    extra_css="""
.sis { border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; display:flex; flex-direction:column; }
.sis-top { color:#fff; padding:14px 22px; display:flex; gap:16px; align-items:center; }
.sis-top i { font-size:calc(30px * var(--tz)); opacity:0.9; }
.sis-top p { margin:0; }
.sis-k { font-family:'Montserrat',sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; font-size:calc(12.5px * var(--tz)); opacity:0.85; }
.sis-t { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(22px * var(--tz)); line-height:1.2; }
.sis-b { flex:1; padding:16px 22px; display:flex; flex-direction:column; justify-content:space-evenly; gap:12px; }
.sis-b p { margin:0; }
.sis-b .stat-num { font-size:calc(27px * var(--tz)); white-space:nowrap; }
.sis-d { color:#475569; font-size:calc(16.5px * var(--tz)); line-height:1.45; }
.sis-d strong { color:#003366; }
.sis-x { color:#5B21B6; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(15.5px * var(--tz)); }
""",
    tag=TAG_B4,
    base=1.78,
)

# ---------------------------------------------------------------------------
# 24 — Melhorias a encaminhar em conjunto
# ---------------------------------------------------------------------------
def _melh(n, t, d, quem, base_txt):
    return f"""
      <div class="ml">
        <div class="ml-top"><span class="ml-n">{n}</span><p class="ml-t">{t}</p></div>
        <p class="ml-d">{d}</p>
        <div class="ml-f"><span class="quem">{quem}</span><span class="ml-b">{base_txt}</span></div>
      </div>"""


novo(
    24,
    "Melhorias a encaminhar em conjunto",
    "Propostas de melhoria · para discussão",
    "O que podemos encaminhar juntos",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-3 gap-5">
    {_melh("1", "Um calendário só para ouvir o setor",
           "Consulta externa do PAF aberta no 1º semestre, dentro do ciclo de participação social da Agenda Regulatória, sem consultar duas vezes os mesmos respondentes.",
           "SRG", "NT 27/2026, item 8.2, I")}
    {_melh("2", "Fiscalização como evidência para a norma",
           "Resultados das temáticas e das operacionais alimentam a AIR e a Avaliação de Resultado Regulatório; o que não tem método vai ao GT do tema 2.8.",
           "SRG", "NT 27/2026, item 8.2, VIII")}
    {_melh("3", "Temáticas e estudos lado a lado",
           "Temáticas ancoradas em estudos ainda abertos (P1, P14, P21) e, na navegação interior, pauta de campo para os estudos que ficaram sem demanda.",
           "SEPH", "NT 27/2026, itens 5.3 e 6.4")}
    {_melh("4", "Meio ambiente no radar do PAF",
           "Resíduos de embarcações e riscos climáticos com a área do Índice de Desempenho Ambiental, com método desenhado em conjunto.",
           "SESGI · GMS", "NT 27/2026, item 5.16")}
    {_melh("5", "O dado de uma área vira Nível 1 da outra",
           "Estatístico Aquaviário, Sistema de Desempenho Portuário e SisPAT como fontes de monitoramento automatizado, com as lacunas de Nível 1 no PDTIC.",
           "SESGI · GEA · SGE", "NT de arquitetura da F3N")}
    {_melh("6", "Planejamento que conversa com pessoas",
           "A capacidade do PAF vem do PGD: lotação no Norte e capacitação no PGA, e o EPAF no acompanhamento do desempenho institucional.",
           "SGE", "minuta da NT de Metodologia, itens 6 a 8")}
  </div>
  <div class="px-16 pb-2">
    <div class="destaque flex items-center gap-6">
      <i class="fas fa-handshake text-3xl" style="color:#FFD700;"></i>
      <p class="text-lg" style="margin:0;"><strong>Para começar:</strong> um ponto focal por agenda e um marco comum no calendário, para que a revisão
      de cada agenda considere <strong style="color:#FFD700;">o que as outras aprenderam no ciclo</strong>.</p>
    </div>
  </div>
""",
    extra_css="""
.ml { border:1px solid #E2E8F0; border-radius:16px; padding:16px 20px; display:flex; flex-direction:column; gap:10px; background:#fff; }
.ml p { margin:0; }
.ml-top { display:flex; gap:14px; align-items:center; }
.ml-n { width:42px; height:42px; border-radius:50%; flex-shrink:0; background:#003366; color:#FFD700; display:flex; align-items:center; justify-content:center;
        font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(19px * var(--tz)); }
.ml-t { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(20px * var(--tz)); line-height:1.2; }
.ml-d { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.45; flex:1; }
.ml-f { display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap; border-top:1px solid #F1F5F9; padding-top:8px; }
.ml-b { color:#94A3B8; font-size:calc(13px * var(--tz)); }
""",
    tag=TAG_B4,
    base=1.71,
)


# ---------------------------------------------------------------------------
# Posição final das telas herdadas do deck do PAF ao DG (pelo número em que
# foram escritas lá) e a etiqueta de bloco que cada uma passa a levar aqui.
# Capa (1) e encerramento (25) são escritos à mão; 4, 9, 14 e 21 são divisórias.
# ---------------------------------------------------------------------------
POSICAO = {3: 6, 2: 11, 5: 12, 6: 13, 8: 15, 10: 16, 13: 17, 15: 18, 17: 20}
ETIQUETA = {6: TAG_B1, 11: TAG_B2, 12: TAG_B2, 13: TAG_B2,
            15: TAG_B3, 16: TAG_B3, 17: TAG_B3, 18: TAG_B3, 20: TAG_B3}
for s in SLIDES:
    if not s.get("fix"):
        s["n"] = POSICAO[s["n"]]
        s["tag"] = ETIQUETA[s["n"]]

# ---------------------------------------------------------------------------
# Divisórias de bloco — espelham IA-Dia-a-Dia-SFC/slide-04.html (KIT, seção 7.1)
# ---------------------------------------------------------------------------
DIVISOR = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
<style>
body {{ margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }}
.slide {{ width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden;
  background:linear-gradient(135deg, #002244 0%, #003366 50%, #004488 100%); color:white; }}
.font-montserrat {{ font-family:'Montserrat',sans-serif; }}
.accent-left-gold {{ position:absolute; left:0; top:0; width:12px; height:100%; background:#FFD700; z-index:20; }}
.accent-left-blue {{ position:absolute; left:12px; top:0; width:4px; height:100%; background:#0066CC; z-index:20; }}
.shape-circle {{ position:absolute; border-radius:50%; z-index:0; }}
.shape-1 {{ width:620px; height:620px; top:-180px; right:-160px; border:60px solid rgba(255,255,255,0.03); }}
.shape-2 {{ width:420px; height:420px; bottom:-140px; right:18%; border:40px solid rgba(255,255,255,0.03); }}
.bg-pattern {{ background-image:radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px); background-size:22px 22px; }}
.module-num {{ font-family:'Montserrat',sans-serif; font-weight:900; line-height:0.9; font-size:188px;
  letter-spacing:-4px; color:#FFD700; text-shadow:0 8px 24px rgba(0,0,0,0.35); }}
.seal {{ display:inline-flex; align-items:center; gap:16px;
  background:linear-gradient(90deg, rgba(255,215,0,0.16) 0%, rgba(255,215,0,0.04) 100%);
  border:2px solid rgba(255,215,0,0.55); border-radius:999px; padding:16px 34px; }}
.chip {{ display:flex; align-items:center; gap:18px; background:rgba(255,255,255,0.07);
  border:1px solid rgba(255,255,255,0.14); border-radius:16px; padding:22px 22px; }}
.chip-icon {{ width:64px; height:64px; border-radius:14px; flex-shrink:0; display:flex; align-items:center;
  justify-content:center; font-size:28px; background:rgba(0,102,204,0.30); color:#7CC0FF; }}
.chip-text {{ font-family:'Montserrat',sans-serif; font-weight:600; color:#FFFFFF; font-size:22px; line-height:1.25; margin:0; }}
</style>
</head>
<body>
<div class="slide">
  <div class="accent-left-gold"></div>
  <div class="accent-left-blue"></div>
  <div class="shape-circle shape-1"></div>
  <div class="shape-circle shape-2"></div>
  <div class="absolute inset-0 bg-pattern"></div>
  <img src="assets/logo-antaq-branca.png" alt="" class="absolute"
       style="top:42%; left:66%; width:48vw; max-width:720px; transform:translate(-50%,-50%); opacity:0.05; z-index:0; pointer-events:none;"/>
  <div class="absolute text-white z-0"
       style="bottom:-60px; right:-40px; font-size:500px; line-height:0; opacity:0.05; transform:translate(8%,8%);">
    <i class="fas {icone}"></i>
  </div>

  <div class="absolute z-10 flex items-center gap-4" style="top:56px; left:96px;">
    <img src="assets/logo-antaq-branca.png" alt="Logo ANTAQ" style="height:52px; width:auto;"/>
    <div style="border-left:1px solid rgba(255,255,255,0.20); padding-left:18px;">
      <p class="font-montserrat font-bold uppercase" style="font-size:18px; letter-spacing:.18em; color:#BFDBFE;">Agendas em Sincronia · 13 de outubro de 2026</p>
      <p class="font-montserrat font-semibold uppercase" style="font-size:17px; letter-spacing:.12em; color:#93C5FD; opacity:.85;">SFC · GRAT · GPF · GCOR</p>
    </div>
  </div>

  <div class="relative z-10 flex-1 flex flex-col justify-center"
       style="padding-left:96px; padding-right:80px; padding-top:96px; padding-bottom:24px;">
    <div class="flex items-center gap-4" style="margin-bottom:26px;">
      <div style="width:72px; height:4px; background-color:#FFD700;"></div>
      <p class="font-montserrat font-semibold uppercase" style="font-size:22px; letter-spacing:.3em; color:#BFDBFE;">Bloco</p>
    </div>
    <div class="flex items-end" style="gap:40px; margin-bottom:46px;">
      <span class="module-num">{num}</span>
      <div style="border-left:5px solid rgba(255,215,0,0.55); padding-left:36px; padding-bottom:10px;">
        <h1 class="font-montserrat font-black text-white" style="font-size:80px; line-height:1.06; letter-spacing:-1.5px;">{titulo}</h1>
        <p class="font-montserrat" style="font-size:30px; font-weight:400; line-height:1.4; color:#DBEAFE; max-width:1300px; margin-top:16px;">{resumo}</p>
      </div>
    </div>
    <div class="grid grid-cols-{ncol}" style="gap:20px; max-width:1640px;">
{chips}
    </div>
    <div style="margin-top:44px;">
      <span class="seal">
        <i class="fas fa-file-lines" style="color:#FFD700; font-size:28px;"></i>
        <span class="font-montserrat" style="font-size:26px; font-weight:700; color:#fff;">{base_doc}</span>
      </span>
    </div>
  </div>

  <div class="relative z-10 flex justify-between items-end" style="padding:0 96px 32px;">
    <p class="font-montserrat" style="font-size:18px; color:#BFDBFE; opacity:.75;">{rodape}</p>
    <p class="font-mono" style="font-size:18px; color:#BFDBFE; opacity:.75;">{n} / {total}</p>
  </div>
</div>
<script>document.addEventListener("keydown",function(e){{if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){{e.preventDefault();window.parent.postMessage({{type:"slide-nav",key:e.key}},"*");}}}});</script>
</body>
</html>
"""


def divisor(n, num, titulo, resumo, icone, chips, base_doc):
    html_chips = "\n".join(
        f'      <div class="chip"><div class="chip-icon"><i class="fas {ic}"></i></div>'
        f'<p class="chip-text">{tx}</p></div>'
        for ic, tx in chips
    )
    (DST / f"slide-{n:02d}.html").write_text(DIVISOR.format(
        title=f"Bloco {int(num)} — {titulo}", num=num, titulo=titulo, resumo=resumo,
        icone=icone, chips=html_chips, ncol=len(chips), base_doc=base_doc,
        rodape=RODAPE, n=n, total=TOTAL,
    ), encoding="utf-8")
    print(f"slide-{n:02d}.html (divisória)")


divisor(
    4, "01", "A agenda da fiscalização",
    "O PPF 2025-2028 organiza a fiscalização em três enfoques: o risco de cada regulado, "
    "o meio de verificar cada obrigação e a especialização das equipes.",
    "fa-compass-drafting",
    [("fa-flag", "Premissas do PPF"), ("fa-gauge-high", "Fiscalização Responsiva"),
     ("fa-layer-group", "Fiscalização em 3 Níveis"), ("fa-users-gear", "Grupos Especializados")],
    "Plano Plurianual de Fiscalização 2025-2028",
)
divisor(
    9, "02", "O rito do PAF",
    "Da nota de risco de cada outorga à proposta que vai à Diretoria Colegiada até 31/10: "
    "quem faz o quê, e se o plano cabe na equipe.",
    "fa-route",
    [("fa-sitemap", "Quem faz o quê"), ("fa-code-branch", "PAF 2027 em duas frentes"),
     ("fa-list-check", "O que entra no plano"), ("fa-users", "Força de trabalho")],
    "Minuta da NT de Metodologia do PAF 2027 · Regimento Interno",
)
divisor(
    14, "03", "Conexão com as outras agendas",
    "As temáticas de 2027 partiram das contribuições da Agenda Regulatória e foram confrontadas "
    "com a Agenda de Estudos: o que já se cruza e o que ainda falta.",
    "fa-link",
    [("fa-inbox", "99 demandas externas"), ("fa-check-double", "Quem já alcança cada uma"),
     ("fa-arrows-rotate", "Manter quatro, substituir três"), ("fa-list-ol", "Candidatos às vagas"),
     ("fa-diagram-project", "Mapa de conexões")],
    "Nota Técnica nº 27/2026/GPF/SFC · SEI 3024667",
)
divisor(
    21, "04", "Projetos e melhorias",
    "O que está em curso na SFC e o que podemos encaminhar em conjunto com as demais agendas.",
    "fa-rocket",
    [("fa-scale-balanced", "Normas em implantação"), ("fa-database", "Sistemas: SisPAT e SAI"),
     ("fa-handshake", "Seis propostas de melhoria")],
    "Projetos SFC 2026 · propostas para discussão",
)


def render(s):
    css = f':root {{ --tz-base: {s.get("base", 1.0) * TEXT_SCALE:.4g}; }}\n' + BASE_CSS + s.get("extra_css", "")
    return HEAD.format(
        title=s["title"], css=css, kicker=s["kicker"], titulo=s["titulo"],
        tag=s.get("tag", ""), body=s["body"], rodape=RODAPE, n=s["n"], total=TOTAL,
    )


for s in sorted(SLIDES, key=lambda s: s["n"]):
    if s.get("raw"):
        continue
    (DST / f"slide-{s['n']:02d}.html").write_text(render(s), encoding="utf-8")
    print(f"slide-{s['n']:02d}.html")
