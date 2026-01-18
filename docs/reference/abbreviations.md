# Common Abbreviations

The Turkish electricity market uses many abbreviations, both in Turkish and English. This reference helps you understand the terminology.

## Price Terms

| Abbreviation | Turkish | English | Description |
|--------------|---------|---------|-------------|
| **PTF** | Piyasa Takas Fiyatı | Market Clearing Price (MCP) | Day-ahead market price |
| **SMF** | Sistem Marjinal Fiyatı | System Marginal Price (SMP) | Real-time balancing price |
| **AOF** | Ağırlıklı Ortalama Fiyat | Weighted Average Price (WAP) | Volume-weighted average |
| **GÖP Fiyatı** | Gün Öncesi Piyasası Fiyatı | Day-Ahead Market Price | = PTF |
| **GİP Fiyatı** | Gün İçi Piyasası Fiyatı | Intraday Market Price | Intraday trading price |

## Consumption & Generation

| Abbreviation | Turkish | English | Description |
|--------------|---------|---------|-------------|
| **UEÇM** | Uzlaştırmaya Esas Çekiş Miktarı | Settlement Actual Consumption | Official consumption for settlement |
| **UEVM** | Uzlaştırmaya Esas Veriş Miktarı | Settlement Actual Generation | Official generation for settlement |
| **KGÜP** | Kesinleşmiş Günlük Üretim Planı | Finalized Daily Production Plan | Final daily production schedule |
| **KUDÜP** | Kesinleşmiş Uzlaştırma Dönemi Üretim Planı | Finalized Settlement Period Production Plan | Production plan for settlement |

## Market Names

| Abbreviation | Turkish | English | Description |
|--------------|---------|---------|-------------|
| **GÖP** | Gün Öncesi Piyasası | Day-Ahead Market (DAM) | Market for next-day delivery |
| **GİP** | Gün İçi Piyasası | Intraday Market (IDM) | Same-day trading market |
| **DGP** | Dengeleme Güç Piyasası | Balancing Power Market (BPM) | Real-time balancing market |

## Balancing & Imbalance

| Abbreviation | Turkish | English | Description |
|--------------|---------|---------|-------------|
| **YAL** | Yük Alma | Up Regulation | Increasing generation/decreasing consumption |
| **YAT** | Yük Atma | Down Regulation | Decreasing generation/increasing consumption |
| **KÜPST** | Kesinleşmiş Üretim Planından Sapma Tutarı | Production Plan Deviation Cost | Cost for deviating from production plan |
| **DSG** | Dengeden Sorumlu Grup | Balance Responsible Party | Entity responsible for imbalances |

## Organizations & Systems

| Abbreviation | Turkish | English | Description |
|--------------|---------|---------|-------------|
| **EPİAŞ** | Enerji Piyasaları İşletme A.Ş. | Energy Markets Operating Inc. | Market operator |
| **TEİAŞ** | Türkiye Elektrik İletim A.Ş. | Turkish Electricity Transmission Corp. | Transmission system operator |
| **EÜAŞ** | Elektrik Üretim A.Ş. | Electricity Generation Corp. | State generation company |
| **TEDAŞ** | Türkiye Elektrik Dağıtım A.Ş. | Turkish Electricity Distribution Corp. | Distribution company |
| **YEKDEM** | Yenilenebilir Enerji Kaynakları Destekleme Mekanizması | Renewable Energy Resources Support Mechanism | Feed-in tariff system |

## Technical Terms

| Abbreviation | Turkish | English | Description |
|--------------|---------|---------|-------------|
| **UEVCB** | Uzlaştırmaya Esas Veriş Çekiş Birimi | Settlement Metering Point | Metering unit for settlement |
| **İA** | İkili Anlaşma | Bilateral Agreement | Direct contracts between parties |
| **SFK** | Sekonder Frekans Kontrol | Secondary Frequency Control | Frequency regulation service |
| **PFK** | Primer Frekans Kontrol | Primary Frequency Control | Automatic frequency response |

## Units

| Unit | Description |
|------|-------------|
| **MWh** | Megawatt-hour (energy) |
| **MW** | Megawatt (power/capacity) |
| **TL** | Turkish Lira (currency) |
| **TL/MWh** | Price per megawatt-hour |

## Common API Call Keys

| Key | Full Form | Description |
|-----|-----------|-------------|
| `mcp` / `ptf` | Market Clearing Price | Day-ahead price |
| `smp` / `smf` | System Marginal Price | Real-time price |
| `rt-cons` | Real-Time Consumption | Live consumption |
| `rt-generation` | Real-Time Generation | Live generation |
| `load-plan` | Load Plan | Demand forecast |
| `dpp` / `kgup` | Daily Production Plan | Generation schedule |
| `uevm` | UEVM | Settlement generation |
| `uecm` | UEÇM | Settlement consumption |
| `imbalance-price` | Imbalance Price | Imbalance prices |

## See Also

- [Available API Calls](../user-guide/api-calls.md)
- [Calculator App](../tutorials/calculator.md)
