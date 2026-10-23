"""Onde e como os dados são gravados. Layout completo em docs/dados/contratos.md.

Duas implementações com a mesma interface:
- `S3Sink`: produção (bucket da stack).
- `LocalSink`: desenvolvimento (`liberty collect --local` grava em ./data, ignorado pelo Git).

Toda chave é determinística por dia: rodar de novo no mesmo dia sobrescreve (idempotente).
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterable, Mapping
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


def raw_key(source: str, board: str, day: date) -> str:
    return f"raw/source={source}/board={board}/dt={day.isoformat()}/payload.json.gz"


def postings_key(day: date) -> str:
    return f"postings/dt={day.isoformat()}/postings.jsonl.gz"


def health_key(day: date) -> str:
    return f"health/dt={day.isoformat()}/health.json"


def _jsonl_gz(records: Iterable[Mapping[str, Any]]) -> bytes:
    lines = "".join(
        json.dumps(record, ensure_ascii=False, default=str) + "\n" for record in records
    )
    return gzip.compress(lines.encode("utf-8"))


def _json_gz(obj: Any) -> bytes:
    return gzip.compress(json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8"))


def _json(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str).encode("utf-8")


class Sink(Protocol):
    def write_jsonl_gz(self, key: str, records: Iterable[Mapping[str, Any]]) -> str: ...

    def write_json_gz(self, key: str, obj: Any) -> str: ...

    def write_json(self, key: str, obj: Any) -> str: ...


class S3Sink:
    def __init__(self, bucket: str, client: S3Client | None = None) -> None:
        if client is None:
            import boto3  # já vem no runtime da Lambda

            client = boto3.client("s3")
        self.bucket = bucket
        self.client = client

    def _put(self, key: str, body: bytes, content_type: str, *, gzipped: bool) -> str:
        if gzipped:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType=content_type,
                ContentEncoding="gzip",
            )
        else:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType=content_type)
        return f"s3://{self.bucket}/{key}"

    def write_jsonl_gz(self, key: str, records: Iterable[Mapping[str, Any]]) -> str:
        return self._put(key, _jsonl_gz(records), "application/x-ndjson", gzipped=True)

    def write_json_gz(self, key: str, obj: Any) -> str:
        return self._put(key, _json_gz(obj), "application/json", gzipped=True)

    def write_json(self, key: str, obj: Any) -> str:
        return self._put(key, _json(obj), "application/json", gzipped=False)


class LocalSink:
    def __init__(self, root: Path) -> None:
        self.root = root

    def _write(self, key: str, body: bytes) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        return str(path)

    def write_jsonl_gz(self, key: str, records: Iterable[Mapping[str, Any]]) -> str:
        return self._write(key, _jsonl_gz(records))

    def write_json_gz(self, key: str, obj: Any) -> str:
        return self._write(key, _json_gz(obj))

    def write_json(self, key: str, obj: Any) -> str:
        return self._write(key, _json(obj))
