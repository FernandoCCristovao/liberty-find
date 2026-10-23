"""Lever Postings API.

A implementar no Marco 1 (tarefa 1.3), no padrão de greenhouse.py.

Endpoint: GET https://api.lever.co/v0/postings/{token}?mode=json
- Público: vagas publicadas são "publicly viewable" (https://github.com/lever/postings-api).
- Paginação: parâmetros `skip` e `limit`; buscar até a página vir vazia.
- Campos úteis (conferir numa amostra real antes de codar): `id`, `text` (título),
  `hostedUrl`, `categories` (location, team, commitment), `workplaceType`, `country`,
  `descriptionPlain`, `createdAt` (epoch em milissegundos).
- `workplaceType` às vezes contradiz a descrição: guardar como veio; a extração decide.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from liberty_find.models import Board, JobPosting, Source

BASE_URL = "https://api.lever.co/v0/postings/{token}"


class LeverSource:
    source = Source.LEVER

    def fetch_raw(self, board: Board, client: httpx.Client) -> Any:
        raise NotImplementedError("Marco 1, tarefa 1.3: ver docs/marcos/marco-1-coleta.md")

    def normalize(self, board: Board, payload: Any, collected_at: datetime) -> list[JobPosting]:
        raise NotImplementedError("Marco 1, tarefa 1.3: ver docs/marcos/marco-1-coleta.md")
