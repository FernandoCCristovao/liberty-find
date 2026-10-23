# Contratos de dados

O formato de cada arquivo e tabela. O código que garante estes contratos está em
`src/liberty_find/models.py`; os dois mudam juntos, com os testes. Camadas e porquê:
[ADR 0010](../decisoes/0010-lakehouse-iceberg-dbt.md) (lago) e [ADR 0012](../decisoes/0012-banco-de-servico-postgres.md) (índice).

## Princípios

- **Retrato diário idempotente:** cada dia tem um arquivo de vagas; rodar de novo no mesmo dia sobrescreve.
- **IDs estáveis:** `posting_id = <source>:<board>:<source_job_id>`.
- **Tempo em UTC:** `dt` é a data UTC da coleta (`AAAA-MM-DD`); datas e horas em ISO 8601 com fuso.
- **JSON Lines com gzip** no bronze; Iceberg na prata e no ouro.
- **Colunas e valores de categoria em inglês**, `snake_case`. Rótulos em português nascem na
  camada de apresentação.
- **Procedência sempre:** todo campo gerado por LLM carrega `model_id`, `prompt_version` e
  `schema_version`.
- **Nada pessoal no lago:** `description_text` é interno e nunca é publicado; dado de usuário só no
  banco de serviço ([privacidade.md](../privacidade.md)).

## Bronze: arquivos no S3

| Chave | Conteúdo | Gravado por | Estado |
| --- | --- | --- | --- |
| `raw/source={source}/board={board}/dt={dt}/payload.json.gz` | Resposta da API como veio | coleta | Pronto |
| `postings/dt={dt}/postings.jsonl.gz` | Uma linha `JobPosting` por vaga aberta no dia | coleta | Pronto |
| `health/dt={dt}/health.json` | `CollectionReport`: estado por empresa e total | coleta | Pronto |
| `extractions/dt={dt}/extractions.jsonl.gz` | Uma linha `ExtractionRecord` por vaga extraída no dia | extração | Marco 1 |
| `state/extracted.jsonl.gz` | Chaves de extração já feitas (`posting_id`, `content_hash`, versões, modelo) | extração | Marco 1 |

## Tabela `postings` (Athena, banco `liberty_find`)

Uma linha por vaga aberta em cada dia de coleta. Partição: `dt` (projeção por data, sem crawler).

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `posting_id` | string | `<source>:<board>:<source_job_id>`; único dentro de um `dt` |
| `source` | string | `greenhouse`, `lever`, `ashby` ou `workable` |
| `board` | string | Token da empresa na fonte |
| `company` | string | Nome da empresa, de `boards.yaml` |
| `source_job_id` | string | ID da vaga na fonte |
| `title` | string | Título, sem espaços nas pontas |
| `url` | string | Link público da vaga (https) |
| `location` | string | Local como a fonte informa |
| `workplace_type` | string | Modelo de trabalho como a fonte informa; nulo quando a fonte não tem o campo |
| `country` | string | País, quando a fonte informa |
| `department` | string | Primeira área ou departamento informado |
| `language` | string | Idioma da vaga, quando a fonte informa |
| `description_text` | string | Descrição em texto puro. **Interna: nunca publicada** |
| `content_hash` | string | SHA-256 de título e descrição; muda quando a vaga muda |
| `published_at` | string | Primeira publicação (ISO 8601), quando a fonte informa |
| `updated_at` | string | Última atualização (ISO 8601), quando a fonte informa |
| `collected_at` | string | Momento da coleta (ISO 8601, UTC) |
| `dt` | string | Partição: data UTC da coleta |

Datas ficam como texto nesta camada; o dbt converte para `timestamp`.

## Tabela `extractions` (Marco 1)

Uma linha por vaga extraída, com a procedência. Os campos de hoje (`ExtractedFields`, versão 1)
estão no código; a versão 2, com os sinais de liberdade, é candidata e só entra no código depois da
auditoria de rótulos ([extracao.md](extracao.md)).

| Coluna | Tipo | Valores (v1) |
| --- | --- | --- |
| `posting_id`, `content_hash` | string | Ligam a extração à versão da vaga |
| `model_id`, `prompt_version`, `schema_version` | string | Procedência: qual modelo, qual prompt e qual versão do esquema |
| `extracted_at` | string | ISO 8601, UTC |
| `role_family` | string | `ai`, `data_engineering`, `analytics_bi`, `analytics_engineering`, `automation`, `software`, `other` |
| `seniority` | string | `intern`, `junior`, `mid`, `senior`, `staff_plus`, `manager`, `not_informed` |
| `work_model` | string | `remote`, `hybrid`, `onsite`, `not_informed` |
| `contract_type` | string | `clt`, `pj`, `other`, `not_informed` |
| `english_level` | string | `none`, `basic`, `intermediate`, `advanced`, `fluent`, `not_informed` |
| `english_required` | boolean | `true` obrigatório, `false` desejável, nulo quando não citado |
| `salary_min`, `salary_max` | double | Faixa informada; nulo quando não há número |
| `salary_currency` | string | `BRL`, `USD`, `EUR` ou nulo |
| `salary_period` | string | `month`, `year`, `hour` ou nulo |
| `years_experience_min` | int | Anos mínimos pedidos, de 0 a 30, ou nulo |
| `stack` | array<string> | Até 15 tecnologias, em minúsculas |

Uma vaga é reextraída quando muda o `content_hash`, o prompt ou o esquema. Para análise vale a
extração mais recente de cada par `posting_id` e `content_hash` (regra aplicada no dbt).

## Relatório de saúde (`health.json`)

```json
{
  "collected_at": "2026-10-12T09:00:00Z",
  "postings_total": 412,
  "postings_key": "postings/dt=2026-10-12/postings.jsonl.gz",
  "boards": [
    {"source": "greenhouse", "board": "quintoandar", "status": "ok", "postings": 96, "detail": null},
    {"source": "lever", "board": "neon", "status": "skipped", "postings": 0, "detail": "sem implementação"}
  ]
}
```

## Prata e ouro (planejado, Marco 2)

Tabelas Iceberg geridas pelo dbt. O contrato de cada modelo fica no `schema.yml` do dbt, com
testes; esta tabela é o mapa.

| Tabela | Camada | Grão | Para quê |
| --- | --- | --- | --- |
| `posting_versions` | Prata | Uma linha por versão (`posting_id`, `content_hash`) | Histórico; liga a extração à versão certa |
| `postings_current` | Prata | Uma linha por vaga | Estado atual, atualizado por MERGE |
| `posting_presence` | Prata | Uma linha por vaga | `first_seen`, `last_seen`, `closed_at` (fecha após duas coletas sem a vaga) |
| `posting_extractions` | Prata | Uma linha por vaga e versão | Extração mais recente válida |
| `dedup_clusters` | Prata | Uma linha por vaga | `cluster_id` para a mesma vaga em fontes ou repostagens diferentes |
| `active_postings` | Ouro | Uma linha por vaga ativa e canônica | O que vai para o índice, o site e os canais |
| `market_*` | Ouro | Agregados por semana e recorte | Insights do mercado |
| `board_health` | Ouro | Uma linha por empresa e dia | Saúde das fontes |

## Índice de vagas e dados do app (planejado, Marcos 4 e 5)

No Postgres. O esquema nasce em migrações versionadas no repositório.

| Tabela | Conteúdo | Dado pessoal |
| --- | --- | --- |
| `postings` | Vagas ativas: campos derivados, `summary_en`, `tsvector`, embedding (`halfvec`) com `embedding_model` | Não |
| `users` | Conta (identificador do Cognito e e-mail) | Sim |
| `search_profiles` | Preferências e texto livre normalizado, com versão | Sim |
| `match_explanations` | Explicação por (perfil, versão do perfil, vaga, `content_hash`) | Sim |
| `feedback` | Vaga marcada como boa ou ruim, com motivo | Sim |

Tabelas com dado pessoal têm row-level security por usuário.

## Política de publicação

| Dado | Pode ser público? |
| --- | --- |
| Contagens, médias, distribuições, tendências | Sim |
| Título, empresa, local, link e campos extraídos de uma vaga | Sim (é o que a própria vaga já publica), respeitando a política da fonte |
| Resumo curto escrito pelo pipeline, com link | Sim |
| Trechos curtos de evidência (até 3 por vaga, 200 caracteres cada), com link | Sim, quando a política da fonte permite exibir |
| Descrição completa | Não |
| E-mail, telefone ou nome de recrutador | Nunca |
| Qualquer dado de usuário | Nunca |

## Como mudar um contrato

1. Proponha a mudança na tarefa ou num ADR, se afetar consumidores (site, índice, app, agente).
2. Mude `models.py`, este arquivo e os testes no mesmo commit.
3. Se uma tabela do Athena mudar, ajuste a definição na infraestrutura como código.
4. Coluna nova entra sempre no fim e aceitando nulo, para não quebrar arquivos antigos.
