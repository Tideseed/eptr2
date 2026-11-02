from eptr2.main import DEFAULT_COMPOSITE_TIMEOUT_LONG
from eptr2 import EPTR2
import pandas as pd
from datetime import datetime, timedelta
import logging
import time
import os
from typing import Any
from eptr2.util.time import get_hourly_contract_range_list, get_today_utc3


logger = logging.getLogger(__name__)

## idm-log quantities are in lots. 1 lot = 0.1 MWh: for every hourly contract
## sum(price * quantity) / 10 equals the idm-volume tradingVolume, and the
## log-derived WAP equals the wap endpoint to the cent.
IDM_LOT_MWH = 0.1

IDM_CONTRACT_STATS_COLUMNS = [
    "contract",
    "idm_wap",
    "idm_mad",
    "idm_tad",
    "idm_trade_count",
    "idm_volume_mwh",
]


def idm_log_longer(
    start_date: str,
    end_date: str,
    eptr: EPTR2 | None = None,
    contract_wise: bool = True,
    verbose: bool = False,
    trials: int = 3,
    cooldown: int = 15,
    days_interval: int = 6,
    **kwargs,
) -> pd.DataFrame:
    """
    This function gets the IDM log data for a longer period.

    If contract_wise is True, start_date is taken from a day earlier to get the previous day's transactions of the start_date's contracts. For instance if start_date is 2025-05-15, trading for PH25051500 starts at 2025-05-14 18:00:00. Therefore, the start_date is set to 2025-05-14. The end_date is not changed as contract closing times are before the contract times.
    """

    if eptr is None:
        eptr = EPTR2(dotenv_path=kwargs.get("dotenv_path", ".env"))

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    if contract_wise:
        ## Get conract range list
        c_l = get_hourly_contract_range_list(start_date=start_date, end_date=end_date)
        start_dt = start_dt - timedelta(days=1)
        start_date = start_dt.strftime("%Y-%m-%d")

    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    ## Make a sanity check and show a friendly warning
    whole_interval = (end_dt - start_dt).days
    if whole_interval > 32:
        logger.warning(
            "Friendly warning: Your time interval might be a bit long. You might lose all data if the API fails. We recommmend monthly aggregate calls in order to have proper checkpoints."
        )

    period_start_dt = start_dt
    period_end_dt = min(period_start_dt + timedelta(days=days_interval), end_dt)

    main_df = pd.DataFrame()
    while period_start_dt <= end_dt:
        period_start_date = period_start_dt.strftime("%Y-%m-%d")
        period_end_date = period_end_dt.strftime("%Y-%m-%d")
        if verbose:
            logger.info(
                "Getting IDM log data for %s to %s",
                period_start_date,
                period_end_date,
            )
        chunk_start = time.time()

        try:
            df = eptr.call(
                "idm-log",
                start_date=period_start_date,
                end_date=period_end_date,
                ## The intraday log returns every order for the period, so it
                ## needs a longer budget than an ordinary composite request.
                request_kwargs={
                    "timeout": kwargs.get("timeout", DEFAULT_COMPOSITE_TIMEOUT_LONG)
                },
                retry_attempts=trials,
                retry_backoff=cooldown,
                retry_backoff_max=cooldown,
                retry_jitter=0.0,
            )
        except Exception as e:
            logger.warning(
                f"Error getting IDM log data for {period_start_date} to {period_end_date}"
            )
            logger.warning("%s", e)
            break

        if verbose:
            logger.info(
                "  %d trades in %.1f s", len(df), time.time() - chunk_start
            )

        main_df = pd.concat([main_df, df], ignore_index=True)

        period_start_dt = period_end_dt + timedelta(days=1)
        period_end_dt = min(period_start_dt + timedelta(days=days_interval), end_dt)

    if contract_wise:
        c_df = pd.DataFrame(data={"contractName": c_l})
        main_df = main_df.merge(c_df, on="contractName", how="inner")

    main_df = main_df.sort_values(by=["contractName", "date", "id"]).reset_index(
        drop=True
    )
    return main_df


def idm_log_period(period: str, eptr: EPTR2 | None = None, **kwargs):
    """
    This function is a wrapper for the IDM log data for a specific monthly period (e.g. 2025-05-01).
    """

    if eptr is None:
        eptr = EPTR2(dotenv_path=kwargs.get("dotenv_path", ".env"))

    ## Check if the period is a valid date
    try:
        period_dt = datetime.strptime(period, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    ## Start of month
    start_dt = period_dt.replace(day=1)
    ## End of month
    end_dt = (start_dt + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")
    return idm_log_longer(
        start_date=start_date,
        end_date=end_date,
        eptr=eptr,
        **kwargs,
    )


def calculate_idm_contract_stats(log_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates per contract intraday statistics from the IDM trade log (idm-log or idm_log_longer output).

    Returns a DataFrame with columns:
        contract: Hourly contract name (PHyyMMddhh)
        idm_wap: Weighted average price of all trades in the contract
        idm_mad: MAD (mean absolute deviation, TL/MWh), a volatility metric. Quantity weighted average of |price - idm_wap| over all trades in the contract
        idm_tad: TAD (total absolute deviation, TL) of the contract: sum of |price - idm_wap| * quantity over all trades, i.e. idm_mad * idm_volume_mwh
        idm_trade_count: Number of trades
        idm_volume_mwh: Total traded quantity in MWh (log quantities are lots of 0.1 MWh)

    Only hourly (PH) contracts are taken into account.
    """
    cols = IDM_CONTRACT_STATS_COLUMNS
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
    abs_dev_df = df.groupby("contract", as_index=False)["abs_dev_q"].sum()

    stats_df = wap_df.merge(abs_dev_df, on="contract", how="left")
    stats_df["idm_mad"] = stats_df["abs_dev_q"] / stats_df["q"]
    stats_df["idm_tad"] = stats_df["abs_dev_q"] * IDM_LOT_MWH
    stats_df["idm_volume_mwh"] = stats_df["q"] * IDM_LOT_MWH

    return stats_df[cols].sort_values("contract").reset_index(drop=True)


def get_idm_contract_stats(
    start_date: str,
    end_date: str,
    eptr: EPTR2 | None = None,
    idm_log_df: pd.DataFrame | None = None,
    export_to_csv: bool = True,
    export_dir: str = "data",
    check_existing: bool = True,
    verbose: bool = False,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Market wide intraday (GİP) statistics per hourly contract for the given period (start_date and end_date inclusive), from the IDM trade log: idm_wap, idm_mad (MAD, mean absolute deviation, TL/MWh), idm_tad (TAD, total absolute deviation, TL), idm_trade_count and idm_volume_mwh. See calculate_idm_contract_stats.

    The trade log is large (about 20k trades a day) and slow to fetch (roughly 30-70 s per week, depending on EPİAŞ), so by default the results are kept in files: idm_log_{start_date}_{end_date}.csv (the log, idm_log_longer output) and idm_contract_stats_{start_date}_{end_date}.csv in export_dir. With check_existing=True (default) the statistics file is read if it exists, otherwise the log file, and only then is the log fetched. get_org_estimated_activity uses the same files.

    end_date must be before today (Europe/Istanbul): the log of the current day is not final, so neither are the statistics or the files.

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (inclusive), before today
        eptr: EPTR2 object. Created from .env if needed.
        idm_log_df: Previously fetched trade log covering the period (idm_log_longer output). Used instead of the files and the API.
        export_to_csv: Write the log and the statistics to export_dir (files that were read are not written again).
        export_dir: Directory of the CSV files, created if missing.
        check_existing: Read existing files of the same period before fetching.
        verbose: Log each step.
        **kwargs: Passed to idm_log_longer (e.g. days_interval, timeout).

    Returns:
        pd.DataFrame: One row per hourly contract with the columns above.
    """
    today = get_today_utc3()
    if end_date >= today:
        raise ValueError(
            f"end_date must be before today ({today}, Europe/Istanbul): the trade log of the current day is not final. Got end_date={end_date}."
        )

    def csv_path(name):
        return os.path.join(export_dir, f"{name}_{start_date}_{end_date}.csv")

    stats_path, log_path = csv_path("idm_contract_stats"), csv_path("idm_log")

    if idm_log_df is None and check_existing and os.path.exists(stats_path):
        stats_df = pd.read_csv(stats_path, dtype={"contract": str})
        if all(c in stats_df.columns for c in IDM_CONTRACT_STATS_COLUMNS):
            if verbose:
                logger.info("Read IDM contract statistics from %s", stats_path)
            return stats_df[IDM_CONTRACT_STATS_COLUMNS]
        ## e.g. files of eptr2 1.4.0, whose idm_tad column was the MAD
        logger.warning(
            "%s does not have the current columns, recalculating it.", stats_path
        )

    log_loaded = False
    if idm_log_df is None and check_existing and os.path.exists(log_path):
        if verbose:
            logger.info("Reading the IDM trade log from %s", log_path)
        idm_log_df = pd.read_csv(log_path, dtype={"contractName": str})
        log_loaded = True

    if idm_log_df is None:
        if verbose:
            logger.info(
                "Getting the IDM trade log for %s to %s (market wide, about 20k trades a day)...",
                start_date,
                end_date,
            )
        idm_log_df = idm_log_longer(
            start_date=start_date,
            end_date=end_date,
            eptr=eptr,
            contract_wise=True,
            verbose=verbose,
            **kwargs,
        )

    stats_df = calculate_idm_contract_stats(idm_log_df)

    if export_to_csv:
        os.makedirs(export_dir, exist_ok=True)
        if not log_loaded:
            idm_log_df.to_csv(log_path, index=False)
        stats_df.to_csv(stats_path, index=False)
        if verbose:
            logger.info("Wrote %s and %s", log_path, stats_path)

    return stats_df
