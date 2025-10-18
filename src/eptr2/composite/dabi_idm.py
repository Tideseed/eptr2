from eptr2 import EPTR2
import pandas as pd
from eptr2.util.time import (
    iso_to_contract,
    get_previous_day,
    get_start_end_dates_period,
)


def process_idm_data(
    eptr: EPTR2, start_date: str, end_date: str, org_id: str, **kwargs
) -> pd.DataFrame:
    """
    This function processes IDM data and includes it in the DataFrame.
    It fetches day ahead and bilateral matches, and merges them with IDM data.
    """
    lives = kwargs.get("lives", 2)
    while lives > 0:
        try:
            df = eptr.call(
                "idm-qty",
                start_date=get_previous_day(start_date),
                end_date=end_date,
                org_id=org_id,
                request_kwargs={"timeout": 5},
            )
            break
        except Exception as e:
            print("Error fetching IDM data:", e)
            lives -= 1
            if lives <= 0:
                raise Exception("Max lives reached. Exiting.")
            continue

    ### Due to naming confusion by EPIAS, ask is mapped to buy and bid is mapped to sell.

    if df.empty:
        df = pd.DataFrame(columns=["contract", "idm_long", "idm_short"])
    else:
        df = df.drop("kontratTuru", axis=1).rename(
            {
                "kontratAdi": "contract",
                "clearingQuantityAsk": "idm_long",
                "clearingQuantityBid": "idm_short",
            },
            axis=1,
        )

    return df


def get_day_ahead_and_bilateral_matches(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    include_contract_symbol: bool = False,
    org_id: str = None,
    include_idm_data: bool = False,
    include_org_id: bool = False,
    verbose: bool = False,
    **kwargs,
):
    """
    This composite function gets day ahead and bilateral matches for the whole market or for a single organization. You can also include IDM data if you provide an org_id.
    """

    if verbose:
        print("Getting day ahead matches...")

    lives = kwargs.get("lives", 2)
    while lives > 0:
        try:
            df_da = eptr.call(
                "dam-clearing",
                start_date=start_date,
                end_date=end_date,
                org_id=org_id,
                request_kwargs={"timeout": 5},
            )
            break
        except Exception as e:
            print("Error fetching day ahead matches:", e)
            lives -= 1
            if lives <= 0:
                raise Exception("Max lives reached. Exiting.")

            continue

    df = df_da.rename(
        {"matchedBids": "da_long", "matchedOffers": "da_short"}, axis=1
    ).drop("hour", axis=1)

    for cc in ["bi-long", "bi-short"]:
        if verbose:
            print(f"Getting bilateral {cc} matches...")

        lives = kwargs.get("lives", 2)
        while lives > 0:
            try:
                df_bi = eptr.call(
                    cc,
                    start_date=start_date,
                    end_date=end_date,
                    org_id=org_id,
                    request_kwargs={"timeout": 5},
                )

                df = df.merge(
                    df_bi.rename({"quantity": cc.replace("-", "_")}, axis=1).drop(
                        "hour", axis=1
                    ),
                    on="date",
                    how="left",
                )
                break
            except Exception as e:
                print("Error fetching bilateral long matches:", e)
                lives -= 1
                if lives <= 0:
                    raise Exception("Max lives reached. Exiting.")
                continue

    # if verbose:
    #     print("Getting bilateral short matches...")

    # df_bi_short = eptr.call(
    #     "bi-short",
    #     start_date=start_date,
    #     end_date=end_date,
    #     org_id=org_id,
    #     request_kwargs={"timeout": 5},
    # )

    # df = df.merge(
    #     df_bi_short.rename({"quantity": "bi_short"}, axis=1).drop("hour", axis=1),
    #     on="date",
    #     how="left",
    # )

    df["dabi_net"] = df["da_long"] - df["da_short"] + df["bi_long"] - df["bi_short"]

    if include_idm_data:
        include_contract_symbol = True

    if include_contract_symbol:
        try:
            df["contract"] = df["date"].apply(lambda x: iso_to_contract(x))
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    if include_idm_data:
        if verbose:
            print("Getting IDM data...")
        df_idm = process_idm_data(eptr, start_date, end_date, org_id)
        df = (
            df.merge(df_idm, on=["contract"], how="left")
            .fillna(0.0)
            .infer_objects(copy=False)
        )
        df["idm_net"] = df["idm_long"] - df["idm_short"]
        df["dabi_idm_net"] = df["dabi_net"] + df["idm_net"]
        df["dabi_idm_net"] = df["dabi_idm_net"].round(2)

    if include_org_id and org_id is not None:
        df["org_id"] = org_id

    return df


def get_dabi_idm_data(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    org_id: str | None = None,
    verbose: bool = False,
):
    """
    This function retrieves DABI IDM data for a specific organization. It is a wrapper around the `process_idm_data` function.
    """

    return get_day_ahead_and_bilateral_matches(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        include_idm_data=True,
        include_contract_symbol=True,
        include_org_id=True,
        verbose=verbose,
    )


def get_dabi_idm_data_period(
    eptr: EPTR2,
    period: str,
    org_id: str | None = None,
    verbose: bool = False,
):
    """
    This function retrieves DABI IDM data for a specific organization over a period.
    It is a wrapper around the `get_dabi_idm_data` function.
    """

    start_date, end_date = get_start_end_dates_period(period=period)

    return get_dabi_idm_data(
        eptr=eptr,
        start_date=start_date,
        end_date=end_date,
        org_id=org_id,
        verbose=verbose,
    )


def get_day_ahead_detail_info(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    verbose: bool = False,
    include_contract_symbol: bool = False,
    lives: int = 3,
    **kwargs,
) -> pd.DataFrame:
    """
    This function gets day ahead detail information such as regular, block, flexible bids & asks (offers).
    """

    df_d: dict[pd.DataFrame] = {}

    items = [
        "dam-bid",
        "dam-offer",
        "dam-block-bid",
        "dam-block-offer",
        "dam-flexible-bid",
        "dam-flexible-offer",
        # "dam-flexible-matching",
    ]

    map_d = {
        "dam-bid": {"bidQuantity": "bid"},
        "dam-offer": {"offerQuantity": "ask"},
        "dam-block-bid": {
            "amountOfPurchasingTowardsMatchedBlock": "block_long_match",
            "amountOfPurchasingTowardsUnMatchedBlock": "block_long_remaining",
        },
        "dam-block-offer": {
            "amountOfSalesTowardsMatchedBlock": "block_short_match",
            "amountOfSalesTowardsUnMatchedBlock": "block_short_remaining",
        },
        "dam-flexible-bid": {
            "totalBuyingFlexibleOfferQuantity": "flex_long_total",
            "matchedBuyingFlexibleOfferQuantity": "flex_long_match",
            "unmatchedBuyingFlexibleOfferQuantity": "flex_long_remaining",
        },
        "dam-flexible-offer": {
            "totalSellingFlexibleOfferQuantity": "flex_short_total",
            "matchedSellingFlexibleOfferQuantity": "flex_short_match",
            "unmatchedSellingFlexibleOfferQuantity": "flex_short_remaining",
        },
    }

    df: pd.DataFrame | None = None

    while len(items) > 0:
        for item in items:
            try:
                if verbose:
                    print(f"Fetching {item} data...")
                df_d[item] = eptr.call(
                    item,
                    start_date=start_date,
                    end_date=end_date,
                    request_kwargs={"timeout": kwargs.get("timeout", 5)},
                )

                df_d[item].rename(map_d[item], axis=1, inplace=True)
                if "hour" in df_d[item].columns:
                    df_d[item].drop("hour", axis=1, inplace=True)
                elif "time" in df_d[item].columns:
                    df_d[item].drop("time", axis=1, inplace=True)

                if df is None:
                    df = df_d[item].copy()
                else:
                    df = df.merge(df_d[item], on="date", how="outer")

            except Exception as e:
                if verbose:
                    print(f"Error fetching {item}: {e}")
                lives -= 1
                if lives <= 0:
                    print("Max lives reached. Exiting.")
                    break
                continue

        items = [item for item in items if item not in df_d or df_d[item].empty]

    if include_contract_symbol:
        try:
            df["contract"] = df["date"].apply(lambda x: iso_to_contract(x))
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    return df
