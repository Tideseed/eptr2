"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_bi_euas",
    "get_bi_long",
    "get_bi_short",
]

def get_bi_euas(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Amount of Bilateral Contracts of EÜAŞ - Authorized Retailers / EÜAŞ - GTŞ İkili Anlaşmalar

    Category: İA

    EN (Amount of Bilateral Contracts of EÜAŞ - Authorized Retailers):
        It indicates the monthly totals of bilateral agreements realized between EÜAŞ and Authorized Retail Companies according to the regulated tariff.

    TR (EÜAŞ - GTŞ İkili Anlaşmalar):
        Düzenlemeye tabi tarife kapsamına göre EÜAŞ ile GTŞ’lerin arasında yapılan ikili anlaşmaların aylık toplamlarını göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/bilateral-contracts/amount-of-bilateral-contracts-of-euas-authorized-retailers
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bi-euas", start_date=start_date, end_date=end_date, **kwargs)


def get_bi_long(start_date: str, end_date: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Bilateral Contracts Bid Quantity / İkili Anlaşma (İA) Alış Miktarı

    Category: İA

    EN (Bilateral Contracts Bid Quantity):
        It indicates the purchased power amount through bilateral power contracts.

    TR (İkili Anlaşma (İA) Alış Miktarı):
        İkili anlaşmalara ait alış miktarları verisidir

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/bilateral-contracts/bilateral-contracts-bid-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bi-long", start_date=start_date, end_date=end_date, org_id=org_id, **kwargs)


def get_bi_short(start_date: str, end_date: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Bilateral Contracts Offer Quantity / İkili Anlaşma (İA) Satış Miktarı

    Category: İA

    EN (Bilateral Contracts Offer Quantity):
        It indicates the sold power amount through bilateral power contracts.

    TR (İkili Anlaşma (İA) Satış Miktarı):
        İkili anlaşmalara ait satış miktarları verisidir

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/bilateral-contracts/bilateral-contracts-offer-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bi-short", start_date=start_date, end_date=end_date, org_id=org_id, **kwargs)

