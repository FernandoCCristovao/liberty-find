"""Fixtures compartilhadas. Regra: teste unitário nunca acessa a rede (pytest --disable-socket)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from liberty_find.models import Board, Source

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 10, 12, 9, 0, tzinfo=UTC)


@pytest.fixture
def greenhouse_board() -> Board:
    return Board(source=Source.GREENHOUSE, token="exemplo", company="Empresa Exemplo")


@pytest.fixture
def greenhouse_payload() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(
        (FIXTURES / "greenhouse_jobs.json").read_text(encoding="utf-8")
    )
    return data
