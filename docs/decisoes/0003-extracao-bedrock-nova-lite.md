# ADR 0003: Extração com Bedrock e Amazon Nova Lite, via tool use

- Status: substituída pelo [ADR 0013](0013-extracao-v2-sinais-de-liberdade.md)
- Data: 2026-10-12

## Contexto

Os campos que interessam (nível, regime, inglês, salário, stack) estão no texto livre da vaga,
em português ou inglês. Regras com expressão regular quebram fácil. Cada vaga é extraída uma vez
por versão, então o volume diário é baixo, mas a primeira carga tem milhares de vagas.

## Decisão

- Bedrock Converse API com o perfil de inferência `us.amazon.nova-lite-v1:0`.
- Saída estruturada por tool use forçado (`toolChoice` com o nome da ferramenta), `temperature` 0.
- Esquema da ferramenta escrito à mão, dentro do subconjunto de JSON Schema que o Nova aceita, e
  validação da resposta com pydantic.
- Prompt versionado; reextração quando muda a vaga (`content_hash`) ou o prompt (`prompt_version`).
- Modelo configurável por variável de ambiente, para comparar alternativas sem mudar código.

## Alternativas consideradas

- Claude Haiku no Bedrock: provavelmente mais preciso, com custo por token maior. É o primeiro
  candidato se a avaliação ficar abaixo da meta.
- Gemini ou OpenAI fora da AWS: tira o projeto da AWS e exige gerenciar chave de API.
- Regras e expressões regulares: frágeis com texto livre e bilíngue.

## Consequências

- Custo de centavos por mil vagas; nenhuma chave de API para guardar (acesso por IAM).
- A qualidade precisa ser medida: 50 vagas rotuladas à mão (Marco 2, tarefa 2.3).
- O teste de contrato garante que esquema e modelo pydantic não se separem.

## Rever se

O acerto ficar abaixo de 85% em família, nível, modelo de trabalho ou inglês na avaliação, ou
o Nova Lite sair de linha no Bedrock.
