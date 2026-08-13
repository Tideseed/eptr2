# Price Analysis API Reference

## Day-Ahead Market (GÖP) Price Endpoints

### mcp / ptf - Market Clearing Price

**Description**: Hourly electricity purchase-sale price determined as a result of matching the purchase and sale bids for all bidding zones in the day-ahead market.

**Turkish**: Piyasa Takas Fiyatı - Gün Öncesi Piyasası'na sunulan tekliflerin arz ve talebe göre eşleşmesiyle oluşan saatlik elektrik enerjisi fiyatıdır.

```python
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
# Columns: date, price
```

**URL**: https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/market-clearing-price-mcp

### interim-mcp - Interim Market Clearing Price

**Description**: Temporary hourly energy price determined within the objection period before finalization.

**Turkish**: Kesinleşmemiş PTF - itiraz süreci tamamlanmamış saatlik elektrik enerjisi fiyatıdır.

```python
df = eptr.call("interim-mcp", start_date="2024-07-29", end_date="2024-07-29")
```

### dam-volume - DAM Trade Value

**Description**: The hourly total financial volume of the matching bids in Day-Ahead Market.

**Turkish**: GÖP İşlem Hacmi - Gün Öncesi Piyasası'nda eşleşen alış tekliflerinin saatlik toplam mali değeridir.

```python
df = eptr.call("dam-volume", start_date="2024-07-29", end_date="2024-07-29")
```

### dam-diff - DAM Side Payment

**Description**: Financing of the gap between daily system purchase and sales amounts from block and flexible orders.

**Turkish**: GÖP Fark Tutarı - Blok ve esnek teklif eşleşmelerinden kaynaklanan fark tutarı.

```python
df = eptr.call("dam-diff", start_date="2024-07-29", end_date="2024-07-29")
```

---

## Intraday Market (GİP) Price Endpoints

### wap - Weighted Average Price

**Description**: Hourly weighted average price for transactions on each contract in Intraday Market.

**Turkish**: GİP Ağırlıklı Ortalama Fiyat - Gün İçi Piyasası'ndaki her bir kontrata ilişkin işlemlerin saatlik bazda hacimsel ağırlıklı ortalama fiyatıdır.

```python
df = eptr.call("wap", start_date="2024-07-29", end_date="2024-07-29")
# Columns: date, hour, wap
```

**URL**: https://seffaflik.epias.com.tr/electricity/electricity-markets/intraday-market-idm/idm-weighted-average-price

### idm-volume - IDM Trade Value

**Description**: Hourly total financial volume of matching bids and offers in the Intraday Market.

**Turkish**: GİP İşlem Hacmi - Gün İçi Piyasası'nda eşleşen alış-satış tekliflerinin saatlik toplam mali değeridir.

```python
df = eptr.call("idm-volume", start_date="2024-07-29", end_date="2024-07-29")
```

### idm-mm-matching - IDM Min-Max Matching Price

**Description**: Min and max matching price in the intraday market, categorized as hourly or block.

**Turkish**: GİP Min - Maks Eşleşme Fiyat - En yüksek ve en düşük eşleşme fiyatıdır.

```python
df = eptr.call("idm-mm-matching", start_date="2024-07-29", end_date="2024-07-29")
```

---

## System Marginal Price Endpoints

### smp / smf - System Marginal Price

**Description**: Price of the last accepted balancing power bid/offer used to balance the system.

**Turkish**: Sistem Marjinal Fiyatı - Sistemin dengelenmesi için kabul edilen son dengeleme gücü teklif fiyatı.

```python
df = eptr.call("smp", start_date="2024-07-29", end_date="2024-07-29")
# Columns: date, smpDirection, smp
```

**URL**: https://seffaflik.epias.com.tr/electricity/electricity-markets/balancing-power-market-bpm/system-marginal-price-smp

---

## Imbalance Price Endpoints

### imbalance-price - Imbalance Prices

**Description**: Positive and negative imbalance prices used in settlement.

**Turkish**: Dengesizlik Fiyatları - Pozitif ve negatif dengesizlik fiyatları.

```python
df = eptr.call("imbalance-price", start_date="2024-07-29", end_date="2024-07-29")
# Columns: date, positiveImbalancePrice, negativeImbalancePrice
```

### mcp-smp-imb - Combined Price Data

**Description**: Combined endpoint returning MCP, SMP, and imbalance prices in one call.

```python
df = eptr.call("mcp-smp-imb", start_date="2024-07-29", end_date="2024-07-29")
# Columns: date, time, ptf, smf, positiveImbalance, negativeImbalance, systemStatus
```

---

## Balancing Power Market (DGP) Endpoints

### bpm-price - BPM Offer Prices

**Description**: Up and down regulation prices from the Balancing Power Market.

**Turkish**: DGP Teklif Fiyatları - Yük alma (YAL) ve yük atma (YAT) fiyatları.

```python
df = eptr.call("bpm-price", start_date="2024-07-29", end_date="2024-07-29")
```

---

## Key Price Relationships

### System Direction and Imbalance Costs

| System Direction | Turkish | Sign | Positive Imbalance | Negative Imbalance |
|-----------------|---------|------|-------------------|-------------------|
| Up-regulation (deficit) | Enerji Açığı | -1 | Pay MCP | Pay max(MCP, SMP) |
| Down-regulation (surplus) | Enerji Fazlası | +1 | Receive min(MCP, SMP) | Receive MCP |
| Balanced | Dengede | 0 | Pay MCP | Receive MCP |

### KUPST Cost Formula

KUPST (Kesinleşmiş Üretim Planından Sapma Tutarı) = Deviation cost from production plan

```python
kupst_cost = abs(mcp - smp) * 0.03  # 3% of MCP-SMP spread
```

---

## Parameters

All price endpoints accept:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | str | Yes | Start date in YYYY-MM-DD format |
| `end_date` | str | Yes | End date in YYYY-MM-DD format |

## Return Format

All endpoints return pandas DataFrame by default. Use `postprocess=False` for raw JSON.
