from eptr2 import EPTR2
import pandas as pd


def get_imbalance_data(
    eptr: EPTR2, start_date: str, end_date: str, verbose: bool = False
):
    """
    This composite function gets imbalance volume, imbalance quantity and imbalance cost data.
    Imbalance cost data consists of MCP (ptf), SMP (smf), system direction (Enerji Açığı - up regulated, Energy Fazlası - down regulated, Dengede - Balanced), positive imbalance cost and negative imbalance cost.

    Resulting columns are:
    - date: Datetime in ISO format and +03:00 timezone
    - pos_imb_vol: Positive imbalance volume in TL (Turkish Lira)
    - neg_imb_vol: Negative imbalance volume in TL (Turkish Lira) (negative value)
    - pos_imb_mwh: Positive imbalance quantity in MWh
    - neg_imb_mwh: Negative imbalance quantity in MWh (negative value)
    - ptf: Market Clearing Price (MCP) in TL (Turkish Lira)
    - smf: System Marginal Price (SMP) in TL (Turkish Lira)
    - system_direction: System direction (Enerji Açığı - up regulated, Energy Fazlası - down regulated, Dengede - Balanced)
    - sd_sign: System direction sign (1 for Enerji Fazlası, -1 for Enerji Açığı, 0 for Dengede)
    - pos_imb_price: Positive imbalance price in TL (Turkish Lira)
    - neg_imb_price: Negative imbalance price in TL (Turkish Lira) (negative value)
    - pos_imb_cost: Positive imbalance cost in TL (Turkish Lira) (ptf - pos_imb_price)
    - neg_imb_cost: Negative imbalance cost in TL (Turkish Lira) (neg_imb_price - ptf)
    """

    imb_vol_df = eptr.call(
        "imb-vol", start_date=start_date, end_date=end_date, verbose=True
    )
    imb_vol_df.drop(columns=["hour"], inplace=True)
    imb_vol_df.rename(
        columns={
            "positiveImbalance": "pos_imb_vol",
            "negativeImbalance": "neg_imb_vol",
        },
        inplace=True,
    )

    imb_qty_df = eptr.call(
        "imb-qty", start_date=start_date, end_date=end_date, verbose=True
    )
    imb_qty_df.drop(columns=["hour"], inplace=True)

    imb_qty_df.rename(
        columns={
            "positiveImbalance": "pos_imb_mwh",
            "negativeImbalance": "neg_imb_mwh",
        },
        inplace=True,
    )

    merged_df = imb_vol_df.merge(imb_qty_df, on="date", how="outer")

    price_df = eptr.call("mcp-smp-imb", start_date=start_date, end_date=end_date)

    price_df.drop(columns=["time"], inplace=True)

    price_df.rename(
        columns={
            "positiveImbalance": "pos_imb_price",
            "negativeImbalance": "neg_imb_price",
            "systemStatus": "system_direction",
        },
        inplace=True,
    )

    price_df["sd_sign"] = price_df["system_direction"].apply(
        lambda x: -1 if x == "Enerji Açığı" else 1 if x == "Enerji Fazlası" else 0
    )

    price_df["pos_imb_cost"] = price_df["ptf"] - price_df["pos_imb_price"]
    price_df["neg_imb_cost"] = price_df["neg_imb_price"] - price_df["ptf"]

    merged_df = merged_df.merge(price_df, on="date", how="outer")

    return merged_df
