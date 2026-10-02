"""Parameter mapping checks against EPİAŞ's technical documentation. Offline, no credentials.

The 2026-10-02 review of the electricity documentation found calls whose parameters did not
reach the endpoint: a parameter with no API label crashed ``EPTR2.call``, optional parameters
registered under a misspelled key were dropped, and filters the endpoint does not read were
silently ignored.
"""

import ast
import inspect
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from eptr2.mapping import parameters
from eptr2.mapping.parameters import (
    get_optional_parameters,
    get_param_label,
    get_required_parameters,
)
from eptr2.mapping.path import get_path_map

ALL_KEYS = get_path_map(just_call_keys=True)


def _dict_keys(fn) -> set[str]:
    """String keys of the dict literal a mapping function builds."""
    tree = ast.parse(inspect.getsource(fn))
    d = next(n for n in ast.walk(tree) if isinstance(n, ast.Dict))
    return {k.value for k in d.keys if isinstance(k, ast.Constant)}


def _offline_client():
    from eptr2 import EPTR2

    obj = EPTR2.__new__(EPTR2)
    obj.check_renew_tgt = lambda **kw: None
    obj.custom_aliases = {}
    obj.path_map_keys = ALL_KEYS
    obj.root_phrase = "https://example.invalid"
    obj.ssl_verify = True
    obj.is_test = False
    obj.tgt = "TGT-FAKE"
    obj.tgt_exp = 9999999999
    obj.recycle_tgt = False
    obj.postprocess = False
    obj.get_raw_response = False
    obj.strict_params = False
    return obj


def _sent_body(key, **kwargs) -> dict:
    fake = SimpleNamespace(data=b'{"items": []}', status=200)
    with patch("eptr2.main.transparency_call", return_value=fake) as sent:
        _offline_client().call(key, **kwargs)
    return sent.call_args.kwargs["call_body"]


@pytest.mark.parametrize("key", ALL_KEYS)
def test_every_parameter_has_an_api_label(key):
    # ra_spg_name had none, so EPTR2.call raised "string indices must be integers"
    for p in get_required_parameters(key) + get_optional_parameters(key):
        assert isinstance(get_param_label(p), dict), f"{key}: {p} has no label"


@pytest.mark.parametrize(
    "fn", [parameters.get_required_parameters, parameters.get_optional_parameters]
)
def test_parameter_tables_only_name_real_call_keys(fn):
    # "ra-meter-volume-period" (no s) left ra-meter-volumes-period without optionals
    assert _dict_keys(fn) - set(ALL_KEYS) == set()


def test_eligible_consumer_quantity_sends_dates():
    # the endpoint answers 400 without startDate/endDate
    body = _sent_body("eligible-consumer-quantity", start_date="2026-06-01", end_date="2026-07-01")
    assert {"startDate", "endDate"} <= set(body)


def test_interim_mcp_takes_start_date_only():
    # the endpoint reads startDate only; end_date silently returned a single day
    assert get_required_parameters("interim-mcp") == ["start_date"]


def test_eligible_consumer_count_has_no_ignored_filters():
    # st-adedi reads dates only; province/district/profile filters had no effect
    assert get_optional_parameters("eligible-consumer-count") == []


def test_ra_meters_profile_group_filter_reaches_the_api():
    body = _sent_body(
        "ra-meters", distribution_id=1004, start_date="2026-01-01",
        end_date="2026-06-01", ra_spg_name="AYDINLATMA",
    )
    assert body["subscriberProfileGroupName"] == "AYDINLATMA"


@pytest.mark.parametrize(
    "key, required",
    [
        ("ra-meter-volumes-period", dict(period_start_date="2025-01-01", period_end_date="2025-02-01")),
        ("ra-meter-volumes-version", dict(version_start_date="2025-01-01", version_end_date="2025-02-01")),
    ],
)
def test_ra_meter_volumes_profile_group_filter_reaches_the_api(key, required):
    # MeterVolumeRequestDto names the field subscriberProfileGroup (no "Name")
    body = _sent_body(key, mr_org_id=1005, subscriber_pg="AYDINLATMA", **required)
    assert body["subscriberProfileGroup"] == "AYDINLATMA"


def test_unset_optional_parameters_are_not_sent():
    # generated wrappers forward unset optionals as None; a None date crashed preprocessing
    body = _sent_body(
        "ra-meter-volumes-period", mr_org_id=1005, period_start_date="2025-01-01",
        period_end_date="2025-02-01", subscriber_pg=None, version_start_date=None, version_end_date=None,
    )
    assert not {"subscriberProfileGroup", "versionStartDate", "versionEndDate"} & set(body)
