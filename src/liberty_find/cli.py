"""Linha de comando para desenvolvimento local (sem AWS).

uv run liberty boards                          # empresas e estado de cada fonte
uv run liberty probe greenhouse quintoandar    # testa uma empresa na API real
uv run liberty collect --local                 # coleta tudo e grava em ./data
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

from liberty_find.boards import load_boards
from liberty_find.collect import run_collection
from liberty_find.models import Board, Source
from liberty_find.sources import REGISTRY, build_http_client
from liberty_find.storage import LocalSink


def _cmd_boards(_: argparse.Namespace) -> int:
    for board in load_boards():
        status = "implementada" if board.source in REGISTRY else "a implementar"
        flag = "" if board.enabled else " (desligada)"
        print(
            f"{board.source.value:<11} {board.token:<18} {board.company:<20} fonte {status}{flag}"
        )
    return 0


def _cmd_probe(args: argparse.Namespace) -> int:
    source = REGISTRY.get(Source(args.source))
    if source is None:
        print(f"a fonte {args.source} ainda não foi implementada", file=sys.stderr)
        return 2
    board = Board(source=Source(args.source), token=args.token, company=args.token)
    with build_http_client() as client:
        postings = source.normalize(board, source.fetch_raw(board, client), datetime.now(UTC))
    print(f"{len(postings)} vagas em {args.source}/{args.token}")
    for posting in postings[: args.limit]:
        print(f"- {posting.title} | {posting.location or 'sem local'}")
    return 0


def _cmd_collect(args: argparse.Namespace) -> int:
    if not args.local:
        print("use --local; em produção a coleta roda na Lambda", file=sys.stderr)
        return 2
    sink = LocalSink(Path(args.out))
    with build_http_client() as client:
        report = run_collection(load_boards(), REGISTRY, sink, client, datetime.now(UTC))
    for result in report.boards:
        print(f"{result.status:<8} {result.source.value}/{result.board} {result.postings} vagas")
    print(f"total: {report.postings_total} vagas em {Path(args.out) / report.postings_key}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="liberty", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("boards", help="lista as empresas").set_defaults(func=_cmd_boards)

    probe = sub.add_parser("probe", help="testa uma empresa na API real")
    probe.add_argument("source", choices=[s.value for s in Source])
    probe.add_argument("token")
    probe.add_argument("--limit", type=int, default=5)
    probe.set_defaults(func=_cmd_probe)

    collect = sub.add_parser("collect", help="roda a coleta")
    collect.add_argument("--local", action="store_true", help="grava em disco, não no S3")
    collect.add_argument("--out", default="data")
    collect.set_defaults(func=_cmd_collect)

    args = parser.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
