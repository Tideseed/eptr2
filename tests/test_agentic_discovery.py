"""Offline tests for eptr2.agentic.discovery (no credentials needed)."""

import pytest

from eptr2.agentic import discovery
from eptr2.mapping.path import get_path_map


def test_list_calls_covers_all_path_map_keys():
    calls = discovery.list_calls()
    assert set(calls) == set(get_path_map(just_call_keys=True))
    assert len(calls) >= 231


def test_list_calls_category_filter():
    dgp = discovery.list_calls(category="DGP")
    assert dgp
    assert all(v["category"] == "DGP" for v in dgp.values())
    assert "smp" in dgp
    # case-insensitive
    assert discovery.list_calls(category="dgp").keys() == dgp.keys()


def test_list_categories_counts_sum_to_total():
    cats = discovery.list_categories()
    assert sum(cats.values()) == len(discovery.list_calls())
    assert "GÖP" in cats


def test_search_calls_finds_price_endpoints():
    matches = discovery.search_calls("market clearing price")
    assert "mcp" in matches
    # results are a subset of all calls
    assert set(matches) <= set(discovery.list_calls())


def test_search_calls_turkish():
    matches = discovery.search_calls("takas fiyat")
    assert "mcp" in matches


def test_search_with_category_filter():
    matches = discovery.search_calls("price", category="DGP")
    assert matches
    assert all(v["category"] == "DGP" for v in matches.values())


def test_describe_call_basic():
    d = discovery.describe_call("mcp")
    assert d["key"] == "mcp"
    assert d["required_body_params"] == ["start_date", "end_date"]
    assert d["call_method"] in ("GET", "POST")
    assert d["help"]["title"]["en"].startswith("Market Clearing Price")


def test_describe_call_resolves_alias():
    d = discovery.describe_call("ptf")
    assert d["key"] == "mcp"
    assert d["alias_of"] == {"alias": "ptf", "resolves_to": "mcp"}


def test_describe_call_unknown_returns_none():
    assert discovery.describe_call("definitely-not-a-call") is None


def test_describe_call_without_help_entry_still_works():
    # dpp-bulk exists in the path map but has no help dictionary entry
    d = discovery.describe_call("dpp-bulk")
    assert d is not None
    assert d["key"] == "dpp-bulk"
    assert d["help"] is not None


def test_format_calls_table():
    table = discovery.format_calls_table(discovery.list_calls(category="DGP"))
    assert "DGP" in table
    assert "smp" in table
    assert discovery.format_calls_table({}) == "No matching endpoints found."


def test_page_update_date_call_is_fully_wired():
    """New call: POST menu/get-page-update-date with menu_id -> menuId."""
    from eptr2.agentic import validate_call, EptrValidationError
    from eptr2.calls import get_page_update_date
    from eptr2.mapping.parameters import get_param_label

    d = discovery.describe_call("page-update-date")
    assert d is not None
    assert d["call_method"] == "POST"
    assert d["call_path"] == "electricity-service/v1/menu/get-page-update-date"
    assert d["required_body_params"] == ["menu_id"]
    assert get_param_label("menu_id")["label"] == "menuId"
    assert d["help"]["title"]["en"] == "Page Update Date"

    ## discoverable in both languages, and shipped as a typed wrapper
    assert "page-update-date" in discovery.search_calls("update date")
    assert "page-update-date" in discovery.search_calls("güncelleme")
    assert callable(get_page_update_date)

    ## agent-facing validation accepts a numeric id and rejects a missing one
    validate_call("page-update-date", {"menu_id": 123})
    with pytest.raises(EptrValidationError):
        validate_call("page-update-date", {})
