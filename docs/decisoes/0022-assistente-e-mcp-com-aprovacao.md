# ADR 0022: Assistente e MCP, com toda ação externa aprovada pelo usuário

- Status: aceita (MCP local no Marco 4; assistente no Marco 6)
- Data: 2026-10-20

## Contexto

A visão do produto inclui um assistente que ajuda na jornada: montar o perfil, entender o encaixe
com cada vaga e preparar a candidatura. A ideia de um agente que se candidata ou contata
recrutadores sozinho esbarra em:

- **Termos de uso:** o LinkedIn proíbe automação e robôs (Contrato do Usuário, seção 8.2); a maioria
  dos portais também.
- **Dado pessoal de terceiros:** contato de recrutador é dado pessoal, e mensagem não solicitada
  precisa de base legal.
- **Reputação do usuário:** mensagens ou candidaturas em massa saem com o nome dele.
- **Regulação:** no AI Act europeu, sistemas para recrutamento e seleção, inclusive para "colocar
  anúncios de vaga direcionados" e avaliar candidatos, são de alto risco (Anexo III, ponto 4a), com
  obrigações a partir de dezembro de 2027; uma ferramenta do lado de quem procura vaga, que só busca
  e explica, tende a ficar fora desse grupo ([AI Act](https://artificialintelligenceact.eu/annex/3/)).
- **Segurança:** a descrição da vaga é texto de terceiros e pode tentar instruir o modelo (injeção de
  prompt, primeiro item do OWASP Top 10 para aplicações com LLM).

Por outro lado, o Model Context Protocol (MCP) cresce rápido em vagas de IA e é barato de oferecer:
um servidor que expõe a busca do Liberty Find a qualquer assistente compatível.

## Decisão

- **Princípio:** a IA prepara, a pessoa decide e envia. Nenhuma ação externa em nome do usuário
  (candidatura, mensagem, convite, contato) é executada pelo sistema.
- **Assistente (Marco 6):** LangGraph com modelo do Bedrock. Ferramentas de leitura sobre o índice e
  o perfil; ações internas (salvar perfil, marcar vaga) só com confirmação explícita na tela;
  rascunhos (resumo de encaixe, carta, respostas de formulário) entregues para o usuário revisar.
- **Servidor MCP só de leitura:** `search_jobs`, `get_job` e `explain_fit`, primeiro local, por
  stdio (Marco 4); `list_saved` quando houver contas (Marco 5); depois remoto, com autenticação e
  limite de uso (Marco 6, hospedagem decidida em ADR próprio).
- **Proteções:** instruções e dados separados no prompt; nenhuma ferramenta com efeito colateral
  alcançável a partir de conteúdo de vaga; saída validada; conjunto de avaliação com tentativas de
  injeção.
- **Fora do escopo:** recursos para empregadores (ranquear candidatos, anúncios segmentados).

## Alternativas consideradas

- **Agente autônomo de candidatura:** categoria saturada e mal vista, com risco jurídico e de
  reputação.
- **Agente sem framework:** possível; o LangGraph entra pelo controle explícito de estado e pelas
  interrupções para aprovação humana, que são o centro deste desenho.

## Consequências

- O valor do assistente está em economizar o tempo de leitura e de preparação, não em agir sozinho.
- Toda ferramenta nova do assistente declara se é leitura, ação interna com confirmação ou proibida.

## Rever se

Surgir canal oficial e base legal para uma ação externa específica, pedida pelo usuário e aprovada
caso a caso.
