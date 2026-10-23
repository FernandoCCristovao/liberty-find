# Marcos

Cada marco vale sozinho, fecha com critério de aceite verificável e vira uma release. Não há datas:
um marco começa quando o anterior fecha. O MVP público é o Marco 3.

| Marco | Entrega | Release | Estado |
| --- | --- | --- | --- |
| [1. Coleta no ar](marco-1-coleta.md) | Conta e repositório, infra em Terraform, coleta diária de quatro fontes, descoberta de empresas, auditoria de rótulos e extração com o modelo escolhido por avaliação | v0.1.0 | em andamento |
| [2. Lakehouse e qualidade](marco-2-lakehouse.md) | dbt com Iceberg, deduplicação, vagas fechadas, orquestração no Step Functions, registro de empresas em escala, deploy com OIDC, avaliação contínua, Airflow local e insights | v0.2.0 | a fazer |
| [3. Canal público (MVP)](marco-3-canal-publico.md) | Site com vagas verificadas, Telegram e newsletter semanal, sem login, e a medição da demanda | v0.3.0 | a fazer |
| [4. Matching pessoal](marco-4-matching.md) | Perfil de busca, índice no Postgres, busca híbrida com explicação, avaliação e servidor MCP local | v0.4.0 | a fazer |
| [5. App beta](marco-5-app-beta.md) | Login, perfis salvos, alertas por e-mail, feedback e LGPD na prática | v0.5.0 | a fazer |
| [6. Assistente](marco-6-assistente.md) | Assistente com aprovação do usuário, avaliação, proteções e MCP remoto | v1.0.0 | a fazer |

Cada tarefa traz o que fazer e o critério de aceite. Ao concluir, marque a caixa no próprio arquivo,
no mesmo commit da entrega. Tarefas marcadas como "fora do caminho do MVP" podem ser feitas depois do
Marco 3 sem atrasar o canal público.

Depois do Marco 3, os números do canal (assinantes, cliques, vagas por semana) orientam a prioridade
dos marcos seguintes.
