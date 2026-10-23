# ADR 0004: Infraestrutura como código com AWS SAM

- Status: substituída pelo [ADR 0016](0016-terraform.md)
- Data: 2026-10-12

## Contexto

Toda a infraestrutura precisa ser reproduzível com um comando, versionada no Git e simples o
bastante para um projeto de uma pessoa, com a maior parte em Lambda e serviços gerenciados.

## Decisão

AWS SAM: um `template.yaml` (CloudFormation com a transformação do SAM) e um `samconfig.toml`
sem nada pessoal. Build com `sam build` a partir de `src/requirements.txt`, gerado do `uv.lock`
(`uv run poe build`). Validação no CI com `cfn-lint`. Parâmetros pessoais, como o e-mail de
alerta, entram no deploy pelo `.env`.

## Alternativas consideradas

- AWS CDK: mais poder de abstração, mas mais conceitos e código para o tamanho do projeto.
- Terraform: padrão de mercado, mas fora do ecossistema AWS e com estado para gerenciar.
- Console: rápido no começo, impossível de reproduzir e revisar.

## Consequências

- `sam build`, `sam deploy` e `sam delete` cobrem o ciclo de vida inteiro.
- O build no Windows baixa rodas Linux compatíveis; se uma dependência compilada falhar,
  `sam build --use-container` resolve com Docker.

## Rever se

O template passar de cerca de 600 linhas ou precisar de lógica que o YAML não expressa bem (aí CDK).
