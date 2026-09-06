"""Regression tests for agent-facing contract and correctness fixes.

These cover defects found by the agent-first evaluation (helpdocs/astra_evaluation):
F01 bulk plan/realization semantics, F02 portfolio tolerance across regulation
boundaries, F04 stdout purity, F07 credential-free MCP discovery, and F12 system
direction handling. All run offline with no credentials.
"""

import logging
import subprocess
import sys
import tempfile
import warnings
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd
import pytest

from eptr2.util.costs import (
    calculate_kupsm,
    calculate_unit_price_and_costs_by_contract,
    get_kupst_tolerance_by_contract,
    normalize_system_direction,
)

mcp_server = pytest.importorskip("eptr2.mcp.server")
pytestmark = pytest.mark.skipif(
    not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed"
)


# --- F12: system direction -------------------------------------------------


class TestSystemDirection:
    """Direction must be honoured under its documented name, not silently
    swallowed by **kwargs (which produced balanced-system prices)."""

    def test_normalize_accepts_ints_labels_and_none(self):
        assert normalize_system_direction(None) is None
        assert normalize_system_direction(-1) == -1
        assert normalize_system_direction("Enerji Açığı") == -1
        assert normalize_system_direction("Enerji Fazlası") == 1
        assert normalize_system_direction("dengede") == 0
        with pytest.raises(ValueError):
            normalize_system_direction("not a direction")

    @pytest.mark.parametrize(
        "kwargs",
        [{"sd_sign": -1}, {"system_direction": -1}, {"system_direction": "Enerji Açığı"}],
    )
    def test_deficit_hour_matches_api(self, kwargs):
        """Live-observed 2026-07-01 01:00: MCP==SMP==4000, systemStatus deficit.
        The API reported a negative imbalance price of 4240 TL/MWh."""
        result = calculate_unit_price_and_costs_by_contract(
            contract="PH26070101", mcp=4000, smp=4000, **kwargs
        )
        assert result["neg_imb_price"] == pytest.approx(4240.0, abs=0.01)

    def test_equal_prices_without_direction_still_infers_balanced(self):
        """Unchanged library behaviour: ambiguous input infers a balanced system."""
        result = calculate_unit_price_and_costs_by_contract(
            contract="PH26070101", mcp=4000, smp=4000
        )
        assert result["neg_imb_price"] == pytest.approx(4120.0, abs=0.01)

    def test_mcp_tool_requires_direction_when_prices_equal(self):
        import json

        out = json.loads(
            mcp_server.calculate_imbalance_prices_and_costs(
                contract="PH26070101", mcp_price=4000, smp_price=4000
            )
        )
        assert "system_direction is required" in out["error"]

        ok = json.loads(
            mcp_server.calculate_imbalance_prices_and_costs(
                contract="PH26070101",
                mcp_price=4000,
                smp_price=4000,
                system_direction="Enerji Açığı",
            )
        )
        assert ok["neg_imb_price"] == pytest.approx(4240.0, abs=0.01)

    def test_mcp_tool_infers_when_prices_differ(self):
        import json

        out = json.loads(
            mcp_server.calculate_imbalance_prices_and_costs(
                contract="PH26070101", mcp_price=4000, smp_price=4200
            )
        )
        assert "error" not in out


# --- F01: plans vs realizations --------------------------------------------


class _RecordingClient:
    """Fake client recording the endpoint key and id namespace actually used."""

    def __init__(self):
        self.calls = []

    def call(self, call_key, **params):
        self.calls.append((call_key, params))
        ## Include both column spellings so either bulk path can post-process.
        return pd.DataFrame(
            {
                "date": ["2026-01-01T00:00:00+03:00"],
                "hour": ["00:00"],
                "time": ["00:00"],
                "toplam": [1.0],
            }
        )


class TestBulkPlanVersusRealization:
    """The production-plan tool must not return realized generation."""

    def test_production_plans_tool_calls_plan_endpoint_with_uevcb_ids(self, monkeypatch):
        fake = _RecordingClient()
        monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

        mcp_server.get_bulk_production_plans("2026-01-01", "2026-01-01", [3204384])

        key, params = fake.calls[-1]
        assert key == "dpp-bulk", "production plans must use the plan endpoint"
        assert params["uevcb_ids"] == [3204384]
        assert "pp_ids" not in params

    def test_actual_generation_tool_calls_realtime_endpoint_with_pp_ids(
        self, monkeypatch
    ):
        fake = _RecordingClient()
        monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

        mcp_server.get_bulk_actual_generation("2026-01-01", "2026-01-01", [641])

        key, params = fake.calls[-1]
        assert key == "rt-gen-bulk", "actual generation must use the realtime endpoint"
        assert params["pp_ids"] == [641]
        assert "uevcb_ids" not in params

    def test_two_tools_use_different_endpoints(self, monkeypatch):
        fake = _RecordingClient()
        monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)
        mcp_server.get_bulk_production_plans("2026-01-01", "2026-01-01", [1])
        mcp_server.get_bulk_actual_generation("2026-01-01", "2026-01-01", [1])
        assert {k for k, _ in fake.calls} == {"dpp-bulk", "rt-gen-bulk"}

    def test_correctly_named_alias_matches_legacy_helper(self):
        from eptr2.composite import get_dpp_bulk_range, get_rt_gen_bulk_range

        assert callable(get_rt_gen_bulk_range)
        assert callable(get_dpp_bulk_range)


# --- F02: tolerance across regulation boundaries ---------------------------


def test_portfolio_tolerance_resolved_per_contract():
    """A range crossing the 2026 boundary must use each contract's tolerance."""
    import eptr2.composite.plant_costs as pc

    contracts = ["PH25123123", "PH26010100"]
    data = pd.DataFrame(
        {
            "contract": contracts,
            "total_rt": [80.0, 80.0],
            "toplam_kgup_v1": [100.0, 100.0],
            "toplam_kgup": [100.0, 100.0],
        }
    )
    ids = pd.DataFrame(
        [dict(plant_name="FAKE", uevcb_id=1, rt_id=1, source="wind")]
    )
    cost_cols = [
        "sd_sign",
        "unit_pos_imb_cost",
        "unit_neg_imb_cost",
        "unit_kupst_cost",
        "mcp",
        "smp",
        "pos_imb_price",
        "neg_imb_price",
    ]
    costs = pd.DataFrame(
        {"contract": contracts, **{k: [1.0, 1.0] for k in cost_cols}}
    )

    with tempfile.TemporaryDirectory() as directory, patch.object(
        pc, "wrapper_hourly_production_plan_and_realized", return_value=data
    ):
        output = pc.calculate_portfolio_costs(
            "2025-12-31", "2026-01-01", ids, cost_df=costs,
            verbose=False, export_dir=directory,
        )

    expected = [
        calculate_kupsm(
            actual=80, forecast=100, tol=get_kupst_tolerance_by_contract(c, "wind")
        )
        for c in contracts
    ]
    assert output["costs_detail"]["kupsm"].tolist() == expected
    assert expected == [3.0, 5.0], "fixture guards the pre-2026/2026 tolerance change"


# --- F04: stdout purity ----------------------------------------------------


def test_library_logging_does_not_target_stdout():
    logger = logging.getLogger("eptr2")
    assert logger.handlers, "eptr2 configures a default handler"
    assert not any(
        getattr(h, "stream", None) is sys.stdout for h in logger.handlers
    ), "diagnostics on stdout corrupt CLI data and MCP stdio frames"


def test_cli_keeps_stdout_clean_on_credential_failure(tmp_path):
    """Without credentials the CLI must fail with empty stdout, not warnings."""
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(tmp_path),
        "PYTHONPATH": str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src"),
    }
    proc = subprocess.run(
        [sys.executable, "-m", "eptr2", "call", "mcp",
         "--start-date", "2026-01-01", "--end-date", "2026-01-01"],
        capture_output=True, text=True, cwd=str(tmp_path), env=env,
    )
    assert proc.returncode != 0
    assert proc.stdout == "", f"stdout must stay clean, got: {proc.stdout!r}"
    assert proc.stderr.strip(), "diagnostics belong on stderr"


# --- F07: discovery without credentials ------------------------------------


def test_mcp_server_starts_and_discovers_without_credentials(monkeypatch, tmp_path):
    """create_mcp_server must not construct an authenticated client."""
    import json

    monkeypatch.delenv("EPTR_USERNAME", raising=False)
    monkeypatch.delenv("EPTR_PASSWORD", raising=False)
    monkeypatch.setattr(mcp_server, "_eptr_client", None)
    monkeypatch.chdir(tmp_path)  # no .env here

    mcp_server.create_mcp_server()
    assert mcp_server._eptr_client is None, "client must stay lazy until a data call"

    keys = json.loads(mcp_server.get_available_eptr2_calls())["keys"]
    assert len(keys) >= 231
    assert json.loads(mcp_server.describe_eptr2_call("ptf"))["key"] == "mcp"


def test_data_tool_still_requires_credentials(monkeypatch, tmp_path):
    monkeypatch.delenv("EPTR_USERNAME", raising=False)
    monkeypatch.delenv("EPTR_PASSWORD", raising=False)
    monkeypatch.setattr(mcp_server, "_eptr_client", None)
    monkeypatch.chdir(tmp_path)
    with pytest.raises(Exception):
        mcp_server.get_market_clearing_price("2026-01-01", "2026-01-01")


# --- F03: unknown parameters must not be dropped in silence ----------------


def _offline_client():
    """Minimal EPTR2 instance that never touches the network or credentials."""
    from eptr2 import EPTR2
    from eptr2.mapping import get_path_map

    obj = EPTR2.__new__(EPTR2)
    obj.check_renew_tgt = lambda **kw: None
    obj.custom_aliases = {}
    obj.path_map_keys = get_path_map(just_call_keys=True)
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


def test_unknown_parameter_warns_and_names_the_right_one():
    """A misspelled filter silently became an unfiltered request."""
    from types import SimpleNamespace

    fake_response = SimpleNamespace(data=b'{"items": []}', status=200)
    with patch("eptr2.main.transparency_call", return_value=fake_response) as sent:
        with pytest.warns(UserWarning, match="does not accept") as record:
            _offline_client().call(
                "rt-gen", start_date="2025-01-01", end_date="2025-01-01", ppID=641
            )

    message = str(record[0].message)
    assert "ppID" in message
    assert "pp_id" in message, "the message should point at the accepted spelling"
    ## Behaviour is unchanged: the request still goes out without the bad key.
    assert "ppID" not in sent.call_args.kwargs["call_body"]


def test_reserved_options_do_not_warn():
    """Transport/behaviour options are not endpoint parameters and are fine."""
    from types import SimpleNamespace

    fake_response = SimpleNamespace(data=b'{"items": []}', status=200)
    with patch("eptr2.main.transparency_call", return_value=fake_response):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            _offline_client().call(
                "rt-gen",
                start_date="2025-01-01",
                end_date="2025-01-01",
                request_kwargs={"timeout": 5},
                map_param_labels=True,
            )
    assert [w for w in caught if "does not accept" in str(w.message)] == []


# --- F03 strict mode / F05 timeouts / F06 ticket scoping / F09 / F10 --------


def test_strict_params_raises_and_suggests(monkeypatch):
    from types import SimpleNamespace

    fake_response = SimpleNamespace(data=b'{"items": []}', status=200)
    client = _offline_client()
    client.strict_params = False

    with patch("eptr2.main.transparency_call", return_value=fake_response):
        ## per-call opt-in
        with pytest.raises(ValueError, match="does not accept"):
            client.call(
                "rt-gen", start_date="2025-01-01", end_date="2025-01-01",
                ppID=641, strict_params=True,
            )
        ## client-level opt-in
        client.strict_params = True
        with pytest.raises(ValueError) as exc:
            client.call(
                "rt-gen", start_date="2025-01-01", end_date="2025-01-01", ppID=641
            )
    assert "pp_id" in str(exc.value), "should suggest the correct spelling"


def test_default_timeout_is_bounded_and_overridable():
    import urllib3

    client = _offline_client()
    client.strict_params = False
    client.connect_timeout = 10.0
    client.read_timeout = 60.0

    with patch("urllib3.PoolManager.request") as request:
        request.return_value = SimpleNamespace(data=b'{"items": []}', status=200)
        client.call("rt-gen", start_date="2025-01-01", end_date="2025-01-01")
        timeout = request.call_args.kwargs["timeout"]
        assert isinstance(timeout, urllib3.Timeout)
        assert timeout.connect_timeout == 10.0
        assert timeout.read_timeout == 60.0

        ## an explicit timeout always wins
        client.call(
            "rt-gen", start_date="2025-01-01", end_date="2025-01-01",
            request_kwargs={"timeout": 3},
        )
        assert request.call_args.kwargs["timeout"] == 3


class TestTicketCacheScoping:
    """Cached tickets are per account/profile and only touched when recycling."""

    @staticmethod
    def _client(tmp_path, user, **kwargs):
        from eptr2 import EPTR2

        with patch.object(EPTR2, "check_renew_tgt", lambda self, **kw: None):
            return EPTR2(
                username=user, password="pw", use_dotenv=False,
                tgt_path=str(tmp_path), **kwargs,
            )

    def _seed(self, tmp_path, user="alice@example.com", **kwargs):
        client = self._client(tmp_path, user, recycle_tgt=True, **kwargs)
        client.tgt = "TGT-ALICE"
        client.tgt_exp = 9e9
        client.tgt_exp_0 = 9e9
        client.export_tgt_info()
        return client

    def test_same_account_reuses_ticket(self, tmp_path):
        self._seed(tmp_path)
        assert self._client(tmp_path, "alice@example.com", recycle_tgt=True).tgt == "TGT-ALICE"

    def test_other_account_does_not_reuse_ticket(self, tmp_path):
        self._seed(tmp_path)
        assert self._client(tmp_path, "bob@example.com", recycle_tgt=True).tgt is None

    def test_recycling_disabled_does_not_read_cache(self, tmp_path):
        self._seed(tmp_path)
        assert self._client(tmp_path, "alice@example.com", recycle_tgt=False).tgt is None

    def test_explicit_ticket_is_honoured_without_recycling(self, tmp_path):
        client = self._client(
            tmp_path, "bob@example.com", recycle_tgt=False,
            tgt_d={"tgt": "EXPLICIT", "tgt_exp": 9e9, "tgt_exp_0": 9e9},
        )
        assert client.tgt == "EXPLICIT"

    def test_profiles_are_separate(self, tmp_path):
        self._seed(tmp_path)
        other = self._client(
            tmp_path, "alice@example.com", recycle_tgt=True, tgt_profile="second"
        )
        assert other.tgt is None

    def test_cache_is_private_and_holds_no_password(self, tmp_path):
        import stat

        self._seed(tmp_path)
        path = tmp_path / ".eptr2-tgt"
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
        assert "pw" not in path.read_text(encoding="utf-8")

    def test_corrupt_cache_is_a_miss(self, tmp_path):
        self._seed(tmp_path)
        (tmp_path / ".eptr2-tgt").write_text("{not json", encoding="utf-8")
        assert self._client(tmp_path, "alice@example.com", recycle_tgt=True).tgt is None


def test_bundled_schema_available_without_pandas():
    """Minimal installs cannot regenerate the schema but must still read it."""
    import json

    from eptr2.agentic import load_bundled_schema

    schema = json.loads(load_bundled_schema())
    assert schema["endpoint_count"] >= 231


def test_empty_production_plans_return_empty_frame_not_crash():
    from types import SimpleNamespace as NS

    from eptr2.composite.production import get_hourly_production_plan_data

    fake = NS(call=lambda *a, **kw: pd.DataFrame())
    out = get_hourly_production_plan_data("2025-01-01", "2025-01-01", eptr=fake)
    assert isinstance(out, pd.DataFrame)
    assert out.empty
    assert "dt" in out.columns


def test_optional_settings_survive_partially_constructed_clients():
    """EPTR2.__getattr__ returns a callable for any missing attribute, so
    getattr(self, name, default) silently yields a method instead of the
    default. Optional settings must be read via __dict__."""
    import urllib3

    client = _offline_client()
    for attr in ("strict_params", "connect_timeout", "read_timeout", "tgt_profile"):
        client.__dict__.pop(attr, None)

    with patch("urllib3.PoolManager.request") as request:
        request.return_value = SimpleNamespace(data=b'{"items": []}', status=200)
        client.call("rt-gen", start_date="2025-01-01", end_date="2025-01-01")
        timeout = request.call_args.kwargs["timeout"]

    assert isinstance(timeout, urllib3.Timeout)
    assert isinstance(timeout.connect_timeout, float)
    assert isinstance(timeout.read_timeout, float)


def test_reserved_options_cover_everything_the_call_path_consumes():
    """Any option EPTR2/transparency_call consumes must be reserved, or the
    unknown-parameter warning fires on the library's own internal calls."""
    import re
    from pathlib import Path

    from eptr2.main import RESERVED_CALL_OPTIONS

    source = (Path(__file__).resolve().parents[1] / "src" / "eptr2" / "main.py").read_text(
        encoding="utf-8"
    )
    consumed = set(re.findall(r'kwargs\.(?:pop|get)\("([a-z_]+)"', source))
    missing = sorted(consumed - set(RESERVED_CALL_OPTIONS))
    assert not missing, f"not reserved, will warn spuriously: {missing}"


def test_ticket_cache_is_scoped_to_service_environment(tmp_path):
    """A ticket issued by the -prp test platform is not valid on production,
    so the same account must not share a cache across environments."""
    from eptr2 import EPTR2

    def client(**kwargs):
        with patch.object(EPTR2, "check_renew_tgt", lambda self, **kw: None):
            return EPTR2(
                username="alice@example.com", password="pw", use_dotenv=False,
                tgt_path=str(tmp_path), **kwargs,
            )

    prod = client(recycle_tgt=True)
    prod.tgt, prod.tgt_exp, prod.tgt_exp_0 = "TGT-PROD", 9e9, 9e9
    prod.export_tgt_info()

    assert client(recycle_tgt=True).tgt == "TGT-PROD"
    assert client(recycle_tgt=True, is_test=True).tgt is None
    assert client(recycle_tgt=True, root_phrase="https://other.example.com").tgt is None


# --- production composite: skip-flag derivation and kwargs collision --------


class _ProductionClient:
    """Fake client returning a minimal frame both production sources accept."""

    def __init__(self):
        self.keys = []

    def call(self, call_key, **params):
        self.keys.append(call_key)
        return pd.DataFrame(
            {"date": ["2026-07-01T00:00:00+03:00"], "hour": ["00:00"], "toplam": [1.0]}
        )


def test_production_without_plant_ids_fetches_system_totals():
    """A missing plant id means 'no filter', not 'skip': asking for total
    production used to raise 'Both skip_rt and skip_uevm cannot be True'."""
    from eptr2.composite.production import get_hourly_production_data

    fake = _ProductionClient()
    df = get_hourly_production_data("2026-07-01", "2026-07-01", eptr=fake)

    assert set(fake.keys) == {"rt-gen", "uevm"}, "both sources should be queried"
    assert isinstance(df, pd.DataFrame)


def test_production_with_one_plant_id_skips_the_other_source():
    """Plant-level and system-wide figures must not be merged into one frame."""
    from eptr2.composite.production import get_hourly_production_data

    fake = _ProductionClient()
    get_hourly_production_data("2026-07-01", "2026-07-01", eptr=fake, rt_pp_id=641)
    assert fake.keys == ["rt-gen"]

    fake = _ProductionClient()
    get_hourly_production_data("2026-07-01", "2026-07-01", eptr=fake, uevm_pp_id=142)
    assert fake.keys == ["uevm"]


def test_explicit_skip_flags_still_win():
    from eptr2.composite.production import get_hourly_production_data

    fake = _ProductionClient()
    get_hourly_production_data("2026-07-01", "2026-07-01", eptr=fake, skip_rt=True)
    assert fake.keys == ["uevm"]

    with pytest.raises(ValueError, match="cannot be True"):
        get_hourly_production_data(
            "2026-07-01", "2026-07-01", eptr=_ProductionClient(),
            skip_rt=True, skip_uevm=True,
        )


def test_wrapper_accepts_skip_flags_in_kwargs(monkeypatch):
    """The wrapper passed skip_uevm= explicitly *and* forwarded **kwargs, so a
    caller supplying it hit 'got multiple values for keyword argument'."""
    import eptr2.composite.production as prod

    received = {}

    def fake_plan(*args, **kwargs):
        return pd.DataFrame({"dt": ["2026-07-01T00:00:00+03:00"], "contract": ["PH26070100"]})

    def fake_realized(*args, **kwargs):
        received.update(kwargs)
        return pd.DataFrame({"dt": ["2026-07-01T00:00:00+03:00"], "contract": ["PH26070100"]})

    monkeypatch.setattr(prod, "get_hourly_production_plan_data", fake_plan)
    monkeypatch.setattr(prod, "get_hourly_production_data", fake_realized)

    prod.wrapper_hourly_production_plan_and_realized(
        "2026-07-01", "2026-07-01", eptr=_ProductionClient(), skip_uevm=True
    )
    assert received.get("skip_uevm") is True, "caller's flag must be forwarded"
