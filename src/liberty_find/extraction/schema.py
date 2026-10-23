"""Esquema da ferramenta que o modelo é obrigado a chamar (saída estruturada via tool use).

O Amazon Nova aceita só um subconjunto de JSON Schema: no topo, apenas `type` (object),
`properties` e `required`. Para não depender de recursos não documentados, cada campo usa
um tipo simples (sem listas de tipos nem anyOf); "nulo quando não informado" vai na
descrição, e quem garante o contrato é a validação com `ExtractedFields` depois da resposta.
Um teste confere que este esquema bate com o modelo (tests/unit/test_extraction_schema.py).
"""

from __future__ import annotations

from typing import Any

from liberty_find.models import (
    ContractType,
    Currency,
    EnglishLevel,
    RoleFamily,
    SalaryPeriod,
    Seniority,
    WorkModel,
)

TOOL_NAME = "record_posting_fields"
# Sobe quando os campos mudam (v2 entra depois da auditoria de rótulos; docs/dados/extracao.md).
SCHEMA_VERSION = "v1"
NULL_NOTE = " Use null quando a vaga não informar."


def _enum(values: list[str], description: str) -> dict[str, Any]:
    return {"type": "string", "enum": values, "description": description}


INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "role_family": _enum(
            [e.value for e in RoleFamily],
            "Família da função, pelo trabalho descrito e não pelo título.",
        ),
        "seniority": _enum([e.value for e in Seniority], "Nível da vaga."),
        "work_model": _enum([e.value for e in WorkModel], "Modelo de trabalho."),
        "contract_type": _enum([e.value for e in ContractType], "Regime de contratação."),
        "english_level": _enum([e.value for e in EnglishLevel], "Nível de inglês pedido."),
        "english_required": {
            "type": "boolean",
            "description": "true se o inglês é obrigatório; false se desejável." + NULL_NOTE,
        },
        "salary_min": {"type": "number", "description": "Menor valor da faixa." + NULL_NOTE},
        "salary_max": {"type": "number", "description": "Maior valor da faixa." + NULL_NOTE},
        "salary_currency": _enum([e.value for e in Currency], "Moeda do salário." + NULL_NOTE),
        "salary_period": _enum([e.value for e in SalaryPeriod], "Período do salário." + NULL_NOTE),
        "years_experience_min": {
            "type": "integer",
            "description": "Anos mínimos de experiência pedidos." + NULL_NOTE,
        },
        "stack": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Até 15 tecnologias citadas, em minúsculas (ex.: python, sql, aws, power bi)."
            ),
        },
    },
    "required": [
        "role_family",
        "seniority",
        "work_model",
        "contract_type",
        "english_level",
        "english_required",
        "salary_min",
        "salary_max",
        "salary_currency",
        "salary_period",
        "years_experience_min",
        "stack",
    ],
}

TOOL_CONFIG: dict[str, Any] = {
    "tools": [
        {
            "toolSpec": {
                "name": TOOL_NAME,
                "description": "Registra os campos estruturados extraídos de uma vaga de emprego.",
                "inputSchema": {"json": INPUT_SCHEMA},
            }
        }
    ],
    "toolChoice": {"tool": {"name": TOOL_NAME}},
}
