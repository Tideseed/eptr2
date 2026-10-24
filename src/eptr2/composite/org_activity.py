from eptr2.main import DEFAULT_COMPOSITE_BACKOFF, DEFAULT_COMPOSITE_RETRIES, DEFAULT_COMPOSITE_TIMEOUT
import logging
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
    Decomposes an organization's hourly positions into day ahead / intraday trades, day trades and free quantity and adds a fictitious (estimated) PnL.

    Required columns: da_long, da_short, idm_long, idm_short, mcp, idm_wap, idm_tad. Optional columns: bi_long, bi_short (taken as 0 if missing).

    Added columns (all quantities in MWh, positive is buy / long):
        da_net: da_long - da_short
        idm_net: idm_long - idm_short
        bi_net: bi_long - bi_short
        day_trade: min(idm_long, idm_short). Intraday quantity bought and sold back within the intraday market.
        da_id_close: Day ahead position closed (reversed) in the intraday market. min(|da_net|, |idm_net|) if da_net and idm_net have opposite signs, otherwise 0. Always non-negative, direction follows da_net.
        free_qty: da_net + bi_net + idm_net. Net quantity that shall either be consumed (positive, net buyer) or generated (negative, net seller). Subtract bi_net for the organized market (DA + IDM) only part.
        da_id_pnl: Fictitious PnL of day ahead open / intraday close trades. da_id_close * sign(da_net) * (idm_wap - mcp). Buying in DA and selling in IDM gains when idm_wap > mcp, the reverse for selling in DA.
        day_trade_pnl: Fictitious PnL of day trades. day_trade * idm_tad. Note that this is one sided TAD (not 2 * TAD for a buy and a sell around WAP) by definition.
        total_pnl: da_id_pnl + day_trade_pnl

    The PnL is an estimate: actual trade prices of the organization are not public, so intraday trades are assumed to be at idm_wap and day trades to capture the average TAD. If mcp, idm_wap or idm_tad is missing, the related PnL is NaN.
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
    df["free_qty"] = df["da_net"] + df["bi_net"] + df["idm_net"]

    df["da_id_pnl"] = (
        df["da_id_close"] * np.sign(df["da_net"]) * (df["idm_wap"] - df["mcp"])
    )
    ## No closed quantity means no PnL even if a price is missing
    df.loc[df["da_id_close"] == 0, "da_id_pnl"] = 0.0
    df["day_trade_pnl"] = df["day_trade"] * df["idm_tad"]
    df.loc[df["day_trade"] == 0, "day_trade_pnl"] = 0.0
    df["total_pnl"] = df["da_id_pnl"] + df["day_trade_pnl"]

    round_cols = ["da_net", "idm_net", "bi_net", "day_trade", "da_id_close", "free_qty"]
    df[round_cols] = df[round_cols].round(2)

    return df


def get_org_estimated_activity(
    start_date: str,
    end_date: str,
    org_id: str,
    eptr: EPTR2 | None = None,
    idm_log_df: pd.DataFrame | None = None,
    verbose: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Estimates an organization's (company's) trading activity for the given period (start_date and end_date inclusive) on an hourly contract basis.

    Day ahead, bilateral and intraday matched quantities of the organization (get_dabi_idm_data) are combined with MCP and the intraday WAP and TAD calculated from the intraday trade log (idm_log_longer). See calculate_org_activity for the decomposition (day ahead open / intraday close, day trade, free quantity) and the fictitious PnL columns.

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (inclusive)
        org_id: Organization ID
        eptr: EPTR2 object. Created from .env if not provided.
        idm_log_df: Previously fetched IDM trade log covering the period (e.g. idm_log_longer output). The log is market wide, so it can be reused for several organizations to avoid fetching it again.
        verbose: Log progress

    Returns:
        pd.DataFrame: One row per hourly contract with quantity, price, decomposition and PnL columns. Prices (mcp, idm_wap, idm_tad) are left NaN if they could not be retrieved, they are not filled with 0.
    """

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

    if verbose:
        logger.info("Getting day ahead, bilateral and intraday quantities...")
    pos_df = get_dabi_idm_data(
        start_date=start_date,
        end_date=end_date,
        eptr=eptr,
        org_id=org_id,
        verbose=verbose,
        **kwargs,
    )

    if verbose:
        logger.info("Getting MCP...")
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

    if idm_log_df is None:
        if verbose:
            logger.info("Getting IDM trade log...")
        idm_log_df = idm_log_longer(
            start_date=start_date,
            end_date=end_date,
            eptr=eptr,
            contract_wise=True,
            verbose=verbose,
        )
    stats_df = calculate_idm_contract_stats(idm_log_df)

    ## All hourly contracts of the period, so that missing rows of any source do not drop contracts
    df = pd.DataFrame(
        {"contract": get_hourly_contract_range_list(start_date=start_date, end_date=end_date)}
    )
    pos_cols = ["contract", "date"] + [c for c in QUANTITY_COLUMNS if c in pos_df.columns]
    df = (
        df.merge(pos_df[pos_cols], on="contract", how="left")
        .merge(mcp_df, on="contract", how="left")
        .merge(stats_df, on="contract", how="left")
    )
    ## Only quantities are filled. Missing prices stay NaN so that PnL is not silently zeroed.
    for col in QUANTITY_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = df[col].fillna(0.0)

    if df["idm_wap"].isna().any():
        logger.warning(
            "IDM WAP is missing for %d contract(s), their intraday PnL is NaN.",
            int(df["idm_wap"].isna().sum()),
        )

    df = calculate_org_activity(df)
    df["org_id"] = org_id

    return df
