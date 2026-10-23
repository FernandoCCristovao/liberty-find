# ADR 0019: Superfícies públicas: site estático, Telegram e newsletter; Streamlit só interno

- Status: aceita
- Data: 2026-10-20
- Substitui: [ADR 0007](0007-paineis-fora-da-aws.md)

## Contexto

O ADR 0007 escolheu Power BI e Streamlit Community Cloud para os painéis de um observatório. O
primeiro entregável público do Liberty Find é outro: um canal com vagas verificadas, sem login,
que precisa ser rápido, barato, indexável e capaz de medir se alguém quer o produto (assinantes,
aberturas, cliques). Fatos que pesam:

- Comunidades de tecnologia no Brasil usam muito Telegram e newsletters; uma newsletter gratuita
  de vagas remotas para brasileiros passa de 36 mil assinantes, e um agregador recente chegou a
  1.000 usuários em 23 dias sem anúncio.
- O Google for Jobs exige uma página por vaga com a descrição completa na marcação `JobPosting`
  ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)), o que
  conflita com a regra de não publicar descrição e com fontes que proíbem o Google Jobs
  ([ADR 0009](0009-fontes-por-permissao.md)).
- O CloudFront tem 1 TB de transferência por mês sem custo, e o S3 serve arquivos estáticos por
  centavos.

## Decisão

- **Site estático gerado pelo pipeline** (Jinja2 para HTML) no S3 com CloudFront: listas por recorte
  (por exemplo, "dados, remoto, aberto a quem mora no Brasil"), uma página por vaga com os campos
  derivados, o resumo próprio e o link para a vaga original, e uma página de insights do mercado.
  Sem JavaScript pesado e sem rastreamento por cookie.
- **Telegram:** canal em que um bot publica as vagas novas verificadas (API gratuita).
- **Newsletter semanal:** numa plataforma gratuita (escolha na tarefa do Marco 3), com rascunho
  gerado pelo pipeline e curadoria humana antes do envio.
- **Marcação `JobPosting`:** fora do MVP; decidida fonte a fonte se a busca orgânica virar canal.
- **Power BI:** opcional, num projeto PBIP versionado sobre os marts de insights.
- **Streamlit:** só ferramenta interna e local (rotulagem e avaliação), sem publicação.

## Alternativas consideradas

- **Streamlit Community Cloud público:** gratuito, mas dorme sem uso e não serve como site de produto.
- **Vercel ou GitHub Pages:** os termos proíbem uso comercial ou SaaS.
- **App com login como primeira superfície:** mais caro e mais lento para testar demanda.

## Consequências

- O canal mostra se há interesse antes de qualquer login.
- A política de exibição por fonte vale também para o site e os canais.
- O conteúdo de insights serve de material público sem expor nada além do mercado.

## Rever se

A busca orgânica virar canal relevante (decidir a marcação por fonte), a plataforma de newsletter
mudar de limite, ou o app (ADR 0015) passar a servir as páginas públicas.
