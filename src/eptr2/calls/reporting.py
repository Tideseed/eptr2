"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_bpm_orders",
    "get_bpm_orders_w_avg",
    "get_electricity_market_quantity",
    "get_idm_contract_list",
    "get_idm_order_history",
    "get_idm_summary",
    "get_mcp_smp_imb",
]

def get_bpm_orders(date: str, eptr: EPTR2 | None = None, **kwargs):
    """BPM Instructions / DGP Talimatları

    Category: Elektrik Piyasası Raporları

    EN (BPM Instructions):
        (No description)

    TR (DGP Talimatları):
        (Açıklama Yok)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-market-reports/bpm-instructions
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bpm-orders", date=date, **kwargs)


def get_bpm_orders_w_avg(date: str, eptr: EPTR2 | None = None, **kwargs):
    """BPM Instructions (Weighted Average) / DGP Talimatları (Ağırlıklı Ortalama)

    Category: Elektrik Piyasası Raporları

    EN (BPM Instructions (Weighted Average)):
        (No description)

    TR (DGP Talimatları (Ağırlıklı Ortalama)):
        (Açıklama Yok)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-market-reports/bpm-instructions-weighted-average
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bpm-orders-w-avg", date=date, **kwargs)


def get_electricity_market_quantity(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Electricity Market Volume Physically / Elektrik Piyasa Hacimleri Fiziksel

    Category: Elektrik Piyasası Raporları

    EN (Electricity Market Volume Physically):
        (No description)

    TR (Elektrik Piyasa Hacimleri Fiziksel):
        (Açıklama Yok)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-market-reports/electricity-market-volume-physically
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("electricity-market-quantity", start_date=start_date, end_date=end_date, **kwargs)


def get_idm_contract_list(se_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Contract List / GİP Kontrat Listesi

    Category: Elektrik Piyasası Raporları

    EN (IDM Contract List):
        (No description)

    TR (GİP Kontrat Listesi):
        (Açıklama Yok)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-market-reports/idm-order-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-contract-list", se_date=se_date, **kwargs)


def get_idm_order_history(se_date: str, idm_contract_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-order-history", se_date=se_date, idm_contract_id=idm_contract_id, **kwargs)


def get_idm_summary(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Contract Summary / GİP Kontrat Özeti

    Category: Elektrik Piyasası Raporları

    EN (IDM Contract Summary):
        (No description)

    TR (GİP Kontrat Özeti):
        (Açıklama Yok)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-market-reports/idm-contract-summary
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-summary", start_date=start_date, end_date=end_date, **kwargs)


def get_mcp_smp_imb(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """MCP SMP and Imbalance Price Listing / PTF, SMF ve SDF Listeleme

    Category: Elektrik Piyasası Raporları

    EN (MCP SMP and Imbalance Price Listing):
        (No description)

    TR (PTF, SMF ve SDF Listeleme):
        (Açıklama Yok)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-market-reports/mcp-smp-and-imbalance-price-listing
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mcp-smp-imb", start_date=start_date, end_date=end_date, **kwargs)

