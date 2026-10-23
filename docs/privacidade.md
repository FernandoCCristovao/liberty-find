# Privacidade e dados pessoais

Regras de como o Liberty Find trata dado pessoal. A decisão e o porquê estão no
[ADR 0018](decisoes/0018-privacidade-desde-o-desenho.md). Vale para código, logs, prompts, testes e
documentação. Este texto não é parecer jurídico.

## Que dado pessoal existe

| Dado | Desde | Onde fica |
| --- | --- | --- |
| E-mail de quem assina a newsletter | Marco 3 | Na plataforma da newsletter |
| Contato de recrutador dentro do texto de uma vaga | Marco 1 | Só no bruto privado, que expira em 90 dias; removido na normalização |
| Conta (e-mail) e perfil de busca | Marcos 4 e 5 | Banco de serviço, com isolamento por usuário |
| Feedback (vaga marcada, motivo) | Marco 5 | Banco de serviço |
| Currículo (opcional) | Não antes do Marco 5, e só com ADR próprio | A decidir |

O lago (S3, Athena) guarda vagas e números agregados. Nunca guarda dado de usuário.

## Regras

1. **Minimização.** Pergunte só o que muda o resultado da busca. Nada de dado sensível (origem
   racial ou étnica, religião, opinião política, filiação sindical, saúde, vida sexual, genética,
   biometria). Para elegibilidade, pergunte "em quais países você pode trabalhar", nunca a
   nacionalidade.
2. **Um lugar só.** Dado de usuário vive no banco de serviço, com row-level security por usuário;
   o papel do app não é dono das tabelas e as políticas são forçadas.
3. **LLM recebe o mínimo.** Para explicar o encaixe, o modelo recebe preferências pseudonimizadas
   (sem nome, sem e-mail, sem identificador externo) e os campos da vaga. Só provedores que não
   treinam com os dados enviados.
4. **Nada pessoal em log, métrica ou rastreio de LLM.** Use o identificador interno do usuário.
   Texto de vaga também não vai para log.
5. **Testes e fixtures** usam dados inventados. Nunca e-mail, nome ou perfil real.
6. **Direitos.** Pelo próprio app: ver e exportar os dados, corrigir o perfil e apagar a conta (o
   apagamento remove perfil, feedback e cache de explicações). Cada vaga mostrada tem o porquê.
7. **Retenção.** Conta apagada some do banco na rotina seguinte; cópias de segurança expiram no
   ciclo do provedor. Logs de acesso do app são guardados por 6 meses quando o projeto operar como
   empresa (Marco Civil da Internet, art. 15).
8. **Aviso de privacidade em português**, publicado antes do primeiro usuário externo, com
   finalidade, base legal, fornecedores, países onde os dados são tratados, prazos e canal de
   contato.
9. **Incidente.** Suspeita de vazamento: conter, registrar e avaliar o risco no mesmo dia. Com risco
   relevante, comunicar à ANPD e aos titulares no prazo da Resolução CD/ANPD 15/2024.

## Checklist do pull request que toca dado pessoal

- [ ] O dado novo é necessário para a busca? Está nesta tabela?
- [ ] Fica só no banco de serviço, com política de isolamento testada?
- [ ] Não aparece em log, métrica, rastreio de LLM nem mensagem de erro?
- [ ] O prompt recebe só o mínimo, sem identificação direta?
- [ ] Exportar e apagar a conta continuam cobrindo o dado novo?
- [ ] O aviso de privacidade precisa mudar?
