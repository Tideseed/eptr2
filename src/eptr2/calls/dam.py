"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""
from __future__ import annotations

from eptr2.main import EPTR2

__all__ = [
    "get_dam_bid",
    "get_dam_block_bid",
    "get_dam_block_offer",
    "get_dam_clearing",
    "get_dam_clearing_org_list",
    "get_dam_diff",
    "get_dam_flexible_bid",
    "get_dam_flexible_matching",
    "get_dam_flexible_offer",
    "get_dam_offer",
    "get_dam_volume",
    "get_interim_mcp",
    "get_interim_mcp_status",
    "get_mcp",
    "get_pi_bid",
    "get_pi_offer",
    "get_supply_demand",
    "get_ptf",
]

def get_dam_bid(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Submitted Bid Order Volume / GÖP Teklif Edilen Alış Miktarları

    Category: GÖP

    EN (DAM Submitted Bid Order Volume):
        Submitted Bid Quantity: Sum of hourly, block and flexible bid quantities at 0 TL/MWh price step

    TR (GÖP Teklif Edilen Alış Miktarları):
        Gün Öncesi Piyasası’nda 0 TL/MWh fiyat seviyesine sunulan saatlik, blok ve esnek alış teklif miktarlarının toplamıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-submitted-bid-order-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-bid", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_block_bid(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Block Bid / GÖP Blok Alış Miktarı

    Category: GÖP

    EN (DAM Block Bid):
        Blok Bid: Active electricity purchase bids of market participants participating in the day-ahead market that includes a single price during the specified time slot and variable volume information based on a given settlement period.

    TR (GÖP Blok Alış Miktarı):
        Gün Öncesi Piyasası'nda sunulan en az 4 en fazla 24 saati kapsayan ve eşleşen blok alış tekliflerinin toplam miktarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-block-bid
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-block-bid", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_block_offer(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Block Offer / GÖP Blok Satış Miktarı

    Category: GÖP

    EN (DAM Block Offer):
        Block Offer: Active electricity sales offers of market participants participating in the day-ahead market that includes a single price during the specified time slot and variable volume information based on a given settlement period

    TR (GÖP Blok Satış Miktarı):
        Gün Öncesi Piyasası'nda sunulan en az 4 en fazla 24 saati kapsayan ve eşleşen blok satış tekliflerinin toplam miktarıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-block-offer
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-block-offer", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_clearing(start_date: str, end_date: str, org_id: str | int | None = None, eptr: EPTR2 | None = None, **kwargs):
    """DAM Matching Quantity / GÖP Eşleşme Miktarı

    Category: GÖP

    EN (DAM Matching Quantity):
        Hourly aggregate cleared order quantity.

    TR (GÖP Eşleşme Miktarı):
        Gün Öncesi Piyasası'nda eşleşen tekliflerin saatlik toplam miktardır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-matching-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-clearing", start_date=start_date, end_date=end_date, org_id=org_id, **kwargs)


def get_dam_clearing_org_list(period: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Clearing Quantity Organization Listing / Göp Eşleşme Miktarı Organizasyon Listeleme

    Category: GÖP

    EN (DAM Clearing Quantity Organization Listing):
        Lists organizations for the DAM Clearing Quantity Data Listing Service.

    TR (Göp Eşleşme Miktarı Organizasyon Listeleme):
        Göp Eşleşme Miktarı Organizasyon Listeleme.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-matching-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-clearing-org-list", period=period, **kwargs)


def get_dam_diff(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Side Payment / GÖP Fark Tutarı

    Category: GÖP

    EN (DAM Side Payment):
        Collected from the relevant market participants registered with the Day Ahead Market in accordance with the Electricity Market Balancing and Settlement Regulation for the financing of the gap between the daily system purchase amounts and the daily system sales amounts arising out of rounding off and block and flexible orders within the scope of the Day Ahead Market.

    TR (GÖP Fark Tutarı):
        Alış tekliflerinden kaynaklı fark tutarı alış yönlü blok ve esnek teklif eşleşmelerinden, satış tekliflerinden kaynaklı fark tutarı satış yönlü blok ve esnek teklif eşleşmelerinden kaynaklanmaktadır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-side-payment
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-diff", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_flexible_bid(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Flexible Buying Offer Quantity / GÖP Esnek Alış Teklif Miktarı

    Category: GÖP

    EN (DAM Flexible Buying Offer Quantity):
        Flexible Purchase Bid Quantity: The flexible purchase bid shall include the purchase volumes of the market participant participating in the day-ahead market for a specified order period within a certain order time period in terms of lots, which may vary on a settlement period basis.

    TR (GÖP Esnek Alış Teklif Miktarı):
        Gün öncesi piyasasına katılan piyasa katılımcısının, belirli bir teklif zaman aralığında belirtilen teklif süresi için, lot cinsinden uzlaştırma dönemi bazlı değişebilen alış miktarlarını eşleşen ve eşleşmeyen teklif kırılımında içerir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-flexible-buying-offer-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-flexible-bid", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_flexible_matching(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Matched Flexible Offer Quantity / GÖP Esnek Teklif Eşleşme Miktarları

    Category: GÖP

    EN (DAM Matched Flexible Offer Quantity):
        Matched Flexible Offer Quantity: Bid and offer matching quantities of flexible offers, which consist of quantities that can change for a given bid period during a given bid time interval.

    TR (GÖP Esnek Teklif Eşleşme Miktarları):
        Esnek Teklif Eşleşme Miktarları Belirli bir teklif zaman aralığı boyunca belirli bir teklif süresi için değişebilen miktarlardan ve bu miktarlar için tek fiyat bilgilerinden oluşan esnek tekliflerin alış ve satış yönlü eşleşme miktarları.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-matched-flexible-offer-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-flexible-matching", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_flexible_offer(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Flexible Selling Offer Quantity / GÖP Esnek Satış Teklif Miktarı

    Category: GÖP

    EN (DAM Flexible Selling Offer Quantity):
        Flexible Sales Offer Quantity: The flexible sales offer shall include the sales volumes of the market participant participating in the day-ahead market for a specified order period within a certain order time period in terms of lots, which may vary on a settlement period basis.

    TR (GÖP Esnek Satış Teklif Miktarı):
        Gün öncesi piyasasına katılan piyasa katılımcısının, belirli bir teklif zaman aralığında belirtilen teklif süresi için, lot cinsinden uzlaştırma dönemi bazlı değişebilen satış miktarlarını eşleşen ve eşleşmeyen teklif kırılımında içerir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-flexible-selling-offer-quantity
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-flexible-offer", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_offer(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Submitted Sales Order Volume / GÖP Teklif Edilen Satış Miktarları

    Category: GÖP

    EN (DAM Submitted Sales Order Volume):
        Submitted Offer Quantity: Sum of hourly, block and flexible offer quantities at maximum clearing price step.

    TR (GÖP Teklif Edilen Satış Miktarları):
        Gün Öncesi Piyasası’nda azami uzlaştırma (veya tavan) fiyat seviyesine sunulan saatlik, blok ve esnek satış teklif miktarlarının toplamıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-submitted-sales-order-volume
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-offer", start_date=start_date, end_date=end_date, **kwargs)


def get_dam_volume(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Trade Value / GÖP İşlem Hacmi

    Category: GÖP

    EN (DAM Trade Value):
        The hourly total financial volume of the matching bids in Day-Ahead Market

    TR (GÖP İşlem Hacmi):
        Gün Öncesi Piyasası’nda eşleşen alış tekliflerinin saatlik toplam mali değeridir

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-trade-value
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("dam-volume", start_date=start_date, end_date=end_date, **kwargs)


def get_interim_mcp(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Interim Market Clearing Price (I.MCP) / Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF)

    Category: GÖP

    EN (Interim Market Clearing Price (I.MCP)):
        Interim Market Clearing Price is the temporary hourly energy price which is determined within the objection period with respect to orders that are cleared according to total supply and demand.

    TR (Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF)):
        Kesinleşmemiş Piyasa Takas Fiyatı , Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan itiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/interim-market-clearing-price-i-mcp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("interim-mcp", start_date=start_date, end_date=end_date, **kwargs)


def get_interim_mcp_status(eptr: EPTR2 | None = None, **kwargs):
    """Interim Market Clearing Price (I.MCP) published status / Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumu

    Category: GÖP

    EN (Interim Market Clearing Price (I.MCP) published status):
        Interim Market Clearing Price is the temporary hourly energy price which is determined within the objection period with respect to orders that are cleared according to total supply and demand.

    TR (Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumu):
        Kesinleşmemiş Piyasa Takas Fiyatı , Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan itiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/interim-market-clearing-price-i-mcp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("interim-mcp-status", **kwargs)


def get_mcp(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """Market Clearing Price (MCP) / Piyasa Takas Fiyatı (PTF)

    Category: GÖP

    EN (Market Clearing Price (MCP)):
        Market Clearing Price: Hourly electricity purchase-sale price determined as a result of matching the purchase and sale bids for all bidding zones in the day-ahead market for a certain hour.

    TR (Piyasa Takas Fiyatı (PTF)):
        Piyasa Takas Fiyatı, Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan saatlik elektrik enerjisi fiyatıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/market-clearing-price-mcp
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("mcp", start_date=start_date, end_date=end_date, **kwargs)


def get_pi_bid(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Price Independent Bid Order / GÖP Fiyattan Bağımsız Alış Teklifi

    Category: GÖP

    EN (DAM Price Independent Bid Order):
        Price Independent Bid: Sum of the bids submitted hourly in the day ahead market without any price step

    TR (GÖP Fiyattan Bağımsız Alış Teklifi):
        Gün öncesi piyasasında saatlik olarak fiyat kırılımı oluşturulmadan sunulan alış tekliflerinin toplamıdır.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-price-independent-bid-order
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("pi-bid", start_date=start_date, end_date=end_date, **kwargs)


def get_pi_offer(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Price Independent Sales Order / GÖP Fiyattan Bağımsız Satış Teklifi

    Category: GÖP

    EN (DAM Price Independent Sales Order):
        Sum of the offers submitted hourly in the day ahead market without any price step

    TR (GÖP Fiyattan Bağımsız Satış Teklifi):
        Gün öncesi piyasasında saatlik olarak fiyat kırılımı oluşturulmadan sunulan satış tekliflerinin toplamıdır

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-price-independent-sales-order
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("pi-offer", start_date=start_date, end_date=end_date, **kwargs)


def get_supply_demand(date_time: str, eptr: EPTR2 | None = None, **kwargs):
    """DAM Supply-Demand / GÖP Arz-Talep

    Category: GÖP

    EN (DAM Supply-Demand):
        Displaying created order sets by adding block and flexible bids to hourly bids at each price step.

    TR (GÖP Arz-Talep):
        Her bir fiyat kırılımındaki saatlik teklif miktarına, kabul edilen blok ve esnek teklif miktarlarının ilave edilmesiyle oluşturulmuş teklif setlerinin gösterilmesidir.

    Reference: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-supply-demand
    """
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("supply-demand", date_time=date_time, **kwargs)


def get_ptf(start_date: str, end_date: str, eptr: EPTR2 | None = None, **kwargs):
    if eptr is None:
        eptr = EPTR2()
    return eptr.call("ptf", start_date=start_date, end_date=end_date, **kwargs)

