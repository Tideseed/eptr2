from eptr2 import EPTR2
import pandas as pd
from eptr2.util.time import iso_to_contract, get_utc3_now
import time
from datetime import datetime, timedelta


def get_bpm_range(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    max_lives: int = 2,
    verbose: bool = False,
    strict: bool = True,
    include_contract_symbol: bool = True,
) -> pd.DataFrame:
    """
    This function retrieves BPM (Balancing Power Market) weighted average data for multiple days between the specified start and end dates.

    start_date: str
        The start date in "YYYY-MM-DD" format.
    end_date: str
        The end date in "YYYY-MM-DD" format.
    max_lives: int
        The maximum number of retries for fetching data in case of errors.
    verbose: bool
        If True, prints detailed information about the fetching process.
    strict: bool
        If True, raises an exception if data fetching fails after retries.
    include_contract_symbol: bool
        If True, adds a column with the contract symbol derived from the date.
    Returns:
    pd.DataFrame
        A DataFrame containing the BPM data with columns for date, time, and YAL-YAT values.
    """

    date_range = pd.date_range(start=start_date, end=end_date, freq="D").to_list()

    date_range = sorted([d.strftime("%Y-%m-%d") for d in date_range])

    main_df = pd.DataFrame()

    today = get_utc3_now().strftime("%Y-%m-%d")

    for i, date_str in enumerate(date_range):

        if date_str > today:
            print("Skipping future dates:", date_str)
            break

        if verbose:
            print(f"Fetching data for {date_str} ({i + 1}/{len(date_range)})...")
        lives = max_lives

        while lives > 0:
            try:
                df = eptr.call(
                    "bpm-orders-w-avg",
                    date=date_str,
                    request_kwargs={"timeout": 5},
                )
                if df.empty:
                    print(f"No data found for {date_str}. Skipping...")
                else:
                    df.drop(columns=["date"], inplace=True)
                    df.rename(columns={"time": "dt"}, inplace=True)
                    main_df = pd.concat([main_df, df])
                break
            except Exception as e:
                if lives > 0:
                    print(
                        f"Error fetching data for {date_str}: {e}. Retrying after sleeping..."
                    )
                    lives -= 1
                    time.sleep(max_lives - lives)  # Sleep longer with each retry
                else:
                    print(f"Failed to fetch data for {date_str} after retries.")
                    if strict:
                        raise Exception("Failed to fetch data after retries.")

    main_df.reset_index(drop=True, inplace=True)

    if include_contract_symbol:
        try:
            main_df["contract"] = main_df["dt"].apply(lambda x: iso_to_contract(x))
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    return main_df


def get_bpm_period(
    eptr: EPTR2,
    period: str,
    max_lives: int = 2,
    verbose: bool = False,
    strict: bool = True,
    include_contract_symbol: bool = True,
) -> pd.DataFrame:
    """
    This function is a wrapper for `get_bpm_range` that retrieves BPM data for a specific month, regardless of the day.

    eptr: EPTR2
        An instance of the EPTR2 class to interact with the EPT API.
    period: str
        The period for which to retrieve BPM data, formatted as "YYYY-MM-DD".
    max_lives: int
        The maximum number of retries for fetching data in case of errors.
    verbose: bool
        If True, prints detailed information about the fetching process.
    strict: bool
        If True, raises an exception if data fetching fails after retries.
    include_contract_symbol: bool
        If True, adds a column with the contract symbol derived from the date.
    Returns:
    pd.DataFrame
        A DataFrame containing the BPM data for the specified month, with columns for date, time, and YAL-YAT values.
    """

    start_dt = datetime.strptime(period, "%Y-%m-%d").replace(day=1)
    end_dt = (start_dt + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")

    df = get_bpm_range(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        max_lives=max_lives,
        verbose=verbose,
        strict=strict,
        include_contract_symbol=include_contract_symbol,
    )

    return df
