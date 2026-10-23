"""Coleta diária: busca cada empresa, normaliza e grava bruto, vagas e relatório de saúde.

Regra de robustez: uma empresa que falha não derruba as outras. A execução só falha
(e dispara o alarme) quando nenhuma empresa deu certo.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Literal

import httpx
from pydantic import BaseModel

from liberty_find.models import Board, JobPosting, Source
from liberty_find.sources import SourceClient
from liberty_find.storage import Sink, health_key, postings_key, raw_key

logger = logging.getLogger(__name__)

BoardStatus = Literal["ok", "error", "skipped"]


class BoardResult(BaseModel):
    source: Source
    board: str
    status: BoardStatus
    postings: int = 0
    detail: str | None = None


class CollectionReport(BaseModel):
    collected_at: datetime
    boards: list[BoardResult]
    postings_total: int
    postings_key: str

    @property
    def ok_count(self) -> int:
        return sum(1 for b in self.boards if b.status == "ok")


class CollectionFailedError(RuntimeError):
    """Nenhuma empresa foi coletada: a Lambda falha de propósito para o alarme disparar."""


def run_collection(
    boards: Sequence[Board],
    sources: Mapping[Source, SourceClient],
    sink: Sink,
    client: httpx.Client,
    now: datetime,
) -> CollectionReport:
    day = now.date()
    results: list[BoardResult] = []
    postings: dict[str, JobPosting] = {}

    for board in (b for b in boards if b.enabled):
        source = sources.get(board.source)
        if source is None:
            results.append(
                BoardResult(
                    source=board.source,
                    board=board.token,
                    status="skipped",
                    detail="sem implementação",
                )
            )
            continue
        try:
            payload = source.fetch_raw(board, client)
            # o bruto é gravado antes de normalizar: se a normalização falhar, dá para reprocessar
            sink.write_json_gz(raw_key(board.source.value, board.token, day), payload)
            board_postings = source.normalize(board, payload, now)
        except Exception as exc:  # uma empresa com problema não pode parar a coleta
            logger.exception("falha na coleta de %s/%s", board.source.value, board.token)
            results.append(
                BoardResult(
                    source=board.source, board=board.token, status="error", detail=repr(exc)[:300]
                )
            )
            continue
        for posting in board_postings:
            postings[posting.posting_id] = posting
        results.append(
            BoardResult(
                source=board.source, board=board.token, status="ok", postings=len(board_postings)
            )
        )

    key = postings_key(day)
    sink.write_jsonl_gz(key, (p.model_dump(mode="json") for p in postings.values()))
    report = CollectionReport(
        collected_at=now, boards=results, postings_total=len(postings), postings_key=key
    )
    sink.write_json(health_key(day), report.model_dump(mode="json"))

    attempted = [r for r in results if r.status != "skipped"]
    if attempted and report.ok_count == 0:
        msg = f"nenhuma das {len(attempted)} empresas foi coletada"
        raise CollectionFailedError(msg)
    return report
