# Decisões de arquitetura (ADRs)

Cada decisão que muda a arquitetura, a stack ou um contrato importante vira um registro curto.
ADR aceito não se edita: se a decisão mudar, um ADR novo o substitui e os dois apontam um para o
outro (o antigo só ganha a linha de status com o ponteiro).

| ADR | Decisão | Status |
| --- | --- | --- |
| [0001](0001-aws-serverless.md) | AWS, arquitetura serverless | substituída pelo 0008 |
| [0002](0002-s3-athena-glue.md) | S3 em JSON Lines, Glue Data Catalog e Athena | substituída pelo 0010 |
| [0003](0003-extracao-bedrock-nova-lite.md) | Extração com Bedrock e Amazon Nova Lite, via tool use | substituída pelo 0013 |
| [0004](0004-iac-aws-sam.md) | Infraestrutura como código com AWS SAM | substituída pelo 0016 |
| [0005](0005-python-uv-ruff-pytest.md) | Python 3.12 com uv, ruff, mypy, pytest e poe | aceita |
| [0006](0006-somente-apis-publicas.md) | Só APIs públicas de ATS; descrição nunca publicada | substituída pelo 0009 |
| [0007](0007-paineis-fora-da-aws.md) | Power BI e Streamlit Community Cloud para os painéis | substituída pelo 0019 |
| [0008](0008-arquitetura-em-camadas.md) | Arquitetura em camadas, nuvem AWS e monólito modular | aceita |
| [0009](0009-fontes-por-permissao.md) | Fontes por nível de permissão, com política de exibição por fonte | aceita |
| [0010](0010-lakehouse-iceberg-dbt.md) | Lakehouse: bronze em JSON Lines, prata e ouro em Iceberg com dbt-athena | aceita |
| [0011](0011-orquestracao-step-functions-airflow.md) | Step Functions em produção; Airflow 3 local para comparação | aceita |
| [0012](0012-banco-de-servico-postgres.md) | Postgres no Neon, com pgvector e busca textual | aceita |
| [0013](0013-extracao-v2-sinais-de-liberdade.md) | Extração v2: sinais de liberdade e modelo escolhido por avaliação | aceita |
| [0014](0014-embeddings-multilingues.md) | Embeddings multilíngues escolhidos por avaliação | aceita |
| [0015](0015-app-web-fastapi-htmx-cognito.md) | App web: FastAPI no Lambda, HTMX e Cognito | aceita |
| [0016](0016-terraform.md) | Infraestrutura como código com Terraform | aceita |
| [0017](0017-licenca-fair-source.md) | Licença FSL-1.1-ALv2 e o que fica fora do repositório | aceita |
| [0018](0018-privacidade-desde-o-desenho.md) | Privacidade desde o desenho (LGPD) | aceita |
| [0019](0019-superficies-publicas.md) | Site estático, Telegram e newsletter; Streamlit só interno | aceita |
| [0020](0020-observabilidade-avaliacao-custo.md) | Observabilidade, avaliação contínua e proteção de custo | aceita |
| [0021](0021-fora-do-mvp.md) | Tecnologias deliberadamente fora do MVP | aceita |
| [0022](0022-assistente-e-mcp-com-aprovacao.md) | Assistente e MCP, com toda ação externa aprovada pelo usuário | aceita |
| [0023](0023-taxonomia-de-competencias-esco.md) | Taxonomia de competências: ESCO com extensão própria | aceita |

Próximos ADRs previstos: hospedagem do MCP remoto (Marco 6) e, se o gatilho disparar, qualquer item
do [ADR 0021](0021-fora-do-mvp.md).

## Como decidir

1. Escreva o contexto com fatos verificáveis e a data em que foram conferidos.
2. Liste as alternativas reais, cada uma com o motivo de não ter sido escolhida.
3. Diga o que fica mais fácil, o que fica mais difícil e o que passa a ser obrigatório.
4. Termine com um gatilho observável para rever. "Se não funcionar bem" não vale.

## Modelo

Arquivo `NNNN-titulo-curto.md`, numeração sequencial:

```markdown
# ADR NNNN: título

- Status: proposta | aceita | substituída pelo ADR XXXX
- Data: AAAA-MM-DD
- Substitui: ADR YYYY (quando houver)

## Contexto
O que força a decisão, com fatos e fontes.

## Decisão
O que foi decidido.

## Alternativas consideradas
- Alternativa: por que não.

## Consequências
O que fica mais fácil, o que fica mais difícil e o que passa a ser obrigatório.

## Rever se
Evento observável que reabre a decisão.
```
