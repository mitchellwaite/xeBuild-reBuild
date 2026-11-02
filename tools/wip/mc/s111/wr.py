# wr.py: 141 pushed (key K) + drop one round-3 push X (X built in round 3 instead) -> dist
import sys
from wi import *
pre, g, first = r4sim.load(sys.argv[1])
pushed = sorted({e[1] for e in pre if e[0]=='push'} | {e[2] for e in pre if e[0]=='ins' and e[1]=='next'})
for K in (-1000307, -1000306, -1000310, -7, -6):
    p2 = push141(pre, K)
    res = []
    for X in pushed + [None]:
        p3 = [e for e in p2 if not ((e[0]=='push' and e[1]==X) or (e[0]=='ins' and e[1]=='next' and e[2]==X) or (e[0]=='chg' and e[1]==X))]
        try: o = srch.sim(p3, g)
        except Exception as ex: continue
        o2 = [b for b in o if b != X]
        T2 = [b for b in srch.T if b != X]
        import difflib
        sm = difflib.SequenceMatcher(None, o2, T2, autojunk=False)
        d = len(T2) - sum(m.size for m in sm.get_matching_blocks())
        res.append((d, X))
    res.sort(key=lambda r:(r[0], str(r[1]))); print(K, res[:8])
