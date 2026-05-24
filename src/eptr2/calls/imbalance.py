"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_imb_org_list",
    "get_imb_qty",
    "get_imb_qty_g",
    "get_imb_vol",
]

def get_imb_org_list(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DSG Organization List / DSG Organizasyon Listesi

    Category: Dengesizlik

    EN (DSG Organization List):
        Organization List used on Balance Responsible Group Imbalance Quantity

    TR (DSG Organizasyon Listesi):
        Dengeden Sorumlu Grup servisinde kullanılan Organizasyon Listesi

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/balance-responsible-group-imbalance-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("imb-org-list", start_date=start_date, end_date=end_date, **kwargs)


def get_imb_qty(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Imbalance Quantity / Dengesizlik Miktarı

    Category: Dengesizlik

    EN (Imbalance Quantity):
        It is the amount that indicates how much the market participants deviate from the production/consumption values realized as a result of the Day-ahead Market, Intraday Market, Balancing Power Market and Bilateral Agreement transactions.

    TR (Dengesizlik Miktarı):
        Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/imbalance-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("imb-qty", start_date=start_date, end_date=end_date, **kwargs)


def get_imb_qty_g(start_date: str, end_date: str, imb_org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Balance Responsible Group Imbalance Quantity / Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı

    Category: Dengesizlik

    EN (Balance Responsible Group Imbalance Quantity):
        Parties responsible for the balance may come together within the scope of balancing obligations and form a group responsible for the balance. A balance responsible party from within the group on behalf of the balance responsible group assumes the financial responsibility of the balance responsible group to the Market Operator regarding the energy imbalance. It is the amount that indicates how much the organization in the portfolio of the parties responsible for the balance deviates from the production/consumption values realized as a result of market transactions.

    TR (Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı):
        Dengeden sorumlu taraflar dengeleme yükümlülükleri kapsamında bir araya gelerek dengeden sorumlu grup oluşturabilirler. Dengeden sorumlu grup adına grup içinden bir dengeden sorumlu taraf, dengeden sorumlu grubun enerji dengesizliğine ilişkin Piyasa İşletmecisine karşı mali sorumluluğunu üstlenir. Dengeden sorumlu taraflarının portföyünde yer alan organizasyonların piyasa işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/balance-responsible-group-imbalance-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("imb-qty-g", start_date=start_date, end_date=end_date, imb_org_id=imb_org_id, **kwargs)


def get_imb_vol(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Imbalance Cost / Dengesizlik Tutarı

    Category: Dengesizlik

    EN (Imbalance Cost):
        It is the amount that the market participants are credited/debt in case of deviations from the production/consumption values realized as a result of the Day-ahead Market, Intraday Market, Balancing Power Market and Bilateral Agreement transactions.

    TR (Dengesizlik Tutarı):
        Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden sapmaları durumunda alacaklı/borçlu olduğu tutardır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/imbalance-cost
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("imb-vol", start_date=start_date, end_date=end_date, **kwargs)

