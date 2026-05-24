"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_capacity_demand",
    "get_congestion_cost",
    "get_eic_w_org_list",
    "get_eic_w_uevcb_list",
    "get_eic_x_org_list",
    "get_international_line_events",
    "get_intl_capacity_demand_direction_list",
    "get_intl_direction_list",
    "get_iskk",
    "get_line_capacities",
    "get_nominal_capacity",
    "get_tcat_pre_month_forecast",
    "get_tcat_pre_year_forecast",
    "get_zero_balance",
]

def get_capacity_demand(start_date: str, end_date: str, intl_direction: str, eptr: EPTR2 | None = None, **kwargs):
    """Interconnection Line - Capacity Requests / Kapasite Talepleri

    Category: İletim

    EN (Interconnection Line - Capacity Requests):
        Shows the requests for capacity auctions and allocated capacities.

    TR (Kapasite Talepleri):
        Kapasite ihalelerine ait talepleri ve tahsis edilen kapasiteleri gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacity-requests
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("capacity-demand", start_date=start_date, end_date=end_date, intl_direction=intl_direction, **kwargs)


def get_congestion_cost(start_date: str, end_date: str, price_type: str, order_type: str, eptr: EPTR2 | None = None, **kwargs):
    """Congestion Cost / Kısıt Maliyeti

    Category: İletim

    EN (Congestion Cost):
        The data set regarding the total congestion cost of up and down regulation instructions with code 1.

    TR (Kısıt Maliyeti):
        Şehir bazında 1 kodlu Yük Alma ve Yük Atma Talimatlarının toplam mali değerine ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/congestion/congestion-cost
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("congestion-cost", start_date=start_date, end_date=end_date, price_type=price_type, order_type=order_type, **kwargs)


def get_eic_w_org_list(period: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """ENTSO-E (W) Codes / ENTSO-E (W) Kodları

    Category: İletim

    EN (ENTSO-E (W) Codes):
        The EIC code of type W is used to identify objects to be used for production, consumption or storage of energy.

    TR (ENTSO-E (W) Kodları):
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağının piyasadaki Santral ve UEVÇBlere, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodudur.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/general-data/entso-e-w-codes
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eic-w-org-list", period=period, org_id=org_id, **kwargs)


def get_eic_w_uevcb_list(uevcb_name: str, period: str, province_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """ENTSO-E (W) Codes UEVCB / ENTSO-E (W) Kodları UEVÇB

    Category: İletim

    EN (ENTSO-E (W) Codes UEVCB):
        The EIC code of type W is used to identify objects to be used for production, consumption or storage of energy.

    TR (ENTSO-E (W) Kodları UEVÇB):
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağının piyasadaki Santral ve UEVÇBlere, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodudur.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/general-data/entso-e-w-codes
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eic-w-uevcb-list", uevcb_name=uevcb_name, period=period, province_id=province_id, **kwargs)


def get_eic_x_org_list(period: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """ENTSO-E (X) Codes / ENTSO-E (X) Kodları

    Category: İletim

    EN (ENTSO-E (X) Codes):
        It is the Energy Identification Code defined by the European Network of Electricity Transmission System Operators to the organizations in the market in a format in accordance with European standards.

    TR (ENTSO-E (X) Kodları):
        Avrupa Elektrik İletim Sistemi İşletmecileri Ağı’nın piyasadaki organizasyonlara, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodudur.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/general-data/entso-e-x-codes
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eic-x-org-list", period=period, org_id=org_id, **kwargs)


def get_international_line_events(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Interconnection Failure and Maintenance Notices / Enterkonneksiyon Arıza Bakım Bildirimleri

    Category: İletim

    EN (Interconnection Failure and Maintenance Notices):
        This is the page for information on international lines obtained from TCAT.

    TR (Enterkonneksiyon Arıza Bakım Bildirimleri):
        TCAT'ten temin edilen uluslararası hatlarda oluşan kesinti bilgileri sayfasıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-failure-and-maintenance-notices
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("international-line-events", start_date=start_date, end_date=end_date, **kwargs)


def get_intl_capacity_demand_direction_list(eptr: EPTR2 | None = None, **kwargs):
    """Capacity Requests Direction Listing / Kapasite Talepleri Yön Listesi

    Category: İletim

    EN (Capacity Requests Direction Listing):
        Capacity Requests Direction Listing

    TR (Kapasite Talepleri Yön Listesi):
        Kapasite Talepleri Yön Listesi

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacity-requests
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("intl-capacity-demand-direction-list", **kwargs)


def get_intl_direction_list(eptr: EPTR2 | None = None, **kwargs):
    """Interconnection Line Capacities Direction Listing / Hat Kapasiteleri Yön Listesi

    Category: İletim

    EN (Interconnection Line Capacities Direction Listing):
        Interconnection Line Capacities Direction Listing

    TR (Hat Kapasiteleri Yön Listesi):
        Hat Kapasiteleri Yön Listesi

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacities
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("intl-direction-list", **kwargs)


def get_iskk(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Transmission Loss Factor / İletim Sistemi Kayıp Katsayısı (ISKK)

    Category: İletim

    EN (Transmission Loss Factor):
        The data set regarding the ratio of difference between injection to the system and withdrawal from the system, to injection to the system.

    TR (İletim Sistemi Kayıp Katsayısı (ISKK)):
        Uzlaştırma dönemi bazında iletim sistemi veriş ve çekiş miktarları arasındaki farkın veriş miktarına oranlanmasıyla hesaplanan iletim sistemi kayıp katsayısına ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/congestion/transmission-loss-factor
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("iskk", start_date=start_date, end_date=end_date, **kwargs)


def get_line_capacities(start_date: str, end_date: str, intl_direction: str, eptr: EPTR2 | None = None, **kwargs):
    """Interconnection Line Capacities / Hat Kapasiteleri

    Category: İletim

    EN (Interconnection Line Capacities):
        Total Capacity and Available Capacity values are shown on the page.

    TR (Hat Kapasiteleri):
        Enterkonneksiyonlara ait hat toplam kapasite ve Kullanıma açık kapasite değerleri gösterilmektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacities
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("line-capacities", start_date=start_date, end_date=end_date, intl_direction=intl_direction, **kwargs)


def get_nominal_capacity(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Nomine Capacity / Nomine Kapasite

    Category: İletim

    EN (Nomine Capacity):
        Nomine Capacity values show the bilateral agreements made for import (sales quantities) and exports (purchased quantities).

    TR (Nomine Kapasite):
        Nomine Kapasite değerleri ithalat (satış miktarları) ve ihracat(alış miktarı) için yapılan ikili anlaşmaları göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/nomine-capacity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("nominal-capacity", start_date=start_date, end_date=end_date, **kwargs)


def get_tcat_pre_month_forecast(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Monthly Forecasts for Interconnection Capacity / Enterkonneksiyon Kapasitesine İlişkin Ay Öncesi Tahminler

    Category: İletim

    EN (Monthly Forecasts for Interconnection Capacity):
        The data set regarding the pre-month forecasts of Net Transfer Capacity, Available Capacity and Allocated Capacity values according to transfer directions.

    TR (Enterkonneksiyon Kapasitesine İlişkin Ay Öncesi Tahminler):
        Transfer yönü kapsamında ay öncesi Net Transfer Kapasitesi, Kullanıma Açık Kapasite ve Tahsis Edilmiş Kapasite değerlerinin yıl öncesi tahminlerine ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/forecasts-for-interconnection-capacity/monthly-forecasts-for-interconnection-capacity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("tcat-pre-month-forecast", start_date=start_date, end_date=end_date, **kwargs)


def get_tcat_pre_year_forecast(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Yearly Forecasts for Interconnection Capacity / Enterkonneksiyon Kapasitesine İlişkin Yıl Öncesi Tahminler

    Category: İletim

    EN (Yearly Forecasts for Interconnection Capacity):
        The data set regarding the pre-year forecasts of Net Transfer Capacity, Available Capacity and Allocated Capacity values according to transfer directions.

    TR (Enterkonneksiyon Kapasitesine İlişkin Yıl Öncesi Tahminler):
        Transfer yönü kapsamında yıl öncesi Net Transfer Kapasitesi, Kullanıma Açık Kapasite ve Tahsis Edilmiş Kapasite değerlerinin yıl öncesi tahminlerine ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/forecasts-for-interconnection-capacity/yearly-forecasts-for-interconnection-capacity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("tcat-pre-year-forecast", start_date=start_date, end_date=end_date, **kwargs)


def get_zero_balance(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Monthly Zero Balance Adjustment / Sıfır Bakiye Düzeltme Tutarı Aylık

    Category: İletim

    EN (Monthly Zero Balance Adjustment):
        The data set regarding montly amounts of zero balance adjustment and its components.

    TR (Sıfır Bakiye Düzeltme Tutarı Aylık):
        Sıfır bakiye düzeltme tutarı ve bileşenlerine ait aylık tutarlara ilişkin veri seti

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-transmission/zero-balance-adjustment/monthly-zero-balance-adjustment
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("zero-balance", start_date=start_date, end_date=end_date, **kwargs)

