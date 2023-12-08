def get_param_label(key):
    d = {
        "start_date": {
            "label": "startDate",
        },
        "end_date": {
            "label": "endDate",
        },
        "date_time": {"label": "date"},
        "period": {"label": "period"},
        "org_id": {"label": "organizationId"},
    }
    return d.get(key, key)


def get_required_parameters(key):
    d = {
        "mcp": ["start_date", "end_date"],
        "interim-mcp": ["start_date", "end_date"],
        "interim-mcp-status": [],
        "date-init": [],
        "smp": ["start_date", "end_date"],
        "dam-volume": ["start_date", "end_date"],
        "pi-offer": ["start_date", "end_date"],
        "pi-bid": ["start_date", "end_date"],
        "dam-bid": ["start_date", "end_date"],
        "dam-offer": ["start_date", "end_date"],
        "supply-demand": ["date_time"],
        "dam-clearing": ["start_date", "end_date"],
        "dam-clearing-org-list": ["period"],
        "dam-block-bid": ["start_date", "end_date"],
        "dam-block-offer": ["start_date", "end_date"],
        "dam-flexible-matching": ["start_date", "end_date"],
        "dam-flexible-bid": ["start_date", "end_date"],
        "dam-flexible-offer": ["start_date", "end_date"],
        "dam-diff": ["start_date", "end_date"],
        "mcp-smp-imb": ["start_date", "end_date"],
        "bpm-orders-w-avg": ["date_time"],
    }
    ## UPDATE: As a precaution every call should have an input parameter
    return d[key]


def get_optional_parameters(key):
    d = {"dam-clearing": ["org_id"]}

    return d.get(key, [])
