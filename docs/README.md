# Base de conhecimento

Tudo o que uma pessoa ou um agente de IA precisa para construir e operar o Liberty Find. Cada
arquivo trata de um assunto; o código e estes textos mudam juntos, no mesmo commit.

| Quero | Leia |
| --- | --- |
| Entender o produto, os princípios e as metas | [produto.md](produto.md) |
| Ver como as peças se ligam e qual é a stack | [arquitetura.md](arquitetura.md) |
| Saber de onde vêm os dados, o que pode e o que não pode | [dados/fontes.md](dados/fontes.md) |
| Saber o formato de cada arquivo e tabela | [dados/contratos.md](dados/contratos.md) |
| Mexer na extração com LLM | [dados/extracao.md](dados/extracao.md) |
| Tratar dado pessoal | [privacidade.md](privacidade.md) |
| Implementar a próxima tarefa | [marcos/](marcos/README.md) (o primeiro marco não concluído) |
| Entender por que algo é como é | [decisoes/](decisoes/README.md) |
| Publicar, ver custo ou investigar uma falha | [operacao.md](operacao.md) |
| Seguir o padrão de código, teste e commit | [convencoes.md](convencoes.md) |
| Entender um termo | [glossario.md](glossario.md) |

## Como usar com IA

O [AGENTS.md](../AGENTS.md) na raiz é lido primeiro por qualquer agente. Pedidos que funcionam bem:

- "Leia o AGENTS.md e a tarefa 1.3 de docs/marcos/marco-1-coleta.md. Implemente a fonte Lever:
  teste primeiro, depois o código, e rode `uv run poe check`."
- "Proponha um ADR para a hospedagem do MCP remoto, no modelo de docs/decisoes/README.md, com as
  alternativas, os custos e o que a avaliação mostrou."
- "Revise o diff atual contra as regras do AGENTS.md, os contratos de docs/dados/contratos.md e o
  checklist de docs/privacidade.md."

## Regras de manutenção

- Um fato mora num lugar só; os outros arquivos apontam para ele.
- ADR aceito não se edita: um novo ADR o substitui e os dois apontam um para o outro.
- Cada marco marca as tarefas conforme fecham; o README da raiz mostra o estado.
- Documento desatualizado é bug: corrija no mesmo commit da mudança de código.
