from pathlib import Path

import pytest

from liberty_find.boards import load_boards
from liberty_find.models import Source


def test_packaged_boards_file_is_valid() -> None:
    boards = load_boards()
    assert boards, "boards.yaml não pode estar vazio"
    assert {b.source for b in boards} <= set(Source)
    assert all(b.company for b in boards)


def test_duplicate_board_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "boards.yaml"
    path.write_text(
        "boards:\n"
        "  - { source: greenhouse, token: exemplo, company: A }\n"
        "  - { source: greenhouse, token: exemplo, company: B }\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="repetido"):
        load_boards(path)


def test_invalid_token_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "boards.yaml"
    path.write_text(
        "boards:\n  - { source: greenhouse, token: 'Com Espaço', company: A }\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="token"):
        load_boards(path)
