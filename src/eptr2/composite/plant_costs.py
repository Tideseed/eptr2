from eptr2 import EPTR2
import pandas as pd
from eptr2.composite.production import wrapper_hourly_production_plan_and_realized
from eptr2.composite.price_and_cost import get_hourly_price_and_cost_data
from eptr2.util.costs import calculate_kupsm, get_kupst_tolerance
from typing import Literal


def postprocess_plant_cost_df(df: pd.DataFrame):
    df["cumulative_kupst_cost"] = df["total_kupst_cost"].cumsum()
    df["cumulative_imb_cost"] = df["total_imb_cost"].cumsum()
    df["cumulative_total_cost"] = df["total_cost"].cumsum()

    d = {
        "total_forecast": df["forecast"].sum(),
        "total_actual": df["actual"].sum(),
        "total_kupsm": df["kupsm"].sum(),
        "total_bias": df["diff"].sum(),
        "total_mae": df["diff"].abs().sum(),
        "total_kupst_cost": df["total_kupst_cost"].sum(),
        "total_imb_cost": df["total_imb_cost"].sum(),
        "total_cost": df["total_cost"].sum(),
    }

    return {"summary": d, "data": df}


def gather_and_calculate_plant_costs(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    pp_id: int | str,
    org_id: int | str,
    uevcb_id: int | str,
    plant_type: str,
    forecast_source: Literal["kgup_v1", "kgup", "kudup"] = "kudup",
    actual_source: Literal["rt", "uevm"] = "uevm",
    verbose=False,
    timeout=5,
    postprocess: bool = False,
    **kwargs,
):
    """
    For a given power plant and selected forecast and actual production sources, this function gathers data and calculates imbalance and kupst costs.

    Example usage:
    pp_id=120,  ## BOZCAADA RES
    org_id=195,  ## EÜAŞ
    uevcb_id=3204384,  ## BOZCAADA RES
    plant_type="wind",
    """

    ### Regulate skips
    params = dict(
        skip_kgup=True,
        skip_kgup_v1=True,
        skip_kudup=True,
        skip_uevm=True,
        skip_rt=True,
    )

    params[f"skip_{forecast_source}"] = False
    params[f"skip_{actual_source}"] = False

    ### Regulate ids
    if actual_source == "rt":
        params["rt_pp_id"] = pp_id
        params["uevm_pp_id"] = None
    else:
        params["rt_pp_id"] = None
        params["uevm_pp_id"] = pp_id

    df = wrapper_hourly_production_plan_and_realized(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        verbose=verbose,
        include_contract_symbol=True,
        org_id=org_id,
        uevcb_id=uevcb_id,
        timeout=timeout,
        **params,
        **kwargs,
    )

    cost_df = get_hourly_price_and_cost_data(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        verbose=verbose,
        include_contract_symbol=True,
        include_wap=False,
        timeout=timeout,
    )

    #### Merge and calculate costs
    prod_df = (
        df[["dt", "contract", f"toplam_{forecast_source}", f"total_{actual_source}"]]
        .rename(
            columns={
                f"toplam_{forecast_source}": "forecast",
                f"total_{actual_source}": "actual",
            }
        )
        .copy()
    )

    prod_df["diff"] = prod_df["forecast"] - prod_df["actual"]

    merged_df = prod_df.merge(
        cost_df.rename(columns={"date": "dt"})[
            ["dt", "pos_imb_cost", "neg_imb_cost", "kupst_cost"]
        ],
        on="dt",
        how="inner",
    )

    ## Calculate kupsm and costs
    kupst_tolerance = get_kupst_tolerance(plant_type)
    merged_df["kupsm"] = merged_df.apply(
        lambda row: calculate_kupsm(
            actual=row["actual"], forecast=row["forecast"], tol=kupst_tolerance
        ),
        axis=1,
    )

    ### Calculate total costs
    merged_df["total_kupst_cost"] = merged_df["kupsm"] * merged_df["kupst_cost"]
    merged_df["total_imb_cost"] = merged_df.apply(
        lambda row: (row["pos_imb_cost"] if row["diff"] < 0 else row["neg_imb_cost"])
        * abs(row["diff"]),
        axis=1,
    )
    merged_df["total_cost"] = (
        merged_df["total_kupst_cost"] + merged_df["total_imb_cost"]
    )

    if postprocess:
        d = postprocess_plant_cost_df(merged_df)
        return d

    return merged_df
