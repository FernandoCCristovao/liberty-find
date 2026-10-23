# ADR 0015: App web com FastAPI no Lambda, HTML no servidor com HTMX e login pelo Cognito

- Status: aceita (implementação no Marco 5)
- Data: 2026-10-20

## Contexto

O app beta (Marco 5) precisa de login, edição do perfil de busca, lista de vagas com explicação e
botões de feedback. As páginas públicas de vagas ficam no site estático
([ADR 0019](0019-superficies-publicas.md)). Para quem mantém um projeto de dados e IA, a interface
pesa pouco: o que conta é a qualidade da busca, da avaliação e da operação. Fatos conferidos em
2026-10-20:

- FastAPI aparece em cerca de 11% dos anúncios de engenharia de IA analisados; TypeScript em cerca
  de 23%, mais em vagas de produto.
- O plano Hobby da Vercel proíbe uso comercial, e o GitHub Pages não pode hospedar SaaS
  ([Vercel](https://vercel.com/docs/plans/hobby),
  [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
- O Cognito (planos Lite e Essentials) tem 10 mil usuários ativos por mês gratuitos, sem prazo,
  e login sem senha por e-mail ([Cognito](https://aws.amazon.com/cognito/pricing/)).

## Decisão

- **API e páginas:** FastAPI no Lambda (adaptador ASGI), atrás de uma API Gateway HTTP API com
  autorizador JWT do Cognito. HTML renderizado no servidor (Jinja2) com HTMX para as partes
  interativas. A mesma aplicação expõe JSON com OpenAPI, que o servidor MCP e um front-end futuro
  podem usar.
- **Login:** Cognito Essentials com código por e-mail (sem senha) e tela de login gerenciada.
- **Arquivos estáticos:** S3 com CloudFront.
- **Sem estado no servidor:** sessão no token; dados no Postgres com isolamento por usuário
  ([ADR 0012](0012-banco-de-servico-postgres.md)).

## Alternativas consideradas

- **Next.js com TypeScript:** o mais pedido em vagas de produto, mas dobra a stack (outra linguagem,
  outro build, outra hospedagem) antes de haver usuário; entra quando a experiência pedir.
- **Streamlit:** ótimo para ferramenta interna, ruim como produto (sessão, SEO, controle de
  interface).
- **Clerk, Neon Auth ou Supabase Auth:** experiência de desenvolvimento melhor ou menos peças da AWS;
  o Cognito vence por ficar na mesma conta, sem chave a mais e com o autorizador nativo da API Gateway.
- **Login próprio com link mágico:** risco de segurança alto para um ganho pequeno.

## Consequências

- Uma linguagem só no projeto inteiro.
- As páginas são rápidas e indexáveis; a interatividade fica limitada ao que o HTMX resolve.
- A configuração do Cognito é mais trabalhosa que a de alternativas como o Clerk; o custo aceito em
  troca é ficar dentro da AWS.

## Rever se

A experiência exigir interatividade rica, entrar alguém dedicado ao front-end, ou o Cognito bloquear
um fluxo necessário.
