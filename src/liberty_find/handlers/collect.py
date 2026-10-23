"""Lambda de coleta diária, acionada pelo EventBridge Scheduler (ver template.yaml)."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from liberty_find.boards import load_boards
from liberty_find.collect import run_collection
from liberty_find.sources import REGISTRY, build_http_client
from liberty_find.storage import S3Sink

logger = Logger()


@logger.inject_lambda_context
def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    bucket = os.environ["BUCKET_NAME"]
    with build_http_client() as client:
        report = run_collection(
            boards=load_boards(),
            sources=REGISTRY,
            sink=S3Sink(bucket),
            client=client,
            now=datetime.now(UTC),
        )
    summary = {
        "postings_total": report.postings_total,
        "boards_ok": report.ok_count,
        "boards": len(report.boards),
        "postings_key": report.postings_key,
    }
    logger.info("coleta concluída", extra=summary)
    return summary
