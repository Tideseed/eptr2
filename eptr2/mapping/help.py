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
        "interim-mcp-status": {
            "category": "GÖP",
            "title": {
                "tr": "Kesinleşmemiş Piyasa Takas Fiyatı (K.PTF) yayınlanma durumu",
                "en": "Interim Market Clearing Price (I.MCP) published status",
            },
            "desc": {
                "tr": "Kesinleşmemiş Piyasa Takas Fiyatı , Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan itiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.",
                "en": "Interim Market Clearing Price is the temporary hourly energy price which is determined within the objection period with respect to orders that are cleared according to total supply and demand.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/interim-market-clearing-price-i-mcp",
        },
        ## GİP Ağırlıklı Ortalama Fiyat
        "wap": {
            "category": "GİP",
            "title": {
                "tr": "GİP Ağırlıklı Ortalama Fiyat",
                "en": "IDM Weighted Average Price",
            },
            "desc": {
                "tr": "Gün İçi Piyasası'ndaki her bir kontrata ilişkin işlemlerin saatlik bazda hacimsel ağırlıklı ortalama fiyatıdır.",
                "en": "It is the hourly weighted average price for the transactions on each contract in Intraday Market.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-weighted-average-price",
        },
        "idm-qty": {
            "category": "GİP",
            "title": {
                "tr": "GİP Eşleşme Miktarı",
                "en": "IDM Matching Quantity",
            },
            "desc": {
                "tr": "Gün İçi Piyasası’nda kontrat türüne göre saatlik veya blok olarak gösterilen toplam eşleşme miktarıdır.",
                "en": "It is the total matching quantity in the intraday market which is categorized as hourly or block depending on the contract type.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-matching-quantity",
        },
        "idm-mm-bid": {
            "category": "GİP",
            "title": {
                "tr": "GİP Min - Maks Alış Teklif Fiyatı",
                "en": "IDM Min.-Max. Bid Price",
            },
            "desc": {
                "tr": "Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük alış teklif fiyatıdır.",
                "en": "It is the highest and lowest bid price displayed in the Intraday Market according to the contract type.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-min-max-bid-price",
        },
        "idm-mm-offer": {
            "category": "GİP",
            "title": {
                "tr": "GİP Min - Maks Satış Teklif Fiyatı",
                "en": "IDM Min-Max Offer Price",
            },
            "desc": {
                "tr": "Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük satış teklif fiyatıdır.",
                "en": "Max. and min. offer price given as hourly or block depending on the contract type.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-min-max-offer-price",
        },
        "idm-mm-matching": {
            "category": "GİP",
            "title": {
                "tr": "GİP Min - Maks Eşleşme Fiyat",
                "en": "IDM Min.-Max. Matching Price",
            },
            "desc": {
                "tr": "Gün İçi Piyasası'nda kontrat türüne göre saatlik veya blok olarak gösterilen en yüksek ve en düşük eşleşme fiyatıdır.",
                "en": "It is the min and max matching price in the intraday market which is categorized as hourly or block depending on the contract type.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-min-max-matching-price",
        },
        "idm-volume": {
            "category": "GİP",
            "title": {
                "tr": "GİP İşlem Hacmi",
                "en": "IDM Trade Value",
            },
            "desc": {
                "tr": "Gün İçi Piyasası’nda eşleşen alış-satış tekliflerinin saatlik toplam mali değeridir.",
                "en": "It is the hourly total financial volume of the matching bids and offers in the Intraday Market",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-trade-value",
        },
        "idm-log": {
            "category": "GİP",
            "title": {
                "tr": "GİP İşlem Akışı",
                "en": "IDM Transaction History",
            },
            "desc": {
                "tr": "Gün İçi Piyasası’nda gerçekleşen anlık işlemlerin fiyat ve miktarlarıdır.",
                "en": "It shows the prices and quantities of instant transactions realized in the Intraday Market.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-transaction-history",
        },
        "idm-ob-qty": {
            "category": "GİP",
            "title": {
                "tr": "GİP Teklif Edilen Alış Satış Miktarları",
                "en": "IDM Bid/Offer Quantities",
            },
            "desc": {
                "tr": "Gün İçi Piyasasında sunulan tekliflerin alış ve satış tekliflerinin toplam miktarlarıdır.",
                "en": "It is the total quantity of orders in buy and sell side in the Intra Day Market.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-bid-offer-quantities",
        },
        "smp": {
            "category": "DGP",
            "title": {
                "tr": "Sistem Marjinal Fiyatı",
                "en": "System Marginal Price",
            },
            "desc": {
                "tr": "Sistem Marjinal Fiyatı, Dengeleme Güç Piyasasında net talimat hacmine karşılık gelen teklifin fiyatıdır.",
                "en": "Price that corresponds to the net regulation quantity of the Balancing Power Market.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/system-marginal-price",
        },
        "smp-dir": {
            "category": "GİP",
            "title": {
                "tr": "Sistem Yönü",
                "en": "System Direction",
            },
            "desc": {
                "tr": "Sistemde elektrik fazlası veya elektrik açığı olduğunu gösterir.",
                "en": "It displays whether the system is in energy surplus or deficit.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/system-s-direction",
        },
        "bpm-up": {
            "category": "DGP",
            "title": {
                "tr": "Yük Alma (YAL) Talimat Miktarları",
                "en": "Up Regulation Instructions",
            },
            "desc": {
                "tr": "0, 1, 2 kodlu Alma Talimat Miktarı (YAL), sistem yönünde elektrik açığı durumlarda sistemi dengelemek için verilen talimat miktarıdır.",
                "en": "Up Regulation Instructions quantities are released to power units to keep the system balanced in case of energy deficit.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/up-regulation-instructions",
        },
        "bpm-down": {
            "category": "DGP",
            "title": {
                "tr": "Yük Atma (YAT) Talimat Miktarı",
                "en": "Down Regulation Instructions",
            },
            "desc": {
                "tr": "0, 1, 2 kodlu Alma Talimat Miktarı (YAT), sistem yönünde elektrik fazlası durumlarda sistemi dengelemek için verilen talimat miktarıdır.",
                "en": "Down Regulation Instructions quantities are released to power units to keep the system balanced in case of energy surplus.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/down-regulation-instructions",
        },
        "bi-long": {
            "category": "İA",
            "title": {
                "tr": "İkili Anlaşma (İA) Alış Miktarı",
                "en": "Bilateral Contracts Bid Quantity",
            },
            "desc": {
                "tr": "İkili anlaşmalara ait alış miktarları verisidir",
                "en": "It indicates the purchased power amount through bilateral power contracts.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/bilateral-contracts/bilateral-contracts-bid-quantity",
        },
        "bi-short": {
            "category": "İA",
            "title": {
                "tr": "İkili Anlaşma (İA) Satış Miktarı",
                "en": "Bilateral Contracts Offer Quantity",
            },
            "desc": {
                "tr": "İkili anlaşmalara ait satış miktarları verisidir",
                "en": "It indicates the sold power amount through bilateral power contracts.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/bilateral-contracts/bilateral-contracts-offer-quantity",
        },
        "bi-euas": {
            "category": "İA",
            "title": {
                "tr": "EÜAŞ - GTŞ İkili Anlaşmalar",
                "en": "Amount of Bilateral Contracts of EÜAŞ - Authorized Retailers",
            },
            "desc": {
                "tr": "Düzenlemeye tabi tarife kapsamına göre EÜAŞ ile GTŞ’lerin arasında yapılan ikili anlaşmaların aylık toplamlarını göstermektedir.",
                "en": "It indicates the monthly totals of bilateral agreements realized between EÜAŞ and Authorized Retail Companies according to the regulated tariff.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/bilateral-contracts/amount-of-bilateral-contracts-of-euas-authorized-retailers",
        },
        "imb-qty": {
            "category": "Dengesizlik",
            "title": {
                "tr": "Dengesizlik Miktarı",
                "en": "Imbalance Quantity",
            },
            "desc": {
                "tr": "Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.",
                "en": "It is the amount that indicates how much the market participants deviate from the production/consumption values realized as a result of the Day-ahead Market, Intraday Market, Balancing Power Market and Bilateral Agreement transactions.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/imbalance-quantity",
        },
        "imb-vol": {
            "category": "Dengesizlik",
            "title": {
                "tr": "Dengesizlik Tutarı",
                "en": "Imbalance Cost",
            },
            "desc": {
                "tr": "Piyasa katılımcılarının Gün Öncesi Piyasasındaki Gün İçi Piyasası, Dengeleme Güç Piyasası ve ikili Anlaşma işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden sapmaları durumunda alacaklı/borçlu olduğu tutardır.",
                "en": "It is the amount that the market participants are credited/debt in case of deviations from the production/consumption values realized as a result of the Day-ahead Market, Intraday Market, Balancing Power Market and Bilateral Agreement transactions.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/imbalance-cost",
        },
        "imb-qty-g": {
            "category": "Dengesizlik",
            "title": {
                "tr": "Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı",
                "en": "Balance Responsible Group Imbalance Quantity",
            },
            "desc": {
                "tr": "Dengeden sorumlu taraflar dengeleme yükümlülükleri kapsamında bir araya gelerek dengeden sorumlu grup oluşturabilirler. Dengeden sorumlu grup adına grup içinden bir dengeden sorumlu taraf, dengeden sorumlu grubun enerji dengesizliğine ilişkin Piyasa İşletmecisine karşı mali sorumluluğunu üstlenir. Dengeden sorumlu taraflarının portföyünde yer alan organizasyonların piyasa işlemleri neticesinde gerçekleşen üretim/tüketim değerlerinden ne kadar saptığını gösteren miktardır.",
                "en": "Parties responsible for the balance may come together within the scope of balancing obligations and form a group responsible for the balance. A balance responsible party from within the group on behalf of the balance responsible group assumes the financial responsibility of the balance responsible group to the Market Operator regarding the energy imbalance. It is the amount that indicates how much the organization in the portfolio of the parties responsible for the balance deviates from the production/consumption values realized as a result of market transactions.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/balance-responsible-group-imbalance-quantity",
        },
        # ## DSG Organizasyon Listesi
        "imb-org-list": {
            "category": "Dengesizlik",
            "title": {
                "tr": "DSG Organizasyon Listesi",
                "en": "DSG Organization List",
            },
            "desc": {
                "tr": "Dengeden Sorumlu Grup servisinde kullanılan Organizasyon Listesi",
                "en": "Organization List used on Balance Responsible Group Imbalance Quantity",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/imbalance/balance-responsible-group-imbalance-quantity",
        },
        "mcp-smp-imb": {
            "category": "Elektrik Piyasası Raporları",
            "title": {
                "tr": "PTF, SMF ve SDF Listeleme",
                "en": "MCP SMP and Imbalance Price Listing",
            },
            "desc": {
                "tr": "(Açıklama Yok)",
                "en": "(No description)",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-market-reports/mcp-smp-and-imbalance-price-listing",
        },
        "bpm-orders-w-avg": {
            "category": "Elektrik Piyasası Raporları",
            "title": {
                "tr": "DGP Talimatları (Ağırlıklı Ortalama)",
                "en": "BPM Instructions (Weighted Average)",
            },
            "desc": {
                "tr": "(Açıklama Yok)",
                "en": "(No description)",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-market-reports/bpm-instructions-weighted-average",
        },
        "kgup": {
            "category": "Üretim Planlama",
            "title": {
                "tr": "Kesinleşmiş Günlük Üretim Planı (KGÜP)",
                "en": "Final Daily Production Program (FDPP)",
            },
            "desc": {
                "tr": "Kesinleşmiş Gün Öncesi Üretim Programı, katılımcının bir sonraki güne ilişkin gerçekleştirmeyi öngördüğü ve sistem işletmecisine dengeleme güç piyasasının başlangıcında bildirdiği üretim değeridir.",
                "en": "Final day-ahead generation/consumption schedule (FDGS): The generation or consumption values which a settlement feed in-feed out unit anticipates to realize in the following day and notifies the System Operator at the opening of the balancing power market, depending on the obligations of the balancing responsible unit that it is a member of and the result of day-ahead balancing.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/final-daily-production-program-fdpp",
        },
        "kudup": {
            "category": "Üretim Planlama",
            "title": {
                "tr": "Kesinleştirilmiş Uzlaştırma Dönemi Üretim Planı (KUDÜP)",
                "en": "Settlement Based Final Generation Plan (SBFGP)",
            },
            "desc": {
                "tr": "Gün öncesinde bildirilen UEVÇB bazında kaynaklara göre kesinleşmiş günlük üretim planlarının gün içi piyasasının kapanışından sonra DUY 69. madde kapsamında güncellenmesiyle oluşan kesinleşmiş günlük üretim planları.",
                "en": "Final Settlement Period Generation Schedule: The generation schedules of power plants that have become unbalanced after the gate closure intraday market.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/settlement-based-final-generation-plan-sbfgp",
        },
        "eak": {
            "category": "Üretim Planlama",
            "title": {
                "tr": "Emre Amade Kapasite (EAK)",
                "en": "Available Installed Capacity (AIC)",
            },
            "desc": {
                "tr": "Emre Amade Kapasite: Bir üretim biriminin sisteme sağlayabileceği aktif güç kapasitesidir.",
                "en": "Available Installed Capacity: The active power capacity that a generation unit can provide to the system.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/available-installed-capacity-aic",
        },
        "rt-gen": {
            "category": "Gerçekleşen Üretim",
            "title": {
                "tr": "Gerçek Zamanlı Üretim",
                "en": "Real-Time Generation",
            },
            "desc": {
                "tr": "Elektrik üretiminin kaynak bazında saatlik gösterimidir.",
                "en": "Real time generation: The display of hourly generation values of electricity generation plants on a resource basis.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/real-time-generation",
        },
        "uevm": {
            "category": "Üretim Planlama",
            "title": {
                "tr": "Uzlaştırma Esas Veriş Miktarı (UEVM)",
                "en": "Injection Quantity",
            },
            "desc": {
                "tr": "Uzlaştırmaya esas veriş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sisteme verdiği elektrik miktarının toplam değeridir.",
                "en": "Settlement Based Power Generation: The total value of the resource based electricity amount given to the system hourly by the settlement units within a settlement period.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/injection-quantity",
        },
        "uevm-pp-list": {
            "category": "Listeleme",
            "title": {
                "tr": "Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi",
                "en": "Injection Quantity Powerplant Listing",
            },
            "desc": {
                "tr": "Uzlaştırma Esas Veriş Miktarı (UEVM) Santral Listesi",
                "en": "Injection Quantity Powerplant Listing",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/injection-quantity",
        },
        "pp-list": {
            "category": "Listeleme",
            "title": {
                "tr": "Santral Listeleme",
                "en": "Powerplant listing",
            },
            "desc": {
                "tr": "Santral Listeleme",
                "en": "Powerplant listing",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/real-time-generation",
        },
        "gen-org": {
            "category": "Listeleme",
            "title": {
                "tr": "Organizasyon Listesi",
                "en": "Organization Listing",
            },
            "desc": {
                "tr": "Tanımlı organizasyonların listesi",
                "en": "Organization Listing",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/planning/final-daily-production-program-fdpp",
        },
        "region-list": {
            "category": "Listeleme",
            "title": {
                "tr": "Bölge Listesi",
                "en": "Region Listing",
            },
            "desc": {
                "tr": "Bölge listesi",
                "en": "Region Listing",
            },
            "url": "https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_region-list",
        },
        "mms-message-type-list": {
            "category": "Listeleme",
            "title": {
                "tr": "Piyasa Mesaj Sistemi Mesaj Tipi Listesi",
                "en": "Market Message System Message Type List",
            },
            "desc": {
                "tr": "Piyasa Mesaj Sistemi Mesaj Tipi Listesi",
                "en": "Market Message System Message Type List",
            },
            "url": "https://seffaflik.epias.com.tr/electricity-service/technical/tr/index.html#_umm-message-type-list",
        },
        "gen-uevcb": {
            "category": "Listeleme",
            "title": {
                "tr": "Uevçb Listeleme",
                "en": "Injection/Withdrawal Unit Listing",
            },
            "desc": {
                "tr": "Verilen organizasyon idye ait UEVÇBlerin listesini döner",
                "en": "Injection/Withdrawal Unit list by the given organization id",
            },
            "url": "https://seffaflik.epias.com.tr/electricity-service/technical/en/index.html#_uevcb-list",
        },
        "lic-pp-list": {
            "category": "Elektrik Üretim",
            "title": {
                "tr": "Lisanslı Santral Yatırımları",
                "en": "Licenced Power Plant Investments",
            },
            "desc": {
                "tr": "Enerji İşleri Genel Müdürlüğü tarafından ön kabulü tamamlanmış ve devreye alınmış elektrik üretim tesislerinin aylık listesidir.",
                "en": "It is the monthly list of electricity generation facilities that are pre-approved and put into operation by the General Directorate of Energy Affairs.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-generation/licenced-power-plant-investments",
        },
        "load-plan": {
            "category": "Tüketim Tahmin",
            "title": {
                "tr": "Yük Tahmin Planı",
                "en": "Load Forecast Plan",
            },
            "desc": {
                "tr": "Bir sonraki gün için yapılan saatlik talep miktarıdır.",
                "en": "Total hourly power consumption forecast plans for the next day.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-consumption/forecast/load-forecast-plan",
        },
        "rt-cons": {
            "category": "Gerçekleşen Tüketim",
            "title": {
                "tr": "Gerçek Zamanlı Tüketim",
                "en": "Real Time Consumption",
            },
            "desc": {
                "tr": "Anlık olarak gerçekleşen tüketim değerinin saatlik bazda gösterildiği veridir.",
                "en": "It is the data that shows the instantaneous consumption value on an hourly basis.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/real-time-consumption",
        },
        "uecm": {
            "category": "Gerçekleşen Tüketim",
            "title": {
                "tr": "Uzlaştırmaya Esas Çekiş Miktarı (UEÇM)",
                "en": "Withdrawal Quantity",
            },
            "desc": {
                "tr": "Uzlaştırmaya esas çekiş birimlerinin, bir uzlaştırma dönemi içinde saatlik olarak sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti",
                "en": "The data set regarding total hourly energy withdrawal quantity of withdrawal units",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/withdrawal-quantity",
        },
        "st-uecm": {
            "category": "Gerçekleşen Tüketim",
            "title": {
                "tr": "Serbest Tüketici Uzlaştırmaya Esas Çekiş Miktarı",
                "en": "Eligible Customer Withdrawal Quantity",
            },
            "desc": {
                "tr": "Serbest tüketici hakkını kullananların, bir uzlaştırma dönemi içinde saatlik olarak sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti",
                "en": "The data set regarding total hourly energy withdrawal quantity of eligible customers",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/eligible-customer-withdrawal-quantity",
        },
        "su-uecm": {
            "category": "Gerçekleşen Tüketim",
            "title": {
                "tr": "Tedarik Yükümlülüğü Kapsamındaki Uzlaştırmaya Esas Çekiş Miktarı (UEÇM)",
                "en": "Withdrawal Quantity Under Supply Liability",
            },
            "desc": {
                "tr": "Uzlaştırmaya esas çekiş birimlerinin, tedarik yükümlülüğü kapsamında sistemden aldığı enerji miktarlarının toplam değerine ilişkin veri seti",
                "en": "The data set regarding total energy withdrawal quantity under supply liability of withdrawal units.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-consumption/ex-post-consumption/withdrawal-quantity-under-supply-liability",
        },
        "wind-forecast": {
            "category": "Üretim",
            "title": {
                "tr": "RES Üretim ve Tahmin",
                "en": "WPP Generation and Forecast",
            },
            "desc": {
                "tr": "Türkiye geneli izlenebilen RES’lerin toplam güç üretimi ve tahiminidir.Veriler rüzgar gücü izleme ve tahmin merkezinden temin edilmektedir. Veriler 10 dk arayla güncellenmektedir. Q5, Q25,Q75,Q95 tahmin aralıklarını ifade etmektedir. Band tahmin aralıkları minimum ve maksimum risk senaryolarına göre oluşturulmuştur.",
                "en": "It is the total power production and estimation of WPPs that can be monitored throughout Turkey. The data is obtained from the wind power monitoring and estimation center. Data is updated every 10 minutes. Q5, Q25, Q75, Q95 refer to the prediction intervals. Band prediction intervals are created according to minimum and maximum risk scenarios.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/wpp-generation-and-forecast",
        },
        # ## YEKDEM Santral Listesi
        "ren-pp-list": {
            "category": "Listeleme",
            "title": {
                "tr": "YEKDEM Santral Listesi",
                "en": "Licensed Power Plant List",
            },
            "desc": {
                "tr": "YEKDEM Santral Listesi",
                "en": "Licensed Power Plant List",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/licensed-generation-amount/real-time-generation",
        },
        # ## YEKDEM Gerçek Zamanlı Üretim
        "ren-rt-gen": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Gerçek Zamanlı Üretim",
                "en": "YEKDEM Real-Time Generation",
            },
            "desc": {
                "tr": "Lisanslı YEKDEM santrallerine ait elektrik üretiminin kaynak bazında saatlik gösterimine ilişkin veri seti.",
                "en": "The data set regarding hourly electricity generation quantity of licensed power plants within the scope of Renewable Energy Support Mechanism (YEKDEM)",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/licensed-generation-amount/real-time-generation",
        },
        "ren-uevm": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Uzlaştırma Esas Veriş Miktarı (UEVM)",
                "en": "YEKDEM Injection Quantity",
            },
            "desc": {
                "tr": "YEKDEM kapsamındaki lisanslı santrallerin kaynak bazında saatlik olarak uzlaştırmaya esas veriş değerlerine ilişkin veri seti.",
                "en": "The data set regarding hourly electricity injection quantity based on settlement of licensed power plants within the scope of Renewable Energy Support Mechanism (YEKDEM).",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/licensed-generation-amount/injection-quantity",
        },
        # ## Lisanssız Üretim
        "ren-ul-gen": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Lisanssız Üretim Miktarı",
                "en": "YEKDEM License Exempt Generation Feed-In Amount",
            },
            "desc": {
                "tr": "YEKDEM kapsamındaki lisanssız santrallerin kaynak bazında saatlik olarak uzlaştırmaya esas lisanssız veriş değerleridir.",
                "en": "These are the unlicensed data values of unlicensed power plants within the scope of YEKDEM for hourly reconciliation on a resource basis.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/license-exempt-generation-feed-in-amount",
        },
        "ren-ul-cost": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Lisanssız Üretim Bedeli",
                "en": "YEKDEM License Exempt Generation Feed-In Cost",
            },
            "desc": {
                "tr": "İlgili fatura dönemi için YEKDEM kapsamındaki lisanssız üretim santrallerine sahip katılımcılara ödenecek YEK bedelini (TL) ifade etmektedir.",
                "en": "It represents the RES fee (TL) to be paid for owning unlicensed generation plants within the scope of YEKDEM for the relevant invoice period.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/license-exempt-generation-feed-in-cost",
        },
        "ren-lic-cost": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEK Bedeli (YEKBED)",
                "en": "YEKDEM Licensed Generation Feed-In Cost",
            },
            "desc": {
                "tr": "İlgili fatura dönemi için YEKDEM kapsamındaki lisanssız üretim santrallerine sahip katılımcılara ödenecek YEK bedelini (TL) ifade etmektedir.",
                "en": "Hourly aggregate monetary value derived by the multiplication of feed-in energy quantity that is generated by licensed facilities under the renewables support mechanism and feed-in tariff prices. CBRT's fx buying rate of the date of energy feed-in is taken basis for TL currency conversion.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/licensed-generation-feed-in-cost",
        },
        "ren-income": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEK Geliri (YG)",
                "en": "YEKDEM Renewables Support Mechanism Income",
            },
            "desc": {
                "tr": "YEKDEM gelirine ilişkin veri setidir.",
                "en": "The data set regarding the Renewables Support Mechanism Income.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/renewables-support-mechanism-income",
        },
        "ren-total-cost": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Toplam Gider (YEKTOB)",
                "en": "YEKDEM Total Cost (Licensed & License Exempt)",
            },
            "desc": {
                "tr": "İlgili fatura dönemi için YEKDEM kapsamındaki hem lisanslı hem de lisanssız üretim santraline sahip katılımcılara ödenecek toplam YEK bedelini (TL) ifade eder.",
                "en": "The data set regarding the total renewable energy amount to be paid to licensed and unlicensed power plants within the scope of Renewable Energy Support Mechanism.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/total-cost-licensed-license-exempt",
        },
        "ren-capacity": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Kurulu Güç",
                "en": "YEKDEM Installed Capacity",
            },
            "desc": {
                "tr": "YEKDEM kapsamındaki üretim tesislerinin kurulu güç miktarıdır. Lisanslı kurulu güç bilgileri EPİAŞ’a kayıtlı santraller olup, lisanssız kurulu güç bilgisi dağıtım şirketlerinden temin edilmektedir.",
                "en": "Total installed capacity of the generation facilities under renewables support mechanism. Licenced installation capacities are registered to EXIST, unlicenced installation capacities are fetched from the distribution corporations.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/installed-capacity",
        },
        "ren-unit-cost": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Birim Maliyeti",
                "en": "YEKDEM Unit Cost",
            },
            "desc": {
                "tr": "Tedarik edilen birim enerji miktarı başına, hesaplanan YEKDEM maliyetidir. YEKDEM birim maliyeti ilgili aylar için versiyonlu olarak yayımlanmaktadır. Bir fatura döneminde, YEKDEM gelirinin YEK toplam bedelinden fazla olması durumunda, Yenilenebilir Enerji Kaynaklarının Belgelendirilmesi ve Desteklenmesine İlişkin Yönetmenliğin 13üncü maddesinin dördüncü fıkrası uyarınca hesaplama yapılmaktadır.",
                "en": "It is the cost of Renewable Support Mechanism calculated per unit of energy supplied.Renewable Support Mechanism unit cost is published in versions for the relevant months.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/unit-cost",
        },
        "ren-participant-list": {
            "category": "YEKDEM",
            "title": {
                "tr": "YEKDEM Katılımcı Listesi",
                "en": "YEKDEM Renewables Support Mechanism (RSM) Participant List",
            },
            "desc": {
                "tr": "İlgili yıl içerisinde Yenilenebilir Enerji Destekleme Mekanizmasına dahil olan lisanslı üretim santraline sahip tüzel kişilerin listesidir. 2020 yılından itibaren “Önceki Yıl gerçekleştirilen Üretim (MWh)” yayınlanmamaktadır.",
                "en": "It is a list of legal entities with a licensed power plant involved in the Renewable energy support mechanism within the relevant year. Since 2020, Previous year's production (Mwh) has not been published.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/renewables-support-mechanism/unit-cost",
        },
        "zero-balance": {
            "category": "İletim",
            "title": {
                "tr": "Sıfır Bakiye Düzeltme Tutarı Aylık",
                "en": "Monthly Zero Balance Adjustment",
            },
            "desc": {
                "tr": "Sıfır bakiye düzeltme tutarı ve bileşenlerine ait aylık tutarlara ilişkin veri seti",
                "en": "The data set regarding montly amounts of zero balance adjustment and its components.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/zero-balance-adjustment/monthly-zero-balance-adjustment",
        },
        "iskk": {
            "category": "İletim",
            "title": {
                "tr": "İletim Sistemi Kayıp Katsayısı (ISKK)",
                "en": "Transmission Loss Factor",
            },
            "desc": {
                "tr": "Uzlaştırma dönemi bazında iletim sistemi veriş ve çekiş miktarları arasındaki farkın veriş miktarına oranlanmasıyla hesaplanan iletim sistemi kayıp katsayısına ilişkin veri seti.",
                "en": "The data set regarding the ratio of difference between injection to the system and withdrawal from the system, to injection to the system.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/congestion/transmission-loss-factor",
        },
        "congestion-cost": {
            "category": "İletim",
            "title": {
                "tr": "Kısıt Maliyeti",
                "en": "Congestion Cost",
            },
            "desc": {
                "tr": "Şehir bazında 1 kodlu Yük Alma ve Yük Atma Talimatlarının toplam mali değerine ilişkin veri seti.",
                "en": "The data set regarding the total congestion cost of up and down regulation instructions with code 1.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/congestion/congestion-cost",
        },
        "eic-x-org-list": {
            "category": "İletim",
            "title": {
                "tr": "ENTSO-E (X) Kodları",
                "en": "ENTSO-E (X) Codes",
            },
            "desc": {
                "tr": "Avrupa Elektrik İletim Sistemi İşletmecileri Ağı’nın piyasadaki organizasyonlara, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodudur.",
                "en": "It is the Energy Identification Code defined by the European Network of Electricity Transmission System Operators to the organizations in the market in a format in accordance with European standards.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/general-data/entso-e-x-codes",
        },
        "eic-w-org-list": {
            "category": "İletim",
            "title": {
                "tr": "ENTSO-E (W) Kodları",
                "en": "ENTSO-E (W) Codes",
            },
            "desc": {
                "tr": "Avrupa Elektrik İletim Sistemi İşletmecileri Ağının piyasadaki Santral ve UEVÇBlere, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodudur.",
                "en": "The EIC code of type W is used to identify objects to be used for production, consumption or storage of energy.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/general-data/entso-e-w-codes",
        },
        "eic-w-uevcb-list": {
            "category": "İletim",
            "title": {
                "tr": "ENTSO-E (W) Kodları UEVÇB",
                "en": "ENTSO-E (W) Codes UEVCB",
            },
            "desc": {
                "tr": "Avrupa Elektrik İletim Sistemi İşletmecileri Ağının piyasadaki Santral ve UEVÇBlere, Avrupa standartlarına uygun formatta tanımladığı Enerji Tanımlama Kodudur.",
                "en": "The EIC code of type W is used to identify objects to be used for production, consumption or storage of energy.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/general-data/entso-e-w-codes",
        },
        "international-line-events": {
            "category": "İletim",
            "title": {
                "tr": "Enterkonneksiyon Arıza Bakım Bildirimleri",
                "en": "Interconnection Failure and Maintenance Notices",
            },
            "desc": {
                "tr": "TCAT'ten temin edilen uluslararası hatlarda oluşan kesinti bilgileri sayfasıdır.",
                "en": "This is the page for information on international lines obtained from TCAT.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-failure-and-maintenance-notices",
        },
        "tcat-pre-year-forecast": {
            "category": "İletim",
            "title": {
                "tr": "Enterkonneksiyon Kapasitesine İlişkin Yıl Öncesi Tahminler",
                "en": "Yearly Forecasts for Interconnection Capacity",
            },
            "desc": {
                "tr": "Transfer yönü kapsamında yıl öncesi Net Transfer Kapasitesi, Kullanıma Açık Kapasite ve Tahsis Edilmiş Kapasite değerlerinin yıl öncesi tahminlerine ilişkin veri seti.",
                "en": "The data set regarding the pre-year forecasts of Net Transfer Capacity, Available Capacity and Allocated Capacity values according to transfer directions.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/forecasts-for-interconnection-capacity/yearly-forecasts-for-interconnection-capacity",
        },
        "tcat-pre-month-forecast": {
            "category": "İletim",
            "title": {
                "tr": "Enterkonneksiyon Kapasitesine İlişkin Ay Öncesi Tahminler",
                "en": "Monthly Forecasts for Interconnection Capacity",
            },
            "desc": {
                "tr": "Transfer yönü kapsamında ay öncesi Net Transfer Kapasitesi, Kullanıma Açık Kapasite ve Tahsis Edilmiş Kapasite değerlerinin yıl öncesi tahminlerine ilişkin veri seti.",
                "en": "The data set regarding the pre-month forecasts of Net Transfer Capacity, Available Capacity and Allocated Capacity values according to transfer directions.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/forecasts-for-interconnection-capacity/monthly-forecasts-for-interconnection-capacity",
        },
        # ##Enterkonneksiyon Hat Kapasiteleri
        "line-capacities": {
            "category": "İletim",
            "title": {
                "tr": "Hat Kapasiteleri",
                "en": "Interconnection Line Capacities",
            },
            "desc": {
                "tr": "Enterkonneksiyonlara ait hat toplam kapasite ve Kullanıma açık kapasite değerleri gösterilmektedir.",
                "en": "Total Capacity and Available Capacity values are shown on the page.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacities",
        },
        "capacity-demand": {
            "category": "İletim",
            "title": {
                "tr": "Kapasite Talepleri",
                "en": "Interconnection Line - Capacity Requests",
            },
            "desc": {
                "tr": "Kapasite ihalelerine ait talepleri ve tahsis edilen kapasiteleri gösterir.",
                "en": "Shows the requests for capacity auctions and allocated capacities.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacity-requests",
        },
        "nominal-capacity": {
            "category": "İletim",
            "title": {
                "tr": "Nomine Kapasite",
                "en": "Nomine Capacity",
            },
            "desc": {
                "tr": "Nomine Kapasite değerleri ithalat (satış miktarları) ve ihracat(alış miktarı) için yapılan ikili anlaşmaları göstermektedir.",
                "en": "Nomine Capacity values show the bilateral agreements made for import (sales quantities) and exports (purchased quantities).",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/nomine-capacity",
        },
        "intl-direction-list": {
            "category": "İletim",
            "title": {
                "tr": "Hat Kapasiteleri Yön Listesi",
                "en": "Interconnection Line Capacities Direction Listing",
            },
            "desc": {
                "tr": "Hat Kapasiteleri Yön Listesi",
                "en": "Interconnection Line Capacities Direction Listing",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacities",
        },
        "intl-capacity-demand-direction-list": {
            "category": "İletim",
            "title": {
                "tr": "Kapasite Talepleri Yön Listesi",
                "en": "Capacity Requests Direction Listing",
            },
            "desc": {
                "tr": "Kapasite Talepleri Yön Listesi",
                "en": "Capacity Requests Direction Listing",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-transmission/interconnection-line-capacity-requests",
        },
        "mms": {
            "category": "PMS",
            "title": {
                "tr": "PİYASA MESAJ SİSTEMİ",
                "en": "MARKET MESSAGE SYSTEM",
            },
            "desc": {
                "tr": "İlgili santralin arıza veya bakım bilgileridir.",
                "en": "It is the outage or maintenance information of the relevant power plant.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/market-message-system",
        },
        "mms-pp-list": {
            "category": "Listeleme",
            "title": {
                "tr": "PMS Organizasyona Göre Santral Listeleme",
                "en": "MMS Power Plant Listing by Organization",
            },
            "desc": {
                "tr": "PMS Organizasyona Göre Santral Listeleme.",
                "en": "MMS Power Plant Listing by Organization.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/market-message-system",
        },
        "mms-uevcb-list": {
            "category": "Listeleme",
            "title": {
                "tr": "PMS UEVÇB'ye Göre Santral Listeleme",
                "en": "MMS Power Plant Listing by UEVCB",
            },
            "desc": {
                "tr": "PMS UEVÇB'ye Göre Santral Listeleme.",
                "en": "MMS Power Plant Listing by UEVCB.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/market-message-system",
        },
        # ## Gün bilgileri
        "date-init": {
            "category": "Genel",
            "title": {
                "tr": "Şeffaflık Tarih Bilgisi",
                "en": "Transparency Date Information",
            },
            "desc": {
                "tr": "Şeffaflık Tarih Bilgisi",
                "en": "Transparency Date Information",
            },
            "url": "https://seffaflik.epias.com.tr/electricity-service/technical/en/index.html#_date-init",
        },
        # ## Piyasa Katılımcıları
        "market-participants": {
            "category": "Listeleme",
            "title": {
                "tr": "Piyasa Katılımcıları",
                "en": "Market Participants",
            },
            "desc": {
                "tr": "Piyasa Katılımcıları’nın GÖP, GİP, VEP, YEK-G piyasalarına katılım durumunu belirtir. Ayrıca Tüzel kişilik olarak firmanın aktiflik/pasiflik durumunu bildirir.",
                "en": "It displays the participation status of market Participants in DAM, IDM, PFM, YEK-G markets. It also reports the activity status the participants.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/general-data/market-participants",
        },
        "market-participants-organization-list": {
            "category": "Listeleme",
            "title": {
                "tr": "Piyasa Katılımcıları Organizasyon Listesi",
                "en": "Market Participants Organization List",
            },
            "desc": {
                "tr": "Piyasa Katılımcıları’nın organizasyon listesi.",
                "en": "Market Participants organization list.",
            },
            "url": "https://seffaflik.epias.com.tr/electricity/electricity-markets/general-data/market-participants",
        },
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
