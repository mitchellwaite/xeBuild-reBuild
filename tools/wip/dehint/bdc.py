"""python tools/wip/dehint/bdc.py a,b c,d,e ... : score each comma-separated set of tricks off, in parallel"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdtricks
b = bdtricks.base()
sets = [s.split(',') for s in sys.argv[1:]]
with bdtricks.pool() as p:
    rs = list(p.map(lambda s: bdtricks.score(s, b), sets))
for s, r in zip(sets, rs):
    print('%-40s %s' % (','.join(s), bdlib.fmt(r)[:240]))
