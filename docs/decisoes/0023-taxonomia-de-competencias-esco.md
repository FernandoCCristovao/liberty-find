# ADR 0023: Taxonomia de competências: ESCO com extensão própria para ferramentas

- Status: aceita (implementação no Marco 4)
- Data: 2026-10-20

## Contexto

O matching compara as competências pedidas na vaga com as do perfil, em português, inglês e
espanhol. Sem normalização, "Postgres" e "PostgreSQL" ou "pipelines de dados" e "data pipelines"
viram coisas diferentes, e a cobertura de competências na pontuação fica sem sentido. Opções
conferidas em 2026-10-20:

| Opção | Idiomas | Licença | Observação |
| --- | --- | --- | --- |
| ESCO (Comissão Europeia), versão 1.2.1 | 28, incluindo português | Download livre; conteúdo da Comissão sob CC BY 4.0, salvo indicação | Competências e ocupações com identificador estável; pouca ferramenta específica de tecnologia |
| O*NET (EUA) | Inglês | CC BY 4.0, com regras de atribuição | Tem lista de tecnologias; fraco para português |
| Lightcast Open Skills | Inglês | Os termos excluem uso comercial sem contrato e permitem cancelamento a qualquer momento | Rica em tecnologia, incompatível com produto comercial |
| Lista própria | Qualquer | Própria | Rápida, sem rótulos multilíngues nem estrutura |

Fontes: [ESCO](https://esco.ec.europa.eu/en/use-esco/download),
[O*NET](https://www.onetcenter.org/license_db.html),
[Lightcast](https://legal.lightcast.io/lightcast-legal/open-terms-of-use).

## Decisão

- **ESCO como base**, porque os rótulos multilíngues levam uma menção em português, inglês ou
  espanhol ao mesmo identificador.
- **Extensão própria para ferramentas e tecnologias** que a ESCO não tem (por exemplo, dbt,
  LangGraph, pgvector), versionada no repositório e, quando fizer sentido, ligada às tecnologias do
  O*NET, com atribuição.
- **Normalização em etapas:** forma escrita na vaga, dicionário de apelidos, vizinhos por embedding
  entre a menção e os rótulos da ESCO e da extensão, aceite acima de um limiar e, abaixo dele, um
  modelo pequeno escolhe um candidato ou nenhum. O resultado vai para uma tabela de apelidos em cache.
- **Atribuição** da ESCO e do O*NET no site e no app, conforme as licenças.

## Alternativas consideradas

- **Lightcast:** a mais completa para tecnologia, mas os termos excluem uso comercial sem contrato.
- **Só O*NET:** inglês apenas.
- **Só lista própria:** sem estrutura e sem idiomas; vira um dicionário que ninguém mantém.

## Consequências

- Competência vira identificador estável, e a cobertura de competências no matching pode ser medida.
- A extensão própria precisa de manutenção, porque ferramentas novas surgem rápido.
- A mesma taxonomia alimenta os insights do mercado (competências mais pedidas).

## Rever se

Um cliente B2B precisar de identificadores da Lightcast, ou a ESCO ficar defasada para tecnologia a
ponto de a extensão própria ficar maior que a parte usada da ESCO.
