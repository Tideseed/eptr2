"""meter-count and multiple-factor-bulk: paths, methods and request bodies (no credentials needed)."""
import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from eptr2 import EPTR2
from eptr2.mapping import get_path_map
from eptr2.mapping.path import get_call_method, get_total_path


def _client():
    eptr = EPTR2.__new__(EPTR2)
    eptr.check_renew_tgt = lambda **kw: None
    eptr.custom_aliases = {}
    eptr.path_map_keys = get_path_map(just_call_keys=True)
    eptr.root_phrase = "https://example.invalid"
    eptr.ssl_verify = True
    eptr.is_test = False
    eptr.tgt = "TGT-FAKE"
    eptr.tgt_exp = 9999999999
    eptr.recycle_tgt = False
    eptr.postprocess = True
    eptr.get_raw_response = False
    eptr.strict_params = True
    return eptr


@pytest.mark.parametrize(
    "key, path",
    [
        ("meter-count", "electricity-service/v1/consumption/data/meter-count"),
        ("multiple-factor-bulk", "electricity-service/v1/consumption/data/multiple-factor-bulk"),
    ],
)
def test_paths_and_methods(key, path):
    assert get_total_path(key) == path
    assert get_call_method(key) == "POST"


def test_meter_count_sends_empty_body():
    items = [{"date": "2026-12-01T00:00:00+03:00", "meterQuantity": 1}]
    response = SimpleNamespace(data=json.dumps({"items": items}).encode(), status=200)
    with patch("eptr2.main.transparency_call", return_value=response) as sent:
        df = _client().call("meter-count")
    assert sent.call_args.kwargs["call_body"] == {}
    assert list(df.columns) == ["date", "meterQuantity"]


def test_multiple_factor_bulk_body():
    response = SimpleNamespace(data=b'{"items": []}', status=200)
    with patch("eptr2.main.transparency_call", return_value=response) as sent:
        _client().call("multiple-factor-bulk", period="2026-10-01", distribution_id=1005)
    assert sent.call_args.kwargs["call_body"] == {
        "period": "2026-10-01T00:00:00+03:00",
        "distributionId": 1005,
    }


def test_wrappers_exist():
    from eptr2.calls import get_meter_count, get_multiple_factor_bulk  # noqa: F401
