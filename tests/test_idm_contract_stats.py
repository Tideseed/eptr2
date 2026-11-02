"""get_idm_contract_stats: market wide MAD / TAD per contract, written to and read from files (no credentials needed)."""
import pandas as pd
import pytest

import eptr2.composite.idm_log as il

LOG = pd.DataFrame(
    {
        "contractName": ["PH26102000", "PH26102000", "PH26102001", "PB26102000"],
        "price": [100.0, 130.0, 150.0, 999.0],
        "quantity": [20, 10, 5, 50],
    }
)
KW = dict(start_date="2026-10-20", end_date="2026-10-20")


@pytest.fixture
def fetches(monkeypatch):
    calls = []
    monkeypatch.setattr(il, "idm_log_longer", lambda **kw: calls.append(kw) or LOG.copy())
    return calls


def test_stats_mad_and_tad(tmp_path, fetches):
    df = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path)).set_index("contract")
    assert list(df.index) == ["PH26102000", "PH26102001"]  # block contracts left out
    r = df.loc["PH26102000"]
    ## wap = (100*20 + 130*10) / 30 = 110; mad = (10*20 + 20*10) / 30 TL/MWh over 3 MWh
    assert r.idm_wap == pytest.approx(110.0)
    assert r.idm_mad == pytest.approx(400 / 30)
    assert r.idm_tad == pytest.approx(40.0)  # sum |p - wap| * q in MWh = mad * volume
    assert r.idm_tad == pytest.approx(r.idm_mad * r.idm_volume_mwh)
    assert df.loc["PH26102001", "idm_tad"] == pytest.approx(0.0)


def test_writes_files_and_reads_them_first(tmp_path, fetches):
    first = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path), days_interval=3)
    assert len(fetches) == 1 and fetches[0]["days_interval"] == 3
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "idm_contract_stats_2026-10-20_2026-10-20.csv",
        "idm_log_2026-10-20_2026-10-20.csv",
    ]
    second = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path))
    assert len(fetches) == 1  # read from file, not fetched
    pd.testing.assert_frame_equal(first, second, check_dtype=False)

    ## without the statistics file, the log file is used
    (tmp_path / "idm_contract_stats_2026-10-20_2026-10-20.csv").unlink()
    third = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path))
    assert len(fetches) == 1
    pd.testing.assert_frame_equal(first, third, check_dtype=False)


def test_old_stats_file_is_recalculated(tmp_path, fetches):
    ## eptr2 1.4.0 wrote idm_tad meaning the MAD and no idm_mad column
    pd.DataFrame({"contract": ["PH26102000"], "idm_wap": [110.0], "idm_tad": [13.3]}).to_csv(
        tmp_path / "idm_contract_stats_2026-10-20_2026-10-20.csv", index=False
    )
    df = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path))
    assert len(fetches) == 1 and "idm_mad" in df


def test_no_files_without_export(tmp_path, fetches):
    il.get_idm_contract_stats(**KW, export_dir=str(tmp_path), export_to_csv=False, check_existing=False)
    assert list(tmp_path.iterdir()) == []


def test_rejects_today_or_later(monkeypatch, fetches):
    monkeypatch.setattr(il, "get_today_utc3", lambda: "2026-10-20")
    with pytest.raises(ValueError, match="before today"):
        il.get_idm_contract_stats(**KW)
    assert fetches == []
