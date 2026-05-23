"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_date_init",
    "get_district_list",
    "get_market_participants",
    "get_market_participants_organization_list",
    "get_menu",
    "get_page_settings",
    "get_participant_count_based_upon_license_type",
    "get_province_list",
]

def get_date_init(eptr: EPTR2 | None = None, **kwargs):
    """Transparency Date Information / Şeffaflık Tarih Bilgisi

    Category: Genel

    EN (Transparency Date Information):
        Transparency Date Information

    TR (Şeffaflık Tarih Bilgisi):
        Şeffaflık Tarih Bilgisi

    Reference: https://seffaflik.epias.com.tr/electricity-service/technical/en/index.html#_date-init
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("date-init", **kwargs)


def get_district_list(province_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("district-list", province_id=province_id, **kwargs)


def get_market_participants(org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Market Participants / Piyasa Katılımcıları

    Category: Listeleme

    EN (Market Participants):
        It displays the participation status of market Participants in DAM, IDM, PFM, YEK-G markets. It also reports the activity status the participants.

    TR (Piyasa Katılımcıları):
        Piyasa Katılımcıları’nın GÖP, GİP, VEP, YEK-G piyasalarına katılım durumunu belirtir. Ayrıca Tüzel kişilik olarak firmanın aktiflik/pasiflik durumunu bildirir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/general-data/market-participants
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("market-participants", org_id=org_id, **kwargs)


def get_market_participants_organization_list(eptr: EPTR2 | None = None, **kwargs):
    """Market Participants Organization List / Piyasa Katılımcıları Organizasyon Listesi

    Category: Listeleme

    EN (Market Participants Organization List):
        Market Participants organization list.

    TR (Piyasa Katılımcıları Organizasyon Listesi):
        Piyasa Katılımcıları’nın organizasyon listesi.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/general-data/market-participants
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("market-participants-organization-list", **kwargs)


def get_menu(eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("menu", **kwargs)


def get_page_settings(menu_id: str | int, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("page-settings", menu_id=menu_id, **kwargs)


def get_participant_count_based_upon_license_type(start_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Participant Count Based Upon License Type / Lisans Türüne Göre Katılımcı Sayısı

    Category: Listeleme

    EN (Participant Count Based Upon License Type):
        It indicates the number of market participants by the licence types.

    TR (Lisans Türüne Göre Katılımcı Sayısı):
        Kamu ve Özel Sektör piyasa katılımcılarının Üretim, Tedarik, Dağıtım, OSB Üretim, İletim ve Görevli Tedaril lisansları türlerine göre toplam sayılarını gösterir. Görevli tedarik şirketleri tüketici grupları için K1 (21), K2 (21) ve K3 (21) olacak şekilde kategorize edilmiştir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/general-data/participant-count-based-upon-license-type
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("participant-count-based-upon-license-type", start_date=start_date, **kwargs)


def get_province_list(eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("province-list", **kwargs)

