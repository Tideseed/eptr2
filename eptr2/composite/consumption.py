from eptr2 import EPTR2
import pandas as pd
from eptr2.util.time import iso_to_contract


def get_hourly_consumption_and_forecast_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    verbose: bool = False,
    include_contract_symbol: bool = False,
):
    """
    This composite function gets load plan, UECM (settlement consumption), real time and consumption data. If end date is after the last settlement data, UECM is filled with real time consumption under consumption column.
    """

    if verbose:
        print("Loading load plan...")

    lp_df = eptr.call(
        "load-plan",
        start_date=start_date,
        end_date=end_date,
        request_kwargs={"timeout": 5},
    )

    df = lp_df[["date", "lep"]].rename(columns={"lep": "load_plan", "date": "dt"})

    if verbose:
        print("Loading UECM...")

    uecm_df: pd.DataFrame = eptr.call(
        "uecm", start_date=start_date, end_date=end_date, request_kwargs={"timeout": 5}
    )

    if not uecm_df.empty:
        uecm_df = uecm_df[["period", "swv"]].rename(
            columns={"period": "dt", "swv": "uecm"}
        )

        df = df.merge(
            uecm_df,
            on="dt",
            how="outer",
        )

    if verbose:
        print("Loading real time consumption...")

    rt_cons = eptr.call(
        "rt-cons",
        start_date=start_date,
        end_date=end_date,
        request_kwargs={"timeout": 5},
    )

    df = df.merge(
        rt_cons[["date", "consumption"]].rename(
            columns={"date": "dt", "consumption": "rt_cons"}
        ),
        on="dt",
        how="outer",
    )

    if not uecm_df.empty:
        df["consumption"] = df.apply(
            lambda x: x["rt_cons"] if pd.isnull(x["uecm"]) else x["uecm"], axis=1
        )
    else:
        df["consumption"] = df["rt_cons"].copy()

    if include_contract_symbol:
        try:
            df["contract"] = df["dt"].apply(lambda x: iso_to_contract(x))
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    return df
