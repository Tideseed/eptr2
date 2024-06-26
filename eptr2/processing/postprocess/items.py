import pandas as pd
import json


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
        print(e)

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
def postprocess_ren_capacity_dict_to_df(res, **kwargs):
    df = pd.DataFrame(res["installedCapacities"])
    return df
