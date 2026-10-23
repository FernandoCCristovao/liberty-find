# Marco 1: Coleta no ar

**Objetivo:** coleta diária das quatro fontes rodando sozinha na AWS, com infraestrutura em
Terraform, empresas descobertas de forma sistemática e sinais extraídos por um modelo escolhido por
avaliação.

**Já pronto:** contratos (`models.py`), fonte Greenhouse com testes, núcleo da coleta com gravação
local e no S3, relatório de saúde, CLI `liberty`, esquema e prompt v1 da extração, template do SAM
(a migrar), CI, pre-commit e Dependabot.

## Tarefas (na ordem)

### [ ] 1.1 Conta AWS e repositório

- Fazer: conta AWS no plano pago, MFA na raiz, usuário no IAM Identity Center e perfil da CLI, como
  em [operacao.md](../operacao.md); orçamento de US$ 10 com alerta (manual nesta etapa); teste do
  Nova Lite no playground do Bedrock; pedido de aumento da cota de concorrência do Lambda. Criar o
  repositório público no GitHub (aprovação humana), com o relato privado de vulnerabilidades ligado.
- Aceite: `aws sts get-caller-identity` mostra o usuário do Identity Center, não a raiz; orçamento
  ativo; repositório no ar com o CI verde.

### [ ] 1.2 Infraestrutura em Terraform e primeiro deploy

Decisão: [ADR 0016](../decisoes/0016-terraform.md). Feita antes do primeiro deploy, quando migrar
não custa nada.

- Fazer:
  - `infra/bootstrap/` (estado local, roda uma vez): bucket do estado com versionamento, criptografia
    e bloqueio de acesso público.
  - `infra/envs/dev/` e `infra/envs/prod/` com backend S3 (`use_lockfile = true`) e o mesmo código
    em `infra/modules/` só se houver repetição.
  - Mapear o `template.yaml` recurso a recurso:

    | SAM | Terraform |
    | --- | --- |
    | `DataBucket` | `aws_s3_bucket` com bloqueio público, criptografia e `aws_s3_bucket_lifecycle_configuration` |
    | `CollectFunction` | `aws_lambda_function` (zip, arm64, python3.12, timeout de 900 s), `aws_iam_role` e política só de escrita no bucket |
    | `CollectLogGroup` | `aws_cloudwatch_log_group` com 30 dias |
    | Evento `ScheduleV2` | `aws_scheduler_schedule` (fuso America/Sao_Paulo, uma nova tentativa) e papel para invocar a Lambda |
    | `AlertTopic` | `aws_sns_topic` e `aws_sns_topic_subscription` (e-mail) |
    | `CollectErrorsAlarm` | `aws_cloudwatch_metric_alarm` |
    | `GlueDatabase` e `PostingsTable` | `aws_glue_catalog_database` (`liberty_find`) e `aws_glue_catalog_table` com projeção de partições |
    | `AthenaWorkGroup` | `aws_athena_workgroup` (`liberty-find`, limite de bytes, local dos resultados) |
    | (novo) orçamento | `aws_budgets_budget` de US$ 10 com alertas, no lugar do orçamento manual |

  - `uv run poe package`: `uv export` sem dependências de desenvolvimento, `uv pip install --target`
    com rodas `manylinux` para arm64 e um zip por função, mais teste de que o zip importa o handler.
  - CI: `terraform fmt -check`, `terraform validate` e `tflint`; Dependabot para o ecossistema
    `terraform`.
  - Remover `template.yaml`, `samconfig.toml`, o `cfn-lint` e as tarefas do SAM no mesmo commit em que
    o Terraform vira a única fonte; reescrever a seção "Publicar" do [operacao.md](../operacao.md).
  - `terraform apply` em `dev` (aprovação humana); confirmar o e-mail do alarme; invocar a coleta à
    mão uma vez. Com as 11 empresas do Greenhouse em sequência, a coleta já fica dentro da etiqueta
    de [fontes.md](../dados/fontes.md); o limitador por host chega na 1.3, antes de a lista crescer.
- Aceite: `terraform plan` lista os recursos equivalentes ao template; CI verde com as checagens de
  Terraform; nenhum arquivo do SAM no repositório; `health.json` do dia com as empresas em `ok`; a
  consulta do operacao.md devolve vagas por empresa no Athena; no dia seguinte, a coleta rodou sozinha.

### [ ] 1.3 Fontes Lever, Ashby e Workable

Para cada fonte, no padrão de `sources/greenhouse.py` e `tests/unit/test_greenhouse.py`:

1. Baixar uma amostra real (endpoint de [fontes.md](../dados/fontes.md)) e anotar os campos. A
   amostra real não entra no repositório.
2. Criar uma fixture sintética mínima com a mesma forma, em `tests/fixtures/`.
3. Escrever os testes de `normalize` (campos, opcionais ausentes, resposta vazia) e de `fetch_raw`
   (URL e parâmetros, com respx).
4. Implementar em `sources/<fonte>.py` e registrar em `sources/__init__.py`.
5. Conferir com `uv run liberty probe <fonte> <token>`.

Para todas as fontes, no núcleo:

- Limitador por host: no máximo uma requisição por segundo em cada host, hosts diferentes em
  paralelo, espera crescente com variação aleatória e respeito a `Retry-After`.
- `redact_contacts` em `text.py`: a normalização remove e-mails e telefones da descrição, com testes
  ([privacidade.md](../privacidade.md)).

- Atenção: a Lever pagina com `skip` e `limit`, manda `createdAt` em milissegundos e tem instância
  na UE; a Ashby marca com `isListed = false` as vagas que não podem ser listadas; a Workable pode
  precisar de `details=true`. Guardar `workplaceType` como veio.
- Aceite: as três fontes registradas, testes passando, e `uv run liberty collect --local` coletando
  todas as empresas de `boards.yaml` (as que falharem aparecem explicadas no relatório de saúde).

### [ ] 1.4 Cobertura e descoberta de empresas

- Fazer: consultar o índice do Common Crawl no Athena (procedimento em
  [fontes.md](../dados/fontes.md#descoberta-de-empresas)), num workgroup próprio com limite de
  leitura; filtrar por domínio registrado para ler pouco e conferir no console o volume lido antes de
  repetir. A lista de candidatos fica fora do repositório (arquivo local ignorado pelo Git). Validar
  com `liberty probe` e levar ao `boards.yaml` só as empresas validadas com vagas de dados ou IA
  abertas a quem mora no Brasil ou em Portugal.
- Aceite: de 20 a 40 empresas ativas em `boards.yaml`, todas em `ok`, cada uma com a data da
  verificação; lista de candidatos guardada para a tarefa 2.4; custo da consulta anotado.

### [ ] 1.5 Auditoria de rótulos

Desenho em [extracao.md](../dados/extracao.md), seção "Auditoria de rótulos".

- Fazer: 200 vagas, com pré-rótulo de um modelo maior que não participa da escolha e correção
  campo a campo à mão (ferramenta local em `tools/annotator` ou planilha); medir a cobertura de cada
  campo; rotular de novo 20 vagas depois de uma semana; se faltar, montar a fatia do selo (só os
  campos de elegibilidade); fechar o esquema v2 e levá-lo ao código (`models.py`, `schema.py`,
  `prompt.py`, testes de contrato e [contratos.md](../dados/contratos.md)).
- Aceite: `evals/extraction/labels.jsonl` com 200 vagas rotuladas (só identificadores e valores, sem
  texto de vaga), separadas em 100 para ajuste e 100 para avaliação; pelo menos 60 vagas abertas a
  quem mora no Brasil ou em Portugal fora do ajuste, contando a fatia do selo; tabela de cobertura no
  extracao.md; esquema v2 no código com os testes de contrato passando.

### [ ] 1.6 Extração com LLM, selo e escolha do modelo

- Fazer:
  1. `extraction/bedrock.py`: interface `LLMClient` e a implementação Bedrock (Converse), com
     validação, nova tentativa, modelo de reserva e testes com `botocore.stub.Stubber`. Prompt v2 com
     a descrição entre delimitadores e a instrução de tratá-la como dado.
  2. `eligibility.py`: o selo de elegibilidade como função pura, com testes de casos conhecidos.
  3. `handlers/extract.py`: lê as vagas do dia, descarta o que está no manifesto, extrai até
     `MAX_EXTRACTIONS_PER_RUN` com concorrência 4, grava `extractions/` e atualiza o manifesto.
     Testes com moto e Stubber.
  4. Terraform: função de extração (timeout de 900 s), gatilho do S3 só no prefixo `postings/` e
     sufixo `.jsonl.gz`, permissão `bedrock:InvokeModel` só nos modelos usados, grupo de logs e
     tabela `extractions` no Glue.
  5. `uv run poe eval-extraction`: compara Nova Lite, Claude Haiku 5.5 e Nova Micro nas 100 vagas
     de avaliação, com as métricas do extracao.md, a precisão do selo e o custo projetado.
  6. Primeira carga em lote com o modelo vencedor; anotar o custo real.
- Aceite: depois da coleta, `extractions/dt=<dia>/` existe; uma consulta no Athena junta `postings`
  e `extractions`; rodar de novo no mesmo dia não reextrai nada; tabela da avaliação no README com o
  modelo escolhido, a precisão do selo e o custo por mil vagas.

### [ ] 1.7 README com números e fechamento

- Fazer: atualizar o README com o estado, o diagrama, os primeiros números (vagas por dia, empresas,
  custo do mês, acerto da extração) e a seção de conformidade; marcar as tarefas deste arquivo.
- Aceite: alguém de fora entende o projeto em um minuto; tag `v0.1.0` com notas da release.

## Fora deste marco

dbt, deduplicação, orquestração e o registro em escala (Marco 2); qualquer superfície pública
(Marco 3).
