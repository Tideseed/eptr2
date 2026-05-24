"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_mms",
    "get_mms_message_type_list",
    "get_mms_pp_list",
    "get_mms_region_list",
    "get_mms_uevcb_list",
]

def get_mms(start_date: str, end_date: str, region_id: str | int, org_id: str | int | None = None, uevcb_id: str | int | None = None, pp_id: str | int | None = None, message_type_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Market Message System / Piyasa Mesaj Sistemi

    Category: PMS

    EN (Market Message System):
        It is the outage or maintenance information of the relevant power plant.

    TR (Piyasa Mesaj Sistemi):
        İlgili santralin arıza veya bakım bilgileridir.

    Reference: https://seffaflik.epias.com.tr/electricity/market-message-system
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mms", start_date=start_date, end_date=end_date, region_id=region_id, org_id=org_id, uevcb_id=uevcb_id, pp_id=pp_id, message_type_id=message_type_id, **kwargs)


def get_mms_message_type_list(eptr: EPTR2 | None = None, **kwargs):
    """Market Message System Message Type List / Piyasa Mesaj Sistemi Mesaj Tipi Listesi

    Category: Listeleme

    EN (Market Message System Message Type List):
        Market Message System Message Type List

    TR (Piyasa Mesaj Sistemi Mesaj Tipi Listesi):
        Piyasa Mesaj Sistemi Mesaj Tipi Listesi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_umm-message-type-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mms-message-type-list", **kwargs)


def get_mms_pp_list(start_date: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """MMS Power Plant Listing by Organization / PMS Organizasyona Göre Santral Listeleme

    Category: Listeleme

    EN (MMS Power Plant Listing by Organization):
        MMS Power Plant Listing by Organization.

    TR (PMS Organizasyona Göre Santral Listeleme):
        PMS Organizasyona Göre Santral Listeleme.

    Reference: https://seffaflik.epias.com.tr/electricity/market-message-system
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mms-pp-list", start_date=start_date, org_id=org_id, **kwargs)


def get_mms_region_list(eptr: EPTR2 | None = None, **kwargs):
    """Market Message System Region List / Piyasa Mesaj Sistemi Bölge Listeleme Servisi

    Category: Listeleme

    EN (Market Message System Region List):
        Market Message System Region List

    TR (Piyasa Mesaj Sistemi Bölge Listeleme Servisi):
        Piyasa Mesaj Sistemi Bölge Listeleme Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_umm-region-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mms-region-list", **kwargs)


def get_mms_uevcb_list(start_date: str, pp_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    """MMS Power Plant Listing by UEVCB / PMS UEVÇB'ye Göre Santral Listeleme

    Category: Listeleme

    EN (MMS Power Plant Listing by UEVCB):
        MMS Power Plant Listing by UEVCB.

    TR (PMS UEVÇB'ye Göre Santral Listeleme):
        PMS UEVÇB'ye Göre Santral Listeleme.

    Reference: https://seffaflik.epias.com.tr/electricity/market-message-system
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mms-uevcb-list", start_date=start_date, pp_id=pp_id, **kwargs)

