# Domain routing

The installed catalog is the authoritative list; use `eptr2 categories` and `eptr2 search` instead of maintaining a second full endpoint list here.

| Question | Starting keys or search |
|---|---|
| Day-ahead / PTF price | `mcp` (alias `ptf`) |
| Balancing / SMF price | `smp` (alias `smf`) |
| Intraday weighted price | `wap` |
| Imbalance prices and system direction | `mcp-smp-imb` |
| Consumption versus demand forecast | `rt-cons`, `load-plan`, `uecm` |
| Actual generation | `rt-gen`, `rt-gen-bulk` |
| Generation plans | `kgup`, `kgup-v1`, `kudup`, `dpp-bulk` |
| Settlement generation | `uevm` |
| Market volumes | `dam-clearing`, `idm-qty`, `bi-long`, `bi-short` |
| Natural gas | Search `gas`; inspect the matching `ng-*` calls |

## IDs are endpoint-specific

- `pp-list` supplies real-time power-plant IDs.
- `uevm-pp-list` supplies settlement-generation plant IDs.
- `gen-org` supplies organizations; its response uses `organizationId`, not `id`.
- `gen-uevcb` supplies production units for an organization; inspect the returned `id` values.
- `dpp-bulk` takes `uevcb_ids`; `rt-gen-bulk` takes `pp_ids`.

Do not treat plant, organization, settlement-plant, and UEVCB identifiers as interchangeable. Resolve and verify the entity name in each listing. Some endpoints have sparse descriptions: inspect their parameters and a bounded sample response before building an analysis.
