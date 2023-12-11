from eptr2.processing.postprocess.items import (
    postprocess_items_to_df,
    postprocess_mcp_status,
    postprocess_direct_dict,
    postprocess_direct_dict_to_df,
    postprocess_ren_capacity_dict_to_df,
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
        "smp-dir",
        "bpm-up",
        "bpm-down",
        "mcp",
        "wap",
        "idm-qty",
        "idm-mm-bid",
        "idm-mm-offer",
        "idm-mm-matching",
        "idm-volume",
        "idm-log",
        "idm-ob-qty",
        "bi-long",
        "bi-short",
        "bi-euas",
        "imb-qty",
        "imb-vol",
        "imb-qty-g",
        "imb-org-list",
        "interim-mcp",
        "mcp-smp-imb",
        "bpm-orders-w-avg",
        "market-participants",
        "market-participants-organization-list",
        "kgup",
        "kudup",
        "eak",
        "gen-org",
        "gen-uevcb",
        "rt-gen",
        "pp-list",
        "lic-pp-list",
        "load-plan",
        "rt-cons",
        "uecm",
        "st-uecm",
        "su-uecm",
        "uevm",
        "wind-forecast",
        "ren-rt-gen",
        "ren-ul-gen",
        "ren-ul-cost",
        "ren-unit-cost",
        "ren-income",
        "ren-total-cost",
        "ren-participant-list",
        "ren-uevm",
        "ren-lic-cost",
        "zero-balance",
        "iskk",
        "congestion-cost",
        "eic-x-list",
        "eic-w-list",
    ]:
        return postprocess_items_to_df

    elif key in ["interim-mcp-status"]:
        return postprocess_mcp_status

    elif key in ["date-init"]:
        return postprocess_direct_dict

    elif key in ["ren-pp-list"]:
        return postprocess_direct_dict_to_df

    elif key in ["ren-capacity"]:
        return postprocess_ren_capacity_dict_to_df
    else:
        raise Exception("Postprocess function is not defined for this call.")
