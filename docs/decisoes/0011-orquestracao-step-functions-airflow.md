# ADR 0011: Orquestração com Step Functions em produção e Airflow 3 local como trilha de comparação

- Status: aceita
- Data: 2026-10-20

## Contexto

A rotina diária tem passos encadeados: coletar dezenas a centenas de empresas, extrair só o que
mudou, rodar o `dbt build`, sincronizar o índice e publicar nos canais; uma vez por semana, manter
as tabelas Iceberg e conferir as APIs. Precisa de novas tentativas, alerta de falha e custo perto
de zero.

O que pesa (conferido em 2026-10-20):

| Opção | Custo na escala do projeto | Observação |
| --- | --- | --- |
| EventBridge Scheduler + Step Functions | Dentro da cota gratuita (14 milhões de chamadas e 4 mil transições por mês) | Nativo da AWS; a definição fica na infraestrutura como código |
| Airflow no MWAA | Cerca de US$ 358 por mês no menor ambiente | Fora do orçamento |
| Airflow no MWAA Serverless | Centavos (US$ 0,08 por hora de tarefa) | Lançado em 2025; detalhes de limitação (operadores, interface) ainda por conferir |
| Airflow em máquina própria | Máquina ligada o mês todo, mais IPv4 público (US$ 3,65 por mês) | Custo fixo e manutenção de servidor |
| Astronomer | Cerca de US$ 255 por mês | Fora do orçamento |
| Dagster+ ou Prefect Cloud | US$ 10 por mês ou plano gratuito limitado | Bons, mas pouco pedidos no mercado |
| GitHub Actions agendado | Gratuito em repositório público | Atrasa no início de cada hora e desliga após 60 dias sem atividade no repositório |

Fontes: [Step Functions](https://aws.amazon.com/step-functions/pricing),
[EventBridge](https://aws.amazon.com/eventbridge/pricing/),
[MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/pricing/),
[GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).

O Airflow é o orquestrador mais adotado em equipes de dados: aparece em cerca de dez vezes mais
anúncios que o Dagster no Reino Unido, e numa pesquisa de 2026 o Dagster está em 6,2% das equipes
e o Prefect em 1,3% ([Practical Data 2026](https://joereis.github.io/practical_data_data_eng_survey/)).
Saber operar Airflow tem valor por si só para quem mantém o projeto.

## Decisão

- **Produção:** o EventBridge Scheduler dispara, às 06:00 (America/Sao_Paulo), uma máquina de
  estados do Step Functions (Standard): `Map` sobre lotes de até 50 empresas chamando a Lambda de
  coleta, extração do delta, `dbt build` (Lambda em imagem de contêiner), sincronização do índice e
  publicação. `Retry` com espera crescente em cada passo e `Catch` para o alerta. Granularidade
  grossa, para ficar abaixo de 4 mil transições por mês.
- **Airflow 3 local:** um DAG em `airflow/` que chama as mesmas funções, rodando com Docker Compose,
  para desenvolvimento e para uma comparação documentada com o Step Functions (Marco 2). Não roda em
  produção.
- **Regra de código:** nenhuma lógica dentro do orquestrador. Cada passo é uma função Python
  testada, que qualquer orquestrador consegue chamar.
- **GitHub Actions:** só CI e uma conferência semanal das APIs das fontes (canário).

## Alternativas consideradas

- **Airflow gerenciado em produção:** o mais reconhecido, mas o menor ambiente custa, em um mês,
  cerca de três vezes o orçamento de um ano inteiro do projeto.
- **MWAA Serverless:** promissor pelo preço; entra como candidato quando as limitações estiverem
  conferidas em uso real.
- **Só GitHub Actions:** gratuito, mas não é confiável para produção.
- **Dagster ou Prefect:** boa experiência local, pouca adoção.

## Consequências

- Custo de orquestração zero na escala do MVP.
- Duas definições de fluxo para manter; o custo é baixo porque os passos são finos.
- Falha de qualquer passo gera alerta com o passo e o erro.

## Rever se

O MWAA Serverless rodar o DAG com custo de centavos e com as funções que o projeto usa, o fluxo
passar de cerca de 15 passos com dependências cruzadas, ou o projeto passar a ter mais de uma
pessoa operando.
