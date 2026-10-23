# ADR 0009: Fontes de vagas por nível de permissão, com política de exibição por fonte

- Status: aceita
- Data: 2026-10-20
- Substitui: [ADR 0006](0006-somente-apis-publicas.md)

## Contexto

O ADR 0006 limitou a coleta a quatro APIs públicas de ATS e manteve a descrição das vagas
privada. Com o produto passando a buscar vagas para qualquer perfil, a cobertura importa mais, e
um levantamento de cerca de 40 fontes (2026-10-20) mostrou três grupos bem diferentes:

- **Feitas para serem lidas por terceiros:** as APIs públicas de Greenhouse, Lever e Ashby
  ([Greenhouse](https://developers.greenhouse.io/job-board.html): GET sem autenticação;
  [Lever](https://github.com/lever/postings-api): "These jobs may be scraped by third parties"),
  e o feed XML da Workable, que existe para job boards e reúne vagas de todos os clientes
  ([Workable](https://help.workable.com/hc/en-us/articles/4420464031767)).
- **Agregadores com regras de exibição:** Jobicy e Remote OK exigem atribuição e link de volta;
  a Remotive proíbe repassar vagas a terceiros (inclusive o Google Jobs) e usá-las para captar
  cadastros ou e-mails
  ([Remotive](https://github.com/remotive-com/remote-jobs-api)); a Himalayas proíbe redistribuir
  ([termos](https://himalayas.app/terms)).
- **Proibidos:** LinkedIn, Indeed ("competitors of Indeed (including job aggregation/posting
  websites) may not use Indeed", [termos](https://www.indeed.com/legal)), Glassdoor, o portal de
  busca da Gupy ("agregar, copiar ou duplicar partes do Gupy", [termos](https://www.gupy.io/termos-de-uso-recrutamento-e-selecao-candidatos)),
  Vagas.com, Catho, InfoJobs, Remotar e Trampos. O caso hiQ contra LinkedIn terminou com
  pagamento de US$ 500 mil, proibição permanente e destruição dos dados coletados
  ([resumo](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn)).

Há ainda rotas de parceria legítimas: a Gupy tem um feed oficial para job boards parceiros, em que
cada cliente escolhe onde a vaga aparece ([Gupy](https://developers.gupy.io/docs/integra%C3%A7%C3%A3o-com-job-boards-parceiros)),
e o ITJobs.pt tem API com chave, mas os termos pedem autorização para uso comercial
([ITJobs](https://www.itjobs.pt/api)).

## Decisão

1. **Catálogo de fontes em quatro níveis**, mantido em [dados/fontes.md](../dados/fontes.md):
   - **A, em uso ou próximas (sem chave):** Greenhouse, Lever (instâncias global e UE), Ashby,
     Workable (widget por empresa e feed XML), SmartRecruiters, Teamtailor, Recruitee e Personio.
     Cada uma entra só depois de conferida com `liberty probe` e com os termos anotados.
   - **B, agregadores com regras:** Jobicy e Remote OK, cada um com a sua política de exibição
     aplicada em código.
   - **C, parceria ou permissão (pedido formal, com aprovação humana):** feed de job boards da
     Gupy, API do ITJobs.pt, Landing.jobs, Net-Empregos e ProgramaThor; a Remotive só com permissão
     expressa, porque as regras dela conflitam com newsletter e Telegram.
   - **D, fora:** LinkedIn, Indeed, Glassdoor, portal de busca da Gupy, Vagas.com, Catho,
     InfoJobs, Remotar, Trampos, Himalayas, Jooble e The Muse. Os endpoints internos do Workday
     (não documentados, e sem clareza se os termos do site valem para as páginas de carreira dos
     clientes) ficam fora até haver parecer jurídico.
2. **Política de exibição por fonte**, como configuração versionada e aplicada no site, no app e
   em qualquer marcação de SEO: atribuição, link seguido para a vaga original, URL original
   intacta, nada de cadastro na frente quando a fonte proíbe e nada de marcação `JobPosting`
   quando a fonte proíbe o Google Jobs.
3. **A descrição completa continua sem publicação.** Público: campos derivados, um resumo curto
   escrito pelo próprio pipeline, até três trechos curtos de evidência por vaga (no máximo 200
   caracteres cada) nas fontes cuja política permite exibir, e o link para a vaga original. Rever
   por fonte se o produto precisar de páginas completas para busca orgânica.
4. **Descoberta de empresas** pelo índice colunar do Common Crawl consultado no Athena (hosts
   como `boards.greenhouse.io`, `jobs.lever.co` e `jobs.ashbyhq.com`), seguida de validação com
   uma chamada à API e registro com estado de saúde ([Common Crawl](https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format)).
   O índice serve para descobrir empresas, nunca como fonte de texto de vaga.
5. **Etiqueta de coleta:** no máximo uma requisição por segundo por host, o `Crawl-delay` da
   Lever, a cadência que cada fonte pede (o feed da Workable atualiza de hora em hora; a Remotive
   pede no máximo quatro leituras por dia), User-Agent com contato, espera exponencial com
   variação aleatória e respeito a `Retry-After`.

## Alternativas consideradas

- **Manter só as quatro fontes:** simples, mas a cobertura fica pequena e enviesada para
  empresas internacionais.
- **Raspar os sites com mais vagas:** maior cobertura, mas viola termos de uso, expõe o projeto e
  tem precedente caro.
- **APIs de agregadores comerciais (Adzuna, Careerjet, Jooble):** exigem licença para uso que
  gera receita ou proíbem republicação.
- **Comprar uma base de vagas:** custo e licença incompatíveis com o orçamento.

## Consequências

- A cobertura cresce sem risco jurídico, e o viés fica documentado: as fontes permitidas
  concentram empresas de tecnologia e scale-ups; o mercado doméstico brasileiro depende de
  parceria.
- Cada fonte nova vem com uma linha no catálogo: nível, termos com data, cadência e política de
  exibição.
- A configuração de exibição vira contrato testado, não convenção de cabeça.

## Rever se

Os termos de uma fonte mudarem (a data da última conferência fica no catálogo), uma parceria for
aprovada, ou um parecer jurídico liberar ou vetar uma fonte do nível D.
