import pandas as pd


def postprocess_direct_dict(res):
    ## for date-init
    return res.json()


def postprocess_direct_dict_to_df(res):
    ## for date-init
    return pd.DataFrame(res.json())


def postprocess_mcp_status(res):
    return res.json()["body"]["content"]["completed"]


def postprocess_items_to_df(res):
    df = pd.DataFrame(res.json()["items"])
    return df


## Adhoc non-standard response postprocess
def postprocess_ren_capacity_dict_to_df(res):
    df = pd.DataFrame(res.json()["installedCapacities"])
    return df
