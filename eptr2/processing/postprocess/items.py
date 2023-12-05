import pandas as pd


def postprocess_items_to_df(res):
    df = pd.DataFrame(res.json()["items"])
    return df
