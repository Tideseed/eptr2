from eptr2.main import DEFAULT_COMPOSITE_BACKOFF, DEFAULT_COMPOSITE_RETRIES, DEFAULT_COMPOSITE_TIMEOUT
import logging
import time
from eptr2 import EPTR2
import numpy as np
import pandas as pd
from eptr2.composite.dabi_idm import get_dabi_idm_data
from eptr2.composite.idm_log import idm_log_longer
from eptr2.util.time import iso_to_contract, get_hourly_contract_range_list


logger = logging.getLogger(__name__)

## idm-log quantities are in lots. 1 lot = 0.1 MWh: for every hourly contract
## sum(price * quantity) / 10 equals the idm-volume tradingVolume, and the
## log-derived WAP equals the wap endpoint to the cent.
IDM_LOT_MWH = 0.1

QUANTITY_COLUMNS = ["da_long", "da_short", "bi_long", "bi_short", "idm_long", "idm_short"]


def calculate_idm_contract_stats(log_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates per contract intraday statistics from the IDM trade log (idm-log or idm_log_longer output).

    Returns a DataFrame with columns:
        contract: Hourly contract name (PHyyMMddhh)
        idm_wap: Weighted average price of all trades in the contract
        idm_tad: Trade absolute deviation. Quantity weighted average of |price - idm_wap| over all trades in the contract
        idm_trade_count: Number of trades
        idm_volume_mwh: Total traded quantity in MWh (log quantities are lots of 0.1 MWh)

    Only hourly (PH) contracts are taken into account.
    """
    cols = ["contract", "idm_wap", "idm_tad", "idm_trade_count", "idm_volume_mwh"]
    if log_df is None or log_df.empty:
        return pd.DataFrame(columns=cols)

    df = log_df.loc[
        log_df["contractName"].str.startswith("PH"),
        ["contractName", "price", "quantity"],
    ].rename({"contractName": "contract"}, axis=1)

    df["pq"] = df["price"] * df["quantity"]
    wap_df = df.groupby("contract", as_index=False).agg(
        pq=("pq", "sum"), q=("quantity", "sum"), idm_trade_count=("price", "size")
    )
    wap_df["idm_wap"] = wap_df["pq"] / wap_df["q"]

    df = df.merge(wap_df[["contract", "idm_wap"]], on="contract", how="left")
    df["abs_dev_q"] = (df["price"] - df["idm_wap"]).abs() * df["quantity"]
    tad_df = df.groupby("contract", as_index=False)["abs_dev_q"].sum()

    stats_df = wap_df.merge(tad_df, on="contract", how="left")
    stats_df["idm_tad"] = stats_df["abs_dev_q"] / stats_df["q"]
    stats_df["idm_volume_mwh"] = stats_df["q"] * IDM_LOT_MWH

    return stats_df[cols].sort_values("contract").reset_index(drop=True)


def calculate_org_activity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Decomposes an organization's hourly positions into day ahead / intraday trades, day trades and net positions and, if prices are given, adds a fictitious (estimated) PnL.

    Required columns: da_long, da_short, idm_long, idm_short. Optional columns: bi_long, bi_short (taken as 0 if missing); mcp and idm_wap (add da_id_pnl and total_pnl); idm_tad (also adds day_trade_pnl).

    Added columns (all quantities in MWh, positive is buy / long):
        da_net: da_long - da_short
        idm_net: idm_long - idm_short
        bi_net: bi_long - bi_short
        day_trade: min(idm_long, idm_short). Intraday quantity bought and sold back within the intraday market.
        da_id_close: Day ahead position closed (reversed) in the intraday market. min(|da_net|, |idm_net|) if da_net and idm_net have opposite signs, otherwise 0. Always non-negative, direction follows da_net.
        dabi_net: da_net + bi_net. Day ahead (GÖP + İA) net position.
        dabi_idm_net: dabi_net + idm_net. Net quantity that shall either be consumed (positive, net buyer) or generated (negative, net seller). Subtract bi_net for the organized market (GÖP + GİP) only part.
        da_id_pnl: Fictitious PnL of day ahead open / intraday close trades. da_id_close * sign(da_net) * (idm_wap - mcp). Buying in DA and selling in IDM gains when idm_wap > mcp, the reverse for selling in DA.
        day_trade_pnl: Only with idm_tad. Fictitious PnL of day trades. day_trade * idm_tad. Note that this is one sided TAD (not 2 * TAD for a buy and a sell around WAP) by definition.
        total_pnl: da_id_pnl (+ day_trade_pnl when available)

    The PnL is an estimate: actual trade prices of the organization are not public, so intraday trades are assumed to be at idm_wap and day trades to capture the average TAD. If a price is missing, the related PnL is NaN.
    """
    df = df.copy()
    for col in ["bi_long", "bi_short"]:
        if col not in df.columns:
            df[col] = 0.0

    df["da_net"] = df["da_long"] - df["da_short"]
    df["idm_net"] = df["idm_long"] - df["idm_short"]
    df["bi_net"] = df["bi_long"] - df["bi_short"]

    df["day_trade"] = np.minimum(df["idm_long"], df["idm_short"])
    is_opposite = np.sign(df["da_net"]) * np.sign(df["idm_net"]) < 0
    df["da_id_close"] = np.where(
        is_opposite, np.minimum(df["da_net"].abs(), df["idm_net"].abs()), 0.0
    )
    df["dabi_net"] = df["da_net"] + df["bi_net"]
    df["dabi_idm_net"] = df["dabi_net"] + df["idm_net"]

    round_cols = ["da_net", "idm_net", "bi_net", "dabi_net", "dabi_idm_net", "day_trade", "da_id_close"]
    df[round_cols] = df[round_cols].round(2)

    if not {"mcp", "idm_wap"} <= set(df.columns):
        return df

    df["da_id_pnl"] = (
        df["da_id_close"] * np.sign(df["da_net"]) * (df["idm_wap"] - df["mcp"])
    )
    ## No closed quantity means no PnL even if a price is missing
    df.loc[df["da_id_close"] == 0, "da_id_pnl"] = 0.0
    df["total_pnl"] = df["da_id_pnl"]

    if "idm_tad" in df.columns:
        df["day_trade_pnl"] = df["day_trade"] * df["idm_tad"]
        df.loc[df["day_trade"] == 0, "day_trade_pnl"] = 0.0
        df["total_pnl"] = df["total_pnl"] + df["day_trade_pnl"]

    return df


def get_org_estimated_activity(
    start_date: str,
    end_date: str,
    org_id: str,
    eptr: EPTR2 | None = None,
    include_pnl: bool = False,
    include_day_trade_pnl: bool = False,
    idm_log_df: pd.DataFrame | None = None,
    verbose: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Estimates an organization's (company's) trading activity for the given period (start_date and end_date inclusive) on an hourly contract basis.

    The activity comes from the organization's own matched quantities only: day ahead (GÖP), bilateral (İA) and intraday (GİP) matchings by organization id (get_dabi_idm_data, a few seconds per week). See calculate_org_activity for the decomposition (day ahead open / intraday close, day trade, dabi_net and dabi_idm_net net positions).

    With include_pnl=True a fictitious PnL of day ahead open / intraday close trades is added from MCP and the published intraday WAP (two more calls, fast).

    With include_day_trade_pnl=True a fictitious day trade PnL (day_trade * TAD) is added as well. TAD can only be calculated from the market wide intraday trade log (idm_log_longer), which is large (about 20k trades a day, a few seconds per day to fetch), so this is much slower.

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (inclusive)
        org_id: Organization ID
        eptr: EPTR2 object. Created from .env if not provided.
        include_pnl: Add mcp, idm_wap, da_id_pnl and total_pnl (fetches MCP and WAP).
        include_day_trade_pnl: Also add idm_tad and day_trade_pnl (fetches the IDM trade log). Implies include_pnl=True.
        idm_log_df: Previously fetched IDM trade log covering the period (e.g. idm_log_longer output). The log is market wide, so it can be reused for several organizations to avoid fetching it again. Implies include_day_trade_pnl=True.
        verbose: Log each step and each IDM log chunk with row counts and elapsed time (to stderr)

    Returns:
        pd.DataFrame: One row per hourly contract with quantity and decomposition columns, and the price and PnL columns that were requested. Prices (mcp, idm_wap, idm_tad) are left NaN if they could not be retrieved, they are not filled with 0.
    """
    t_start = time.time()

    def log_step(message, *args):
        if verbose:
            logger.info("[%5.1fs] " + message, time.time() - t_start, *args)

    if idm_log_df is not None:
        include_day_trade_pnl = True
    if include_day_trade_pnl:
        include_pnl = True

    if eptr is None:
        eptr = EPTR2(dotenv_path=kwargs.get("dotenv_path", ".env"))

    retry_kwargs = {
        "retry_attempts": kwargs.get("lives", DEFAULT_COMPOSITE_RETRIES),
        "retry_backoff": kwargs.get("retry_backoff", DEFAULT_COMPOSITE_BACKOFF),
        "retry_backoff_max": kwargs.get(
            "retry_backoff_max", kwargs.get("retry_backoff", DEFAULT_COMPOSITE_BACKOFF)
        ),
        "retry_jitter": kwargs.get("retry_jitter", 0.0),
    }

    log_step("Getting GÖP, İA and GİP matchings of organization %s for %s to %s...", org_id, start_date, end_date)
    pos_df = get_dabi_idm_data(
        start_date=start_date,
        end_date=end_date,
        eptr=eptr,
        org_id=org_id,
        verbose=verbose,
        **kwargs,
    )
    log_step("Got matchings for %d hour(s).", len(pos_df))

    ## All hourly contracts of the period, so that missing rows of any source do not drop contracts
    df = pd.DataFrame(
        {"contract": get_hourly_contract_range_list(start_date=start_date, end_date=end_date)}
    )
    pos_cols = ["contract", "date"] + [c for c in QUANTITY_COLUMNS if c in pos_df.columns]
    df = df.merge(pos_df[pos_cols], on="contract", how="left")
    for col in QUANTITY_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = df[col].fillna(0.0)

    if include_pnl:
        log_step("Getting MCP...")
        mcp_df = eptr.call(
            "mcp",
            start_date=start_date,
            end_date=end_date,
            request_kwargs={"timeout": DEFAULT_COMPOSITE_TIMEOUT},
            **retry_kwargs,
        )
        mcp_df = pd.DataFrame(
            {
                "contract": mcp_df["date"].apply(lambda x: iso_to_contract(x)),
                "mcp": mcp_df["price"],
            }
        )

        log_step("Getting intraday WAP...")
        wap_df = eptr.call(
            "wap",
            start_date=start_date,
            end_date=end_date,
            request_kwargs={"timeout": DEFAULT_COMPOSITE_TIMEOUT},
            **retry_kwargs,
        )
        wap_df = pd.DataFrame(
            {
                "contract": wap_df["date"].apply(lambda x: iso_to_contract(x)),
                "idm_wap": wap_df["wap"],
            }
        )

        ## Missing prices stay NaN so that PnL is not silently zeroed
        df = df.merge(mcp_df, on="contract", how="left").merge(wap_df, on="contract", how="left")

        if include_day_trade_pnl:
            if idm_log_df is None:
                log_step("Getting the IDM trade log for TAD (market wide, a few seconds per day)...")
                idm_log_df = idm_log_longer(
                    start_date=start_date,
                    end_date=end_date,
                    eptr=eptr,
                    contract_wise=True,
                    verbose=verbose,
                    ## Daily requests: one 7-day request took ~72 s, seven daily ones ~3 s each
                    days_interval=kwargs.get("idm_log_days_interval", 0),
                )
                log_step("Got %d IDM trades.", len(idm_log_df))
            stats_df = calculate_idm_contract_stats(idm_log_df)
            df = df.merge(stats_df[["contract", "idm_tad"]], on="contract", how="left")

        if df["idm_wap"].isna().any():
            logger.warning(
                "IDM WAP is missing for %d contract(s), their intraday PnL is NaN.",
                int(df["idm_wap"].isna().sum()),
            )

    df = calculate_org_activity(df)
    df["org_id"] = org_id
    log_step("Done.")

    return df
