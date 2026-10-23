"""Greenhouse Job Board API: implementação de referência para as outras fontes.

Endpoint: GET https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true
Sem autenticação nos GETs. O campo `content` vem com o HTML escapado como entidades.
Documentação: https://developers.greenhouse.io/job-board.html
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from liberty_find.models import Board, JobPosting, Source
from liberty_find.text import content_hash, html_to_text, posting_id

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs"


class GreenhouseSource:
    source = Source.GREENHOUSE

    def fetch_raw(self, board: Board, client: httpx.Client) -> Any:
        response = client.get(BASE_URL.format(token=board.token), params={"content": "true"})
        response.raise_for_status()
        return response.json()

    def normalize(self, board: Board, payload: Any, collected_at: datetime) -> list[JobPosting]:
        jobs = payload.get("jobs", []) if isinstance(payload, dict) else []
        return [self._to_posting(board, job, collected_at) for job in jobs]

    def _to_posting(self, board: Board, job: dict[str, Any], collected_at: datetime) -> JobPosting:
        job_id = str(job["id"])
        title = str(job["title"]).strip()
        description = html_to_text(job.get("content") or "", escaped=True)
        departments = job.get("departments") or []
        location = (job.get("location") or {}).get("name")
        return JobPosting(
            posting_id=posting_id(self.source.value, board.token, job_id),
            source=self.source,
            board=board.token,
            company=board.company,
            source_job_id=job_id,
            title=title,
            url=job["absolute_url"],
            location=location,
            workplace_type=None,  # o Greenhouse não tem campo próprio; a extração infere
            country=None,
            department=departments[0].get("name") if departments else None,
            language=job.get("language"),
            description_text=description,
            content_hash=content_hash(title, description),
            published_at=job.get("first_published"),
            updated_at=job.get("updated_at"),
            collected_at=collected_at,
        )
