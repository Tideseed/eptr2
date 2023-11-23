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
    }
    return d.get(key, key)


def get_required_parameters(key):
    d = {
        "mcp": ["start_date", "end_date"],
        "smp": ["start_date", "end_date"],
        "da-volume": ["start_date", "end_date"],
        "pi-offer": ["start_date", "end_date"],
        "pi-bid": ["start_date", "end_date"],
        "dam-bid": ["start_date", "end_date"],
        "dam-offer": ["start_date", "end_date"],
        "supply-demand": ["date_time"],
        "dam-clearing": ["date_time"],
        "dam-clearing-org-list": ["period"],
        "dam-block-bid": ["start_date", "end_date"],
        "dam-block-offer": ["start_date", "end_date"],
        "mcp-smp-imb": ["start_date", "end_date"],
        "bpm-orders-w-avg": ["date_time"],
    }
    return d.get(key, [])
