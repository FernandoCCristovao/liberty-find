"""Ashby Public Job Posting API.

A implementar no Marco 1 (tarefa 1.3), no padrão de greenhouse.py.

Endpoint: GET https://api.ashbyhq.com/posting-api/job-board/{token}?includeCompensation=true
- Respondeu JSON sem credenciais em 2026-10-12 (https://developers.ashbyhq.com/docs/public-job-posting-api).
- Campos úteis (conferir numa amostra real antes de codar): `jobs[]` com `id`, `title`,
  `jobUrl`, `location`, `isRemote`, `workplaceType`, `descriptionPlain`, `publishedAt`
  e, com includeCompensation, a faixa salarial.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from liberty_find.models import Board, JobPosting, Source

BASE_URL = "https://api.ashbyhq.com/posting-api/job-board/{token}"


class AshbySource:
    source = Source.ASHBY

    def fetch_raw(self, board: Board, client: httpx.Client) -> Any:
        raise NotImplementedError("Marco 1, tarefa 1.3: ver docs/marcos/marco-1-coleta.md")

    def normalize(self, board: Board, payload: Any, collected_at: datetime) -> list[JobPosting]:
        raise NotImplementedError("Marco 1, tarefa 1.3: ver docs/marcos/marco-1-coleta.md")
