"""Tests for the generated ``get_*`` convenience wrappers in ``eptr2.calls``.

These tests do not hit the API. A mock ``eptr`` records the forwarded
arguments and asserts that every endpoint key in ``get_path_map`` has a
matching wrapper that forwards the key and parameters correctly.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

import eptr2.calls as calls_module
from eptr2.mapping import get_path_map
from eptr2.mapping.parameters import get_required_parameters, get_optional_parameters
from eptr2.mapping.path import get_alias_map


ALL_KEYS = get_path_map(just_call_keys=True)
ALIAS_MAP = get_alias_map()


def _fname(key: str) -> str:
    return "get_" + key.replace("-", "_")


@pytest.mark.parametrize("key", ALL_KEYS)
def test_wrapper_exists(key):
    """Every endpoint key has a matching ``get_<key>`` in ``eptr2.calls``."""
    assert hasattr(calls_module, _fname(key)), (
        f"Missing wrapper for endpoint key {key!r}"
    )
    fn = getattr(calls_module, _fname(key))
    assert callable(fn)
    assert _fname(key) in calls_module.__all__


@pytest.mark.parametrize("alias_key", list(ALIAS_MAP.keys()))
def test_alias_wrapper_exists(alias_key):
    """Each alias key also gets a wrapper."""
    assert hasattr(calls_module, _fname(alias_key))


@pytest.mark.parametrize("key", ALL_KEYS)
def test_wrapper_forwards_key_and_params(key):
    """Calling ``get_<key>(eptr, **required)`` forwards correctly to ``eptr.call``."""
    fn = getattr(calls_module, _fname(key))
    required = list(get_required_parameters(key) or [])
    optional = [p for p in (get_optional_parameters(key) or []) if p not in required]

    eptr = MagicMock()
    eptr.call.return_value = "sentinel"

    # Use parameter name as the sample value so we can verify forwarding.
    required_kwargs = {p: f"<{p}>" for p in required}
    extra_kwargs = {"postprocess": False}

    result = fn(eptr=eptr, **required_kwargs, **extra_kwargs)

    assert result == "sentinel"
    eptr.call.assert_called_once()
    args, kwargs = eptr.call.call_args
    assert args == (key,)
    for p, v in required_kwargs.items():
        assert kwargs[p] == v
    for p in optional:
        assert kwargs[p] is None
    assert kwargs["postprocess"] is False


@pytest.mark.parametrize("key", [k for k in ALL_KEYS if get_required_parameters(k)])
def test_required_params_enforced(key):
    """Wrappers raise ``TypeError`` when a required keyword is omitted."""
    fn = getattr(calls_module, _fname(key))
    eptr = MagicMock()
    with pytest.raises(TypeError):
        fn(eptr=eptr)


def test_alias_uses_alias_key(monkeypatch):
    """Alias wrapper forwards the alias key (not the canonical one)."""
    from eptr2.calls import get_ptf

    eptr = MagicMock()
    get_ptf(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
    args, _ = eptr.call.call_args
    assert args == ("ptf",)


def test_all_export_count():
    """Sanity check: package exports cover every endpoint plus aliases."""
    expected = {_fname(k) for k in ALL_KEYS} | {_fname(a) for a in ALIAS_MAP}
    assert set(calls_module.__all__) == expected
