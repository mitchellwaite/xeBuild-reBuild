import inspect, sys, re
def why(fake7, f, P):
    src = inspect.getsource(fake7.ok).split('\n')
    # evaluate each 'return False' line by re-running ok with that line's condition logged
    code = []
    for i, l in enumerate(src):
        code.append(l.replace('return False', 'return %d' % i) if 'return False' in l else l)
    ns = dict(fake7.__dict__)
    exec('\n'.join(code).replace('def ok(', 'def okw('), ns)
    r = ns['okw'](f, dict(P))
    return r if r is True else src[r].strip()
