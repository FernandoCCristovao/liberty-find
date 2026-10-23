# ADR 0001: AWS, arquitetura serverless

- Status: substituída pelo [ADR 0008](0008-arquitetura-em-camadas.md)
- Data: 2026-10-12

## Contexto

O projeto precisa rodar sozinho todo dia, custar quase nada e usar a nuvem que mais aparece nas
vagas de dados no Brasil. Nas vagas remotas de dados, a AWS aparece mais que Azure e Google Cloud.

## Decisão

AWS, só com serviços sem servidor e cobrados por uso: Lambda para computação, EventBridge
Scheduler para agendamento, S3 para dados, Glue Data Catalog e Athena para SQL, Bedrock para LLM,
Step Functions para orquestração (Marco 2) e Bedrock AgentCore para publicar o agente (Marco 4).
Região `us-east-1`, que tem mais modelos no Bedrock. Logs com Powertools; alerta com CloudWatch e SNS.

## Alternativas consideradas

- Google Cloud (BigQuery, Cloud Run): bom e barato, mas menos pedido nas vagas-alvo.
- Execução local com DuckDB: custo zero, mas não mostra nuvem nem operação.
- Servidor sempre ligado (EC2, contêiner): custo fixo sem necessidade para uma carga diária curta.

## Consequências

- Custo de centavos por mês; a maior parte dos serviços cai na cota mensal gratuita.
- A conta precisa do plano pago para o AgentCore; o orçamento com alerta passa a ser obrigatório.
- Partes fora da AWS só com motivo registrado (ADR 0007).

## Rever se

A fatura mensal passar de US$ 5 depois dos créditos, ou a AWS deixar de liderar nas vagas-alvo.
