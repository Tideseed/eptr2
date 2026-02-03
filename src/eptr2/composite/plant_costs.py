import os
from typing import Literal

import pandas as pd

from eptr2 import EPTR2
from eptr2.composite.price_and_cost import get_hourly_price_and_cost_data
from eptr2.composite.production import wrapper_hourly_production_plan_and_realized
from eptr2.util.costs import (
    calculate_kupsm,
    get_kupst_tolerance,
    get_kupst_tolerance_by_contract,
    calculate_unit_imbalance_cost,
    calculate_unit_kupst_cost,
)
from eptr2.util.time import contract_to_floor_ceil_prices, date_str_to_contract


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
    *,
    plant_name_col="plant_name",
    export_to_excel: bool = False,
    export_dir: str = "data",
    check_existing: bool = False,
    portfolio_name: str | None = None,
    translate: bool = False,
    verbose=True,
    use_uevm=False,
    ignore_org_id=True,
    reduce_cost_details=False,
    forecast_source: Literal["kgup", "kudup"] = "kgup",
    use_latest_regulation: bool = False,
    include_price_range_adjustment: bool = False,
    **kwargs,
):
    """
    For a given portfolio (e.g. an aggregator) of power plants, this function calculates the overall imbalance and kupst costs based on provided production data. There are some caveats to consider.

    + This function is suitable for only production/generation portfolios (not consumption). If your portfolio includes consumption units, results will be inaccurate.
    + KUPST calculations are based on a single plant type. Aggregators have more complex rules that are not covered here.
    + Your portfolio does not have to be an aggregator but calculations resemble those of an aggregator. You can use this function to estimate costs for potential aggregators.
    """
    #####
    ### Validate forecast source
    if forecast_source.lower() in ["kgüp", "kgup", "kagup", "kagüp"]:
        forecast_source = "kgup"
    elif forecast_source.lower() in ["kudüp", "kudup"]:
        forecast_source = "kudup"

    if forecast_source not in ["kgup", "kudup"]:
        raise ValueError(
            "forecast_source must be either 'kgup' or 'kudup'. For day ahead forecasts, we use kgup_v1 by default."
        )

    if use_latest_regulation:
        if forecast_source == "kudup":
            raise ValueError(
                "When using latest regulation, 'kudup' forecast source is not supported as aggregator uevcb organizations might be different by then. Please use 'kgup' as forecast source."
            )

    if ignore_org_id:
        if forecast_source == "kudup":
            raise ValueError(
                "When using 'kudup' as forecast source, org_id is required. Set ignore_org_id=False or use kgup as forecast_source."
            )

    if forecast_source == "kgup":
        kwargs["skip_kgup"] = False
        kwargs["skip_kudup"] = True
    else:
        kwargs["skip_kgup"] = True
        kwargs["skip_kudup"] = False
    ##########

    res_d = {}

    if not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)

    if portfolio_name is None:
        portfolio_name = ""
    else:
        portfolio_name = f"_{portfolio_name.lower().replace(' ', '_')}"

    excel_export_path = os.path.join(
        export_dir, f"portfolio{portfolio_name}_costs_data_{start_date}_{end_date}.xlsx"
    )

    if check_existing and os.path.exists(excel_export_path):
        res_d["costs_detail"] = pd.read_excel(
            excel_export_path, sheet_name="costs_detail"
        )
        res_d["contract_summary"] = pd.read_excel(
            excel_export_path, sheet_name="contract_summary"
        )
        return res_d

    plan_realized_df = pd.DataFrame()
    id_df = id_df.reset_index(drop=True).copy()
    res_d["plant_info"] = id_df.copy()
    for idx, row in id_df.iterrows():
        if verbose:
            print(f"Processing Plant: {row[plant_name_col]}", idx + 1, "of", len(id_df))

        sub_df = wrapper_hourly_production_plan_and_realized(
            start_date=start_date,
            end_date=end_date,
            org_id=row["org_id"] if not ignore_org_id else None,
            uevcb_id=row["uevcb_id"],
            rt_pp_id=row["rt_id"],
            uevm_pp_id=row["uevm_id"] if use_uevm else None,
            verbose=verbose,
            include_contract_symbol=True,
            **kwargs,
        )
        sub_df["uevcb_id"] = row["uevcb_id"]
        sub_df["plant_name"] = row[plant_name_col]

        if use_uevm:
            sub_df["actual"] = sub_df.apply(
                lambda x: x["total_rt"]
                if pd.isna(x["total_uevm"])
                else x["total_uevm"],
                axis=1,
            )
        else:
            sub_df["actual"] = sub_df["total_rt"]

        sub_df["da_forecast"] = sub_df["toplam_kgup_v1"]
        sub_df["forecast"] = sub_df[f"toplam_{forecast_source}"]
        ## Negative means underproduction, negative imbalance
        sub_df["imb_qty"] = sub_df["actual"] - sub_df["forecast"]
        sub_df["da_imb_qty"] = sub_df["actual"] - sub_df["da_forecast"]
        for pfx in ["", "da_"]:
            if use_latest_regulation:
                tol = get_kupst_tolerance(
                    source=row.get("source", "other"), regulation_period="current"
                )
            else:
                tol = get_kupst_tolerance_by_contract(
                    contract=sub_df["contract"].iloc[0],
                    source=row.get("source", "other"),
                )

            sub_df[f"{pfx}kupsm"] = sub_df.apply(
                lambda subrow: calculate_kupsm(
                    actual=subrow["actual"],
                    forecast=subrow[f"{pfx}forecast"],
                    tol=tol,
                ),
                axis=1,
            )

        if reduce_cost_details:
            sub_df = sub_df[
                [
                    "contract",
                    "plant_name",
                    "uevcb_id",
                    "da_forecast",
                    "forecast",
                    "actual",
                    "da_imb_qty",
                    "imb_qty",
                    "da_kupsm",
                    "kupsm",
                ]
            ]

        plan_realized_df = pd.concat([plan_realized_df, sub_df], ignore_index=True)

    # res_d["costs_detail"] = plan_realized_df.copy()

    cost_df = kwargs.get("cost_df", None)
    if cost_df is None:
        cost_df = get_hourly_price_and_cost_data(
            start_date=start_date,
            end_date=end_date,
            include_contract_symbol=True,
            add_kupst_cost=True,
            add_unit_prefix_to_cost_colnames=True,
            verbose=verbose,
        )

        if use_latest_regulation:
            if verbose:
                print(
                    "Using latest regulation for cost data. But beware, currently we adjust ceiling prices only based on start date."
                )

            ceil_price = contract_to_floor_ceil_prices(
                c=date_str_to_contract(start_date)
            )["max"]

            cost_df2 = cost_df[["contract", "mcp", "smp", "sd_sign"]].copy()
            temp_series = cost_df2.apply(
                lambda row: calculate_unit_imbalance_cost(
                    mcp=row["mcp"],
                    smp=row["smp"],
                    include_prices=True,
                    regulation_period="current",
                    ceil_price=ceil_price,
                    sd_sign=row["sd_sign"],
                ),
                axis=1,
            )
            cost_df2 = pd.concat([cost_df2, pd.json_normalize(temp_series)], axis=1)
            cost_df2["unit_kupst_cost"] = cost_df2.apply(
                lambda row: calculate_unit_kupst_cost(
                    mcp=row["mcp"], smp=row["smp"], regulation_period="current"
                ),
                axis=1,
            )
            cost_df = cost_df2.reset_index(drop=True).copy()

    plan_realized_w_costs_df = plan_realized_df.merge(
        cost_df[
            [
                "contract",
                "sd_sign",
                "unit_pos_imb_cost",
                "unit_neg_imb_cost",
                "unit_kupst_cost",
            ]
        ],
        on="contract",
        how="left",
    )

    # plan_realized_w_costs_df["kupsm_da"] = plan_realized_w_costs_df.apply(
    #     lambda row: calculate_kupsm(
    #         actual=row["actual"],
    #         forecast=row["forecast"],
    #         tol=get_kupst_tolerance_by_contract(
    #             contract=row["contract"], source=row.get("source", "other")
    #         ),
    #     ),
    #     axis=1,
    # )

    unit_costs_l = []
    total_actual = plan_realized_w_costs_df["actual"].sum()

    for pfx in ["da_", ""]:
        plan_realized_w_costs_df[f"{pfx}imb_cost"] = plan_realized_w_costs_df.apply(
            lambda row: abs(row[f"{pfx}imb_qty"]) * row["unit_pos_imb_cost"]
            if row[f"{pfx}imb_qty"] > 0
            else abs(row[f"{pfx}imb_qty"]) * row["unit_neg_imb_cost"],
            axis=1,
        ).round(2)
        plan_realized_w_costs_df[f"{pfx}kupst_cost"] = (
            plan_realized_w_costs_df[f"{pfx}kupsm"]
            * plan_realized_w_costs_df["unit_kupst_cost"]
        ).round(2)
        plan_realized_w_costs_df[f"{pfx}total_cost"] = (
            plan_realized_w_costs_df[f"{pfx}imb_cost"]
            + plan_realized_w_costs_df[f"{pfx}kupst_cost"]
        ).round(2)

        total_imb_cost = plan_realized_w_costs_df[f"{pfx}imb_cost"].sum()
        total_kupst_cost = plan_realized_w_costs_df[f"{pfx}kupst_cost"].sum()

        unit_costs_l.extend(
            [
                {
                    "cost": f"{pfx}unit_kupst_cost",
                    "cost_version": "pre_aggregator",
                    "value": total_kupst_cost / total_actual,
                },
                {
                    "cost": f"{pfx}unit_imb_cost",
                    "cost_version": "pre_aggregator",
                    "value": total_imb_cost / total_actual,
                },
                {
                    "cost": f"{pfx}unit_total_cost",
                    "cost_version": "pre_aggregator",
                    "value": (total_kupst_cost + total_imb_cost) / total_actual,
                },
            ]
        )

    # plan_realized_w_costs_df = plan_realized_w_costs_df.drop(
    #     columns=[
    #         "unit_pos_imb_cost",
    #         "unit_neg_imb_cost",
    #         "unit_kupst_cost",
    #     ]
    # ).copy()

    res_d["costs_detail"] = plan_realized_w_costs_df.copy()

    #####
    ## SUMMARY BY CONTRACT
    #####
    summary_by_contract_df_raw = (
        plan_realized_w_costs_df[
            [
                "contract",
                "da_forecast",
                "forecast",
                "actual",
                "da_kupsm",
                "kupsm",
                "da_kupst_cost",
                "kupst_cost",
            ]
        ]
        .groupby("contract")
        .agg("sum")
        .reset_index()
    )

    ### PRODUCER ONLY; OTHERWISE FORECAST - ACTUAL
    summary_by_contract_df_raw["da_imb_qty"] = (
        summary_by_contract_df_raw["actual"] - summary_by_contract_df_raw["da_forecast"]
    )

    ### PRODUCER ONLY; OTHERWISE FORECAST - ACTUAL
    summary_by_contract_df_raw["imb_qty"] = (
        summary_by_contract_df_raw["actual"] - summary_by_contract_df_raw["forecast"]
    )

    cost_summary_by_contract_df = summary_by_contract_df_raw.merge(
        cost_df[
            [
                "contract",
                "mcp",
                "smp",
                "pos_imb_price",
                "neg_imb_price",
                "unit_pos_imb_cost",
                "unit_neg_imb_cost",
                "unit_kupst_cost",
            ]
        ],
        on="contract",
        how="left",
    )

    for pfx in ["da_", ""]:
        cost_summary_by_contract_df[f"{pfx}imb_cost"] = (
            cost_summary_by_contract_df.apply(
                lambda row: abs(row[pfx + "imb_qty"]) * row["unit_pos_imb_cost"]
                if row[pfx + "imb_qty"] > 0
                else abs(row[pfx + "imb_qty"]) * row["unit_neg_imb_cost"],
                axis=1,
            ).round(2)
        )

        total_imb_cost = cost_summary_by_contract_df[f"{pfx}imb_cost"].sum()
        total_kupst_cost = cost_summary_by_contract_df[f"{pfx}kupst_cost"].sum()

        unit_costs_l.extend(
            [
                {
                    "cost": f"{pfx}unit_kupst_cost",
                    "cost_version": "aggregator",
                    "value": total_kupst_cost / total_actual,
                },
                {
                    "cost": f"{pfx}unit_imb_cost",
                    "cost_version": "aggregator",
                    "value": total_imb_cost / total_actual,
                },
                {
                    "cost": f"{pfx}unit_total_cost",
                    "cost_version": "aggregator",
                    "value": (total_kupst_cost + total_imb_cost) / total_actual,
                },
            ]
        )

    cost_summary_by_contract_df["da_total_cost"] = (
        cost_summary_by_contract_df["da_imb_cost"]
        + cost_summary_by_contract_df["da_kupst_cost"]
    ).round(2)
    cost_summary_by_contract_df["total_cost"] = (
        cost_summary_by_contract_df["imb_cost"]
        + cost_summary_by_contract_df["kupst_cost"]
    ).round(2)

    col_order = [
        "contract",
        "actual",
        ## Day Ahead
        "da_forecast",
        "da_imb_qty",
        "da_kupsm",
        "da_imb_cost",
        "da_kupst_cost",
        "da_total_cost",
        ##
        ## Intraday
        "forecast",
        "imb_qty",
        "kupsm",
        "imb_cost",
        "kupst_cost",
        "total_cost",
        ##
        ## Price Data
        "mcp",
        "smp",
        "pos_imb_price",
        "neg_imb_price",
        "unit_pos_imb_cost",
        "unit_neg_imb_cost",
        "unit_kupst_cost",
    ]

    all_cols = col_order + [
        x for x in cost_summary_by_contract_df.columns if x not in col_order
    ]
    cost_summary_by_contract_df = cost_summary_by_contract_df[all_cols]

    if translate:
        cost_summary_by_contract_df_translated = cost_summary_by_contract_df.rename(
            columns={
                "contract": "Kontrat",
                "actual": "Gerçekleşen",
                "da_forecast": "GÖP Tahmin",
                "da_imb_qty": "GÖP Dengesizlik (MWh)",
                "da_kupsm": "GÖP KUPSM (MWh)",
                "da_imb_cost": "GÖP DM (TL)",
                "da_kupst_cost": "GÖP KÜPST (TL)",
                "da_total_cost": "GÖP Toplam (TL)",
                "forecast": "Tahmin",
                "imb_qty": "Dengesizlik (MWh)",
                "kupsm": "KUPSM (MWh)",
                "imb_cost": "DM (TL)",
                "kupst_cost": "KÜPST (TL)",
                "total_cost": "Toplam (TL)",
                "mcp": "PTF (TL/MWh)",
                "smp": "SMF (TL/MWh)",
                "pos_imb_price": "PDF (TL/MWh)",
                "neg_imb_price": "NDF (TL/MWh)",
                "unit_pos_imb_cost": "Birim PDM (TL/MWh)",
                "unit_neg_imb_cost": "Birim NDM (TL/MWh)",
                "unit_kupst_cost": "Birim KÜPST (TL/MWh)",
            }
        )

        res_d["contract_summary"] = cost_summary_by_contract_df_translated.copy()
    else:
        res_d["contract_summary"] = cost_summary_by_contract_df.copy()

    ### Summary of summaries

    unit_costs_df = pd.DataFrame(unit_costs_l)
    unit_costs_df["value"] = unit_costs_df["value"].round(2)
    unit_costs_df = unit_costs_df.pivot(
        index="cost", columns="cost_version", values="value"
    ).reset_index()

    sos_df = (
        plan_realized_w_costs_df[
            [
                x
                for x in plan_realized_w_costs_df.columns
                if x.endswith("_cost") and not x.startswith("unit_")
            ]
        ]
        .sum()
        .reset_index(drop=False)
        .rename(columns={"index": "cost", 0: "pre_aggregator"})
    )

    cs_df = (
        cost_summary_by_contract_df[
            [
                x
                for x in cost_summary_by_contract_df.columns
                if x.endswith("_cost") and not x.startswith("unit_")
            ]
        ]
        .sum()
        .reset_index(drop=False)
        .rename(columns={"index": "cost", 0: "aggregator"})
    )

    sos_df = sos_df.merge(cs_df, on="cost", how="outer")

    sos_df = pd.concat([sos_df, unit_costs_df], axis=0, ignore_index=True)

    sos_df["savings"] = (sos_df["pre_aggregator"] - sos_df["aggregator"]).round(2)

    sos_df["savings_perc"] = (
        1 - sos_df["aggregator"] / sos_df["pre_aggregator"]
    ).round(4)

    if translate:
        sos_df_translated = sos_df.rename(
            columns={
                "cost": "Maliyet Kalemi",
                "pre_aggregator": "Toplayıcı Öncesi (TL)",
                "aggregator": "Toplayıcı İle (TL)",
                "savings": "Tasarruf (TL)",
                "savings_perc": "Tasarruf (%)",
            }
        )
        res_d["final_summary"] = sos_df_translated.copy()
    else:
        res_d["final_summary"] = sos_df.copy()

    if export_to_excel:
        name_map = {
            "plant_info": "Santral Bilgileri",
            "costs_detail": "Detay Maliyetler",
            "contract_summary": "Kontrat Bazlı Toplayıcı Özeti",
            "final_summary": "Nihai Özet",
        }

        if verbose:
            print(f"Exporting cost details to Excel: {excel_export_path}")
        with pd.ExcelWriter(excel_export_path) as writer:
            for k, v in res_d.items():
                v: pd.DataFrame
                v.to_excel(
                    writer,
                    sheet_name=name_map.get(k, k) if translate else k,
                    index=False,
                )

    return res_d


def create_template_id_df(
    export_to_excel: bool = False,
    export_dir: str = "data",
    export_file_name: str = "portfolio_costs_template_id_df.xlsx",
):
    """
    Creates a template DataFrame for portfolio cost calculations.
    """
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, export_file_name)

    df = pd.DataFrame(
        columns=[
            "plant_name",
            "org_id",
            "uevcb_id",
            "rt_id",
            "uevm_id",
            "source",
        ]
    )
    if export_to_excel:
        df.to_excel(export_path, index=False)
    return df
