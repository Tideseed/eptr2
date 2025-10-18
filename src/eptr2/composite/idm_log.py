from eptr2 import EPTR2
import pandas as pd
from datetime import datetime, timedelta
from eptr2.util.time import get_hourly_contract_range_list
import time


def idm_log_longer(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    contract_wise: bool = True,
    verbose: bool = False,
    trials: int = 3,
    cooldown: int = 15,
    days_interval: int = 6,
) -> pd.DataFrame:
    """
    This function gets the IDM log data for a longer period.

    If contract_wise is True, start_date is taken from a day earlier to get the previous day's transactions of the start_date's contracts. For instance if start_date is 2025-05-15, trading for PH25051500 starts at 2025-05-14 18:00:00. Therefore, the start_date is set to 2025-05-14. The end_date is not changed as contract closing times are before the contract times.
    """

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
        print(
            "Friendly warning: Your time interval might be a bit long. You might lose all data if the API fails. We recommmend monthly aggregate calls in order to have proper checkpoints."
        )

    period_start_dt = start_dt
    period_end_dt = min(period_start_dt + timedelta(days=days_interval), end_dt)

    main_df = pd.DataFrame()
    while period_start_dt <= end_dt:

        try:
            period_start_date = period_start_dt.strftime("%Y-%m-%d")
            period_end_date = period_end_dt.strftime("%Y-%m-%d")
            if verbose:
                print(
                    f"Getting IDM log data for {period_start_date} to {period_end_date}"
                )

            # Get the IDM log data
            df = eptr.call(
                "idm-log",
                start_date=period_start_date,
                end_date=period_end_date,
            )

            main_df = pd.concat([main_df, df], ignore_index=True)

            period_start_dt = period_end_dt + timedelta(days=1)
            period_end_dt = min(period_start_dt + timedelta(days=days_interval), end_dt)
        except Exception as e:
            print(
                f"Error getting IDM log data for {period_start_date} to {period_end_date}"
            )
            print(e)

            trials -= 1

            if trials < 0:
                print("Max trials reached. Exiting.")
                break

            print(f"Retrying after {cooldown} seconds... {trials} trials left.")
            time.sleep(cooldown)
            continue

    if contract_wise:
        c_df = pd.DataFrame(data={"contractName": c_l})
        main_df = main_df.merge(c_df, on="contractName", how="inner")

    main_df = main_df.sort_values(by=["contractName", "date", "id"]).reset_index(
        drop=True
    )
    return main_df


def idm_log_period(eptr: EPTR2, period: str, **kwargs):
    """
    This function is a wrapper for the IDM log data for a specific monthly period (e.g. 2025-05-01).
    """
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
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        **kwargs,
    )
