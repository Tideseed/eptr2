# Price response fields

These columns were observed in the EPIAS hourly responses. Check the actual response for changes; this is not a complete output schema.

| Call | Relevant columns |
|---|---|
| `mcp` / `ptf` | `date`, `hour`, `price`, `priceUsd`, `priceEur` |
| `smp` / `smf` | `date`, `hour`, `systemMarginalPrice` |
| `wap` | `date`, `hour`, `wap` |
| `mcp-smp-imb` | `date`, `time`, `ptf`, `smf`, `positiveImbalance`, `negativeImbalance`, `systemStatus` |

The primary TL price fields have units TL/MWh; USD/EUR fields use the named currency per MWh. The composite renames `ptf` to `mcp`, `smf` to `smp`, and the imbalance fields to `pos_imb_price`/`neg_imb_price`.

Use `eptr2 describe <key>` to check input parameters. `postprocess=False` returns the decoded API response envelope, not necessarily a flat list. Keep raw field names distinct from composite names.
