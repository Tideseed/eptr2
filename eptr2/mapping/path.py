path_map = {
    "mcp": {"prefix": "data", "prev": "dam"},
    "dam": {"prev": "markets"},
    "markets": {"prev": "electricity-service"},
    #### services
    "electricity-service": {"next": "version"},
    "version": {"label": "v1"},
}


def get_total_path(key: str, join_path: bool = True):
    d = path_map.get(key, None)
    if d is not None:
        total_path = [d.get("label", key)]
        if d.get("prefix", None) is not None:
            total_path = [d["prefix"]] + total_path
        if d.get("suffix", None) is not None:
            total_path = total_path + [d["suffix"]]

        if d.get("prev", None) is not None:
            total_path = get_total_path(key=d["prev"], join_path=False) + total_path
        if d.get("next", None) is not None:
            total_path += get_total_path(key=d["next"], join_path=False)

        return "/".join(total_path) if join_path else total_path
    else:
        return []
