# Marco 2: Lakehouse e qualidade

**Objetivo:** camada de dados confiável (histórico, estado atual, deduplicação e vagas fechadas),
rotina diária orquestrada, registro de empresas em escala, deploy sem chave fixa, qualidade da
extração medida a cada mudança e os primeiros insights do mercado.

Decisões: [ADR 0010](../decisoes/0010-lakehouse-iceberg-dbt.md),
[ADR 0011](../decisoes/0011-orquestracao-step-functions-airflow.md) e
[ADR 0009](../decisoes/0009-fontes-por-permissao.md).

## Tarefas (na ordem)

### [ ] 2.1 dbt com dbt-athena e Iceberg

- Fazer: projeto em `dbt/` com dbt-core 1.x e `dbt-athena`, perfil apontando para o workgroup
  `liberty-find`, tabelas Iceberg em `silver/` e `gold/`.
  - Staging: `stg_postings` e `stg_extractions` (tipos, nomes e a extração mais recente válida).
  - Prata: `posting_versions`, `postings_current` (incremental com `merge`), `posting_presence` e
    `posting_extractions`, como em [contratos.md](../dados/contratos.md).
  - Ouro: `active_postings` com o selo de elegibilidade em SQL, espelhando a função do Marco 1, e
    `board_health`.
  - Testes: `not_null`, `unique`, `accepted_values`, `relationships`, frescor da fonte e qualidade
    (completude, validade das categorias, valores plausíveis de salário por moeda e período);
    contratos de modelo nas tabelas de ouro; teste de que o selo em SQL e a função em Python
    concordam nos mesmos casos.
  - Lambda do dbt em imagem de contêiner, criada no Terraform.
- Aceite: `dbt build` passa sem erro no `dev`; as tabelas de ouro respondem às perguntas do
  [produto.md](../produto.md).

### [ ] 2.2 Deduplicação e vagas fechadas

- Fazer: agrupar posts do Greenhouse pelo `internal_job_id`; dentro de cada empresa, marcar como
  mesma vaga as que tiverem título normalizado e local compatíveis e texto muito parecido (MinHash
  sobre trechos de cinco palavras, limiar inicial de 0,85, ajustado em cerca de 200 pares
  rotulados); `cluster_id` com uma vaga canônica. Fechar uma vaga depois de duas coletas
  bem-sucedidas sem ela; pôr em quarentena a empresa cujo número de vagas cair mais de 50% de uma vez.
- Aceite: testes com casos sintéticos de repostagem, vaga em dois idiomas e vaga em duas fontes;
  precisão da deduplicação medida nos pares rotulados; nenhuma vaga fechada por falha de coleta.

### [ ] 2.3 Orquestração no Step Functions

- Fazer: máquina de estados (Terraform) com coleta em `Map` por lotes de empresas, hosts diferentes
  em paralelo, extração, `dbt build` e um ramo semanal de manutenção (`OPTIMIZE` e `VACUUM`); o
  agendamento diário passa a iniciar a máquina; alarme quando uma execução falha; canário semanal
  das APIs no GitHub Actions.
- Aceite: uma execução completa aparece verde no console; a falha de qualquer passo gera e-mail com
  o passo e o erro; menos de 4 mil transições por mês.

### [ ] 2.4 Registro de empresas em escala e fontes novas

- Fazer: validar os candidatos da tarefa 1.4 e de novas consultas de descoberta; quando o registro
  passar de cerca de 100 empresas, movê-lo para o bucket privado (o repositório fica com um exemplo);
  feed XML da Workable; avaliar SmartRecruiters, Teamtailor, Recruitee, Personio, Jobicy e Remote OK,
  cada fonte nova com a linha completa no catálogo de [fontes.md](../dados/fontes.md) (nível, termos
  com data, cadência e política de exibição) e com testes.
- Aceite: registro com 200 ou mais empresas validadas e em `ok`; cada fonte nova com testes e com a
  política de exibição em código.

### [ ] 2.5 Deploy pelo GitHub Actions com OIDC

Antes: a conta atual nega criar o provedor OIDC ([ADR 0024](../decisoes/0024-conta-aws-experiencia-nova-us-east-2.md)).
Decidir num ADR entre ativar os recursos avançados da conta (irreversível) e outro caminho sem
chave fixa.

- Fazer: provedor OIDC do GitHub e papéis do IAM no Terraform (um só de leitura para `plan` nos pull
  requests e outro para `apply`, preso ao ambiente do GitHub com aprovação humana); workflow de
  deploy para `dev` e `prod`.
- Aceite: um merge na `main` publica no `dev` depois da aprovação; nenhuma chave fixa da AWS em
  segredo do repositório.

### [ ] 2.6 Avaliação contínua da extração

- Fazer: o script do Marco 1 vira tarefa do CI (manual ou quando mudam prompt, esquema, modelo ou
  código de extração), lendo os textos do bucket privado com o papel da tarefa 2.5; tabela de
  resultados no README.
- Aceite: uma mudança de prompt mostra o antes e o depois por campo, sem passo manual além de
  aprovar a execução.

### [ ] 2.7 Airflow 3 local (fora do caminho do MVP)

- Fazer: `airflow/` com Docker Compose e um DAG que chama as mesmas funções dos passos do Step
  Functions; um README comparando os dois (definição, novas tentativas, observabilidade, custo,
  operação).
- Aceite: `docker compose up` e uma execução completa do DAG contra o ambiente `dev`.

### [ ] 2.8 Insights do mercado (fora do caminho do MVP)

- Fazer: marts `market_*` (vagas por semana e recorte, competências mais pedidas, percentual aberto a
  quem mora no Brasil e em Portugal, faixas salariais por moeda, exigência de inglês). Opcional:
  relatório em Power BI salvo como PBIP em `powerbi/`, com capturas no README.
- Aceite: os marts passam nos testes e respondem "o que as vagas de dados e IA abertas ao Brasil
  pedem este mês?".

### [ ] 2.9 Fechamento

- Aceite: README com o desenho do lakehouse, a avaliação e os números; tag `v0.2.0`.
