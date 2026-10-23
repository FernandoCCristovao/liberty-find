# ADR 0006: Só APIs públicas de ATS; descrição nunca publicada

- Status: substituída pelo [ADR 0009](0009-fontes-por-permissao.md)
- Data: 2026-10-12

## Contexto

Os maiores sites de vagas (LinkedIn, Glassdoor, Indeed e Gupy) proíbem coleta automática nos
termos de uso ou no robots.txt. Greenhouse, Lever, Ashby e Workable oferecem APIs públicas
documentadas, sem autenticação, para as vagas publicadas. As descrições têm autoria das empresas
e podem conter dados de recrutadores.

## Decisão

- Coletar só das APIs públicas listadas em `docs/dados/fontes.md`.
- Uma chamada por empresa por dia, com User-Agent identificável.
- Guardar a descrição só no S3 privado, para análise e busca internas.
- Publicar só campos derivados, agregados e o link para a vaga original.

## Alternativas consideradas

- Raspar sites de vagas: maior cobertura, mas viola termos de uso e expõe o projeto.
- Comprar dados de vagas: custo e licença incompatíveis com um projeto aberto.

## Consequências

- Cobertura parcial (só empresas nessas APIs), que o painel declara.
- O projeto pode ser mostrado publicamente sem risco de conformidade.

## Rever se

Uma fonte relevante passar a oferecer API pública, ou uma das APIs atuais mudar os termos.
