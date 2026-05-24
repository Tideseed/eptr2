"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_dpp_bulk",
    "get_eak",
    "get_gen_org",
    "get_gen_uevcb",
    "get_kgup",
    "get_kgup_v1",
    "get_kudup",
    "get_lic_pp_list",
    "get_pp_list",
    "get_pp_list_for_date_range",
    "get_region_list",
    "get_rt_gen",
    "get_rt_gen_bulk",
    "get_uevcb_list_bulk",
    "get_uevm",
    "get_uevm_pp_list",
]

def get_dpp_bulk(date: str, uevcb_ids: list, region: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dpp-bulk", date=date, uevcb_ids=uevcb_ids, region=region, **kwargs)


def get_eak(start_date: str, end_date: str, region: str, org_id: str | int | None = None, uevcb_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Available Installed Capacity (AIC) / Emre Amade Kapasite (EAK)

    Category: Üretim Planlama

    EN (Available Installed Capacity (AIC)):
        Available Installed Capacity: The active power capacity that a generation unit can provide to the system.

    TR (Emre Amade Kapasite (EAK)):
        Emre Amade Kapasite: Bir üretim biriminin sisteme sağlayabileceği aktif güç kapasitesidir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/available-installed-capacity-aic
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("eak", start_date=start_date, end_date=end_date, region=region, org_id=org_id, uevcb_id=uevcb_id, **kwargs)


def get_gen_org(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Organization Listing / Organizasyon Listesi

    Category: Listeleme

    EN (Organization Listing):
        Organization Listing

    TR (Organizasyon Listesi):
        Tanımlı organizasyonların listesi

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/final-daily-production-program-fdpp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("gen-org", start_date=start_date, end_date=end_date, **kwargs)


def get_gen_uevcb(org_id: str | int, start_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Injection/Withdrawal Unit Listing / Uevçb Listeleme

    Category: Listeleme

    EN (Injection/Withdrawal Unit Listing):
        Injection/Withdrawal Unit list by the given organization id

    TR (Uevçb Listeleme):
        Verilen organizasyon idye ait UEVÇBlerin listesini döner

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/en/index.html#_uevcb-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("gen-uevcb", org_id=org_id, start_date=start_date, **kwargs)


def get_kgup(start_date: str, end_date: str, region: str, org_id: str | int | None = None, uevcb_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Final Daily Production Program (FDPP) / Kesinleşmiş Günlük Üretim Planı (KGÜP)

    Category: Üretim Planlama

    EN (Final Daily Production Program (FDPP)):
        Final day-ahead generation/consumption schedule (FDGS): The generation or consumption values which a settlement feed in-feed out unit anticipates to realize in the following day and notifies the System Operator at the opening of the balancing power market, depending on the obligations of the balancing responsible unit that it is a member of and the result of day-ahead balancing.

    TR (Kesinleşmiş Günlük Üretim Planı (KGÜP)):
        Kesinleşmiş Gün Öncesi Üretim Programı, katılımcının bir sonraki güne ilişkin gerçekleştirmeyi öngördüğü ve sistem işletmecisine dengeleme güç piyasasının başlangıcında bildirdiği üretim değeridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/final-daily-production-program-fdpp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("kgup", start_date=start_date, end_date=end_date, region=region, org_id=org_id, uevcb_id=uevcb_id, **kwargs)


def get_kgup_v1(start_date: str, end_date: str, region: str, org_id: str | int | None = None, uevcb_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Final Daily Production Program (FDPP) - First Version / Kesinleşmiş Günlük Üretim Planı (KGÜP) – İlk Versiyon

    Category: Üretim Planlama

    EN (Final Daily Production Program (FDPP) - First Version):
        Final day-ahead generation/consumption schedule (FDGS): The generation or consumption values which a settlement feed in-feed out unit anticipates to realize in the following day and notifies the System Operator at the opening of the balancing power market, depending on the obligations of the balancing responsible unit that it is a member of and the result of day-ahead balancing.

    TR (Kesinleşmiş Günlük Üretim Planı (KGÜP) – İlk Versiyon):
        Kesinleşmiş Gün Öncesi Üretim Programı, katılımcının bir sonraki güne ilişkin gerçekleştirmeyi öngördüğü ve sistem işletmecisine dengeleme güç piyasasının başlangıcında bildirdiği üretim değeridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/final-daily-production-program-fdpp-first-version
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("kgup-v1", start_date=start_date, end_date=end_date, region=region, org_id=org_id, uevcb_id=uevcb_id, **kwargs)


def get_kudup(start_date: str, end_date: str, region: str, org_id: str | int | None = None, uevcb_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Settlement Based Final Generation Plan (SBFGP) / Kesinleştirilmiş Uzlaştırma Dönemi Üretim Planı (KUDÜP)

    Category: Üretim Planlama

    EN (Settlement Based Final Generation Plan (SBFGP)):
        Final Settlement Period Generation Schedule: The generation schedules of power plants that have become unbalanced after the gate closure intraday market.

    TR (Kesinleştirilmiş Uzlaştırma Dönemi Üretim Planı (KUDÜP)):
        Gün öncesinde bildirilen UEVÇB bazında kaynaklara göre kesinleşmiş günlük üretim planlarının gün içi piyasasının kapanışından sonra DUY 69. madde kapsamında güncellenmesiyle oluşan kesinleşmiş günlük üretim planları.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/settlement-based-final-generation-plan-sbfgp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("kudup", start_date=start_date, end_date=end_date, region=region, org_id=org_id, uevcb_id=uevcb_id, **kwargs)


def get_lic_pp_list(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Licenced Power Plant Investments / Lisanslı Santral Yatırımları

    Category: Elektrik Üretim

    EN (Licenced Power Plant Investments):
        It is the monthly list of electricity generation facilities that are pre-approved and put into operation by the General Directorate of Energy Affairs.

    TR (Lisanslı Santral Yatırımları):
        Enerji İşleri Genel Müdürlüğü tarafından ön kabulü tamamlanmış ve devreye alınmış elektrik üretim tesislerinin aylık listesidir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/licenced-power-plant-investments
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("lic-pp-list", start_date=start_date, end_date=end_date, **kwargs)


def get_pp_list(eptr: EPTR2 | None = None, **kwargs):
    """Powerplant listing / Santral Listeleme

    Category: Listeleme

    EN (Powerplant listing):
        Powerplant listing

    TR (Santral Listeleme):
        Santral Listeleme

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/real-time-generation
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("pp-list", **kwargs)


def get_pp_list_for_date_range(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Powerplant listing (with Date Range) / Santral Listeleme (Tarih Aralığı ile)

    Category: Listeleme

    EN (Powerplant listing (with Date Range)):
        Powerplant listing (with Date Range)

    TR (Santral Listeleme (Tarih Aralığı ile)):
        Santral Listeleme (Tarih Aralığı ile)

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/real-time-generation
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("pp-list-for-date-range", start_date=start_date, end_date=end_date, **kwargs)


def get_region_list(eptr: EPTR2 | None = None, **kwargs):
    """Region Listing / Bölge Listesi

    Category: Listeleme

    EN (Region Listing):
        Region Listing

    TR (Bölge Listesi):
        Bölge listesi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_region-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("region-list", **kwargs)


def get_rt_gen(start_date: str, end_date: str, pp_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Real-Time Generation / Gerçek Zamanlı Üretim

    Category: Gerçekleşen Üretim

    EN (Real-Time Generation):
        Real time generation: The display of hourly generation values of electricity generation plants on a resource basis.

    TR (Gerçek Zamanlı Üretim):
        Elektrik üretiminin kaynak bazında saatlik gösterimidir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/real-time-generation
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("rt-gen", start_date=start_date, end_date=end_date, pp_id=pp_id, **kwargs)


def get_rt_gen_bulk(date: str, pp_ids: list, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("rt-gen-bulk", date=date, pp_ids=pp_ids, **kwargs)


def get_uevcb_list_bulk(start_date: str, org_ids: list, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("uevcb-list-bulk", start_date=start_date, org_ids=org_ids, **kwargs)


def get_uevm(start_date: str, end_date: str, pp_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Injection Quantity / Uzlaştırma Esas Veriş Miktarı (UEVM)

    Category: Üretim Planlama

    EN (Injection Quantity):
        Settlement Based Power Generation: The total value of the resource based electricity amount given to the system hourly by the settlement units within a settlement period.

    TR (Uzlaştırma Esas Veriş Miktarı (UEVM)):
        Uzlaştırmaya esas veriş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sisteme verdiği elektrik miktarının toplam değeridir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/injection-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("uevm", start_date=start_date, end_date=end_date, pp_id=pp_id, **kwargs)


def get_uevm_pp_list(eptr: EPTR2 | None = None, **kwargs):
    """Injection Quantity Powerplant Listing / Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi

    Category: Listeleme

    EN (Injection Quantity Powerplant Listing):
        Injection Quantity Powerplant Listing

    TR (Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi):
        Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/injection-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("uevm-pp-list", **kwargs)

