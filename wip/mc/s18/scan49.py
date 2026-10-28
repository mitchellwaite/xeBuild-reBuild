"""scan49.py SLOT [lo hi n]: from slot's ov.json, scan mode_client:49>50 and 45>49 for P49 = f49 - 1."""
import sys, json, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\mc\s18')
import runq, analyze
from concurrent.futures import ThreadPoolExecutor
slot = sys.argv[1]
MCD = os.environ['MCD']
base = json.load(open(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\%s\slot%s\ov.json' % (MCD, slot)))
ip0, k0 = base['mode_client:49>50'], base['mode_client:45>49']
import os
K = [float(x) for x in os.environ.get('KS', '').split(',') if x] or [k0]
I = [float(x) for x in os.environ.get('IS', '').split(',') if x] or [ip0]
grid = [(i, k) for i in I for k in K]
def run(i_x):
    i, (ip, k) = i_x
    ov = dict(base); ov['mode_client:49>50'] = ip; ov['mode_client:45>49'] = k
    s = '%s_s%d' % (slot, i % 4)
    fn, out = runq.compile_(s, ov)
    o, inv, keys, named = analyze.analyze(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\%s\slot%s' % (MCD, s))
    return ip, k, keys.get(49), named.get('k48'), fn, inv
res = []
for chunk in range(0, len(grid), 4):
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(run, list(enumerate(grid))[chunk:chunk + 4]):
            print('%.3f %.3f 49=%s k48=%s fncmp=%s inv=%s' % r, flush=True)
