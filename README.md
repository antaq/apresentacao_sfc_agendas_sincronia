# Agendas em Sincronia — O Plano de Fiscalização e as Agendas da ANTAQ (13/10/2026)

Apresentação da SFC no *Agendas em Sincronia*, o Ciclo de Workshops sobre as Agendas da ANTAQ
(bloco da tarde, com SEPH, SESGI e SGE; Plenário da ANTAQ e Teams). Cerca de 1 h: 50 min de
exposição e 10 min de conversa. Pedido da organização: o rito do PAF, a conexão com as outras
agendas, os projetos em andamento e as melhorias a encaminhar em conjunto.

25 telas, em quatro blocos:

| Telas | Conteúdo | Origem |
|---|---|---|
| 01–03 | Capa, roteiro, onde a fiscalização entra no planejamento | novas |
| 04–08 | Bloco 1 · PPF 2025-2028: premissas, Fiscalização Responsiva, 3 Níveis, GEF | Trilha Técnica, aula 8; deck do PAF ao DG; Projetos SFC 2026 |
| 09–13 | Bloco 2 · Rito do PAF: quem faz o quê, PAF 2027, composição, força de trabalho | Regimento Interno; deck do PAF ao DG |
| 14–20 | Bloco 3 · Conexões: Agenda Regulatória, Agenda de Estudos, temáticas, mapa de conexões, operacionais | NT 27/2026; deck do PAF ao DG |
| 21–25 | Bloco 4 · Projetos em andamento, SisPAT e SAI, seis propostas de melhoria, encerramento | Projetos SFC 2026 (ago/2026); NT 27/2026; NT da F3N |

- `slide-01.html` (capa) e `slide-25.html` (encerramento): escritos à mão.
- As demais telas saem de `build_slides.py` (`python3 build_slides.py`). O gerador herda o
  esqueleto e nove telas de `../apresentacao_paf_diretoria/build_slides.py`, remapeadas pelo
  dicionário `POSICAO`; as telas novas usam `novo()` e já levam a posição final.
- O `base=` de cada tela nova foi fechado em 95% do maior fator de texto que cabe sem invadir o
  rodapé (medido no Chrome em 12/10/2026). Depois de mexer no conteúdo, meça de novo antes de subir o `base`.
- Cartão de compartilhamento: `assets/og-capa.jpg`, gerado a partir de `assets/og-fonte.html`.

Para ver: `python3 -m http.server 8766` nesta pasta e abrir `http://localhost:8766/`.

## Animação dos cards

`anim.js` faz os cards entrarem em sequência, como cartas postas na mesa, quando o slide abre (no máximo ~3 s). Vale para todas as telas de conteúdo e para o encerramento; capa e divisórias ficam de fora. Respeita a preferência "reduzir movimento" do sistema.
