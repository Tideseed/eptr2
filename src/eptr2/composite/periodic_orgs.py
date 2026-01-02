from eptr2 import EPTR2
from datetime import datetime, timedelta
import pandas as pd
import time
import numpy as np
from eptr2.util.time import get_utc3_now, transform_date


def get_generation_organization_list(period: str, **kwargs):
    """
    Get a list of generation organizations active during the specified period's year. It checks for organizations that were active at any point during that year.
    """

    eptr = kwargs.get("eptr", None)
    if eptr is None:
        eptr = EPTR2(recycle_tgt=True)

    period_range = kwargs.get("period_range", "year")

    if period_range == "month":
        start_date = transform_date(period, key="start_of_month", to_str=True)
        end_date = transform_date(period, key="end_of_month", to_str=True)
    elif period_range == "year":
        start_date = transform_date(period, key="start_of_year", to_str=True)
        end_date = transform_date(period, key="end_of_year", to_str=True)
    else:
        raise ValueError("period_range must be either 'month' or 'year'")

    # start_date = datetime.strptime(period, "%Y-%m-%d")
    # end_date = datetime.strptime(period, "%Y-%m-%d")

    # if period_range == "year":
    #     start_date = start_date.replace(month=1, day=1).date().strftime("%Y-%m-%d")
    #     end_date = end_date.replace(month=12, day=31).date().strftime("%Y-%m-%d")
    # elif period_range == "month":
    #     start_date = start_date.replace(day=1).date().strftime("%Y-%m-%d")
    #     next_month = start_date.month % 12 + 1
    #     next_month_year = start_date.year + (start_date.month // 12)
    #     end_date = (
    #         (datetime(next_month_year, next_month, 1) - timedelta(days=1))
    #         .date()
    #         .strftime("%Y-%m-%d")
    #     )

    df = eptr.call("gen-org", start_date=start_date, end_date=end_date)
    df = df.drop_duplicates().reset_index(drop=True)

    df.rename(
        columns={
            "organizationId": "org_id",
            "organizationName": "org_name",
            "organizationShortName": "org_short_name",
        },
        inplace=True,
    )

    return df


def get_uevcb_ids(org_df: pd.DataFrame, period: str, **kwargs):
    """
    Get UEVCB IDs for the given organization DataFrame and period. The difference of this function is it checks both the start and end dates of the period to ensure capturing all relevant UEVCB IDs. It also uses the latest bulk function for efficiency.
    """

    eptr = kwargs.get("eptr", None)
    if eptr is None:
        eptr = EPTR2(recycle_tgt=True)

    start_date = transform_date(period, key="start_of_month", to_str=True)
    end_date = transform_date(period, key="end_of_month", to_str=False)

    now_dt = get_utc3_now()
    now_ts = now_dt.timestamp()
    now_dt = datetime.fromtimestamp(now_ts)
    if end_date > now_dt:
        end_date = now_dt

    end_date = end_date.date().strftime("%Y-%m-%d")

    org_id_list = org_df["org_id"].tolist()

    main_df = pd.DataFrame()
    c = 1
    chunk_size = kwargs.get("chunk_size", 950)
    max_lives = kwargs.get("max_lives", 3)
    verbose = kwargs.get("verbose", False)

    while True:
        org_ids_chunk = org_id_list[(c - 1) * chunk_size : c * chunk_size]
        if len(org_ids_chunk) == 0:
            break

        if verbose:
            print(f"Processing chunk {c}")

        def fetch_uevcb_list(the_date):
            return eptr.call(
                "uevcb-list-bulk",
                start_date=the_date,
                org_ids=org_ids_chunk,
                request_kwargs={"timeout": 5},
            )

        lives = max_lives

        while lives > 0:
            try:
                df = fetch_uevcb_list(start_date)
                break
            except Exception as e:
                print("Error fetching UEVCB data:", e)
                lives -= 1
                if lives <= 0:
                    raise Exception("Max lives reached. Exiting.")
                time.sleep(2)
                continue

        df = df.drop_duplicates().reset_index(drop=True)
        df["period"] = start_date

        time.sleep(1)  # To avoid overwhelming the API
        while lives > 0:
            try:
                df_end = fetch_uevcb_list(end_date)
                break
            except Exception as e:
                print("Error fetching UEVCB data:", e)
                lives -= 1
                if lives <= 0:
                    raise Exception("Max lives reached. Exiting.")
                time.sleep(2)
                continue
        df_end = df_end.drop_duplicates().reset_index(drop=True)
        df_end["period"] = end_date

        main_df = pd.concat([main_df, df, df_end], ignore_index=True)
        c += 1

    main_df.drop_duplicates(subset=["eic"], inplace=True)
    # main_df.drop("period", axis=1, inplace=True)

    main_df.rename(
        columns={
            "id": "uevcb_id",
            "orgId": "org_id",
            "name": "uevcb_name",
            "eic": "uevcb_eic",
        },
        inplace=True,
    )

    return main_df


def get_generation_org_and_uevcb_wrapper(period: str, **kwargs):
    """This is a wrapper function to get generation organizations with their UEVCB IDs."""

    df_gen_orgs = get_generation_organization_list(period=period, **kwargs)
    df_uevcb_ids = get_uevcb_ids(org_df=df_gen_orgs, period=period, **kwargs)

    org_uevcb_df = df_gen_orgs.merge(
        df_uevcb_ids,
        on="org_id",
        how="outer",
    )
    org_uevcb_df.replace({np.nan: None}, inplace=True)
    org_uevcb_df["period"] = period

    return org_uevcb_df


def get_periodic_generation_organization_lists(
    start_date: str, end_date: str, **kwargs
) -> pd.DataFrame:
    """
    This wrapper function gets generation organization lists for periodic intervals (monthly) between the specified start and end dates. Each month organization names can be different, so it captures the changes over time.
    """

    sd_dt = datetime.strptime(start_date, "%Y-%m-%d")
    ed_dt = datetime.strptime(end_date, "%Y-%m-%d")

    df = pd.DataFrame()

    periods = []
    current_dt = transform_date(sd_dt, key="start_of_month", to_str=False)

    while current_dt <= ed_dt:
        periods.append(current_dt.strftime("%Y-%m-%d"))
        current_dt = transform_date(
            current_dt + timedelta(days=31), key="start_of_month", to_str=False
        )

    for period in periods:
        print(f"Processing period: {period}")
        df_res = get_generation_organization_list(period=period, period_range="month")
        df_res["period"] = period
        df = pd.concat([df, df_res], ignore_index=True)
        time.sleep(1)

    return df


def get_multiperiod_generation_org_and_uevcb_wrapper(
    start_date: str, end_date: str, **kwargs
) -> pd.DataFrame:
    """
    This is a wrapper function to get generation organizations with their UEVCB IDs for multiple periods between start_date and end_date.
    """

    sd_dt = datetime.strptime(start_date, "%Y-%m-%d")
    ed_dt = datetime.strptime(end_date, "%Y-%m-%d")
    ed_dt = transform_date(ed_dt, key="end_of_month", to_str=False)

    df = pd.DataFrame()

    periods = []
    current_dt = transform_date(sd_dt, key="start_of_month", to_str=False)

    while current_dt <= ed_dt:
        periods.append(current_dt.strftime("%Y-%m-%d"))
        current_dt = transform_date(
            current_dt + timedelta(days=31), key="start_of_month", to_str=False
        )

    verbose = kwargs.get("verbose", False)

    for period in periods:
        if verbose:
            print(f"Processing period: {period}")
        df_res = get_generation_org_and_uevcb_wrapper(period=period, **kwargs)
        df = pd.concat([df, df_res], ignore_index=True)
        time.sleep(1)

    return df


def get_aggregators_data_for_period(
    period: str | None = None, **kwargs
) -> pd.DataFrame:
    """
    Get a list of aggregators with their units (UEVCB) for the specified period (month).
    """

    eptr = kwargs.pop("eptr", None)
    if eptr is None:
        eptr = EPTR2(recycle_tgt=True)

    if period is None:
        print("No period provided. Using current month as default.")
        period = get_utc3_now().replace(day=1).strftime("%Y-%m-%d")

    df: pd.DataFrame = get_generation_org_and_uevcb_wrapper(
        period=period, eptr=eptr, **kwargs
    )

    df = (
        df[df["org_name"].str.contains("TOPLAYICI", case=True, na=False)]
        .sort_values(["org_name", "uevcb_name"])
        .reset_index(drop=True)
    )

    return df
