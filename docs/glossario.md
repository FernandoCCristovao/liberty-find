# Glossário

| Termo | Significado aqui |
| --- | --- |
| ATS | Sistema de recrutamento que a empresa usa para publicar vagas (Greenhouse, Lever, Ashby, Workable) |
| Board, token | A página de vagas de uma empresa num ATS; o token é o identificador dela na URL e na API |
| Fonte | Uma origem de vagas com permissão para coleta, implementada em `src/liberty_find/sources/` |
| Nível da fonte (A a D) | Grau de permissão de uma fonte: API pública, agregador com regras, parceria ou fora ([dados/fontes.md](dados/fontes.md)) |
| Política de exibição | Regras de cada fonte sobre atribuição, link, login e SEO, aplicadas em código |
| Vaga (posting) | Uma oportunidade publicada; no código, `JobPosting` |
| Retrato do dia | O arquivo com todas as vagas abertas num dia de coleta (`postings/dt=...`) |
| `dt` | Data UTC da coleta; é a partição das tabelas do bronze |
| Bruto (raw) | A resposta da fonte exatamente como veio, guardada por 90 dias |
| Bronze, prata, ouro | Camadas do lago: dado como chegou; dado limpo e com histórico; dado pronto para consumo |
| Iceberg | Formato aberto de tabela sobre arquivos no S3, com atualização linha a linha e histórico |
| Normalizar | Converter a resposta de cada fonte para o mesmo formato (`JobPosting`) |
| `content_hash` | Assinatura do título e da descrição; muda quando a vaga é editada |
| Extração | Uso de LLM para preencher campos estruturados a partir do texto da vaga |
| Sinal de liberdade | Campo extraído que diz algo sobre liberdade de lugar, de dinheiro ou de tempo, sempre com evidência |
| Selo de elegibilidade | Indicação derivada de que uma vaga remota está "aberta", "não aberta" ou "a confirmar" para quem mora no Brasil ou em Portugal |
| Evidência | Trecho curto da vaga que sustenta um sinal |
| ESCO | Classificação europeia de competências e ocupações, em 28 idiomas, usada para normalizar competências ([ADR 0023](decisoes/0023-taxonomia-de-competencias-esco.md)) |
| Auditoria de rótulos | Rotulagem à mão de uma amostra para medir quais sinais aparecem nas vagas antes de fechar o esquema |
| Família da função | Classificação do trabalho: IA, engenharia de dados, ciência de dados, BI, analytics engineering, infraestrutura, automação, software ou outra |
| Perfil de busca | O que uma pessoa quer, em filtros e em texto livre (`SearchProfile`) |
| Índice de vagas | As vagas ativas no Postgres, com texto para busca e embeddings, derivadas da camada de ouro |
| Embedding | Vetor que representa o significado de um texto, usado para busca semântica |
| Busca híbrida | Combinação de busca por texto e busca por vetor |
| RRF | Reciprocal Rank Fusion: forma simples e robusta de combinar duas listas ordenadas |
| nDCG@10 | Métrica de qualidade das 10 primeiras posições de um ranking, comparada com julgamentos humanos |
| Relatório de saúde | `health.json`: estado de cada empresa na coleta do dia |
| Workgroup | Configuração do Athena com limite de leitura por consulta e local dos resultados |
| Projeção de partições | Recurso do Athena que acha as partições pelo padrão da chave, sem crawler |
| Rótulo humano | Resposta certa anotada à mão, usada para medir a extração, o matching e o assistente |
| Marco | Etapa do projeto que vale sozinha e fecha com critério de aceite (`docs/marcos/`) |
| ADR | Registro de decisão de arquitetura (`docs/decisoes/`) |
| MCP | Model Context Protocol: padrão para expor ferramentas a assistentes de IA |
| Fair source | Código público que pode ser usado e estudado, mas não oferecido como produto concorrente por um prazo (FSL) |
