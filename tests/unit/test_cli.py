import pytest

from liberty_find.cli import main


def test_boards_command_lists_companies(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["boards"]) == 0
    out = capsys.readouterr().out
    assert "greenhouse" in out
    assert "a implementar" in out


def test_probe_refuses_unimplemented_source(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["probe", "lever", "ciandt"]) == 2
    assert "ainda não foi implementada" in capsys.readouterr().err


def test_collect_requires_local_flag(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["collect"]) == 2
