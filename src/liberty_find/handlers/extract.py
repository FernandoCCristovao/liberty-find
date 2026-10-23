"""Lambda de extração com LLM. A implementar no Marco 1, tarefa 1.6.

Fluxo previsto (docs/dados/extracao.md):
1. Ler `postings/dt=<dia>/postings.jsonl.gz` (evento do S3 ou chamada direta).
2. Descartar o que já foi extraído: manifesto `state/extracted.jsonl.gz`, com a chave
   (posting_id, content_hash, schema_version, prompt_version, model_id).
3. Para as novas, até MAX_EXTRACTIONS_PER_RUN, chamar `extract_fields` com concorrência limitada.
4. Gravar `extractions/dt=<dia>/extractions.jsonl.gz` e atualizar o manifesto.

Não registrar esta função no template.yaml antes de implementada e testada.
"""

from __future__ import annotations

from typing import Any


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    raise NotImplementedError("Marco 1, tarefa 1.6: ver docs/marcos/marco-1-coleta.md")
