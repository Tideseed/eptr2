"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_consumer_breakdown",
    "get_consumption_breakdown",
    "get_distribution_region_list",
    "get_elig_profile_groups",
    "get_eligible_consumer_count",
    "get_eligible_consumer_count_detail",
    "get_eligible_consumer_quantity",
    "get_get_distribution_companies",
    "get_load_plan",
    "get_long_term_demand_forecast",
    "get_main_tariff_group_list",
    "get_mf_distribution",
    "get_mf_meter_reading_type",
    "get_mf_profile_group",
    "get_monthly_index",
    "get_multiple_factor",
    "get_percentage_consumption_info",
    "get_planned_outages",
    "get_profile_group_list",
    "get_rt_cons",
    "get_st_uecm",
    "get_su_uecm",
    "get_uecm",
    "get_unplanned_outages",
]

def get_consumer_breakdown(period: str, province_id: str | int | None = None, profile_group_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("consumer-breakdown", period=period, province_id=province_id, profile_group_id=profile_group_id, **kwargs)


def get_consumption_breakdown(period: str, province_id: str | int | None = None, profile_group_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("consumption-breakdown", period=period, province_id=province_id, profile_group_id=profile_group_id, **kwargs)


def get_distribution_region_list(eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("distribution-region-list", **kwargs)


def get_elig_profile_groups(period: str, district_name: str | None = None, province_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """City, District EC Listing - Customer Profile Group Service / İl, İlçe ST Listeleme - Profil Abone Grubu Listeleme Servisi

    Category: Servis

    EN (City, District EC Listing - Customer Profile Group Service):
        City, District EC Listing - Customer Profile Group Service

    TR (İl, İlçe ST Listeleme - Profil Abone Grubu Listeleme Servisi):
        İl ilçe st adedi sayfası için profil abone grubu listesi döner

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_profile-subscription-group-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("elig-profile-groups", period=period, district_name=district_name, province_id=province_id, **kwargs)


def get_eligible_consumer_count(start_date: str, end_date: str, district_name: str | None = None, pg_name: str | None = None, province_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Eligible Customer Count / Serbest Tüketici Adedi

    Category: Serbest Tüketici

    EN (Eligible Customer Count):
        The number of meters with eligible costumer usage type

    TR (Serbest Tüketici Adedi):
        Sayaç kullanım tipi serbest tüketici olan sayaçların sayısıdır

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/eligible-consumer/eligible-customer-count
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eligible-consumer-count", start_date=start_date, end_date=end_date, district_name=district_name, pg_name=pg_name, province_id=province_id, **kwargs)


def get_eligible_consumer_count_detail(period: str, eptr: EPTR2 | None = None, **kwargs):
    """City, District Eligible Customer Number / İl, İlçe ST Adedi

    Category: Serbest Tüketici

    EN (City, District Eligible Customer Number):
        The number of meters with eligible costumer usage type based on district and profile subscriber group

    TR (İl, İlçe ST Adedi):
        Sayaç kullanım tipi serbest tüketici olan sayaçların ilçe ve profil abone grubu bazındaki sayısıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/eligible-consumer/city-district-eligible-customer-number
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eligible-consumer-count-detail", period=period, **kwargs)


def get_eligible_consumer_quantity(eptr: EPTR2 | None = None, **kwargs):
    """Eligible Customer Quantity / Serbest Tüketici Tüketim Miktarı

    Category: Serbest Tüketici

    EN (Eligible Customer Quantity):
        The number of meters with eligible costumer usage type based on district and profile subscriber group

    TR (Serbest Tüketici Tüketim Miktarı):
        Sayaç kullanım tipi serbest tüketici olan sayaçların uzlaştırmaya esas çekiş miktarı toplamıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/eligible-consumer/eligible-customer-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eligible-consumer-quantity", **kwargs)


def get_get_distribution_companies(eptr: EPTR2 | None = None, **kwargs):
    """Distribution Company Listing Service / Dağıtım Şirketlerinin Alındığı Servis

    Category: Servis

    EN (Distribution Company Listing Service):
        Distribution Company Listing Service

    TR (Dağıtım Şirketlerinin Alındığı Servis):
        Dağıtım Şirketlerinin Alındığı Servis

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_distribution-company-data
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("get-distribution-companies", **kwargs)


def get_load_plan(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Load Forecast Plan / Yük Tahmin Planı

    Category: Tüketim Tahmin

    EN (Load Forecast Plan):
        Total hourly power consumption forecast plans for the next day.

    TR (Yük Tahmin Planı):
        Bir sonraki gün için yapılan saatlik talep miktarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/forecast/load-forecast-plan
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("load-plan", start_date=start_date, end_date=end_date, **kwargs)


def get_long_term_demand_forecast(dist_org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Demand Forecast / Talep Tahmini

    Category: Talep Tahmini

    EN (Demand Forecast):
        These are the annual gross estimated values of consumers between 2018 and 2027 belonging to the distribution company in the relevant distribution region.

    TR (Talep Tahmini):
        İlgili dağıtım bölgesinde dağıtım şirketine ait 2018-2027 arası tüketicilerin yıllık brüt tahmin değerleridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/forecast/demand-forecast
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("long-term-demand-forecast", dist_org_id=dist_org_id, **kwargs)


def get_main_tariff_group_list(eptr: EPTR2 | None = None, **kwargs):
    """Main Tariff Group / Ana Tarife Grubu

    Category: Servis

    EN (Main Tariff Group):
        Main Tariff Group Service

    TR (Ana Tarife Grubu):
        Ana Tarife gruplarını dönen servis

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_main-tariff-group-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("main-tariff-group-list", **kwargs)


def get_mf_distribution(period: str, eptr: EPTR2 | None = None, **kwargs):
    """Multiple Factor - Distribution Companies Listing Service / Çarpan Değeri - Dağıtım Firmaları Listeleme Servisi

    Category: Servis

    EN (Multiple Factor - Distribution Companies Listing Service):
        Multiple Factor - Distribution Companies Listing Service

    TR (Çarpan Değeri - Dağıtım Firmaları Listeleme Servisi):
        Çarpan Değeri - Dağıtım Firmaları Listeleme Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_multiple-factor-distribution
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mf-distribution", period=period, **kwargs)


def get_mf_meter_reading_type(eptr: EPTR2 | None = None, **kwargs):
    """Multiple Factor - Meter Reading Type Listing Service / Çarpan Değeri - Sayaç Okuma Tipi Listeleme Servisi

    Category: Servis

    EN (Multiple Factor - Meter Reading Type Listing Service):
        Multiple Factor - Meter Reading Type Listing Service

    TR (Çarpan Değeri - Sayaç Okuma Tipi Listeleme Servisi):
        Çarpan Değeri - Sayaç Okuma Tipi Listeleme Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_multiple-factor-meter-reading-type
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mf-meter-reading-type", **kwargs)


def get_mf_profile_group(period: str, distribution_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    """Multiple Factor - Profile Subscriber Group Listing Service / Çarpan Değeri - Profil Abone Grubu Listeleme Servisi

    Category: Servis

    EN (Multiple Factor - Profile Subscriber Group Listing Service):
        If the distributionId field is provided, it will list the valid Profile Group according to the distribution company/organization ID information for the relevant period, if left empty, it will list all Profile Group.

    TR (Çarpan Değeri - Profil Abone Grubu Listeleme Servisi):
        Profil Abone Grubu Listeleme Servisi,distributionId alanı verilirse verilen dönemdeki ilgili dağıtım firma/organizasyon id bilgisine göre ilgili dönemdeki geçerli abone grupları,boş gönderilirse tüm abone grupları listelenmektedir.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_multiple-factor-profile-group
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mf-profile-group", period=period, distribution_id=distribution_id, **kwargs)


def get_monthly_index(start_date: str, end_date: str, tariff_group_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    """Monthly Index / Aylık Endeks

    Category: Tedarik Fiyat Endeksi

    EN (Monthly Index):
        The data set regarding the value calculated by using Market Clearing Price (MCP), Negative System Imbalance Price, Renewable Energy Support Mechanism Unit Cost, National Tariff Unit Cost, Withdrawal Quantities on the basis of settlement period for customers registered in the Market Management System.

    TR (Aylık Endeks):
        Piyasa Takas Fiyatı (PTF), Negatif Sistem Dengesizlik Fiyatı, YEKDEM Birim Fiyat, Ulusal Tarife Birim Fiyatları ve Piyasa Yönetim Sistemine kayıtlı tüketicilere ait uzlaştırma dönemi bazındaki çekiş miktarları kullanılarak hesaplanan değere ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/supply-price-index/monthly-index
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("monthly-index", start_date=start_date, end_date=end_date, tariff_group_id=tariff_group_id, **kwargs)


def get_multiple_factor(period: str, mr_type: str, distribution_id: str | int, subscriber_pg: str, eptr: EPTR2 | None = None, **kwargs):
    """Multiple Factor / Çarpan Değeri

    Category: Profil Katsaıları

    EN (Multiple Factor):
        The data set regarding the value used for profiling of meters that cannot be read on a settlement period basis.

    TR (Çarpan Değeri):
        Uzlaştırma dönemi bazında ölçüm yapılamayan sayaçlar için uygulanan profilleme işleminde kullanılan değerlere ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/profile-coefficients/multiple-factor
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("multiple-factor", period=period, mr_type=mr_type, distribution_id=distribution_id, subscriber_pg=subscriber_pg, **kwargs)


def get_percentage_consumption_info(period: str, province_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    """Percentage of Consumption Information / Yüzdesel Tüketim Bilgileri

    Category: Gerçekleşen Tüketim

    EN (Percentage of Consumption Information):
        The data set regarding the percentage of actual consumption by city and customer profile group.

    TR (Yüzdesel Tüketim Bilgileri):
        Fiili tüketimin il bazında ve profil abone grubu bazında yüzdesel kırılımına ilişkin veri seti.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/percentage-of-consumption-information
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("percentage-consumption-info", period=period, province_id=province_id, **kwargs)


def get_planned_outages(period: str, province_id: str | int | None = None, dist_company_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Planned Failure Information / Planlı Kesinti Bilgisi

    Category: Kesinti Bilgisi

    EN (Planned Failure Information):
        This is the screen where information about the planned outage is presented.

    TR (Planlı Kesinti Bilgisi):
        Yapılması planlanan kesinti bilgilerinin sunulduğu ekrandır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/failure-information/planned-failure-information
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("planned-outages", period=period, province_id=province_id, dist_company_id=dist_company_id, **kwargs)


def get_profile_group_list(eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("profile-group-list", **kwargs)


def get_rt_cons(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Real Time Consumption / Gerçek Zamanlı Tüketim

    Category: Gerçekleşen Tüketim

    EN (Real Time Consumption):
        It is the data that shows the instantaneous consumption value on an hourly basis.

    TR (Gerçek Zamanlı Tüketim):
        Anlık olarak gerçekleşen tüketim değerinin saatlik bazda gösterildiği veridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/real-time-consumption
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("rt-cons", start_date=start_date, end_date=end_date, **kwargs)


def get_st_uecm(period: str, eptr: EPTR2 | None = None, **kwargs):
    """Eligible Customer Withdrawal Quantity / Serbest Tüketici Uzlaştırmaya Esas Çekiş Miktarı

    Category: Gerçekleşen Tüketim

    EN (Eligible Customer Withdrawal Quantity):
        The data set regarding total hourly energy withdrawal quantity of eligible customers

    TR (Serbest Tüketici Uzlaştırmaya Esas Çekiş Miktarı):
        Serbest tüketici hakkını kullananların, bir uzlaştırma dönemi içinde saatlik olarak sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/eligible-customer-withdrawal-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("st-uecm", period=period, **kwargs)


def get_su_uecm(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Withdrawal Quantity Under Supply Liability / Tedarik Yükümlülüğü Kapsamındaki Uzlaştırmaya Esas Çekiş Miktarı (UEÇM)

    Category: Gerçekleşen Tüketim

    EN (Withdrawal Quantity Under Supply Liability):
        The data set regarding total energy withdrawal quantity under supply liability of withdrawal units.

    TR (Tedarik Yükümlülüğü Kapsamındaki Uzlaştırmaya Esas Çekiş Miktarı (UEÇM)):
        Uzlaştırmaya esas çekiş birimlerinin, tedarik yükümlülüğü kapsamında sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/withdrawal-quantity-under-supply-liability
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("su-uecm", start_date=start_date, end_date=end_date, **kwargs)


def get_uecm(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Withdrawal Quantity / Uzlaştırmaya Esas Çekiş Miktarı (UEÇM)

    Category: Gerçekleşen Tüketim

    EN (Withdrawal Quantity):
        The data set regarding total hourly energy withdrawal quantity of withdrawal units

    TR (Uzlaştırmaya Esas Çekiş Miktarı (UEÇM)):
        Uzlaştırmaya esas çekiş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/withdrawal-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("uecm", start_date=start_date, end_date=end_date, **kwargs)


def get_unplanned_outages(period: str, province_id: str | int | None = None, dist_company_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Unplanned Failure Information / Plansız Kesinti Bilgisi

    Category: Kesinti Bilgisi

    EN (Unplanned Failure Information):
        This is the screen where unplanned outage are presented.

    TR (Plansız Kesinti Bilgisi):
        Plansız kesintilerin sunulduğu ekrandır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-consumption/failure-information/unplanned-failure-information
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("unplanned-outages", period=period, province_id=province_id, dist_company_id=dist_company_id, **kwargs)

