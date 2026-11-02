import threading
_m = {}; _l = threading.Lock()
def tid():
    k = threading.get_ident()
    with _l:
        if k not in _m: _m[k] = len(_m)
        return _m[k]
