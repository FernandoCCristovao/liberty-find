# Fontes de dados

Só entram fontes cujos termos permitem coleta e exibição, sempre com atribuição e link para a vaga
original. A decisão e o porquê estão no [ADR 0009](../decisoes/0009-fontes-por-permissao.md). Termos
e endpoints conferidos em 2026-10-20; a data vale para cada linha até uma nova conferência.

## Nível A: APIs públicas de ATS, sem chave

| Fonte | Endpoint | Sinal de permissão | Campos úteis | Estado |
| --- | --- | --- | --- | --- |
| Greenhouse | `GET https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true`; detalhe com `?pay_transparency=true` | GET sem autenticação; o `robots.txt` só bloqueia `/embed/` [1] | `content` (HTML escapado), `location.name`, `departments`, `first_published`, `updated_at`, `internal_job_id`; faixa salarial só no detalhe. Sem campo de remoto | Implementada (`sources/greenhouse.py`) |
| Lever | `GET https://api.lever.co/v0/postings/{token}?mode=json`, com `skip` e `limit`; instância UE em `api.eu.lever.co` | "These jobs may be scraped by third parties"; `robots.txt` com `Crawl-delay: 1` [2] | `descriptionPlain`, `lists`, `categories`, `workplaceType`, `country`, `salaryRange` (opcional), `createdAt` em milissegundos | Marco 1 |
| Ashby | `GET https://api.ashbyhq.com/posting-api/job-board/{token}?includeCompensation=true` | API pública de vagas, sem credenciais; o `robots.txt` do site bloqueia só a API interna, então use apenas esta [3] | `descriptionPlain`, `location`, `secondaryLocations`, `isRemote`, `workplaceType`, `compensation`, `publishedAt`, `isListed` (falso: só por link direto, não exibir) | Marco 1 |
| Workable | Widget por empresa: `GET https://apply.workable.com/api/v1/widget/accounts/{token}` (`details=true` traz a descrição). Feed de todas as contas: `https://www.workable.com/boards/workable.xml` | O feed existe para job boards e "the job URLs should not be altered"; atualiza de hora em hora [4] | Título, descrição, local, indicação de remoto, departamento, datas | Widget no Marco 1; feed no Marco 2 (arquivo grande) |
| SmartRecruiters | `GET https://api.smartrecruiters.com/v1/companies/{id}/postings` | A documentação de 2026-10-20 indica vagas públicas sem chave; a anotação de 2026-10-12 dizia que exigia chave. Conferir com `liberty probe` antes de usar [5] | Seções do anúncio, local, departamento, tipo de emprego, nível, data | A avaliar (Marco 2) |
| Teamtailor | RSS `https://{site}/jobs.rss` | "All of the data is publicly available" [6] | Título, descrição, data, remoto, locais, departamento | A avaliar |
| Recruitee | `https://{empresa}.recruitee.com/api/offers/` | Documentado como lista de vagas; a anotação anterior falava em cabeçalho de token. Conferir [7] | Descrição, requisitos, locais, remoto, salário, datas | A avaliar |
| Personio | `https://{empresa}.jobs.personio.de/xml?language=xx` | Feito para integrar vagas em sites [8] | Nome, categoria, tipo de emprego, jornada, descrição, escritório | A avaliar |

## Nível B: agregadores com regras de exibição

| Fonte | Endpoint | Regras que o produto precisa cumprir | Estado |
| --- | --- | --- | --- |
| Jobicy | `https://jobicy.com/api/jobs` | Creditar e linkar a fonte; sincronizar no máximo de hora em hora; só os últimos 7 dias [9] | A avaliar |
| Remote OK | `https://remoteok.com/api` | Link de volta seguido (sem `nofollow`) e citar a fonte; sem logo sem permissão [10] | A avaliar |

## Nível C: parceria (pedido formal, com aprovação humana)

| Fonte | Rota | Observação |
| --- | --- | --- |
| Gupy | Feed para job boards parceiros: aprovação, depois URL e token [12] | Cada cliente escolhe por vaga em quais job boards ela aparece; a cobertura cresce aos poucos |
| ITJobs.pt | API com chave, JSON ou XML, com faixa salarial e modelo de trabalho [13] | Os termos pedem autorização para exploração comercial |
| Remotive | `https://remotive.com/api/remote-jobs`, no máximo 4 leituras por dia [11] | Proíbe repassar vagas a terceiros (inclusive o Google Jobs) e usá-las para captar cadastros ou e-mails, o que conflita com newsletter e Telegram: só com permissão expressa |
| ProgramaThor | Sem API; termos limitam o uso dos dados ao objeto do serviço | Só por acordo |
| Landing.jobs, Net-Empregos, Sapo Emprego | Sem API pública para terceiros | Só por acordo |

## Nível D: fora, e por quê

| Fonte | Motivo |
| --- | --- |
| LinkedIn | O Contrato do Usuário proíbe robôs e coleta; no caso hiQ, o acordo de 2022 incluiu US$ 500 mil, proibição permanente e destruição dos dados [14] |
| Indeed | Termos: uso pessoal e não comercial; concorrentes, incluindo agregadores, não podem usar [15] |
| Glassdoor | Termos proíbem coleta automática |
| Portal de busca da Gupy | Termos para candidatos proíbem "agregar, copiar ou duplicar partes do Gupy", incluindo vagas; o endpoint mudou duas vezes em poucas semanas [16] |
| Vagas.com, Catho, InfoJobs, Remotar, Trampos | Termos proíbem robôs ou reprodução do conteúdo |
| Himalayas | Termos proíbem redistribuir vagas para outros job boards e agregadores [17] |
| Jooble, The Muse | Termos proíbem robôs ou republicação |
| Adzuna, Careerjet | Programas de publisher; uso que gera receita exige licença |
| Workday (endpoints internos `cxs`) | Não documentados; os termos do site da Workday proíbem extração automática, e não está claro se valem para as páginas de carreira dos clientes. Fora até haver parecer jurídico |
| Hacker News "Who is hiring" | Os termos do Y Combinator proíbem coleta; serve só como pista manual de empresas |

## Descoberta de empresas

As APIs não listam quais empresas usam cada ATS. O caminho é descobrir pelo índice de URLs do Common
Crawl, que é público, colunar e fica no S3 em `us-east-1`, consultável pelo Athena com custo de
centavos quando se leem só as colunas necessárias [18]:

```sql
-- Depois de registrar a tabela do índice conforme a documentação do Common Crawl
SELECT url_host_name,
       regexp_extract(url_path, '^/([^/?#]+)', 1) AS slug,
       count(*) AS pages
FROM ccindex.ccindex
WHERE crawl = 'CC-MAIN-2026-39'
  AND subset = 'warc'
  AND url_host_name IN ('boards.greenhouse.io', 'job-boards.greenhouse.io',
                        'jobs.lever.co', 'jobs.ashbyhq.com', 'apply.workable.com')
GROUP BY 1, 2;
```

Cada candidato é validado com uma chamada à API (`liberty probe`) e entra no registro com o estado de
saúde. O índice serve só para descobrir empresas, nunca como fonte de texto de vaga. O feed da
Workable também lista todas as empresas com vagas publicadas.

A conta do projeto fica em `us-east-2`, e a política da AWS para a conta pode negar a leitura do
índice em `us-east-1` ([ADR 0024](../decisoes/0024-conta-aws-experiencia-nova-us-east-2.md)). Se negar, a alternativa é a
API do índice do Common Crawl (https://index.commoncrawl.org), consultada por domínio, sem AWS.

## Política de exibição por fonte

Configuração versionada, aplicada no site, nos canais e no app:

| Regra | Greenhouse, Lever, Ashby | Workable | Jobicy | Remote OK |
| --- | --- | --- | --- | --- |
| Link para a vaga original | Sim | Sim, URL inalterada | Sim | Sim, link seguido |
| Citar a fonte | Recomendado | Recomendado | Obrigatório | Obrigatório |
| Pode ir para Telegram e newsletter | Sim | Sim | Sim | Sim, com o link e a citação |
| Pode aparecer atrás de login | Sim | Sim | Sim | Sim |
| Trechos curtos de evidência (até 3 por vaga, 200 caracteres cada) | Sim | Sim | Sim | Sim |
| Pode ter marcação `JobPosting` | Decisão futura | Decisão futura | Decisão futura | Decisão futura |
| Descrição completa publicada | Não | Não | Não | Não |

Fontes do nível C seguem o que o acordo ou a permissão disser; sem acordo, não aparecem.

## Etiqueta de coleta

- No máximo uma requisição por segundo por host, em sequência dentro do mesmo host.
- Respeitar o `Crawl-delay` da Lever e a cadência de cada fonte (feed da Workable de hora em hora,
  Jobicy no máximo de hora em hora).
- User-Agent identificável: `liberty-find/<versão> (+<URL do repositório>)`.
- Espera exponencial com variação aleatória e respeito ao `Retry-After`; circuito aberto para um
  host que falha seguido.
- Guardar a resposta bruta por 90 dias, para reprocessar sem chamar a fonte de novo.
- Guardar a data da última conferência dos termos de cada fonte.

## Adicionar uma empresa

1. Ache o token no endereço da página de vagas da empresa:
   `job-boards.greenhouse.io/<token>` ou `boards.greenhouse.io/<token>`, `jobs.lever.co/<token>`,
   `jobs.ashbyhq.com/<token>`, `apply.workable.com/<token>`.
2. Teste: `uv run liberty probe <fonte> <token>`. Precisa listar vagas.
3. Acrescente uma linha em `src/liberty_find/boards.yaml` (fonte, token e nome da empresa).
4. `uv run poe check` e commit `feat(boards): adiciona <empresa>`.

Empresa que mudou de ATS ou cujo token parou de responder: corrija o token ou marque
`enabled: false`, com um comentário do motivo.

## Saúde das fontes

Cada coleta grava `health/dt=<dia>/health.json` com o estado de cada empresa: `ok` (com o número de
vagas), `error` (com o erro resumido) ou `skipped` (fonte ainda sem implementação). Empresa em
`error` por dois dias seguidos merece investigação; queda brusca no número de vagas de uma empresa
deixa o registro em quarentena antes de fechar vagas em massa.

## Onde fica o registro de empresas

- `src/liberty_find/boards.yaml` guarda a lista curada e validada (as primeiras dezenas de empresas),
  pública de propósito: mostra o que o projeto coleta.
- Os candidatos que saem da descoberta ficam fora do repositório (arquivo local ignorado pelo Git ou
  bucket privado) até serem validados.
- Quando o registro passar de cerca de 100 empresas, ele vai para o bucket privado e o repositório
  fica com um exemplo ([ADR 0017](../decisoes/0017-licenca-fair-source.md)).

## Referências

1. Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html
2. Lever Postings API: https://github.com/lever/postings-api
3. Ashby Job Postings API: https://developers.ashbyhq.com/docs/public-job-posting-api
4. Workable, feed XML: https://help.workable.com/hc/en-us/articles/4420464031767 e endpoints públicos: https://help.workable.com/hc/en-us/articles/115012771647
5. SmartRecruiters Posting API: https://developers.smartrecruiters.com/docs/posting-api
6. Teamtailor, RSS: https://support.teamtailor.com/en/articles/11171756-rss-feed-how-to-guide
7. Recruitee, ofertas: https://docs.recruitee.com/reference/offers
8. Personio, vagas abertas: https://developer.personio.de/docs/integration-of-open-positions
9. Jobicy: https://jobicy.com/jobs-rss-feed
10. Remote OK: https://remoteok.com/api
11. Remotive: https://github.com/remotive-com/remote-jobs-api
12. Gupy, job boards parceiros: https://developers.gupy.io/docs/integra%C3%A7%C3%A3o-com-job-boards-parceiros
13. ITJobs.pt, API: https://www.itjobs.pt/api
14. hiQ Labs v. LinkedIn: https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn
15. Termos do Indeed: https://www.indeed.com/legal
16. Termos da Gupy para candidatos: https://www.gupy.io/termos-de-uso-recrutamento-e-selecao-candidatos
17. Termos da Himalayas: https://himalayas.app/terms
18. Índice colunar do Common Crawl: https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format
