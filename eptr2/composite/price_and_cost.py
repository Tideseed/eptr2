from eptr2 import EPTR2
from eptr2.util.costs import calculate_unit_kupst_cost
import pandas as pd


def get_hourly_price_and_cost_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    include_wap: bool = True,
    add_kupst_cost: bool = True,
    verbose: bool = False,
):
    """
    This composite function gets price and imbalance (kupst included) cost data.
    Imbalance cost data consists of MCP (PTF), SMP (SMF), system direction (Enerji Açığı - up regulated, Energy Fazlası - down regulated, Dengede - Balanced), positive imbalance cost and negative imbalance cost.

    Resulting columns are:
    - date: Datetime in ISO format and +03:00 timezone
    - mcp: Market Clearing Price (MCP/PTF) in TL (Turkish Lira)
    - smp: System Marginal Price (SMP/SMF) in TL (Turkish Lira)
    - wap: Weighted Average Price (WAP) in TL (Turkish Lira)
    - system_direction: System direction (Enerji Açığı - up regulated, Energy Fazlası - down regulated, Dengede - Balanced)
    - sd_sign: System direction sign (1 for Enerji Fazlası, -1 for Enerji Açığı, 0 for Dengede)
    - pos_imb_price: Positive imbalance price in TL (Turkish Lira)
    - neg_imb_price: Negative imbalance price in TL (Turkish Lira) (negative value)
    - pos_imb_cost: Positive imbalance cost in TL (Turkish Lira) (ptf - pos_imb_price)
    - neg_imb_cost: Negative imbalance cost in TL (Turkish Lira) (neg_imb_price - ptf)
    """

    if verbose:
        print("Getting MCP, SMP and imbalance price data...")

    price_df = eptr.call("mcp-smp-imb", start_date=start_date, end_date=end_date)

    price_df.drop(columns=["time"], inplace=True)

    price_df.rename(
        columns={
            "ptf": "mcp",
            "smf": "smp",
            "positiveImbalance": "pos_imb_price",
            "negativeImbalance": "neg_imb_price",
            "systemStatus": "system_direction",
        },
        inplace=True,
    )

    price_df["sd_sign"] = price_df["system_direction"].apply(
        lambda x: -1 if x == "Enerji Açığı" else 1 if x == "Enerji Fazlası" else 0
    )

    price_df["pos_imb_cost"] = price_df["mcp"] - price_df["pos_imb_price"]
    price_df["neg_imb_cost"] = price_df["neg_imb_price"] - price_df["mcp"]

    if include_wap:
        if verbose:
            print("Getting WAP data...")
        wap_df = eptr.call("wap", start_date=start_date, end_date=end_date)
        wap_df.drop(columns=["hour"], inplace=True)

        price_df = price_df.merge(wap_df, on="date", how="outer")

    if add_kupst_cost:
        if verbose:
            print("Calculating unit KUPST cost...")

        price_df["kupst_cost"] = price_df.apply(
            lambda x: calculate_unit_kupst_cost(mcp=x["mcp"], smp=x["smp"]), axis=1
        )

    ### Column ordering
    columns_order = [
        "date",
        "pos_imb_vol",
        "neg_imb_vol",
        "pos_imb_mwh",
        "neg_imb_mwh",
        "mcp",
        "wap",
        "smp",
        "pos_imb_price",
        "neg_imb_price",
        "system_direction",
        "sd_sign",
        "pos_imb_cost",
        "neg_imb_cost",
        "kupst_cost",
    ]

    columns_order = [col for col in columns_order if col in price_df.columns]

    price_df = price_df[columns_order]

    return price_df


def get_hourly_imbalance_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    include_price_and_cost_data: bool = True,
    include_wap: bool = True,
    add_kupst_cost: bool = True,
    verbose: bool = False,
):
    """
    This composite function gets imbalance volume, imbalance quantity and imbalance cost data.
    Imbalance cost data consists of MCP (PTF), SMP (SMF), system direction (Enerji Açığı - up regulated, Energy Fazlası - down regulated, Dengede - Balanced), positive imbalance cost and negative imbalance cost.

    Resulting columns are:
    - date: Datetime in ISO format and +03:00 timezone
    - pos_imb_vol: Positive imbalance volume in TL (Turkish Lira)
    - neg_imb_vol: Negative imbalance volume in TL (Turkish Lira) (negative value)
    - pos_imb_mwh: Positive imbalance quantity in MWh
    - neg_imb_mwh: Negative imbalance quantity in MWh (negative value)
    - mcp: Market Clearing Price (MCP/PTF) in TL (Turkish Lira)
    - smp: System Marginal Price (SMP/SMF) in TL (Turkish Lira)
    - system_direction: System direction (Enerji Açığı - up regulated, Energy Fazlası - down regulated, Dengede - Balanced)
    - sd_sign: System direction sign (1 for Enerji Fazlası, -1 for Enerji Açığı, 0 for Dengede)
    - pos_imb_price: Positive imbalance price in TL (Turkish Lira)
    - neg_imb_price: Negative imbalance price in TL (Turkish Lira) (negative value)
    - pos_imb_cost: Positive imbalance cost in TL (Turkish Lira) (ptf - pos_imb_price)
    - neg_imb_cost: Negative imbalance cost in TL (Turkish Lira) (neg_imb_price - ptf)
    """

    imb_vol_df = eptr.call(
        "imb-vol", start_date=start_date, end_date=end_date, verbose=verbose
    )

    if imb_vol_df.empty:
        raise ValueError(
            "Imbalance data returns empty. Settlement data is published after the 15th of the next month (e.g. May data is published at June 15 earliest) or in the first following working day normally. Check the date range."
        )

    imb_vol_df.drop(columns=["hour"], inplace=True)
    imb_vol_df.rename(
        columns={
            "positiveImbalance": "pos_imb_vol",
            "negativeImbalance": "neg_imb_vol",
        },
        inplace=True,
    )

    imb_vol_df["neg_imb_vol"] = -imb_vol_df["neg_imb_vol"]

    imb_qty_df = eptr.call(
        "imb-qty", start_date=start_date, end_date=end_date, verbose=verbose
    )
    imb_qty_df.drop(columns=["hour"], inplace=True)

    imb_qty_df.rename(
        columns={
            "positiveImbalance": "pos_imb_mwh",
            "negativeImbalance": "neg_imb_mwh",
        },
        inplace=True,
    )

    imb_qty_df["neg_imb_mwh"] = -imb_qty_df["neg_imb_mwh"]

    merged_df = imb_vol_df.merge(imb_qty_df, on="date", how="outer")

    if not include_price_and_cost_data:
        return merged_df

    price_df = get_hourly_price_and_cost_data(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        include_wap=include_wap,
        add_kupst_cost=add_kupst_cost,
        verbose=verbose,
    )

    merged_df = merged_df.merge(price_df, on="date", how="outer")

    return merged_df
