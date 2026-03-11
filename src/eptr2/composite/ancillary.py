import logging
from eptr2 import EPTR2
from eptr2.util.time import datetime_to_contract
import pandas as pd

logger = logging.getLogger(__name__)


def get_ancillary_reserve_data(
    start_date, end_date, eptr=None, verbose=False, **kwargs
):
    if eptr is None:
        eptr = EPTR2()

    if verbose:
        logger.info("Loading ancillary data...")

    calls_d = {
        "anc-pf-qty": "fcr_mwh",
        "anc-sf-qty": "afrr_mwh",
        "anc-pfk": "fcr_price",
        "anc-sfk": "afrr_price",
    }

    main_df = pd.DataFrame()

    for k, v in calls_d.items():
        df = eptr.call(
            k,
            start_date=start_date,
            end_date=end_date,
            request_kwargs={"timeout": 5},
        )

        try:
            df.drop(columns=["hour"], inplace=True)
        except Exception:
            pass

        if v.endswith("mwh"):
            df.rename(columns={"amount": v}, inplace=True)
        elif v.endswith("price"):
            df.rename(columns={"price": v}, inplace=True)

        if main_df.empty:
            main_df = df.copy()
            main_df["contract"] = main_df["date"].apply(
                lambda x: datetime_to_contract(x)
            )
            main_df = main_df[["date", "contract", v]].copy()
        else:
            main_df = main_df.merge(df, on=["date"], how="outer")

    main_df.rename(columns={"date": "dt"}, inplace=True)
    return main_df


if __name__ == "__main__":
    # eptr = EPTR2()
    # df = eptr.call(
    #     "anc-pf-qty",
    #     start_date="2026-01-01",
    #     end_date="2026-01-02",
    # )

    df = get_ancillary_reserve_data(
        start_date="2026-01-01",
        end_date="2026-01-02",
        verbose=True,
    )

    print("End")
