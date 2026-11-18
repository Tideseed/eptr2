"""Warnings for data leaving the mandatory Transparency Platform list on 2027-01-01 (EPDK 14968 / 14967)."""

import json
import warnings
from types import SimpleNamespace

import pytest

import eptr2.mapping.publication as publication
from eptr2 import TransparencyListWarning
from eptr2.mapping import get_path_map
from eptr2.mapping.parameters import get_optional_parameters, get_required_parameters
from eptr2.mapping.publication import (
    PUBLICATION_CHANGES,
    get_publication_change,
    publication_notice,
)


@pytest.fixture(autouse=True)
def _reset_warned(monkeypatch):
    monkeypatch.setattr(publication, "_warned", set())


def _client(monkeypatch, items):
    import eptr2.main as main
    from eptr2 import EPTR2

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
    eptr.postprocess = False
    eptr.get_raw_response = False
    eptr.strict_params = True
    response = SimpleNamespace(data=json.dumps({"items": items}).encode(), status=200)
    monkeypatch.setattr(main, "transparency_call", lambda *a, **kw: response)
    return eptr


def test_registry_keys_and_params_exist():
    keys = set(get_path_map(just_call_keys=True))
    for key, entry in PUBLICATION_CHANGES.items():
        assert key in keys, key
        assert entry["kind"] in {"participant", "dbp", "not_listed", "aggregated"}
        params = get_required_parameters(key) + get_optional_parameters(key)
        for p in entry["when_params"] or []:
            assert p in params, (key, p)


def test_notice_depends_on_parameters():
    assert publication_notice("idm-qty", {"org_id": None}) is None
    assert publication_notice("idm-qty", {}) is None
    assert "Art. 6/4" in publication_notice("idm-qty", {"org_id": 123})
    assert publication_notice("mcp", {}) is None
    ## Without params the general notice is returned (docs, describe_call).
    assert "with org_id" in publication_notice("idm-qty")
    assert "Dâhilî Bilgi Platformu" in publication_notice("mms", {})


def test_call_warns_once_per_key(monkeypatch):
    eptr = _client(monkeypatch, [])
    with pytest.warns(TransparencyListWarning, match="dam-clearing' with org_id"):
        eptr.call("dam-clearing", start_date="2026-11-01", end_date="2026-11-01", org_id=1)
    with warnings.catch_warnings():
        warnings.simplefilter("error", TransparencyListWarning)
        eptr.call("dam-clearing", start_date="2026-11-02", end_date="2026-11-02", org_id=1)


def test_market_total_does_not_warn(monkeypatch):
    eptr = _client(monkeypatch, [])
    with warnings.catch_warnings():
        warnings.simplefilter("error", TransparencyListWarning)
        eptr.call("dam-clearing", start_date="2026-11-01", end_date="2026-11-01")
        eptr.call("idm-qty", start_date="2026-11-01", end_date="2026-11-01")
        eptr.call("mcp", start_date="2026-11-01", end_date="2026-11-01")


def test_warning_is_shown_by_default():
    assert issubclass(TransparencyListWarning, FutureWarning)


def test_describe_call_and_schema_carry_the_change():
    from eptr2.agentic.discovery import describe_call
    from eptr2.agentic.schema import load_bundled_schema

    d = describe_call("planned-outages")
    assert d["publication_change"]["effective_date"] == "2027-01-01"
    assert "14968" in d["publication_change"]["source"]
    assert "publication_change" not in describe_call("mcp")
    schema = load_bundled_schema()
    schema = json.loads(schema) if isinstance(schema, str) else schema
    assert schema["endpoints"]["mms"]["publication_change"] == get_publication_change("mms")
