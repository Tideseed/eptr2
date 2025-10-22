from eptr2 import EPTR2
from eptr2.util.time import iso_to_contract
import pandas as pd


def get_mms_detail(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    org_id: str | None = None,
    uevcb_id: str | None = None,
    pp_id: str | None = None,
    message_type_id: str | None = None,
    include_contract_symbol: bool = False,
    include_summary: bool = False,
    verbose: bool = False,
):
    """
    This composite function gets market message system (MMS) data, expands it and adds the contract symbols (optional).
    """

    df: pd.DataFrame = eptr.call(
        "mms",
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        uevcb_id=uevcb_id,
        pp_id=pp_id,
        message_type_id=message_type_id,
    )

    df_wip = df.explode("faultDetails", ignore_index=True)

    df_res = df_wip.drop(columns=["faultDetails"]).join(
        pd.json_normalize(df_wip["faultDetails"], sep="_")
    )

    if include_summary and not include_contract_symbol:
        if verbose:
            print(
                "Contract symbols are required for summary. Setting include_contract_symbol to True."
            )
        include_contract_symbol = True

    if include_contract_symbol:
        df_res["contract"] = df_res["hour"].apply(iso_to_contract)

    if include_summary:
        if verbose:
            print("Getting MMS loss summary by contract...")
        df_summary = get_mms_loss_summary_by_contract(df_res)
        return {"detail": df_res, "summary": df_summary}

    return df_res


def get_mms_loss_summary_by_contract(df: pd.DataFrame):
    """
    This function gets the loss summary of the MMS data.
    """

    summary_df = (
        df.groupby("contract")[["faultCausedPowerLoss", "faultCausedEnergyLoss"]]
        .sum()
        .reset_index()
        .sort_values("contract", ignore_index=True)
    )

    return summary_df
