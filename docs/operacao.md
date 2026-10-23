# Operação

Como publicar, acompanhar e desligar o Liberty Find. Deploy, remoção e gasto novo só com aprovação
humana.

## Preparação (uma vez)

A conta é um projeto do cadastro novo da AWS, com região fixa em `us-east-2` e políticas geridas
pela AWS ([ADR 0024](decisoes/0024-conta-aws-experiencia-nova-us-east-2.md)).

1. **Plano:** o gratuito não gera cobrança e cobre os serviços do Marco 1. No pago, defina em
   https://settings.aws.com um limite de gasto mensal (a partir de US$ 20): ao chegar nele, a AWS
   pausa o projeto em vez de cobrar mais.
2. **Login protegido:** verificação em duas etapas no provedor de login (por exemplo, o Google) ou
   MFA no AWS Builder ID.
3. **Orçamento** no AWS Budgets: US$ 10 por mês, com alerta por e-mail, se a conta permitir
   (depois da tarefa 1.2, ele vem do Terraform).
4. **Ferramentas:** [uv](https://docs.astral.sh/uv/), AWS CLI v2 (2.32 ou mais novo, para o
   `aws login`) e Terraform 1.11 ou mais novo (até a tarefa 1.2, o AWS SAM CLI).
5. **Perfil da CLI**, sem chave fixa: `aws configure set region us-east-2 --profile liberty-find`
   e `aws login --region us-east-2 --profile liberty-find`; confira com
   `aws sts get-caller-identity --profile liberty-find`. A credencial vale 12 horas e se renova por
   até 90 dias sem voltar ao navegador.
6. Copie `.env.example` para `.env` e preencha `AWS_PROFILE` e `ALERT_EMAIL`.
7. **Cota de concorrência do Lambda:** `aws lambda get-account-settings --profile liberty-find`
   mostra a cota; contas novas começam baixas. Peça o aumento antes de usar concorrência reservada.

**Onde guardar o repositório:** fora de pastas sincronizadas (Google Drive, OneDrive, Dropbox). A
sincronização corrompe o `.git`; a cópia de segurança do código é o próprio GitHub.

## Publicar

Até a migração para Terraform (Marco 1, tarefa 1.2):

```bash
uv run poe check     # tudo verde antes de publicar
uv run poe build     # gera src/requirements.txt e roda sam build
uv run poe deploy    # sam deploy: mostra o changeset e pede confirmação
```

Depois da migração, o fluxo passa a ser `uv run poe package`, `terraform plan` e `terraform apply`
no ambiente escolhido em `infra/envs/`, sempre lendo o plano antes de aplicar. Esta seção é
reescrita na tarefa 1.2.

No primeiro deploy, confirme a inscrição no e-mail que o SNS manda (sem isso o alarme não chega).

## Primeiro teste depois do deploy

```bash
aws lambda invoke --function-name <nome da Lambda de coleta> --profile liberty-find saida.json
```

O nome da função aparece nas saídas da stack. Depois, confira `health/dt=<hoje>/health.json` no
bucket e rode no Athena, com o workgroup `liberty-find`:

```sql
SELECT company, count(*) AS vagas
FROM liberty_find.postings
WHERE dt = '2026-10-21'
GROUP BY company
ORDER BY vagas DESC;
```

## Rotina

Nenhuma: a coleta roda todo dia às 06:00 (America/Sao_Paulo). Olhe o relatório de saúde quando
chegar alerta ou quando um número parecer estranho. A partir do Marco 3, a edição semanal da
newsletter tem revisão humana antes do envio.

## Custos e proteções

| Proteção | Onde |
| --- | --- |
| Limite de 1 GB lido por consulta | Workgroup `liberty-find` |
| Bruto expira em 90 dias, resultados de consulta em 7 | Regras de ciclo de vida do bucket |
| Teto de extrações e de tokens por execução | Variáveis da Lambda de extração |
| Orçamento mensal com alerta | AWS Budgets |
| Logs com retenção de 30 dias | Grupos de logs |
| Lambdas fora de VPC (sem NAT Gateway) | Infraestrutura como código |
| Nada com custo fixo sem ADR | Regra 6 do AGENTS.md e [ADR 0020](decisoes/0020-observabilidade-avaliacao-custo.md) |

## Problemas comuns

| Sintoma | O que fazer |
| --- | --- |
| Empresa em `error` com HTTP 404 | Trocou de ATS ou de token: procure o novo ([dados/fontes.md](dados/fontes.md)) ou marque `enabled: false` |
| Todas as empresas em `error` | Veja o log da Lambda; costuma ser rede ou mudança grande numa API |
| Número de vagas de uma empresa caiu pela metade de uma vez | Quarentena: confira a API antes de fechar vagas |
| Alerta não chega | Confirme a inscrição do e-mail no tópico do SNS |
| Athena recusa a consulta por limite de bytes | Filtre por `dt`; o limite existe para isso |
| Bedrock com `ThrottlingException` | Baixe a concorrência ou o teto por execução |
| `sam build` falha com dependência compilada no Windows | `sam build --use-container` (precisa do Docker) |

## Desligar

Remover a stack (`sam delete --stack-name liberty-find` até a tarefa 1.2; `terraform destroy`
depois) apaga a infraestrutura. O bucket só some vazio, e esvaziar é irreversível: decisão humana,
nunca automática.
