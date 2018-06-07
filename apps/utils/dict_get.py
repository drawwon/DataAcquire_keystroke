def dict_get(d, *args):
    """Get the values corresponding to the given keys in the provided dict."""
    return [d[arg] for arg in args]
