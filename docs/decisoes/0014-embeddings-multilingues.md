# ADR 0014: Embeddings multilíngues escolhidos por avaliação

- Status: aceita
- Data: 2026-10-20

## Contexto

O perfil de busca costuma ser escrito em português e as vagas chegam em inglês, português e
espanhol. A busca por vetor precisa funcionar entre idiomas. Opções conferidas em 2026-10-20:

| Modelo | Preço por milhão de tokens | Observação |
| --- | --- | --- |
| Amazon Titan Text Embeddings V2 (Bedrock) | cerca de US$ 0,02 | Lista o português, mas a AWS avisa que é otimizado para inglês e que a busca entre idiomas é "subótima" |
| Cohere Embed v4 (Bedrock) | cerca de US$ 0,12 | Mais de 100 idiomas, de 256 a 1.536 dimensões, tipos de entrada para consulta e documento |
| Qwen3-Embedding-0.6B (aberto, Apache-2.0) | só computação | Bom resultado no MTEB multilíngue; precisa empacotar o modelo e aguentar partida a frio |
| bge-m3 (aberto, MIT) | só computação | Denso e esparso; mesmo custo de operação |
| jina-embeddings-v3 | só computação | Licença CC BY-NC: não serve para uso comercial |

Fontes: [Titan V2](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html),
[Cohere Embed v4](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed-v4.html),
[Qwen3-Embedding](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B),
[jina v3](https://huggingface.co/jinaai/jina-embeddings-v3).

Na escala do MVP, com resumos de cerca de 300 tokens para 60 mil vagas por mês, o custo é de cerca
de US$ 0,36 por mês com o Titan e de US$ 2,20 com o Cohere: a diferença de preço é pequena perto da
diferença de qualidade possível.

## Decisão

- **O que vira vetor:** o resumo curto em inglês produzido pela extração (`summary_en`), mais título
  e competências. Do lado do usuário, o perfil normalizado pelo mesmo caminho. Isso reduz o problema
  de idioma antes mesmo do modelo.
- **Modelo padrão:** Cohere Embed v4 no Bedrock, com 1.024 dimensões, guardado como `halfvec` no
  Postgres.
- **Comparação obrigatória:** o Titan V2 é medido no mesmo conjunto de avaliação do matching
  (nDCG@10). Se ficar a até 2 pontos do Cohere, ele vence pelo preço.
- **Versionamento:** cada vetor guarda `model_id` e dimensões; trocar de modelo é reprocessar,
  nunca misturar vetores de modelos diferentes.

## Alternativas consideradas

- **Modelo aberto rodando no Lambda:** custo de token zero, mas imagem pesada, partida a frio e
  manutenção do modelo; entra se a avaliação mostrar vantagem clara.
- **Embeddings da OpenAI ou do Gemini:** bons e baratos, mas fora da AWS e com chave de API para
  guardar.
- **Vetorizar a descrição inteira, no idioma original:** mais tokens e mais risco entre idiomas.

## Consequências

- A extração ganha o campo `summary_en` (cerca de 100 tokens de saída a mais por vaga).
- O conjunto de avaliação do matching passa a decidir modelo e dimensões.

## Rever se

A avaliação mostrar um modelo aberto vencendo com folga, ou o preço e a disponibilidade do Cohere
no Bedrock mudarem.
