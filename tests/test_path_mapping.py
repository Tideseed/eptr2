"""Regression tests for call-key to endpoint path mapping. Offline, no credentials."""

import pytest

from eptr2.mapping.path import get_call_method, get_total_path

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
