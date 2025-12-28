# API Endpoint Categories

Complete listing of eptr2 API endpoints organized by category.

---

## GÖP - Day-Ahead Market (Gün Öncesi Piyasası)

### Prices
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `mcp` | Market Clearing Price | Piyasa Takas Fiyatı (PTF) |
| `interim-mcp` | Interim MCP | Kesinleşmemiş PTF |
| `interim-mcp-status` | Interim MCP Status | K.PTF Yayınlanma Durumu |

### Quantities
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dam-clearing` | DAM Matching Quantity | GÖP Eşleşme Miktarı |
| `dam-volume` | DAM Trade Value | GÖP İşlem Hacmi |
| `dam-bid` | DAM Submitted Bid Volume | GÖP Alış Teklif Miktarı |
| `dam-offer` | DAM Submitted Sales Volume | GÖP Satış Teklif Miktarı |
| `dam-diff` | DAM Side Payment | GÖP Fark Tutarı |

### Block Orders
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dam-block-bid` | DAM Block Bid | GÖP Blok Alış Miktarı |
| `dam-block-offer` | DAM Block Offer | GÖP Blok Satış Miktarı |

### Flexible Orders
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dam-flexible-bid` | DAM Flexible Buying Offer | GÖP Esnek Alış Teklif |
| `dam-flexible-offer` | DAM Flexible Selling Offer | GÖP Esnek Satış Teklif |
| `dam-flexible-matching` | DAM Matched Flexible Offers | GÖP Esnek Teklif Eşleşme |

### Price Independent
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `pi-bid` | Price Independent Bid | Fiyattan Bağımsız Alış |
| `pi-offer` | Price Independent Sales | Fiyattan Bağımsız Satış |

### Other
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `supply-demand` | DAM Supply-Demand | GÖP Arz-Talep |
| `dam-clearing-org-list` | DAM Clearing Org List | GÖP Eşleşme Org Listesi |

---

## GİP - Intraday Market (Gün İçi Piyasası)

### Prices
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `wap` | Weighted Average Price | Ağırlıklı Ortalama Fiyat |
| `idm-mm-bid` | IDM Min-Max Bid Price | GİP Min-Maks Alış Fiyat |
| `idm-mm-offer` | IDM Min-Max Offer Price | GİP Min-Maks Satış Fiyat |
| `idm-mm-matching` | IDM Min-Max Matching Price | GİP Min-Maks Eşleşme Fiyat |

### Quantities
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `idm-qty` | IDM Matching Quantity | GİP Eşleşme Miktarı |
| `idm-volume` | IDM Trade Value | GİP İşlem Hacmi |
| `idm-ob-qty` | IDM Bid/Offer Quantities | GİP Alış Satış Miktarları |

### Transaction Data
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `idm-log` | IDM Transaction History | GİP İşlem Akışı |
| `idm-order-list` | IDM Order List | GİP Teklif Listesi |
| `idm-contract-list` | IDM Contract List | GİP Kontrat Listesi |
| `idm-summary` | IDM Contract Summary | GİP Kontrat Özeti |

---

## DGP - Balancing Power Market (Dengeleme Güç Piyasası)

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `smp` | System Marginal Price | Sistem Marjinal Fiyatı |
| `smp-dir` | System Direction | Sistem Yönü |
| `bpm-up` | Up Regulation Instructions | Yük Alma (YAL) Talimat |
| `bpm-down` | Down Regulation Instructions | Yük Atma (YAT) Talimat |
| `bpm-orders-w-avg` | BPM Instructions (W.Avg) | DGP Talimatları (AOF) |

---

## Dengesizlik - Imbalance

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `imbalance-price` | Imbalance Prices | Dengesizlik Fiyatları |
| `imb-qty` | Imbalance Quantity | Dengesizlik Miktarı |
| `imb-vol` | Imbalance Cost | Dengesizlik Tutarı |
| `imb-qty-g` | DSG Imbalance Quantity | DSG Dengesizlik Miktarı |
| `imb-org-list` | DSG Organization List | DSG Organizasyon Listesi |
| `mcp-smp-imb` | MCP SMP Imbalance Combined | PTF SMF SDF Listeleme |

---

## İA - Bilateral Contracts (İkili Anlaşmalar)

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `bi-long` | Bilateral Bid Quantity | İA Alış Miktarı |
| `bi-short` | Bilateral Offer Quantity | İA Satış Miktarı |
| `bi-euas` | EÜAŞ-GTŞ Bilaterals | EÜAŞ-GTŞ İkili Anlaşmalar |

---

## Üretim - Generation

### Real-Time Generation
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `rt-generation` | RT Generation by Type | Kaynak Bazlı GZÜ |
| `rt-gen` | RT Generation | Gerçek Zamanlı Üretim |
| `rt-gen-org` | RT Generation by Org | Organizasyon Bazlı GZÜ |
| `rt-gen-org-list` | RT Gen Org List | GZÜ Org Listesi |

### Settlement Generation (UEVM)
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `uevm` | Settlement Generation | UEVM |
| `uevm-pp` | UEVM by Power Plant | Santral Bazlı UEVM |

### Production Plans
| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dpp` / `kgup` | Daily Production Plan | KGÜP |
| `kgup-v1` | KGUP Version 1 | KGÜP v1 |
| `kudup` | Settlement Production Plan | KUDÜP |

---

## Tüketim - Consumption

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `rt-cons` | Real-Time Consumption | Gerçek Zamanlı Tüketim |
| `rt-consumption` | Real-Time Consumption | Gerçek Zamanlı Tüketim |
| `uecm` | Settlement Consumption | UEÇM |
| `load-plan` | Demand Forecast | Yük Tahmini |

---

## Barajlar - Dams/Reservoirs

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `dams-daily-level` | Daily Water Level | Günlük Kot |
| `dams-daily-volume` | Daily Volume | Günlük Hacim |
| `dams-active-fullness` | Active Fullness | Aktif Doluluk |
| `dams-active-volume` | Active Volume | Aktif Hacim |
| `dams-water-energy-provision` | Water Energy Equivalent | Suyun Enerji Karşılığı |
| `dams-level-minmax` | Dam Level Min/Max | Kot Min/Max |
| `dams-volume-minmax` | Dam Volume Min/Max | Hacim Min/Max |

---

## Kurulu Güç - Installed Capacity

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `installed-capacity` | Installed Capacity | Kurulu Güç |
| `lic-pp-list` | Licensed Power Plants | Lisanslı Santraller |
| `uevcb-list` | UEVCB List | UEVCB Listesi |
| `org-list` | Organization List | Organizasyon Listesi |
| `pp-list` | Power Plant List | Santral Listesi |

---

## Elektrik Piyasası Raporları - Market Reports

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `electricity-market-quantity` | Market Volumes (Physical) | Piyasa Hacimleri |
| `mcp-smp-imb` | MCP SMP Imbalance List | PTF SMF SDF Listeleme |
| `idm-summary` | IDM Contract Summary | GİP Kontrat Özeti |

---

## Uluslararası - International

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `cross-border-physical` | Cross-Border Physical Flow | Sınır Ötesi Fiziki Akış |
| `congestion-cost` | Congestion Cost | Kısıt Maliyeti |

---

## Aliases (Shortcuts)

| Alias | Full Call |
|-------|-----------|
| `ptf` | `mcp` |
| `smf` | `smp` |
| `kgup` | `dpp` |
| `rt-cons` | `rt-consumption` |

---

## Notes

1. **Date Format**: All endpoints use `YYYY-MM-DD` format
2. **Time Zone**: All timestamps are in Turkey time (UTC+3)
3. **Return Type**: Most endpoints return pandas DataFrame by default
4. **Authentication**: Required for all endpoints
