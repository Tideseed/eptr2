"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_ra_distribution_list",
    "get_ra_meter_volumes_period",
    "get_ra_meter_volumes_version",
    "get_ra_meters",
    "get_ra_organization_list",
    "get_ra_spg_list",
    "get_ra_sum",
    "get_ra_vspg_list",
]

def get_ra_distribution_list(eptr: EPTR2 | None = None, **kwargs):
    """Retroactive Adjustment Distribution List / GDDK Dağıtım Liste Servisi

    Category: GDDK

    EN (Retroactive Adjustment Distribution List):
        Retroactive Adjustment Distribution List

    TR (GDDK Dağıtım Liste Servisi):
        GDDK Dağıtım Liste Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_distribution-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-distribution-list", **kwargs)


def get_ra_meter_volumes_period(mr_org_id: str | int, period_start_date: str, period_end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Meter Volumes Subject to Retroactive Adjustment Data (Mandatory Period Selection) / GDDK’ya Konu olan Sayaç Hacim Verileri (Zorunlu Period Seçimi)

    Category: GDDK

    EN (Meter Volumes Subject to Retroactive Adjustment Data (Mandatory Period Selection)):
        The item that is reflected on the invoice due to under- or over-invoicing of the relevant month’s consumption in the previous 12 months is called 'Retroactive Adjustment Item'. This data refers to the volume of meters associated with Retroactive Adjustment Item.

    TR (GDDK’ya Konu olan Sayaç Hacim Verileri (Zorunlu Period Seçimi)):
        Geçmiş 12 ay içindeki ilgili ayın tüketiminin eksik ya da fazla faturalandırılması nedeniyle faturaya yansıtılan kalem 'Geçmişe Dönük Düzeltme Kalemi' olarak adlandırılır. Bu veri GDDK ile ilişkilendirilen sayaçların hacim verilerini ifade eder.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_meter-volume-subject-to-retroactive-adjustment
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-meter-volumes-period", mr_org_id=mr_org_id, period_start_date=period_start_date, period_end_date=period_end_date, **kwargs)


def get_ra_meter_volumes_version(mr_org_id: str | int, version_start_date: str, version_end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Meter Volumes Subject to Retroactive Adjustment Data (Mandatory Version Selection) / GDDK’ya Konu olan Sayaç Hacim Verileri (Zorunlu Versiyon Seçimi)

    Category: GDDK

    EN (Meter Volumes Subject to Retroactive Adjustment Data (Mandatory Version Selection)):
        The item that is reflected on the invoice due to under- or over-invoicing of the relevant month’s consumption in the previous 12 months is called 'Retroactive Adjustment Item'. This data refers to the volume of meters associated with Retroactive Adjustment Item.

    TR (GDDK’ya Konu olan Sayaç Hacim Verileri (Zorunlu Versiyon Seçimi)):
        Geçmiş 12 ay içindeki ilgili ayın tüketiminin eksik ya da fazla faturalandırılması nedeniyle faturaya yansıtılan kalem 'Geçmişe Dönük Düzeltme Kalemi' olarak adlandırılır. Bu veri GDDK ile ilişkilendirilen sayaçların hacim verilerini ifade eder.

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_meter-volume-subject-to-retroactive-adjustment
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-meter-volumes-version", mr_org_id=mr_org_id, version_start_date=version_start_date, version_end_date=version_end_date, **kwargs)


def get_ra_meters(distribution_id: str | int, start_date: str, end_date: str, ra_spg_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Meter Count Subject To Retroactive Adjustment Data / GDDK’ya Konu olan Sayaç Sayısı

    Category: GDDK

    EN (Meter Count Subject To Retroactive Adjustment Data):
        The item that is reflected on the invoice due to under- or over-invoicing of the relevant month’s consumption in the previous 12 months is called 'Retroactive Adjustment Item'. This data refers to the number of meters associated with Retroactive Adjustment Item.

    TR (GDDK’ya Konu olan Sayaç Sayısı):
        Geçmiş 12 ay içindeki ilgili ayın tüketiminin eksik ya da fazla faturalandırılması nedeniyle faturaya yansıtalan kalem “Geçmişe Dönük Düzeltme Kalemi” olarak adlandırılır. Bu veri GDDK ile ilişkilendirilen sayaç sayısını ifade eder.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/retroactive-adjustment/meter-count-subject-to-retroactive-adjustment
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-meters", distribution_id=distribution_id, start_date=start_date, end_date=end_date, ra_spg_name=ra_spg_name, **kwargs)


def get_ra_organization_list(eptr: EPTR2 | None = None, **kwargs):
    """Meter Reading Organizations List / Sayaç Okuyan Kurum Liste Servisi

    Category: GDDK

    EN (Meter Reading Organizations List):
        Meter Reading Organizations List

    TR (Sayaç Okuyan Kurum Liste Servisi):
        Sayaç Okuyan Kurum Liste Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_gddk-organization-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-organization-list", **kwargs)


def get_ra_spg_list(eptr: EPTR2 | None = None, **kwargs):
    """GDDK Volume Customer Profile Group List / GDDK Profil Abone Grubu Liste Servisi

    Category: GDDK

    EN (GDDK Volume Customer Profile Group List):
        GDDK Volume Customer Profile Group List

    TR (GDDK Profil Abone Grubu Liste Servisi):
        GDDK Profil Abone Grubu Liste Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/en/index.html#_subscriber-profile-group-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-spg-list", **kwargs)


def get_ra_sum(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Retroactive Adjustment Sum / GDDK Tutarı

    Category: GDDK

    EN (Retroactive Adjustment Sum):
        The item that is reflected on the invoice due to under- or over-invoicing of the relevant month’s consumption in the previous 12 months is called 'Retroactive Adjustment Item'. This data refers to the financial amount associated with Retroactive Adjustment Item

    TR (GDDK Tutarı):
        Geçmiş 12 ay içindeki ilgili ayın tüketiminin eksik ya da fazla faturalandırılması nedeniyle faturaya yansıtılan kalem 'Geçmişe Dönük Düzeltme Kalemi' olarak adlandırılır. Bu veri GDDK ile ilişkilendirilen finansal tutarı ifade eder.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/retroactive-adjustment/retroactive-adjustment-sum
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-sum", start_date=start_date, end_date=end_date, **kwargs)


def get_ra_vspg_list(eptr: EPTR2 | None = None, **kwargs):
    """GDDK Volume Customer Profile Group List / GDDK Hacim Profil Abone Grubu Liste Servisi

    Category: GDDK

    EN (GDDK Volume Customer Profile Group List):
        GDDK Volume Customer Profile Group List

    TR (GDDK Hacim Profil Abone Grubu Liste Servisi):
        GDDK Hacim Profil Abone Grubu Liste Servisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/en/index.html#_volume-subscriber-profile-group-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ra-vspg-list", **kwargs)

