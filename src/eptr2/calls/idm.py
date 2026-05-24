"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_idm_log",
    "get_idm_mm_bid",
    "get_idm_mm_matching",
    "get_idm_mm_offer",
    "get_idm_ob_qty",
    "get_idm_qty",
    "get_idm_volume",
    "get_wap",
]

def get_idm_log(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Transaction History / GİP İşlem Akışı

    Category: GİP

    EN (IDM Transaction History):
        It shows the prices and quantities of instant transactions realized in the Intraday Market.

    TR (GİP İşlem Akışı):
        Gün İçi Piyasası’nda gerçekleşen anlık işlemlerin fiyat ve miktarlarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-transaction-history
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-log", start_date=start_date, end_date=end_date, **kwargs)


def get_idm_mm_bid(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Min.-Max. Bid Price / GİP Min - Maks Alış Teklif Fiyatı

    Category: GİP

    EN (IDM Min.-Max. Bid Price):
        It is the highest and lowest bid price displayed in the Intraday Market according to the contract type.

    TR (GİP Min - Maks Alış Teklif Fiyatı):
        Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük alış teklif fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-min-max-bid-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-mm-bid", start_date=start_date, end_date=end_date, **kwargs)


def get_idm_mm_matching(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Min.-Max. Matching Price / GİP Min - Maks Eşleşme Fiyat

    Category: GİP

    EN (IDM Min.-Max. Matching Price):
        It is the min and max matching price in the intraday market which is categorized as hourly or block depending on the contract type.

    TR (GİP Min - Maks Eşleşme Fiyat):
        Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük eşleşme fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-min-max-matching-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-mm-matching", start_date=start_date, end_date=end_date, **kwargs)


def get_idm_mm_offer(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Min-Max Offer Price / GİP Min - Maks Satış Teklif Fiyatı

    Category: GİP

    EN (IDM Min-Max Offer Price):
        Max. and min. offer price given as hourly or block depending on the contract type.

    TR (GİP Min - Maks Satış Teklif Fiyatı):
        Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük satış teklif fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-min-max-offer-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-mm-offer", start_date=start_date, end_date=end_date, **kwargs)


def get_idm_ob_qty(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Bid/Offer Quantities / GİP Teklif Edilen Alış Satış Miktarları

    Category: GİP

    EN (IDM Bid/Offer Quantities):
        It is the total quantity of orders in buy and sell side in the Intra Day Market.

    TR (GİP Teklif Edilen Alış Satış Miktarları):
        Gün İçi Piyasasında sunulan tekliflerin alış ve satış tekliflerinin toplam miktarlarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-bid-offer-quantities
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-ob-qty", start_date=start_date, end_date=end_date, **kwargs)


def get_idm_qty(start_date: str, end_date: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """IDM Matching Quantity / GİP Eşleşme Miktarı

    Category: GİP

    EN (IDM Matching Quantity):
        It is the total matching quantity in the intraday market which is categorized as hourly or block depending on the contract type.

    TR (GİP Eşleşme Miktarı):
        Gün İçi Piyasası’nda kontrat türüne göre saatlik veya blok olarak gösterilen toplam eşleşme miktarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-matching-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-qty", start_date=start_date, end_date=end_date, org_id=org_id, **kwargs)


def get_idm_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Trade Value / GİP İşlem Hacmi

    Category: GİP

    EN (IDM Trade Value):
        It is the hourly total financial volume of the matching bids and offers in the Intraday Market

    TR (GİP İşlem Hacmi):
        Gün İçi Piyasası’nda eşleşen alış-satış tekliflerinin saatlik toplam mali değeridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-trade-value
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("idm-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_wap(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """IDM Weighted Average Price / GİP Ağırlıklı Ortalama Fiyat

    Category: GİP

    EN (IDM Weighted Average Price):
        It is the hourly weighted average price for the transactions on each contract in Intraday Market.

    TR (GİP Ağırlıklı Ortalama Fiyat):
        Gün İçi Piyasası'ndaki her bir kontrata ilişkin işlemlerin saatlik bazda hacimsel ağırlıklı ortalama fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-weighted-average-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("wap", start_date=start_date, end_date=end_date, **kwargs)

