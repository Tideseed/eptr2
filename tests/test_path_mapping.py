"""Regression tests for call-key to endpoint path mapping. Offline, no credentials."""

import pytest

from eptr2.mapping.path import get_call_method, get_path_map, get_total_path
from eptr2.mapping.processing import get_postprocess_function

TRANSMISSION = "electricity-service/v1/transmission/data/"


@pytest.mark.parametrize(
    "key, label, method",
    [
        ("line-capacities", "line-capacities", "POST"),
        ("capacity-demand", "capacity-demand", "POST"),
        ("intl-direction-list", "line-capacities-direction", "GET"),
        ("intl-capacity-demand-direction-list", "capacity-demand-direction", "GET"),
    ],
)
def test_interconnection_capacity_paths(key, label, method):
    # Tideseed/eptr2#6: the capacity-request keys called the line-capacities endpoints
    assert get_total_path(key) == TRANSMISSION + label
    assert get_call_method(key) == method


@pytest.mark.parametrize("key", get_path_map(just_call_keys=True))
def test_every_call_key_has_a_postprocess(key):
    # page-update-date had none, so EPTR2.call raised under the default postprocess=True
    assert callable(get_postprocess_function(key))
