import os
import time
from typing import Literal

import pandas as pd

from eptr2 import EPTR2
from eptr2.composite.price_and_cost import get_hourly_price_and_cost_data
from eptr2.composite.production import wrapper_hourly_production_plan_and_realized
from eptr2.util.costs import (
    calculate_kupsm,
    get_kupst_tolerance,
    get_kupst_tolerance_by_contract,
)


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
    start_date: str,
    end_date: str,
    pp_id: int | str,
    org_id: int | str,
    uevcb_id: int | str,
    plant_type: str,
    eptr: EPTR2 | None = None,
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

    if eptr is None:
        eptr = EPTR2(dotenv_path=kwargs.get("dotenv_path", ".env"))

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
        start_date=start_date,
        end_date=end_date,
        eptr=eptr,
        verbose=verbose,
        include_contract_symbol=True,
        org_id=org_id,
        uevcb_id=uevcb_id,
        timeout=timeout,
        **params,
        **kwargs,
    )

    cost_df = get_hourly_price_and_cost_data(
        start_date=start_date,
        end_date=end_date,
        eptr=eptr,
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


def calculate_portfolio_costs(
    start_date: str,
    end_date: str,
    id_df: pd.DataFrame,
    export_to_excel: bool = False,
    export_dir: str = "data",
    check_existing: bool = False,
    portfolio_name: str | None = None,
    translate_cost_summary: bool = False,
    verbose=True,
    **kwargs,
):
    """
    For a given portfolio (e.g. an aggregator) of power plants, this function calculates the overall imbalance and kupst costs based on provided production data. There are some caveats to consider.

    + This function is suitable for only production/generation portfolios (not consumption). If your portfolio includes consumption units, results will be inaccurate.
    + KUPST calculations are based on a single plant type. Aggregators have more complex rules that are not covered here.
    + Your portfolio does not have to be an aggregator but calculations resemble those of an aggregator. You can use this function to estimate costs for potential aggregators.
    """

    if not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)

    if portfolio_name is None:
        portfolio_name = ""
    else:
        portfolio_name = f"_{portfolio_name.lower()}"

    plan_realized_path = os.path.join(
        export_dir, f"portfolio{portfolio_name}_costs_data_{start_date}_{end_date}.xlsx"
    )

    if check_existing and os.path.exists(plan_realized_path):
        plan_realized_df = pd.read_excel(plan_realized_path)
    else:
        plan_realized_df = pd.DataFrame()
        id_df = id_df.reset_index(drop=True).copy()
        for idx, row in id_df.iterrows():
            if verbose:
                print(
                    f"Processing UEVCB: {row['uevcb_name']}", idx + 1, "of", len(id_df)
                )
            lives = kwargs.get("max_lives", 3)
            while lives > 0:
                try:
                    sub_df = wrapper_hourly_production_plan_and_realized(
                        start_date=start_date,
                        end_date=end_date,
                        org_id=row["org_id"],
                        uevcb_id=row["uevcb_id"],
                        rt_pp_id=row["rt_id"],
                        uevm_pp_id=row["uevm_id"],
                        verbose=verbose,
                        skip_uevm=True,
                    )
                    sub_df["org_id"] = row["org_id"]
                    sub_df["uevcb_id"] = row["uevcb_id"]
                    sub_df["rt_id"] = row["rt_id"]
                    sub_df["uevm_id"] = row["uevm_id"]
                    sub_df["uevcb_name"] = row["uevcb_name"]
                    sub_df["pp_name"] = row["rt_shortname"]
                    plan_realized_df = pd.concat(
                        [plan_realized_df, sub_df], ignore_index=True
                    )
                    break
                except Exception as e:
                    lives -= 1
                    print(f"Error occurred: {e}. Remaining lives: {lives}")
                    time.sleep(3)

        if export_to_excel:
            if verbose:
                print(f"Exporting cost details to Excel: {plan_realized_path}")

            plan_realized_df.to_excel(plan_realized_path, index=False)

    cost_df = get_hourly_price_and_cost_data(
        start_date=start_date,
        end_date=end_date,
        include_contract_symbol=True,
        add_kupst_cost=True,
    )

    summary_df = (
        plan_realized_df[
            ["contract", "toplam_kgup_v1", "toplam_kgup", "toplam_kudup", "total_rt"]
        ]
        .groupby("contract")
        .agg("sum")
        .reset_index()
    )

    ### PRODUCER ONLY; OTHERWISE FORECAST - ACTUAL
    summary_df["imb_da"] = summary_df["total_rt"] - summary_df["toplam_kgup_v1"]

    summary_df["kupsm_da"] = summary_df.apply(
        lambda row: calculate_kupsm(
            actual=row["total_rt"],
            forecast=row["toplam_kgup_v1"],
            tol=get_kupst_tolerance_by_contract(
                contract=row["contract"], source=row.get("source", "wind")
            ),
        ),
        axis=1,
    )

    ### PRODUCER ONLY; OTHERWISE FORECAST - ACTUAL
    summary_df["imb"] = summary_df["total_rt"] - summary_df["toplam_kgup"]

    summary_df["kupsm"] = summary_df.apply(
        lambda row: calculate_kupsm(
            actual=row["total_rt"],
            forecast=row["toplam_kudup"],
            tol=get_kupst_tolerance_by_contract(
                contract=row["contract"], source="wind"
            ),
        ),
        axis=1,
    )

    cost_summary_df = summary_df.merge(
        cost_df[
            [
                "contract",
                "mcp",
                "smp",
                "pos_imb_price",
                "neg_imb_price",
                "pos_imb_cost",
                "neg_imb_cost",
                "kupst_cost",
            ]
        ],
        on="contract",
        how="left",
    )

    for col in ["imb_da", "imb"]:
        cost_summary_df[f"{col}_cost"] = cost_summary_df.apply(
            lambda row: abs(row[col]) * row["pos_imb_cost"]
            if row[col] > 0
            else abs(row[col]) * row["neg_imb_cost"],
            axis=1,
        ).round(2)
    for col in ["kupsm_da", "kupsm"]:
        cost_summary_df[f"{col}_cost"] = (
            cost_summary_df[col] * cost_summary_df["kupst_cost"]
        ).round(2)
    cost_summary_df["total_da_cost"] = (
        cost_summary_df["imb_da_cost"] + cost_summary_df["kupsm_da_cost"]
    ).round(2)
    cost_summary_df["total_cost"] = (
        cost_summary_df["imb_cost"] + cost_summary_df["kupsm_cost"]
    ).round(2)

    cost_summary_df["cum_cost"] = cost_summary_df["total_cost"].cumsum()
    cost_summary_df["cum_da_cost"] = cost_summary_df["total_da_cost"].cumsum()

    col_order = [
        "contract",
        "total_cost",
        "total_da_cost",
        "imb",
        "imb_cost",
        "imb_da",
        "imb_da_cost",
        "kupsm",
        "kupsm_cost",
        "kupsm_da_cost",
        "kupsm_da",
        "total_rt",
        "toplam_kgup",
        "toplam_kgup_v1",
        "toplam_kudup",
        "pos_imb_cost",
        "neg_imb_cost",
        "kupst_cost",
        "mcp",
        "smp",
        "pos_imb_price",
        "neg_imb_price",
    ]

    all_cols = col_order + [x for x in cost_summary_df.columns if x not in col_order]
    cost_summary_df = cost_summary_df[all_cols]

    if translate_cost_summary:
        cost_summary_df = cost_summary_df.rename(
            columns={
                "contract": "Kontrat",
                "toplam_kgup_v1": "KGÜP V1",
                "toplam_kgup": "KGÜP",
                "toplam_kudup": "KUDÜP",
                "total_rt": "GZ Üretim",
                "imb_da": "GÖP Dengesizlik (MWh)",
                "kupsm_da": "GÖP KUPSM (MWh)",
                "imb": "Dengesizlik (MWh)",
                "kupsm": "KUPSM (MWh)",
                "mcp": "PTF (TL/MWh)",
                "smp": "SMF (TL/MWh)",
                "pos_imb_price": "PDF (TL/MWh)",
                "neg_imb_price": "NDF (TL/MWh)",
                "pos_imb_cost": "PDM (TL/MWh)",
                "neg_imb_cost": "NDM (TL/MWh)",
                "kupst_cost": "B.KÜPST (TL/MWh)",
                "imb_da_cost": "GÖP DM (TL)",
                "kupsm_da_cost": "GÖP KÜPST (TL)",
                "total_da_cost": "GÖP Toplam (TL)",
                "imb_cost": "DM (TL)",
                "kupsm_cost": "KÜPST (TL)",
                "total_cost": "Toplam (TL)",
                "cum_cost": "Kümülatif Toplam Maliyet (TL)",
                "cum_da_cost": "Kümülatif GÖP Maliyet (TL)",
            }
        )

    if export_to_excel:
        summary_path = os.path.join(
            export_dir,
            f"portfolio{portfolio_name}_summary_data_{start_date}_{end_date}.xlsx",
        )
        if verbose:
            print(f"Exporting cost summary to Excel: {summary_path}")
        cost_summary_df.to_excel(summary_path, index=False)

    return cost_summary_df


def create_template_id_df(
    export_to_excel: bool = False, export_path: str = "template_id_df.xlsx"
):
    """
    Creates a template DataFrame for portfolio cost calculations.
    """
    df = pd.DataFrame(
        columns=[
            "org_id",
            "uevcb_id",
            "rt_id",
            "uevm_id",
            "uevcb_name",
            "rt_shortname",
            "source",
        ]
    )
    if export_to_excel:
        df.to_excel(export_path, index=False)
    return df
