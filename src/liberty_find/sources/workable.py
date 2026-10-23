"""Workable (widget público de vagas).

A implementar no Marco 1 (tarefa 1.3), no padrão de greenhouse.py.

Endpoint: GET https://apply.workable.com/api/v1/widget/accounts/{token}
- `https://www.workable.com/api/accounts/{token}` redireciona (302) para o endereço acima.
- Documentado como endpoint público, sem cabeçalho de autenticação
  (https://help.workable.com/hc/en-us/articles/115012771647).
- Campos úteis (conferir numa amostra real antes de codar): `jobs[]` com título, `shortcode`,
  URL, cidade, país e indicação de remoto. A descrição completa pode exigir `?details=true`.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from liberty_find.models import Board, JobPosting, Source

BASE_URL = "https://apply.workable.com/api/v1/widget/accounts/{token}"


class WorkableSource:
    source = Source.WORKABLE

    def fetch_raw(self, board: Board, client: httpx.Client) -> Any:
        raise NotImplementedError("Marco 1, tarefa 1.3: ver docs/marcos/marco-1-coleta.md")

    def normalize(self, board: Board, payload: Any, collected_at: datetime) -> list[JobPosting]:
        raise NotImplementedError("Marco 1, tarefa 1.3: ver docs/marcos/marco-1-coleta.md")
