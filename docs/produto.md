# Produto

## Em uma frase

O Liberty Find encontra vagas que dão mais liberdade (de lugar, de dinheiro e de tempo) para cada
pessoa, mostra os sinais com a frase da vaga que os sustenta, explica o encaixe e avisa quando
surge uma nova.

**Find opportunities. Find freedom.**

## Propósito e missão

- **Propósito:** ajudar as pessoas a conquistar mais liberdade por meio de melhores oportunidades
  de trabalho, gastando menos tempo procurando.
- **Missão:** usar IA para transformar a procura de vaga em algo personalizado, contínuo e
  estratégico, conectando cada pessoa às oportunidades mais compatíveis com o que ela sabe fazer,
  precisa e quer.

## O problema

- Procurar vaga boa é repetitivo: as mesmas buscas, todo dia, em vários sites.
- "Remoto" muitas vezes não vale para quem mora no Brasil ou em Portugal: a vaga é só para um país,
  o fuso não fecha ou o inglês fluente é obrigatório.
- Salário, moeda, regime e carga quase nunca estão claros, e a pessoa descobre tarde.

## A resposta: sinais de liberdade verificáveis

| Liberdade | Sinais que o Liberty Find extrai | De onde vêm |
| --- | --- | --- |
| Geográfica | Modelo de trabalho; países e regiões de onde se pode trabalhar; fuso exigido | Campos do ATS e texto da vaga |
| Financeira | Faixa salarial, moeda e período; regime (CLT, PJ, contrato internacional) | Campos de remuneração do ATS e texto |
| De tempo | Sobreaviso, hora extra, horário flexível, semana de quatro dias, meio período | Texto da vaga, quando está escrito |
| Acesso | Nível de inglês e outros idiomas exigidos; patrocínio de visto e ajuda de mudança | Texto da vaga |

Regras: sinal ausente aparece como "não informado" e nunca é adivinhado; cada sinal mostra a
evidência; as três liberdades são uma aspiração, não uma garantia de resultado.

## Para quem, primeiro

Profissionais de tecnologia que falam português, no Brasil e em Portugal, procurando vagas remotas
ou internacionais. O recorte inicial é dados e IA, onde as fontes permitidas têm mais oferta. A
plataforma aceita qualquer perfil; a cobertura cresce com as fontes ([dados/fontes.md](dados/fontes.md)).

## Como funciona

1. **Coleta diária** em fontes que permitem coleta, com atribuição e link para a vaga original.
2. **Extração dos sinais** com LLM, medida contra rótulos feitos à mão.
3. **Perfil de busca:** o que a pessoa quer, em texto livre e em filtros (países onde pode
   trabalhar, fuso, salário mínimo e moeda, regimes aceitos, inglês, o que evitar).
4. **Matching:** filtros, busca híbrida (texto e significado), pontuação transparente e uma
   explicação curta: por que combina, o que falta e o que merece atenção.
5. **Entrega:** canal público, lista pessoal, alertas e, depois, um assistente.

## Princípios

1. **Só fontes que permitem.** Nada de raspar quem proíbe; sempre atribuição e link para a vaga.
2. **Precisão antes de volume.** Melhor 20 vagas certas que 200 duvidosas. Selo só com evidência.
3. **Transparência.** Cada sinal mostra a frase que o sustenta; o ranking se explica.
4. **A pessoa decide.** A IA prepara; a pessoa envia. Nada é feito em nome do usuário sem
   aprovação: nem candidatura, nem mensagem, nem contato ([ADR 0022](decisoes/0022-assistente-e-mcp-com-aprovacao.md)).
5. **Dados mínimos.** Só o necessário para buscar; nada sensível; apagar é fácil ([privacidade.md](privacidade.md)).
6. **Custo perto de zero e operação sozinha.**

## Estágios

Cada estágio é um marco e vale sozinho ([marcos/](marcos/README.md)).

| Estágio | O que a pessoa recebe | Marco |
| --- | --- | --- |
| Coleta e sinais | Base interna: vagas coletadas, sinais extraídos e medidos | 1 |
| Lakehouse e qualidade | Histórico, deduplicação, vagas fechadas detectadas, insights do mercado | 2 |
| Canal público (MVP) | Vagas verificadas no site, no Telegram e numa newsletter semanal, sem login | 3 |
| Matching pessoal | Ranking com explicação para um perfil; servidor MCP para assistentes | 4 |
| App beta | Login, perfis salvos, alertas por e-mail e feedback | 5 |
| Assistente | Conversa para montar o perfil, entender o encaixe e preparar a candidatura | 6 |

## Escopo

**Dentro:** vagas de tecnologia de empresas presentes nas fontes permitidas, começando por dados e
IA; sinais de liberdade; canal público; matching; app beta; assistente com aprovação do usuário.

**Fora, por enquanto:** raspar sites que proíbem; candidatura automática; contato automático com
recrutadores; recursos para empregadores (ranquear candidatos, anúncios segmentados); guardar
currículo antes do app beta; previsão de salário; cobrança.

## Metas iniciais (revisáveis)

| Tema | Meta | Onde se mede |
| --- | --- | --- |
| Coleta | Roda todo dia; falha gera alerta | Relatório de saúde e alarme |
| Oferta | Vagas novas por semana em dados e IA, abertas a quem mora no Brasil ou em Portugal | Marts de ouro |
| Extração | 90% ou mais de acerto nos campos principais | `evals/extraction` |
| Selo de elegibilidade | 95% ou mais de precisão | `evals/extraction` |
| Frescor | Vaga fechada sai em até duas coletas | `posting_presence` |
| Matching | nDCG@10 acima da busca por palavra-chave | `evals/matching` |
| Custo | Até US$ 10 por mês depois dos créditos | Fatura e orçamento |

## Limitações conhecidas

- **Cobertura:** só entram empresas presentes nas fontes permitidas. Vagas de empresas que publicam
  só em portais fechados dependem de parceria. Os números publicados dizem qual é o recorte.
- **Sinal ausente não é sinal negativo:** muitas vagas não dizem o salário nem a carga.
- **Salário raro:** poucas vagas informam a faixa (tende a melhorar na UE com a diretiva de
  transparência salarial).
- **Fontes mudam:** empresas trocam de ATS e endpoints mudam; o relatório de saúde diário mostra.

## Visão de longo prazo

Um assistente de oportunidades que entende cada pessoa, mapeia o mercado com amplitude e ajuda a
encontrar, avaliar e conquistar vagas que aumentem a autonomia e a qualidade de vida dela, sempre
com a pessoa no comando das decisões.
