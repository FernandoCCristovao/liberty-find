# ADR 0002: S3 em JSON Lines, Glue Data Catalog e Athena

- Status: substituída pelo [ADR 0010](0010-lakehouse-iceberg-dbt.md)
- Data: 2026-10-12

## Contexto

O volume é pequeno (milhares de vagas por dia, alguns MB) e cresce devagar. A consulta é
analítica, feita por pessoas, pelo dbt e pelo agente. Não deve haver servidor nem custo fixo.

## Decisão

- Dados no S3, em JSON Lines com gzip, um arquivo por dia e por camada (`raw`, `postings`,
  `extractions`), particionados por `dt`.
- Tabelas no Glue Data Catalog definidas no `template.yaml`, com projeção de partições: o Athena
  acha as partições pelo padrão da chave, sem crawler.
- Consulta pelo Athena, num workgroup com limite de bytes por consulta.
- Estado da extração num manifesto no próprio S3 (`state/extracted.jsonl.gz`).
- No Marco 2, o dbt (adaptador `dbt-athena`) materializa as camadas analíticas.

## Alternativas consideradas

- Redshift Serverless: SQL completo, mas cobra por capacidade mínima enquanto ativo.
- RDS PostgreSQL: servidor ligado o tempo todo.
- DynamoDB: barato, mas ruim para consulta analítica.
- Parquet desde a coleta: mais eficiente, mas pede dependências pesadas na Lambda; o dbt converte depois.
- DynamoDB para o estado da extração: robusto, mas um serviço a mais para um caso simples.

## Consequências

- Custo de armazenamento e consulta em centavos.
- Rodar a coleta duas vezes no mesmo dia sobrescreve o arquivo do dia (idempotente).
- O JSON fica legível para depuração; o dbt resolve tipos e desempenho na camada analítica.

## Rever se

O volume passar de 1 GB por mês, ou a extração precisar de execuções concorrentes (aí o
estado vai para o DynamoDB).
