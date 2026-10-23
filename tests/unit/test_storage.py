import gzip
import json
from datetime import date
from pathlib import Path

import boto3
from moto import mock_aws

from liberty_find.storage import LocalSink, S3Sink, health_key, postings_key, raw_key

DAY = date(2026, 10, 12)


def test_keys_follow_the_documented_layout() -> None:
    assert raw_key("greenhouse", "exemplo", DAY) == (
        "raw/source=greenhouse/board=exemplo/dt=2026-10-12/payload.json.gz"
    )
    assert postings_key(DAY) == "postings/dt=2026-10-12/postings.jsonl.gz"
    assert health_key(DAY) == "health/dt=2026-10-12/health.json"


def test_local_sink_writes_gzipped_json_lines(tmp_path: Path) -> None:
    path = LocalSink(tmp_path).write_jsonl_gz("postings/x.jsonl.gz", [{"a": 1}, {"a": "ção"}])
    lines = gzip.decompress(Path(path).read_bytes()).decode("utf-8").splitlines()
    assert [json.loads(line) for line in lines] == [{"a": 1}, {"a": "ção"}]


@mock_aws
def test_s3_sink_writes_object_with_encoding() -> None:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="liberty-find-teste")

    uri = S3Sink("liberty-find-teste", s3).write_jsonl_gz(postings_key(DAY), [{"a": 1}])

    assert uri == "s3://liberty-find-teste/postings/dt=2026-10-12/postings.jsonl.gz"
    obj = s3.get_object(Bucket="liberty-find-teste", Key=postings_key(DAY))
    assert obj["ContentEncoding"] == "gzip"
    assert json.loads(gzip.decompress(obj["Body"].read())) == {"a": 1}
