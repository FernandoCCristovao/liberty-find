# Marco 3: Canal público (MVP)

**Objetivo:** pessoas reais recebendo, sem login e sem custo, vagas verificadas como abertas a quem
mora no Brasil ou em Portugal, com salário, inglês e sinais de liberdade, e números que digam se o
produto tem demanda.

Decisão: [ADR 0019](../decisoes/0019-superficies-publicas.md). Antes de publicar: precisão do selo
de elegibilidade de 95% ou mais na avaliação da tarefa 1.6, medida como em
[extracao.md](../dados/extracao.md), e testes da política de exibição por fonte.

## Tarefas (na ordem)

### [ ] 3.1 Marca e domínio

- Fazer: buscar "Liberty Find" e variações na base de marcas do INPI (classes 35 e 42) e conferir
  domínios (.com, .com.br e .pt); decidir o nome público e o domínio. Registrar o domínio é gasto:
  só com aprovação humana.
- Aceite: decisão registrada, com o resultado da busca; domínio apontando para o CloudFront.

### [ ] 3.2 Site estático

- Fazer: gerador em `site/` (Jinja2 para HTML) rodando como passo da orquestração, com páginas por
  recorte, uma página por vaga (campos derivados, evidências, resumo próprio e link para a vaga
  original), página de insights, página de privacidade e termos, um canal para pedir a remoção de
  uma vaga ou empresa e uma lista de espera para o matching pessoal (sem cobrança). S3 e CloudFront
  no Terraform. Sem cookies de rastreamento.
- Aceite: o site se atualiza sozinho todo dia; vaga fechada some na mesma atualização; a política de
  cada fonte tem teste (atribuição, link, nada de descrição completa).

### [ ] 3.3 Canal no Telegram

- Fazer: um bot (token no SSM Parameter Store) publica as vagas novas verificadas num canal, com
  selo, salário quando houver, inglês exigido, a fonte citada e o link; só fontes cuja política
  permite canais de terceiros ([fontes.md](../dados/fontes.md)); limite de mensagens por dia.
- Aceite: as vagas novas do dia aparecem no canal sem passo manual; nenhuma vaga repetida.

### [ ] 3.4 Newsletter semanal

- Fazer: escolher uma plataforma gratuita (assinatura, descadastro e métricas incluídos); o pipeline
  gera o rascunho da edição (as melhores vagas da semana e um número do mercado); revisão humana antes
  do envio; formulário de assinatura no site.
- Aceite: primeira edição enviada; o rascunho sai pronto do pipeline.

### [ ] 3.5 Medição

- Fazer: acompanhar assinantes, aberturas, cliques, membros e visualizações do canal e visitas do
  site, edição a edição, numa planilha privada.
- Aceite: os números de cada edição registrados.

### [ ] 3.6 Fechamento

- Aceite: README com os links do site e dos canais e os primeiros números; tag `v0.3.0`.
