"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_ng_participant_list",
    "get_ng_participants",
]

def get_ng_participant_list(eptr: EPTR2 | None = None, **kwargs):
    """Natural Gas Market Participant List / Doğal Gaz Katılımcı Listesi

    Category: NG

    EN (Natural Gas Market Participant List):
        Participant List Service

    TR (Doğal Gaz Katılımcı Listesi):
        Katılımcı Listesi Servisi

    Reference: https://seffaflik.epias.com.tr/natural-gas-service/technical/tr/index.html#_participant-list
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-participant-list", **kwargs)


def get_ng_participants(org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """Natural Gas Market Participants / Doğal Gaz Piyasa Katılımcıları

    Category: NG

    EN (Natural Gas Market Participants):
        It shows market (SGP, VGP) registration status of the participants.

    TR (Doğal Gaz Piyasa Katılımcıları):
        Katılımcıların piyasa (SGP, VGP) kayıt durumlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/natural-gas/natural-gas-markets/general-data/natural-gas-market-participants
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ng-participants", org_id=org_id, **kwargs)

