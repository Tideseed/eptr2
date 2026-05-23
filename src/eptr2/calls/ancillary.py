"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_anc_pf_qty",
    "get_anc_pfk",
    "get_anc_sf_qty",
    "get_anc_sfk",
]

def get_anc_pf_qty(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Primary Frequency Capacity Amount / Primer Frekans Rezerv Miktarı

    Category: Yan Hizmetler

    EN (Primary Frequency Capacity Amount):
        It displays hourly total primary frequency capacity volume that the participants need to reserve for the real time frequency balancing.

    TR (Primer Frekans Rezerv Miktarı):
        Katılımcıların gerçek zamanlı frekans dengeleme için ayırması gereken saatlik toplam birincil frekans kapasite hacimleridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/ancillary-services/primary-frequency-capacity-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("anc-pf-qty", start_date=start_date, end_date=end_date, **kwargs)


def get_anc_pfk(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Primary Frequency Capacity Price (PFCP) / Primer Frekans Kontrolü (PFK) Fiyat

    Category: Yan Hizmetler

    EN (Primary Frequency Capacity Price (PFCP)):
        It displays Primary Frequency Capacity Price determined by the tender on an hourly basis. Tenders are held by Transmission System Operator.

    TR (Primer Frekans Kontrolü (PFK) Fiyat):
        Saatlik bazda ihale ile belirlenen PFK kapasite bedelidir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/ancillary-services/primary-frequency-capacity-price-pfcp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("anc-pfk", start_date=start_date, end_date=end_date, **kwargs)


def get_anc_sf_qty(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Secondary Frequency Capacity Amount / Sekonder Frekans Rezerv Miktarı

    Category: Yan Hizmetler

    EN (Secondary Frequency Capacity Amount):
        It displays hourly total secondary frequency capacity volume that the participants need to reserve for the real time frequency balancing.

    TR (Sekonder Frekans Rezerv Miktarı):
        Saatlik toplam belirlenen rezerv miktarlarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/ancillary-services/secondary-frequency-capacity-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("anc-sf-qty", start_date=start_date, end_date=end_date, **kwargs)


def get_anc_sfk(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Secondary Frequency Capacity Price (SFCP) / Sekonder Frekans Kontrolü (SFK) Fiyat

    Category: Yan Hizmetler

    EN (Secondary Frequency Capacity Price (SFCP)):
        It displays Secondary Frequency Capacity Price determined by the tender on an hourly basis. Tenders are held by Transmission System Operator.

    TR (Sekonder Frekans Kontrolü (SFK) Fiyat):
        Saatlik bazda ihale ile belirlenen SFK kapasite bedelidir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/ancillary-services/secondary-frequency-capacity-price-sfcp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("anc-sfk", start_date=start_date, end_date=end_date, **kwargs)

