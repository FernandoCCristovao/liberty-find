# ADR 0007: Power BI e Streamlit Community Cloud para os painéis

- Status: substituída pelo [ADR 0019](0019-superficies-publicas.md)
- Data: 2026-10-12

## Contexto

O painel precisa de um link público e gratuito, e a frente de BI do mercado brasileiro pede
Power BI. O BI da AWS (QuickSight) cobra por usuário ou por sessão para painel público e quase
não aparece nas vagas-alvo.

## Decisão

- Power BI Desktop ligado ao Athena pelo conector nativo (driver ODBC do Athena), salvo em
  formato PBIP (texto, versionável) em `powerbi/`, com capturas de tela no README.
- Painel público e, no Marco 3, conversa com o agente num app Streamlit no Streamlit Community
  Cloud, lendo as tabelas finais com uma credencial só de leitura e cache de 1 dia.

## Alternativas consideradas

- Amazon QuickSight: nativo da AWS, mas link público pago e pouco pedido nas vagas.
- Publicar na web pelo Power BI: exige conta corporativa e licença.
- Hospedar o Streamlit na AWS (App Runner, ECS): custo fixo.

## Consequências

- Duas peças fora da AWS, ambas gratuitas.
- O app Streamlit dorme depois de 12 horas sem acesso; o primeiro acesso demora alguns segundos.
- A credencial do Streamlit fica nos segredos do Streamlit Community Cloud, nunca no repositório.

## Rever se

O Streamlit Community Cloud mudar os limites gratuitos, ou uma vaga-alvo pedir QuickSight.
