"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_vep_contract_price_summary",
    "get_vep_delivery_period_list",
    "get_vep_delivery_year_list",
    "get_vep_ggf",
    "get_vep_ggf_period",
    "get_vep_load_types",
    "get_vep_matching_quantity",
    "get_vep_open_positions",
    "get_vep_price_summaries",
    "get_vep_trade_volume",
    "get_vep_transaction_history",
    "get_vep_transaction_history_periods",
]

def get_vep_contract_price_summary(start_date: str, end_date: str, load_type: str | None = None, year: str | int | None = None, delivery_period: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """PFM Contract Price Summary / VEP Kontrat Fiyatları Özet

    Category: VEP

    EN (PFM Contract Price Summary):
        First, highest, lowest, last matching prices and DIP of the contracts that are open for trading at the filtered dates.

    TR (VEP Kontrat Fiyatları Özet):
        Seçilen tarihte YEK-G Belgelerinin kaynak bazında gerçekleşen son eşleşme miktarı ve işlem miktarlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-contract-price-summary
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-contract-price-summary", start_date=start_date, end_date=end_date, load_type=load_type, year=year, delivery_period=delivery_period, **kwargs)


def get_vep_delivery_period_list(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """PFM Delivery Period Listing Service / VEP Teslimat Dönemi Listeleme Servisi

    Category: VEP

    EN (PFM Delivery Period Listing Service):
        Returns the Delivery Period List for PFM pages.

    TR (VEP Teslimat Dönemi Listeleme Servisi):
        VEP sayfaları için Teslimat Dönemi Listesi verir.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_delivery-period-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-delivery-period-list", start_date=start_date, end_date=end_date, **kwargs)


def get_vep_delivery_year_list(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """PFM Delivery Year Listing Service / VEP Teslimat Yılı Listeleme Servisi

    Category: VEP

    EN (PFM Delivery Year Listing Service):
        Returns the Delivery Year List for PFM pages.

    TR (VEP Teslimat Yılı Listeleme Servisi):
        VEP sayfaları için Teslimat Yılı Listesi verir.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_delivery-year-list-data
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-delivery-year-list", start_date=start_date, end_date=end_date, **kwargs)


def get_vep_ggf(start_date: str, end_date: str, load_type: str | None = None, year: str | int | None = None, delivery_period: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """PFM Daily Index Price / VEP Günlük Gösterge Fiyatı

    Category: VEP

    EN (PFM Daily Index Price):
        The Daily Index Price of contracts that are open for trading at the filtered dates. Daily Index Price is published at 16:45 o'clock on business days for the contracts that are open for trading.

    TR (VEP Günlük Gösterge Fiyatı):
        Seçilen tarihte işleme açık kontratların Günlük Gösterge Fiyatını göstermektedir. Seansın açık olduğu her gün işleme açık kontratların ilgili gün için Günlük Gösterge fiyatı saat 16:45'te yayımlanır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-daily-index-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-ggf", start_date=start_date, end_date=end_date, load_type=load_type, year=year, delivery_period=delivery_period, **kwargs)


def get_vep_ggf_period(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """PFM DIP Delivery Period List / VEP GGF Teslimat Dönemi Listeleme Servisi

    Category: VEP

    EN (PFM DIP Delivery Period List):
        Returns the Delivery Period List for PFM DIP pages.

    TR (VEP GGF Teslimat Dönemi Listeleme Servisi):
        VEP GGF sayfaları için Teslimat Dönemi Listesi verir.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_ggf-delivery-period-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-ggf-period", start_date=start_date, end_date=end_date, **kwargs)


def get_vep_load_types(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """PFM Load Type List / VEP Yük Tipi Listeme Servisi

    Category: VEP

    EN (PFM Load Type List):
        Returns the load type list for PFM pages.

    TR (VEP Yük Tipi Listeme Servisi):
        VEP sayfaları için Yük Tipi listesini verir.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_load-type-list-data
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-load-types", start_date=start_date, end_date=end_date, **kwargs)


def get_vep_matching_quantity(start_date: str, end_date: str, load_type: str | None = None, year: str | int | None = None, delivery_period: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """PFM Matching Quantity / VEP Eşleşme Miktarı

    Category: VEP

    EN (PFM Matching Quantity):
        Matching quantity of the contracts that are open for trading at the filtered dates.

    TR (VEP Eşleşme Miktarı):
        Seçilen tarihte işleme açık + işlem yapılan kontratların eşleşme miktarını göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-matching-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-matching-quantity", start_date=start_date, end_date=end_date, load_type=load_type, year=year, delivery_period=delivery_period, **kwargs)


def get_vep_open_positions(start_date: str, end_date: str, load_type: str | None = None, year: str | int | None = None, delivery_period: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """PFM Open Position / VEP Açık Pozisyon

    Category: VEP

    EN (PFM Open Position):
        Open Position of the contracts that are open for trading at the filtered dates.

    TR (VEP Açık Pozisyon):
        Seçilen tarihte işleme açık + işlem yapılan kontratların açık pozisyon miktarını göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-open-position
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-open-positions", start_date=start_date, end_date=end_date, load_type=load_type, year=year, delivery_period=delivery_period, **kwargs)


def get_vep_price_summaries(eptr: EPTR2 | None = None, **kwargs):
    """PFM Order Prices / VEP Teklif Fiyatları

    Category: VEP

    EN (PFM Order Prices):
        The price information of the best bid and sell orders of each contract in VEP, the price of the last match and its change according to the previous match.

    TR (VEP Teklif Fiyatları):
        VEP'teki her bir kontrata ait en iyi alış ve satış tekliflerine sait fiyat bilgisi, son eşleşme fiyatı ve bir önceki eşleşmeye göre değişimi.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-order-prices
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-price-summaries", **kwargs)


def get_vep_trade_volume(start_date: str, end_date: str, load_type: str | None = None, year: str | int | None = None, delivery_period: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """PFM Trade Value / VEP İşlem Hacmi

    Category: VEP

    EN (PFM Trade Value):
        Trade value of the contracts that are open for trading at the filtered dates.

    TR (VEP İşlem Hacmi):
        Seçilen tarihte işleme açık + işlem yapılan kontratların işlem hacmini göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-trade-value
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-trade-volume", start_date=start_date, end_date=end_date, load_type=load_type, year=year, delivery_period=delivery_period, **kwargs)


def get_vep_transaction_history(start_date: str, end_date: str, load_type: str | None = None, year: str | int | None = None, delivery_period: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """PFM Transaction History / VEP İşlem Akışı

    Category: VEP

    EN (PFM Transaction History):
        Transaction history of the contracts that are open for trading at the filtered dates.

    TR (VEP İşlem Akışı):
        Seçilen tarihte işleme açık + işlem yapılan kontratların işlem akışını göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/power-future-market-pfm/pfm-transaction-history
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-transaction-history", start_date=start_date, end_date=end_date, load_type=load_type, year=year, delivery_period=delivery_period, **kwargs)


def get_vep_transaction_history_periods(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """PFM Transaction History Delivery Period List / VEP İşlem Akışı Teslimat Dönemi Listesi

    Category: VEP

    EN (PFM Transaction History Delivery Period List):
        PFM Transaction History Delivery Period List.

    TR (VEP İşlem Akışı Teslimat Dönemi Listesi):
        VEP İşlem Akışı Teslimat Dönemi Listesi.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_th-delivery-period-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("vep-transaction-history-periods", start_date=start_date, end_date=end_date, **kwargs)

