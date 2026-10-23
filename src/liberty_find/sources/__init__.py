"""Registro das fontes. Só entram aqui as fontes já implementadas e testadas."""

from __future__ import annotations

from liberty_find.models import Source
from liberty_find.sources.base import SourceClient, build_http_client
from liberty_find.sources.greenhouse import GreenhouseSource

REGISTRY: dict[Source, SourceClient] = {
    Source.GREENHOUSE: GreenhouseSource(),
    # Marco 1, tarefa 1.3: registrar LeverSource, AshbySource e WorkableSource
    # quando estiverem prontas e testadas.
}

__all__ = ["REGISTRY", "SourceClient", "build_http_client"]
