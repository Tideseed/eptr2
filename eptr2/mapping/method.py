def get_method(key):
    post_methods = ["mcp"]

    if key in post_methods:
        return "POST"
    else:
        return "GET"
