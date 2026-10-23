@AGENTS.md

## Notas para o Claude Code

- Antes de mudanças em vários arquivos, use o modo de plano e espere aprovação.
- As permissões do projeto estão em `.claude/settings.json`: lint e testes rodam sem pedir; as formas
  mais comuns de deploy, de remoção de stack e de remoção no S3 estão negadas. A lista é uma proteção
  de conveniência, não uma barreira: a barreira real é não deixar credencial de deploy disponível sem
  aprovação humana.
- Código gerado vem com uma explicação curta do que faz e por quê: quem mantém o projeto precisa
  conseguir explicar cada linha.
- Contexto de gestão do projeto fica fora deste repositório. Não traga anotações pessoais para cá.
