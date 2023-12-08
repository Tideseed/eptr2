from eptr2.processing.postprocess.items import (
    postprocess_items_to_df,
    postprocess_mcp_status,
    postprocess_direct_dict,
)


def get_postprocess_function(key):
    if key in [
        "dam-volume",
        "pi-offer",
        "pi-bid",
        "supply-demand",
        "dam-bid",
        "dam-offer",
        "dam-block-bid",
        "dam-block-offer",
        "dam-flexible-bid",
        "dam-flexible-offer",
        "dam-flexible-matching",
        "dam-clearing",
        "dam-clearing-org-list",
        "dam-diff",
        "smp",
        "mcp",
        "wap",
        "idm-qty",
        "idm-mm-bid",
        "idm-mm-offer",
        "idm-mm-matching",
        "idm-volume",
        "idm-log",
        "idm-ob-qty",
        "interim-mcp",
        "mcp-smp-imb",
        "bpm-orders-w-avg",
    ]:
        return postprocess_items_to_df

    elif key in ["interim-mcp-status"]:
        return postprocess_mcp_status

    elif key in ["date-init"]:
        return postprocess_direct_dict

    else:
        raise Exception("Postprocess function is not defined for this call.")
