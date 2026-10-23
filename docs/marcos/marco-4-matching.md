# Marco 4: Matching pessoal

**Objetivo:** dado um perfil de busca, um ranking de vagas com explicação (por que combina, o que
falta e o que merece atenção), medido contra julgamentos humanos e disponível por CLI e por MCP.

Decisões: [ADR 0012](../decisoes/0012-banco-de-servico-postgres.md),
[ADR 0014](../decisoes/0014-embeddings-multilingues.md),
[ADR 0023](../decisoes/0023-taxonomia-de-competencias-esco.md) e
[ADR 0022](../decisoes/0022-assistente-e-mcp-com-aprovacao.md).

## Tarefas (na ordem)

### [ ] 4.1 Perfil de busca

- Fazer: contrato `SearchProfile` em `models.py` (funções e títulos desejados, nível, competências
  obrigatórias e desejáveis, países onde pode trabalhar, fuso, salário mínimo com moeda e período,
  regimes aceitos, nível de inglês, idiomas, o que evitar, texto livre); leitor de YAML para uso
  local; normalização do texto livre por LLM em campos e num resumo em inglês.
- Aceite: testes do contrato e da normalização com respostas simuladas; um perfil real do autor em
  YAML fora do repositório.

### [ ] 4.2 Normalização de competências

- Fazer: ESCO (download da versão atual) mais a extensão própria de ferramentas em arquivo versionado;
  dicionário de apelidos; ligação de cada competência extraída a um identificador por embedding e
  limiar, com um modelo pequeno decidindo os casos duvidosos; tabela de apelidos em cache;
  atribuição da ESCO no site e no app.
- Aceite: 100 competências reais ligadas à mão conferem com a ligação automática em 90% ou mais; o
  mesmo identificador para formas em português, inglês e espanhol.

### [ ] 4.3 Índice no Postgres

- Fazer: projeto no Neon pelo Terraform; migrações versionadas (`postings` com `tsvector` e
  `halfvec`); Lambda de sincronização a partir de `active_postings`, com embeddings; branch do Neon
  para desenvolvimento e CI.
- Aceite: o índice reflete o ouro depois de cada execução; reconstruir do zero funciona com um
  comando.

### [ ] 4.4 Busca e explicação

- Fazer: filtros em SQL (elegibilidade, modelo de trabalho, salário com penalidade quando não
  informado, idiomas, exclusões); busca textual e por vetor combinadas por RRF numa função SQL;
  pontuação transparente (cobertura de competências pela taxonomia da tarefa 4.2, distância de nível,
  recência, salário); para as 10 primeiras, explicação estruturada por LLM a partir dos campos e das
  evidências, guardada por (versão do perfil, vaga, `content_hash`).
- Aceite: testes da pontuação e dos filtros; a explicação nunca cita algo que não esteja nos campos
  ou nas evidências.

### [ ] 4.5 Avaliação do matching

- Fazer: `evals/matching/` com 30 perfis e as 20 primeiras vagas de cada um julgadas à mão (boa,
  talvez, ruim); nDCG@10 e precisão@10; comparação entre só texto, só vetor, RRF e RRF com pontuação;
  comparação dos modelos de embedding.
- Aceite: tabela no README; a busca híbrida ganha da linha de base por palavra-chave, ou os ADRs 0012
  e 0014 são revistos.

### [ ] 4.6 CLI e servidor MCP local

- Fazer: `uv run liberty match --perfil <arquivo>` com a lista e as explicações; servidor MCP por
  stdio, só de leitura, com `search_jobs`, `get_job` e `explain_fit`.
- Aceite: o autor usa o próprio ranking na busca dele; um cliente MCP lista e usa as ferramentas.

### [ ] 4.7 Fechamento

- Aceite: README com o desenho do matching e a avaliação; tag `v0.4.0`.
