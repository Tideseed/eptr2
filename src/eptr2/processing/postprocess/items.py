import pandas as pd
import json
import logging


logger = logging.getLogger(__name__)


def postprocess_direct_dict(res, key: str | None = None):
    ## for date-init
    subkey_map = {
        "dam-list": "damList",
    }

    subkey = subkey_map.get(key, None)
    d = res
    try:
        if subkey is not None:
            return d[subkey]
    except Exception as e:
        logger.warning("%s", e)

    return d


def postprocess_direct_dict_to_df(res, **kwargs):
    ## for date-init
    return pd.DataFrame(res)


def postprocess_mcp_status(res, **kwargs):
    return res["body"]["content"]["completed"]


def postprocess_items_to_df(res, **kwargs):
    df = pd.DataFrame(res["items"])
    return df


## Adhoc non-standard response postprocess
def postprocess_mcp_smp_imb(res, **kwargs):
    ## EPİAŞ returned every hour of 2026-11-01 twice (identical rows); drop identical rows
    df = pd.DataFrame(res["items"])
    n_rows = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    if len(df) < n_rows:
        logger.warning(
            "mcp-smp-imb: dropped %d duplicate row(s) returned by EPİAŞ.",
            n_rows - len(df),
        )
    if "date" in df.columns and df["date"].duplicated().any():
        logger.warning(
            "mcp-smp-imb: conflicting rows for the same hour, kept as returned: %s",
            sorted(df.loc[df["date"].duplicated(), "date"].unique()),
        )
    return df


def postprocess_idm_qty(res, **kwargs):
    ## EPİAŞ labels GİP purchases (alış) as clearingQuantityAsk and sales (satış) as
    ## clearingQuantityBid; swap them so Bid = bought and Ask = sold, as on the platform page
    df = pd.DataFrame(res["items"])
    return df.rename(
        columns={
            "clearingQuantityAsk": "clearingQuantityBid",
            "clearingQuantityBid": "clearingQuantityAsk",
        }
    )


def postprocess_ren_capacity_dict_to_df(res, **kwargs):
    df = pd.DataFrame(res["installedCapacities"])
    return df
