import re


def get_path_template(template: str, label: str):

    template_map_d = {
        "ng-sgp": {
            "prefix": "data",
            "prev": "sgp",
            "root": "natural-gas",
        },
        "ng-general": {
            "prefix": "data",
            "prev": "general-data",
            "root": "natural-gas",
        },
        "ra": {
            "prefix": "data",
            "prev": "retroactive-adjustment",
        },
    }

    d = template_map_d[template]
    d["label"] = label

    return d


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
            ## DGP Talimat Ağırlıklı Ortalama
            "bpm-orders": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "dgp-talimat",
            },
            ## KGÜP
            "kgup": {
                "prefix": "data",
                "prev": "generation",
                "label": "dpp",
            },
            ## KUDUP
            "kudup": {
                "prefix": "data",
                "prev": "generation",
                "label": "sbfgp",
            },
            ## EAK
            "eak": {
                "prefix": "data",
                "prev": "generation",
                "label": "aic",
            },
            ## Gerçek Zamanlı Üretim
            "rt-gen": {
                "prefix": "data",
                "prev": "generation",
                "label": "realtime-generation",
            },
            ## UEVM
            "uevm": {
                "prefix": "data",
                "prev": "generation",
                "label": "injection-quantity",
            },
            ## Santral Listeleme
            "pp-list": {
                "prefix": "data",
                "prev": "generation",
                "label": "powerplant-list",
            },
            ## Santral Listeleme
            "uevm-pp-list": {
                "prefix": "data",
                "prev": "generation",
                "label": "injection-quantity-powerplant-list",
            },
            ## Üretici Organizasyon Listesi
            "gen-org": {
                "prefix": "data",
                "prev": "generation",
                "label": "organization-list",
            },
            ## Bölge Listesi
            "region-list": {
                "prefix": "data",
                "prev": "generation",
                "label": "region-list",
            },
            ## PMS Mesaj Tipi Listesi
            "mms-message-type-list": {
                "prefix": "data",
                "prev": "markets",
                "label": "umm-message-type-list",
            },
            ## PMS Bölge Listeleme Servisi
            "mms-region-list": {
                "prefix": "data",
                "prev": "markets",
                "label": "umm-region-list",
            },
            ## Üretici UEVÇB Listesi
            "gen-uevcb": {
                "prefix": "data",
                "prev": "generation",
                "label": "uevcb-list",
            },
            ## Lisanslı Santral Yatırımları
            "lic-pp-list": {
                "prefix": "data",
                "prev": "generation",
                "label": "licensed-powerplant-investment-list",
            },
            ## Talep Tahmini Listeleme Servisi
            "long-term-demand-forecast": {
                "prefix": "data",
                "prev": "consumption",
                "label": "demand-forecast",
            },
            ## Tüketici Sayısı Servisi
            "consumer-breakdown": {
                "prefix": "data",
                "prev": "consumption",
                "label": "consumer-quantity",
            },
            ## Tüketim Miktarları (İl ve Profil Bazında)
            "consumption-breakdown": {
                "prefix": "data",
                "prev": "consumption",
                "label": "consumption-quantity",
            },
            ## Dağıtım Bölgesi Servisi
            "distribution-region-list": {
                "prefix": "data",
                "prev": "consumption",
                "label": "distribution-region",
            },
            ## Yük Tahmin Planı
            "load-plan": {
                "prefix": "data",
                "prev": "consumption",
                "label": "load-estimation-plan",
            },
            ## Gerçek Zamanlı Tüketim
            "rt-cons": {
                "prefix": "data",
                "prev": "consumption",
                "label": "realtime-consumption",
            },
            ## UEÇM
            "uecm": {
                "prefix": "data",
                "prev": "consumption",
                "label": "uecm",
            },
            ## Serbest Tüketici UEÇM
            "st-uecm": {
                "prefix": "data",
                "prev": "consumption",
                "label": "st-uecm",
            },
            ## Tedarik Yükümlülüğü Kapsamındaki UEÇM
            "su-uecm": {
                "prefix": "data",
                "prev": "consumption",
                "label": "withdrawal-quantity-under-supply-liability",
            },
            ## Yan Hizmetler - Primer Frekans Rezerv Miktarı
            "anc-pf-qty": {
                "prefix": "data",
                "prev": "ancillary-services",
                "label": "primary-frequency-capacity-amount",
            },
            ## Yan Hizmetler - Primer Frekans Kapasite fiyatı (PFK)
            "anc-pfk": {
                "prefix": "data",
                "prev": "ancillary-services",
                "label": "primary-frequency-capacity-price",
            },
            ## Yan Hizmetler - Sekonder Frekans Rezerv Miktarı
            "anc-sf-qty": {
                "prefix": "data",
                "prev": "ancillary-services",
                "label": "secondary-frequency-capacity-amount",
            },
            ## Yan Hizmetler - Sekonder Frekans Kapasite fiyatı (SFK)
            "anc-sfk": {
                "prefix": "data",
                "prev": "ancillary-services",
                "label": "secondary-frequency-capacity-price",
            },
            ## YEKDEM RES Üretim ve Tahmin Listeleme
            "wind-forecast": {
                "prefix": "data",
                "prev": "renewables",
                "label": "res-generation-and-forecast",
            },
            ## YEKDEM Santral Listesi
            "ren-pp-list": {
                "prefix": "data",
                "prev": "renewables",
                "label": "licensed-powerplant-list",
            },
            ## YEKDEM Gerçek Zamanlı Üretim
            "ren-rt-gen": {
                "prefix": "data",
                "prev": "renewables",
                "label": "licensed-realtime-generation",
            },
            ## YEKDEM UEVM
            "ren-uevm": {
                "prefix": "data",
                "prev": "renewables",
                "label": "renewable-sm-licensed-injection-quantity",
            },
            ## Lisanssız Üretim
            "ren-ul-gen": {
                "prefix": "data",
                "prev": "renewables",
                "label": "unlicensed-generation-amount",
            },
            ## Lisanssız Üretim Bedeli
            "ren-ul-cost": {
                "prefix": "data",
                "prev": "renewables",
                "label": "unlicensed-generation-cost",
            },
            ## YEK Bedeli
            # "yekbed": {"redirect": "ren-lic-cost"},
            "ren-lic-cost": {
                "prefix": "data",
                "prev": "renewables",
                "label": "licensed-generation-cost",
            },
            ## YEK Geliri
            "ren-income": {
                "prefix": "data",
                "prev": "renewables",
                "label": "renewables-support-mechanism-income",
            },
            ## YEK Toplam Gider (YEKTOB)
            "ren-total-cost": {
                "prefix": "data",
                "prev": "renewables",
                "label": "total-cost",
            },
            ## Lisanssız Üretim Bedeli
            "ren-capacity": {
                "prefix": "data",
                "prev": "renewables",
                "label": "new-installed-capacity",
            },
            ## YEKDEM Birim Maliyeti
            "ren-unit-cost": {
                "prefix": "data",
                "prev": "renewables",
                "label": "unit-cost",
            },
            ## YEKDEM Katılımcı Listesi
            "ren-participant-list": {
                "prefix": "data",
                "prev": "renewables",
                "label": "renewables-participant",
            },
            ## Sıfır Bakiye Düzeltme Tutarı
            "zero-balance": {
                "prefix": "data",
                "prev": "transmission",
                "label": "zero-balance",
            },
            ## İSKK
            "iskk": {
                "prefix": "data",
                "prev": "transmission",
                "label": "iskk-list",
            },
            ## Kısıt Maliyeti
            "congestion-cost": {
                "prefix": "data",
                "prev": "transmission",
                "label": "congestion-cost",
            },
            ##ENTSO-E (X) Kodları
            "eic-x-org-list": {
                "prefix": "data",
                "prev": "transmission",
                "label": "organization-list",
            },
            ##ENTSO-E (W) Kodları
            "eic-w-org-list": {
                "prefix": "data",
                "prev": "transmission",
                "label": "entso-w-organization",
            },
            ##ENTSO-E (W) Kodları UEVCB
            "eic-w-uevcb-list": {
                "prefix": "data",
                "prev": "transmission",
                "label": "entso-w-uevcb",
            },
            ## Enterkonneksiyon Arıza Bakım Bildirimleri
            "international-line-events": {
                "prefix": "data",
                "prev": "transmission",
                "label": "international-line-events",
            },
            ##Enterkonneksiyon Kapasitesine İlişkin Yıl Öncesi Tahminler
            "tcat-pre-year-forecast": {
                "prefix": "data",
                "prev": "transmission",
                "label": "tcat-pre-year-forecast",
            },
            ##Enterkonneksiyon Kapasitesine İlişkin Ay Öncesi Tahminler
            "tcat-pre-month-forecast": {
                "prefix": "data",
                "prev": "transmission",
                "label": "tcat-pre-month-forecast",
            },
            ##Enterkonneksiyon Hat Kapasiteleri
            "line-capacities": {
                "prefix": "data",
                "prev": "transmission",
                "label": "line-capacities",
            },
            ##Enterkonneksiyon Hat Kapasiteleri
            "capacity-demand": {
                "prefix": "data",
                "prev": "transmission",
                "label": "line-capacities",
            },
            ##Nomine Kapasite
            "nominal-capacity": {
                "prefix": "data",
                "prev": "transmission",
                "label": "nominal-capacity",
            },
            ##Enterkonneksiyon Hat Kapasiteleri Yön Listesi
            "intl-direction-list": {
                "prefix": "data",
                "prev": "transmission",
                "label": "line-capacities-direction",
            },
            ##Enterkonneksiyon Hat Kapasite Talepleri Yön Listesi
            "intl-capacity-demand-direction-list": {
                "prefix": "data",
                "prev": "transmission",
                "label": "line-capacities-direction",
            },
            ## Piyasa Mesaj Sistemi
            "mms": {
                "prefix": "data",
                "prev": "markets",
                "label": "market-message-system",
            },
            ## Organizasyona Göre Santral Listeleme (Piyasa Mesaj Sistemi)
            "mms-pp-list": {
                "prefix": "data",
                "prev": "markets",
                "label": "power-plant-list-by-organization-id",
            },
            ## UEVÇB'ye Göre Santral Listeleme (Piyasa Mesaj Sistemi)
            "mms-uevcb-list": {
                "prefix": "data",
                "prev": "markets",
                "label": "uevcb-list-by-power-plant-id",
            },
            ## İlçe Listeleme
            "district-list": {
                "prefix": "main",
                "prev": "electricity-service",
                "label": "district-list",
            },
            ## Profil Grubu Listeleme
            "profile-group-list": {
                "prefix": "data",
                "prev": "consumption",
                "label": "consumer-sector-list",
            },
            ## Şehir Listeleme
            "province-list": {
                "prefix": "main",
                "prev": "electricity-service",
                "label": "province-list",
            },
            ## Gün bilgileri
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
            ##Lisans Türüne Göre Katılımcı Sayısı
            "participant-count-based-upon-license-type": {
                "prefix": "data",
                "prev": "general-data",
                "label": "participant-count-based-upon-license-type",
            },
            ## Aktif Doluluk
            "dams-active-fullness": {
                "prefix": "data",
                "prev": "dams",
                "label": "active-fullness",
            },
            ## Günlük Kot
            "dams-daily-level": {
                "prefix": "data",
                "prev": "dams",
                "label": "daily-kot",
            },
            ## Aktif Hacim
            "dams-active-volume": {
                "prefix": "data",
                "prev": "dams",
                "label": "active-volume",
            },
            ## Günlük Hacim
            "dams-daily-volume": {
                "prefix": "data",
                "prev": "dams",
                "label": "daily-volume",
            },
            ## Havza Listesi
            "basin-list": {
                "prefix": "data",
                "prev": "dams",
                "label": "basin-list",
            },
            ## Baraj Listesi
            "dam-list": {
                "prefix": "data",
                "prev": "dams",
                "label": "dam-list",
            },
            ## Baraj Kot Min-Max
            "dams-level-minmax": {
                "prefix": "data",
                "prev": "dams",
                "label": "dam-kot",
            },
            ## Baraj Hacim Min-Max
            "dams-volume-minmax": {
                "prefix": "data",
                "prev": "dams",
                "label": "dam-volume",
            },
            ## Baraj Debi ve Kurulu Güç
            "dams-info": {
                "prefix": "data",
                "prev": "dams",
                "label": "flow-rate-and-installed-power",
            },
            ## Suyun Enerji Karşılığı
            "dams-water-energy-provision": {
                "prefix": "data",
                "prev": "dams",
                "label": "water-energy-provision",
            },
            # GİP Kontrat Özeti
            "idm-summary": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "idm-contract-summary",
            },
            # Elektrik Piyasa Hacimleri Fiziksel
            "electricity-market-quantity": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "electricity-market-volume-physically",
            },
            ## GİP Kontrat Listeleme Servisi
            "idm-contract-list": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "gip-kontrat",
            },
            ## GİP Teklif Listesi
            "idm-order-history": {
                "prefix": "data",
                "prev": "reporting-service",
                "label": "idm-order-list",
            },
            ## GDDK Dağıtım Liste
            "ra-distribution-list": get_path_template("ra", "distribution-list"),
            ## GDDK Sayaç Okuyan Kurum Liste
            "ra-organization-list": get_path_template("ra", "organization-list"),
            ## GDDK Profil Abone Grubu Liste Servisi
            "ra-spg-list": get_path_template("ra", "subscriber-profile-group-list"),
            ## GDDK Hacim Profil Abone Grubu Liste Servisi
            "ra-vspg-list": get_path_template(
                "ra", "volume-subscriber-profile-group-list"
            ),
            ## GDDK’ya Konu olan Sayaç Sayısı Listeleme Servisi
            "ra-meters": get_path_template(
                "ra", "meter-count-subject-to-retroactive-adjustment"
            ),
            ## GDDK’ya Konu olan Sayaç Hacim Verileri Listeleme Servisi (with Period)
            "ra-meter-volumes-period": get_path_template("ra", "meter-volume"),
            ## GDDK’ya Konu olan Sayaç Hacim Verileri Listeleme Servisi (with Version)
            "ra-meter-volumes-version": get_path_template("ra", "meter-volume"),
            ## GDDK Tutarı
            "ra-sum": get_path_template("ra", "retroactive-adjustment-sum"),
            ## Doğal Gaz Piyasa Katılımcıları
            "ng-participants": get_path_template("ng-general", "market-participant"),
            ## Doğal Gaz Katılımcı Listesi
            "ng-participant-list": get_path_template("ng-general", "participant-list"),
            ## İlave Dengeleyici Bildirimleri Listeleme Servisi
            "ng-balancing-notifications": get_path_template(
                "ng-sgp", "additional-notifications"
            ),
            ## Dengeleme Gazı Fiyatları (DGF) Listeleme Servisi
            "ng-balancing-price": get_path_template("ng-sgp", "balancing-gas-price"),
            ## Bakiye Sıfırlama Tutarı (BAST) Listeleme Servisi
            "ng-bast": get_path_template("ng-sgp", "bast"),
            ## 2 Kodlu İşlemler Listeleme Servisi
            "ng-blue-code-ops": get_path_template("ng-sgp", "blue-code-operation"),
            ## SGP Günlük Eşleşme Miktarı Listeleme Servisi
            "ng-daily-match-qty": get_path_template("ng-sgp", "daily-matched-quantity"),
            ## Günlük Referans Fiyatı (GRF) Listeleme Servisi
            "ng-drp": get_path_template("ng-sgp", "daily-reference-price"),
            ## SGP Günlük İşlem Hacmi Listeleme Servisi
            "ng-daily-trade-volume": get_path_template("ng-sgp", "daily-trade-volume"),
            ## 4 Kodlu İşlemler Listeleme Servisi
            "ng-code-four-ops": get_path_template("ng-sgp", "four-code-operation"),
            ## Geriye Dönük Düzeltme Kalemi (GDDK) Tutarı Listeleme Servisi
            "ng-gddk": get_path_template("ng-sgp", "gddk-amount"),
            ## 1 Kodlu İşlemler Listeleme Servisi
            "ng-green-code-ops": get_path_template("ng-sgp", "green-code-operation"),
            ## GRF Eşleşme Miktarı Listeleme Servisi
            "ng-grp-match-qty": get_path_template("ng-sgp", "grf-match-quantity"),
            ## GRF İşlem Hacmi Listeleme Servisi
            "ng-grp-trade-volume": get_path_template("ng-sgp", "grf-trade-volume"),
            ## SGP Dengesizlik Tutarı Listeleme Servisi
            "ng-imbalance-amount": get_path_template("ng-sgp", "imbalance-amount"),
            ## SGP Dengesizlik Sistem Listeleme Servisi
            "ng-imbalance-system": get_path_template("ng-sgp", "imbalance-system"),
            ## Sgp Son Uzlaştırma Tarihi Servisi
            "ng-latest-settlement-date": get_path_template(
                "ng-sgp", "last-reconciliation-date"
            ),
            ## SGP Toplam Eşleşme Miktarı Listeleme Servisi
            "ng-match-quantity": get_path_template("ng-sgp", "match-quantity"),
            ## 3 Kodlu İşlemler Listeleme Servisi
            "ng-orange-code-ops": get_path_template("ng-sgp", "orange-code-operation"),
            ## Fiziki Gerçekleşme Listeleme Servisi
            "ng-physical-realization": get_path_template(
                "ng-sgp", "physical-realization"
            ),
            ## SGP Fiyatlar Listeleme Servisi
            "ng-spot-prices": get_path_template("ng-sgp", "sgp-price"),
            # get_path_template("ng-sgp", "shippers-imbalance-quantity"),
            ## Dengesizlik Taşıtan Listeleme Servisi
            "ng-shippers-imbalance-quantity": get_path_template(
                "ng-sgp", "shippers-imbalance-quantity"
            ),
            ## Sistem Yönü Listeleme Servisi
            "ng-system-direction": get_path_template("ng-sgp", "system-direction"),
            ## SGP Toplam İşlem Hacmi Listeleme Servisi
            "ng-total-trade-volume": get_path_template("ng-sgp", "total-trade-volume"),
            ## SGP İşlem Akışı Listeleme Servisi
            "ng-transaction-history": get_path_template(
                "ng-sgp", "transaction-history"
            ),
            ## Sanal Gerçekleşme Listeleme Servisi
            "ng-virtual-realization": get_path_template(
                "ng-sgp", "virtual-realization"
            ),
            ## SGP Haftalık Eşleşme Miktarı Listeleme Servisi
            "ng-weekly-matched-quantity": get_path_template(
                "ng-sgp", "weekly-matched-quantity"
            ),
            ## Haftalık Referans Fiyatı (HRF) Listeleme Servisi
            "ng-wrp": get_path_template("ng-sgp", "weekly-ref-price"),
        },
        ## category
        "idm": {"prev": "markets"},
        "dam": {"prev": "markets"},
        "bpm": {"prev": "markets"},
        "sgp": {"prev": "markets"},
        "bilateral-contracts": {"prev": "markets"},
        "general-data": {"prev": "markets"},
        "imbalance": {"prev": "markets"},
        "retroactive-adjustment": {"prev": "markets"},
        "ancillary-services": {"prev": "markets"},
        "dams": {"prev": "electricity-service"},
        "markets": {"prev": "electricity-service"},
        "generation": {"prev": "electricity-service"},
        "consumption": {"prev": "electricity-service"},
        "renewables": {"prev": "electricity-service"},
        "transmission": {"prev": "electricity-service"},
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
    redirect_key = None if d is None else d.get("redirect", None)
    if redirect_key is not None:
        d = get_path_map().get(redirect_key, None)

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

        full_path = "/".join(total_path) if join_path else total_path
        root_path = d.get("root", None)
        if root_path is not None:
            full_path = re.sub("electricity-service", root_path + "-service", full_path)
        return full_path
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
        "pp-list",
        "uevm-pp-list",
        "region-list",
        "mms-message-type-list",
        "mms-region-list",
        "intl-direction-list",
        "intl-capacity-demand-direction-list",
        "basin-list",
        "distribution-region-list",
        "province-list",
        "profile-group-list",
        "ra-distribution-list",
        "ra-organization-list",
        "ra-spg-list",
        "ra-vspg-list",
        "ng-participant-list",
        "ng-latest-settlement-date",
    ]

    if key in get_methods:
        return "GET"
    else:
        return "POST"
