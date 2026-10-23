# ADR 0010: Lakehouse no S3: bronze em JSON Lines, prata e ouro em Iceberg com dbt-athena

- Status: aceita
- Data: 2026-10-20
- Substitui: [ADR 0002](0002-s3-athena-glue.md)

## Contexto

O ADR 0002 guardava tudo em JSON Lines por dia e deixava para o dbt a camada analítica, sem
definir o formato. O produto agora precisa de mais que retratos diários:

- histórico de versões de cada vaga (o texto muda e a extração precisa acompanhar);
- estado atual com atualização linha a linha (MERGE), para saber o que abriu e o que fechou;
- deduplicação entre fontes e detecção de vaga expirada;
- uma camada de ouro limpa para sincronizar com o índice ([ADR 0012](0012-banco-de-servico-postgres.md)).

Fatos que pesam na escolha (conferidos em 2026-10-20):

- O Athena faz `MERGE` só em tabelas Iceberg (engine 3) e lê Delta Lake só para consulta
  ([MERGE](https://docs.aws.amazon.com/athena/latest/ug/merge-into-statement.html),
  [Delta](https://docs.aws.amazon.com/athena/latest/ug/delta-lake-tables.html)).
- A manutenção do Iceberg no Athena (`OPTIMIZE` e `VACUUM`) é manual e barata
  ([otimização](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-data-optimization.html)).
- O dbt v2 (setembro de 2026) ainda não tem adaptador para Athena; o `dbt-athena` segue na linha
  1.x, com suporte a Iceberg e estratégia `merge`
  ([dbt v2](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-v2),
  [dbt-athena](https://docs.getdbt.com/reference/resource-configs/athena-configs)).
- Lakehouse com formato aberto de tabela é o ambiente principal de 26,8% das equipes de dados, e
  de 40% na América Latina, numa pesquisa com 1.101 profissionais
  ([Practical Data 2026](https://joereis.github.io/practical_data_data_eng_survey/)).
- O volume é pequeno: dezenas de milhares de vagas, alguns MB por dia. Athena custa US$ 5 por TB
  lido, com mínimo de 10 MB por consulta.

## Decisão

- **Bronze (como está no código):** `raw/` (resposta da API, 90 dias), `postings/` (retrato do
  dia normalizado, JSON Lines com gzip), `health/` e, na extração, `extractions/` e `state/`.
  Escrita idempotente por dia.
- **Prata e ouro:** tabelas Apache Iceberg no Glue Data Catalog, criadas e mantidas pelo
  `dbt-athena` (dbt-core 1.x), nos prefixos `silver/` e `gold/` do mesmo bucket.
  - Prata: `stg_*` (views de tipagem), `posting_versions` (histórico por `content_hash`),
    `postings_current` (MERGE por chave da vaga), `posting_presence` (`first_seen`, `last_seen`,
    `closed_at`), `posting_extractions` e `dedup_clusters`.
  - Ouro: `active_postings` (o que vai para o índice e para o site), `market_*` (insights) e
    `board_health`.
- **Manutenção:** `OPTIMIZE` e `VACUUM` uma vez por semana, como passo da orquestração.
- **Partições:** poucas ou nenhuma nas tabelas pequenas; arquivo demais custa mais que tabela grande.
- **DuckDB** só para exploração local dos mesmos dados, sem escrever no lago.
- **S3 Tables** (Iceberg gerenciado) fica para depois: a compatibilidade com o `dbt-athena` ainda
  não foi comprovada neste projeto.

## Alternativas consideradas

- **Parquet simples recriado toda noite:** mais simples, mas sem MERGE, sem histórico e sem
  viagem no tempo.
- **Delta Lake:** só leitura no Athena.
- **Redshift Serverless, Snowflake ou BigQuery:** cobram capacidade mínima ou tiram o projeto da
  AWS, sem ganho nesta escala.
- **DuckDB ou MotherDuck como motor principal:** ótimo ciclo local, mas a escrita em Iceberg ainda
  é limitada e seria mais um fornecedor.
- **dbt v2:** sem adaptador para Athena na data desta decisão.

## Consequências

- Custo de armazenamento e consulta em centavos por mês.
- O dbt traz testes, contratos de modelo e documentação; qualidade de dados passa a ser código.
- A manutenção do Iceberg entra na rotina e precisa de alarme se falhar.
- A versão do dbt fica travada na 1.x enquanto o adaptador exigir.

## Rever se

O dbt v2 ganhar adaptador para Athena, o volume passar de cerca de 1 GB por dia, ou o S3 Tables
se provar compatível com o `dbt-athena`.
