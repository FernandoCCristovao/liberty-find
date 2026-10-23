# Convenções

## Nomes

| O quê | Nome |
| --- | --- |
| Produto | Liberty Find (nome de trabalho até a checagem de marca do Marco 3) |
| Repositório | `liberty-find` |
| Pacote Python | `liberty_find` |
| Comando local | `liberty` |
| Banco no Glue e no Athena | `liberty_find` |
| Workgroup do Athena e prefixo de recursos | `liberty-find` |
| Tag em todo recurso da AWS | `project=liberty-find` |

## Código

- Python 3.12, com tipos em tudo; o mypy roda em modo strict.
- Código, nomes, colunas e valores de categoria em inglês. Documentação, mensagens de log,
  mensagens de erro para pessoas e commits em português.
- Contratos de dados em pydantic (`models.py`); nada de dicionário solto atravessando módulos.
- Núcleo puro, I/O nas bordas: `normalize` não faz rede; `fetch_raw`, os destinos de gravação e os
  handlers fazem. Isso é o que torna tudo testável sem rede.
- Handlers da Lambda são finos: montam dependências e chamam o núcleo. Orquestrador também não tem
  lógica ([ADR 0011](decisoes/0011-orquestracao-step-functions-airflow.md)).
- Módulos conversam por contrato: um módulo não importa o interior de outro.
- Erro de uma empresa não derruba a coleta: registra no relatório de saúde e segue.
- Logs: Powertools `Logger` nas Lambdas e `logging` padrão no núcleo. Nunca logar a descrição de
  uma vaga nem dados pessoais ([privacidade.md](privacidade.md)).
- Prompts versionados em arquivo, com `PROMPT_VERSION`; esquemas com `SCHEMA_VERSION`.
- Lint e formatação com ruff (regras no `pyproject.toml`), linha de até 100 caracteres.

## Testes

- pytest. Unitário nunca acessa a rede: o `pytest-socket` bloqueia.
- HTTP com respx, S3 com moto e Bedrock com `botocore.stub.Stubber`.
- Fixtures sintéticas em `tests/fixtures/`, com a mesma forma da resposta real e conteúdo
  inventado. Nunca texto real de vaga nem dado real de pessoa.
- Um teste por comportamento, com nome que diz o comportamento
  (`test_one_failing_board_does_not_stop_the_run`).
- Bug corrigido ganha um teste que falhava antes da correção.
- Avaliações de LLM ficam em `evals/`, separadas dos testes unitários, e rodam quando prompt,
  modelo, esquema ou código de enriquecimento mudam.

## Commits e branches

- Conventional Commits em português: `tipo(escopo): descrição no imperativo`.
  - Tipos: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, `ci`.
  - Escopos: `fontes`, `coleta`, `extracao`, `infra`, `dbt`, `matching`, `site`, `canal`, `app`,
    `agente`, `boards`, `evals`, `docs`.
  - Exemplos: `feat(fontes): adiciona a Lever`, `fix(coleta): trata token removido`.
- Uma branch curta por tarefa (`marco-1/lever`), pull request com o modelo do repositório e merge
  com squash depois do CI verde.
- Commits ao longo do tempo, pequenos: o histórico conta a história do projeto.

## Versões e releases

- Uma tag por marco: `v0.1.0` a `v0.5.0` (Marcos 1 a 5) e `v1.0.0` (Marco 6).
- Cada release lista o que entrou e os números do marco (vagas por dia, acerto, custo).

## AWS e infraestrutura

- Tudo pelo Terraform em `infra/` (o `template.yaml` do SAM vale até a tarefa 1.2). No console, só
  conta, limite de gasto, orçamento e consultas.
- Região `us-east-2`, a da conta ([ADR 0024](decisoes/0024-conta-aws-experiencia-nova-us-east-2.md)); tag
  `project=liberty-find` em tudo.
- Papel do IAM com o mínimo necessário; nada de chave fixa, nem na máquina (`aws login`) nem no CI
  (OIDC, quando a conta permitir).
- Segredos de serviços de fora da AWS no SSM Parameter Store, nunca no repositório.

## Dependências

- `uv add <pacote>` (ou `uv add --dev`); o `uv.lock` vai no commit.
- Dependabot abre atualizações mensais; o CI decide se entram.
- Antes de adicionar uma dependência, veja se a biblioteca padrão ou uma já presente resolve.

## Documentação

- Português, frases curtas, sem travessão.
- Um fato num lugar só; os outros arquivos apontam para ele.
- Mudou o código, mudou o documento no mesmo commit.
- Texto público não afirma o que o projeto ainda não faz.
