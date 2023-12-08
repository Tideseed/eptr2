def get_path_map(just_call_keys: bool = False):
    path_map = {
        "call": {
            ## GÖP İşlem Hacmi
            "dam-volume": {
                "prefix": "data",
                "prev": "dam",
                "label": "day-ahead-market-trade-volume",  ## GÖP İşlem Hacmi
            },
            ## Fiyattan bağımsız satış teklifi
            "pi-offer": {
                "prefix": "data",
                "prev": "dam",
                "label": "price-independent-offer",  ## Fiyattan bağımsız satış teklifi
            },
            ## Fiyattan bağımsız alış teklifi
            "pi-bid": {
                "prefix": "data",
                "prev": "dam",
                "label": "price-independent-bid",
            },
            ## Arz talep
            "supply-demand": {
                "prefix": "data",
                "prev": "dam",
            },
            ## GÖP Teklif Edilen Alış Miktarları
            "dam-bid": {
                "prefix": "data",
                "prev": "dam",
                "label": "submitted-bid-order-volume",
            },
            ## GÖP Teklif Edilen Satış Miktarları
            "dam-offer": {
                "prefix": "data",
                "prev": "dam",
                "label": "submitted-sales-order-volume",
            },
            ## GÖP Blok Alış Miktarı
            "dam-block-bid": {
                "prefix": "data",
                "prev": "dam",
                "label": "amount-of-block-buying",
            },
            ## GÖP Blok Satış Miktarı
            "dam-block-offer": {
                "prefix": "data",
                "prev": "dam",
                "label": "amount-of-block-selling",
            },
            ## GÖP Esnek Alış Teklif Miktarı Listeleme Servisi
            "dam-flexible-bid": {
                "prefix": "data",
                "prev": "dam",
                "label": "flexible-offer-buying-quantity",
            },
            ## GÖP Esnek Satış Miktarı
            "dam-flexible-offer": {
                "prefix": "data",
                "prev": "dam",
                "label": "flexible-offer-selling-quantity",
            },
            ## GÖP Esnek Teklif Eşleşme Miktarları
            "dam-flexible-matching": {
                "prefix": "data",
                "prev": "dam",
                "label": "matched-flexible-offer-quantity",
            },
            ## GÖP Eşleşme Miktarı
            "dam-clearing": {
                "prefix": "data",
                "prev": "dam",
                "label": "clearing-quantity",
            },
            ## Göp Eşleşme Miktarı Organizasyon Listeleme
            "dam-clearing-org-list": {
                "prefix": "data",
                "prev": "dam",
                "label": "clearing-quantity-organization-list",
            },
            ## GÖP Fark Tutarı
            "dam-diff": {
                "prefix": "data",
                "prev": "dam",
                "label": "side-payments",
            },
            ## GİP Ağırlıklı Ortalama Fiyat
            "wap": {
                "prefix": "data",
                "prev": "idm",
                "label": "weighted-average-price",
            },
            ## GİP Eşleşme Miktarı
            "idm-qty": {
                "prefix": "data",
                "prev": "idm",
                "label": "matching-quantity",
            },
            ## GİP Min - Maks Alış Teklif Fiyatı
            "idm-mm-bid": {
                "prefix": "data",
                "prev": "idm",
                "label": "min-max-bid-price",
            },
            ## GİP Min - Maks Satış Teklif Fiyatı
            "idm-mm-offer": {
                "prefix": "data",
                "prev": "idm",
                "label": "min-max-sales-offer-price",
            },
            ## GİP Min - Maks Eşleşme Fiyatı
            "idm-mm-matching": {
                "prefix": "data",
                "prev": "idm",
                "label": "min-max-matching-price",
            },
            ## GİP İşlem Hacmi
            "idm-volume": {
                "prefix": "data",
                "prev": "idm",
                "label": "trade-value",
            },
            ## GİP İşlem Akışı
            "idm-log": {
                "prefix": "data",
                "prev": "idm",
                "label": "transaction-history",
            },
            ## GİP Teklif Edilen Alış Satış Miktarları
            "idm-ob-qty": {
                "prefix": "data",
                "prev": "idm",
                "label": "bid-offer-quantities",
            },
            ## SMF
            "smp": {"prefix": "data", "prev": "bpm", "label": "system-marginal-price"},
            ## SMF Yön
            "smp-dir": {"prefix": "data", "prev": "bpm", "label": "system-direction"},
            ## YAL Talimat Miktarı
            "bpm-up": {"prefix": "data", "prev": "bpm", "label": "order-summary-up"},
            ## YAT Talimat Miktarı
            "bpm-down": {
                "prefix": "data",
                "prev": "bpm",
                "label": "order-summary-down",
            },
            ## İkili Anlaşma (İA) Alış Miktarı
            "bi-long": {
                "prefix": "data",
                "prev": "bilateral-contracts",
                "label": "bilateral-contracts-bid-quantity",
            },
            ## İkili Anlaşma (İA) Satış Miktarı
            "bi-short": {
                "prefix": "data",
                "prev": "bilateral-contracts",
                "label": "bilateral-contracts-offer-quantity",
            },
            ### EÜAŞ - GTŞ İkili Anlaşmalar
            "bi-euas": {
                "prefix": "data",
                "prev": "bilateral-contracts",
                "label": "amount-of-bilateral-contracts",
            },
            ## Dengesizlik Miktarı
            "imb-qty": {
                "prefix": "data",
                "prev": "imbalance",
                "label": "imbalance-quantity",
            },
            ## Dengesizlik Tutarı
            "imb-vol": {
                "prefix": "data",
                "prev": "imbalance",
                "label": "imbalance-amount",
            },
            ## Dengeden Sorumlu Grup (DSG) Dengesizlik Miktarı
            "imb-qty-g": {
                "prefix": "data",
                "prev": "imbalance",
                "label": "dsg-imbalance-quantity",
            },
            ## DSG Organizasyon Listesi
            "imb-org-list": {
                "prefix": "data",
                "prev": "imbalance",
                "label": "dsg-organization-list",
            },
            ## PTF
            "mcp": {"prefix": "data", "prev": "dam"},
            ## Kesinleşmemiş PTF
            "interim-mcp": {"prefix": "data", "prev": "dam"},
            ## Kesinleşmemiş PTF yayınlandı mı?
            "interim-mcp-status": {
                "prefix": "data",
                "prev": "dam",
                "label": "interim-mcp-published-status",
            },
            ### PTF-SMF-SDF
            "mcp-smp-imb": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "ptf-smf-sdf",
            },
            ## DGP Talimat Ağırlıklı Ortalama
            "bpm-orders-w-avg": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "dgp-talimat-agr-ort",
            },
            "date-init": {
                "prefix": "main",
                "prev": "electricity-service",
                "label": "date-init",
            },
            ## Piyasa Katılımcıları
            "market-participants": {
                "prefix": "data",
                "prev": "general-data",
                "label": "market-participants",
            },
            ##Piyasa Katılımcıları Organizasyon
            "market-participants-organization-list": {
                "prefix": "data",
                "prev": "general-data",
                "label": "market-participants-organization-filter-list",
            },
        },
        ## category
        "idm": {"prev": "markets"},
        "dam": {"prev": "markets"},
        "bpm": {"prev": "markets"},
        "bilateral-contracts": {"prev": "markets"},
        "general-data": {"prev": "markets"},
        "imbalance": {"prev": "markets"},
        "markets": {"prev": "electricity-service"},
        #### services
        "electricity-service": {"next": "version"},
        "reporting-service": {"next": "version"},
        "version": {"label": "v1"},
    }

    if just_call_keys:
        return list(path_map["call"].keys())
    else:
        call_d = path_map.pop("call")
        return {**path_map, **call_d}


def get_total_path(key: str, join_path: bool = True):
    d = get_path_map().get(key, None)
    if d is not None:
        total_path = [d.get("label", key)]
        if d.get("prefix", None) is not None:
            total_path = [d["prefix"]] + total_path
        if d.get("suffix", None) is not None:
            total_path = total_path + [d["suffix"]]

        if d.get("prev", None) is not None:
            total_path = get_total_path(key=d["prev"], join_path=False) + total_path
        if d.get("next", None) is not None:
            total_path += get_total_path(key=d["next"], join_path=False)

        return "/".join(total_path) if join_path else total_path
    else:
        raise Exception("Key not found in path map.")


def get_call_method(key):
    """
    Get the call method for a given key. If the key is in the list of keys that require GET method, return GET, else return POST.
    """
    get_methods = [
        "date-init",
        "interim-mcp-status",
        "market-participants-organization-list",
    ]

    if key in get_methods:
        return "GET"
    else:
        return "POST"
