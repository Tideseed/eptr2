"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_bpm_down",
    "get_bpm_up",
    "get_smp",
    "get_smp_dir",
    "get_smf",
]

def get_bpm_down(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Down Regulation Instructions / Yük Atma (YAT) Talimat Miktarı

    Category: DGP

    EN (Down Regulation Instructions):
        Down Regulation Instructions quantities are released to power units to keep the system balanced in case of energy surplus.

    TR (Yük Atma (YAT) Talimat Miktarı):
        0, 1, 2 kodlu Alma Talimat Miktarı (YAT), sistem yönünde elektrik fazlası durumlarda sistemi dengelemek için verilen talimat miktarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/down-regulation-instructions
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bpm-down", start_date=start_date, end_date=end_date, **kwargs)


def get_bpm_up(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Up Regulation Instructions / Yük Alma (YAL) Talimat Miktarları

    Category: DGP

    EN (Up Regulation Instructions):
        Up Regulation Instructions quantities are released to power units to keep the system balanced in case of energy deficit.

    TR (Yük Alma (YAL) Talimat Miktarları):
        0, 1, 2 kodlu Alma Talimat Miktarı (YAL), sistem yönünde elektrik açığı durumlarda sistemi dengelemek için verilen talimat miktarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/up-regulation-instructions
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("bpm-up", start_date=start_date, end_date=end_date, **kwargs)


def get_smp(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """System Marginal Price / Sistem Marjinal Fiyatı

    Category: DGP

    EN (System Marginal Price):
        Price that corresponds to the net regulation quantity of the Balancing Power Market.

    TR (Sistem Marjinal Fiyatı):
        Sistem Marjinal Fiyatı, Dengeleme Güç Piyasasında net talimat hacmine karşılık gelen teklifin fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/system-marginal-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("smp", start_date=start_date, end_date=end_date, **kwargs)


def get_smp_dir(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """System Direction / Sistem Yönü

    Category: GİP

    EN (System Direction):
        It displays whether the system is in energy surplus or deficit.

    TR (Sistem Yönü):
        Sistemde elektrik fazlası veya elektrik açığı olduğunu gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/system-s-direction
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("smp-dir", start_date=start_date, end_date=end_date, **kwargs)


def get_smf(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("smf", start_date=start_date, end_date=end_date, **kwargs)

