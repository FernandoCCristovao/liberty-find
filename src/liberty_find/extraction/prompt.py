"""Prompt versionado da extração. Mudou o texto, suba PROMPT_VERSION: as vagas são reextraídas.

As regras de decisão de cada campo estão em docs/dados/extracao.md; este texto é a versão
que vai para o modelo.
"""

from __future__ import annotations

PROMPT_VERSION = "v1"

# Limite de caracteres da descrição enviada ao modelo (custo e latência previsíveis).
MAX_DESCRIPTION_CHARS = 12_000

SYSTEM_PROMPT = """\
You extract structured fields from job postings published by companies hiring in Brazil.
Postings may be in Portuguese or English. Use only what the posting states; never guess.
When a field is not stated, use "not_informed" (enums) or null (other fields).

Rules:
- role_family: classify by the work described, not by the title.
  ai = builds LLM, ML or agent systems; data_engineering = pipelines, data platforms;
  analytics_bi = dashboards, reporting, BI tools; analytics_engineering = dbt-style modeling
  for analytics; automation = workflow or RPA automation; software = general software
  engineering; other = anything else.
- seniority: estágio = intern; júnior = junior; pleno = mid; sênior = senior;
  especialista, staff, principal = staff_plus;
  coordenação, gerência, liderança de pessoas = manager.
- work_model: remoto/100% remoto/home office = remote; híbrido = hybrid; presencial = onsite.
- contract_type: CLT = clt; PJ, pessoa jurídica, prestador = pj; cooperado, estágio,
  temporário, contractor abroad = other.
- english_level: "fluente" = fluent; "avançado" = advanced; "intermediário" = intermediate;
  "básico" = basic; explicitly not needed = none. english_required = true when mandatory,
  false when "desejável", "diferencial" or "nice to have", null when English is not mentioned.
- salary: only when a number is stated. Monthly Brazilian salaries use salary_period = month.
- stack: up to 15 technologies explicitly cited, lowercase, canonical names
  (e.g. "python", "sql", "aws", "power bi", "dbt", "spark", "langchain").

Always answer by calling the tool. Do not write any other text.
"""


def build_user_message(title: str, company: str, location: str | None, description: str) -> str:
    """Mensagem com os dados da vaga. A descrição é cortada em MAX_DESCRIPTION_CHARS."""
    return (
        f"Title: {title}\n"
        f"Company: {company}\n"
        f"Location: {location or 'not stated'}\n\n"
        f"Description:\n{description[:MAX_DESCRIPTION_CHARS]}"
    )
