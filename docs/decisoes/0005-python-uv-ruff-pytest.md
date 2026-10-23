# ADR 0005: Python 3.12 com uv, ruff, mypy, pytest e poe

- Status: aceita
- Data: 2026-10-12

## Contexto

O projeto vai ser construído com muita ajuda de agentes de IA. Quanto mais rápido e rígido o
retorno (tipos, lint e testes), mais seguro é aceitar código gerado. O ambiente precisa funcionar
igual no Windows, no Linux da Lambda e no CI.

## Decisão

- Python 3.12, a mesma versão do runtime da Lambda.
- uv para ambiente, dependências e `uv.lock` versionado.
- ruff para lint e formatação; mypy em modo strict; pytest com pytest-socket (sem rede), respx e moto.
- pydantic para contratos de dados; httpx para HTTP.
- poethepoet para as tarefas (`uv run poe check`, `build`, `deploy`), porque Makefile não roda nativo no Windows.
- CI no GitHub Actions rodando `uv run poe check`; Dependabot mensal; pre-commit opcional.

## Alternativas consideradas

- Poetry ou pip-tools: mais lentos e com mais configuração que o uv.
- black, isort e flake8: o ruff cobre os três com uma ferramenta.
- Makefile: não funciona sem instalar nada no Windows.

## Consequências

- `uv sync` e `uv run poe check` deixam qualquer máquina pronta e verificada.
- Tipagem estrita cobra disciplina, e em troca pega erro de código gerado antes do teste.

## Rever se

O runtime `python3.13` virar o padrão das bibliotecas do projeto, ou o uv deixar de ser mantido.
