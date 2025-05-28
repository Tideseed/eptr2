from eptr2 import EPTR2
import pandas as pd
from eptr2.util.time import iso_to_contract


def get_day_ahead_and_bilateral_matches(
    eptr: EPTR2,
    start_date: str,
    end_date: str,
    verbose: bool = False,
    include_contract_symbol: bool = False,
    org_id: str = None,
):
    """
    This composite function gets day ahead and bilateral matches for the whole market or for a single organization.
    """

    if verbose:
        print("Getting day ahead matches...")

    df_da = eptr.call(
        "dam-clearing", start_date=start_date, end_date=end_date, org_id=org_id
    )

    df = df_da.rename(
        {"matchedBids": "da_long", "matchedOffers": "da_short"}, axis=1
    ).drop("hour", axis=1)

    if verbose:
        print("Getting bilateral long matches...")

    df_bi_long = eptr.call(
        "bi-long", start_date=start_date, end_date=end_date, org_id=org_id
    )

    df = df.merge(
        df_bi_long.rename({"quantity": "bi_long"}, axis=1).drop("hour", axis=1),
        on="date",
        how="left",
    )

    if verbose:
        print("Getting bilateral short matches...")

    df_bi_short = eptr.call(
        "bi-short", start_date=start_date, end_date=end_date, org_id=org_id
    )

    df = df.merge(
        df_bi_short.rename({"quantity": "bi_short"}, axis=1).drop("hour", axis=1),
        on="date",
        how="left",
    )

    if include_contract_symbol:
        try:
            df["contract"] = df["date"].apply(lambda x: iso_to_contract(x))
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    return df


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

    # df.fillna(0, inplace=True)

    if include_contract_symbol:
        try:
            df["contract"] = df["date"].apply(lambda x: iso_to_contract(x))
        except Exception as e:
            print("Contract information could not be added. Error:", e)

    return df
