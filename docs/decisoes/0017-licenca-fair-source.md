# ADR 0017: Licença FSL-1.1-ALv2 (fair source) e o que fica fora do repositório

- Status: aceita
- Data: 2026-10-20

## Contexto

O repositório precisa ser público, porque é a forma de mostrar o trabalho, e o produto também pode
virar negócio. A licença precisa deixar qualquer pessoa ler, rodar e estudar o código, sem permitir
que terceiros o ofereçam como produto concorrente. O repositório ainda não foi publicado, então a
escolha da licença não tem legado.

| Licença | Efeito | Quem usa |
| --- | --- | --- |
| MIT ou Apache-2.0 | Qualquer um pode hospedar uma cópia comercial | A maioria das bibliotecas |
| AGPL-3.0 | Código aberto (OSI); quem hospeda uma versão modificada publica o código, mas pode competir | Elastic (desde 2024), Redis 8 |
| FSL-1.1 (fair source) | Qualquer uso, menos oferecer um produto concorrente; cada versão vira Apache-2.0 depois de 2 anos | Sentry, GitButler, Liquibase |
| BSL 1.1 | Parecida, com prazos e condições definidos por quem licencia | HashiCorp |
| Repositório privado | Protege tudo | Não serve para mostrar o trabalho |

Fontes: [FSL](https://fsl.software/), [empresas fair source](https://fair.io/companies/).

## Decisão

- **FSL-1.1-ALv2** no repositório inteiro, com o texto em [LICENSE](../../LICENSE). O README diz
  "fair source", nunca "open source".
- **Fora do repositório:** respostas brutas das fontes, descrições de vagas, conjuntos rotulados que
  contenham texto de vaga, o registro de empresas quando ele crescer por descoberta automática,
  credenciais e qualquer documento de negócio.
- **A marca "Liberty Find" não é licenciada** (a própria FSL não concede direitos de marca).
- **Contribuições externas:** quando a primeira aparecer, adotar o DCO (assinatura nos commits) para
  manter a possibilidade de relicenciar.

## Alternativas consideradas

- **MIT (a licença anterior):** máxima reutilização, inclusive por um concorrente hospedado.
- **AGPL-3.0:** código aberto de verdade, mas não impede concorrente hospedado e afasta parte das
  empresas.
- **Repositório privado:** some a vitrine pública do trabalho.

## Consequências

- Qualquer pessoa pode ler, rodar, estudar e usar internamente; ninguém pode oferecer o código como
  produto concorrente por 2 anos a partir de cada versão.
- Como titular único, o autor pode mudar a licença de versões futuras a qualquer momento.

## Rever se

Aparecer o primeiro colaborador externo, surgir a decisão de abrir como código aberto (AGPL ou
Apache), ou fizer sentido separar os coletores numa biblioteca Apache-2.0.
