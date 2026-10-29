"""RA-swap probe: python rap.py base.json key=val[,key=val] ...  (each arg one variant, parallel 4)"""
import json, sys, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import run
base = json.load(open(sys.argv[1]))
def one(a):
    i, s = a
    x = dict(base)
    for kv in s.split(','):
        k, v = kv.split('='); x[k] = float(v)
    f, inv, pre, _ = run.run('r%d' % (i % 4), x)
    d = open(run.ROOT + r'\build\mcsp\slotr%d\fdo.diff' % (i % 4)).read()
    return '%s fncmp %d inv %d pre %d swap %s' % (s, f, inv, pre, '+lea edx,[1+ecx]' in d)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(one, enumerate(sys.argv[2:])): print(r, flush=True)
