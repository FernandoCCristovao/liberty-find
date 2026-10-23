# Marco 6: Assistente

**Objetivo:** um assistente que ajuda a montar o perfil, entender o encaixe com cada vaga e
preparar a candidatura, com toda ação externa nas mãos do usuário; medido por um conjunto fixo de
casos e protegido contra instruções escondidas em texto de vaga.

Decisão: [ADR 0022](../decisoes/0022-assistente-e-mcp-com-aprovacao.md).

## Tarefas (na ordem)

### [ ] 6.1 Assistente em LangGraph

- Fazer: grafo com modelo do Bedrock e três fluxos: conversa para montar ou refinar o perfil,
  explicação de encaixe e lacunas para uma vaga, e rascunhos de candidatura (resumo de encaixe,
  carta, respostas de formulário). Ferramentas só de leitura sobre o índice e o perfil; salvar o
  perfil passa por confirmação na tela.
- Aceite: nenhuma ferramenta com efeito externo; toda ação interna passa por confirmação.

### [ ] 6.2 Avaliação do assistente

- Fazer: `evals/assistant/` com 30 casos e respostas de referência; asserções automáticas para o
  que é verificável e LLM como juiz para o resto, conferido contra notas humanas em 10 casos;
  latência e custo por caso.
- Aceite: tabela no README; o juiz concorda com as notas humanas na maior parte dos 10 casos, ou o
  critério do juiz é refeito.

### [ ] 6.3 Proteções

- Fazer: casos de teste com vagas que tentam dar instruções ao modelo; separação de instruções e
  dados no prompt; saída validada.
- Aceite: nenhum caso de teste muda o comportamento do assistente.

### [ ] 6.4 MCP remoto

- Fazer: ADR da hospedagem (AgentCore Gateway ou Lambda), com autenticação e limite de uso; as mesmas
  ferramentas só de leitura do Marco 4.
- Aceite: um cliente MCP remoto usa a busca com autenticação.

### [ ] 6.5 Fechamento

- Aceite: README final com links, diagrama, avaliações, custos e limitações; tag `v1.0.0`.
