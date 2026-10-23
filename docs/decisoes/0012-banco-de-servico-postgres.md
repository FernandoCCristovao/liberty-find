# ADR 0012: Banco de serviço e busca: Postgres no Neon, com pgvector e busca textual

- Status: aceita (região do Neon revista pelo [ADR 0024](0024-conta-aws-experiencia-nova-us-east-2.md))
- Data: 2026-10-20

## Contexto

O matching precisa, em menos de um segundo: filtros duros (país, modelo de trabalho, salário,
idioma), busca por texto, busca por vetor e combinação dos resultados. O app precisa de
transações para perfis e feedback, e de isolamento por usuário. Escala do MVP: 10^4 a 10^5 vagas
ativas, dezenas a centenas de usuários. O lago (Athena) responde em segundos e cobra por consulta:
serve para análise, não para o usuário esperando a página.

Opções e custos conferidos em 2026-10-20:

| Opção | Custo | Observação |
| --- | --- | --- |
| Postgres no Neon, plano gratuito | US$ 0 (1 GB por projeto, 100 horas de computação por mês, desliga sozinho após 5 min parado) | pgvector, branches para dev e CI, sem VPC |
| Postgres no Supabase, plano gratuito | US$ 0 (500 MB) | Pausa após 7 dias sem uso; traz autenticação junto |
| Aurora Serverless v2 com pausa em 0 ACU | Cerca de US$ 3,60 por mês com 60 horas ativas, mais armazenamento | Volta da pausa em cerca de 15 s; o cluster vive numa VPC, e o Lambda pode usar a Data API sem entrar nela |
| RDS PostgreSQL db.t4g.micro | Cerca de US$ 12 por mês, mais US$ 3,65 de IPv4 público | Servidor ligado o tempo todo |
| DynamoDB com S3 Vectors | Quase zero | Sem SQL, sem busca híbrida e sem isolamento por linha |
| OpenSearch Serverless | A partir de cerca de US$ 175 por mês na versão clássica | Melhor busca textual, custo fora do orçamento |
| Aurora DSQL | Cota gratuita | Sem suporte documentado a pgvector |

Fontes: [Neon](https://neon.com/pricing), [Supabase](https://supabase.com/pricing),
[Aurora em pausa](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html),
[VPC e IPv4](https://aws.amazon.com/vpc/pricing/), [OpenSearch](https://aws.amazon.com/opensearch-service/pricing/).

O PostgreSQL é o banco mais usado entre desenvolvedores (55,6% na
[pesquisa do Stack Overflow 2025](https://survey.stackoverflow.co/2025/technology/)), e nenhum banco
vetorial dedicado aparece em mais de 6% dos anúncios de engenharia de IA analisados.

## Decisão

- **Postgres no Neon (plano gratuito, região AWS `us-east-1`)** como índice de vagas e banco do app.
- **Busca:** `pgvector` com índice HNSW em `halfvec` + busca textual nativa (`tsvector`), combinadas
  por Reciprocal Rank Fusion (k = 60) numa função SQL
  ([pgvector](https://github.com/pgvector/pgvector), [RRF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)).
- **Acesso:** `psycopg` com SQL padrão numa camada fina (`liberty_find.serving`), sem recurso
  exclusivo do Neon. Trocar para Aurora ou RDS é trocar a string de conexão.
- **Esquema por migrações versionadas** no repositório; branch do Neon para desenvolvimento e CI.
- **Isolamento:** row-level security nas tabelas de usuário, com o papel do app sem ser dono das
  tabelas ([ADR 0018](0018-privacidade-desde-o-desenho.md)).
- **O índice é derivado:** a sincronização diária reconstrói as vagas ativas a partir da camada de
  ouro do lago.

## Alternativas consideradas

- **Supabase:** tudo em um (banco, autenticação, armazenamento), mas a pausa por inatividade e o
  limite de 500 MB pesam mais que a autenticação incluída.
- **Aurora Serverless v2:** a opção para manter tudo na AWS; perde pelo custo e pelos 15 s de volta
  da pausa na primeira visita.
- **Banco vetorial dedicado (Pinecone, Qdrant):** um fornecedor a mais sem ganho nesta escala, e a
  busca textual ficaria em outro lugar.
- **S3 Vectors:** ótimo para vetores frios e baratos, fraco para busca interativa com filtros e
  texto.

## Consequências

- Um banco só para vagas ativas, perfis e feedback, com custo zero.
- Um fornecedor fora da AWS, gerenciado no Terraform pelo provider do Neon
  ([ADR 0016](0016-terraform.md)).
- Depois de 5 minutos parado, o banco desliga sozinho e a consulta seguinte espera ele voltar; no
  plano gratuito esse comportamento não pode ser desligado.

## Rever se

O índice passar de 1 GB ou de 100 horas de computação por mês, a latência piorar para o usuário,
surgir exigência de manter tudo na AWS (aí Aurora Serverless v2 com Data API), ou o Neon mudar o
plano gratuito.
