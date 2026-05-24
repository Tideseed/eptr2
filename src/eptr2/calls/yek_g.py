"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_yek_g_bilateral_contracts",
    "get_yek_g_expirations",
    "get_yek_g_issued",
    "get_yek_g_match_price_minmax",
    "get_yek_g_match_quantity",
    "get_yek_g_order_quantity",
    "get_yek_g_redemptions",
    "get_yek_g_trade_volume",
    "get_yek_g_wap",
    "get_yek_g_withdrawals",
]

def get_yek_g_bilateral_contracts(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Bilateral Contract Amount / YEK-G İkili Anlaşma Miktarları

    Category: YEK-G

    EN (YEK-G Bilateral Contract Amount):
        It displays the number of YEK-G documents transferred between accounts on the selected date.

    TR (YEK-G İkili Anlaşma Miktarları):
        Seçilen tarihte hesaplar arası transfer edilen YEK-G Belgelerinin sayısı kaynak ve adet bazlı gösterilir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-bilateral-contract-amount
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-bilateral-contracts", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_expirations(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Expiry Quantity / İlga edilen YEK-G Belge Miktarı

    Category: YEK-G

    EN (YEK-G Expiry Quantity):
        It displays the total number of YEK-G documents cancelled due to the fact that 12 months have passed since the production period.

    TR (İlga edilen YEK-G Belge Miktarı):
        Seçilen tarihte üretim tarihinden itibaren 12 ay geçmesine rağmen itfa edilmemiş olması sebebiyle İlga edilen YEK-G Belgelerinin sayısını kaynak ve adet bazlı gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-expiry-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-expirations", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_issued(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Issued Quantity of YEK-G Documents / İhraç edilen YEK-G Belge Miktarı

    Category: YEK-G

    EN (Issued Quantity of YEK-G Documents):
        It displays the total number of YEK-G documents issued to user accounts on a resource basis on the selected date.

    TR (İhraç edilen YEK-G Belge Miktarı):
        Seçilen tarihte kaynak bazında kullanıcı hesaplarına ihraç edilen toplam YEK-G Belgesi sayısını gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/issued-quantity-of-yek-g-documents
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-issued", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_match_price_minmax(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Min–Max Matching Price / YEK-G Min-Max Eşleşme Fiyatları

    Category: YEK-G

    EN (YEK-G Min–Max Matching Price):
        It displays the resource based minimum and maximum macthed YEK-G document prices in Organized YEK-G market sessions.

    TR (YEK-G Min-Max Eşleşme Fiyatları):
        Seçilen Tarihte YEK-G Belgelerinin kaynak bazında minimum ve maksimum eşleşme fiyatlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-min-max-matching-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-match-price-minmax", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_match_quantity(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Matching Quantity / Org. YEK-G Piyasa Eşleşme Miktarları

    Category: YEK-G

    EN (YEK-G Matching Quantity):
        It displays resource based matched YEK-G documents between parties in Organized YEK-G market sessions.

    TR (Org. YEK-G Piyasa Eşleşme Miktarları):
        Seçilen tarihte YEK-G Belgelerinin kaynak bazında gerçekleşen son eşleşme miktarı ve işlem miktarlarını gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-matching-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-match-quantity", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_order_quantity(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Organized Market Bid/Ask Quantity / YEK-G Org. Piyasa Alış/Satış Teklif Miktarı

    Category: YEK-G

    EN (YEK-G Organized Market Bid/Ask Quantity):
        It displays resourse based bid and offer amounts given in Organized YEK-G Market

    TR (YEK-G Org. Piyasa Alış/Satış Teklif Miktarı):
        Kaynak bazlı açılan her bir kontrata ilişkin verilmiş olan alış ve satış teklif miktarlarını göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-organized-market-bid-ask-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-order-quantity", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_redemptions(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Cancelation Quantity of YEK-G Documents / YEK-G İtfa İşlem Miktarları

    Category: YEK-G

    EN (Cancelation Quantity of YEK-G Documents):
        Indicates the number of cancelation of the YEK-G Document to be used for disclosure on the selected date.

    TR (YEK-G İtfa İşlem Miktarları):
        Seçilen tarihte YEK-G Belgesinin ifşa amacıyla kullanılmak üzere itfa edilme sayısını göstermektedir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/cancelation-quantity-of-yek-g-documents
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-redemptions", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_trade_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Organized Market Trading Volume / YEK-G Org. Piyasa İşlem Hacmi

    Category: YEK-G

    EN (YEK-G Organized Market Trading Volume):
        It displays the trade volume of Organized YEK-G market in resource base.

    TR (YEK-G Org. Piyasa İşlem Hacmi):
        Her bir kaynakta açılan kontratlara verilmiş olan tekliflerin eşleşmesi ile oluşan işlem hacminin gösterilmesi

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-organized-market-trading-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-trade-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_wap(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Weighted Average Price / Org. YEK-G Piyasa Ağırlıklı Ortalama Fiyat

    Category: YEK-G

    EN (YEK-G Weighted Average Price):
        It displays resource based weighted average prices of Organized YEK-G Market.

    TR (Org. YEK-G Piyasa Ağırlıklı Ortalama Fiyat):
        Seçilen Tarihte Organize YEK-G Piyasasında belirli bir enerji kaynağına ilişkin YEK-G Belgelesinin eşleştiği fiyatlara göre Ağırlıklı Ortalama Fiyat olarak gösterir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-weighted-average-price
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-wap", start_date=start_date, end_date=end_date, **kwargs)


def get_yek_g_withdrawals(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """YEK-G Withdrawal Quantity / İptal edilen YEK-G Belge Miktarı

    Category: YEK-G

    EN (YEK-G Withdrawal Quantity):
        It displays the number of YEK-G documents cancelled due to system malfunction.

    TR (İptal edilen YEK-G Belge Miktarı):
        Seçilen tarihte ihraç ve transfer süresinde oluşabilecek hatalar sebebiyle iptal edilen YEK-G Belgelerinin sayısını kaynak ve adet bazlı gösterir. İkili Anlaşma Piyasası’nda veriler takip eden iş günü 15:00’dan sonra, Organize Piyasa’da ise sean sonrası sürecinden sonra yayımlanır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/yek-g/yek-g-withdrowal-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("yek-g-withdrawals", start_date=start_date, end_date=end_date, **kwargs)

