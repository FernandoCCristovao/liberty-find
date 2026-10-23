# ADR 0024: Conta AWS na experiência nova de projetos, em us-east-2

- Status: aceita
- Data: 2026-10-23
- Substitui: a região do [ADR 0008](0008-arquitetura-em-camadas.md) (`us-east-1`) e o que dependia
  dela nos ADRs [0012](0012-banco-de-servico-postgres.md) e [0018](0018-privacidade-desde-o-desenho.md)

## Contexto

A conta do projeto foi criada pelo cadastro novo da AWS (setembro de 2026). Nele, uma conta é um
"projeto" administrado em https://settings.aws.com, com login por provedor (Google, GitHub, Apple ou
Amazon) e um AWS Builder ID no lugar do usuário raiz
([AWS](https://aws.amazon.com/blogs/aws/aws-reimagines-the-getting-started-experience/)). Fatos que
pesam, conferidos em 2026-10-23:

- A região é atribuída pelo país do endereço e não muda: o Brasil fica em `us-east-2` (Ohio)
  ([regiões](https://docs.aws.amazon.com/accounts/latest/reference/project-regions.html)).
- Políticas geridas pela AWS (SCPs e RCPs) negam quase tudo fora da região do projeto. Em
  `us-east-1` e `us-west-2` sobram serviços globais e a inferência do Bedrock
  ([políticas](https://docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html)).
- Não há IAM Identity Center, e a política nega as ações `iam:*Provider*`, o que inclui criar o
  provedor OIDC do GitHub. O login da pessoa e o da CLI são pelo `aws login`, com credencial
  temporária.
- O plano gratuito não gera cobrança e inclui Lambda, S3, Athena, Glue, Step Functions,
  EventBridge, SNS, Bedrock, CloudFormation, Budgets e Cost Explorer. O pago acrescenta serviços e
  permite um limite de gasto mensal (a partir de US$ 20) que pausa o projeto em vez de cobrar mais
  ([serviços](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html)).
- "Ativar recursos avançados" libera Identity Center, outras regiões e o controle das políticas,
  mas é irreversível, exige o plano pago e acaba com o limite de gasto
  ([ativação](https://docs.aws.amazon.com/accounts/latest/reference/activate-advanced-features.html)).

## Decisão

- **Conta:** o projeto do cadastro novo, no plano gratuito enquanto ele cobrir o que o projeto usa.
  No pago, o limite de gasto mensal fica ligado (o mínimo da AWS, US$ 20) como teto rígido, além do
  alerta de US$ 10 no AWS Budgets, se a conta permitir.
- **Região:** `us-east-2` para tudo no MVP. O Bedrock é chamado pelos perfis de inferência dos EUA
  (prefixo `us.`), que a política exclui do bloqueio de região; o teste do Nova Lite na tarefa 1.1
  confirma. O Postgres no Neon fica na região AWS `us-east-2`.
- **Acesso:** `aws login` com o perfil `liberty-find`, sem chave fixa em lugar nenhum.
- **Deploy:** da máquina do mantenedor, com aprovação humana, até haver caminho para o CI sem chave
  fixa. Antes da tarefa 2.5, um ADR decide entre ativar os recursos avançados e outra saída.
- **Dados pessoais ([ADR 0018](0018-privacidade-desde-o-desenho.md)):** `us-east-2` no beta
  fechado. Antes do cadastro público, reavaliar a região, sabendo que outra região exige ativar os
  recursos avançados.

## Alternativas consideradas

- **Conta clássica pelo cadastro avançado, em `us-east-1`:** casa com tudo o que os ADRs previam
  (Identity Center, OIDC e região livre), mas pede mais configuração e não tem teto rígido de gasto.
- **Ativar os recursos avançados já:** irreversível, acaba com o limite de gasto e não é necessário
  para o Marco 1.

## Consequências

- Custo zero no plano gratuito e teto rígido no pago; menos configuração (sem Identity Center).
- A região deixa de ser escolha: o que só existe em outra região fica de fora ou exige ativar os
  recursos avançados.
- O deploy pelo GitHub Actions com OIDC (tarefa 2.5) fica pendente.
- A descoberta de empresas lê o índice do Common Crawl, que fica em `us-east-1`. Se a política
  negar, a alternativa é a API do índice ([fontes](../dados/fontes.md#descoberta-de-empresas)).
- O certificado do ACM para um domínio próprio no CloudFront fica em `us-east-1`; a tarefa 3.2
  confere se a política permite.
- Serviços que podem estar fora da lista do plano gratuito (SSM Parameter Store, ECR, SQS, Cognito
  e Service Quotas) são conferidos quando uma tarefa precisar deles.

## Rever se

Uma ação necessária for negada pela política da conta (OIDC na 2.5, ACM na 3.2 ou um serviço fora
da lista), o projeto precisar de outra região para dados pessoais, ou o plano pago exigir ativar os
recursos avançados. Os caminhos são ativar os recursos avançados (irreversível) ou migrar para uma
conta clássica, recriando a infraestrutura pelo Terraform.
