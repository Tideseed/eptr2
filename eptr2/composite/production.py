from eptr2 import EPTR2
import pandas as pd
from eptr2.util.time import (
    iso_to_contract,
    check_date_for_settlement,
)
import time


def get_hourly_production_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    rt_pp_id: str | int | None = None,
    uevm_pp_id: str | int | None = None,
    verbose: bool = False,
    include_contract_symbol: bool = True,
    skip_uevm: bool = False,
    skip_rt: bool = False,
    **kwargs,
):
    """
    This composite function gets production data (Gerçek Zamanlı Üretim, UEVM) and merges them.

    It is also possible to enter pp_id to get the production data for a specific production plan. Example ID values are given below.

    rt_pp_id=641, ## ATATÜRK HES
    uevm_pp_id=142, ## ATATÜRK HES
    """

    max_trials = kwargs.get("max_trials", 2)
    timeout = kwargs.get("timeout", 5)
    sleep_interval = kwargs.get("sleep_interval", 3)

    #### SANITY CHECKS ####
    if skip_rt and skip_uevm:
        raise ValueError("Both skip_rt and skip_uevm cannot be True.")

    #### REAL TIME GENERATION PHASE ####
    if skip_rt:
        rt_included = False
        rt_gen_df = pd.DataFrame()

    else:
        rt_included = True
        if verbose:
            print("Loading real time production data...")

        trials = max_trials
        while trials > 0:
            try:
                rt_gen_df: pd.DataFrame = eptr.call(
                    "rt-gen",
                    start_date=start_date,
                    end_date=end_date,
                    pp_id=rt_pp_id,
                    request_kwargs={"timeout": timeout},
                )
                break
            except Exception as e:
                trials -= 1

                if trials == 0:
                    raise e

                time.sleep(sleep_interval)
                if verbose:
                    print(
                        f"An error occurred while fetching RT data. Retrying after {sleep_interval} seconds... ({trials} attempts left)"
                    )

        if rt_gen_df.empty:
            raise ValueError("No data (production) is available for this date range.")

        try:
            rt_gen_df.drop("hour", axis=1, inplace=True)
        except Exception as e:
            if verbose:
                print(e)

        rt_gen_df.columns = [
            x + "_rt" if x not in ["date"] else x for x in rt_gen_df.columns
        ]

    #### UEVM PHASE ####
    if skip_uevm:
        uevm_included = False
        uevm_df = pd.DataFrame()

    else:
        uevm_included = True
        if verbose:
            print("Loading UEVM data...")

        trials = max_trials
        while trials > 0:
            try:
                uevm_df: pd.DataFrame = eptr.call(
                    "uevm",
                    start_date=start_date,
                    end_date=end_date,
                    pp_id=uevm_pp_id,
                    request_kwargs={"timeout": timeout},
                )
                break
            except Exception as e:
                trials -= 1
                if trials == 0:
                    raise e

                time.sleep(sleep_interval)
                if verbose:
                    print(
                        f"An error occurred while fetching UEVM data. Retrying after {sleep_interval} seconds... ({trials} attempts left)"
                    )

        try:
            uevm_df.drop("hour", axis=1, inplace=True)
        except Exception as e:
            within_settlement = check_date_for_settlement(x=end_date)
            if not within_settlement:
                print("Warning: The end date may not be within the settlement period.")
            if verbose:
                print(e)

        uevm_df.columns = [
            x + "_uevm" if x not in ["date"] else x for x in uevm_df.columns
        ]

    if uevm_included and rt_included:
        if verbose:
            print("Merging data...")

        if uevm_df.empty:
            merged_df = rt_gen_df.copy()
        else:
            merged_df = rt_gen_df.merge(uevm_df, how="left", on=["date"])
    elif uevm_included:
        merged_df = uevm_df.copy()
    elif rt_included:
        merged_df = rt_gen_df.copy()

    if include_contract_symbol:
        try:
            merged_df["contract"] = merged_df["date"].apply(
                lambda x: iso_to_contract(x)
            )
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    merged_df = merged_df.rename(columns={"date": "dt"})

    return merged_df


def get_hourly_production_plan_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    org_id: str | None = None,
    uevcb_id: str | None = None,
    verbose: bool = False,
    include_contract_symbol: bool = True,
    skip_kgup: bool = False,
    skip_kgup_v1: bool = False,
    skip_kudup: bool = False,
    **kwargs,
):
    """
    This composite function gets KGUP v1, KGUP and KUDUP data and merges them.

    It is also possible to enter org_id to get the total production plan for a specific organization. If uevcb_id is also added with org_id, it will get the production plan for a specific uevcb. Example ID values are given below.

    org_id=195, ## ELEKTRİK ÜRETİM AŞ
    uevcb_id=733, ## ATATÜRK HES DB
    """

    max_trials = kwargs.get("max_trials", 2)
    timeout = kwargs.get("timeout", 5)

    if all([skip_kgup_v1, skip_kgup, skip_kudup]):
        raise ValueError(
            "At least one of skip_kgup, skip_kgupv1, or skip_kudup must be False."
        )

    if uevcb_id is not None:
        if org_id is None:
            raise ValueError("org_id is required if uevcb_id is specified.")

    if not skip_kgup_v1:

        if verbose:
            print("Loading KGUP v1...")

        trials = max_trials
        while trials > 0:
            try:
                kgup_v1_df: pd.DataFrame = eptr.call(
                    "kgup-v1",
                    start_date=start_date,
                    end_date=end_date,
                    org_id=org_id,
                    uevcb_id=uevcb_id,
                    request_kwargs={"timeout": timeout},
                )
                break
            except Exception as e:
                trials -= 1
                if trials == 0:
                    raise e
                if verbose:
                    print(
                        f"An error occurred while fetching KGUP v1 data. Retrying... ({trials} attempts left)"
                    )

        if kgup_v1_df.empty:
            skip_kgup_v1 = True
            print("No data (KGUP v1) is available for this date range.")
        else:
            kgup_v1_df.columns = [
                x + "_kgup_v1" if x not in ["date", "time"] else x
                for x in kgup_v1_df.columns
            ]

    if not skip_kgup:
        if verbose:
            print("Loading KGUP...")

        trials = max_trials
        while trials > 0:
            try:
                kgup_df: pd.DataFrame = eptr.call(
                    "kgup",
                    start_date=start_date,
                    end_date=end_date,
                    org_id=org_id,
                    uevcb_id=uevcb_id,
                    request_kwargs={"timeout": timeout},
                )
                break
            except Exception as e:
                trials -= 1
                if trials == 0:
                    raise e
                if verbose:
                    print(
                        f"An error occurred while fetching KGUP data. Retrying... ({trials} attempts left)"
                    )
        if kgup_df.empty:
            skip_kgup = True
            print("No data (KGUP) is available for this date range.")
        else:
            kgup_df.columns = [
                x + "_kgup" if x not in ["date", "time"] else x for x in kgup_df.columns
            ]

    if not skip_kudup:
        if verbose:
            print("Loading KUDUP...")

        trials = max_trials
        while trials > 0:
            try:
                kudup_df: pd.DataFrame = eptr.call(
                    "kudup",
                    start_date=start_date,
                    end_date=end_date,
                    org_id=org_id,
                    uevcb_id=uevcb_id,
                    request_kwargs={"timeout": timeout},
                )
                break
            except Exception as e:
                trials -= 1
                if trials == 0:
                    raise e
                if verbose:
                    print(
                        f"An error occurred while fetching KUDUP data. Retrying... ({trials} attempts left)"
                    )

        if kudup_df.empty:
            skip_kudup = True
            print("No data (KUDUP) is available for this date range.")
        else:
            kudup_df.columns = [
                x + "_kudup" if x not in ["date", "time"] else x
                for x in kudup_df.columns
            ]

    #### MERGE PHASE ####
    if verbose:
        print("Merging dataframes...")

    merged_df = None
    for _ in ["kgup_v1", "kgup", "kudup"]:
        if not eval(f"skip_{_}"):
            if merged_df is None:
                merged_df: pd.DataFrame = eval(f"{_}_df").copy()
            else:
                merged_df = merged_df.merge(
                    eval(f"{_}_df"), on=["date", "time"], how="outer"
                )

    ### Column reordering and contract addition
    if include_contract_symbol:
        try:
            merged_df["contract"] = merged_df["date"].apply(
                lambda x: iso_to_contract(x)
            )
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    merged_df = merged_df.rename(columns={"date": "dt"})

    col_order = (
        ["dt", "time"] + ["contract"]
        if include_contract_symbol
        else [] + [x for x in merged_df.columns if x.startswith("toplam")]
    )

    merged_df = merged_df[
        col_order + [x for x in merged_df.columns if x not in col_order]
    ]

    return merged_df


def wrapper_hourly_production_plan_and_realized(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    org_id: str | None = None,
    uevcb_id: str | None = None,
    rt_pp_id: str | None = None,
    uevm_pp_id: str | None = None,
    verbose: bool = False,
    include_contract_symbol: bool = True,
    **kwargs,
):

    if verbose:
        print("Loading production plan data...")

    plan_df = get_hourly_production_plan_data(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        uevcb_id=uevcb_id,
        verbose=verbose,
        include_contract_symbol=include_contract_symbol,
        **kwargs,
    )

    if verbose:
        print("Loading production realizations data...")

    realized_df = get_hourly_production_data(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        rt_pp_id=rt_pp_id,
        uevm_pp_id=uevm_pp_id,
        verbose=verbose,
        include_contract_symbol=include_contract_symbol,
        **kwargs,
    )

    merged_df = plan_df.merge(
        realized_df,
        how="outer",
        on=["dt"] + (["contract"] if include_contract_symbol else []),
    )

    return merged_df
