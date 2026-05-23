"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_ng_vgp_contract_price_summary",
    "get_ng_vgp_contract_price_summary_period",
    "get_ng_vgp_contract_price_summary_se",
    "get_ng_vgp_delivery_period",
    "get_ng_vgp_delivery_year",
    "get_ng_vgp_ggf",
    "get_ng_vgp_ggf_period",
    "get_ng_vgp_ggf_se",
    "get_ng_vgp_matched_quantity",
    "get_ng_vgp_matched_quantity_period",
    "get_ng_vgp_matched_quantity_se",
    "get_ng_vgp_open_positions",
    "get_ng_vgp_open_positions_period",
    "get_ng_vgp_open_positions_se",
    "get_ng_vgp_order_book",
    "get_ng_vgp_transaction_history",
    "get_ng_vgp_transaction_history_period",
    "get_ng_vgp_transaction_history_se",
    "get_ng_vgp_transaction_volumes",
    "get_ng_vgp_transaction_volumes_period",
    "get_ng_vgp_transaction_volumes_se",
]

def get_ng_vgp_contract_price_summary(is_txn_period: bool, start_date: str | None = None, end_date: str | None = None, delivery_period: str | None = None, delivery_year: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """GFM Contract Price Summary / VGP Kontrat Fiyatları Özeti

    Category: NG

    EN (GFM Contract Price Summary):
        It shows Match Price Statistics of futures contracts.

    TR (VGP Kontrat Fiyatları Özeti):
        Vadeli kontratların Eşleşme Fiyatı İstatistiklerini gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-contract-price-summary
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-contract-price-summary", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_contract_price_summary_period(is_txn_period: bool, delivery_period: str, delivery_year: str | int, eptr: EPTR2 | None = None, **kwargs):
    """GFM Contract Price Summary (Compulsory Period Selection) / VGP Kontrat Fiyatları Özeti (Zorunlu Period Seçimi)

    Category: NG

    EN (GFM Contract Price Summary (Compulsory Period Selection)):
        It shows Match Price Statistics of futures contracts.

    TR (VGP Kontrat Fiyatları Özeti (Zorunlu Period Seçimi)):
        Vadeli kontratların Eşleşme Fiyatı İstatistiklerini gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-contract-price-summary
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-contract-price-summary-period", is_txn_period=is_txn_period, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_contract_price_summary_se(is_txn_period: bool, start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """GFM Contract Price Summary (Compulsory Date Selection) / VGP Kontrat Fiyatları Özeti (Zorunlu Tarih Seçimi)

    Category: NG

    EN (GFM Contract Price Summary (Compulsory Date Selection)):
        It shows Match Price Statistics of futures contracts.

    TR (VGP Kontrat Fiyatları Özeti (Zorunlu Tarih Seçimi)):
        Vadeli kontratların Eşleşme Fiyatı İstatistiklerini gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-contract-price-summary
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-contract-price-summary-se", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, **kwargs)


def get_ng_vgp_delivery_period(eptr: EPTR2 | None = None, **kwargs):
    """VGP Delivery Period / VGP Teslimat Dönemi

    Category: NG

    EN (VGP Delivery Period):
        Delivery period information.

    TR (VGP Teslimat Dönemi):
        Teslimat dönemi bilgilerini gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas-service/technical/tr/index.html#_delivery-period
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-delivery-period", **kwargs)


def get_ng_vgp_delivery_year(eptr: EPTR2 | None = None, **kwargs):
    """VGP Delivery Year / VGP Teslimat Yılı

    Category: NG

    EN (VGP Delivery Year):
        Delivery year information

    TR (VGP Teslimat Yılı):
        Teslimat yılı bilgilerini gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas-service/technical/tr/index.html#_delivery-year
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-delivery-year", **kwargs)


def get_ng_vgp_ggf(is_txn_period: bool, start_date: str | None = None, end_date: str | None = None, delivery_period: str | None = None, delivery_year: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """GFM Daily Index Price / VGP Günlük Gösterge Fiyatı

    Category: NG

    EN (GFM Daily Index Price):
        It shows Weighted Average Price of day-ahead and intraday pairings in the Futures Natural Gas Market (VGP).

    TR (VGP Günlük Gösterge Fiyatı):
        Vadeli Doğal Gaz Piyasasında (VGP) gün öncesi ve gün içi eşleşmelerinin Ağırlıklı Ortalama Fiyatını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-daily-index-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-ggf", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_ggf_period(is_txn_period: bool, delivery_period: str, delivery_year: str | int, eptr: EPTR2 | None = None, **kwargs):
    """GFM Daily Index Price (Compulsory Period Selection) / VGP Günlük Gösterge Fiyatı (Zorunlu Period Seçimi)

    Category: NG

    EN (GFM Daily Index Price (Compulsory Period Selection)):
        It shows Weighted Average Price of day-ahead and intraday pairings in the Futures Natural Gas Market (VGP).

    TR (VGP Günlük Gösterge Fiyatı (Zorunlu Period Seçimi)):
        Vadeli Doğal Gaz Piyasasında (VGP) gün öncesi ve gün içi eşleşmelerinin Ağırlıklı Ortalama Fiyatını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-daily-index-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-ggf-period", is_txn_period=is_txn_period, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_ggf_se(is_txn_period: bool, start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """GFM Daily Index Price (Compulsory Date Selection) / VGP Günlük Gösterge Fiyatı (Zorunlu Tarih Seçimi)

    Category: NG

    EN (GFM Daily Index Price (Compulsory Date Selection)):
        It shows Weighted Average Price of day-ahead and intraday pairings in the Futures Natural Gas Market (VGP).

    TR (VGP Günlük Gösterge Fiyatı (Zorunlu Tarih Seçimi)):
        Vadeli Doğal Gaz Piyasasında (VGP) gün öncesi ve gün içi eşleşmelerinin Ağırlıklı Ortalama Fiyatını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-daily-index-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-ggf-se", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, **kwargs)


def get_ng_vgp_matched_quantity(is_txn_period: bool, start_date: str | None = None, end_date: str | None = None, delivery_period: str | None = None, delivery_year: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """GFM Matching Amount (1000.Sm3/day) / VGP Piyasa Eşleşme Miktarı (1000.Sm3/gün)

    Category: NG

    EN (GFM Matching Amount (1000.Sm3/day)):
        It shows Weighted Average Prices of Bids and/or Matches of Futures Contracts.

    TR (VGP Piyasa Eşleşme Miktarı (1000.Sm3/gün)):
        Vadeli kontratların Teklif ve/veya Eşleşmelerinin Ağırlıklı Ortalama Fiyatlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-matching-amount-1000-sm-day
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-matched-quantity", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_matched_quantity_period(is_txn_period: bool, delivery_period: str, delivery_year: str | int, eptr: EPTR2 | None = None, **kwargs):
    """GFM Matching Amount (1000.Sm3/day) (Compulsory Period Selection) / VGP Piyasa Eşleşme Miktarı (1000.Sm3/gün) (Zorunlu Period Seçimi)

    Category: NG

    EN (GFM Matching Amount (1000.Sm3/day) (Compulsory Period Selection)):
        It shows Weighted Average Prices of Bids and/or Matches of Futures Contracts.

    TR (VGP Piyasa Eşleşme Miktarı (1000.Sm3/gün) (Zorunlu Period Seçimi)):
        Vadeli kontratların Teklif ve/veya Eşleşmelerinin Ağırlıklı Ortalama Fiyatlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-matching-amount-1000-sm-day
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-matched-quantity-period", is_txn_period=is_txn_period, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_matched_quantity_se(is_txn_period: bool, start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """GFM Matching Amount (1000.Sm3/day) (Compulsory Date Selection) / VGP Piyasa Eşleşme Miktarı (1000.Sm3/gün) (Zorunlu Tarih Seçimi)

    Category: NG

    EN (GFM Matching Amount (1000.Sm3/day) (Compulsory Date Selection)):
        It shows Weighted Average Prices of Bids and/or Matches of Futures Contracts.

    TR (VGP Piyasa Eşleşme Miktarı (1000.Sm3/gün) (Zorunlu Tarih Seçimi)):
        Vadeli kontratların Teklif ve/veya Eşleşmelerinin Ağırlıklı Ortalama Fiyatlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-matching-amount-1000-sm-day
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-matched-quantity-se", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, **kwargs)


def get_ng_vgp_open_positions(is_txn_period: bool, start_date: str | None = None, end_date: str | None = None, delivery_period: str | None = None, delivery_year: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """GFM Open Position (1000.Sm3/day) / VGP Açık Pozisyon Miktarı (1000.Sm3/gün)

    Category: NG

    EN (GFM Open Position (1000.Sm3/day)):
        It shows the Spread Amount of the Futures Contracts for Bid and Sell Matches.

    TR (VGP Açık Pozisyon Miktarı (1000.Sm3/gün)):
        Vadeli kontratların Alış ve Satış Eşleşmeleri Fark Miktarını gösterir

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-open-position-1000-sm-day
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-open-positions", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_open_positions_period(is_txn_period: bool, delivery_period: str, delivery_year: str | int, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-open-positions-period", is_txn_period=is_txn_period, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_open_positions_se(is_txn_period: bool, start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-open-positions-se", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, **kwargs)


def get_ng_vgp_order_book(eptr: EPTR2 | None = None, **kwargs):
    """GFM Order Prices / VGP Teklif Fiyatları

    Category: NG

    EN (GFM Order Prices):
        It shows Bid Price Statistics of futures contracts.

    TR (VGP Teklif Fiyatları):
        Vadeli kontratların Teklif Fiyatı İstatistiklerini gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-order-prices
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-order-book", **kwargs)


def get_ng_vgp_transaction_history(is_txn_period: bool, eptr: EPTR2 | None = None, **kwargs):
    """GFM Transaction History / VGP İşlem Akışı

    Category: NG

    EN (GFM Transaction History):
        It shows Matching Times of futures contracts.

    TR (VGP İşlem Akışı):
        Vadeli kontratların Eşleşme Zamanlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-transaction-history
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-transaction-history", is_txn_period=is_txn_period, **kwargs)


def get_ng_vgp_transaction_history_period(is_txn_period: bool, delivery_period: str, delivery_year: str | int, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-transaction-history-period", is_txn_period=is_txn_period, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_transaction_history_se(is_txn_period: bool, start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-transaction-history-se", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, **kwargs)


def get_ng_vgp_transaction_volumes(is_txn_period: bool, eptr: EPTR2 | None = None, **kwargs):
    """GFM Trade Volume / VGP İşlem Hacmi

    Category: NG

    EN (GFM Trade Volume):
        It shows Matched Amount of futures contracts.

    TR (VGP İşlem Hacmi):
        Vadeli kontratların Eşleşme Tutarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/gas-future-market-gfm/gfm-trade-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-transaction-volumes", is_txn_period=is_txn_period, **kwargs)


def get_ng_vgp_transaction_volumes_period(is_txn_period: bool, delivery_period: str, delivery_year: str | int, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-transaction-volumes-period", is_txn_period=is_txn_period, delivery_period=delivery_period, delivery_year=delivery_year, **kwargs)


def get_ng_vgp_transaction_volumes_se(is_txn_period: bool, start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-vgp-transaction-volumes-se", is_txn_period=is_txn_period, start_date=start_date, end_date=end_date, **kwargs)

