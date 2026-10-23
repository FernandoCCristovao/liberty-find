"""Chamada ao Bedrock (Converse API com tool use). A implementar no Marco 1, tarefa 1.6.

Contrato esperado (ver docs/dados/extracao.md):
- `converse(modelId=..., system=[{"text": SYSTEM_PROMPT}], messages=[...],
  toolConfig=TOOL_CONFIG, inferenceConfig={"temperature": 0, "maxTokens": 800})`
  (800 no esquema v1; 1.000 no v2).
- Ler o bloco `toolUse` da resposta e validar com `ExtractedFields.model_validate`.
- Erro de validação: uma nova tentativa; persistindo, registrar a vaga como falha e seguir.
- Testes com `botocore.stub.Stubber`, sem rede.
"""

from __future__ import annotations

from typing import Any

from liberty_find.models import ExtractedFields, JobPosting

DEFAULT_MODEL_ID = "us.amazon.nova-lite-v1:0"


def extract_fields(
    posting: JobPosting, client: Any, model_id: str = DEFAULT_MODEL_ID
) -> ExtractedFields:
    """Extrai os campos estruturados de uma vaga."""
    raise NotImplementedError("Marco 1, tarefa 1.6: ver docs/marcos/marco-1-coleta.md")
