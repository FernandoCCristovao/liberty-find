"""Funções puras de texto: HTML para texto, hash de conteúdo e IDs."""

from __future__ import annotations

import hashlib
import html
import re
from html.parser import HTMLParser

_BLOCK_TAGS = frozenset(
    {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "section"}
)


class _TextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag: str) -> None:
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_to_text(raw: str, *, escaped: bool = False) -> str:
    """Converte HTML em texto puro, com uma linha por bloco.

    `escaped=True` para fontes que mandam o HTML como entidades (o Greenhouse manda
    `&lt;p&gt;`, às vezes escapado duas vezes).
    """
    source = html.unescape(raw) if escaped else raw
    collector = _TextCollector()
    collector.feed(source)
    collector.close()
    text = "".join(collector.parts).replace("\xa0", " ")
    lines = (re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def content_hash(title: str, description_text: str) -> str:
    """SHA-256 de título + descrição: muda quando a vaga muda e dispara nova extração."""
    payload = f"{title.strip()}\n{description_text.strip()}".encode()
    return hashlib.sha256(payload).hexdigest()


def posting_id(source: str, board: str, source_job_id: str) -> str:
    """ID estável de uma vaga: `<source>:<board>:<source_job_id>`."""
    return f"{source}:{board}:{source_job_id}"
