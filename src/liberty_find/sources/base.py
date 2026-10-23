"""Interface comum das fontes. Cada ATS implementa duas etapas separadas:

1. `fetch_raw`: I/O. Busca a resposta da API como veio (vai para a camada bruta no S3).
2. `normalize`: função pura. Converte a resposta em `JobPosting`. É onde ficam os testes.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

import httpx

from liberty_find import __version__
from liberty_find.models import Board, JobPosting, Source

USER_AGENT = f"liberty-find/{__version__} (+https://github.com/FernandoCCristovao/liberty-find)"


class SourceClient(Protocol):
    source: Source

    def fetch_raw(self, board: Board, client: httpx.Client) -> Any:
        """Chama a API pública e devolve o JSON sem tratamento."""
        ...

    def normalize(self, board: Board, payload: Any, collected_at: datetime) -> list[JobPosting]:
        """Converte o JSON da fonte em vagas normalizadas. Sem I/O."""
        ...


def build_http_client(timeout_seconds: float = 20.0) -> httpx.Client:
    """Cliente HTTP padrão: timeout, redirecionamentos e User-Agent identificável.

    Sem transporte customizado de propósito: assim o httpx respeita proxy do ambiente
    (HTTPS_PROXY). Falha passageira de uma empresa fica no relatório de saúde e a coleta
    do dia seguinte cobre; o agendador ainda faz uma nova tentativa se a execução falhar.
    """
    return httpx.Client(
        timeout=timeout_seconds,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        follow_redirects=True,
    )
