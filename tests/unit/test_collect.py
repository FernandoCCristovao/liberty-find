import gzip
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import pytest

from liberty_find.collect import CollectionFailedError, run_collection
from liberty_find.models import Board, JobPosting, Source
from liberty_find.sources import SourceClient
from liberty_find.sources.greenhouse import GreenhouseSource
from liberty_find.storage import LocalSink


class FixtureSource:
    """Fonte falsa: devolve o payload da fixture para `ok` e falha para `quebrado`."""

    source = Source.GREENHOUSE

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def fetch_raw(self, board: Board, client: httpx.Client) -> Any:
        if board.token == "quebrado":
            raise httpx.ConnectError("sem conexão")
        return self.payload

    def normalize(self, board: Board, payload: Any, collected_at: datetime) -> list[JobPosting]:
        return GreenhouseSource().normalize(board, payload, collected_at)


def _boards() -> list[Board]:
    return [
        Board(source=Source.GREENHOUSE, token="ok", company="OK"),
        Board(source=Source.GREENHOUSE, token="quebrado", company="Quebrado"),
        Board(source=Source.LEVER, token="semfonte", company="Sem fonte"),
        Board(source=Source.GREENHOUSE, token="desligado", company="Desligado", enabled=False),
    ]


def test_one_failing_board_does_not_stop_the_run(
    tmp_path: Path, greenhouse_payload: dict[str, Any], now: datetime
) -> None:
    sources: dict[Source, SourceClient] = {Source.GREENHOUSE: FixtureSource(greenhouse_payload)}
    with httpx.Client() as client:
        report = run_collection(_boards(), sources, LocalSink(tmp_path), client, now)

    status = {r.board: r.status for r in report.boards}
    assert status == {"ok": "ok", "quebrado": "error", "semfonte": "skipped"}
    assert report.postings_total == 2

    postings = gzip.decompress((tmp_path / report.postings_key).read_bytes()).decode().splitlines()
    assert [json.loads(p)["posting_id"] for p in postings] == [
        "greenhouse:ok:1001",
        "greenhouse:ok:1002",
    ]
    health = json.loads((tmp_path / "health/dt=2026-10-12/health.json").read_text(encoding="utf-8"))
    assert health["postings_total"] == 2
    assert (tmp_path / "raw/source=greenhouse/board=ok/dt=2026-10-12/payload.json.gz").exists()


def test_run_fails_when_no_board_succeeds(
    tmp_path: Path, greenhouse_payload: dict[str, Any], now: datetime
) -> None:
    boards = [Board(source=Source.GREENHOUSE, token="quebrado", company="Quebrado")]
    sources: dict[Source, SourceClient] = {Source.GREENHOUSE: FixtureSource(greenhouse_payload)}
    with httpx.Client() as client, pytest.raises(CollectionFailedError):
        run_collection(boards, sources, LocalSink(tmp_path), client, now)
    # mesmo falhando, o relatório de saúde fica gravado para investigação
    assert (tmp_path / "health/dt=2026-10-12/health.json").exists()
