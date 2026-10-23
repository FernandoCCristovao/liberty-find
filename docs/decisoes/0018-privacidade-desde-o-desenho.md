# ADR 0018: Privacidade desde o desenho (LGPD)

- Status: aceita (região do beta revista pelo [ADR 0024](0024-conta-aws-experiencia-nova-us-east-2.md))
- Data: 2026-10-20

## Contexto

Até o canal público (Marco 3), o projeto quase não trata dado pessoal: vagas são informação
publicada por empresas, e a newsletter guarda só o e-mail de quem assina. A partir do matching
pessoal e do app (Marcos 4 e 5), entram preferências de cada pessoa: salário mínimo, países onde
pode trabalhar, idiomas, o que quer evitar, feedback e, talvez, currículo. Pontos da LGPD que
pesam no desenho ([lei](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)):

- O titular pode pedir revisão e explicação de decisão tomada só por tratamento automatizado,
  incluindo perfil (art. 20).
- O regime simplificado para agentes de pequeno porte (Resolução CD/ANPD 2/2022) deixa de valer
  para tratamento de alto risco, e tecnologia emergente com perfilamento automatizado pode
  enquadrar.
- Transferência internacional (por exemplo, para APIs de LLM fora do Brasil) precisa de base legal;
  cláusulas-padrão só valem adotadas na íntegra (Resolução CD/ANPD 19/2024).
- Incidente com risco relevante: comunicação à ANPD e aos titulares em 3 dias úteis (Resolução
  CD/ANPD 15/2024), prazo dobrado para agentes de pequeno porte.
- A descrição de uma vaga pode trazer nome, e-mail ou telefone de recrutador.

## Decisão

As regras detalhadas ficam em [privacidade.md](../privacidade.md). Em resumo:

1. **Minimização:** só o necessário para buscar. Sem currículo antes do app beta; sem campo de dado
   sensível; a pergunta é "em quais países você pode trabalhar", nunca a nacionalidade.
2. **Um lugar só para dado pessoal:** o banco de serviço, com row-level security por usuário. O
   lago guarda só vagas e métricas agregadas.
3. **LLM recebe o mínimo:** preferências pseudonimizadas, sem nome nem e-mail, por provedor que não
   treina com os dados (Bedrock).
4. **Logs sem dado pessoal** e sem texto de vaga; contato de recrutador (e-mail e telefone) é
   removido na normalização, e o bruto, que guarda o original, expira em 90 dias.
5. **Direitos na prática:** exportar e apagar a conta pelo próprio app; explicação de por que cada
   vaga apareceu (o matching é explicável por desenho).
6. **Aviso de privacidade em português** publicado antes do primeiro usuário externo, nomeando os
   fornecedores e os países onde os dados são tratados.
7. **Região e transferência:** `us-east-1` no beta fechado. Antes do primeiro usuário externo
   (Marco 5): aviso publicado, base da transferência internacional documentada, página sobre as
   transferências e pedido dos aditivos aos fornecedores. Antes de abrir cadastro público: avaliar
   `sa-east-1` para os dados pessoais.

## Alternativas consideradas

- **Pedir currículo desde o início:** personalização maior, com risco e obrigação muito maiores
  antes de saber se o produto tem demanda.
- **Tudo em `sa-east-1` desde já:** menos transferência, mas menos modelos no Bedrock, preços
  maiores e latência com a plataforma de dados.

## Consequências

- Recursos que tocam dado pessoal precisam de revisão contra [privacidade.md](../privacidade.md) no
  pull request.
- O projeto pode crescer para o GDPR (usuários na UE) sem refazer o desenho.

## Rever se

Entrar upload de currículo, abrir cadastro público, chegar o primeiro pagante ou o primeiro usuário
na UE (GDPR, inclusive o representante do art. 27).
