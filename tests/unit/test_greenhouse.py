from datetime import datetime
from typing import Any

import httpx
import respx

from liberty_find.models import Board, Source
from liberty_find.sources.greenhouse import GreenhouseSource


def test_normalize_maps_fields(
    greenhouse_board: Board, greenhouse_payload: dict[str, Any], now: datetime
) -> None:
    postings = GreenhouseSource().normalize(greenhouse_board, greenhouse_payload, now)

    assert len(postings) == 2
    first = postings[0]
    assert first.posting_id == "greenhouse:exemplo:1001"
    assert first.source is Source.GREENHOUSE
    assert first.company == "Empresa Exemplo"
    assert first.title == "Pessoa Engenheira de Dados Pleno"
    assert first.url == "https://job-boards.greenhouse.io/exemplo/jobs/1001"
    assert first.location == "Remoto, Brasil"
    assert first.department == "Dados"
    assert first.language == "pt"
    assert first.published_at is not None
    assert first.published_at.isoformat() == "2026-10-01T10:00:00-03:00"
    assert first.collected_at == now
    assert "Vaga fictícia para testes. Trabalho 100% remoto." in first.description_text
    assert "- Python e SQL" in first.description_text
    assert "&" not in first.description_text


def test_normalize_tolerates_missing_optional_fields(
    greenhouse_board: Board, greenhouse_payload: dict[str, Any], now: datetime
) -> None:
    second = GreenhouseSource().normalize(greenhouse_board, greenhouse_payload, now)[1]
    assert second.department is None
    assert second.published_at is None
    assert second.description_text == "Sobre a vaga\nConstruir agentes com LLM."


def test_normalize_empty_payload(greenhouse_board: Board, now: datetime) -> None:
    assert GreenhouseSource().normalize(greenhouse_board, {"jobs": []}, now) == []
    assert GreenhouseSource().normalize(greenhouse_board, [], now) == []


@respx.mock
def test_fetch_raw_calls_public_endpoint_with_content(
    greenhouse_board: Board, greenhouse_payload: dict[str, Any]
) -> None:
    route = respx.get("https://boards-api.greenhouse.io/v1/boards/exemplo/jobs").mock(
        return_value=httpx.Response(200, json=greenhouse_payload)
    )
    with httpx.Client() as client:
        payload = GreenhouseSource().fetch_raw(greenhouse_board, client)

    assert route.called
    assert route.calls.last.request.url.params["content"] == "true"
    assert payload == greenhouse_payload
