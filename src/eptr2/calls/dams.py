"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_basin_list",
    "get_dam_list",
    "get_dams_active_fullness",
    "get_dams_active_volume",
    "get_dams_daily_level",
    "get_dams_daily_volume",
    "get_dams_info",
    "get_dams_level_minmax",
    "get_dams_volume_minmax",
    "get_dams_water_energy_provision",
]

def get_basin_list(eptr: EPTR2 | None = None, **kwargs):
    """Basin List / Havza Listesi

    Category: Barajlar

    EN (Basin List):
        Returns the list of basins.

    TR (Havza Listesi):
        Havzaların listesini döner.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/daily-kot
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("basin-list", **kwargs)


def get_dam_list(basin_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Dam List / Baraj Listesi

    Category: Barajlar

    EN (Dam List):
        Returns the list of dams.

    TR (Baraj Listesi):
        Barajların listesini döner.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/daily-kot
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-list", basin_name=basin_name, **kwargs)


def get_dams_active_fullness(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Active Fullness / Aktif Doluluk

    Category: Barajlar

    EN (Active Fullness):
        The percentage of volume between the maximum and minimum operating levels of a dam. Formula: Active Occupancy= [( Volume Corresponding to the Level on the Relevant Date - Minimum Volume ) / ( Maximum Volume - Minimum Volume )] *100. Data is finalized as of 17:00.

    TR (Aktif Doluluk):
        Bir barajın maksimum ve minimum işletme seviyeleri arasındaki hacimin yüzdesidir. Formül: Aktif Doluluk= [( İlgili Tarihteki Seviyeye Karşılık Gelen Hacim – Minimum Hacim ) / ( Maksimum Hacim – Minimum Hacim )] * 100. Veriler saat 17:00 itibariyle nihai halini almaktadır.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/active-fullness
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-active-fullness", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_active_volume(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Active Volume / Aktif Hacim

    Category: Barajlar

    EN (Active Volume):
        The volume between the minimum volume and minimum operating levels of a dam at the relevant date. Data is finalized at 17:00.

    TR (Aktif Hacim):
        Bir barajın ilgili tarihteki seviyeye karşılık gelen hacmi ve minimum işletme seviyeleri arasındaki hacimdir. Veriler saat 17:00 itibariyle nihai halini almaktadır.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/active-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-active-volume", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_daily_level(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Daily Kot / Günlük Kot

    Category: Barajlar

    EN (Daily Kot):
        Indicates the water height of the dam on the relevant day. The data is finalized as of 5 pm.

    TR (Günlük Kot):
        Barajın ilgili gündeki su yüksekliğini belirtir. Veriler saat 17:00 itibariyle nihai halini almaktadır.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/daily-kot
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-daily-level", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_daily_volume(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Daily Volume / Günlük Hacim

    Category: Barajlar

    EN (Daily Volume):
        The volume corresponding to the level of a dam at the relevant date. Data is finalized at 17:00.

    TR (Günlük Hacim):
        Bir barajın ilgili tarihteki seviyesine karşılık gelen hacimdir. Veriler saat 17:00 itibariyle nihai halini almaktadır.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/daily-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-daily-volume", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_info(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Flow Rate and Installed Power / Debi ve Kurulu Güç

    Category: Barajlar

    EN (Flow Rate and Installed Power):
        It shows the amount of water passing through the unit in the relevant dam and the installed power of the dam.

    TR (Debi ve Kurulu Güç):
        İlgili barajda üniteden geçen suyun miktarını ve barajın kurulu gücünü gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/dam-info/volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-info", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_level_minmax(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Kot / Kot

    Category: Barajlar

    EN (Kot):
        Indicates the minimum and maximum water level of the dam.

    TR (Kot):
        İlgili barajın maximum ve minumum seviyesini gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/dam-info/kot
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-level-minmax", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_volume_minmax(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Volume / Hacim

    Category: Barajlar

    EN (Volume):
        It shows the maximum and minimum volume level of the relevant dam.

    TR (Hacim):
        İlgili barajın maksimum ve minumum hacim seviyesini gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/dam-info/volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-volume-minmax", basin_name=basin_name, dam_name=dam_name, **kwargs)


def get_dams_water_energy_provision(basin_name: str | None = None, dam_name: str | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Water Energy Provision / Suyun Enerji Karşılığı

    Category: Barajlar

    EN (Water Energy Provision):
        The energy equivalent of Mwh in the dam. Data is finalized at 17:00.

    TR (Suyun Enerji Karşılığı):
        Barajda yer alan suyun hesaplanan MWh cinsinden enerji karşılığıdır. Veriler saat 17:00 itibariyle nihai halini almaktadır.

    Reference: https://seffaflik.epias.com.tr/electricity/dams/water-energy-provision
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dams-water-energy-provision", basin_name=basin_name, dam_name=dam_name, **kwargs)

