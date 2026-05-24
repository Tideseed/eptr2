"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_ng_balancing_notifications",
    "get_ng_balancing_price",
    "get_ng_bast",
    "get_ng_blue_code_ops",
    "get_ng_code_four_ops",
    "get_ng_daily_match_qty",
    "get_ng_daily_trade_volume",
    "get_ng_drp",
    "get_ng_gddk",
    "get_ng_green_code_ops",
    "get_ng_grp_match_qty",
    "get_ng_grp_trade_volume",
    "get_ng_imbalance_amount",
    "get_ng_imbalance_system",
    "get_ng_latest_settlement_date",
    "get_ng_match_quantity",
    "get_ng_orange_code_ops",
    "get_ng_physical_realization",
    "get_ng_shippers_imbalance_quantity",
    "get_ng_spot_prices",
    "get_ng_system_direction",
    "get_ng_total_trade_volume",
    "get_ng_transaction_history",
    "get_ng_virtual_realization",
    "get_ng_weekly_matched_quantity",
    "get_ng_weekly_trade_volume",
    "get_ng_wrp",
]

def get_ng_balancing_notifications(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Announcement for TSO Transactions / İlave Dengeleyici Bildirimleri

    Category: NG

    EN (Announcement for TSO Transactions):
        It shows to the notifications made to market participants for transactions aiming to eliminate the imbalance in the network.

    TR (İlave Dengeleyici Bildirimleri):
        Şebekede oluşan dengesizliği gidermeyi amaçlayan işlemler için piyasa katılımcılarına yapılan bildirimleri ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/tso-balancing-transactions/announcement-for-tso-transactions
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-balancing-notifications", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_balancing_price(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Balancing Gas Price (BGP) / Dengeleme Gazı Fiyatları (DGF)

    Category: NG

    EN (Balancing Gas Price (BGP)):
        It shows the Weighted Average Price of Additional Balancing Buy or Sell transactions performed by the Transmission Company on the relevant gas day.

    TR (Dengeleme Gazı Fiyatları (DGF)):
        İlgili gaz gününde İletim Şirketince gerçekleştirilen İlave Dengeleme Alış veya Satış işlemlerinin Ağırlıklı Ortalama Fiyatını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/price/balancing-gas-price-bgp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-balancing-price", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_bast(period: str, eptr: EPTR2 | None = None, **kwargs):
    """Neutralization Item / Bakiye Sıfırlama Tutarı (BAST)

    Category: NG

    EN (Neutralization Item):
        It shows amount remaining in EPİAŞ after deducting the receivables or debts of the Transmission Company and to be Distributed to the Participants in accordance with the legislation.

    TR (Bakiye Sıfırlama Tutarı (BAST)):
        İletim Şirketi alacak veya borcunun düşülmesinden sonra EPİAŞ'ta kalan ve mevzuata uygun şekilde Katılımcılara Dağıtılacak Tutarı gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/neutralization-item
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-bast", period=period, **kwargs)


def get_ng_blue_code_ops(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """2 Coded Transaction / 2 Kodlu İşlemler

    Category: NG

    EN (2 Coded Transaction):
        It shows to the 2 Coded Additional Balancer Operations aimed at eliminating the imbalance in the network.

    TR (2 Kodlu İşlemler):
        Şebekede oluşan dengesizliği gidermeyi amaçlayan 2 Kodlu İlave Dengeleyici İşlemlerini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/tso-balancing-transactions/2-coded-transaction
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-blue-code-ops", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_code_four_ops(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """4 Coded Transaction / 4 Kodlu İşlemler

    Category: NG

    EN (4 Coded Transaction):
        It shows to the 4 Coded Additional Balancer Operations aimed at eliminating the imbalance in the network.

    TR (4 Kodlu İşlemler):
        Şebekede oluşan dengesizliği gidermeyi amaçlayan 4 Kodlu İlave Dengeleyici İşlemlerini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/tso-balancing-transactions/4-coded-transaction
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-code-four-ops", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_daily_match_qty(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Daily Matched Quantity / SGP Günlük Eşleşme Miktarı

    Category: NG

    EN (SGP Daily Matched Quantity):
        It shows Total Amount of day-ahead and intra-day matches in daily contracts in the Spot Natural Gas Market.

    TR (SGP Günlük Eşleşme Miktarı):
        Spot Doğal Gaz Piyasasında günlük kontratlardaki gün öncesi ve gün içi eşleşmelerin Toplam Miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/matched-quantity/sgp-daily-matched-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-daily-match-qty", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_daily_trade_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Daily Reference Price (DRP) / SGP Günlük İşlem Hacmi

    Category: NG

    EN (Daily Reference Price (DRP)):
        It shows Weighted Average Price of day-ahead and intraday pairings in the Spot Natural Gas Market.

    TR (SGP Günlük İşlem Hacmi):
        Spot Doğal Gaz Piyasasında günlük kontratlardaki eşleşmelerin Toplam Tutarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/trade-volume/sgp-daily-trade-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-daily-trade-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_drp(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Günlük Referans Fiyatı (GRF)

    Category: NG

    TR (Günlük Referans Fiyatı (GRF)):
        Spot Doğal Gaz Piyasasında gün öncesi ve gün içi eşleşmelerinin Ağırlıklı Ortalama Fiyatını gösterir

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/price/daily-reference-price-drp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-drp", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_gddk(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Retroactive Adjustment Item Amount / Geriye Dönük Düzeltme Kalemi (GDDK) Tutarı

    Category: NG

    EN (Retroactive Adjustment Item Amount):
        It shows total Credit or Payable Amount in the new invoice with the retrospective corrections made in the previous period invoices.

    TR (Geriye Dönük Düzeltme Kalemi (GDDK) Tutarı):
        Geçmiş dönem faturalarında yapılan geriye dönük düzeltmeler ile yeni faturada oluşan Toplam Alacak veya Borç Tutarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/retroactive-adjustment-item-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-gddk", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_green_code_ops(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """1 Coded Transaction / 1 Kodlu İşlemler

    Category: NG

    EN (1 Coded Transaction):
        It shows to Additional Balancer Operations with Code 1 aiming to eliminate the imbalance in the network.

    TR (1 Kodlu İşlemler):
        Şebekede oluşan dengesizliği gidermeyi amaçlayan 1 Kodlu İlave Dengeleyici İşlemlerini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/tso-balancing-transactions/1-coded-transaction
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-green-code-ops", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_grp_match_qty(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Matched Quantity for DRP / GRF Eşleşme Miktarı

    Category: NG

    EN (Matched Quantity for DRP):
        It shows Total Amount of day-ahead and intra-day matches in daily contracts in the Spot Natural Gas Market.

    TR (GRF Eşleşme Miktarı):
        Spot Doğal Gaz Piyasasında günlük kontratlardaki gün öncesi ve gün içi eşleşmelerin Toplam Miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/matched-quantity/matched-quantity-for-drp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-grp-match-qty", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_grp_trade_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """GRP Trade Volume / GRF İşlem Hacmi

    Category: NG

    EN (GRP Trade Volume):
        It shows Total Amount of day-ahead and intra-day pairings in daily contracts in the Spot Natural Gas Market.

    TR (GRF İşlem Hacmi):
        Spot Doğal Gaz Piyasasında günlük kontratlardaki gün öncesi ve gün içi eşleşmelerin Toplam Tutarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/trade-volume/grp-trade-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-grp-trade-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_imbalance_amount(period: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Imbalance Amount / SGP Dengesizlik Tutarı

    Category: NG

    EN (SGP Imbalance Amount):
        It shows the amount that the Shippers are liable to pay for the imbalance in the network as a result of the purchase or sale weighted transactions.

    TR (SGP Dengesizlik Tutarı):
        Taşıtanların Alış veya Satış ağırlıklı işlemleri sonucu şebekede oluşan dengesizlik için ödemekle yükümlü oldukları Tutarı gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/imbalance/sgp-imbalance-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-imbalance-amount", period=period, **kwargs)


def get_ng_imbalance_system(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Imbalance System / Dengesizlik Sistem

    Category: NG

    EN (Imbalance System):
        It shows increase or decrease in the Network Stock Gas Amount compared to the previous gas day. It is marked with (+) if it is greater and (-) if it is less.

    TR (Dengesizlik Sistem):
        Önceki gaz gününe kıyasla, Şebeke Stok Gazı Miktarında oluşan artış veya azalışı gösterir. Büyükse (+) , küçükse (-) işaretlenir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/imbalance/imbalance-system
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-imbalance-system", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_latest_settlement_date(eptr: EPTR2 | None = None, **kwargs):
    """SGP Last Reconciliation Date Service / SGP Son Uzlaştırma Tarihi Servisi

    Category: NG

    EN (SGP Last Reconciliation Date Service):
        Last reconciliation date service.

    TR (SGP Son Uzlaştırma Tarihi Servisi):
        Son uzlaştırma tarihini verir.

    Reference: https://seffaflik.epias.com.tr/natural-gas-service/technical/tr/index.html#_stp-last-reconciliation-date
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-latest-settlement-date", **kwargs)


def get_ng_match_quantity(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Total Matched Quantity / SGP Toplam Eşleşme Miktarı

    Category: NG

    EN (SGP Total Matched Quantity):
        It shows Total Amount of matches in daily and weekly contracts in the Spot Natural Gas Market.

    TR (SGP Toplam Eşleşme Miktarı):
        Spot Doğal Gaz Piyasasında günlük ve haftalık kontratlardaki eşleşmelerin Toplam Miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/matched-quantity/sgp-total-matched-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-match-quantity", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_orange_code_ops(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """3 Coded Transaction / 3 Kodlu İşlemler

    Category: NG

    EN (3 Coded Transaction):
        It shows to the 3 Coded Additional Balancer Operations aimed at eliminating the imbalance in the network.

    TR (3 Kodlu İşlemler):
        Şebekede oluşan dengesizliği gidermeyi amaçlayan 3 Kodlu İlave Dengeleyici İşlemlerini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/tso-balancing-transactions/3-coded-transaction
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-orange-code-ops", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_physical_realization(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-physical-realization", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_shippers_imbalance_quantity(period: str, eptr: EPTR2 | None = None, **kwargs):
    """Shipper's Imbalance Quantity / Dengesizlik Taşıtan

    Category: NG

    EN (Shipper's Imbalance Quantity):
        It shows Natural Gas Excess or Deficiency Amount that occurs in the network as a result of the purchase or sale weighted transactions of the shippers.

    TR (Dengesizlik Taşıtan):
        Taşıtanların Alış veya Satış ağırlıklı işlemleri sonucu şebekede oluşan Doğal Gaz Fazlalığı veya Eksikliği Miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/imbalance/shipper-s-imbalance-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-shippers-imbalance-quantity", period=period, **kwargs)


def get_ng_spot_prices(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Price / SGP Fiyatlar

    Category: NG

    EN (SGP Price):
        It shows Weighted Average Price of matches in the relevant trading range in the Spot Natural Gas Market.

    TR (SGP Fiyatlar):
        Spot Doğal Gaz Piyasasında ilgili ticaret aralığında gerçekleşen eşleşmelerin Ağırlıklı Ortalama Fiyatını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/price/sgp-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-spot-prices", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_system_direction(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """System Balance / Sistem Yönü

    Category: NG

    EN (System Balance):
        It shows actual value compared to the Network Stock Gas Amount value targeted by the Transmission Company for the relevant day. It is valued as (+) if it is greater than (-) if it is less.

    TR (Sistem Yönü):
        İletim Şirketince ilgili gün için hedeflenen Şebeke Stok Gazı Miktarı değerine kıyasla, gerçekleşen değeri gösterir. Büyükse (+) , küçükse (-) değerlenir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/allocation-data/system-balance
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-system-direction", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_total_trade_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Total Trade Volume / SGP Toplam İşlem Hacmi

    Category: NG

    EN (SGP Total Trade Volume):
        It shows Total Amount of the matches in the daily and weekly contracts in the Spot Natural Gas Market.

    TR (SGP Toplam İşlem Hacmi):
        Spot Doğal Gaz Piyasasında günlük ve haftalık kontratlardaki eşleşmelerin Toplam Tutarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/trade-volume/sgp-total-trade-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-total-trade-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_transaction_history(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Transaction History / SGP İşlem Akışı

    Category: NG

    EN (SGP Transaction History):
        It shows Matching Times of spot contracts.

    TR (SGP İşlem Akışı):
        Spot kontratların Eşleşme Zamanlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/sgp-transaction-history
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-transaction-history", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_virtual_realization(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Virtual Realization / Sanal Gerçekleşme

    Category: NG

    EN (Virtual Realization):
        It shows Natural Gas Quantity that the Shippers add or remove from the virtual network points (UDN) through Purchase or Sale.

    TR (Sanal Gerçekleşme):
        Taşıtanların Alış veya Satış yoluyla, sanal şebeke noktalarından (UDN) sisteme eklediği veya çıkardığı Doğal Gaz Miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/allocation-data/virtual-realization
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-virtual-realization", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_weekly_matched_quantity(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Weekly Matched Quantity / SGP Haftalık Eşleşme Miktarı

    Category: NG

    EN (SGP Weekly Matched Quantity):
        It shows Total Amount of weekly contracts in the Spot Natural Gas Market.

    TR (SGP Haftalık Eşleşme Miktarı):
        Spot Doğal Gaz Piyasasında haftalık kontratlardaki eşleşmelerin Toplam Miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/matched-quantity/sgp-weekly-matched-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-weekly-matched-quantity", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_weekly_trade_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """SGP Weekly Trade Volume / SGP Haftalık İşlem Hacmi

    Category: NG

    EN (SGP Weekly Trade Volume):
        It shows Total Amount of weekly contracts in the Spot Natural Gas Market

    TR (SGP Haftalık İşlem Hacmi):
        Spot Doğal Gaz Piyasasında haftalık kontratlardaki eşleşmelerin Toplam Tutarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/trade-volume/sgp-weekly-trade-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-weekly-trade-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_wrp(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Weekly Reference Price (WRP) / Haftalık Referans Fiyatı (HRF)

    Category: NG

    EN (Weekly Reference Price (WRP)):
        It shows Weighted Average Price of weekly contract pairings in the Spot Natural Gas Market

    TR (Haftalık Referans Fiyatı (HRF)):
        Spot Doğal Gaz Piyasasında haftalık kontratlardaki eşleşmelerin Ağırlıklı Ortalama Fiyatını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/spot-gas-markets-sgp/price/weekly-reference-price-wrp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-wrp", start_date=start_date, end_date=end_date, **kwargs)

