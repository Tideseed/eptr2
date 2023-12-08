import pandas as pd


def postprocess_direct_dict(res):
    ## for date-init
    return res.json()


def postprocess_mcp_status(res):
    return res.json()["body"]["content"]["completed"]


def postprocess_items_to_df(res):
    df = pd.DataFrame(res.json()["items"])
    return df
