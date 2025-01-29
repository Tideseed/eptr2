from eptr2 import EPTR2
import pandas as pd


def get_hourly_production_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    rt_pp_id: str | int | None = None,
    uevm_pp_id: str | int | None = None,
    verbose: bool = False,
):
    """
    This composite function gets production data (Gerçek Zamanlı Üretim, UEVM) and merges them.

    It is also possible to enter pp_id to get the production data for a specific production plan. Example ID values are given below.

    rt_pp_id=641, ## ATATÜRK HES
    uevm_pp_id=142, ## ATATÜRK HES
    """

    if verbose:
        print("Loading real time production data...")

    rt_gen_df: pd.DataFrame = eptr.call(
        "rt-gen",
        start_date=start_date,
        end_date=end_date,
        pp_id=rt_pp_id,
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

    if verbose:
        print("Loading UEVM data...")

    uevm_df: pd.DataFrame = eptr.call(
        "uevm",
        start_date=start_date,
        end_date=end_date,
        pp_id=uevm_pp_id,
    )

    try:
        rt_gen_df.drop("hour", axis=1, inplace=True)
    except Exception as e:
        if verbose:
            print(e)

    uevm_df.columns = [x + "_uevm" if x not in ["date"] else x for x in uevm_df.columns]

    if verbose:
        print("Merging data...")

    merged_df = rt_gen_df.merge(uevm_df, how="left", on=["date"])

    return merged_df


def get_hourly_production_plan_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    org_id: str | None = None,
    uevcb_id: str | None = None,
    verbose: bool = False,
):
    """
    This composite function gets KGUP v1, KGUP and KUDUP data and merges them.

    It is also possible to enter org_id to get the total production plan for a specific organization. If uevcb_id is also added with org_id, it will get the production plan for a specific uevcb. Example ID values are given below.

    org_id=195, ## ELEKTRİK ÜRETİM AŞ
    uevcb_id=733, ## ATATÜRK HES DB
    """

    if uevcb_id is not None:
        if org_id is None:
            raise ValueError("org_id is required if uevcb_id is specified.")

    if verbose:
        print("Loading KGUP v1...")

    kgupv1_df: pd.DataFrame = eptr.call(
        "kgup-v1",
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        uevcb_id=uevcb_id,
    )

    if kgupv1_df.empty:
        raise ValueError("No data (KGUP v1) is available for this date range.")

    kgupv1_df.columns = [
        x + "_v1" if x not in ["date", "time"] else x for x in kgupv1_df.columns
    ]

    if verbose:
        print("Loading KGUP...")

    kgup_df: pd.DataFrame = eptr.call(
        "kgup",
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        uevcb_id=uevcb_id,
    )

    if verbose:
        print("Loading KUDUP...")

    kudup_df: pd.DataFrame = eptr.call(
        "kudup",
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        uevcb_id=uevcb_id,
    )

    kudup_df.columns = [
        x + "_kudup" if x not in ["date", "time"] else x for x in kudup_df.columns
    ]

    if verbose:
        print("Merging dataframes...")

    merged_df = kgupv1_df.merge(kgup_df, on=["date", "time"], how="outer")
    merged_df = merged_df.merge(kudup_df, on=["date", "time"], how="outer")

    first_cols = ["date", "time"] + [
        x for x in merged_df.columns if x.startswith("toplam")
    ]

    merged_df = merged_df[
        first_cols + [x for x in merged_df.columns if x not in first_cols]
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
    )

    merged_df = plan_df.merge(realized_df, how="outer", on=["date"])

    return merged_df
