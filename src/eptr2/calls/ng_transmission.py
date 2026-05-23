"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_ng_tr_actual_entry_amount",
    "get_ng_tr_actual_exit_amount",
    "get_ng_tr_bilateral_transfer",
    "get_ng_tr_capacity_point",
    "get_ng_tr_daily_transmission",
    "get_ng_tr_day_ahead",
    "get_ng_tr_day_end",
    "get_ng_tr_entry_nomination",
    "get_ng_tr_exit_nomination",
    "get_ng_tr_max_entry_amount",
    "get_ng_tr_max_exit_amount",
    "get_ng_tr_reserved_entry_amount",
    "get_ng_tr_reserved_exit_amount",
    "get_ng_tr_stock_amount",
    "get_ng_tr_storage_facility_list",
]

def get_ng_tr_actual_entry_amount(start_date: str, end_date: str, point_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Entry Amount / Fiili Gerçekleşme Giriş Miktarı

    Category: NG

    EN (Entry Amount):
        It shows result of the Purchase transaction of the Shippers shows the actual amount of natural gas added to the system.

    TR (Fiili Gerçekleşme Giriş Miktarı):
        Taşıtanların Alış işlemi sonucu, sisteme eklenen fiili doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/actualization/entry-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-actual-entry-amount", start_date=start_date, end_date=end_date, point_id=point_id, **kwargs)


def get_ng_tr_actual_exit_amount(start_date: str, end_date: str, point_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Exit Amount / Fiili Gerçekleşme Çıkış Miktarı

    Category: NG

    EN (Exit Amount):
        It shows result of the Shipper's Sales transaction shows the actual amount of natural gas released from the system.

    TR (Fiili Gerçekleşme Çıkış Miktarı):
        Taşıtanların Satış işlemi sonucu, sistemden çıkan fiili doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/actualization/exit-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-actual-exit-amount", start_date=start_date, end_date=end_date, point_id=point_id, **kwargs)


def get_ng_tr_bilateral_transfer(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Transfer / Transfer

    Category: NG

    EN (Transfer):
        It shows Physical Point-based Bilateral agreement refers to the amount notification.

    TR (Transfer):
        Fiziki Nokta bazlı İkili anlaşma miktar bildirimini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/virtual-trade/transfer
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-bilateral-transfer", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_tr_capacity_point(start_date: str, end_date: str, point_type: str, eptr: EPTR2 | None = None, **kwargs):
    """Capacity Point Service / Kapasite Nokta Servisi

    Category: NG

    EN (Capacity Point Service):
        Capacity point listing service.

    TR (Kapasite Nokta Servisi):
        Kapasite noktalarını listeleyen servis.

    Reference: https://seffaflik.epias.com.tr/natural-gas-service/technical/tr/index.html#_capacity-point
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-capacity-point", start_date=start_date, end_date=end_date, point_type=point_type, **kwargs)


def get_ng_tr_daily_transmission(start_date: str, end_date: str, storage_facility_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Daily Actualization Amount / Günlük Gerçekleşme Miktarı

    Category: NG

    EN (Daily Actualization Amount):
        It shows amount of natural gas transferred from the network to the natural gas storage facilities.

    TR (Günlük Gerçekleşme Miktarı):
        Şebekeden doğal gaz depolama tesislerine aktarılan doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/storage/daily-actualization-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-daily-transmission", start_date=start_date, end_date=end_date, storage_facility_id=storage_facility_id, **kwargs)


def get_ng_tr_day_ahead(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Day Ahead (UDN) / Gün Öncesi (UDN)

    Category: NG

    EN (Day Ahead (UDN)):
        It shows Bilateral agreement refers to the statement of quantity.

    TR (Gün Öncesi (UDN)):
        İkili anlaşma miktar bildirimini ifade eder

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/virtual-trade/day-ahead-udn
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-day-ahead", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_tr_day_end(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Day End (UDN) / Gün Sonu (UDN)

    Category: NG

    EN (Day End (UDN)):
        Day End (UDN)

    TR (Gün Sonu (UDN)):
        Gün Sonu (UDN)

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/virtual-trade/day-end-udn
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-day-end", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_tr_entry_nomination(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Entry Nomination / Taşıma Giriş Miktarı Bildirimi (TMB)

    Category: NG

    EN (Entry Nomination):
        It shows physical point based entry quantity notification

    TR (Taşıma Giriş Miktarı Bildirimi (TMB)):
        Fiziki Nokta bazlı giriş miktar bildirimini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/transport-nomination-tn/entry-nomination
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-entry-nomination", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_tr_exit_nomination(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Exit Nomination / Taşıma Çıkış Miktarı Bildirimi (TMB)

    Category: NG

    EN (Exit Nomination):
        It shows Physical Point-based output quantity notification

    TR (Taşıma Çıkış Miktarı Bildirimi (TMB)):
        Fiziki Nokta bazlı çıkış miktar bildirimini ifade eder.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/transport-nomination-tn/exit-nomination
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-exit-nomination", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_tr_max_entry_amount(start_date: str, end_date: str, point_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Max Entry Amount / Maks Giriş Kapasite Miktarı

    Category: NG

    EN (Max Entry Amount):
        It shows amount of natural gas expected to be added to the transmission network according to the Transmission Company capacity plan.

    TR (Maks Giriş Kapasite Miktarı):
        İletim Şirketi kapasite planına göre iletim şebekesine eklenmesi beklenen doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/capacity/max-entry-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-max-entry-amount", start_date=start_date, end_date=end_date, point_id=point_id, **kwargs)


def get_ng_tr_max_exit_amount(start_date: str, end_date: str, point_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Max Exit Amount / Maks Çıkış Kapasite Miktarı

    Category: NG

    EN (Max Exit Amount):
        It shows amount of natural gas expected to come out of the transmission network according to the Transmission Company capacity plan.

    TR (Maks Çıkış Kapasite Miktarı):
        İletim Şirketi kapasite planına göre iletim şebekesinden çıkması beklenen doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/capacity/max-exit-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-max-exit-amount", start_date=start_date, end_date=end_date, point_id=point_id, **kwargs)


def get_ng_tr_reserved_entry_amount(start_date: str, end_date: str, point_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Reserved Entry Amount / Rezerve Giriş Kapasite Miktarı

    Category: NG

    EN (Reserved Entry Amount):
        It shows amount of natural gas expected to be added to the transmission network according to the Transmission Company reservation program.

    TR (Rezerve Giriş Kapasite Miktarı):
        İletim Şirketi rezervasyon programına göre iletim şebekesine eklenmesi beklenen doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/reserve/entry-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-reserved-entry-amount", start_date=start_date, end_date=end_date, point_id=point_id, **kwargs)


def get_ng_tr_reserved_exit_amount(start_date: str, end_date: str, point_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Reserved Exit Amount / Rezerve Çıkış Kapasite Miktarı

    Category: NG

    EN (Reserved Exit Amount):
        It shows amount of natural gas expected to come out of the transmission network according to the Transmission Company reservation program.

    TR (Rezerve Çıkış Kapasite Miktarı):
        İletim Şirketi rezervasyon programına göre iletim şebekesinden çıkması beklenen doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/reserve/exit-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-reserved-exit-amount", start_date=start_date, end_date=end_date, point_id=point_id, **kwargs)


def get_ng_tr_stock_amount(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Stock Amount / Stok Miktarı

    Category: NG

    EN (Stock Amount):
        It shows daily amount of natural gas trapped in the Transmission Network.

    TR (Stok Miktarı):
        İletim Şebekesinde sıkışmış durumdaki günlük doğal gaz miktarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-transmission/stock-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-stock-amount", start_date=start_date, end_date=end_date, **kwargs)


def get_ng_tr_storage_facility_list(eptr: EPTR2 | None = None, **kwargs):
    """Storage Facility Service / Depolama Tesisi Listeleme Servisi

    Category: NG

    EN (Storage Facility Service):
        Storage Facility Service

    TR (Depolama Tesisi Listeleme Servisi):
        Depolama Tesisi Listeleme Servisi

    Reference: https://seffaflik.epias.com.tr/natural-gas-service/technical/tr/index.html#_storage-facility
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-tr-storage-facility-list", **kwargs)

