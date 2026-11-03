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
