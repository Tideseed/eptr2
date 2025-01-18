from eptr2 import EPTR2
import pandas as pd


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
