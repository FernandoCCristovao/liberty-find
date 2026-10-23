# ADR 0021: Tecnologias deliberadamente fora do MVP

- Status: aceita
- Data: 2026-10-20

## Contexto

Várias tecnologias aparecem com frequência em vagas de dados e de IA, mas não resolvem um problema
que o Liberty Find tem hoje. Usá-las só por estarem em alta deixaria o sistema mais caro, mais lento
de construir e mais difícil de explicar. Registrar o "não, por enquanto" com o gatilho de entrada é
tão importante quanto registrar o "sim".

## Decisão

| Tecnologia | Por que não agora | Entra quando |
| --- | --- | --- |
| Spark (Glue, EMR, Databricks) | O volume é de dezenas de milhares de linhas; Athena e dbt resolvem em segundos. O plano gratuito do Databricks proíbe uso comercial | Processamento diário passar de cerca de 10 GB, ou surgir tarefa que SQL não expressa bem em escala (por exemplo, deduplicação por similaridade no histórico inteiro) |
| Kafka, Flink, streaming | A coleta é diária e as fontes não emitem eventos | Uma fonte passar a empurrar eventos, ou alerta em minutos virar requisito do produto |
| Kubernetes | Lambda cobre toda a carga; um cluster tem custo fixo e operação | Carga contínua que não caiba em Lambda ou contêiner sob demanda |
| OpenSearch | Postgres com pgvector e busca textual atende 10^5 documentos; o OpenSearch tem custo mínimo alto | Volume ou recursos de busca que o Postgres não sustente |
| Airflow gerenciado (MWAA, Astronomer) | Centenas de dólares por mês | Ver [ADR 0011](0011-orquestracao-step-functions-airflow.md) |
| Redshift, Snowflake, BigQuery | Cobram capacidade mínima ou tiram o projeto da AWS | Volume analítico que o Athena não sustente |
| Azure (OpenAI, AI Foundry, Data Factory, Fabric) | A AWS é o núcleo; duas nuvens dobram o trabalho de infraestrutura e de controle de custo | Uma vaga-alvo exigir Azure: demonstração com Azure OpenAI pela interface de LLM do [ADR 0013](0013-extracao-v2-sinais-de-liberdade.md), sem mudar o resto |
| TypeScript e Next.js | Uma linguagem só até o app ter usuários; a interface pesa pouco nas vagas-alvo | Ver [ADR 0015](0015-app-web-fastapi-htmx-cognito.md) |
| Fine-tuning e modelos próprios em servidor | Modelos de prateleira com bom prompt e avaliação devem bastar; servir modelo custa caro | A avaliação mostrar um teto que prompt e troca de modelo não resolvem |
| Candidatura automática e mensagens em massa | Termos de uso das plataformas, risco à reputação do usuário e dado pessoal de terceiros | Não está no plano ([ADR 0022](0022-assistente-e-mcp-com-aprovacao.md)) |

## Alternativas consideradas

- **Incluir uma peça de cada só para cobrir mais tecnologias:** cobertura maior, custo e
  complexidade sem motivo, e uma resposta fraca para "por que isto está aqui?".

## Consequências

- Cada item tem gatilho observável; quando o gatilho disparar, entra com ADR próprio.
- A explicação de por que cada peça ficou de fora faz parte da documentação do projeto.

## Rever se

Qualquer gatilho da tabela disparar.
