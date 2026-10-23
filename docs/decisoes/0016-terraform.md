# ADR 0016: Infraestrutura como código com Terraform

- Status: aceita (migração na tarefa 1.2 do Marco 1, antes do primeiro deploy)
- Data: 2026-10-20
- Substitui: [ADR 0004](0004-iac-aws-sam.md)

## Contexto

O ADR 0004 escolheu o AWS SAM pela velocidade num projeto feito só de Lambda. Três coisas mudaram:

1. **A stack passou a ter peças fora da AWS:** o Postgres no Neon ([ADR 0012](0012-banco-de-servico-postgres.md))
   e, mais adiante, configurações do GitHub e do DNS. O SAM só descreve recursos da AWS.
2. **Adoção no mercado:** numa amostra de 32 vagas de dados e IA no Brasil e em Portugal com
   etiquetas de tecnologia (Built In, 2026-10-20), Terraform aparece em 9, CloudFormation em 2 e
   SAM em nenhuma; Terraform aparece em cerca de 14% de 6.877 anúncios de engenharia de dados
   ([InterviewStack](https://interviewstack.io/blog/data-engineer-skills-companies-want-2026)) e é
   usado por 17,8% dos desenvolvedores ([Stack Overflow 2025](https://survey.stackoverflow.co/2025/technology/)).
3. **Nada foi publicado ainda:** trocar agora custa reescrever um template de cerca de 200 linhas;
   depois do primeiro deploy, custaria também importar o estado.

O Terraform tem licença BSL desde 2023, que restringe só quem oferece produto concorrente da
HashiCorp; o OpenTofu é a bifurcação aberta e compatível
([HashiCorp](https://www.hashicorp.com/blog/hashicorp-adopts-business-source-license),
[OpenTofu](https://opentofu.org/)).

## Decisão

- **Terraform** (1.11 ou mais novo, com o travamento nativo de estado no S3) para toda a
  infraestrutura, em `infra/`, com ambientes `dev` e `prod` e módulos só quando houver repetição real.
- **Estado no S3** com travamento nativo do backend (`use_lockfile = true`, sem tabela no DynamoDB),
  versionamento e criptografia no bucket de estado.
- **Pacote das Lambdas por script** (`uv run poe package`): `uv export` das dependências, instalação
  das rodas Linux para arm64 com `uv pip install --target` e um zip por função. A Lambda do dbt usa
  imagem de contêiner (ECR).
- **CI:** `terraform fmt -check`, `terraform validate` e `tflint` em todo pull request. `plan` e
  `apply` só com aprovação humana (papel da AWS por OIDC, sem chave fixa).
- **Transição:** o `template.yaml` e o `cfn-lint` continuam até a migração ficar pronta; depois saem
  no mesmo commit em que o Terraform passa a ser a única fonte.

## Alternativas consideradas

- **Manter o SAM:** pronto e o mais rápido para Lambda, mas só cobre a AWS e quase não aparece nas
  vagas.
- **AWS CDK:** mais abstração, também só AWS, mais código para manter.
- **OpenTofu:** mesma linguagem e mesmo fluxo; é a saída se a licença do Terraform passar a pesar.
- **Pulumi:** infraestrutura em Python, com pouca adoção nas vagas-alvo.

## Consequências

- Uma ferramenta nova para dominar (estado, `plan` e `apply`, providers), toda a infraestrutura num
  lugar só, incluindo o Neon.
- O empacotamento das Lambdas passa a ser responsabilidade do projeto (script testado no CI).
- O `sam local` deixa de ser o caminho de teste local; a CLI `liberty` já cobre a coleta local.

## Rever se

A licença do Terraform passar a afetar este uso, ou o empacotamento por script der mais trabalho
que o ganho (aí avaliar o SAM CLI com o gancho de Terraform só para o build).
