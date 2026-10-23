# ADR 0013: Extração v2: sinais de liberdade, saída estruturada e modelo escolhido por avaliação

- Status: aceita (o esquema de campos é candidato até a auditoria de rótulos do Marco 1)
- Data: 2026-10-20
- Substitui: [ADR 0003](0003-extracao-bedrock-nova-lite.md)

## Contexto

O esquema v1 (família, nível, modelo de trabalho, regime, inglês, salário, experiência e stack)
foi pensado para um observatório. O Liberty Find promete sinais de liberdade
([produto.md](../produto.md)), e para isso a extração precisa trazer também: de quais países e
regiões se pode trabalhar, fuso exigido, regime de contratação internacional, outros idiomas,
visto e mudança, sinais explícitos de carga e flexibilidade, um resumo curto em inglês para a
busca e a frase da vaga que sustenta cada sinal.

Fatos novos (conferidos em 2026-10-20):

- O Bedrock passou a oferecer saída estruturada com decodificação restrita a um JSON Schema
  (fevereiro de 2026); o anúncio lista Anthropic, Mistral, OpenAI e Qwen, e não cita o Amazon Nova
  ([AWS](https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses)).
- O tool use forçado com o Nova funciona hoje, com a restrição de que o topo do esquema aceita só
  `type`, `properties` e `required` (aprendido no Marco 1).
- Preço por milhão de tokens (entrada / saída): Nova Micro US$ 0,035 / 0,14; Nova Lite
  US$ 0,06 / 0,24; Claude Haiku 5.5 US$ 0,10 / 0,50 (lançado em 2026-10-07). Inferência em lote
  custa 50% menos ([Bedrock](https://aws.amazon.com/bedrock/pricing/),
  [Anthropic](https://platform.claude.com/docs/en/about-claude/pricing)). Preços de terceiros: conferir no dia.
- Anúncios de engenharia de IA pedem cada vez mais roteamento entre provedores e controle de custo,
  e a maioria não cita framework algum.

## Decisão

1. **Esquema v2 candidato** em [dados/extracao.md](../dados/extracao.md). Ele é fechado depois de
   uma auditoria em 200 vagas rotuladas à mão (Marco 1, tarefa 1.5): campo que aparece em menos de
   10% das vagas ou que fica abaixo de 85% de acerto sai do esquema ou vira "experimental".
2. **Saída estruturada sempre validada:** tool use forçado em todos os modelos, ou a saída
   estruturada nativa quando o modelo suportar. A resposta passa por Pydantic; falhou, uma nova
   tentativa com o erro; falhou de novo, um modelo maior; persistindo, a vaga entra como falha e a
   execução segue. O `stop_reason` vai para o log.
3. **Modelo escolhido por avaliação, não por preferência:** comparação no conjunto rotulado entre
   Nova Lite, Claude Haiku 5.5 e um piso barato (Nova Micro). Vence o mais barato que cumprir as
   metas (90% ou mais nos campos principais; 95% ou mais de precisão no selo de elegibilidade,
   medida em pelo menos 60 vagas abertas que não foram usadas no ajuste, como em
   [dados/extracao.md](../dados/extracao.md)) e cujo custo projetado caiba no orçamento
   ([ADR 0020](0020-observabilidade-avaliacao-custo.md)).
4. **Interface própria e fina** (`LLMClient`, um `Protocol`) com uma implementação para o Bedrock
   (Converse). Uma segunda implementação, com API direta de outro provedor, só entra quando houver
   motivo medido. Sem framework de LLM no pipeline.
5. **Idempotência e procedência:** a chave de uma extração é (`content_hash`, `schema_version`,
   `prompt_version`, `model_id`); a resposta bruta do modelo vai para o bronze. Carga inicial e
   reextrações rodam em lote (50% mais barato). O delta diário roda sob demanda enquanto for pequeno
   e passa para lote quando superar o mínimo de registros que o lote do Bedrock exige (cerca de mil).
6. **Pré-processamento:** HTML para texto, corte de trechos padrão (texto institucional, benefícios
   genéricos), detecção de idioma e limite de tamanho da descrição.
7. **Entrada não confiável:** a descrição da vaga é dado, nunca instrução. O prompt separa as duas
   coisas, e a ferramenta de extração não tem efeito colateral nenhum.
8. **Selo de elegibilidade como função pura e testada** já no Marco 1, para que a escolha do modelo
   possa medi-lo; no Marco 2, a mesma regra é espelhada em SQL na camada de ouro, com um teste de que
   as duas concordam.

## Alternativas consideradas

- **Manter o esquema v1:** mais simples, mas não sustenta a promessa do produto.
- **Sempre o modelo maior:** mais acerto provável, com custo várias vezes maior e sem medição.
- **LangChain ou LiteLLM no pipeline:** abstração a mais para uma chamada só; o roteamento entra
  pela interface própria se e quando houver um segundo provedor.
- **Regras e expressões regulares:** frágeis com texto livre em três idiomas.

## Consequências

- Custo estimado só da extração, na escala de 2 mil vagas novas ou alteradas por dia, com 1.200
  tokens de entrada e 300 de saída por vaga (cálculo sobre preços de tabela, por mês): Nova Micro
  cerca de US$ 5 sob demanda ou 2,50 em lote; Nova Lite cerca de 8,60 ou 4,30; Claude Haiku 5.5
  cerca de 16 ou 8. Saída maior (esquema v2 com evidências) aumenta a conta. Com as primeiras dezenas
  de empresas, centavos.
- O conjunto rotulado vira patrimônio do projeto: mede modelos, prompts e regressões no CI.
- O teste de contrato continua impedindo que o esquema e o modelo Pydantic se separem.

## Rever se

A avaliação acusar regressão, surgir modelo mais barato que cumpra as metas, o Nova Lite sair de
linha, ou o preço de algum candidato mudar.
