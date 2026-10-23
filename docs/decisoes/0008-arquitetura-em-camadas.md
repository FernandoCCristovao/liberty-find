# ADR 0008: Arquitetura em camadas, nuvem AWS e monólito modular

- Status: aceita (a região foi substituída pelo [ADR 0024](0024-conta-aws-experiencia-nova-us-east-2.md))
- Data: 2026-10-20
- Substitui: [ADR 0001](0001-aws-serverless.md) (reafirma a AWS serverless com os dados de 2026)

## Contexto

O projeto deixou de ser um observatório com perguntas fixas e passou a ser o Liberty Find: cada
pessoa diz que tipo de vaga quer e a plataforma encontra, explica e avisa ([produto.md](../produto.md)).
Isso traz peças que o desenho anterior não tinha: perfil de busca, um banco para servir consultas
rápidas, busca semântica, notificações e, mais adiante, contas de usuário.

Restrições: uma pessoa construindo, de 6 a 10 horas por semana, orçamento perto de zero, e cada
marco precisa valer sozinho (funcionar, ser mostrável e não depender do próximo).

## Decisão

**Nuvem:** AWS como núcleo, com serviços sem servidor e cobrados por uso. Reafirma o ADR 0001 com os
dados de 2026-10-20: a AWS aparece em 62% das vagas de dados de empresas internacionais que contratam
no Brasil e em cerca de 40% das vagas de IA nos polos globais analisados; a Azure é a lacuna
conhecida, coberta pela interface de LLM independente de provedor ([ADR 0013](0013-extracao-v2-sinais-de-liberdade.md)).
Peças fora da AWS só com motivo registrado em ADR (hoje: Neon, Langfuse, Telegram e a plataforma da
newsletter).

**Quatro camadas, com contrato de dados entre elas:**

| Camada | O que faz | Onde roda | ADR |
| --- | --- | --- | --- |
| 1. Plataforma de dados | Coleta, bronze, prata e ouro, enriquecimento com LLM. É o sistema de registro das vagas | AWS (Lambda, S3, Glue, Athena, Bedrock, Step Functions) | 0009, 0010, 0011, 0013 |
| 2. Índice de vagas | Vagas ativas com campos extraídos, embeddings e texto para busca. Derivado do lago e reconstruível | Postgres com pgvector | 0012, 0014 |
| 3. Matching | Filtros, busca híbrida, pontuação e explicação para um perfil. Funções puras sobre o índice | Biblioteca Python, chamada pela CLI, pela API e pelo MCP | 0012, 0022 |
| 4. Superfícies | Site estático e canais, app web, servidor MCP e assistente | S3 e CloudFront, Lambda, Telegram, newsletter | 0015, 0019, 0022 |

**Código:** um monólito modular em Python. Um pacote (`liberty_find`) com módulos de fronteira
clara (`sources`, `collect`, `extraction`, `matching`, `serving`, `web`, `notifications`) e vários
pontos de entrada (Lambdas e CLI). Um módulo não importa o interior de outro: conversa pelos
contratos de `models.py`.

**Produto em estágios**, um por marco ([marcos/](../marcos/README.md)): canal público sem login
(o MVP), matching pessoal, app com login e assistente. Cada estágio reaproveita as camadas de
baixo sem refazê-las.

**Região:** `us-east-1` para tudo no MVP (mais modelos no Bedrock e menor preço). A região dos
dados pessoais é revista antes de abrir cadastro público ([ADR 0018](0018-privacidade-desde-o-desenho.md)).

## Alternativas consideradas

- **Microsserviços:** deploy e escala independentes, mas custo de operação alto para uma pessoa
  e nenhum ganho na escala de 10^4 a 10^5 vagas.
- **Tudo no Postgres, sem lago:** mais simples, mas perde histórico barato, reprocessamento a
  partir do bruto e a camada de engenharia de dados que dá sustentação ao produto.
- **Tudo no lago, com o Athena servindo o app:** um banco a menos, mas cada consulta de usuário
  levaria segundos e custaria por leitura.
- **App com login como primeiro entregável:** parece mais "SaaS", mas atrasa o primeiro uso real
  e exige toda a parte de LGPD antes de validar se alguém quer o produto.

## Consequências

- O lago é a fonte da verdade; o índice é derivado e pode ser apagado e recriado.
- Contratos de dados entre camadas passam a ser regra ([dados/contratos.md](../dados/contratos.md)).
- O primeiro valor público chega sem login, com menos risco jurídico e menos código.
- Cada camada nova precisa de teste sem rede e de contrato documentado antes de entrar.

## Rever se

Um módulo precisar escalar ou ser publicado separadamente (por exemplo, os coletores virarem uma
biblioteca), a latência entre o app e o banco pedir outra região, a fatura passar de US$ 10 por mês
por dois meses depois dos créditos ([ADR 0020](0020-observabilidade-avaliacao-custo.md)), ou a AWS
deixar de liderar nas vagas-alvo.
