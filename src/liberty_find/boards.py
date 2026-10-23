"""Carga e validação da lista de empresas (src/liberty_find/boards.yaml)."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

import yaml

from liberty_find.models import Board


def load_boards(path: Path | None = None) -> list[Board]:
    """Lê boards.yaml (o empacotado com o código, se `path` for None) e valida cada linha."""
    if path is None:
        raw = resources.files("liberty_find").joinpath("boards.yaml").read_text(encoding="utf-8")
    else:
        raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    boards = [Board.model_validate(item) for item in data.get("boards", [])]
    _check_unique(boards)
    return boards


def _check_unique(boards: list[Board]) -> None:
    seen: set[tuple[str, str]] = set()
    for board in boards:
        key = (board.source.value, board.token)
        if key in seen:
            msg = f"board repetido em boards.yaml: {board.source.value}/{board.token}"
            raise ValueError(msg)
        seen.add(key)
