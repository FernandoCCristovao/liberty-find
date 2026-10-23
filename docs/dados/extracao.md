# Extração com LLM

Transforma o texto de cada vaga em campos estruturados: os de base (família, nível, modelo de
trabalho, regime, inglês, salário, experiência e stack) e os sinais de liberdade que o produto
promete. Decisão e porquê: [ADR 0013](../decisoes/0013-extracao-v2-sinais-de-liberdade.md).

## Estado

| Peça | Estado |
| --- | --- |
| Esquema v1 (`ExtractedFields` em `models.py`), esquema da ferramenta e prompt v1 | No código, com teste de contrato |
| Chamada ao Bedrock (`extract_fields`) e Lambda de extração | A implementar (Marco 1) |
| Esquema v2 (sinais de liberdade) | Candidato, abaixo; entra no código depois da auditoria de rótulos |

## Esquema v2 candidato

Os campos v1 continuam. Os novos ou alterados:

| Campo | Tipo | Valores e regra |
| --- | --- | --- |
| `role_family` | enum | v1 mais `data_science` e `infrastructure` (DevOps, SRE, cloud, plataforma) |
| `remote_scope` | enum | `worldwide`, `regions`, `countries`, `not_informed`. "Remoto" sem restrição escrita é `not_informed`, nunca `worldwide` |
| `remote_countries` | lista | Códigos ISO 3166-1 alfa-2 (`BR`, `PT`, `US`), só quando escritos |
| `remote_regions` | lista de enum | `latam`, `americas`, `north_america`, `europe`, `emea`, `apac` |
| `timezone_utc_min`, `timezone_utc_max` | inteiro ou nulo | Faixa de fuso exigida, quando escrita como faixa ou fuso nomeado |
| `contract_type` | enum | `clt`, `pj`, `employee_other` (vínculo de emprego fora do Brasil, inclusive via EOR), `contractor_international` (contrato com empresa estrangeira), `internship`, `other`, `not_informed` |
| `salary_currency` | enum | v1 mais `GBP` |
| `salary_period` | enum | v1 mais `day` |
| `languages_required` | lista | Idiomas exigidos além do inglês, em ISO 639-1 (`pt`, `es`, `de`) |
| `visa_sponsorship`, `relocation_support` | enum | `yes`, `no`, `not_informed` |
| `time_signals` | lista de enum | `on_call`, `overtime`, `weekend_work`, `shift_work`, `flexible_hours`, `async_first`, `four_day_week`, `part_time`; só o que está escrito |
| `summary_en` | texto | Uma ou duas frases em inglês: a função, as responsabilidades e a stack principal. Sem texto institucional e sem dado pessoal. Alimenta a busca ([ADR 0014](../decisoes/0014-embeddings-multilingues.md)) |
| `evidence` | lista | Até 8 pares {`field`, `quote`}, com citação de até 200 caracteres no idioma original, para cada sinal de liberdade preenchido |

**Selo de elegibilidade** (derivado, não extraído): uma função Python pura e testada calcula
"aberta", "não aberta" ou "a confirmar" para quem mora no Brasil e para quem mora em Portugal, a
partir de `work_model`, `remote_scope`, países e regiões, e dos campos estruturados das fontes
(`workplaceType` e `country` da Lever, `isRemote` e locais da Ashby). Ela existe desde o Marco 1,
para a escolha do modelo poder medir o selo; no Marco 2, a mesma regra é espelhada em SQL na camada
de ouro, com um teste de que as duas concordam. Meta: 95% de precisão em "aberta", medida em pelo
menos 60 vagas abertas que não foram usadas para ajustar o prompt (o conjunto de avaliação, mais a
fatia do selo da auditoria, se faltar).

## Auditoria de rótulos (Marco 1)

Antes de pôr o esquema v2 no código:

1. Amostra de 200 vagas estratificada por fonte, idioma, nível e modelo de trabalho, com vagas
   remotas a mais para garantir pelo menos 60 casos de vaga aberta a quem mora no Brasil ou em
   Portugal.
2. Pré-rótulo por um modelo maior que não participa da escolha (para não favorecer um candidato),
   corrigido campo a campo à mão, numa ferramenta local (`tools/annotator`, Streamlit) ou planilha.
   O arquivo de rótulos guarda só `posting_id`, `content_hash` e os valores; o texto das vagas fica
   no bucket privado.
3. Para cada campo, medir a cobertura (em quantas vagas o sinal está escrito). Depois de uma semana,
   rotular de novo 20 vagas para medir a própria consistência.
4. Regra de corte: campo com cobertura abaixo de 10% ou acerto do melhor modelo abaixo de 85% sai do
   esquema ou vira experimental (extraído, mas não exibido).
5. Divisão: 100 vagas para ajustar o prompt e 100 para a escolha do modelo, com as vagas abertas
   repartidas por igual entre as duas metades.
6. Fatia do selo: se a metade de avaliação tiver menos de 60 vagas abertas, rotular só os campos de
   elegibilidade (`work_model`, `remote_scope`, `remote_countries` e `remote_regions`) em vagas
   remotas novas até chegar a 60. É rápido, porque só se lê a parte de local da vaga, e dá ao selo,
   a métrica que mais pesa na confiança do canal, uma medida menos incerta.

## Escolha do modelo (Marco 1)

- Conjunto: as 100 vagas de avaliação, separadas das usadas para ajustar o prompt; para o selo,
  também a fatia do selo, se ela existir.
- Candidatos: Nova Lite, Claude Haiku 5.5 e um piso barato (Nova Micro). Conferir antes o preço, a
  disponibilidade na região e o suporte a saída estruturada.
- Métricas por campo: acurácia e F1 macro (enums); precisão, revocação e F1 (listas); acerto exato
  (moeda e período); tolerância de 1% (valores); precisão de `not_informed`. Mais a precisão do
  selo, o custo e a latência por mil vagas.
- Vence o modelo mais barato com 90% ou mais nos campos principais (`role_family`, `seniority`,
  `work_model`, elegibilidade remota, `english_level`), 95% ou mais de precisão no selo e custo
  projetado dentro do orçamento.
- O resultado vai para uma tabela no README e para o ADR, se mudar a escolha.

## Como funciona

1. **Entrada:** as vagas do dia em `postings/`. Só vão ao modelo as que não estão no manifesto com
   a mesma chave (`content_hash`, `schema_version`, `prompt_version`, `model_id`).
2. **Pré-processamento:** HTML para texto, remoção de trechos padrão (texto institucional,
   benefícios genéricos, aviso de igualdade de oportunidades), remoção de contatos pessoais,
   detecção de idioma e corte em `MAX_DESCRIPTION_CHARS`.
3. **Chamada:** Bedrock Converse com `temperature` 0 e o prompt versionado (`extraction/prompt.py`).
   Saída estruturada por tool use forçado (`toolChoice` com o nome da ferramenta) ou pela saída
   estruturada nativa, quando o modelo suportar. A descrição vai entre delimitadores, como dado,
   com a instrução explícita de que nada dentro dela é instrução para o modelo.
4. **Validação:** a resposta passa por `ExtractedFields`. Falhou: uma nova tentativa com o erro;
   falhou de novo: o modelo de reserva; persistindo, a vaga entra como falha no relatório e a
   execução segue. O `stop_reason` vai para o log.
5. **Gravação:** `extractions/dt=<dia>/extractions.jsonl.gz`, a resposta bruta para auditoria e o
   manifesto atualizado.
6. **Carga inicial e reextração** em lote no Bedrock (50% mais barato); o delta diário sob demanda
   enquanto for pequeno, e em lote quando passar do mínimo de registros do lote (cerca de mil).

## Esquema da ferramenta

Escrito à mão em `extraction/schema.py`, porque o Amazon Nova aceita só um subconjunto de JSON
Schema: no topo, apenas `type`, `properties` e `required`. Cada campo usa um tipo simples; "nulo
quando não informado" vai na descrição do campo, e quem garante o contrato é a validação com
pydantic. O teste `test_extraction_schema.py` impede que o esquema e o modelo se separem. Com o
esquema v2, conferir se listas de objetos (`evidence`) funcionam em cada candidato; se não, a
alternativa é uma lista de textos.

## Regras de decisão

| Campo | Regra |
| --- | --- |
| `role_family` | Pelo trabalho descrito, não pelo título. Construir sistemas com LLM, ML ou agentes é `ai`; pipelines e plataformas de dados, `data_engineering`; modelagem estatística e análise exploratória, `data_science`; painéis e relatórios, `analytics_bi`; modelagem analítica no estilo dbt, `analytics_engineering` |
| `seniority` | Estágio, júnior, pleno, sênior; especialista, staff e principal viram `staff_plus`; gestão de pessoas, `manager` |
| `work_model` | Remoto e home office, `remote`; híbrido, `hybrid`; presencial, `onsite`. O texto vale mais que o campo da fonte, e a divergência fica registrada |
| Elegibilidade remota | Só restrição escrita: "Remote (US only)" vira `countries` com `US`; "LATAM" vira `regions` com `latam`; "anywhere" vira `worldwide`; sem nada escrito, `not_informed` |
| `contract_type` | CLT, `clt`; PJ ou prestador no Brasil, `pj`; contrato de trabalho em outro país ou via EOR, `employee_other`; contractor de empresa estrangeira, `contractor_international` |
| Inglês | Nível pedido; obrigatório (`true`), desejável ou diferencial (`false`), não citado (nulo) |
| Salário | Só com número escrito. Campo de remuneração do ATS tem prioridade sobre o texto |
| `time_signals` | Só menção explícita: plantão e sobreaviso, `on_call`; horas extras, `overtime`; horário flexível, `flexible_hours`; semana de quatro dias, `four_day_week` |
| `stack` | Até 15 tecnologias citadas, em minúsculas e com nome canônico (`power bi`, não `PowerBI`) |

Mudou alguma regra no texto do prompt: suba `PROMPT_VERSION`. Mudou o esquema: suba
`SCHEMA_VERSION`. As vagas são reextraídas aos poucos, dentro do teto por execução.

## Limites e custo

| Parâmetro | Padrão | Por quê |
| --- | --- | --- |
| `MAX_DESCRIPTION_CHARS` | 12.000 caracteres | Custo e latência previsíveis |
| `MAX_EXTRACTIONS_PER_RUN` | 300 vagas | A primeira carga se espalha e o custo diário fica previsível; sobe junto com o orçamento quando a escala crescer |
| Concorrência | 4 chamadas simultâneas | Abaixo das cotas padrão de uma conta nova |
| `maxTokens` da resposta | 800 no v1; 1.000 no v2 | O esquema v2 tem mais campos e as evidências |

Ordem de grandeza: cerca de 1.200 tokens de entrada por vaga depois do corte de trechos padrão (até
3.000 sem corte) e de 300 a 500 de saída. Na escala de 2 mil vagas novas ou alteradas por dia, com
1.200 de entrada e 300 de saída, por mês: Nova Micro cerca de US$ 5 sob demanda (2,50 em lote), Nova
Lite cerca de 8,60 (4,30) e Claude Haiku 5.5 cerca de 16 (8). Com as primeiras dezenas de empresas,
centavos. Confira o preço do dia antes da primeira carga completa e anote o custo real no README.

## Testes

Unitários com `botocore.stub.Stubber` no cliente `bedrock-runtime`: resposta válida, resposta
inválida seguida de válida (nova tentativa), inválida duas vezes (modelo de reserva e depois falha
registrada), corte da descrição e idempotência pela chave. O teste de contrato do esquema cobre v1
e, quando entrar, v2.
