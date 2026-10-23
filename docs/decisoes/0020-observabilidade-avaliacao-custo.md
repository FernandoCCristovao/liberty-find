# ADR 0020: Observabilidade, avaliação contínua e proteção de custo

- Status: aceita (proteção de gasto complementada pelo [ADR 0024](0024-conta-aws-experiencia-nova-us-east-2.md))
- Data: 2026-10-20

## Contexto

O projeto roda sozinho todo dia, chama LLMs pagos por token e vai atender usuários. Três falhas
silenciosas precisam virar alarme: a coleta parar, a qualidade da extração ou do matching cair e o
custo subir. Fatos conferidos em 2026-10-20: o CloudWatch tem 5 GB de logs, 10 métricas e 10
alarmes gratuitos por mês; o Langfuse Cloud tem plano gratuito de 50 mil unidades por mês e versão
própria sob MIT; um NAT Gateway custa cerca de US$ 33 por mês e um IPv4 público cerca de US$ 3,65
([CloudWatch](https://aws.amazon.com/cloudwatch/pricing/), [Langfuse](https://langfuse.com/pricing),
[VPC](https://aws.amazon.com/vpc/pricing/)).

## Decisão

- **Logs e métricas:** Powertools for AWS Lambda (logs em JSON, métricas e rastreamento quando
  útil); alarmes para coleta falha, taxa de erro da extração, índice desatualizado (mais de 36 h) e
  gasto.
- **LLM:** rastreamento no Langfuse Cloud (plano gratuito) com amostragem para caber no limite;
  prompts versionados em arquivo no Git; custo por mil vagas publicado no README.
- **Avaliação contínua:** conjuntos rotulados em `evals/` (extração, matching e, depois, assistente)
  rodam no CI quando muda prompt, modelo, esquema ou código de enriquecimento; a tabela de resultados
  vai para o README.
- **Proteções de custo:** AWS Budgets com orçamento mensal de US$ 10 e alertas; limite de bytes por
  consulta no workgroup do Athena; teto de vagas e de tokens por execução; regras de ciclo de vida no
  S3; Lambdas fora de VPC; concorrência reservada nas Lambdas que chamam LLM quando a cota da conta
  permitir (contas novas começam com cota baixa); tag `project` em tudo.
- **Proibido sem ADR:** NAT Gateway, IPv4 fixo, RDS ou Aurora provisionados, OpenSearch, MWAA,
  Redshift, QuickSight e EC2.

## Alternativas consideradas

- **LangSmith:** bom, com plano gratuito menor (5 mil rastros por mês) e mais ligado ao LangChain.
- **Só CloudWatch para LLM:** um fornecedor a menos, sem a visão de prompts, versões e avaliações.
- **Avaliação manual de vez em quando:** barata, mas regressão passa despercebida.

## Consequências

- Toda mudança de prompt ou modelo vem com números antes e depois.
- O gasto mensal fica visível e limitado por construção.

## Rever se

O volume passar do plano gratuito do Langfuse, ou o custo mensal passar de US$ 10 por dois meses.
