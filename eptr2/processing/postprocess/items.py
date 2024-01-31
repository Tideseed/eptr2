import pandas as pd


def postprocess_direct_dict(res, key: str | None = None):
    ## for date-init
    subkey_map = {
        "dam-list": "damList",
    }

    subkey = subkey_map.get(key, None)
    d = res.json()
    try:
        if subkey is not None:
            return d[subkey]
    except Exception as e:
        print(e)

    return d


def postprocess_direct_dict_to_df(res, **kwargs):
    ## for date-init
    return pd.DataFrame(res.json())


def postprocess_mcp_status(res, **kwargs):
    return res.json()["body"]["content"]["completed"]


def postprocess_items_to_df(res, **kwargs):
    df = pd.DataFrame(res.json()["items"])
    return df


## Adhoc non-standard response postprocess
def postprocess_ren_capacity_dict_to_df(res, **kwargs):
    df = pd.DataFrame(res.json()["installedCapacities"])
    return df
