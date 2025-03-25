## Add test for eptr2/composite/mms.py
from eptr2.composite.mms import get_mms_detail
from dotenv import load_dotenv, find_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params


@pytest.fixture
def mms_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_eptr2_composite_mms(mms_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    d = get_mms_detail(
        eptr=eptr,
        start_date=mms_params["start_date"],
        end_date=mms_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
        include_summary=True,
    )
    assert d is not None
    assert "detail" in d
    assert "summary" in d
    assert d["detail"] is not None
    assert d["summary"] is not None
    assert len(d["detail"]) > 0
    assert len(d["summary"]) > 0
    assert "contract" in d["detail"]
    assert "contract" in d["summary"]
