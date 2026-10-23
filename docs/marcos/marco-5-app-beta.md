# Marco 5: App beta

**Objetivo:** um grupo pequeno de pessoas convidadas usando o Liberty Find com login: perfil salvo,
lista com explicação, alertas por e-mail e feedback, com a LGPD cumprida na prática.

Decisões: [ADR 0015](../decisoes/0015-app-web-fastapi-htmx-cognito.md) e
[ADR 0018](../decisoes/0018-privacidade-desde-o-desenho.md). Antes do primeiro usuário externo:
aviso de privacidade publicado e checklist de [privacidade.md](../privacidade.md) cumprido.

## Tarefas (na ordem)

### [ ] 5.1 API e login

- Fazer: FastAPI no Lambda, API Gateway HTTP API com autorizador JWT do Cognito (código por e-mail,
  sem senha), tabelas de usuário com row-level security e papel do app sem ser dono das tabelas;
  OpenAPI publicado.
- Aceite: testes de que um usuário não lê dado de outro; login funcionando do início ao fim.

### [ ] 5.2 Telas

- Fazer: páginas com HTMX para criar e editar o perfil (formulário e texto livre), ver a lista com
  explicações e marcar cada vaga como boa ou ruim, com motivo.
- Aceite: o fluxo completo funciona no celular e no computador.

### [ ] 5.3 Alertas por e-mail

- Fazer: SES com domínio verificado (DKIM, SPF e DMARC), saída do modo sandbox, alerta diário ou
  semanal à escolha da pessoa, descadastro em um clique; agendamento que escolhe quem recebe, fila no
  SQS e envio em lote.
- Aceite: alertas chegando sem cair em spam nos testes; descadastro imediato.

### [ ] 5.4 LGPD na prática

- Fazer: aviso de privacidade e termos de uso em português; página sobre as transferências
  internacionais e pedido dos aditivos aos fornecedores; canal para pedidos dos titulares; exportar e
  apagar a conta pelo app; roteiro de resposta a incidente; conferência de que logs, métricas e
  rastreios não têm dado pessoal; registro simples das operações de tratamento.
- Aceite: checklist de [privacidade.md](../privacidade.md) cumprido e revisado.

### [ ] 5.5 Observabilidade

- Fazer: rastreios amostrados no Langfuse, alarmes do app, custo por usuário ativo no README.
- Aceite: uma explicação de vaga rastreada do pedido à resposta.

### [ ] 5.6 Beta fechado e fechamento

- Fazer: convidar de 10 a 30 pessoas; recolher feedback; decidir as prioridades seguintes com os
  números do beta.
- Aceite: README com o app e os números do beta; tag `v0.5.0`.
