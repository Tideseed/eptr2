from eptr2.mapping import (
    get_path_map,
    get_total_path,
    get_call_method,
)

from eptr2.mapping.parameters import get_required_parameters, get_optional_parameters


def get_help_d(key=None):
    d = {
        "dam-volume": {
            "category": "GÖP",
            "title": {"tr": "GÖP İşlem Hacmi", "en": "DAM Trade Value"},
            "desc": {
                "tr": "Gün Öncesi Piyasası’nda eşleşen alış tekliflerinin saatlik toplam mali değeridir",
                "en": "The hourly total financial volume of the matching bids in Day-Ahead Market",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-trade-value",
        },
        "pi-offer": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Fiyattan Bağımsız Satış Teklifi",
                "en": "DAM Price Independent Sales Order",
            },
            "desc": {
                "tr": "Gün öncesi piyasasında saatlik olarak fiyat kırılımı oluşturulmadan sunulan satış tekliflerinin toplamıdır",
                "en": "Sum of the offers submitted hourly in the day ahead market without any price step",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-price-independent-sales-order",
        },
        "pi-bid": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Fiyattan Bağımsız Alış Teklifi",
                "en": "DAM Price Independent Bid Order",
            },
            "desc": {
                "tr": "Gün öncesi piyasasında saatlik olarak fiyat kırılımı oluşturulmadan sunulan alış tekliflerinin toplamıdır.",
                "en": "Price Independent Bid: Sum of the bids submitted hourly in the day ahead market without any price step",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-price-independent-bid-order",
        },
        "supply-demand": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Arz-Talep",
                "en": "DAM Supply-Demand",
            },
            "desc": {
                "tr": "Her bir fiyat kırılımındaki saatlik teklif miktarına, kabul edilen blok ve esnek teklif miktarlarının ilave edilmesiyle oluşturulmuş teklif setlerinin gösterilmesidir.",
                "en": "Displaying created order sets by adding block and flexible bids to hourly bids at each price step.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-supply-demand",
        },
        "dam-bid": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Teklif Edilen Alış Miktarları",
                "en": "DAM Submitted Bid Order Volume",
            },
            "desc": {
                "tr": "Gün Öncesi Piyasası’nda 0 TL/MWh fiyat seviyesine sunulan saatlik, blok ve esnek alış teklif miktarlarının toplamıdır.",
                "en": "Submitted Bid Quantity: Sum of hourly, block and flexible bid quantities at 0 TL/MWh price step",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-submitted-bid-order-volume",
        },
        "dam-offer": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Teklif Edilen Satış Miktarları",
                "en": "DAM Submitted Sales Order Volume",
            },
            "desc": {
                "tr": "Gün Öncesi Piyasası’nda azami uzlaştırma (veya tavan) fiyat seviyesine sunulan saatlik, blok ve esnek satış teklif miktarlarının toplamıdır.",
                "en": "Submitted Offer Quantity: Sum of hourly, block and flexible offer quantities at maximum clearing price step.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-submitted-sales-order-volume",
        },
        "dam-block-bid": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Blok Alış Miktarı",
                "en": "DAM Block Bid",
            },
            "desc": {
                "tr": "Gün Öncesi Piyasası'nda sunulan en az 4 en fazla 24 saati kapsayan ve eşleşen blok alış tekliflerinin toplam miktarıdır.",
                "en": "Blok Bid: Active electricity purchase bids of market participants participating in the day-ahead market that includes a single price during the specified time slot and variable volume information based on a given settlement period.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-block-bid",
        },
        "dam-block-offer": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Blok Satış Miktarı",
                "en": "DAM Block Offer",
            },
            "desc": {
                "tr": "Gün Öncesi Piyasası'nda sunulan en az 4 en fazla 24 saati kapsayan ve eşleşen blok satış tekliflerinin toplam miktarıdır.",
                "en": "Block Offer: Active electricity sales offers of market participants participating in the day-ahead market that includes a single price during the specified time slot and variable volume information based on a given settlement period",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-block-offer",
        },
        "dam-flexible-bid": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Esnek Alış Teklif Miktarı",
                "en": "DAM Flexible Buying Offer Quantity",
            },
            "desc": {
                "tr": "Gün öncesi piyasasına katılan piyasa katılımcısının, belirli bir teklif zaman aralığında belirtilen teklif süresi için, lot cinsinden uzlaştırma dönemi bazlı değişebilen alış miktarlarını eşleşen ve eşleşmeyen teklif kırılımında içerir.",
                "en": "Flexible Purchase Bid Quantity: The flexible purchase bid shall include the purchase volumes of the market participant participating in the day-ahead market for a specified order period within a certain order time period in terms of lots, which may vary on a settlement period basis.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-flexible-buying-offer-quantity",
        },
        "dam-flexible-offer": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Esnek Satış Teklif Miktarı",
                "en": "DAM Flexible Selling Offer Quantity",
            },
            "desc": {
                "tr": "Gün öncesi piyasasına katılan piyasa katılımcısının, belirli bir teklif zaman aralığında belirtilen teklif süresi için, lot cinsinden uzlaştırma dönemi bazlı değişebilen satış miktarlarını eşleşen ve eşleşmeyen teklif kırılımında içerir.",
                "en": "Flexible Sales Offer Quantity: The flexible sales offer shall include the sales volumes of the market participant participating in the day-ahead market for a specified order period within a certain order time period in terms of lots, which may vary on a settlement period basis.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-flexible-selling-offer-quantity",
        },
        "dam-flexible-matching": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Esnek Teklif Eşleşme Miktarları",
                "en": "DAM Matched Flexible Offer Quantity",
            },
            "desc": {
                "tr": "Esnek Teklif Eşleşme Miktarları Belirli bir teklif zaman aralığı boyunca belirli bir teklif süresi için değişebilen miktarlardan ve bu miktarlar için tek fiyat bilgilerinden oluşan esnek tekliflerin alış ve satış yönlü eşleşme miktarları.",
                "en": "Matched Flexible Offer Quantity: Bid and offer matching quantities of flexible offers, which consist of quantities that can change for a given bid period during a given bid time interval.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-matched-flexible-offer-quantity",
        },
        ## GÖP Eşleşme Miktarı
        "dam-clearing": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Eşleşme Miktarı",
                "en": "DAM Matching Quantity",
            },
            "desc": {
                "tr": "Gün Öncesi Piyasası'nda eşleşen tekliflerin saatlik toplam miktardır.",
                "en": "Hourly aggregate cleared order quantity.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-matching-quantity",
        },
        "dam-clearing-org-list": {
            "category": "GÖP",
            "title": {
                "tr": "Göp Eşleşme Miktarı Organizasyon Listeleme",
                "en": "DAM Clearing Quantity Organization Listing",
            },
            "desc": {
                "tr": "Göp Eşleşme Miktarı Organizasyon Listeleme.",
                "en": "Lists organizations for the DAM Clearing Quantity Data Listing Service.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-matching-quantity",
        },
        "dam-diff": {
            "category": "GÖP",
            "title": {
                "tr": "GÖP Fark Tutarı",
                "en": "DAM Side Payment",
            },
            "desc": {
                "tr": "Alış tekliflerinden kaynaklı fark tutarı alış yönlü blok ve esnek teklif eşleşmelerinden, satış tekliflerinden kaynaklı fark tutarı satış yönlü blok ve esnek teklif eşleşmelerinden kaynaklanmaktadır.",
                "en": "Collected from the relevant market participants registered with the Day Ahead Market in accordance with the Electricity Market Balancing and Settlement Regulation for the financing of the gap between the daily system purchase amounts and the daily system sales amounts arising out of rounding off and block and flexible orders within the scope of the Day Ahead Market.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/dam-side-payment",
        },
        "mcp": {
            "category": "GÖP",
            "title": {
                "tr": "Piyasa Takas Fiyatı (PTF)",
                "en": "Market Clearing Price (MCP)",
            },
            "desc": {
                "tr": "Piyasa Takas Fiyatı, Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan saatlik elektrik enerjisi fiyatıdır.",
                "en": "Market Clearing Price: Hourly electricity purchase-sale price determined as a result of matching the purchase and sale bids for all bidding zones in the day-ahead market for a certain hour.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/market-clearing-price-mcp",
        },
        ## Kesinleşmemiş PTF
        "interim-mcp": {
            "category": "GÖP",
            "title": {
                "tr": "Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF)",
                "en": "Interim Market Clearing Price (I.MCP)",
            },
            "desc": {
                "tr": "Kesinleşmemiş Piyasa Takas Fiyatı , Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan itiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.",
                "en": "Interim Market Clearing Price is the temporary hourly energy price which is determined within the objection period with respect to orders that are cleared according to total supply and demand.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/interim-market-clearing-price-i-mcp",
        },
        # ## Kesinleşmemiş PTF yayınlandı mı?
        # "interim-mcp-status": {
        #     "prefix": "data",
        #     "prev": "dam",
        #     "label": "interim-mcp-published-status",
        # },
        # ## GİP Ağırlıklı Ortalama Fiyat
        # "wap": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "weighted-average-price",
        # },
        # ## GİP Eşleşme Miktarı
        # "idm-qty": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "matching-quantity",
        # },
        # ## GİP Min - Maks Alış Teklif Fiyatı
        # "idm-mm-bid": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "min-max-bid-price",
        # },
        # ## GİP Min - Maks Satış Teklif Fiyatı
        # "idm-mm-offer": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "min-max-sales-offer-price",
        # },
        # ## GİP Min - Maks Eşleşme Fiyatı
        # "idm-mm-matching": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "min-max-matching-price",
        # },
        # ## GİP İşlem Hacmi
        # "idm-volume": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "trade-value",
        # },
        # ## GİP İşlem Akışı
        # "idm-log": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "transaction-history",
        # },
        # ## GİP Teklif Edilen Alış Satış Miktarları
        # "idm-ob-qty": {
        #     "prefix": "data",
        #     "prev": "idm",
        #     "label": "bid-offer-quantities",
        # },
        # ## SMF
        # "smp": {"prefix": "data", "prev": "bpm", "label": "system-marginal-price"},
        # ## SMF Yön
        # "smp-dir": {"prefix": "data", "prev": "bpm", "label": "system-direction"},
        # ## YAL Talimat Miktarı
        # "bpm-up": {"prefix": "data", "prev": "bpm", "label": "order-summary-up"},
        # ## YAT Talimat Miktarı
        # "bpm-down": {
        #     "prefix": "data",
        #     "prev": "bpm",
        #     "label": "order-summary-down",
        # },
        # ## İkili Anlaşma (İA) Alış Miktarı
        # "bi-long": {
        #     "prefix": "data",
        #     "prev": "bilateral-contracts",
        #     "label": "bilateral-contracts-bid-quantity",
        # },
        # ## İkili Anlaşma (İA) Satış Miktarı
        # "bi-short": {
        #     "prefix": "data",
        #     "prev": "bilateral-contracts",
        #     "label": "bilateral-contracts-offer-quantity",
        # },
        # ### EÜAŞ - GTŞ İkili Anlaşmalar
        # "bi-euas": {
        #     "prefix": "data",
        #     "prev": "bilateral-contracts",
        #     "label": "amount-of-bilateral-contracts",
        # },
        # ## Dengesizlik Miktarı
        # "imb-qty": {
        #     "prefix": "data",
        #     "prev": "imbalance",
        #     "label": "imbalance-quantity",
        # },
        # ## Dengesizlik Tutarı
        # "imb-vol": {
        #     "prefix": "data",
        #     "prev": "imbalance",
        #     "label": "imbalance-amount",
        # },
        # ## Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı
        # "imb-qty-g": {
        #     "prefix": "data",
        #     "prev": "imbalance",
        #     "label": "dsg-imbalance-quantity",
        # },
        # ## DSG Organizasyon Listesi
        # "imb-org-list": {
        #     "prefix": "data",
        #     "prev": "imbalance",
        #     "label": "dsg-organization-list",
        # },
        # ## PTF
        # "mcp": {"prefix": "data", "prev": "dam"},
        # ## Kesinleşmemiş PTF
        # "interim-mcp": {"prefix": "data", "prev": "dam"},
        # ## Kesinleşmemiş PTF yayınlandı mı?
        # "interim-mcp-status": {
        #     "prefix": "data",
        #     "prev": "dam",
        #     "label": "interim-mcp-published-status",
        # },
        # ### PTF-SMF-SDF
        # "mcp-smp-imb": {
        #     "prefix": "data",
        #     "prev": "reporting-service",
        #     "label": "ptf-smf-sdf",
        # },
        # ## DGP Talimat Ağırlıklı Ortalama
        # "bpm-orders-w-avg": {
        #     "prefix": "data",
        #     "prev": "reporting-service",
        #     "label": "dgp-talimat-agr-ort",
        # },
        # ## KGÜP
        # "kgup": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "dpp",
        # },
        # ## KUDUP
        # "kudup": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "sbfgp",
        # },
        # ## EAK
        # "eak": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "aic",
        # },
        # ## Gerçek Zamanlı Üretim
        # "rt-gen": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "realtime-generation",
        # },
        # ## UEVM
        # "uevm": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "injection-quantity",
        # },
        # ## Santral Listeleme
        # "pp-list": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "powerplant-list",
        # },
        # ## Üretici Organizasyon Listesi
        # "gen-org": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "organization-list",
        # },
        # ## Bölge Listesi
        # "region-list": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "region-list",
        # },
        # ## PMS Mesaj Tipi Listesi
        # "mms-message-type-list": {
        #     "prefix": "data",
        #     "prev": "markets",
        #     "label": "umm-message-type-list",
        # },
        # ## Üretici UEVÇB Listesi
        # "gen-uevcb": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "uevcb-list",
        # },
        # ## Lisanslı Santral Yatırımları
        # "lic-pp-list": {
        #     "prefix": "data",
        #     "prev": "generation",
        #     "label": "licensed-powerplant-investment-list",
        # },
        # ## Lisanslı Santral Yatırımları
        # "load-plan": {
        #     "prefix": "data",
        #     "prev": "consumption",
        #     "label": "load-estimation-plan",
        # },
        # ## Gerçek Zamanlı Tüketim
        # "rt-cons": {
        #     "prefix": "data",
        #     "prev": "consumption",
        #     "label": "realtime-consumption",
        # },
        # ## UEÇM
        # "uecm": {
        #     "prefix": "data",
        #     "prev": "consumption",
        #     "label": "uecm",
        # },
        # ## Serbest Tüketici UEÇM
        # "st-uecm": {
        #     "prefix": "data",
        #     "prev": "consumption",
        #     "label": "st-uecm",
        # },
        # ## Tedarik Yükümlülüğü Kapsamındaki UEÇM
        # "su-uecm": {
        #     "prefix": "data",
        #     "prev": "consumption",
        #     "label": "withdrawal-quantity-under-supply-liability",
        # },
        # ## YEKDEM RES Üretim ve Tahmin Listeleme
        # "wind-forecast": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "res-generation-and-forecast",
        # },
        # ## YEKDEM Santral Listesi
        # "ren-pp-list": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "licensed-powerplant-list",
        # },
        # ## YEKDEM Gerçek Zamanlı Üretim
        # "ren-rt-gen": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "licensed-realtime-generation",
        # },
        # ## YEKDEM UEVM
        # "ren-uevm": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "renewable-sm-licensed-injection-quantity",
        # },
        # ## Lisanssız Üretim
        # "ren-ul-gen": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "unlicensed-generation-amount",
        # },
        # ## Lisanssız Üretim Bedeli
        # "ren-ul-cost": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "unlicensed-generation-cost",
        # },
        # ## YEK Bedeli
        # # "yekbed": {"redirect": "ren-lic-cost"},
        # "ren-lic-cost": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "licensed-generation-cost",
        # },
        # ## YEK Geliri
        # "ren-income": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "renewables-support-mechanism-income",
        # },
        # ## YEK Toplam Gider (YEKTOB)
        # "ren-total-cost": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "total-cost",
        # },
        # ## Lisanssız Üretim Bedeli
        # "ren-capacity": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "new-installed-capacity",
        # },
        # ## YEKDEM Birim Maliyeti
        # "ren-unit-cost": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "unit-cost",
        # },
        # ## YEKDEM Katılımcı Listesi
        # "ren-participant-list": {
        #     "prefix": "data",
        #     "prev": "renewables",
        #     "label": "renewables-participant",
        # },
        # ## Sıfır Bakiye Düzeltme Tutarı
        # "zero-balance": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "zero-balance",
        # },
        # ## İSKK
        # "iskk": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "iskk-list",
        # },
        # ## Kısıt Maliyeti
        # "congestion-cost": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "congestion-cost",
        # },
        # ##ENTSO-E (X) Kodları
        # ## TODO: Fix
        # # "eic-x-list": {
        # #     "prefix": "data",
        # #     "prev": "transmission",
        # #     "label": "organization-list",
        # # },
        # ##ENTSO-E (W) Kodları
        # "eic-w-list": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "entso-w-organization",
        # },
        # ## Enterkonneksiyon Arıza Bakım Bildirimleri
        # "international-line-events": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "international-line-events",
        # },
        # ##Enterkonneksiyon Kapasitesine İlişkin Yıl Öncesi Tahminler
        # "tcat-pre-year-forecast": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "tcat-pre-year-forecast",
        # },
        # ##Enterkonneksiyon Kapasitesine İlişkin Ay Öncesi Tahminler
        # "tcat-pre-month-forecast": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "tcat-pre-month-forecast",
        # },
        # ##Enterkonneksiyon Hat Kapasiteleri
        # "line-capacities": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "line-capacities",
        # },
        # ##Enterkonneksiyon Hat Kapasiteleri
        # "capacity-demand": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "line-capacities",
        # },
        # ##Nomine Kapasite
        # "nominal-capacity": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "nominal-capacity",
        # },
        # ##Enterkonneksiyon Hat Kapasiteleri Yön Listesi
        # "intl-direction-list": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "line-capacities-direction",
        # },
        # ##Enterkonneksiyon Hat Kapasite Talepleri Yön Listesi
        # "intl-capacity-demand-direction-list": {
        #     "prefix": "data",
        #     "prev": "transmission",
        #     "label": "line-capacities-direction",
        # },
        # ## Piyasa Mesaj Sistemi
        # "mms": {
        #     "prefix": "data",
        #     "prev": "markets",
        #     "label": "market-message-system",
        # },
        # ## Organizasyona Göre Santral Listeleme (Piyasa Mesaj Sistemi)
        # "mms-pp-list": {
        #     "prefix": "data",
        #     "prev": "markets",
        #     "label": "power-plant-list-by-organization-id",
        # },
        # ## UEVÇB'ye Göre Santral Listeleme (Piyasa Mesaj Sistemi)
        # "mms-uevcb-list": {
        #     "prefix": "data",
        #     "prev": "markets",
        #     "label": "uevcb-list-by-power-plant-id",
        # },
        # ## Gün bilgileri
        # "date-init": {
        #     "prefix": "main",
        #     "prev": "electricity-service",
        #     "label": "date-init",
        # },
        # ## Piyasa Katılımcıları
        # "market-participants": {
        #     "prefix": "data",
        #     "prev": "general-data",
        #     "label": "market-participants",
        # },
        # ##Piyasa Katılımcıları Organizasyon
        # "market-participants-organization-list": {
        #     "prefix": "data",
        #     "prev": "general-data",
        #     "label": "market-participants-organization-filter-list",
        # },
    }

    if key is None:
        return d

    return d.get(key, None)


def get_call_help(key: str) -> str:
    """Returns the help string for the given call.

    Args:
        key (str): The call key.

    Returns:
        str: The help string.
    """

    keylist = get_path_map(just_call_keys=True)
    if key not in keylist:
        return None

    d = get_help_d(key)
    call_path = get_total_path(key)
    call_method = get_call_method(key)
    required_body_params = get_required_parameters(key)
    optional_body_params = get_optional_parameters(key)

    help_d = {
        "help": d,
        "call_path": call_path,
        "call_method": call_method,
        "required_body_params": required_body_params,
        "optional_body_params": optional_body_params,
    }

    return help_d
